import random


from flask import Flask, render_template, request, session, redirect




app = Flask(__name__)
app.secret_key = "secret123"

words = {
    "cherry" : "A small red fruit",
    "spiderman": "A Marvel superhero",
    "jamesbond": "Agent 007",
    "punisher": "A Marvel anti-hero",
    "batman" : "The Dark Knight",
    "superman": "Man of Steel",
    "ironman": "Genius billionaire superhero",
    "thor": "God of Thunder",
    "hulk": "Green rage monster",
    "deadpool": "The Merc with a Mouth",
    "wolverine": "Mutant with adamantium claws",
    "joker": "Batman's arch enemy",
    "venom": "Alien symbiote",
    "flash": "Fastest man alive",

    # Games
    "minecraft": "A block-building sandbox game",
    "fortnite": "Battle royale with building",
    "valorant": "A tactical FPS game",
    "pubg": "Popular battle royale game",
    "pokemon": "Catch them all",
    "zelda": "Princess of Hyrule",
    "mario": "Nintendo's famous plumber",
    "sonic": "Blue hedgehog",
    "pacman": "Yellow arcade character",
    "tetris": "Classic block puzzle game",

    # Technology
    "python": "Popular programming language",
    "flask": "Python web framework",
    "github": "Code hosting platform",
    "javascript": "Language of the web",
    "database": "Stores structured information",
    "algorithm": "Step-by-step problem solving",
    "computer": "Electronic machine",
    "keyboard": "Input device",
    "internet": "Global network",
    "artificialintelligence": "Machines simulating human intelligence",

    # Animals
    "elephant": "Largest land animal",
    "giraffe": "Tallest animal",
    "kangaroo": "Australian jumper",
    "penguin": "Flightless bird",
    "dolphin": "Intelligent marine mammal",
    "tiger": "Striped big cat",
    "cheetah": "Fastest land animal",
    "octopus": "Eight-armed sea creature",
    "panda": "Black and white bear",
    "peacock": "National bird of India",

    # Countries & Places
    "india": "Country known for the Taj Mahal",
    "japan": "Land of the Rising Sun",
    "egypt": "Home of the pyramids",
    "paris": "City of Love",
    "london": "Home of Big Ben",
    "tokyo": "Capital of Japan",
    "everest": "Highest mountain in the world",
    "amazon": "Largest rainforest",
    "sahara": "Largest hot desert",
    "antarctica": "Coldest continent",

    # Science
    "gravity": "Force that pulls objects together",
    "planet": "Orbits a star",
    "galaxy": "Collection of stars",
    "oxygen": "Gas humans breathe",
    "atom": "Basic unit of matter",
    "energy": "Ability to do work",
    "volcano": "Erupts lava",
    "lightning": "Electrical discharge in the sky",
    "eclipse": "Sun or Moon gets obscured",
    "telescope": "Used to observe space",

    # Anime
    "naruto": "Ninja who dreams of becoming Hokage",
    "sasuke": "Naruto's rival",
    "kakashi": "The Copy Ninja",
    "itachi": "Member of the Akatsuki",
    "luffy": "Captain of the Straw Hat Pirates",
    "zoro": "Swordsman of the Straw Hats",
    "sanji": "Cook of the Straw Hats",
    "goku": "Saiyan raised on Earth",
    "vegeta": "Prince of all Saiyans",
    "pikachu": "Electric Pokemon",

    # Movies
    "avengers": "Earth's mightiest heroes",
    "endgame": "Marvel's epic finale",
    "gladiator": "Roman warrior movie",
    "inception": "Dream within a dream",
    "interstellar": "Space and time travel film",
    "matrix": "Reality is an illusion",
    "terminator": "I'll be back",
    "rocky": "Boxing legend",
    "godfather": "Classic mafia film",
    "jurassicpark": "Dinosaurs brought back to life",

    # Games
    "godofwar": "Kratos fights gods",
    "kratos": "Ghost of Sparta",
    "atreus": "Son of Kratos",
    "eldenring": "Open-world soulslike game",
    "bloodborne": "Gothic action RPG",
    "skyrim": "Land of the Nords",
    "cyberpunk": "Futuristic RPG",
    "witcher": "Monster hunter Geralt",
    "overwatch": "Hero shooter game",
    "halo": "Master Chief's series",

    # Technology
    "linux": "Open-source operating system",
    "windows": "Microsoft operating system",
    "android": "Google mobile OS",
    "frontend": "Part of a website users see",
    "backend": "Handles server-side logic",
    "api": "Allows applications to communicate",
    "json": "Popular data format",
    "network": "Connected computers",
    "compiler": "Translates code into machine language",
    "debugging": "Finding and fixing bugs",

    # Space
    "mercury": "Closest planet to the Sun",
    "venus": "Hottest planet",
    "mars": "The red planet",
    "jupiter": "Largest planet",
    "saturn": "Planet with rings",
    "uranus": "Ice giant planet",
    "neptune": "Farthest major planet",
    "milkyway": "Our galaxy",
    "asteroid": "Rocky object in space",
    "blackhole": "Gravity so strong light cannot escape",

    # Mythology
    "zeus": "King of the Greek gods",
    "hades": "God of the underworld",
    "poseidon": "God of the sea",
    "athena": "Goddess of wisdom",
    "odin": "King of the Norse gods",
    "loki": "God of mischief",
    "medusa": "Woman with snake hair",
    "pegasus": "Winged horse",
    "minotaur": "Half man, half bull",

    # Random Fun
    "chocolate": "Sweet treat made from cocoa",
    "pizza": "Popular Italian dish",
    "hamburger": "Patty served in a bun",
    "diamond": "Hardest natural substance",
    "rainbow": "Appears after rain and sunlight",
    "thunder": "Sound following lightning",
    "waterfall": "Water flowing over a cliff",
    "treasure": "Hidden valuable items",
    "pirate": "Sails the seas seeking loot",
    "ninja": "Stealthy warrior",
}
rooms = {}


