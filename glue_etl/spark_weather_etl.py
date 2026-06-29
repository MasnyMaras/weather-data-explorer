import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

raw_path = "s3://weather-raw-data-296066093533-us-east-1-an/"
curated_path = "s3://weather-curated-data-296066093533-us-east-1-an/"

df = spark.read.json(raw_path)

df_cleaned = df.selectExpr(
    "name as city",
    "main.temp as temp_kelvin",
    "main.humidity as humidity",
    "weather[0].main as weather_condition",
    "dt as timestamp_unix"
)

df_cleaned.write.mode("append").parquet(curated_path)

job.commit()
