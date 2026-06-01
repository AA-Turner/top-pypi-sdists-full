"""Infer tool category from tool name/description for component registry matching."""

from __future__ import annotations

import re

_SEARCH_PATTERN = re.compile(
    r"(?i)\b(tavily|exa|serp|brave|google.search|bing|duckduckgo|firecrawl|perplexity)\b"
)
_DATABASE_PATTERN = re.compile(
    r"(?i)\b(postgres|mysql|mongo|redis|dynamodb|elasticsearch|supabase|sqlite|sql)\b"
)
_VECTOR_DB_PATTERN = re.compile(
    r"(?i)\b(pinecone|qdrant|weaviate|chroma|pgvector|milvus|vector.?db|vector.?store)\b"
)
_API_PATTERN = re.compile(r"(?i)\b(slack|github|jira|notion|google.drive|webhook|http|discord)\b")
_MCP_PATTERN = re.compile(r"(?i)\bmcp\b")
_STT_PATTERN = re.compile(r"(?i)\b(deepgram.stt|whisper|speech.to.text|transcri)\b")
_TTS_PATTERN = re.compile(r"(?i)\b(deepgram.tts|elevenlabs|text.to.speech)\b")


def infer_tool_category(
    tool_name: str | None,
    tool_description: str | None = None,
) -> str | None:
    """Return a category hint for a tool based on its name/description.

    Returns one of: "search", "database", "vector_db", "api", "mcp",
    "stt", "tts", or None if unknown.
    """
    raw = (tool_name or "") + " " + (tool_description or "")
    if not raw.strip():
        return None
    # Normalize underscores/hyphens to spaces for word-boundary matching
    text = raw.replace("_", " ").replace("-", " ")

    if _SEARCH_PATTERN.search(text):
        return "search"
    if _VECTOR_DB_PATTERN.search(text):
        return "vector_db"
    if _DATABASE_PATTERN.search(text):
        return "database"
    if _STT_PATTERN.search(text):
        return "stt"
    if _TTS_PATTERN.search(text):
        return "tts"
    if _MCP_PATTERN.search(text):
        return "mcp"
    if _API_PATTERN.search(text):
        return "api"
    return None
