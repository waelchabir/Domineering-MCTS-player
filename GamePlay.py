import Constants as cst
from Move import Move
import utils.HashTable as HashTable

class GamePlay(object):
    def __init__(self):
        self.turn = cst.WHITE_PLAYER

    def legalMoves(self, board):
        moves = []
        for i in range(0, cst.BOARD_X_SIZE):
            for j in range(0, cst.BOARD_Y_SIZE):
                m = Move(i, j)
                if (m.valid(board, i, j)):
                    moves.append(m)
        return moves

    def playMove(self, move, board, ht):
        board[move.x][move.y] = self.turn
        position_hash = ht ^ HashTable.HashTable.getHash(move.x, move.y, self.turn)
        if cst.PLAYERS_ORIENTATION[self.turn] == cst.HORIZONTAL_ORIENTATION:
            position_hash = position_hash ^ HashTable.HashTable.getHash(move.x, move.y + 1, self.turn)
            board[move.x][move.y + 1] = self.turn
        if cst.PLAYERS_ORIENTATION[self.turn] == cst.VERTICAL_ORIENTATION:
            position_hash = position_hash ^ HashTable.HashTable.getHash(move.x + 1, move.y, self.turn)
            board[move.x + 1][move.y] = self.turn
        if self.turn == cst.BLACK_PLAYER:
            self.turn = cst.WHITE_PLAYER
        if self.turn == cst.WHITE_PLAYER:
            self.turn = cst.BLACK_PLAYER
        return position_hash