"""
Tic Tac Toe Player
"""
import random
import math

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
    x,o = 0,0
    for i in board:
        for j in i:
            if j == X:x += 1
            elif j == O:o += 1
    return O if o < x else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    acts = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:acts.add((i,j))
    return acts 

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    play = player(board)
    i,j = action
    if board[i][j] is not EMPTY:
        raise Exception("Invalid move")
    newboard = [row[:] for row in board]
    newboard[i][j] = play
    return newboard
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in board:
        if all(x == X for x in i):
            return X
        elif all(x == O for x in i):
            return O
    for i in range(3):
        if all(board[row][i] == X for row in range(3)):return X
        if all(board[row][i] == O for row in range(3)):return O
    
    if board[0][0] is not EMPTY and all(board[i][i] == board[0][0] for i in range(3)):
        return board[0][0]

    if board[0][2] is not EMPTY and all(board[i][2 - i] == board[0][2] for i in range(3)):
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    count = 0
    for i in board:
        for j in i:
            if j == EMPTY:count += 1
    return True if count == 0 or winner(board) is not None else False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:return 1
    elif winner(board) == O:return -1
    else: return 0

def max_val(board):
    if terminal(board):
        return utility(board)
    value = -math.inf
    for acts in actions(board):
        value = max(value,min_val(result(board,acts)))
    return value
def min_val(board):
    if terminal(board):
        return utility(board)
    value = math.inf
    for acts in actions(board):
        value = min(value,max_val(result(board,acts)))
    return value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):return None
    if board == initial_state():
        return random.randint(0,2),random.randint(0,2)
    empty_count = 0
    occupied = 0,0
    for i in range(len(board)):
        for j in range(len(board)):
            if j == EMPTY:
                empty_count += 1
                occupied = i,j

    if empty_count == 8:
        rand = random.randint(0,2),random.randint(0,2)
        if occupied != rand:
            return rand
        else:
            while occupied == rand:
                rand = random.randint(0,2),random.randint(0,2)
                return rand

    user = player(board)
    best = None
    if user == X:
        best_val = -math.inf
        for action in actions(board):
            val = min_val(result(board,action))
            if best_val < val:
                best_val = val
                best = action
        return best
    else:
        best_val = math.inf
        for action in actions(board):
            val = max_val(result(board,action))
            if best_val > val:
                best_val = val
                best = action
        return best

def get_ai_move(board, difficulty):
    """
    Returns an action (i, j) based on the selected difficulty.
    difficulty: 'easy', 'medium', or 'hard'
    """
    possible_moves = list(actions(board))
    if difficulty == 'easy':
        #Completely random moves
        return random.choice(possible_moves)
    elif difficulty == 'medium':
        #half random and half optimal
        if random.random() < 0.5:
            return random.choice(possible_moves)
        return minimax(board)
    else:  # hard
        return minimax(board)