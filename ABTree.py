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
            self.legal_sts = [] #has NODES, not Boards
            self.forfeited = False #indicator for node generation

            #AB tree node attributes
            self.v = None
            self.a = None
            self.b = None
            self.level = None #1 is max, 2 is min
    
    def __init__(self, root_board):
        self.root = ABTree.Node(root_board) #root_board is a Board object
        self.total = 1 #total number of nodes generated
        self.depth = 0 #root node's depth is 0
        self.root.level = 1 #starts out with max
    
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
        else: #if there are no legal moves, forfeit turn
            if curr.forfeited == False: #if parent is first to forfeit
                child = ABTree.Node(copy.deepcopy(curr_board))
                #child node has same board as parent node
                child.prev_st = curr
                if curr.level == 1:
                    child.level = 2
                else:
                    child.level = 1
                child.forfeited = True
                return [child]
            else: #if parent had already forfeited and child is stuck too...
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
        timeout = time.time()+5 #5 second timer
        while builder.is_empty() == False and time.time()<=timeout:
            curr = builder.dequeue()
            children = self.generate_nodes(curr)
            if children != []:
                for child in children:
                    builder.enqueue(child)
                    self.total += 1 #update total number of nodes generated
        
    '''search through tree--alpha beta wise--starting with the root node
    REMINDER: return Board object, not an ABTree.Node object!!!'''
    def ABSearch(self):
        pass
        #self.root.v = self.max_value(self.root, )