# AI-tools

This project is a static AI tools website with a FastAPI backend powering several AI endpoints.

## Features

- `index.html` - Home landing page with navigation
- `text_generator.html` - Generate text responses from the AI backend
- `friendly.html` - Chat with a jokester-style assistant
- `topic.html` - Ask questions within a specific topic context
- `summarizer.html` - Summarize text inputs
- `code-generator.html` - Generate code from prompts

## Backend

The backend is implemented in `API/main.py` using FastAPI and the GroQ client.

## Setup

1. Create and activate a Python virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Add your GroQ API key in a `.env` file in the project root:

   ```text
   GROK_API_KEY=your_api_key_here
   ```

4. Run the backend server:

   ```powershell
   uvicorn API.main:app --reload
   ```

5. Open the HTML pages in your browser or serve the site with a simple static server.

## Notes

- The backend now includes the `/text_generator` endpoint expected by `text_generator.html`.
- All frontend tool pages call the local API at `http://127.0.0.1:8000`.
