import random

class MinMax:
    def __init__(self, game, board, depth):
        self.game = game
        self.ChessBoard = board
        self.depth = depth

    def best_move(self, game_copy, depth, alpha, beta, maximizing_player):
        """
        Evaluate the best move using a copied game state.
        
        Args:
            game_copy (Game): The copied game state for simulation.
            depth (int): Current search depth.
            alpha (float): Alpha value for pruning.
            beta (float): Beta value for pruning.
            maximizing_player (bool): Whether this is the maximizing player.
        """
        gameStatus = game_copy.CheckWinningConditions()
        if depth == 0 or gameStatus == "Stalemate" or gameStatus == "Checkmate":
            eval = game_copy.ChessBoard.evaluate()
            print(f"Terminal evaluation at depth {depth}: {eval}")
            return eval
            
        if maximizing_player:
            max_eval = float('-inf')
            inCheck = True if gameStatus == "Check" else False
            side = "white" if game_copy.turn == 0 else "black"
            legal_moves = game_copy.LegalMoves(side, inCheck)
            
            
            
            if not legal_moves:
                return game_copy.ChessBoard.evaluate()

            for piece, move in legal_moves:
                # Make the move on the copied board
                piece.move(move, False)  # Don't record captures in simulation
                game_copy.turn = 1 - game_copy.turn
                
                # Evaluate the position (next player is minimizing)
                eval = self.best_move(game_copy, depth-1, alpha, beta, False)

                game_copy.ChessBoard.moveStack.undoMove(False)
                game_copy.turn = 1 - game_copy.turn
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            
            print(f"Maximizing result at depth {depth}: {max_eval}")
            return max_eval
        
        else:
            min_eval = float('inf')
            inCheck = True if gameStatus == "Check" else False
            side = "white" if game_copy.turn == 0 else "black"
            legal_moves = game_copy.LegalMoves(side, inCheck)
            
            
            if not legal_moves:
                return game_copy.ChessBoard.evaluate()

            for piece, move in legal_moves:
                # Make the move on the copied board
                piece.move(move, False)  
                game_copy.turn = 1 - game_copy.turn
                
                eval = self.best_move(game_copy, depth-1, alpha, beta, True)
                
                # Undo the move on the copied board
                game_copy.ChessBoard.moveStack.undoMove(False)
                game_copy.turn = 1 - game_copy.turn
                
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            
            print(f"Minimizing result at depth {depth}: {min_eval}")
            return min_eval
            
    def find_best_move(self, side, inCheck):
        # Create one copy of the board for the entire AI evaluation
        board_copy = self.ChessBoard.copy()
        game_copy = self.game.copy_for_simulation(board_copy)

        bestScore = float('-inf') if side == "white" else float('inf')
        bestMove = None

        # Get legal moves from the ORIGINAL game, not the copy
        legal_moves = self.game.LegalMoves(side, inCheck)

        if not legal_moves:
            print("No legal moves available!")
            return None

        print(f"AI ({side}) evaluating {len(legal_moves)} possible moves...")

        # Make a copy of the list before shuffling to avoid modifying the original
        legal_moves_copy = legal_moves.copy()
        random.shuffle(legal_moves_copy)  

        for i, (piece, move) in enumerate(legal_moves_copy):

            # Find the corresponding piece in the copied board
            copied_piece = board_copy.board[piece.xGrid, piece.yGrid]
            if copied_piece is None:
                print(f"Error: Could not find piece at ({piece.xGrid},{piece.yGrid}) in copied board")
                continue

            copied_piece.move(move, False)
            game_copy.turn = 1 - game_copy.turn

            # Determine if the AI is maximizing or minimizing
            if side == "white":
                # AI is white (maximizing), opponent is black (minimizing)
                score = self.best_move(game_copy, self.depth - 1, float('-inf'), float('inf'), False)
            else:
                # AI is black (minimizing), opponent is white (maximizing)  
                score = self.best_move(game_copy, self.depth - 1, float('-inf'), float('inf'), True)

           
            board_copy.moveStack.undoMove(False)
            # Restore turn
            game_copy.turn = 1 - game_copy.turn

            print(f"Move {piece.ID} from ({piece.xGrid},{piece.yGrid}) to {move} scored: {score}")

            # Update best move based on player type
            if side == "white" and score > bestScore:
                bestScore = score
                bestMove = (piece, move)  # Return original piece, not copied piece
                print(f"New best move for white: {piece.ID} from ({piece.xGrid},{piece.yGrid}) to {move}, score: {bestScore}")
            elif side == "black" and score < bestScore:
                bestScore = score
                bestMove = (piece, move)  # Return original piece, not copied piece
                print(f"New best move for black: {piece.ID} from ({piece.xGrid},{piece.yGrid}) to {move}, score: {bestScore}")

        if bestMove == None:
            bestMove = random.choice(legal_moves)  # Use original legal_moves
            print(f"No improvement found, random move: {bestMove[0].ID} from ({bestMove[0].xGrid},{bestMove[0].yGrid}) to {bestMove[1]}")
        else:
            print(f"Final best move: {bestMove[0].ID} from ({bestMove[0].xGrid},{bestMove[0].yGrid}) to {bestMove[1]} with score {bestScore}")

        return bestMove