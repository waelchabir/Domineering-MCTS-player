import numpy as np
import Constants as cst

class Board(object):
    def __init__(self):
        self.turn = cst.WHITE_PLAYER
        self.board = np.zeros((cst.BOARD_X_SIZE, cst.BOARD_Y_SIZE))