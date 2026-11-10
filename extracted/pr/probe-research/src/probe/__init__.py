"""probe - CLI + SDK client for Probe (tracking for the team's ML work).

Quick start:
    import probe
    probe.init(
        project="folding",  # a slug or id; a new slug creates the project
        experiment="dockq-sweep",
        question="temp 0.7 wins",
    )
    probe.log({"loss": 0.42, "dockq": 0.71}, step=42)   # from anywhere, any thread
    probe.finish()

`project=probe.FROM_ENV` takes the project from PROBE_PROJECT, this chat's project or
`probe project use`; a run naming none of them reads none.

`probe.log()` reaches the run without a handle being threaded through call
frames, which is what makes instrumenting code you do not own practical. The
binding is a contextvar over a process default, so a second run started in a
thread shadows rather than hijacks — see `probe.sdk.fluent`.

The explicit API has no ambient state and is the implementation underneath:
    client = probe.Client()   # resolves token from env / the stored login
    run = client.run(
        project="folding",
        experiment="dockq-sweep",
        question="temp 0.7 wins",
    )   # no token -> browser approval (TTY)
    run.log({"loss": 0.42}, step=42)
    run.finish()
"""

from __future__ import annotations

import importlib
import sys as _sys
from typing import TYPE_CHECKING

from . import errors

# SDK names load lazily (PEP 562): `import probe` -- or, crucially, `import
# probe.sdk.<leaf>` for a stdlib-only module like probe.foundation.durable.durable -- must not
# eagerly pull in Client and therefore httpx. A distributed Miles actor only spills
# metric batches to disk; it should not import the network stack to do that. Naming
# one of these attributes resolves it through .sdk (itself lazy) on first access.
_LAZY = {
    "Authorship",
    "ChartView",
    "DeliveryIncomplete",
    "CaptureLedger",
    "CaptureState",
    "Client",
    "DatasetRef",
    "Edit",
    "CommandKind",
    "FROM_ENV",
    "KeyMetricsView",
    "PaneView",
    "ParallelView",
    "Pin",
    "Reader",
    "Reference",
    "Run",
    "Settings",
    "SourceRef",
    "SpanHandle",
    "active_run",
    "context",
    "expect",
    "expr",
    "finish",
    "init",
    "log",
    "log_artifact",
    "log_hw",
    "resolve",
    "Rewind",
    "source",
    "span",
    "stable_external_key",
    "stable_span_id",
    "update_config",
}


def __getattr__(name: str) -> object:
    # `expr` is a MODULE, not a name re-exported from .sdk: `import probe` alone
    # would not bind it, so `probe.expr.series(...)` needs this leg. Lazy for the
    # same reason as everything else here — it pulls the generated models.
    if name == "expr":
        value = importlib.import_module(".expr", __name__)
        globals()[name] = value
        return value
    # `probe.events.subscribe(...)`: live events, an add-on module (sdk/events), loaded when first named.
    if name == "events":
        value = importlib.import_module(".sdk.events", __name__)
        globals()[name] = value
        return value
    # `probe.commands.sync()`: where every rank of a multi-process script takes the run's commands (sdk/run/commands).
    if name == "commands":
        value = importlib.import_module(".sdk.run.commands", __name__)
        globals()[name] = value
        return value
    if name in _LAZY:
        value = getattr(importlib.import_module(".sdk", __name__), name)
        globals()[name] = value  # cache: the lazy import runs once per name
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | _LAZY | {"expr", "events", "commands"})


if TYPE_CHECKING:  # eager names for type checkers / IDEs; never executed at runtime
    from . import expr
    from .sdk import events
    from .sdk import (
        Authorship,
        ChartView,
        DeliveryIncomplete,
        CaptureLedger,
        CaptureState,
        Client,
        DatasetRef,
        Edit,
        CommandKind,
        FROM_ENV,
        KeyMetricsView,
        PaneView,
        ParallelView,
        Pin,
        Reader,
        Reference,
        Run,
        Settings,
        SourceRef,
        SpanHandle,
        active_run,
        context,
        finish,
        init,
        log,
        log_artifact,
        log_hw,
        resolve,
        source,
        span,
        stable_external_key,
        stable_span_id,
        update_config,
    )

__all__ = [
    "Authorship",
    "ChartView",
    "DeliveryIncomplete",
    "CaptureLedger",
    "CaptureState",
    "Client",
    "DatasetRef",
    "Edit",
    "CommandKind",
    "FROM_ENV",
    "KeyMetricsView",
    "PaneView",
    "ParallelView",
    "Pin",
    "Reader",
    "Reference",
    "Run",
    "Settings",
    "SourceRef",
    "SpanHandle",
    "active_run",
    "context",
    "expect",
    "expr",
    "finish",
    "init",
    "log",
    "log_artifact",
    "log_hw",
    "resolve",
    "source",
    "span",
    "stable_external_key",
    "stable_span_id",
    "update_config",
    "errors",
    "events",
    "commands",
    "__version__",
]

# The distribution name and its installed version (foundation/version/version.py).
from .foundation.version.version import DISTRIBUTION as _DISTRIBUTION  # noqa: E402, F401 -- probe._DISTRIBUTION
from .foundation.version.version import VERSION as __version__  # noqa: E402

# A script's output is teed from here, so the run it opens later keeps what it printed first
# (sdk/capture/logs/early.py, never raises). Only a `.py` `__main__` can need it: the `probe` command
# and `python -c` never load it.
if str(getattr(_sys.modules.get("__main__"), "__file__", "")).endswith(".py"):
    from .sdk.capture.logs import early as _early_capture

    _early_capture.start_at_import()
