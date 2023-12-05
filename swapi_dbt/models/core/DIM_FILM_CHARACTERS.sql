with base as (
    select
        UUID_STRING() as APPEARANCE_ID,
        a.FILM_ID,
        replace(replace(VALUE, 'https://swapi.dev/api/people/', ''), '/', '') as CHARACTER_ID,
        a.FILM_TITLE,
        a.EPISODE
    from {{ ref('STG_FILMS')}} as a, lateral flatten(input => a.CHARACTERS) as b
)
, characters as (
    select 
        CHARACTER_ID, 
        NAME as CHARACTER_NAME 
    from STG_CHARACTERS
)

select base.*, characters.CHARACTER_NAME from base left join characters using (CHARACTER_ID)
