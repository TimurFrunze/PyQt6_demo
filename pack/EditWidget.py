from PyQt6.QtWidgets import QWidget, QTextEdit, QMenu, QMenuBar, QScrollArea, QVBoxLayout, QSizePolicy, \
    QFrame
from PyQt6.QtCore import QRect, Qt, pyqtSignal
from PyQt6.QtGui import QFontDatabase, QKeyEvent, QAction, QFont
from BaseWidget import *
import os
'''
json模块：
    "title":"xxx",
    "width":800,
    "height":600,
    "background_color":"default",
    "font":"default",
    "font_size":"default",
    "font_color":"default",
    "main_title":{"content":(x,y,w,h),...},
    "sub_title":{"content":(x,y,w,h),...},
    "textbox":{"content":(x,y,w,h),...},
    
'''

'''
按键类型：
    1.修改背景色
    2.修改字体颜色
    3.添加:大标题，副标题，文本框，(代码框?)
    4.字体大小
    5.修改字体
'''

'''
1.点击按键触发特定json修改，并改变控件状态
2.修改已有控件的内容(并点击保存?),触发json修改(控件名称作为索引，在同类控件中字典查找)
3.退出时自动保存配置
4.从菜单页面中点击"noteName.json"，自动将笔记配置加载进页面(读入json，加载成python字典)
'''

class EditWidget(BaseWidget):
    __font = None
    __Jetbrains_Font = None
    signal_save_text = pyqtSignal() #触发即保存到:memory:
    signal_back_MainWindow = pyqtSignal() #点击返回，触发
    def __JetBrains_font_init(self):
        font_path=os.path.join("..","fonts","MapleMono_Bold.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("unable to find MapleMono_Bold.ttf")

        else:
            self.__Jetbrains_Font=QFontDatabase.applicationFontFamilies(font_id)
            if not self.__Jetbrains_Font:
                print("unable to load MapleMono_Bold.ttf")

    def keyPressEvent(self,event: QKeyEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key()==Qt.Key.Key_S:
            self.signal_save_text.emit()
            event.accept()
        else:
            super().keyPressEvent(event)

    def alter_font_size(self,font_size:int):
        pass

    def __init__(self,width=800,height=600,title="",parent=None):
        super().__init__(width,height,title,parent)
        self.alter_background_color("#F7EDE2")
        self.__JetBrains_font_init()
        self.__menu_bar = QMenuBar(self)
        self.__menu_bar.setObjectName("bar1")
        self.__menu_bar.setStyleSheet("#bar1{"
                                      "background-color:grey;"
                                      "}")
        alter_width = QAction("Width",self)
        alter_width.setStatusTip("Set width")
        alter_height = QAction("Height",self)
        alter_height.setStatusTip("Set height")
        alter_font_size = QAction("Font Size",self)
        alter_font_size.setStatusTip("Set font size")
        alter_font_color = QAction("Font Color",self)
        alter_font_color.setStatusTip("Set font color")
        alter_background_color = QAction("Background Color",self)
        alter_background_color.setStatusTip("Set background color")
        add_text = QAction("Add Text",self)
        add_text.setStatusTip("Add text")
        add_main_title = QAction("Add Main Title",self)
        add_main_title.setStatusTip("Add main title")
        add_sub_title = QAction("Add Sub Title",self)
        add_sub_title.setStatusTip("Add sub title")
        save_text = QAction("Save Text",self)
        save_text.setStatusTip("Save text")
        self.__menu = QMenu("Edit",self.__menu_bar)
        self.__menu.addAction(alter_width)
        self.__menu.addSeparator()
        self.__menu.addAction(alter_height)
        self.__menu.addSeparator()
        self.__menu.addAction(alter_font_size)
        self.__menu.addSeparator()
        self.__menu.addAction(alter_font_color)
        self.__menu.addSeparator()
        self.__menu.addAction(alter_background_color)
        self.__menu.addSeparator()
        self.__menu.addAction(add_text)
        self.__menu.addSeparator()
        self.__menu.addAction(add_main_title)
        self.__menu.addSeparator()
        self.__menu.addAction(add_sub_title)
        self.__menu.addSeparator()
        self.__menu.addAction(save_text)
        self.__menu.addSeparator()
        self.__menu_bar.addMenu(self.__menu)
        self.__menu_bar.setGeometry(QRect(0,0,self.minimum_width,self.minimum_height//30))
        self.__menu.setGeometry(QRect(0,0,self.__menu_bar.width()//20,self.__menu_bar.height()))
        self.__menu_bar.show()
        self.__menu.show()
        self.__font = QFont()
        self.__font.setFamily(self.__Jetbrains_Font)
        self.__editbox = QTextEdit(self)
        self.__editbox.setGeometry(QRect(self.minimum_width//40,self.minimum_height//20,(self.minimum_width-2*self.minimum_width//40),(self.minimum_height-2*self.minimum_height//30)))
        self.__editbox.setFrameShape(QFrame.Shape.Box)
        self.__editbox.setLineWidth(2)
        self.__editbox.show()