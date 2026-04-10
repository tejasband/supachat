
# SupaChat 🚀

SupaChat is a conversational analytics app built on top of PostgreSQL, FastAPI, and Next.js. It leverages LLMs to translate natural language into SQL queries, providing dynamic data visualizations (Recharts) automatically.

## Architecture
- **Database**: PostgreSQL (Simulating Supabase)
- **Backend**: FastAPI with Python and LangChain for LLM/MCP capabilities
- **Frontend**: Next.js App Router with Vanilla CSS Glassmorphic design
- **Visuals**: Recharts for dynamic visual data representation

## Local Setup

### 1. Database
```bash
docker-compose up -d db
```
*(This starts PostgreSQL on port 5432 and seeds the initial tables).*

### 2. Backend
1. Navigate to the `backend` folder.
2. Create and activate a Virtual Environment.
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate # Mac/Linux
```
3. Install dependencies: `pip install -r requirements.txt`
4. Update `.env` with your actual `OPENAI_API_KEY`.
5. Run the server: `uvicorn main:app --reload` (Runs on http://localhost:8000)

### 3. Frontend
1. Navigate to the `frontend` folder.
2. Install dependencies: `npm install`
3. Run dev server: `npm run dev` (Runs on http://localhost:3000)

## Example Queries to Try
1. "Show top trending topics in last 30 days"
2. "Compare article engagement by topic"
3. "Plot daily views trend for AI articles"

