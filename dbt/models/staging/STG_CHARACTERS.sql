select 
        replace(replace(URL, 'https://swapi.dev/api/people/', ''), '/', '') as CHARACTER_ID,
        *
from {{ source('RAW', 'PEOPLE') }}