from tkinter import *
from CheckerBoard import *

def main():
    game = CheckerBoard()
    game.make_board()
    game.place_checkers()
    game.window.mainloop()
    
main()