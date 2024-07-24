import numpy as np
from enum import Enum
import pygame

class ChessPieceType(Enum):
    
    INVALID = -1
    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5
    
ChessPieceSprites = {
    ChessPieceType.KING : "./assets/sprite/King",
    ChessPieceType.QUEEN : "./assets/sprite/Queen",
    ChessPieceType.ROOK : "./assets/sprite/Rook",
    ChessPieceType.BISHOP : "./assets/sprite/Bishop",
    ChessPieceType.KNIGHT : "./assets/sprite/Knight",
    ChessPieceType.PAWN : "./assets/sprite/Pawn"

}

class ChessPiece:
    def __init__(self, color, xGrid, yGrid, board):
        self.color = color
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.ChessBoard = board
        self.ID = ChessPieceType.INVALID
    
 
    def validMove(self):
        pass
    
    def isValidMove(self, move):
        moves = self.validMove()
        if(move in moves):
            return True
        else:
            return False
    
    def move(self, move):
        if self.isValidMove(move) == False:
            return False
        
        newMove = self.ChessBoard.board[move[0], move[1]]
        if( newMove != None):
            self.ChessBoard.board[newMove[0], newMove[1]] = None
            
        self.ChessBoard.board[self.xGrid, self.yGrid] = None
        
        self.xGrid = move[0]
        self.yGrid = move[1]
        
        self.ChessBoard.board[move[0], move[1]] = self
        
        return True
    
#specific moves for the king, general game rule such as check and checkmate
#will be implemented in the game class
class King(ChessPiece):
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__(color, xGrid, yGrid, board)
        self.ID = ChessPieceType.KING
        
    def validMove(self):
        moves = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            if 0 <= self.xGrid + dx < 8 and 0 <= self.yGrid + dy < 8:
                if self.ChessBoard.board[self.xGrid + dx, self.yGrid + dy] == None or self.ChessBoard.board[self.xGrid + dx, self.yGrid + dy].color != self.color:
                   if(not self.BeExposedToCheck((self.xGrid + dx, self.yGrid + dy))):
                        moves.append((self.xGrid + dx, self.yGrid + dy))
                        
        if(self.CanCastle("left")):
            self.ChessBoard.board[0, self.yGrid].move((4, self.yGrid))
            moves.append((0, self.yGrid))
        elif(self.CanCastle("right")):
            self.ChessBoard.board[7, self.yGrid].move((4, self.yGrid))
            moves.append((7, self.yGrid))
            
            
        return moves  
    #Check if the king would be in check after the move
    #if so, then invalidate the move
    #TODO implement castling and expose to check
    def BeExposedToCheck(self, move):
        opponent = "black" if self.color == "white" else "white"
        for row in self.ChessBoard.board:
            for piece in row:
                if  piece != None and piece.ID != ChessPieceType.KING and piece.color == opponent:
                    if move in piece.validMove():
                        return True
        return False
        
    #First check if the king is in check or will be exposed to check after the move
    #Castling can only be done if neither the king nor the rook involved in the move has been previously moved.
    #There cannot be any pieces between the king and the rook.
    #The king cannot be in check (under attack) before or after castling.
    #The squares the king moves over during castling cannot be under attack.
    def CanCastle(self, direction):
        if(direction == "left"):
            if(self.xGrid == 4 and self.yGrid == 0 and self.ChessBoard.board[0, self.yGrid].ID == ChessPieceType.ROOK and self.ChessBoard.board[1, self.yGrid] == None and self.ChessBoard.board[2, self.yGrid] == None and self.board[3, self.yGrid] == None):
                for i  in range(5):
                    if(self.BeExposedToCheck((i, self.yGrid))):
                        return False
                return True
        else:
            if(self.xGrid == 4 and self.yGrid == 0 and self.ChessBoard.board[7, self.yGrid].ID == ChessPieceType.ROOK and self.ChessBoard.board[5, self.yGrid] == None and self.ChessBoard.board[6, self.yGrid] == None):
                for i  in range(5, 8):
                    if(self.BeExposedToCheck((i, self.yGrid))):
                        return False
                return True
    
    def isValidMove(self, move):
        super().isValidMove(move)
       
    def move(self, move):
        return super().move(move)
    
        
