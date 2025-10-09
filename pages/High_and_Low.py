import streamlit as st
import random as rd

st.title("High and Low Game!")

st.write("数字を予想して、HighかLowか当ててください")
st.write("ルール")
st.write("" \
"・カードは１〜９までの数字が２枚ずつあります" \
"・どのカードも引く確率は同じです")

f_number = 0
b_number = 0
judge = 0
f_number = rd.randint(1 , 10)
b_number = rd.randint(1 , 10)
st.write(f"１枚目の数字：{f_number}")
if f_number > b_number:
    judge = 0
elif f_number == b_number:
    judge = 1
else:
    judge = 2
next1 = False
statu = 0
if st.button("High"):
    statu = 1
    next1 = True
if st.button("Low"):
    statu = 2
    next1 = True
match(statu):
    case 1:
        st.write(f"２枚目の数字：{b_number}")
        if judge == 0:
            st.error("You Lose")
        elif judge == 1:
            st.info("Draw")
        else:
            st.success("You Win")
    case 2:
        st.write(f"２枚目の数字：{b_number}")
        if judge == 2:
            st.error("You Lose")
        elif judge == 1:
            st.info("Draw")
        else:
            st.success("You Win")