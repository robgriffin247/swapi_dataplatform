select
    FILM_ID,
    URL,
    OPENING_CRAWL
from {{ ref('STG_FILMS')}}