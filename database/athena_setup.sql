CREATE DATABASE IF NOT EXISTS weather_db;

CREATE EXTERNAL TABLE IF NOT EXISTS weather_db.curated_weather (
    city string,
    temp_kelvin double,
    humidity bigint,
    weather_condition string,
    timestamp_unix bigint
)
STORED AS PARQUET
LOCATION 's3://weather-curated-data-296066093533-us-east-1-an/';
