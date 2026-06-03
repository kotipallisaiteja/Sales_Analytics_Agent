import pandas as pd
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PARQUET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sales_data.parquet"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sales_data_900K.parquet"
)

print("Loading dataset...")

df = pd.read_parquet(PARQUET_PATH)

print("Original shape:", df.shape)

# Keep 900,000 random rows
df_small = df.sample(
    n=900_000,
    random_state=42
)

print("New shape:", df_small.shape)

print("Saving...")

df_small.to_parquet(
    OUTPUT_PATH,
    engine="pyarrow",
    index=False
)

print("Done!")
print("Saved to:", OUTPUT_PATH)