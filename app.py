import streamlit as st
import random

# Config
st.set_page_config(page_title="Math Quiz", layout="wide")

# Constants
NUM_BOTS = 5
POINTS_PER_QUESTION = 10
BOT_NAMES = [f"🤖 Bot_{i+1}" for i in range(NUM_BOTS)]

questions = [
    {"question": "1 + 1 = ?", "options": [2, 3, 4, 5], "correct": 2},
    {"question": "2 + 2 = ?", "options": [3, 4, 5, 6], "correct": 4},
    # Add more questions as needed
]

if "questions" not in st.session_state:
    st.session_state.questions = random.sample(questions, len(questions))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.name = ""
    st.session_state.answered = False
    st.session_state.feedback_type = ""
    st.session_state.bot_scores = {bot: 0 for bot in BOT_NAMES}

# Name input
if not st.session_state.name:
    st.session_state.name = st.text_input("Enter your nickname:")
    if not st.session_state.name:
        st.stop()

# Quiz end
if st.session_state.index >= len(st.session_state.questions):
    st.balloons()
    st.write("Quiz Complete!")
    final_scores = {st.session_state.name: st.session_state.score}
    final_scores.update(st.session_state.bot_scores)
    st.table(final_scores)
    if st.button("Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
    st.stop()

q = st.session_state.questions[st.session_state.index]
st.write(f"Question: {q['question']}")

if not st.session_state.answered:
    cols = st.columns(2)
    opts = q["options"].copy()
    random.shuffle(opts)
    for i, opt in enumerate(opts):
        with cols[i % 2]:
            if st.button(str(opt), key=f"opt_{opt}"):
                if opt == q["correct"]:
                    st.session_state.score += POINTS_PER_QUESTION
                    st.session_state.feedback_type = "correct"
                else:
                    st.session_state.feedback_type = "wrong"
                st.session_state.answered = True

                # Bots answer
                for bot in BOT_NAMES:
                    if random.random() < 0.75:
                        st.session_state.bot_scores[bot] += POINTS_PER_QUESTION

                st.experimental_rerun()
                st.stop()

if st.session_state.answered:
    if st.session_state.feedback_type == "correct":
        st.success("Correct!")
        st.balloons()
    else:
        st.error("Wrong!")
        st.markdown("<h1 style='color:red;'>❌</h1>", unsafe_allow_html=True)

    # Leaderboard
    scores = {st.session_state.name: st.session_state.score}
    scores.update(st.session_state.bot_scores)
    st.table(scores)

    if st.button("Next"):
        st.session_state.index += 1
        st.session_state.answered = False
        st.experimental_rerun()
        st.stop()
