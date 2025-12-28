import os

import streamlit as st
from dotenv import load_dotenv


def init_app() -> None:
    load_dotenv()
    st.set_page_config(
        page_title="VALORANT Scouting Report Generator",
        page_icon="🎯",
        layout="wide",
    )


def sidebar_controls() -> dict:
    st.sidebar.header("Scout Controls")

    app_mode = os.getenv("APP_MODE", "demo")
    st.sidebar.caption(f"Mode: **{app_mode.upper()}**")

    opponent = st.sidebar.text_input("Opponent Team Name", value="Demo Opponent")
    map_name = st.sidebar.selectbox(
        "Map", ["All", "Haven", "Ascent", "Bind", "Split", "Lotus"], index=0
    )

    st.sidebar.divider()
    st.sidebar.subheader("Chat")
    prompt = st.sidebar.text_area(
        "Ask for insights", height=120, placeholder="e.g., How do we beat them on Haven?"
    )

    run = st.sidebar.button("Generate Report", type="primary")

    return {"opponent": opponent, "map_name": map_name, "prompt": prompt, "run": run}


def main() -> None:
    init_app()
    controls = sidebar_controls()

    st.title("VALORANT Scouting Report Generator")

    col_a, col_b, col_c = st.columns([1.2, 1.2, 0.8], gap="large")

    with col_a:
        st.subheader("Key Conclusions")
        st.info(
            "Demo placeholder: this will show top 3–6 actionable insights with confidence & evidence."
        )

    with col_b:
        st.subheader("Team / Player Tabs")
        tabs = st.tabs(["Team", "P1", "P2", "P3", "P4", "P5"])
        with tabs[0]:
            st.write("Team overview metrics go here.")
        for i in range(1, 6):
            with tabs[i]:
                st.write(f"Player {i} metrics, heatmaps, and counters go here.")

    with col_c:
        st.subheader("Saved Reports")
        st.write("List saved reports here (demo placeholder).")

    if controls["run"]:
        with st.status("Analyzing opponent data…", expanded=True) as status:
            st.write("Identifying high-impact zones…")
            st.write("Evaluating openings, trades, and post-plant…")
            st.write("Generating counters…")
            status.update(label="Report ready", state="complete")


if __name__ == "__main__":
    main()
