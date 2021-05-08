## front-end-of-video-context-analyze-system

## 项目介绍

本项目为视频内容实时监测系统的前端部分，后端为另一位大佬编写，项目地址为：[video-context-analyze](https://github.com/kalenforn/video-context-analyze#configjson%E6%96%87%E4%BB%B6%E4%BB%8B%E7%BB%8D)

本项目使用python语言完成，基于PyQt5构建的前端，共分为四个界面：视频检测、人员管理、视频管理、直播管理。

<center>
![](https://github.com/liujilong0116/front-end-of-video-context-analyze-system/blob/main/imgs/video.png)

视频检测界面

![](https://github.com/liujilong0116/front-end-of-video-context-analyze-system/blob/main/imgs/person.png)

视频检测界面

![](https://github.com/liujilong0116/front-end-of-video-context-analyze-system/blob/main/imgs/check.png)

视频检测界面

![](https://github.com/liujilong0116/front-end-of-video-context-analyze-system/blob/main/imgs/tv.png)

视频检测界面
</center>

## 运行说明

首先按照run.py文件中import的包配置好环境，在修改配置文件config.conf中的参数，根据后端服务器中配置的数据库、文件存储位置以及后台服务进行修改。

人员、本地视频、直播源的信息都可在前端直接修改，在视频管理或直播管理中勾选上对应视频即可开始检测。

*PS：有任何问题欢迎留言，看到就会回。*

## 权限说明

感谢提供思路的老师师兄以及解决方案的第三方python库，开源许可证为MIT，请需要读者根据MIT许可证许可条件自行开发使用
