'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

import sys
from OthelloBoard import *

import random

# So I can access all the functions specific to the Othello board like the score

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    # PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol

    # parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()


class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)

    def clone(self):
        return HumanPlayer(self.symbol)

    # PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        # print(OthelloBoard.count_score(board, "X"))
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return col, row


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol)
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'

    def get_move(self, board):
        """Runs the algorithm and returns the move to be played."""
        value, new_move = self.minimax(board, 7, self.symbol) # 7 is how many turns ahead it'll look. More means slower but better AI
        col = new_move[1][0]
        row = new_move[1][1]

        return col, row

    def succession(self, board, symbol):
        """Expands the board for all possible moves and saves them in a list."""
        moves = []  # Stores the possible moves and coordinates for each turn
        # print(board.count_score(symbol))
        for c in range(0, board.cols):
            for r in range(0, board.rows):
                if board.grid[c][r] == EMPTY and board.is_legal_move(c, r, symbol): # Checks if move can be made at that spot
                    # print(f"Legal move at {c, r}")
                    cloned = board.cloneOBoard()
                    cloned.play_move(c, r, symbol)
                    moves.append([cloned, (c, r)])

        return moves

    def minimax(self, board, depth, symbol):
        """Algorithm to determine best moves. Code adapted from the pseudocode on the Wikipedia page for Minimax."""
        if depth == 0 or self.finalMove(board):
            return board.utility(), board

        if symbol == "X":
            value = float('-inf')  # Start comparing new values with -infinity, so we can get the max
            nextMove = None

            for move in self.succession(board, "X"):  # Finds best move of all legal moves
                newValue = self.minimax(move[0], depth - 1, "O")[0]  # Grabs value
                value = max(value, newValue)

                if value == newValue:
                    nextMove = move # Chooses the best move to be played
            return value, nextMove

        else:   # This is the same code as above just for minimum
            value = float('inf')
            nextMove = None

            for move in self.succession(board, "O"):
                newValue = self.minimax(move[0], depth - 1, "X")[0]
                value = min(value, newValue)

                if value == newValue:
                    nextMove = move
            return value, nextMove

    def finalMove(self, board):
        """Checks if the current board is the last board moves can be made on."""
        if not board.has_legal_moves_remaining("X") and not board.has_legal_moves_remaining("O"):
            return True
        return False
