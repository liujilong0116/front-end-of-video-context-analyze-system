##### 片段显示列表面板 #####

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QListView, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QSize, Qt
import os

class VideoSegList(QWidget):

    videoUrl = pyqtSignal(str)                  # 信号。需要播放小片段时，发送小片段本地地址

    def __init__(self):
        super(VideoSegList, self).__init__()
        self.setUi()
        self.setSize()
        self._style()
        #self.hide()
        self.list_chip.setViewMode(QListView.IconMode)
        self.list_chip.setIconSize(QSize(90, 90))

    '''初始化'''
    def setUi(self):

        self.mainLayout = QVBoxLayout(self, spacing=0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.topWidget = QWidget()
        topLayout = QHBoxLayout(self.topWidget)
        topLayout.setContentsMargins(0, 0, 0, 5)
        self.topLabel_text = QLabel(" 检测结果")
        self.topLabel_chip = QLabel(" 视频片段")

        topLayout.addWidget(self.topLabel_text)
        topLayout.addWidget(self.topLabel_chip)
        self.mainLayout.addWidget(self.topWidget)

        self.list_Widget = QWidget()
        hbox = QHBoxLayout(self.list_Widget)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.list_text = QListWidget()
        self.list_chip = QListWidget()
        hbox.addWidget(self.list_text)
        hbox.addWidget(self.list_chip)
        self.mainLayout.addWidget(self.list_Widget)


    '''设置大小'''
    def setSize(self):
        #self.setMinimumHeight(130)
        self.setMaximumHeight(130)
        self.topWidget.setMaximumHeight(25)
        self.topWidget.setMinimumHeight(25)
        self.list_text.setMaximumHeight(100)
        self.list_text.setMinimumHeight(100)
        self.list_chip.setMaximumHeight(100)
        self.list_chip.setMinimumHeight(100)

    '''设置样式'''
    def _style(self):
        self.topWidget.setStyleSheet('''
            QWidget {background: rgba(255, 255, 255, 0%)}
            QLabel {background: rgba(255, 255, 255, 10%); color: white;font-size:12px;font-family:宋体;}
        ''')
        self.list_text.setStyleSheet('''
            border:none;
            color: white;
            background: rgba(255, 255, 255, 10%);
            QListWidget::Item:hover {background: rgba(255, 255, 255, 10%)}
            QListWidget::Item:selected {background: rgba(255, 255, 255, 22%)}
        ''')
        self.list_chip.setStyleSheet('''
                    border:none;
                    color: white;
                    background: rgba(255, 255, 255, 10%);
                    QListWidget::Item:hover {background: rgba(255, 255, 255, 10%)}
                    QListWidget::Item:selected {background: rgba(255, 255, 255, 22%)}
                ''')

    '''将检索出的小片段，显示在列表上'''
    # def makeSegList(self, thumbnail, info):
    #     pic_path, name = thumbnail
    #
    #     self.list.setViewMode(QListView.IconMode)
    #     self.list.setIconSize(QSize(90, 90))
    #
    #     item = QListWidgetItem(self.list)
    #     item.setIcon(QIcon(pic_path))
    #     item.setText(name)
    #
    #     if info['Chip-way'] == 'Sub':
    #         way = '关键词检测'
    #     else:
    #         way = '人脸检测'
    #     content = '检索方式：' + way + '\n'
    #     content += '检索信息：' + info['Chip-keyfeature']
    #     item.setToolTip(content)

    # def makeSegList(self, thumbnail):
    #     pic_path, name = thumbnail
    #
    #     self.list.setViewMode(QListView.IconMode)
    #     self.list.setIconSize(QSize(90, 90))
    #
    #     item = QListWidgetItem(self.list)
    #     item.setIcon(QIcon(pic_path))
    #     item.setText(name)

    def makeSegList(self, thumbnail, all_people_name):
        pic_path, name = thumbnail

        print(pic_path)

        file_name = pic_path.split('/')[-1].replace('.jpg', '')
        info = file_name.split('#')
        if info[0]=='audio':
            mode = '音频'
        else:
            mode = '视频'
        start_time = info[1].replace('-', ':')
        end_time = info[2].replace('-', ':')
        people_name = all_people_name[int(info[3])]

        item_text = QListWidgetItem(self.list_text)

        item_text.setText('[%s-%s] 检测到%s中存在目标人物：%s' % (start_time, end_time, mode, people_name))

        item_chip = QListWidgetItem(self.list_chip)
        item_chip.setIcon(QIcon(pic_path))
        item_chip.setText(mode + '-' + people_name)
        item_chip.setWhatsThis(file_name)





    '''切换所检测视频时，将另一个视频中，已检测到的片段加入list'''
    def switch_video(self, video_name, all_people_name):
        video_files = os.listdir('./tmp/video_chips')
        print(video_files)
        if len(video_files) == 0:
            return
        video_in_list = []
        for i in range(self.list_chip.count()):
            video_in_list.append(self.list_chip.item(i).text())
        for video_chip in video_files:
            if video_name in video_chip and not video_chip in video_in_list:
                pic_path = './tmp/video_thumbnail/' + video_chip.replace('.mp4', '') + '.jpg'

                file_name = video_chip.replace('.mp4', '')
                info = file_name.split('#')
                if info[0] == 'audio':
                    mode = '音频'
                else:
                    mode = '视频'
                start_time = info[1].replace('-', ':')
                end_time = info[2].replace('-', ':')
                people_name = all_people_name[int(info[3])]

                item_text = QListWidgetItem(self.list_text)
                item_text.setText('[%s-%s] 检测到%s中存在目标人物：%s' % (start_time, end_time, mode, people_name))

                item_chip = QListWidgetItem(self.list_chip)
                item_chip.setIcon(QIcon(pic_path))
                item_chip.setText(mode + '-' + people_name)
                item_chip.setWhatsThis(file_name)






    '''设置右键菜单功能'''
    def contextMenuEvent(self, event):
        hitItem = self.list_chip.currentItem()
        if hitItem:
            itemMenu = QMenu(self)
            playAct = QAction('播放', self.list_chip)
            itemMenu.addAction(playAct)
            playAct.triggered.connect(self.playVideo)

            itemMenu.popup(self.mapToGlobal(event.pos()))

            itemMenu.setStyleSheet('''
                QMenu {background-color: rgba(255, 255, 255, 10%); 
                color: white; font-size:13px;font-family:Times New Roman;}
                QMenu::item:selected {background-color: black}
            ''')

    '''需要播放小片段时，返回播放地址'''
    def playVideo(self):
        hitItem = self.list_chip.currentItem()
        video_name = hitItem.whatsThis()
        self.videoUrl.emit(video_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = VideoSegList()
    gui.resize(QSize(500, 300))
    gui.show()
    sys.exit(app.exec_())