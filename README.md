# Git Project 1 — ETL Pipeline (Python → Snowflake)

A small, real EL pipeline: extract CSVs → light transform → load into Snowflake raw
tables. These raw tables are exactly the `*_SRC` sources your dbt project reads, so this
is the **"loader" layer that feeds dbt** (the E and L of ELT; dbt does the T).

This repo is also the **vehicle for Git Project 1** — see `GIT_EXERCISE.md` to practice
branching, rebasing, squashing, and PRs on it.

## What it does
- **Extract** — reads CSV files from `data/`.
- **Transform** — light cleanup (strip whitespace, standardize column names/casing, add a `_loaded_at` audit timestamp).
- **Load** — writes each into `PC_DBT_DB.PUBLIC.<TABLE>` in Snowflake (create-or-replace).

## Structure
```
etl_pipeline/
├── README.md
├── requirements.txt
├── .env.example          # copy to .env, fill in Snowflake creds (never commit .env)
├── .gitignore
├── config/
│   └── tables.yml        # CSV -> target table mapping
├── data/
│   └── customers.csv     # sample source data
├── src/
│   ├── db.py             # Snowflake connection helper
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── main.py               # orchestrates E -> T -> L
└── GIT_EXERCISE.md       # the git practice guide
```

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then edit .env with your Snowflake details
```

`.env` (use the LEGACY_SERVICE user you made, or your dev user):
```
SNOWFLAKE_ACCOUNT=WQBEAFK-RGC24255
SNOWFLAKE_USER=DBT_PROD_USER
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=PC_DBT_ROLE
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=PC_DBT_DB
SNOWFLAKE_SCHEMA=PUBLIC
```

## Run
```bash
python main.py                 # run the whole pipeline for all tables in config
python main.py --table customers   # just one
python main.py --dry-run       # extract+transform, print rows, skip the load
```

## Notes
- Secrets live only in `.env` (gitignored). Never commit credentials.
- `--dry-run` lets you test extract/transform without touching Snowflake.
 # tiny change to README
