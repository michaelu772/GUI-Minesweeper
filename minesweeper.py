import tkinter as tk
from tkinter import messagebox
import random


GRID_HEIGHT = 20
GRID_WIDTH = 12
NUM_MINES = 30

DEBUG = 0
COVERED_TILE_COLOR = "#f0f0f0"
UNCOVERED_TILE_COLOR = "#bdbdbd"
FLAGGED_TILE_COLOR = "silver"
BUTTON_WIDTH = 2
BUTTON_HEIGHT = 1

NUMBERED_COLORS = {
    1: "#0000FF",
    2: "#339933",
    3: "#FF0000",
    4: "#000080",
    5: "#800000",
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128),
}


def get_color(x):
    return NUMBERED_COLORS[x]


def get_middle_of_board(x):
    if x % 2 == 0:
        return int(x / 2)
    else:
        return int(x / 2)


class InputWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("New Game")

        self.width = tk.IntVar()
        self.height = tk.IntVar()
        self.num_bombs = tk.IntVar()

        tk.Label(self, text="Board width:").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.width).grid(row=0, column=1)
        tk.Label(self, text="Board height:").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.height).grid(row=1, column=1)
        tk.Label(self, text="Number of bombs:").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.num_bombs).grid(row=2, column=1)

        tk.Button(self, text="Start", command=self.start_game).grid(row=3, columnspan=2)

    def start_game(self):
        self.destroy()


