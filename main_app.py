import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from db_connection import get_connection
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
        self.load_data_from_db()

        self.setWindowTitle("GP Sigma")

        self.ui.pushButton_6.clicked.connect(self.open_query_window)

        self.query_window = None 
        self.show()

    # Search button
    def open_query_window(self):
        if self.query_window is None:
            self.query_window = QueryWindow()
        self.query_window.show()
        
    # RI OCV table
    def load_data_from_db(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, ri, ocv FROM hioki_measurements ORDER BY id ASC")
            rows = cursor.fetchall()

            self.ui.tableWidget.setRowCount(len(rows))
            self.ui.tableWidget.setColumnCount(3)

            for row_index, (id, ri, ocv) in enumerate(rows):
                self.ui.tableWidget.setItem(row_index, 0, QTableWidgetItem(str(id)))
                self.ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(str(ri)))
                self.ui.tableWidget.setItem(row_index, 2, QTableWidgetItem(str(ocv)))

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Failed to load data from database: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
