from tkinter import *
from CheckerBoard import *

def main():
    turn = input("Enter 1 to go first, Enter 2 to go second: ")
    game = CheckerBoard(int(turn))
    game.make_board()
    game.place_checkers_init()
    game.window.mainloop()
    
main()