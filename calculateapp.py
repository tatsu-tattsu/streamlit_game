import streamlit as st

st.title("最小公倍数判定")
st.write("任意の整数二つの最小公倍数を判定します")
number1 = int(st.number_input("一つ目の数字を入力してください", format="%.0f"))
number2 = int(st.number_input("二つ目の数字を入力してください", format="%.0f"))
bigger = 0
#st.write(number1)
#st.write(number2)
if number1 >= number2:
    bigger = int(number2)
else:
    bigger = int(number1)
#st.write(bigger)
multiple1 = 0
multiple2 = 0
r1 = 0
r2 = 0
max_multiple = 0 
for i in range(1, bigger + 1):
    r1 = int(number1 % i)
    r2 = int(number2 % i)
    #st.write(r1)
    #st.write(r2)
    if int(r1) == 0:
        multiple1 = int(i)
    if int(r2) == 0:
        multiple2 = int(i)
    #st.write(multiple1)
    #st.write(multiple2)
    if multiple1 == multiple2:
        max_multiple = multiple1
st.write(f"{number1}と{number2}の最小公倍数は{max_multiple}です")