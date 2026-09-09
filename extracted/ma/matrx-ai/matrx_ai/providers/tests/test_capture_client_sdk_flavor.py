"""The capture HTTP client must be built on the httpx flavor its SDK uses.

Provider SDKs vendor their own HTTP layer. ``anthropic`` 1.4.0 moved to
``httpx2`` and its constructor REJECTS an ``httpx.AsyncClient``::

    TypeError: Invalid `http_client` argument; `httpx.AsyncClient` is from
    the `httpx` package, but this SDK uses `httpx2`. Use
    `httpx2.AsyncClient` instead.

Before the fix, ``make_capture_http_client()`` always built a plain
``httpx.AsyncClient``, so EVERY Anthropic call died at client construction
(``keys.py::_get_or_create``) with that TypeError.

Two independent layers, each able to fail alone:

1. ``test_every_sdk_accepts_the_capture_client`` — constructs the REAL SDK
   client through matrx-ai's own factory for every provider the census
   found. No network: SDK constructors do not dial.
2. ``test_every_sdk_call_site_declares_its_sdk`` — a static census of the
   source: any ``http_client=make_capture_http_client(...)`` that does not
   pass ``sdk=`` is the defect returning under a new provider.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import httpx
import pytest

from matrx_ai.providers.outbound_capture import (
    _outbound_request_hook,
    make_capture_http_client,
    resolve_sdk_httpx,
)

PROVIDERS_ROOT = Path(__file__).resolve().parents[1]

# (sdk module name, client class attribute) — every provider whose SDK we
# hand a capture client to.
SDK_CLIENTS: list[tuple[str, str]] = [
    ("anthropic", "AsyncAnthropic"),
    ("openai", "AsyncOpenAI"),
    ("groq", "AsyncGroq"),
    ("cerebras.cloud.sdk", "AsyncCerebras"),
    ("together", "AsyncTogether"),
]


@pytest.mark.parametrize("sdk_name,client_attr", SDK_CLIENTS)
def test_every_sdk_accepts_the_capture_client(sdk_name: str, client_attr: str) -> None:
    """The real SDK constructor accepts the client our factory builds."""
    sdk = importlib.import_module(sdk_name)
    client_cls = getattr(sdk, client_attr)

    http_client = make_capture_http_client(sdk=sdk)

    kwargs = {"api_key": "test-key-not-used", "http_client": http_client}
    if sdk_name == "cerebras.cloud.sdk":
        # Constructing with the SDK default issues a blocking warm-up GET.
        kwargs["warm_tcp_connection"] = False

    # The assertion IS that this does not raise TypeError.
    client = client_cls(**kwargs)
    assert client is not None


@pytest.mark.parametrize("sdk_name,_client_attr", SDK_CLIENTS)
def test_capture_hook_survives_the_flavor_swap(sdk_name: str, _client_attr: str) -> None:
    """Whatever flavor is chosen, the capture behaviour is identical."""
    sdk = importlib.import_module(sdk_name)
    client = make_capture_http_client(sdk=sdk, timeout=123.0)

    assert _outbound_request_hook in client.event_hooks["request"]
    assert client.event_hooks["response"] == []
    assert client.timeout.connect == 123.0
    # It is an AsyncClient of the flavor the SDK itself is built on.
    assert isinstance(client, resolve_sdk_httpx(sdk).AsyncClient)


def test_anthropic_resolves_to_a_non_httpx_flavor() -> None:
    """The falsifiable half: anthropic must NOT resolve to plain httpx.

    If this ever fails because anthropic went back to ``httpx``, the test
    is telling the truth — update the assertion, do not delete the guard.
    """
    import anthropic

    flavor = resolve_sdk_httpx(anthropic)
    assert flavor is not httpx
    assert flavor.__name__ == "httpx2"


def test_no_sdk_still_means_plain_httpx() -> None:
    """Raw call sites (the xAI TTS POST) keep the historical default."""
    assert resolve_sdk_httpx(None) is httpx
    client = make_capture_http_client()
    assert isinstance(client, httpx.AsyncClient)


def test_every_sdk_call_site_declares_its_sdk() -> None:
    """Static census — no provider may hand an SDK an undeclared client."""
    offenders: list[str] = []

    for path in PROVIDERS_ROOT.rglob("*.py"):
        if "tests" in path.parts:
            continue
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            for kw in node.keywords:
                if kw.arg != "http_client":
                    continue
                value = kw.value
                if not isinstance(value, ast.Call):
                    continue
                func = value.func
                name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
                if name != "make_capture_http_client":
                    continue
                if not any(k.arg == "sdk" for k in value.keywords):
                    offenders.append(
                        f"{path.relative_to(PROVIDERS_ROOT)}:{value.lineno}"
                    )

    assert not offenders, (
        "These call sites hand a provider SDK a capture client without "
        "declaring which SDK it is for, so the client is built on plain "
        "httpx and the SDK will reject it if it vendors another flavor "
        f"(anthropic 1.x does): {offenders}. Pass sdk=<the SDK module>."
    )
