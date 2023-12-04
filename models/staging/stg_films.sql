create or replace table <database>.<development_schema>.stg_films as (
select
    "episode_id" as film_id,
    "title" as film_title,
    "episode_id" as episode,
    "opening_crawl" as opening_crawl,
    "director" as director,
    "producer" as producer,
    "release_date" as release_date,
    "characters" as characters,
    "planets" as planets,
    "species" as species,
    "starships" as starships,
    "vehicles" as vehicles, 
    "url" as url,
    "created" as created_date,
    "edited" as edited_date
from {{ source('raw', 'films') }}
);