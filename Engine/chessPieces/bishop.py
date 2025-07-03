from Engine.chessPiece import *

class Bishop(ChessPiece):
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__(color, xGrid, yGrid, board)
        self.ID = ChessPieceType.BISHOP
        
    def validMove(self):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
                for d in range(1, 8):
                    newX = self.xGrid + dx * d
                    newY = self.yGrid + dy * d
                   
                    if 0 <= newX < 8 and 0 <= newY < 8:
                       if self.ChessBoard.board[newX, newY] == None:
                           moves.append((newX, newY))
                       elif self.ChessBoard.board[newX, newY].color != self.color:
                           moves.append((newX, newY))
                           break
                       
                       else:
                           break
                    else:
                       break
        
        
        return moves
          
    
    def isValidMove(self, move):
        return super().isValidMove(move)
       
    def move(self, move, RecordCapture = True):
        return super().move(move, RecordCapture)