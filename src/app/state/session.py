import streamlit as st


def init_session_state() -> None:
    """Initialize streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "How can I help you with your scouting today?",
            }
        ]

    if "opponent" not in st.session_state:
        st.session_state.opponent = "Demo Opponent"

    if "map_name" not in st.session_state:
        st.session_state.map_name = "All"

    if "processing" not in st.session_state:
        st.session_state.processing = False

    if "saved_reports" not in st.session_state:
        st.session_state.saved_reports = [
            "Sentinels vs Fnatic - Bind",
            "G2 vs Paper Rex - Lotus",
            "Team Heretics vs Gen.G - Ascent",
        ]

    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
