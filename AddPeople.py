from PyQt5.Qt import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QDate

from lib.AddPeopleUI import Ui_AddPeople
from Message import Message

class AddPeople(Ui_AddPeople, QDialog):
    out = pyqtSignal(dict)
    def __init__(self, all_people_name):
        super(Ui_AddPeople, self).__init__()
        self.setupUi(self)

        self.all_people_name = all_people_name

        self.select_path = ''
        self.comboBox_reason.addItems(['无', '违法-吸毒', '违法-逃税', '违法-嫖娼', '违法-造假', '失德-出轨', '不当言行', '错误价值观', '贪污受贿'])
        pix = QPixmap('./data/imgs/add_people_image.png')
        self.label_image.setPixmap(pix)
        self.dateEdit_date.setDate(QDate.currentDate())

        self.pushButton_select.clicked.connect(self.add_people_select_image)
        self.pushButton_submit.clicked.connect(self.add_people_submit)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.label_title.setText('添加人员')
        self.pushButton_close.clicked.connect(self.close)
        self.label_4.setText('原因：')

        '''UI设置：'''
        self.setStyleSheet('''
            QDialog{border-image:url(./data/imgs/background.png);}
            #widget{background-color: rgba(255, 255, 255, 10%); }
            #pushButton_close{border-image:url(./data/imgs/close.png);}
            #pushButton_close:selected,#pushButton_close:hover{border-image:url(./data/imgs/close_s.png);}
            #widget_icon{border-image:url(./data/imgs/add_people_icon.png);}
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

        #self.setui('./ui_darkblue.qss')
        self.show()

    '''从本地选择照片传入库中'''
    def add_people_select_image(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self, "选取图片", './', "Image Files (*.jpg;*.png)")  # 设置文件扩展名过滤,用双分号间隔
        if not fileName_choose == '':
            print(fileName_choose)
            pix = QPixmap(fileName_choose).scaled(160, 200)
            self.label_image.setPixmap(pix)
            self.lineEdit_name.setText(fileName_choose.split('/')[-1].split('.')[0])
            self.select_path = fileName_choose


    def add_people_submit(self):
        content = {}
        content['path'] = self.select_path
        content['name'] = self.lineEdit_name.text()
        content['position'] = self.lineEdit_position.text()
        content['reason'] = self.comboBox_reason.currentText()
        content['date'] = self.dateEdit_date.text()
        if self.select_path == '':
            self.message_box = Message('请选择图片')
        elif content['name'] == '':
            self.message_box = Message('请输入姓名')
        elif content['name'] in self.all_people_name:
            self.message_box = Message('此人已在库内，请勿重复添加')
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