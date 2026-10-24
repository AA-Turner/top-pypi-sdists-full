"""Test Holders for code calls held by ``matrx_ai.mandates.hold_code_call``.

A converted code site RESOLVES its mandate on every call, so a unit test of that
site needs a resolver — and the honest one is the real ``hold_code_call`` walking
a real resolution to a real (inline) agent, not a monkeypatched ``hold_code_call``
that could return anything. ``install_inline_holders`` installs exactly that:
each key resolves to an ``InlineAgentSource`` built from the config dict you
give it (``model`` + ``messages`` — the same shape an agent row carries).
An optional ``variables`` entry declares the Holder's variables, in the stored
row shape (``[{"name", "defaultValue"}]``), for a Holder whose authored turns
template the site's offered values.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import mandates as _mandates
from matrx_ai.agents.named import InlineAgentSource
from matrx_ai.agents.variables import AgentVariable


def install_inline_holders(
    monkeypatch: pytest.MonkeyPatch, holders: dict[str, dict[str, Any]]
) -> list[str]:
    """Resolve each mandate key in ``holders`` to an inline agent; any other key
    raises like a real resolver would. Returns the list of keys resolved, in order."""
    resolved: list[str] = []

    async def _resolver(mandate_key: str) -> _mandates.MandateResolution:
        if mandate_key not in holders:
            raise LookupError(f"no test Holder for {mandate_key!r}")
        resolved.append(mandate_key)
        config = dict(holders[mandate_key])
        declared = config.pop("variables", None)
        return _mandates.MandateResolution(
            source=InlineAgentSource(
                config_dict=config,
                variable_defaults=AgentVariable.from_list(declared) if declared else None,
                name=f"holder:{mandate_key}",
            )
        )

    monkeypatch.setattr(_mandates, "_MANDATE_RESOLVER", _resolver)
    if _mandates._MANDATE_RUNNER is None:
        # A converted site prepares through the runner port (runner plan 25 step 6). A package test has no host
        # runner, so the test Holders are served by a minimal one whose ``prepare`` is the same real
        # ``hold_code_call`` the host's adapter runs.
        monkeypatch.setattr(_mandates, "_MANDATE_RUNNER", HolderBackedRunner())
    return resolved


def offered_values(variables: Any) -> dict[str, Any]:
    """The plain values of an offer: each value in hand (``given``) unwrapped; a builder stays a builder.

    The host runner hands ``hold_code_call`` the offer as built (``Offered`` values — the real
    ``hold_code_call`` applies the compute rule); a test double of ``hold_code_call`` that reads the
    values it was sent reads them through this."""
    return {
        n: (v.build(None) if isinstance(v, _mandates.Offered) and v.in_hand else v)
        for n, v in dict(variables or {}).items()
    }


class _Prepared:
    def __init__(self, held: Any) -> None:
        self.held = held

    def held_call(self) -> Any:
        return self.held


class _SendsThroughModule:
    """A test's stand-in held call (a double of ``hold_code_call`` returned it) gains ``send*`` methods that go
    through the module's ``run_held_*`` — whatever the test doubled there."""

    def __init__(self, held: Any) -> None:
        self._held = held

    def __getattr__(self, name: str) -> Any:
        return getattr(self._held, name)

    async def send(self, **kwargs: Any) -> Any:
        return await _mandates.run_held_call(self._held, **kwargs)

    async def send_pydantic(self, **kwargs: Any) -> Any:
        return await _mandates.run_held_pydantic(self._held, **kwargs)

    async def send_text(self, **kwargs: Any) -> Any:
        return await _mandates.run_held_text(self._held, **kwargs)


class HolderBackedRunner:
    """A test runner: ``prepare`` = the real ``hold_code_call`` over the installed resolver; ``finish`` =
    ``HeldCall.finish``. ``run`` refuses — a NamedAgent test installs :func:`install_named_runner`."""

    system = _mandates.Principal(user_id=None, org_id="00000000-0000-4000-8000-000000000001")

    async def run(self, key: str, offer: Any, *, who: Any, opts: Any) -> Any:
        raise _mandates.MandateRunnerUnavailable("HolderBackedRunner serves held calls only")

    async def prepare(self, key: str, offer: Any, *, who: Any, opts: Any) -> Any:
        from matrx_ai.graph_nodes.agent_action import StepOffer

        if isinstance(offer, StepOffer):
            # A workflow AI step (runner plan 25 step 9a): the step's resolution, over the installed resolver.
            return _Prepared(
                await _mandates.resolve_mandate_by_key(key, consumer=opts.consumer or f"mandate_runner:{opts.door}")
            )
        # Values in hand arrive as plain values (the by-name lane); a builder still reaches the real
        # ``hold_code_call``, which applies the compute rule. Looked up on the module at call time, so a
        # test that doubles ``hold_code_call`` / ``run_held_*`` still sees its double.
        variables = offered_values(offer) if offer else None
        held = await _mandates.hold_code_call(
            key,
            consumer=opts.consumer or f"mandate_runner:{opts.door}",
            variables=variables,
            metadata=dict(opts.metadata) if opts.metadata else None,
        )
        return _Prepared(held if isinstance(held, _mandates.HeldCall) else _SendsThroughModule(held))

    async def finish(self, prepared: Any, result: Any) -> Any:
        if isinstance(result, BaseException):
            await prepared.held.finish("", success=False, error=f"{type(result).__name__}: {result}")
        else:
            output, parsed = _mandates.engine_output(result)
            await prepared.held.finish(output, parsed=parsed)

    async def resolve(self, key: str, *, who: Any, holder: Any = None) -> Any:
        raise _mandates.MandateRunnerUnavailable("HolderBackedRunner does not describe mandates")


class _NamedRun:
    def __init__(self, raw: Any) -> None:
        self.raw = raw
        self.success = bool(getattr(raw, "success", True))
        self.output = str(getattr(raw, "output", "") or "")
        self.parsed = getattr(raw, "parsed", None)


def install_named_runner(monkeypatch: pytest.MonkeyPatch, fake: Any) -> list[Any]:
    """Serve ``run(key, Offer.from_inputs(Cls, ...))`` with ``fake(Cls, **kwargs)`` — the shape of the old
    ``run_mandated`` doubles — and record each call's ``(who, opts)``. ``prepare`` / ``finish`` / ``resolve``
    still reach the runner installed before (a held call in the same test keeps working)."""
    calls: list[Any] = []
    inner = _mandates._MANDATE_RUNNER

    class _FakeRunner:
        system = getattr(inner, "system", HolderBackedRunner.system)

        async def run(self, key: str, offer: Any, *, who: Any, opts: Any) -> Any:
            named = offer.named
            calls.append((who, opts))
            kwargs = dict(named.kwargs)
            if named.offered is not None:
                kwargs["offered"] = named.offered
            if named.offered_media is not None:
                kwargs["offered_media"] = named.offered_media
            if named.runner is not None:
                kwargs["_runner"] = named.runner
            return _NamedRun(await fake(named.agent_cls, **kwargs))

        async def prepare(self, *a: Any, **k: Any) -> Any:
            return await (inner or HolderBackedRunner()).prepare(*a, **k)

        async def finish(self, *a: Any, **k: Any) -> Any:
            return await (inner or HolderBackedRunner()).finish(*a, **k)

        async def resolve(self, *a: Any, **k: Any) -> Any:
            return await inner.resolve(*a, **k)

    monkeypatch.setattr(_mandates, "_MANDATE_RUNNER", _FakeRunner())
    return calls


__all__ = ["HolderBackedRunner", "install_inline_holders", "install_named_runner", "offered_values"]
