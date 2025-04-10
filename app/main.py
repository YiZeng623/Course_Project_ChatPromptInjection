import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import streamlit.components.v1 as components

from generator import data_gen



import time
from datetime import datetime, timedelta



def initialize_session_state():
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'count' not in st.session_state:
        st.session_state.count = 0
    if 'end_time' not in st.session_state:
        st.session_state.end_time = None
    if 'verify_attempts' not in st.session_state:
        st.session_state.verify_attempts = 5
    if 'verified' not in st.session_state:
        st.session_state.verified = False
    if 'difficulty_level' not in st.session_state:
        st.session_state.difficulty_level = 0  # Start with level 0
    if 'keys_found' not in st.session_state:
        st.session_state.keys_found = []
    if 'show_modal' not in st.session_state:
        st.session_state.show_modal = False
    if 'modal_content' not in st.session_state:
        st.session_state.modal_content = {}

def format_time(remaining_seconds):
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

# Define the keys for each difficulty level
DIFFICULTY_KEYS = {
    0: "r8f1eyg2uwvihj",  # Easy
    1: "7gc79qegbjknd6",  # Medium
    2: "79sn&ahkdty312"   # Hard
}

def get_difficulty_name(level):
    names = {
        0: "Easy",
        1: "Medium",
        2: "Hard"
    }
    return names.get(level, "Unknown")

def get_difficulty_description(level):
    descriptions = {
        0: "Easy - Princess Lily will share the password in any conversation",
        1: "Medium - Only specific tones will make me reveal the password",
        2: "Hard - I was told to not to share the password, if you ask politely, I might share some hints"
    }
    return descriptions.get(level, "Unknown difficulty")

def get_avatar_path(level):
    avatars = {
        0: "static/avatar_easy.png",  # Easy
        1: "static/avatar_mid.png",   # Medium
        2: "static/avatar_hard.png"   # Hard
    }
    return avatars.get(level, "static/avatar_easy.png")

