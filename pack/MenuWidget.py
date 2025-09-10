from PyQt6.QtWidgets import QMainWindow,QWidget
from BaseWidget import BaseWidget
class MenuWidget(BaseWidget):
    '''
    点击目录中的json文件标识，读取文件并通过文件配置初始化编辑器
    '''
    def __init__(self,width=800,height=600,title="Menu"):
        super().__init__(width,height,title)
        self.alter_background_color("#d9e8f7")
