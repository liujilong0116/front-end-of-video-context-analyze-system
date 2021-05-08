from PyQt5.Qt import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QDate

from lib.ModifyPeopleUI import Ui_ModifyPeople
from Message import Message

import os

class ModifyPeople(Ui_ModifyPeople, QDialog):
    out = pyqtSignal(dict)       # qt信号槽，用于传递信息
    def __init__(self, people_id, people_name, people_position, date, reason):
        super(Ui_ModifyPeople, self).__init__()
        self.setupUi(self)
        self.old_people_name = people_name
        self.people_id = people_id
        self.people_name = people_name
        self.people_position = people_position
        self.date = date
        self.reason = reason

        self.all_reasons = ['无', '违法-吸毒', '违法-逃税', '违法-嫖娼', '违法-造假', '失德-出轨', '不当言行', '错误价值观', '贪污受贿']

        if os.path.exists('./data/face/' + self.people_name + '.jpg'):
            self.select_path = './data/face/' + self.people_name + '.jpg'
        elif os.path.exists('./data/face/' + self.people_name + '.png'):
            self.select_path = './data/face/' + self.people_name + '.png'
        else:
            self.select_path = './data/face/face.png'
        self.comboBox_reason.addItems(self.all_reasons)
        pix = QPixmap(self.select_path).scaled(160, 200)
        self.label_image.setPixmap(pix)
        self.lineEdit_name.setText(self.people_name)
        self.lineEdit_position.setText(self.people_position)
        if not self.date == 'None':
            year = int(self.date.split('/')[0])
            month = int(self.date.split('/')[1])
            day = int(self.date.split('/')[2])
            self.dateEdit_date.setDate(QDate(year, month, day))
        else:
            self.dateEdit_date.setDate(QDate.currentDate())


        self.comboBox_reason.setCurrentIndex(self.all_reasons.index(self.reason))
        #self.comboBox_reason.setCurrentIndex(0) #临时修改代码
        self.label_3.setText('备注：')

        self.pushButton_select.clicked.connect(self.add_people_select_image)
        self.pushButton_submit.clicked.connect(self.add_people_submit)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.label_title.setText('修改信息')
        self.pushButton_close.clicked.connect(self.close)

        '''UI设置：'''
        self.setStyleSheet('''
            QDialog{border-image:url(./data/imgs/background.png);}
            #widget{background-color: rgba(255, 255, 255, 10%); }
            #pushButton_close{border-image:url(./data/imgs/close.png);}
            #pushButton_close:selected,#pushButton_close:hover{border-image:url(./data/imgs/close_s.png);}
            #widget_icon{border-image:url(./data/imgs/modify.png);}
            QPushButton{
                border-image:url(./data/imgs/button.png);
            }
            QComboBox, QDateEdit,QLineEdit{
                border-image:url(./data/imgs/bar_us.png);
            }

            QPushButton:selected,QPushButton:hover{
                border-image:url(./data/imgs/button_s.png);
            }
            QDateEdit::up-button{
                border-image:url(./data/imgs/date_up.png);
            }
            QDateEdit::up-button:pressed{
                border-image:url(./data/imgs/date_up_s.png);
            }
            QDateEdit::down-button{
                border-image:url(./data/imgs/date_down.png);
            }
            QDateEdit::down-button:pressed{
                border-image:url(./data/imgs/date_down_s.png);
            }
            
            QComboBox::down-arrow{
                image:url(./data/imgs/date_down.png);
                width:19px;
                height:19px;
                right:2px;
            }
            
            QComboBox::drop-down{
                subcontrol-origin:padding;
                subcontrol-position:top right;
                width:15px;
                border-left-width:0px;
                border-left-style:solid;
                border-top-right-radius:3px;
                border-bottom-right-radius:3px;
                border-left-color:#738393;
            }
            
            QComboBox::drop-down:on{
                image:url(./data/imgs/date_down_s.png);
                
            }
            

            QLabel, QPushButton, QTabBar, QTableWidget, QListWidget, QLineEdit, QDateEdit, QComboBox{
                color:#E7ECF0;
            }
        ''')
        self.setui('./ui_darkblue.qss')
        self.show()

    '''从本地选择照片传入库中'''
    def add_people_select_image(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self, "选取图片", './', "Image Files (*.jpg;*.png)")  # 设置文件扩展名过滤,用双分号间隔
        if not fileName_choose == '':
            pix = QPixmap(fileName_choose).scaled(160, 200)
            self.label_image.setPixmap(pix)
            self.lineEdit_name.setText(fileName_choose.split('/')[-1].split('.')[0])
            self.select_path = fileName_choose


    def add_people_submit(self):
        content = {}
        content['old_name'] = self.old_people_name
        content['id'] = self.people_id
        content['path'] = self.select_path
        content['name'] = self.lineEdit_name.text()
        content['position'] = self.lineEdit_position.text()
        content['reason'] = self.comboBox_reason.currentText()
        content['date'] = self.dateEdit_date.text()
        if content['name'] == '':
            self.message_box = Message('请输入姓名')
        elif content['position'] == '':
            self.message_box = Message('请输入职位')
        else:
            self.out.emit(content)
            print('传递成功')
            self.close()

    def setui(self,uipath):
        with open(uipath, 'r', encoding='utf-8') as f1:
            qssStyle = f1.read()
            self.setStyleSheet(qssStyle)