import tkinter as tk
from tkinter import messagebox
import random
import time

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe vs AI")
        self.current_player = "X"  # Player is X, AI is O
        self.board = [""] * 9
        self.buttons = []
        self.scores = {"Player": 0, "AI": 0, "Tie": 0}
        self.game_active = True
        
        # Soft, classy color palette
        self.colors = {
            'bg': '#F5F5F5',           # Soft white
            'button': '#E8E8E8',       # Light gray
            'button_hover': '#D0D0D0', # Slightly darker gray
            'player_x': '#7C9CB0',     # Soft blue
            'player_o': '#B07C9C',     # Soft purple
            'win_highlight': '#98B07C', # Soft green
            'text': '#5A5A5A',         # Dark gray
            'reset_btn': '#B0967C'     # Soft brown
        }
        
        # Configure window
        self.window.configure(bg=self.colors['bg'])
        self.window.resizable(False, False)
        
        # Create score labels
        self.create_score_board()
        
        # Create game board
        self.create_board()
        
        # Create reset button
        self.create_reset_button()

    def create_score_board(self):
        score_frame = tk.Frame(self.window, bg=self.colors['bg'])
        score_frame.pack(pady=10)
        
        # Player score
        tk.Label(score_frame, text="Player:", font=('Helvetica', 12, 'bold'), 
                bg=self.colors['bg'], fg=self.colors['text']).grid(row=0, column=0, padx=5)
        self.player_score_label = tk.Label(score_frame, text="0", font=('Helvetica', 12, 'bold'),
                                    bg=self.colors['bg'], fg=self.colors['player_x'])
        self.player_score_label.grid(row=0, column=1, padx=5)
        
        # Tie score
        tk.Label(score_frame, text="Ties:", font=('Helvetica', 12, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text']).grid(row=0, column=2, padx=5)
        self.tie_score_label = tk.Label(score_frame, text="0", font=('Helvetica', 12, 'bold'),
                                      bg=self.colors['bg'], fg=self.colors['text'])
        self.tie_score_label.grid(row=0, column=3, padx=5)
        
        # AI score
        tk.Label(score_frame, text="AI:", font=('Helvetica', 12, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text']).grid(row=0, column=4, padx=5)
        self.ai_score_label = tk.Label(score_frame, text="0", font=('Helvetica', 12, 'bold'),
                                    bg=self.colors['bg'], fg=self.colors['player_o'])
        self.ai_score_label.grid(row=0, column=5, padx=5)

    def create_board(self):
        game_frame = tk.Frame(self.window, bg=self.colors['bg'])
        game_frame.pack()
        
        for i in range(3):
            for j in range(3):
                button = tk.Button(game_frame, text="", font=('Helvetica', 24, 'bold'),
                                 width=5, height=2, bg=self.colors['button'],
                                 fg=self.colors['text'],
                                 activebackground=self.colors['button_hover'],
                                 activeforeground=self.colors['text'],
                                 command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=i, column=j, padx=3, pady=3)
                self.buttons.append(button)

    def create_reset_button(self):
        reset_button = tk.Button(self.window, text="New Game", font=('Helvetica', 12, 'bold'),
                               bg=self.colors['reset_btn'], fg='white',
                               activebackground=self.colors['button_hover'],
                               activeforeground='white', command=self.reset_board)
        reset_button.pack(pady=15)

    def button_click(self, row, col):
        if not self.game_active:
            return
            
        index = row * 3 + col
        if self.board[index] == "" and not self.check_winner():
            # Player move
            self.board[index] = "X"
            self.buttons[index].config(text="X", fg=self.colors['player_x'])
            
            if self.check_winner():
                self.handle_game_end("Player")
            elif "" not in self.board:
                self.handle_game_end("Tie")
            else:
                self.game_active = False  # Temporarily disable board
                self.window.after(500, lambda: self.ai_move())  

    def ai_move(self):
        # Get best move using minimax
        best_score = float('-inf')
        best_move = None
        
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        
        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].config(text="O", fg=self.colors['player_o'])
            
            if self.check_winner():
                self.handle_game_end("AI")
            elif "" not in self.board:
                self.handle_game_end("Tie")
            else:
                self.game_active = True  # Re-enable the board for player's turn

    def minimax(self, board, depth, is_maximizing):
        result = self.check_winner()
        if result:
            return 1 if result == "O" else -1
        elif "" not in board:
            return 0
            
        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ""):
                return self.board[combo[0]]
        return None

    def handle_game_end(self, winner):
        self.game_active = False
        
        # Highlight winning combination only when game ends
        if winner != "Tie":
            win_combinations = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
                [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
                [0, 4, 8], [2, 4, 6]              # Diagonals
            ]
            for combo in win_combinations:
                if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == winner):
                    for i in combo:
                        self.buttons[i].config(bg=self.colors['win_highlight'])
                    break
        
        if winner == "Tie":
            self.scores["Tie"] += 1
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            self.scores[winner] += 1
            messagebox.showinfo("Game Over", f"{winner} wins!")
        self.update_score_labels()
        self.window.after(1000, self.reset_board)

    def update_score_labels(self):
        self.player_score_label.config(text=str(self.scores["Player"]))
        self.ai_score_label.config(text=str(self.scores["AI"]))
        self.tie_score_label.config(text=str(self.scores["Tie"]))

    def reset_board(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        for button in self.buttons:
            button.config(text="", bg=self.colors['button'])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
