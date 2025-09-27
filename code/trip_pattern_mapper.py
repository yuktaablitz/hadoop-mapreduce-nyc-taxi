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
            # Extract datetime and distance
            if len(fields) > 17:  # original_cleaned data
                year = int(fields[14]) if len(fields) > 14 else 2018
                month = int(fields[15]) if len(fields) > 15 else 1  
                hour = int(fields[18]) if len(fields) > 18 else 0
                distance = float(fields[1]) if fields[1] else 0.0
                day_of_week = int(fields[17]) if len(fields) > 17 else 0
            else:  # taxi_trip_data
                pickup_time = fields[1]
                dt = datetime.strptime(pickup_time[:19], '%Y-%m-%d %H:%M:%S')
                year = dt.year
                month = dt.month
                hour = dt.hour
                day_of_week = dt.weekday()
                distance = float(fields[4]) if fields[4] else 0.0
            
            if distance > 0 and distance < 50:
                # Categorize by time periods
                if hour >= 6 and hour < 10:
                    period = "Morning_Rush"
                elif hour >= 10 and hour < 16:
                    period = "Midday"
                elif hour >= 16 and hour < 20:
                    period = "Evening_Rush"
                else:
                    period = "Off_Peak"
                
                # Categorize by distance
                if distance < 2:
                    dist_category = "Short"
                elif distance < 10:
                    dist_category = "Medium"
                else:
                    dist_category = "Long"
                
                print(f"{period}_{dist_category}\t{distance}\t1")
    except:
        continue
