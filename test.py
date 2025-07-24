import streamlit as st
import random
import time

st.set_page_config(page_title="두더지 잡기 게임 🐹", layout="centered")
st.title("🐹 두더지 잡기 게임")

# 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.mole_position = random.randint(1, 9)
    st.session_state.start_time = time.time()
    st.session_state.time_limit = 20

def restart_game():
    st.session_state.score = 0
    st.session_state.mole_position = random.randint(1, 9)
    st.session_state.start_time = time.time()
    st.session_state.time_limit = 20

# 게임 종료 여부
elapsed = int(time.time() - st.session_state.start_time)
remaining = st.session_state.time_limit - elapsed
if remaining <= 0:
    st.error(f"⏰ 게임 종료! 최종 점수: {st.session_state.score}점")
    if st.button("🔄 다시하기"):
        restart_game()
    st.stop()

# 게임 UI
st.markdown(f"⏱️ 남은 시간: **{remaining}초** | 🎯 점수: **{st.session_state.score}점**")

grid = st.columns(3)
for i in range(1, 10):
    col = grid[(i-1)%3]
    if st.session_state.mole_position == i:
        if col.button("🐹", key=i):
            st.session_state.score += 1
            st.session_state.mole_position = random.randint(1, 9)
            st.experimental_rerun()
    else:
        col.button("", key=i, disabled=True)
