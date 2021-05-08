import json
import os
import shutil
import cv2
import paramiko
import traceback
import configparser



def write_video(chip_path, all_people_name):
    # 读取配置文件
    conf = configparser.ConfigParser()
    root_path = os.getcwd()
    conf.read(root_path + '/config.conf', encoding='utf-8')  # 文件路径

    host_ip = conf.get('server', 'host_ip')
    username = conf.get('server', 'username')
    password = conf.get('server', 'password')
    path = './tmp/video_chips/'

    if not os.path.exists(path):
        os.makedirs(path)
    print('chip_path:------------------', chip_path)

    t = paramiko.Transport((host_ip, 22))
    t.connect(username=username, password=password)  # 登录远程服务器
    sftp = paramiko.SFTPClient.from_transport(t)  # sftp传输协议
    people_name = chip_path.split('#')[3]
    print('people_name:-----------------', people_name)
    chip_name = chip_path.split('/')[-1]
    print('chip_name:-------------------', chip_name)
    des = ''
    try:
        src = chip_path
        des = path + chip_name.replace(people_name, str(all_people_name.index(people_name)))
        print('服务器--------------------',src)
        print('本地----------------------',des)
        sftp.get(src, des)
    except Exception as e:
        print(e.args)
        print('----------')
        print(traceback.format_exc())
        print("error:", chip_path.split('/')[-1])
        pass
    t.close()
    return make_thumbnail(des, des.split('/')[-1])

def make_thumbnail(video_path, video_name):
	# 选取视频某一帧为封面
    if not os.path.exists('./tmp/video_thumbnail'):
        os.mkdir('./tmp/video_thumbnail')
    pic_name = video_name.split('.')[0]
    thumbnail_path = './tmp/video_thumbnail/' + pic_name + '.jpg'
    print(video_path)
    print(video_name)

    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()

    params = []
    params.append(cv2.IMWRITE_PXM_BINARY)
    params.append(1)

    success, frame = cap.read()
    cv2.imwrite(thumbnail_path, frame, params)
    cap.release()


    print('图片保存成功')
    return thumbnail_path, pic_name

def write_info(info):
    # 载入已保存的信息
    file_path = './tmp/video_info.json'

    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.close()
        infom_readed = {}
    else:
        with open(file_path, 'r', encoding='utf-8') as json_f:
                infom_readed = json.load(json_f)

    # 追加新信息
    key = info["Chip-name"].split('.')[0]
    infom_readed[key] = info

    # 将信息重新覆盖写入
    with open(file_path, 'w', encoding='utf-8') as f_obj:
        json.dump(infom_readed, f_obj, ensure_ascii=False, indent=4)

def check_info(key, file_path):

    with open(file_path, 'r', encoding='utf-8') as json_f:
        infom_readed = json.load(json_f)

    for id in infom_readed.keys():
        if id == key:
            return infom_readed[id]


def clear():
	# 清除临时文件
    if os.path.exists('./tmp'):
        shutil.rmtree('./tmp')
