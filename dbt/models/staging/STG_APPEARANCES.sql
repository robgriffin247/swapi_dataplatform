select
    *
from {{ source('RAW', 'FILMS__CHARACTERS') }}
