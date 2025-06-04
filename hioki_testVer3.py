import serial
import time
import csv
import os

def continuous_fetch(port='COM1', interval=0.5, csv_file='hioki_sample_dataset.csv'):
    file_exists = os.path.isfile(csv_file)

    try:
        with serial.Serial(port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1) as ser:
            print(f"Listening on {port} every {interval} seconds. Press Ctrl+C to stop.")
            ser.reset_input_buffer()

            ser.write(b'*IDN?\r\n')
            time.sleep(0.05)
            idn_raw = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Device Info: {idn_raw}")
            manufacturer, model, _, firmware = idn_raw.split(',')

            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['Timestamp', 'Manufacturer', 'Model', 'Firmware', 'OCV', 'IR'])

                while True:
                    ser.write(b':FETCh?\r\n')
                    time.sleep(0.05)

                    raw = ser.readline()
                    if raw:
                        decoded = raw.decode('utf-8', errors='ignore').strip()
                        print(f"Measurement: {decoded}")

                        parts = decoded.split(',')
                        if len(parts) == 2:
                            try:
                                ocv = float(parts[0])
                                ir = float(parts[1])
                                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                                writer.writerow([timestamp, manufacturer, model, firmware, ocv, ir])
                                file.flush()
                            except ValueError:
                                print("Invalid numeric data received.")
                        else:
                            print("Unexpected data format")
                    else:
                        print("No data received")

                    time.sleep(interval - 0.05)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    continuous_fetch()
