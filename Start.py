from ABTree import ABTree
from Board import Board
from Game import Game

def main():
    correct_input = False
    while not correct_input:
        turn = input("Enter 1 to go first, Enter 2 to go second: ")
        if turn == 1 or turn == 2:
            correct_input = True
        else:
            print("Invalid input--try again!\n")
    game = Game(turn)
    
main()