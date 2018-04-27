from ABTree import ABTree
from Board import Board

class Game:
    def __init__(self, turn):
        self.turn = turn #1 is player, 2 is AI
        
        self.state = Board() #initial board info
        
        self.AI_score = self.state.AI_score
        self.player_score = self.state.player_score
        
        self.game_loop()
    
    def game_loop(self):
        while not self.done():
            if self.turn == 1:
                print("\nYour turn!")
                moves = self.display_legal_moves()
                self.move_piece(moves)
                print("\nHere's what the board currently looks like:\n")
                print(self.state)
                print("Current score: "+str(self.AI_score)+" for the computer, "+str(self.player_score)+" for you")
                self.turn = 2
            else:
                print("\nWait!... the computer is calculating its move")
                tree = ABTree(self.state)
                tree.build_tree()
                res = tree.AB_search()
                if res is not None:
                    self.state = res[0]
                else:
                    self.state = None
                if self.state is not None:
                    self.AI_score = self.state.AI_score
                    self.player_score = self.state.player_score
                    print("Depth: "+str(res[1])+", Total # of nodes: "+str(res[2])+", Max prune: "+str(res[3])+", Min prune: "+str(res[4]))
                    print("\nCurrent score: "+str(self.AI_score)+" for the computer, "+str(self.player_score)+" for you")
                self.turn = 1
    
    '''Checks status of the game: if a player won or there was a draw'''
    def done(self):
        if self.state is None: #game has ended--no legal moves on either side
            if self.AI_score == self.player_score: #draw
                print("\nIt was a draw with "+str(self.AI_score)+" for the computer and "+str(self.player_score)+" for you!")
            elif self.AI_score > self.player_score: #AI had higher score
                print("\nAw... you lost! The score was "+str(self.AI_score)+" for the computer and "+str(self.player_score)+" for you!")
            else:
                print("\nYes, you won! The score was "+str(self.AI_score)+" for the computer and "+str(self.player_score)+" for you!")
            return True
        return False
    
    '''move piece by taking in input from player'''
    def move_piece(self, moves):
        if moves is None:
            if self.AI_score == 6:
                self.state = None
            return
        correct_input = False
        curr_row = 0
        curr_col = 0
        curr = ""
        while not correct_input: #checking validity of player input for piece to move
            curr_row = input("\nEnter the row of piece you want to move: ")-1
            curr_col = input("Enter the column of piece you want to move: ")-1
            curr = self.state.get_piece_id(curr_row, curr_col)
            for m in moves:
                if m[0] == curr:
                    correct_input = True
                    break
            if correct_input == False:
                print("\nInvalid input--please enter again")
        correct_input = False
        next_row = 0
        next_col = 0
        new_loc = None
        while not correct_input: #checking validity of player input for next placement of piece
            next_row = input("\nEnter the row of your move: ")-1
            next_col = input("Enter the column of your move: ")-1
            for m in moves:
                #checks that two inputs (current and desired location) are related
                if m[0] == curr and next_row == m[1] and next_col == m[2]:
                    correct_input = True
                    if len(m) == 5: #jump move
                        new_loc = (m[1], m[2], m[3], m[4])
                    else: #regular move
                        new_loc = (m[1], m[2])
                    break
            if correct_input == False:
                print("\nInvalid input--please enter again")
                
        self.state.set_board(curr, new_loc) #update board
        #update scores
        self.AI_score = self.state.AI_score
        self.player_score = self.state.player_score
    
    '''display all legal moves for the player (prioritizing jump moves)'''
    def display_legal_moves(self):
        leg_moves = self.state.player_legal_moves()
        jmp_moves = []
        reg_moves = []
        
        #separate legal moves into lists of jump and regular moves
        for entry in leg_moves:
            if len(entry[1]) != 0:
                for move in entry[1]:
                    if len(move) == 4:
                        jmp_moves.append((entry[0],) + move) #tuple: (piece_id, j_r, j_c, o_r, o_c)
                    else:
                        reg_moves.append((entry[0],) + move) #tuple: (piece_id, r_r, r_c)
        
        if len(jmp_moves) != 0: #prioritizing jump moves
            print("\nHere's what the board currently looks like:\n")
            print(self.state)
            print("Here are your list of moves:")
            for move in jmp_moves:
                curr = self.state.find_piece(move[0])
                print("From ("+str(curr.row+1)+", "+str(curr.col+1)+"), you can jump to ("+str(move[1]+1)+", "+str(move[2]+1)+") and capture opponent in ("+str(move[3]+1)+", "+str(move[4]+1)+")")
            return jmp_moves
        elif len(reg_moves) != 0: #if no jump moves, give regular moves
            print("\nHere's what the board currently looks like:\n")
            print(self.state)
            print("Here are your list of moves:")
            for move in reg_moves:
                curr = self.state.find_piece(move[0])
                print("From ("+str(curr.row+1)+", "+str(curr.col+1)+"), you can move to ("+str(move[1]+1)+", "+str(move[2]+1)+")")
            return reg_moves
        else: #if there are no legal moves this turn
            print("\nYou have no legal moves! Forfeiting this turn...")
            return None