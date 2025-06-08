from PySide6.QtWidgets import QWidget, QTableWidgetItem
from PySide6.QtCore import QThread  
from db_connection import get_connection
from ui.GP_ui import Ui_Form as Ui_MainForm
from windows.query_window import QueryWindow
import math
from decimal import Decimal
from measure import run_measure

class SimulateThread(QThread):
    def __init__(self):
        super().__init__()
        self._stop_requested = False

    def run(self):
        run_measure(self.should_stop)

    def stop(self):
        self._stop_requested = True

    def should_stop(self):
        return self._stop_requested

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.load_data_from_db()

        self.setWindowTitle("GP Sigma")
        
        self.ui.lineEdit_6.setText("COM 1")
        self.ui.lineEdit_13.setText("9600")
        # lineEdit_ocv_spec
        self.ui.lineEdit_14.setText("100")         

        self.ui.pushButton_6.clicked.connect(self.open_query_window) # Search   
        
        # start and stop meaursing
        self.ui.pushButton.clicked.connect(self.start_measure)
        self.ui.pushButton_2.clicked.connect(self.stop_measure)  
        
        self.query_window = None 
        self.sim_thread = None
        
        self.show()

    # Search 
    def open_query_window(self):
        if self.query_window is None:
            self.query_window = QueryWindow()
        self.query_window.show()
    
    # Start 
    def start_measure(self):
        if self.sim_thread and self.sim_thread.isRunning():
            print("Measurement already running.")
            return
        self.sim_thread = SimulateThread()
        self.sim_thread.start()
        
    # stop 
    def stop_measure(self):
        if self.sim_thread and self.sim_thread.isRunning():
            self.sim_thread.stop()
            self.sim_thread.wait()
            print("Measurement stopped.")

        
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
                self.ui.lineEdit_14.setText(f"{row_index + 1}")
                ocv_values.append(ocv)
                               
            mean_spec_sigma = Decimal("1.5") # mean under dashboard
            
            # Calculate OCV for average, max, min, standard deviation, deviation and Sigma
            if ocv_values:
                avg_ocv = sum(ocv_values) / len(ocv_values)                
                max_ocv = max(ocv_values)
                min_ocv = min(ocv_values)
                std_dev = math.sqrt(sum((x - avg_ocv) ** 2 for x in ocv_values) / len(ocv_values))
                deviation = max_ocv - min_ocv          
                new_ocv = avg_ocv - mean_spec_sigma * Decimal(std_dev)

                print(f"OCV → AVG: {avg_ocv:.4f}, MAX: {max_ocv:.4f}, MIN: {min_ocv:.4f}, STD: {std_dev:.4f}, DEV: {deviation:.4f}")
                
                self.ui.lineEdit_9.setText(f"{max_ocv:.4f}")
                self.ui.lineEdit_8.setText(f"{avg_ocv:.4f}")
                self.ui.lineEdit_7.setText(f"{min_ocv:.4f}")
                self.ui.lineEdit_12.setText(f"{std_dev:.4f}")  
                self.ui.lineEdit_10.setText(f"{deviation:.4f}")                 
                self.ui.lineEdit_11.setText(f"{new_ocv:.4f}")      
                
            # lineEdit Conclusion                

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Failed to load data from database: {e}")
            
    def closeEvent(self, event):
        if self.sim_thread and self.sim_thread.isRunning():
            self.sim_thread.stop()
            self.sim_thread.wait()
        event.accept()
