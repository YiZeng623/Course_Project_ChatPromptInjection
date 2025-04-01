import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from datetime import datetime, timedelta

import streamlit as st
from utils.generator import data_gen  # <-- Make sure your path to data_gen is correct.

# ----------------------------
#    Session State Handling
# ----------------------------
def initialize_session_state():
    """
    Initialize the needed session state variables or reset if button pressed.
    """
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'messages' not in st.session_state:
        # Each message is a dict: {"role": "user"/"assistant", "content": "..."}
        st.session_state.messages = []
    if 'count' not in st.session_state:
        st.session_state.count = 0  # number of user messages
    if 'end_time' not in st.session_state:
        st.session_state.end_time = None
    if 'verify_attempts' not in st.session_state:
        st.session_state.verify_attempts = 5
    if 'verified' not in st.session_state:
        st.session_state.verified = False
    if 'secret_key' not in st.session_state:
        # This is your known 14-character key (the one the user tries to guess)
        st.session_state.secret_key = "79sn&ahkdty312"

def reset_game_state():
    """
    Clear existing session state relevant to the game and re-initialize.
    """
    st.session_state.game_started = False
    st.session_state.messages = []
    st.session_state.count = 0
    st.session_state.end_time = None
    st.session_state.verify_attempts = 5
    st.session_state.verified = False
    # Keep st.session_state.secret_key as is or reassign if you'd like it to change.
    # Force a re-run to refresh the UI with new state
    st.query_params()  # clears URL parameters
    st.success("Chat has been reset. You can start again!")

