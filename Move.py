import Constants as cst

class Move(object):
    def __init__(self, orientation):
        self.orientation = orientation

    def move(self, toX, toY):
        self.x = toX
        self.y = toY
        print("moving to {},{}".format(toX, toY))

    def valid(self, board):
        if self.x >= cst.BOARD_X_SIZE \
            or self.y >= cst.BOARD_Y_SIZE \
            or self.x < 0 \
            or self.y < 0:
            return False
        if cst.PLAYERS_ORIENTATION[board.turn] == cst.HORIZONTAL_ORIENTATION:
            # TODO implement horizontal validation