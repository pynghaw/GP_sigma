from PySide6.QtWidgets import QWidget
from ui.setup_topup_ui import Ui_SetupTopupForm

class SetupTopupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SetupTopupForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Setting - With Topup")