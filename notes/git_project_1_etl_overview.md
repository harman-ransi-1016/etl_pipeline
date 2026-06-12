# Git Project 1 — ETL Pipeline: Overview & Context

Context document for the first git build project. Explains what the project *is*, how it's
built, how it connects to the dbt work, and which git skills were practiced on it.
(Hands-on steps live in the repo's `GIT_EXERCISE.md`; this is the "what & why".)

---

## What this project is
A small, real **EL pipeline** in Python: it reads CSV files, lightly cleans them, and loads
them into Snowflake raw tables. It is the **"loader" layer** of the modern data stack —
the **E and L of ELT** (dbt does the T).

Crucially: the tables it creates (`CUSTOMER_SRC`, `SALES_SRC`, …) are **exactly the sources
the dbt project reads**. So this project produces the upstream data that dbt then transforms.
End to end: **CSV → (this pipeline) → Snowflake `*_SRC` → dbt `source()` → staging → marts.**

## How it works (architecture)
```
data/*.csv  ──extract──►  pandas DataFrame  ──transform──►  cleaned + _LOADED_AT  ──load──►  Snowflake PC_DBT_DB.PUBLIC.<TABLE>
```
- **Extract** (`src/extract.py`) — read CSV into a DataFrame.
- **Transform** (`src/transform.py`) — light cleanup only (standardize column names to
  UPPER, trim whitespace, add a `_LOADED_AT` audit timestamp for dbt source freshness).
  The *heavy* transform is deliberately left to dbt.
- **Load** (`src/load.py`) — create-or-replace the target table and insert rows.
- **Config-driven** (`config/tables.yml`) — maps each CSV to its target table; add a source
  by adding a YAML entry (no code change).
- **Orchestration** (`main.py`) — runs extract → transform → load; supports `--table` and
  `--dry-run` (extract+transform without touching Snowflake).
- **Secrets** — Snowflake creds in `.env` (gitignored); `.env.example` shows the shape.

## How it ties to the dbt work
- `tables.yml` here says *"load customers.csv INTO `CUSTOMER_SRC`"* (creates the table).
- dbt's `_sources.yml` says *"`CUSTOMER_SRC` is a raw source AT `PC_DBT_DB.PUBLIC`"* (points
  at it). Two sides of the same table — this writes it, dbt reads it.
- The `_LOADED_AT` column this adds is what dbt **source freshness** checks downstream.

## Git skills practiced on this repo
This repo was the *vehicle* for the git module's hands-on:
- **Feature branch + PR** — added a `sales` source on `feature/add-sales-source`, opened a
  PR, merged into `main`, cleaned up the branch.
- **Squashing** — made 3 messy WIP commits, collapsed them into one with `git rebase -i`.
- **Rebasing** — advanced `main` (a README tweak), then `git rebase origin/main` to replay
  the feature branch on top → linear history.
- **Merge conflict** — made `main` and a branch edit the same line of `config/settings.txt`
  (12 vs 48), hit a real CONFLICT on `git merge`, resolved it in the VS Code merge editor,
  and committed the merge.

## Friction hit (and the lessons)
- **SSH vs HTTPS auth** — SSH push failed (no key); switched the remote to HTTPS, which uses
  the normal login flow. (Browser login ≠ git CLI auth.)
- **Editor confusion** — `code --wait` failed (the `code` CLI wasn't installed); switched
  `core.editor` to `nano` for the interactive rebase.
- **`git commit -am` with no edit** — "nothing to commit" because `-a` only commits *changed*
  tracked files; you must actually edit the file first (`echo >` forces it).
- **`-u` on first push** — `git push -u origin <branch>` sets the upstream link on a new
  branch's first push; after that, bare `git push` works.
- **Pasted-in `#` comments** — broke shell commands; keep comments out of pasted commands.

## How to run it
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # fill in Snowflake creds
python main.py --dry-run   # extract+transform only (no Snowflake)
python main.py             # full pipeline -> loads into Snowflake
```

## Status
Project 1 complete — functional pipeline + all git exercises (branch/PR, squash, rebase,
merge conflict) done on the real GitHub repo. Could be extended into a portfolio piece
(more sources, scheduling, logging, tests) later.

**Next:** Git Project 2 — Data Quality Engine (pending, planned for tomorrow). Its code +
`GIT_EXERCISE.md` already exist in `git_project_2_data_quality_engine/`.
