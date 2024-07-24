#coding = utf-8#
import easygui
import os
import tkinter as tk
from tkinter import filedialog
import webbrowser
import wget
import urllib.request
import sys
#让用户自定义启动方式
easygui.msgbox("使用注意事项：建议不要将MCSEasy放置于C盘；\n如果直接启动报错，请检查是否正确选择了启动脚本所在路径；\n在启动服务器时，可能需要关闭第一个命令窗口才能正常启动；\n某些情况下使用虚拟机将无法下载版本","提示",'我已知晓')
msg = '选择启动方式'
choices = ['直接启动','启动（同时启动内网穿透工具）','下载内网穿透软件(Cpolar)','下载Minecraft服务端','我没有服务器启动脚本或需要修改内存']
title = '选择启动方式'
cho = easygui.choicebox(msg,title,choices)
#判断用户选项，做出相应反应
if cho == choices[0]:
    m1 = '选择'
    c1 = ['选择文件位置','我已配置过']
    t1 = '选择文件位置'
    c = easygui.choicebox(m1,t1,c1)
    if c == c1[0]:
        root = tk.Tk()
        root.withdraw()
        Folderpath = filedialog.askdirectory(title='选择文件夹（路径不要带空格）')
        #保存路径
        with open('fdp_save.txt', 'w') as f:
            f.write(Folderpath)
        #显示提示
        easygui.msgbox("启动路径已保存，下次启动可直接选择“我已配置过”，再次选择路径会覆盖原来的路径","提示")
        os.chdir(Folderpath)
        os.system('start StartServer.bat')

    if c == c1[1]:
        #读取保存的路径文件
        with open('fdp_save.txt', 'r') as file:
            content = file.read()
        os.chdir(content)
        os.system('start StartServer.bat')
if cho == choices[1]:
    easygui.msgbox("内网穿透工具仅支持Cpolar，若没有安装，请到官网 https://www.cpolar.com/download 下载","提示",'确定')
    easygui.msgbox("需要手动开启开启隧道,点击“确定”或关闭窗口跳转到Cpolar管理面板",'提示','确定')
    webbrowser.open_new("http://localhost:9200/")
    m2 = '选择服务器启动方式，如果已经选择过路径了，\n请点击“我已配置过”'
    c2 = ['我已配置过','选择文件位置']
    t2 = '选择文件位置'
    ch = easygui.choicebox(m2, t2, c2)
    if ch == c2[1]:
        root = tk.Tk()
        root.withdraw()
        Folderpath = filedialog.askdirectory(title='选择文件夹（路径不要带空格）')
        # Filepath = filedialog.askopenfilename(title='选择文件（路径不要带空格）')
        # 保存路径
        with open('fdp_save.txt', 'w') as f:
            f.write(Folderpath)
        # 显示提示
        easygui.buttonbox('启动路径已保存','启动路径已保存',['确定'])
        os.chdir(Folderpath)
        os.system('start StartServer.bat')

    if ch == c2[0]:
        #读取保存的路径文件
        with open('fdp_save.txt', 'r') as file:
            content = file.read()
        os.chdir(content)
        os.system('start StartServer.bat')

if cho == choices[2]:
    webbrowser.open_new('https://www.cpolar.com/download')
