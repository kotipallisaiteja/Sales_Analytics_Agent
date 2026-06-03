import os
import pandas as pd

from ai_agent import route_powerbi_dataset

# --------------------------------------------------
# Load Power BI CSVs
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

POWERBI_DIR = os.path.join(
    BASE_DIR,
    "..",
    "powerbi"
)

channel_df = pd.read_csv(
    os.path.join(
        POWERBI_DIR,
        "Channel-wise Net Sales.csv"
    )
)

city_df = pd.read_csv(
    os.path.join(
        POWERBI_DIR,
        "City-wise Net Sales MRR.csv"
    )
)

daily_df = pd.read_csv(
    os.path.join(
        POWERBI_DIR,
        "Daily Net Sales and Orders.csv"
    )
)

format_df = pd.read_csv(
    os.path.join(
        POWERBI_DIR,
        "Format-wise Net Sales.csv"
    )
)

# --------------------------------------------------
# Gemini Router
# --------------------------------------------------

def is_powerbi_question(question):
    # try:

    #     dataset = route_powerbi_dataset(
    #         question
    #     )

    #     return dataset in [
    #         "channel",
    #         "city",
    #         "daily",
    #         "format"
    #     ]

    # except Exception:

    #     return False

    # # Disabled Power BI routing to force all queries through the dynamic pandas agent
    return False






# --------------------------------------------------
# Main Power BI Engine
# --------------------------------------------------

def process_powerbi_query(question):

    dataset = route_powerbi_dataset(
        question
    )

    print(
        f"📊 POWER BI DATASET SELECTED: {dataset}"
    )

    if dataset == "channel":

        result = (
            channel_df
            .sort_values(
                "Final_NS",
                ascending=False
            )
            .round(2)
        )
        print(result.head())

        top_channel = result.iloc[0]

        return {
            "result":
                result.to_dict(
                    orient="records"
                ),

            "summary":
                "Channel-wise Net Sales analysis.",

            "insights": [
                f"Highest performing channel is {top_channel['Channel']}."
            ],

            "recommendations": [
                "Invest more in the highest-performing channels.",
                "Review low-performing channels for optimization."
            ],

            "visualization":
                "bar_chart"
        }

    # ------------------------------------------
    # CITY ANALYSIS
    # ------------------------------------------

    elif dataset == "city":

        result = (
            city_df
            .sort_values(
                "Curr. Net Sales",
                ascending=False
            )
            .round(2)
        )

        top_city = result.iloc[0]

        return {
            "result":
                result.to_dict(
                    orient="records"
                ),

            "summary":
                "City-wise sales and growth analysis.",

            "insights": [
                f"Top city is {top_city['City']}.",
                "Growth % can be used to identify expansion opportunities."
            ],

            "recommendations": [
                "Increase focus on fast-growing cities.",
                "Investigate cities with negative growth."
            ],

            "visualization":
                "bar_chart"
        }

    # ------------------------------------------
    # DAILY TREND
    # ------------------------------------------

    elif dataset == "daily":

        result = (
            daily_df
            .sort_values(
                "MonthDate"
            )
            .round(2)
        )

        return {
            "result":
                result.to_dict(
                    orient="records"
                ),

            "summary":
                "Daily sales and orders trend analysis.",

            "insights": [
                "Track daily sales fluctuations.",
                "Identify peak and low-performing days."
            ],

            "recommendations": [
                "Increase staffing during peak days.",
                "Run promotions during low-volume periods."
            ],

            "visualization":
                "line_chart"
        }

    # ------------------------------------------
    # FORMAT ANALYSIS
    # ------------------------------------------

    elif dataset == "format":

        result = (
            format_df
            .round(2)
        )

        return {
            "result":
                result.to_dict(
                    orient="records"
                ),

            "summary":
                "Format-wise Net Sales analysis.",

            "insights": [
                "Different formats contribute differently to revenue."
            ],

            "recommendations": [
                "Focus on the most profitable formats."
            ],

            "visualization":
                "bar_chart"
        }

    # ------------------------------------------
    # FALLBACK
    # ------------------------------------------

    return {
        "result":
            "Information not available",

        "summary":
            "Could not determine the correct Power BI dataset.",

        "insights": [],

        "recommendations": [],

        "visualization":
            "table"
    }