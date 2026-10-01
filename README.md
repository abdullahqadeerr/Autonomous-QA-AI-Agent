# Autonomous Conversational AI QA Agent

This project is a working QA agent built for Python 3.11+, Playwright, pytest, and Streamlit. It understands a requirement, inspects a website, plans tests, generates Playwright automation, runs execution, collects evidence, analyzes failures, and supports optional Jira integration.

## Quick start

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate it:
   - Windows (PowerShell):
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Windows (cmd):
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python -m playwright install chromium
   ```

4. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
   or
   ```bash
   cp .env.example .env
   ```

5. Add your API key and optional Jira config in `.env`.

6. Run the app:
   ```bash
   python -m streamlit run app.py
   ```

## Docker

```bash
docker compose up --build
```

The app will be available at http://localhost:8501.

## Project structure

- `agent/` – orchestrator, LLM layer, website analysis, planner, repair logic, reporting, Jira integration
- `config/` – centralized settings loading
- `tests/generated/` – generated Playwright/pytest test files
- `reports/` – screenshots, traces, JSON, HTML reports, bug files
- `logs/` – runtime logs

## Notes

- OpenAI is optional. If the API key is missing, the system falls back to deterministic heuristics.
- Jira is optional and requires `JIRA_*` environment variables.
- This project is designed to be portable and not tied to any specific machine path.
