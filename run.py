'''
修改时间：2021.3.26
'''
from PyQt5.Qt import QMainWindow, QMessageBox, QApplication, QIcon, QPixmap, QColor, QCursor
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QVBoxLayout, QTableWidgetItem, QPushButton, QHeaderView, QDialog, QFileDialog, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QSize, QUrl, QModelIndex

import sys
import json
import requests
import base64
import pymysql
import os
import paramiko
import configparser
import traceback

from mainwindow import Ui_MainWindow
from utils.tools import write_video, clear
from lib.VideoPlayPlate import VideoPlayer
from lib.VideoSegList import VideoSegList
from Message import Message
from AddPeople import AddPeople
from ModifyPeople import ModifyPeople
from AddVideo import AddVideo
from ModifyVideo import ModifyVideo
from AddTv import AddTv
from ModifyTv import ModifyTv

import threading
import inspect
import ctypes
import time

from apscheduler.schedulers.blocking import BlockingScheduler

#读取配置文件
conf = configparser.ConfigParser()
root_path = os.getcwd()
conf.read(root_path + '/config.conf', encoding='utf-8')  # 文件路径

'''
操作数据库所使用的类
包括数据查询和更新数据库两中方法
'''
class OperationMysql:
    def __init__(self):
        '''创建一个连接数据库的对象'''
        self.conn = pymysql.connect(
            host=conf.get('mysql', 'host'),            # 连接的数据库服务器主机名
            port=int(conf.get('mysql', 'port')),       # 数据库端口号
            user=conf.get('mysql', 'user'),            # 数据库登录用户名
            passwd=conf.get('mysql', 'passwd'),        # 数据库登录密码
            db=conf.get('mysql', 'db'),                # 数据库名称
            charset='utf8',                            # 连接编码
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.conn.cursor()                  # 使用cursor()方法创建一个游标对象，用于操作数据库

    '''查询一条数据'''
    def search_one(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()                   # 使用 fetchone()方法获取单条数据.只显示一行结果
        return result

    '''查询多条数据， 返回值为list，该项目中未使用该函数'''
    def search_all(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()   # 显示所有结果
        return result

    '''更新SQL'''
    def update_one(self, sql):
        try:
            self.cur.execute(sql)      # 执行sql
            self.conn.commit()         # 增删改操作完数据库后，需要执行提交操作
            print('操作成功')
        except:

            self.conn.rollback()       # 发生错误时回滚

'''
MainWindow：
mainwindow.ui中设计好界面，此处定义各种功能
共四个界面：视频检测、人员管理、视频管理、直播管理
'''

class mymainwindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        '''
        变量设置：
        live_url:服务器传来的视频流地址
        all_people_name:存储所有作为Key的人名信息
        current_mode:共有两种模式，本地视频(local)和直播流(living)
        thread_on:显示线程状态，是否开启
        max_people_id:最大的人像的id  用于添加人像时选择插入的id
        all_people_name:
        all_video_name:
        all_video_id:所有视频的id   11位的id
        max_tv_id:最大的tv id，用于添加tv时选择插入的id
        all_tv_name:所有tv的名称    为电视台频道名
        all_tv_id:所有视频的id   为直播流的url
        play_video_name:所播放的所有视频的name
        play_video_id:所播放的所有视频的id（local为11位的id，live为频道名称）
        play_video_url:所播放的所有视频的url
        current_play_video_num:当前播放的视频序号
        max_video_num:允许同时检测的最大视频数
        post_time_span:发送post请求的时间间隔，单位秒
        is_finished:判断当前视频是否检测完，完成检测则不发送post信息
        '''
        self.live_url = None
        self.selected_tv = None
        self.current_mode = None
        self.thread_on = False
        self.max_people_id = 0
        self.all_people_name = []
        self.all_video_name = []
        self.all_video_id = []
        self.max_tv_id = 0
        self.all_tv_name = []
        self.all_tv_id = []
        self.play_video_name = []
        self.play_video_id = []
        self.play_video_url = []
        self.play_video_length = []
        self.play_video_current_length = []
        self.play_video_start_time = []
        self.current_play_video_num = 0
        self.max_video_num = int(conf.get('other', 'max_video_num'))
        self.post_time_span = int(conf.get('other', 'post_time_span'))
        self.is_finished = []



        '''
        服务器链接配置文件：
        host_ip:服务器IP
        username:字面意思
        password:字面意思
        server_image_path:服务器中人脸图像所在位置
        local_image_path:人脸图需要保存到本机的位置
        '''
        self.host_ip = conf.get('server', 'host_ip')
        self.username = conf.get('server', 'username')
        self.password = conf.get('server', 'password')
        self.server_image_path = conf.get('server', 'server_image_path')
        self.server_video_path = conf.get('server', 'server_video_path')
        self.local_image_path = os.getcwd() + '\\data\\face\\'

        '''操作数据库'''
        self.op_mysql = OperationMysql()

        self.videoPlayer = VideoPlayer()  # 视频播放面板
        self.videoSegList = VideoSegList()  # 添加底部检索片段显示列表
        self.videoPlayer.playPuseBtn.setEnabled(False)  # 开始视频检测前，停止单个视频的按钮禁用

        self.gridLayout_play.addWidget(self.videoPlayer)
        self.verticalLayout.addWidget(self.videoSegList)

        '''添加底部状态局域栏显示    师兄的代码，感觉有部分多余的东西，有空再改'''
        self.bottomBar = QWidget()
        bottomLayout = QHBoxLayout(self.bottomBar, spacing=0)
        bottomLayout.setContentsMargins(5, 0, 0, 0)
        self.stateLabel = QLabel(objectName='state')
        bottomLayout.addWidget(self.stateLabel)
        self.stateLabel.setFixedSize(QSize(12, 12))

        tipLabel = QLabel('运行状态', objectName='tip')
        tipLabel.setMaximumSize(60, 15)
        tipLabel.setContentsMargins(10, 0, 0, 0)

        self.messageLabel = QLabel('错误', objectName='message')
        self.messageLabel.setContentsMargins(5, 0, 0, 0)
        bottomLayout.addWidget(tipLabel)
        bottomLayout.addWidget(self.messageLabel)
        self.verticalLayout.addWidget(self.bottomBar)



        '''连接信号槽。将各个按钮、信号与相应的功能连接'''
        self.pushButton_min.clicked.connect(self.window_min)
        self.pushButton_max.clicked.connect(self.window_max)
        self.pushButton_close.clicked.connect(self.window_close)

        self.videoSegList.videoUrl.connect(self.playSeg)                     # 检索界面下方视频片段框：触发播放检索小片段，右键点击下方弹出的小视频后可播放
        self.videoPlayer.segBtn.clicked.connect(self.hidSegList)             # 检索界面右下方信息按钮：触发隐藏/显示检索列表
        self.videoPlayer.playPuseBtn.clicked.connect(self.stop_one)          # 检索界面视频区域左下方停止按钮：用于停止当前播放视频的检测
        self.listWidget_play.itemClicked.connect(self.play_item_clicked)     # 检索界面播放左侧视频名称框：点击其中的Item后切换所播放视频
        self.pushButton_stop_all.clicked.connect(self.stop_all)              # 检索界面左下方全部停止按钮：点击后结束所有检测，关闭线程

        self.pushButton_people_search.clicked.connect(self.people_search)    # 人员管理界面搜索按钮：在列表中检索人物
        self.pushButton_people_add.clicked.connect(self.people_add)          # 人员管理界面添加按钮
        self.pushButton_video_search.clicked.connect(self.video_search)      # 视频管理界面搜索按钮
        self.pushButton_video_check.clicked.connect(self.video_check)        # 视频管理界面检测按钮
        self.pushButton_video_deselect.clicked.connect(self.video_deselect)  # 视频管理界面取消勾选按钮
        self.pushButton_video_add.clicked.connect(self.video_add)            # 视频管理界面添加按钮
        self.pushButton_tv_search.clicked.connect(self.tv_search)            # 直播管理界面搜索按钮
        self.pushButton_tv_check.clicked.connect(self.tv_check)              # 直播管理界面检测按钮
        self.pushButton_tv_deselect.clicked.connect(self.tv_deselect)        # 直播管理界面取消勾选按钮
        self.pushButton_tv_add.clicked.connect(self.tv_add)                  # 直播管理界面添加按钮

        self.stateChange(True, '正常')

        '''各个界面的初始化'''
        self.people_table_init()
        self.video_table_init()
        self.tv_table_init()

        '''UI设置：'''
        self.setui('./ui.qss')

        self.videoPlayer.setStyleSheet('''
        QPushButton{border-image:url(./data/imgs/touming.png);}
        ''')
        self.bottomBar.setStyleSheet('QLabel#state{background:green; border-radius: 6}')
        self.setWindowIcon(QIcon('./data/imgs/icon.png'))
        # self.setWindowTitle('视频检测工具')

        self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏顶部窗口

        '''开始检测前发送关闭全部检索信号，避免前一次开启时未关闭，同时检测与后台服务器是否连接成功'''
        json_data = {
            'mode': 'astop',
            'id': [''],
            'key_words': '',
            'video_mode': '',
            'video_name': [''],
            'video_address': ''
        }
        print(json_data)
        try:
            json_file = json.dumps(json_data)
            result = requests.post("http://" + self.host_ip + ":9999/vdfilter", json=json_file)
            print(result.content)
        except:
            self.message = Message('请检查后台服务是否开启')
            self.close()
            return

    '''-----------------------------------------------------------------主窗口管理------------------------------------------------------------------------------------------------'''
    def window_min(self):
        self.showMinimized()

    def window_max(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def window_close(self):
        self.close()

    '''-----------------------------------------------------------------人员管理界面-----------------------------------------------------------------------------------------------'''

    '''从服务器下载图片至本地'''
    def obtain_image(self):
        people_infor = self.op_mysql.search_all("SELECT distinct people_name  from people WHERE people_name != 'None'")   # 在数据库中检索所有人物的信息
        current_num = 0
        while current_num < len(people_infor):
            if not os.path.exists(os.getcwd() + '\\data\\face\\' + str(people_infor[current_num]["people_name"]).replace(' ','') + ".jpg") and not os.path.exists(os.getcwd() + '\\data\\face\\' + str(people_infor[current_num]["people_name"]).replace(' ','') + ".png"):
                self.download_from_server(people_infor[current_num]["people_name"].replace(' ',''))                       # 下载人物照片
            current_num += 1

    '''
    创建人脸图像的widget，用于嵌入表格中
    people_name：人物名称
    '''
    '''此处有个问题，图片格式不可强行转换，如将jpg格式的图片直接更改后缀为png则无法在qt中打开'''
    def people_image(self, people_name):
        widget = QWidget()
        imglabel = QLabel()  # Qlable用于装载图片，后将其嵌入widget中
        '''人像图片格式共有两种，png或者jpg，根据已有的照片自动选择'''
        if os.path.exists(os.getcwd() + '\\data\\face\\' + str(people_name) + ".jpg"):
            image = QPixmap(os.getcwd() + '\\data\\face\\' + str(people_name) + ".jpg").scaled(80, 100)
        elif os.path.exists(os.getcwd() + '\\data\\face\\' + str(people_name) + ".png"):
            image = QPixmap(os.getcwd() + '\\data\\face\\' + str(people_name) + ".png").scaled(80, 100)
        else:
            image = QPixmap(os.getcwd() + '\\data\\face\\face.png').scaled(80, 100)     # 若无此人照片，则使用定义好的图像代替
        imglabel.setPixmap(image)

        gLayout = QVBoxLayout()
        gLayout.addWidget(imglabel)
        gLayout.setContentsMargins(3, 3, 3, 3)
        widget.setLayout(gLayout)

        return widget

    '''
    人员列表内添加修改和删除按钮
    people_id：人物在数据库中对应的id
    people_name：人物姓名
    people_position：人物职务
    date：落马日期
    reason：落马原因
    '''
    def add_button_people(self, people_id, people_name, people_position, date, reason):
        widget = QWidget()

        modifyBtn = QPushButton('  修改  ')      # 修改
        modifyBtn.setMaximumSize(80, 30)
        modifyBtn.setMinimumSize(80, 30)
        deleteBtn = QPushButton('  删除  ')      # 删除
        deleteBtn.setMaximumSize(80, 30)
        deleteBtn.setMinimumSize(80, 30)

        modifyBtn.clicked.connect(lambda: self.modify_people(people_id, people_name, people_position, date, reason))    # 修改按钮链接self.modify_people函数
        deleteBtn.clicked.connect(lambda: self.delete_people(people_id))                                                # 删除按钮链接self.delete_people函数

        hLayout = QVBoxLayout()
        hLayout.addWidget(modifyBtn)
        hLayout.addWidget(deleteBtn)
        hLayout.setContentsMargins(1, 1, 1, 1)
        widget.setLayout(hLayout)
        widget.setAttribute(Qt.WA_TranslucentBackground)    # 设置widget背景透明
        return widget

    '''关联修改按钮，点击后弹出人员修改界面'''
    def modify_people(self, people_id, people_name, people_position, date, reason):
        self.people_modify_widget = ModifyPeople(people_id, people_name, people_position, date, reason)    #创建ModifyPeople窗口
        self.people_modify_widget.out.connect(self.modify_people_operation)           # out传输数据后，触发add_people_operation执行添加操作

    '''
    获取到返回值后，执行修改人员信息的操作
    处理逻辑为删除原有数据，传入新值，即便没有更改，也是进行这些操作
    此处为偷懒省去了判断图片是否更替
    content = {
        'old_name' : 修改前的人物名字
        'id' ： 人物id，修改信息不更改数据库中id
        'path' ： 新图像的路径
        'name' ： 更改后人物的名字
        'position'： 职务
        'reason' ： 落马原因
        'date' ： 落马日期
    }
    '''
    def modify_people_operation(self, content):
        # 更新数据库信息
        self.op_mysql.update_one("UPDATE people SET people_name = '%s', people_position = '%s', fall_time = '%s', fall_reason = '%s' WHERE id = %d"%(content['name'], content['position'], content['date'], content['reason'], int(content['id'])))

        command = 'rm -rf '+ self.server_image_path + content['old_name']   # 删掉服务器里原始的图片数据
        self.ssh_command(command)

        command = 'mkdir ' + self.server_image_path + content['name']        # 在服务器里创建新文件夹放新图片
        self.ssh_command(command)

        src = content['path']                                               # 新图片在本机上的地址
        des = self.server_image_path + content['name'] + '/' + content['name'] + '.' + src.split('.')[-1]   #新图像在服务器中的存储地址
        self.upload_to_server(src, des)                                     # 将新图片传入服务器


        try:
            os.remove('./data/face/' + content['old_name'] + '.jpg')        # 本地图像删除，有两种可能的格式jpg或png
        except:
            pass

        try:
            os.remove('./data/face/' + content['old_name'] + '.png')        # 本地图像删除，有两种可能的格式jpg或png
        except:
            pass

        self.people_table_init()# 刷新人员列表

    '''
    关联修改按钮，点击后删除对应人员信息
    people
    '''
    def delete_people(self, people_id):

        people_name = self.op_mysql.search_one("SELECT people_name from people WHERE id = '%d'" % int(people_id))['people_name']     # 根据id获取所选人物名字
        self.op_mysql.update_one("DELETE FROM people WHERE people_name = '%s'"%people_name)    # 数据库里删除记录

        try:
            os.remove('./data/face/' + people_name + '.jpg')        # 本地图像删除，有两种可能的格式jpg或png
        except:
            pass

        try:
            os.remove('./data/face/' + people_name + '.png')        # 本地图像删除，有两种可能的格式jpg或png
        except:
            pass

        command = 'rm -rf ' + self.server_image_path + people_name   # 服务器中图像删除
        self.ssh_command(command)

        self.people_table_init()                                    # 初始化人员界面

    '''链接添加按钮，点击后弹出人员添加界面'''
    def people_add(self):
        self.people_add_widget = AddPeople(self.all_people_name)       # 创建人员添加窗口
        self.people_add_widget.out.connect(self.add_people_operation)  # out传输数据后，触发add_people_operation执行添加操作

    '''
    获取到返回值后，执行添加人员信息的操作
    content = {
        'id' ： 人物id
        'path' ： 图像的路径
        'name' ： 人物名字
        'position'： 职务
        'reason' ： 落马原因
        'date' ： 落马日期
    }
    '''
    def add_people_operation(self, content):
        # 数据库中添加记录
        self.op_mysql.update_one("INSERT INTO people (id, people_name, people_position, fall_time, fall_reason) VALUES (%d, '%s', '%s', '%s','%s')"%(self.max_people_id + 1, content['name'], content['position'], content['date'], content['reason']))

        command = 'mkdir ' + self.server_image_path + content['name']
        self.ssh_command(command)              # 上传图片前在服务器中创建新文件夹

        src = content['path']
        des = self.server_image_path + content['name'] + '/' + content['name'] + '.' + src.split('.')[-1]
        self.upload_to_server(src, des)       # 将本地图片上传至数据库对应位置

        # 向后端发送最新的照片
        inquire_data = {'image_path': content['name'] + '/' + content['name'] + '.jpg'}
        print(inquire_data)
        print(inquire_data['image_path'])
        try:
            response = requests.post("http://" + self.host_ip + ":9999/addfeature", data=json.dumps(inquire_data))

            # 解析返回的信息
            output = json.loads(response.content)
            print(output)
        except:
            self.message_box = Message('请检查后台服务器')

        self.people_table_init()              # 初始化人员列表

    '''人员信息列表初始化'''
    def people_table_init(self):
        self.all_people_name.clear()          # 清空所有名字信息
        self.obtain_image()                   # 从服务器中获取人物图像

        people_infor = self.op_mysql.search_all("SELECT * from people WHERE people_name !='None'")     # 从数据库中获取人物信息
        self.tableWidget_people.clear()       # 清空列表
        self.tableWidget_people.setColumnCount(11)                                 # 设置表格列数
        self.tableWidget_people.setRowCount(int(len(people_infor) + 1) / 2)        # 根据检测到的人员数量设置行数，每行两个人

        self.tableWidget_people.setHorizontalHeaderLabels(
            ['照片', '姓名', '职务', '备注', '操作', '  ', '照片', '姓名', '职务', '备注', '操作'])      # 设置列表顶部信息

        people_num = 0
        while people_num < len(people_infor):
            self.tableWidget_people.setCellWidget(int(people_num / 2), 0, self.people_image(people_infor[people_num]['people_name']))      # 添加照片
            self.tableWidget_people.setItem(int(people_num / 2), 1, QTableWidgetItem(str(people_infor[people_num]['people_name'])))        # 添加人名
            self.tableWidget_people.item(int(people_num / 2), 1).setTextAlignment(Qt.AlignCenter)                                          # 设置人名显示位置居中
            self.tableWidget_people.setItem(int(people_num / 2), 2, QTableWidgetItem(str(people_infor[people_num]['people_position'])))    # 添加职务
            self.tableWidget_people.item(int(people_num / 2), 2).setTextAlignment(Qt.AlignCenter)                                          # 设置职务显示位置居中
            self.tableWidget_people.setItem(int(people_num / 2), 3, QTableWidgetItem(str(people_infor[people_num]['fall_reason'])))        # 添加落马原因
            self.tableWidget_people.item(int(people_num / 2), 3).setTextAlignment(Qt.AlignCenter)                                          # 设置落马原因显示位置居中
            self.tableWidget_people.setCellWidget(int(people_num / 2), 4, self.add_button_people(str(people_infor[people_num]['id']),
                                                                                                 str(people_infor[people_num]['people_name']),
                                                                                                 str(people_infor[people_num]['people_position']),
                                                                                                 str(people_infor[people_num]['fall_time']),
                                                                                                 str(people_infor[people_num]['fall_reason'])))  # 添加按钮

            self.all_people_name.append(str(people_infor[people_num]["people_name"]).replace(' ', ''))     # self.all_people_name所存姓名+1
            if int(people_infor[people_num]['id']) > self.max_people_id:     # 若检测到某人id号大于一直的最大id号，更新最大人员id
                self.max_people_id = int(people_infor[people_num]['id'])
            people_num += 1

            if people_num < len(people_infor) and str(people_infor[people_num]['people_name']) is not 'None':                                      # 最后一行的第二个人员信息的位置需判断
                self.tableWidget_people.setItem(int(people_num / 2), 5, QTableWidgetItem("   "))                                                   # 添加间隔
                self.tableWidget_people.setCellWidget(int(people_num / 2), 6, self.people_image(str(people_infor[people_num]['people_name'])))     # 添加照片
                self.tableWidget_people.setItem(int(people_num / 2), 7, QTableWidgetItem(str(people_infor[people_num]['people_name'])))            # 添加人名
                self.tableWidget_people.item(int(people_num / 2), 7).setTextAlignment(Qt.AlignCenter)                                              # 设置人名显示位置居中
                self.tableWidget_people.setItem(int(people_num / 2), 8, QTableWidgetItem(str(people_infor[people_num]['people_position'])))        # 添加职务
                self.tableWidget_people.item(int(people_num / 2), 8).setTextAlignment(Qt.AlignCenter)                                              # 设置职务显示位置居中
                self.tableWidget_people.setItem(int(people_num / 2), 9, QTableWidgetItem(str(people_infor[people_num]['fall_reason'])))            # 添加落马原因
                self.tableWidget_people.item(int(people_num / 2), 9).setTextAlignment(Qt.AlignCenter)                                              # 设置落马原因显示位置居中
                self.tableWidget_people.setCellWidget(int(people_num / 2), 10, self.add_button_people(str(people_infor[people_num]['id']),
                                                                                                      str(people_infor[people_num]['people_name']),
                                                                                                      str(people_infor[people_num]['people_position']),
                                                                                                      str(people_infor[people_num]['fall_time']),
                                                                                                      str(people_infor[people_num]['fall_reason'])))# 添加按钮

                self.all_people_name.append(str(people_infor[people_num]["people_name"]).replace(' ', ''))   # self.all_people_name所存姓名+1
                if int(people_infor[people_num]['id']) > self.max_people_id:     # 若检测到某人id号大于一直的最大id号，更新最大人员id
                    self.max_people_id = int(people_infor[people_num]['id'])

            self.tableWidget_people.setRowHeight(int(people_num / 2), 106)       # 设置列表改行高度
            people_num += 1

        self.tableWidget_people.verticalHeader().setVisible(False)               # 设置列表不展示左侧的序号信息
        self.tableWidget_people.horizontalHeader().setVisible(True)              # 设置列表展示顶部信息

        self.tableWidget_people.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)               # 设置顶部信息大小自适应
        self.tableWidget_people.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)   # 设置第0列宽度自适应
        self.tableWidget_people.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)   # 设置第4列宽度自适应
        self.tableWidget_people.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)   # 设置第6列宽度自适应
        self.tableWidget_people.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeToContents)  # 设置第10列宽度自适应

        self.tableWidget_people.resizeColumnsToContents()                        # 设置列宽高按照内容自适应

        self.tableWidget_people.hide()    #刷新界面，先隐藏后展示，实现刷新，操作比较呆滞，暂无更好方案，能用即可
        self.tableWidget_people.show()

    '''人员检索'''
    def people_search(self):
        text = self.lineEdit_people.text()              # 获取self.lineEdit_people里输入的值
        if text == '':
            self.message_box = Message('请输入关键字')    # 没有输入管检词则弹出提示
        else:
            s = [s for s in self.all_people_name if text in s]    # 从名字进行检索
            if len(s) == 0:
                self.message_box = Message('未找到相关内容')         # 未检测到弹窗提示
            else:
                item = self.tableWidget_people.findItems(s[0], Qt.MatchExactly)       # 获取对应名字的item
                row = item[0].row()                                                   # 获取item的行数
                self.tableWidget_people.verticalScrollBar().setSliderPosition(row)    # table转跳至对应行

    '''--------------------------------------------------------------视频管理界面----------------------------------------------------------------------------------'''

    '''
    视频列表内添加按钮
    video_id：视频的id，一串字符串
    video_name：视频名称
    '''
    def button_video(self, video_id, video_name):
        widget = QWidget()

        modifyBtn = QPushButton('     修改     ')
        modifyBtn.clicked.connect(lambda: self.modify_video(video_id, video_name, self.all_video_id))  # 修改按钮链接self.modify_video函数
        modifyBtn.setMaximumSize(80, 30)
        modifyBtn.setMinimumSize(80, 30)

        deleteBtn = QPushButton('     删除     ')
        deleteBtn.clicked.connect(lambda: self.delete_video(video_id))                                 # 修改按钮链接self.delete_video函数
        deleteBtn.setMaximumSize(80, 30)
        deleteBtn.setMinimumSize(80, 30)

        hLayout = QHBoxLayout()
        hLayout.addWidget(modifyBtn)
        hLayout.addWidget(deleteBtn)
        hLayout.setContentsMargins(1, 1, 1, 1)
        widget.setLayout(hLayout)
        widget.setAttribute(Qt.WA_TranslucentBackground)  #设置widget背景透明
        return widget

    '''
    链接修改按钮，点击后弹出人员修改界面
    video_id：视频的id
    video_name：视频的名称
    all_video_id ： 所有视频的名称,若修改id，则用于判断新id是否重复
    '''
    def modify_video(self, video_id, video_name, all_video_id):
        self.video_modify_widget = ModifyVideo(video_id, video_name, all_video_id)         # 创建ModifyVideo，弹出修改窗口
        self.video_modify_widget.out.connect(self.modify_video_operation)                  # out传输数据后，触发add_people_operation执行添加操作

    '''
    获取到返回值后，执行修改视频信息的操作
    处理逻辑为删除原有数据，传入新值，即便没有更改，也是进行这些操作
    content = {
        'old_id' : 视频修改前的id
        'path' ： 新视频的路径
        'name' ： 新视频的名字
        'id' ： 新视频的id
    }
    '''
    def modify_video_operation(self, content):
        if content['id'] == content['old_id']:         # 若id未修改，则更新对应数据，否则删除原来的记录再插入新的
            self.op_mysql.update_one("UPDATE movie SET video_name = '%s' WHERE id = '%s'" % (content['name'], content['id']))
        else:
            self.op_mysql.update_one("DELETE FROM movie WHERE id = '%s'" % content['old_id'])
            self.op_mysql.update_one("INSERT INTO movie (id, url, video_name) VALUES ('%s', NULL, '%s')" % (str(content['id']), str(content['name'])))

        if content['path'] != '':       # 若更新了视频，则删除原来的，并传入新视频
            command = 'rm -r ' + self.server_video_path + content['old_id'] + '.mp4'
            self.ssh_command(command)

            src = content['path']
            des = self.server_video_path + content['id'] + '.mp4'
            self.upload_to_server(src, des)
        else:
            command = 'os.rename(' + self.server_video_path + content['old_id'] +  '.mp4,' + self.server_video_path + content['id'] + '.mp4)'
            self.ssh_command()

        self.video_table_init()

    '''链接删除按钮，点击后删除对应视频'''
    def delete_video(self, video_id):
        self.op_mysql.update_one("DELETE FROM movie WHERE url = '%s'"%video_id)     #删除数据库中的记录

        command = 'rm -r ' + self.server_video_path + video_id + '.mp4'
        self.ssh_command(command)          # 服务器中图像删除

        self.video_table_init()            # 初始化人员界面


    '''链接添加按钮，点击后弹出视频添加界面'''
    def video_add(self):
        self.video_add_widget = AddVideo(self.all_video_id)          # 创建AddVideo，弹出视频添加窗口
        self.video_add_widget.out.connect(self.add_video_operation)  # out传输数据后，触发add_people_operation执行添加操作

    '''
        获取到返回值后，执行添加视频信息的操作
        content = {
           'path' ： 视频的路径
           'name' ： 视频的名字
           'id' ： 视频的id
    '''
    def add_video_operation(self, content):

        self.op_mysql.update_one("INSERT INTO movie (url, video_name) VALUES ('%s', '%s')" % (str(content['id']), str(content['name'])))    # 向数据库中写入记录

        src = content['path']
        des = self.server_video_path + content['id'] + '.mp4'
        self.upload_to_server(src, des)         # 向服务器传输视频

        self.video_table_init()

    '''视频列表初始化'''
    def video_table_init(self):
        self.tableWidget_video.clear()
        video_infor = self.op_mysql.search_all("SELECT *  from movie")                       # 从数据库中读取所有的视频信息
        self.tableWidget_video.setColumnCount(4)                                             # 视频列表共有5列
        self.tableWidget_video.setRowCount(len(video_infor))                                 # 根据视频数设置行数
        self.tableWidget_video.setHorizontalHeaderLabels([' ', '序号', '名称', '操作'])
        row_number = 0
        self.all_video_name = []
        self.all_video_id = []

        while row_number < len(video_infor):
            self.check = QTableWidgetItem()                                                  # 创建checkbox，置于第1列
            self.check.setCheckState(Qt.Unchecked)
            self.tableWidget_video.setItem(row_number, 0, self.check)
            self.tableWidget_video.setItem(row_number, 1,
                                           QTableWidgetItem(str(video_infor[row_number]['id'])))    # 第2列显示序号
            self.all_video_id.append(str(video_infor[row_number]['url']))                            # 所有视频id+1
            self.tableWidget_video.setItem(row_number, 2, QTableWidgetItem(
                str(video_infor[row_number]['video_name'])))                                        # 第2列显示视频名称
            self.all_video_name.append(str(video_infor[row_number]['video_name']))                  # 所有视频名称+1
            self.tableWidget_video.setCellWidget(row_number, 3,
                                                 self.button_video(str(video_infor[row_number]['url']), str(
                                                     video_infor[row_number]['video_name'])))       # 添加按钮
            row_number += 1

        self.tableWidget_video.verticalHeader().setVisible(False)        # 不显示左侧序号的label
        self.tableWidget_video.horizontalHeader().setVisible(True)       # 显示顶部各列属性的label

        # 设置宽度自适应
        self.tableWidget_video.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_video.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget_video.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget_video.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.tableWidget_video.verticalHeader().setDefaultSectionSize(34)   # 设置顶部label的高度

        self.tableWidget_video.hide()        #刷新界面，先隐藏后展示，实现刷新，操作比较呆滞，暂无更好方案，能用即可
        self.tableWidget_video.show()

    '''链接搜索按钮，在视频列表中检索所查视频'''
    def video_search(self):
        text = self.lineEdit_video.text()            # 获取self.lineEdit_video中输入的信息
        if text == '':
            self.message_box = Message('请输入关键字') # 若无输入则弹窗提示
        else:
            s = [s for s in self.all_video_name if text in s]
            if len(s) == 0:
                self.message_box = Message('未找到相关内容')
            else:
                item = self.tableWidget_video.findItems(s[0], Qt.MatchExactly)
                row = item[0].row()
                self.tableWidget_video.verticalScrollBar().setSliderPosition(row)

    '''
    关联检测按钮，根据checkbox所选的行确定需要检测视频，发起检测后开启线程，定时向后台发送post信息，获取检测到的视频
    '''
    def video_check(self):
        selected_rows = []                          # 用于存储选中的行号
        for row in range(len(self.all_video_id)):
            if self.tableWidget_video.item(row, 0).checkState() == 2:
                selected_rows.append(row)           # 若某行的checkbox被选中，则对应行数存入selected_rows中
        if len(selected_rows) < 1:
            self.message_box = Message('请选择视频')  # 未选择就点击了检测则弹窗提示
            return
        if len(selected_rows) + len(self.play_video_name) > self.max_video_num:
            self.message_box = Message('同时检测的视频数不能超过'+ str(self.max_video_num) + '条')    # 若已开始检测视频数加上所选的数量超过了最大数量，则弹窗提示
            return

        select_video_name = []              # 用于记录所选中的视频名称
        select_video_id = []                # 用于记录所选择的视频id
        for i in selected_rows:
            if self.all_video_name[i] in self.play_video_name:
                self.message_box = Message('请确认所选视频，勿重复发起请求')    # 若所选视频已经开始检测则弹窗提示
                return

            self.listitem = QListWidgetItem(self.all_video_name[i])    # 创建视频检测页面中，list里的item，显示视频的名称
            self.play_video_name.append(self.all_video_name[i])        # 所检测的视频名称+1
            self.play_video_id.append(self.all_video_id[i])            # 所检测的视频id+1
            self.listWidget_play.addItem(self.listitem)                # self.listitem嵌入self.listWidget_play中
            self.is_finished.append(False)                             # 所检测视频是否完成+1
            select_video_name.append(self.all_video_id[i] + '.mp4')    # 所选视频名称，服务器中所存储的视频，是以id号来命名的，故在此视频名用id+'.mp4'
            # select_video_name.append(self.all_video_id[i])  # 所选视频名称，服务器中所存储的视频，是以id号来命名的，故在此视频名用id+'.mp4'
            select_video_id.append(self.all_video_id[i])               # 所选视频的id+1

        infoContent = {"mode": 'new',
                       "id": select_video_id,
                       "key_words": self.all_people_name,
                       "video_mode": 'local',
                       "video_name": select_video_name,
                       "video_address": ''
                       }
        print(infoContent)

        try:
            response = requests.post("http://" + self.host_ip + ":9999/vdfilter", data=json.dumps(infoContent))

            output = json.loads(response.content)      # 解析服务器返回的信息
            print(output)
            for id in select_video_id:
                self.play_video_length.append(int(output['all_frame'][id]))    #获取每个视频的时长，单位秒
                self.play_video_current_length.append(0)
                self.play_video_start_time.append(0)
        except:
            self.message_box = Message('请检查后台服务是否开启')
            if not self.thread_on:
                self.data_reset()
                self.listWidget_play.clear()
            return

        i = 0
        while i < len(select_video_id):
            self.play_video_url.append(output['Live-address'][len(output['Live-address']) - len(select_video_id) + i])          # 将返回信息中，推流端的地址接收
            i += 1




        print(self.play_video_length)

        print(self.play_video_url)

        '''若第一次点击开始检测，则开启新线程，若已开启线程，之前已发送过开启检测信号，也更新了self.play_video_name和self.play_video_id'''
        if not self.thread_on:
            self.video_threading = threading.Thread(
                target=lambda: self.start_check_video())  # 新线程关联start_check_video函数
            self.video_threading.start()                  # 开启线程
            self.thread_on = True                         # 用于判断线程是否已经开启

            self.current_play_video_num = 0               # 当前播放的视频序号为list里的第0个

            self.videoPlayer.playVideo(self.play_video_url[0])     # 播放第一个视频
            #self.videoPlayer.player.play()
            self.videoPlayer.playPuseBtn.setEnabled(True) # 开始检索后，停止按钮开启

            ## 定时3秒
            # self.timer = QTimer()
            # self.timer.start(1000)
            # self.timer.timeout.connect(self.update_time)

            self.play_video_start_time[0] = int(time.time())
            
        self.tabWidget.setCurrentIndex(0)                 # 转跳倒视频检测界面

    '''链接取消选择按钮，点击后checkbox全部清空'''
    def video_deselect(self):
        for row in range(len(self.all_video_id)):
            self.tableWidget_video.item(row, 0).setCheckState(Qt.Unchecked)

    '''-------------------------------------------------------直播管理界面-------------------------------------------------------------------------'''

    '''直播列表内添加按钮'''
    def add_button_tv(self,tv_id, tv_name, tv_url):
        widget = QWidget()

        modifyBtn = QPushButton('     修改     ')
        modifyBtn.clicked.connect(lambda: self.modify_tv(tv_id, tv_name, tv_url))    # 修改按钮链接self.modify_tv函数
        modifyBtn.setMaximumSize(80, 30)
        modifyBtn.setMinimumSize(80, 30)

        deleteBtn = QPushButton('     删除     ')
        deleteBtn.clicked.connect(lambda: self.delete_tv(tv_name))                   # 修改按钮链接self.delete_tv
        deleteBtn.setMaximumSize(80, 30)
        deleteBtn.setMinimumSize(80, 30)

        hLayout = QHBoxLayout()
        hLayout.addWidget(modifyBtn)
        hLayout.addWidget(deleteBtn)
        hLayout.setContentsMargins(1, 1, 1, 1)
        widget.setLayout(hLayout)
        widget.setAttribute(Qt.WA_TranslucentBackground)                              # 设置widget背景透明
        return widget

    '''链接修改按钮，点击后弹出修改直播流窗口'''
    def modify_tv(self, tv_id, tv_name, tv_url):
        self.tv_modify_widget = ModifyTv(tv_id, tv_name, tv_url)
        self.tv_modify_widget.out.connect(self.modify_tv_operation)  # out传输数据后，触发add_people_operation执行添加操作

    '''
    获取到返回值后，执行修改直播流信息的操作,只需修改数据库里的内容
    '''
    def modify_tv_operation(self, content):
        # 更新数据库信息
        print(content)
        self.op_mysql.update_one(
            "UPDATE tv SET tv_name = '%s', tv_url = '%s' WHERE id = %d" % (content['name'], content['url'], int(content['id'])))
        self.tv_table_init()

    def delete_tv(self, tv_name):
        self.op_mysql.update_one("DELETE FROM tv WHERE tv_name = '%s'" % tv_name)

        # 初始化直播界面
        self.tv_table_init()

    '''弹出视频添加界面'''

    def tv_add(self):
        self.tv_add_widget = AddTv(self.all_tv_name)
        self.tv_add_widget.out.connect(self.add_tv_operation)  # out传输数据后，触发add_people_operation执行添加操作

    '''获取到返回值后，执行添加视频信息的操作'''

    def add_tv_operation(self, content):
        print(content)
        self.op_mysql.update_one(
            "INSERT INTO tv (id, tv_name, tv_url, tv_icon_path) VALUES (%d, '%s', '%s', NULL)" % (self.max_tv_id + 1, content['name'], content['url']))

        self.tv_table_init()

    '''视频列表初始化'''
    def tv_table_init(self):
        self.tableWidget_tv.clear()
        tv_infor = self.op_mysql.search_all("SELECT *  from tv")
        self.tableWidget_tv.setColumnCount(5)
        self.tableWidget_tv.setRowCount(len(tv_infor))
        self.tableWidget_tv.setHorizontalHeaderLabels([' ', '序号', '名称', 'url', '操作'])
        row_number = 0

        self.all_tv_name = []
        self.all_tv_id = []


        while row_number < len(tv_infor):
            self.check = QTableWidgetItem()
            self.check.setCheckState(Qt.Unchecked)
            self.tableWidget_tv.setItem(row_number, 0, self.check)
            self.tableWidget_tv.setItem(row_number, 1, QTableWidgetItem(str(tv_infor[row_number]['id'])))
            self.tableWidget_tv.setItem(row_number, 2,
                                           QTableWidgetItem(str(tv_infor[row_number]['tv_name'])))
            self.all_tv_name.append(str(tv_infor[row_number]['tv_name']))
            self.tableWidget_tv.setItem(row_number, 3, QTableWidgetItem(
                str(tv_infor[row_number]['tv_url'])))
            self.all_tv_id.append(str(tv_infor[row_number]['tv_url']))
            self.tableWidget_tv.setCellWidget(row_number, 4,
                                                 self.add_button_tv(str(tv_infor[row_number]['id']), str(tv_infor[row_number]['tv_name']), str(tv_infor[row_number]['tv_url'])))  # 添加按钮
            if int(tv_infor[row_number]['id']) > self.max_tv_id:
                self.max_tv_id = int(tv_infor[row_number]['id'])
            row_number += 1
        # 显示顶部各列属性的label，不显示左侧序号的label
        self.tableWidget_tv.verticalHeader().setVisible(False)
        self.tableWidget_tv.horizontalHeader().setVisible(True)

        # 设置宽度自适应
        self.tableWidget_tv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_tv.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget_tv.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget_tv.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableWidget_tv.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        #self.tableWidget_tv.resizeColumnsToContents()  # 设置列宽高按照内容自适应
        self.tableWidget_tv.verticalHeader().setDefaultSectionSize(34)

        # 刷新界面
        self.tableWidget_tv.hide()
        self.tableWidget_tv.show()

    '''在视频列表中检索所查视频'''

    def tv_search(self):
        text = self.lineEdit_tv.text()
        if text == '':
            self.message_box = Message('请输入关键字')
        else:
            s = [s for s in self.all_tv_name if text in s]
            if len(s) == 0:
                self.message_box = Message('未找到相关内容')
            else:
                item = self.tableWidget_tv.findItems(s[0], Qt.MatchExactly)
                row = item[0].row()
                self.tableWidget_tv.verticalScrollBar().setSliderPosition(row)

    def tv_check(self):
        selected_rows = []
        for row in range(len(self.all_tv_id)):
            if self.tableWidget_tv.item(row, 0).checkState() == 2:
                selected_rows.append(row)
        if len(selected_rows) < 1:
            self.message_box = Message('请选择频道')
            return
        if len(selected_rows) + len(self.play_video_url) > self.max_video_num:
            self.message_box = Message('同时检测的视频数不能超过5个')
            return

        select_tv_id = []
        select_tv_address = []
        for i in selected_rows:
            if self.all_tv_name[i] in self.play_video_name:
                self.message_box = Message('请确认所选视频，勿重复发起请求')
                return
            # self.listitem = QListWidgetItem(self.all_video_id[i])
            self.listitem = QListWidgetItem(self.all_tv_name[i])
            #self.listitem.setIcon
            self.play_video_name.append(self.all_tv_name[i])
            self.play_video_id.append(self.all_tv_id[i])
            self.listWidget_play.addItem(self.listitem)
            self.is_finished.append(False)
            select_tv_id.append(self.all_tv_name[i])
            select_tv_address.append(self.all_tv_id[i])

        print(select_tv_id)
        print(select_tv_address)

        infoContent = {"mode": 'new',
                       "id": select_tv_id,
                       "key_words": self.all_people_name,
                       "video_mode": 'live',
                       "video_name": '',
                       "video_address": select_tv_address
                       }

        print(json.dumps(infoContent))

        response = requests.post("http://" + self.host_ip + ":9999/vdfilter", data=json.dumps(infoContent))

        # 解析返回的信息
        output = json.loads(response.content)

        for i in select_tv_address:
            self.play_video_url.append(i)

        '''若第一次点击开始检测，则开启新线程'''
        if not self.thread_on:
            # 创建新线程
            self.video_threading = threading.Thread(
                target=lambda: self.start_check_video())  # 新线程关联start_check_video函数
            self.video_threading.start()
            self.thread_on = True

            self.current_play_video_num = 0

            # self.videoPlayer.init_player()

            print(self.play_video_url)
            print(self.play_video_url[0])

            self.videoPlayer.playVideo(self.play_video_url[0])
            self.videoPlayer.player.play()
            self.videoPlayer.playPuseBtn.setEnabled(True)  # 开始检索后，停止按钮开启

        self.tabWidget.setCurrentIndex(0)

        self.current_mode = 'live'


    def tv_deselect(self):
        for row in range(len(self.all_tv_id)):
            self.tableWidget_tv.item(row, 0).setCheckState(Qt.Unchecked)

    '''-------------------------------------------------------------其他设置------------------------------------------------------------------'''

    '''
    设置线程内的定时器，每间隔self.post_time_span的时间，向后台发送mode为post的请求
    '''
    def start_check_video(self):
        self.sched = BlockingScheduler()

        self.sched.add_job(lambda: self.post_for_chip(), 'interval', seconds=self.post_time_span)
        self.sched.start()
        self.stateChange(True, '当前视频检测中')

    def post_for_chip(self):
        if False in self.is_finished:
            """请求片段，id必须是list并且和video_name等长"""

            i = 0
            post_id = []
            post_name = []
            while i < len(self.is_finished):
                if not self.is_finished[i]:
                    post_id.append(self.play_video_id[i])
                    post_name.append(self.play_video_name[i])
                i += 1



            json_data = {"mode": 'post',
                           "id": post_id,
                           "key_words": [],
                           "video_mode": '',
                           "video_name": '',
                           "video_address": ''
                           }

            print('当前检测视频数量',len(self.play_video_name))
            print('当前检测视频序号',self.current_play_video_num)
            if not self.play_video_name[self.current_play_video_num] in self.all_tv_name:
                json_data['video_mode'] = 'local'
                json_data['video_name'] = post_name
            else:
                json_data['id'] = [self.play_video_name[self.current_play_video_num]]
                json_data['video_mode'] = 'live'
            print(json_data)
            json_file = json.dumps(json_data)
            try:
                result_json = requests.post("http://" + self.host_ip + ":9999/vdfilter", json=json_file)
                result = json.loads(result_json.content)
                print(result)
            except:
                self.message_box = Message('请检查后台服务是否开启')
                self.stop_all()
                return
            if result['message'] == 'New chips!':
                chip_ids = result['chips'].keys()
                for chip_id in chip_ids:
                    if result['chips'][chip_id][0] == 'Finished':
                        self.is_finished[self.play_video_id.index(chip_id)] = True
                        continue
                    self.listWidget_play.item(self.play_video_id.index(chip_id)).setBackground(QColor('red'))
                    time.sleep(2)

                    self.play_video_current_length[self.current_play_video_num] += 1

                    for chip_path in result['chips'][chip_id]:
                        thumbnail = write_video(chip_path, self.all_people_name)
                        if self.play_video_id[self.current_play_video_num] in chip_id:
                            self.videoSegList.makeSegList(thumbnail, self.all_people_name)

                        self.stateChange(True, '有新的片段被检索出')


            if not False in self.is_finished:
                self.stateChange(True, '所有视频检测完成')

    '''UI界面设置'''
    def setui(self,uipath):
        with open(uipath, 'r', encoding='utf-8') as f1:
            qssStyle = f1.read()
            self.setStyleSheet(qssStyle)



    '''从服务器获取文件到本地'''
    def download_from_server(self, people_name):
        t = paramiko.Transport((self.host_ip, 22))
        t.connect(username=self.username, password=self.password)  # 登录远程服务器
        sftp = paramiko.SFTPClient.from_transport(t)  # sftp传输协议
        try:
            src = self.server_image_path + people_name + '/' + sftp.listdir(self.server_image_path + people_name)[0]
            des = self.local_image_path + people_name + '.' +sftp.listdir(self.server_image_path + people_name)[0].split('.')[-1]
            sftp.get(src, des)
        except Exception as e:
            print(e.args)
            print('----------')
            print(traceback.format_exc())
            print("error:", people_name)
            pass
        t.close()

    '''上传数据至服务器'''
    def upload_to_server(self, src, des):
        t = paramiko.Transport((self.host_ip, 22))
        t.connect(username=self.username, password=self.password)  # 登录远程服务器
        sftp = paramiko.SFTPClient.from_transport(t)  # sftp传输协议
        try:
            sftp.put(src, des)
        except:
            print("error:", src)
            pass
        t.close()

    '''服务器执行命令行操作'''
    def ssh_command(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host_ip, port=22, username=self.username, password=self.password)
        stdin, stdout, stderr = ssh.exec_command(command=command, get_pty=True)
        stdin.close()
        stderr.read()
        ssh.close()

    '''关闭界面时清理临时文件'''
    def closeEvent(self, e):
        self.close()
        clear()

    '''检索列表隐藏与显示'''
    def hidSegList(self):
        if self.videoSegList.isHidden():
            self.videoSegList.show()
        else:
            self.videoSegList.hide()

    '''底部信息提示'''
    def stateChange(self, state, content):
        if isinstance(content, str):
            self.messageLabel.setText(content)
        else:
            message = base64.b64decode((content['message'].encode('utf-8'))).decode('utf-8')
            self.messageLabel.setText(message)
            state = False if content['status'] == 'Failed' else True
        color = 'green' if state else 'red'
        self.stateLabel.setStyleSheet("QLabel#state {background: %s}" % color)

    '''播放检索的小片段'''
    def playSeg(self, content):
        print('视频地址：', content)
        self.videoPlayer.playSegment(content)

    '''threading未提供停止线程的方法，以下两个函数用于杀死线程'''
    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):

        json_data = {
            'mode': 'astop',
            'id': [''],
            'key_words': '',
            'video_mode': '',
            'video_name': [''],
            'video_address': ''
        }
        print(json_data)
        json_file = json.dumps(json_data)
        result = requests.post("http://" + self.host_ip + ":9999/vdfilter", json=json_file)
        print(result.content)
        self._async_raise(thread.ident, SystemExit)

    def play_item_clicked(self, item):
        # 点击非当前正在播放的视频才执行
        if not self.current_play_video_num == self.play_video_name.index(item.text()):
            print(self.play_video_name.index(item.text()))
            self.current_play_video_num = self.play_video_name.index(item.text())

            for _ in range(self.videoSegList.list_chip.count()):
                self.videoSegList.list_chip.takeItem(0)
            for _ in range(self.videoSegList.list_text.count()):
                self.videoSegList.list_text.takeItem(0)

            self.videoPlayer.playVideo(self.play_video_url[self.play_video_name.index(item.text())])
            print(self.play_video_url)
            print(self.play_video_url[self.play_video_name.index(item.text())])
            try:
                self.videoSegList.switch_video(self.play_video_id[self.play_video_name.index(item.text())], self.all_people_name)
            except:
                print('当前未接收到任何chip')
            # self.stateChange(True, '当前视频检测中')

    '''发送停止检索的信号'''
    def stop_one(self):
        if len(self.play_video_name) == 1:
            self.stop_all()
            return
        self.listWidget_play.takeItem(self.current_play_video_num)

        #发送停止指令
        json_data = {
            'mode': 'stop',
            'id': [self.play_video_id[self.current_play_video_num]],
            'key_words': '',
            'video_mode': '',
            'video_name': [self.play_video_name[self.current_play_video_num]],
            'video_address': ''
        }
        print(json_data)
        json_file = json.dumps(json_data)
        result = requests.post("http://" + self.host_ip + ":9999/vdfilter", json=json_file)
        print(result.content)

        del self.play_video_name[self.current_play_video_num]
        del self.play_video_id[self.current_play_video_num]
        del self.play_video_url[self.current_play_video_num]
        del self.is_finished[self.current_play_video_num]

        for _ in range(self.videoSegList.list_chip.count()):
            self.videoSegList.list_chip.takeItem(0)
        for _ in range(self.videoSegList.list_text.count()):
            self.videoSegList.list_text.takeItem(0)

        if self.current_play_video_num == len(self.play_video_name):
            self.current_play_video_num -= 1
        self.videoPlayer.playVideo(self.play_video_url[self.current_play_video_num])
        try:
            self.videoSegList.switch_video(self.play_video_id[self.current_play_video_num])
        except:
            print('当前未接收到任何chip')

    def stop_all(self):
        if self.thread_on == True:
            self.videoPlayer.player.stop()
            self.listWidget_play.clear()
            try:
                self.stop_thread(self.video_threading)
                print('线程成功停止')
            except:
                pass
            json_data = {
                'mode': 'astop',
                'id': [''],
                'key_words': '',
                'video_mode': '',
                'video_name': [''],
                'video_address': ''
            }
            print(json_data)
            json_file = json.dumps(json_data)
            result = requests.post("http://" + self.host_ip + ":9999/vdfilter", json=json_file)
            print(result.content)

            self.videoPlayer.init_player()
            self.data_reset()
            clear()
            for _ in range(self.videoSegList.list_chip.count()):
                self.videoSegList.list_chip.takeItem(0)
            for _ in range(self.videoSegList.list_text.count()):
                self.videoSegList.list_text.takeItem(0)
            self.stateChange(True, '系统运行正常')
        else:
            self.message = Message('当前无检测任务')

    def second_to_time(self, second):
        m, s = divmod(second, 60)
        return("%02d:%02d" % (m, s))

    def update_time(self):
        print(self.videoPlayer.player.state())
        self.play_video_current_length[self.current_play_video_num] = int(time.time()) - self.play_video_start_time[self.current_play_video_num]
        self.videoPlayer.label_time.setText('%s' % self.second_to_time(self.play_video_current_length[self.current_play_video_num]))

        if self.play_video_length[self.current_play_video_num] <= self.play_video_current_length[self.current_play_video_num]:
            self.timer.stop()
            self.videoPlayer.label_time.setText('00:00')

            self.videoPlayer.player.stop()
            print(self.videoPlayer.player.state())
            self.videoPlayer.init_player()
            print(self.videoPlayer.player.state())


    def data_reset(self):
        self.current_mode = ''
        self.thread_on = False
        self.play_video_name = []
        self.play_video_url = []
        self.play_video_id = []
        self.play_video_current_length = []
        self.play_video_length = []
        self.is_finished = []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mymainwindow()
    mainwindow.show()
    sys.exit(app.exec_())