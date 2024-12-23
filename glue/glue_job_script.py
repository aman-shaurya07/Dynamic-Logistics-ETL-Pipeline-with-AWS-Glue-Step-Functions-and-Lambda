import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions

# Initialize Glue Context
args = getResolvedOptions(sys.argv, ['JOB_NAME', 's3_input', 's3_output'])
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# Read input data from S3
input_data = args['s3_input']
output_data = args['s3_output']

df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [input_data]},
    format="csv"
)

# Transform data (filtering, renaming columns, etc.)
df_transformed = ApplyMapping.apply(frame=df,
                                    mappings=[
                                        ("delivery_id", "long", "delivery_id", "long"),
                                        ("date", "string", "delivery_date", "string"),
                                        ("origin", "string", "origin", "string"),
                                        ("destination", "string", "destination", "string"),
                                        ("vehicle_type", "string", "vehicle_type", "string"),
                                        ("delivery_status", "string", "status", "string"),
                                        ("delivery_time", "string", "time_taken", "string")
                                    ])

# Write output to S3 as Parquet
glueContext.write_dynamic_frame.from_options(
    frame=df_transformed,
    connection_type="s3",
    connection_options={"path": output_data},
    format="parquet"
)
