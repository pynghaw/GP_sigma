import serial
import time

def continuous_fetch(port='COM1', interval=0.5):
    try:
        with serial.Serial(port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1) as ser:
            print(f"Listening on {port} every {interval} seconds. Press Ctrl+C to stop.")
            ser.reset_input_buffer()

            while True:
                command = b':FETCh?\r\n'
                ser.write(command)
                time.sleep(0.05)  # short delay to allow response
                
                raw = ser.readline()
                if raw:
                    decoded = raw.decode('utf-8', errors='ignore').strip()
                    print(f"Measurement: {decoded}")
                else:
                    print("No data received")

                time.sleep(interval - 0.05)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    continuous_fetch()
