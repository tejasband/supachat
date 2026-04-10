import logging
import ast
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase

logger = logging.getLogger(__name__)


class SupaChatAgent:
    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri)
        self.db = SQLDatabase(
            self.engine,
            include_tables=["articles", "pageviews", "engagement"]
        )

    # =========================
    # 🔧 HELPER FUNCTION
    # =========================

    def format_table(self, columns, rows):
        return [dict(zip(columns, row)) for row in rows]

    # =========================
    # 🔧 MCP TOOLS
    # =========================

    def get_all_articles(self):
        query = "SELECT id, title, topic, author, created_at FROM articles LIMIT 5;"
        result = self.db.run(query)

        rows = ast.literal_eval(result)
        columns = ["id", "title", "topic", "author", "created_at"]

        return self.format_table(columns, rows)

    def count_articles(self):
        result = self.db.run("SELECT COUNT(*) FROM articles;")
        rows = ast.literal_eval(result)

        return rows[0][0]

    def trending_topics(self):
        query = """
        SELECT topic, COUNT(*) as count
        FROM articles
        GROUP BY topic
        ORDER BY count DESC
        LIMIT 5;
        """
        result = self.db.run(query)

        rows = ast.literal_eval(result)
        columns = ["topic", "count"]

        return self.format_table(columns, rows)

    def engagement_by_topic(self):
        query = """
        SELECT topic, SUM(engagement) as total_engagement
        FROM engagement
        GROUP BY topic
        ORDER BY total_engagement DESC;
        """
        result = self.db.run(query)

        rows = ast.literal_eval(result)
        columns = ["topic", "total_engagement"]

        return self.format_table(columns, rows)

    def daily_views(self):
        query = """
        SELECT date, SUM(views) as views
        FROM pageviews
        GROUP BY date
        ORDER BY date;
        """
        result = self.db.run(query)

        rows = ast.literal_eval(result)
        columns = ["date", "views"]

        return self.format_table(columns, rows)

    # =========================
    # 🧠 MCP AGENT (ROUTER)
    # =========================

    def run_query(self, user_query: str) -> dict:
        query = user_query.lower()

        try:
            if "all articles" in query:
                result = self.get_all_articles()
                return {
                    "type": "table",
                    "content": "Showing latest articles",
                    "data": result
                }

            elif "count" in query or "how many" in query:
                result = self.count_articles()
                return {
                    "type": "text",
                    "content": f"Total articles: {result}",
                    "data": []
                }

            elif "trending" in query:
                result = self.trending_topics()
                return {
                    "type": "barchart",
                    "content": "Trending topics",
                    "data": result,
                    "xAxis": "topic",
                    "yAxis": "count"
                }

            elif "engagement" in query:
                result = self.engagement_by_topic()
                return {
                    "type": "barchart",
                    "content": "Engagement by topic",
                    "data": result,
                    "xAxis": "topic",
                    "yAxis": "total_engagement"
                }

            elif "views" in query or "trend" in query:
                result = self.daily_views()
                return {
                    "type": "linechart",
                    "content": "Daily views trend",
                    "data": result,
                    "xAxis": "date",
                    "yAxis": "views"
                }

            else:
                return {
                    "type": "text",
                    "content": "Sorry, I could not understand the query.",
                    "data": []
                }

        except Exception as e:
            logger.error(f"Error: {e}")
            return {
                "type": "text",
                "content": f"Error: {str(e)}",
                "data": []
            }