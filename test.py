import streamlit as st
import base64
import os
import random

# ---------------------- 설정 ---------------------- #
st.set_page_config(layout="wide")

TOOLS = {
    "hammer": {"icon": "assets/tools/hammer.png", "crack": "assets/cracks/crack1.png"},
    "gun": {"icon": "assets/tools/gun.png", "crack": "assets/cracks/crack2.png"},
    "rock": {"icon": "assets/tools/rock.png", "crack": "assets/cracks/crack3.png"},
    "axe": {"icon": "assets/tools/axe.png", "crack": "assets/cracks/crack4.png"},
    "electric": {"icon": "assets/tools/electric.png", "crack": "assets/cracks/crack5.png"},
    "ice": {"icon": "assets/tools/ice.png", "crack": "assets/cracks/crack6.png"},
    "meteor": {"icon": "assets/tools/meteor.png", "crack": "assets/cracks/crack7.png"},
}

# ---------------------- 초기화 ---------------------- #
if "score" not in st.session_state:
    st.session_state.score = 0
if "crack_count" not in st.session_state:
    st.session_state.crack_count = 0
if "tool" not in st.session_state:
    st.session_state.tool = "hammer"

# ---------------------- 배경 이미지 로드 ---------------------- #
def load_background():
    bg_path = "assets/background.jpg"
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    else:
        uploaded = st.file_uploader("🔺 배경 이미지가 없습니다. 업로드해주세요 (JPG/PNG)", type=["jpg", "jpeg", "png"])
        if uploaded:
            return base64.b64encode(uploaded.read()).decode()
    return None

bg_b64 = load_background()
if bg_b64:
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.stop()

# ---------------------- 상단 UI ---------------------- #
st.markdown("""
    <h1 style="text-align:center; color:white; font-size:3em;">💥 바탕화면 깨기 게임 💥</h1>
    <div style="text-align:center; font-size:1.3em; color:lightgreen">
    🏆 점수: {}점 &nbsp;&nbsp;&nbsp;&nbsp; 💥 깬 횟수: {}회
    </div>
""".format(st.session_state.score, st.session_state.crack_count), unsafe_allow_html=True)

# ---------------------- 도구 선택 ---------------------- #
cols = st.columns(len(TOOLS))
for i, (tool_name, tool_data) in enumerate(TOOLS.items()):
    with cols[i]:
        if os.path.exists(tool_data["icon"]):
            with open(tool_data["icon"], "rb") as f:
                icon_b64 = base64.b64encode(f.read()).decode()
            if st.button(f'<img src="data:image/png;base64,{icon_b64}" width="50">', key=tool_name, use_container_width=True):
                st.session_state.tool = tool_name

# ---------------------- 커서 이미지 적용 ---------------------- #
tool_icon = TOOLS[st.session_state.tool]["icon"]
if os.path.exists(tool_icon):
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

# ---------------------- 클릭 시 깨기 효과 ---------------------- #
st.markdown("<br><br><br>", unsafe_allow_html=True)
click_area = st.empty()

if click_area.button("💣 바탕화면 클릭해서 깨기!", use_container_width=True):
    crack_image = TOOLS[st.session_state.tool]["crack"]
    if os.path.exists(crack_image):
        with open(crack_image, "rb") as f:
            crack_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <img src="data:image/png;base64,{crack_b64}" style="position:absolute; top:{random.randint(100, 500)}px; left:{random.randint(100, 800)}px; width:150px; z-index:999;">
        """, unsafe_allow_html=True)

    st.session_state.score += random.randint(5, 20)
    st.session_state.crack_count += 1
