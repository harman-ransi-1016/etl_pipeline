"""Extract: read source CSVs into pandas DataFrames."""
import pandas as pd


def extract_csv(path):
    """Read a CSV file into a DataFrame. Raises if the file is missing/empty."""
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Source file {path} has no rows.")
    return df
