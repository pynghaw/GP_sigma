import csv
import time
from datetime import datetime

def simulate_get_data(input_csv='hioki_simulated_data.csv', output_csv='hioki_simulated_data_retrieved.csv', interval=0.5):
    try:
        with open(input_csv, mode='r') as infile, open(output_csv, mode='w', newline='') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.writer(outfile)
            writer.writerow(['Timestamp', 'OCV', 'RI'])

            print("Simulating Hioki measurement fetch. Press Ctrl+C to stop.")

            for row in reader:
                try:
                    ri = float(row['RI'])
                    ocv = float(row['OCV'])
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"Measurement: OCV={ocv}, RI={ri}")

                    writer.writerow([timestamp, ocv, ri])
                    outfile.flush()
                    time.sleep(interval)
                except ValueError:
                    print("Invalid data row, skipping:", row)

    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    simulate_get_data()
