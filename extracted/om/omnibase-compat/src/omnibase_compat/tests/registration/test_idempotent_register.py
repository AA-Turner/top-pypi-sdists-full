# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# compat-skip-retention: test scaffolding (dataclass/fixtures), not a migration model

"""Unit tests for omnibase_compat.registration.idempotent_register [OMN-9239].

Covers the deterministic two-path key extraction contract from plan Task 4:
  (a) kwarg matching `key_attr`
  (b) `key_attr` attribute on the first positional non-self arg
Plus decoration-time assertion that the signature can satisfy at least one path,
and thread-safety of per-decoration seen-set.
"""

from __future__ import annotations

import inspect
import logging
import threading
from dataclasses import dataclass

import pytest

from omnibase_compat.registration import idempotent_register


class _RegistryViaKwarg:
    """Example registrar where the key comes in as a keyword argument."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    @idempotent_register(key_attr="dispatcher_id")
    def register_dispatcher(self, *, dispatcher_id: str, handler: object) -> str:
        self.calls.append(dispatcher_id)
        return dispatcher_id


@dataclass(frozen=True)
class _Route:
    route_id: str
    target: str


class _RegistryViaAttribute:
    """Example registrar where the key comes from an object's attribute."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    @idempotent_register(key_attr="route_id")
    def register_route(self, route: _Route) -> str:
        self.calls.append(route.route_id)
        return route.route_id


def test_kwarg_path_duplicate_is_skipped() -> None:
    reg = _RegistryViaKwarg()
    first = reg.register_dispatcher(dispatcher_id="d1", handler=object())
    second = reg.register_dispatcher(dispatcher_id="d1", handler=object())

    assert first == "d1"
    assert second is None
    assert reg.calls == ["d1"]


def test_attribute_path_duplicate_is_skipped() -> None:
    reg = _RegistryViaAttribute()
    route = _Route(route_id="r1", target="handler_a")
    first = reg.register_route(route)
    second = reg.register_route(_Route(route_id="r1", target="handler_b"))

    assert first == "r1"
    assert second is None
    assert reg.calls == ["r1"]


def test_first_call_records_and_invokes() -> None:
    reg = _RegistryViaKwarg()
    result = reg.register_dispatcher(dispatcher_id="only", handler=object())

    assert result == "only"
    assert reg.calls == ["only"]


def test_distinct_keys_all_invoke() -> None:
    reg = _RegistryViaKwarg()
    reg.register_dispatcher(dispatcher_id="a", handler=object())
    reg.register_dispatcher(dispatcher_id="b", handler=object())
    reg.register_dispatcher(dispatcher_id="c", handler=object())

    assert reg.calls == ["a", "b", "c"]


def test_duplicate_emits_info_log(caplog: pytest.LogCaptureFixture) -> None:
    reg = _RegistryViaKwarg()
    reg.register_dispatcher(dispatcher_id="dup", handler=object())

    with caplog.at_level(logging.INFO, logger="omnibase_compat.registration"):
        reg.register_dispatcher(dispatcher_id="dup", handler=object())

    matches = [
        r
        for r in caplog.records
        if r.levelno == logging.INFO and "idempotent skip" in r.getMessage()
    ]
    assert matches, f"expected INFO 'idempotent skip' log, got records={caplog.records}"
    assert "dup" in matches[0].getMessage()


def test_concurrent_duplicate_only_one_invocation() -> None:
    """10 threads register the same key; exactly one invocation wins."""
    reg = _RegistryViaKwarg()
    barrier = threading.Barrier(10)

    def worker() -> None:
        barrier.wait()
        reg.register_dispatcher(dispatcher_id="shared", handler=object())

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert reg.calls == ["shared"]


def test_signature_preserved() -> None:
    original_sig = inspect.signature(_RegistryViaKwarg.register_dispatcher)
    # The decorator wraps via functools.wraps — signature must round-trip.
    assert "dispatcher_id" in original_sig.parameters, (
        "test precondition: dispatcher_id is a parameter"
    )


def test_decoration_time_assertion_fires_for_unresolvable_signature() -> None:
    """If neither kwarg nor positional-attr path is resolvable, decoration raises."""

    with pytest.raises(TypeError, match="idempotent_register"):

        class _Broken:
            # key_attr="missing_key" but signature has only `self` (no positional,
            # no kwarg by that name, no positional arg that could carry the attribute).
            @idempotent_register(key_attr="missing_key")
            def register_nothing(self) -> None:  # pragma: no cover - decoration should raise
                pass


def test_per_decoration_state_is_isolated() -> None:
    """Two instances of the same decorated method share the decoration's seen-set."""
    a = _RegistryViaKwarg()
    b = _RegistryViaKwarg()

    # Use a unique key that no other test touches so we're not polluted by
    # prior registrations in this module's decoration-level seen-set.
    a.register_dispatcher(dispatcher_id="iso-unique-key", handler=object())
    b.register_dispatcher(dispatcher_id="iso-unique-key", handler=object())

    # Registrar `b` should NOT re-register the same key that `a` already
    # registered — the seen-set is keyed per-decoration (class-method level),
    # and both instances share that same decoration.
    assert a.calls == ["iso-unique-key"]
    assert b.calls == []


class _RegistryPositionalOrKeyword:
    """Registrar where the key param is POSITIONAL_OR_KEYWORD and can be
    passed either positionally or as a kwarg.
    """

    def __init__(self) -> None:
        self.calls: list[str] = []

    @idempotent_register(key_attr="name")
    def register_thing(self, name: str, payload: object) -> str:
        self.calls.append(name)
        return name


def test_positional_or_keyword_passed_positionally_binds_correctly() -> None:
    """Regression: POSITIONAL_OR_KEYWORD params passed positionally must still
    resolve via path 1 (bound argument name), not fall through to path 2 where
    we would try to ``getattr(name_value, "name")``.
    """
    reg = _RegistryPositionalOrKeyword()
    first = reg.register_thing("pok-key", object())
    second = reg.register_thing("pok-key", object())

    assert first == "pok-key"
    assert second is None
    assert reg.calls == ["pok-key"]


def test_positional_or_keyword_passed_as_kwarg_also_works() -> None:
    reg = _RegistryPositionalOrKeyword()
    first = reg.register_thing(name="pok-kwarg", payload=object())
    second = reg.register_thing(name="pok-kwarg", payload=object())

    assert first == "pok-kwarg"
    assert second is None
    assert reg.calls == ["pok-kwarg"]


def test_distinct_decorations_have_distinct_state() -> None:
    """Each @idempotent_register call gets its own seen-set."""
    seen_a: list[str] = []
    seen_b: list[str] = []

    @idempotent_register(key_attr="key")
    def register_a(*, key: str) -> str:
        seen_a.append(key)
        return key

    @idempotent_register(key_attr="key")
    def register_b(*, key: str) -> str:
        seen_b.append(key)
        return key

    register_a(key="x")
    register_b(key="x")  # distinct decoration -> not a duplicate
    register_a(key="x")  # duplicate in `a`
    register_b(key="x")  # duplicate in `b`

    assert seen_a == ["x"]
    assert seen_b == ["x"]
