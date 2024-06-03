# 根据时间来管理
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPixmap
import sys

app = QApplication(sys.argv)


def get_clipboard_content():
    clipboard = app.clipboard()

    pixmap = clipboard.pixmap()
    text_data = clipboard.text()

    if not pixmap.isNull():
        image = QImage(pixmap.toImage())
        return image
    if text_data:
        return text_data
    return None


# 使用函数
image = get_clipboard_content()
if image:
    # 这里可以处理图像，例如保存或显示
    print("剪贴板中有图像数据。", image)
else:
    print("剪贴板中没有图像数据。")


# TODO
"""
save content，text -> sqliteDB, image -> sqliteDB （fuzzy search / search by text/date）
1. while True, text print/image print summary
2. text classification, categories: 
- 普通文本
- 密码类
- 代码类
- 配置类 /json/dict/yaml/ini etc
- 表格类
- 图片
- 链接

GUI（自定义快捷键）
调出界面，不会丢失焦点？


根据内容自动拆分，填写表单

复制一段list，拆分后， ctr+p,亮起选择界面，选择，当鼠标进入文本状态，自动粘贴

image -> text -> split -> input

文本编辑功能：
替换功能，替换后再使用等需求

# 加入标记，比如英文笔记等，然后可以回顾英文
"""
