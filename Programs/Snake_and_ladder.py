import tkinter as tk
import random
import time
from PIL import Image, ImageTk

# Snakes and Ladders positions
snakes = {97: 61, 91: 73, 76: 54, 51: 10, 38: 20}
ladders = {5: 58, 14: 49, 53: 72, 64: 83}

class SnakesLaddersGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snakes and Ladders")
        
        self.canvas = tk.Canvas(self.master, width=600, height=600)
        self.canvas.pack()
        
        # Load and display the board image
        self.board_image = Image.open(r"C:\Users\KIIT\Desktop\Work\AI-LAB-6TH-SEM\board.jpg")
        self.board_image = self.board_image.resize((600, 600), Image.Resampling.LANCZOS)
        self.board_photo = ImageTk.PhotoImage(self.board_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.board_photo)
        
        self.player_positions = {"Player 1": 1, "Player 2": 1}
        self.player_icons = {}
        
        # Create player tokens
        self.player_icons["Player 1"] = self.canvas.create_oval(10, 550, 30, 570, fill="red")
        self.player_icons["Player 2"] = self.canvas.create_oval(40, 550, 60, 570, fill="blue")
        
        self.turn = "Player 1"
        
        self.label = tk.Label(self.master, text=f"{self.turn}'s turn", font=("Arial", 14))
        self.label.pack()
        
        self.dice_label = tk.Label(self.master, text="Roll the dice!", font=("Arial", 14))
        self.dice_label.pack()
        
        self.roll_button = tk.Button(self.master, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack()
        
    def roll_dice(self):
        if not self.master.winfo_exists():
            return
        
        roll = random.randint(1, 6)
        self.dice_label.config(text=f"Rolled: {roll}")
        
        new_position = self.player_positions[self.turn] + roll
        if new_position > 100:
            self.switch_turn()
            return
        
        if new_position in snakes:
            new_position = snakes[new_position]
        elif new_position in ladders:
            new_position = ladders[new_position]
        
        self.animate_movement(self.turn, self.player_positions[self.turn], new_position)
        self.player_positions[self.turn] = new_position
        
        if new_position == 100:
            if self.label.winfo_exists():
                self.label.config(text=f"{self.turn} wins!")
            self.roll_button.config(state=tk.DISABLED)
        else:
            self.switch_turn()
        
    def animate_movement(self, player, start, end):
        step = 1 if end > start else -1
        for pos in range(start + step, end + step, step):
            if not self.master.winfo_exists():
                return
            x, y = self.get_coordinates(pos)
            if self.canvas.winfo_exists():
                self.canvas.coords(self.player_icons[player], x, y, x+20, y+20)
            self.master.update()
            time.sleep(0.3)
        
    def get_coordinates(self, position):
        row = (position - 1) // 10
        col = (position - 1) % 10
        if row % 2 == 1:
            col = 9 - col
        x = col * 60 + 10
        y = (9 - row) * 60 + 10
        return x, y
        
    def switch_turn(self):
        if not self.master.winfo_exists():
            return
        self.turn = "Player 1" if self.turn == "Player 2" else "Player 2"
        if self.label.winfo_exists():
            self.label.config(text=f"{self.turn}'s turn")
        
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakesLaddersGame(root)
    root.mainloop()
