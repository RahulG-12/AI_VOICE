import streamlit as st
from voice_agent import start_voice_loop

st.set_page_config(
    page_title="AI Voice Agent",
    page_icon="🎙️",
    layout="wide"
)

# ---------- CUSTOM STYLE ----------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown("<div class='main-title'>🎙️ AI Voice Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Voice AI Agent with Tool Execution & Reasoning</div>", unsafe_allow_html=True)

# ---------- SESSION ----------
if "running" not in st.session_state:
    st.session_state.running = False


# ---------- SIDEBAR ----------
with st.sidebar:

    st.header("🎛 Controls")

    if st.button("▶️ Start Agent"):
        st.session_state.running = True

    if st.button("⏹ Stop Agent"):
        st.session_state.running = False

    st.divider()

    st.markdown(
        """
        ### 💡 Try Commands
        
        - Create folder test
        - Open calculator
        - Weather in Mumbai
        - Create folder on desktop
        """
    )


# ---------- MAIN ----------
col1, col2 = st.columns([3, 1])

with col1:

    st.subheader("💬 Conversation")

    chat_container = st.container(height=500, border=True)

    with chat_container:

        if st.session_state.running:
            start_voice_loop(st)
        else:
            st.info("Agent stopped. Click Start Agent to begin.")


with col2:

    st.subheader("📊 Status")

    if st.session_state.running:
        st.success("Agent Running")
    else:
        st.warning("Agent Stopped")

    st.divider()

    st.markdown(
        """
        **Features**
        - 🎤 Voice Input
        - 🧠 Reasoning Steps
        - 🛠 Tool Execution
        - 🔊 Voice Output
        """
    )


# ---------- FOOTER ----------
st.divider()
st.caption("Built with OpenAI + Streamlit | Voice Agent Project")