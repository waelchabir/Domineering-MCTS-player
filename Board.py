import numpy as np
import Constants as cst
from sys import stdin, stdout, stderr

class Board(object):
    def __init__(self):
        self.turn = cst.WHITE_PLAYER
        self.board = np.zeros((cst.BOARD_X_SIZE, cst.BOARD_Y_SIZE))

    def print(self):
        for i in range(0, cst.BOARD_X_SIZE):
            stdout.write('|')
            for j in range(0, cst.BOARD_Y_SIZE):
                if self.board[i][j] == cst.NONE_PLAYER:
                    stdout.write(cst.NONE_ORIENTATION)
                if self.board[i][j] == cst.BLACK_PLAYER:
                    stdout.write(cst.PLAYERS_ORIENTATION[cst.BLACK_PLAYER])
                if self.board[i][j] == cst.WHITE_PLAYER:
                    stdout.write(cst.PLAYERS_ORIENTATION[cst.WHITE_PLAYER])
                stdout.write('|')
            stdout.write('\n')