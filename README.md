# Conversational AI Calendar Booking Bot

A simple chatbot to help users book appointments via Google Calendar using natural language.

## Tech Stack
- FastAPI (backend)
- LangChain Agent (LLM-powered booking flow)
- Streamlit (chat frontend)
- Google Calendar API (via Service Account)

## Setup

1. Place your `credentials.json` in the `backend/` folder.
2. Replace your `CALENDAR_ID` in `calendar_utils.py`.
3. Run backend:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

4. Run frontend:
   ```bash
   cd frontend
   streamlit run app.py
   ```
