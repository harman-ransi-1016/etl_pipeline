"""ETL Pipeline entry point: extract CSVs -> transform -> load into Snowflake.

Usage:
    python main.py                  # all tables in config/tables.yml
    python main.py --table customers
    python main.py --dry-run        # extract + transform only, no load
"""
import argparse
import sys
import yaml

from src.extract import extract_csv
from src.transform import transform
from src.load import load_dataframe


def load_config(path="config/tables.yml"):
    with open(path) as f:
        return yaml.safe_load(f)["tables"]


def run(table_filter=None, dry_run=False):
    tables = load_config()
    if table_filter:
        tables = [t for t in tables if t["name"] == table_filter]
        if not tables:
            print(f"No table named '{table_filter}' in config.")
            sys.exit(1)

    conn = None
    if not dry_run:
        from src.db import get_connection
        conn = get_connection()

    try:
        for t in tables:
            print(f"[extract] {t['csv']}")
            df = extract_csv(t["csv"])
            print(f"[transform] {len(df)} rows")
            df = transform(df)

            if dry_run:
                print(f"[dry-run] would load {len(df)} rows into {t['target_table']}")
                print(df.head().to_string(index=False))
            else:
                n = load_dataframe(conn, df, t["target_table"])
                print(f"[load] {n} rows -> {t['target_table']}")
    finally:
        if conn:
            conn.close()
    print("Done.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="CSV -> Snowflake ETL pipeline.")
    p.add_argument("--table", help="Run only this table (by config name).")
    p.add_argument("--dry-run", action="store_true", help="Extract+transform only; skip load.")
    args = p.parse_args()
    run(table_filter=args.table, dry_run=args.dry_run)
