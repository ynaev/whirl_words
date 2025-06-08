import os
import math

#def masterListCreator():

# Convert the Excel sheet into a grid (2D list)
grid = [[cell.value.upper() for cell in row] for row in ws.iter_rows()]

# Get grid dimensions
ROWS, COLS = len(grid), len(grid[0])

# Directions for moving in 8 directions (dx, dy)
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),         (0, 1),
              (1, -1), (1, 0), (1, 1)]

# Recursive DFS function to explore words
def find_words(x, y, path, visited, word, words_found, dictionary):
    if word in dictionary and len(word) > 2:
        words_found.add(word)  # Save valid words

    if len(word) > 10:  # Prevent excessive recursion depth
        return

    # Explore neighbors
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and (nx, ny) not in visited:
            find_words(nx, ny, path + [(nx, ny)], visited | {(nx, ny)}, word + grid[nx][ny], words_found, dictionary)

# Function to initiate word search from each letter
def boggle_solver(grid, dictionary):
    words_found = set()
    for i in range(ROWS):
        for j in range(COLS):
            find_words(i, j, [(i, j)], {(i, j)}, grid[i][j], words_found, dictionary)
    return words_found

# Load dictionary and find words
dictionary = load_dictionary()
found_words = boggle_solver(grid, dictionary)

# Display results
print("Words found:", sorted(found_words))
