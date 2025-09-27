cat > README.md << 'EOF'
# NYC Taxi Data Analysis with Hadoop MapReduce

## Overview
This project demonstrates distributed data processing using Hadoop MapReduce on 2.1GB of NYC taxi trip data containing 18+ million records.

## Dataset
- **Size**: 2.1 GB across 3 files
- **Records**: ~18 million taxi trips from 2018
- **Files**: Trip data, geographic zones, operational metrics

## Technologies Used
- Hadoop 3.4.2 (ARM64 optimized)
- Python MapReduce streaming
- HDFS distributed storage
- MacBook M1 Pro

## Project Structure
├── code/                    # Python MapReduce scripts
├── documentation/           # Assignment report and analysis
├── screenshots/            # Terminal and web UI screenshots
├── results/               # MapReduce job outputs
└── README.md             # Project overview
## Key Results
- **Data Quality**: 98.3% clean records from 18M+ processed
- **Peak Performance**: Processed 2.1GB data across distributed cluster
- **Business Insights**: Credit card tips 35-46% vs 0% for cash payments

## MapReduce Jobs
1. **Data Cleaning**: Quality assessment and preprocessing
2. **Trip Pattern Analysis**: Temporal and spatial traffic patterns  
3. **Revenue Analysis**: Payment methods and tipping behavior

## Corner Cases Tested
- Zero reducers (map-only processing)
- Multiple reducers (data distribution)
- Small dataset edge cases

## How to Run
See documentation/hadoop_assignment_report.md for detailed setup and execution instructions.
