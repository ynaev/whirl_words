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
    while True:
        try:
            num_dice = int(input("How many dice would you like to compete against? (Minimum: 16) "))
            if num_dice < 16:
                print("That's too few! You need at least a 4x4 grid to play.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    # Find nearest perfect square and adjust
    nearest_perfect_square = math.ceil(math.sqrt(num_dice)) ** 2
    grid_size = int(math.sqrt(nearest_perfect_square))

    if nearest_perfect_square != num_dice:
        num_dice = nearest_perfect_square
        print(f"I've rounded the dice up to the nearest perfect square to create a nice grid of {grid_size} x {grid_size}")

    # Get number of faces per die
    while True:
        try:
            num_faces = int(input("How many faces would you like each die to have? "))
            if num_faces < 2:
                print("Dice need at least two faces. Chaos comes later.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    total_tiles = num_dice * num_faces

#=================================================================================================    
    dice = helper.letter_pool(total_tiles, num_dice, num_faces)

    w_w_grid = helper.generate_grid_from_dice(dice, grid_size)
    
    submitted_words = []
    score_tracker = [0]
    game_time = 30
    
    root = tk.Tk()
    root.title("whirl_words")
    
    create_board(root, w_w_grid)  #Calls the function to build the board

    right_frame = tk.Frame(root)  #Create frame to hold entry, submit button, score, timer, AND submitted words
    right_frame.pack(side="right", fill="y", padx=10, pady=10)
    
    entry = tk.Entry(root, font=("Helvetica", 16))
    entry.pack(pady=10)    
    entry.bind('<Return>', lambda event: helper.submit_word(entry, submitted_words, valid_words, score_label, score_tracker, submitted_listbox))

    submit_btn = tk.Button(root, text="Submit Word", command=lambda: helper.submit_word(entry, submitted_words, valid_words, score_label, score_tracker, submitted_listbox))

    score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 14))
    score_label.pack(pady=5)

    timer_label = tk.Label(root, text="Time Left: 30", font=("Helvetica", 14))
    timer_label.pack(pady=5)

    submitted_label = tk.Label(right_frame, text="Words Submitted:", font=("Helvetica", 14, "bold"))  #Submitted words listbox + scrollbar
    submitted_label.pack(pady=(10,0))

    submitted_listbox = tk.Listbox(right_frame, height=15, width=20, font=("Helvetica", 12))
    submitted_listbox.pack(side="left", fill="y")

    scrollbar = tk.Scrollbar(right_frame, orient="vertical")
    scrollbar.config(command=submitted_listbox.yview)
    scrollbar.pack(side="left", fill="y")

    submitted_listbox.config(yscrollcommand=scrollbar.set)
    
    helper.force_focus(root, entry)

    helper.start_timer(root, timer_label, entry, submit_btn, game_time)

    root.mainloop()

if __name__ == "__main__":
    whirl_words()
