# Structured Extraction with Prompt Caching

Extract structured metadata from any text — title, summary, key points, entities, sentiment — using Claude's structured output capability and prompt caching.

## What this shows

- **Prompt caching**: The system prompt is cached after the first call. Subsequent calls with the same system prompt are faster and ~90% cheaper for that portion of input.
- **Structured output**: Claude returns valid JSON directly, no post-processing needed.
- **Cache hit/miss reporting**: The demo prints token counts including cache creation and cache read tokens so you can see the savings.

## Run it

```bash
pip install -r requirements.txt

# Requires ANTHROPIC_API_KEY in .env (copy from ../../.env.example)
python demo.py                  # built-in sample article
python demo.py path/to/text.txt # your own text file
```

## Expected output

```
Extracting from: built-in sample article

First call (cache miss — system prompt is written to cache)...
Tokens — input: 412, output: 198, cache_written: 312

Second call (cache hit — system prompt is read from cache, cheaper)...
Tokens — input: 100, output: 198, cache_read: 312

Extracted data:
{
  "title": "Anthropic Releases Claude 3.5 Sonnet ...",
  ...
}
```

## Tests

```bash
pip install pytest
pytest test_demo.py -v
```

Tests mock the Anthropic API so no key is needed.
