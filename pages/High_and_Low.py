import streamlit as st
import random as rd

st.title("High and Low Game!")

st.write("数字を予想して、HighかLowか当ててください")
st.write("ルール")
st.write("" \
"・カードは１〜９までの数字が２枚ずつあります" \
"・どのカードも引く確率は同じです")

def judge(a ,b):
    if a < b:
        return 0
    elif a > b:
        return 1
    else:
        return 2

def winlose(a, b):
    if a == 2:
        return st.info("Draw")
    elif a == b:
        return st.success("You Win")
    else:
        return st.error("You Lose")
    
def reset(a):
    if st.button("reset"):
        a = 3

def highandlow():
    f_number = 0
    b_number = 0
    judged = 0
    f_number = rd.randint(1 , 10)
    b_number = rd.randint(1 , 10)
    st.write(f"１枚目の数字：{f_number}")
    judged = judge(f_number, b_number)
    statu = 3
    if st.button("High"):
        statu = 0
    elif st.button("Low"):
        statu = 1
    else:
        statu = 3
    if statu != 3:
        st.write(f"２枚目の数字：{b_number}")
        winlose(judged, statu)
        reset(statu)

highandlow()