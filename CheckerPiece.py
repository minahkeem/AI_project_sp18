class CheckerPiece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        
    def update_loc(self, row, col):
        self.row = row
        self.col = col