from tkinter import *
from CheckerPiece import *

class CheckerBoard:
    #basic game window properties
    window = Tk()
    window.title("Checkers Game")
    
    def __init__(self):
        self.AI_pieces = []
        self.AI_pieces.append(CheckerPiece("white",2,1))
        self.AI_pieces.append(CheckerPiece("white",1,2))
        self.AI_pieces.append(CheckerPiece("white",2,3))
        self.AI_pieces.append(CheckerPiece("white",1,4))
        self.AI_pieces.append(CheckerPiece("white",2,5))
        self.AI_pieces.append(CheckerPiece("white",1,6))
        
        self.player_pieces = []
        self.player_pieces.append(CheckerPiece("black",6,1))
        self.player_pieces.append(CheckerPiece("black",5,2))
        self.player_pieces.append(CheckerPiece("black",6,3))
        self.player_pieces.append(CheckerPiece("black",5,4))
        self.player_pieces.append(CheckerPiece("black",6,5))
        self.player_pieces.append(CheckerPiece("black",5,6))
        
    def make_board(self):
        b_frame = Frame(self.window, bg="gray")
        b_frame.pack()
        
    def place_checkers(self):
        pass