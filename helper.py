import random
import tkinter as tk

#=================================================================================================
def letter_pool(num_faces, num_dice):
    """
    Generates a list of dice, each with a balanced selection of letters.
    Ensures high-value letters are evenly distributed across dice.
    """
    high_value_letters = {'B', 'C', 'J', 'K', 'Qu', 'V', 'W', 'X', 'Z'}

    letter_probabilities = {
        'A': 7.5, 'B': 2.9, 'C': 1.7, 'D': 6, 'E': 10.8,
        'F': 4, 'G': 3, 'H': 3, 'I': 5, 'J': 2,
        'K': 2, 'L': 4, 'M': 3, 'N': 4, 'O': 6,
        'P': 3, 'Qu': 1, 'R': 4, 'S': 5, 'T': 6,
        'U': 4, 'V': 2, 'W': 2.8, 'X': 1.5, 'Y': 4,
        'Z': 2
    }

    letters = list(letter_probabilities.keys())
    weights = list(letter_probabilities.values())

    raw_pool = random.choices(letters, weights=weights, k=num_faces * num_dice)  #Generate a raw pool of letters using weighted probabilities
    high_value_pool = [ltr for ltr in raw_pool if ltr in high_value_letters]  #Extract high-value letters from the raw pool
    random.shuffle(high_value_pool)  #Shuffle to randomize which ones are chosen

    max_allowed = min(len(high_value_pool), num_dice)  #Limit to one high-value letter per die (or fewer if there aren’t enough)
    selected_hv = high_value_pool[:max_allowed]
    for hv in selected_hv:  #Remove those selected high-value letters from the pool to avoid duplicates
        raw_pool.remove(hv)

    dice = [[] for _ in range(num_dice)]  #Prepare an empty list for each die

    for i in range(len(selected_hv)):  #Iterate through the list of high-value letters
        dice[i].append(selected_hv[i])  #Add one high-value letter per die (only to as many dice as selected_hv)

    for die in dice:  #Fill in the remaining spaces on each die with random letters from the pool
        needed = num_faces - len(die)
        chosen = random.sample(raw_pool, needed)
        die.extend(chosen)
        for ltr in chosen:
            raw_pool.remove(ltr)

    leftover = num_dice * num_faces - sum(len(d) for d in dice)  #Check for any imbalance (usually caused by not enough letters left)
    if leftover > 0:
        print("⚠️ Warning: Could not fully balance dice. Game may contain dangerous levels of spice.")

    for die in dice:  #Shuffle each die so high-value letters aren’t always first
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
