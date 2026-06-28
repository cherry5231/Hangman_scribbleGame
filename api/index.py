import random


from flask import Flask, render_template, request, session, redirect

from flask_socketio import SocketIO, join_room, leave_room, emit

import string
app = Flask(__name__)
app.secret_key = "secret123"

socketio = SocketIO(app)
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

def create_room_code():
    while True:
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        if code not in rooms:
            return code

@app.route("/multiplayer")
def multiplayer():
    return render_template(
        "multiplayer.html",
        room_code="",
        players=[],
        display="",
        attempts=6,
        hint="",
        message="",
        hangman="",
        game_over=False
    )
@app.route("/create-room")
def create_room_page():

    code = create_room_code()

    word = random.choice(list(words.keys()))
    rooms[code] = {
        "players":["Player1"],
        "messages":[],
        "word":word,
        "hint":words[word],
        "guessed":[],
        "attempts":6,
        "turn":0
    }
    return render_template(
        "room.html",
        room_code=code,
        players=rooms[code]["players"],
        player_name="Player1",
        display="",
        attempts=6,
        hint="",
        message="Waiting for players...",
        hangman="",
        game_over=False
    )
   

@app.route("/join-room", methods=["GET", "POST"])
def join_room_page():

    if request.method == "POST":

        code = request.form["code"].upper()

        if code not in rooms:

            return render_template(
                "join_room.html",
                players=0,
                message="❌ Room Not Found"
            )

        if len(rooms[code]["players"]) >= 6:

            return render_template(
                "join_room.html",
                players=6,
                message="❌ Room Full"
            )

        player = f"Player{len(rooms[code]['players'])+1}"

        rooms[code]["players"].append(player)

        return render_template(
        "room.html",
        room_code=code,
        players=rooms[code]["players"],
        player_name=player,
        display="",
        attempts=6,
        hint="",
        message=f"{player} Joined!",
        hangman="",
        game_over=False
    )

    return render_template(
        "join_room.html",
        players=0,
        message=""
    )
   
@socketio.on("create_room")
def create_room():

    code = create_room_code()
    word = random.choice(list(words.keys()))

    rooms[code] = {
    "players":["Player1"],
    "messages":[],
    "word":word,
    "hint":words[word],
    "guessed":[],
    "attempts":6,
    "turn":0
}
    join_room(code)

    emit("room_created",{
    "room":code,
    "players":rooms[code]["players"]
})

    emit(
        "update_players",
        rooms[code]["players"]
    )
    
@socketio.on("join_room")
def join(data):

    code = data["room"]

    if code not in rooms:
        emit("error",{"msg":"Room not found"})
        return

    if len(rooms[code]["players"]) >= 6:
        emit("error",{"msg":"Room Full"})
        return

    player = f"Player{len(rooms[code]['players'])+1}"

    rooms[code]["players"].append(player)

    join_room(code)

    emit(
        "update_players",
        rooms[code]["players"],
        room=code
    )
@socketio.on("connect_room")
def connect_room(data):

    code = data["room"]

    join_room(code)

    emit(
        "update_players",
        rooms[code]["players"],
        room=code
    )
    
@socketio.on("disconnect")
def disconnect():

    # Later we can remove player automatically.
    pass
def reset_game():
    word = random.choice(list(words.keys()))
    session["word"] = word
    session["hint"] = words[word]
    session["guessed"] = []
    session["attempts"] = 6

@socketio.on("leave_room")
def leave(data):

    code = data["room"]
    player = data["player"]

    if code not in rooms:
        return

    if player in rooms[code]["players"]:
        rooms[code]["players"].remove(player)

    leave_room(code)

    emit(
        "update_players",
        rooms[code]["players"],
        room=code
    )


@app.route("/restart")
def restart():
    reset_game()
    return redirect("/")





@app.route("/")
def home():
    return render_template("home.html")





    




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
        guess = request.form["guess"].lower()

        # FIX: "hint" is checked before the single-letter-length check now,
        # otherwise it always failed the len(guess) != 1 test first and the
        # hint branch was unreachable.
        if guess == "hint":
            message = hint
        elif len(guess) != 1:
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

@socketio.on("send_message")
def handle_message(data):

    emit(
        "receive_message",
        {
            "player": data["player"],
            "text": data["text"]
        },
        room=data["room"]
    )

@socketio.on("get_game")
def get_game(data):

    room = rooms[data["room"]]

    display = ""

    for letter in room["word"]:
        if letter in room["guessed"]:
            display += letter + " "
        else:
            display += "_ "

    hangman = hangman_stages[6-room["attempts"]]

    emit(
        "game_update",
        {
            "display": display,
            "attempts": room["attempts"],
            "hint": room["hint"],
            "hangman": hangman,
            "message": "",
            "turn": room["players"][room["turn"]]
        }
    )
@socketio.on("guess_letter")
def guess_letter(data):

    room_code = data["room"]
    guess = data["guess"].lower()

    room = rooms[room_code]

    if guess in room["guessed"]:
        return

    room["guessed"].append(guess)

    if guess not in room["word"]:
        room["attempts"] -= 1
    room["turn"] += 1

    if room["turn"] >= len(room["players"]):
        room["turn"] = 0
    display = ""

    for letter in room["word"]:
        if letter in room["guessed"]:
            display += letter + " "
        else:
            display += "_ "

    if "_" not in display:
        message = "🎉 You Win!"
        hangman = hangman_stages[7]

    elif room["attempts"] <= 0:
        message = "💀 Game Over! Word was " + room["word"]
        hangman = hangman_stages[6]

    else:
        message = ""
        index = max(0, min(5, 6-room["attempts"]))
        hangman = hangman_stages[index]
    
    emit(
    "game_update",
    {
        "display": display,
        "attempts": room["attempts"],
        "hint": room["hint"],
        "hangman": hangman,
        "message": message,
        "turn": room["players"][room["turn"]]
    },
    room=room_code
)

if __name__ == "__main__":
    
    socketio.run(app, debug=True)