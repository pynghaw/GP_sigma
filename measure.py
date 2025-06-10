import csv
import time
from datetime import datetime
from ui.GP_ui import Ui_Form as Ui_MainForm
from PySide6.QtWidgets import QWidget, QTableWidgetItem

def run_measure(stop_flag, main_window, input_csv='hioki_sample_dataset.csv', interval=0.5):
    try:
        with open(input_csv, mode='r') as infile:
            reader = csv.DictReader(infile)
            print("Simulating Hioki measurement fetch.")          
            
                                    
            for row in reader:
                if stop_flag():  
                    print("Measurement stopped by signal.")
                    break

                try:
                    ri = float(row['RI'])
                    ocv = float(row['OCV'])
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] Measurement: OCV={ocv}, RI={ri}")
                    
                    main_window.add_row_to_table(ocv, ri, timestamp) # add data to table
                    
                    time.sleep(interval)
                    
                except ValueError:
                    print("Invalid data row, skipping:", row)     
                    
            main_window.calculate_metrics() # calcualte metrics               
            

    except Exception as e:
        print(f"Error: {e}")

