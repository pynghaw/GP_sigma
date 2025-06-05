from PySide6.QtWidgets import QWidget
from ui.setup_xtopup_ui import Ui_SetupXTopupForm

class SetupXTopupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SetupXTopupForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Setting - Without Topup")