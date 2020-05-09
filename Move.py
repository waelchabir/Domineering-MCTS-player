import Constants as cst

class Move(object):

    def __init__(self, toX, toY):
        self.x = toX
        self.y = toY

    def valid(self, board, x, y):
        if self.x >= cst.BOARD_X_SIZE \
            or self.y >= cst.BOARD_Y_SIZE \
            or self.x < 0 \
            or self.y < 0:
            return False
        if cst.PLAYERS_ORIENTATION[board.turn] == cst.HORIZONTAL_ORIENTATION:
            # implement horizontal player validation
            if self.y >= cst.BOARD_Y_SIZE - 1:
                return False
            if board[self.x][self.y] != cst.NONE_PLAYER \
                or board[self.x][self.y + 1] != cst.NONE_PLAYER:
                return False
            return True
        if cst.PLAYERS_ORIENTATION[board.turn] == cst.VERTICAL_ORIENTATION:
            # implement horizontal player validation
            if self.x >= cst.BOARD_X_SIZE - 1:
                return False
            if board[self.x][self.y] != cst.NONE_PLAYER \
                or board[self.x + 1][y] != cst.NONE_PLAYER:
                return False
            return True
