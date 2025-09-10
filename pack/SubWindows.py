from PyQt6.QtWidgets import QMainWindow, QWidget, QTextEdit, QPushButton
from PyQt6.QtCore import QRect, pyqtSignal



class SubWindow_alterData(QMainWindow):

    def __init__(self,tips:str, parent:QWidget=None):
        input_sig = pyqtSignal(str)
        
        super().__init__(parent)
        self.__edit_area = QTextEdit(str(tips),self)
        self.__edit_area.setGeometry(QRect(self.width()//5,self.height()//3,(self.width()-2*self.width()//5)),(self.height()-2*self.height()//3))
        self.__edit_area.show()
        self.__sure_button = QPushButton("OK",self)
        self.__sure_button.setGeometry(QRect((self.width()-2*self.width()//3),(2*self.height()//3+self.height()//12),(self.width()-2*self.width()//3),(self.height()//3-2*self.height()//12)))
        self.__sure_button.show()
