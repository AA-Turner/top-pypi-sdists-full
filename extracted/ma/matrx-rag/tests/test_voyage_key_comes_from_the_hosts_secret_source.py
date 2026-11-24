"""The Voyage key is read at CALL time: the host's ``secret_source`` when injected, else the environment.

Standalone (no source) the package reads ``VOYAGE_API_KEY`` from its own environment exactly as before; with a
source injected the source's answer is final (an empty answer is "not set", never the environment copy); and a
changed key rebuilds the client on the next call, so a rotation needs no restart.
"""

from __future__ import annotations

import sys
import types

import pytest

from matrx_rag import _ext
from matrx_rag.embeddings import DefaultOpenAIVoyageProvider


@pytest.fixture
def fake_voyage(monkeypatch):
    built: list[str] = []

    class _Client:
        def __init__(self, api_key: str) -> None:
            built.append(api_key)
            self.api_key = api_key

    monkeypatch.setitem(sys.modules, "voyageai", types.SimpleNamespace(Client=_Client))
    monkeypatch.delitem(_ext._registry, "secret_source", raising=False)
    return built


def test_unset_everywhere_is_not_set(fake_voyage, monkeypatch):
    monkeypatch.delenv("VOYAGE_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="VOYAGE_API_KEY not set"):
        DefaultOpenAIVoyageProvider()._voyage()
    assert fake_voyage == []


def test_no_source_reads_the_environment(fake_voyage, monkeypatch):
    monkeypatch.setenv("VOYAGE_API_KEY", "env-key")
    DefaultOpenAIVoyageProvider()._voyage()
    assert fake_voyage == ["env-key"]


def test_injected_source_answers_and_rotation_rebuilds(fake_voyage, monkeypatch):
    monkeypatch.setenv("VOYAGE_API_KEY", "env-key")
    held = {"VOYAGE_API_KEY": "vault-1"}
    monkeypatch.setitem(_ext._registry, "secret_source", held.get)
    provider = DefaultOpenAIVoyageProvider()
    first = provider._voyage()
    assert provider._voyage() is first  # same key: same client
    held["VOYAGE_API_KEY"] = "vault-2"
    assert provider._voyage() is not first
    assert fake_voyage == ["vault-1", "vault-2"]


def test_an_unreadable_held_key_is_not_configured(fake_voyage, monkeypatch):
    # The host answers "" for a held key that does not decrypt: the not-set branch, never the env copy.
    monkeypatch.setenv("VOYAGE_API_KEY", "env-key")
    monkeypatch.setitem(_ext._registry, "secret_source", lambda name: "")
    with pytest.raises(RuntimeError, match="VOYAGE_API_KEY not set"):
        DefaultOpenAIVoyageProvider()._voyage()
    assert fake_voyage == []
