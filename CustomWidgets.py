# coding:utf-8
from PyQt5.QtCore import Qt, QSize, QMimeData
from PyQt5.QtGui import QIcon, QColor, QContextMenuEvent, QClipboard, QFont, QTextCursor, QPalette, QPainter
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QListWidgetItem, QWidget, QLabel, QSizePolicy, QPushButton, QTextEdit

from qfluentwidgets import (RoundMenu, Action, MenuAnimationType, InfoBar, InfoBarPosition, ListWidget, TextEdit,
                            PixmapLabel)
from qfluentwidgets import FluentIcon as FIF

from config import FilterType, DataType
from tool import MonitorTextEdit
from pynput.keyboard import Key, Controller


class CustomWidgetItem(QWidget):
    def __init__(self, row_data: dict):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.item_size = QSize(300, 95)
        self.setFixedSize(self.item_size)
        self.row_data = row_data
        self.text_edit_qss = "QTextEdit {border:none;}"
        # self.setFont(QFont("Arial", 32))

        if self.row_data['dataType'] == DataType.IMAGE:
            self.item = QLabel()
            scaled_pixmap = self.row_data['data'].scaled(self.item_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.item.setPixmap(scaled_pixmap)
            self.item.setAlignment(Qt.AlignLeft)
            # self.item.setEnabled(True)
            # self.item.setStyleSheet("QLabel:disabled {background-color: transparent;}")
            # self.item.setForegroundRole(QPalette.Disabled, QColor(0, 0, 0, 0))
            # QLabel 设置disable会导致变灰色

        elif self.row_data['dataType'] == DataType.HTML:
            self.item = QTextEdit()
            self.item.setReadOnly(True)
            self.item.setCursor(Qt.ArrowCursor)
            self.item.setHtml(self.row_data['data'])
            self.item.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.item.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setStyleSheet(self.text_edit_qss)
            self.item.setFont(QFont("Arial", 11))
            # self.item.setAutoFormatting(QTextEdit.AutoAll)
            # self.item.setFontPointSize(30)
            # self.item.setFontWeight(50)
            # self.item.setFontFamily('Console')
            # 这样可以禁用鼠标所有事件(目的是为了保留上一层QListWidget的鼠标事件)
            # FIXME disabled后，字体变灰色了
            self.setDisabled(True)
            self.setStyleSheet("QWidget:disabled {background-color: transparent;border:none}")
        elif self.row_data['dataType'] == DataType.TEXT:
            self.item = QTextEdit()
            self.item.setReadOnly(True)
            self.item.setCursor(Qt.ArrowCursor)
            self.item.setText(self.row_data['data'])
            self.item.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.item.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setStyleSheet(self.text_edit_qss)
            self.item.setFont(QFont("Arial", 11))
            # self.item.setAutoFormatting(QTextEdit.AutoAll)
            # 这样可以禁用鼠标所有事件(目的是为了保留上一层QListWidget的鼠标事件)
            self.setDisabled(True)
            self.setStyleSheet("QWidget:disabled {background-color: transparent;border:none}")
            # self.item.setFontPointSize(30)
            # self.item.setFontWeight(50)
            # self.item.setFontFamily('Console')


        # self.layout.add
        self.layout.addWidget(self.item)

        # self.setBackgroundRole(QPalette.Foreground)
        # self.setForegroundRole(QPalette.Background)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        # 不起作用
        # print(self.item.setEnabled(True))
        # print(self.item.isEnabled())

        # self.image_label = QLabel()
        # self.image_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.layout.addWidget(self.image_label)

        # button_layout = QHBoxLayout()
        # self.button = QPushButton(button_text)
        # self.button.clicked.connect(self.on_button_clicked)
        # button_layout.addWidget(self.button)
        # self.layout.addLayout(button_layout)

        # self.text_label = QLabel(text)
        # self.text_label.setAlignment(Qt.AlignCenter)
        # self.layout.addWidget(self.text_label)
        #
        # self.text_edit = TextEdit()
        # self.text_edit.setText('Demoxxxx')
        #
        # self.layout.addWidget(self.text_edit)            self.setFocusPolicy(Qt.NoFocus)


class CustomListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu()
        self.parent = parent
        self.select_item = None

    def contextMenuEvent(self, event: QContextMenuEvent):
        item = self.itemAt(event.pos())
        if not item:
            # No action if outside the Item position
            return
        self.select_item = item
        # 显示上下文菜单
        self.menu.exec_(event.globalPos(), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)

    def init_menu(self):
        self.menu = RoundMenu(self)

        up_action = Action(FIF.UP, "置顶")
        modify_action = Action(FIF.EDIT, "修改")
        delete_action = Action(FIF.DELETE, "删除")

        # 使用event.pos()获取相对于ListWidget的鼠标位置
        self.menu.addAction(up_action)
        self.menu.addAction(modify_action)
        self.menu.addSeparator()
        self.menu.addAction(delete_action)

        delete_action.triggered.connect(self.delete_action)

    def delete_action(self):
        data_id = self.select_item.data(Qt.UserRole)
        self.removeItemWidget(self.select_item)
        self.parent.parent.history = [row for row in self.parent.parent.history if row['id'] != data_id]
        self.parent.parent.save_history()
        self.parent.update_content()

        InfoBar.warning(
            title='Removed',
            content="",
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )

