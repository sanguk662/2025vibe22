import streamlit as st
import time
import random

st.set_page_config(layout="centered")
st.title("🐹 두더지 잡기 게임")

grid_size = 3
game_time = 20  # 게임 시간 (초)

# 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "mole_position" not in st.session_state:
    st.session_state.mole_position = (random.randint(0, 2), random.randint(0, 2))

# 두더지 클릭 시
def hit_mole(i, j):
    if (i, j) == st.session_state.mole_position:
        st.session_state.score += 1
        st.session_state.mole_position = (random.randint(0, 2), random.randint(0, 2))

# 남은 시간 계산
elapsed = int(time.time() - st.session_state.start_time)
remaining = game_time - elapsed

# UI 출력
st.markdown(f"**점수: {st.session_state.score} | 남은 시간: {remaining}초**")
st.write("")  # 줄 바꿈

if remaining > 0:
    for i in range(grid_size):
        cols = st.columns(grid_size)
        for j in range(grid_size):
            is_mole = (i, j) == st.session_state.mole_position
            label = "🐹" if is_mole else ""
            cols[j].button(
                label,
                on_click=hit_mole,
                args=(i, j),
                key=f"cell-{i}-{j}-{elapsed}"  # 고유 key 생성 (시간까지 포함)
            )
    st.experimental_rerun()  # 1프레임마다 갱신
else:
    st.success(f"⏰ 게임 종료! 최종 점수는 {st.session_state.score}점입니다.")
    if st.button("🔄 다시 시작"):
        for key in ["score", "start_time", "mole_position"]:
            del st.session_state[key]
        st.experimental_rerun()
