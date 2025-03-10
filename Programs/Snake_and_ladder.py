import tkinter as tk
from tkinter import messagebox
import random

class CuteSnakeAndLadder:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake & Ladder")
        self.window.geometry("550x600")
        self.window.configure(bg="#FFEBF6")  # Light Pink Background

        # Game variables
        self.player_position = 1
        self.computer_position = 1

        # Snakes & Ladders (positions)
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

        # Create UI
        self.create_board()
        self.create_controls()

    def create_board(self):
        self.board_frame = tk.Frame(self.window, bg="#FFEBF6")
        self.board_frame.pack(pady=10)

        self.cells = {}
        number = 100
        for i in range(10):
            for j in range(10):
                cell = tk.Frame(self.board_frame, borderwidth=1, relief="solid", width=45, height=45, bg="#FFF5F9")
                cell.grid_propagate(False)
                cell.grid(row=i, column=j, padx=1, pady=1)

                label = tk.Label(cell, text=str(number), font=('Comic Sans MS', 9, 'bold'), bg="#FFF5F9")
                label.place(relx=0.5, rely=0.5, anchor="center")

                self.cells[number] = cell
                number -= 1

        # Color snake and ladder cells
        for snake in self.snakes:
            self.cells[snake].configure(bg='#FF9AA2')  # Soft Pink for Snakes 🐍
        for ladder in self.ladders:
            self.cells[ladder].configure(bg='#B5EAD7')  # Soft Green for Ladders 🪜

    def create_controls(self):
        self.control_frame = tk.Frame(self.window, bg="#FFEBF6")
        self.control_frame.pack(pady=10)

        # Player & Computer Info
        self.player_label = tk.Label(self.control_frame, text="🐰 Player: 1", font=('Comic Sans MS', 12, 'bold'),
                                     bg="#FFD3E3", fg="black", padx=10, pady=5, relief="ridge")
        self.player_label.grid(row=0, column=0, padx=10)

        self.computer_label = tk.Label(self.control_frame, text="🐻 Computer: 1", font=('Comic Sans MS', 12, 'bold'),
                                       bg="#FFD3E3", fg="black", padx=10, pady=5, relief="ridge")
        self.computer_label.grid(row=0, column=1, padx=10)

        # Dice Roll Button
        self.roll_button = tk.Button(self.control_frame, text="🎲 Roll Dice", font=('Comic Sans MS', 14, 'bold'),
                                     bg="#FFC3A0", fg="black", width=12, height=1, relief="ridge",
                                     command=self.play_turn)
        self.roll_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.update_positions()

    def play_turn(self):
        # Player's turn
        dice_roll = random.randint(1, 6)
        messagebox.showinfo("🎲 Cute Dice!", f"🐰 You rolled: {dice_roll} 🎲")
        self.move_player(dice_roll)
        if self.player_position == 100:
            messagebox.showinfo("🎉 Yay!", "🐰 You win! 🎀🎊")
            self.window.quit()
            return

        # Computer's turn
        dice_roll = random.randint(1, 6)
        messagebox.showinfo("🎲 Cute Dice!", f"🐻 Computer rolled: {dice_roll} 🎲")
        self.move_computer(dice_roll)
        if self.computer_position == 100:
            messagebox.showinfo("😢 Oh no!", "🐻 Computer wins! 😭")
            self.window.quit()

    def move_player(self, steps):
        new_position = self.player_position + steps
        if new_position <= 100:
            self.player_position = new_position
            if self.player_position in self.snakes:
                messagebox.showinfo("🐍 Oh No!", "🐰 You got bit by a cute snake! 😭")
                self.player_position = self.snakes[self.player_position]
            if self.player_position in self.ladders:
                messagebox.showinfo("🪜 Yay!", "🐰 You climbed a ladder! 🎉")
                self.player_position = self.ladders[self.player_position]
        self.update_positions()

    def move_computer(self, steps):
        new_position = self.computer_position + steps
        if new_position <= 100:
            self.computer_position = new_position
            if self.computer_position in self.snakes:
                messagebox.showinfo("🐍 Oh No!", "🐻 Computer got bit by a snake! 😆")
                self.computer_position = self.snakes[self.computer_position]
            if self.computer_position in self.ladders:
                messagebox.showinfo("🪜 Yay!", "🐻 Computer climbed a ladder! 🎉")
                self.computer_position = self.ladders[self.computer_position]
        self.update_positions()

    def update_positions(self):
        for cell in self.cells.values():
            for widget in cell.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.destroy()

        # 🐰 Player Token
        player_cell = self.cells[self.player_position]
        player_token = tk.Canvas(player_cell, width=20, height=20, bg="#FFF5F9", highlightthickness=0)
        player_token.create_oval(2, 2, 18, 18, fill='pink')  # Cute pink token
        player_token.place(relx=0.3, rely=0.5, anchor="center")

        # 🐻 Computer Token
        computer_cell = self.cells[self.computer_position]
        computer_token = tk.Canvas(computer_cell, width=20, height=20, bg="#FFF5F9", highlightthickness=0)
        computer_token.create_oval(2, 2, 18, 18, fill='brown')  # Cute brown token
        computer_token.place(relx=0.7, rely=0.5, anchor="center")

        self.player_label.configure(text=f"🐰 Player: {self.player_position}")
        self.computer_label.configure(text=f"🐻 Computer: {self.computer_position}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = CuteSnakeAndLadder()
    game.run()
