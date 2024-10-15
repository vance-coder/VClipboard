import sys

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (MSFluentTitleBar, TransparentToolButton, isDarkTheme, InfoBar,
                            InfoBarPosition, ListWidget, LineEditButton, ComboBox, LineEdit, SearchLineEdit,
                            TransparentPushButton, FluentIcon, FluentIconBase, TransparentDropDownPushButton,
                            SplitPushButton, RoundMenu, Action, SplitToolButton, TransparentDropDownToolButton)
from qfluentwidgets import FluentIcon as FIF

from enum import Enum
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig

from qfluentwidgets import FluentWindow, isDarkTheme, MSFluentWindow
from qframelesswindow import FramelessWindow


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QHBoxLayout(self)
        self.vBoxLayout.setSpacing(0)

        # self.setStyleSheet('MainWindow {background: white}')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # 设置让边框空白区域变透明（不设置会导致边跨有白边）
        # self.setAttribute(Qt.WA_TranslucentBackground)

        line_edit = SearchLineEdit(self)

        # Font size
        fonts = QFont()
        fonts.setPointSize(14)
        fonts.setWeight(28)
        line_edit.setFont(fonts)

        # 设置内置的图标大小
        line_edit.searchButton.setIconSize(QSize(15, 15))
        line_edit.searchSignal.connect(lambda text: print("搜索：" + text))
        line_edit.setFixedWidth(640)
        line_edit.setFixedHeight(42)
        # line_edit.setClearButtonEnabled(True)

        # button = TransparentDropDownToolButton(FluentIcon.MAIL, 'Email')
        button = TransparentDropDownToolButton(
            QIcon(r'D:\PythonProject\tmp\Jamscreenshot-master\images\1690984151.png'), 'Email')
        button.setIconSize(QSize(52, 52))
        button.setFixedWidth(62)
        button.setFixedHeight(58)
        # 创建菜单
        menu = RoundMenu(parent=button)
        menu.addAction(Action(FluentIcon.DOCUMENT, 'Send', triggered=lambda: print("已发送")))
        menu.addAction(Action(FluentIcon.SAVE, 'Save', triggered=lambda: print("已保存")))

        # 添加菜单
        button.setMenu(menu)

        # comboBox = ComboBox()
        # comboBox.setFixedWidth(120)
        # comboBox.setFixedHeight(42)
        # items = ['FileSearch', 'Chrome', 'Edge', 'CMD']
        # # TransparentPushButton(FluentIcon.BOOK_SHELF, 'Transparent push button')
        # # TransparentPushButton(QIcon("/path/to/icon.png"), 'Transparent push button')
        # comboBox.addItem('FileSearch', FluentIcon.SEARCH_MIRROR)
        # comboBox.addItem('Chrome', FluentIcon.PHOTO)
        # comboBox.addItem('Edge', FluentIcon.CHAT)
        # comboBox.addItem('CMD', FluentIcon.FILTER)

        self.vBoxLayout.addWidget(button, 0, Qt.AlignLeft)

        # line_edit.hBoxLayout.addWidget(comboBox, 1, Qt.AlignLeft)

        self.vBoxLayout.addWidget(line_edit)

        # 让窗口置中
        # desktop = QApplication.desktop().availableGeometry()
        # w, h = desktop.width(), desktop.height()
        # self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        # self.show()
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Tab:
            print('Tab key pressed')
        else:
            print(event.key())


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()

# 1. 监控tab按键

# TODO 自动加载存在的浏览器
# 加载CMD图标
