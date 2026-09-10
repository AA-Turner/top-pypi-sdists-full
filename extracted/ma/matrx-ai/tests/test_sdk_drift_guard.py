"""The SDK-drift guard: a floating SDK signature must never turn a
catalog-resolved wire param into a ``TypeError`` — and never into a silent drop.

Incident 2026-09-09: ``anthropic`` 1.4.0 dropped ``temperature``/``top_p``/
``top_k`` from ``messages.create``/``messages.stream``; every Anthropic call
carrying one died client-side. These tests run against the INSTALLED SDK, not
a pinned version — the deps float as "latest" on purpose, so the proof must too.
"""

from __future__ import annotations

import inspect
from typing import Any

import pytest

from matrx_ai.catalog.models import Adjustment
from matrx_ai.catalog.processors import ProcessorContext, anthropic_temp_topp_exclusion
from matrx_ai.providers.sdk_drift import (
    declared_parameters,
    plan_sdk_kwargs,
    route_undeclared_params,
)

# ── fixtures ─────────────────────────────────────────────────────────────────


def _with_extra_body(*, model, max_tokens, messages, extra_body=None, thinking=None):  # noqa: ARG001
    return "ok"


def _without_extra_body(*, model, prompt):  # noqa: ARG001
    return "ok"


def _accepts_anything(**kwargs):
    return kwargs


def _anthropic_stream():
    from anthropic import AsyncAnthropic

    return AsyncAnthropic(api_key="test-key").messages.stream


def _bind_ok(fn, kwargs: dict[str, Any]) -> bool:
    try:
        inspect.signature(fn).bind(**kwargs)
    except TypeError:
        return False
    return True


# ── the failing-then-passing proof against the real installed SDK ────────────


def test_old_behaviour_fails_against_the_installed_anthropic_sdk():
    """The pre-guard request shape (top-level temperature) is exactly what the
    1.x signature rejects. If this ever starts binding, the SDK re-added the
    kwargs and ai_076's wire_container can be revisited."""
    old_request = {"model": "m", "max_tokens": 5, "messages": [], "temperature": 0.2}
    assert not _bind_ok(_anthropic_stream(), old_request)


def test_guard_makes_the_same_request_bind_and_records_the_route():
    stream = _anthropic_stream()
    old_request = {"model": "m", "max_tokens": 5, "messages": [], "temperature": 0.2, "top_k": 3}
    plan = plan_sdk_kwargs(stream, old_request)
    assert _bind_ok(stream, plan.kwargs)
    assert plan.kwargs["extra_body"] == {"temperature": 0.2, "top_k": 3}
    assert "temperature" not in plan.kwargs and "top_k" not in plan.kwargs
    assert plan.routed == ("temperature", "top_k") and plan.dropped == ()
    assert {a.action for a in plan.adjustments} == {"mapped"}
    assert all(a.expected for a in plan.adjustments)
    assert old_request["temperature"] == 0.2  # caller's dict untouched


def test_catalog_declared_container_needs_no_rescue():
    """ai_076: with wire_container=extra_body the processor already emits the
    SDK 1.x shape, so the guard has nothing to do — it is the backstop, not
    the mechanism."""
    adjustments: list[Adjustment] = []
    ctx = ProcessorContext(
        key="temperature",
        config={"consumes": ["top_p", "top_k"], "order": 200, "wire_container": "extra_body"},
        adjustments=adjustments,
    )
    params = anthropic_temp_topp_exclusion({"temperature": 0.3}, {"max_tokens": 5}, ctx)
    assert params == {"max_tokens": 5, "extra_body": {"temperature": 0.3}}
    request = {"model": "m", "messages": [], **params}
    plan = plan_sdk_kwargs(_anthropic_stream(), request)
    assert not plan.changed
    assert _bind_ok(_anthropic_stream(), plan.kwargs)


