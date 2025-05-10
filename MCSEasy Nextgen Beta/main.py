# coding=utf-8
# Copyright (C) 2024-2025 Golden_Hoe,HOE Software Team. #

# 导入库
import sys
import os
import json
import ctypes
import urllib.request
import psutil
import logging
import ctypes
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QFileDialog, QMessageBox,
                             QLabel, QLineEdit, QStackedWidget, QPlainTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QProcess, QTimer
from PyQt5.QtGui import QFont, QTextCursor
from pywinstyles import apply_style


# ==================== 主程序 ====================
# 最后修改 2025/5/11
# ==================== 配置日志 ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("launch.log"),  # 日志输出到文件
        logging.StreamHandler()  # 日志输出到控制台
    ]
)
logger = logging.getLogger(__name__)
# ++++++++++++++++++++ 检测硬件信息 ++++++++++++++++++++
def check_hardware():
    # 设定警告数量初始值
    warn_n = 0
    # 检查CPU核心数量
    cpu_cores = psutil.cpu_count(logical=False)  # 获取物理核心数
    logger.info(f"CPU物理核心数量: {cpu_cores}")
    if cpu_cores < 2:
        logger.warning("警告: CPU核心数量不足 (少于2个)。")
        ctypes.windll.user32.MessageBoxW(0, "CPU物理核心数核心数少于2，可能会导致服务器性能偏低。", "警告", 0x30)
        warn_n = warn_n + 1
    else:
        logger.info("CPU核心数量检查通过。")

    # 检查内存
    memory = psutil.virtual_memory()
    logger.info(f"计算机总内存: {memory.total / 1024**2} MB")
    if memory.total / 1024**2 < 2048:
        logger.warning("警告:计算机已安装内存过低 (低于 2048 MB)。")
        ctypes.windll.user32.MessageBoxW(0, "已安装的运行内存少于2048M，可能会导致服务器性能偏低。", "警告", 0x30)
        warn_n = warn_n+1
    else:
        logger.info("内存检查通过。")

    # 检查磁盘空间
    current_file_path = os.path.abspath(__file__)
    disk_root = os.path.splitdrive(current_file_path)[0] + '\\'
    disk_usage = psutil.disk_usage(disk_root)
    logger.info(f"当前磁盘可用容量: {disk_usage.free / 1024**3} GB")
    if disk_usage.free / 1024**3 < 8:
        logger.warning("磁盘空间不足 (可用空间少于 8 GB)。")
        ctypes.windll.user32.MessageBoxW(0, "磁盘可用空间不足8GB，可能会导致服务器文件无法存放。", "警告", 0x30)
        warn_n = warn_n + 1
    else:
        logger.info("磁盘容量检查通过。")

    if warn_n != 0:
        logger.info(f"硬件检查结束，共发现{warn_n}个性能问题。")
        ctypes.windll.user32.MessageBoxW(0, f"硬件检测发现了{warn_n}个性能问题。", "警告", 0x30)
    else:
        logger.info('硬件检查结束，没有发现问题。')


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
    log_signal = pyqtSignal(str)
    process_output = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("简单 Minecraft 服务器部署工具(MCSEasy) Version-1.2.0.0-Beta2")
        self.setGeometry(100, 100, 1000, 500)#self.setGeometry(100, 100, 800, 500)
        self.download_thread = None
        self.log_widget = None  # 日志控件
        # 新增进程对象
        self.server_process = None
        self.process_output.connect(self.update_log)  # 连接输出信号
        self.has_unsaved_changes = False
        self.config_controls = {}
        self.original_config = {}

        # ================== 样式设置 ==================
        apply_style(self, "normal")
        # 在样式表中修改QPushButton部分
        self.setStyleSheet("""
            QWidget {
                color: black;
                font-family: 'Microsoft YaHei';
            }
            QComboBox, QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #0078D4;
                padding: 5px;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #FFFFFF;
                border: 2px solid #0078D4;
                padding: 5px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
            QPushButton:pressed {
                background-color: #E0E0E0;
            }
            QComboBox::drop-down {
                border: none;
            }
            QPlainTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #333333;
                border-radius: 8px;
                font-family: 'Microsoft Yahei';
                font-weight: bold;
            }
        """)

        # ================== 初始化数据 ==================
        self.url_list = load_list_file('url_list.txt')
        self.version_list = load_list_file('version_list.txt')

        # ================== 主控件布局 ==================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 左侧操作区域 (2:3比例)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.stacked_widget = QStackedWidget()

        self.create_start_page()
        self.create_download_page()
        self.create_memory_page()
        self.create_config_page()

        left_layout.addWidget(QLabel("选择操作模式:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['启动服务器', '下载服务端', '配置内存'])
        left_layout.addWidget(self.mode_combo)
        left_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(left_widget, stretch=2)  # 左侧占2份

        # 右侧日志区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(QLabel("服务器日志输出:"))
        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)
        # 设置日志字体
        log_font = QFont("Microsoft YaHei")
        log_font.setBold(True)
        log_font.setPointSize(9)
        self.log_widget.setFont(log_font)
        right_layout.addWidget(self.log_widget)
        main_layout.addWidget(right_widget, stretch=3)  # 右侧占3份
        self.right_widget = right_widget  # 保存引用
        # 新增指令输入框
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("输入服务器指令（按回车发送）")
        self.command_input.returnPressed.connect(self.send_command)
        right_layout.addWidget(self.command_input)
        # 绑定信号
        self.mode_combo.currentIndexChanged.connect(self.switch_mode_page)
        self.log_signal.connect(self.update_log)
        self.load_settings()
        # 加载保存的配置
        self.load_settings()

    def load_settings(self):
        """加载保存的配置"""
        settings_file = "mcseasy_settings.meconf"
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.path_label_start.setText(settings.get("start_path", ""))
                    self.path_label_download.setText(settings.get("download_path", ""))
                    self.path_label_memory.setText(settings.get("memory_path", ""))
                    self.mem_min.setText(settings.get("min_mem", ""))
                    self.mem_max.setText(settings.get("max_mem", ""))
                self.log_signal.emit("[MCSEasy-INFO] 已加载保存的配置")
            except Exception as e:
                self.log_signal.emit(f"[MCSEasy-ERROR] 配置加载失败: {str(e)}")

    def save_settings(self):
        """保存当前配置到文件"""
        settings = {
            "start_path": self.path_label_start.text(),
            "download_path": self.path_label_download.text(),
            "memory_path": self.path_label_memory.text(),
            "min_mem": self.mem_min.text(),
            "max_mem": self.mem_max.text()
        }
        try:
            with open("mcseasy_settings.meconf", 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
            self.log_signal.emit("[MCSEasy-INFO] 配置已保存")
        except Exception as e:
            self.log_signal.emit(f"[MCSEasy-ERROR] 配置保存失败: {str(e)}")

    def create_start_page(self):
        """启动页面"""
        self.start_page = QWidget()
        layout = QVBoxLayout(self.start_page)
        # 調整邊距和間距
        layout.setContentsMargins(5, 5, 5, 5)  # 統一四邊邊距
        layout.setSpacing(5)

        # 路徑相關控件
        path_group = QWidget()
        path_layout = QVBoxLayout(path_group)
        path_layout.addWidget(QLabel("服务器路径:"))
        self.path_label_start = QLabel("未选择路径")
        self.path_label_start.setWordWrap(True)
        path_layout.addWidget(self.path_label_start)
        self.path_btn_start = QPushButton("选择服务器路径")
        self.path_btn_start.clicked.connect(self.select_directory)
        path_layout.addWidget(self.path_btn_start)

        # 將路徑組件添加到主佈局
        layout.addWidget(path_group)

        # 添加拉伸空間，將按鈕推到底部
        layout.addStretch(1)

        # 按鈕組（啟動/停止）
        btn_group = QWidget()
        btn_layout = QVBoxLayout(btn_group)
        btn_layout.setSpacing(5)
        self.execute_btn_start = QPushButton("启动服务器")
        self.execute_btn_start.clicked.connect(lambda: self.execute_action('启动服务器'))
        self.stop_btn = QPushButton("停止服务器")
        self.stop_btn.hide()
        self.stop_btn.clicked.connect(self.stop_server)
        self.config_btn = QPushButton("修改服务器配置")
        self.config_btn.clicked.connect(lambda: self.load_server_config())
        btn_layout.addWidget(self.execute_btn_start)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.config_btn)

        # 將按鈕組添加到主佈局底部
        layout.addWidget(btn_group)

        self.stacked_widget.addWidget(self.start_page)

    def create_download_page(self):
        """下载服务端页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        # 調整邊距和間距
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # 版本选择组件
        version_group = QWidget()
        version_layout = QVBoxLayout(version_group)
        version_layout.addWidget(QLabel("选择服务端版本:"))
        self.version_combo = QComboBox()
        self.version_combo.addItems(self.version_list)
        version_layout.addWidget(self.version_combo)
        layout.addWidget(version_group)

        # 路径选择组件
        path_group = QWidget()
        path_layout = QVBoxLayout(path_group)
        path_layout.addWidget(QLabel("安装路径:"))
        self.path_label_download = QLabel("未选择路径")
        self.path_label_download.setWordWrap(True)
        path_layout.addWidget(self.path_label_download)
        self.path_btn_download = QPushButton("选择安装路径")
        self.path_btn_download.clicked.connect(self.select_directory)
        path_layout.addWidget(self.path_btn_download)
        layout.addWidget(path_group)

        # 添加拉伸空间
        layout.addStretch(1)

        # 下载按钮置底
        self.execute_btn_download = QPushButton("开始下载")
        self.execute_btn_download.clicked.connect(lambda: self.execute_action('下载服务端'))
        layout.addWidget(self.execute_btn_download)

        self.stacked_widget.addWidget(page)

    def create_memory_page(self):
        """配置内存页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # 内存输入组件
        mem_group = QWidget()
        mem_layout = QVBoxLayout(mem_group)
        mem_layout.addWidget(QLabel("最小内存(GB):"))
        self.mem_min = QLineEdit()
        mem_layout.addWidget(self.mem_min)
        mem_layout.addWidget(QLabel("最大内存(GB):"))
        self.mem_max = QLineEdit()
        mem_layout.addWidget(self.mem_max)
        layout.addWidget(mem_group)

        # 路径选择组件
        path_group = QWidget()
        path_layout = QVBoxLayout(path_group)
        path_layout.addWidget(QLabel("服务器路径:"))
        self.path_label_memory = QLabel("未选择路径")
        self.path_label_memory.setWordWrap(True)
        path_layout.addWidget(self.path_label_memory)
        self.path_btn_memory = QPushButton("选择服务器路径")
        self.path_btn_memory.clicked.connect(self.select_directory)
        path_layout.addWidget(self.path_btn_memory)
        layout.addWidget(path_group)

        # 添加拉伸空间
        layout.addStretch(1)

        # 保存按钮置底
        self.execute_btn_memory = QPushButton("保存配置")
        self.execute_btn_memory.clicked.connect(lambda: self.execute_action('配置内存'))
        layout.addWidget(self.execute_btn_memory)

        self.stacked_widget.addWidget(page)

    def switch_mode_page(self):
        """切换模式页面"""
        index = self.mode_combo.currentIndex()
        self.stacked_widget.setCurrentIndex(index)
        # 显示/隐藏日志区域
        self.right_widget.setVisible(index != 3)  # 配置页隐藏日志

    def select_directory(self):
        """选择路径并更新对应页面的标签"""
        path = QFileDialog.getExistingDirectory(self, "选择路径")
        if not path:
            return

        # 根据当前模式更新对应的路径标签
        mode = self.mode_combo.currentText()
        if mode == '启动服务器':
            self.path_label_start.setText(path)
        elif mode == '下载服务端':
            self.path_label_download.setText(path)
        elif mode == '配置内存':
            self.path_label_memory.setText(path)
        self.save_settings()

    def execute_action(self, mode):
        """执行操作并记录日志"""
        try:
            if mode == '启动服务器':
                path = self.path_label_start.text()
                self.launch_server(path)
            elif mode == '下载服务端':
                path = self.path_label_download.text()
                version = self.version_combo.currentText()
                self.download_server(path, version)
            elif mode == '配置内存':
                path = self.path_label_memory.text()
                self.configure_memory(path)

            self.log_signal.emit(f"[MCSEasy-INFO] {mode} 操作已执行")
        except Exception as e:
            self.log_signal.emit(f"[MCSEasy-ERROR] {str(e)}")
            QMessageBox.critical(self, "错误", f"操作失败: {str(e)}")

    def update_log(self, message):
        """更新日志内容（优化版）"""
        cursor = self.log_widget.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(f"{message}\n")
        self.log_widget.setTextCursor(cursor)
        self.log_widget.ensureCursorVisible()

    # 以下方法保持原有功能实现，仅修改路径获取方式
    def launch_server(self, path):
        """修改后的启动方法"""
        self.modify_eila(path)
        if not path or not os.path.exists(os.path.join(path, 'StartServer.bat')):
            raise ValueError("无效的服务器路径")

        try:
            os.chdir(path)
            self.server_process = QProcess()
            self.server_process.setProcessChannelMode(QProcess.MergedChannels)
            self.server_process.readyReadStandardOutput.connect(self.handle_process_output)
            self.server_process.finished.connect(self.on_server_stopped)  # 新增结束信号

            # 启动后更新界面
            self.execute_btn_start.hide()
            self.stop_btn.show()
            self.server_process.start("cmd.exe", ["/c", "StartServer.bat"])

        except Exception as e:
            self.log_signal.emit(f"[MCSEasy-ERROR] 启动失败: {str(e)}")

    def on_server_stopped(self):
        """服务器停止时的处理"""
        self.execute_btn_start.show()
        self.stop_btn.hide()
        self.log_signal.emit("[MCSEasy-INFO] 服务器已停止")

    def stop_server(self):
        """停止服务器"""
        if self.server_process:
            self.server_process.write("stop\n".encode())  # 发送stop命令
            QTimer.singleShot(2000, self.force_kill_server)  # 2秒后强制终止

    def force_kill_server(self):
        if self.server_process and self.server_process.state() == QProcess.Running:
            self.server_process.kill()
            self.log_signal.emit("[MCSEasy-WARN] 已强制终止服务器进程")

    def send_command(self):
        """发送指令到服务器"""
        command = self.command_input.text()
        if command and self.server_process:
            self.server_process.write(f"{command}\n".encode())
            self.command_input.clear()

    def handle_process_output(self):
        """处理进程输出"""
        if self.server_process:
            output = self.server_process.readAllStandardOutput().data().decode("gbk")
            self.process_output.emit(output.strip())

    def download_server(self, path, version):
        if not path:
            raise ValueError("请先选择安装路径")
        try:
            index = self.version_list.index(version)
            url = self.url_list[index]
        except ValueError:
            raise ValueError("无效的版本选择")
        try:
            urllib.request.urlopen('http://connectivitycheck.gstatic.com/generate_204', timeout=5)
        except:
            raise ConnectionError("网络连接异常")

        self.download_thread = DownloadThread(url, path)
        self.download_thread.progress_updated.connect(lambda p: self.execute_btn_download.setText(f"下载中... {p}%"))
        self.download_thread.download_finished.connect(self.on_download_finished)
        self.execute_btn_download.setEnabled(False)
        self.download_thread.start()

    def on_download_finished(self, success, message):
        self.execute_btn_download.setEnabled(True)
        self.execute_btn_download.setText("开始下载")
        if success:
            QMessageBox.information(self, "完成", f"服务端已保存至:\n{message}")
        else:
            QMessageBox.critical(self, "错误", f"下载失败: {message}")

    def configure_memory(self, path):
        min_mem = self.mem_min.text()
        max_mem = self.mem_max.text()
        if not min_mem.isdigit() or not max_mem.isdigit():
            raise ValueError("请输入有效的数字")
        if int(max_mem) <= int(min_mem):
            raise ValueError("最大内存必须大于最小内存")

        bat_path = os.path.join(path, 'StartServer.bat')
        with open(bat_path, 'w') as f:
            f.write(f'java -Xmx{max_mem}G -Xms{min_mem}G -jar server.jar --nogui')
        self.save_settings()
    def modify_eila(self, path):
        """首次启动修改EULA.txt"""
        eula_path = os.path.join(path, "eula.txt")
        if os.path.exists(eula_path):
            with open(eula_path, "r")as f:
                content = f.read()
            if "eula=false" in content.lower():
                with open(eula_path, 'w')as f:
                    f.write(content.replace("eula=false","eula=true"))
                self.log_signal.emit("[MCSeasy-INFO] 已自动同意EULA协议")

    def create_config_page(self):
        """创建服务器配置编辑页"""
        self.config_page = QWidget()
        layout = QVBoxLayout(self.config_page)
        #返回主页面按钮
        back_btn = QPushButton('返回')
        back_btn.clicked.connect(self.check_unsaved_changes)
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        # 配置项容器
        self.config_widget = QWidget()
        self.config_layout = QVBoxLayout(self.config_widget)
        layout.addWidget(self.config_widget)
        # 按钮组
        btn_group = QWidget()
        btn_layout = QHBoxLayout(btn_group)
        self.save_btn = QPushButton("保存并退出")
        self.save_btn.clicked.connect(self.save_server_config)
        self.revert_btn = QPushButton("撤销全部更改")
        self.revert_btn.clicked.connect(self.load_server_config)
        btn_layout.addWidget(self.revert_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addWidget(btn_group)
        self.stacked_widget.addWidget(self.config_page)

    def load_server_config(self):
        """加载服务器配置"""
        path = self.path_label_start.text()
        prop_path = os.path.join(path, 'server.properties')
        self.original_config = {}

        if os.path.exists(prop_path):
            with open(prop_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key_val = line.split('=')
                        if len(key_val) == 2:
                            self.original_config[key_val[0]] = key_val[1]

        # 清空现有控件
        for i in reversed(range(self.config_layout.count())):
            self.config_layout.itemAt(i).widget().setParent(None)

        # 生成配置控件
        self.config_controls = {}
        for key, value in self.original_config.items():
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(QLabel(f"{key}:"), stretch=1)

            # 根据值类型创建控件
            if value.lower() in ['true', 'false']:
                combo = QComboBox()
                combo.addItems(['true', 'false'])
                combo.setCurrentText(value)
                layout.addWidget(combo, stretch=2)
                self.config_controls[key] = combo
            else:
                edit = QLineEdit(value)
                layout.addWidget(edit, stretch=2)
                self.config_controls[key] = edit

            self.config_layout.addWidget(widget)

        self.stacked_widget.setCurrentIndex(3)  # 假设配置页是第4个页面
        self.has_unsaved_changes = False
        for control in self.config_controls.values():
            if isinstance(control, QComboBox):
                control.currentIndexChanged.connect(lambda: setattr(self, 'has_unsaved_changes', True))
            else:
                control.textChanged.connect(lambda: setattr(self, 'has_unsaved_changes', True))

    def save_server_config(self):
        """保存服务器配置"""
        path = self.path_label_start.text()
        prop_path = os.path.join(path, 'server.properties')

        new_config = []
        for key, control in self.config_controls.items():
            value = control.currentText() if isinstance(control, QComboBox) else control.text()
            new_config.append(f"{key}={value}")

        with open(prop_path, 'w') as f:
            f.write('\n'.join(new_config))

        self.stacked_widget.setCurrentIndex(0)
        self.log_signal.emit("[MCSEasy-INFO] 服务器配置已更新")
        self.has_unsaved_changes = False

    def check_unsaved_changes(self):
        """检查未保存的更改"""
        if self.has_unsaved_changes:
            msg = QMessageBox()
            msg.setWindowTitle("未保存的更改")
            msg.setText("您有未保存的更改，是否要保存？")
            msg.addButton("保存并退出", QMessageBox.AcceptRole)
            msg.addButton("不保存退出", QMessageBox.RejectRole)
            msg.addButton("返回", QMessageBox.HelpRole)
            ret = msg.exec_()

            if ret == 0:  # 保存并退出
                self.save_server_config()
            elif ret == 1:  # 不保存退出
                self.stacked_widget.setCurrentIndex(0)
            else:  # 返回
                return
        else:
            self.stacked_widget.setCurrentIndex(0)



if __name__ == "__main__":
    check_hardware()
    app = QApplication(sys.argv)
    app_font = QFont("Microsoft YaHei")
    app.setFont(app_font)
    window = ServerDeployWindow()
    window.show()
    sys.exit(app.exec_())
