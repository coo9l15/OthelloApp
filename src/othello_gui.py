"""
Othello GUI
Provides a graphical user interface for playing Othello
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QGridLayout, QPushButton, 
                            QLabel, QVBoxLayout, QHBoxLayout, QMessageBox,
                            QMenuBar, QMenu)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPalette, QFont, QAction
from othello_game import OthelloGame, BLACK, WHITE, EMPTY

class OthelloSquare(QPushButton):
    """Represents a single square on the Othello board."""
    
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.setFixedSize(QSize(60, 60))
        self.setStyleSheet("""
            QPushButton {
                background-color: #008000;
                border: 1px solid #006400;
            }
            QPushButton:hover {
                background-color: #009000;
            }
        """)
        self.piece = EMPTY  # Current piece on this square
    
    def update_piece(self, piece):
        """Update the appearance based on the piece."""
        self.piece = piece
        if piece == EMPTY:
            self.setText("")
        else:
            self.setText("●")
            if piece == BLACK:
                self.setStyleSheet("""
                    QPushButton {
                        background-color: #008000;
                        border: 1px solid #006400;
                        color: black;
                        font-size: 32px;
                    }
                    QPushButton:hover {
                        background-color: #009000;
                    }
                """)
            else:  # WHITE
                self.setStyleSheet("""
                    QPushButton {
                        background-color: #008000;
                        border: 1px solid #006400;
                        color: white;
                        font-size: 32px;
                    }
                    QPushButton:hover {
                        background-color: #009000;
                    }
                """)

class OthelloGUI(QMainWindow):
    """Main window for the Othello game."""
    
    def __init__(self):
        super().__init__()
        self.game = OthelloGame()
        self.init_ui()
        self.update_board()
        self.highlight_valid_moves()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Othello")
        self.setGeometry(100, 100, 600, 650)
        
        # Create menu bar
        menu_bar = self.menuBar()
        game_menu = menu_bar.addMenu("Game")
        
        # Add menu actions
        new_game_action = QAction("New Game", self)
        new_game_action.triggered.connect(self.restart_game)
        game_menu.addAction(new_game_action)
        
        home_action = QAction("Return to Home", self)
        home_action.triggered.connect(self.return_to_home)
        game_menu.addAction(home_action)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Game info area
        info_layout = QHBoxLayout()
        self.black_score = QLabel("Black: 2")
        self.black_score.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.white_score = QLabel("White: 2")
        self.white_score.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.turn_label = QLabel("Current Turn: Black")
        self.turn_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        info_layout.addWidget(self.black_score)
        info_layout.addStretch()
        info_layout.addWidget(self.turn_label)
        info_layout.addStretch()
        info_layout.addWidget(self.white_score)
        
        main_layout.addLayout(info_layout)
        
        # Game board
        board_layout = QGridLayout()
        board_layout.setSpacing(0)
        
        self.squares = []
        for row in range(8):
            row_squares = []
            for col in range(8):
                square = OthelloSquare(row, col)
                square.clicked.connect(self.on_square_clicked)
                board_layout.addWidget(square, row, col)
                row_squares.append(square)
            self.squares.append(row_squares)
        
        main_layout.addLayout(board_layout)
        
        # Set dark green background
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 100, 0))
        self.setPalette(palette)
    
    def update_board(self):
        """Update the GUI board to match the game state."""
        # Update square pieces
        for row in range(8):
            for col in range(8):
                piece = self.game.board[row, col]
                self.squares[row][col].update_piece(piece)
        
        # Update scores
        black_count, white_count = self.game.count_pieces()
        self.black_score.setText(f"Black: {black_count}")
        self.white_score.setText(f"White: {white_count}")
        
        # Update turn label
        if self.game.game_over:
            if self.game.winner == BLACK:
                self.turn_label.setText("Game Over: Black Wins!")
            elif self.game.winner == WHITE:
                self.turn_label.setText("Game Over: White Wins!")
            else:
                self.turn_label.setText("Game Over: Draw!")
        else:
            player = "Black" if self.game.current_player == BLACK else "White"
            self.turn_label.setText(f"Current Turn: {player}")
    
    def highlight_valid_moves(self):
        """Highlight squares where the current player can place a piece."""
        # Reset all square styling
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                square.update_piece(self.game.board[row][col])
        
        # Highlight valid moves with a slightly different color
        valid_moves = self.game.get_valid_moves(self.game.current_player)
        for row, col in valid_moves:
            self.squares[row][col].setStyleSheet("""
                QPushButton {
                    background-color: #00A000;
                    border: 1px solid #006400;
                }
                QPushButton:hover {
                    background-color: #00B000;
                }
            """)
    
    def on_square_clicked(self):
        """Handle a square being clicked."""
        if self.game.game_over:
            self.show_game_over_message()
            return
            
        # Get the clicked square
        sender = self.sender()
        row, col = sender.row, sender.col
        
        # Try to make a move
        if self.game.play_turn(row, col):
            self.update_board()
            self.highlight_valid_moves()
            
            # Check for game over
            if self.game.game_over:
                self.show_game_over_message()
    
    def show_game_over_message(self):
        """Show a message box with game results."""
        black_count, white_count = self.game.count_pieces()
        
        if self.game.winner == BLACK:
            message = f"Black wins!\nFinal Score:\nBlack: {black_count}\nWhite: {white_count}"
        elif self.game.winner == WHITE:
            message = f"White wins!\nFinal Score:\nBlack: {black_count}\nWhite: {white_count}"
        else:
            message = f"It's a draw!\nFinal Score:\nBlack: {black_count}\nWhite: {white_count}"
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setInformativeText("What would you like to do?")
        
        new_game_btn = msg_box.addButton("New Game", QMessageBox.ButtonRole.ActionRole)
        menu_btn = msg_box.addButton("Return to Menu", QMessageBox.ButtonRole.ActionRole)
        
        result = msg_box.exec()
        
        clicked_button = msg_box.clickedButton()
        if clicked_button == new_game_btn:
            self.restart_game()
        elif clicked_button == menu_btn:
            self.return_to_home()
    
    def restart_game(self):
        """Restart the game with a new board."""
        self.game = OthelloGame()
        self.update_board()
        self.highlight_valid_moves()
    
    def return_to_home(self):
        """Return to the home screen."""
        # The parent (home screen) will be notified when this window is closed
        self.close() 