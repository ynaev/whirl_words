import tkinter as tk

square_size = 100
color_b = "#212B40"
color_d = "#A68C6D"

def create_board(board_frame, grid):
    """
    Draws a grid-based game board using Tkinter Canvas.
    
    Args:
        parent: The Tkinter root or frame to attach the Canvas to.
        grid: 2D list of letters representing the board layout.
    """
    rows, cols = len(grid), len(grid[0])
    canvas = tk.Canvas(board_frame, width=cols * square_size, height=rows * square_size)
    canvas.pack(padx=5, pady=5)

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
            canvas.create_rectangle(x1, y1, x2, y2, fill=color_d, outline=color_b, width=8)

            #Draw letter slightly above center
            canvas.create_text(
                cx,
                cy - 10,
                text=str(grid[i][j]),
                font=("Georgia", 28, "bold"),
                fill="#073642"
            )

            #Draw cell coordinates slightly below center
            show_coords = False
            if show_coords:
                canvas.create_text(
                    cx,
                    cy + 20,
                    text=f"({i},{j})",
                    font=("Consolas", 10),
                    fill="gray"
                )
