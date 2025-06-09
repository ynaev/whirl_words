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
def submit_word(entry, submitted_words, valid_words):
        import tkinter as tk
        word = entry.get().strip().lower()  #grab the text and clean whitespace
        if word:
            print(f"You submitted: {word}")
            entry.delete(0, tk.END)  # Clear the box after submission
        if not word:
            return #Do nothing on an empty input
        
        if word in submitted_words:
            print(f"You've already submitted {word}. Try again.")
        else:
            if word in valid_words:
                submitted_words.append(word)
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