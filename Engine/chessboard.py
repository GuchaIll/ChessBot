import pygame
import numpy as np
import copy
from Engine.moveStack import *
from Engine.evaluation import *
from Engine.chessPiece import *
from Engine.chessPieces.bishop import Bishop
from Engine.chessPieces.knight import Knight
from Engine.chessPieces.rook import Rook
from Engine.chessPieces.pawn import Pawn
from Engine.chessPieces.queen import Queen
from Engine.chessPieces.king import King

class Chessboard:
    """Class representing the chessboard."""
    def __init__(self):
        self.moveStack = moveStack(self)
        self.board = np.empty((8, 8), dtype=object)
        self.captured = []
        self.Evaluator = Evaluator()

    def SetUpBoard(self):
        """Set up the initial positions of all chess pieces on the board."""
        for i in range(8):
            self.board[i, 1] = Pawn("white", i, 1, self)
            self.board[i, 6] = Pawn("black", i, 6, self)

        self.board[0, 0] = Rook("white", 0, 0, self)
        self.board[7, 0] = Rook("white", 7, 0, self)
        self.board[0, 7] = Rook("black", 0, 7, self)
        self.board[7, 7] = Rook("black", 7, 7, self)

        self.board[1, 0] = Knight("white", 1, 0, self)
        self.board[6, 0] = Knight("white", 6, 0, self)
        self.board[1, 7] = Knight("black", 1, 7, self)
        self.board[6, 7] = Knight("black", 6, 7, self)

        self.board[2, 0] = Bishop("white", 2, 0, self)
        self.board[5, 0] = Bishop("white", 5, 0, self)
        self.board[2, 7] = Bishop("black", 2, 7, self)
        self.board[5, 7] = Bishop("black", 5, 7, self)

        self.board[3, 0] = Queen("white", 3, 0, self)
        self.board[4, 0] = King("white", 4, 0, self)
        self.board[3, 7] = Queen("black", 3, 7, self)
        self.board[4, 7] = King("black", 4, 7, self)

    def find(self, pieceType, color):
        """
        Find a specific piece on the board.

        Args:
            pieceType (ChessPieceType): The type of the piece to find.
            color (str): The color of the piece ('white' or 'black').

        Returns:
            ChessPiece: The found piece, or None if not found.
        """
        for row in self.board:
            for piece in row:
                if piece and piece.ID == pieceType and piece.color == color:
                    return piece
        return None
    def remove(self, piece):
        self.board[piece.xGrid, piece.yGrid] = None
        
    def add(self, piece):
        self.board[piece.xGrid, piece.yGrid] = piece

    def render(self, screen):
        """
        Render the chessboard and pieces on the screen.

        Args:
            screen (pygame.Surface): The screen to render on.
        """
        screen.fill((255, 255, 255))
        cell_size = 75
        boardColor = [(255, 255, 255), (30, 0, 100)]

        for x, col in enumerate(self.board):
            for y, piece in enumerate(col):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                color = boardColor[(x + y) % 2]
                pygame.draw.rect(screen, color, rect)
                if piece:
                    sprite_link = ChessPieceSprites.get(piece.ID) + "_" + piece.color + ".png"
                    if sprite_link:
                        sprite = pygame.image.load(sprite_link).convert_alpha()
                        pos_x = x * 75 + 5
                        pos_y = y * 75 + 5
                        screen.blit(sprite, (pos_x, pos_y))

    def capture(self, piece, RecordCapture=True):
        """
        Capture a piece and add it to the captured list.

        Args:
            piece (ChessPiece): The piece to capture.
            RecordCapture (bool): Whether to record the capture.
        """
        if RecordCapture:
            self.captured.append(piece)

    def evaluate(self):
        """
        Evaluate the current board state.

        Returns:
            int: The evaluation score of the board.
        """
        return self.Evaluator.evaluate(self.board)
    
    def renderCapturedPieces(self, screen):
        """
        Render the captured pieces on the screen.

        Args:
            screen (pygame.Surface): The screen to render on.
        """
        white_captured = [piece for piece in self.captured if piece.color == "white"]
        black_captured = [piece for piece in self.captured if piece.color == "black"]

        # Render white captured pieces
        for i, piece in enumerate(white_captured):
            sprite_link = ChessPieceSprites.get(piece.ID) + "_white.png"
            if sprite_link:
                sprite = pygame.image.load(sprite_link).convert_alpha()
                screen.blit(sprite, (600 + i * 40, 650))  

        # Render black captured pieces
        for i, piece in enumerate(black_captured):
            sprite_link = ChessPieceSprites.get(piece.ID) + "_black.png"
            if sprite_link:
                sprite = pygame.image.load(sprite_link).convert_alpha()
                screen.blit(sprite, (600 + i * 40, 700))  
    def renderValidSquares(self, screen, moves):
        cell_size = 75
        for move in moves:
            x, y = move
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 255, 0), rect)

    def makeMove(self, piece, newLoc, updateCapture=True):
        """
        Make a move on the chessboard.

        Args:
            piece (ChessPiece): The piece to move.
            newLoc (tuple): The target position (x, y).
            updateCapture (bool): Whether to update the capture list.
        """
        piece.move(newLoc, updateCapture)

    def undoMove(self, updateCapture=True):
        """
        Undo the last move on the chessboard.

        Args:
            updateCapture (bool): Whether to update the capture list.
        """
        self.moveStack.undoMove(updateCapture)

    def evaluate(self):
        """
        Evaluate the current board state.

        Returns:
            int: The evaluation score of the board.
        """
        return self.Evaluator.evaluate(self.board)
    
    def remove(self, piece):
        self.board[piece.xGrid, piece.yGrid] = None
        
    def add(self, piece):
        self.board[piece.xGrid, piece.yGrid] = piece

    def copy(self):
        """
        Create a deep copy of the chessboard.

        Returns:
            Chessboard: A new Chessboard instance with the same state.
        """
        new_board = Chessboard()

        new_board.board = np.empty((8, 8), dtype=object)
        
        for x in range(8):
            for y in range(8):
                if self.board[x, y] is not None:
                    original_piece = self.board[x, y]
                    
                    # Create new piece of the same type
                    if original_piece.ID == ChessPieceType.PAWN:
                        new_piece = Pawn(original_piece.color, x, y, new_board)
                        new_piece.movedTwoSpaces = original_piece.movedTwoSpaces
                    elif original_piece.ID == ChessPieceType.ROOK:
                        new_piece = Rook(original_piece.color, x, y, new_board)
                    elif original_piece.ID == ChessPieceType.KNIGHT:
                        new_piece = Knight(original_piece.color, x, y, new_board)
                    elif original_piece.ID == ChessPieceType.BISHOP:
                        new_piece = Bishop(original_piece.color, x, y, new_board)
                    elif original_piece.ID == ChessPieceType.QUEEN:
                        new_piece = Queen(original_piece.color, x, y, new_board)
                    elif original_piece.ID == ChessPieceType.KING:
                        new_piece = King(original_piece.color, x, y, new_board)
                    
                    new_board.board[x, y] = new_piece
                else:
                    new_board.board[x, y] = None

        new_board.captured = copy.deepcopy(self.captured)
        new_board.Evaluator = self.Evaluator
        new_board.moveStack = moveStack(new_board)

        return new_board