#!/opt/homebrew/bin/python3
import sys

pattern_stats = {}
for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            pattern, distance, count = line.split('\t')
            distance = float(distance)
            count = int(count)
            
            if pattern not in pattern_stats:
                pattern_stats[pattern] = {'total_distance': 0, 'count': 0}
            
            pattern_stats[pattern]['total_distance'] += distance
            pattern_stats[pattern]['count'] += count
        except:
            continue

for pattern, stats in sorted(pattern_stats.items()):
    avg_distance = stats['total_distance'] / stats['count'] if stats['count'] > 0 else 0
    print(f"{pattern}\t{avg_distance:.2f}\t{stats['count']}")
