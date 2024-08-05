from enum import Enum

class ChessPieceType(Enum):
    
    INVALID = -1
    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5
    
PieceValue = {
    "PAWN": 10,
    "KNIGHT": 30,
    "BISHOP": 30,
    "ROOK": 50,  # Add this line
    "QUEEN": 90,
    "KING": 900,
    # Add any other missing pieces
}  
  
class Evaluator():
    def __init__(self):
        pass
    def evaluate(self, board):
        current_score = 0
        for i, col in enumerate(board):
            for j, piece in enumerate(col):
                if piece != None:
                    mult = 1 if piece.color == "white" else -1
                    current_score += mult * int(PieceValue[piece.ID.name])
                    
       
        return current_score