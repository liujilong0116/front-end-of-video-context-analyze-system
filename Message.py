from lib.MessageUI import Ui_Message
from PyQt5.Qt import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

'''消息提示弹窗'''
class Message(Ui_Message, QDialog):
    def __init__(self, text):
        super(Ui_Message, self).__init__()
        self.setupUi(self)

        self.pushButton_confirm.clicked.connect(self.close)
        self.label.setText(text)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.pushButton_close.clicked.connect(self.close)

        self.label_title.setText('提示')
        '''UI设置：'''
        self.setStyleSheet('''
            QDialog{border-image:url(./data/imgs/background.png);}
            #widget{background-color: rgba(255, 255, 255, 10%); }
            #pushButton_close{border-image:url(./data/imgs/close.png);}
            #pushButton_close:selected,#pushButton_close:hover{border-image:url(./data/imgs/close_s.png);}
            #widget_icon{border-image:url(./data/imgs/message.png);}
            QPushButton{
                border-image:url(./data/imgs/button.png);
            }
            
            QPushButton:selected,QPushButton:hover{
                border-image:url(./data/imgs/button_s.png);
            }
            
            QLabel, QPushButton, QTabBar, QTableWidget, QListWidget, QLineEdit{
                color:#E7ECF0;
            }
        ''')
        self.setui('./ui_darkblue.qss')
        self.show()

    def setui(self, uipath):
        with open(uipath, 'r', encoding='utf-8') as f1:
            qssStyle = f1.read()
            self.setStyleSheet(qssStyle)