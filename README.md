# NYC Taxi Data Analysis with Hadoop MapReduce

Distributed processing of 2.1 GB of 2018 NYC taxi trip data (about 18.3 million records) with Hadoop MapReduce and
Python streaming: data-quality checks, trip patterns by time of day and distance, and revenue / tipping analysis.

## Key results (full dataset)

| Job | Result |
|---|---|
| Data cleaning | 18,011,493 clean records, 308,435 dirty, 264 unparseable (98.3% clean); average trip 9.12 mi, average fare $31.75 |
| Trip patterns | 12 time-of-day × distance segments; off-peak medium trips are the largest group (3.65M) |
| Revenue | Credit-card trips tip 34.5-46.5% of the fare on average; cash trips record 0% (cash tips aren't captured) |
| Corner cases | Map-only job (zero reducers) wrote 18 part files; a 5-reducer job showed how keys spread across partitions |

Full outputs are in [`results/`](results/).

## Dataset

Two 2018 NYC yellow-taxi CSVs (about 2.1 GB together), from Kaggle:

- `taxi_trip_data.csv`, standard TLC columns:
  `vendor_id, pickup_datetime, dropoff_datetime, passenger_count, trip_distance, rate_code, store_and_fwd_flag,
  payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, imp_surcharge, total_amount,
  pickup_location_id, dropoff_location_id`
- `original_cleaned_nyc_taxi_data_2018.csv`, a pre-cleaned version with extra derived columns
  (year, month, day of week, hour, trip duration).

The mappers detect which file a line comes from by its column count, so both can be loaded into the same HDFS folder.
The raw data isn't committed; a small synthetic file in the TLC format is in `sample/` for testing.

## Jobs

| Job | Mapper emits | Reducer outputs |
|---|---|---|
| `data_cleaning` | `CLEAN` / `DIRTY` / `ERROR` per record (rules: 0 < distance < 100 mi, 0 < fare < $500, numeric pickup zone) | record counts, average distance and fare |
| `trip_pattern` | `<period>_<distance class>` (Morning_Rush, Midday, Evening_Rush, Off_Peak × Short/Medium/Long) | average distance and trip count per segment |
| `revenue_analysis` | `<payment>_<revenue class>` (Credit_Card/Cash × Low/Medium/High) | average fare, tip, total, tip rate and count |

## Run it locally (no Hadoop needed)

Requires Python 3.

```bash
git clone https://github.com/yuktaablitz/hadoop-mapreduce-nyc-taxi.git
cd hadoop-mapreduce-nyc-taxi
./run_local.sh                              # runs all 3 jobs on sample/sample_taxi_trip_data.csv
./run_local.sh path/to/taxi_trip_data.csv   # or on your own CSV
```

This is the same pipeline Hadoop runs (`map | sort | reduce`), so it's the quickest way to test a change to a script.

## Run it on Hadoop

Tested with Hadoop 3.4.2 in pseudo-distributed mode (single node). Install Hadoop
([single-node setup guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html)),
start HDFS and YARN, then:

```bash
# load the data into HDFS
hdfs dfs -mkdir -p /user/$USER/taxi/input
hdfs dfs -put taxi_trip_data.csv original_cleaned_nyc_taxi_data_2018.csv /user/$USER/taxi/input/

STREAMING_JAR=$(ls $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar)

# one job (repeat with trip_pattern and revenue_analysis)
hadoop jar $STREAMING_JAR \
  -files code/data_cleaning_mapper.py,code/data_cleaning_reducer.py \
  -mapper data_cleaning_mapper.py -reducer data_cleaning_reducer.py \
  -input /user/$USER/taxi/input -output /user/$USER/taxi/data_cleaning

hdfs dfs -cat /user/$USER/taxi/data_cleaning/part-*

# corner cases
#   map-only:          add  -D mapreduce.job.reduces=0  and drop -reducer
#   several reducers:  add  -D mapreduce.job.reduces=5
```

Each output folder must not exist before a run (`hdfs dfs -rm -r <folder>` to rerun).

## Project structure

```
code/            mappers and reducers (Python, Hadoop streaming)
results/         outputs from the full 18M-record run
sample/          small synthetic CSV in the TLC format
run_local.sh     runs every job locally with map | sort | reduce
```

## Tech stack

Hadoop 3.4.2 (HDFS, YARN, MapReduce streaming), Python.
