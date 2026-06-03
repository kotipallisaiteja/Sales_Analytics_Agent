import pandas as pd
import os

# Project root
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "Sample_Sales_Data.csv"
)

PARQUET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sales_data.parquet"
)

print("Loading CSV...")
print(CSV_PATH)

df = pd.read_csv(
    CSV_PATH,
    low_memory=False
)

print("Converting to Parquet...")

df.to_parquet(
    PARQUET_PATH,
    engine="pyarrow",
    index=False
)

print("Done!")
print("Saved to:", PARQUET_PATH)