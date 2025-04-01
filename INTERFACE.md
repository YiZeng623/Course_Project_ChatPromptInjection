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

# Interface Design Document

## Overview
The application features a modern, responsive interface with a dark theme optimized for user engagement and accessibility.

## Core Components

### 1. Header Section
- **Title**: "Jailbreak.Me (Princess Lily Chat Adventure)"
- **Difficulty Level Indicator**: Shows current level (Easy/Medium/Hard)
- **Progress Bar**: Visual representation of difficulty progression
- **Timer Display**: Countdown timer with color-coded status

### 2. Chat Interface
- **Message Display**: 
  - User messages: Light gray background (#d1d1d1)
  - Assistant messages: Dark blue background (#2d3348)
  - Rounded corners (5px radius)
  - Custom padding (10px)
- **Input Area**: 
  - Fixed position at bottom
  - Placeholder text: "Type your question here..."
  - Maximum 10 conversation rounds
  - Counter display: "Conversations: X/10 rounds used"

### 3. Verification Section
- **Key Input Field**: 
  - Placeholder: "Enter the key here..."
  - Submit button with custom styling
  - Real-time validation feedback
- **Success/Error Messages**: 
  - Success: Green background (#4CAF50)
  - Error: Red background (#ff4b4b)
  - Animated transitions

### 4. Floating Tips Box
- **Position**: Fixed at bottom-left
- **Content**: 
  - Title: "💡 Tips"
  - Bullet points with custom styling
  - Semi-transparent background
- **Responsive Design**:
  - Desktop: 340px width
  - Mobile: 300px width
  - Custom padding and margins

### 5. Modal Popups
- **Success Modal**:
  - Centered overlay
  - Custom icon (🎉)
  - Animated entrance
  - Close button (×)
- **Error Modal**:
  - Red background for warnings
  - Clear error messages
  - Dismissible interface

## Visual Design

### Color Scheme
- **Primary Colors**:
  - Background: Dark (#0E1117)
  - Text: White (#FFFFFF)
  - Accent: Gold (#FFD700)
- **Secondary Colors**:
  - User Messages: Light Gray (#d1d1d1)
  - Assistant Messages: Dark Blue (#2d3348)
  - Success: Green (#4CAF50)
  - Error: Red (#ff4b4b)
  - Timer: Gold (#f4e4bc)

### Typography
- **Font Family**: System default
- **Font Sizes**:
  - Headers: 1.2em
  - Body Text: 1.1em
  - Mobile: 1em
- **Line Height**: 1.6
- **Text Colors**:
  - Primary: White (#FFFFFF)
  - Secondary: Light Gray (#CCCCCC)
  - Accent: Gold (#f4e4bc)

### Spacing
- **Padding**:
  - Container: 20px
  - Messages: 10px
  - Buttons: 8px 16px
- **Margins**:
  - Between Messages: 10px
  - Section Spacing: 20px
  - Mobile Adjustments: 10px

### Animations
- **Transitions**:
  - Duration: 0.3s
  - Timing: ease-in-out
- **Effects**:
  - Fade in/out
  - Slide up/down
  - Scale transform

## Responsive Design

### Desktop View (>768px)
- Full-width layout
- Maximum width: 1200px
- Side padding: 20px
- Tips box: 340px width

### Tablet View (768px)
- Adjusted padding: 15px
- Tips box: 320px width
- Font size: 1.1em

### Mobile View (<768px)
- Full-width layout
- Tips box: 300px width
- Font size: 1em
- Adjusted spacing
- Touch-friendly buttons

## Accessibility Features
- High contrast color scheme
- Clear typography hierarchy
- Responsive text sizing
- Touch-friendly interface
- Keyboard navigation support
- Screen reader compatibility 