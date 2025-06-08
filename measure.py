import csv
import time
from datetime import datetime

def run_measure(stop_flag, input_csv='hioki_simulated_data.csv', interval=0.5):
    try:
        with open(input_csv, mode='r') as infile:
            reader = csv.DictReader(infile)
            print("Simulating Hioki measurement fetch.")

            for row in reader:
                if stop_flag():  # externally signaled to stop
                    print("Measurement stopped by signal.")
                    break

                try:
                    ri = float(row['RI'])
                    ocv = float(row['OCV'])
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] Measurement: OCV={ocv}, RI={ri}")
                    time.sleep(interval)
                except ValueError:
                    print("Invalid data row, skipping:", row)

    except Exception as e:
        print(f"Error: {e}")
