from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "secret123"

words = {
    "cherry": "A small red fruit",
    "spiderman": "A Marvel superhero",
    "jamesbond": "Agent 007",
    "punisher": "A Marvel anti-hero"
}

hangman_stages = [
"""
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
""",
"""
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
""",
"""
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
""",
"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
"""
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
"""
  +---+
  |   |
      |
      |
      |
      |
=========
"""
]

def reset_game():
    word = random.choice(list(words.keys()))
    session["word"] = word
    session["hint"] = words[word]
    session["guessed"] = []
    session["attempts"] = 6

@app.route("/", methods=["GET", "POST"])
def index():
    if "word" not in session:
        reset_game()

    word = session["word"]
    guessed = session["guessed"]
    attempts = session["attempts"]
    hint = session["hint"]

    message = ""

    if request.method == "POST":
        guess = request.form["guess"].lower()

        if guess == "hint":
            message = hint

        elif guess in guessed:
            message = "Already guessed!"

        elif guess in word:
            guessed.append(guess)
            session["guessed"] = guessed
            message = "Correct!"
        else:
            attempts -= 1
            session["attempts"] = attempts
            message = "Wrong!"

    # build word display
    display = ""
    for letter in word:
        if letter in guessed:
            display += letter + " "
        else:
            display += "_ "

    # game status
    if "_" not in display:
        message = "🎉 You Win!"

    if attempts == 0:
        message = f"💀 Game Over! Word was {word}"

    # choose hangman stage
    stage_index = 6 - attempts
    hangman = hangman_stages[stage_index]

    return render_template(
        "index.html",
        display=display,
        attempts=attempts,
        message=message,
        hint=hint,
        hangman=hangman
    )

if __name__ == "__main__":
    app.run(debug=True)