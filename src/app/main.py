import streamlit as st
from dotenv import load_dotenv

from src.app.components.chat_panel import render_chat_panel
from src.app.state.session import init_session_state


def init_app() -> None:
    load_dotenv()
    st.set_page_config(
        page_title="VALORANT Scouting Report Generator",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_session_state()


def main() -> None:
    init_app()

    # Sidebar: Saved Reports and API Key
    with st.sidebar:
        st.title("Scout Library")
        st.markdown("---")

        st.subheader("Saved Reports")
        if st.session_state.saved_reports:
            for report in st.session_state.saved_reports:
                if st.button(
                    report,
                    key=f"saved_{report}",
                    use_container_width=True,
                    disabled=st.session_state.processing,
                ):
                    st.toast(f"Loading {report}...")
        else:
            st.info("No saved reports yet.")

        st.markdown("---")

        # Demo Mode info
        st.warning("⚠️ **Demo Mode**")
        st.caption(
            "Currently showing pre-computed data. To switch to **full-access mode**, please enter your GRID API key below."
        )

        api_key = st.text_input(
            "GRID API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your GRID API key to ingest live data.",
            disabled=st.session_state.processing,
        )
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            if api_key:
                st.success("API Key updated! Switching to live mode...")
                st.rerun()

    # Title and Top Controls
    st.markdown(
        """
        <style>
        /* Global Background and Text Color */
        .stApp {
            background: #000000 !important;
            color: #ffffff !important;
        }
        .main-title {
            margin: 0px !important;
            padding: 0px !important;
            font-size: 1.8rem !important;
            color: #ffffff !important;
            white-space: nowrap;
            text-align: left !important;
            font-weight: 700 !important;
            margin-top: -45px !important;
        }
        /* Style for the top buttons to be much smaller */
        [data-testid="column"]:has([key="save_report_btn"]) button,
        [data-testid="column"]:has([data-testid="stPopover"]) button {
            border-radius: 15px !important;
            font-size: 0.65rem !important;
            padding: 1px 8px !important;
            height: 24px !important;
            min-height: 0px !important;
            width: auto !important;
            margin-top: -45px !important;
            background-color: #0f172a !important;
            color: #ffffff !important;
            border: 1px solid #1e293b !important;
            white-space: nowrap !important;
        }
        /* Ensure Export and Save buttons stay on one line */
        [data-testid="column"]:has([data-testid="stPopover"]) button div p,
        [data-testid="column"]:has([key="save_report_btn"]) button div p {
            white-space: nowrap !important;
        }
        /* Fix the overlap and align tabs with the Scout Assistant title */
        [data-testid="stTabs"] {
            margin-top: 10px !important;
            padding-top: 0px !important;
        }
        [data-testid="stTabs"] button {
            color: #94a3b8 !important;
        }
        [data-testid="stTabs"] button[aria-selected="true"] {
            color: #ffffff !important;
            border-bottom-color: #ffffff !important;
        }

        /* Right-side Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(2, 6, 23, 0.95) !important;
            backdrop-filter: blur(15px) !important;
            border-left: 1px solid rgba(255, 255, 255, 0.1) !important;
            left: auto !important;
            right: 0px !important;
            transform: none !important;
        }
        /* Adjust main content when sidebar is right-aligned */
        [data-testid="stSidebar"] + section {
            margin-left: 0px !important;
            margin-right: 0px !important;
        }
        /* Force the sidebar container to the right */
        section[data-testid="stSidebar"] {
            position: fixed;
            right: 0;
            left: auto;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] .stButton button {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
        }

        [data-testid="stTabs"] [data-testid="stHorizontalBlock"] {
             margin-top: 0px !important;
        }
        /* Tighten spacing for the column containing the report */
        [data-testid="column"]:nth-child(3) {
            margin-top: 0px !important;
            color: #ffffff !important;
        }
        /* Fix left margin for content in the main area */
        .report-content {
            padding-left: 5px;
            color: #ffffff !important;
        }
        .report-content * {
            color: #ffffff !important;
        }
        /* Raise chatbox higher - can be done via column margin */
        [data-testid="column"]:nth-child(1) {
            margin-top: -30px !important;
        }
        [data-testid="column"]:nth-child(2) {
            margin-top: -30px !important;
        }

        /* Ensure all text is white for high contrast */
        h1, h2, h3, p, span, label {
            color: #ffffff !important;
        }
        </style>

    """,
        unsafe_allow_html=True,
    )

    # Header with Title and Top Controls in one row
    st.markdown('<div class="header-row-container">', unsafe_allow_html=True)
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown(
            '<h1 class="main-title">VALORANT Scouting Report Generator</h1>',
            unsafe_allow_html=True,
        )
    with header_col2:
        btn_cols = st.columns([1.3, 1.5])
        with btn_cols[0]:
            if st.button(
                "Save report",
                key="save_report_btn",
                use_container_width=True,
                disabled=st.session_state.processing,
            ):
                st.toast("Success! Report saved to library.", icon="✅")
        with btn_cols[1]:
            # Export report with popover for more details
            with st.popover(
                "Export report",
                use_container_width=True,
                disabled=st.session_state.processing,
            ):
                st.markdown("### Export Configuration")
                st.markdown("Select details to include in your scouting report:")
                st.checkbox("Match Summaries", value=True)
                st.checkbox("Player Heatmaps", value=True)
                st.checkbox("Economic Analysis", value=True)
                st.checkbox("Tactical Counter-strats", value=True)
                st.checkbox("Raw GRID Telemetry Logs", value=False)

                st.markdown("---")
                st.selectbox("Format", ["PDF", "CSV", "JSON", "Interactive HTML"])

                if st.button("Generate Export", type="primary", use_container_width=True):
                    st.toast("Export started! Your file will be ready shortly.", icon="📥")
    st.markdown("</div>", unsafe_allow_html=True)

    # Main Layout
    # Column A: Chatbot (1/4)
    # Column B: Insights & Reports (3/4)
    # We add a bit of padding between columns using a container or CSS
    col_chat, col_spacer, col_main = st.columns([1, 0.1, 3])

    with col_chat:
        render_chat_panel()

    with col_main:
        # Main Content Area: Team + Player Tabs + Prediction Tool
        tab_titles = [
            "Team",
            "Player 1",
            "Player 2",
            "Player 3",
            "Player 4",
            "Player 5",
            "Prediction Tool ✨",
        ]
        report_tabs = st.tabs(tab_titles)

        for tab_idx, tab in enumerate(report_tabs):
            with tab:
                current_tab_title = tab_titles[tab_idx]

                if current_tab_title == "Prediction Tool ✨":
                    st.markdown('<div class="report-content">', unsafe_allow_html=True)
                    st.markdown(
                        f'<h3 style="margin-top: 10px;">{current_tab_title}</h3>',
                        unsafe_allow_html=True,
                    )
                    st.info("Input match data and player stats below to run strategic simulations.")
                    st.markdown(
                        '<div style="height: 300px; border: 1px dashed #1e293b; border-radius: 15px; display: flex; align-items: center; justify-content: center; color: #475569;">[Data Input Workspace]</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    continue

                # Custom CSS for the horizontal navbar
                st.markdown(
                    """
                    <style>
                    /* Fix alignment of the nav buttons to match data text */
                    .nav-container {
                        display: flex;
                        flex-direction: row;
                        gap: 0px;
                        margin-bottom: 0px;
                        margin-top: -10px;
                        margin-left: 5px;
                        justify-content: flex-start;
                    }
                    /* Target specifically the navigation buttons in this section */
                    .nav-container button {
                        font-size: 0.6rem !important;
                        padding: 1px 6px !important;
                        min-height: 0px !important;
                        height: 20px !important;
                        width: auto !important;
                        border-radius: 10px !important;
                        line-height: 1 !important;
                    }
                    /* Remove Streamlit's default column gap for this container */
                    [data-testid="stHorizontalBlock"]:has(.nav-container) {
                        gap: 0px !important;
                    }
                    /* Further reduce space between tabs and this nav */
                    [data-testid="stVerticalBlock"] > div:has(.nav-container) {
                        margin-top: -15px !important;
                    }
                    /* Reduce space after the nav */
                    .nav-divider {
                        margin-top: -15px !important;
                        margin-bottom: 0px !important;
                        margin-left: 5px !important;
                        opacity: 0.5;
                    }
                    </style>
                """,
                    unsafe_allow_html=True,
                )

                nav_items = [
                    "Overview",
                    "Offense",
                    "Defense",
                    "Tendencies",
                    "Strategies",
                ]

                # Use session state to track the selection for each tab
                if f"nav_selection_{tab_idx}" not in st.session_state:
                    st.session_state[f"nav_selection_{tab_idx}"] = "Overview"

                # Use a single container with a custom class for the navigation buttons
                # We use columns but with small widths to prevent stretching
                # We align it with the top of the chatbox by reducing margin-top even more
                st.markdown(
                    """
                    <style>
                    .second-nav-row {
                        margin-top: -30px !important;
                    }
                    </style>
                """,
                    unsafe_allow_html=True,
                )

                with st.container():
                    cols = st.columns(
                        [1, 1, 1, 1.2, 1.2, 4.6]
                    )  # Give more space to Tendencies and Strategies

                    for i, item in enumerate(nav_items):
                        is_active = st.session_state[f"nav_selection_{tab_idx}"] == item
                        with cols[i]:
                            st.markdown('<div class="nav-container">', unsafe_allow_html=True)
                            if st.button(
                                item,
                                key=f"btn_{tab_idx}_{item}",
                                type="secondary" if not is_active else "primary",
                            ):
                                st.session_state[f"nav_selection_{tab_idx}"] = item
                                st.rerun()
                            st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<hr class="nav-divider">', unsafe_allow_html=True)

                selection = st.session_state[f"nav_selection_{tab_idx}"]
                st.markdown('<div class="report-content">', unsafe_allow_html=True)
                st.markdown(
                    f'<h3 style="margin-top: -30px;">{selection}</h3>',
                    unsafe_allow_html=True,
                )
                st.write(f"Report section for {selection} will be displayed here.")
                st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
