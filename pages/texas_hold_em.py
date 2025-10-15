"""
ここにはルールを作るための下書きが残してあります
・使用するのは52枚のトランプ
・トランプのデッキは二重多層構造のlistであり、
　一層目の中に52枚のカード分のリストが存在し、二層目にカードの数字と絵柄が格納されている
・大きな構造はHigh and Lowを利用(phase,newgameなどのシステム)
・5ラウンド制
・常に"New Game" ボタンは表示しておく(流用)
・phase"start"の時点で、画面上には所持チップの総数とベット額を決める入力欄、
　"ゲームを始める"ボタンが存在する(High and Lowを流用)
・ゲームを始めるを押すと、プレイヤーとオーナーにデッキからカードが２枚づつ渡される。
　この時、プレイヤーには自分のカードの絵柄と数字が開示される。そして、phaseが"first"に変化する

"""

import streamlit as st
import random
from collections import Counter

# ===============================
# 初期化処理（New Game時にも呼ぶ）
# ===============================
def initialize_game():
    st.session_state["deck"] = [
        [i, suit] for suit in ["spade", "heart", "clover", "daia"] for i in range(1, 14)
    ]
    random.shuffle(st.session_state["deck"])
    st.session_state["wallet"] = 100
    st.session_state["bet"] = 10
    st.session_state["round_counter"] = 1
    # 各ハンドは「カードを格納するリスト（0番にカードが入る想定）」にする
    st.session_state["player_card1"] = []  # will contain one card: [value, suit]
    st.session_state["player_card2"] = []
    st.session_state["owner_card1"] = []
    st.session_state["owner_card2"] = []
    st.session_state["open_card1"] = []
    st.session_state["open_card2"] = []
    st.session_state["open_card3"] = []
    st.session_state["open_card4"] = []
    st.session_state["open_card5"] = []
    st.session_state["player_choice1"] = None
    st.session_state["player_choice2"] = None
    st.session_state["player_choice3"] = None
    st.session_state["round_history"] = []
    st.session_state["game_over"] = False
    st.session_state["phase"] = "start"  # フェーズ管理
    st.session_state["allin"] = False
    st.session_state["fold"] = False
    st.session_state["player_card_list"] = None
    st.session_state["owner_card_list"] = None

# 初期化チェック
if "phase" not in st.session_state:
    initialize_game()

# ===============================
# カードを1枚引く
# ===============================
def draw_card():
    if st.session_state["deck"]:
        return st.session_state["deck"].pop(0)  # 先頭から引く（小デッキなので十分）
    return None

# ===============================
# フェーズ①：playerとownerがカードを引き、５枚のオープンカードが引かれる
# ===============================
def draw_base_card():
    # 引くカードを個別に取得してそれぞれリストにappendする（各handは1枚格納のリスト）
    a = draw_card(); b = draw_card(); c = draw_card(); d = draw_card()
    e = draw_card(); f = draw_card(); g = draw_card(); h = draw_card(); i = draw_card()
    st.session_state["player_card1"].append(a)
    st.session_state["player_card2"].append(b)
    st.session_state["owner_card1"].append(c)
    st.session_state["owner_card2"].append(d)
    st.session_state["open_card1"].append(e)
    st.session_state["open_card2"].append(f)
    st.session_state["open_card3"].append(g)
    st.session_state["open_card4"].append(h)
    st.session_state["open_card5"].append(i)
    st.session_state["phase"] = "firstopen"  # タイプミス修正

# ===============================
# フェーズ②：firstopen
# ===============================
def firstopen(choice):
    st.session_state["player_choice1"] = choice
    bet = st.session_state["bet"]
    wallet = st.session_state["wallet"]
    # bet を2倍にできるかどうか（十分な所持があるか）を判定
    if choice == "reise":
        if bet * 2 <= wallet:
            st.session_state["bet"] = bet * 2
            st.session_state["phase"] = "secondopen"
        else:
            # insufficient -> allin to wallet
            st.session_state["bet"] = wallet
            st.session_state["allin"] = True
            st.session_state["phase"] = "secondopen"
    elif choice == "allin":
        st.session_state["bet"] = wallet
        st.session_state["allin"] = True
        st.session_state["phase"] = "secondopen"
    elif choice == "check":
        st.session_state["phase"] = "secondopen"
    else:  # fold
        st.session_state["fold"] = True
        st.session_state["phase"] = "calculate"

