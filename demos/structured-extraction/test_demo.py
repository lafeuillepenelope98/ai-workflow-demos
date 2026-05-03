"""Tests for the structured-extraction demo (API is mocked — no key required)."""

import json
from unittest.mock import MagicMock

import demo

MOCK_RESULT = {
    "title": "Test Article",
    "summary": "A test summary.",
    "key_points": ["Point one", "Point two"],
    "entities": {"people": [], "organizations": ["Anthropic"], "topics": ["AI"]},
    "sentiment": "neutral",
    "word_count": 42,
}


def _make_mock_response(text: str, input_tokens=100, output_tokens=50, cache_creation=80, cache_read=0):
    usage = MagicMock()
    usage.input_tokens = input_tokens
    usage.output_tokens = output_tokens
    usage.cache_creation_input_tokens = cache_creation
    usage.cache_read_input_tokens = cache_read

    content_block = MagicMock()
    content_block.text = text

    response = MagicMock()
    response.usage = usage
    response.content = [content_block]
    return response


def test_extract_returns_parsed_json():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _make_mock_response(json.dumps(MOCK_RESULT))

    result, stats = demo.extract("some text", mock_client)

    assert result["title"] == "Test Article"
    assert result["sentiment"] == "neutral"
    assert stats["input_tokens"] == 100


def test_extract_passes_cache_control():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _make_mock_response(json.dumps(MOCK_RESULT))

    demo.extract("some text", mock_client)

    call_kwargs = mock_client.messages.create.call_args[1]
    system = call_kwargs["system"]
    assert isinstance(system, list)
    assert system[0]["cache_control"] == {"type": "ephemeral"}


def test_extract_cache_hit_stats():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _make_mock_response(
        json.dumps(MOCK_RESULT), input_tokens=20, cache_read=80
    )

    _, stats = demo.extract("some text", mock_client)

    assert stats["cache_read_tokens"] == 80
    assert stats["input_tokens"] == 20


def test_sample_article_is_nonempty():
    assert len(demo.SAMPLE_ARTICLE.strip()) > 100


def test_system_prompt_mentions_json():
    assert "JSON" in demo.SYSTEM_PROMPT
    assert "title" in demo.SYSTEM_PROMPT
