class CheckerPiece:
    def __init__(self, color, row, col, on_b):
        self.color = color
        self.row = row
        self.col = col
        self.on_board = on_b
        
    def update_loc(self, row, col):
        self.row = row
        self.col = col
        
    def __str__(self):
        return str(self.row)+str(self.col);