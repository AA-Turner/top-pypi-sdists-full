import json
import os

import pytest

from codrninja.tools import ToolRegistry
from codrninja.web_tools import WebToolError, extract_text, web_enabled


def test_extract_text_removes_markup():
    html = "<html><body><h1>Hello</h1><script>alert(1)</script><p>World</p></body></html>"
    text = extract_text(html)
    assert "Hello" in text
    assert "World" in text
    assert "alert" not in text


def test_web_fetch_uses_helper(monkeypatch):
    registry = ToolRegistry()

    def fake_fetch(url, timeout=10, max_length=10000):
        assert url == "https://example.com"
        assert timeout == 10
        assert max_length == 10000
        return "Example text"

    monkeypatch.setattr("codrninja.tools.fetch_web_text", fake_fetch)
    result = registry.web_fetch("https://example.com")
    assert result.success is True
    assert result.output == "Example text"


def test_web_search_returns_json(monkeypatch):
    registry = ToolRegistry()

    def fake_search(query, num_results=5):
        assert query == "python"
        assert num_results == 5
        return [{"title": "Python", "url": "https://python.org", "snippet": "Language"}]

    monkeypatch.setattr("codrninja.tools.search_web", fake_search)
    result = registry.web_search("python")
    assert result.success is True
    payload = json.loads(result.output)
    assert payload[0]["title"] == "Python"


def test_web_disabled(monkeypatch):
    monkeypatch.setenv("NO_WEB", "1")
    assert web_enabled() is False
    registry = ToolRegistry()
    result = registry.web_search("python")
    assert result.success is False
    assert "NO_WEB" in result.error
    monkeypatch.delenv("NO_WEB", raising=False)
