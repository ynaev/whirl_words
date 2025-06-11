import os
import random
import math
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import helper
from createWWBoard import create_board

# Load English dictionary safely
valid_words = set()
dictionary_path = os.path.join(os.path.dirname(__file__), 'dictionary_words.txt')
try:
    with open(dictionary_path, 'r') as f:
        valid_words = set(word.strip().lower() for word in f)
except FileNotFoundError:
    print(f"⚠️ Error: Dictionary file not found at:\n{dictionary_path}")
    print("The game cannot continue without a valid word list.")
    exit(1)
except Exception as e:
    print(f"⚠️ An unexpected error occurred while loading the dictionary:\n{e}")
    exit(1)

def whirl_words():
    """
    whirlWords_main.py
    A Boggle-style word game with customizable dice and grid settings.
    Built with tkinter.
    """
    while True:
        try:
            num_dice = simpledialog.askinteger("Grid Setup", "How many dice would you like to Whirl through?\n(Minimum: 9)")
            if num_dice is None:                
                return
            if num_dice < 9:
                messagebox.showwarning("Invalid Input", "That's too few! You need at least a 3x3 grid to play.")
                continue
            break
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid integer.")

    nearest_perfect_square = math.ceil(math.sqrt(num_dice)) ** 2
    grid_size = int(math.sqrt(nearest_perfect_square))

    if nearest_perfect_square != num_dice:
        num_dice = nearest_perfect_square
        print(f"I've rounded the dice up to the nearest perfect square to create a nice grid of {grid_size} x {grid_size}")

    while True:
        num_faces = simpledialog.askinteger("Dice Setup", "How many faces should each die have?\n(Minimum: 2)")
        if num_faces is None:
            exit()
        if num_faces < 2:
            messagebox.showwarning("Invalid Input", "Dice need at least two faces. Chaos comes later.")
            continue
        break

    total_tiles = num_dice * num_faces

    dice = helper.letter_pool(total_tiles, num_dice, num_faces)
    w_w_grid = helper.generate_grid_from_dice(dice, grid_size)
    prefixes = helper.build_prefix_set(valid_words)

    submitted_words = []
    master_word_list = set()
    score_tracker = [0]    

    root = tk.Tk()
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.title("whirl_words")

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    board_frame = tk.Frame(main_frame)
    board_frame.pack(side="left", padx=10)

    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="right", fill="y", padx=10)

    create_board(board_frame, w_w_grid)

    entry = tk.Entry(right_frame, font=("Helvetica", 16))
    entry.pack(pady=10)    
    entry.bind('<Return>', lambda event: helper.submit_word(entry, submitted_words, submitted_listbox))
    entry.config(state="disabled")

    submit_btn = tk.Button(right_frame, text="Submit Word", command=lambda: helper.submit_word(entry, submitted_words, submitted_listbox))
    submit_btn.config(state="disabled")
    submit_btn.pack(pady=5)

    timer_label = tk.Label(right_frame, text="Time Left: 30", font=("Helvetica", 14))
    timer_label.pack(pady=5)

    possible_words_label = tk.Label(right_frame, text="Number of Hidden Words: Calculating...", font=("Helvetica", 12, "italic"))
    possible_words_label.pack()

    submitted_label = tk.Label(right_frame, text="Words Submitted:", font=("Helvetica", 14, "bold"))
    submitted_label.pack(pady=(10,0))

    listbox_frame = tk.Frame(right_frame)
    listbox_frame.pack()

    submitted_listbox = tk.Listbox(right_frame, height=15, width=20, font=("Helvetica", 12))
    submitted_listbox.pack(side="left", fill="y")

    scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=submitted_listbox.yview)
    scrollbar.pack(side="left", fill="y")

    submitted_listbox.config(yscrollcommand=scrollbar.set)

    reshuffled = [False]

    def reshuffle_grid():
        if reshuffled[0]:
            return
        for die in dice:
            random.shuffle(die)
        random.shuffle(dice)
        helper.clear_frame(board_frame)
        w_w_grid = helper.generate_grid_from_dice(dice, grid_size)
        create_board(board_frame, w_w_grid)
        reshuffle_button.config(state="disabled")
        reshuffled[0] = True

    reshuffle_button = tk.Button(right_frame, text="Reshuffle Grid", font=("Helvetica", 14), bg="#ffccaa", command=reshuffle_grid)
    reshuffle_button.pack(pady=5)

    game_time = tk.IntVar(value=30)

    def start_game():        
        entry.config(state="normal")
        submit_btn.config(state="normal")
        helper.force_focus(root, entry)
        game_time.set(30)
        reshuffled[0] = False
        reshuffle_button.config(state="disabled")
        start_button.config(state="disabled")
        start_timer(game_time, on_end=on_timer_end)
        nonlocal master_word_list
        master_word_list = helper.boggle_solver(w_w_grid, valid_words, prefixes)
        possible_words_label.config(text=f"Number of Hidden Words: {len(master_word_list)}")

    start_button = tk.Button(right_frame, text="Start Game", font=("Helvetica", 14), bg="#aaffaa", command=start_game)
    start_button.pack(pady=10)

    def on_timer_end():
        helper.validate_user_words(submitted_words, master_word_list, score_tracker, messagebox)
        result = messagebox.askyesno("Game Over", "Play again?")
        if result:
            root.destroy()
            whirl_words()
        else:
            root.destroy()

    def start_timer(game_time, on_end=None):
        if game_time.get() > 0:
            game_time.set(game_time.get() - 1)
            timer_label.config(text=f"Time Left: {game_time.get()}")
            root.after(1000, lambda: start_timer(game_time, on_end=on_end))
        else:
            entry.config(state="disabled")
            submit_btn.config(state="disabled")
            print("Time’s up!")
            if on_end:
                on_end()  # Call your custom game-over logic
            else:
                root.after(1000, root.destroy)  # Default behavior: auto-close after 1 second

    root.update_idletasks()
    root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    whirl_words()