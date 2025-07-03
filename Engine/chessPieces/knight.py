from Engine.chessPiece import *

class Knight(ChessPiece):
    """Class representing the Knight piece."""
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__(color, xGrid, yGrid, board)
        self.ID = ChessPieceType.KNIGHT

    def validMove(self):
        """
        Generate valid moves for the Knight.

        Returns:
            list: A list of valid moves as (x, y) tuples.
        """
        moves = []
        directions = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]  # L-shaped moves
        for dx, dy in directions:
            nx, ny = self.xGrid + dx, self.yGrid + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = self.ChessBoard.board[nx, ny]
                if target is None or target.color != self.color:
                    moves.append((nx, ny))
        return moves

    def isValidMove(self, move):
        """Check if a move is valid for the Knight."""
        return super().isValidMove(move)

    def move(self, move, RecordCapture=True):
        """Move the Knight to a new position."""
        return super().move(move, RecordCapture)