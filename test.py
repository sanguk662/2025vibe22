import streamlit as st
import random
import numpy as np

st.set_page_config(layout="centered")

st.title("2048 숫자 합치기 게임 🎮")

SIZE = 4

# -------------------- 초기화 -------------------- #
if "board" not in st.session_state:
    st.session_state.board = np.zeros((SIZE, SIZE), dtype=int)
    def place():
        empty = list(zip(*np.where(st.session_state.board == 0)))
        if empty:
            i, j = random.choice(empty)
            st.session_state.board[i][j] = 2 if random.random() < 0.9 else 4
    place()
    place()

# -------------------- 보드 렌더링 -------------------- #
def draw_board():
    for i in range(SIZE):
        cols = st.columns(SIZE)
        for j in range(SIZE):
            value = st.session_state.board[i][j]
            cell = str(value) if value != 0 else ""
            cols[j].button(cell, key=f"{i}-{j}", disabled=True)

draw_board()

# -------------------- 이동 처리 -------------------- #
def move_left():
    moved = False
    for i in range(SIZE):
        tiles = st.session_state.board[i][st.session_state.board[i] != 0]
        new_row = []
        skip = False
        for j in range(len(tiles)):
            if skip:
                skip = False
                continue
            if j+1 < len(tiles) and tiles[j] == tiles[j+1]:
                new_row.append(tiles[j]*2)
                skip = True
                moved = True
            else:
                new_row.append(tiles[j])
        new_row += [0]*(SIZE - len(new_row))
        if not np.array_equal(st.session_state.board[i], new_row):
            moved = True
        st.session_state.board[i] = new_row
    return moved

def rotate_board(k):
    st.session_state.board = np.rot90(st.session_state.board, k)

def move(direction):
    if direction == "left":
        moved = move_left()
    elif direction == "right":
        rotate_board(2)
        moved = move_left()
        rotate_board(2)
    elif direction == "up":
        rotate_board(1)
        moved = move_left()
        rotate_board(-1)
    elif direction == "down":
        rotate_board(-1)
        moved = move_left()
        rotate_board(1)
    else:
        moved = False

    if moved:
        empty = list(zip(*np.where(st.session_state.board == 0)))
        if empty:
            i, j = random.choice(empty)
            st.session_state.board[i][j] = 2 if random.random() < 0.9 else 4

def is_game_over():
    temp = st.session_state.board.copy()
    for dir in ["left", "right", "up", "down"]:
        st.session_state.board = temp.copy()
        if move_left():
            st.session_state.board = temp
            return False
        rotate_board(1)
    st.session_state.board = temp
    return True

# -------------------- 방향 버튼 -------------------- #
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("⬆️ 위로"):
        move("up")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ 왼쪽"):
        move("left")
with col2:
    if st.button("🔄 새로 시작"):
        del st.session_state.board
        st.experimental_rerun()
with col3:
    if st.button("➡️ 오른쪽"):
        move("right")
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("⬇️ 아래로"):
        move("down")

# -------------------- 게임 오버 -------------------- #
if is_game_over():
    st.error("💀 게임 오버! 새로 시작을 눌러주세요.")
