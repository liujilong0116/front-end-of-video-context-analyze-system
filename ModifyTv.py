from PyQt5.Qt import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QDate

from lib.AddTvUI import Ui_AddTv
from Message import Message

class ModifyTv(Ui_AddTv, QDialog):
    out = pyqtSignal(dict)
    def __init__(self, tv_id, tv_name, tv_url):
        super(Ui_AddTv, self).__init__()
        self.setupUi(self)
        self.tv_id = tv_id
        self.tv_name = tv_name
        self.tv_url = tv_url
        print(self.tv_id, self.tv_name, self.tv_url)
        self.lineEdit_name.setText(self.tv_name)
        self.lineEdit_url.setText(self.tv_url)
        self.pushButton_submit.clicked.connect(self.modify_tv_submit)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.label_title.setText('修改直播流')
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
        print('all is ok')

    def modify_tv_submit(self):
        content = {}
        content['id'] = self.tv_id
        content['name'] = self.lineEdit_name.text()
        content['url'] = self.lineEdit_url.text()
        if content['name'] == '':
            self.message_box = Message('请输入直播源名称')
        elif content['url'] == '':
            self.message_box = Message('请输入直播源url')
        else:
            self.out.emit(content)
            print('传递成功')
            self.close()

    def setui(self,uipath):
        with open(uipath, 'r', encoding='utf-8') as f1:
            qssStyle = f1.read()
            self.setStyleSheet(qssStyle)