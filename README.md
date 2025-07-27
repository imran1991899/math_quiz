# 🎮 Math Quiz Battle (Kahoot-style with Bots)

A fun and colorful math quiz game built with [Streamlit](https://streamlit.io/) — compete against 5 AI bots and test your addition skills!

---

## 🚀 Features

- ✅ Easy addition-only questions
- 🎯 10 points per correct answer
- 🤖 Compete against 5 bots with realistic accuracy
- 🎈 Balloons for correct answers, ❌ X mark for wrong ones
- 📊 Live scoreboard after each question
- 🏆 Final leaderboard with all scores

---

## 📸 Screenshots

| Quiz Question | Scoreboard |
|---------------|------------|
| ![](assets/screenshot-question.png) | ![](assets/screenshot-scoreboard.png) |

---

## 🧑‍🏫 How to Play

1. Enter your nickname to start
2. Answer each question (you get 10 points per correct answer)
3. Bots also answer in the background
4. See how your score stacks up after each round
5. View the final leaderboard and play again!

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/) for UI
- Python 3.9+
- No database needed — all state is handled in memory

---

## 📦 Installation

### 🔧 Run locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/math-quiz-battle.git
cd math-quiz-battle

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