def test_processor_without_container_is_rescued_by_the_guard():
    """A stale catalog (no wire_container) is exactly the incident shape: the
    processor emits top-level temperature; the guard routes it and voices it."""
    adjustments: list[Adjustment] = []
    ctx = ProcessorContext(
        key="temperature",
        config={"consumes": ["top_p", "top_k"], "order": 200},
        adjustments=adjustments,
    )
    params = anthropic_temp_topp_exclusion({"temperature": 0.3}, {"max_tokens": 5}, ctx)
    assert params == {"max_tokens": 5, "temperature": 0.3}
    plan = plan_sdk_kwargs(_anthropic_stream(), {"model": "m", "messages": [], **params})
    assert plan.routed == ("temperature",)


def test_processor_never_sends_an_empty_container():
    adjustments: list[Adjustment] = []
    ctx = ProcessorContext(
        key="temperature",
        config={"consumes": ["top_p", "top_k"], "order": 200, "wire_container": "extra_body"},
        adjustments=adjustments,
    )
    params = anthropic_temp_topp_exclusion(
        {"temperature": 0.3, "top_k": 4}, {"thinking": {"type": "enabled"}}, ctx
    )
    assert "extra_body" not in params
    assert {a.key for a in adjustments} == {"temperature", "top_k"}


# ── the shared semantics, SDK-independent ────────────────────────────────────


def test_undeclared_keys_move_to_extra_body_and_merge():
    req = {"model": "m", "max_tokens": 5, "messages": [], "extra_body": {"a": 1}, "top_p": 0.9}
    routed = route_undeclared_params(_with_extra_body, req, provider="test")
    assert routed["extra_body"] == {"a": 1, "top_p": 0.9}
    _with_extra_body(**routed)


def test_declared_keys_are_left_alone():
    req = {"model": "m", "max_tokens": 5, "messages": [], "thinking": {"type": "adaptive"}}
    assert route_undeclared_params(_with_extra_body, req, provider="test") == req


def test_no_escape_hatch_drops_loudly_never_type_errors():
    req = {"model": "m", "prompt": "hi", "temperature": 0.2}
    plan = plan_sdk_kwargs(_without_extra_body, req)
    assert plan.kwargs == {"model": "m", "prompt": "hi"}
    assert plan.dropped == ("temperature",)
    (adj,) = plan.adjustments
    assert adj.action == "dropped" and adj.expected is False
    _without_extra_body(**route_undeclared_params(_without_extra_body, req, provider="test"))


def test_var_keyword_signature_passes_through():
    req = {"anything": 1, "goes": 2}
    assert plan_sdk_kwargs(_accepts_anything, req).changed is False
    assert declared_parameters(_accepts_anything) is None


def test_declared_parameters_cache_is_keyed_by_the_underlying_function():
    """A bound method is a fresh object per attribute access; caching by its id
    would be recycled across unrelated callables."""

    class Client:
        def create(self, *, model, extra_body=None):  # noqa: ARG002
            return model

    a, b = Client(), Client()
    assert a.create is not a.create  # fresh bound method each access
    assert (
        declared_parameters(a.create)
        == declared_parameters(b.create)
        == frozenset({"model", "extra_body"})
    )


@pytest.mark.parametrize("provider", ["openai", "groq", "cerebras", "together"])
def test_openai_family_signatures_still_declare_the_sampling_knobs(provider: str):
    """Today these SDKs declare temperature; the guard is a no-op there. If one
    of them drifts, this test documents the moment and the guard carries on."""
    mod = {
        "openai": ("openai.resources.chat.completions", "AsyncCompletions"),
        "groq": ("groq.resources.chat.completions", "AsyncCompletions"),
        "cerebras": ("cerebras.cloud.sdk.resources.chat.completions", "AsyncCompletionsResource"),
        "together": ("together.resources.chat.completions", None),
    }[provider]
    module = __import__(mod[0], fromlist=["*"])
    cls = (
        getattr(module, mod[1])
        if mod[1]
        else next(
            c for n, c in vars(module).items() if n.startswith("Async") and hasattr(c, "create")
        )
    )
    declared = declared_parameters(cls.create)
    assert declared is None or {"temperature", "extra_body"} <= declared
