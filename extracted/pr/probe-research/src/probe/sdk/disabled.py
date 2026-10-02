"""``PROBE_MODE=disabled``: a run that does nothing (plan 2.5).

W&B's ``WANDB_MODE=disabled`` shape. The same training script runs in CI, in a
unit test or on a laptop with no network, and every ``probe.*`` call in it is a
no-op: no :class:`~probe.sdk.client.Client` is built, so nothing is sent, no
outbox directory is created, no heartbeat or capture thread starts and no exit
hook is installed.

The handle answers the calls a training script makes (``log``, ``span``,
``log_artifact``, ``finish``, ``with ... as run``) and any other public method
with ``None``, so code written against a real run keeps running. It is NOT a
fallback: ``probe.init()`` never switches to it on its own (D9) -- a run that
silently records nothing is the failure this plan exists to remove.
"""

from __future__ import annotations

import contextlib
import inspect
import uuid
from typing import Any

from .unit_context import FailureContext


class DisabledSpan(str):
    """What ``DisabledRun.span()`` returns: a span id usable as a context manager."""

    def __new__(cls) -> "DisabledSpan":
        return super().__new__(cls, "disabled")

    def __enter__(self) -> "DisabledSpan":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None


def _noop(*_args: Any, **_kwargs: Any) -> None:
    return None


def _as_config(value: Any) -> dict:
    """``value`` as a plain config dict, the shapes ``config=`` takes online
    (a dict, a ``DictConfig``, an ``argparse.Namespace``, a dataclass, a pydantic
    model -- plan (c)) or a plain iterable of pairs. Never raises: a disabled
    run records nothing, so a config it cannot read is simply not kept."""
    if value is None:
        return {}
    from . import coerce

    try:
        return coerce.to_config(value)
    except Exception:  # noqa: BLE001
        pass
    try:
        return dict(value)
    except Exception:  # noqa: BLE001
        return {}


class DisabledConfig(dict):
    """``run.config`` of a disabled run: the surface of a real run's
    (``cfg["lr"] = ...``, ``cfg.lr = ...``, ``cfg.update(args)`` with an
    argparse ``Namespace``), kept in this process only. Nothing is sent."""

    def update(self, *args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        for arg in args:
            super().update(_as_config(arg))
        super().update(kwargs)

    def __ior__(self, other: Any) -> "DisabledConfig":
        self.update(other)
        return self

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value


def _noop_like(name: str):
    """A no-op standing in for ``Run.<name>``, returning an empty collection when
    the real method's signature promises one."""
    from .run import Run

    method = getattr(Run, name, None)
    if not callable(method):
        return _noop
    try:
        returns = str(inspect.signature(method).return_annotation)
    except (TypeError, ValueError):
        return _noop
    if returns.endswith("None"):
        return _noop
    if returns.startswith("list"):
        return lambda *_a, **_kw: []
    if returns.startswith("dict"):
        return lambda *_a, **_kw: {}
    return _noop


class DisabledRun:
    """A run handle that records nothing. See the module docstring."""

    #: True here and absent on a real :class:`~probe.sdk.run.Run`.
    disabled = True

    def __init__(
        self,
        *,
        name: str | None = None,
        config: dict | None = None,
        tags: list[str] | None = None,
    ) -> None:
        # Every PUBLIC ATTRIBUTE of a real Run, with a value of its type -- the
        # `__getattr__` fallback below answers with a function, which is right
        # for a method and wrong for a property (`run.foreign_keys["k"]` would
        # raise). `tests/test_fluent.py` pins the two surfaces against each other.
        self.id = f"disabled-{uuid.uuid4().hex[:12]}"
        self.slug = self.id
        self.name = name or self.id
        self.description: str | None = None
        self.repo: str | None = None
        self.config = DisabledConfig(_as_config(config))
        self.tags = list(tags or [])
        self.foreign_keys: dict = {}
        self.env_ref: str | None = None
        self.status = "running"
        self.url = None
        self.project_id = None
        self.experiment_id = None
        self.write_epoch = 1
        self.session_id = str(uuid.uuid4())
        self.attached = False

    @property
    def data(self) -> dict:
        return {"id": self.id, "name": self.name, "status": self.status}

    # -- the calls a training loop makes ---------------------------------------
    def log(self, metrics: Any = None, **kw: Any) -> None:
        return None

    def span(self, span_type: str = "", **kw: Any) -> DisabledSpan:
        return DisabledSpan()

    def context(self, **ids: Any) -> FailureContext:
        return FailureContext(None, ids)

    def unit(self, *args: Any, **kw: Any) -> contextlib.AbstractContextManager:
        return contextlib.nullcontext()

    def child(self, *args: Any, **kw: Any) -> "DisabledRun":
        return DisabledRun(name=kw.get("name") or (args[0] if args else None))

    def refresh(self) -> "DisabledRun":
        return self

    def update_config(self, values: Any, **_kw: Any) -> None:
        self.config.update(values)
        return None

    def finish(self, status: str = "completed", **kw: Any) -> None:
        self.status = status
        from . import _open_runs

        _open_runs.closed(self)  # one run fewer open (F5 binding)
        return None

    def __enter__(self) -> "DisabledRun":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.finish("failed" if exc_type is not None else "completed")

    def __getattr__(self, name: str) -> Any:
        # Only reached for names not defined above. Every other PUBLIC method of
        # a real run is a no-op answering what the real one would when nothing
        # is recorded: an empty list or dict where Run's signature promises one
        # (`list_artifacts`, `edges`, `view_data`, ...), else None (`log_hw`,
        # `log_artifact`, `set_tags`, ...). Private names stay an AttributeError
        # so copy/pickle probes and genuine bugs are not swallowed.
        if name.startswith("_"):
            raise AttributeError(name)
        return _noop_like(name)

    def __repr__(self) -> str:
        return f"<DisabledRun {self.id} (PROBE_MODE=disabled: nothing is recorded)>"