# ===============================
# フェーズ③：secondopen
# ===============================
def secondopen(choice):
    st.session_state["player_choice2"] = choice
    bet = st.session_state["bet"]
    wallet = st.session_state["wallet"]
    if choice == "reise":
        if bet * 2 <= wallet:
            st.session_state["bet"] = bet * 2
            st.session_state["phase"] = "thirdopen"
        else:
            st.session_state["bet"] = wallet
            st.session_state["allin"] = True
            st.session_state["phase"] = "thirdopen"
    elif choice == "allin":
        st.session_state["bet"] = wallet
        st.session_state["allin"] = True
        st.session_state["phase"] = "thirdopen"
    elif choice == "check":
        st.session_state["phase"] = "thirdopen"
    else:  # fold
        st.session_state["fold"] = True
        st.session_state["phase"] = "calculate"

# ===============================
# フェーズ④：thirdopen
# ===============================
def thirdopen(choice):
    st.session_state["player_choice3"] = choice
    bet = st.session_state["bet"]
    wallet = st.session_state["wallet"]
    if choice == "reise":
        if bet * 2 <= wallet:
            st.session_state["bet"] = bet * 2
            st.session_state["phase"] = "calculate"
        else:
            st.session_state["bet"] = wallet
            st.session_state["allin"] = True
            st.session_state["phase"] = "calculate"
    elif choice == "allin":
        st.session_state["bet"] = wallet
        st.session_state["allin"] = True
        st.session_state["phase"] = "calculate"
    elif choice == "check":
        # check の場合はそのまま calculate に遷移（場は全部見える想定）
        st.session_state["phase"] = "calculate"
    else:  # fold
        st.session_state["fold"] = True
        st.session_state["phase"] = "calculate"

