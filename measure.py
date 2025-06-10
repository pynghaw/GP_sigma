import csv
import time

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
                    
                    main_window.add_row_to_table(ocv, ri) # add data to table
                    
                    time.sleep(interval)
                    
                except ValueError:
                    print("Invalid data row, skipping:", row)     
                    
            main_window.calculate_metrics() # calcualte metrics               
            

    except Exception as e:
        print(f"Error: {e}")

