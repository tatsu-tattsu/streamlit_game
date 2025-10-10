import streamlit as st
import random

# ===============================
# 初期化処理（New Game時にも呼ぶ）
# ===============================
def initialize_game():
    st.session_state["deck"] = list(range(1, 14))
    random.shuffle(st.session_state["deck"])
    st.session_state["wallet"] = 100
    st.session_state["bet"] = 10
    st.session_state["round_counter"] = 1
    st.session_state["base_card"] = None
    st.session_state["result_card"] = None
    st.session_state["player_choice"] = None
    st.session_state["round_history"] = []
    st.session_state["game_over"] = False
    st.session_state["phase"] = "start"  # ← フェーズ管理追加

# ゲーム開始時に初期化
if "phase" not in st.session_state:
    initialize_game()

# ===============================
# カードを1枚引く
# ===============================
def draw_card():
    if st.session_state["deck"]:
        return st.session_state["deck"].pop(0)
    return None

# ===============================
# フェーズ①：ベースカードを引く
# ===============================
def draw_base_card():
    st.session_state["base_card"] = draw_card()
    st.session_state["phase"] = "declare"

# ===============================
# フェーズ②：High/Low 宣言
# ===============================
def declare(choice):
    st.session_state["player_choice"] = choice
    st.session_state["result_card"] = draw_card()

    base = st.session_state["base_card"]
    result = st.session_state["result_card"]
    bet = st.session_state["bet"]
    wallet = st.session_state["wallet"]

    if choice == "High" and result > base:
        outcome = "WIN"
        wallet += bet
    elif choice == "Low" and result < base:
        outcome = "WIN"
        wallet += bet
    elif result == base:
        outcome = "DRAW"
    else:
        outcome = "LOSE"
        wallet -= bet

    st.session_state["wallet"] = wallet
    st.session_state["round_history"].append({
        "round": st.session_state["round_counter"],
        "base": base,
        "result": result,
        "choice": choice,
        "outcome": outcome,
        "wallet_after": wallet
    })

    # 🧨 ここを追加 → walletが0なら即ゲームオーバー
    if wallet <= 0:
        st.session_state["game_over"] = True
        st.session_state["phase"] = "end"
    else:
        st.session_state["phase"] = "result"


# ===============================
# フェーズ③：次ラウンドへ
# ===============================
def next_round():
    st.session_state["round_counter"] += 1

    # 終了条件チェック
    if st.session_state["round_counter"] > 3 or st.session_state["wallet"] <= 0 or not st.session_state["deck"]:
        st.session_state["game_over"] = True
        st.session_state["phase"] = "end"
    else:
        st.session_state["base_card"] = None
        st.session_state["result_card"] = None
        st.session_state["player_choice"] = None
        st.session_state["bet"] = 10  # ←★ ラウンド移動時にデフォルトベット額をリセット
        st.session_state["phase"] = "start"


# ===============================
# フェーズ④：New Game
# ===============================
def new_game():
    initialize_game()

# ===============================
# UI描画
# ===============================
st.title("High & Low カードゲーム")

# 💥 New Game ボタン → 完全リセット
if st.button("New Game"):
    new_game()

# 終了時
if st.session_state["game_over"]:
    st.header("ゲーム終了！")
    wins = sum(1 for r in st.session_state["round_history"] if r["outcome"] == "WIN")
    draws = sum(1 for r in st.session_state["round_history"] if r["outcome"] == "DRAW")
    losses = sum(1 for r in st.session_state["round_history"] if r["outcome"] == "LOSE")
    st.write(f"勝ち：{wins} 回 / 負け：{losses} 回 / 引き分け：{draws} 回")
    st.write(f"最終チップ：{st.session_state['wallet']}")
    st.write("**勝負履歴**")
    for h in st.session_state["round_history"]:
        st.write(
            f"Round {h['round']}: ベース {h['base']} / 結果 {h['result']} / 宣言 {h['choice']} / "
            f"勝敗 {h['outcome']} / 所持チップ {h['wallet_after']}"
        )

# ===============================
# フェーズごとのUI制御
# ===============================
else:
    st.write(f"### Round {st.session_state['round_counter']}")
    st.write(f"所持チップ：{st.session_state['wallet']}")

    # ベット額設定
    st.session_state["bet"] = st.number_input(
        "ベット額",
        min_value=1,
        max_value=st.session_state["wallet"],
        value=1
    )

    # フェーズ① ベースカード
    if st.session_state["phase"] == "start":
        if st.button("カードを引く", on_click=draw_base_card):
            pass

    # フェーズ② 宣言
    elif st.session_state["phase"] == "declare":
        st.write(f"ベースカード： {st.session_state['base_card']}")
        col1, col2 = st.columns(2)
        with col1:
            st.button("High", on_click=declare, args=("High",))
        with col2:
            st.button("Low", on_click=declare, args=("Low",))

    # フェーズ③ 結果
    elif st.session_state["phase"] == "result":
        last = st.session_state["round_history"][-1]
        st.write(f"ベースカード： {last['base']}")
        st.write(f"結果カード： {last['result']}")
        st.write(f"結果： {last['outcome']}")
        st.button("Next Round", on_click=next_round)
