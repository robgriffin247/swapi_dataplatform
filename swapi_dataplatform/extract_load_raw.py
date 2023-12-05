import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import os 
from api_wan import api_wan

ctx = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USERNAME'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SWAPI_WAREHOUSE'),
    database='SWAPI',
    schema='RAW',
)
cs = ctx.cursor()

resources = ['films', 'people', 'planets', 'species', 'starships', 'vehicles']
for res in resources:
    write_pandas(ctx, api_wan(res), res.upper(), auto_create_table=True, overwrite=True)
