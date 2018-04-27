class Board:
    
    #CheckerPiece: subclass of Board
    class CheckerPiece:
        def __init__(self, color, row, col, piece_id):
            self.color = color
            self.row = row
            self.col = col
            self.piece_id = piece_id

        def __eq__(self, other):
            return self.piece_id == other.piece_id
        
        
    def __init__(self):
        self.board = [] #6x6 board with info about checker pieces in a list

        #create board of white and gray tiles
        for i in range(6):
            columns = []
            for j in range(6):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    columns.append([False, None]) #white tiles: [valid_move, CheckerPiece]
                else:
                    columns.append([True, None]) #gray tiles:[valid_move, CheckerPiece]
            self.board.append(columns)

        #white checker pieces (AI) insertion
        self.board[1][0][1] = Board.CheckerPiece("white", 1, 0, "A0")
        self.board[0][1][1] = Board.CheckerPiece("white", 0, 1, "A1")
        self.board[1][2][1] = Board.CheckerPiece("white", 1, 2, "A2")
        self.board[0][3][1] = Board.CheckerPiece("white", 0, 3, "A3")
        self.board[1][4][1] = Board.CheckerPiece("white", 1, 4, "A4")
        self.board[0][5][1] = Board.CheckerPiece("white", 0, 5, "A5")

        #black checker pieces (player) insertion
        self.board[5][0][1] = Board.CheckerPiece("black", 5, 0, "P0")
        self.board[4][1][1] = Board.CheckerPiece("black", 4, 1, "P1")
        self.board[5][2][1] = Board.CheckerPiece("black", 5, 2, "P2")
        self.board[4][3][1] = Board.CheckerPiece("black", 4, 3, "P3")
        self.board[5][4][1] = Board.CheckerPiece("black", 5, 4, "P4")
        self.board[4][5][1] = Board.CheckerPiece("black", 4, 5, "P5")
        
        self.player_score = 0
        self.AI_score = 0

        self.num_jumps = 0 #for use in eval function in AB tree
    
    '''updates the board with new move; only called when a legal move is chosen'''
    def set_board(self, piece_id, new_loc):
        curr = self.find_piece(piece_id)
        if len(new_loc) == 2: #new location indicates regular move
            #place a CheckerPiece with same attributes as the curr in new_loc
            nr = new_loc[0]
            nc = new_loc[1]
            self.board[nr][nc][1] = Board.CheckerPiece(curr.color, nr, nc, curr.piece_id)
            #delete CheckerPiece from old location
            self.board[curr.row][curr.col][1] = None
        elif len(new_loc) == 4: #new location indicates jump move
            nr = new_loc[0]
            nc = new_loc[1]
            oppr = new_loc[2]
            oppc = new_loc[3]
            if curr.color == "white":
                self.AI_score += 1
            else:
                self.player_score += 1
            #place a CheckerPiece with same attributes as the curr in jump location
            self.board[nr][nc][1] = Board.CheckerPiece(curr.color, nr, nc, curr.piece_id)
            #delete captured opponent's CheckerPiece
            self.board[oppr][oppc][1] = None
            #delete CheckerPiece from old location
            self.board[curr.row][curr.col][1] = None
    
    '''finds and returns CheckerPiece on board with piece_id'''
    def find_piece(self, piece_id):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                curr = self.board[i][j][1]
                if curr is not None and curr.piece_id == piece_id:
                    return curr

    '''returns a list of legal moves for each AI checker piece at current board's state:
       [ for each CheckerPiece: [ piece_id, [legal moves]]]'''
    def AI_legal_moves(self):
        leg_moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j][0] != False and self.board[i][j][1] is not None:
                    if self.board[i][j][1].color == "white": #iterating through white checkers
                        curr = self.board[i][j][1]
                        piece_info = [curr.piece_id] #piece's list of legal moves (info)
                        piece_moves = []
                        reg = self.ai_reg_move_helper(i, j)
                        jmp = self.ai_jmp_move_helper(i, j)

                        #determine if there are jump moves left of the piece
                        if reg[0] != None and jmp[0] != None:
                            opp = self.board[reg[0][0]][reg[0][1]][1]
                            sq = self.board[jmp[0][0]][jmp[0][1]][1]
                            if opp is not None and opp.color is "black" and sq is None:
                                piece_moves.append(jmp[0]+reg[0]) #(j_r, j_c, o_r, o_c)
                        #determine if there are jump moves left of the piece
                        if reg[1] != None and jmp[1] != None:
                            opp = self.board[reg[1][0]][reg[1][1]][1]
                            sq = self.board[jmp[1][0]][jmp[1][1]][1]
                            if opp is not None and opp.color is "black" and sq is None:
                                piece_moves.append(jmp[1]+reg[1]) #(j_r, j_c, o_r, o_c)
                        self.num_jumps += len(piece_moves)
                        if len(piece_moves) == 0: #if no jump moves, determine regular moves
                            #determine if there are regular moves left of the piece
                            if reg[0] != None:
                                sq = self.board[reg[0][0]][reg[0][1]][1]
                                if sq is None:
                                    piece_moves.append(reg[0])
                            #determine if there are regular moves right of the piece
                            if reg[1] != None:
                                sq = self.board[reg[1][0]][reg[1][1]][1]
                                if sq is None:
                                    piece_moves.append(reg[1])
                        piece_info.append(piece_moves)
                        leg_moves.append(piece_info)
        return leg_moves

    '''helper function for AI_legal_moves:
    get possible regular moves'''
    def ai_reg_move_helper(self, row, col):
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

    '''helper function for AI_legal_moves:
    get possible jump moves'''
    def ai_jmp_move_helper(self, row, col):
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

    '''returns a list of legal moves for each player checker piece at current board's state:
       [ for each CheckerPiece: [ piece_id, [legal moves]]]'''
    def player_legal_moves(self):
        leg_moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j][0] != False and self.board[i][j][1] is not None:
                    if self.board[i][j][1].color == "black": #iterating through black checkers
                        curr = self.board[i][j][1]
                        piece_info = [curr.piece_id] #piece's list of legal moves (info)
                        piece_moves = []
                        reg = self.p_reg_move_helper(i, j)
                        jmp = self.p_jmp_move_helper(i, j)

                        #determine if there are jump moves left of the piece
                        if reg[0] != None and jmp[0] != None:
                            opp = self.board[reg[0][0]][reg[0][1]][1]
                            sq = self.board[jmp[0][0]][jmp[0][1]][1]
                            if opp is not None and opp.color is "white" and sq is None:
                                piece_moves.append(jmp[0]+reg[0]) #(j_r, j_c, o_r, o_c)
                        #determine if there are jump moves left of the piece
                        if reg[1] != None and jmp[1] != None:
                            opp = self.board[reg[1][0]][reg[1][1]][1]
                            sq = self.board[jmp[1][0]][jmp[1][1]][1]
                            if opp is not None and opp.color is "white" and sq is None:
                                piece_moves.append(jmp[1]+reg[1]) #(j_r, j_c, o_r, o_c)
                        self.num_jumps += len(piece_moves)
                        if len(piece_moves) == 0: #if no jump moves, determine regular moves
                            #determine if there are regular moves left of the piece
                            if reg[0] != None:
                                sq = self.board[reg[0][0]][reg[0][1]][1]
                                if sq is None:
                                    piece_moves.append(reg[0])
                            #determine if there are regular moves right of the piece
                            if reg[1] != None:
                                sq = self.board[reg[1][0]][reg[1][1]][1]
                                if sq is None:
                                    piece_moves.append(reg[1])
                        piece_info.append(piece_moves)
                        leg_moves.append(piece_info)
        return leg_moves

    '''helper function for player_legal_moves:
    get possible regular moves'''
    def p_reg_move_helper(self, row, col):
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

    '''helper function for player_legal_moves:
    get possible jump moves'''
    def p_jmp_move_helper(self, row, col):
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
    
    '''prints board on command line:
    space = white tile, '-' = gray tile
    'w' = AI piece, 'b' = player piece'''
    def __repr__(self):
        bd = ""
        for i in range(len(self.board)):
            line = ""
            for j in range(len(self.board[i])):
                if self.board[i][j][0] is False:
                    line += " "
                elif self.board[i][j][1] is None:
                    line += "-"
                elif self.board[i][j][1].color is "white":
                    line += "w"
                elif self.board[i][j][1].color is "black":
                    line += "b"
            bd += line+"\n"
        return bd
