from PyQt5.QtWidgets import QSlider, QStyle, QStyleOptionSlider, QToolTip
from PyQt5.QtGui import QMouseEvent, QCursor, QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
import math

class SliderTimebar(QSlider):
    signal = pyqtSignal('qint64')

    def __init__(self, direction):
        super().__init__()

        self.setStyleSheet("""
                                    QSlider{ max-height: 17px; }
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
                                        border: 4px solid red;
                                        border-color: #FF1493;
                                        width: 10px;
                                        margin-top: 0px;
                                        margin-bottom: 0px;
                                    }
        
                                    QSlider::handle:horizontal:hover {
                                        border-radius: 4px;
        
                                    }
                
                                """)

        self.setMouseTracking(True)
        self.setOrientation(direction)

    def mousePressEvent(self, a0: QMouseEvent):
        super(SliderTimebar, self).mousePressEvent(a0)
        if a0.button() == Qt.LeftButton:
            val = self.pixelPosToRangeValue(a0.pos())
            self.setValue(val)
            self.signal.emit(val)

    def pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                                        sliderMax - sliderMin, opt.upsideDown)

    def mouseMoveEvent(self, a0: QMouseEvent):
        super(SliderTimebar, self).mouseMoveEvent(a0)
        val = self.pixelPosToRangeValue(a0.pos())
        point = QPoint(QCursor.pos().x(), self.pos().y() + 60)
        QToolTip.showText(point, self.getDurationString(val))
        QToolTip.setFont(QFont("Times New Roman", 12, 3))
        p = QPalette()
        p.setColor(QPalette.ToolTipText, QColor("#FF1493"))
        QToolTip.setPalette(p)

    def getDurationString(self, position):

        seconds = round(position / 1000)
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