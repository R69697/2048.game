import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.game_over = False
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.create_widgets()
        self.initialize_game()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        self.canvas.pack()
        self.master.bind("<Key>", self.handle_keypress)

    def initialize_game(self):
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

    def add_new_tile(self):
        empty_tiles = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def slide_left(self):
        moved = False
        for row in self.grid:
            original = row[:]
            filtered = [num for num in row if num != 0]
            for i in range(len(filtered) - 1):
                if filtered[i] == filtered[i + 1]:
                    filtered[i] *= 2
                    filtered[i + 1] = 0
                    self.score += filtered[i]
            filtered = [num for num in filtered if num != 0]
            row[:] = filtered + [0] * (4 - len(filtered))
            if row != original:
                moved = True
        return moved

    def slide_right(self):
        self.grid = [row[::-1] for row in self.grid]
        moved = self.slide_left()
        self.grid = [row[::-1] for row in self.grid]
        return moved

    def slide_up(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self.slide_left()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved

    def slide_down(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self.slide_right()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved

    def handle_keypress(self, event):
        if self.game_over:
            return
        if event.keysym in ("Left", "Right", "Up", "Down"):
            moved = False
            if event.keysym == "Left":
                moved = self.slide_left()
            elif event.keysym == "Right":
                moved = self.slide_right()
            elif event.keysym == "Up":
                moved = self.slide_up()
            elif event.keysym == "Down":
                moved = self.slide_down()
            if moved:
                self.add_new_tile()
                self.update_ui()
                if not self.can_move():
                    self.game_over = True
                    self.show_game_over()

    def update_ui(self):
        self.canvas.delete("all")
        for r in range(4):
            for c in range(4):
                value = self.grid[r][c]
                if value:
                    self.canvas.create_rectangle(c * 100, r * 100, c * 100 + 100, r * 100 + 100, fill=self.get_color(value))
                    self.canvas.create_text(c * 100 + 50, r * 100 + 50, text=str(value), font=("Arial", 24, "bold"))

    def get_color(self, value):
        colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#cdc1b4")

    def can_move(self):
        for r in range(4):
            for c in range(4):
                if self.grid[r][c] == 0:
                    return True
                if c < 3 and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r < 3 and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    def show_game_over(self):
        self.canvas.create_text(200, 200, text="Game Over!", font=("Arial", 32, "bold"), fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

