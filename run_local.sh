#!/bin/bash
# Run all three MapReduce jobs locally without Hadoop (map | sort | reduce), to test the scripts.
# Usage: ./run_local.sh [input.csv]   (defaults to the small synthetic sample)
set -e
IN="${1:-sample/sample_taxi_trip_data.csv}"
mkdir -p output_local
for job in data_cleaning trip_pattern revenue_analysis; do
  python3 "code/${job}_mapper.py" < "$IN" | sort | python3 "code/${job}_reducer.py" > "output_local/${job}.txt"
  echo "== $job"; cat "output_local/${job}.txt"
done
