import streamlit as st
import random
import base64
import os

st.set_page_config(layout="wide")

# 도구 정의 (10개) + 점수 포함
TOOLS = {
    "🔫 총": {"cracks": ["assets/cracks/gun1.png"], "sound": "assets/sounds/gun.mp3", "score": 5},
    "🔨 망치": {"cracks": ["assets/cracks/hammer1.png"], "sound": "assets/sounds/hammer.mp3", "score": 4},
    "🪨 돌": {"cracks": ["assets/cracks/rock1.png"], "sound": "assets/sounds/rock.mp3", "score": 3},
    "🪓 도끼": {"cracks": ["assets/cracks/axe1.png"], "sound": "assets/sounds/axe.mp3", "score": 6},
    "☄️ 운석": {"cracks": ["assets/cracks/meteor1.png"], "sound": "assets/sounds/meteor.mp3", "score": 10},
    "⚡️ 전기 충격기": {"cracks": ["assets/cracks/electric1.png"], "sound": "assets/sounds/electric.mp3", "score": 7},
    "🧊 냉동광선기": {"cracks": ["assets/cracks/ice1.png"], "sound": "assets/sounds/ice.mp3", "score": 8},
    "🧽 고무망치": {"cracks": ["assets/cracks/rubber1.png"], "sound": "assets/sounds/rubber.mp3", "score": 1},
    "🧠 정신 공격": {"cracks": ["assets/cracks/mind1.png"], "sound": "assets/sounds/mind.mp3", "score": 9},
    "🦖 공룡 발톱": {"cracks": ["assets/cracks/dino1.png"], "sound": "assets/sounds/dino.mp3", "score": 12}
}

# 배경 이미지 적용 함수
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# 사운드 재생
def play_sound(sound_path):
    with open(sound_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

# 금 이미지 출력
def render_crack(x, y, img_path):
    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <div style="position: fixed; top: {y}%; left: {x}%; z-index: 999;">
            <img src="data:image/png;base64,{encoded}" width="150">
        </div>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if "cracks" not in st.session_state:
    st.session_state.cracks = []

if "score" not in st.session_state:
    st.session_state.score = 0

# ✅ 배경 이미지 처리 (assets 없으면 대체)
DEFAULT_BG = "assets/background.jpg"

if os.path.exists(DEFAULT_BG):
    set_background(DEFAULT_BG)
else:
    uploaded_bg = st.file_uploader("배경 이미지를 업로드하세요 (jpg/png)", type=["jpg", "png"])
    if uploaded_bg:
        bg_bytes = uploaded_bg.read()
        encoded = base64.b64encode(bg_bytes).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("⚠️ 배경 이미지가 없습니다. 업로드하거나 assets/background.jpg를 추가하세요.")

# 타이틀 및 점수 표시
st.markdown("""
    <h1 style="text-align: center; color: white;">💥 바탕화면 깨기 게임</h1>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="text-align: center; color: lightgreen; font-size: 22px;">
        🏆 점수: <strong>{st.session_state.score}</strong>점 &nbsp;&nbsp;
        💥 깬 횟수: <strong>{len(st.session_state.cracks)}</strong>회
    </div><br>
    """,
    unsafe_allow_html=True
)

# 도구 선택 및 초기화
st.sidebar.header("🧰 도구 선택")
tool = st.sidebar.radio("깨는 도구를 고르세요", list(TOOLS.keys()))

if st.sidebar.button("🔄 초기화"):
    st.session_state.cracks = []
    st.session_state.score = 0

# 메인 버튼
cols = st.columns(12)
for i in range(len(cols)):
    if cols[i].button("💣", key=f"btn-{i}-{random.random()}"):
        x = random.randint(5, 90)
        y = random.randint(5, 80)
        tool_data = TOOLS[tool]
        crack_img = random.choice(tool_data["cracks"])
        st.session_state.cracks.append({
            "x": x,
            "y": y,
            "img": crack_img,
            "sound": tool_data["sound"]
        })
        st.session_state.score += tool_data["score"]
        play_sound(tool_data["sound"])

# 금 이미지 표시
for crack in st.session_state.cracks:
    render_crack(crack["x"], crack["y"], crack["img"])
