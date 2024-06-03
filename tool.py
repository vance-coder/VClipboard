import win32gui
import time
from PyQt5.QtCore import QThread, pyqtSignal
from pynput.mouse import Listener as MouseListener, Button


class MonitorTextEdit(QThread):
    send_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def on_click(self, x, y, button, pressed):
        cursor_infos = win32gui.GetCursorInfo()
        cursor_flag = cursor_infos[1]
        # 鼠标release并且 处于文本编辑状态
        # if button == Button.left and not pressed and cursor_flag == 65541:
        # 鼠标release左键 就粘贴
        if button == Button.left and not pressed:
            # 返回False表示结束run的join
            return False

    def run(self):
        with MouseListener(on_click=self.on_click) as listener:
            listener.join()
        self.send_signal.emit('Done')






