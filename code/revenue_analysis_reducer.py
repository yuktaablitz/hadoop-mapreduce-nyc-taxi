#!/opt/homebrew/bin/python3
import sys

revenue_stats = {}
for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            category, fare, tip, total, tip_rate, count = line.split('\t')
            fare = float(fare)
            tip = float(tip)
            total = float(total)
            tip_rate = float(tip_rate)
            count = int(count)
            
            if category not in revenue_stats:
                revenue_stats[category] = {
                    'total_fare': 0, 'total_tip': 0, 'total_revenue': 0, 
                    'total_tip_rate': 0, 'count': 0
                }
            
            revenue_stats[category]['total_fare'] += fare
            revenue_stats[category]['total_tip'] += tip
            revenue_stats[category]['total_revenue'] += total
            revenue_stats[category]['total_tip_rate'] += tip_rate
            revenue_stats[category]['count'] += count
        except:
            continue

for category, stats in sorted(revenue_stats.items()):
    if stats['count'] > 0:
        avg_fare = stats['total_fare'] / stats['count']
        avg_tip = stats['total_tip'] / stats['count']
        avg_revenue = stats['total_revenue'] / stats['count']
        avg_tip_rate = stats['total_tip_rate'] / stats['count']
        print(f"{category}\t{avg_fare:.2f}\t{avg_tip:.2f}\t{avg_revenue:.2f}\t{avg_tip_rate:.1f}%\t{stats['count']}")
