select
    replace(replace(URL, 'https://swapi.dev/api/films/', ''), '/', '') as FILM_ID,
    TITLE as FILM_TITLE,
    EPISODE_ID as EPISODE,
    OPENING_CRAWL,
    DIRECTOR,
    PRODUCER,
    RELEASE_DATE,
    --CHARACTERS,
    --PLANETS,
    --SPECIES,
    --STARSHIPS,
    --VEHICLES, 
    URL,
    CREATED as CREATED_DATE,
    EDITED as EDITED_DATE
from {{ source('RAW', 'FILMS') }}
