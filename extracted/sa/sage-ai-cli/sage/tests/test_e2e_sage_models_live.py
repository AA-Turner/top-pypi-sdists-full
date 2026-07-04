"""
Live SAGE E2E: `ProviderRouter.generate` across model types your environment supports.

- OpenAI-compat (Groq, OpenRouter, …): every *registered* id per key-bearing provider
- Gemini: every free id when a Gemini key is present
- Ollama: only models already **pulled** (never auto-pulls)

Set ``SAGE_E2E_LIVE=1`` to run; otherwise tests are skipped (CI-safe).

Optional env filters:

    SAGE_E2E_PROVIDERS=groq,ollama
    SAGE_E2E_MODEL_FILTER=openai,gemma
    SAGE_E2E_MODEL_LIMIT=3
    SAGE_E2E_PROMPT_LIMIT=2

    SAGE_E2E_LIVE=1 pytest sage/tests/test_e2e_sage_models_live.py -v --no-cov

Ollama sample size::

    SAGE_E2E_LIVE=1 SAGE_E2E_OLLAMA_MAX=8 pytest ... --no-cov
"""

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

import httpx
import pytest

from sage.config import load_config
from sage.cli_core import _build_router
from sage.models.catalog import OLLAMA_CATALOG
from sage.providers.base import Message
from sage.providers.gemini import _FREE_MODELS as GEMINI_FREE, GeminiProvider
from sage.providers.openai_compat import (
    PROVIDER_SPECS,
    OllamaProvider,
    OpenAICompatProvider,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from sage.core.router import ProviderRouter

# --- Live gate ----------------------------------------------------------------


def _live_enabled() -> bool:
    return os.environ.get("SAGE_E2E_LIVE", "").strip() in ("1", "true", "yes")


pytestmark: list[pytest.MarkDecorator] = [
    pytest.mark.integration,
    pytest.mark.slow,
    pytest.mark.skipif(not _live_enabled(), reason="set SAGE_E2E_LIVE=1 to run network E2E"),
]

# --- Varied prompt matrix (per model) -----------------------------------------


def _csv_env(name: str) -> set[str]:
    value = os.environ.get(name, "").strip()
    if not value:
        return set()
    return {part.strip().lower() for part in value.split(",") if part.strip()}


def _env_int(name: str, default: int = 0) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _provider_enabled(provider: str) -> bool:
    filters = _csv_env("SAGE_E2E_PROVIDERS")
    return not filters or provider.lower() in filters


def _model_selected(model_id: str) -> bool:
    filters = _csv_env("SAGE_E2E_MODEL_FILTER")
    lowered = model_id.lower()
    return not filters or any(part in lowered for part in filters)


def _apply_limit(items: list, env_name: str) -> list:
    limit = _env_int(env_name, 0)
    return items[:limit] if limit > 0 else items


_BASE_ROUTER_PROMPT_MATRIX: list[tuple[str, Callable[[str], bool]]] = [
    (
        "Say exactly: E2E_PING in those two tokens.",
        lambda t: "e2e" in t.lower() and "ping" in t.lower(),
    ),
    (
        "What is 19 + 23? Answer with digits only.",
        lambda t: "42" in t.replace(" ", "").replace("\n", ""),
    ),
    ("One Python line: x = 0", lambda t: "x" in t and "=" in t),
    ("Name the capital of Japan in one word.", lambda t: "tokyo" in t.lower()),
    (
        'Output only: ["a","b"] as JSON.',
        lambda t: "a" in t and "b" in t and ("[" in t or "{" in t),
    ),
]

ROUTER_PROMPT_MATRIX = _apply_limit(_BASE_ROUTER_PROMPT_MATRIX, "SAGE_E2E_PROMPT_LIMIT")


def _is_transient(exc: Exception) -> bool:
    s = f"{type(exc).__name__}: {exc}".lower()
    return any(
        w in s
        for w in (
            "timeout",
            "timed out",
            "connection",
            "connect",
            "reset",
            "temporar",
            "rate",
            "429",
            "502",
            "503",
            "504",
            "remotedisconnected",
        )
    )


def _gen_with_retry(router: ProviderRouter, model_id: str) -> str:
    for attempt in range(2):
        try:
            return router.generate(
                [Message(role="user", content=ROUTER_PROMPT_MATRIX[0][0])],
                model_id,
                0.2,
                300,
            )
        except Exception as e:
            if _is_transient(e) and attempt == 0:
                time.sleep(2.0)
                continue
            if _is_transient(e):
                pytest.skip(str(e))
            raise
    raise RuntimeError("unreachable")


@pytest.fixture(scope="module")
def router() -> ProviderRouter:
    return _build_router(load_config())


# --- Keyed OpenAI-compat: all models per spec when the provider is available ----


def _all_keyed_provider_model_ids() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for spec in PROVIDER_SPECS:
        if not spec.requires_key:
            continue
        if not _provider_enabled(spec.name):
            continue
        for m in spec.models:
            full_id = f"{spec.name}:{m.id}"
            if _model_selected(full_id):
                rows.append((spec.name, m.id))
    return _apply_limit(rows, "SAGE_E2E_MODEL_LIMIT")


def _get_spec(name: str):
    for s in PROVIDER_SPECS:
        if s.name == name:
            return s
    raise KeyError(name)


_keyed = _all_keyed_provider_model_ids()
_keyed_ids = [f"{a}:{b}" for a, b in _keyed]


class TestE2eOpenAICompatKeyed:
    @pytest.mark.parametrize("spec_name, model_id", _keyed, ids=_keyed_ids)
    def test_generate_when_key_present(
        self, router: ProviderRouter, spec_name: str, model_id: str
    ) -> None:
        spec = _get_spec(spec_name)
        p = OpenAICompatProvider(spec, load_config())
        if not p.is_available():
            pytest.skip(f"provider {spec_name} not configured or unavailable")
        out = _gen_with_retry(router, f"{spec_name}:{model_id}")
        assert len(out.strip()) >= 2


# --- Gemini ------------------------------------------------------------------


class TestE2eGemini:
    @pytest.mark.parametrize("m", GEMINI_FREE, ids=[m.id for m in GEMINI_FREE])
    def test_free_models(self, router: ProviderRouter, m) -> None:
        if not _provider_enabled("gemini") or not _model_selected(f"gemini:{m.id}"):
            pytest.skip("filtered out by E2E selection")
        if not GeminiProvider(load_config()).is_available():
            pytest.skip("SAGE_GEMINI_API_KEY / no Gemini access")
        out = _gen_with_retry(router, f"gemini:{m.id}")
        assert len(out.strip()) > 1


# --- Ollama: only pulled, optional cap ----------------------------------------


def _pulled_ollama_bases() -> list[str]:
    try:
        with httpx.Client(timeout=3) as client:
            r = client.get("http://localhost:11434/api/tags")
            if r.status_code != 200:
                return []
            bases: set[str] = set()
            for row in r.json().get("models", []):
                n = row.get("name", "")
                if n:
                    bases.add(n.split(":")[0] if ":" in n else n)
            return sorted(bases)
    except Exception:
        return []


def _ollama_test_bases() -> list[str]:
    b = _pulled_ollama_bases()
    if not b:
        return []
    catalog_bases = {m.name.removeprefix("ollama:") for m in OLLAMA_CATALOG}
    preferred = [x for x in b if x in catalog_bases]
    chosen = preferred if preferred else b
    max_n = int(os.environ.get("SAGE_E2E_OLLAMA_MAX", "0") or 0)
    if max_n and len(chosen) > max_n:
        return chosen[:max_n]
    return chosen


class TestE2eOllamaPulled:
    def test_pulled_model_responds(self, router: ProviderRouter) -> None:
        if not _provider_enabled("ollama"):
            pytest.skip("ollama filtered out by E2E selection")

        bases = [
            base
            for base in _apply_limit(_ollama_test_bases(), "SAGE_E2E_OLLAMA_MAX")
            if _model_selected(f"ollama:{base}")
        ]
        if not bases:
            pytest.skip("no Ollama models to exercise (filtered out, unavailable, or none pulled)")
        if not OllamaProvider(load_config()).is_available():
            pytest.skip("Ollama not running")

        for ollama_base in bases:
            out = _gen_with_retry(router, f"ollama:{ollama_base}")
            assert len(out.strip()) > 0
