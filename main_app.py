import sys
from PySide6.QtWidgets import QApplication, QWidget
from GP_ui import Ui_Form 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
     
        self.ui = Ui_Form()
       
        self.ui.setupUi(self) 

        self.setWindowTitle("GP Sigma") 
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())