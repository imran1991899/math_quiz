import streamlit as st
import random

# --------- CONFIG ----------
st.set_page_config(page_title="Kahoot Math Quiz", layout="wide")

# --------- CONSTANTS ----------
NUM_BOTS = 5
POINTS_PER_QUESTION = 10
BOT_NAMES = [f"🤖 Bot_{i+1}" for i in range(NUM_BOTS)]

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

# --------- INITIALIZE SESSION STATE ----------
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(questions, len(questions))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.name = ""
    st.session_state.answered = False
    st.session_state.feedback_type = ""  # "correct" or "wrong"
    st.session_state.bot_scores = {bot: 0 for bot in BOT_NAMES}
    st.session_state.answer_selected = None  # store user’s selected answer

# --------- PLAYER NAME INPUT ----------
if not st.session_state.name:
    st.markdown("<h1 style='text-align:center;'>🎮 Welcome to Math Quiz Battle!</h1>", unsafe_allow_html=True)
    st.session_state.name = st.text_input("Enter your nickname to start:")
    if not st.session_state.name:
        st.stop()

# --------- QUIZ FINISHED ----------
if st.session_state.index >= len(st.session_state.questions):
    st.balloons()
    st.markdown(f"<h1 style='text-align:center; color:green;'>🎉 Quiz Complete! 🎉</h1>", unsafe_allow_html=True)

    final_scores = {st.session_state.name: st.session_state.score}
    final_scores.update(st.session_state.bot_scores)
    sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    st.markdown("### 🏆 Final Leaderboard")
    st.table({name: score for name, score in sorted_scores})

    if st.button("🔁 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()  # safe here because inside button event
    st.stop()

# --------- CURRENT QUESTION ----------
q = st.session_state.questions[st.session_state.index]
st.markdown(f"<h2 style='text-align:center;'>{q['question']}</h2>", unsafe_allow_html=True)
st.progress((st.session_state.index + 1) / len(st.session_state.questions))

# --------- ANSWER SELECTION ----------
if not st.session_state.answered:
    options = q["options"].copy()
    random.shuffle(options)
    cols = st.columns(2)

    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(str(opt), key=f"opt_{opt}"):
                st.session_state.answer_selected = opt
                if opt == q["correct"]:
                    st.session_state.score += POINTS_PER_QUESTION
                    st.session_state.feedback_type = "correct"
                else:
                    st.session_state.feedback_type = "wrong"
                st.session_state.answered = True

                # Bots answer (75% chance to get it right)
                for bot in BOT_NAMES:
                    if random.random() < 0.75:
                        st.session_state.bot_scores[bot] += POINTS_PER_QUESTION

                # No rerun, just let Streamlit naturally rerun after interaction
                # So no st.experimental_rerun() here
                # Just break to stop rendering buttons after click
                break
else:
    # Show feedback
    if st.session_state.feedback_type == "correct":
        st.success("✅ Correct!")
        st.balloons()
    else:
        st.error("❌ Wrong!")
        st.markdown("<h1 style='text-align:center; color:red;'>❌</h1>", unsafe_allow_html=True)

    # Leaderboard after question
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
        # no need for st.experimental_rerun()