# ===============================
# フェーズ⑤：calculate（勝敗判定）
# ===============================
def calculate():
    # 現在ウォレットをローカルに取り出す（計算後に保存）
    wallet = st.session_state["wallet"]
    bet = st.session_state["bet"]

    # player_card_list / owner_card_list を構築（視認用）
    st.session_state["player_card_list"] = [
        st.session_state["player_card1"][0] if st.session_state["player_card1"] else None,
        st.session_state["player_card2"][0] if st.session_state["player_card2"] else None,
        st.session_state["open_card1"][0] if st.session_state["open_card1"] else None,
        st.session_state["open_card2"][0] if st.session_state["open_card2"] else None,
        st.session_state["open_card3"][0] if st.session_state["open_card3"] else None,
        st.session_state["open_card4"][0] if st.session_state["open_card4"] else None,
        st.session_state["open_card5"][0] if st.session_state["open_card5"] else None,
    ]

    player_card_number = [c[0] for c in st.session_state["player_card_list"] if c is not None]

    # カウント情報（多重度）
    counts_p = Counter(player_card_number)
    player_card_len1 = counts_p.most_common(1)[0][1] if counts_p else 0
    player_card_len2 = counts_p.most_common(2)[1][1] if len(counts_p) >= 2 else 0
    player_card_number_common1 = counts_p.most_common(1)[0][0] if counts_p else 0
    player_card_number_common2 = counts_p.most_common(2)[1][0] if len(counts_p) >= 2 else 0

    # ストレート判定（ユニーク化してソート）
    player_card_number_sorted = sorted(set(player_card_number))
    player_card_number_max = player_card_number_sorted[-1] if player_card_number_sorted else 0
    player_straight = False
    player_max_val = 0
    if len(player_card_number_sorted) >= 5:
        for i in range(len(player_card_number_sorted) - 4):
            if player_card_number_sorted[i+4] - player_card_number_sorted[i] == 4:
                player_straight = True
                player_max_val = player_card_number_sorted[i+4]

    player_card_mark = [
        st.session_state["player_card1"][0][1] if st.session_state["player_card1"] else None,
        st.session_state["player_card2"][0][1] if st.session_state["player_card2"] else None,
        st.session_state["open_card1"][0][1] if st.session_state["open_card1"] else None,
        st.session_state["open_card2"][0][1] if st.session_state["open_card2"] else None,
        st.session_state["open_card3"][0][1] if st.session_state["open_card3"] else None,
        st.session_state["open_card4"][0][1] if st.session_state["open_card4"] else None,
        st.session_state["open_card5"][0][1] if st.session_state["open_card5"] else None,
    ]
    # マークの最多数
    marks_p = [m for m in player_card_mark if m is not None]
    player_mark_len = Counter(marks_p).most_common(1)[0][1] if marks_p else 0

    # プレイヤーポイント決定
    player_point = None
    # フラッシュ（5枚） + ストレート -> ストレートフラッシュ
    if player_mark_len >= 5 and player_straight:
        player_point = [9, player_max_val]
    elif player_card_len1 == 4:
        player_point = [8, player_card_number_common1, player_card_number_max if 'player_card_number_max' in locals() else player_card_number_max]
    elif player_card_len1 == 3 and player_card_len2 == 2:
        player_point = [7, player_card_number_common1, player_card_number_common2]
    elif player_mark_len >= 5:
        player_point = [6, player_card_number_max]
    elif player_straight:
        player_point = [5, player_max_val]
    elif player_card_len1 == 3:
        player_point = [4, player_card_number_common1, player_card_number_max]
    elif player_card_len1 == 2 and player_card_len2 == 2:
        player_point = [3, player_card_number_common1, player_card_number_common2, player_card_number_max]
    elif player_card_len1 == 2:
        player_point = [2, player_card_number_common1, player_card_number_max]
    else:
        player_point = [1, player_card_number_max]

    # ---------------- owner 側 ----------------
    st.session_state["owner_card_list"] = [
        st.session_state["owner_card1"][0] if st.session_state["owner_card1"] else None,
        st.session_state["owner_card2"][0] if st.session_state["owner_card2"] else None,
        st.session_state["open_card1"][0] if st.session_state["open_card1"] else None,
        st.session_state["open_card2"][0] if st.session_state["open_card2"] else None,
        st.session_state["open_card3"][0] if st.session_state["open_card3"] else None,
        st.session_state["open_card4"][0] if st.session_state["open_card4"] else None,
        st.session_state["open_card5"][0] if st.session_state["open_card5"] else None,
    ]
    owner_card_number = [c[0] for c in st.session_state["owner_card_list"] if c is not None]

    counts_o = Counter(owner_card_number)
    owner_card_len1 = counts_o.most_common(1)[0][1] if counts_o else 0
    owner_card_len2 = counts_o.most_common(2)[1][1] if len(counts_o) >= 2 else 0
    owner_card_number_common1 = counts_o.most_common(1)[0][0] if counts_o else 0
    owner_card_number_common2 = counts_o.most_common(2)[1][0] if len(counts_o) >= 2 else 0

    owner_card_number_sorted = sorted(set(owner_card_number))
    owner_card_number_max = owner_card_number_sorted[-1] if owner_card_number_sorted else 0
    owner_straight = False
    owner_max_val = 0
    if len(owner_card_number_sorted) >= 5:
        for i in range(len(owner_card_number_sorted) - 4):
            if owner_card_number_sorted[i+4] - owner_card_number_sorted[i] == 4:
                owner_straight = True
                owner_max_val = owner_card_number_sorted[i+4]

    owner_card_mark = [
        st.session_state["owner_card1"][0][1] if st.session_state["owner_card1"] else None,
        st.session_state["owner_card2"][0][1] if st.session_state["owner_card2"] else None,
        st.session_state["open_card1"][0][1] if st.session_state["open_card1"] else None,
        st.session_state["open_card2"][0][1] if st.session_state["open_card2"] else None,
        st.session_state["open_card3"][0][1] if st.session_state["open_card3"] else None,
        st.session_state["open_card4"][0][1] if st.session_state["open_card4"] else None,
        st.session_state["open_card5"][0][1] if st.session_state["open_card5"] else None,
    ]
    marks_o = [m for m in owner_card_mark if m is not None]
    owner_mark_len = Counter(marks_o).most_common(1)[0][1] if marks_o else 0

    owner_point = None
    if owner_mark_len >= 5 and owner_straight:
        owner_point = [9, owner_max_val]
    elif owner_card_len1 == 4:
        owner_point = [8, owner_card_number_common1, owner_card_number_max]
    elif owner_card_len1 == 3 and owner_card_len2 == 2:
        owner_point = [7, owner_card_number_common1, owner_card_number_common2]
    elif owner_mark_len >= 5:
        owner_point = [6, owner_card_number_max]
    elif owner_straight:
        owner_point = [5, owner_max_val]
    elif owner_card_len1 == 3:
        owner_point = [4, owner_card_number_common1, owner_card_number_max]
    elif owner_card_len1 == 2 and owner_card_len2 == 2:
        owner_point = [3, owner_card_number_common1, owner_card_number_common2, owner_card_number_max]
    elif owner_card_len1 == 2:
        owner_point = [2, owner_card_number_common1, owner_card_number_max]
    else:
        owner_point = [1, owner_card_number_max]

    # ---------------- 勝敗判定 ----------------
    # fold の場合は player 負け（所有チップは減る）
    if st.session_state["fold"]:
        outcome = "LOSE"
        wallet -= bet
    else:
        # 比較のために要素長を保証（不足要素は0で埋める）
        def normalize_point(pt):
            # pt is list like [rank, key1, key2, ...]
            return pt + [0] * (4 - len(pt))
        p = normalize_point(player_point)
        o = normalize_point(owner_point)

        if p[0] > o[0]:
            outcome = "WIN"; wallet += bet
        elif p[0] < o[0]:
            outcome = "LOSE"; wallet -= bet
        else:  # same rank -> 比較
            if p[1] > o[1]:
                outcome = "WIN"; wallet += bet
            elif p[1] < o[1]:
                outcome = "LOSE"; wallet -= bet
            else:
                if p[2] > o[2]:
                    outcome = "WIN"; wallet += bet
                elif p[2] < o[2]:
                    outcome = "LOSE"; wallet -= bet
                else:
                    outcome = "DRAW"  # 完全同値

    # 保存と履歴登録
    st.session_state["wallet"] = wallet
    st.session_state["round_history"].append({
        "round": st.session_state["round_counter"],
        "outcome": outcome,
        "wallet_after": wallet
    })

    if wallet <= 0 or st.session_state["round_counter"] >= 5:
        st.session_state["game_over"] = True
        st.session_state["phase"] = "end"
    else:
        st.session_state["phase"] = "result"

