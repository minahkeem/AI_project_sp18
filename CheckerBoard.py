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
        
        self.play_status = -1 #1 is player's turn, 2 is AI's turn
        
        self.AI_score = 0
        self.player_score = 0
        
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
        reg_moves = self.get_reg_moves(curr_row, curr_col)
        jmp_moves = self.get_jmp_moves(curr_row, curr_col)
        leg_moves = []
        jmp = False
        #determine if there are jump moves: "white" right in front AND position is empty
        #check left if valid
        if reg_moves[0] != None and jmp_moves[0] != None:
            square = self.frame.grid_slaves(jmp_moves[0][0], jmp_moves[0][1])[0]
            if self.found_opponent_piece(self.AI_pieces, CheckerPiece("black", reg_moves[0][0], reg_moves[0][1], False)) and square.find_all() is ():
                leg_moves.append(jmp_moves[0])
        #check right if valid
        if reg_moves[1] != None and jmp_moves[1] != None:
            square = self.frame.grid_slaves(jmp_moves[1][0], jmp_moves[1][1])[0]
            if self.found_opponent_piece(self.AI_pieces, CheckerPiece("black", reg_moves[1][0], reg_moves[1][1], False)) and square.find_all() is ():
                leg_moves.append(jmp_moves[1])
        #if no jump moves, determine all regular moves
        if len(leg_moves) == 0:
            if reg_moves[0] != None:
                square = self.frame.grid_slaves(reg_moves[0][0], reg_moves[0][1])[0]
                if square.find_all() is ():
                    leg_moves.append(reg_moves[0])
            if reg_moves[1] != None:
                square = self.frame.grid_slaves(reg_moves[1][0], reg_moves[1][1])[0]
                if square.find_all() is ():
                    leg_moves.append(reg_moves[1])
        #if no legal moves, play_status = 2, return
        
        print(leg_moves)
        
        #highlight the tiles the piece can move to (number and map to keyboard)
        #when a tile is chosen, unhighlight
        #move checker piece from (x_0, y_0) to (x_1, y_1)
        #update piece info in player_pieces[ind]
        #update play status to AI's turn
    
    #returns a list of left and right regular moves (within bounds)
    def get_reg_moves(self, row, col):
        moves = []
        if row-1 >=0 and col-1 >=0:
            moves.append((row-1, col-1))
        else:
            moves.append(None)
        if row-1 >=0 and col+1 <=5:
            moves.append((row-1, col+1))
        else:
            moves.append(None)
        return moves
    
    #returns a list of left and right jump moves (within bounds)
    def get_jmp_moves(self, row, col):
        moves = []
        if row-2 >=0 and col-2 >=0:
            moves.append((row-2, col-2))
        else:
            moves.append(None)
        if row-2 >=0 and col+2 <=5:
            moves.append((row-2, col+2))
        else:
            moves.append(None)
        return moves
    #returns a boolean of whether an opponent exists on the specified tile
    def found_opponent_piece(self, opponent, piece):
        found_opp = False
        for opp in opponent:
            if opp == piece:
                found_opp = True
        return found_opp