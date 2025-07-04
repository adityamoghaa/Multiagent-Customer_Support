# Multi-Agent Customer Support System
A modular, inteligent, multi-agent support platform powered by NLP, Hugging Face, CrewAI and SQLAlchemy.

## Features

- Specialized agents (Technical, Billing, Product, Escalation)
- NLP ticket classification and sentiment analysis
- Language detection and translation
- Voice (speech-to-text & text-to-speech)
- Proactive suggestions (LLM)
- REST API (FastAPI) and CLI interface

## Setup

See `docs/SETUP.md` for instructions.

## Usage

- Start the API:
    ```bash
    uvicorn multiagent_support.api:app --reload
    ```

- Command-line interface:
    ```bash
    python -m multiagent_support.cli
    ```

- API endpoints:
    - `POST /ticket` — Submit a support request
    - `POST /ticket/audio` — Submit a WAV audio file
    - `GET /ticket/{id}` — Get ticket details

## Extending (In progress)

- Add new agents in `agents.py`
- Improve classifiers or sentiment in `classifier.py` and `sentiment.py`
- Expand CLI or API as needed

MIT License
