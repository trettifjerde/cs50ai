"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from helpers import empty_cells

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return O if empty_cells(board) % 2 == 0 else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if not board[i][j]}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not a valid action")

    result_board = deepcopy(board)
    i, j = action
    result_board[i][j] = player(board)

    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # check horisontal
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        # check vertical
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    # check diagonal
    if board[1][1] == board[0][0] == board[2][2] or board[1][1] == board[0][2] == board[2][0]:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return bool(winner(board)) or not empty_cells(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    wins = winner(board)
    if wins == X: 
        return 1
    elif wins == O: 
        return -1
    else: 
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    x_params = (None, -1, 1, max)
    o_params = (None, 1, -1, min)

    def best_move(board):
        if terminal(board):
            return (None, utility(board))

        best_action, best_score, goal_score, update_function = x_params if player(board) == X else o_params
        for action in actions(board):
            score = update_function(best_score, best_move(result(board, action))[1])
            if score == goal_score:
                return (action, score)
            elif score != best_score:
                best_action, best_score = action, score
        return (best_action, best_score) 

    return best_move(board)[0]

