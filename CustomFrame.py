# coding:utf-8
import os

from PyQt5.QtCore import Qt, QSize, QMimeData
from PyQt5.QtGui import QIcon, QColor, QContextMenuEvent, QClipboard, QFont, QTextCursor, QPalette, QPainter, QImage, \
    QPixmap, QWindow
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QListWidgetItem, QWidget, QLabel, QSizePolicy, QPushButton, QTextEdit, \
    QApplication, QGraphicsDropShadowEffect

from qfluentwidgets import (RoundMenu, Action, MenuAnimationType, InfoBar, InfoBarPosition, ListWidget, TextEdit,
                            PixmapLabel, ImageLabel)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar

from config import FilterType, DataType, IMAGE_FOLDER, IMAGE_TYPE
from tool import MonitorTextEdit
from pynput.keyboard import Key, Controller

from CustomWidgets import CustomWidgetItem, CustomListWidget


class PreviewWindow(QWidget):

    def __init__(self):
        super().__init__()
        # self.setTitleBar(StandardTitleBar(self))
        self.vBoxLayout = QHBoxLayout(self)
        # self.vBoxLayout.setContentsMargins(0, 80, 0, 0)
        self.setStyleSheet('PreviewWindow {background: white}')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 设置让边框空白区域变透明（不设置会导致边跨有白边）
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.vBoxLayout.setSpacing(0)
        self.item = None
        # self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        # self.setWindowTitle('Click Image 👇️🥵')
        # self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))

        # FIXME 边框阴影设置，会触发告警
        # self.effect_shadow = QGraphicsDropShadowEffect(self)
        # self.effect_shadow.setOffset(0, 0)  # 偏移
        # self.effect_shadow.setBlurRadius(10)  # 阴影半径
        # self.effect_shadow.setColor(Qt.blue)  # 阴影颜色
        # self.setGraphicsEffect(self.effect_shadow)

    def set_image(self, data):
        if self.item:
            self.vBoxLayout.removeWidget(self.item)
        filename = os.path.join(IMAGE_FOLDER, str(data['id']) + IMAGE_TYPE)
        pix_image = QPixmap(filename)
        self.item = ImageLabel()
        self.item.clicked.connect(self.close_image)
        self.item.setImage(pix_image)
        self.vBoxLayout.addWidget(self.item)

        self.setFixedSize(pix_image.size())

        # 让窗口置中
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.show()

        # 激活窗口（让窗口提升至最前端）
        self.activateWindow()
        self.raise_()

    def set_text(self, data):
        if self.item:
            self.vBoxLayout.removeWidget(self.item)

        self.item = QTextEdit()
        self.item.setReadOnly(True)
        # self.item.clicked.connect(self.close_image)
        if data['dataType'] == DataType.TEXT:
            self.item.setText(data['data'])
        elif data['dataType'] == DataType.HTML:
            self.item.setHtml(data['data'])
        self.vBoxLayout.addWidget(self.item)

        self.setFixedSize(QSize(860, 680))

        # 让窗口置中
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.show()

        # 激活窗口（让窗口提升至最前端）
        self.activateWindow()
        self.raise_()

    def close_image(self):
        self.hide()


