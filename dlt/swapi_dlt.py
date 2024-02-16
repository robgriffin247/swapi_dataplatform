import dlt
from dlt.sources.helpers import requests

def get_resource(resource):
    url = f"https://swapi.dev/api/{resource}/?page=1"
    while True:
        response = requests.get(url)
        response.raise_for_status()
        yield response.json()["results"]
        print('Data ingested from ' + url)

        if response.json()["next"] == None:
            break
        url = response.json()["next"]


@dlt.source
def swapi_source(resources):
    for resource in resources:
        yield dlt.resource(
            get_resource(resource),
            name="raw_"+resource,
            write_disposition="merge",
            primary_key="url"
        )

pipeline = dlt.pipeline(
    pipeline_name="swapi_dynamic_pipeline",
    destination="duckdb",
    dataset_name="swapi_raw"
)


resources = list(requests.get('https://swapi.dev/api/').json())

load_info = pipeline.run(swapi_source(resources))

print(load_info)