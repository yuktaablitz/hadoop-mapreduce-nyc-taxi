#!/opt/homebrew/bin/python3
import sys

clean_count = 0
dirty_count = 0
error_count = 0
total_distance = 0
total_fare = 0

for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            parts = line.split('\t')
            status = parts[0]
            
            if status == "CLEAN":
                clean_count += 1
                total_distance += float(parts[1])
                total_fare += float(parts[2])
            elif status == "DIRTY":
                dirty_count += 1
            elif status == "ERROR":
                error_count += 1
        except:
            continue

print(f"CLEAN_RECORDS\t{clean_count}")
print(f"DIRTY_RECORDS\t{dirty_count}")
print(f"ERROR_RECORDS\t{error_count}")
if clean_count > 0:
    print(f"AVG_DISTANCE\t{total_distance/clean_count:.2f}")
    print(f"AVG_FARE\t{total_fare/clean_count:.2f}")
