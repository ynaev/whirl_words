import os
import math
import random
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog

import helper
from createWWBoard import create_board

#Load English dictionary
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

# ==== Color Scheme ====
color_a = "#0B0A0D"
color_b = "#212B40"
color_c = "#2B2D16"
color_e = "#D9AB82"

# ==== Globals ====
submitted_words = []
master_word_list = [set()]
score_tracker = [0]
reshuffled = [False]
nonlocal_grid = [None]
dice = []
prefixes = helper.build_prefix_set(valid_words)

#=================================================================================================
def whirl_words(num_dice, num_faces, grid_size):
    """
    Main game logic for the WhirlWords game.
    A Boggle-style word game with customizable dice and grid settings.
    Built with tkinter.
    """
    global dice, nonlocal_grid

    dice = helper.letter_pool(num_faces, num_dice)
    random.shuffle(dice)
    w_w_grid = helper.generate_grid_from_dice(dice, grid_size)
    nonlocal_grid[0] = w_w_grid

    # ==== Main game screen filling the root ====
    main_screen = tk.Frame(root, bg=color_c)
    main_screen.pack(fill='both', expand=True)

    # ============================ Set Up Screen ============================
    # ==== Left Frame ====
    left_frame = tk.Frame(main_screen, bg=color_c, width=600)
    left_frame.pack(side="left", fill="y")

    # ==== Center Frame ====
    center_frame = tk.Frame(main_screen, bg=color_c)
    center_frame.pack(side="left", fill="both", expand=True)

    # ==== Right Frame ====
    right_frame = tk.Frame(main_screen, bg=color_c, width=600)
    right_frame.pack(side="right", fill="y")

    # ============================ Set Up Center Play Screen ============================
    # ================= Inner Play Screen =================
    # ==== Game Frame ====
    game_frame = tk.Frame(center_frame, bg=color_c)
    game_frame.place(relx=0.5, rely=0.5, anchor='center')

    # ==== Timer countdown box ====
    timer_label = tk.Label(game_frame, text="Time Left: 30", font=("Helvetica", 20, "bold"), bg=color_c, fg=color_e)
    timer_label.pack(pady=10)

    # ==== Score Box ====
    score_label = tk.Label(game_frame, text="Your Score Here", font=("Helvetica", 18, "bold"), bg=color_c, fg=color_e)
    score_label.pack()  # Hidden until needed

    # ==== Game Board ====
    board_frame = tk.Frame(game_frame, bg=color_c)
    board_frame.pack(pady=(20, 20))
    create_board(board_frame, w_w_grid)

    # ==== User Entry Box ====
    entry = tk.Entry(game_frame, font=("Helvetica", 16))
    entry.pack(pady=10)
    entry.config(state="disabled")

    # ==== Submit Entry Box ====
    submit_btn = tk.Button(game_frame, text="Submit Word", command=lambda: helper.submit_word(entry, submitted_words, submitted_listbox))
    submit_btn.pack(pady=5)
    submit_btn.config(state="disabled")

    # ==== Rotate ====
    def rotate_board():
        current_grid = nonlocal_grid[0]
        rotated_grid = list(zip(*current_grid[::-1]))  # 90° clockwise
        rotated_grid = [list(row) for row in rotated_grid]  # convert tuples back to lists
        nonlocal_grid[0] = rotated_grid
        helper.clear_frame(board_frame)
        create_board(board_frame, rotated_grid)

    rotate_button = tk.Button(game_frame, text="↻ Rotate Board", font=("Helvetica", 20), bg="#ccddff", command=rotate_board)
    rotate_button.pack(pady=5)

    # ==== Reshuffle ====
    def reshuffle_grid():
        if reshuffled[0]:
            return        
        for die in dice:
            random.shuffle(die)
        random.shuffle(dice)
        
        new_grid = helper.generate_grid_from_dice(dice, grid_size)
        nonlocal_grid[0] = new_grid
        helper.clear_frame(board_frame)
        create_board(board_frame, new_grid)

        reshuffle_button.config(state="disabled")
        reshuffled[0] = True

    reshuffle_button = tk.Button(game_frame, text="Reshuffle Grid", font=("Helvetica", 20), bg="#ffccaa", command=reshuffle_grid)
    reshuffle_button.pack(pady=5)

    # ==== Start Game ====
    def flash_board_start():
        original_color = board_frame.cget("bg")
        board_frame.config(bg="green")
        root.after(200, lambda: board_frame.config(bg=original_color))

    game_time = tk.IntVar(value=30)

    def start_game():        
        entry.config(state="normal")
        submit_btn.config(state="normal")
        helper.force_focus(root, entry)
        game_time.set(30)
        reshuffled[0] = False
        reshuffle_button.config(state="disabled")
        start_button.config(state="disabled")
        rotate_button.config(state="normal")
        flash_board_start()

        master_word_list[0] = helper.boggle_solver(nonlocal_grid[0], valid_words, prefixes)
        master_words_label.config(text=f"Number of Hidden Words:\n{len(master_word_list[0])}")
        start_timer(game_time, on_end=on_timer_end)

    start_button = tk.Button(game_frame, text="Start Game", font=("Helvetica", 14), bg="#aaffaa", command=start_game)
    start_button.pack(pady=10)

    # ==== Quit Button ====
    quit_button = tk.Button(game_frame, text="Quit", font=("Helvetica", 14), bg="red", command=root.quit)
    quit_button.pack(pady=(10))  # Adds top padding for spacing

    # ==== Timer ====
    def start_timer(game_time, on_end=None):
        if game_time.get() > 0:
            game_time.set(game_time.get() - 1)
            timer_label.config(text=f"Time Left: {game_time.get()}")
            root.after(1000, lambda: start_timer(game_time, on_end=on_end))
        else:
            entry.config(state="disabled")
            submit_btn.config(state="disabled")
            if on_end:
                on_end()  # Call your custom game-over logic
            else:
                root.after(1000, root.destroy)  # Default behavior: auto-close after 1 second
    
    # ============================ Set Up Right Frame ============================
    listbox_wrapper = tk.Frame(right_frame, bg=color_c)
    listbox_wrapper.pack(pady=10)

    #==== Submitted words header box ====
    submitted_words_label = tk.Label(listbox_wrapper, text="Words Submitted:", font=("Helvetica", 16, "bold"), bg=color_c, fg=color_e)
    submitted_words_label.pack(pady=10)

    #==== Submitted words list box ====
    submitted_listbox = tk.Listbox(listbox_wrapper, height=40, width=20, font=("Helvetica", 16), bg=color_b, fg=color_e)
    scrollbar = tk.Scrollbar(listbox_wrapper, orient="vertical", command=submitted_listbox.yview)
    scrollbar.pack(side="left", fill="y")
    submitted_listbox.config(yscrollcommand=scrollbar.set)
    submitted_listbox.pack(pady=10)

    # ============================ Set Up Left Frame ============================
    masterbox_wrapper = tk.Frame(left_frame, bg=color_c)
    masterbox_wrapper.pack(pady=10)

    #==== Master words header box ====
    master_words_label = tk.Label(masterbox_wrapper, text="Number of Hidden Words:\nCalculating...", font=("Helvetica", 16, "bold"), bg=color_c, fg=color_e)
    master_words_label.pack(pady=10)

    #==== Master words list box ====
    master_listbox = tk.Listbox(masterbox_wrapper, height=40, width=20, font=("Helvetica", 16), bg=color_b, fg=color_e)
    master_scrollbar = tk.Scrollbar(masterbox_wrapper, orient="vertical", command=master_listbox.yview)
    master_scrollbar.pack(side="right", fill="y")
    master_listbox.config(yscrollcommand=master_scrollbar.set)
    master_listbox.pack(pady=10)

    entry.bind('<Return>', lambda event: helper.submit_word(entry, submitted_words, submitted_listbox))

    # ============================ End Game ============================
    def on_timer_end():
        entry.config(state="disabled")
        submit_btn.config(state="disabled")
        entry.unbind('<Return>')

        def restart_game():
            main_screen.destroy()
            submitted_words.clear()
            master_word_list[0].clear()
            reshuffled[0] = False
            score_tracker[0] = 0
            whirl_words(num_dice, num_faces, grid_size)

        start_button.config(text="Play Again", command=restart_game)
        start_button.config(state="normal")

        dummy_focus = tk.Label(root)
        dummy_focus.pack()
        dummy_focus.focus_set()

        # NEW: split into two steps
        valid_entries, missed_words, score, total_possible_score = helper.validate_and_score(
            submitted_words, master_word_list[0]
        )
        score_tracker[0] = score

        score_label.config(text=f"You scored {score_tracker[0]}/{total_possible_score}!")
        master_listbox.delete(0, tk.END)
        for word in sorted(master_word_list[0]):
            master_listbox.insert(tk.END, word)
        
        submitted_words_label.config(text="Valid Words:")

        submitted_listbox.delete(0, tk.END)
        for word in sorted(valid_entries):
            submitted_listbox.insert(tk.END, word)