# ===============================
# フェーズ⑥：次ラウンドへ
# ===============================
def next_round():
    st.session_state["round_counter"] += 1

    # 終了条件チェック
    if st.session_state["round_counter"] > 5 or st.session_state["wallet"] <= 0 or not st.session_state["deck"]:
        st.session_state["game_over"] = True
        st.session_state["phase"] = "end"
        return

    # ハンドやオープンカードを空に戻す（次ラウンド準備）
    st.session_state["player_card1"] = []
    st.session_state["player_card2"] = []
    st.session_state["owner_card1"] = []
    st.session_state["owner_card2"] = []
    st.session_state["open_card1"] = []
    st.session_state["open_card2"] = []
    st.session_state["open_card3"] = []
    st.session_state["open_card4"] = []
    st.session_state["open_card5"] = []
    st.session_state["player_choice1"] = None
    st.session_state["player_choice2"] = None
    st.session_state["player_choice3"] = None
    st.session_state["bet"] = 1  # ラウンド移動時にデフォルトベット額をリセット
    st.session_state["fold"] = False
    st.session_state["allin"] = False
    st.session_state["phase"] = "start"

# ===============================
# フェーズ⑦：New Game
# ===============================
def new_game():
    initialize_game()

# ===============================
# UI描画
# ===============================
st.title("Texas Hold'em")

# New Game ボタン
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
        st.write(f"Round {h['round']}: 勝敗 {h['outcome']} / 所持チップ {h['wallet_after']}")
