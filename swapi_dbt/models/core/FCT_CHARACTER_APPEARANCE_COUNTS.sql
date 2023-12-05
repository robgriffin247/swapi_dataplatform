select 
    CHARACTER_NAME as NAME, 
    count(1) as APPEARANCES 
from {{ ref('DIM_FILM_CHARACTERS') }}
group by CHARACTER_NAME
order by APPEARANCES desc