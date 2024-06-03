# coding:utf-8
import sys
import logging
import time
from datetime import datetime

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget

from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentWindow, InfoBar, InfoBarPosition,
                            NavigationBarPushButton)
from qfluentwidgets import FluentIcon as FIF

from CustomFrame import CustomFrame
from GitProject.VClipboardLocal.CustomTray import SystemTrayIcon
from TitleBar import CustomTitleBar

from data_helper import save_data, load_data
from config import FilterType, DataType


class Window(MSFluentWindow):

    def __init__(self):
        self.isMicaEnabled = False

        super().__init__()

        # if need to save clipboard data to disk and update history list
        self.save_demand = True
        # current filter by which datatype
        self.filter_type = FilterType.ALL

        self.setTitleBar(CustomTitleBar(self))
        # self.tabBar = self.titleBar.tabBar  # type: # TabBar
        self.history = load_data()
        self.previous_data = None

        # self.stackWidget = QStackedWidget(self)

        # create sub interface
        # self.homeInterface = QStackedWidget(self, objectName='homeInterface')
        self.homeInterface = CustomFrame('ALL Interface', self)
        self.settingInterface = CustomFrame('Setting Interface', self)

        # Clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard.changed.connect(self.update_history)
        # self.clipboard.setText()

        # 窗口置顶
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint )
        # | Qt.SplashScreen
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint )
        # self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        # 取消最大化
        # self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

        # 禁止大小调整
        # self.setWindowFlags(self.windowFlags() & Qt.MSWindowsFixedSizeDialogHint)

        self.initNavigation()
        self.initWindow()

        # init Item
        self.homeInterface.update_content()

        # 启动system tray
        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()

        # 设置日志
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def exit_app(self):
        sys.exit(0)

    def switchTo(self, interface: QWidget):
        # 重写navigationInterface函数里面调用的switchTo以刷新界面
        super().switchTo(interface)
        self.switch_type(_type=FilterType.ALL)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.MENU, 'ALL')

        text_nvg_btn: NavigationBarPushButton = self.navigationInterface.addItem(routeKey='text',
                                                                                 icon=FIF.DOCUMENT,
                                                                                 text='文本',
                                                                                 onClick=lambda: self.switch_type(
                                                                                     FilterType.TEXT))
        self.navigationInterface.addItem(routeKey='image', icon=FIF.PHOTO, text='图片',
                                         onClick=lambda: self.switch_type(FilterType.IMAGE))
        self.navigationInterface.addItem(routeKey='link', icon=FIF.LINK, text='链接',
                                         onClick=lambda: self.switch_type(FilterType.LINK))
        self.navigationInterface.addItem(routeKey='table', icon=FIF.CALENDAR, text='表格',
                                         onClick=lambda: self.switch_type(FilterType.TABLE))
        self.navigationInterface.addItem(routeKey='password', icon=FIF.HIDE, text='密码',
                                         onClick=lambda: self.switch_type(FilterType.PASSWORD))
        self.navigationInterface.addItem(routeKey='code', icon=FIF.COMMAND_PROMPT, text='代码',
                                         onClick=lambda: self.switch_type(FilterType.CODE))

        self.addSubInterface(self.settingInterface, FIF.SETTING,
                             '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)

        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(
            self.homeInterface.objectName())

        # add tab
        # self.addTab('Heart', 'As long as you love me', icon='resource/Heart.png')

        # self.tabBar.currentChanged.connect(self.onTabChanged)
        # self.tabBar.tabAddRequested.connect(self.onTabAddRequested)

    def initWindow(self):
        self.resize(488, 680)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('VClipBoard')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(int(w // 1.2) - self.width() // 2, h // 2 - self.height() // 2)

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))

    def save_history(self):
        save_data(self.history)

    def get_content_from_clipboard(self):
        now = int(time.time())
        _time = str(datetime.fromtimestamp(now))
        content = {
            'id': now,
            'time': _time,
        }
        mime_data = self.clipboard.mimeData()
        # TODO mime data format study
        # print('data format:', mime_data.formats())
        # print(mime_data.data())
        # mime_data.setData()
        try:
            if mime_data.hasImage():
                content['filterType'] = FilterType.IMAGE
                content['data'] = QPixmap.fromImage(self.clipboard.image())
                content['dataType'] = DataType.IMAGE
                content['text'] = ''
            elif mime_data.hasHtml():
                content['filterType'] = FilterType.TEXT
                content['data'] = mime_data.html()
                content['dataType'] = DataType.HTML
                content['text'] = mime_data.text()
            elif mime_data.hasText():
                content['filterType'] = FilterType.TEXT
                content['data'] = mime_data.text()
                content['dataType'] = DataType.TEXT
                content['text'] = mime_data.text()
            else:
                raise Exception('No content in clipboard')
        except Exception as e:
            logging.error(f"Error processing clipboard data: {e}")

        return content

    def switch_type(self, _type):
        self.filter_type = _type
        self.homeInterface.update_content()

    def remove_item_from_history(self, _id):
        self.history = [row for row in self.history if row['id'] != _id]
        self.update_history()

    def update_history(self):
        if self.save_demand is False:
            self.save_demand = True
            return

        content = self.get_content_from_clipboard()

        if content['filterType'] == FilterType.TEXT:
            # 重复内容不再添加
            if self.previous_data == content['data']:
                return
            self.previous_data = content['data']

        self.history.append(content)  # 将新内容添加到历史列表
        # save data
        self.save_history()

        # update interface
        self.homeInterface.update_content()


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()

