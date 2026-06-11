"""Transform: light cleanup only (the heavy T is dbt's job).

Standardizes column names, trims string whitespace, and adds a _loaded_at audit
timestamp so downstream dbt source freshness has a column to check.
"""
import pandas as pd


def transform(df):
    out = df.copy()

    # standardize column names: strip + uppercase (matches the *_SRC convention)
    out.columns = [c.strip().upper() for c in out.columns]

    # trim whitespace on string columns
    for col in out.select_dtypes(include="object").columns:
        out[col] = out[col].str.strip()

    # audit timestamp for source freshness downstream
    out["_LOADED_AT"] = pd.Timestamp.utcnow().tz_localize(None)

    return out
