import time

import streamlit as st


def render_chat_panel() -> None:
    """Renders the chatbot panel on the left side."""

    # Custom CSS for smaller text, smaller padding, and tighter lines
    st.markdown(
        """
        <style>
        .stChatMessage {
            padding: 0.5rem;
            margin-bottom: 0.2rem;
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 15px !important;
        }
        /* Right align user messages and constrain width */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
            flex-direction: row-reverse;
            text-align: right;
            margin-left: auto;
            max-width: 70%;
            width: fit-content;
            background-color: rgba(30, 41, 59, 0.9) !important;
        }
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stChatMessageContent {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        /* Hide user avatar */
        [data-testid="stChatMessageAvatarUser"] {
            display: none;
        }
        .stChatMessage [data-testid="stMarkdownContainer"] p {
            font-size: 0.85rem;
            line-height: 1.2;
            color: #ffffff !important;
        }
        .stCaptionContainer p {
            font-size: 0.75rem !important;
            margin-top: 0px !important;
            margin-bottom: 0px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            line-height: 1.0 !important;
            color: #94a3b8 !important;
        }
        .stCaptionContainer {
            margin-top: -15px !important;
            margin-bottom: -15px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
        }
        [data-testid="stVerticalBlock"] > div:has(.stCaptionContainer) {
            margin-top: -20px !important;
        }
        /* Custom styling for suggestion buttons */
        button[kind="secondary"] {
            font-size: 0.7rem !important;
            padding: 5px 15px !important;
            height: auto !important;
            min-height: 0px !important;
            margin-bottom: 5px !important;
            text-align: left !important;
            justify-content: flex-start !important;
            border-radius: 25px !important;
            background-color: #0f172a !important;
            color: #ffffff !important;
            border: 1px solid #1e293b !important;
        }
        button[kind="secondary"]:hover {
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }
        /* Chat box area styling */
        [data-testid="stChatInput"] {
            background-color: #020617 !important;
            border: 1px solid #1e293b !important;
            border-radius: 25px !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #ffffff !important;
        }
        /* Floating Chatbot Panel Styling */
        [data-testid="column"]:first-child > div {
            background: linear-gradient(180deg, #020617 0%, #000000 100%) !important;
            border: 2px solid #1e3a8a !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8) !important;
            padding: 15px !important;
            border-radius: 20px !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<h3 class="scout-assistant-title">Scout Assistant</h3>', unsafe_allow_html=True)

    # CSS for the title to remove top margin
    st.markdown(
        """
        <style>
        .scout-assistant-title {
            margin-top: -10px !important;
            padding-top: 0px !important;
            margin-bottom: 5px !important;
            font-size: 1.2rem !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Container for messages
    chat_container = st.container(height=500)

    with chat_container:
        for message in st.session_state.messages:
            avatar = "👤" if message["role"] == "assistant" else None
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Chat input at the bottom
    prompt = st.chat_input("Ask for insights...", disabled=st.session_state.processing)

    # Suggested inputs
    suggestions = [
        "Generate me a scouting report for Sentinels within the last 10 games",
        "Generate me a scouting report for Fnatic within the last 5 games",
        "Generate me a scouting report for G2 Esports within the last 20 games",
    ]

    # Vertical stack of suggestion buttons
    for i, suggestion in enumerate(suggestions):
        if st.button(
            suggestion,
            key=f"suggest_{i}",
            use_container_width=True,
            disabled=st.session_state.processing,
        ):
            prompt = suggestion

    if prompt:
        # Set processing to True and rerun to disable inputs immediately
        st.session_state.processing = True

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        st.rerun()

    # If we are processing, run the animation
    if st.session_state.processing and st.session_state.messages[-1]["role"] == "user":
        prompt = st.session_state.messages[-1]["content"]

        # 1.5 second delay before thinking
        time.sleep(1.5)

        # Assistant response with sequential "thinking" steps
        with chat_container:
            with st.chat_message("assistant", avatar="👤"):
                steps = [
                    "Filtering match history...",
                    "Parsing GRID telemetry artifacts...",
                    "Cross-referencing agent ability usage...",
                    "Identifying eco-round buy patterns...",
                    "Mapping first-blood heatmaps...",
                    "Detecting site rotation tendencies...",
                    "Evaluating post-plant utility timing...",
                    "Synthesizing tactical counters...",
                ]

                # Randomize delays but sum to 5.0 seconds
                import random

                total_time = 5.0
                # Generate random weights for each step
                weights = [random.uniform(0.1, 1.0) for _ in steps]
                total_weight = sum(weights)
                # Normalize weights to sum to total_time
                delays = [(w / total_weight) * total_time for w in weights]

                # Each step shows up as a new line with typewriter effect
                for i, step in enumerate(steps):
                    placeholder = st.empty()
                    typed_text = ""
                    # Calculate typing delay based on step delay and length
                    # We want to use most of the delay for typing
                    char_delay = delays[i] / len(step) if len(step) > 0 else 0.05
                    for char in step:
                        typed_text += char
                        placeholder.caption(typed_text)
                        time.sleep(char_delay)

                # Final "Done!" with typewriter effect
                done_text = "Done!"
                placeholder = st.empty()
                typed_done = ""
                for char in done_text:
                    typed_done += char
                    placeholder.markdown(f":green[{typed_done}]")
                    time.sleep(0.05)

                final_response = "Done!"

            st.session_state.messages.append({"role": "assistant", "content": final_response})
            st.session_state.processing = False
            st.rerun()
