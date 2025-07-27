import streamlit as st
import random

# --------- CONFIG ----------
st.set_page_config(page_title="Kahoot Math Quiz", layout="wide")

# --------- CONSTANTS ----------
NUM_BOTS = 5
POINTS_PER_QUESTION = 10

# List of realistic names for bots
REALISTIC_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan",
    "Fiona", "George", "Hannah", "Ian", "Julia",
    "Kevin", "Lily", "Michael", "Nina", "Oscar",
    "Paula", "Quinn", "Rachel", "Steve", "Tina"
]

# --------- QUESTION BANK ----------
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

# --------- SESSION STATE INIT ---------
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(questions, len(questions))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.name = ""
    st.session_state.answered = False
    st.session_state.feedback_type = ""  # "correct" or "wrong"
    st.session_state.answer_selected = None

if "bot_names" not in st.session_state:
    st.session_state.bot_names = random.sample(REALISTIC_NAMES, NUM_BOTS)

if "bot_scores" not in st.session_state:
    st.session_state.bot_scores = {bot: 0 for bot in st.session_state.bot_names}

# --------- CSS FOR BIG BUTTONS AND TEXT ---------
st.markdown("""
<style>
div.stButton > button {
    font-size: 1.8rem !important;
    padding: 15px 0 !important;
    width: 100% !important;
    font-weight: bold !important;
}
.big-text {
    font-size: 2rem !important;
    font-weight: 600;
    text-align: center;
}
.center-text {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --------- PLAYER NAME INPUT ---------
if not st.session_state.name:
    st.markdown("<h1 class='center-text'>🎮 Welcome to Math Quiz Battle!</h1>", unsafe_allow_html=True)
    st.session_state.name = st.text_input("Enter your nickname to start:", key="name_input", label_visibility="visible")
    if not st.session_state.name:
        st.stop()

# --------- QUIZ COMPLETE ---------
if st.session_state.index >= len(st.session_state.questions):
    st.balloons()
    st.markdown(f"<h1 class='center-text' style='color:green;'>🎉 Quiz Complete! 🎉</h1>", unsafe_allow_html=True)

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

# --------- DISPLAY CURRENT QUESTION ---------
q = st.session_state.questions[st.session_state.index]
st.markdown(f"<h2 class='center-text big-text'>{q['question']}</h2>", unsafe_allow_html=True)
st.progress((st.session_state.index + 1) / len(st.session_state.questions))

# --------- ANSWER SELECTION ---------
if not st.session_state.answered:
    if st.session_state.answer_selected is None:
        options = q["options"].copy()
        random.shuffle(options)
        cols = st.columns(2)

        for i, opt in enumerate(options):
            with cols[i % 2]:
                if st.button(str(opt), key=f"opt_{opt}", help="Click to answer"):
                    st.session_state.answer_selected = opt
                    if opt == q["correct"]:
                        st.session_state.score += POINTS_PER_QUESTION
                        st.session_state.feedback_type = "correct"
                    else:
                        st.session_state.feedback_type = "wrong"
                    st.session_state.answered = True

                    # Bots answer (75% chance correct)
                    for bot in st.session_state.bot_names:
                        if random.random() < 0.75:
                            st.session_state.bot_scores[bot] += POINTS_PER_QUESTION
else:
    st.markdown(f"<p class='big-text center-text'>You selected: <strong>{st.session_state.answer_selected}</strong></p>", unsafe_allow_html=True)

# --------- FEEDBACK AND LEADERBOARD ---------
if st.session_state.answered:
    if st.session_state.feedback_type == "correct":
        st.success("✅ Correct!")
        st.balloons()
    else:
        st.error("❌ Wrong!")
        st.markdown("<h1 class='center-text' style='color:red;'>❌</h1>", unsafe_allow_html=True)

    current_scores = {st.session_state.name: st.session_state.score}
    current_scores.update(st.session_state.bot_scores)
    sorted_current = sorted(current_scores.items(), key=lambda x: x[1], reverse=True)

    st.markdown("### 📊 Leaderboard")
    st.table({name: score for name, score in sorted_current})

    if st.button("➡️ Next Question"):
        st.session_state.index += 1
        st.session_state.answered = False
        st.session_state.answer_selected = None
        st.session_state.feedback_type = ""
