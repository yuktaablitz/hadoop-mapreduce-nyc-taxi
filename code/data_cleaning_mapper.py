#!/opt/homebrew/bin/python3
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    if not line or 'pickup_datetime' in line or 'vendor_id' in line:
        continue
    
    try:
        fields = line.split(',')
        if len(fields) >= 10:
            # Handle different file formats
            if len(fields) > 17:  # original_cleaned_nyc_taxi_data_2018.csv
                trip_distance = float(fields[1]) if fields[1] else 0.0
                fare_amount = float(fields[5]) if fields[5] else 0.0
                pickup_location = fields[12] if len(fields) > 12 else "0"
                trip_duration = float(fields[19]) if len(fields) > 19 else 0.0
            else:  # taxi_trip_data.csv
                trip_distance = float(fields[4]) if fields[4] else 0.0
                fare_amount = float(fields[8]) if fields[8] else 0.0
                pickup_location = fields[15] if len(fields) > 15 else "0"
                trip_duration = 0.0
            
            # Data cleaning rules
            if (trip_distance > 0 and trip_distance < 100 and 
                fare_amount > 0 and fare_amount < 500 and
                pickup_location.isdigit()):
                print(f"CLEAN\t{trip_distance}\t{fare_amount}\t{pickup_location}\t{trip_duration}")
            else:
                print(f"DIRTY\t{line[:50]}...")
    except:
        print(f"ERROR\t{line[:50]}...")
