from Board import Board
from ABTree import ABTree
from tkinter import *
import time

class Game:
    def __init__(self, play_status):
        self.game_window = Tk() #window displaying checkerboard
        self.board_frame = Canvas(self.game_window)
        self.board_frame.grid(row=0,column=0)
        
        self.state = Board() #initialize board and pieces info object Board
        self.make_board() #make board initially
        
        self.play_status = play_status #1 is player, 2 is AI
        
        self.player_sc = Label(self.game_window, text="Player: "+str(self.state.player_score)+"\nComputer: "+str(self.state.AI_score))
        self.player_sc.grid(row=0,column=1)
        
        self.game_loop()
    
    '''main game loop; had to use continual window update to avoid GUI loop clashing with AB algorithm running'''
    def game_loop(self):
        while True:
            if self.play_status == 1:
                self.game_window.mainloop()
                self.assign_checker_events()
                self.game_window.quit()
                self.play_status = 2 #hands over turn to AI
            else:
                self.game_window.update()
                self.AI_turn()
                self.make_board()
                self.game_window.update()
                self.play_status = 1 #hands over turn to player
    
    '''create board on GUI as specified by Board obect'''
    def make_board(self):
        curr_board = self.state.board
        self.board_frame.delete(ALL)
        #make checkerboard tiles and place checker pieces with tags
        for i in range(len(curr_board)):
            for j in range(len(curr_board[i])):
                if curr_board[i][j][0] is False:
                    Canvas(self.board_frame, bg="white", height="100", width="100").grid(row=i, column=j)
                else:
                    square = Canvas(self.board_frame, bg="gray", height="100", width="100")
                    square.grid(row=i, column=j)
                    #placing checkers on the board
                    piece=curr_board[i][j][1]
                    if piece is not None:
                        square.create_oval(10, 10, 90, 90, fill=piece.color, tags=piece.piece_id)
    
    '''event binding player's checker pieces with legal moves'''
    def assign_checker_events(self):
        leg_moves = self.state.player_legal_moves()
        jmp_moves = []
        reg_moves = []
        #separate legal moves into lists of jump moves and regular moves
        for entry in leg_moves:
            if len(entry[1]) != 0: #if a piece has legal moves
                for move in entry[1]:
                    if len(move) == 4:
                        jmp_moves.append(entry)
                    else:
                        reg_moves.append(entry)
        if len(jmp_moves) != 0: #prioritize jump moves
            for entry in jmp_moves:
                piece = self.state.find_piece(entry[0]) #find checker piece with piece_id
                r = piece.row
                c = piece.col
                square = self.board_frame.grid_slaves(r, c)[0] #get the tile at (r,c)
                square.itemconfig(entry[0], activefill="green")
                for move in entry[1]:
                    pos_move = self.board_frame.grid_slaves(move[0], move[1])[0]
                    pos_move.config(activefill="green")
                square.tag_bind(entry[0], "<1>", lambda event, p_id=event[0], next_pos=entry[1]: self.highlight(event, p_id, next_pos))
        else: #if there are no jump moves, look at regular moves
            for entry in reg_moves:
                piece = self.state.find_piece(entry[0]) #find checker piece with piece_id
                r = piece.row
                c = piece.col
                square = self.board_frame.grid_slaves(r, c)[0] #get the tile at (r,c)
                square.itemconfig(entry[0], activefill="green")
                
    def highlight(self, p_id, event, next_pos):
        pass
        
    def AI_turn(self):
        #AB tree generation and search
        tree = ABTree(self.state)
        tree.build_tree()
        res = tree.AB_search()
        self.state = res[0] #update board to post-AI move
        print("AI stats:\nmax depth: "+str(res[1])+", total nodes: "+str(res[2])+", max prune: "+str(res[3])+", min prune: "+str(res[4]))