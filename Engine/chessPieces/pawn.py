from Engine.chessPiece import *
from Engine.chessPieces.queen import Queen

class Pawn(ChessPiece):
    """Class representing the Pawn piece."""
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__(color, xGrid, yGrid, board)
        self.ID = ChessPieceType.PAWN
        self.movedTwoSpaces = False

    def validMove(self):
        """
        Generate valid moves for the Pawn.

        Returns:
            list: A list of valid moves as (x, y) tuples.
        """
        moves = []
        direction = 1 if self.color == "white" else -1

        # Move forward
        if 0 <= self.yGrid + direction < 8:
            if self.ChessBoard.board[self.xGrid, self.yGrid + direction] is None:
                moves.append((self.xGrid, self.yGrid + direction))

            # Move two spaces forward (only if the pawn hasn't moved yet)
            if (self.yGrid == 1 and self.color == "white") or (self.yGrid == 6 and self.color == "black"):
                if self.ChessBoard.board[self.xGrid, self.yGrid + 2 * direction] is None:
                    moves.append((self.xGrid, self.yGrid + 2 * direction))

            # Capture diagonally
            for dx in [-1, 1]:
                if 0 <= self.xGrid + dx < 8:
                    target = self.ChessBoard.board[self.xGrid + dx, self.yGrid + direction]
                    if target and target.color != self.color:
                        moves.append((self.xGrid + dx, self.yGrid + direction))

            # En passant
            #for dx in [-1, 1]:
                #if 0 <= self.xGrid + dx < 8:
                    #adjacent = self.ChessBoard.board[self.xGrid + dx, self.yGrid]
                    #if adjacent and adjacent.color != self.color and adjacent.ID == ChessPieceType.PAWN and adjacent.movedTwoSpaces:
                        #moves.append((self.xGrid + dx, self.yGrid + direction))
            for dx in [-1, 1]:
                if 0 <= self.xGrid + dx < 8:
                    if self.ChessBoard.board[self.xGrid + dx, self.yGrid] != None and self.ChessBoard.board[self.xGrid+dx, self.yGrid].color != self.color and self.ChessBoard.board[self.xGrid+dx, self.yGrid].ID == ChessPieceType.PAWN and self.ChessBoard.board[self.xGrid+dx, self.yGrid].movedTwoSpaces:
                        moves.append((self.xGrid+dx, self.yGrid+direction))

        return moves

    def move(self, move, RecordCapture=True):
        """
        Move the Pawn to a new position, handling special moves like en passant and promotion.

        Args:
            move (tuple): The target position (x, y).
            RecordCapture (bool): Whether to record captures.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if not self.isValidMove(move):
            return False

        newMove = self.ChessBoard.board[move[0], move[1]]
        if newMove:
            self.ChessBoard.capture(newMove, RecordCapture)
            self.ChessBoard.board[move[0], move[1]] = None
        elif move[0] != self.xGrid:
            # En passant
            self.ChessBoard.capture(self.ChessBoard.board[move[0], self.yGrid], RecordCapture)
            self.ChessBoard.board[move[0], self.yGrid] = None

        # Check if the pawn moved two spaces
        self.movedTwoSpaces = abs(move[1] - self.yGrid) == 2

        # Update the board and position
        self.ChessBoard.moveStack.pushMove(self, (self.xGrid, self.yGrid), move, newMove)
        self.ChessBoard.board[self.xGrid, self.yGrid] = None
        self.xGrid, self.yGrid = move
        self.ChessBoard.board[move[0], move[1]] = self

        # Handle promotion
        if (self.yGrid == 7 and self.color == "white") or (self.yGrid == 0 and self.color == "black"):
            self.ChessBoard.board[self.xGrid, self.yGrid] = Queen(self.color, self.xGrid, self.yGrid, self.ChessBoard)

        return True
