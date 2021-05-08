
# -*- coding: utf-8 -*-
import os
import time

import pymysql
import os

class OperationMysql:
    def __init__(self):
        '''创建一个连接数据库的对象'''
        self.conn = pymysql.connect(
            host='svrproject.tpddns.net',            # 连接的数据库服务器主机名
            port=3306,       # 数据库端口号
            user='root',            # 数据库登录用户名
            passwd='568884899..',        # 数据库登录密码
            db='projectdata',                # 数据库名称
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

if __name__ == '__main__':
    mysql = OperationMysql()
    all_name = mysql.search_all("SELECT video_name FROM movie")
    print(all_name)
    #设定文件路径
    path = os.getcwd()
    #对目录下的文件进行遍历
    for file in os.listdir(path):
        #判断是否是文件
        if 'mp4' in file:
            #设置新文件名
            new_name = str(int(time.time())) + '.mp4'
            #重命名
            os.rename(os.path.join(path,file),os.path.join(path,new_name))
            order = "INSERT INTO movie (url, video_name) VALUES ('%s', '%s')"%(new_name.replace('.mp4', ''), file.replace('.mp4', ''))
            mysql.update_one(order)
            time.sleep(1)

