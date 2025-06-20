# Minecraft 简易开服程序  <small>MCSEasy</small>

用于 *帮助有需要创建 Minecraft 服务器的用户开启并监视他们的MC服务器*
> [!NOTE]
> 我们推出了MCSEasy 1.2的Beta版本，拥有更美观的UI（*Hoe碎碎念：其实就是控件疯狂加圆角*），更方便的操作，以及更流畅的运行，MCSEasy 1.2目前处于Beta阶段，尚不稳定，源码可到**GoldenHoe\MCSEasy\main.py**查看。

> [!IMPORTANT]
> MCSEasy 1.2版本仅支持原版端，后续会增加对模组/插件端的支持。

> [!IMPORTANT]
> MCSEasy**不支持**Windows 8(Build 9200 *经过验证可以运行的Windows版本*)或Windows Server 2012**以下**的Windows版本，请升级到以下版本来使用MCSEasy：
> - Windows Server 2012
> - Windows 8(Build 9200)
> - 更高版本的Windows

> [!WARNING]
> 尚不确定Windows 7 with SP1/SP2是否可以运行。

## 概述

本程序是一个**用于自动化部署 Minecraft 服务器的工具**，使用 **Python** 编写，**PyInstaller** 封装。
<br>它旨在**简化服务器的安装和启动操作，让有需要创建 Minecraft 服务器的用户能够更轻松地部署他们的 Minecraft 服务器并监视服务器状态**。

## 功能特性

### 快捷启动
支持通过简单的UI配置、交互、启动和监视 Minecraft 服务器。

### 版本下载
选择不同的版本并自动下载 Minecraft 服务器 jar 文件并且引导用户设置，支持 Vanilla 原版和最新（1.21.5）的Paper 和 Spigot端（MCSEasy 1.1，后续会更新插件端下载和部署)，后续会添加对 Fabric 和 Forge 端的支持。

## 使用指南
### 程序硬性要求
1. Windows 8及Windows Server 2012以上64位操作系统
2. 确保网络连接。
3. *CPUID和MAC地址未被禁止（预更新）*

### 建议
1. Java Development Kit(Java JDK) 8或OpenJDK 8。
2. 足够的磁盘空间用于Minecraft服务器文件。
3. CPU推荐2核心及以上，8核心以上最佳。
4. 拥有至少2GB RAM。
5. 使用以太网连接。
6. 使用frp等内网穿透软件（公网IP可忽略）。
7. 下载Python3.6以上版本。

## 下载方式
1. 直接从GitHub仓库克隆本项目。
2. 下载发布的压缩包并解压到指定目录。
3. 下载Release的发布版本(已打包成exe可执行文件)

## 启动

解压后**直接**运行 MCSEasy.exe

## 注意事项

根据你的计算机性能和网络状况，某些操作（下载与启动）可能需要一些时间。

## 贡献与反馈

如果你发现任何问题或有改进建议，请发送邮件到**Golden_Hoe_Lee@outlook.com**或**hoe_team@outlook.com**。也欢迎任何形式的贡献，包括代码、文档和测试。

## 许可证

本项目遵循MIT许可证。

Copyright © 2024 Golden_Hoe,HOE Software Team