if cho == choices[3]:
    mxd = '选择服务器服务端'
    cxd = ['Vanilla(原版端)','Spigot[暂未开放]']
    txd = '选择服务端'
    c0xd = easygui.choicebox(mxd,txd,cxd)
    if c0xd == cxd[0]:
        mbb = '选择服务端版本'
        #cbb为服务器版本列表显示的版本
        cbb = [
            'Release-1.21',
            'Release-1.20.6',
            'Release-1.20.5',
            'Release-1.20.4',
            'Release-1.20.2',
            'Release-1.20.1',
            'Release-1.20',
            'Release-1.19.4',
            'Release-1.19.3',
            'Release-1.19.2',
            'Release-1.19.1',
            'Release-1.19',
            'Release-1.12.2',
            'Release-1.9.4',
            'Release-1.7.10',
            'Release-1.6.4',
            'Release-1.5.2',
            'Release-1.4.7',
            'Release-1.3.2',
            'Release-1.2.5',
        ]
        tbb = '选择服务端版本'
        #URL为mojang原版服务器端下载地址
        URL = ['https://piston-data.mojang.com/v1/objects/450698d1863ab5180c25d7c804ef0fe6369dd1ba/server.jar',
               'https://piston-data.mojang.com/v1/objects/145ff0858209bcfc164859ba735d4199aafa1eea/server.jar',
               'https://piston-data.mojang.com/v1/objects/79493072f65e17243fd36a699c9a96b4381feb91/server.jar',
               'https://piston-data.mojang.com/v1/objects/8dd1a28015f51b1803213892b50b7b4fc76e594d/server.jar',
               'https://piston-data.mojang.com/v1/objects/4fb536bfd4a83d61cdbaf684b8d311e66e7d4c49/server.jar',
               'https://piston-data.mojang.com/v1/objects/5b868151bd02b41319f54c8d4061b8cae84e665c/server.jar',
               'https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba59902951553/server.jar',
               'https://piston-data.mojang.com/v1/objects/15c777e2cfe0556eef19aab534b186c0c6f277e1/server.jar',
               'https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar',
               'https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar',
               'https://piston-data.mojang.com/v1/objects/f69c284232d7c7580bd89a5a4931c3581eae1378/server.jar',
               'https://piston-data.mojang.com/v1/objects/e00c4052dac1d59a1188b2aa9d5a87113aaf1122/server.jar',
               'https://piston-data.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar',
               'https://piston-data.mojang.com/v1/objects/edbb7b1758af33d365bf835eb9d13de005b1e274/server.jar',
               'https://launcher.mojang.com/v1/objects/952438ac4e01b4d115c5fc38f891710c4941df29/server.jar',
               'https://launcher.mojang.com/v1/objects/050f93c1f3fe9e2052398f7bd6aca10c63d64a87/server.jar',
               'https://launcher.mojang.com/v1/objects/f9ae3f651319151ce99a0bfad6b34fa16eb6775f/server.jar',
               'https://launcher.mojang.com/v1/objects/2f0ec8efddd2f2c674c77be9ddb370b727dec676/server.jar',
               'https://launcher.mojang.com/v1/objects/3de2ae6c488135596e073a9589842800c9f53bfe/server.jar',
               'https://launcher.mojang.com/v1/objects/d8321edc9470e56b8ad5c67bbd16beba25843336/server.jar']
        c0bb = easygui.choicebox(mbb,tbb,cbb)
        Folderpath_download = filedialog.askdirectory(title='选择安装路径（路径不要带空格）')
        # 检测机器与baidu.com的连接
        url = 'https://www.baidu.com'
        try:
            urllib.request.urlopen(url, timeout=5)
        except urllib.error.URLError as ex:
            easygui.buttonbox('网络连接异常，请检查网络连接','联网失败',['确定'])
            sys.exit(1)
        if c0bb == cbb[0]:
            URL = URL[0]
            PATH = Folderpath_download
            wget.download(URL, PATH)

        if c0bb == cbb[1]:
            URL = URL[1]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[2]:
            URL = URL[2]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[3]:
            URL = URL[3]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[4]:
            URL = URL[4]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[5]:
            URL = URL[5]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[6]:
            URL = URL[6]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[7]:
            URL = URL[7]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[8]:
            URL = URL[8]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[9]:
            URL = URL[9]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[10]:
            URL = URL[10]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[11]:
            URL = URL[11]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[12]:
            URL = URL[12]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[13]:
            URL = URL[13]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[14]:
            URL = URL[14]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[15]:
            URL = URL[15]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[16]:
            URL = URL[16]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[17]:
            URL = URL[17]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[18]:
            URL = URL[18]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        if c0bb == cbb[19]:
            URL = URL[19]
            PATH = Folderpath_download
            wget.download(URL, PATH)
        easygui.buttonbox('下载完成','下载完成',['继续'])
        while True:
            rmin = easygui.enterbox('输入服务端最小内存分配(GB)')
            rmax = easygui.enterbox('输入服务器最大内存分配(GB)')
            if rmax <= rmin:
                easygui.buttonbox('最大分配内存不可小于最小分配内存','错误',['重试'])
            if rmax > rmin:
                server_path = Folderpath_download
                full_server_path = server_path+'/StartServer.bat'
                with open(full_server_path, 'w') as f:
                    f.write('java -Xmx'+rmax+'G -Xms'+rmin+'G -jar server.jar')
                easygui.buttonbox('启动脚本写入完成','完成',['确定'])
                break
            else:
                easygui.buttonbox('无效的值','请重试',['重试'])
    if c0xd == cxd[1]:
        easygui.buttonbox('暂未开放','错误',['关闭'])

if cho == choices[4]:
    Folderpath_server = filedialog.askdirectory(title='选择服务器jar文件夹路径（路径不要带空格）')
    while True:
        rmine = easygui.enterbox('输入服务端最小内存分配(GB)')
        rmaxe = easygui.enterbox('输入服务器最大内存分配(GB)')

        if rmaxe > rmine:
            server_path_sele = Folderpath_server
            full_server_path_sele = server_path_sele + '/StartServer.bat'
            with open(full_server_path_sele, 'w') as f:
                f.write('java -Xmx' + rmaxe + 'G -Xms' + rmine + 'G -jar server.jar')
            easygui.buttonbox('启动脚本写入完成','完成',['确定'])
            break
        elif rmaxe <= rmine:
            easygui.buttonbox('最大分配内存不可小于最小分配内存','错误',['重试'])
        else:
            easygui.buttonbox('无效的值','请重试',['重试'])
