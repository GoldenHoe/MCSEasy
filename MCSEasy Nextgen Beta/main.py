# coding = utf-8 #
# A program that helps people in need deploy Minecraft servers #
# Copyright (c) 2024 Golden_Hoe.All right reserved             #
# This project follows the MIT License                         #
import sys
import os
import urllib.request
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QComboBox, QFileDialog, QMessageBox,
                             QLabel, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from pywinstyles import apply_style


def load_list_file(filename):
    """从文本文件加载Python列表"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    try:
        return eval(content)
    except Exception as e:
        print(f"加载列表文件错误: {str(e)}")
        return []


class DownloadThread(QThread):
    progress_updated = pyqtSignal(int)
    download_finished = pyqtSignal(bool, str)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            with urllib.request.urlopen(self.url) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                chunk_size = 8192
                filename = os.path.join(self.save_path, self.url.split('/')[-1])

                with open(filename, 'wb') as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            self.progress_updated.emit(int((downloaded / total_size) * 100))

                self.download_finished.emit(True, filename)
        except Exception as e:
            self.download_finished.emit(False, str(e))


class ServerDeployWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("简便 Minecraft 服务器部署工具(MCSEasy) Version-1.2.0.0-Beta")
        self.setGeometry(100, 100, 600, 400)
        self.download_thread = None

        # ================== 样式设置 ==================
        apply_style(self, "normal")
        self.setStyleSheet("""
            QWidget {
                color: black;
                font-family: 'Microsoft YaHei';
            }
            QComboBox, QPushButton, QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #333333;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        # ================== 初始化数据 ==================
        self.url_list = load_list_file('url_list.txt')
        self.version_list = load_list_file('version_list.txt')

        # ================== 主控件布局 ==================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 功能选择
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['启动服务器', '下载服务端', '配置内存'])
        layout.addWidget(QLabel("选择操作模式:"))
        layout.addWidget(self.mode_combo)

        # 版本选择
        self.version_combo = QComboBox()
        self.version_combo.addItems(self.version_list)
        layout.addWidget(QLabel("选择服务端版本:"))
        layout.addWidget(self.version_combo)
        self.version_combo.hide()

        # 路径选择
        self.path_btn = QPushButton("选择安装路径")
        self.path_btn.clicked.connect(self.select_directory)
        self.path_label = QLabel("未选择路径")
        layout.addWidget(QLabel("安装路径:"))
        layout.addWidget(self.path_btn)
        layout.addWidget(self.path_label)

        # 内存配置
        self.mem_min = QLineEdit()
        self.mem_max = QLineEdit()
        layout.addWidget(QLabel("最小内存(GB):"))
        layout.addWidget(self.mem_min)
        layout.addWidget(QLabel("最大内存(GB):"))
        layout.addWidget(self.mem_max)
        self.mem_min.hide()
        self.mem_max.hide()

        # 操作按钮
        self.execute_btn = QPushButton("执行")
        self.execute_btn.clicked.connect(self.execute_action)
        layout.addWidget(self.execute_btn)

        # 绑定事件
        self.mode_combo.currentIndexChanged.connect(self.update_ui)

    def update_ui(self):
        """根据选择的操作模式显示/隐藏控件"""
        mode = self.mode_combo.currentText()
        self.version_combo.setVisible(mode == '下载服务端')
        self.mem_min.setVisible(mode == '配置内存')
        self.mem_max.setVisible(mode == '配置内存')

    def select_directory(self):
        """选择安装目录"""
        path = QFileDialog.getExistingDirectory(self, "选择安装路径")
        if path:
            self.path_label.setText(path)

    def execute_action(self):
        """执行主要操作"""
        try:
            mode = self.mode_combo.currentText()
            path = self.path_label.text()

            if mode == '直接启动':
                self.launch_server(path)
            elif mode == '下载服务端':
                version = self.version_combo.currentText()
                self.download_server(path, version)
            elif mode == '配置内存':
                self.configure_memory(path)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"操作失败: {str(e)}")

    def launch_server(self, path):
        """启动服务器"""
        if not path or not os.path.exists(os.path.join(path, 'StartServer.bat')):
            raise ValueError("无效的服务器路径")
        os.chdir(path)
        os.system('start StartServer.bat')

    def download_server(self, path, version):
        """初始化下载流程"""
        if not path:
            raise ValueError("请先选择安装路径")

        try:
            index = self.version_list.index(version)
            url = self.url_list[index]
        except ValueError:
            raise ValueError("无效的版本选择")

        # 网络检查
        try:
            urllib.request.urlopen('http://connectivitycheck.gstatic.com/generate_204', timeout=5)
        except:
            raise ConnectionError("网络连接异常")

        # 初始化下载线程
        self.download_thread = DownloadThread(url, path)
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.download_finished.connect(self.on_download_finished)

        self.execute_btn.setEnabled(False)
        self.download_thread.start()

    def update_progress(self, percent):
        """更新下载进度"""
        self.execute_btn.setText(f"下载中... {percent}%")

    def on_download_finished(self, success, message):
        """下载完成处理"""
        self.execute_btn.setEnabled(True)
        self.execute_btn.setText("执行")

        if success:
            QMessageBox.information(self, "完成", f"服务端已保存至:\n{message}")
        else:
            QMessageBox.critical(self, "错误", f"下载失败: {message}")

    def configure_memory(self, path):
        """配置内存"""
        min_mem = self.mem_min.text()
        max_mem = self.mem_max.text()

        if not min_mem.isdigit() or not max_mem.isdigit():
            raise ValueError("请输入有效的数字")

        if int(max_mem) <= int(min_mem):
            raise ValueError("最大内存必须大于最小内存")

        bat_path = os.path.join(path, 'StartServer.bat')
        with open(bat_path, 'w') as f:
            f.write(f'java -Xmx{max_mem}G -Xms{min_mem}G -jar server.jar')
        QMessageBox.information(self, "完成", "内存配置已更新")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_font = QFont("Microsoft YaHei")
    app.setFont(app_font)
    window = ServerDeployWindow()
    window.show()
    sys.exit(app.exec_())