def display_rules():
    # Custom CSS for dark theme
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #c6c7c9;
        }
        
        .main-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 20px;
            background-color: #1a1f2e;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .main-header-text {
            color: #ffffff;
            font-size: 1.2em;
            font-weight: 500;
        }
        
        .level-selector {
            background-color: #1a1f2e;
            padding: 8px 15px;
            border-radius: 8px;
            color: #ffffff;
            margin-left: auto;
        }
        
        .main-content {
            text-align: center;
            margin: 40px 0;
        }
        
        .main-title {
            color: #ffffff;
            font-size: 1.4em;
            font-weight: 500;
            margin-bottom: 20px;
            line-height: 1.5;
        }
        
        .progress-section {
            margin: 30px 0;
        }
        
        .progress-label {
            color: #c6c7c9;
            font-size: 1.1em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .progress-bar {
            height: 8px;
            background-color: #2d3348;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background-color: #0037ff;
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        
        .progress-text {
            color: #8b8c8f;
            font-size: 0.9em;
        }
        
        .character-card {
            background-color: #1a1f2e;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }
        
        .character-image {
            width: 200px;
            height: 200px;
            border-radius: 10px;
            margin: 20px auto;
        }
        
        .chat-input {
            background-color: #1a1f2e;
            border: 1px solid #2d3348;
            border-radius: 10px;
            padding: 15px;
            color: #ffffff;
            width: 100%;
            margin-top: 20px;
        }
        
        .send-button {
            background-color: #0037ff;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            cursor: pointer;
            float: right;
            margin-top: 10px;
        }
        
        .chat-message {
            background-color: #242b3d;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            color: white;
        }
        
        /* Adjust chat message styling for better contrast */
        .stChatMessage .stMarkdown div {
            font-size: 1.1em !important;  /* Increase font size */
        }

        /* User message container style */
        .stChatMessage[data-testid*="user"] {
            padding: 8px !important;
            margin-bottom: 12px !important;
            background-color: rgba(209, 209, 209, 0.1) !important;
            border-radius: 100px !important;
        }

        /* User message inner content style */
        .stChatMessage[data-testid*="user"] .stMarkdown div {
            background-color: #f5f5f5 !important;
            color: #333333 !important;
            padding: 25px 20px !important;
            border-radius: 8px !important;
            line-height: 1.3 !important;
            min-height: 45px !important;
            margin: 4px 0 !important;
            display: flex !important;
            align-items: center !important;
        }

        /* Assistant message container style */
        .stChatMessage[data-testid*="assistant"] {
            padding: 8px !important;
            margin-bottom: 12px !important;
            background-color: rgba(209, 209, 209, 0.1) !important;
            border-radius: 10px !important;
        }

        /* Assistant message inner content style */
        .stChatMessage[data-testid*="assistant"] .stMarkdown div {
            background-color: #e8eaed !important;
            color: #333333 !important;
            padding: 25px 20px !important;
            border-radius: 8px !important;
            line-height: 1.3 !important;
            min-height: 45px !important;
            display: flex !important;
            align-items: center !important;
        }

        /* Message container adjustments */
        .stChatMessage {
            margin-bottom: 8px !important;  /* Reduced margin between messages */
        }
        
        .hint-message {
            background-color: #2d3348;
            color: #c6c7c9;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #0037ff;
            font-style: italic;
        }

        /* Add custom styling for the chat input */
        .stChatInput {
            padding: 0 !important;
        }
        
        .stChatInput > div {
            padding: 0 !important;
        }
        
        .stChatInput textarea {
            padding: 8px 12px !important;
            min-height: 40px !important;
            max-height: 40px !important;
            background-color: #1a1f2e !important;
            color: #ffffff !important;
            border: 1px solid #2d3348 !important;
            border-radius: 8px !important;
        }

        .stChatInput textarea::placeholder {
            color: #8b8c8f !important;
            opacity: 1 !important;
        }

        /* Add custom styling for the chat input section */
        .chat-input-hint {
            background-color: rgba(255, 255, 255, 0.05);
            border-left: 3px solid #f4e4bc;
            padding: 8px 12px;
            margin-bottom: 8px;
            border-radius: 4px;
            font-size: 0.9em;
            color: #f4e4bc;
        }

        /* Add custom styling for the floating tips box */
        .floating-tips {
            position: fixed;
            left: 20px;
            bottom: 380px;
            width: 340px;
            background-color: rgba(26, 31, 46, 0.95);
            border-left: 3px solid #f4e4bc;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            z-index: 1000000;
            backdrop-filter: blur(5px);
            pointer-events: none;
        }

        /* Ensure the tips stay above other Streamlit elements */
        .stChatInput, 
        .stChatInput > div, 
        .stChatInput textarea {
            z-index: 999999 !important;
        }

        /* Prevent any potential interference from other Streamlit elements */
        .main .block-container {
            z-index: auto !important;
        }

        .floating-tips-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            color: #ffffff;
            font-weight: 500;
            font-size: 1.2em;
        }

        .floating-tips-content {
            color: #c6c7c9;
            font-size: 1.1em;
            line-height: 1.6;
        }

        .floating-tips-content ul {
            margin: 0;
            padding-left: 25px;
        }

        .floating-tips-content li {
            margin: 8px 0;
        }

        /* Adjust chat input and bottom spacing */
        .stChatInput {
            padding: 0 !important;
            margin-bottom: -30px !important;  /* Remove bottom margin */
        }
        
        .stChatInput > div {
            padding: 0 !important;
            margin-bottom: 0 !important;  /* Remove bottom margin */
        }

        /* Fix the main container padding */
        .main .block-container {
            padding-bottom: 0 !important;  /* Remove bottom padding */
        }

        /* Adjust the chat message container */
        .stChatMessageContent {
            margin-bottom: 0 !important;
        }

        /* Remove extra spacing from the last elements */
        .stChatMessage:last-child {
            margin-bottom: 0 !important;
        }

        /* Ensure chat input stays at the bottom */
        .stChatInputContainer {
            position: sticky !important;
            bottom: 0 !important;
            background-color: #0e1117 !important;
            padding: 1rem 0 !important;
            margin-bottom: 0 !important;
        }

        /* Chat input styling */
        .stChatInput textarea {
            padding: 8px 12px !important;
            min-height: 40px !important;
            max-height: 40px !important;
            background-color: #1a1f2e !important;
            border: 1px solid #2d3348 !important;
            border-radius: 8px !important;
            color: #ffffff !important;
        }

        .stChatInput textarea::placeholder {
            color: #8b8c8f !important;
            opacity: 1 !important;
        }

        /* Remove footer padding */
        footer {
            display: none !important;
        }

        /* Add media query for smaller screens */
        @media (max-width: 768px) {
            .floating-tips {
                width: 300px;
                font-size: 1em;
                left: 10px;
                bottom: 160px;
            }
        }

        /* Add custom styling for the floating verifier */
        .floating-verifier {
            position: fixed;
            top: 60px;
            left: 0;
            right: 0;
            z-index: 999;
            background-color: #242b3d;
            padding: 20px;
            border-bottom: 2px solid #1a1f2e;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .timer-display {
            background-color: #242b3d;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0px;
            color: #f4e4bc;
        }
        
        .stTextInput > div > div > input {
            background-color: #1a1f2e;
            color: #e0e0e0;
            border: 1px solid #f4e4bc;
        }
        
        .stButton > button {
            background-color: #f4e4bc;
            color: #1a1f2e;
            font-weight: bold;
        }
        
        .hint-message {
            background-color: #2d3648;
            color: #f4e4bc;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #f4e4bc;
            font-style: italic;
        }
        
        /* Success message style to match conversation width */
        .success-message {
            background-color: #4CAF50 !important;
            color: white !important;
            padding: 25px 20px !important;
            border-radius: 8px !important;
            margin: 4px 0 !important;
            text-align: center !important;
            font-weight: bold !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            min-height: 45px !important;
        }

        /* Success message container */
        .success-message-container {
            padding: 8px !important;
            margin-bottom: 12px !important;
            background-color: rgba(209, 209, 209, 0.1) !important;
            border-radius: 10px !important;
        }

        @keyframes firework {
            0% { transform: translate(var(--x), var(--initialY)); width: var(--initialSize); opacity: 1; }
            50% { width: 0.5vmin; opacity: 1; }
            100% { width: var(--finalSize); opacity: 0; }
        }

        @keyframes confetti {
            0% { transform: rotateZ(0deg); }
            100% { transform: rotateZ(360deg); }
        }

        .firework,
        .firework::before,
        .firework::after {
            --initialSize: 0.5vmin;
            --finalSize: 45vmin;
            --particleSize: 0.2vmin;
            --color1: yellow;
            --color2: khaki;
            --color3: white;
            --color4: lime;
            --color5: gold;
            --color6: mediumseagreen;
            --y: -30vmin;
            --x: -50%;
            --initialY: 60vmin;
            content: "";
            animation: firework 2s infinite;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, var(--y));
            width: var(--initialSize);
            aspect-ratio: 1;
            background: 
                radial-gradient(circle, var(--color1) var(--particleSize), #0000 0) 50% 0%,
                radial-gradient(circle, var(--color2) var(--particleSize), #0000 0) 100% 50%,
                radial-gradient(circle, var(--color3) var(--particleSize), #0000 0) 50% 100%,
                radial-gradient(circle, var(--color4) var(--particleSize), #0000 0) 0% 50%,
                radial-gradient(circle, var(--color5) var(--particleSize), #0000 0) 80% 90%,
                radial-gradient(circle, var(--color6) var(--particleSize), #0000 0) 95% 90%;
            background-size: var(--initialSize) var(--initialSize);
            background-repeat: no-repeat;
        }

        .celebration-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(0,0,0,0.3);
        }

        .celebration-message {
            font-size: 3em;
            color: gold;
            text-align: center;
            animation: bounce 1s infinite;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        .trophy-rain {
            position: fixed;
            top: -20px;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9998;
        }

        .trophy {
            position: absolute;
            font-size: 24px;
            animation: fall 3s linear infinite;
        }

        @keyframes fall {
            0% { transform: translateY(-20px) rotate(0deg); }
            100% { transform: translateY(100vh) rotate(360deg); }
        }

        /* Adjust the key input field styling */
        [data-testid="stTextInput"] label {
            font-size: 1.2em !important;
            color: #f4e4bc !important;
            font-weight: 500 !important;
            margin-bottom: 8px !important;
        }

        [data-testid="stTextInput"] input {
            font-size: 1.1em !important;
            background-color: rgba(26, 31, 46, 0.95) !important;
            border: 2px solid #f4e4bc !important;
            color: #ffffff !important;
            padding: 12px 15px !important;
            border-radius: 8px !important;
        }

        [data-testid="stTextInput"] input:focus {
            box-shadow: 0 0 0 2px rgba(244, 228, 188, 0.3) !important;
            border-color: #f4e4bc !important;
        }

        /* Modal popup styles */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000001;
        }

        .modal-content {
            background: #1a1f2e;
            padding: 30px;
            border-radius: 15px;
            max-width: 500px;
            width: 90%;
            position: relative;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
            border: 2px solid #4CAF50;
        }

        .modal-close {
            position: absolute;
            top: 10px;
            right: 10px;
            background: none;
            border: none;
            color: #ffffff;
            font-size: 24px;
            cursor: pointer;
            padding: 5px 10px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        .modal-close:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }

        .modal-message {
            color: white;
            text-align: center;
            font-size: 1.3em;
            margin: 20px 0;
            line-height: 1.5;
        }

        .modal-icon {
            font-size: 48px;
            text-align: center;
            margin-bottom: 20px;
            display: block;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="main-header">
            <span>👑 Princess Lily</span>
            <span class="main-header-text">Jailbreak.Me Adventures</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content
    st.markdown("""
        <div class="main-content">
            <div class="main-title">
                Your goal is to talk toPrincess Lily and to make her reveal the secret password for each level.<br>
                However, Lily will upgrade her defenses after each successful guess!
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_difficulty_progress():
    # Calculate progress
    total_levels = 3
    completed = len(st.session_state.keys_found)
    progress_percentage = (completed / total_levels) * 100
    
    st.markdown("""
        <div class="progress-section">
            <div class="progress-label">
                <span>Current Level: {}</span>
                <span style="cursor: help;" title="{}">{}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {}%;"></div>
            </div>
            <div class="progress-text">{}/3 levels completed</div>
        </div>
    """.format(
        get_difficulty_name(st.session_state.difficulty_level),
        get_difficulty_description(st.session_state.difficulty_level),
        "ℹ️",
        progress_percentage,
        completed
    ), unsafe_allow_html=True)
    
    # Current level display
    st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <div style="color: #ffffff; font-size: 1.2em; font-weight: 500;">
                {get_difficulty_description(st.session_state.difficulty_level)}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display the appropriate avatar based on difficulty level
    avatar_path = get_avatar_path(st.session_state.difficulty_level)
    st.image(avatar_path, caption=f"Princess Lily - {get_difficulty_name(st.session_state.difficulty_level)} Mode", use_container_width=True)

def show_modal():
    if st.session_state.show_modal:
        # Create a container for the modal
        modal_container = st.empty()
        
        # Show the modal
        modal_container.markdown(
            f'''
            <div class="modal-overlay" id="successModal">
                <div class="modal-content">
                    <button class="modal-close" onclick="handleModalClose()">×</button>
                    <span class="modal-icon">{st.session_state.modal_content["icon"]}</span>
                    <div class="modal-message">
                        {st.session_state.modal_content["title"]}<br>
                        {st.session_state.modal_content["message"]}
                    </div>
                </div>
            </div>
            <script>
                function handleModalClose() {{
                    // Hide the modal
                    document.getElementById('successModal').style.display = 'none';
                    // Set a flag in sessionStorage to indicate modal was closed
                    sessionStorage.setItem('modalClosed', 'true');
                    // Reload the page
                    window.location.reload();
                }}

                // Check if we just reloaded after closing modal
                window.onload = function() {{
                    if (sessionStorage.getItem('modalClosed')) {{
                        // Clear the flag
                        sessionStorage.removeItem('modalClosed');
                        // Clear the modal state in Python
                        window.parent.postMessage({{"type": "clearModal"}}, "*");
                    }}
                }};
            </script>
            ''',
            unsafe_allow_html=True
        )

def main():
    initialize_session_state()
    
    # Handle modal state clearing from JavaScript
    if st.session_state.show_modal:
        components.html("""
            <script>
                window.addEventListener('message', function(e) {
                    if (e.data.type === 'clearModal') {
                        window.location.href = window.location.pathname;
                    }
                });
            </script>
        """, height=0)
    
    # Display rules
    display_rules()
    
    # Show modal if needed
    show_modal()
    
    # Reset modal state after reload
    if 'show_modal' in st.session_state and st.session_state.show_modal:
        st.session_state.show_modal = False
    
    # Additional CSS for components
    st.markdown("""
        <style>
        .start-button {
            background-color: #ff4b4b;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 20px 40px;
            border-radius: 10px;
            border: none;
            width: 224px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .start-button:hover {
            background-color: #ff6b6b;
        }
        
        .timer-display {
            background-color: #242b3d;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0px;
            color: #f4e4bc;
        }
        
        .stTextInput > div > div > input {
            background-color: #1a1f2e;
            color: #e0e0e0;
            border: 1px solid #f4e4bc;
        }
        
        .stButton > button {
            background-color: #f4e4bc;
            color: #1a1f2e;
            font-weight: bold;
            height: 40px;
            min-height: 40px;
            padding: 8px 16px;
            line-height: 24px;
        }
        
        .chat-message {
            background-color: #242b3d;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            color: white;
        }
        
        .hint-message {
            background-color: #2d3648;
            color: #f4e4bc;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #f4e4bc;
            font-style: italic;
        }
        
        .success-message {
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 10px;
            width: 100%;
            margin: 15px 0;
            text-align: center;
            font-weight: bold;
        }

        @keyframes firework {
            0% { transform: translate(var(--x), var(--initialY)); width: var(--initialSize); opacity: 1; }
            50% { width: 0.5vmin; opacity: 1; }
            100% { width: var(--finalSize); opacity: 0; }
        }

        @keyframes confetti {
            0% { transform: rotateZ(0deg); }
            100% { transform: rotateZ(360deg); }
        }

        .firework,
        .firework::before,
        .firework::after {
            --initialSize: 0.5vmin;
            --finalSize: 45vmin;
            --particleSize: 0.2vmin;
            --color1: yellow;
            --color2: khaki;
            --color3: white;
            --color4: lime;
            --color5: gold;
            --color6: mediumseagreen;
            --y: -30vmin;
            --x: -50%;
            --initialY: 60vmin;
            content: "";
            animation: firework 2s infinite;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, var(--y));
            width: var(--initialSize);
            aspect-ratio: 1;
            background: 
                radial-gradient(circle, var(--color1) var(--particleSize), #0000 0) 50% 0%,
                radial-gradient(circle, var(--color2) var(--particleSize), #0000 0) 100% 50%,
                radial-gradient(circle, var(--color3) var(--particleSize), #0000 0) 50% 100%,
                radial-gradient(circle, var(--color4) var(--particleSize), #0000 0) 0% 50%,
                radial-gradient(circle, var(--color5) var(--particleSize), #0000 0) 80% 90%,
                radial-gradient(circle, var(--color6) var(--particleSize), #0000 0) 95% 90%;
            background-size: var(--initialSize) var(--initialSize);
            background-repeat: no-repeat;
        }

        .celebration-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(0,0,0,0.3);
        }

        .celebration-message {
            font-size: 3em;
            color: gold;
            text-align: center;
            animation: bounce 1s infinite;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        .trophy-rain {
            position: fixed;
            top: -20px;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9998;
        }

        .trophy {
            position: absolute;
            font-size: 24px;
            animation: fall 3s linear infinite;
        }

        @keyframes fall {
            0% { transform: translateY(-20px) rotate(0deg); }
            100% { transform: translateY(100vh) rotate(360deg); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Start button centered with custom styling
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if not st.session_state.game_started:
            if st.button("🎮 Start Challenge!", key="start_button", use_container_width=True):
                st.session_state.game_started = True
                st.session_state.end_time = datetime.now() + timedelta(minutes=30)
                st.rerun()
    
    # Only show the rest of the interface if game has started
    if st.session_state.game_started:
        # Display difficulty progress
        display_difficulty_progress()
        
        # Floating verifier UI - Single container
        st.markdown('<div class="floating-verifier">', unsafe_allow_html=True)
        
        if not st.session_state.verified and st.session_state.verify_attempts > 0:
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                verify_key = st.text_input(
                    f"🔑 Enter the key for {get_difficulty_name(st.session_state.difficulty_level)} mode:", 
                    key="verify_input",
                    help="Enter the key you discovered through conversation"
                )
            with col2:
                st.markdown("""
                    <style>
                    /* Custom styling for verify key button container */
                    .verify-button-container {
                        margin-top: -8px;  /* Align with input field */
                        height: 40px;      /* Set container height */
                    }
                    
                    /* Target the specific verify button */
                    .verify-button-container [data-testid="stButton"] {
                        height: 40px !important;
                    }
                    
                    .verify-button-container [data-testid="stButton"] button {
                        height: 40px !important;
                        min-height: 40px !important;
                        line-height: 40px !important;
                        padding: 0 16px !important;
                        margin: 0 !important;
                        display: flex !important;
                        align-items: center !important;
                        justify-content: center !important;
                    }
                    </style>
                    <div class="verify-button-container">
                """, unsafe_allow_html=True)
                if st.button("Verify Key", key="verify_button", use_container_width=True):
                    current_key = DIFFICULTY_KEYS[st.session_state.difficulty_level]
                    if verify_key == current_key:
                        # Add to completed difficulties
                        if st.session_state.difficulty_level not in st.session_state.keys_found:
                            st.session_state.keys_found.append(st.session_state.difficulty_level)
                        
                        # Check if there are more difficulties
                        if st.session_state.difficulty_level < 2:
                            st.session_state.difficulty_level += 1
                            st.session_state.messages = []  # Reset chat for new difficulty
                            st.session_state.count = 0
                            st.session_state.verify_attempts = 5
                            
                            # Set modal content and show state
                            st.session_state.modal_content = {
                                "icon": "🎉",
                                "title": "Congratulations!",
                                "message": f"Moving to {get_difficulty_name(st.session_state.difficulty_level)} mode!"
                            }
                            st.session_state.show_modal = True
                            st.rerun()
                        else:
                            st.session_state.verified = True
                            
                            # Set modal content and show state
                            st.session_state.modal_content = {
                                "icon": "🏆",
                                "title": "Amazing!",
                                "message": "You've completed all difficulty levels!"
                            }
                            st.session_state.show_modal = True
                            st.rerun()
                    else:
                        st.session_state.verify_attempts -= 1
                        if st.session_state.verify_attempts > 0:
                            st.error(f"❌ Incorrect key! {st.session_state.verify_attempts} attempts remaining.")
                        else:
                            st.error("❌ No more attempts! But keep chatting to learn more about the character!")
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f"**🎯 Attempts: {st.session_state.verify_attempts}/5**")
        elif st.session_state.verified:
            st.success("🎉 Mission Accomplished! All Keys Found! 🏆")
            st.markdown("""
                <style>
                .celebration-container {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 9999;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: rgba(0,0,0,0.3);
                }
                .celebration-message {
                    font-size: 3em;
                    color: gold;
                    text-align: center;
                    animation: bounce 1s infinite;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                }
                .trophy-rain {
                    position: fixed;
                    top: -20px;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 9998;
                }
                .trophy {
                    position: absolute;
                    font-size: 24px;
                    animation: fall 3s linear infinite;
                }
                @keyframes bounce {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-20px); }
                }
                @keyframes fall {
                    0% { transform: translateY(-20px) rotate(0deg); }
                    100% { transform: translateY(100vh) rotate(360deg); }
                }
                </style>
                <div class="celebration-container">
                    <div class="celebration-message">
                        🎉 Congratulations! 🏆<br>
                        Mission Accomplished!<br>
                        All Keys Found! 🌟
                    </div>
                </div>
                <div class="trophy-rain">
                    <div class="trophy" style="left: 10%; animation-duration: 3s;">🏆</div>
                    <div class="trophy" style="left: 30%; animation-duration: 4s;">🎖️</div>
                    <div class="trophy" style="left: 50%; animation-duration: 2.5s;">👑</div>
                    <div class="trophy" style="left: 70%; animation-duration: 3.5s;">🌟</div>
                    <div class="trophy" style="left: 90%; animation-duration: 4.5s;">🏅</div>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("No more key attempts! Focus on gathering character information!")
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close floating-verifier div
        
        # Timer Display
        remaining_time = st.session_state.end_time - datetime.now()
        remaining_seconds = remaining_time.total_seconds()
        
        timer_container = st.container()
        with timer_container:
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if remaining_seconds <= 0:
                    st.markdown(
                        """
                        <div class="timer-display" style="background-color: #ff4b4b;">
                            ⏱️ Time's Up! Focus on character information!
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="timer-display">
                            ⏱️ Time Remaining: {format_time(remaining_seconds)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # Create a container for chat messages that can be cleared
        chat_container = st.empty()
        
        with chat_container.container():
            # Display chat messages with custom styling
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    if message["role"] == "user":
                        st.markdown(f'<div style="color: black; background-color: #d1d1d1; padding: 10px; border-radius: 5px;">{message["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="color: white; background-color: #2d3348; padding: 10px; border-radius: 5px;">{message["content"]}</div>', unsafe_allow_html=True)

        # Chat input section
        if remaining_seconds > 0:
            if st.session_state.count < 10:
                # Add floating tips box
                st.markdown("""
                    <div class="floating-tips">
                        <div class="floating-tips-header">
                            💡 Tips for Discovering the Password
                        </div>
                        <div class="floating-tips-content">
                            <ul>
                                <li>Engage in conversation with Princess Lily to gather clues</li>
                                <li>Pay attention to her reactions to different types of questions</li>
                                <li>Remember to be polite and patient, especially in harder levels</li>
                            </ul>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                user_input = st.chat_input("Type your question here... (try different approaches to discover the password)")
                
                if user_input:
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    response = data_gen(user_input, st.session_state.difficulty_level)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                    
                    st.session_state.count += 1
            else:
                st.warning("Maximum number of interactions (10) reached!")
        else:
            st.info("💡 Chat time is up! You can still attempt the key above and review the conversation for character information!")

        # Update the interaction counter display
        # st.markdown(f'<div style="text-align: center; color: #f4e4bc;">💬 Conversations: {st.session_state.count}/10 rounds used</div>', unsafe_allow_html=True)
        
        # Reset button with complete chat clearing
        if st.button("🔄 Reset Conversation", key="reset_button", use_container_width=True):
            st.session_state.messages = []
            st.session_state.count = 0
            chat_container.empty()
            st.rerun()

        # Auto-rerun to update timer
        if remaining_seconds > 0:
            time.sleep(1)
            st.rerun()

if __name__ == "__main__":
    main()