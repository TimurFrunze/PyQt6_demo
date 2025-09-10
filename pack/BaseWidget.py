from PyQt6.QtWidgets import QWidget, QMainWindow
class BaseWidget(QMainWindow):
    def alter_background_color(self,color:str,text_color="black"):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.setObjectName("centralWidget")
        self.setStyleSheet(
            " #centralWidget {"+
            f" background-color: {color};"
            f" color: {text_color};"
            "}"
        )
    def __init__(self,width=800,height=600,title:str="",parent=None):
        super().__init__(parent=parent)
        super().setFixedWidth(width)
        super().setFixedHeight(height)
        super().setWindowTitle(title)
        self.minimum_width = width
        self.minimum_height = height