'''sets up the board to begin the game'''
def board_initial_state():
    board = []
    
    #create board of white and gray tiles
    for i in range(6):
        columns = []
        for j in range(6):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                columns.append([False, None]) #white tiles: [valid_move, CheckerPiece]
            else:
                columns.append([True, None]) #gray tiles:[valid_move, CheckerPiece]
        board.append(columns)
    
    #white checker pieces (AI) insertion
    board[1][0][1] = CheckerPiece("white", 1, 0, "A0")
    board[0][1][1] = CheckerPiece("white", 0, 1, "A1")
    board[1][2][1] = CheckerPiece("white", 1, 2, "A2")
    board[0][3][1] = CheckerPiece("white", 0, 3, "A3")
    board[1][4][1] = CheckerPiece("white", 1, 4, "A4")
    board[0][5][1] = CheckerPiece("white", 0, 5, "A5")
    
    #black checker pieces (player) insertion
    board[5][0][1] = CheckerPiece("black", 5, 0, "P0")
    board[4][1][1] = CheckerPiece("black", 4, 1, "P1")
    board[5][2][1] = CheckerPiece("black", 5, 2, "P2")
    board[4][3][1] = CheckerPiece("black", 4, 3, "P3")
    board[5][4][1] = CheckerPiece("black", 5, 4, "P4")
    board[4][5][1] = CheckerPiece("black", 4, 5, "P5")
    
    return board

'''returns a list of legal moves for each AI checker piece:
   [ for each CheckerPiece[ piece_id, [legal moves]]]'''
def AI_legal_moves(init_board):
    leg_moves = []
    for i in range(len(init_board)):
        for j in range(len(init_board[i])):
            if init_board[i][j][0] != False and init_board[i][j][1] != None:
                if init_board[i][j][1].color == "white": #iterating through white checkers
                    curr = init_board[i][j][1]
                    piece_info = [curr.piece_id] #piece's list of legal moves (info)
                    piece_moves = []
                    reg = ai_reg_move_helper(i, j)
                    jmp = ai_jmp_move_helper(i, j)
                    
                    #determine if there are jump moves left of the piece
                    if reg[0] != None and jmp[0] != None:
                        opp = init_board[reg[0][0]][reg[0][1]][1]
                        sq = init_board[jmp[0][0]][jmp[0][1]][1]
                        if opp is not None and opp.color is "black" and sq is None:
                            piece_moves.append(jmp[0]+reg[0]) #(j_r, j_c, o_r, o_c)
                    #determine if there are jump moves left of the piece
                    if reg[1] != None and jmp[1] != None:
                        opp = init_board[reg[1][0]][reg[1][1]][1]
                        sq = init_board[jmp[1][0]][jmp[1][1]][1]
                        if opp is not None and opp.color is "black" and sq is None:
                            piece_moves.append(jmp[1]+reg[1]) #(j_r, j_c, o_r, o_c)
                    if len(piece_moves) == 0: #if no jump moves, determine regular moves
                        #determine if there are regular moves left of the piece
                        if reg[0] != None:
                            sq = init_board[reg[0][0]][reg[0][1]][1]
                            if sq is None:
                                piece_moves.append(reg[0])
                        #determine if there are regular moves right of the piece
                        if reg[1] != None:
                            sq = init_board[reg[1][0]][reg[1][1]][1]
                            if sq is None:
                                piece_moves.append(reg[1])
                    piece_info.append(piece_moves)
                    leg_moves.append(piece_info)
    return leg_moves

'''helper function for AI_legal_moves:
get possible regular moves'''
def ai_reg_move_helper(row, col):
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
def ai_jmp_move_helper(row, col):
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

'''returns a list of legal moves for each player checker piece:
   [ for each CheckerPiece[ piece_id, [legal moves]]]'''
def player_legal_moves(init_board):
    leg_moves = []
    for i in range(len(init_board)):
        for j in range(len(init_board[i])):
            if init_board[i][j][0] != False and init_board[i][j][1] != None:
                if init_board[i][j][1].color == "black": #iterating through black checkers
                    curr = init_board[i][j][1]
                    piece_info = [curr.piece_id] #piece's list of legal moves (info)
                    piece_moves = []
                    reg = p_reg_move_helper(i, j)
                    jmp = p_jmp_move_helper(i, j)
                    
                    #determine if there are jump moves left of the piece
                    if reg[0] != None and jmp[0] != None:
                        opp = init_board[reg[0][0]][reg[0][1]][1]
                        sq = init_board[jmp[0][0]][jmp[0][1]][1]
                        if opp is not None and opp.color is "white" and sq is None:
                            piece_moves.append(jmp[0]+reg[0]) #(j_r, j_c, o_r, o_c)
                    #determine if there are jump moves left of the piece
                    if reg[1] != None and jmp[1] != None:
                        opp = init_board[reg[1][0]][reg[1][1]][1]
                        sq = init_board[jmp[1][0]][jmp[1][1]][1]
                        if opp is not None and opp.color is "white" and sq is None:
                            piece_moves.append(jmp[1]+reg[1]) #(j_r, j_c, o_r, o_c)
                    if len(piece_moves) == 0: #if no jump moves, determine regular moves
                        #determine if there are regular moves left of the piece
                        if reg[0] != None:
                            sq = init_board[reg[0][0]][reg[0][1]][1]
                            if sq is None:
                                piece_moves.append(reg[0])
                        #determine if there are regular moves right of the piece
                        if reg[1] != None:
                            sq = init_board[reg[1][0]][reg[1][1]][1]
                            if sq is None:
                                piece_moves.append(reg[1])
                    piece_info.append(piece_moves)
                    leg_moves.append(piece_info)
    return leg_moves

'''helper function for player_legal_moves:
get possible regular moves'''
def p_reg_move_helper(row, col):
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
def p_jmp_move_helper(row, col):
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
    
def print_board():
    board = board_initial_state()
    for i in range(len(board)):
        line = ""
        for j in range(len(board[i])):
            if board[i][j][0] is False:
                line += " "
            elif board[i][j][1] is None:
                line += "-"
            elif board[i][j][1].color is "white":
                line += "w"
            elif board[i][j][1].color is "black":
                line += "b"
        print(line)

print_board()