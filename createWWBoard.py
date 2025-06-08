import tkinter as tk

def createWWBoard(wWGrid):
    #Create a main window
    root = tk.Tk()
    root.title("WhirlWords Grid")
    
    #Iterate over your chosen letters to create a grid
    for i, row in enumerate(wWGrid):
        for j, letter in enumerate(row):
            # Create a label for each letter and place it in a grid
            label = tk.Label(root, text=letter, width=5, height=2, relief="solid", anchor="center")
            label.grid(row=i, column=j, padx=5, pady=5)
    
    root.mainloop()  #Run the tkinter event loop

# Example 4x4 grid of letters
grid_letters = [
    ["T", "R", "A", "P"],
    ["E", "O", "L", "S"],
    ["M", "B", "I", "N"],
    ["C", "K", "U", "D"]
]

def create_board(grid):
    rows, cols = len(grid), len(grid[0])

    root = tk.Tk()
    root.title("WhirlWords Grid")

    square_size = 80

    canvas = tk.Canvas(root, width=cols * square_size, height=rows * square_size)
    canvas.pack()

    for i in range(rows):
        for j in range(cols):
            x1 = j * square_size
            y1 = i * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size

            # Draw square
            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

            # Draw letter (centered)
            canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2 - 10,
                text=grid[i][j],
                font=("Consolas", 24, "bold")
            )

            # Draw coordinates
            canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2 + 20,
                text=f"({i},{j})",
                font=("Consolas", 10),
                fill="gray"
            )

    root.mainloop()

if __name__ == "__main__":
    create_board(grid_letters)
