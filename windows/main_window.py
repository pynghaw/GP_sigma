from PySide6.QtWidgets import QWidget, QTableWidgetItem
from db_connection import get_connection
from ui.GP_ui import Ui_Form as Ui_MainForm
from windows.query_window import QueryWindow
import math

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
            
            ocv_values = []

            for row_index, (id, ri, ocv) in enumerate(rows):
                self.ui.tableWidget.setItem(row_index, 0, QTableWidgetItem(str(id)))
                self.ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(str(ri)))
                self.ui.tableWidget.setItem(row_index, 2, QTableWidgetItem(str(ocv)))
                ocv_values.append(ocv)
                
            # Calculate OCV for average, max, min, standard deviation, deviation and New???
            if ocv_values:
                avg_ocv = sum(ocv_values) / len(ocv_values)
                max_ocv = max(ocv_values)
                min_ocv = min(ocv_values)
                std_dev = math.sqrt(sum((x - avg_ocv) ** 2 for x in ocv_values) / len(ocv_values))
                deviation = max_ocv - min_ocv

                print(f"OCV → AVG: {avg_ocv:.4f}, MAX: {max_ocv:.4f}, MIN: {min_ocv:.4f}, STD: {std_dev:.4f}, DEV: {deviation:.4f}")
                
                self.ui.lineEdit_9.setText(f"{max_ocv:.4f}")
                self.ui.lineEdit_8.setText(f"{avg_ocv:.4f}")
                self.ui.lineEdit_7.setText(f"{min_ocv:.4f}")
                self.ui.lineEdit_12.setText(f"{std_dev:.4f}")  
                self.ui.lineEdit_10.setText(f"{deviation:.4f}") 
                self.ui.lineEdit_11.setText("New OCV value")  

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Failed to load data from database: {e}")