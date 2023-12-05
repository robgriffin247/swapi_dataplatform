select
    FILM_ID,
    FILM_TITLE,
    EPISODE,
    DIRECTOR,
    PRODUCER,
    RELEASE_DATE
from {{ ref('STG_FILMS')}}