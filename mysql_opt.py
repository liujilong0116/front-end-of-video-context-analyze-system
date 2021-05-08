import pymysql
import os

class OperationMysql:
    def __init__(self):
        '''创建一个连接数据库的对象'''
        self.conn = pymysql.connect(
            host='114.213.209.9',            # 连接的数据库服务器主机名
            port=3306,       # 数据库端口号
            user='root',            # 数据库登录用户名
            passwd='123456',        # 数据库登录密码
            db='video_filter',                # 数据库名称
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
    order = "INSERT INTO movie (url, video_name) VALUES ('a', 'a')"
    mysql.update_one(order)
    # files = os.listdir(os.getcwd())
    # num = 1
    # print(files)
    # for i in files:
    #     if 'mp4' in i:
    #         order = "INSERT INTO movie (id, url, video_name) VALUES (%d, '%s', '%s')"%(num, i, i.replace('.mp4', ''))
    #         mysql.update_one(order)
    #         num += 1
