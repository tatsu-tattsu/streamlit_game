import streamlit as st

st.title("hello, streamlit")
st.write("これは最小限のstreamlitアプリです")

# 初期化​

if "count" not in st.session_state:
    st.session_state.count = 0

# 更新​

if st.button("カウントアップ"):
    st.session_state.count += 1

# 表示​

st.write("カウント:", st.session_state.count)

import streamlit as st

# まだ存在しない場合は初期化​

if "chips" not in st.session_state:
    st.session_state["chips"] = 3

# 自分で "chips" という名前をつけて値を保存​

# 値を更新​

st.session_state["chips"] += 1

# 参照​

st.write("チップ数:", st.session_state["chips"])
import streamlit as st

qp = st.query_params

round_num = int(qp.get("round", "1"))  # なければ 1​

st.write(f"現在のラウンド: {round_num}")

if st.button("次のラウンドへ"):

    round_num += 1

    st.query_params["round"] = str(round_num)  # URLを更新​

    st.write(f"次のラウンドは {round_num} です")