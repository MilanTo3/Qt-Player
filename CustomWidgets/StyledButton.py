from PyQt5.QtWidgets import QPushButton

class StyledButton(QPushButton):

    def __init__(self, text):

        super().__init__()
        self.setText(text)
        self.setStyleSheet("QPushButton{ background: rgb(30, 30, 30); color: white; font-weight: bold; } QPushButton:hover{ background: rgb(100, 100, 100); }")