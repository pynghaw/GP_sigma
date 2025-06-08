from PySide6.QtWidgets import QWidget, QTableWidgetItem
from PySide6.QtCore import QThread  
from db_connection import get_connection
from ui.GP_ui import Ui_Form as Ui_MainForm
from windows.query_window import QueryWindow
import math
from measure import run_measure

ocv_values = []

class SimulateThread(QThread):
    def __init__(self, main_window):
        super().__init__()
        self._stop_requested = False
        self.main_window = main_window

    def run(self):
        run_measure(self.should_stop, self.main_window)

    def stop(self):
        self._stop_requested = True

    def should_stop(self):
        return self._stop_requested

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)

        self.setWindowTitle("GP Sigma")
        
        self.ui.lineEdit_6.setText("COM 1")
        self.ui.lineEdit_13.setText("9600")
        # lineEdit_ocv_spec
        self.ui.lineEdit_14.setText("0")        
     
        self.ui.pushButton_6.clicked.connect(self.open_query_window) # Search   
        
        # start, stop and redo(clear)
        self.ui.pushButton.clicked.connect(self.start_measure)
        self.ui.pushButton_2.clicked.connect(self.stop_measure)  
        self.ui.pushButton_5.clicked.connect(self.redo_measure)  #clear
        
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
        self.sim_thread = SimulateThread(main_window=self)
        self.sim_thread.start()
        
    # stop 
    def stop_measure(self):
        if self.sim_thread and self.sim_thread.isRunning():
            self.sim_thread.stop()
            self.sim_thread.wait()
            print("Measurement stopped.")
            
    # re-do / Clear
    def redo_measure(self):
        ocv_values.clear()

        self.ui.tableWidget.setRowCount(0)

        self.ui.lcdNumber.display("0")
        self.ui.lcdNumber_2.display("0")

        self.ui.lineEdit_14.clear()
        self.ui.lineEdit_7.clear()    
        self.ui.lineEdit_8.clear()    
        self.ui.lineEdit_9.clear()    
        self.ui.lineEdit_10.clear()  
        self.ui.lineEdit_11.clear()  
        self.ui.lineEdit_12.clear()   

            
    # RI OCV table        
    def add_row_to_table(self, ocv, ri, timestamp):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO hioki_measurements (ocv, ri, timestamp) VALUES (%s, %s, %s)",
                (ocv, ri, timestamp)
            )
            
            conn.commit()
            
            row_index = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_index)
            self.ui.tableWidget.setItem(row_index, 0, QTableWidgetItem(str(row_index + 1)))     
            self.ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(f"{ri:.4f}"))           
            self.ui.tableWidget.setItem(row_index, 2, QTableWidgetItem(f"{ocv:.4f}"))          
            self.ui.lineEdit_14.setText(str(row_index + 1))  
            self.ui.lcdNumber.display(f"{ri:.4f}")                                  
            self.ui.lcdNumber_2.display(f"{ocv:.4f}")  
            ocv_values.append(ocv)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Failed to load data from database: {e}")
        
    def calculate_metrics(self):
        mean_spec_sigma = 1.5 # mean under dashboard
        print(len(ocv_values))
        
        if ocv_values:
            avg_ocv = sum(ocv_values) / len(ocv_values)     
            max_ocv = max(ocv_values)
            min_ocv = min(ocv_values)
            std_dev = math.sqrt(sum((x - avg_ocv) ** 2 for x in ocv_values) / len(ocv_values))
            deviation = max_ocv - min_ocv          
            new_ocv = avg_ocv - mean_spec_sigma * std_dev
            
            self.ui.lineEdit_9.setText(f"{max_ocv:.4f}")
            self.ui.lineEdit_8.setText(f"{avg_ocv:.4f}")
            self.ui.lineEdit_7.setText(f"{min_ocv:.4f}")
            self.ui.lineEdit_12.setText(f"{std_dev:.4f}")  
            self.ui.lineEdit_10.setText(f"{deviation:.4f}")                 
            self.ui.lineEdit_11.setText(f"{new_ocv:.4f}")                                 

        
            
    def closeEvent(self, event):
        if self.sim_thread and self.sim_thread.isRunning():
            self.sim_thread.stop()
            self.sim_thread.wait()
        event.accept()
