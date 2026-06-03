import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import data_engine
from ai_agent import generate_pandas_code

from powerbi_engine import (
    is_powerbi_question,
    process_powerbi_query
)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data_engine import load_data, prep_data

print("Loading dataset...")

GLOBAL_DF = load_data()

if GLOBAL_DF is not None:
    GLOBAL_DF = prep_data(GLOBAL_DF)

print("Dataset loaded successfully!")
# --------------------------------------------------
# FastAPI App
# --------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Query Processor
# --------------------------------------------------
def process_query(user_question):

    print(f"\n🗣️ USER: '{user_question}'")

    global GLOBAL_DF

    if GLOBAL_DF is None:
        return {
            "result": "",
            "summary": "Could not load dataset.",
            "insights": [],
            "recommendations": [],
            "visualization": "table"
        }

    # Use already loaded dataframe
    df = GLOBAL_DF

    # Generate schema for AI
    columns = ", ".join(
        [f"'{col}' ({dtype})" for col, dtype in zip(df.columns, df.dtypes)]
    )

    print("🧠 AI is thinking of the code...")

    code = generate_pandas_code(user_question, columns)

    if not code:
        return {
            "result": "",
            "summary": "Failed to generate code.",
            "insights": [],
            "recommendations": [],
            "visualization": "table"
        }

    print(f"\n⚙️ GENERATED CODE:\n{code}\n")

    local_vars = {
        "df": df,
        "pd": pd
    }

    try:

        exec(code, {}, local_vars)

        result = local_vars.get("result", "")
        summary = local_vars.get("summary", "")
        insights = local_vars.get("insights", [])
        recommendations = local_vars.get("recommendations", [])
        risks = local_vars.get("risks", [])
        future_impact = local_vars.get("future_impact", [])
        visualization = local_vars.get("visualization", "table")

        if isinstance(result, pd.DataFrame):

            result = result.copy()

            numeric_cols = result.select_dtypes(
                include=['number']
            ).columns

            result[numeric_cols] = (
                result[numeric_cols]
                .round(2)
            )

            formatted_result = (
                result.head(20)
                .to_dict(orient="records")
            )

        elif isinstance(result, pd.Series):

            result = result.round(2)

            formatted_result = (
                result.reset_index()
                .to_dict(orient="records")
            )

        elif isinstance(result, (int, float)):

            formatted_result = f"{float(result):.2f}"

        else:

            formatted_result = str(result)

        response = {
            "result": formatted_result,
            "summary": summary,
            "insights": insights,
            "recommendations": recommendations,
            "risks": risks,
            "future_impact": future_impact,
            "visualization": visualization
        }

        print("\n✅ FINAL RESPONSE:")
        print(response)

        return response

    except Exception as e:

        print("❌ EXECUTION ERROR:", e)

        return {
            "result": "",
            "summary": f"Error executing generated code: {str(e)}",
            "insights": [],
            "recommendations": [],
            "risks": [],
            "future_impact": [],
            "visualization": "table"
        }

# --------------------------------------------------
# Request Model
# --------------------------------------------------
class QueryRequest(BaseModel):
    question: str

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "AI Analytics Agent API Running Successfully"
    }

@app.post("/api/ask")
def ask_agent(request: QueryRequest):

    if is_powerbi_question(request.question):

        print("📊 ROUTED TO POWER BI")

        result = process_powerbi_query(
            request.question
        )

    else:

        print("🐼 ROUTED TO PANDAS")

        result = process_query(
            request.question
        )

    return {
        "reply": result
    }   