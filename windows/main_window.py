from PySide6.QtWidgets import QWidget, QTableWidgetItem
from PySide6.QtCore import QThread, QDate
from db_connection import get_connection
from measure import run_measure
from ui.GP_ui import Ui_Form as Ui_MainForm
from windows.query_window import QueryWindow
from datetime import datetime
import math

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
        
        # display board
        self.ui.lineEdit_6.setText("COM 1")
        self.ui.lineEdit_13.setText("9600")
        self.ui.lineEdit_15.setText("1.28") #ocv spec
        self.ui.comboBox_2.addItems(["1.0", "1.5", "2.0"])
        self.ui.lineEdit_14.setText("0")     
        self.ui.lineEdit_2.setText("default resistance") #resistance              
        
        # Simulate Fill in area
        self.ui.lineEdit.setText("100") #quantity
        self.ui.lineEdit_3.setText("L001") #lot
        self.ui.lineEdit_4.setText("MA001") #machine
        self.ui.lineEdit_5.setText("Chen") #operator
        self.ui.plainTextEdit.setPlainText("No") #memo   
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.dateEdit_2.setDate(QDate.currentDate())
        self.ui.dateEdit_3.setDate(QDate.currentDate())                      
     
        # search
        self.ui.pushButton_6.clicked.connect(self.open_query_window)    
        
        # start, stop and reset(clear)
        self.ui.pushButton.clicked.connect(self.start_measure)
        self.ui.pushButton_2.clicked.connect(self.stop_measure)  
        self.ui.pushButton_5.clicked.connect(self.redo_measure)
        
        # save
        self.ui.pushButton_4.clicked.connect(self.save_all)
        
        self.query_window = None 
        self.sim_thread = None
        
        self.show()

    def open_query_window(self):
        if self.query_window is None:
            self.query_window = QueryWindow()
        self.query_window.show()
    
    def start_measure(self):
        if self.sim_thread and self.sim_thread.isRunning():
            print("Measurement already running.")
            return
        self.sim_thread = SimulateThread(main_window=self)
        self.sim_thread.start()
        
    def stop_measure(self):
        if self.sim_thread and self.sim_thread.isRunning():
            self.sim_thread.stop()
            self.sim_thread.wait()
            print("Measurement stopped.")
            
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
        
    def save_all(self):
        try:
            # save lots details
            model = "MO1"
            machine = self.ui.lineEdit_4.text()
            lot = self.ui.lineEdit_3.text()
            quantity = self.ui.lineEdit.text()
            operator = self.ui.lineEdit_5.text()
            memo = self.ui.plainTextEdit.toPlainText()            
            sampling_date = self.ui.dateEdit.date().toPython()
            aging_start_45deg = self.ui.dateEdit_2.date().toPython()
            aging_start_roomtemp = self.ui.dateEdit_3.date().toPython()
            
            max_ocv = self.ui.lineEdit_9.text()
            avg_ocv = self.ui.lineEdit_8.text()
            min_ocv = self.ui.lineEdit_7.text()
            std_deviation = self.ui.lineEdit_12.text()
            deviation = self.ui.lineEdit_10.text()
            sigma = self.ui.lineEdit_11.text()
            
            conclusion = self.ui.textBrowser.text() #rules and calculation

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO lots (
                    lot_no, model_no, machine_no, sample_qty, memo, sampling_date, aging_start_45deg, aging_start_roomtemp, 
                    ocv_max, ocv_min, ocv_avg, std_deviation, deviation, sigma, operator
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                lot, model, machine, quantity, memo, sampling_date, aging_start_45deg, aging_start_roomtemp,
                max_ocv, min_ocv, avg_ocv, std_deviation, deviation, sigma, operator
            ))
            lot_id = cursor.fetchone()[0]

            # save measurements
            row_count = self.ui.tableWidget.rowCount()
            ocv_spec = float(self.ui.lineEdit_15.text())  # user-defined ocv spec            

            for row in range(row_count):
                index = self.ui.tableWidget.item(row, 0).text()
                ri = float(self.ui.tableWidget.item(row, 1).text())
                ocv = float(self.ui.tableWidget.item(row, 2).text())
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                below_spec = ocv < ocv_spec

                cursor.execute("""
                    INSERT INTO measurements (lot_id, measurement_index, ocv, ri, timestamp, below_spec)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (lot_id, index, ocv, ri, timestamp, below_spec))

            conn.commit()
            cursor.close()
            conn.close()
            print("All data saved successfully.")

        except Exception as e:
            print(f"Failed to save all data: {e}")    
     
    def add_row_to_table(self, ocv, ri):          
        row_index = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row_index)
        self.ui.tableWidget.setItem(row_index, 0, QTableWidgetItem(str(row_index + 1)))     
        self.ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(f"{ri:.4f}"))           
        self.ui.tableWidget.setItem(row_index, 2, QTableWidgetItem(f"{ocv:.4f}"))          
        self.ui.lineEdit_14.setText(str(row_index + 1))  
        self.ui.lcdNumber.display(f"{ri:.4f}")                                  
        self.ui.lcdNumber_2.display(f"{ocv:.4f}")  
        ocv_values.append(ocv)               
        
    def calculate_metrics(self):
        mean_spec_sigma = 1.5 # mean under dashboard
        print(f"Num of measurements: {len(ocv_values)}")
        
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
