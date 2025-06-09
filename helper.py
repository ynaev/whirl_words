#=================================================================================================
def letter_pool(total_tiles, num_dice, num_faces):
    import random

    high_value_letters = {'C', 'J', 'K', 'Qu', 'V', 'X', 'Z'}

    letter_probabilities = {
        'A': 7, 'B': 3, 'C': 2, 'D': 6, 'E': 10,
        'F': 4, 'G': 3, 'H': 3, 'I': 5, 'J': 2,
        'K': 2, 'L': 4, 'M': 3, 'N': 4, 'O': 6,
        'P': 3, 'Qu': 1, 'R': 4, 'S': 5, 'T': 6,
        'U': 4, 'V': 2, 'W': 3, 'X': 2, 'Y': 4,
        'Z': 2
    }

    letters = list(letter_probabilities.keys())
    weights = list(letter_probabilities.values())

    raw_pool = random.choices(letters, weights=weights, k=total_tiles)  #Generate a raw pool of letters using weighted probabilities

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
    import random
    
    selected_letters = [random.choice(die) for die in dice]  #Grabs one letter from each die
    grid = [
        selected_letters[i:i + grid_size]
        for i in range(0, len(selected_letters), grid_size)
    ]

    return grid

#=================================================================================================
#Search the board and store words into the dictionary.
def boggle_solver(w_w_grid, dictionary):
    words_found = set()  #Instantiate the words list
    rows, cols = len(w_w_grid), len(w_w_grid[0])
    for i in range(rows):
        for j in range(cols):
            find_words(i, j, [(i, j)], {(i, j)}, w_w_grid[i][j], words_found, dictionary, w_w_grid)  #Call to function find_words
    return words_found

#=================================================================================================
# Directions for moving in 8 directions (dx, dy)
directions = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0),  (1, 1)]

def find_words(x, y, path, visited, word, words_found, dictionary, w_w_grid):
    if word in dictionary and len(word) > 2:
        words_found.add(word)

    if len(word) > 10:  # You can adjust this limit if needed
        return

    rows, cols = len(w_w_grid), len(w_w_grid[0])

    # Explore neighbors
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
            find_words(nx, ny,
                    path + [(nx, ny)],
                    visited | {(nx, ny)},
                    word + w_w_grid[nx][ny],
                    words_found, dictionary)

#=================================================================================================
def submit_word(entry, submitted_words, valid_words, score_label, score_tracker, submitted_listbox):
        import tkinter as tk

        word = entry.get().strip().lower()  #grab the text and clean whitespace
        if word:            
            entry.delete(0, tk.END)  #Clear the box after submission
        if not word:
            return #Do nothing on an empty input
        if word in submitted_words:
            print(f"You've already submitted {word}. Try again.")
        else:
            if word in valid_words:
                submitted_words.append(word)
                submitted_listbox.insert(tk.END, word)  # Add word to listbox
                points = calculate_score(word)
                score_tracker[0] += points
                score_label.config(text=f"Score: {score_tracker[0]}")
            else:
                print(f"{word} is not found in the dictionary. Try again.")

#=================================================================================================
def start_timer(root, timer_label, entry, submit_btn, game_time):
    if game_time > 0:        
        game_time -= 1
        timer_label.config(text=f"Time Left: {game_time}")
        root.after(1000, lambda: start_timer(root, timer_label, entry, submit_btn, game_time))
    else:
        entry.config(state="disabled")
        submit_btn.config(state="disabled")
        print("Time’s up!")
        root.after(1000, root.destroy)  #Automatically close the window after 1 second delay

#=================================================================================================
def calculate_score(word):
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
    root.deiconify()  #Show the window (in case it's minimized)
    root.lift()  #Bring it to the front
    root.attributes('-topmost', True)  #Stay on top
    root.after(500, lambda: root.attributes('-topmost', False))  #Drop "always on top"
    root.focus_force()  #Try to grab focus
    entry.focus_set()  #Set cursor in the text box too