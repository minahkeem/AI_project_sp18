from tkinter import *
from CheckerPiece import *

class CheckerBoard:
    #basic game window properties
    window = Tk()
    window.title("Checkers Game")
    window.resizable(width=FALSE,height=FALSE)
    
    def __init__(self):
        self.frame = Frame(self.window)
        self.frame.pack()
        
        self.AI_pieces = []
        self.AI_pieces.append(CheckerPiece("white",1,0,True))
        self.AI_pieces.append(CheckerPiece("white",0,1,True))
        self.AI_pieces.append(CheckerPiece("white",1,2,True))
        self.AI_pieces.append(CheckerPiece("white",0,3,True))
        self.AI_pieces.append(CheckerPiece("white",1,4,True))
        self.AI_pieces.append(CheckerPiece("white",0,5,True))
        
        self.player_pieces = []
        self.player_pieces.append(CheckerPiece("black",5,0,True))
        self.player_pieces.append(CheckerPiece("black",4,1,True))
        self.player_pieces.append(CheckerPiece("black",5,2,True))
        self.player_pieces.append(CheckerPiece("black",4,3,True))
        self.player_pieces.append(CheckerPiece("black",5,4,True))
        self.player_pieces.append(CheckerPiece("black",4,5,True))
        
        self.current_id = -1
        
    def make_board(self):
        for i in range(6):
            for j in range(6):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    Canvas(self.frame, bg="white", height="100", width="100").grid(row=i, column=j)
                else:
                    Canvas(self.frame, bg="gray", height="100", width="100").grid(row=i, column=j)
        
    def place_checkers_init(self):
        for AI_piece in self.AI_pieces:
            square = self.frame.grid_slaves(AI_piece.row, AI_piece.col)[0]
            piece = square.create_oval(10,10,90,90,fill=AI_piece.color)
            square.tag_bind(piece, '<ButtonPress-1>', self.AI_move(AI_piece.row, AI_piece.col))
    
    def AI_move(self, row, col):
        #square = self.frame.grid_slaves(row,col)
        print(str(row)+str(col))
    
    def player_move(self):
        pass