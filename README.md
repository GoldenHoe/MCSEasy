<h1 align="center">Minecraft简易开服程序MCSEasy</h1>

<p align="center">
  <img src="logo.svg" alt="MCSEasy Logo" width="150">
</p>

<div align="center">

[![Stars](https://img.shields.io/github/stars/GoldenHoe/MCSEasy?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEiIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PHBhdGggZD0iTTggLjI1YS43NS43NSAwIDAgMSAuNjczLjQxOGwxLjg4MiAzLjgxNSA0LjIxLjYxMmEuNzUuNzUgMCAwIDEgLjQxNiAxLjI3OWwtMy4wNDYgMi45Ny43MTkgNC4xOTJhLjc1MS43NTEgMCAwIDEtMS4wODguNzkxTDggMTIuMzQ3bC0zLjc2NiAxLjk4YS43NS43NSAwIDAgMS0xLjA4OC0uNzlsLjcyLTQuMTk0TC44MTggNi4zNzRhLjc1Ljc1IDAgMCAxIC40MTYtMS4yOGw0LjIxLS42MTFMNy4zMjcuNjY4QS43NS43NSAwIDAgMSA4IC4yNVoiIGZpbGw9IiNlYWM1NGYiLz48L3N2Zz4=&logoSize=auto&label=Stars&labelColor=444444&color=eac54f)](https://github.com/GoldenHoe/MCSEasy)
[![LICENSE](https://img.shields.io/github/license/GoldenHoe/MCSEasy?style=for-the-badge)](https://github.com/GoldenHoe/MCSEasy/blob/main/LICENSE)
![GitHub Release](https://img.shields.io/github/v/release/GoldenHoe/MCSEasy?label=Release&logo=github&style=for-the-badge)
</div>

用于 *帮助有需要创建 Minecraft 服务器的用户开启并监视他们的MC服务器*
> [!TIP]
> 我们推出了针对`MCSEasy 1.2.0.0-RC1`的GUI重构版本`MCSEasy 1.2.0.0-RC1-GUIRefactor`，拥有更美观的UI、更好的个性化、更方便的操作以及更流畅的运行，MCSEasy 1.2.0正在开发阶段，已经修复了已知的内存管理错误，源码可到[**GoldenHoe\MCSEasy\gui-re-main.py**[↗]](https://github.com/GoldenHoe/MCSEasy/blob/main/gui-re-main.py)查看，现编译的发行版本为`1.2.0-RC1`，详情请到[GitHub Release[↗]](https://github.com/GoldenHoe/MCSEasy/releases)查看。


> [!NOTE]
> #### 支持的Windows版本:  
> - Windows 7 with Service Pack 1/2(Build 7601/7602)
> - Windows Server 2008 R2 Service Pack 1/2(Build 7601/7602)
> - Windows 8(Build 9200)
> - Windows Server 2012(Build 9200)
> - Windows 8.1(Build 9600)
> - Windows Server 2012 R2(Build 9600)
> - Windows 10
> - Windows Server 2016/2019/2022(Build 14393/17763/20348)
> - Windows 11
> - Windows Server 2025(Build 26100)

## 概述

本程序是一个**用于自动化部署 Minecraft 服务器的工具**，使用 **Python** 编写，**PyInstaller** 封装。
<br>它旨在**简化服务器的安装和启动操作，让有需要创建 Minecraft 服务器的用户能够更轻松地部署他们的 Minecraft 服务器并监视服务器状态**。

## 功能特性

### 快捷启动
支持通过简单的UI配置、交互、启动和监视 Minecraft 服务器。

### 版本支持
选择不同的版本并自动下载 Minecraft 服务器 jar 文件并且采用半自动配置，支持 Vanilla 端 ，已经有对于插件端和模组端的**启动**支持。

## 使用指南
### 程序硬性要求
1. Windows 7 Service Pack 1及Windows Server 2008 R2 Service Pack 1以上64位操作系统
2. 网络连接。

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

## * AI 内容生成提示

本项目部分 GUI 代码由 ChatGPT / Google Gemini 辅助生成，后续已由人工审查和修改。  
AI 生成的内容仅用于提高开发效率，不保证完全正确性。项目维护与责任由开发者承担。  


## 贡献与反馈

如果你发现任何问题或有改进建议，请发送邮件到**Golden_Hoe_Lee@outlook.com**或**hoe_team@outlook.com**。也欢迎任何形式的贡献，包括代码、文档和测试。  
本项目应用图标生成自[AppIcon Force[↗]](https://zhangyu1818.github.io/appicon-forge/)

## 许可证
Copyright © 2024-2025 Golden_Hoe&HOE Software Team
项目遵循[MIT许可证[↗]](https://github.com/GoldenHoe/MCSEasy/blob/main/LICENSE)

> [!NOTE]
> 这份许可证意味着：
> 
> 1.  **你可以随意使用这个项目代码**，无论是在个人项目还是商业项目中。
> 2.  **你可以修改并重新发布**这个代码。
> 3.  **你甚至可以用它来开发商业软件并销售**，只要你在你的产品中包含原始的 MIT 许可证文本和版权声明。
> 4.  **作者不提供任何保证**，如果使用该软件导致任何问题，你需要自己承担风险。
