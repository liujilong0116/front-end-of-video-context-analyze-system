from PyQt5.Qt import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QDate

from lib.AddVideoUI import Ui_AddVideo
from Message import Message

class ModifyVideo(Ui_AddVideo, QDialog):
    out = pyqtSignal(dict)
    # video_id 此处为视频编号，根据文件名修改时间自动生成的
    def __init__(self, video_id, video_name, all_video_id):
        super(Ui_AddVideo, self).__init__()
        self.setupUi(self)
        self.old_video_id = video_id
        self.all_video_id = all_video_id
        self.video_id = video_id
        self.video_name = video_name
        self.select_path = ''
        pix = QPixmap('./data/imgs/got_video.png')
        self.label_image.setPixmap(pix)
        self.lineEdit_name.setText(self.video_name)
        self.lineEdit_id.setText(self.video_id)
        print(all_video_id)

        self.pushButton_select.clicked.connect(self.modify_video_select_v)
        self.pushButton_submit.clicked.connect(self.modify_video_submit)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.label_title.setText('修改视频信息')
        self.pushButton_close.clicked.connect(self.close)

        '''UI设置：'''
        self.setStyleSheet('''
            QDialog{border-image:url(./data/imgs/background.png);}
            #widget{background-color: rgba(255, 255, 255, 10%); }
            #pushButton_close{border-image:url(./data/imgs/close.png);}
            #pushButton_close:selected,#pushButton_close:hover{border-image:url(./data/imgs/close_s.png);}
            #widget_icon{border-image:url(./data/imgs/add_video_icon.png);}
            QPushButton{
                border-image:url(./data/imgs/button.png);
            }
            QComboBox, QDateEdit,QLineEdit{
                border-image:url(./data/imgs/bar_us.png);
            }

            QPushButton:selected,QPushButton:hover{
                border-image:url(./data/imgs/button_s.png);
            }


            QLabel, QPushButton, QTabBar, QTableWidget, QListWidget, QLineEdit, QDateEdit, QComboBox{
                color:#E7ECF0;
            }
        ''')
        self.show()

    '''从本地选择视频传入库中'''
    def modify_video_select_v(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self, "选取视频", './', "Image Files (*.mp4;*.MP4)")  # 设置文件扩展名过滤,用双分号间隔
        if not fileName_choose == '':
            pix = QPixmap('./data/imgs/update_video.png')
            self.label_image.setPixmap(pix)
            self.lineEdit_name.setText(fileName_choose.split('/')[-1].split('.')[0])
            self.select_path = fileName_choose


    def modify_video_submit(self):
        content = {}
        content['old_id'] = self.old_video_id
        content['path'] = self.select_path
        content['name'] = self.lineEdit_name.text()
        content['id'] = self.lineEdit_id.text()
        if content['name'] == '':
            self.message_box = Message('请输入视频名称')
        elif content['id'] == '':
            self.message_box = Message('请输入视频ID')
        elif content['id'] in self.all_video_id and content['id'] != self.old_video_id:
            self.message_box = Message('此视频ID已在库内，请更换ID')
        else:
            self.out.emit(content)
            print('传递成功')
            self.close()

    def setui(self,uipath):
        with open(uipath, 'r', encoding='utf-8') as f1:
            qssStyle = f1.read()
            self.setStyleSheet(qssStyle)