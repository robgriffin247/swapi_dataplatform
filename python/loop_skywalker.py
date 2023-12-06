from api_wan import api_wan
from r2db import r2db

resources = ['films', 'people', 'planets', 'species', 'starships', 'vehicles']
for resource in resources:
    r2db(resource, api_wan(resource))
