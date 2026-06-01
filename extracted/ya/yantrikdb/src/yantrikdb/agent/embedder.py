"""Lightweight HTTP-based embedder using llama.cpp embedding server."""

from __future__ import annotations

import logging

import httpx

log = logging.getLogger("yantrik.embedder")


class LlamaEmbedder:
    """Embedder that calls llama-server's /embedding endpoint.

    Compatible with YantrikDB's embedder protocol (has .encode(text) method).
    """

    def __init__(self, base_url: str = "http://localhost:8082", timeout: float = 30.0):
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(base_url=self._base_url, timeout=timeout)

    def encode(self, text: str) -> list[float]:
        """Encode text to embedding vector. Called by YantrikDB Rust engine."""
        resp = self._client.post("/embedding", json={"input": text})
        resp.raise_for_status()
        data = resp.json()

        # llama-server returns: [{"embedding": [[...384 floats...]]}]
        if isinstance(data, list) and len(data) > 0:
            emb = data[0].get("embedding", [])
        elif isinstance(data, dict):
            # OpenAI-compatible format
            emb_data = data.get("data", [{}])
            emb = emb_data[0].get("embedding", []) if emb_data else []
        else:
            emb = []

        # Unwrap nested list if needed: [[...floats...]] → [...floats...]
        if emb and isinstance(emb[0], list):
            emb = emb[0]

        return emb

    def close(self):
        self._client.close()
