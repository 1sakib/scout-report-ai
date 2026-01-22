import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

from src.app.components.chat_panel import render_chat_panel
from src.app.state.session import init_session_state


def get_report_data():
    """Fetches real data if a report has been generated, else returns mock data."""
    if (
        st.session_state.get("report_data")
        and st.session_state.report_data.get("status") == "completed"
    ):
        # In a real implementation, we would query DuckDB here
        # db = DuckDBClient()
        # team_stats = db.query(f"SELECT * FROM team_metrics WHERE team_name = '{st.session_state.report_data['team_name']}'")

        # For this demo/implementation step, we'll return data that reflects the requested team
        return {"team_name": st.session_state.report_data["team_name"], "is_real": True}
    return {"team_name": "Mock Team", "is_real": False}


def init_app() -> None:
    load_dotenv()
    st.set_page_config(
        page_title="VALORANT Scouting Report Generator",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed",
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
                    width="stretch",
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

        /* Standard Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(2, 6, 23, 0.95) !important;
            backdrop-filter: blur(15px) !important;
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

    report_data = get_report_data()
    team_display_name = report_data["team_name"]

    # Header with Title and Top Controls in one row
    st.markdown('<div class="header-row-container">', unsafe_allow_html=True)
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown(
            f'<h1 class="main-title">VALORANT Scouting Report: {team_display_name}</h1>',
            unsafe_allow_html=True,
        )
    with header_col2:
        btn_cols = st.columns([1.3, 1.5])
        with btn_cols[0]:
            if st.button(
                "Save report",
                key="save_report_btn",
                width="stretch",
                disabled=st.session_state.processing,
            ):
                st.toast("Success! Report saved to library.", icon="✅")
        with btn_cols[1]:
            # Export report with popover for more details
            with st.popover(
                "Export report",
                width="stretch",
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

                if st.button("Generate Export", type="primary", width="stretch"):
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

                if current_tab_title == "Team":
                    nav_items = [
                        "Overview",
                        "Offense",
                        "Defense",
                        "Clutch & Economy",
                        "Positions & Map Control",
                        "Strategies",
                    ]
                else:
                    nav_items = [
                        "Overview",
                        "Offense",
                        "Defense",
                        "Utility & Tendencies",
                        "Clutch & Economy",
                        "Positions & Map Control",
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
                    # Dynamic columns based on number of items
                    num_items = len(nav_items)
                    # We give roughly equal space to items, and more to the spacer at the end
                    col_widths = [1] * num_items + [10 - num_items]
                    cols = st.columns(col_widths)

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

                # Mock data based on selection
                is_team = current_tab_title == "Team"

                if selection == "Overview":
                    col1, col2, col3, col4 = st.columns(4)
                    if is_team:
                        col1.metric(
                            "Avg Team Rank",
                            "Ascendant 2" if not report_data["is_real"] else "Pro / Semi-Pro",
                            "+1",
                        )
                        col2.metric(
                            "Win/Loss Ratio",
                            "1.45" if not report_data["is_real"] else "1.62",
                            "+0.12",
                        )
                        col3.metric(
                            "KDA (Team)",
                            "1.12" if not report_data["is_real"] else "1.25",
                            "+0.02",
                        )
                        col4.metric(
                            "Avg. ADR",
                            "142.5" if not report_data["is_real"] else "148.2",
                            "+3.2",
                        )
                    else:
                        col1.metric("Player Rank", "Immortal 1", "+1")
                        col2.metric("Win/Loss Ratio", "1.28", "-0.05")
                        col3.metric("KDA", "1.34", "+0.08")
                        col4.metric("Avg. ADR", "158.2", "+12.1")

                    st.markdown("---")
                    sub_col1, sub_col2 = st.columns([2, 1])

                    with sub_col1:
                        if is_team:
                            st.markdown("#### Team Best Map Picks")
                            # Custom layout for map picks
                            map_col1, map_col2 = st.columns([2, 1])
                            with map_col1:
                                # Best Map (Large)
                                st.markdown(
                                    """
                                    <div style="position: relative; height: 210px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 2px solid #3b82f6;">
                                        <div style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); padding: 2px 8px; border-radius: 5px; font-size: 0.8rem;">82%</div>
                                        <span style="font-weight: bold; color: #3b82f6;">ASCENT</span>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            with map_col2:
                                # Second Best (Smaller)
                                st.markdown(
                                    """
                                    <div style="position: relative; height: 100px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b; margin-bottom: 10px;">
                                        <div style="position: absolute; top: 5px; right: 5px; background: rgba(0,0,0,0.7); padding: 1px 5px; border-radius: 4px; font-size: 0.7rem;">75%</div>
                                        <span style="font-size: 0.8rem;">BIND</span>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                # Third Best (Smaller)
                                st.markdown(
                                    """
                                    <div style="position: relative; height: 100px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">
                                        <div style="position: absolute; top: 5px; right: 5px; background: rgba(0,0,0,0.7); padding: 1px 5px; border-radius: 4px; font-size: 0.7rem;">68%</div>
                                        <span style="font-size: 0.8rem;">HAVEN</span>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.markdown("#### Best / Worst Agents")
                            st.markdown(
                                """
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                                    <div>
                                        <div style="color: #22c55e; font-weight: bold; margin-bottom: 12px; padding-left: 5px;">Best Agents</div>
                                        <div style="background-color: #0f172a; padding: 10px 15px; border-radius: 8px; border: 1px solid #1e293b; display: flex; justify-content: space-between; margin-bottom: 8px;">
                                            <span>Jett</span> <span style="color: #94a3b8;">1.45 KD</span>
                                        </div>
                                        <div style="background-color: #0f172a; padding: 10px 15px; border-radius: 8px; border: 1px solid #1e293b; display: flex; justify-content: space-between; margin-bottom: 8px;">
                                            <span>Raze</span> <span style="color: #94a3b8;">1.22 KD</span>
                                        </div>
                                        <div style="background-color: #0f172a; padding: 10px 15px; border-radius: 8px; border: 1px solid #1e293b; display: flex; justify-content: space-between;">
                                            <span>Reyna</span> <span style="color: #94a3b8;">1.15 KD</span>
                                        </div>
                                    </div>
                                    <div>
                                        <div style="color: #ef4444; font-weight: bold; margin-bottom: 12px; padding-left: 5px;">Worst Agents</div>
                                        <div style="background-color: #0f172a; padding: 10px 15px; border-radius: 8px; border: 1px solid #1e293b; display: flex; justify-content: space-between; margin-bottom: 8px;">
                                            <span>Neon</span> <span style="color: #94a3b8;">0.85 KD</span>
                                        </div>
                                        <div style="background-color: #0f172a; padding: 10px 15px; border-radius: 8px; border: 1px solid #1e293b; display: flex; justify-content: space-between; margin-bottom: 8px;">
                                            <span>Yoru</span> <span style="color: #94a3b8;">0.92 KD</span>
                                        </div>
                                        <div style="background-color: #0f172a; padding: 10px 15px; border-radius: 8px; border: 1px solid #1e293b; display: flex; justify-content: space-between;">
                                            <span>Phoenix</span> <span style="color: #94a3b8;">0.98 KD</span>
                                        </div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        st.markdown(
                            """
                            <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; margin-top: 10px;">
                                <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 10px; font-weight: bold;">Role Distribution</div>
                                <div style="background: rgba(59, 130, 246, 0.1); padding: 12px; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 10px;">
                                    <div style="color: #3b82f6; font-size: 0.7rem; font-weight: bold;">PRIMARY ROLE</div>
                                    <div style="font-size: 1.3rem; font-weight: bold; margin-top: 2px;">Duelist</div>
                                    <div style="color: #94a3b8; font-size: 0.8rem;">82% frequency</div>
                                </div>
                                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                                    <div style="background: rgba(255, 255, 255, 0.05); padding: 8px; border-radius: 6px; border: 1px solid #1e293b; text-align: center;">
                                        <div style="color: #94a3b8; font-size: 0.65rem;">Initiator</div>
                                        <div style="font-size: 0.9rem; font-weight: bold;">12%</div>
                                    </div>
                                    <div style="background: rgba(255, 255, 255, 0.05); padding: 8px; border-radius: 6px; border: 1px solid #1e293b; text-align: center;">
                                        <div style="color: #94a3b8; font-size: 0.65rem;">Controller</div>
                                        <div style="font-size: 0.9rem; font-weight: bold;">4%</div>
                                    </div>
                                    <div style="background: rgba(255, 255, 255, 0.05); padding: 8px; border-radius: 6px; border: 1px solid #1e293b; text-align: center;">
                                        <div style="color: #94a3b8; font-size: 0.65rem;">Sentinel</div>
                                        <div style="font-size: 0.9rem; font-weight: bold;">2%</div>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with sub_col2:
                        st.markdown("#### Recently Played (Last 10)")
                        st.write("W-W-L-W-W-W-L-W-L-W (70% WR)")

                        if is_team:
                            st.markdown("#### Side Strength")
                            st.markdown(
                                """
                                <style>
                                    /* Refined single bar style */
                                    .side-strength-container {
                                        margin: 20px 0;
                                    }
                                    .strength-bar {
                                        display: flex;
                                        height: 32px;
                                        border-radius: 16px;
                                        overflow: hidden;
                                        background: #1e293b;
                                        border: 1px solid #334155;
                                    }
                                    .offense-segment {
                                        background: linear-gradient(90deg, #2563eb, #3b82f6);
                                        display: flex;
                                        align-items: center;
                                        padding-left: 15px;
                                        color: white;
                                        font-weight: bold;
                                        font-size: 0.8rem;
                                    }
                                    .defense-segment {
                                        background: linear-gradient(90deg, #ef4444, #dc2626);
                                        display: flex;
                                        align-items: center;
                                        justify-content: flex-end;
                                        padding-right: 15px;
                                        color: white;
                                        font-weight: bold;
                                        font-size: 0.8rem;
                                    }
                                </style>
                                <div class="side-strength-container">
                                    <div class="strength-bar">
                                        <div style="width: 57.5%; background: linear-gradient(90deg, #2563eb, #3b82f6); border-right: 2px solid #0f172a; display: flex; align-items: center; padding-left: 15px;">
                                            <span style="font-size: 0.8rem; font-weight: bold;">OFFENSE 65%</span>
                                        </div>
                                        <div style="width: 42.5%; background: linear-gradient(90deg, #ef4444, #dc2626); display: flex; align-items: center; justify-content: flex-end; padding-right: 15px;">
                                            <span style="font-size: 0.8rem; font-weight: bold;">DEFENSE 48%</span>
                                        </div>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 0.75rem; color: #94a3b8; font-weight: bold;">
                                        <span>Primary Win Condition: Entry Fragging</span>
                                        <span>Retake Proficiency: Moderate</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown("#### Multi-frags / Survival")
                            st.markdown(
                                """
                                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 10px;">
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center;">
                                        <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">MULTI-FRAG ROUNDS</div>
                                        <div style="font-size: 1.4rem; font-weight: bold; color: #ffffff;">18%</div>
                                    </div>
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center;">
                                        <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">AVG SURVIVAL</div>
                                        <div style="font-size: 1.4rem; font-weight: bold; color: #ffffff;">78s</div>
                                        <div style="color: #475569; font-size: 0.7rem; margin-top: 5px;">Low baiting risk</div>
                                    </div>
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center;">
                                        <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">FIRST DUEL WIN %</div>
                                        <div style="font-size: 1.4rem; font-weight: bold; color: #22c55e;">54%</div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    st.markdown("#### Performance Benchmark")
                    st.info(
                        "Performance is **12% higher** than the average Immortal 1 player in this region."
                    )

                elif selection == "Offense":
                    if not is_team:
                        # Performance stats moved to own cards at the top
                        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
                        with perf_col1:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center;">
                                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">ATTACK WIN RATE</div>
                                    <div style="font-size: 1.4rem; font-weight: bold; color: #22c55e;">58% <span style="font-size: 0.8rem; margin-left: 5px;">+4%</span></div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with perf_col2:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center;">
                                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">OPENING DUEL WR</div>
                                    <div style="font-size: 1.4rem; font-weight: bold; color: #3b82f6;">54% <span style="font-size: 0.8rem; margin-left: 5px;">+2%</span></div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with perf_col3:
                            st.markdown(
                                f"""
                                <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center;">
                                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">SPIKE PLANTER</div>
                                    <div style="font-size: 1.4rem; font-weight: bold; color: #ffffff;">{"Frequently" if tab_idx == 3 else "Rarely"}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with perf_col4:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center;">
                                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">LURK PROFILE</div>
                                    <div style="font-size: 1.4rem; font-weight: bold; color: #ffffff;">Low</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        st.markdown(
                            '<div style="margin-top: 20px;"></div>',
                            unsafe_allow_html=True,
                        )

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        if is_team:
                            st.markdown("#### Common Attack Routes")
                            st.markdown(
                                '<div style="height: 250px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Attack Route Heatmap Visualization]</div>',
                                unsafe_allow_html=True,
                            )
                            st.markdown("#### Common Plant Spots")
                            plant_col1, plant_col2 = st.columns([2, 1])
                            with plant_col1:
                                st.markdown(
                                    '<div style="height: 200px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Team Plant Spot Distribution]</div>',
                                    unsafe_allow_html=True,
                                )
                            with plant_col2:
                                st.markdown(
                                    """
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 200px;">
                                        <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px;">PLANT PREFERENCE</div>
                                        <ol style="margin: 0; padding-left: 20px; color: #ffffff; font-size: 0.85rem;">
                                            <li style="margin-bottom: 8px;"><b>Default A</b> (65%)</li>
                                            <li style="margin-bottom: 8px;"><b>Backsite B</b> (20%)</li>
                                            <li style="margin-bottom: 8px;"><b>Open A (Long)</b> (10%)</li>
                                            <li><b>Safe B Corner</b> (5%)</li>
                                        </ol>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            st.markdown("#### Bonus Round Offense Setup")
                            bonus_col1, bonus_col2 = st.columns([2, 1])
                            with bonus_col1:
                                st.markdown(
                                    '<div style="height: 200px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Bonus Round Attack Positions]</div>',
                                    unsafe_allow_html=True,
                                )
                            with bonus_col2:
                                st.markdown(
                                    """
                                    <div style="display: flex; flex-direction: column; gap: 10px; height: 200px;">
                                        <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                                            <div style="color: #94a3b8; font-size: 0.7rem; font-weight: bold; margin-bottom: 5px;">BONUS WEAPONS</div>
                                            <div style="font-size: 0.9rem; font-weight: bold;">Stinger / Bulldog</div>
                                        </div>
                                        <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                                            <div style="color: #94a3b8; font-size: 0.7rem; font-weight: bold; margin-bottom: 5px;">BONUS FRAG LEADER</div>
                                            <div style="font-size: 0.9rem; font-weight: bold;">Player 2</div>
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            st.markdown("#### Post-Plant Setups by Site")
                            st.markdown(
                                '<div style="height: 200px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Post-Plant Setup: Default vs Backsite]</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown("#### Attack Patterns & Utility")
                            ap_col1, ap_col2 = st.columns([2, 1])
                            with ap_col1:
                                st.markdown(
                                    '<div style="height: 250px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Attack Pattern: Abilites + Movement Map]</div>',
                                    unsafe_allow_html=True,
                                )
                            with ap_col2:
                                st.markdown(
                                    """
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 250px;">
                                        <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px;">UTILITY SEQUENCE</div>
                                        <ul style="margin: 0; padding-left: 18px; color: #ffffff; font-size: 0.85rem;">
                                            <li style="margin-bottom: 8px;">1. <b>Toxic Screen</b> (Site Split)</li>
                                            <li style="margin-bottom: 8px;">2. <b>Poison Cloud</b> (Entry Cover)</li>
                                            <li style="margin-bottom: 8px;">3. <b>Snake Bite</b> (Corner Clear)</li>
                                            <li>4. <b>Toxic Screen</b> (Post-plant Re-smoke)</li>
                                        </ul>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                            st.markdown("#### Common Plant Spots")
                            p_plant_col1, p_plant_col2 = st.columns([2, 1])
                            with p_plant_col1:
                                st.markdown(
                                    '<div style="height: 200px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Player Plant Spot Heatmap]</div>',
                                    unsafe_allow_html=True,
                                )
                            with p_plant_col2:
                                st.markdown(
                                    """
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 200px;">
                                        <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px;">PLANT PREFERENCE</div>
                                        <ol style="margin: 0; padding-left: 20px; color: #ffffff; font-size: 0.85rem;">
                                            <li style="margin-bottom: 8px;"><b>Default A</b> (72%)</li>
                                            <li style="margin-bottom: 8px;"><b>Safe B</b> (18%)</li>
                                            <li><b>Ninja Plant</b> (10%)</li>
                                        </ol>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                            st.markdown("#### Post-Plant Positioning")
                            pp_col1, pp_col2 = st.columns([2, 1])
                            with pp_col1:
                                st.markdown(
                                    '<div style="height: 200px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Post-Plant Spot Heatmap]</div>',
                                    unsafe_allow_html=True,
                                )
                            with pp_col2:
                                st.markdown(
                                    """
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 200px;">
                                        <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px;">COMMON POSITIONS</div>
                                        <ol style="margin: 0; padding-left: 20px; color: #ffffff; font-size: 0.85rem;">
                                            <li style="margin-bottom: 8px;"><b>A-Main (Long)</b></li>
                                            <li style="margin-bottom: 8px;"><b>A-Site (Backside)</b></li>
                                            <li style="margin-bottom: 8px;"><b>B-Main Entrance</b></li>
                                            <li><b>B-Back Pillar</b></li>
                                        </ol>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                            st.markdown("#### Common Lurk Routes")
                            st.markdown(
                                '<div style="height: 200px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Attack-Side Lurk Heatmap]</div>',
                                unsafe_allow_html=True,
                            )

                    with col2:
                        if is_team:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; margin-bottom: 15px; border-left: 4px solid #22c55e;">
                                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">ATTACK WIN RATE</div>
                                    <div style="font-size: 1.8rem; font-weight: bold; color: #22c55e;">58% <span style="font-size: 0.9rem; margin-left: 5px;">+4%</span></div>
                                </div>
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; margin-bottom: 15px;">
                                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">ATTACK TENDENCY</div>
                                    <div style="font-size: 1.1rem; font-weight: bold;">5-man Hits (72%)</div>
                                    <div style="color: #475569; font-size: 0.8rem;">vs Defaults (28%)</div>
                                </div>
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; margin-bottom: 15px;">
                                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">EARLY AGGRESSION</div>
                                    <div style="font-size: 1.1rem; font-weight: bold;">35% Contestation</div>
                                    <div style="color: #475569; font-size: 0.8rem;">Avg push: 0:15 into round</div>
                                </div>
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
                                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 5px;">ROTATION BEHAVIOR</div>
                                    <div style="font-size: 1.1rem; font-weight: bold;">Full Rotate (85%)</div>
                                    <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 2px;">Triggered immediately when site hit is stalled.</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    if is_team:
                        st.markdown("---")
                        pistol_map_col, pistol_text_col = st.columns([1, 1.5])
                        with pistol_map_col:
                            st.markdown(
                                '<div style="height: 250px; background-color: #0f172a; border-radius: 15px; display: flex; align-items: center; justify-content: center; border: 1px solid #3b82f6; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);">[Map: Attack Pistol Setup]</div>',
                                unsafe_allow_html=True,
                            )
                        with pistol_text_col:
                            st.markdown(
                                """
                                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 30px; border-radius: 15px; border: 1px solid #3b82f6; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2); position: relative; overflow: hidden; height: 250px;">
                                    <div style="position: absolute; top: 0; right: 0; padding: 10px 20px; background: #3b82f6; color: white; font-size: 0.7rem; font-weight: bold; border-bottom-left-radius: 15px; text-transform: uppercase; letter-spacing: 1px;">Pistol Strategy</div>
                                    <h4 style="margin: 0 0 20px 0; color: #ffffff; font-size: 1.4rem; letter-spacing: 0.5px;">Attack-Side Pistol Strategy</h4>
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                                        <div>
                                            <div style="color: #3b82f6; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">Standard Setup</div>
                                            <div style="font-size: 1.1rem; font-weight: bold; color: #ffffff;">4-man A-Main / 1 Mid</div>
                                            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 5px;">Spread to maximize info while maintaining trade potential.</div>
                                        </div>
                                        <div>
                                            <div style="color: #3b82f6; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">Utility</div>
                                            <ul style="margin: 0; padding-left: 18px; color: #ffffff; font-size: 0.85rem;">
                                                <li style="margin-bottom: 5px;">Double smoke Heaven</li>
                                                <li>Sova dart back-site</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                elif selection == "Defense":
                    if is_team:
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown("#### Common Defensive Setups")
                            st.write("- **Standard 2-1-2** on most maps")
                            st.write("- **Aggressive A Main push** on Ascent (45% frequency)")
                            st.markdown("#### Bonus Round Defense Setup")
                            st.markdown(
                                '<div style="height: 200px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Bonus Round Defense Positions]</div>',
                                unsafe_allow_html=True,
                            )
                            st.markdown("#### Vulnerabilities: Angles Opened on Death")
                            v_col1, v_col2 = st.columns([2, 1])
                            with v_col1:
                                st.markdown(
                                    '<div style="height: 200px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Vulnerabilities & Opened Angles]</div>',
                                    unsafe_allow_html=True,
                                )
                            with v_col2:
                                st.error(
                                    "- **If B Defender dies:** B Main to Market link is exposed."
                                )
                                st.error(
                                    "- **If Mid Defender dies:** A Short and B Link become vulnerable."
                                )
                        with col2:
                            st.metric("Defense Win Rate", "48%", "-2%")
                            st.write("**Site Preference:** Plays A Site (75%)")
                            st.write("**Retake Frequency:** High (Retakes 65% of lost sites)")
                            st.markdown("---")
                            st.warning(
                                "⚠️ **Vulnerability:** When Defender dies at B, Mid-to-B link is left completely open."
                            )

                        st.markdown("---")
                        st.markdown(
                            """
                            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 30px; border-radius: 15px; border: 1px solid #3b82f6; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2); position: relative; overflow: hidden;">
                                <div style="position: absolute; top: 0; right: 0; padding: 10px 20px; background: #3b82f6; color: white; font-size: 0.7rem; font-weight: bold; border-bottom-left-radius: 15px; text-transform: uppercase; letter-spacing: 1px;">Pistol Strategy</div>
                                <h4 style="margin: 0 0 20px 0; color: #ffffff; font-size: 1.4rem; letter-spacing: 0.5px;">Defense-Side Pistol Strategy</h4>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                                    <div>
                                        <div style="color: #3b82f6; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">Standard Setup</div>
                                        <div style="font-size: 1.1rem; font-weight: bold; color: #ffffff;">2-1-2 Passive Hold</div>
                                        <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 5px;">Playing for information and cross-fires rather than aggressive duels.</div>
                                    </div>
                                    <div>
                                        <div style="color: #3b82f6; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">Utility Holding</div>
                                        <ul style="margin: 0; padding-left: 18px; color: #ffffff; font-size: 0.9rem;">
                                            <li style="margin-bottom: 5px;"><b>Ghost/Classic</b> spam on common choke points</li>
                                            <li><b>Sentinel utility</b> placed deep to delay execution</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        # Player Defense Tab Redesign
                        st.markdown("#### Defense Utility Setup & Hold Patterns")
                        main_row_col1, main_row_col2 = st.columns([2, 1])

                        with main_row_col1:
                            # Top Map: Setups
                            st.markdown(
                                '<div style="height: 400px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b; margin-bottom: 20px;">[Map: Defense Setups & Hold Positions]</div>',
                                unsafe_allow_html=True,
                            )
                            # Bottom Map: Duel Locations (Restored)
                            st.markdown(
                                '<div style="height: 400px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Best Defensive Duel Locations]</div>',
                                unsafe_allow_html=True,
                            )

                        with main_row_col2:
                            # Vertically spaced cards to fill 820px total height
                            # (400 + 400 + 20 = 820)

                            # Row 1: Summary/Explanation (Increased height to 400px)
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; height: 400px; overflow-y: auto; margin-bottom: 20px;">
                                    <h5 style="margin:0; color: #22c55e; font-size: 1rem;">Sentinel Anchor Setup</h5>
                                    <p style="margin:0; font-size: 0.8rem; color: #94a3b8; margin-top: 5px;">Primary Traps: <b>Tripwire / Alarmbot</b></p>
                                    <p style="margin:0; font-size: 0.85rem; margin-top: 10px; line-height: 1.4;">
                                        Consistent use of <b>Tripwires</b> at A-Main and <b>Cyber Cage</b> for one-way info denial.
                                        This setup is active in 90% of defensive rounds on this site.
                                    </p>
                                    <hr style="border: 0; border-top: 1px solid #1e293b; margin: 15px 0;">
                                    <h5 style="margin:0; color: #22c55e; font-size: 1rem;">Retake Utility Prep</h5>
                                    <p style="margin:0; font-size: 0.85rem; margin-top: 10px; line-height: 1.4;">
                                        Keeps 1x <b>Cloudburst</b> and <b>Tailwind</b> specifically for retake commitment if site is lost early.
                                    </p>
                                    <hr style="border: 0; border-top: 1px solid #1e293b; margin: 15px 0;">
                                    <h5 style="margin:0; color: #22c55e; font-size: 1rem;">Communication Patterns</h5>
                                    <p style="margin:0; font-size: 0.85rem; margin-top: 10px; line-height: 1.4;">
                                        Prioritizes calling "contact" at A-Main 2 seconds before engaging.
                                        High tendency to ask for flash support from Mid.
                                    </p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            # Row 2: Hold Stats (Increased height to 400px total)
                            st.markdown(
                                """
                                <div style="display: flex; flex-direction: column; gap: 20px; height: 400px;">
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                                        <div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 10px;">Avg. Hold Time</div>
                                        <div style="font-weight: bold; font-size: 2.2rem; color: #ffffff;">24.5s</div>
                                    </div>
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                                        <div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 10px;">Hold Break Triggers</div>
                                        <div style="font-weight: bold; font-size: 0.95rem; color: #ffffff; line-height: 1.3;">
                                            Sound (40%)<br>Plant (35%)<br>Sight (25%)
                                        </div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            st.markdown("#### Common Flank Routes")
                            st.markdown(
                                '<div style="height: 200px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Defense-Side Flank Routes]</div>',
                                unsafe_allow_html=True,
                            )

                        st.markdown(
                            '<div style="margin-top: 30px;"></div>',
                            unsafe_allow_html=True,
                        )

                        # Bottom Row: 3 cards for Win Rate, Site Preference, Behavior
                        bottom_cols = st.columns(3)
                        bottom_data = [
                            {
                                "title": "Defense Win Rate",
                                "stat": "48%",
                                "trend": "-2%",
                            },
                            {
                                "title": "Site Preference",
                                "stat": "A Site (75%)",
                                "trend": "",
                            },
                            {"title": "Behavior", "stat": "Anchor", "trend": ""},
                        ]

                        for i, data in enumerate(bottom_data):
                            with bottom_cols[i]:
                                trend_html = (
                                    f'<span style="color: #ef4444; font-size: 0.8rem; margin-left: 8px;">{data["trend"]}</span>'
                                    if data["trend"]
                                    else ""
                                )
                                st.markdown(
                                    f"""
                                    <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; text-align: center; height: 120px; display: flex; flex-direction: column; justify-content: center;">
                                        <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">{data["title"]}</div>
                                        <div style="font-weight: bold; font-size: 1.4rem; color: #ffffff;">
                                            {data["stat"]}{trend_html}
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                elif selection == "Utility & Tendencies":
                    if is_team:
                        st.info("Utility analysis is detailed in individual player tabs.")
                    else:
                        st.markdown(
                            '<div style="margin-top: 10px;"></div>',
                            unsafe_allow_html=True,
                        )

                        # Row 1: Ability Profile, Ult Performance, and Signature Efficiency
                        util_row1_col1, util_row1_col2, util_row1_col3 = st.columns([1, 1, 1])
                        with util_row1_col1:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; height: 330px;">
                                    <h5 style="margin:0; color: #94a3b8; font-size: 0.85rem; margin-bottom: 20px;">Ability Usage Profile</h5>
                                    <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 15px;">
                                        <div style="color: #3b82f6; font-size: 0.75rem; font-weight: bold;">MOST USED</div>
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px;">
                                            <span style="font-size: 1.5rem; font-weight: bold;">Cloudburst</span>
                                            <span style="font-size: 1.2rem; color: #94a3b8;">6.1/gm</span>
                                        </div>
                                    </div>
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                        <div style="background: rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 8px; border: 1px solid #1e293b;">
                                            <div style="color: #94a3b8; font-size: 0.7rem;">2ND LEAST USED</div>
                                            <div style="font-weight: bold; margin-top: 5px;">Tailwind</div>
                                            <div style="color: #475569; font-size: 0.75rem;">1.2/gm</div>
                                        </div>
                                        <div style="background: rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 8px; border: 1px solid #1e293b;">
                                            <div style="color: #94a3b8; font-size: 0.7rem;">3RD LEAST USED</div>
                                            <div style="font-weight: bold; margin-top: 5px;">Updraft</div>
                                            <div style="color: #475569; font-size: 0.75rem;">0.8/gm</div>
                                        </div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with util_row1_col2:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; height: 330px;">
                                    <h5 style="margin:0; color: #94a3b8; font-size: 0.85rem; margin-bottom: 20px;">Ultimate Performance</h5>
                                    <div style="text-align: center; padding: 20px 0;">
                                        <div style="font-size: 3rem; font-weight: bold; color: #ffffff;">3.5</div>
                                        <div style="color: #94a3b8; font-size: 0.9rem;">Ults per Match</div>
                                    </div>
                                    <div style="background: rgba(34, 197, 94, 0.1); padding: 15px; border-radius: 8px; border: 1px solid rgba(34, 197, 94, 0.2); margin-top: 10px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center;">
                                            <span style="color: #22c55e; font-weight: bold;">Impact Value</span>
                                            <span style="color: #ffffff; font-weight: bold;">0.85 Kills/Usage</span>
                                        </div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with util_row1_col3:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; height: 330px;">
                                    <h5 style="margin:0; color: #94a3b8; font-size: 0.85rem; margin-bottom: 20px;">Signature Efficiency</h5>
                                    <div style="text-align: center; padding: 40px 0;">
                                        <div style="font-size: 3.5rem; font-weight: bold; color: #22c55e;">1.5x</div>
                                        <div style="color: #94a3b8; font-size: 1rem;">Average per Round</div>
                                    </div>
                                    <p style="font-size: 0.75rem; color: #475569; margin-top: 20px; text-align: center;">
                                        Maximum utility value extracted from signature ability resets.
                                    </p>
                                </div>
                                <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; margin-top: 15px;">
                                    <div style="color: #94a3b8; font-size: 0.7rem; font-weight: bold; margin-bottom: 5px;">LURK/FLANK FREQUENCY</div>
                                    <div style="font-size: 1.1rem; font-weight: bold;">Low (12% of rounds)</div>
                                    <div style="color: #475569; font-size: 0.75rem; margin-top: 2px;">Maintains group cohesion over solo play.</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        st.markdown(
                            '<div style="margin-top: 50px;"></div>',
                            unsafe_allow_html=True,
                        )

                        # Row 2: Usage Triggers (2/3 Width)
                        trig_col1, trig_col2 = st.columns([2, 1])
                        with trig_col1:
                            st.markdown(
                                """
                                <style>
                                    /* Target the Plotly chart container and its previous markdown sibling */
                                    [data-testid="stPlotlyChart"] {
                                        background-color: #0f172a !important;
                                        border: 1px solid #1e293b !important;
                                        border-top: none !important;
                                        border-radius: 0 0 10px 10px !important;
                                        padding: 0 20px 20px 20px !important;
                                        margin-top: -20px !important;
                                    }
                                    .chart-header {
                                        background-color: #0f172a;
                                        border: 1px solid #1e293b;
                                        border-bottom: none;
                                        border-radius: 10px 10px 0 0;
                                        padding: 20px 20px 0 20px;
                                    }
                                </style>
                                <div class="chart-header">
                                    <h5 style="margin:0; color: #94a3b8; font-size: 0.85rem;">Usage Triggers</h5>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            fig_triggers = go.Figure(
                                data=[
                                    go.Pie(
                                        labels=["Pre-emptive", "Reactionary"],
                                        values=[65, 35],
                                        hole=0.75,
                                        marker=dict(colors=["#3b82f6", "#1e293b"]),
                                        textinfo="percent",
                                        showlegend=True,
                                        domain={"x": [0, 0.35]},
                                    )
                                ]
                            )
                            fig_triggers.update_layout(
                                margin=dict(t=20, b=20, l=20, r=20),
                                height=280,
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#ffffff", size=12),
                                legend=dict(
                                    orientation="v",
                                    yanchor="middle",
                                    y=0.5,
                                    xanchor="left",
                                    x=0.45,
                                ),
                            )
                            st.plotly_chart(
                                fig_triggers,
                                width="stretch",
                                config={"displayModeBar": False},
                                key=f"triggers_{tab_idx}",
                            )

                        st.markdown(
                            '<div style="margin-top: 50px;"></div>',
                            unsafe_allow_html=True,
                        )

                        # Row 3: Spike Interaction (2/3 Width)
                        spike_col1, spike_col2 = st.columns([2, 1])
                        with spike_col1:
                            st.markdown(
                                """
                                <div class="chart-header">
                                    <h5 style="margin:0; color: #94a3b8; font-size: 0.85rem;">Spike Interaction</h5>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            fig_spike = go.Figure(
                                data=[
                                    go.Pie(
                                        labels=[
                                            "Defuse: Taps",
                                            "Defuse: Half",
                                            "Plant: Default",
                                            "Plant: Other",
                                        ],
                                        values=[45, 25, 20, 10],
                                        hole=0.75,
                                        marker=dict(
                                            colors=[
                                                "#3b82f6",
                                                "#60a5fa",
                                                "#1e293b",
                                                "#334155",
                                            ]
                                        ),
                                        textinfo="percent",
                                        showlegend=True,
                                        domain={"x": [0, 0.35]},
                                    )
                                ]
                            )
                            fig_spike.update_layout(
                                margin=dict(t=20, b=20, l=20, r=20),
                                height=280,
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#ffffff", size=12),
                                legend=dict(
                                    orientation="v",
                                    yanchor="middle",
                                    y=0.5,
                                    xanchor="left",
                                    x=0.45,
                                ),
                            )
                            st.plotly_chart(
                                fig_spike,
                                width="stretch",
                                config={"displayModeBar": False},
                                key=f"spike_{tab_idx}",
                            )

                elif selection == "Clutch & Economy":
                    if is_team:
                        # Row 1: Econ Graph (2/3) + Summary (1/3)
                        team_econ_col1, team_econ_col2 = st.columns([2, 1])
                        with team_econ_col1:
                            st.markdown("#### Win Rate by Economy State")
                            st.bar_chart(
                                {"Win Rate": [0.2, 0.45, 0.75, 0.8]},
                                x_label="Econ State (Eco, Force, Semi, Full)",
                            )
                        with team_econ_col2:
                            st.markdown("#### Graph Summary")
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; height: 300px; overflow-y: auto;">
                                    <h5 style="margin:0; color: #3b82f6; font-size: 1rem;">Team Economic Performance</h5>
                                    <p style="margin:0; font-size: 0.85rem; margin-top: 10px; line-height: 1.4;">
                                        The team shows a very strong <b>Full Buy</b> conversion rate (80%), suggesting high tactical discipline when fully equipped.
                                    </p>
                                    <p style="margin:0; font-size: 0.85rem; margin-top: 10px; line-height: 1.4;">
                                        <b>Force Buy</b> rounds (45%) are a significant vulnerability. Data suggests they often over-invest in utility without sufficient firepower, leading to lost trades.
                                    </p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        st.markdown(
                            '<div style="margin-top: 30px;"></div>',
                            unsafe_allow_html=True,
                        )

                        # Row 2: Buy Behavior (3 Horizontal Cards)
                        st.markdown("#### Buy Behavior & Economy")
                        team_synergy_cols = st.columns(3)
                        team_synergy_data = [
                            {"title": "Pistol Save Frequency", "stat": "65% (High)"},
                            {"title": "Force-Buy Rate", "stat": "35% (Medium)"},
                            {"title": "Preferred Team Gun", "stat": "Vandal (78%)"},
                        ]
                        for i, data in enumerate(team_synergy_data):
                            with team_synergy_cols[i]:
                                st.markdown(
                                    f"""
                                    <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; text-align: center; height: 120px; display: flex; flex-direction: column; justify-content: center;">
                                        <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">{data["title"]}</div>
                                        <div style="font-weight: bold; font-size: 1.2rem; color: #ffffff;">{data["stat"]}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        st.markdown(
                            '<div style="margin-top: 30px;"></div>',
                            unsafe_allow_html=True,
                        )

                        # Row 3: Man-Disadvantage Conversion (Pie Chart at Bottom)
                        st.markdown(
                            """
                            <style>
                                /* Target the Plotly chart container for Team Clutch */
                                [data-testid="stPlotlyChart"] {
                                    background-color: #0f172a !important;
                                    border: 1px solid #1e293b !important;
                                    border-top: none !important;
                                    border-radius: 0 0 10px 10px !important;
                                    padding: 0 20px 20px 20px !important;
                                    margin-top: -20px !important;
                                }
                                .chart-header {
                                    background-color: #0f172a;
                                    border: 1px solid #1e293b;
                                    border-bottom: none;
                                    border-radius: 10px 10px 0 0;
                                    padding: 20px 20px 0 20px;
                                }
                            </style>
                            <div class="chart-header">
                                <h5 style="margin:0; color: #94a3b8; font-size: 0.85rem;">Man-Disadvantage Conversion Rates</h5>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        fig_team_clutch = go.Figure(
                            data=[
                                go.Pie(
                                    labels=[
                                        "4v5 Conversion",
                                        "3v5 Conversion",
                                        "Other Rounds",
                                    ],
                                    values=[32, 12, 56],
                                    hole=0.75,
                                    marker=dict(colors=["#3b82f6", "#ef4444", "#1e293b"]),
                                    textinfo="percent",
                                    showlegend=True,
                                    domain={"x": [0, 0.35]},
                                )
                            ]
                        )
                        fig_team_clutch.update_layout(
                            margin=dict(t=20, b=20, l=20, r=20),
                            height=280,
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#ffffff", size=12),
                            legend=dict(
                                orientation="v",
                                yanchor="middle",
                                y=0.5,
                                xanchor="left",
                                x=0.45,
                            ),
                        )
                        st.plotly_chart(
                            fig_team_clutch,
                            width="stretch",
                            config={"displayModeBar": False},
                            key=f"team_clutch_{tab_idx}",
                        )
                    else:
                        # Row 1: Econ Graph (2/3) + Summary (1/3)
                        econ_col1, econ_col2 = st.columns([2, 1])
                        with econ_col1:
                            st.markdown("#### Win Rate by Economy State")
                            st.bar_chart(
                                {"Win Rate": [0.2, 0.45, 0.75, 0.8]},
                                x_label="Econ State (Eco, Force, Semi, Full)",
                            )
                        with econ_col2:
                            st.markdown("#### Graph Summary")
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; height: 300px; overflow-y: auto;">
                                    <h5 style="margin:0; color: #3b82f6; font-size: 1rem;">Economic Impact Analysis</h5>
                                    <p style="margin:0; font-size: 0.85rem; margin-top: 10px; line-height: 1.4;">
                                        Player shows extreme proficiency during <b>Full Buy</b> rounds, significantly outperforming the rank average.
                                    </p>
                                    <p style="margin:0; font-size: 0.85rem; margin-top: 10px; line-height: 1.4;">
                                        However, the <b>Eco</b> round win rate (20%) indicates a struggle to find impact with low-tier weaponry.
                                        Recommended focus: improving Sheriff/Marshal utility in save rounds.
                                    </p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        st.markdown(
                            '<div style="margin-top: 30px;"></div>',
                            unsafe_allow_html=True,
                        )

                        # Row 2: Team Synergy & Buy Behavior (4 Horizontal Cards)
                        st.markdown("#### Team Synergy & Buy Behavior")
                        synergy_cols = st.columns(4)
                        synergy_data = [
                            {"title": "Best Partners", "stat": "Player 3, 5"},
                            {"title": "Clutch Likelihood", "stat": "82% (High)"},
                            {"title": "Preferred Gun", "stat": "Vandal (78%)"},
                            {"title": "Buy Discipline", "stat": "Strict Save"},
                        ]
                        for i, data in enumerate(synergy_data):
                            with synergy_cols[i]:
                                st.markdown(
                                    f"""
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center; height: 100px; display: flex; flex-direction: column; justify-content: center;">
                                        <div style="color: #94a3b8; font-size: 0.75rem; margin-bottom: 5px;">{data["title"]}</div>
                                        <div style="font-weight: bold; font-size: 1rem; color: #ffffff;">{data["stat"]}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        st.markdown(
                            '<div style="margin-top: 30px;"></div>',
                            unsafe_allow_html=True,
                        )

                        # Row 3: Clutch Conversion Rates (Pie Chart at Bottom)
                        st.markdown(
                            """
                            <style>
                                /* Target the Plotly chart container for Clutch Conversion */
                                [data-testid="stPlotlyChart"] {
                                    background-color: #0f172a !important;
                                    border: 1px solid #1e293b !important;
                                    border-top: none !important;
                                    border-radius: 0 0 10px 10px !important;
                                    padding: 0 20px 20px 20px !important;
                                    margin-top: -20px !important;
                                }
                                .chart-header {
                                    background-color: #0f172a;
                                    border: 1px solid #1e293b;
                                    border-bottom: none;
                                    border-radius: 10px 10px 0 0;
                                    padding: 20px 20px 0 20px;
                                }
                            </style>
                            <div class="chart-header">
                                <h5 style="margin:0; color: #94a3b8; font-size: 0.85rem;">Clutch Conversion Rates (1vX)</h5>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        fig_clutch = go.Figure(
                            data=[
                                go.Pie(
                                    labels=[
                                        "1v1 Success",
                                        "1v2 Success",
                                        "1v3+ Success",
                                        "Failed Attempts",
                                    ],
                                    values=[45, 22, 5, 28],
                                    hole=0.75,
                                    marker=dict(
                                        colors=[
                                            "#22c55e",
                                            "#3b82f6",
                                            "#6366f1",
                                            "#1e293b",
                                        ]
                                    ),
                                    textinfo="percent",
                                    showlegend=True,
                                    domain={"x": [0, 0.35]},
                                )
                            ]
                        )
                        fig_clutch.update_layout(
                            margin=dict(t=20, b=20, l=20, r=20),
                            height=280,
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#ffffff", size=12),
                            legend=dict(
                                orientation="v",
                                yanchor="middle",
                                y=0.5,
                                xanchor="left",
                                x=0.45,
                            ),
                        )
                        st.plotly_chart(
                            fig_clutch,
                            width="stretch",
                            config={"displayModeBar": False},
                            key=f"clutch_{tab_idx}",
                        )

                elif selection == "Positions & Map Control":
                    if is_team:
                        st.markdown("#### Team Map Control & Coverage")
                        team_pos_col1, team_pos_col2 = st.columns([2, 1])
                        with team_pos_col1:
                            st.markdown(
                                '<div style="height: 400px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b; margin-bottom: 20px;">[Team Map Control & Rotation Paths Map]</div>',
                                unsafe_allow_html=True,
                            )
                        with team_pos_col2:
                            st.markdown(
                                """
                                <div style="display: flex; flex-direction: column; gap: 20px; height: 400px;">
                                    <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                                        <h5 style="margin:0; color: #94a3b8; font-size: 0.8rem; margin-bottom: 5px;">Safest Ult Orbs</h5>
                                        <p style="margin:0; font-weight: bold; font-size: 1.1rem; color: #3b82f6;">A Main (Ascent)</p>
                                        <p style="margin:0; font-weight: bold; font-size: 1.1rem; color: #3b82f6;">B Link (Bind)</p>
                                    </div>
                                    <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                                        <h5 style="margin:0; color: #94a3b8; font-size: 0.8rem; margin-bottom: 5px;">Positioning by Site</h5>
                                        <p style="margin:0; font-weight: bold; font-size: 1.2rem;">Balanced (2-1-2)</p>
                                        <p style="margin:0; font-size: 0.85rem; color: #94a3b8; margin-top: 5px;">High emphasis on Mid control during rounds 3-9.</p>
                                    </div>
                                    <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                                        <h5 style="margin:0; color: #94a3b8; font-size: 0.8rem; margin-bottom: 5px;">Map Control Coverage</h5>
                                        <p style="margin:0; font-weight: bold; font-size: 1.2rem; color: #22c55e;">72% Efficiency</p>
                                        <p style="margin:0; font-size: 0.85rem; color: #94a3b8; margin-top: 5px;">Low coverage on A-Long during defaults.</p>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    else:
                        # Redesigned Player Positioning: Map on left, stats in cards on right
                        st.markdown("#### Most Common Played Positions")
                        pos_row1_col1, pos_row1_col2 = st.columns([2, 1])
                        with pos_row1_col1:
                            st.markdown(
                                '<div style="height: 250px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Most Common Played Positions Map]</div>',
                                unsafe_allow_html=True,
                            )
                        with pos_row1_col2:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; margin-bottom: 10px; height: 120px; display: flex; flex-direction: column; justify-content: center;">
                                    <h5 style="margin:0; color: #94a3b8; font-size: 0.8rem;">Site Preference</h5>
                                    <p style="margin:0; font-weight: bold; font-size: 1.1rem;">A Site (75%)</p>
                                </div>
                                <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 120px; display: flex; flex-direction: column; justify-content: center;">
                                    <h5 style="margin:0; color: #94a3b8; font-size: 0.8rem;">Avg Rotation Time</h5>
                                    <p style="margin:0; font-weight: bold; font-size: 1.1rem;">12.4s (Site to Site)</p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        st.markdown("---")
                        st.markdown("#### Best Kill Locations & Successful Duel Angles")
                        pos_row2_col1, pos_row2_col2 = st.columns([2, 1])
                        with pos_row2_col1:
                            st.markdown(
                                '<div style="height: 350px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Best Kill Locations & Successful Duel Angles Map]</div>',
                                unsafe_allow_html=True,
                            )
                        with pos_row2_col2:
                            st.markdown(
                                """
                                <div style="display: flex; flex-direction: column; gap: 15px; height: 350px;">
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                                        <h5 style="margin:0; color: #94a3b8; font-size: 0.8rem;">Avg Angle Hold Time</h5>
                                        <p style="margin:0; font-weight: bold; font-size: 1.5rem;">28s</p>
                                    </div>
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; flex: 1.5; display: flex; flex-direction: column; justify-content: center;">
                                        <h5 style="margin:0; color: #94a3b8; font-size: 0.8rem; margin-bottom: 5px;">Hold Stop Triggers</h5>
                                        <p style="margin:0; font-size: 0.9rem; line-height: 1.4;">Enemy spotted (45%)<br>Utility/Flash (30%)<br>Noise elsewhere (25%)</p>
                                    </div>
                                    <div style="background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; flex: 1; display: flex; flex-direction: column; justify-content: center;">
                                        <h5 style="margin:0; color: #94a3b8; font-size: 0.8rem;">Common Death Pos</h5>
                                        <p style="margin:0; font-weight: bold; font-size: 1.2rem;">Mid (35%)</p>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                elif selection == "Strategies":
                    if is_team:
                        st.markdown("#### Macro Team Strategies")

                        # Macro Strategy 1
                        st.markdown(
                            """
                            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 15px; border: 1px solid #3b82f6; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1); margin-bottom: 10px;">
                                <div style="color: #3b82f6; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">Primary Playbook</div>
                                <h3 style="margin: 0 0 5px 0; color: #ffffff;">Strategy: 'The Fast A Split'</h3>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        with st.popover("Strategy Details", width="stretch"):
                            st.markdown(
                                """
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                                    <div style="color: #e2e8f0; font-size: 0.9rem; line-height: 1.5;">
                                        1. 2 Players Push A Main<br>
                                        2. 3 Players Push Tree/Garden<br>
                                        3. Coordinate smokes on Heaven
                                    </div>
                                    <div style="background: rgba(15, 23, 42, 0.5); padding: 10px; border-radius: 8px; border: 1px solid #1e293b; font-size: 0.8rem; color: #94a3b8;">
                                        Executed in 45% of offensive rounds. High success when executed within first 20s.
                                    </div>
                                </div>
                                <div style="margin-top: 20px; height: 300px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Fast A Split Execution]</div>
                                """,
                                unsafe_allow_html=True,
                            )

                        # Macro Strategy 2
                        st.markdown(
                            """
                            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 15px; border: 1px solid #3b82f6; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1); margin-bottom: 10px; margin-top: 20px;">
                                <div style="color: #3b82f6; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">Secondary Playbook</div>
                                <h3 style="margin: 0 0 5px 0; color: #ffffff;">Strategy: 'The Mid-to-B Pincer'</h3>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        with st.popover("Strategy Details", width="stretch"):
                            st.markdown(
                                """
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                                    <div style="color: #e2e8f0; font-size: 0.9rem; line-height: 1.5;">
                                        1. 1 Player hold B Main for info<br>
                                        2. 4 Players take Mid control<br>
                                        3. Split B through Market and B Main
                                    </div>
                                    <div style="background: rgba(15, 23, 42, 0.5); padding: 10px; border-radius: 8px; border: 1px solid #1e293b; font-size: 0.8rem; color: #94a3b8;">
                                        Counter to passive 2-1-2 setups. Forces Market defender into 1v2 situations.
                                    </div>
                                </div>
                                <div style="margin-top: 20px; height: 300px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Mid-to-B Pincer Execution]</div>
                                """,
                                unsafe_allow_html=True,
                            )

                        st.markdown(
                            '<div style="margin-top: 30px;"></div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown("#### Dynamic Strategy Changes")

                        # Scenario 1: Winning Heavily
                        st.markdown(
                            '<div style="color: #22c55e; font-weight: bold; margin-bottom: 10px;">When Winning Heavily (+6 Score Lead)</div>',
                            unsafe_allow_html=True,
                        )
                        dyn_col1, dyn_col2 = st.columns([2, 1])
                        with dyn_col1:
                            st.markdown(
                                '<div style="height: 250px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b; margin-bottom: 20px;">[Map: Aggressive Positioning & Mid Splits]</div>',
                                unsafe_allow_html=True,
                            )
                        with dyn_col2:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; height: 180px; margin-bottom: 10px;">
                                    <h5 style="margin:0; color: #22c55e; font-size: 0.9rem;">Hyper-Aggressive Macro</h5>
                                    <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 10px;">
                                        Team shifts to high-risk, high-reward plays.
                                        <b>Mid Control</b> is prioritized with 3+ players.
                                    </p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            with st.popover("Tactical Analysis", width="stretch"):
                                st.markdown(
                                    """
                                    <div style="font-size: 0.85rem; color: #e2e8f0; line-height: 1.5;">
                                        <b>Why it works:</b> Exploits enemy economic instability and psychological pressure.
                                        <br><br>
                                        <b>Key Indicators:</b> 3 players contesting Mid within 5 seconds of round start.
                                        <br><br>
                                        <b>Counter:</b> Play passive 3-Mid setup to punish over-aggression.
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        # Scenario 2: Losing / Stalled
                        st.markdown(
                            '<div style="color: #ef4444; font-weight: bold; margin-bottom: 10px; margin-top: 20px;">When Losing / Stalled</div>',
                            unsafe_allow_html=True,
                        )
                        dyn2_col1, dyn2_col2 = st.columns([2, 1])
                        with dyn2_col1:
                            st.markdown(
                                '<div style="height: 250px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b; margin-bottom: 20px;">[Map: Slow Default & Utility Baiting]</div>',
                                unsafe_allow_html=True,
                            )
                        with dyn2_col2:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; height: 180px; margin-bottom: 10px;">
                                    <h5 style="margin:0; color: #ef4444; font-size: 0.9rem;">Slow Default Transition</h5>
                                    <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 10px;">
                                        Switch to 1-3-1 defaults. Focus on baiting out Sentinel utility.
                                    </p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            with st.popover("Tactical Analysis", width="stretch"):
                                st.markdown(
                                    """
                                    <div style="font-size: 0.85rem; color: #e2e8f0; line-height: 1.5;">
                                        <b>Why it works:</b> Forces the defense to waste utility or reveal positions through impatience.
                                        <br><br>
                                        <b>Key Indicators:</b> No contact for first 45 seconds; heavy utility usage at choke points.
                                        <br><br>
                                        <b>Counter:</b> Deep info-utility (Sova dart, Fade prowler) to confirm site-commitment early.
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        st.markdown(
                            '<div style="margin-top: 30px;"></div>',
                            unsafe_allow_html=True,
                        )
                        strat_cols = st.columns(2)
                        with strat_cols[0]:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b;">
                                    <div style="color: #22c55e; font-weight: bold; margin-bottom: 5px;">Best Sites to Attack</div>
                                    <div style="font-size: 1.2rem; font-weight: bold;">A Site (62% Success Rate)</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with strat_cols[1]:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; border-left: 4px solid #3b82f6;">
                                    <div style="color: #3b82f6; font-weight: bold; margin-bottom: 5px;">Recommended Counter</div>
                                    <div style="font-size: 0.9rem;">Play Retake B. 85% plant success but only 40% hold success.</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    else:
                        st.markdown("#### Counter-Strategies & Matchups")

                        # Custom CSS for Strategy Cards with hover effect
                        st.markdown(
                            """
                            <style>
                            .strat-card-container {
                                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                                padding: 25px;
                                border-radius: 15px;
                                border: 1px solid #ef4444;
                                box-shadow: 0 4px 20px rgba(239, 68, 68, 0.1);
                                height: 180px;
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                width: 100%;
                                transition: transform 0.3s ease, box-shadow 0.3s ease;
                                margin-bottom: 15px;
                            }
                            .strat-card-container:hover {
                                transform: scale(1.03);
                                box-shadow: 0 10px 30px rgba(239, 68, 68, 0.2);
                                border-color: #f87171;
                            }
                            .strat-title {
                                color: #ffffff;
                                font-size: 1.2rem;
                                font-weight: bold;
                                margin: 0;
                            }
                            .strat-label {
                                color: #ef4444;
                                font-size: 0.75rem;
                                font-weight: bold;
                                margin-bottom: 10px;
                                text-transform: uppercase;
                                letter-spacing: 1px;
                            }
                            /* Make the popover look like a card */
                            [data-testid="stPopover"] {
                                width: 100%;
                            }
                            [data-testid="stPopover"] > div:first-child {
                                width: 100%;
                            }
                            [data-testid="stPopover"] button {
                                background-color: rgba(255, 255, 255, 0.05) !important;
                                border: 1px solid #1e293b !important;
                                padding: 10px !important;
                                width: 100% !important;
                                text-align: center !important;
                                border-radius: 8px !important;
                            }
                            [data-testid="stPopover"] button:hover {
                                background-color: rgba(255, 255, 255, 0.1) !important;
                                border-color: #3b82f6 !important;
                            }
                            [data-testid="stPopover"] button div p {
                                color: #ffffff !important;
                                font-weight: bold !important;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )

                        strat_row = st.columns(3)

                        # Anti-Player Strategy 1
                        with strat_row[0]:
                            st.markdown(
                                """
                                <div class="strat-card-container">
                                    <div class="strat-label">Anti-Player Strategy #1</div>
                                    <div class="strat-title">Exploit Over-Rotation</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            with st.popover("Execution Details", width="stretch"):
                                st.markdown("### Execution Guide: Exploit Over-Rotation")
                                st.markdown(
                                    """
                                    <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px;">
                                        This player has a <b>85% tendency</b> to rotate immediately upon hearing sound on the opposite site.
                                        <br><br>
                                        <b>How to Execute:</b> Use 2-man fakes with heavy utility (Omen smokes, Sova dart) to pull them out of position, then execute the empty site.
                                        <br><br>
                                        <b>Expected Outcome:</b> Player is caught in transition or site is completely abandoned.
                                    </div>
                                    <div style="height: 250px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Fake & Rotate Strategy]</div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        # Anti-Player Strategy 2
                        with strat_row[1]:
                            st.markdown(
                                """
                                <div class="strat-card-container">
                                    <div class="strat-label">Anti-Player Strategy #2</div>
                                    <div class="strat-title">Pressure Off-Angles</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            with st.popover("Execution Details", width="stretch"):
                                st.markdown("### Execution Guide: Pressure Off-Angles")
                                st.markdown(
                                    """
                                    <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px;">
                                        In 70% of defensive rounds, the player holds aggressive off-angles.
                                        <br><br>
                                        <b>How to Execute:</b> Do not dry-peek common anchor spots. Use <b>Breach Stuns</b> or <b>KAY/O Flashes</b> to clear deep angles before entry.
                                        <br><br>
                                        <b>Target Map Areas:</b> A-Short, B-Backsite, and Mid-Links.
                                    </div>
                                    <div style="height: 250px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Off-Angle Clear Path]</div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        # Anti-Player Strategy 3
                        with strat_row[2]:
                            st.markdown(
                                """
                                <div class="strat-card-container">
                                    <div class="strat-label">Anti-Player Strategy #3</div>
                                    <div class="strat-title">Neutralize Utility</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            with st.popover("Execution Details", width="stretch"):
                                st.markdown("### Execution Guide: Neutralize Utility")
                                st.markdown(
                                    """
                                    <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px;">
                                        The player heavily relies on <b>Sentinel traps</b> to hold B site.
                                        <br><br>
                                        <b>How to Execute:</b> Prioritize destroying <b>Tripwires</b> or <b>Alarmbots</b> early in the round using <b>Raze Paint Shells</b> or <b>Sova Shock Bolts</b>.
                                        <br><br>
                                        <b>Expected Outcome:</b> Without utility support, this player's win rate in duels drops by 30%.
                                    </div>
                                    <div style="height: 250px; background-color: #0f172a; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #1e293b;">[Map: Utility Destruction Setup]</div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        st.markdown(
                            '<div style="margin-top: 30px;"></div>',
                            unsafe_allow_html=True,
                        )

                        match_col1, match_col2 = st.columns(2)
                        with match_col1:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b;">
                                    <div style="color: #ef4444; font-weight: bold; margin-bottom: 10px;">Weak Agent Matchups</div>
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                        <span>vs Cypher</span> <span style="color: #ef4444; font-weight: bold;">40% WR</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between;">
                                        <span>vs Breach</span> <span style="color: #ef4444; font-weight: bold;">42% WR</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with match_col2:
                            st.markdown(
                                """
                                <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #1e293b;">
                                    <div style="color: #3b82f6; font-weight: bold; margin-bottom: 10px;">Preferred Duel Matchups</div>
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                        <span>vs Jett</span> <span style="color: #22c55e; font-weight: bold;">62% WR</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between;">
                                        <span>vs Reyna</span> <span style="color: #22c55e; font-weight: bold;">58% WR</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
