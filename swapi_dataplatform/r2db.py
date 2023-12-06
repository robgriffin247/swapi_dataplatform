import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import os 

def r2db(table, df, database='SWAPI', schema='RAW'):
    ctx = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USERNAME'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SWAPI_WAREHOUSE'),
        database=database,
        schema=schema,
    )
    
    write_pandas(ctx, df, table.upper(), auto_create_table=True, overwrite=True)
