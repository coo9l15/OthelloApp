#!/usr/bin/env python3
"""
Othello (Reversi) Game
Main entry point for the application
"""

import sys
from PyQt6.QtWidgets import QApplication
from home_screen import HomeScreen

def main():
    app = QApplication(sys.argv)
    window = HomeScreen()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
