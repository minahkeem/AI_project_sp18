class CheckerPiece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        
    def update_loc(self, row, col):
        self.row = row
        self.col = col
        
    def __str__(self):
        return str(self.row)+str(self.col);
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col