else:
    st.write(f"### Round {st.session_state['round_counter']}")
    st.write(f"所持チップ：{st.session_state['wallet']}")

    # ベット額設定
    st.session_state["bet"] = st.number_input(
        "ベット額",
        min_value=1,
        max_value=st.session_state["wallet"],
        value=st.session_state["bet"]
    )

    # フェーズ① ベースカード
    if st.session_state["phase"] == "start":
        if st.button("ゲームを始める", on_click=draw_base_card):
            pass

    # フェーズ② firstopen
    elif st.session_state["phase"] == "firstopen":
        # カード表示（存在チェックして表示）
        p1 = st.session_state["player_card1"][0] if st.session_state["player_card1"] else None
        p2 = st.session_state["player_card2"][0] if st.session_state["player_card2"] else None
        oc1 = st.session_state["open_card1"][0] if st.session_state["open_card1"] else None
        oc2 = st.session_state["open_card2"][0] if st.session_state["open_card2"] else None
        oc3 = st.session_state["open_card3"][0] if st.session_state["open_card3"] else None

        st.write(f"あなたの手札： {p1[1]} の {p1[0]} と {p2[1]} の {p2[0]}")
        st.write(f"場のカード： {oc1[1]}の{oc1[0]} , {oc2[1]}の{oc2[0]} , {oc3[1]}の{oc3[0]}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("reise", on_click=firstopen, args=("reise",))
        with col2:
            st.button("check", on_click=firstopen, args=("check",))
        with col3:
            st.button("fold", on_click=firstopen, args=("fold",))
        with col4:
            st.button("allin", on_click=firstopen, args=("allin",))

    # フェーズ③ secondopen
    elif st.session_state["phase"] == "secondopen":
        p1 = st.session_state["player_card1"][0] if st.session_state["player_card1"] else None
        p2 = st.session_state["player_card2"][0] if st.session_state["player_card2"] else None
        oc1 = st.session_state["open_card1"][0] if st.session_state["open_card1"] else None
        oc2 = st.session_state["open_card2"][0] if st.session_state["open_card2"] else None
        oc3 = st.session_state["open_card3"][0] if st.session_state["open_card3"] else None
        oc4 = st.session_state["open_card4"][0] if st.session_state["open_card4"] else None

        st.write(f"あなたの手札： {p1[1]} の {p1[0]} と {p2[1]} の {p2[0]}")
        st.write(f"場のカード： {oc1[1]}の{oc1[0]} , {oc2[1]}の{oc2[0]} , {oc3[1]}の{oc3[0]} , {oc4[1]}の{oc4[0]}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("reise", on_click=secondopen, args=("reise",))
        with col2:
            st.button("check", on_click=secondopen, args=("check",))
        with col3:
            st.button("fold", on_click=secondopen, args=("fold",))
        with col4:
            st.button("allin", on_click=secondopen, args=("allin",))

    # フェーズ④ thirdopen
    elif st.session_state["phase"] == "thirdopen":
        p1 = st.session_state["player_card1"][0] if st.session_state["player_card1"] else None
        p2 = st.session_state["player_card2"][0] if st.session_state["player_card2"] else None
        oc1 = st.session_state["open_card1"][0] if st.session_state["open_card1"] else None
        oc2 = st.session_state["open_card2"][0] if st.session_state["open_card2"] else None
        oc3 = st.session_state["open_card3"][0] if st.session_state["open_card3"] else None
        oc4 = st.session_state["open_card4"][0] if st.session_state["open_card4"] else None
        oc5 = st.session_state["open_card5"][0] if st.session_state["open_card5"] else None

        st.write(f"あなたの手札： {p1[1]} の {p1[0]} と {p2[1]} の {p2[0]}")
        st.write(f"場のカード： {oc1[1]}の{oc1[0]} , {oc2[1]}の{oc2[0]} , {oc3[1]}の{oc3[0]} , {oc4[1]}の{oc4[0]} , {oc5[1]}の{oc5[0]}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("reise", on_click=thirdopen, args=("reise",))
        with col2:
            st.button("check", on_click=thirdopen, args=("check",))
        with col3:
            st.button("fold", on_click=thirdopen, args=("fold",))
        with col4:
            st.button("allin", on_click=thirdopen, args=("allin",))

    # フェーズ⑤ 結果
    elif st.session_state["phase"] == "result":
        last = st.session_state["round_history"][-1]
        st.write("ベースカード（player）:", st.session_state["player_card_list"])
        st.write("ベースカード（owner）:", st.session_state["owner_card_list"])
        st.write(f"結果： {last['outcome']}")
        st.button("Next Round", on_click=next_round)

    # fallback: すぐ計算に進める場合
    elif st.session_state["phase"] == "calculate":
        # 計算を実行して結果画面へ
        calculate()
        st.experimental_rerun()
