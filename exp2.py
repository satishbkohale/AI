# Experiment 2 - 8 Queens using backtracking
# INPUT: none (N = 8, board starts empty). Output: first solution drawn in a window.
import tkinter as tk

N = 8

def is_safe(board, row, col):
    for i in range(row):                                   # column
        if board[i][col] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):  # upper-left diagonal
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, N)):       # upper-right diagonal
        if board[i][j] == 1:
            return False
    return True

def solve_n_queens(board, row):
    if row >= N:
        return True
    for col in range(N):
        if is_safe(board, row, col):
            board[row][col] = 1
            if solve_n_queens(board, row + 1):
                return True
            board[row][col] = 0
    return False

def initialize_board():
    return [[0 for _ in range(N)] for _ in range(N)]

def display_solution(board):
    window = tk.Tk()
    window.title("8 Queens Solution")
    window.geometry("400x400")
    for row in range(N):
        for col in range(N):
            color = "white" if (row + col) % 2 == 0 else "gray"
            cell = tk.Frame(window, width=50, height=50, bg=color)
            cell.grid(row=row, column=col)
            if board[row][col] == 1:
                queen = tk.Label(cell, text="♛", font=("Arial", 24), fg="black")
                queen.place(relx=0.5, rely=0.5, anchor="center")
    window.mainloop()

if __name__ == "__main__":
    board = initialize_board()
    if solve_n_queens(board, 0):
        for r in board:
            print(r)
        display_solution(board)
    else:
        print("No solution exists")
