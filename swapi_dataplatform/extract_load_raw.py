import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import os 
from api_wan import api_wan
#from dotenv import load_dotenv

#load_dotenv('.env')

ctx = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USERNAME'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse='SWAPI_DATAPLATFORM',
    database='SWAPI_RAW',
    schema='SWAPI',
)
cs = ctx.cursor()

resources = ['films', 'people', 'planets', 'species', 'starships', 'vehicles']
resources = ['films']

for res in resources:
    write_pandas(ctx, api_wan(res), res, auto_create_table=True, overwrite=True)
