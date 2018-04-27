from Board import Board
from SimpleQueue import Queue #for BF node generation in build_tree
import copy
import time

class ABTree:
    class Node:
        def __init__(self, curr_board):
            #regular n-ary tree node attributes
            self.prev_st = None
            self.curr_board = curr_board
            self.legal_sts = None #has NODES, not Boards
            self.forfeited = False #indicator for node generation

            #AB tree node attributes
            self.v = None
            self.a = None
            self.b = None
            self.level = None #1 is max, 2 is min
    
    def __init__(self, root_board):
        self.root = ABTree.Node(root_board) #root_board is a Board object
        self.total = 1 #total number of nodes generated
        self.max_prune = 0
        self.min_prune = 0
        self.root.level = 1 #starts out with max
        self.AB_search_results = None
    
    '''returns a list of legal states (child Nodes) for current state'''
    def generate_nodes(self, curr):
        legal_sts = []
        jmp_moves = []
        reg_moves = []
        if curr.level == 1: #if parent is a max level, use AI_legal_moves
            leg_moves = curr.curr_board.AI_legal_moves()
        else: #if parent is a min level, use player_legal_moves
            leg_moves = curr.curr_board.player_legal_moves()
            #iterating thru legal moves and separating jump moves and regular moves
        for piece in leg_moves:
            piece_id = piece[0]
            if len(piece[1]) != 0:
                for move in piece[1]:
                    if len(move) == 2: #if move is a regular move
                        reg_moves.append((piece_id, move))
                    else: #if move is a jump move
                        jmp_moves.append((piece_id, move))
        moves = []
        if len(jmp_moves) != 0: #if jmp_moves is not empty, use jmp_moves to obtain legal states (children)
            moves = jmp_moves
        elif len(reg_moves) != 0: #else if reg_moves is not empty, use reg_moves to obtain legal states (children)
            moves = reg_moves
        #if either player won (so doesn't have any legal move left)
        elif (curr.level == 1 and curr.curr_board.AI_score == 6) or curr.level == 2 and curr.curr_board.player_score == 6:
            curr.legal_sts = []
            return []
        else: #if there are no legal moves, forfeit turn
            if curr.forfeited == False: #if parent is first to forfeit
                child = ABTree.Node(copy.deepcopy(curr.curr_board))
                #child node has same board as parent node
                child.prev_st = curr
                if curr.level == 1:
                    child.level = 2
                else:
                    child.level = 1
                child.forfeited = True
                legal_sts.append(child)
                curr.legal_sts = legal_sts
                return legal_sts
            else: #if parent had already forfeited and child is stuck too...
                curr.legal_sts = []
                return []
        for move in moves:
            #make a child ABTree Node initially containing same state as current node
            child = ABTree.Node(copy.deepcopy(curr.curr_board)) 
            child.curr_board.set_board(move[0], move[1]) #change Board state according to move
            child.prev_st = curr #set child's parent to current
            if curr.level == 1:
                child.level = 2 #child is a min level if parent is max level
            else:
                child.level = 1
            legal_sts.append(child)
        curr.legal_sts = legal_sts
        return legal_sts
    
    '''build a tree--Breadth First wise--starting with the root node'''
    def build_tree(self):
        builder = Queue()
        builder.enqueue(self.root)
        timeout = time.time()+13 #13 second timer
        while builder.is_empty() == False and time.time()<=timeout:
            curr = builder.dequeue()
            children = self.generate_nodes(curr)
            if children != []:
                for child in children:
                    builder.enqueue(child)
                    self.total += 1 #update total number of nodes generated
                    
    '''returns maximum depth of this tree'''
    def max_depth(self):
        root_node = self.root
        return self.max_depth_helper(root_node)
    
    '''recursive helper function of max_depth'''
    def max_depth_helper(self, node):
        if node.legal_sts == [] or node.legal_sts is None:
            return 0
        maxdepth = 0
        for n in node.legal_sts:
            maxdepth = max(maxdepth, self.max_depth_helper(n))
        return maxdepth+1
        
    '''search through tree--alpha beta wise--starting with the root node
    return (Board, max depth, total number of nodes, max prune, min prune)'''
    def AB_search(self):
        '''terminal state values:
            v = 10*total_captured_by_AI = 60 if AI wins
            v = -5*total_captured_by_player = -30 if player wins
            v = 10*total_captured_by_AI - 5*total_captured_by_player if draw
                *draw could or could not be more advantageous than keep going another path*
            ef(max level) = 10*total_captured_by_AI - 5*total_captured_by_player + num_jump_moves_by_AI
            ef(min level) = 10*total_captured_by_AI - 5*total_captured_by_player - num_jump_moves_by_player'''
        self.root.v = self.max_value(self.root, -100, 100) #initial a = -100, b = 100
        for move in self.root.legal_sts:
            if move.v == self.root.v:
                self.AB_search_results = (move.curr_board, self.max_depth(), self.total, self.max_prune, self.min_prune)
                return self.AB_search_results
    
    def max_value(self, node, a, b):
        if self.terminal_test(node) == True:
            if node.legal_sts == [] and node.curr_board.AI_score == 6: #if state shows AI's win
                return 10*node.curr_board.AI_score
            elif node.legal_sts == [] and node.curr_board.player_score == 6: #if state shows player's win
                return -5*node.curr_board.player_score
            elif node.legal_sts == []: #if there was a draw
                return 10*node.curr_board.AI_score-5*node.curr_board.player_score
            elif node.legal_sts is None: #if cutoff leaf is at max level
                return 10*node.curr_board.AI_score-5*node.curr_board.player_score+node.curr_board.num_jumps
        node.v = -100
        for move in node.legal_sts:
            node.v = max(node.v, self.min_value(move, a, b))
            if node.v >= b:
                self.max_prune += 1
                return node.v
            a = max(a, node.v)
        return node.v
    
    def min_value(self, node, a, b):
        if self.terminal_test(node) == True:
            if node.legal_sts == [] and node.curr_board.AI_score == 6: #if state shows AI's win
                return 10*node.curr_board.AI_score
            elif node.legal_sts == [] and node.curr_board.player_score == 6: #if state shows player's win
                return -5*node.curr_board.player_score
            elif node.legal_sts == []: #if there was a draw
                return 10*node.curr_board.AI_score-5*node.curr_board.player_score
            elif node.legal_sts is None: #if cutoff leaf is at min level
                return 10*node.curr_board.AI_score-5*node.curr_board.player_score-node.curr_board.num_jumps
        node.v = 100
        for move in node.legal_sts:
            node.v = min(node.v, self.max_value(move, a, b))
            if node.v <= a:
                self.min_prune += 1
                return node.v
            b = min(b, node.v)
        return node.v
    
    '''terminal state test: checking if node is a leaf'''
    def terminal_test(self, node):
        if node.legal_sts == [] or node.legal_sts is None:
            return True
        return False