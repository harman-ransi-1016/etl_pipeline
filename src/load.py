"""Load: write a DataFrame into a Snowflake table (create-or-replace)."""


def _sql_type(dtype):
    """Map a pandas dtype to a Snowflake column type (simple heuristic)."""
    s = str(dtype)
    if "int" in s:
        return "NUMBER"
    if "float" in s:
        return "FLOAT"
    if "datetime" in s:
        return "TIMESTAMP_NTZ"
    return "STRING"


def load_dataframe(conn, df, target_table):
    """Create-or-replace `target_table` and insert all rows from `df`."""
    cols = list(df.columns)
    col_defs = ", ".join(f'"{c}" {_sql_type(df[c].dtype)}' for c in cols)
    col_list = ", ".join(f'"{c}"' for c in cols)
    placeholders = ", ".join(["%s"] * len(cols))

    cur = conn.cursor()
    try:
        cur.execute(f"CREATE OR REPLACE TABLE {target_table} ({col_defs})")
        rows = [tuple(None if str(v) == "nan" else v for v in row) for row in df.itertuples(index=False, name=None)]
        cur.executemany(
            f"INSERT INTO {target_table} ({col_list}) VALUES ({placeholders})", rows
        )
        conn.commit()
        return len(rows)
    finally:
        cur.close()
