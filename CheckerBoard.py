from tkinter import *
from CheckerPiece import *
import time

class CheckerBoard:
    #basic game window properties
    window = Tk()
    window.title("Checkers Game")
    window.resizable(width=FALSE,height=FALSE)
    
    def __init__(self):
        #frame is the checkerboard
        self.frame = Frame(self.window)
        self.frame.pack()
        
        #options contains scoreboard and "skip" option (when there's no legal move)
        self.options = Frame(self.window)
        self.options.pack()
        
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
            #check left if valid
            if reg_moves[0] != None:
                square = self.frame.grid_slaves(reg_moves[0][0], reg_moves[0][1])[0]
                if square.find_all() is ():
                    leg_moves.append(reg_moves[0])
            #check right if valid
            if reg_moves[1] != None:
                square = self.frame.grid_slaves(reg_moves[1][0], reg_moves[1][1])[0]
                if square.find_all() is ():
                    leg_moves.append(reg_moves[1])
        print(leg_moves)
        
        #highlight the tiles the piece can move to (number and map to keyboard)
        tiles = []
        for m in leg_moves:
            tiles.append(((m[0],m[1]), self.frame.grid_slaves(m[0],m[1])[0]))
        for t in tiles:
            t[1].config(bg="red")
            t[1].bind("<Button-1>", lambda event, ind=ind, coords=t[0], tiles=tiles: self.player_move_piece(event, ind, coords, tiles))
            
        #update play status to AI's turn
        self.play_status = 2
    
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
    
    #move checker piece from current location to location indicated by coords
    def player_move_piece(self, event, ind, coords, tiles):
        tag="p"+str(ind)
        curr_row = self.player_pieces[ind].row
        curr_col = self.player_pieces[ind].col
        curr_sq = self.frame.grid_slaves(curr_row, curr_col)[0]
        curr_sq.delete(ALL) #delete checker piece at current location
        new_sq = self.frame.grid_slaves(coords[0], coords[1])[0]
        #create checker piece in the new location
        new_sq.create_oval(10,10,90,90,fill=self.player_pieces[ind].color, tags=tag)
        new_sq.tag_bind(tag, '<1>', lambda event,tag=tag: self.player_move(event,tag))
        #unbind the events from the highlighted tiles and unhighlight
        for t in tiles:
            t[1].config(bg="gray")
            t[1].unbind("<Button-1>")
        #update CheckerPiece info in the list
        self.player_pieces[ind].row = coords[0]
        self.player_pieces[ind].col = coords[1]