class Queen(ChessPiece):
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__(color, xGrid, yGrid, board)
        self.ID = ChessPieceType.QUEEN
        
    def validMove(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Horizontal, vertical, and diagonal
        for dx, dy in directions:
            x, y = self.xGrid, self.yGrid
            while True:
                x += dx
                y += dy
                if 0 <= x < 8 and 0 <= y < 8:
                    if self.ChessBoard.board[x, y] == None:
                        moves.append((x,y))
                    elif self.ChessBoard.board[x][y].color != self.color:
                        moves.append((x, y))
                        break
                    else:
                        break
                else:
                    break
        return moves
                    
    def isValidMove(self, move):
        return super().isValidMove(move)
       
    def move(self, move):
        return super().move(move)
    
class Rook(ChessPiece):
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__(color, xGrid, yGrid, board)
        self.ID = ChessPieceType.ROOK
        
    def validMove(self):
        moves = []
        for dx in range(-7, 8):
            if 0 <= self.xGrid + dx < 8:
                if self.ChessBoard.board[self.xGrid + dx, self.yGrid] == None:
                    moves.append((self.xGrid + dx, self.yGrid))
                elif self.ChessBoard.board[self.xGrid + dx, self.yGrid].color != self.color:
                    moves.append((self.xGrid + dx, self.yGrid))
                    break
                else:
                    break
        for dy in range(-7, 8):
            if 0 <= self.yGrid + dy < 8:
                if self.ChessBoard.board[self.xGrid, self.yGrid + dy] == None:
                    moves.append((self.xGrid, self.yGrid + dy))
                elif self.ChessBoard.board[self.xGrid, self.yGrid + dy].color != self.color:
                    moves.append((self.xGrid, self.yGrid + dy))
                    break
                else:
                    break
        
        return moves
          
    
    def isValidMove(self, move):
        super().isValidMove(move)
       
    def move(self, move):
        super().move(move)
    
class Knight(ChessPiece):
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__(color, xGrid, yGrid, board)
        self.ID = ChessPieceType.KNIGHT
        
    def validMove(self):
        moves = []
        for dx, dy in [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]:
            if 0 <= self.xGrid + dx < 8 and 0 <= self.yGrid + dy < 8:
                if self.ChessBoard.board[self.xGrid + dx, self.yGrid + dy] == None or self.ChessBoard.board[self.xGrid + dx, self.yGrid + dy].color != self.color:
                    moves.append((self.xGrid + dx, self.yGrid + dy))
        return moves
          
    
    def isValidMove(self, move):
        super().isValidMove(move)
       
    def move(self, move):
        super().move(move)
    
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
        
        
        return moves
          
    
    def isValidMove(self, move):
        super().isValidMove(move)
       
    def move(self, move):
        super().move(move)
        
class Pawn(ChessPiece):
    def __init__(self, color, xGrid, yGrid, board):
        super().__init__( color, xGrid, yGrid, board)
        self.ID = ChessPieceType.PAWN
        
    def validMove(self):
        moves = []
        direction = 1 if self.color == "white" else -1
        
        if 0 <= self.yGrid + direction < 8 :
            #Move forward
            if self.ChessBoard.board[self.xGrid, self.yGrid+direction] == None:
                moves.append((self.xGrid, self.yGrid+direction))
            
            #Capture Diagonally
            for dx in [-1, 1]:
                if 0 <= self.xGrid + dx < 8:
                    if self.ChessBoard.board[self.xGrid + dx, self.yGrid + direction] != None and self.ChessBoard.board[self.xGrid+dx, self.yGrid+direction].color != self.color:
                        moves.append((self.xGrid+dx, self.yGrid+direction))
        
        #check for en passant
        #TODO implement en passant
        
        
        return moves
          
    
    def isValidMove(self, move):
        super().isValidMove(move)
       
    def move(self, move):
        if self.isValidMove(move) == False:
            return False
        
        newMove = self.ChessBoard.board[move[0], move[1]]
        if( newMove != None):
            self.ChessBoard.board[newMove[0]][newMove[1]] = None
            
        self.ChessBoard.board[self.xGrid, self.yGrid] = None
        
        self.xGrid = move[0]
        self.yGrid = move[1]
        
        self.ChessBoard.board[move[0], move[1]] = self
        
        
        #Check if the pawn has reached the end of the board, if so then promote
        if self.yGrid == 7 and self.color == "white" or self.yGrid == 0 and self.color == "black":
    
            self.ChessBoard.board.remove(self)
            self.ChessBoard.board.add(Queen(self.color, self.xGrid, self.yGrid))
                
        return True
        

class Chessboard:
    def __init__(self):
        self.board = np.empty((8, 8), dtype = ChessPiece)
       
        
    def SetUpBoard(self):
        for i in range(8):
            self.board[i, 1] = Pawn("white", i, 1, self)
            self.board[i, 6] = Pawn("black", i, 6, self)
            
        self.board[0, 0] = Rook("white", 0, 0, self)
        self.board[0, 7] = Rook("white", 7, 0, self)
        self.board[7, 0] = Rook("black", 0, 7, self)
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
        screen.fill((255, 255, 255))
        cell_size = 75
        boardColor = [(255, 255, 255), (30, 0, 30)]

        for x, col in enumerate(self.board):
            for y, piece in enumerate(col):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                color = boardColor[(x + y) % 2]
                pygame.draw.rect(screen, color, rect
                                 )
                if piece != None:
                    sprite_link =  ChessPieceSprites.get(piece.ID) + "_" + piece.color + ".png"
                    if sprite_link:
                        sprite = pygame.image.load(sprite_link).convert_alpha()
                        pos_x = x * 75 
                        pos_y = y * 75
                        screen.blit(sprite, (pos_x, pos_y))
           
    def renderValidSquares(self, screen, moves):
        cell_size = 75
        for move in moves:
            x, y = move
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 255, 0), rect)
            
