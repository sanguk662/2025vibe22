import streamlit as st
import time
import random

st.set_page_config(layout="centered")
st.title("🦖 미니 공룡 달리기 게임")

# ------------------ 초기 설정 ------------------ #
if "position" not in st.session_state:
    st.session_state.position = 3  # 공룡 위치 (0~6)
    st.session_state.obstacle = 6  # 장애물 시작 위치
    st.session_state.jump = False
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.jump_frame = 0

# ------------------ 화면 구성 ------------------ #
def draw():
    line = ["⬜"] * 7
    if not st.session_state.jump:
        line[st.session_state.position] = "🦖"
    else:
        line[st.session_state.position] = "⬛"
    if st.session_state.obstacle == st.session_state.position and not st.session_state.jump:
        st.session_state.game_over = True
    else:
        line[st.session_state.obstacle] = "🌵"
    st.markdown("".join(line))
    st.markdown(f"**점수: {st.session_state.score}**")

# ------------------ 점프 처리 ------------------ #
def trigger_jump():
    if not st.session_state.jump:
        st.session_state.jump = True
        st.session_state.jump_frame = 2  # 점프 유지 프레임 수

# ------------------ 프레임 처리 ------------------ #
def next_frame():
    if st.session_state.game_over:
        return

    st.session_state.obstacle -= 1
    if st.session_state.obstacle < 0:
        st.session_state.obstacle = 6
        st.session_state.score += 1

    if st.session_state.jump:
        st.session_state.jump_frame -= 1
        if st.session_state.jump_frame <= 0:
            st.session_state.jump = False

# ------------------ UI 구성 ------------------ #
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.button("🆙 점프", on_click=trigger_jump)

placeholder = st.empty()

draw()

# ------------------ 게임 루프 ------------------ #
if not st.session_state.game_over:
    time.sleep(0.5)
    next_frame()
    st.experimental_rerun()
else:
    st.error(f"💀 게임 오버! 최종 점수: {st.session_state.score}")
    if st.button("🔄 다시 시작"):
        for key in ["position", "obstacle", "jump", "score", "game_over", "jump_frame"]:
            del st.session_state[key]
        st.experimental_rerun()
