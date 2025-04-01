# Princess Lily Chat Adventure - Interface Guide

## Quick Interface Tour

### 🎮 Game Progress Tracking
![Progress Bar](screenshots/progress.png)
- Dynamic progress bar showing completed levels
- Current difficulty level indicator
- Visual progress tracking (X/3 levels completed)

### 👑 Adaptive Avatar System
- Character avatar changes based on difficulty level:
  - Easy Mode: Friendly and approachable Princess
  - Medium Mode: More reserved Princess
  - Hard Mode: Mysterious Princess
- Each avatar reflects the increasing challenge

### ⏱️ Game Mechanics
- 30-minute countdown timer
- 10 conversation rounds limit
- Password verification system with 5 attempts per level
- Difficulty progression:
  1. Easy: Princess freely shares the password
  2. Medium: Specific conversation tones trigger password reveal
  3. Hard: Requires polite interaction for hints

### 🎉 Celebration Features
- Trophy rain animation on completion
- Falling award emojis (🏆, 🎖️, 👑, 🌟, 🏅)
- Bouncing golden congratulation message
- Streamlit balloon animation

## Implementation Details

### URL of Prototype
- Run locally using: `streamlit run app/main.py`
- Requirements: Python 3.9+, modern web browser

### Libraries and Frameworks
1. **Streamlit** (v1.44.0)
   - Main web application framework
   - Real-time chat interface
   - Session state management
   - Built-in UI components

2. **Together AI**
   - Chat response generation
   - Natural language processing

3. **Custom CSS**
   - Dark theme implementation
   - Responsive design
   - Animation effects
   - Progress indicators

### Browser Compatibility
- Tested on:
  - Chrome (latest)
  - Firefox (latest)
  - Safari (latest)
- Recommended: Use in full-screen mode for best experience

### Key Files
- `app/main.py`: Core application logic and UI
- `app/generator.py`: Chat response generation
- `static/`: Avatar images for different difficulty levels
- `README.md`: Project overview and setup instructions 