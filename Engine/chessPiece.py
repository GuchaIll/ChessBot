from enum import Enum 
# Enum for Chess Piece Types
class ChessPieceType(Enum):
    """Enumeration for different types of chess pieces."""
    INVALID = -1
    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5

# Dictionary for Chess Piece Sprites
ChessPieceSprites = {
    ChessPieceType.KING: "./assets/sprite/King",
    ChessPieceType.QUEEN: "./assets/sprite/Queen",
    ChessPieceType.ROOK: "./assets/sprite/Rook",
    ChessPieceType.BISHOP: "./assets/sprite/Bishop",
    ChessPieceType.KNIGHT: "./assets/sprite/Knight",
    ChessPieceType.PAWN: "./assets/sprite/Pawn"
}


# Base Class for Chess Pieces
class ChessPiece:
    """Base class for all chess pieces."""
    def __init__(self, color, xGrid, yGrid, board):
        """
        Initialize a chess piece.

        Args:
            color (str): The color of the piece ('white' or 'black').
            xGrid (int): The x-coordinate on the board.
            yGrid (int): The y-coordinate on the board.
            board (Chessboard): Reference to the chessboard.
        """
        self.color = color
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.ChessBoard = board
        self.ID = ChessPieceType.INVALID

    def validMove(self):
        """Generate valid moves for the piece. To be implemented by subclasses."""
        pass

    def isValidMove(self, move):
        """
        Check if a move is valid.

        Args:
            move (tuple): The target position (x, y).

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        moves = self.validMove()
        return move in moves

    def move(self, move, RecordCapture=True):
        """
        Move the piece to a new position.

        Args:
            move (tuple): The target position (x, y).
            RecordCapture (bool): Whether to record captures.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        
        """Move the piece to a new position."""
        if not self.isValidMove(move):
            return False

     
        newMove = self.ChessBoard.board[move[0], move[1]]
        if newMove is not None:
            self.ChessBoard.capture(newMove, RecordCapture)

        # Push move to stack with special state
        self.ChessBoard.moveStack.pushMove(self, (self.xGrid, self.yGrid), move, newMove)

        # Update piece position
        self.ChessBoard.board[self.xGrid, self.yGrid] = None
        self.xGrid, self.yGrid = move
        self.ChessBoard.board[move[0], move[1]] = self


        return True
