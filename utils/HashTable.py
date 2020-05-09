import Constants as cst
from random import random


class HashCell(object):
    def __init__(self, hBlack, hWhite, hNone):
        self.black = hBlack
        self.white = hWhite
        self.none = hNone

class HashTable(object):

    hashTable = []

    def __init__(self):
        super().__init__()
        HashTable.hashTable = generate()

    def generate(self):
        hashTable = []
        for i in range(cst.BOARD_X_SIZE):
            for j in range(cst.BOARD_Y_SIZE):
                hs = HashCell(
                    int(random() * (2**64)),
                    int(random() * (2**64)),
                    int(random() * (2**64))
                )
                hashTable.append(hs)
        return hashTable

    def getHash(self, x, y, color):
        hs = HashTable.hashTable[cst.BOARD_Y_SIZE * x + y]
        if color == cst.NONE_PLAYER:
            return hs.none
        if color == cst.BLACK_PLAYER:
            return hs.black
        if color == cst.WHITE_PLAYER:
            return hs.white
