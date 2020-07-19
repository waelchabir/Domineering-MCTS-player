from collections import namedtuple
from random import choice
from sys import stdout

import config as conf
from utils import update_tuple
from monte_carlo_tree_search import MCTS, Node

_DOMB = namedtuple("DomineeringBoard", "tup turn winner terminal")


def _find_winner(tup, next_turn):
    "Returns None if no winner, or the code of the winning player"
    if conf.PLAYERS_ORIENTATION[next_turn] == conf.VERTICAL_ORIENTATION:
        for i, value in enumerate(tup[:-conf.BOARD_Y_SIZE]):
            if value == conf.NONE_PLAYER and tup[i + conf.BOARD_Y_SIZE] == conf.NONE_PLAYER:
                return conf.NONE_PLAYER
        return not next_turn
    if conf.PLAYERS_ORIENTATION[next_turn] == conf.HORIZONTAL_ORIENTATION:
        for i, value in enumerate(tup[:-1]):
            if i % conf.BOARD_Y_SIZE < conf.BOARD_Y_SIZE - 2 \
                    and value == conf.NONE_PLAYER \
                    and tup[i + 1] == conf.NONE_PLAYER:
                return conf.NONE_PLAYER
        return not next_turn


class DomineeringBoard(_DOMB, Node):
    def find_random_child(board):
        if board.terminal:
            return None  # If the game is finished then no moves can be made
        empty_spots = []
        for i, value in enumerate(board.tup):
            if (value is None) and (board.is_valid_move(i)):
                empty_spots.append(i)
        if len(empty_spots) == 0:
            print("Empty spots found")

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
        if conf.PLAYERS_ORIENTATION[board.turn] == conf.HORIZONTAL_ORIENTATION:
            tup = update_tuple(tup, index, board.turn)
            tup = update_tuple(tup, index + 1, board.turn)
        if conf.PLAYERS_ORIENTATION[board.turn] == conf.VERTICAL_ORIENTATION:
            tup = update_tuple(tup, index, board.turn)
            tup = update_tuple(tup, index + conf.BOARD_Y_SIZE, board.turn)
        turn = not board.turn
        winner = _find_winner(tup, turn)
        is_terminal = winner is not None
        return DomineeringBoard(tup, turn, winner, is_terminal)

    def is_valid_move(board, index):
        x = index // conf.BOARD_Y_SIZE
        y = index % conf.BOARD_Y_SIZE
        if x >= conf.BOARD_X_SIZE \
                or y >= conf.BOARD_Y_SIZE \
                or x < 0 \
                or y < 0:
            return False
        if conf.PLAYERS_ORIENTATION[board.turn] == conf.HORIZONTAL_ORIENTATION:
            # implement horizontal player validation
            if y >= conf.BOARD_Y_SIZE - 1:
                return False
            if board.tup[index] is not conf.NONE_PLAYER \
                    or board.tup[index + 1] is not conf.NONE_PLAYER:
                return False
            return True
        if conf.PLAYERS_ORIENTATION[board.turn] == conf.VERTICAL_ORIENTATION:
            # implement horizontal player validation
            if x >= conf.BOARD_X_SIZE - 1:
                return False
            if board.tup[index] is not conf.NONE_PLAYER \
                    or board.tup[index + conf.BOARD_Y_SIZE] is not conf.NONE_PLAYER:
                return False
            return True

    def to_pretty_string(board):
        stdout.write('\n ')
        {stdout.write(' {}'.format(i)) for i in range(1, conf.BOARD_X_SIZE + 1)}
        stdout.write('\n')
        for i in range(0, conf.BOARD_X_SIZE):
            stdout.write('{}|'.format(i+1))
            for j in range(0, conf.BOARD_Y_SIZE):
                if board.tup[i * conf.BOARD_Y_SIZE + j] is conf.NONE_PLAYER:
                    stdout.write(conf.NONE_ORIENTATION)
                if board.tup[i * conf.BOARD_Y_SIZE + j] == conf.BLACK_PLAYER:
                    stdout.write(conf.PLAYERS_ORIENTATION[conf.BLACK_PLAYER])
                if board.tup[i * conf.BOARD_Y_SIZE + j] == conf.WHITE_PLAYER:
                    stdout.write(conf.PLAYERS_ORIENTATION[conf.WHITE_PLAYER])
                stdout.write('|')
            stdout.write('\n')