# ============================ UI Setup ============================
if __name__ == "__main__":
    # ==== Root Window ====
    root = tk.Tk()
    root.title("WhirlWords")
    root.configure(bg=color_a)
    root.state('zoomed')

    # ==== Game setup frame ====
    setup_frame = tk.Frame(root, bg=color_c)
    setup_frame.pack(expand=True)

    # ==== Welcome Box ====
    heading = tk.Label(setup_frame, text="Welcome to WhirlWords!", font=("Helvetica", 36, "bold"), fg=color_e, bg=color_c)
    heading.pack(pady=40)

    # ==== Instructions Box ====
    instructions = tk.Label(setup_frame, text="Configure your dice and let the Whirling commence!", font=("Helvetica", 24), fg=color_e, bg=color_c)
    instructions.pack(pady=10)

    # ==== Number of dice text box ====
    dice_frame = tk.Frame(setup_frame, bg=color_c)
    dice_frame_label = tk.Label(dice_frame, text="Number of Dice (min 9):", font=("Helvetica", 16), bg=color_c, fg=color_e).pack(side="left", padx=5)
    dice_frame.pack(pady=10)

    # ==== Number of dice entry box ====
    dice_entry = tk.Entry(dice_frame, font=("Helvetica", 16))
    dice_entry.pack(side="left")

    # ==== Sides per die text box ====
    face_frame = tk.Frame(setup_frame, bg=color_c)
    face_frame_label = tk.Label(face_frame, text="Number of Faces per Die (min 2):", font=("Helvetica", 16), bg=color_c, fg=color_e).pack(side="left", padx=5)
    face_frame.pack(pady=10)

    # ==== Sides per die entry box ====
    face_entry = tk.Entry(face_frame, font=("Helvetica", 16))
    face_entry.pack(side="left")

    # Feedback Label
    feedback_label = tk.Label(setup_frame, text="", font=("Helvetica", 14), bg=color_c, fg="red")
    feedback_label.pack(pady=10)

    def validate_and_start():
        try:
            num_dice = int(dice_entry.get())
            num_faces = int(face_entry.get())

            if num_dice < 9:
                feedback_label.config(text="You need at least 9 dice for a 3x3 grid.")
                return
            if num_faces < 2:
                feedback_label.config(text="Each die needs at least 2 faces. No chaos dice yet.")
                return

            nearest_perfect_square = math.ceil(math.sqrt(num_dice)) ** 2
            grid_size = int(math.sqrt(nearest_perfect_square))

            if nearest_perfect_square != num_dice:
                num_dice = nearest_perfect_square
                print(f"Rounding up to make a {grid_size}x{grid_size} grid.")
            
            try:  #Test if dice generation works before destroying setup screen
                test_dice = helper.letter_pool(num_faces, num_dice)
            except ValueError as e:
                feedback_label.config(text="Not enough letters to fill all dice. Try fewer dice or faces.")
                return

            # If all good, proceed
            setup_frame.destroy()
            whirl_words(num_dice, num_faces, grid_size)

        except ValueError:
            feedback_label.config(text="Please enter valid numbers.")

    start_button = tk.Button(setup_frame, text="Begin the Whirling", font=("Helvetica", 18), bg="#88cc88", command=validate_and_start)
    start_button.pack(pady=30)
    start_button.bind("<Return>", lambda event: validate_and_start())
    
    dice_entry.focus_set()

    root.mainloop()