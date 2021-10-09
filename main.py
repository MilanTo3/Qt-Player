from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QMenuBar, QAction, QErrorMessage, QMessageBox, QMainWindow, QStackedWidget, QGraphicsOpacityEffect
import sys, math, srt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QFont, QColor, QResizeEvent, QMouseEvent
from PyQt5.QtCore import Qt, QUrl, QPoint, QPropertyAnimation, pyqtSlot
from CustomWidgets.SubtitleSettings import SubtitleSettings
from CustomWidgets.SearchSubtitlesOnline import SearchSubtitlesOnline
from CustomWidgets.SliderTimebar import SliderTimebar

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        #self.setWindowFlag(Qt.FramelessWindowHint)

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
        self.fileMenu = self.menuBar.addMenu("File")
        self.viewMenu = self.menuBar.addMenu("View")
        self.editMenu = self.menuBar.addMenu("Edit")
        self.helpMenu = self.menuBar.addMenu("Help")
        self.fullscreenVar = False

        self.playPauseAction = QAction("Play", self)
        openFileAction = QAction("Open file", self)
        exitAction = QAction("Exit", self)
        self.toggleFullscreenAction = QAction("Fullscreen", self)
        subtitlesAction = QAction("Add subtitles", self)
        volumeIncAction = QAction("Increase volume by 10%", self)
        volumeDecAction = QAction("Decrease the volume by 10%", self)
        self.volumeMuteAction = QAction("Mute the volume", self)
        forwardAction = QAction("Jump 10 seconds forward", self)
        backAction = QAction("Jump 10 seconds backward", self)
        incPlaybackRate = QAction("Increase the playback rate", self)
        decPlaybackRate = QAction("Decrease the playback rate", self)
        resetPlaybackRate = QAction("Reset the playback rate", self)
        subtitlesOffAction = QAction("Turn off the subtitles", self)
        customizeSubtitlesAction = QAction("Subtitle settings", self)
        showPlaylistAction = QAction("Show Playlist", self)
        onlineSubtitlesAction = QAction("Search online subtitles", self)
        aboutInfoAction = QAction("About...", self)
        videoNotPlayingHelpAction = QAction("Video not playing. What the fuck dude?", self)
        customizeAppearance = QAction("Customize appearance color n font")
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setShortcut("Ctrl+E")
        volumeIncAction.setShortcut("Ctrl+-")
        volumeDecAction.setShortcut("Ctrl++")
        self.volumeMuteAction.setShortcut("Ctrl+S")
        forwardAction.setShortcut("right")
        backAction.setShortcut("left")
        self.toggleFullscreenAction.setShortcut("Ctrl+F")
        subtitlesAction.setShortcut("Ctrl+A")
        self.fileMenu.addAction(openFileAction)
        self.fileMenu.addAction(self.playPauseAction)
        self.viewMenu.addAction(self.toggleFullscreenAction)
        self.viewMenu.addAction(subtitlesAction)
        self.viewMenu.addAction(subtitlesOffAction)
        self.viewMenu.addAction(showPlaylistAction)
        self.fileMenu.addAction(exitAction)
        self.editMenu.addAction(volumeIncAction)
        self.editMenu.addAction(volumeDecAction)
        self.editMenu.addAction(self.volumeMuteAction)
        self.editMenu.addAction(incPlaybackRate)
        self.editMenu.addAction(decPlaybackRate)
        self.editMenu.addAction(forwardAction)
        self.editMenu.addAction(backAction)
        self.editMenu.addAction(resetPlaybackRate)
        self.editMenu.addAction(customizeSubtitlesAction)
        self.editMenu.addAction(onlineSubtitlesAction)
        self.editMenu.addAction(customizeAppearance)
        self.helpMenu.addAction(aboutInfoAction)
        self.helpMenu.addAction(videoNotPlayingHelpAction)
        openFileAction.triggered.connect(self.open_file)
        self.playPauseAction.triggered.connect(self.play_video)
        self.toggleFullscreenAction.triggered.connect(self.toggleFullscreen)
        exitAction.triggered.connect(self.quitApplication)
        subtitlesAction.triggered.connect(self.addSubtitles)
        subtitlesOffAction.triggered.connect(self.turnOFFTheSubtitles)
        volumeIncAction.triggered.connect(self.volumeIncrease)
        volumeDecAction.triggered.connect(self.volumeDecrease)
        self.volumeMuteAction.triggered.connect(self.volumeMute)
        forwardAction.triggered.connect(self.jumpForward10Sec)
        backAction.triggered.connect(self.jumpBack10Sec)
        incPlaybackRate.triggered.connect(self.increasePlaybackRate)
        decPlaybackRate.triggered.connect(self.decreasePlaybackRate)
        resetPlaybackRate.triggered.connect(self.resetPlayback)
        customizeSubtitlesAction.triggered.connect(self.settingsSubtitles)
        aboutInfoAction.triggered.connect(self.aboutInfoMessageBoxShow)
        videoNotPlayingHelpAction.triggered.connect(self.videoNotPlayingMessageBoxShow)
        onlineSubtitlesAction.triggered.connect(self.findSubtitlesOnline)
        customizeAppearance.triggered.connect(self.changeAppearance)

        # create videowidget object

        container = QWidget()
        videowidget = QVideoWidget()
        videowidget.setMouseTracking(True)
        lay = QVBoxLayout(container)
        lay.addWidget(videowidget)

        # create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.backBtn = QPushButton()
        self.backBtn.setEnabled(False)
        self.backBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.backBtn.clicked.connect(self.jumpBack10Sec)

        self.forwardBtn = QPushButton()
        self.forwardBtn.setEnabled(False)
        self.forwardBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forwardBtn.clicked.connect(self.jumpForward10Sec)

        # create slider
        self.slider = SliderTimebar(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        self.slider.signal.connect(self.jumpPosition)
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.sliderMoved.connect(self.volumeChanged)
        self.volumeSlider.sliderPressed.connect(self.volumeSliderClicked)
        self.volumeSlider.sliderReleased.connect(self.volumeSliderLetGoOff)
        self.volumeSlider.setMaximumWidth(63)

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
        self.subTiTlesLabel.hide()
        self.durationLabel.setText("")
        self.durationLabel.setStyleSheet("QLabel { color : white; font-weight: bold; }")
        self.volumeLabel.setStyleSheet("QLabel { color : white; font-weight: bold; }")
        self.durationLabel.setMaximumHeight(17)
        self.volumeLabel.setMaximumHeight(18)
        self.volumeChanged(100)

        # create hbox layout

        self.vboxLayout1 = QVBoxLayout()
        hboxLayout1 = QHBoxLayout()
        hboxLayout2 = QHBoxLayout()
        hboxLayout1.setContentsMargins(0, 0, 0, 0)

        # set widgets to the hbox layout
        hboxLayout1.addWidget(self.slider)
        hboxLayout1.addWidget(self.durationLabel)
        hboxLayout1.addWidget(self.volumeSlider)
        hboxLayout1.addWidget(self.volumeLabel)
        hboxLayout2.addWidget(self.backBtn)
        hboxLayout2.addWidget(self.playBtn)
        hboxLayout2.addWidget(self.forwardBtn)
        self.vboxLayout1.addLayout(hboxLayout2)
        self.vboxLayout1.addLayout(hboxLayout1)
        hboxLayout2.setAlignment(Qt.AlignHCenter)

        # create vbox layout
        carrier = QMenuBar()
        carrier.setFixedHeight(1)
        carrier.setStyleSheet("QMenuBar{ background: black; }")
        MenuBarLayout = QVBoxLayout()
        MenuBarLayout.addWidget(carrier)
        MenuBarLayout.addWidget(self.menuBar)
        MenuBarLayout.setSpacing(0)
        vboxLayout2 = QVBoxLayout()
        vboxLayout2.addLayout(MenuBarLayout)
        vboxLayout2.addWidget(container)
        vboxLayout2.addLayout(self.vboxLayout1)
        vboxLayout2.setAlignment(Qt.AlignHCenter)
        hboxLayout2.setContentsMargins(0, 0, 0, 12)
        hboxLayout2.setSpacing(7)
        self.setLayout(vboxLayout2)

        self.mediaPlayer.setVideoOutput(videowidget)

        # media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.setStyling()

    def mousePressEvent(self, a0: QMouseEvent):

        if self.fullscreenVar:
            if self.playBtn.isHidden():
                self.showControlBar()
            else:
                self.hideControlBar()

    def open_file(self):

        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.backBtn.setEnabled(True)
            self.playBtn.setEnabled(True)
            self.forwardBtn.setEnabled(True)
            self.play_video()

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playPauseAction.setText("Play")
        else:
            self.mediaPlayer.play()
            self.playPauseAction.setText("Pause")

    def turnOFFTheSubtitles(self):
        self.subTitlesOn = False

    def volumeIncrease(self):
        if self.mediaPlayer.volume() <= 90:
            self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
            self.volumeSlider.setSliderPosition(self.mediaPlayer.volume())
        elif self.mediaPlayer.volume() > 90 and self.mediaPlayer.volume() < 100:
            self.mediaPlayer.setVolume(100)
            self.volumeSlider.setSliderPosition(self.mediaPlayer.volume())

    def volumeDecrease(self):
        if self.mediaPlayer.volume() >= 10:
            self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)
            self.volumeSlider.setSliderPosition(self.mediaPlayer.volume())
        elif self.mediaPlayer.volume() < 10 and self.mediaPlayer.volume() > 0:
            self.mediaPlayer.setVolume(0)
            self.volumeSlider.setSliderPosition(self.mediaPlayer.volume())

    def volumeMute(self):

        if self.mediaPlayer.isMuted() == False:
            self.mediaPlayer.setMuted(True)
            self.volumeMuteAction.setText("Unmute")
        elif self.mediaPlayer.isMuted() == True:
            self.mediaPlayer.setMuted(False)
            self.volumeMuteAction.setText("Mute")

    def jumpForward10Sec(self):
        if self.mediaPlayer.position() + 10000 <= self.mediaPlayer.duration():
            self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000)
        elif self.mediaPlayer.position() < self.mediaPlayer.duration() and (self.mediaPlayer.position() + 10000 <= self.mediaPlayer.duration()) == False:
            self.mediaPlayer.setPosition(self.mediaPlayer.duration())

    def jumpBack10Sec(self):
        if self.mediaPlayer.position() - 10000 >= 0:
            self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000)
        elif self.mediaPlayer.position() > 0 and (self.mediaPlayer.position() - 10000 < 0):
            self.mediaPlayer.setPosition(0)

    def increasePlaybackRate(self):
        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate() + 1)

    def decreasePlaybackRate(self):
        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate() - 1)

    def resetPlayback(self):
        self.mediaPlayer.setPlaybackRate(1)

    def settingsSubtitles(self):
        self.settingsWindow = SubtitleSettings(self.subTiTlesLabel)

        if self.settingsWindow.exec_():
            if self.settingsWindow.acceptBtn:

                if self.settingsWindow.font != -1:
                    self.subTiTlesLabel.setFont(self.settingsWindow.font)
                if self.settingsWindow.textcolor != -1:
                    p = self.subTiTlesLabel.palette()
                    p.setColor(self.subTiTlesLabel.foregroundRole(), self.settingsWindow.textcolor)
                    self.subTiTlesLabel.setPalette(p)
                if self.settingsWindow.backgroundcolor != -1:
                    self.subTiTlesLabel.setStyleSheet("QLabel { background-color: %s }" % self.settingsWindow.backgroundcolor.name())

    def aboutInfoMessageBoxShow(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)

        self.msg.setText("About Info")
        self.msg.setInformativeText("This is a simple player application written in python using pyqt5 library. It's built on top of pyqt5 QMediaPlayer and QVideoPlayer. Its completely free for use, as far as monetary value goes. On the other hand you may be required to work in Albanian mines for a few months after some time.\nOther than that have fun enjoy :) I like your hair you cheeky cunt. It goes like wooooosh ~~~ wavy and curly and straight and idk bye.")
        self.msg.setWindowTitle("About Info Message")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()

    def videoNotPlayingMessageBoxShow(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setTextFormat(Qt.RichText)
        self.msg.setText("<a href='https://codecguide.com/download_kl.htm'>Video not playing what the fuck dude?</a>")
        self.msg.setInformativeText("Okay so, turns out you have to have codecs installed on your system in order to play some formats. Crazy, right? Maybe have that in your mind before you start the cussin' or ill come to your house cash u unprepared ya know. N' be like that cash me ousside houbo de girl. I won't put my unwashed hands on your face tho tahts a rumor.\nAnyways heres the link where you can download the latest codec pack:\nGet the codecs by clicking on the link in the title. \n\nEnjoy :)")
        self.msg.setWindowTitle("Video not playing, what the fuck?")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()

    def findSubtitlesOnline(self):
        self.window = SearchSubtitlesOnline()
        self.window.show()

    def changeAppearance(self):
        pass

    def setStyling(self):

        self.volumeSlider.setStyleSheet("""
        
                        QSlider{
                            max-height: 17px;
                        }
        
                        QSlider::groove:horizontal {
                                background: white;
                            }

                        QSlider::sub-page:horizontal {
                            background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
                            stop: 0 #FFC0CB, stop: 1 #FF69B4);
                        }

                        QSlider::add-page:horizontal {
                            background: #fff;
                        }

                        QSlider::handle:horizontal {
                            background: #FF1493;
                            border: 4px solid; 
                            border-color: #FF1493;
                            width: 7px;
                            margin-top: 0px;
                            margin-bottom: 0px;
                        }

                        QSlider::handle:horizontal:hover {
                	        border-radius: 4px;

                        }
        """)

        self.menuBar.setStyleSheet(
            "QMenuBar{ color: white; background-color: rgb(70, 70, 70); font-weight: bold; border: 1px solid; } QMenuBar::item:selected { background: #FFC0CB; }@")
        self.fileMenu.setStyleSheet(
            "QMenu{ background-color: #FF69B4; color: white; font-weight: bold; } QMenu::item:selected { background: #FFC0CB; }@")
        self.viewMenu.setStyleSheet(
            "QMenu{ background-color: #FF69B4; color: white; font-weight: bold; } QMenu::item:selected { background: #FFC0CB; }@")
        self.editMenu.setStyleSheet(
            "QMenu{ background-color: #FF69B4; color: white; font-weight: bold; } QMenu::item:selected { background: #FFC0CB; }@")
        self.helpMenu.setStyleSheet(
            "QMenu{ background-color: #FF69B4; color: white; font-weight: bold; } QMenu::item:selected { background: #FFC0CB; }@")

        self.playBtn.setStyleSheet("""QPushButton{ color: white; background-color: #FF69B4; border-style: outset;
                                                 padding: 3px;
                                                 font: bold 20px;
                                                 border-width: 3px;
                                                 border-radius: 21px;
                                                 min-width: 34px;
                                                 min-height: 34px;
                                                 border-color: #FF1493; }""")

        self.backBtn.setStyleSheet("""QPushButton{ color: white; background-color: #FF69B4; border-style: outset;
                                                 padding: 3px;
                                                 font: bold 20px;
                                                 border-width: 3px;
                                                 border-radius: 12px;
                                                 min-width: 21px;
                                                 min-height: 21px;
                                                 border-color: #FF1493; }""")

        self.forwardBtn.setStyleSheet("""QPushButton{ color: white; background-color: #FF69B4; border-style: outset;
                                                 padding: 3px;
                                                 font: bold 20px;
                                                 border-width: 3px;
                                                 border-radius: 12px;
                                                 min-width: 21px;
                                                 min-height: 21px;
                                                 border-color: #FF1493; }""")

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

    def hideControlBar(self):

        self.slider.hide()
        self.durationLabel.hide()
        self.volumeSlider.hide()
        self.volumeLabel.hide()
        self.backBtn.hide()
        self.playBtn.hide()
        self.forwardBtn.hide()
        self.menuBar.hide()

    def showControlBar(self):

        self.slider.show()
        self.durationLabel.show()
        self.volumeSlider.show()
        self.volumeLabel.show()
        self.backBtn.show()
        self.playBtn.show()
        self.forwardBtn.show()
        self.menuBar.show()

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

    @pyqtSlot('qint64')
    def jumpPosition(self, position):
        self.set_position(position)
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

    def resizeEvent(self, a0: QResizeEvent) -> None:
        movecoef = (self.width() - self.subTiTlesLabel.width()) / 2
        self.subTiTlesLabel.setGeometry(int(movecoef), self.height() - 200, self.subTiTlesLabel.width(),
                                        self.subTiTlesLabel.height())

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