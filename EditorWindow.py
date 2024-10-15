import sys
import bisect
from random import randint
from PyQt5.QtCore import QSize, QEventLoop, QTimer
from PyQt5.QtGui import QIcon, QTextCursor, QTextCharFormat, QColor, QFont
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTextEdit
# coding:utf-8
from qfluentwidgets import SplashScreen
from qframelesswindow import FramelessWindow, StandardTitleBar

from MagicEditor import analyze_string


class MonitorTextEdit(QTextEdit):
    def __init__(self, index_list: list, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.index_list = index_list

    def mousePressEvent(self, event):
        # 首先调用父类的方法来处理事件
        super().mousePressEvent(event)
        # 然后可以添加自己的处理逻辑
        # 鼠标摁下后恢复文本状态
        format = QTextCharFormat()
        format.setBackground(QColor("white"))
        cursor = self.textCursor()
        cursor.setPosition(0)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(self.toPlainText()))
        cursor.mergeCharFormat(format)  # 改变文本的背景颜色

    def mouseReleaseEvent(self, event):
        # 首先调用父类的方法来处理事件
        super().mouseReleaseEvent(event)

        text_cursor = self.textCursor()
        current_selection_text = text_cursor.selectedText()
        sel_start = text_cursor.selectionStart()
        sel_end = text_cursor.selectionEnd()
        column_number = text_cursor.columnNumber()
        index_number = text_cursor.blockNumber()

        print(sel_start, sel_end, column_number, index_number)
        current_row = self.index_list[index_number]
        insert_idx = bisect.bisect_left(current_row, column_number)
        print(current_row, insert_idx)

        format = QTextCharFormat()
        format.setBackground(QColor('#CCCCCC'))

        sum_index = 0
        for idx, row in enumerate(self.index_list):
            # TODO 换行符 算一个位置
            if idx > 0:
                # sum_index是每行之后累计的index
                # +1是每行位都有一个换行符
                row = [sum_index + i + 1 for i in row]
            # index start with 0
            row = [sum_index + min(1, idx)] + row
            print(row)
            text_cursor.setPosition(row[insert_idx])
            text_cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, row[insert_idx + 1] - row[insert_idx])
            text_cursor.mergeCharFormat(format)
            sum_index = row[-1]


class Demo(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.resize(700, 600)
        self.setWindowTitle('PyQt-Fluent-Widgets')

        self.vBoxLayout = QHBoxLayout(self)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)

        with open('text.txt', encoding='utf-8') as fp:
            text = fp.read().strip()

        data, index_list = analyze_string(text)
        self.index_list = index_list
        print(index_list)

        self.textEdit = MonitorTextEdit(index_list)
        # errorFormat = '<font color="#333333" style="background-color:#CCCCCC;padding:20px"  size="12">{}</font>'
        # &nbsp;
        # errorFormat = '<font color="#333333" size="12">{}</font>'
        #
        # text_list = ['Vance-liu@139.com', '(ANPPQ4)', '-', 'A']
        # combine_text = '<font color="#CCCCCC" size="12">|</font>'.join([errorFormat.format(i) for i in text_list])
        # self.textEdit.append(combine_text)  # 该内容显示为红色

        self.textEdit.append(text)

        # text selection changed binding function
        # self.textEdit.selectionChanged.connect(self.selection_changed)
        # cursorPositionChanged function

        # color: 未选中时字体颜色
        # selection-color: 选中时字体颜色
        # background-color: 背景色
        # selection-background-color: 选中字体的背景色
        self.textEdit.setStyleSheet("selection-background-color: #CCCCCC;selection-color:black;")

        font = QFont('Arial', 16)
        self.textEdit.setFont(font)

        # textEdit.setMarkdown("## Steel Ball Run \n * Johnny Joestar 🦄 \n * Gyro Zeppeli 🐴 ")

        self.vBoxLayout.addWidget(self.textEdit)

        # current selection
        self.selection_text = ''

        # 2. 在创建其他子页面前先显示主界面
        self.show()

    def selection_changed(self):
        self.text_cursor = self.textEdit.textCursor()
        current_selection_text = self.text_cursor.selectedText()
        if self.selection_text != current_selection_text:
            # self.background_reset()
            self.selection_text = current_selection_text
            print('select text:', self.selection_text)
            print(self.text_cursor.selectionStart(), self.text_cursor.selectionEnd(),
                  self.text_cursor.columnNumber(), self.text_cursor.blockNumber())
            # 移除选中的文本
            # tc.removeSelectedText()
            # tx_cur = self.textEdit.textCursor()

            format = QTextCharFormat()
            format.setBackground(QColor('#CCCCCC'))

            for idx in [21, 46, 82]:
                self.text_cursor.setPosition(idx)
                self.text_cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, randint(4, 6))
                self.text_cursor.mergeCharFormat(format)

            # print(self.textEdit.toHtml())
            # self.textEdit.setTextCursor(tx_cur)
            # self.textEdit.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()

    # https://www.cnblogs.com/yinsedeyinse/p/10793143.html textEdit 文档

    # TODO 选中高亮，恢复颜色
