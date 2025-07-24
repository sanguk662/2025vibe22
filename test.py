import streamlit as st
import random
import time

st.set_page_config(page_title="두더지 잡기 게임", layout="centered")
st.title("🐹 두더지 잡기 게임")

# 초기화
grid_size = 3
if "score" not in st.session_state:
    st.session_state.score = 0
if "mole_position" not in st.session_state:
    st.session_state.mole_position = (random.randint(0, 2), random.randint(0, 2))
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# 시간 계산
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(20 - elapsed, 0)

# 두더지 클릭 처리
def hit_mole(i, j):
    if (i, j) == st.session_state.mole_position:
        st.session_state.score += 1
    st.session_state.mole_position = (random.randint(0, 2), random.randint(0, 2))
    st.experimental_rerun()

# 게임 종료 시
if remaining == 0:
    st.markdown("## ⏰ 시간 종료!")
    st.markdown(f"### 🎯 최종 점수: {st.session_state.score}점")
    if st.button("🔄 다시 시작"):
        st.session_state.score = 0
        st.session_state.mole_position = (random.randint(0, 2), random.randint(0, 2))
        st.session_state.start_time = time.time()
        st.experimental_rerun()
else:
    # 점수와 타이머 출력
    st.markdown(f"### 점수: {st.session_state.score} | 남은 시간: {remaining}초")

    # 버튼 그리드 렌더링
    for i in range(grid_size):
        cols = st.columns(grid_size)
        for j in range(grid_size):
            if (i, j) == st.session_state.mole_position:
                cols[j].button("🐹", on_click=hit_mole, args=(i, j))
            else:
                cols[j].button("", on_click=hit_mole, args=(i, j))
