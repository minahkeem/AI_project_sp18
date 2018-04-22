from tkinter import *
from CheckerBoard import *

def main():
    game = CheckerBoard()
    game.make_board()
    game.place_checkers_init()
    game.window.mainloop()
    
main()