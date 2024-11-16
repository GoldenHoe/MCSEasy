# coding = utf-8 #
# A program that helps people in need deploy Minecraft servers #
# Copyright (c) 2024 Golden_Hoe.All right reserved             #
# This project follows the MIT License                         #
import easygui
import os
import tkinter as tk
from tkinter import filedialog
import webbrowser
import wget
import urllib.request
import sys
import platform

# 让用户自定义启动方式
msg = '选择启动方式'
choices = ['直接启动','下载Minecraft服务端','配置服务器内存']
title = '选择启动方式'
cho = easygui.choicebox(msg,title,choices)
# 判断用户选项，做出相应反应
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
    mxd = '选择服务器服务端'
    cxd = ['服务端类型，此处省略']
    txd = '选择服务端'
    c0xd = easygui.choicebox(mxd,txd,cxd)
    if c0xd == cxd[0]:
        mbb = '选择服务端版本'
        # cbb为服务器版本列表显示的版本
        cbb = ['版本号，此处省略']
        tbb = '选择服务端版本'
        # URL为mojang原版服务器端下载地址
        URL = ['下载版本的URL，此处省略']
        c0bb = easygui.choicebox(mbb,tbb,cbb)
        Folderpath_download = filedialog.askdirectory(title='选择安装路径（路径不要带空格）')
        # 检测机器与Internet的连接
        url = 'https://test.ustc.edu.cn/'
        try:
            urllib.request.urlopen(url, timeout=5)
        except urllib.error.URLError as ex:
            easygui.buttonbox('网络连接异常，请检查网络连接','联网失败',['确定'])
            sys.exit(1)

        # 检查用户是否选择了有效的版本
        if c0bb in cbb:
            # 获取用户选择的版本在cbb中的索引
            index = cbb.index(c0bb)
            # 使用wget下载对应版本的服务器
            PATH = Folderpath_download
            wget.download(URL[index], PATH)
        else:
            easygui.msgbox("无效的选择，请重试。", title="错误")
            exit(1)
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
        #paper_1.21.1-https://api.papermc.io/v2/projects/paper/versions/1.21.1/builds/105/downloads/paper-1.21.1-105.jar
        Folderpath_download = filedialog.askdirectory(title='选择安装路径（路径不要带空格）')
        URL = 'https://api.papermc.io/v2/projects/paper/versions/1.21.1/builds/105/downloads/paper-1.21.1-105.jar'
        PATH = Folderpath_download
        wget.download(URL, PATH)
        easygui.buttonbox('下载完成', '下载完成', ['继续'])
        while True:
            rmin = easygui.enterbox('输入服务端最小内存分配(GB)')
            rmax = easygui.enterbox('输入服务器最大内存分配(GB)')
            if rmax <= rmin:
                easygui.buttonbox('最大分配内存不可小于最小分配内存', '错误', ['重试'])
            if rmax > rmin:
                server_path = Folderpath_download
                full_server_path = server_path + '/StartServer.bat'
                with open(full_server_path, 'w') as f:
                    f.write('java -Xmx' + rmax + 'G -Xms' + rmin + 'G -jar server.jar')
                easygui.buttonbox('启动脚本写入完成', '完成', ['确定'])
                break
            else:
                easygui.buttonbox('无效的值', '请重试', ['重试'])
    if c0xd == cxd[2]:
        easygui.msgbox('暂未开放','提示','确定')
        exit(0)
if cho == choices[2]:
    Folderpath_server = filedialog.askdirectory(title='选择服务器jar文件夹路径（路径不要带空格）')
    while True:
        rmine = easygui.enterbox('输入服务端最小内存分配(GB)')
        rmaxe = easygui.enterbox('输入服务器最大内存分配(GB)')

        if rmaxe > rmine:
            server_path_sele = Folderpath_server
            full_server_path_sele = server_path_sele + '/StartServer.bat'
            with open(full_server_path_sele, 'w') as f:
                f.write('java -Xmx' + rmaxe + 'G -Xms' + rmine + 'G -jar server.jar')
            easygui.buttonbox('','完成',['确定'])
            break
        elif rmaxe <= rmine:
            easygui.buttonbox('最大分配内存不可小于最小分配内存','错误',['重试'])
        else:
            easygui.buttonbox('无效的值','请重试',['重试'])
