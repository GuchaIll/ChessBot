class moveStack:
    """Class representing the history of moves in the game."""
    def __init__(self, ChessBoard):
        """
        Initialize the move stack.

        Args:
            ChessBoard (Chessboard): The chessboard instance.
        """
        self.stack = []
        self.ChessBoard = ChessBoard

    def canUndoMove(self):
        """
        Check if there are moves to undo.

        Returns:
            bool: True if there are moves to undo, False otherwise.
        """
        return len(self.stack) > 0

    def pushMove(self, piece, start_pos, end_pos, captured_piece=None):
        """
        Push a move onto the stack.

        Args:
            piece (ChessPiece): The piece that was moved.
            start_pos (tuple): The starting position of the piece.
            end_pos (tuple): The ending position of the piece.
            captured_piece (ChessPiece): The captured piece, if any.
        """
        self.stack.append((piece, start_pos, end_pos, captured_piece)) 

    def getLastMove(self):
        """
        Get the last move from the stack.

        Returns:
            tuple: The last move as (piece, start_pos, end_pos, captured_piece).
        """
        if len(self.stack) == 0:
            return None
        return self.stack[-1]

    def undoMove(self, RecordCapture=True):
        """
        Undo the last move.

        Args:
            RecordCapture (bool): Whether to record the capture.
        """

        if not self.canUndoMove():
            print("No moves to undo")
            return None
        
        piece, start_pos, end_pos, captured_piece = self.stack.pop()

        print(f"Undoing move: {piece.ID} from {end_pos} back to {start_pos}")

        # Restore piece to original position
        self.ChessBoard.board[start_pos[0], start_pos[1]] = piece
        piece.xGrid, piece.yGrid = start_pos

        # Handle captured piece restoration
        if captured_piece:
            self.ChessBoard.board[end_pos[0], end_pos[1]] = captured_piece
            if RecordCapture and captured_piece in self.ChessBoard.captured:
                # Remove the exact piece object from captured list
                self.ChessBoard.captured.remove(captured_piece)
                print(f"Restored captured piece: {captured_piece.ID}")
        else:
            self.ChessBoard.board[end_pos[0], end_pos[1]] = None

        return (piece, start_pos, end_pos, captured_piece)

    def clear(self):
        """Clear the move stack."""
        self.stack = []

    def __str__(self):
        """Return a string representation of the move stack."""
        return str([f"{move[0].ID}: {move[1]} -> {move[2]}" for move in self.stack])