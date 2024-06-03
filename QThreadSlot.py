import sys
import time

from PyQt5.QtCore import QDateTime, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QDialog


class my_thread(QThread):
    send_signal = pyqtSignal(str)
    stop_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._stop = False

    def stop(self):
        self._stop = True
        self.stop_requested.emit()

    def run(self):
        while not self._stop:
            print('干活中')
            date = QDateTime.currentDateTime()
            current_time = date.toString("yyyy-MM-dd hh:mm:ss")
            self.send_signal.emit(current_time)
            time.sleep(1)
        # self.quit()  # 退出run循环后，线程会结束



class custom_window(QDialog):

    def __init__(self):
        # 子类构造器调用父类的构造器有两种方式：
        # 1、父类名.__init__(self)
        # 2、super.__init__(self)
        QDialog.__init__(self)
        self.sum = 0
        self.init_ui()

    def init_ui(self):

        # 设置主窗口大小
        self.setGeometry(500, 1000, 500, 500)

        # 设置窗口名称
        self.setWindowTitle("时间流逝")

        # 创建文本框
        self.text_edit = QTextEdit()

        # 创建按钮
        self.switch_btn = QPushButton()
        self.switch_btn.setText("启动时间")

        # 创建垂直布局
        self.v_layout = QVBoxLayout(self)

        # 将按钮与文本框添加到垂直布局
        self.v_layout.addWidget(self.text_edit)
        self.v_layout.addWidget(self.switch_btn)

        self.total_signal()

    def total_signal(self):
        # 实例化线程类
        self.myThread = my_thread()
        # self.myThread.send_signal.connect(self.switch_slot)
        # self.myThread.stop_requested.connect(self.myThread.stop)
        # 单击按钮, 以单击为发送信号
        self.switch_btn.clicked.connect(self.on_clicked)

    # 单击按钮的槽
    def on_clicked(self):
        print(self.myThread.isRunning())
        self.sum += 1
        if self.sum % 2 == 0:
            self.myThread.stop()
            self.myThread.send_signal.disconnect(self.switch_slot)
            self.myThread = my_thread()
            # self.myThread.stop_requested.connect(self.myThread.stop)  # 添加这行来连接停止信号
            self.switch_btn.setText("重新启动")
        else:
            self.myThread.send_signal.connect(self.switch_slot)
            # self.myThread.stop_requested.disconnect(self.myThread.stop)  # 添加这行来断开停止信号
            self.switch_btn.setText("关闭连接")
            self.myThread.start()

    # 连接信号的槽
    def switch_slot(self, text):
        # 追加文本到文本框
        self.text_edit.append(text)


if __name__ == "__main__":
    # 每个Qt的GUI程序必须的类, sys.argv表示空列表
    app = QApplication(sys.argv)

    # 创建窗口实例
    main_win = custom_window()
    # 展示窗口
    main_win.show()

    # 关闭窗口
    sys.exit(app.exec_())
