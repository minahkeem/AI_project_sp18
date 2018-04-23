from tkinter import *
from CheckerPiece import *

class CheckerBoard:
    #basic game window properties
    window = Tk()
    window.title("Checkers Game")
    window.resizable(width=FALSE,height=FALSE)
    
    def __init__(self):
        #frame is the checkerboard
        self.frame = Frame(self.window)
        self.frame.pack()
        
        #pack in AI checker pieces, initial positions
        self.AI_pieces = []
        self.AI_pieces.append(CheckerPiece("white",1,0,True))
        self.AI_pieces.append(CheckerPiece("white",0,1,True))
        self.AI_pieces.append(CheckerPiece("white",1,2,True))
        self.AI_pieces.append(CheckerPiece("white",0,3,True))
        self.AI_pieces.append(CheckerPiece("white",1,4,True))
        self.AI_pieces.append(CheckerPiece("white",0,5,True))
        
        #pack in player's checker pieces, initial positions
        self.player_pieces = []
        self.player_pieces.append(CheckerPiece("black",5,0,True))
        self.player_pieces.append(CheckerPiece("black",4,1,True))
        self.player_pieces.append(CheckerPiece("black",5,2,True))
        self.player_pieces.append(CheckerPiece("black",4,3,True))
        self.player_pieces.append(CheckerPiece("black",5,4,True))
        self.player_pieces.append(CheckerPiece("black",4,5,True))
        
        self.play_status = 1 #1 is player's turn, 2 is AI's turn
        
    #makes the initial checkerboard on frame
    def make_board(self):
        for i in range(6):
            for j in range(6):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1): #white tiles
                    Canvas(self.frame, bg="white", height="100", width="100").grid(row=i, column=j)
                else: #gray tiles
                    Canvas(self.frame, bg="gray", height="100", width="100").grid(row=i, column=j)
        
    #place AI and player checker pieces on the board
    def place_checkers_init(self):
        for i,AI_piece in enumerate(self.AI_pieces):
            tag = "AI"+str(i)
            square = self.frame.grid_slaves(AI_piece.row, AI_piece.col)[0]
            piece = square.create_oval(10,10,90,90,fill=AI_piece.color, tags=tag)
            
        for i,player_piece in enumerate(self.player_pieces):
            tag = "p"+str(i)
            square = self.frame.grid_slaves(player_piece.row, player_piece.col)[0]
            piece = square.create_oval(10,10,90,90,fill=player_piece.color, tags=tag)
            square.tag_bind(tag, '<1>', lambda event,tag=tag: self.player_move(event,tag))
    
    def AI_move(self):
        pass
    
    def player_move(self, event, tag):
        ind = int(tag[1])
        curr_row = self.player_pieces[ind].row
        curr_col = self.player_pieces[ind].col
        
        #determine all possible moves (0-2 regulars, 0-2 jumps)=[0,2] moves
        pos_moves = self.pos_moves_player(curr_row, curr_col)
        print(pos_moves)
        
        #highlight the tiles the piece can move to (number and map to keyboard)
        #when a tile is chosen, unhighlight
        #move checker piece from (x_0, y_0) to (x_1, y_1)
        #update piece info in player_pieces[ind]
        #update play status to AI's turn
    
    #returns a list of possible moves (tuples): only checks for checkerboard bounds
    def pos_moves_player(self, row, col):
        lst = []
        if row-1 >=0 and col-1 >=0:
            lst.append((row-1, col-1))
        if row-1 >=0 and col+1 <=5:
            lst.append((row-1, col+1))
        if row-2 >=0 and col-2 >=0:
            lst.append((row-2, col-2))
        if row-2 >=0 and col+2 <=5:
            lst.append((row-2, col+2))
        return lst