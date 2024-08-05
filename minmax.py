import random

        
class MinMax:
    def __init__ (self, game, board, depth):
        self.game = game
        self.ChessBoard = board
        self.depth = depth

    def best_move(self, depth, board, alpha, beta, maximizing_player):
        gameStatus = self.game.CheckWinningConditions()
        if depth == 0 or gameStatus == "Stalemate" or "Checkmate":
            eval = self.ChessBoard.evaluate()
            print("Terminal Node ", eval)
            return eval
            
        if maximizing_player:
            max_eval = float('-inf')
            inCheck = True if gameStatus == "Check" else False
            side = "white" if self.game.turn == 0 else "black"
            for piece, move in self.game.LegalMoves(side, inCheck):
                self.ChessBoard.makeMove(piece, move)
                eval = self.best_move(depth-1, alpha, beta, self.ChessBoard, False)
                self.ChessBoard.undoMove()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    print("return early from node ", alpha, beta)
                    break
            print("Maximizing ", max_eval)
            return max_eval
        
        else:
            min_eval = float('inf')
            inCheck = True if gameStatus == "Check" else False
            side = "white" if self.game.turn == 0 else "black"
            for piece, move in self.game.LegalMoves(side, inCheck):
                self.ChessBoard.makeMove(piece, move)
                eval = self.best_move(depth-1, alpha, beta, self.ChessBoard, True)
                self.ChessBoard.undoMove()
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    print("return early from node ", alpha, beta)
                    break
            print("Minimizing ", max_eval)
            return min_eval
            
            
    def find_best_move(self, side, inCheck):
        bestScore = float('inf')
        bestMove = None
        for piece, move in self.game.LegalMoves(side, inCheck):
            self.ChessBoard.makeMove(piece, move)
            score = self.best_move(self.depth - 1, float('-inf'), float('inf'), self.ChessBoard, False)
            self.ChessBoard.undoMove()
            if score > bestScore:
                best_score = score
                bestMove = (piece, move)
                print("newBestScore/move", best_score, bestMove)
        if bestMove == None:
                bestMove = random.choice(self.game.LegalMoves(side, inCheck))
                print("bestMove", bestMove[0], bestMove[1])
                self.ChessBoard.makeMove(piece, move)
                bestScore = self.ChessBoard.evaluate()
                self.ChessBoard.undoMove()
        return bestMove
                