import streamlit as st
import base64
import random
import os

st.set_page_config(layout="wide")

# 세션 초기화
if "cracks" not in st.session_state:
    st.session_state.cracks = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "tool" not in st.session_state:
    st.session_state.tool = "🔨 망치"
if "crack_img" not in st.session_state:
    st.session_state.crack_img = None
if "sound_path" not in st.session_state:
    st.session_state.sound_path = None
if "tool_cursor" not in st.session_state:
    st.session_state.tool_cursor = None

# 업로드: 깨진 흔적 이미지 (필수)
st.sidebar.header("🖼 금 간 이미지 업로드")
crack_file = st.sidebar.file_uploader("금 간 유리 PNG (투명 배경)", type=["png"])
if crack_file:
    st.session_state.crack_img = crack_file.read()

# 업로드: 도구 아이콘 (선택)
st.sidebar.markdown("🎯 커서 도구 이미지 (선택)")
tool_cursor_file = st.sidebar.file_uploader("도구 이미지 PNG", type=["png"])
if tool_cursor_file:
    tool_cursor_bytes = tool_cursor_file.read()
    st.session_state.tool_cursor = base64.b64encode(tool_cursor_bytes).decode()

# 도구 사운드
tool_sound = st.sidebar.selectbox("🔊 도구 소리 선택", options=["hammer", "gun", "ice", "rock"])
sound_path = f"assets/sounds/{tool_sound}.mp3"
if os.path.exists(sound_path):
    st.session_state.sound_path = sound_path

# 배경 업로드
bg = st.sidebar.file_uploader("🖼 배경 이미지 업로드", type=["jpg", "jpeg", "png"])
if bg:
    bg_bytes = bg.read()
    bg_b64 = base64.b64encode(bg_bytes).decode()
    st.markdown(
        f"""<style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_b64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>""",
        unsafe_allow_html=True,
    )

# 커서 스타일 적용
if st.session_state.tool_cursor:
    st.markdown(f"""
    <style>
    * {{
        cursor: url("data:image/png;base64,{st.session_state.tool_cursor}"), auto;
    }}
    </style>
    """, unsafe_allow_html=True)

# 제목 및 점수
st.markdown("""
    <h1 style="text-align:center; color:white;">💥 바탕화면 깨기 게임</h1>
    <p style="text-align:center; color:lightgreen;">🏆 점수: <strong>{}</strong>점 | 💥 깬 횟수: <strong>{}</strong>회</p>
""".format(st.session_state.score, len(st.session_state.cracks)), unsafe_allow_html=True)

# 클릭 감지 버튼
clicked = st.button("🖱 화면 클릭 시 금 생성 (임시 구현용 버튼)")

# 클릭 시 금 생성
if clicked and st.session_state.crack_img:
    x = random.randint(5, 85)
    y = random.randint(5, 80)
    encoded = base64.b64encode(st.session_state.crack_img).decode()
    st.session_state.cracks.append({"x": x, "y": y, "img": encoded})

    # 사운드
    if st.session_state.sound_path:
        with open(st.session_state.sound_path, "rb") as f:
            sound_b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{sound_b64}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

    # 점수 추가
    st.session_state.score += 5

# 금 이미지 표시
for c in st.session_state.cracks:
    st.markdown(f"""
    <div style="position: fixed; top: {c['y']}%; left: {c['x']}%; z-index: 1000;">
        <img src="data:image/png;base64,{c['img']}" width="150">
    </div>
    """, unsafe_allow_html=True)

# 리셋
if st.sidebar.button("🔄 초기화"):
    st.session_state.cracks = []
    st.session_state.score = 0
