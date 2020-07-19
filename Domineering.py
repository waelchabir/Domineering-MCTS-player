from sys import stdout

from monte_carlo_tree_search import MCTS
from domineering_core import DomineeringBoard
import config as conf


def new_domineering_board():
    return DomineeringBoard(tup=(conf.NONE_PLAYER,) * (conf.BOARD_X_SIZE * conf.BOARD_Y_SIZE),
                            turn=conf.BLACK_PLAYER,
                            winner=conf.NONE_PLAYER,
                            terminal=False)


def play_game():
    tree = MCTS()
    board = new_domineering_board()
    board.to_pretty_string()
    while True:
        row_col = input("enter row,col: ")
        row, col = map(int, row_col.split(","))
        stdout.write('You choose ({}, {})'.format(row, col))
        index = conf.BOARD_Y_SIZE * (row - 1) + (col - 1)
        if (board.tup[index] is not None) and (board.is_valid_move(index + conf.BOARD_Y_SIZE)):
            raise RuntimeError("Invalid move")
        board = board.make_move(index)
        board.to_pretty_string()
        if board.terminal:
            stdout.write("\nWinner is {}".format(conf.PLAYERS_NAME[board.winner]))
            break
        # You can train as you go, or only at the beginning.
        # Here, we train as we go, doing fifty rollouts each turn.
        for _ in range(conf.TRAINING_EPOCHS):
            tree.do_rollout(board)
        board = tree.choose(board)
        board.to_pretty_string()
        if board.terminal:
            stdout.write("\nWinner is {}".format(conf.PLAYERS_NAME[board.winner]))
            break

if __name__ == "__main__":
    play_game()