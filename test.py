import streamlit as st
import random
import time

st.set_page_config(layout="wide")
st.title("💣 폭탄 피하기 게임")

# ---------------- 세션 초기화 ---------------- #
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 2
if "bombs" not in st.session_state:
    st.session_state.bombs = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

cols = st.columns(5)

def draw_board():
    board = [["⬜" for _ in range(5)] for _ in range(6)]
    for b in st.session_state.bombs:
        if 0 <= b[0] < 6:
            board[b[0]][b[1]] = "💣"
    board[5][st.session_state.player_pos] = "😃"
    for row in board:
        st.write("".join(row))

def drop_bomb():
    if random.random() < 0.5:
        st.session_state.bombs.append([0, random.randint(0, 4)])
    new_bombs = []
    for b in st.session_state.bombs:
        b[0] += 1
        if b[0] == 5 and b[1] == st.session_state.player_pos:
            st.session_state.game_over = True
        elif b[0] < 6:
            new_bombs.append(b)
    st.session_state.bombs = new_bombs
    st.session_state.score += 1

def move_player(direction):
    if direction == "left" and st.session_state.player_pos > 0:
        st.session_state.player_pos -= 1
    elif direction == "right" and st.session_state.player_pos < 4:
        st.session_state.player_pos += 1

def reset_game():
    st.session_state.player_pos = 2
    st.session_state.bombs = []
    st.session_state.score = 0
    st.session_state.game_over = False

draw_board()
st.markdown(f"### 점수: {st.session_state.score}")

# ---------------- 키보드 이벤트 ---------------- #
st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        let d = '';
        if (e.key === 'a') { d = 'left'; }
        else if (e.key === 'd') { d = 'right'; }
        if (d !== '') {
            fetch(`/?move=` + d);
        }
    });
    </script>
""", unsafe_allow_html=True)

query_params = st.experimental_get_query_params()
if 'move' in query_params:
    direction = query_params['move'][0]
    move_player(direction)
    st.experimental_set_query_params()  # clear query param

# ---------------- 조작 버튼 ---------------- #
c1, c2, c3 = st.columns([1,2,1])
with c1:
    if st.button("⬅️ 왼쪽"):
        move_player("left")
with c3:
    if st.button("➡️ 오른쪽"):
        move_player("right")

# ---------------- 게임 루프 ---------------- #
if not st.session_state.game_over:
    drop_bomb()
    time.sleep(0.3)
    st.experimental_rerun()
else:
    st.error("💥 게임 오버! 새로 시작을 눌러주세요.")
    if st.button("🔄 새로 시작"):
        reset_game()
        st.experimental_rerun()