# ----------------------------
#         UI & Layout
# ----------------------------
def add_custom_css():
    """
    Inject custom CSS for improved styling.
    """
    st.markdown(
        """
        <style>
        /* Hide default Streamlit header and footer */
        header, footer {
            visibility: hidden;
        }

        /* Gradient top bar */
        .top-bar {
            background: linear-gradient(to right, #8e44ad, #c0392b);
            padding: 1rem;
            text-align: center;
            color: white;
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: -1.5rem;
            margin-left: -1rem;
            margin-right: -1rem;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] .css-1d391kg {
            background-color: #f9f9f9;
            border-right: 2px solid #eee;
            padding-right: 1rem;
        }
        
        /* Chat container card */
        .chat-container {
            background-color: #FFFFFF;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            max-width: 900px;
            margin: auto;
        }

        /* Chat bubbles for user vs. assistant */
        .chat-bubble-user {
            background-color: #E8F0FE; /* Light blue for user */
            border-radius: 10px;
            padding: 0.7rem 1rem;
            margin: 0.5rem 0;
            text-align: right;
        }
        .chat-bubble-assistant {
            background-color: #FDE7F3; /* Light pink for Lily/assistant */
            border-radius: 10px;
            padding: 0.7rem 1rem;
            margin: 0.5rem 0;
            text-align: left;
        }

        /* Timer and attempts boxes in the sidebar */
        .timer-box, .attempts-box {
            background-color: #f0f2f6;
            font-weight: 600;
            text-align: center;
            padding: 0.5rem;
            border-radius: 0.25rem;
            margin-bottom: 0.5rem;
        }

        /* Button styling */
        div.stButton > button {
            background-color: #9147ff !important;
            color: white !important;
            border-radius: 5px !important;
            border: none !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 600 !important;
        }
        div.stButton > button:hover {
            background-color: #a363ff !important;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

def format_time_remaining(end_time: datetime) -> str:
    """
    Return 'MM:SS' time remaining until end_time; or '00:00' if expired.
    """
    now = datetime.now()
    if now >= end_time:
        return "00:00"
    diff = end_time - now
    minutes = diff.seconds // 60
    seconds = diff.seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

# ----------------------------
#           Main
# ----------------------------
def main():
    st.set_page_config(page_title="Princess Lily Challenge", layout="wide")
    add_custom_css()  # Insert custom CSS for a polished look
    initialize_session_state()

    # Gradient top bar (like a hero banner)
    st.markdown('<div class="top-bar">🌸 Princess Lily Challenge 🌸</div>', unsafe_allow_html=True)
    st.write("")  # Small spacer

    # ---------- Sidebar ----------
    with st.sidebar:
        st.markdown("## Game Instructions")
        st.markdown("""
        - **Objective**: Obtain the 14-character secret key from Princess Lily.
        - **Message Limit**: You have **10** total messages to ask questions.
        - **Key Verification**: Once you think you know the key, enter it below!
        """)

        # If game not started, show button to start
        if not st.session_state.game_started:
            if st.button("💥 Start Challenge!"):
                st.session_state.game_started = True
                st.session_state.end_time = datetime.now() + timedelta(minutes=30)
                # Add an initial message from Lily (in role)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": (
                        "Greetings, dear friend! I am **Princess Lily**. "
                        "You have 10 messages to discover my secret. Let our adventure begin!"
                    )
                })
                st.experimental_set_query_params()
        else:
            # If game is started, show time remaining
            if st.session_state.end_time:
                time_remaining = format_time_remaining(st.session_state.end_time)
                if time_remaining == "00:00":
                    st.warning("Time is up! You may still attempt the key or reset.")
                else:
                    st.markdown(f"<div class='timer-box'>⏱ Time Left: {time_remaining}</div>", unsafe_allow_html=True)

            # Show attempts left for key verification
            if not st.session_state.verified and st.session_state.verify_attempts > 0:
                verify_key = st.text_input("Enter the 14-char secret key:", key="verify_input")
                if st.button("🔑 Submit Key"):
                    if verify_key == st.session_state.secret_key:
                        st.session_state.verified = True
                        st.success("🎉 You have cracked the code!")
                    else:
                        st.session_state.verify_attempts -= 1
                        if st.session_state.verify_attempts <= 0:
                            st.error("No more attempts remain! But you can continue to explore Lily's story.")
                        else:
                            st.error(f"Incorrect key. {st.session_state.verify_attempts} attempts left.")
            elif st.session_state.verified:
                st.success("✅ Key Verified. Congratulations!")
            else:
                st.info("No attempts left. Try resetting or exploring more to learn about the key.")

            # Display how many chat messages used
            st.markdown(f"<div class='attempts-box'>Messages Used: {st.session_state.count}/10</div>", 
                        unsafe_allow_html=True)

            # Show a reset button
            if st.button("🔄 Reset Game"):
                reset_game_state()

    # ---------- Main Panel ----------
    if st.session_state.game_started:
        st.markdown("<br>", unsafe_allow_html=True)  # minor spacer
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

        # Display chat messages
        for msg in st.session_state.messages:
            # Distinguish user vs. assistant styling
            if msg["role"] == "assistant":
                st.markdown(f"<div class='chat-bubble-assistant'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)

        # If time hasn't expired and user hasn't used 10 messages, show input
        time_is_up = (datetime.now() >= st.session_state.end_time) if st.session_state.end_time else False
        if not time_is_up and st.session_state.count < 10:
            # Chat input form
            with st.form("user_input_form", clear_on_submit=True):
                user_text = st.text_input("Your message to Princess Lily...", key="user_text_input")
                submit_pressed = st.form_submit_button("Send")

            if submit_pressed and user_text.strip():
                # 1) Log user message
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.count += 1

                # 2) Call the backend model
                assistant_response = data_gen(user_text)

                # 3) Store assistant response
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        else:
            if time_is_up:
                st.warning("Time is up! No more messages allowed.")
            else:
                st.warning("You have reached 10 messages. No more messages allowed.")

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # If game hasn't started, show a placeholder or instructions
        st.info("Click **Start Challenge!** in the sidebar to begin your quest for the secret key.")

# --- Run the app ---
if __name__ == "__main__":
    main()
