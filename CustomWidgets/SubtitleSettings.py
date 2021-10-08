from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QColorDialog, QFontDialog, QPushButton, QDialog
from PyQt5.QtGui import QColor, QFontInfo, QFont, QPalette
from PyQt5.QtCore import Qt

class SubtitleSettings(QDialog):

    def __init__(self, label):
        super().__init__()

        self.textcolor = -1
        self.backgroundcolor = -1
        self.font = -1
        self.acceptChangesVariable = False
        self.label : QLabel = label
        p = QPalette()
        p.setColor(QPalette.Window, QColor("#FF69B4"))
        p.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(p)
        self.initUI()
        self.show()

    def initUI(self):

        self.testText = QLabel("This is how the subtitles will look.")
        self.testText.setStyleSheet(self.label.styleSheet())
        self.testText.setFont(self.label.font())
        self.testText.setPalette(self.label.palette())
        self.textColorBtn = QPushButton("Change text color")
        self.backgroundColorBtn = QPushButton("Change background color")
        self.fontBtn = QPushButton("Change font")
        self.acceptBtn = QPushButton("Accept")
        self.cancelBtn = QPushButton("Cancel")
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hboxControlButtons = QHBoxLayout()
        vbox.addWidget(self.testText)
        hbox.addWidget(self.textColorBtn)
        hbox.addWidget(self.backgroundColorBtn)
        hbox.addWidget(self.fontBtn)
        hboxControlButtons.addWidget(self.acceptBtn)
        hboxControlButtons.addWidget(self.cancelBtn)
        vbox.addLayout(hbox)
        vbox.addLayout(hboxControlButtons)
        self.testText.setAlignment(Qt.AlignHCenter)
        self.textColorBtn.clicked.connect(self.set_text_color)
        self.backgroundColorBtn.clicked.connect(self.set_background_color)
        self.fontBtn.clicked.connect(self.set_font)
        self.acceptBtn.clicked.connect(self.accept_button)
        self.cancelBtn.clicked.connect(self.cancel_button)
        self.setLayout(vbox)
        self.setModal(True)

    def set_text_color(self):
        self.textcolor = QColorDialog.getColor()
        p = self.testText.palette()
        p.setColor(self.testText.foregroundRole(), self.textcolor)
        self.testText.setPalette(p)

    def set_background_color(self):
        self.backgroundcolor = QColorDialog.getColor()
        self.testText.setStyleSheet("QLabel { background-color: %s; font-weight: bold; }" % self.backgroundcolor.name())

    def set_font(self):
        font, valid = QFontDialog.getFont()
        if valid:
            self.font = font
            self.testText.setFont(font)

    def accept_button(self):
        self.acceptChangesVariable = True
        self.accept()

    def cancel_button(self):
        self.close()
