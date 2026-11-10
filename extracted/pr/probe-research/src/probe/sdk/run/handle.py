"""RunHandle: the Protocol Run, OfflineRun and DisabledRun all satisfy, and `_UNSET`, the "not passed"
default their signatures share."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


#: "The caller did not pass this at all", as distinct from an explicit ``None``.
#: Load-bearing for spans: the ATIF expander and the Harbor trial importer replay
#: STORED trajectories and pass ``started_at=<maybe None>`` deliberately, because a
#: stored step may have no usable timestamp. Defaulting those to ``now()`` would
#: write a fabricated time into a historical record. Omitting the argument — which
#: only live code does — is what opts into a default.
_UNSET: Any = object()


@runtime_checkable
class RunHandle(Protocol):
    """What every run the SDK hands out answers: Run, OfflineRun (recorded with no network, sent by
    `probe sync`) and DisabledRun (PROBE_MODE=disabled, records nothing), so `probe.init()` callers
    and the fluent forwarders never branch on which one they got."""

    def log(self, metrics: Any = None, **kw: Any) -> Any: ...

    def span(self, span_type: str = ..., **kw: Any) -> Any: ...

    def update_config(self, values: Any, **kw: Any) -> Any: ...

    def log_dataset(self, path_or_uri: Any = None, name: Any = None, **kw: Any) -> Any: ...

    def context(self, **ids: Any) -> Any: ...

    def unit(self, *args: Any, **kw: Any) -> Any: ...

    def child(self, *args: Any, **kw: Any) -> Any: ...

    def refresh(self) -> Any: ...

    def on(self, kind: Any, handler: Any) -> Any: ...

    def finish(self, status: str | None = None, **kw: Any) -> Any: ...

    def __enter__(self) -> Any: ...

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> Any: ...
