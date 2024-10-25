import tkinter as tk
from tkinter import messagebox

SIZE = 3
player_marker = 'X'
computer_marker = 'O'
player_wins = 0
computer_wins = 0
board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]

# Function to evaluate board score
def evaluate():
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return 10 if row[0] == computer_marker else -10
    for col in range(SIZE):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return 10 if board[0][col] == computer_marker else -10
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return 10 if board[0][0] == computer_marker else -10
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return 10 if board[0][2] == computer_marker else -10
    return 0

# Minimax algorithm for AI moves
def minimax(depth, is_max):
    score = evaluate()
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if not any(' ' in row for row in board):
        return 0

    if is_max:
        best = -1000
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == ' ':
                    board[i][j] = computer_marker
                    best = max(best, minimax(depth + 1, False))
                    board[i][j] = ' '
        return best
    else:
        best = 1000
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == ' ':
                    board[i][j] = player_marker
                    best = min(best, minimax(depth + 1, True))
                    board[i][j] = ' '
        return best

# Function to make AI move
def computer_move():
    best_val = -1000
    best_move = (-1, -1)
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == ' ':
                board[i][j] = computer_marker
                move_val = minimax(0, False)
                board[i][j] = ' '
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    row, col = best_move
    board[row][col] = computer_marker
    buttons[row][col].config(text=computer_marker, state='disabled')
    check_winner()

# Function to check winner or tie
def check_winner():
    global player_wins, computer_wins
    score = evaluate()
    if score == 10:
        computer_wins += 1
        messagebox.showinfo("Game Over", "Computer wins!")
        reset_game()
    elif score == -10:
        player_wins += 1
        messagebox.showinfo("Game Over", "You win!")
        reset_game()
    elif not any(' ' in row for row in board):
        messagebox.showinfo("Game Over", "It's a tie!")
        reset_game()

# Reset game
def reset_game():
    global board
    board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
    for row in range(SIZE):
        for col in range(SIZE):
            buttons[row][col].config(text=' ', state='normal')

# Player move
def player_move(row, col):
    if board[row][col] == ' ':
        board[row][col] = player_marker
        buttons[row][col].config(text=player_marker, state='disabled')
        check_winner()
        computer_move()

# Set up the Tkinter window
root = tk.Tk()
root.title("Tic Tac Toe")
buttons = [[None for _ in range(SIZE)] for _ in range(SIZE)]

# Create buttons for the grid
for i in range(SIZE):
    for j in range(SIZE):
        buttons[i][j] = tk.Button(root, text=' ', font=('Arial', 20), width=5, height=2,
                                  command=lambda i=i, j=j: player_move(i, j))
        buttons[i][j].grid(row=i, column=j)

# Run the Tkinter main loop
root.mainloop()
