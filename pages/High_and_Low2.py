import streamlit as st
import json
from pathlib import Path
import random as rd

# ----Pathを指定して JSONファイルを読み込み ----
json_path = Path(__file__).parent.parent / "sample_data" / "highandlow_round3.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)
if ["deck"] not in st.session_state:
    st.session_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
if ["round_data"] not in st.session_state:
    st.session_state["round_data"] = {
        "round": 1,
        "wallet": 100,
        "win_count": 0,
        "lose_count": 0,
        "in": 0,
        "out": 0,
        "all": 0
    }
if ["round_counter"] not in st.session_state:
    st.session_state["round_counter"] = 1
if ["wallet"] not in st.session_state:
    st.session_state["wallet"] = st.session_state["wallet"]
if ["bet"] not in st.session_state:
    st.session_state = 1
if ["f_number"] not in st.session_state:
    st.session_state = 0
if ["b_number"] not in st.session_state:
    st.session_state = 0
if ["judge"] not in st.session_state:
    st.session_state = 0  #後のカードが大きければ0、前のカードが大きければ1、同じだったら2
if ["highlow"] not in st.session_state:
    st.session_state = 0  #highの時は0、lowの時は1
if ["winlose"] not in st.session_state:
    st.session_state = 0  #勝利の時は0、敗北の時は1、引き分けの時は2

def betting(a, b):  #aにはwallet、bにはbetを入力
    min_bet = 1
    max_bet = a
    b = st.number_input("掛け金を入力してください", min_value = min_bet, max_value = max_bet, value = 10, format = "%.0f")
    st.write(f"掛け金：{b}")

def output_number(a, b, c):  #aにはdeck、bにはf_number、cにはb_numberを入力
    b = rd.choice(a)
    a.remove(b)
    c = rd.choice(a)
    a.remove(c)

def judge(a, b, c):  #aにはf_number、bにはb_number、cにはjudgeを入力
    if a < b:
        c = 0
    elif a > b:
        c = 1
    else:
        c = 2

def input_highlow(a, b):  #aにはhighlow、bにはplayer_shoiceを入力
    st.write("あなたの予想は？")
    if st.button("High"):
        a = 0
    elif st.button("Low"):
        a = 1

def winlose(a, b, c):  #aにはjudge、bにはhighlow、cにはwinloseを入力
    if a == b:
        c = 0
    elif a == 2:
        c = 2
    else:
        c = 1

def result(a, b, c):  #aにはwinlose、bにはbet、cにはwalletを入力
    if a == 0:
        st.success("You Win!!")
        c += b
        st.write(f"あなたの所持チップは{c}枚まで増えた！")
    elif a == 1:
        st.error("You Lose!!")
        c -= b
        st.write(f"あなたの所持チップは{c}枚まで減った！")
    else:
        st.warning("Draw!!")
        st.write(f"あなたの所持チップは{c}枚のまま変わらなかった！")

def judge_continue(a, b):
    pass

def game_continue(a, b, c, d, e, f, g):  #ここでwallet以外の全てのデータをリセットする。aがround_counterであること以外は順不同
    if st.button("Next game"):
        a += 1
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        g = 0