from PySide6.QtWidgets import QWidget, QTableWidgetItem
from PySide6.QtCore import QDate
from ui.Query_ui import Ui_QueryForm
from windows.setup_topup_window import SetupTopupWindow
from windows.setup_xtopup_window import SetupXTopupWindow
from db_connection import get_connection

class QueryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_QueryForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Record")
        self.load_list(all_data=True)
        
        self.ui.dateEdit.setDate(QDate.currentDate())
        
        # search, all button
        self.ui.pushButton.clicked.connect(self.load_list)
        self.ui.pushButton_2.clicked.connect(lambda: self.load_list(all_data=True))

        # top up and exit button
        self.ui.pushButton_3.clicked.connect(self.open_setup_xtopup_window)
        self.ui.pushButton_4.clicked.connect(self.open_setup_topup_window)
        self.ui.pushButton_6.clicked.connect(self.close)

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
        
    def load_list(self, all_data=False):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            date = self.ui.dateEdit.date().toPython()  
            model = self.ui.lineEdit.text().strip()
            lotno = self.ui.lineEdit_2.text().strip()

            # Base query
            query = """
                SELECT 
                    mo.model_no, 
                    l.lot_no, 
                    l.sample_qty, 
                    l.machine_no, 
                    l.std_deviation, 
                    l.sigma, 
                    l.sampling_date
                FROM lots l
                JOIN machines ma ON l.machine_no = ma.machine_no
                JOIN models mo ON ma.model_no = mo.model_no
            """
            conditions = []
            params = []

            if not all_data:
                if model:
                    conditions.append("mo.model_no ILIKE %s")
                    params.append(f"%{model}%")

                if lotno:
                    conditions.append("l.lot_no ILIKE %s")
                    params.append(f"%{lotno}%")

                if date:
                    conditions.append("DATE(l.sampling_date) = %s")
                    params.append(date)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY l.sampling_date DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()
            self.ui.tableWidget.setRowCount(0)

            for row_index, row_data in enumerate(rows):
                self.ui.tableWidget.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error loading filtered data: {e}")
