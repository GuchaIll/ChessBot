import numpy as np
from enum import Enum
import pygame
from Engine.evaluation import *
from Engine.AI.minmax import *
from Engine.chessboard import *


class Game:
    """Class representing the chess game."""
    def __init__(self, screen, clock, font, color="white"):
        """
        Initialize the game.

        Args:
            screen (pygame.Surface): The screen to render the game on.
            clock (pygame.time.Clock): The game clock.
            font (pygame.font.Font): The font for rendering text.
            color (str): The player's color ('white' or 'black').
        """
        self.ChessBoard = Chessboard()
        self.screen = screen
        self.color = color
        self.turn = 0 if color == "white" else 1
        self.winner = None
        self.AI = MinMax(self, self.ChessBoard, 3)
        self.endGame = False
        self.clock = clock
        self.font = font
        self.score = 0

    def StartGame(self):
        """Start the game by setting up the board and initializing the score counter."""
        self.ChessBoard.SetUpBoard()
        self.InitializeScoreCounter()

    def InitializeScoreCounter(self):
        """Initialize the score counters for both players."""
        self.whiteScore = 0
        self.blackScore = 0

    def DeclareWinner(self):
        """Declare the winner based on the scores."""
        if self.whiteScore > self.blackScore:
            self.winner = "White"
        elif self.whiteScore < self.blackScore:
            self.winner = "Black"
        else:
            self.winner = "Tie"

    def PlayerMove(self, side, forcedCheck=False, possibleMoves=[]):
        """
        Handle the player's move.

        Args:
            side (str): The player's side ('white' or 'black').
            forcedCheck (bool): Whether the player is in check.
            possibleMoves (list): List of possible moves.
        """
        pieceMoved = self.UserInput(side)
        if pieceMoved and forcedCheck:
            current_player_king = self.ChessBoard.find(ChessPieceType.KING, side)
            if self.inCheck(current_player_king, side):
                print("Invalid Move")
                pieceMoved.ChessBoard.moveStack.undoMove()
                self.PlayerMove(side, forcedCheck, possibleMoves)

    def AIMove(self, side, forcedCheck, possibleMoves):
        """
        Handle the AI's move.

        Args:
            side (str): The AI's side ('white' or 'black').
            forcedCheck (bool): Whether the AI is in check.
            possibleMoves (list): List of possible moves.
        """
        piece, move = self.AI.find_best_move(side, forcedCheck)
        piece.move(move)

    def PlayGame(self):
        """Run the main game loop."""
        while not self.endGame:
            forcedCheck = False
            possibleMoves = []
            res = self.CheckWinningConditions()
            side = "white" if self.turn == 0 else "black"

            if res in ["Checkmate", "Stalemate"]:
                if res == "Checkmate":
                    print(f"{side} wins!")
                else:
                    print("Stalemate! It's a draw!")
                self.endGame = True
            elif res == "Check":
                possibleMoves = self.LegalMoves(side, True)
                forcedCheck = True
                print("Check")

            self.ChessBoard.render(self.screen)
            self.ChessBoard.renderCapturedPieces(self.screen)

            score_text_surface = self.font.render(f"Current Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text_surface, (600, 550))

            side_text_surface = self.font.render(f"{side}'s turn", True, (0, 0, 0))
            self.screen.blit(side_text_surface, (600, 600))

            pygame.display.flip()

            if self.turn == 0:
                self.PlayerMove(side, forcedCheck, possibleMoves)
                self.score = self.ChessBoard.evaluate()
            else:
                self.AIMove(side, forcedCheck, possibleMoves)
                self.score = self.ChessBoard.evaluate()

            self.turn = 1 - self.turn

            pygame.display.flip() 
            self.clock.tick(60)

        self.DeclareWinner()
        pygame.quit()

    def UserInput(self, side):
        """
        Handle user input for selecting and moving pieces.

        Args:
            side (str): The player's side ('white' or 'black').

        Returns:
            ChessPiece: The piece that was moved.
        """
        validInputSequence = False
        while not validInputSequence and not self.endGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.endGame = True
                    return None
            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = (pos[0] // 75) % 8
                    y = (pos[1] // 75) % 8

                    print(f"Clicked on {x}, {y}")

                    if self.ChessBoard.board[x, y] is not None and self.ChessBoard.board[x, y].color == side:
                        valid_moves = self.ChessBoard.board[x, y].validMove()
                        print(f"Valid moves: {valid_moves}")

                        # Highlight the selected piece and valid moves
                        self.ChessBoard.render(self.screen)
                        self.ChessBoard.renderCapturedPieces(self.screen)
                        rect = pygame.Rect(x * 75, y * 75, 75, 75)
                        pygame.draw.rect(self.screen, (255, 255, 0), rect)
                        self.ChessBoard.renderValidSquares(self.screen, valid_moves)
                        pygame.display.flip()

                        # Wait for the second click
                        waiting_for_move = True
                        while waiting_for_move and not self.endGame:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    self.endGame = True
                                    return None

                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    pos = pygame.mouse.get_pos()
                                    lx = (pos[0] // 75) % 8
                                    ly = (pos[1] // 75) % 8

                                    print(f"Second click on {lx}, {ly}")

                                    # Check if clicking on another piece of the same color
                                    if (self.ChessBoard.board[lx, ly] is not None and 
                                        self.ChessBoard.board[lx, ly].color == side):
                                        # Select new piece
                                        x, y = lx, ly
                                        valid_moves = self.ChessBoard.board[x, y].validMove()
                                        print(f"New piece selected, valid moves: {valid_moves}")

                                        # Re-render with new selection
                                        self.ChessBoard.render(self.screen)
                                        self.ChessBoard.renderCapturedPieces(self.screen)
                                        rect = pygame.Rect(x * 75, y * 75, 75, 75)
                                        pygame.draw.rect(self.screen, (255, 255, 0), rect)
                                        self.ChessBoard.renderValidSquares(self.screen, valid_moves)
                                        pygame.display.flip()
                                        continue
                                    
                                    # Check if the move is valid
                                    if (lx, ly) in valid_moves:
                                        # Validate that the move doesn't leave king in check
                                        current_player_king = self.ChessBoard.find(ChessPieceType.KING, side)

                                        # Temporarily make the move
                                        piece = self.ChessBoard.board[x, y]
                                        original_target = self.ChessBoard.board[lx, ly]
                                        piece.move((lx, ly))

                                        # Check if king is in check after the move
                                        if self.inCheck(current_player_king, side):
                                            print("Move leaves king in check - invalid")
                                            # Undo the move
                                            self.ChessBoard.moveStack.undoMove()
                                            waiting_for_move = False
                                            break
                                        else:
                                            print("Valid move made")
                                            validInputSequence = True
                                            waiting_for_move = False
                                            return self.ChessBoard.board[lx, ly]
                                    else:
                                        print("Invalid move")
                                        waiting_for_move = False
                                        break
                
        

    def CheckWinningConditions(self):
        """
        Check the current game state for winning conditions.

        Returns:
            str: The game state ('Checkmate', 'Stalemate', 'Check', or 'Continue').
        """
        side = "white" if self.turn == 0 else "black"
        current_player_king = self.ChessBoard.find(ChessPieceType.KING, side)
        
         # If king is not found, it's checkmate (king was captured)
        if current_player_king is None:
            print(f"King not found for {side} - game over")
            return "Checkmate"
    
        if self.inCheck(current_player_king, side):
            if self.inCheckmate(current_player_king, side):
                return "Checkmate"
            else:
                return "Check"
        elif self.inStalemate(current_player_king, side):

            return "Stalemate"
        else:
            return "Continue"

    def inCheck(self, king, side):
        """
        Check if the king is in check.

        Args:
            king (ChessPiece): The king piece.
            side (str): The player's side ('white' or 'black').

        Returns:
            bool: True if the king is in check, False otherwise.
        """
        if king is None:
            print(f"Warning: King not found for {side}")
            return False
    
        opponent = "black" if side == "white" else "white"
        for row in self.ChessBoard.board:
            for piece in row:
                if piece and piece.color == opponent and piece.ID != ChessPieceType.KING:
                    if (king.xGrid, king.yGrid) in piece.validMove():
                        return True
        return False

    def inCheckmate(self, king, side):
        """
        Check if the king is in checkmate.

        Args:
            king (ChessPiece): The king piece.
            side (str): The player's side ('white' or 'black').

        Returns:
            bool: True if the king is in checkmate, False otherwise.
        """
        if not self.inCheck(king, side):
            return False
        moves = self.LegalMoves(side)
        if len(moves) == 0:
            print("Checkmate")
        return len(moves) == 0

    def inStalemate(self, king, side):
        """
        Check if the game is in stalemate.

        Args:
            king (ChessPiece): The king piece.
            side (str): The player's side ('white' or 'black').

        Returns:
            bool: True if the game is in stalemate, False otherwise.
        """
        print("checking Stalemate")
        print(f"Checking stalemate for {side}")
        print(f"King in check: {self.inCheck(king, side)}")
        legal_moves = self.LegalMoves(side)
        print(f"Legal moves available: {len(legal_moves)} -> {legal_moves}")

        return not self.inCheck(king, side) and len(self.LegalMoves(side)) == 0

    def LegalMoves(self, side, check=False):
        """
        Generate all legal moves for the player.

        Args:
            side (str): The player's side ('white' or 'black').
            check (bool): Whether to filter moves that leave the king in check.

        Returns:
            list: A list of legal moves as (piece, move) tuples.
        """
        moves = []
        for row in self.ChessBoard.board:
            for piece in row:
                if piece and piece.color == side:
                    for move in piece.validMove():
                        moves.append((piece, move))

        if check:
            current_player_king = self.ChessBoard.find(ChessPieceType.KING, side)
            checked_moves = []
            for piece, move in moves:
                piece.move(move)
                if not self.inCheck(current_player_king, side):
                    checked_moves.append((piece, move))
                piece.ChessBoard.moveStack.undoMove()
            return checked_moves

        return moves

    def copy_for_simulation(self, board_copy):
        """
        Create a game copy for AI simulation.
        
        Args:
            board_copy (Chessboard): The copied board.
            
        Returns:
            Game: A game instance for simulation.
        """
        # Create a minimal game copy for evaluation purposes
        sim_game = Game.__new__(Game)  # Create without calling __init__
        sim_game.ChessBoard = board_copy
        sim_game.turn = self.turn
        sim_game.endGame = False

        return sim_game


    