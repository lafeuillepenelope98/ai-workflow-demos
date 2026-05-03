# AI Workflow Demos

Actionable Claude API demos and tutorials — working code that you can run in under 5 minutes.

## What's here

```
demos/               Standalone runnable demos (each is self-contained)
  structured-extraction/   Extract structured data from text with prompt caching
  prompt-caching-chat/     Multi-turn chat with cached system prompt
tutorials/           Step-by-step written tutorials (with embedded code)
shared/              Utilities shared across demos
```

## Prerequisites

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

## Quickstart

```bash
# 1. Clone
git clone https://github.com/lafeuillepenelope98/ai-workflow-demos.git
cd ai-workflow-demos

# 2. Copy env file and add your key
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=sk-ant-...

# 3. Run a demo (each demo has its own venv/deps)
cd demos/structured-extraction
pip install -r requirements.txt
python demo.py
```

## Running all examples locally

Each demo is self-contained. From the repo root:

```bash
# Install dev tools
pip install ruff pytest

# Lint all Python files
ruff check .

# Run tests (no API key required — API is mocked)
pytest
```

## CI

GitHub Actions runs on every push and PR:

- **Lint** — `ruff` checks all Python files
- **Test** — `pytest` with mocked API calls (no API key required)
- **Integration** — full demo run when `ANTHROPIC_API_KEY` is set as a repo secret

## Contributing

1. Create a folder under `demos/` or `tutorials/`
2. Include a `README.md`, `requirements.txt`, and at least one test
3. Use prompt caching where the system prompt is >1024 tokens
4. No hardcoded API keys — use `python-dotenv` and `.env`

## Code standard

- Every demo runs end-to-end with `python demo.py`
- Prompt caching is used where applicable (cached system prompts, large context)
- Tests mock the Anthropic API so CI doesn't require a live key
