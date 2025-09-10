from PyQt6.QtWidgets import QApplication
import sys
from MyWidget import *
from EditWidget import *
app = QApplication(sys.argv)
# window=MyWidget(1000,800)
# window.show()
window = EditWidget()
window.show()
sys.exit(app.exec())