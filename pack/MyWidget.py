import os
from PyQt6.QtCore import QRect,Qt,pyqtSignal,pyqtSlot,QObject
from PyQt6.QtGui import QFont,QFontDatabase,QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton
from BaseWidget import *
from MenuWidget import MenuWidget
from threading import Thread, Lock

'''
开始界面：创建新笔记，打开笔记目录，设置
目录界面：打开笔记(读写)，删除笔记，允许打开多个笔记界面同时进行编辑
    是否上传云端(本地只存储笔记名字)
编辑界面：标题框，编辑框，保存按键(本地保存)
    允许在目录页中打开多个编辑页面，每一个页面是一个单独的线程？
打开笔记：将.db文件中的文本内容重新加载到界面中(是否可以进行文本压缩？)
    (还是直接存储文本？)
    (如何做出Typora的高亮和语法效果？)
'''

class MyWidget(BaseWidget):

    __font_family = None
    __font_comma=None
    __init_graph_list=[]
    def __graph__init(self):
        path1=os.path.join("..","graphics","graphic02.png")
        path2=os.path.join("..","graphics","graphic03.png")
        path3=os.path.join("..","graphics","graphic04.png")
        self.__init_graph_list.append(QPixmap(path1))
        self.__init_graph_list.append(QPixmap(path2))
        self.__init_graph_list.append(QPixmap(path3))

    def __font_init(self):
        font_path = os.path.join("..","fonts","ShanHaiHeiQiShiGeTeW.ttf")
        font_id=QFontDatabase.addApplicationFont(font_path)
        if font_id==-1:
            print("字体加载失败！")
        else:
            self.__font_family=QFontDatabase.applicationFontFamilies(font_id)
            if not self.__font_family:
                print("字体添加失败！")
    def __font_init_comma(self):
        font_path = os.path.join("..","fonts","MFYuYue_Noncommercial.otf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("字体加载失败")
        else:
            self.__font_comma=QFontDatabase.applicationFontFamilies(font_id)
            if not self.__font_comma:
                print("字体加载失败")

    def __create_EditWindow(self):
        pass

    def __init__(self,width:int,height:int,parent=None):
        super().__init__(width,height,"TIMUR NOTE++",parent)
        self.alter_background_color("#F5F5DC")
        #新笔记创建按键
        self.enter_butt = QPushButton("新建笔记",self)
        self.enter_butt.setGeometry(QRect((self.minimum_width-100)//2, self.minimum_height//2, self.minimum_width//8, self.minimum_height//20))
        self.enter_butt.setObjectName("EnterButton")
        self.enter_butt.setStyleSheet(
            "#EnterButton{"
            "   background-color: #F0E68C;"
            "   color: black;"
            "}"
        )
        self.__font_init()
        costume=QFont(self.__font_family,18)
        self.enter_butt.setFont(costume)
        self.enter_butt.show()
        #进入笔记目录按键
        self.__menu_button = QPushButton("笔记历史",self)
        self.__menu_button.setFont(costume)
        self.__menu_button.setGeometry(QRect((self.minimum_width-100)//2,(self.minimum_height//2+self.minimum_height//20),self.minimum_width//8, self.minimum_height//20))
        self.__menu_button.setObjectName("MenuButton")
        self.__menu_button.setStyleSheet(
            "#MenuButton{"
            "   background-color: #F0E68C;"
            "   color: black;"
            "}"
        )
        self.__menu_button.show()
        #中央大标题
        self.__central_text=QLabel("TIMUR NOTE++",self)
        self.__central_text.setObjectName("CentralText")
        self.__central_text.setStyleSheet(
            "#CentralText{"
            "color: black;"
            "}"
        )
        self.__central_text.setGeometry(QRect(0,0,self.minimum_width,self.minimum_height//2))
        comma=QFont(self.__font_comma,50)
        self.__central_text.setFont(comma)
        self.__central_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__central_text.show()
        #“设置”按键
        self.__setting_button=QPushButton("Settings",self)
        self.__setting_button.setGeometry(QRect(0,30,self.minimum_width//8,self.minimum_height//20))
        self.__setting_button.setObjectName("SettingButton")
        self.__setting_button.setStyleSheet(
            "#SettingButton"
            "{"
            "   background-color: #F5F5DC;"
            "   color: black;"
            "}"
        )
        self.__setting_button.show()
        #笔记目录页
        self.__MenuWindow=None

        #设置编辑区队列，每一个编辑区对应一个线程
        #关闭的编辑区线程放进队列中缓存，队列满后将最近最少使用的线程删除
        self.__thread_queue=[]
        '''
        LRU线程队列：(尾部为最新)
            打开的窗口线程，如果id在队列中不存在，即将线程添加到队列尾部
            如果id在队列中存在，将线程替换到尾部
            打开新线程时如果队列已满，则将队首线程弹出并销毁
        '''