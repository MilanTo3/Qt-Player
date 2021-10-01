from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QMenuBar, QAction, QErrorMessage, QMessageBox, QMainWindow, QStackedWidget
import sys, math, srt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QFont, QColor
from PyQt5.QtCore import Qt, QUrl


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))
        self.setWindowFlag(Qt.FramelessWindowHint)

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)

        self.setPalette(p)

        self.init_ui()

        self.show()

    def init_ui(self):

        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.menuBar = QMenuBar()
        self.menuBar.setMaximumHeight(22)
        fileMenu = self.menuBar.addMenu("File")
        viewMenu = self.menuBar.addMenu("View")
        editMenu = self.menuBar.addMenu("Edit")
        self.fullscreenVar = False

        self.playPauseAction = QAction("Play", self)
        openFileAction = QAction("Open file", self)
        exitAction = QAction("Exit", self)
        self.toggleFullscreenAction = QAction("Fullscreen", self)
        subtitlesAction = QAction("Add subtitles", self)
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setShortcut("Ctrl+E")
        self.toggleFullscreenAction.setShortcut("Ctrl+F")
        subtitlesAction.setShortcut("Ctrl+A")
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(self.playPauseAction)
        viewMenu.addAction(self.toggleFullscreenAction)
        viewMenu.addAction(subtitlesAction)
        fileMenu.addAction(exitAction)
        openFileAction.triggered.connect(self.open_file)
        self.playPauseAction.triggered.connect(self.play_video)
        self.toggleFullscreenAction.triggered.connect(self.toggleFullscreen)
        exitAction.triggered.connect(self.quitApplication)
        subtitlesAction.triggered.connect(self.addSubtitles)

        # create videowidget object

        container = QWidget()
        videowidget = QVideoWidget()
        lay = QVBoxLayout(container)
        lay.addWidget(videowidget)

        # create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.sliderMoved.connect(self.volumeChanged)
        self.volumeSlider.sliderPressed.connect(self.volumeSliderClicked)
        self.volumeSlider.sliderReleased.connect(self.volumeSliderLetGoOff)
        self.volumeSlider.setMaximumWidth(63)

        # create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.durationLabel = QLabel()
        self.volumeLabel = QLabel()
        self.volumeLabel.setVisible(False)
        self.subTiTlesLabel = QLabel("", container)
        self.subTiTlesLabel.setFont(QFont("Arial", 22))
        self.subTitlesOn = False

        sample_palette = QPalette()
        sample_palette.setColor(QPalette.WindowText, Qt.white)

        self.subTiTlesLabel.setPalette(sample_palette)
        self.subTiTlesLabel.setAlignment(Qt.AlignHCenter)
        self.durationLabel.setText("")
        self.durationLabel.setStyleSheet("QLabel { color : white; }")
        self.volumeLabel.setStyleSheet("QLabel { color : white; }")
        self.durationLabel.setMaximumHeight(17)
        self.volumeLabel.setMaximumHeight(18)
        self.volumeChanged(100)

        # create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        # set widgets to the hbox layout
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(self.durationLabel)
        hboxLayout.addWidget(self.volumeSlider)
        hboxLayout.addWidget(self.volumeLabel)

        # create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.menuBar)
        vboxLayout.addWidget(container)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        vboxLayout.setAlignment(Qt.AlignHCenter)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)

        # media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playPauseAction.setText("Play")
        else:
            self.mediaPlayer.play()
            self.playPauseAction.setText("Pause")

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def toggleFullscreen(self):
        if self.fullscreenVar == False:
            self.showFullScreen()
            self.fullscreenVar = True
            self.toggleFullscreenAction.setText("Exit fullscreen")
        else:
            self.showNormal()
            self.fullscreenVar = False
            self.toggleFullscreenAction.setText("Fullscreen")

    def addSubtitles(self):

        filename, _ = QFileDialog.getOpenFileName(self, "Add subtitle")

        if filename != '':
            try:

                with open(filename) as f:
                    lines = f.readlines()
                    lines = ''.join(map(str, lines))
                    self.subtitles = list(srt.parse(lines))
                    self.subTitlesOn = True
            except:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Error.")
                msgBox.setWindowTitle("Sowie, couldn't load the subtitles.")
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msgBox.show()

    def volumeSliderClicked(self):
        self.volumeLabel.setVisible(True)

    def volumeSliderLetGoOff(self):
        self.volumeLabel.setVisible(False)

    def position_changed(self, position):
        self.slider.setValue(position)
        result = round(position / 1000)
        self.durationLabel.setText(self.getDurationString(result))
        if self.subTitlesOn:
            self.displaySubs(position)

    def displaySubs(self, timeposition):

        x : srt.Subtitle
        subtitle = self.findSubtitle(timeposition)

        if hasattr(subtitle, "content"):
            self.subTiTlesLabel.show()
            self.subTiTlesLabel.setText(subtitle.content)
            self.subTiTlesLabel.adjustSize()
            movecoef = (self.width() - self.subTiTlesLabel.width()) / 2
            self.subTiTlesLabel.setGeometry(int(movecoef), self.height() - 200, self.subTiTlesLabel.width(), self.subTiTlesLabel.height())

        else:
            self.subTiTlesLabel.hide()


    def findSubtitle(self, timeposition):

        x : srt.Subtitle
        for x in self.subtitles:
            if (((x.start.seconds * 1000 + (x.start.microseconds / 1000)) <= timeposition) and ((x.end.seconds * 1000 + (x.end.microseconds / 1000)) >= timeposition)):
                return x

        return -1

    def getDurationString(self, seconds):

        sec = seconds % 60
        secStr = str(sec)
        if sec < 10:
            secStr = "0" + secStr

        min = math.floor(seconds / 60)
        min = min % 60
        minstring = str(min)
        if min < 10:
            minstring = "0" + minstring

        hours = math.floor(seconds / 3600)
        hoursStr = str(hours)
        if hours < 10:
            hoursStr = "0" + hoursStr

        return hoursStr + ":" + minstring + ":" + secStr

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def volumeChanged(self, position):
        self.volumeSlider.setValue(position)
        self.mediaPlayer.setVolume(position)
        self.volumeLabel.setText(str(position) + "%")

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def quitApplication(self):
        sys.exit(app.exec_())

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())