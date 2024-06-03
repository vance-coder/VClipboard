# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QHBoxLayout, QLabel

from qfluentwidgets import Action, SystemTrayMenu, MessageBox, setTheme, Theme


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setIcon(parent.windowIcon())
        self.setToolTip('test tool tip')

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action('打开', triggered=self.show_app),
            Action('退出', triggered=self.parent.exit_app),
        ])
        self.setContextMenu(self.menu)

    def show_app(self):
        print('显示程序')

# TODO 点击打开main window，左键两个菜单：打开，退出
# TODO 不显示任务栏窗口
