from Engine.chessPiece import *
# King Class
class King(ChessPiece):
    """Class representing the King piece."""
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__(color, xGrid, yGrid, board)
        self.ID = ChessPieceType.KING

    def validMove(self):
        """Generate valid moves for the King."""
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = self.xGrid + dx, self.yGrid + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = self.ChessBoard.board[nx, ny]
                if target is None or target.color != self.color:
                    if not self.BeExposedToCheck((nx, ny)):
                        moves.append((nx, ny))

        # Add castling moves
        if self.CanCastle("left"):
            moves.append((0, self.yGrid))
        if self.CanCastle("right"):
            moves.append((7, self.yGrid))
        return moves

    def BeExposedToCheck(self, move):
        """
        Check if the King would be exposed to check after a move.

        Args:
            move (tuple): The target position (x, y).

        Returns:
            bool: True if the King would be in check, False otherwise.
        """
        opponent = "black" if self.color == "white" else "white"
        for row in self.ChessBoard.board:
            for piece in row:
                if piece and piece.color == opponent and piece.ID != ChessPieceType.KING:
                    if move in piece.validMove():
                        return True
        return False

    def CanCastle(self, direction):
        """
        Check if castling is possible.

        Args:
            direction (str): 'left' or 'right'.

        Returns:
            bool: True if castling is possible, False otherwise.
        """
        if direction == "left":
            if (self.xGrid == 4 and self.yGrid == 0 and
                self.ChessBoard.board[0, self.yGrid] and
                self.ChessBoard.board[0, self.yGrid].ID == ChessPieceType.ROOK and
                all(self.ChessBoard.board[i, self.yGrid] is None for i in range(1, 4))):
                return not any(self.BeExposedToCheck((i, self.yGrid)) for i in range(5))
        elif direction == "right":
            if (self.xGrid == 4 and self.yGrid == 0 and
                self.ChessBoard.board[7, self.yGrid] and
                self.ChessBoard.board[7, self.yGrid].ID == ChessPieceType.ROOK and
                all(self.ChessBoard.board[i, self.yGrid] is None for i in range(5, 7))):
                return not any(self.BeExposedToCheck((i, self.yGrid)) for i in range(5, 8))
        return False

    def move(self, move, castle=False, RecordCapture=True):
        """
        Move the King, handling castling if applicable.

        Args:
            move (tuple): The target position (x, y).
            castle (bool): Whether the move is a castling move.
            RecordCapture (bool): Whether to record captures.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if castle:
            if move[0] == 0:  # Left castle
                self.ChessBoard.board[0, self.yGrid].move((3, self.yGrid))
            elif move[0] == 7:  # Right castle
                self.ChessBoard.board[7, self.yGrid].move((5, self.yGrid))
        return super().move(move, RecordCapture)