class Game:
    def __init__(self, ai, screen, clock, font, color = "white"):
        self.ChessBoard = Chessboard()
        self.screen = screen
        self.color = color
        self.turn = 0 if color == "white" else 1
        self.whiteScore = 0
        self.blackScore = 0
        self.winner = None
        self.ai = ai
        self.endGame = False
        self.clock = clock
        self.font = font
        
    def StartGame(self):
        self.ChessBoard.SetUpBoard()
        self.InitializeScoreCounter()
        
        #Set up AI
        
        
    def InitializeScoreCounter(self):
        self.whiteScore = 0
        self.blackScore = 0
    
    def DeclareWinner(self):
        if self.whiteScore > self.blackScore:
            self.winner = "White"
        elif self.whiteScore < self.blackScore:
            self.winner = "Black"
        else:
            self.winner = "Tie"
    #Get player input and move accordingly 
    #if no valid move is found, prompt player to try again
    #add special moves such as castling, en passant, and pawn promotion
    def PlayerMove(self, side): 
        
        self.UserInput(side)
        
            
        
    def AIMove(self):
        pass

    def PlayGame(self):
        while self.endGame == False:
            
    
            forcedCheck = False
            possibleMoves = []
            res = self.CheckWinningConditions()
            side = "white" if self.turn == 0 else "black"
            if res == "Checkmate" or res == "Stalemate":
                self.endGame = True
            elif res == "Check":
                
                possibleMoves = self.ChessBoard.LegalMoves(side, True)
                forcedCheck = True
                
            self.ChessBoard.render(self.screen) 
            side_text_surface = self.font.render("{}'s turn".format(side), True, (0, 0, 0))
            self.screen.blit(side_text_surface, (0, 0))
            
            pygame.display.flip()   
            
            if self.turn == 0:
                self.PlayerMove(side)
            else:
                self.PlayerMove(side)
                
            self.turn = 1 - self.turn
            

            # fill the screen with a color to wipe away anything from last frame

            # RENDER YOUR GAME HERE

            # flip() the display to put your work on screen
            pygame.display.flip() 

            self.clock.tick(60)
            
            # limits FPS to 60
        
        self.DeclareWinner()
        
        pygame.quit()
    
    def UserInput(self, side):
        
        validInputSequence = False
        while not validInputSequence:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.endGame = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = (pos[0] // 75) % 7
                    y = (pos[1] // 75) % 7
                    rect = pygame.Rect(x * 75, y * 75, 75, 75)
                    pygame.draw.rect(self.screen, (255, 255, 0), rect)
                    
                    
                    print(x, y)
                    if(self.ChessBoard.board[x, y] != None and self.ChessBoard.board[x,y].color == side ):
                        
                       
                        
                        valid_moves = self.ChessBoard.board[x, y].validMove()
                        print(valid_moves)
                        self.ChessBoard.renderValidSquares(self.screen, valid_moves)
                        pygame.display.flip()
                        reset = False
                        while not reset:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    
                                    
                                    pos = pygame.mouse.get_pos()
                                    lx = (pos[0] // 75) % 7
                                    ly = (pos[1] // 75) % 7
                                    print(lx, ly)
                                    if self.ChessBoard.board[lx, ly] != None and self.ChessBoard.board[lx, ly].color == side:
                                        #If the user clicks on another piece of the same color, consider the new piece
                                        #as the selected piece
                                        self.ChessBoard.render(self.screen)
                                        
                                        x = lx
                                        y = ly
                                        
                                        rect = pygame.Rect(x * 75, y * 75, 75, 75)
                                        pygame.draw.rect(self.screen, (255, 255, 0), rect)
                                        valid_moves = self.ChessBoard.board[x, y].validMove()
                                        print(valid_moves)
                                        self.ChessBoard.renderValidSquares(self.screen, valid_moves)
                                        pygame.display.flip()
                                        
                                        break
                                    if (lx, ly) in valid_moves:
                                        self.ChessBoard.board[x, y].move((lx, ly))
                                        return
                                    else:
                                        print("Invalid Move")
                                        break
        
                            
                        
                    
    def CheckWinningConditions(self):
        #Check if the king is in check
        #Check if the king is in checkmate
        #Check if the king is in stalemate
        side = "white" if self.turn == 0 else "black"
        current_player_king = self.ChessBoard.find(ChessPieceType.KING, side)
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
        #Check if the opponent's pieces can attack the king
        opponent = "black" if side == "white" else "white"
        for row in self.ChessBoard.board:
            for piece in row:
                if piece != None and piece.color == opponent:
                    if (king.xGrid, king.yGrid) in piece.validMove():
                        return True
        return False
    
    def inCheckmate(self, king, side):
        #Check if there are any legal moves that can remove the king from check
        #Check if the king can move out of check
        #Check if pieces can block the check
        #Check if the attacking piece can be captured
        if not self.inCheck(king, side):
            return False
        
        moves = self.LegalMoves(side)
        
        if len(moves) == 0:
            return True
        
        return False
        
            
    def inStalemate(self, king, side):
        #Check if the current player has no legal moves but the king is not in check
        if not self.inCheck(king, side) and len(self.LegalMoves(side)) == 0:
            return True
        return False
                    
    def LegalMoves(self, side, check = False):
        #Generate all legal moves for the player
        moves = []
        for row in self.ChessBoard.board:
            for piece in row:
                if piece and piece.color == side:
                    moves.extend(piece.validMove())
        return moves
    
   
        
        
        