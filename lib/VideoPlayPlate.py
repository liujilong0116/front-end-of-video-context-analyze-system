import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QHBoxLayout, QVBoxLayout, QStyle
from PyQt5.QtWidgets import QPushButton, QSlider, QSizePolicy, QSpacerItem, QLabel
from PyQt5.QtWidgets import QStyleOptionSlider
from PyQt5.QtCore import Qt, QUrl, QSize, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtGui
import qtawesome
import time

from utils.tools import check_info

'''重写滑块。音量控制'''
class ClickJumpSlider(QSlider):
    def mousePressEvent(self, event):
        # 获取上面的拉动块位置
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
        if rect.contains(event.pos()):
            # 如果鼠标点击的位置在滑块上则交给Qt自行处理
            super(ClickJumpSlider, self).mousePressEvent(event)
            return
        if self.orientation() == Qt.Horizontal:
            # 横向，要考虑invertedAppearance是否反向显示的问题
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                event.x() if not self.invertedAppearance() else (self.width(
                ) - event.x()), self.width()))
        else:
            # 纵向
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                (self.height() - event.y()) if not self.invertedAppearance(
                ) else event.y(), self.height()))

'''子播放窗口，提供给小片段播放'''
class subPlayer(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, title='检索播放'):
        super(subPlayer, self).__init__()
        self.setWindowTitle(title)
        layout = QHBoxLayout(self)
        self.player = QMediaPlayer()
        playerWindow = QVideoWidget()
        self.player.setVideoOutput(playerWindow)
        layout.addWidget(playerWindow)


    def playVideo(self, url, info=None):
        self.player.setMedia(QMediaContent(QUrl(url)))
        self.player.play()

    '''关闭时，清除小窗口(销毁)'''
    def closeEvent(self, e):
        self.player.stop()
        self.player.deleteLater()
        self.close_signal.emit()
        self.close()

