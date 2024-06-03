# coding:utf-8

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout

from qfluentwidgets import (MSFluentTitleBar, TransparentToolButton, isDarkTheme, SearchLineEdit)
from qfluentwidgets import FluentIcon as FIF


class CustomTitleBar(MSFluentTitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # add buttons
        self.toolButtonLayout = QHBoxLayout()
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        # self.searchButton = TransparentToolButton(FIF.SEARCH_MIRROR.icon(color=color), self)
        self.pinButton = TransparentToolButton(FIF.PIN.icon(color=color), self)

        # add search line edit
        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setPlaceholderText('搜索内容')
        self.searchLineEdit.setFixedWidth(168)
        self.searchLineEdit.setClearButtonEnabled(True)
        # TODO 监控回车 或者按钮事件，否则文本不改变的情况下无法再次触发搜索
        self.searchLineEdit.textChanged.connect(self.search_text_changed)

        self.toolButtonLayout.setContentsMargins(10, 0, 0, 0)
        self.toolButtonLayout.setSpacing(15)
        self.toolButtonLayout.addWidget(self.searchLineEdit)
        self.toolButtonLayout.addWidget(self.pinButton)
        self.hBoxLayout.insertLayout(4, self.toolButtonLayout)

    def search_text_changed(self):
        text = self.searchLineEdit.text()
        self.parent.homeInterface.update_content(text)
        # add tab bar
        # self.tabBar = TabBar(self)
        #
        # self.tabBar.setMovable(True)
        # self.tabBar.setTabMaximumWidth(220)
        # self.tabBar.setTabShadowEnabled(False)
        # self.tabBar.setTabSelectedBackgroundColor(QColor(255, 255, 255, 125), QColor(255, 255, 255, 50))
        # # self.tabBar.setScrollable(True)
        # # self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        #
        # self.tabBar.tabCloseRequested.connect(self.tabBar.removeTab)
        # self.tabBar.currentChanged.connect(lambda i: print(self.tabBar.tabText(i)))
        #
        # self.hBoxLayout.insertWidget(5, self.tabBar, 1)
        # self.hBoxLayout.setStretch(6, 0)

        # add avatar
        # self.avatar = TransparentDropDownToolButton('resource/shoko.png', self)
        # self.avatar.setIconSize(QSize(26, 26))
        # self.avatar.setFixedHeight(30)
        # self.hBoxLayout.insertWidget(7, self.avatar, 0, Qt.AlignRight)
        # self.hBoxLayout.insertSpacing(8, 20)

    # def canDrag(self, pos: QPoint):
    #     if not super().canDrag(pos):
    #         return False
    #
    #     pos.setX(pos.x() - self.tabBar.x())
    #     return not self.tabBar.tabRegion().contains(pos)
