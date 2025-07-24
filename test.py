import streamlit as st
import time
import random

st.set_page_config("반응 속도 테스트", layout="centered")
st.title("⚡ 반응 속도 테스트")
st.markdown("🖱️ 버튼을 누르고 기다리세요. 초록색이 되면 바로 클릭!")

# ---------------- 초기화 ---------------- #
if "phase" not in st.session_state:
    st.session_state.phase = "ready"
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = 0
if "wait_time" not in st.session_state:
    st.session_state.wait_time = 0

# ---------------- 리셋 함수 ---------------- #
def reset_game():
    st.session_state.phase = "ready"
    st.session_state.start_time = 0
    st.session_state.reaction_time = 0
    st.session_state.wait_time = 0

# ---------------- 게임 진행 ---------------- #
if st.session_state.phase == "ready":
    if st.button("▶️ 시작"):
        st.session_state.wait_time = random.uniform(2, 5)
        st.session_state.start_time = time.time()
        st.session_state.phase = "waiting"

elif st.session_state.phase == "waiting":
    elapsed = time.time() - st.session_state.start_time
    if elapsed >= st.session_state.wait_time:
        st.session_state.start_time = time.time()
        st.session_state.phase = "go"
        st.experimental_rerun()
    else:
        st.markdown("⏳ 준비 중... (절대 누르지 마세요!)")
        if st.button("🚫 실수로 눌렀어요"):
            st.error("너무 빨랐어요! 다시 시도하세요.")
            reset_game()

elif st.session_state.phase == "go":
    if st.button("💥 지금 클릭!"):
        reaction = time.time() - st.session_state.start_time
        st.session_state.reaction_time = int(reaction * 1000)
        st.success(f"🎉 반응 속도: **{st.session_state.reaction_time}ms**")
        reset_game()