class VideoPlayer(QWidget):

    def __init__(self):
        super(VideoPlayer, self).__init__()
        self.setUi()
        self.setSize()
        self._style()
        self.init_player()

        self.volume_switch = True
        volume = self.player.volume()
        self.volume = volume*0.5
        self.volumSlider.setRange(0, volume)
        self.volumSlider.setValue(0.5*volume)

        # 信号槽连接
        #self.playPuseBtn.clicked.connect(self.puse)
        self.volumBtn.clicked.connect(self.mute)
        self.volumSlider.valueChanged.connect(self.setVolume)





    '''初始播放窗口显示画面/更换播放内容'''
    def init_player(self, video=None):
        if video is None:
            #self.player.r
            #self.player.BufferedMedia
            #self.player.setMedia(QMediaContent(QUrl.fromLocalFile(r'./data/imgs/bg.gif')))


            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(r'./data/imgs/bg.gif')))
            self.player.play()
        else:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video)))
        self.player.play()

    '''初始化'''
    def setUi(self):

        self.mainLayout = QVBoxLayout(self, spacing=0)          # 设置为垂直分布
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # 添加视频播放窗口
        self.player = QMediaPlayer()
        playerWidget = QVideoWidget()
        playerWidget.setUpdatesEnabled(False)

        #playerWidget.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)


        #playerWidget.setAspectRatioMode(Qt.IgnoreAspectRatio)

        playerWidget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.player.setVideoOutput(playerWidget)
        self.mainLayout.addWidget(playerWidget)

        # 添加视频控制栏(音量，检索列表显示与隐藏按钮，进度条以及暂停因需求关系删除)
        self.bottomBar = QWidget()
        bottomLayout = QHBoxLayout(self.bottomBar)
        bottomLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.bottomBar)

        # 播放/暂停按钮，不使用
        self.playPuseBtn = QPushButton(qtawesome.icon('fa.stop', color='white', font=18), "")

        #self.playPuseBtn.setEnabled(False)
        bottomLayout.addWidget(self.playPuseBtn)

        # 填充空白
        bottomLayout.addSpacerItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Fixed))

        # self.label_time = QLabel('00:00')
        # bottomLayout.addWidget(self.label_time)

        # 音量控制
        self.volumBtn = QPushButton(qtawesome.icon('fa.volume-up', color='white', font=25), "")
        bottomLayout.addWidget(self.volumBtn)
        self.volumSlider = ClickJumpSlider(Qt.Horizontal)
        bottomLayout.addWidget(self.volumSlider)

        # 检索列表显示与隐藏按钮
        self.segBtn = QPushButton('信息')
        bottomLayout.addWidget(self.segBtn)

    '''样式设置'''
    def _style(self):
        self.volumSlider.setStyleSheet('''
            QSlider::groove:horizontal {  
                    background: rgba(255, 255, 255, 10%); height: 5px; 
                    border-radius: 2.5px; padding-left:-1px; padding-right:-1px;}
            QSlider::sub-page:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #B1B1B1, stop:1 #c4c4c4);
                    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #5DCCFF, stop: 1 #1874CD);
                    height: 10px;border-radius: 2px;}
            QSlider::add-page:horizontal { 
                    background:rgba(255, 255, 255, 10%); border: none; height: 10px; border-radius: 2px;}
            QSlider::handle:horizontal {
                    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,stop:0.6 #45ADED, 
                    stop:0.778409 rgba(255, 255, 255, 255));
                    width: 11px; margin-top: -3px; margin-bottom: -3px; border-radius: 5px;}
            QSlider::handle:horizontal:hover {
                    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 #2A8BDA,
                    stop:0.778409 rgba(255, 255, 255, 255));
                    width: 11px;margin-top: -3px;margin-bottom: -3px;border-radius: 5px;}
            QSlider::sub-page:horizontal:disabled {
                    background: #00009C;}
            QSlider::add-page:horizontal:disabled {
                    background: rgba(255, 255, 255, 10%);}
            QSlider::handle:horizontal:disabled {
                    background: #eee; border: 1px solid #aaa;border-radius: 4px;}
        ''')
        self.segBtn.setStyleSheet('''
            QPushButton {color: white}
        ''')



    '''大小设置'''
    def setSize(self):
        self.bottomBar.setMinimumHeight(25)
        self.bottomBar.setMaximumHeight(25)
        self.volumSlider.setMaximumWidth(100)

    '''播放视频'''
    def playVideo(self, url):
        self.subPlayer = subPlayer()
        self.subPlayer.playVideo(url)

        time.sleep(1)
        self.player.setMedia(QMediaContent(QUrl(url)))
        self.player.play()
        self.subPlayer.player.stop()

    '''播放/停止(已停止使用)'''
    def puse(self):
        if self.player.state() == 1:
            self.playPuseBtn.setIcon(qtawesome.icon('fa.pause', color='white', font=18))
            self.player.pause()
        elif self.player.state() == 2:
            self.playPuseBtn.setIcon(qtawesome.icon('fa.play', color='white', font=18))
            self.player.play()
        else:
            pass

    '''静音设置'''
    def mute(self):
        if self.volume_switch:
            self.volumBtn.setIcon(qtawesome.icon('fa.volume-off', color='white', font=25))
            self.volume = self.player.volume()
            self.player.setVolume(0)
            self.volumSlider.setValue(0)
            self.volume_switch = False
        else:
            self.volumBtn.setIcon(qtawesome.icon('fa.volume-up', color='white', font=25))
            self.player.setVolume(self.volume)
            self.volumSlider.setValue(self.volume)
            self.volume_switch = True

    '''音量设置'''
    def setVolume(self, volume):
        self.player.setVolume(volume)
        if volume == 0:
            self.volumBtn.setIcon(qtawesome.icon('fa.volume-off', color='white', font=25))
            self.volume_switch = False
        else:
            self.volumBtn.setIcon(qtawesome.icon('fa.volume-up', color='white', font=25))
            self.volume_switch = True

    '''播放检索小片段'''
    def playSegment(self, video_name):
        self.mute()
        self.subPlayer = subPlayer()
        self.subPlayer.resize(QSize(500, 400))
        #info = check_info(video_name, file_path='./tmp/video_info.json')
        url = './tmp/video_chips/' + video_name + '.mp4'
        self.subPlayer.playVideo(url)
        self.subPlayer.show()
        self.subPlayer.close_signal.connect(self.mute)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = VideoPlayer()
    gui.resize(QSize(500, 300))
    gui.playVideo('http://ivi.bupt.edu.cn/hls/cctv2.m3u8')
    gui.show()
    sys.exit(app.exec_())