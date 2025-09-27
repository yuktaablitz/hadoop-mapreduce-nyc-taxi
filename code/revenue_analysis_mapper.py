#!/opt/homebrew/bin/python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or 'pickup_datetime' in line or 'vendor_id' in line:
        continue
    
    try:
        fields = line.split(',')
        if len(fields) >= 10:
            # Extract fare and tip information
            if len(fields) > 17:  # original_cleaned data
                fare = float(fields[5]) if fields[5] else 0.0
                tip = float(fields[8]) if len(fields) > 8 else 0.0
                total = float(fields[11]) if len(fields) > 11 else 0.0
                payment_type = int(fields[4]) if fields[4] else 1
            else:  # taxi_trip_data
                fare = float(fields[8]) if fields[8] else 0.0
                tip = float(fields[11]) if len(fields) > 11 else 0.0
                total = float(fields[14]) if len(fields) > 14 else 0.0
                payment_type = int(fields[7]) if fields[7] else 1
            
            if fare > 0 and total > 0 and fare < 200:
                # Payment type analysis (1=Credit, 2=Cash)
                pay_method = "Credit_Card" if payment_type == 1 else "Cash"
                
                # Revenue categories
                if total < 10:
                    revenue_category = "Low_Revenue"
                elif total < 25:
                    revenue_category = "Medium_Revenue"
                else:
                    revenue_category = "High_Revenue"
                
                tip_rate = (tip / fare) * 100 if fare > 0 else 0
                
                print(f"{pay_method}_{revenue_category}\t{fare}\t{tip}\t{total}\t{tip_rate}\t1")
    except:
        continue
