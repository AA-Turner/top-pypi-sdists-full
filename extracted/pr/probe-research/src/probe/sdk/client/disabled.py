"""``PROBE_MODE=disabled`` for the explicit client: an SDK `Client()` is a `DisabledClient`, which builds nothing
(no transport, socket, outbox or Probe service) and opens runs that record nothing (`DisabledRun`), as
`probe.init()` does in that mode (`sdk/run/disabled.py`)."""

from __future__ import annotations

from typing import Any

from ..run.disabled import DisabledRun


def _do_nothing(*_args: Any, **_kwargs: Any) -> None:
    return None


def is_disabled_mode() -> bool:
    """``PROBE_MODE=disabled``. A value that is not a mode keeps the client online, as before this check."""
    from .. import errors
    from ..settings.settings import Mode, resolve_mode

    try:
        return resolve_mode(None) is Mode.DISABLED
    except errors.ValidationError:
        return False


class DisabledClient:
    """What `Client()` is under ``PROBE_MODE=disabled``: `run()` opens a `DisabledRun`; every other public method
    answers None and sends nothing, so a script written against a real client keeps running."""

    #: True here and absent on a real `Client`.
    is_disabled = True

    def run(self, *, name: str | None = None, config: Any = None, tags: list[str] | None = None,
            **_kwargs: Any) -> DisabledRun:
        """A run that records nothing (its other keywords are ignored)."""
        from ..capture.logs import early as _early
        from ..run.launch import open_runs as _open_runs

        run = DisabledRun(name=name, config=config, tags=tags)
        _early.end_held_window()  # records nothing: the tee `import probe` started stops too
        _open_runs.opened(run)
        return run

    def close(self, *_args: Any, **_kwargs: Any) -> None:
        return None

    def __enter__(self) -> DisabledClient:
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        return _do_nothing

    def __repr__(self) -> str:
        return "<DisabledClient (PROBE_MODE=disabled: nothing is sent)>"
