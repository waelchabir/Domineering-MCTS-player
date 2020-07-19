from monte_carlo_tree_search import MCTS
from domineering_core import DomineeringBoard
import Constants as cst


def new_domineering_board():
    return DomineeringBoard(tup=(cst.NONE_PLAYER,) * (cst.BOARD_X_SIZE * cst.BOARD_Y_SIZE),
                            turn=cst.BLACK_PLAYER,
                            winner=cst.NONE_PLAYER,
                            terminal=False)


def play_game():
    tree = MCTS()
    board = new_domineering_board()
    board.to_pretty_string()
    while True:
        row_col = input("enter row,col: ")
        row, col = map(int, row_col.split(","))
        index = 3 * (row - 1) + (col - 1)
        if (board.tup[index] is not None) and (board.is_valid_move(index+cst.BOARD_Y_SIZE)):
            raise RuntimeError("Invalid move")
        board = board.make_move(index)
        board.to_pretty_string()
        if board.terminal:
            break
        # You can train as you go, or only at the beginning.
        # Here, we train as we go, doing fifty rollouts each turn.
        for _ in range(50):
            tree.do_rollout(board)
        board = tree.choose(board)
        board.to_pretty_string()
        if board.terminal:
            break

if __name__ == "__main__":
    play_game()