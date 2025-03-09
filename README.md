# Minecraft 简易开服程序  <small>MCSEasy</small>

用于 *帮助有需要创建 Minecraft 服务器的用户开启他们的MC服务器*
> [!NOTE]
> 我们推出了MCSEasy下一代 （*Nextgen*） 的测试版本，拥有更直观的UI，更方便的操作，以及更流畅的运行，MCSEasy Nextgen目前处于Beta阶段，尚不稳定，源码可到**GoldenHoe\MCSEasy\MCSEasy Nextgen Beta\main.py**查看。

> [!IMPORTANT]
> Nextgen版本仅支持原版端，后续会增加对模组/插件端的支持。

> [!TIP]
> 试试Nextgen版本的下载功能?（*虽然还是很慢*)

> [!IMPORTANT]
> 我们已经在 2024 年 10 月 1 日 之后 **结束对 Windows Server 2012 R2 和 Windows 8.1 的支持**(***Nextgen不再阻止Windows 8.1与Windows Server 2012 R2***)，请将设备升级到以下版本以继续使用 MCSEasy：<br>
> - Windows Server 2016 <small>14393.10</small><br/>
> - Windows 10 1507 <small>10.0.10240</small>
> - 更高版本的Windows

> [!TIP]
> Q:为什么Legacy版本有Windows版本限制？
>
> A:请看GoldenHoe\Chen-Kai-Say仓库
>
> Q:为什么Nextgen取消了Windows版本限制？
>
> A:释怀了

## 概述

本程序是一个**用于自动化部署 Minecraft 服务器的工具**，使用 **Python** 编写，**PyInstaller** 封装。
<br>它旨在**简化服务器的安装和启动操作，让有需要创建 Minecraft 服务器的用户能够更轻松地部署他们的 Minecraft 服务器**。

## 功能特性

### 快捷启动
支持通过简单的UI交互启动 Minecraft 服务器。

### 版本下载
选择不同的版本并自动下载 Minecraft 服务器 jar 文件并且引导用户设置，支持 Vanilla 原版和最新（1.21.4）的Paper 和 Spigot端，后续会添加对 Fabric 和 Forge 端的支持。

## 使用指南
### 程序硬性要求
1. Windows 10及Windows Server 2016以上64位操作系统
2. 确保网络连接。

### 建议
1. Java Development Kit(Java JDK) 8或OpenJDK 8。
2. 足够的磁盘空间用于Minecraft服务器文件。
3. CPU推荐2核心及以上，8核心以上最佳。
4. 拥有至少2GB RAM。
5. 建议使用以太网连接。
6. 使用frp等内网穿透软件。

## 下载方式
1. 直接从GitHub仓库克隆本项目。
2. 下载发布的压缩包并解压到指定目录。

## 启动

解压后**直接**运行 MCSEasy.exe

## 注意事项

根据你的服务器性能和网络状况，某些操作（下载与启动）可能需要一些时间。

## 贡献与反馈

如果你发现任何问题或有改进建议，请发送邮件到**Golden_Hoe_Lee@outlook.com**。也欢迎任何形式的贡献，包括代码、文档和测试。

## 许可证

本项目遵循MIT许可证。

Copyright © 2024 Golden_Hoe

