import streamlit as st
import base64
import os
import random

st.set_page_config(layout="wide")

# -------------------- 도구 설정 ------------------------
TOOLS = {
    "🔨 망치": {
        "icon": "assets/tools/hammer.png",
        "crack": "assets/cracks/crack1.png",
        "sound": "assets/sounds/hammer.mp3",
        "score": 5
    },
    "🔫 총": {
        "icon": "assets/tools/gun.png",
        "crack": "assets/cracks/crack2.png",
        "sound": "assets/sounds/gun.mp3",
        "score": 7
    },
    "🪨 돌": {
        "icon": "assets/tools/rock.png",
        "crack": "assets/cracks/crack3.png",
        "sound": "assets/sounds/rock.mp3",
        "score": 3
    },
    "🪓 도끼": {
        "icon": "assets/tools/axe.png",
        "crack": "assets/cracks/crack4.png",
        "sound": "assets/sounds/axe.mp3",
        "score": 6
    },
    "⚡ 전기": {
        "icon": "assets/tools/electric.png",
        "crack": "assets/cracks/crack5.png",
        "sound": "assets/sounds/electric.mp3",
        "score": 9
    },
    "🧊 얼음": {
        "icon": "assets/tools/ice.png",
        "crack": "assets/cracks/crack6.png",
        "sound": "assets/sounds/ice.mp3",
        "score": 8
    },
    "☄️ 운석": {
        "icon": "assets/tools/meteor.png",
        "crack": "assets/cracks/crack7.png",
        "sound": "assets/sounds/meteor.mp3",
        "score": 10
    }
}

# -------------------- 세션 초기화 ------------------------
if "cracks" not in st.session_state:
    st.session_state.cracks = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "tool" not in st.session_state:
    st.session_state.tool = list(TOOLS.keys())[0]

# -------------------- 도구 선택 ------------------------
st.sidebar.title("🧰 도구 선택")
st.session_state.tool = st.sidebar.radio("무기를 골라주세요", list(TOOLS.keys()))

if st.sidebar.button("🔄 초기화"):
    st.session_state.cracks = []
    st.session_state.score = 0

# -------------------- 배경 이미지 처리 ------------------------
DEFAULT_BG = "assets/background.jpg"
bg_b64 = None

if os.path.exists(DEFAULT_BG):
    with open(DEFAULT_BG, "rb") as f:
        bg_b64 = base64.b64encode(f.read()).decode()
else:
    uploaded = st.file_uploader("🖼 배경 이미지가 없습니다. 업로드해주세요 (JPG/PNG)", type=["jpg", "png"])
    if uploaded:
        bg_b64 = base64.b64encode(uploaded.read()).decode()

if bg_b64:
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
else:
    st.warning("❗ 배경 이미지가 없습니다. assets/background.jpg 를 넣거나 업로드 해주세요.")

# -------------------- 마우스 커서 도구 ------------------------
tool_icon = TOOLS[st.session_state.tool]["icon"]
with open(tool_icon, "rb") as f:
    tool_b64 = base64.b64encode(f.read()).decode()
st.markdown(f"""
    <style>
    body {{ cursor: none; }}
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
    document.addEventListener("mousemove", e => {{
        cursor.style.left = e.clientX + "px";
        cursor.style.top = e.clientY + "px";
    }});
    </script>
""", unsafe_allow_html=True)

# -------------------- 점수 표시 ------------------------
st.markdown(f"""
    <div style="text-align:center; color:white;">
        <h1>💥 바탕화면 깨기 게임</h1>
        <p>🏆 점수: {st.session_state.score}점 | 💥 깬 횟수: {len(st.session_state.cracks)}회</p>
    </div>
""", unsafe_allow_html=True)

# -------------------- 화면 클릭 감지 ------------------------
cols = st.columns(12)
for i in range(12):
    if cols[i].button(" ", key=f"click-{random.random()}"):
        x = random.randint(5, 85)
        y = random.randint(5, 80)
        crack_path = TOOLS[st.session_state.tool]["crack"]
        with open(crack_path, "rb") as f:
            crack_b64 = base64.b64encode(f.read()).decode()
        st.session_state.cracks.append({"x": x, "y": y, "img": crack_b64})

        # 사운드
        sound_path = TOOLS[st.session_state.tool]["sound"]
        with open(sound_path, "rb") as f:
            sound_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{sound_b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

        # 점수
        st.session_state.score += TOOLS[st.session_state.tool]["score"]

# -------------------- 금 이미지 출력 ------------------------
for c in st.session_state.cracks:
    st.markdown(f"""
        <div style="position: fixed; top: {c['y']}%; left: {c['x']}%; z-index: 1000;">
            <img src="data:image/png;base64,{c['img']}" width="150">
        </div>
    """, unsafe_allow_html=True)
