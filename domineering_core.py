from collections import namedtuple
from random import choice
from sys import stdout

import Constants as cst
from utils import update_tuple
from monte_carlo_tree_search import MCTS, Node

_DOMB = namedtuple("DomineeringBoard", "tup turn winner terminal")


def _find_winner(tup, next_turn):
    "Returns None if no winner, or the code of the winning player"
    if cst.PLAYERS_ORIENTATION[next_turn] == cst.VERTICAL_ORIENTATION:
        for i, value in enumerate(tup[:-cst.BOARD_Y_SIZE]):
            if value == cst.NONE_PLAYER and tup[i + cst.BOARD_Y_SIZE] == cst.NONE_PLAYER:
                return cst.NONE_PLAYER
        return not next_turn
    if cst.PLAYERS_ORIENTATION[next_turn] == cst.HORIZONTAL_ORIENTATION:
        for i, value in enumerate(tup[:-1]):
            if value == cst.NONE_PLAYER and tup[i + 1] == cst.NONE_PLAYER:
                return cst.NONE_PLAYER
        return not next_turn


class DomineeringBoard(_DOMB, Node):
    def find_random_child(board):
        if board.terminal:
            return None  # If the game is finished then no moves can be made
        empty_spots = []
        for i, value in enumerate(board.tup):
            if (value is None) and (board.is_valid_move(i)):
                empty_spots.append(i)
        # [i for i, value in enumerate(board.tup) if (value is None) and (board.is_valid_move(i))]
        return board.make_move(choice(empty_spots))

    def is_terminal(board):
        return board.terminal

    def reward(board):
        if not board.terminal:
            raise RuntimeError(f"reward called on nonterminal board {board}")
        if board.winner is board.turn:
            # It's your turn and you've already won. Should be impossible.
            raise RuntimeError(f"reward called on unreachable board {board}")
        if board.turn is (not board.winner):
            return 0  # Your opponent has just won. Bad.
        if board.winner is None:
            return 0.5  # Board is a tie
        # The winner is neither True, False, nor None
        raise RuntimeError(f"board has unknown winner type {board.winner}")

    def find_children(board):
        if board.terminal:  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        result = set()
        for i, value in enumerate(board.tup):
            if (value is None) and (board.is_valid_move(i)):
                result.add(board.make_move(i))
        return result

    def make_move(board, index):
        tup = board.tup
        if cst.PLAYERS_ORIENTATION[board.turn] == cst.HORIZONTAL_ORIENTATION:
            tup = update_tuple(tup, index, board.turn)
            tup = update_tuple(tup, index+1, board.turn)
        if cst.PLAYERS_ORIENTATION[board.turn] == cst.VERTICAL_ORIENTATION:
            tup = update_tuple(tup, index, board.turn)
            tup = update_tuple(tup, index + cst.BOARD_Y_SIZE, board.turn)
        turn = not board.turn
        winner = _find_winner(tup, turn)
        is_terminal = winner is not None
        return DomineeringBoard(tup, turn, winner, is_terminal)

    def is_valid_move(board, index):
        x = index / cst.BOARD_Y_SIZE
        y = index % cst.BOARD_Y_SIZE
        if x >= cst.BOARD_X_SIZE \
                or y >= cst.BOARD_Y_SIZE \
                or x < 0 \
                or y < 0:
            return False
        if cst.PLAYERS_ORIENTATION[board.turn] == cst.HORIZONTAL_ORIENTATION:
            # implement horizontal player validation
            if y >= cst.BOARD_Y_SIZE - 1:
                return False
            if board.tup[index] is not cst.NONE_PLAYER \
                    or board.tup[index + 1] is not cst.NONE_PLAYER:
                return False
            return True
        if cst.PLAYERS_ORIENTATION[board.turn] == cst.VERTICAL_ORIENTATION:
            # implement horizontal player validation
            if x >= cst.BOARD_X_SIZE - 1:
                return False
            if board.tup[index] is not cst.NONE_PLAYER \
                    or board.tup[index + cst.BOARD_Y_SIZE] is not cst.NONE_PLAYER:
                return False
            return True

    def to_pretty_string(board):
        stdout.write('\n')
        for i in range(0, cst.BOARD_X_SIZE):
            stdout.write('|')
            for j in range(0, cst.BOARD_Y_SIZE):
                if board.tup[i*cst.BOARD_Y_SIZE + j] is cst.NONE_PLAYER:
                    stdout.write(cst.NONE_ORIENTATION)
                if board.tup[i*cst.BOARD_Y_SIZE + j] == cst.BLACK_PLAYER:
                    stdout.write(cst.PLAYERS_ORIENTATION[cst.BLACK_PLAYER])
                if board.tup[i*cst.BOARD_Y_SIZE + j] == cst.WHITE_PLAYER:
                    stdout.write(cst.PLAYERS_ORIENTATION[cst.WHITE_PLAYER])
                stdout.write('|')
            stdout.write('\n')
