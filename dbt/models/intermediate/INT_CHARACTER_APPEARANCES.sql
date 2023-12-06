with flat as (
    select 
        UUID_STRING() as APPEARANCE_ID,
        a.FILM_ID,
        a.FILM_TITLE,
        replace(replace(VALUE, 'https://swapi.dev/api/people/', ''), '/', '') as CHARACTER_ID
    from {{ ref('STG_FILMS')}} as a, lateral flatten(input => a.CHARACTERS) as b
)
, joined as (
    select 
        flat.APPEARANCE_ID,
        flat.FILM_ID,
        flat.FILM_TITLE,
        flat.CHARACTER_ID, 
        STG_CHARACTERS.NAME as CHARACTER_NAME 
    from flat left join STG_CHARACTERS using (CHARACTER_ID)
)

select * from JOINED