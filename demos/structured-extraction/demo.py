"""
Structured extraction demo using Claude with prompt caching.

Extract article metadata (title, summary, key points, entities) from raw text.
The system prompt is cached so repeated runs are faster and cheaper.

Usage:
    python demo.py                  # runs with a built-in sample article
    python demo.py article.txt      # reads text from a file
"""

import json
import os
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a precise content analyst. Given a piece of text, extract structured metadata and return it as valid JSON with exactly these fields:

{
  "title": "string — inferred or extracted title (max 100 chars)",
  "summary": "string — 2-3 sentence neutral summary",
  "key_points": ["array of 3-5 main points as short strings"],
  "entities": {
    "people": ["named people mentioned"],
    "organizations": ["companies or orgs mentioned"],
    "topics": ["main topic tags, max 5"]
  },
  "sentiment": "positive | neutral | negative",
  "word_count": 0
}

Rules:
- Return ONLY the JSON object — no markdown fences, no extra text
- If a field has no data, use an empty array [] or empty string ""
- word_count is the approximate count of words in the source text
- Keep key_points concise (under 15 words each)
"""

SAMPLE_ARTICLE = """
Anthropic Releases Claude 3.5 Sonnet With Major Performance Improvements

San Francisco-based AI safety company Anthropic has released Claude 3.5 Sonnet,
a significant upgrade to its Claude 3 Sonnet model. The new release delivers
faster response times and improved performance on coding, reasoning, and
vision tasks — while remaining at the same price point as its predecessor.

In internal benchmarks, Claude 3.5 Sonnet outperformed GPT-4o and Gemini 1.5
Pro on several software engineering tasks. The model introduces a new
"Artifacts" feature in Claude.ai that lets users work with generated code,
documents, and other content in a dedicated side panel.

Anthropic CEO Dario Amodei said the company continues to focus on AI safety
research alongside capability improvements. The company recently raised $4 billion
from Amazon and Google combined, valuing it at $18.4 billion.

Claude 3.5 Sonnet is available via the Anthropic API, Amazon Bedrock, and
Google Cloud Vertex AI. Anthropic plans to release Claude 3.5 Opus and
Claude 3.5 Haiku later this year to complete the model family refresh.
"""


def extract(text: str, client: anthropic.Anthropic) -> dict:
    response = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": text}],
    )

    cache_stats = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cache_creation_tokens": getattr(response.usage, "cache_creation_input_tokens", 0),
        "cache_read_tokens": getattr(response.usage, "cache_read_input_tokens", 0),
    }

    return json.loads(response.content[0].text), cache_stats


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
        print(f"Extracting from: {sys.argv[1]}")
    else:
        text = SAMPLE_ARTICLE
        print("Extracting from: built-in sample article")

    print("\nFirst call (cache miss — system prompt is written to cache)...")
    result, stats = extract(text, client)
    print(f"Tokens — input: {stats['input_tokens']}, output: {stats['output_tokens']}, "
          f"cache_written: {stats['cache_creation_tokens']}")

    print("\nSecond call (cache hit — system prompt is read from cache, cheaper)...")
    result, stats = extract(text, client)
    print(f"Tokens — input: {stats['input_tokens']}, output: {stats['output_tokens']}, "
          f"cache_read: {stats['cache_read_tokens']}")

    print("\nExtracted data:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
