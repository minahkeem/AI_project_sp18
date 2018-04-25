from tkinter import *
from CheckerPiece import *
import time

class CheckerBoard:
    def __init__(self, play_status):
        #basic game window properties
        self.window = Tk()
        self.window.title("Checkers Game")
        self.window.resizable(width=FALSE,height=FALSE)
        
        #frame is the checkerboard
        self.frame = Frame(self.window)
        self.frame.pack()
        
        #pack in AI checker pieces, initial positions
        self.AI_pieces = []
        self.AI_pieces.append(CheckerPiece("white",1,0))
        self.AI_pieces.append(CheckerPiece("white",0,1))
        self.AI_pieces.append(CheckerPiece("white",1,2))
        self.AI_pieces.append(CheckerPiece("white",0,3))
        self.AI_pieces.append(CheckerPiece("white",1,4))
        self.AI_pieces.append(CheckerPiece("white",0,5))
        
        #pack in player's checker pieces, initial positions
        self.player_pieces = []
        self.player_pieces.append(CheckerPiece("black",5,0))
        self.player_pieces.append(CheckerPiece("black",4,1))
        self.player_pieces.append(CheckerPiece("black",5,2))
        self.player_pieces.append(CheckerPiece("black",4,3))
        self.player_pieces.append(CheckerPiece("black",5,4))
        self.player_pieces.append(CheckerPiece("black",4,5))
        
        self.play_status = play_status #1 is player's turn, 2 is AI's turn
        
        self.AI_score = 0
        self.player_score = 0
        
        #options contains scoreboard and "skip" option (when there's no legal move)
        self.options = Tk()
        self.player_score_display = Label(self.options, text="player: "+str(self.player_score))
        self.player_score_display.pack()
        self.AI_score_display = Label(self.options, text="computer: "+str(self.AI_score))
        self.AI_score_display.pack()
        self.skip_button = Button(self.options, text = "skip turn", command=lambda: self.skip_turn()).pack()
        
    '''makes the initial checkerboard on frame'''
    def make_board(self):
        for i in range(6):
            for j in range(6):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1): #white tiles
                    Canvas(self.frame, bg="white", height="100", width="100").grid(row=i, column=j)
                else: #gray tiles
                    Canvas(self.frame, bg="gray", height="100", width="100").grid(row=i, column=j)
        
    '''place AI and player checker pieces on the board'''
    def place_checkers_init(self):
        for i,AI_piece in enumerate(self.AI_pieces): #placing AI checker pieces
            tag = "AI"+str(i)
            square = self.frame.grid_slaves(AI_piece.row, AI_piece.col)[0]
            piece = square.create_oval(10,10,90,90,fill=AI_piece.color, tags=tag)
            
        for i,player_piece in enumerate(self.player_pieces): #placing player checker pieces
            tag = "p"+str(i)
            square = self.frame.grid_slaves(player_piece.row, player_piece.col)[0]
            piece = square.create_oval(10,10,90,90,fill=player_piece.color, tags=tag)
            #bind each checker piece to action "player_move"
            square.tag_bind(tag, '<1>', lambda event,tag=tag: self.player_move(event,tag))
    
    '''general methods:
    found_opponent_piece, update_scoreboard, skip_turn'''
    
    '''returns a boolean of whether an opponent exists on the specified tile'''
    def found_opponent_piece(self, opponent, piece):
        found_opp = False
        for opp in opponent:
            if opp == piece:
                found_opp = True
        return found_opp
    
    '''updates the scoreboard on GUI (called whenever a jump move is made)'''
    def update_scoreboard(self):
        self.player_score_display.config(text="player: "+str(self.player_score))
        self.AI_score_display.config(text="computer: "+str(self.AI_score))
    
    '''skips the players turn'''
    def skip_turn(self):
        if self.play_status==1:
            self.play_status = 2
            self.AI_move()
    
    '''AI methods:
    AI_move, AI_get_reg_moves, AI_get_jmp_moves'''
    
    '''this function is called when it is the AI turn'''
    def AI_move(self):
        #update play_status to 1 (player's turn)
        self.play_status = 1
    
    '''returns a list of left and right regular moves of AI (within bounds)'''
    def AI_get_reg_moves(self, row, col):
        moves = []
        if row+1 <=5 and col-1 >=0:
            moves.append((row+1, col-1))
        else:
            moves.append(None)
        if row+1 <=5 and col+1 <=5:
            moves.append((row+1, col+1))
        else:
            moves.append(None)
        return moves
    
    '''returns a list of left and right jump moves of AI (within bounds)'''
    def AI_get_jmp_moves(self, row, col):
        moves = []
        if row+2 <=5 and col-2 >=0:
            moves.append((row+2, col-2))
        else:
            moves.append(None)
        if row+2 <=5 and col+2 <=5:
            moves.append((row+2, col+2))
        else:
            moves.append(None)
        return moves
    
    '''player methods:
    player_move, p_get_reg_moves, p_get_jmp_moves, player_reg_move_piece, player_jmp_move_piece'''
    
    '''this function is called when a player checker piece is clicked'''
    def player_move(self, event, tag):
        if self.play_status == 2:
            return
        ind = int(tag[1])
        curr_row = self.player_pieces[ind].row
        curr_col = self.player_pieces[ind].col
        
        #determine all possible moves (0-2 regulars, 0-2 jumps)=[0,2] moves
        reg_moves = self.p_get_reg_moves(curr_row, curr_col)
        jmp_moves = self.p_get_jmp_moves(curr_row, curr_col)
        leg_moves = []
        
        #determine if there are jump moves: "white" right in front AND position is empty
        
        #check left if valid
        if reg_moves[0] != None and jmp_moves[0] != None:
            square = self.frame.grid_slaves(jmp_moves[0][0], jmp_moves[0][1])[0]
            if self.found_opponent_piece(self.AI_pieces, CheckerPiece("black", reg_moves[0][0], reg_moves[0][1])) and square.find_all() is ():
                leg_moves.append(jmp_moves[0]+reg_moves[0]) #appends a tuple of four elements: (j_r, j_c, o_r, o_c)
        #check right if valid
        if reg_moves[1] != None and jmp_moves[1] != None:
            square = self.frame.grid_slaves(jmp_moves[1][0], jmp_moves[1][1])[0]
            if self.found_opponent_piece(self.AI_pieces, CheckerPiece("black", reg_moves[1][0], reg_moves[1][1])) and square.find_all() is ():
                leg_moves.append(jmp_moves[1]+reg_moves[1])
                
        #if there are jump moves, carry out jump moves
        if len(leg_moves) != 0:
            tiles = []
            for m in leg_moves:
                tiles.append(((m[0],m[1]), (m[2],m[3]), self.frame.grid_slaves(m[0],m[1])[0]))
            for t in tiles:
                t[2].config(bg="red")
                t[2].bind("<Button-1>", lambda event, ind=ind, coords=t[0], opp=t[1], tiles=tiles: self.player_jmp_move_piece(event, ind, coords, opp, tiles))
        #if no jump moves, determine all regular moves
        else:
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
            #carry out regular moves
            tiles = []
            for m in leg_moves:
                tiles.append(((m[0],m[1]), self.frame.grid_slaves(m[0],m[1])[0]))
            for t in tiles:
                t[1].config(bg="red")
                t[1].bind("<Button-1>", lambda event, ind=ind, coords=t[0], tiles=tiles: self.player_reg_move_piece(event, ind, coords, tiles))
            
        #update play status to AI's turn and call AI to play
        self.play_status = 2
        self.AI_move()
    
    '''returns a list of left and right regular moves of player (within bounds)'''
    def p_get_reg_moves(self, row, col):
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
    
    '''returns a list of left and right jump moves of player (within bounds)'''
    def p_get_jmp_moves(self, row, col):
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
    
    '''make regular move from current location to location indicated by coords'''
    def player_reg_move_piece(self, event, ind, coords, tiles):
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
    
    '''make jump move: move from current location to location indicated by coords AND capture opponent's piece'''
    def player_jmp_move_piece(self, event, ind, coords, opp, tiles):
        tag = "p"+str(ind)
        curr_row = self.player_pieces[ind].row
        curr_col = self.player_pieces[ind].col
        curr_sq = self.frame.grid_slaves(curr_row, curr_col)[0]
        curr_sq.delete(ALL) #delete checker piece at current location
        new_sq = self.frame.grid_slaves(coords[0], coords[1])[0]
        #create checker piece in the new location
        new_sq.create_oval(10,10,90,90,fill=self.player_pieces[ind].color, tags=tag)
        new_sq.tag_bind(tag, '<1>', lambda event, tag=tag: self.player_move(event,tag))
        #delete opponent's checker piece
        opp_sq = self.frame.grid_slaves(opp[0], opp[1])[0]
        opp_sq.delete(ALL)
        self.player_score += 1 #update player's score
        self.update_scoreboard()
        #unbind the events from the highlighted tiles and unhighlight
        for t in tiles:
            t[2].config(bg="gray")
            t[2].unbind("<Button-1>")
        #update CheckerPiece info in the list
        self.player_pieces[ind].row = coords[0]
        self.player_pieces[ind].col = coords[1]
        for p in self.AI_pieces:
            if p.row == opp[0] and p.col == opp[1]:
                self.AI_pieces.remove(p)