class Minesweeper:
    def __init__(self, master):
        # Create the main window
        self.marked_bombs = NUM_MINES
        self.master = master
        self.master.title("Minesweeper")
        reset = tk.Button(self.master, text="Reset")



        # Create the grid of squares
        self.grid = []
        for row in range(GRID_HEIGHT):
            self.grid.append([])
            for col in range(GRID_WIDTH):
                button = tk.Button(master, font="unispace" ,width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda row=row, col=col: self.reveal_number(row, col))
                button.bind("<3>", lambda event, row=row, col=col: self.flag(row, col))
                button.grid(row=row, column=col)
                self.grid[row].append(button)

        top_button = tk.Button(master, font="unispace", text=':)', width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: self.reset_game())
        top_button.grid(row=GRID_HEIGHT, column=get_middle_of_board(GRID_WIDTH))

        # Place mines randomly
        self.mines = set()
        while len(self.mines) < NUM_MINES:
            self.mines.add((random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1)))

    def reset_game(self):
        self.master.destroy()
        root = tk.Tk()
        mine_sweeper = Minesweeper(root)
        root.mainloop()

    def get_neighbors(self, list_of_coordinates):
        neighbors = []
        for (x, y) in list_of_coordinates:

            temp_x = x
            temp_y = y
            for i in range(3):
                if i == 0:
                    temp_x -= 1
                    temp_y -= 1
                    if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_HEIGHT and temp_y < GRID_WIDTH):
                        neighbors.append((temp_x, temp_y))
                    continue

                temp_x += 1
                if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_HEIGHT and temp_y < GRID_WIDTH):
                    neighbors.append((temp_x, temp_y))

            temp_x = x
            temp_y = y
            for i in range(3):
                if i == 0:
                    temp_x -= 1
                    if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_HEIGHT and temp_y < GRID_WIDTH):
                        neighbors.append((temp_x, temp_y))
                    continue

                if i == 1:
                    continue

                temp_x += 2
                if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_HEIGHT and temp_y < GRID_WIDTH):
                    neighbors.append((temp_x, temp_y))

            temp_x = x
            temp_y = y
            for i in range(3):
                if i == 0:
                    temp_x -= 1
                    temp_y += 1
                    if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_HEIGHT and temp_y < GRID_WIDTH):
                        neighbors.append((temp_x, temp_y))
                    continue

                temp_x += 1
                if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_HEIGHT and temp_y < GRID_WIDTH):
                    neighbors.append((temp_x, temp_y))

        if DEBUG:
            print(f"Sending back: {neighbors}")

        return neighbors

    def flag(self, row, col):

        # If button is already flagged, unflag it
        if self.grid[row][col]["bg"] == FLAGGED_TILE_COLOR:
            self.grid[row][col]["text"] = ""
            self.grid[row][col]["bg"] = COVERED_TILE_COLOR
            # self.grid[row][col]["state"] = "normal"
            self.marked_bombs += 1
            return

        # If the button is already revealed, do nothing
        if self.grid[row][col]["text"] != "":
            return

        # Flag the button with an X
        if self.marked_bombs > 0:
            self.grid[row][col]["text"] = "X"
            self.grid[row][col]["bg"] = FLAGGED_TILE_COLOR
            # self.grid[row][col]["state"] = "disabled"
            self.marked_bombs -= 1

        if self.check_game_complete():
            self.uncover_mines()
            messagebox.showinfo("Congrats!", "You win!")
            self.master.destroy()
            return

    def check_game_complete(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.grid[i][j]["bg"] != UNCOVERED_TILE_COLOR and (i, j) not in self.mines:
                    return False

        # Return true if every tile is "disabled" or a bomb
        return True

    # UNCOVERS ALL BOMBS IF BOMB IS HIT
    def uncover_mines(self):
        for (x, y) in self.mines:
            self.grid[x][y]["text"] = "B"
            self.grid[x][y]["fg"] = "white"
            self.grid[x][y]["bg"] = "black"

    def uncover_square_with_col(self, x, y, num_of_bombs):
        self.grid[x][y]["text"] = str(num_of_bombs)
        self.grid[x][y]["fg"] = get_color(num_of_bombs)
        self.grid[x][y]["bg"] = UNCOVERED_TILE_COLOR  # get_color(num_of_bombs)

    # assumes it always gets an empty coord
    def flood_fill(self, row, col):
        empty_neighbors = []
        continue_flag = False

        self.grid[row][col]["text"] = " "
        self.grid[row][col]["bg"] = UNCOVERED_TILE_COLOR
        self.grid[row][col]["state"] = "disabled"

        neighbors = self.get_neighbors([(row, col)])

        if DEBUG:
            print(f"neighbors of {row, col} = {neighbors}")

        # return

        for x, y in neighbors:
            if self.mines_touching([(x, y)]) != 0:
                self.reveal_number(x, y)
            elif self.grid[x][y]["state"] != "disabled":
                self.grid[x][y]["text"] = " "
                self.grid[row][col]["bg"] = UNCOVERED_TILE_COLOR
                self.grid[x][y]["state"] = "disabled"
                empty_neighbors.append((x, y))
                continue_flag = True

        if not continue_flag:
            return

        for x, y in empty_neighbors:
            self.flood_fill(x, y)

    def mines_touching(self, coord):
        # Count the number of mines adjacent to this square
        for (row, col) in coord:
            num_adjacent_mines = 0
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if (r, c) in self.mines:
                        num_adjacent_mines += 1

        return num_adjacent_mines

    def reveal_number(self, row, col):

        if self.grid[row][col]["bg"] == FLAGGED_TILE_COLOR:
            return

        if (row, col) in self.mines:
            self.uncover_mines()
            result = messagebox.askquestion("Game Over", "You hit a mine! Would you like to play again?")
            if result == 'yes':
                self.reset_game()
            else:
                self.master.destroy()
                quit()

        num_of_bombs = self.mines_touching([(row, col)])
        if num_of_bombs == 0:
            self.flood_fill(row, col)
        else:
            # self.grid[row][col].configure(bg='#bdbdbd')
            self.uncover_square_with_col(row, col, num_of_bombs)

        if self.check_game_complete():
            self.uncover_mines()
            messagebox.showinfo("Congratulations!", "You win!")
            self.master.destroy()
            return


if __name__ == '__main__':
    # Create the game and start the main loop
    root = tk.Tk()
    root.withdraw()
    input_win = InputWindow(root)
    root.wait_window(input_win)

    GRID_WIDTH = input_win.width.get()
    GRID_HEIGHT = input_win.height.get()
    NUM_MINES = input_win.num_bombs.get()

    mine_sweeper = Minesweeper(root)
    root.deiconify()
    root.mainloop()