class CustomFrame(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        # self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)
        # self.setAutoFillBackground(True)
        # setFont(self.label, 24)
        # self.label.setAlignment(Qt.AlignCenter)
        # self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.item_size = QSize(300, 95)
        self.listWidget = CustomListWidget(self)
        self.listWidget.setIconSize(self.item_size)
        self.listWidget.setSelectRightClickedRow(True)  # 点击右键也可以选中

        self.listWidget.itemClicked.connect(self.item_click)
        self.listWidget.itemDoubleClicked.connect(self.item_double_click)

        self.hBoxLayout.addWidget(self.listWidget)

        # self.listWidget.setContentsMargins(100,100, 100, 100)

        # self.setStyleSheet("QListWidgetItem{font-size: 28px;}")
        # self.listWidget.setStyleSheet("listWidgetItem{margin: 10, 10;}")
        self.hBoxLayout.setContentsMargins(5, 5, 8, 5)
        self.setObjectName(text.replace(' ', '-'))

        self.keyboard = Controller()

        # preview window
        self.preview_wind = PreviewWindow()

        self.init_signal()

    def init_signal(self):
        self.monitor_thread = MonitorTextEdit()

    def paste_clipboard(self, signal):
        # self.monitor_thread.stop()
        self.monitor_thread.send_signal.disconnect()
        # 按下CTRL + V键（表示粘贴）
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('v')
        self.keyboard.release('v')
        self.keyboard.release(Key.ctrl)
        # TODO 支持键盘输入模式

    def item_click(self, item: QListWidgetItem):
        # include left click and double click(exclude right click)
        # TODO item 选择问题，切换filter type的时候，item选择有问题
        _id = item.data(Qt.UserRole)
        data = [row for row in self.parent.history if row['id'] == _id]
        if data:
            # no need to update history and save data
            self.parent.save_demand = False

            data = data[0]
            if data['dataType'] == DataType.TEXT:
                self.parent.clipboard.setText(data['data'])
            elif data['dataType'] == DataType.IMAGE:
                self.parent.clipboard.setPixmap(data['data'])
            elif data['dataType'] == DataType.HTML:
                # mime_data = QMimeData()
                # mime_data.setHtml(data['data'])
                # mime_data.setData('text/plain', data['data'].encode('utf-8'))
                self.parent.clipboard.setText(data['text'])
                # FIXME HTML内容复制到剪切板无法粘贴！
                # self.parent.clipboard.setText(mime_data.text())

        # InfoBar.success(
        #     title='Copied',
        #     content="",
        #     orient=Qt.Horizontal,
        #     isClosable=False,
        #     position=InfoBarPosition.TOP,
        #     duration=1000,
        #     parent=self
        # )

        if not self.monitor_thread.isRunning():
            self.monitor_thread.send_signal.connect(self.paste_clipboard)
            self.monitor_thread.start()

    def item_double_click(self, item: QListWidgetItem):
        # double click will set content of the item to clipboard
        # print('double click')
        _id = item.data(Qt.UserRole)
        data = [row for row in self.parent.history if row['id'] == _id]
        if not data:
            raise Exception('No data can be found')
        row_data = data[0]
        if row_data['dataType'] == DataType.IMAGE:
            self.preview_wind.set_image(row_data)
        elif row_data['dataType'] in [DataType.TEXT, DataType.HTML]:
            self.preview_wind.set_text(row_data)
        # self.preview_wind.show()
        pass

    def update_content(self, search_by_text: str = None):
        _type = self.parent.filter_type
        history = self.parent.history
        self.listWidget.clear()
        if _type == FilterType.ALL:
            data_list = history.copy()
        else:
            data_list = [row for row in history if row['filterType'] == _type]

        if search_by_text:
            data_list = [row for row in data_list if
                         row['filterType'] == FilterType.TEXT and search_by_text.lower() in row['data'].lower()]

        for idx, row in enumerate(data_list[::-1]):
            _type = row['filterType']
            data = row['data']
            item = QListWidgetItem()
            item.setSizeHint(self.item_size)
            item.setBackground(QColor(254, 254, 254))
            item.setData(Qt.UserRole, row['id'])

            # if _type == FilterType.TEXT:
            #     item.setText(row['text'])
            #     self.listWidget.addItem(item)
            # elif _type == FilterType.IMAGE:
            #     scaled_pixmap = data.scaled(self.item_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            #     item.setIcon(QIcon(scaled_pixmap))
            #     item.setSelected(False)
            #     self.listWidget.addItem(item)

            custom_widget = CustomWidgetItem(row)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, custom_widget)

            # fonts = QFont()
            # fonts.setPointSize(10)
            # fonts.setWeight(30)
            # item.setFont(fonts)

        self.update()
