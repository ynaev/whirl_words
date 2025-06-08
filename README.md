🌀🧠 WhirlWords 🧠🌀
WhirlWords is a Python-powered Boggle-style word game in which players try to find hidden words in a dynamically generated letter grid. It’s part game, part chaos engine, and all brain workout.
#======================================================================================
🧠 Game Concept
- A set number of dice, each with custom faces, are used to generate a random grid.
- A dictionary of valid English words is loaded from a file.
- Words are found by “snaking” through adjacent letters (8 directions allowed).
- Difficulty can be increased by tweaking the number of dice and faces.
#======================================================================================
📦 Features
- 🔁 Dynamically generates a new grid every game
- 🧊 Dice with customizable number of sides
- 📚 Uses a dictionary file to validate real words
- 🔍 Recursive search algorithm finds **all** possible words
- ⚙️ Flexible board size based on dice count
#======================================================================================
🛠️ How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/ynaev/whirl_words.git
   cd whirl_words
2. Ensure you’re running Python 3.10 or later.
3. Each word should be on its own line.
4. Run the game: python whirlwords.py
#======================================================================================
🧪 Sample Output
How many dice would you like to compete against?  16
How many faces would you like each die to have?  6

Grid:
T  H  E  Qu
U  A  L  S
O  V  E  R
I  N  G  Z

Words found:
['the', 'hat', 'over', 'leaving', 'squealer', ...]
#======================================================================================
🗺️ Future Features
- ✅ Validate user-entered words during gameplay
- 🎯 Scoring system (like Boggle)
- 🖱️ Interactive Tkinter UI with clickable tiles
- ⏱️ Countdown timer and scoreboard
- 🧑‍🤝‍🧑 Multiplayer support
- 🧾 Game history and stats tracking
- ✨ Highlight found words on the grid
#======================================================================================
📝 License
This project is licensed under the MIT License. Go wild.
#======================================================================================
💬 Contact
Built with love, recursion, and chaos by Ynaev Squigglebraid.
May your tiles be ever in your favor.
github.com/ynaev
