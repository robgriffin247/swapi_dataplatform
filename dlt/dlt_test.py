import dlt

data = [{"id":1, "name":"Alice"},
        {"id":2, "name":"Bob"}]

pipeline = dlt.pipeline(
    pipeline_name="dlt_test",
    destination="duckdb",
    dataset_name="test_data"
)

load_info = pipeline.run(data, table_name="users")

print(load_info)