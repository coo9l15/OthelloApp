"""
Othello Game Logic
Contains the core game mechanics and board representation
"""

import numpy as np

# Constants for game pieces
EMPTY = 0
BLACK = 1
WHITE = 2

class OthelloGame:
    def __init__(self):
        # Initialize 8x8 board with zeros (empty)
        self.board = np.zeros((8, 8), dtype=int)
        
        # Set up initial board state with 4 pieces in the middle
        self.board[3, 3] = WHITE
        self.board[3, 4] = BLACK
        self.board[4, 3] = BLACK
        self.board[4, 4] = WHITE
        
        # Black goes first
        self.current_player = BLACK
        
        # Game state
        self.game_over = False
        self.winner = None
    
    def get_opponent(self, player):
        """Return the opponent of the given player."""
        return BLACK if player == WHITE else WHITE
    
    def count_pieces(self):
        """Return the count of black and white pieces on the board."""
        black_count = np.count_nonzero(self.board == BLACK)
        white_count = np.count_nonzero(self.board == WHITE)
        return black_count, white_count
    
    def is_valid_move(self, row, col, player):
        """Check if placing a piece at (row, col) is valid for the given player."""
        # Check if position is on the board
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
            
        # Check if position is empty
        if self.board[row, col] != EMPTY:
            return False
            
        opponent = self.get_opponent(player)
        
        # Check all 8 directions
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            
            # Check if adjacent position has opponent piece
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                # Continue in this direction
                r += dr
                c += dc
                
                # Keep going until finding player's piece
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r, c] == EMPTY:
                        break
                    if self.board[r, c] == player:
                        return True  # Found a valid move
                    r += dr
                    c += dc
                    
        return False
    
    def get_valid_moves(self, player):
        """Return a list of valid move positions (row, col) for the given player."""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves
    
    def make_move(self, row, col, player):
        """Place a piece at (row, col) for the given player and flip captured pieces."""
        if not self.is_valid_move(row, col, player):
            return False
            
        # Place the player's piece
        self.board[row, col] = player
        opponent = self.get_opponent(player)
        
        # Capture pieces in all 8 directions
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        
        for dr, dc in directions:
            pieces_to_flip = []
            r, c = row + dr, col + dc
            
            # Check for opponent pieces in this direction
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
                
                # Check if we found a player piece at the end
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == player:
                    # Flip all opponent pieces in between
                    for flip_r, flip_c in pieces_to_flip:
                        self.board[flip_r, flip_c] = player
                    break
        
        return True
    
    def switch_player(self):
        """Switch the current player."""
        self.current_player = self.get_opponent(self.current_player)
    
    def check_game_over(self):
        """Check if the game is over and determine the winner."""
        # Check if either player has valid moves
        black_moves = self.get_valid_moves(BLACK)
        white_moves = self.get_valid_moves(WHITE)
        
        if not black_moves and not white_moves:
            self.game_over = True
            black_count, white_count = self.count_pieces()
            
            if black_count > white_count:
                self.winner = BLACK
            elif white_count > black_count:
                self.winner = WHITE
            else:
                self.winner = EMPTY  # Draw
            
            return True
        
        return False
    
    def play_turn(self, row, col):
        """Execute a single turn of the game."""
        if self.game_over:
            return False
            
        # Make the move
        if not self.make_move(row, col, self.current_player):
            return False
            
        # Switch player
        self.switch_player()
        
        # Check if the new player has any valid moves
        if not self.get_valid_moves(self.current_player):
            # Skip the player's turn if they have no valid moves
            self.switch_player()
            
        # Check if game is over
        self.check_game_over()
        
        return True 