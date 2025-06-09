import tkinter as tk

square_size = 100  # You could also move this to a config module later

def create_board(parent, grid):
    """
    Draws a grid-based game board using Tkinter Canvas.
    
    Args:
        parent: The Tkinter root or frame to attach the Canvas to.
        grid: 2D list of letters representing the board layout.
    """
    rows, cols = len(grid), len(grid[0])
    canvas = tk.Canvas(parent, width=cols * square_size, height=rows * square_size)
    canvas.pack()

    for i in range(rows):
        for j in range(cols):
            x1 = j * square_size
            y1 = i * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size

            #Compute center coordinates once
            cx = x1 + square_size // 2
            cy = y1 + square_size // 2

            #Draw square
            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

            #Draw letter slightly above center
            canvas.create_text(
                cx,
                cy - 10,
                text=grid[i][j],
                font=("Consolas", 24, "bold")
            )

            #Draw cell coordinates slightly below center
            show_coords = True  #Set to False later for "clean" mode
            if show_coords:
                canvas.create_text(
                    cx,
                    cy + 20,
                    text=f"({i},{j})",
                    font=("Consolas", 10),
                    fill="gray"
                )
