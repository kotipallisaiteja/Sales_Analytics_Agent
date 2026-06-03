import pandas as pd
import os

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to Parquet file
PARQUET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sales_data_900K.parquet"
)

def load_data():
    """Loads the sales dataset from Parquet."""
    try:
        df = pd.read_parquet(
            PARQUET_PATH,
            engine="pyarrow"
        )
        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def prep_data(df):
    """Cleans and prepares data types for accurate math."""

    df['Business Date'] = pd.to_datetime(
        df['Business Date'],
        errors='coerce'
    )

    df['Total'] = pd.to_numeric(
        df['Total'],
        errors='coerce'
    ).fillna(0)

    return df


def analyze_outlet_performance(df, top_n=5, underperforming=False):
    """Groups data by Branch Name and sums Total sales."""

    grouped = (
        df.groupby('Branch Name')['Total']
        .sum()
        .reset_index()
    )

    grouped = grouped.sort_values(
        by='Total',
        ascending=underperforming
    )

    return grouped.head(top_n).to_dict('records')


def analyze_channel_sales(df):
    """Groups data by Channel and sums Total sales."""

    grouped = (
        df.groupby('Channel')['Total']
        .sum()
        .reset_index()
    )

    grouped = grouped.sort_values(
        by='Total',
        ascending=False
    )

    return grouped.to_dict('records')


if __name__ == "__main__":

    print("--- LOADING PARQUET DATASET ---")

    df = load_data()

    if df is not None:

        print("\n✅ Dataset loaded successfully!")

        df = prep_data(df)

        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        print("\n📊 Top 3 Branches")
        print(
            analyze_outlet_performance(
                df,
                top_n=3,
                underperforming=False
            )
        )

        print("\n📉 Bottom 3 Branches")
        print(
            analyze_outlet_performance(
                df,
                top_n=3,
                underperforming=True
            )
        )

        print("\n📈 Channel Sales")
        print(
            analyze_channel_sales(df)
        )

    else:
        print("❌ Failed to load dataset.")