import streamlit as st
import json
from pathlib import Path

# ----Pathを指定して JSONファイルを読み込み ----
json_path = Path(__file__).parent.parent / "sample_data" / "highandlow_round3.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)
round1 = data["rounds"][0]
rounds_1to2 = data["rounds"][:2]
rounds_all = data["rounds"]
st.write(round1)
st.write(rounds_1to2)
st.write(rounds_all)