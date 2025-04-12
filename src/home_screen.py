"""
Othello Home Screen
Initial screen with game mode options
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette

from othello_gui import OthelloGUI

class HomeScreen(QMainWindow):
    """Main menu for the Othello game."""
    
    def __init__(self):
        super().__init__()
        self.game_window = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Othello")
        self.setGeometry(100, 100, 400, 400)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # Title
        title_label = QLabel("OTHELLO")
        title_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white;")
        
        # Subtitle
        subtitle_label = QLabel("Classic Board Game")
        subtitle_label.setFont(QFont("Arial", 16))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: white;")
        
        # Single Player button
        single_player_btn = QPushButton("Single Player")
        single_player_btn.setFont(QFont("Arial", 14))
        single_player_btn.setFixedHeight(60)
        single_player_btn.setStyleSheet("""
            QPushButton {
                background-color: #006400;
                color: white;
                border-radius: 5px;
                border: 2px solid #004000;
            }
            QPushButton:hover {
                background-color: #008000;
            }
        """)
        single_player_btn.clicked.connect(self.on_single_player_clicked)
        
        # Two Players button
        two_players_btn = QPushButton("Two Players")
        two_players_btn.setFont(QFont("Arial", 14))
        two_players_btn.setFixedHeight(60)
        two_players_btn.setStyleSheet("""
            QPushButton {
                background-color: #006400;
                color: white;
                border-radius: 5px;
                border: 2px solid #004000;
            }
            QPushButton:hover {
                background-color: #008000;
            }
        """)
        two_players_btn.clicked.connect(self.on_two_players_clicked)
        
        # Add widgets to layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addStretch()
        main_layout.addWidget(single_player_btn)
        main_layout.addWidget(two_players_btn)
        main_layout.addStretch()
        
        # Set dark green background
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 100, 0))
        self.setPalette(palette)
    
    def on_single_player_clicked(self):
        """Handle Single Player button click."""
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Single Player Mode")
        msg_box.setText("Single Player mode is not implemented yet.")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()
    
    def on_two_players_clicked(self):
        """Handle Two Players button click."""
        self.game_window = OthelloGUI()
        self.game_window.show()
        self.game_window.destroyed.connect(self.show_home_screen)
        self.hide()
    
    def show_home_screen(self):
        """Show the home screen when game window is closed."""
        self.show() 