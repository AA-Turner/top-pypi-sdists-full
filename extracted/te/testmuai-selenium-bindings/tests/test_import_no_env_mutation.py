"""The binding must not mutate the host process environment on import.

Importing testmu_selenium must NOT call python-dotenv's load_dotenv(), which
would read a developer's local .env into os.environ. Auteur and HyperExecute
inject env vars themselves; the binding reading them is fine, writing them is not.
"""
import importlib

import dotenv

import testmu_selenium


def test_import_does_not_call_load_dotenv(monkeypatch):
    """Reloading the package (re-runs __init__) must not invoke dotenv.load_dotenv."""
    calls = []
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *a, **k: calls.append((a, k)))
    importlib.reload(testmu_selenium)
    assert calls == []
