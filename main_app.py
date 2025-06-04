import sys
from PySide6.QtWidgets import QApplication, QWidget
from ui.GP_ui import Ui_Form as Ui_MainForm
from ui.Query_ui import Ui_QueryForm  
from ui.setup_topup_ui import Ui_SetupTopupForm
from ui.setup_xtopup_ui import Ui_SetupXTopupForm

class QueryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QueryForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Record")

        self.ui.pushButton_3.clicked.connect(self.open_setup_xtopup_window)
        self.ui.pushButton_4.clicked.connect(self.open_setup_topup_window)

        self.topup_window = None
        self.xtopup_window = None

        self.show()

    def open_setup_topup_window(self):
        if self.topup_window is None:
            self.topup_window = SetupTopupWindow()
        self.topup_window.show()

    def open_setup_xtopup_window(self):
        if self.xtopup_window is None:
            self.xtopup_window = SetupXTopupWindow()
        self.xtopup_window.show()

        
class SetupTopupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SetupTopupForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Setting - With Topup")
        
class SetupXTopupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SetupXTopupForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Setting - Without Topup")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.setWindowTitle("GP Sigma")

        self.ui.pushButton_6.clicked.connect(self.open_query_window)

        self.query_window = None 
        self.show()

    def open_query_window(self):
        if self.query_window is None:
            self.query_window = QueryWindow()
        self.query_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
