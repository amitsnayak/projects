import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
   

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.resizable(False, False)

        # Game state
        self.current_player = "X"
        self.board = [""] * 9  
        self.buttons = []

        # Game mode: "AI" for single-player, "2P" for two-player
        self.game_mode = None

        # Score tracking
        self.scores = {"X": 0, "O": 0, "Ties": 0}

        # Initialize GUI
        self.create_mode_selection()
        self.create_game_board()
        self.create_scoreboard()

        # Start the main loop
        self.window.mainloop()

    
    # GUI Initialization
 
    def create_mode_selection(self):
        """Create game mode selection buttons."""
        mode_frame = tk.Frame(self.window)
        mode_frame.grid(row=0, column=0, columnspan=3, pady=10)

        tk.Label(mode_frame, text="Select Game Mode:").pack(side="left", padx=5)
        tk.Button(mode_frame, text="Human vs AI", command=lambda: self.set_game_mode("AI")).pack(side="left", padx=5)
        tk.Button(mode_frame, text="2 Players", command=lambda: self.set_game_mode("2P")).pack(side="left", padx=5)

    def set_game_mode(self, mode):
        """Set the selected game mode and reset the board."""
        self.game_mode = mode
        self.reset_board()
        mode_text = "Human vs AI" if mode == "AI" else "2 Players"
        messagebox.showinfo("Game Mode Selected", f"🎮 Mode: {mode_text}")

    def create_game_board(self):
        """Create the 3x3 Tic-Tac-Toe button grid."""
        for i in range(9):
            button = tk.Button(
                self.window,
                text="",
                font=("Helvetica", 24),
                width=5,
                height=2,
                command=lambda index=i: self.handle_move(index)
            )
            button.grid(row=(i // 3) + 1, column=i % 3)
            self.buttons.append(button)

    def create_scoreboard(self):
        """Display the scoreboard below the game board."""
        self.score_label = tk.Label(
            self.window,
            text=self.get_score_text(),
            font=("Helvetica", 12),
            fg="blue"
        )
        self.score_label.grid(row=4, column=0, columnspan=3, pady=10)

    def update_scoreboard(self):
        """Update the scoreboard text."""
        self.score_label.config(text=self.get_score_text())

    def get_score_text(self):
        """Return formatted scoreboard string."""
        return f"X: {self.scores['X']}  |  O: {self.scores['O']}  |  Ties: {self.scores['Ties']}"

   
    # Game Logic
   
    def handle_move(self, index):
        """Process a move for the current player."""
        if self.board[index] != "" or self.game_mode is None:
            return 
        
        # Make move
        self.board[index] = self.current_player
        self.buttons[index].config(text=self.current_player)

        # Check for win or tie
        if self.check_winner(self.board, self.current_player):
            messagebox.showinfo("Game Over", f"🎉 Player {self.current_player} wins!")
            self.scores[self.current_player] += 1
            self.update_scoreboard()
            self.reset_board()
            return
        elif "" not in self.board:
            messagebox.showinfo("Game Over", "🤝 It's a tie!")
            self.scores["Ties"] += 1
            self.update_scoreboard()
            self.reset_board()
            return

        # Switch turn or let AI play
        if self.game_mode == "AI" and self.current_player == "X":
            self.current_player = "O"
            self.window.after(500, self.ai_move)
        else:
            self.current_player = "O" if self.current_player == "X" else "X"

    def ai_move(self):
        """AI calculates the optimal move using Minimax."""
        best_score = -float('inf')
        best_move = None

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i

        # Make AI move
        self.board[best_move] = "O"
        self.buttons[best_move].config(text="O")

        # Check for win or tie
        if self.check_winner(self.board, "O"):
            messagebox.showinfo("Game Over", "🤖 AI wins!")
            self.scores["O"] += 1
            self.update_scoreboard()
            self.reset_board()
            return
        elif "" not in self.board:
            messagebox.showinfo("Game Over", "🤝 It's a tie!")
            self.scores["Ties"] += 1
            self.update_scoreboard()
            self.reset_board()
            return

        self.current_player = "X"

    def minimax(self, board_state, depth, is_maximizing):
        """Minimax algorithm to determine the best move for AI."""
        if self.check_winner(board_state, "O"):
            return 1
        elif self.check_winner(board_state, "X"):
            return -1
        elif "" not in board_state:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board_state[i] == "":
                    board_state[i] = "O"
                    score = self.minimax(board_state, depth + 1, False)
                    board_state[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board_state[i] == "":
                    board_state[i] = "X"
                    score = self.minimax(board_state, depth + 1, True)
                    board_state[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, board_state, player):
        """Return True if the player has a winning combination."""
        winning_combos = [
            [0,1,2],[3,4,5],[6,7,8], 
            [0,3,6],[1,4,7],[2,5,8], 
            [0,4,8],[2,4,6]           
        ]
        return any(all(board_state[i] == player for i in combo) for combo in winning_combos)

    def reset_board(self):
        """Clear the board for a new round and reset current player."""
        for i in range(9):
            self.board[i] = ""
            self.buttons[i].config(text="")
        self.current_player = "X"


# Run the game

if __name__ == "__main__":
    TicTacToeGame()
