import streamlit as st
import random
import time

st.set_page_config(page_title="폭탄 피하기 게임 💣", layout="wide")
st.title("💣 폭탄 피하기 게임")

# 게임 설정
BOARD_WIDTH = 10
BOARD_HEIGHT = 15
BOMB_EMOJI = "💣"
PLAYER_EMOJI = "😀"

if "player_x" not in st.session_state:
    st.session_state.player_x = BOARD_WIDTH // 2
    st.session_state.bombs = []
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.last_update = time.time()

# 폭탄 생성 확률
BOMB_PROB = 0.15
UPDATE_INTERVAL = 0.5  # 초

def new_frame():
    # 폭탄 아래로 이동
    new_bombs = []
    for x, y in st.session_state.bombs:
        if y + 1 < BOARD_HEIGHT:
            new_bombs.append((x, y + 1))
    st.session_state.bombs = new_bombs

    # 폭탄 새로 생성
    for i in range(BOARD_WIDTH):
        if random.random() < BOMB_PROB:
            st.session_state.bombs.append((i, 0))

    # 충돌 체크
    for x, y in st.session_state.bombs:
        if y == BOARD_HEIGHT - 1 and x == st.session_state.player_x:
            st.session_state.game_over = True
            return

    st.session_state.score += 1

# 키 조작 처리
key = st.session_state.get("key")
if key == "left" and st.session_state.player_x > 0:
    st.session_state.player_x -= 1
elif key == "right" and st.session_state.player_x < BOARD_WIDTH - 1:
    st.session_state.player_x += 1
st.session_state.key = None  # 초기화

# 시간 경과 확인하여 업데이트
if not st.session_state.game_over:
    now = time.time()
    if now - st.session_state.last_update > UPDATE_INTERVAL:
        new_frame()
        st.session_state.last_update = now

# 보드 출력
for y in range(BOARD_HEIGHT):
    cols = st.columns(BOARD_WIDTH)
    for x in range(BOARD_WIDTH):
        cell = ""
        if (x, y) in st.session_state.bombs:
            cell = BOMB_EMOJI
        elif y == BOARD_HEIGHT - 1 and x == st.session_state.player_x:
            cell = PLAYER_EMOJI
        cols[x].markdown(f"<div style='text-align:center; font-size:24px'>{cell}</div>", unsafe_allow_html=True)

# 조작 버튼
st.markdown("<hr>")
c1, c2, c3 = st.columns([2, 1, 2])
with c1:
    if st.button("⬅️ 왼쪽"):
        st.session_state.key = "left"
with c2:
    st.markdown(f"**점수: {st.session_state.score}**")
with c3:
    if st.button("➡️ 오른쪽"):
        st.session_state.key = "right"

# 게임 오버 처리
if st.session_state.game_over:
    st.error(f"💥 게임 오버! 최종 점수: {st.session_state.score}")
    if st.button("🔄 다시 시작"):
        for k in ["player_x", "bombs", "game_over", "score"]:
            del st.session_state[k]
        st.experimental_rerun()

# 자동 새로고침
st.experimental_rerun()
