import random
import tkinter as tk

#=================================================================================================
def letter_pool(num_faces, num_dice):
    """
    Generates a list of dice, each with a balanced selection of letters.
    Enforces:
        - max 2 vowels per die
        - max 2 special letters per die
        - no duplicates per die
    """
    def is_valid_die(die):
        vowels = {'A', 'E', 'I', 'O', 'U'}
        specials = {'B', 'C', 'J', 'K', 'QU', 'V', 'W', 'X', 'Z'}

        normalized = [ltr.upper() for ltr in die]  # Ensure all are uppercase
        no_duplicates = len(set(normalized)) == len(normalized)

        vowel_count = sum(1 for ltr in normalized if ltr in vowels)
        special_count = sum(1 for ltr in normalized if ltr in specials)

        return no_duplicates and vowel_count <= 2 and special_count <= 2

    letter_probabilities = {
        'A': 8.33, 'B': 3.12, 'C': 3.12, 'D': 4.17, 'E': 10.42,
        'F': 2.08, 'G': 3.12, 'H': 3.12, 'I': 7.29, 'J': 1.04,
        'K': 2.08, 'L': 5.21, 'M': 3.12, 'N': 5.21, 'O': 6.25,
        'P': 3.12, 'Qu': 1.04, 'R': 4.17, 'S': 5.21, 'T': 5.21,
        'U': 4.17, 'V': 2.08, 'W': 2.08, 'X': 1.04, 'Y': 3.12,
        'Z': 1.04
    }

    letters = list(letter_probabilities.keys())
    weights = list(letter_probabilities.values())

    max_attempts = 1000  # To prevent infinite loops
    dice = []

    attempts = 0
    while len(dice) < num_dice and attempts < max_attempts:
        attempts += 1
        pool = random.choices(letters, weights=weights, k=num_faces)
        
        # Ensure no duplicates and check other constraints
        if is_valid_die(pool):
            dice.append(pool)

    if len(dice) < num_dice:
        print(f"⚠️ Only generated {len(dice)} of {num_dice} dice after {max_attempts} attempts.")
        print("⚠️ Dice factory jammed. May contain cursed cubes.")

    # Final shuffle for fairness
    for die in dice:
        random.shuffle(die)

    return dice

#=================================================================================================
def generate_grid_from_dice(dice, grid_size):
    """Selects one random letter per die and arranges them into a 2D grid."""
    selected_letters = [random.choice(die) for die in dice]  #Grabs one letter from each die
    grid = [selected_letters[i:i + grid_size] for i in range(0, len(selected_letters), grid_size)]
    return grid

#=================================================================================================
def boggle_solver(grid, dictionary, prefixes):
    """Runs a full grid DFS to find all valid words."""
    words_found = set()  #Instantiate the words list
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            find_words(i, j, [(i, j)], {(i, j)}, grid[i][j], words_found, dictionary, grid, prefixes)  #Call to function find_words
    return words_found

#=================================================================================================
directions = [(-1, -1), (-1, 0), (-1, 1),  #Directions for moving in 8 directions (dx, dy)
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

def find_words(x, y, path, visited, word, words_found, dictionary, w_w_grid, prefixes):
    """Recursive DFS function to explore all word paths."""
    word = word.lower()

    if len(word) > 2 and word not in prefixes:
        return
    
    if word in dictionary and len(word) > 2:
        words_found.add(word)

    rows, cols = len(w_w_grid), len(w_w_grid[0])

    # Explore neighbors
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
            find_words(nx, ny, path + [(nx, ny)], visited | {(nx, ny)}, word + w_w_grid[nx][ny], words_found, dictionary, w_w_grid, prefixes)

#=================================================================================================
def submit_word(entry_widget, submitted_words, listbox_widget):
    word = entry_widget.get().strip().lower()

    if not word:
        return

    if word in submitted_words:
        entry_widget.delete(0, tk.END)

        # Flash red background
        original_color = entry_widget.cget("bg")
        entry_widget.config(bg="red")
        entry_widget.after(200, lambda: entry_widget.config(bg=original_color))

        return

    submitted_words.append(word)
    listbox_widget.insert(tk.END, word)
    entry_widget.delete(0, tk.END)

#=================================================================================================
def calculate_score(word):
    """Returns the score of a word based on length."""
    length = len(word)
    if length < 3:
        return 0
    elif length <= 4:
        return 1
    elif length == 5:
        return 2
    elif length == 6:
        return 3
    elif length == 7:
        return 5
    else:
        return 11

#=================================================================================================    
def force_focus(root, entry):
    """Brings the game window to front and focuses the entry field."""
    root.deiconify()  #Show the window (in case it's minimized)
    root.lift()  #Bring it to the front
    root.attributes('-topmost', True)  #Stay on top
    root.after(500, lambda: root.attributes('-topmost', False))  #Drop "always on top"
    root.focus_force()  #Try to grab focus
    entry.focus_set()  #Set cursor in the text box too

#=================================================================================================
def clear_frame(frame):
    """Destroys all widgets in a frame."""
    for widget in frame.winfo_children():
        widget.destroy()

#=================================================================================================
def validate_and_score(submitted_words, master_word_list):
    """
    Returns:
    - valid_entries: list of submitted words that are correct
    - missed_words: list of valid words not found
    - score: score from valid entries
    - total_possible_score: score from all possible valid words
    """
    valid_entries = sorted([word for word in submitted_words if word in master_word_list])
    missed_words = sorted(master_word_list - set(valid_entries))
    score = sum(calculate_score(word) for word in valid_entries)
    total_possible_score = sum(calculate_score(word) for word in master_word_list)
    return valid_entries, missed_words, score, total_possible_score

#=================================================================================================
def build_prefix_set(words):
    """Returns a set of all possible prefixes from a word list."""
    prefixes = set()
    return {word[:i+1] for word in words for i in range(len(word))}
