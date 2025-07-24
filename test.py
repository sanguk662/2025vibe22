import streamlit as st
import base64
import random
import os

st.set_page_config(layout="wide")

# 도구 정의
TOOLS = {
    "🔨 망치": {
        "icon": "assets/tools/hammer.png",
        "crack": "assets/cracks/crack1.png",
        "sound": "assets/sounds/hammer.mp3",
        "score": 5
    },
    "🔫 총": {
        "icon": "assets/tools/gun.png",
        "crack": "assets/cracks/crack1.png",
        "sound": "assets/sounds/gun.mp3",
        "score": 7
    },
    "🪨 돌": {
        "icon": "assets/tools/rock.png",
        "crack": "assets/cracks/crack1.png",
        "sound": "assets/sounds/rock.mp3",
        "score": 3
    }
}

# 세션 상태 초기화
if "cracks" not in st.session_state:
    st.session_state.cracks = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "tool" not in st.session_state:
    st.session_state.tool = "🔨 망치"

# 도구 선택
st.sidebar.header("🧰 도구 선택")
st.session_state.tool = st.sidebar.radio("사용할 도구를 고르세요", list(TOOLS.keys()))

# 초기화 버튼
if st.sidebar.button("🔄 초기화"):
    st.session_state.cracks = []
    st.session_state.score = 0

# 배경 설정
with open("assets/background.jpg", "rb") as bg_file:
    bg_b64 = base64.b64encode(bg_file.read()).decode()
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
""", unsafe_allow_html=True)

# 도구 커서 이미지 표시
tool_icon_path = TOOLS[st.session_state.tool]["icon"]
with open(tool_icon_path, "rb") as f:
    tool_b64 = base64.b64encode(f.read()).decode()
st.markdown(f"""
    <style>
    body {{
        cursor: none;
    }}
    #tool-cursor {{
        position: fixed;
        z-index: 9999;
        width: 80px;
        pointer-events: none;
    }}
    </style>
    <img id="tool-cursor" src="data:image/png;base64,{tool_b64}">
    <script>
    const cursor = document.getElementById("tool-cursor");
    document.addEventListener("mousemove", (e) => {{
        cursor.style.left = e.clientX + "px";
        cursor.style.top = e.clientY + "px";
    }});
    </script>
""", unsafe_allow_html=True)

# 화면 중앙 상단: 점수 출력
st.markdown(f"""
    <div style="text-align:center; color:white;">
        <h1>💥 바탕화면 깨기 게임</h1>
        <p>🏆 점수: {st.session_state.score}점 | 💥 깬 횟수: {len(st.session_state.cracks)}회</p>
    </div>
""", unsafe_allow_html=True)

# 투명 클릭 버튼 만들기
cols = st.columns(12)
for i in range(12):
    if cols[i].button(" ", key=f"click-{random.random()}", help="클릭해서 깨기"):
        x = random.randint(5, 85)
        y = random.randint(5, 80)
        crack_img_path = TOOLS[st.session_state.tool]["crack"]
        with open(crack_img_path, "rb") as f:
            crack_b64 = base64.b64encode(f.read()).decode()
        st.session_state.cracks.append({"x": x, "y": y, "img": crack_b64})

        # 소리
        sound_path = TOOLS[st.session_state.tool]["sound"]
        with open(sound_path, "rb") as f:
            sound_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{sound_b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

        st.session_state.score += TOOLS[st.session_state.tool]["score"]

# 깨진 이미지 표시
for c in st.session_state.cracks:
    st.markdown(f"""
        <div style="position: fixed; top: {c['y']}%; left: {c['x']}%; z-index: 1000;">
            <img src="data:image/png;base64,{c['img']}" width="150">
        </div>
    """, unsafe_allow_html=True)
