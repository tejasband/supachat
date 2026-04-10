import json
import logging
import os
import ast

from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_sql_query_chain

logger = logging.getLogger(__name__)


class SupaChatAgent:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self.engine = create_engine(db_uri)

        try:
            self.db = SQLDatabase(
                self.engine,
                include_tables=["articles", "pageviews", "engagement"]
            )

            # ✅ FIXED Gemini model
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.0-pro",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0,
            
            )

        except Exception as e:
            logger.error(f"Error initializing DB or LLM: {e}")
            self.db = None
            self.llm = None

    def run_query(self, user_query: str) -> dict:
        if not self.db or not self.llm:
            raise ValueError(
                "Agent not initialized properly (check DB connection and GOOGLE_API_KEY)."
            )

        try:
            # 🔹 Step 1: Generate SQL
            chain = create_sql_query_chain(self.llm, self.db)
            sql_query = chain.invoke({"question": user_query})

            # Clean SQL output
            if isinstance(sql_query, str):
                if sql_query.startswith("```sql"):
                    sql_query = sql_query[6:-3].strip()
                if sql_query.startswith("SQLQuery:"):
                    sql_query = sql_query[9:].strip()

            print("SQL GENERATED:", sql_query)

            # 🔹 Step 2: Execute SQL
            result_str = self.db.run(sql_query)
            print("DB RESULT:", result_str)

            try:
                result_data = ast.literal_eval(result_str)
            except Exception:
                result_data = [{"raw": result_str}]

            # 🔹 Step 3: Format response using LLM
            format_prompt = f"""
You are a data formatting assistant.

User query: "{user_query}"
SQL executed: {sql_query}
Raw result: {result_str}

Format into JSON:

{{
    "type": "text" | "table" | "barchart" | "linechart",
    "content": "<insight>",
    "data": [{{}}],
    "xAxis": "<x-axis key or null>",
    "yAxis": "<y-axis key or null>"
}}

Rules:
- Use "linechart" for trends/time
- Use "barchart" for comparisons
- Use "table" for lists
- Clean column names
- Output ONLY valid JSON
"""

            response = self.llm.invoke(format_prompt)

            # Handle Gemini response safely
            if hasattr(response, "content"):
                content = response.content
            else:
                content = str(response)

            print("LLM RESPONSE:", content)

            if "```json" in content:
                content = content.split("```json")[-1].split("```")[0].strip()

            return json.loads(content)

        except Exception as e:
            logger.error(f"Error in run_query: {e}")
            return {
                "type": "text",
                "content": f"Error fulfilling query: {str(e)}",
                "data": []
            }