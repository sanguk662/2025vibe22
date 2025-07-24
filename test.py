import streamlit as st
import random
import time
import streamlit.components.v1 as components

# 초기 설정
st.set_page_config(page_title="가위 바위 보 챌린지", page_icon="✊", layout="centered")

# 배경음악
audio_file = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
components.html(
    f"""
    <audio autoplay loop>
      <source src="{audio_file}" type="audio/mp3">
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

# 게임 설정
choices = ["가위", "바위", "보"]
emoji_map = {"가위": "✌", "바위": "✊", "보": "✋"}
goal_score = st.slider("🎯 도전 모드: 몇 점 먼저 도달하면 승리?", 1, 10, 5)

# 제목
st.title("🔥 가위 바위 보 챌린지")
st.markdown("가위✌ 바위✊ 보✋ 중 하나를 선택하세요!")

# 사용자 선택
user_choice = st.radio("당신의 선택은?", choices, index=None, horizontal=True)

# 게임 실행
if user_choice and st.button("대결 시작!"):
    with st.spinner("컴퓨터가 선택 중..."):
        time.sleep(1.2)
        computer_choice = random.choice(choices)

    # 결과 출력
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

# 점수판
st.markdown("---")
st.markdown(f"🏆 **스코어**  
- 🙋‍♂️ 당신: `{st.session_state.user_score}` 점  
- 🤖 컴퓨터: `{st.session_state.computer_score}` 점")

# 도전 모드 클리어 여부
if st.session_state.user_score >= goal_score:
    st.success(f"🎉 당신이 {goal_score}점에 먼저 도달하여 승리했습니다!")
    if st.button("다시 시작하기"):
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.session_state.round_result = ""

elif st.session_state.computer_score >= goal_score:
    st.error(f"💀 컴퓨터가 {goal_score}점에 먼저 도달하여 당신은 패배했습니다!")
    if st.button("다시 시작하기"):
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.session_state.round_result = ""
