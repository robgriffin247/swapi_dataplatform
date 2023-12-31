## SWAPI Data Platform

### Aim 

Create a functioning data platform using:
- [x] Git and GitHub for version control and collaboration
- [x] Snowflake for data warehousing
- [x] Python Pandas & Snowflake Connector for data extraction and loading
- [ ] Switch to dlt data extraction and loading
- [x] dbt for data transformation
- [ ] Dagster for orchestration
- [ ] OpenMetaData for data governance
- [ ] HEX and/or PowerBI for a dashboard

It should also include precommit hooks, to ensure all data sets have a complete yml file and that everything in the yml file has a matching data entry, and a makefile to shorten repetitive command-line actions.

The focus is proof-of-concept and testing, not a comprehensive data platform &mdash; just enough to develop and test each component.
Data comes from SWAPI, the [Star Wars API](https://swapi.dev). The pipeline will generate the following datasets:

| Raw        | Staging         | Intermediate                | Core                       |
|------------|-----------------|-----------------------------|----------------------------|
| FILMS      | STG_FILMS       | INT_CHARACTER_APPEARANCES   | DIM_CHARACTER_APPEARANCES  |
| PEOPLE     | STG_CHARACTERS  |                             |                            |


### Current status:

To Do:
- Add material to instructions below; will repeat the process from scratch on a fresh machine with new accounts to make sure they are thorough.
- Add dlt, dagster, openmetadata and hex

### Instructions

1. Setup WSL
    1. Install Windows Subsystem for Linux (WSL) by running `wsl --install` in Windows Powershell or Command Prompt
1. Setup Python
    1. Install Python in WSL
    1. Setup Linux/Ubuntu profile
1. Setup Poetry
    1. Install Poetry in WSL
    1. Create a Poetry project (will form _project directory_)
1. Setup Git
    1. Install Git in WSL
1. Setup GitHub (and regularly commit and push!)
    1. Create a GitHub Account
    1. Create a GitHub repo with the same name as the project directory
    1. Connect Git to GitHub
    1. Initialise Git in the project directory
    1. (Regularly) commit and push; develop on branches
1. Create .env file and add to .gitignore
1. Setup Snowflake (add relevant credentials to .env)
    1. Create a Snowflake account
    1. Use a worksheet to create a warehouse, database and raw/dev schemas
1. Setup dbt
    1. Install dbt in WSL
    1. Run `dbt init` in the project directory in WSL
    1. Follow prompts and provide the necessary information for setup 
1. Create a Python function to extract raw data as Pandas dataframe; `api_wan()`
1. Load raw data to snowflake with the Python-Snowflake connector
    1. Create a function that loads a Pandas dataframe to Snowflake; `r2db()`
    1. Write code to leverage the extract and load functions for each raw asset; `loop_skywalker.py`
1. Use dbt to create and load staging, intermediate and core modules to Snowflake
    1. In project_directory/dbt/models/, write 
        - SQL code to create each module
        - .yml files for the schemas and source
        - My preferred example structure:
        
        ```
        models/
        |- sources.yml
        |- staging/
        |  |- STG_FILMS.sql
        |  |- STG_FILMS.yml
        |  |- STG_CHARACTERS.sql
        |  |- STG_CHARACTERS.yml
        |- intermediate/
        |  |- INT_FILMS.sql
        |  |- INT_FILMS.yml
        ...
        ...
        ``` 

<!---------------------------------------------------------

#### OLD Step-by-step guide

1. Create GitHub repo

1. Create the necessary warehouse, databases and schemas in Snowflake browser UI (worksheets)
    ```sql
    create warehouse if not exists SWAPI_DATAPLATFORM;
    create database if not exists SWAPI;
    create schema if not exists SWAPI.RAW;
    create schema if not exists SWAPI.DEV_ROB;
    ```

1. Create local directory for the project using `poetry add <project_name>`

1. `cd` to the project directory

1. Ensure the following dependencies with `poetry add ...`
    ```bash
    python =  ">=3.10,<3.11"
    requests = "^2.31.0"
    snowflake-snowpark-python = {extras = ["pandas"], version = "^1.10.0"}
    dbt-snowflake = "^1.7.0"
    ```

1. Add .gitignore with `echo '.env' >> .gitignore`

1. Add .env file with 
    ```bash
    SNOWFLAKE_USERNAME=<username>
    SNOWFLAKE_PASSWORD=<password>
    SNOWFLAKE_ACCOUNT=<account>
    SNOWFLAKE_SERVER=<server>
    SNOWFLAKE_DATASOURCE=Snowflake
    ```

1. Initialise, create connection and push git from the new repo
    ```bash
    git init
    git remote add origin git@github.com:<github_username>/<project_name>.git
    git add .
    git commit -m 'initialise'
    git push -u origin main
    ```

1. Create a Python function (api_wan.py) to collect and return the SWAPI data as a pandas dataframe
    ```python
    import requests
    import json
    from math import ceil
    import pandas as pd

    def api_wan(resource):
        # Perform initial request; this will get the first page of data AND show whether more pages exist
        response = requests.get(f'https://swapi.dev/api/{resource}')
        response_json = response.json()
        
        # Store first page of data
        response_data = [item for item in response_json['results']]
        
        # Loop through remaining pages to collect data (will do nothing if there is only 1 page)
        number_of_pages = ceil( response_json['count'] / 10 )
        for page in range(2, number_of_pages+1):
            response = requests.get(f'https://swapi.dev/api/{resource}/?page={page}')
            response_json = response.json()
            response_data = response_data + [item for item in response_json['results']]
        
        response_df = pd.DataFrame(response_data)
        return response_df
    ```

1. Create and execute a Python program (extract_load_raw.py) to send the raw SWAPI data to Snowflake with `poetry run python3 extract_load_raw.py`
    ```python
    import snowflake.connector
    import pandas as pd
    from snowflake.connector.pandas_tools import write_pandas
    import os 
    from api_wan import api_wan

    ctx = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USERNAME'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SWAPI_WAREHOUSE'),
        database=os.getenv('RAW_DATABASE'),
        schema=os.getenv('RAW_SCHEMA'),
    )
    cs = ctx.cursor()

    resources = ['films', 'people', 'planets', 'species', 'starships', 'vehicles']

    for res in resources:
        write_pandas(ctx, api_wan(res), res, auto_create_table=True, overwrite=True)
    ```
    - Check the data loaded into the Snowflake data tables

1. `dbt init`
    - follow terminal prompts (see screenshot and add details)


1. Create a model to stage the films data as /models/staging/stg_films.sql
    ```sql
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
    ```

1. Add metadata to the /models/staging/schema.yml
    ```yml
    version: 2

    models:
        - name: stg_films
        description: Staging of the raw films dataset from SWAPI.
        columns:
            - name: film_id
            description: Primary key of the dataset.
            tests:
                - unique
                - not_null
          - name: film_title
            description: Title of the film.
          - name: episode
            description: Episode number of the film.
          - name: opening_crawl
            description: Opening text crawl in film intro.
          - name: director
            description: Director of the film.
          - name: producer
            description: Producer(s) of the film.
          - name: release_date
            description: Date of film release (US).
          - name: characters
            description: Array of characters that appear in the film. Relates to raw.people.
          - name: planets
            description: Array of planets that appear in the film. Relates to raw.planets.
          - name: species
            description: Array of species that appear in the film. Relates to raw.species.
          - name: starships
            description: Array of starships that appear in the film. Relates to raw.starships.
          - name: vehicles
            description: Array of vehicles that appear in the film. Relates to raw.vehicles.
          - name: url
            description: Web address for the resource in SWAPI.
          - name: created_date
            description: Date the record was created in SWAPI.
          - name: edited_date
            description: Date the record was last edited in SWAPI.
    ```
1. Add films to the /models/source.yml
    ```yml
    version: 2

    sources:
    - name: raw
        description: Raw data extracted from SWAPI.
        database: swapi_raw
        schema: swapi
        tables:
        - name: films
            description: One record per film.
            columns:
            - name: title
                description: Title of the film.
            - name: episode_id
                description: Episode number of the film.
                test:
                  - unique
                  - not_null
            - name: opening_crawl
                description: Opening text crawl in film intro.
            - name: director
                description: Director of the film.
            - name: producer
                description: Producer(s) of the film.
            - name: release_date
                description: Date of film release (US).
            - name: characters
                description: Array of characters that appear in the film.
            - name: planets
                description: Array of planets that appear in the film.
            - name: starships
                description: Array of starships that appear in the film.
            - name: vehicles
                description: Array of vehicles that appear in the film.
            - name: species
                description: Array of species that appear in the film. 
            - name: created
                description: Date the record was created in SWAPI.
            - name:  edited
                description: Date the record was last edited in SWAPI.
            - name: url
                description: Web address for the resource in SWAPI.
    ```

1. Execute `poetry run dbt build` and check that the data has been created in Snowflake

1. Create and build staging, intermediate and core models for all relevant datasets, including entries in the relevant schema.yml and source.yml files.
--------->

