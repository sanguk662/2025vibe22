import streamlit as st
import random
import time
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(page_title="가위 바위 보 챌린지", page_icon="✊", layout="centered")

# 배경음악 삽입
audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
components.html(
    f"""
    <audio autoplay loop>
        <source src="{audio_url}" type="audio/mp3">
    </audio>
    """,
    height=0,
)

# 세션 상태 초기화
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "round_result" not in st.session_state:
    st.session_state.round_result = ""

# 선택 옵션
choices = ["가위", "바위", "보"]
emoji_map = {"가위": "✌", "바위": "✊", "보": "✋"}

# 목표 점수 설정
st.sidebar.title("🎯 도전 모드 설정")
goal_score = st.sidebar.slider("몇 점 먼저 도달하면 승리?", 1, 10, 5)

# 타이틀 및 선택
st.title("🔥 가위 바위 보 챌린지")
st.markdown("가위✌ 바위✊ 보✋ 중 하나를 선택하세요!")

user_choice = st.radio("당신의 선택은?", choices, index=None, horizontal=True)

# 대결 버튼
if user_choice and st.button("🎮 대결 시작!"):
    with st.spinner("🤖 컴퓨터가 선택 중..."):
        time.sleep(1.2)
        computer_choice = random.choice(choices)

    # 결과 판단
    st.write(f"🙋‍♂️ 당신: {emoji_map[user_choice]} **{user_choice}**")
    st.write(f"🤖 컴퓨터: {emoji_map[computer_choice]} **{computer_choice}**")

    if user_choice == computer_choice:
        result = "😐 비겼습니다!"
    elif (
        (user_choice == "가위" and computer_choice == "보") or
        (user_choice == "바위" and computer_choice == "가위") or
        (user_choice == "보" and computer_choice == "바위")
    ):
        result = "🎉 당신이 이겼습니다!"
        st.session_state.user_score += 1
    else:
        result = "💀 컴퓨터가 이겼습니다!"
        st.session_state.computer_score += 1

    st.session_state.round_result = result

# 결과 출력
if st.session_state.round_result:
    st.subheader(st.session_state.round_result)

# 점수 출력
st.markdown("---")
st.markdown(f"""
🏆 **스코어**  
- 🙋‍♂️ 당신: `{st.session_state.user_score}` 점  
- 🤖 컴퓨터: `{st.session_state.computer_score}` 점
""")

# 도전 모드 종료 조건
if st.session_state.user_score >= goal_score:
    st.balloons()
    st.success(f"🎉 당신이 {goal_score}점에 도달하여 승리했습니다!")
    if st.button("🔁 다시 시작"):
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.se
