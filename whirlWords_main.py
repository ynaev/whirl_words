import random
import math
import genWWDice
import tkinter as tk
import helper
from createWWBoard import create_board

#Load English dictionary safely
valid_words = set()  #Instantiate the list of acceptable words
dictionary_path = r"C:\Users\ynaev\AppData\Local\Programs\Python\Python313\whirl_words\dictionary_words.txt"
try:
    with open(dictionary_path, 'r') as f:
        valid_words = set(word.strip().lower() for word in f)
except FileNotFoundError:  #Catches the most likely issue — bad path.
    print(f"⚠️ Error: Dictionary file not found at:\n{dictionary_path}")
    print("The game cannot continue without a valid word list.")
    exit(1)  #Stops the script so you’re not running a game without words.
except Exception as e:  #Catches anything else weird, like encoding errors.
    print(f"⚠️ An unexpected error occurred while loading the dictionary:\n{e}")
    exit(1)  #Stops the script so you’re not running a game without words.

def whirl_words():
    """
    Play a Boggle-style word game with customizable grid sizes
    """
#=================================================================================================
    num_dice = int(input("How many dice would you like to compete against?  ")) #Get user customization
    nearest_perfect_square = (math.ceil(math.sqrt(num_dice)) **2)  #Find the nearest perfect square
    grid_size = int(math.sqrt(nearest_perfect_square))
    if nearest_perfect_square != num_dice:
        num_dice = nearest_perfect_square  #Reset numDice to updated value
        print(f"I've rounded the dice up to the nearest perfect square to create a nice grid of {grid_size} x {grid_size}")
    num_faces = int(input("How many faces would you like each die to have?  ")) #Get user customization

#=================================================================================================    
    dice = genWWDice.gen_w_w_dice(num_dice, num_faces)  #Call the function to generate the dice
    chosen_letters = [random.choice(die).upper() for die in dice]  #Randomly choose one face from each die
    w_w_grid = [chosen_letters[i:i+grid_size] for i in range(0, len(chosen_letters), grid_size)]  #Arrange the letters into a grid
    max_word_length = num_dice  # Placeholder for future validation
    print("Can you find all the words hidden in this grid?  You've got 30 seconds.\n\nGo!\n")

#=================================================================================================
    #Call the function to display the board
    game_time = 30
    submitted_words = []
    
    root = tk.Tk()
    root.title("whirl_words")
    root.lift()  #Tells the window to come forward
    root.attributes('-topmost', True)  #Forces it to the very top (over everything)
    root.after(1000, lambda: root.attributes('-topmost', False))  #Drops the "always on top" behavior after 1 second so it doesn’t block other windows later on.

    create_board(root, w_w_grid)  #Calls the function to build the board

    entry = tk.Entry(root, font=("Helvetica", 16))
    entry.pack(pady=10)
    entry.bind('<Return>', lambda event: helper.submit_word(entry, submitted_words, valid_words))

    submit_btn = tk.Button(root, text="Submit Word", command=lambda: helper.submit_word(entry, submitted_words, valid_words))

    score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 14))
    score_label.pack(pady=5)

    timer_label = tk.Label(root, text="Time Left: 30", font=("Helvetica", 14))
    timer_label.pack(pady=5)
    helper.start_timer(root, timer_label, entry, submit_btn, game_time)

    root.mainloop()

if __name__ == "__main__":
    whirl_words()
