import streamlit as st
import random

# ---------- CONFIG ----------
st.set_page_config(page_title="Kahoot Math Quiz", layout="wide")

# ---------- CONSTANTS ----------
NUM_BOTS = 5
POINTS_PER_QUESTION = 10

REALISTIC_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan",
    "Fiona", "George", "Hannah", "Ian", "Julia",
    "Kevin", "Lily", "Michael", "Nina", "Oscar",
    "Paula", "Quinn", "Rachel", "Steve", "Tina"
]

# ---------- SOUND & MUSIC ----------
BACKGROUND_MUSIC_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
SOUND_CORRECT = "https://actions.google.com/sounds/v1/crowds/cheer.ogg"
SOUND_WRONG = "https://actions.google.com/sounds/v1/alarms/buzzer.ogg"

# ---------- QUESTIONS ----------
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
]

# ---------- CSS FOR BIG BUTTONS ----------
st.markdown("""
<style>
div.stButton > button {
    font-size: 55px !important;
    padding: 25px 0 !important;
    height: 90px !important;
    width: 100% !important;
    font-weight: bold !important;
    border-radius: 12px;
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

# ---------- SESSION INIT ----------
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(questions, len(questions))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.name = ""
    st.session_state.answered = False
    st.session_state.answer_selected = None
    st.session_state.feedback_type = ""
    st.session_state.music_muted = False
    st.session_state.bot_names = random.sample(REALISTIC_NAMES, NUM_BOTS)
    st.session_state.bot_scores = {bot: 0 for bot in st.session_state.bot_names}

# ---------- BACKGROUND MUSIC ----------
if not st.session_state.music_muted:
    st.markdown(f"""
    <audio autoplay loop>
      <source src="{BACKGROUND_MUSIC_URL}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

# ---------- MUTE TOGGLE ----------
mute_btn = "🔈 Mute Music" if not st.session_state.music_muted else "🔇 Unmute Music"
if st.button(mute_btn):
    st.session_state.music_muted = not st.session_state.music_muted
    st.experimental_rerun()

# ---------- NAME INPUT ----------
if not st.session_state.name:
    st.markdown("<h1 class='center-text'>🎮 Welcome to Math Quiz Battle!</h1>", unsafe_allow_html=True)
    st.session_state.name = st.text_input("Enter your nickname to start:")
    if not st.session_state.name:
        st.stop()

# ---------- GAME COMPLETE ----------
if st.session_state.index >= len(st.session_state.questions):
    st.balloons()
    st.markdown("<h1 class='center-text' style='color:green;'>🎉 Quiz Complete!</h1>", unsafe_allow_html=True)

    final_scores = {st.session_state.name: st.session_state.score}
    final_scores.update(st.session_state.bot_scores)
    leaderboard = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    st.markdown("### 🏆 Final Leaderboard")
    st.table({name: score for name, score in leaderboard})

    if st.button("🔁 Play Again"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()
    st.stop()

# ---------- SHOW QUESTION ----------
q = st.session_state.questions[st.session_state.index]
st.markdown(f"<h2 class='center-text big-text'>{q['question']}</h2>", unsafe_allow_html=True)
st.progress((st.session_state.index + 1) / len(st.session_state.questions))

# ---------- ANSWER CHOICE ----------
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

                # Bot simulate answer
                for bot in st.session_state.bot_names:
                    if random.random() < 0.75:
                        st.session_state.bot_scores[bot] += POINTS_PER_QUESTION

# ---------- FEEDBACK ----------
if st.session_state.answered:
    if st.session_state.feedback_type == "correct":
        st.success("✅ Correct!")
        st.balloons()
        st.markdown(f"""
            <audio autoplay>
              <source src="{SOUND_CORRECT}" type="audio/ogg">
            </audio>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Wrong!")
        st.markdown("<h1 class='center-text' style='color:red;'>❌</h1>", unsafe_allow_html=True)
        st.markdown(f"""
            <audio autoplay>
              <source src="{SOUND_WRONG}" type="audio/ogg">
            </audio>
        """, unsafe_allow_html=True)

    # Show leaderboard
    scores = {st.session_state.name: st.session_state.score}
    scores.update(st.session_state.bot_scores)
    leaderboard = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    st.markdown("### 📊 Leaderboard")
    st.table({name: score for name, score in leaderboard})

    # Next button
    if st.button("➡️ Next Question"):
        st.session_state.index += 1
        st.session_state.answered = False
        st.session_state.answer_selected = None
        st.session_state.feedback_type = ""