hangman_stages = [
    """
    +---+
    |   |
    O   |
   /|\\  |
   / \\  |
 ████████████
  ██████████
   ████████
    ██████
     ████
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
  ██████████
   ████████
    ██████
     ████
=========
""",
    """
    +---+
    |   |
    O   |
   /|\\  |
   / \\  |
   ██████████
    ████████
     ██████
      ████
=========
""",
    """
   +---+
  |   |
  O   |
 /|\\  |
 / \\  |
   ████████
    ██████
     ████
=========
""",
    """
    +---+
   |   |
   O   |
  /|\\  |
  / \\  |
     ██████
      ████
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
     ████
=========
""",
    """
  +---+
  |   |
 X X  |
 ___  |
 /|\\  |
 / \\  |
=========
DEAD
""",
    """
   \\(^_^)/
    \\   /
     \\|/
      |
     / \\
    /   \\

 I'M FREE!!
""",
]
def reset_game():
    word = random.choice(list(words.keys()))
    session["word"] = word
    session["guessed"] = []
    session["attempts"] = 6
    session["hint"] = words[word]
@app.route("/")
def home():
    return redirect("/single")

@app.route("/restart")
def restart():
    reset_game()
   
    return redirect("/single")











    



@app.route("/single", methods=["GET", "POST"])
def index():
    if "word" not in session:
        reset_game()

    word = session["word"]
    guessed = session["guessed"]
    attempts = session["attempts"]
    hint = session["hint"]

    message = ""

    if request.method == "POST" and attempts > 0:
        guess = request.form.get("guess", "").strip().lower()

        # FIX: "hint" is checked before the single-letter-length check now,
        # otherwise it always failed the len(guess) != 1 test first and the
        # hint branch was unreachable.
        if len(guess) != 1:
          message = "Enter only one letter." 
      
        elif guess in guessed:
            message = "Already guessed!"
        elif guess in word:
            guessed.append(guess)
            session["guessed"] = guessed
            message = "Correct!"
        else:
            attempts = max(0, attempts - 1)
            session["attempts"] = attempts
            message = "Wrong!"

    # build word display
    display = ""
    for letter in word:
        if letter in guessed:
            display += letter + " "
        else:
            display += "_ "

    won = "_" not in display
    game_over = attempts == 0 or won

    if won:
        message = "You Win!"
    if attempts == 0:
        message = f"💀 Game Over! Word was {word}"

    # choose hangman stage
    if won:
        hangman = hangman_stages[7]
    elif attempts == 0:
        hangman = hangman_stages[6]
    else:
       index = max(0, min(6, 6 - attempts))
       hangman = hangman_stages[index]

    return render_template(
        "index.html",
        display=display,
        attempts=attempts,
        message=message,
        hint=hint,
        hangman=hangman,
        game_over=game_over,
    )



if __name__ == "__main__":
    app.run(debug = True)
