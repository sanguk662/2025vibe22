import streamlit as st
import time
import random

st.set_page_config(layout="wide")
st.title("🏃 미니 달리기 게임")

# 초기 세션 상태
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 0
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.is_jumping = False
    st.session_state.jump_start_time = None
    st.session_state.game_over = False
    st.session_state.speed = 0.2

# 점프 처리
def jump():
    if not st.session_state.is_jumping:
        st.session_state.is_jumping = True
        st.session_state.jump_start_time = time.time()

# 장애물 생성
def generate_obstacle():
    if random.random() < 0.3:
        st.session_state.obstacles.append(20)

# 장애물 이동
def move_obstacles():
    st.session_state.obstacles = [x - 1 for x in st.session_state.obstacles if x - 1 > 0]

# 충돌 검사
def check_collision():
    if 1 in st.session_state.obstacles and not st.session_state.is_jumping:
        st.session_state.game_over = True

# 게임 보드 그리기
def draw_board():
    row = ["⬜"] * 20
    if st.session_state.is_jumping:
        row[st.session_state.player_pos] = "🕴️"  # 점프 중
    else:
        row[st.session_state.player_pos] = "🏃"

    for pos in st.session_state.obstacles:
        if pos == st.session_state.player_pos and not st.session_state.is_jumping:
            row[pos] = "💥"
        elif 0 <= pos < 20:
            row[pos] = "🟥"

    st.markdown("".join(row))
    st.markdown(f"**점수: {st.session_state.score}**")

# 새로 시작
def reset_game():
    st.session_state.player_pos = 0
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.is_jumping = False
    st.session_state.jump_start_time = None
    st.session_state.game_over = False
    st.session_state.speed = 0.2

# 게임 루프 실행 버튼
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("⏫ 점프"):
        jump()
with col2:
    if st.button("🔄 새로 시작"):
        reset_game()

# 게임 루프 실행
if not st.session_state.game_over:
    placeholder = st.empty()
    while not st.session_state.game_over:
        with placeholder.container():
            draw_board()
        generate_obstacle()
        move_obstacles()
        check_collision()

        # 점프 시간 1초 유지
        if st.session_state.is_jumping and time.time() - st.session_state.jump_start_time > 1:
            st.session_state.is_jumping = False

        st.session_state.score += 1
        time.sleep(st.session_state.speed)
        st.rerun()
else:
    st.error("💀 게임 오버!")
