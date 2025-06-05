from PySide6.QtWidgets import QWidget
from ui.Query_ui import Ui_QueryForm
from windows.setup_topup_window import SetupTopupWindow
from windows.setup_xtopup_window import SetupXTopupWindow

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

    # With topup button
    def open_setup_topup_window(self):
        if self.topup_window is None:
            self.topup_window = SetupTopupWindow()
        self.topup_window.show()

    # Without topup button
    def open_setup_xtopup_window(self):
        if self.xtopup_window is None:
            self.xtopup_window = SetupXTopupWindow()
        self.xtopup_window.show()