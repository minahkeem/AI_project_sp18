from Board import Board
from ABTree import ABTree as ab

def main():
    game = Board(1)
    print(game)
    tree = ab(game)
    lst = tree.generate_nodes(tree.root)
    for i in lst:
        print(i.curr_board)
    sample = tree.root.legal_sts[0]
    lst = tree.generate_nodes(sample)
    for i  in lst:
        print(i.curr_board)
    tree.build_tree()
    print(str(tree.total))

main()