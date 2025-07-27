import streamlit as st
import random

# ---------- CONFIG ----------
st.set_page_config(page_title="Kahoot Math Quiz", layout="wide")

# ---------- CONSTANTS ----------
NUM_BOTS = 5
POINTS_PER_QUESTION = 10

BOT_NAME_POOL = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan",
    "Fiona", "George", "Hannah", "Ian", "Julia",
    "Kevin", "Luna", "Mason", "Nina", "Oscar"
]

BACKGROUND_MUSIC_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
SOUND_CORRECT = "https://actions.google.com/sounds/v1/crowds/cheer.ogg"
SOUND_WRONG = "https://actions.google.com/sounds/v1/alarms/buzzer.ogg"

# ---------- QUESTION BANK ----------
questions = [
    {"question": "1 + 1 = ?", "options": [2, 3, 4, 5], "correct": 2},
    {"question": "2 + 2 = ?", "options": [3, 4, 5, 6], "correct": 4},
    {"question": "3 + 1 = ?", "options": [3, 4, 5, 6], "correct": 4},
    {"question": "4 + 4 = ?", "options": [7, 8, 9, 10], "correct": 8},
    {"question": "2 + 5 = ?", "options": [6, 7, 8, 9], "correct": 7},
    {"question": "1 + 3 = ?", "options": [3, 4, 5, 6], "correct": 4},
    {"question": "0 + 2 = ?", "options": [1, 2, 3, 4], "correct": 2},
    {"question": "2 + 3 = ?", "options": [4, 5, 6, 7], "correct": 5},
    {"question": "6 + 2 = ?", "options": [7, 8, 9, 10], "correct": 8},
    {"question": "5 + 3 = ?", "options": [7, 8, 9, 10], "correct": 8},
    {"question": "3 + 3 = ?", "options": [5, 6, 7, 8], "correct": 6},
    {"question": "6 + 1 = ?", "options": [6, 7, 8, 9], "correct": 7},
    {"question": "2 + 6 = ?", "options": [7, 8, 9, 10], "correct": 8},
    {"question": "4 + 2 = ?", "options": [5, 6, 7, 8], "correct": 6},
    {"question": "5 + 5 = ?", "options": [9, 10, 11, 12], "correct": 10},
    {"question": "1 + 5 = ?", "options": [5, 6, 7, 8], "correct": 6},
    {"question": "3 + 2 = ?", "options": [4, 5, 6, 7], "correct": 5},
    {"question": "0 + 4 = ?", "options": [3, 4, 5, 6], "correct": 4},
    {"question": "6 + 3 = ?", "options": [8, 9, 10, 11], "correct": 9},
    {"question": "7 + 1 = ?", "options": [7, 8, 9, 10], "correct": 8},
]

# ---------- CSS ----------
st.markdown(
    """
    <style>
    .big-button > button {
        height: 70px;
        font-size: 30px;
        font-weight: bold;
    }
    .big-text {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    .center-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SESSION STATE INIT ----------
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(questions, len(questions))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.name = ""
    st.session_state.answered = False
    st.session_state.feedback_type = ""  # "correct" or "wrong"
    st.session_state.just_answered = False
    st.session_state.bot_names = random.sample(BOT_NAME_POOL, NUM_BOTS)
    st.session_state.bot_scores = {bot: 0 for bot in st.session_state.bot_names}

# ---------- BACKGROUND MUSIC (Sidebar with controls) ----------
st.sidebar.markdown("### 🎵 Background Music")
st.sidebar.audio(BACKGROUND_MUSIC_URL, format='audio/mp3')

# ---------- NAME INPUT ----------
if not st.session_state.name:
    st.markdown("<h1 class='big-text'>🎮 Welcome to Math Quiz Battle!</h1>", unsafe_allow_html=True)
    st.session_state.name = st.text_input("Enter your nickname to start:", max_chars=20)
    if not st.session_state.name:
        st.stop()

# ---------- QUIZ COMPLETE ----------
if st.session_state.index >= len(st.session_state.questions):
    st.balloons()
    st.markdown(f"<h1 class='big-text' style='color:green;'>🎉 Quiz Complete!</h1>", unsafe_allow_html=True)

    final_scores = {st.session_state.name: st.session_state.score}
    final_scores.update(st.session_state.bot_scores)
    sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    st.markdown("### 🏆 Final Leaderboard")
    st.table({name: score for name, score in sorted_scores})

    if st.button("🔁 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
    st.stop()

# ---------- CURRENT QUESTION ----------
q = st.session_state.questions[st.session_state.index]
st.markdown(f"<div class='big-text'>{q['question']}</div>", unsafe_allow_html=True)
st.progress(st.session_state.index / len(st.session_state.questions))

# ---------- HANDLE ANSWER ----------
if not st.session_state.answered:
    options = q["options"].copy()
    random.shuffle(options)
    cols = st.columns(2)
    clicked_option = None

    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(str(opt), key=f"option_{i}"):
                clicked_option = opt

    if clicked_option is not None:
        if clicked_option == q["correct"]:
            st.session_state.score += POINTS_PER_QUESTION
            st.session_state.feedback_type = "correct"
        else:
            st.session_state.feedback_type = "wrong"

        st.session_state.answered = True
        st.session_state.just_answered = True

        # Simulate bots answering
        for bot in st.session_state.bot_names:
            if random.random() < 0.75:
                st.session_state.bot_scores[bot] += POINTS_PER_QUESTION

# ---------- FEEDBACK AND LEADERBOARD ----------
if st.session_state.answered:
    if st.session_state.feedback_type == "correct":
        st.success("✅ Correct!")
        st.balloons()
        if st.button("▶️ Play Cheer Sound"):
            st.audio(SOUND_CORRECT, format="audio/ogg")
    else:
        st.error("❌ Wrong!")
        st.markdown("<h1 class='center-text' style='color:red;'>❌</h1>", unsafe_allow_html=True)
        if st.button("▶️ Play Buzz Sound"):
            st.audio(SOUND_WRONG, format="audio/ogg")

    # Show leaderboard after this question
    current_scores = {st.session_state.name: st.session_state.score}
    current_scores.update(st.session_state.bot_scores)
    sorted_current = sorted(current_scores.items(), key=lambda x: x[1], reverse=True)

    st.markdown("### 📊 Leaderboard")
    st.table({name: score for name, score in sorted_current})

    # Next question button
    if st.button("➡️ Next") and st.session_state.just_answered:
        st.session_state.index += 1
        st.session_state.answered = False
        st.session_state.just_answered = False
