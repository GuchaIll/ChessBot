from Engine.chessPiece import *

class Queen(ChessPiece):
    """Class representing the Queen piece."""
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__(color, xGrid, yGrid, board)
        self.ID = ChessPieceType.QUEEN

    def validMove(self):
        """
        Generate valid moves for the Queen.

        Returns:
            list: A list of valid moves as (x, y) tuples.
        """
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Horizontal, vertical, and diagonal
        for dx, dy in directions:
            x, y = self.xGrid, self.yGrid
            while True:
                x += dx
                y += dy
                if 0 <= x < 8 and 0 <= y < 8:
                    target = self.ChessBoard.board[x, y]
                    if target is None:
                        moves.append((x, y))
                    elif target.color != self.color:
                        moves.append((x, y))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def isValidMove(self, move):
        """Check if a move is valid for the Queen."""
        return super().isValidMove(move)

    def move(self, move, RecordCapture=True):
        """Move the Queen to a new position."""
        return super().move(move, RecordCapture)