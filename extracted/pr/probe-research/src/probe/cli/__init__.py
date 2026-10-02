"""The ``probe`` command-line adapter over :mod:`probe.sdk`."""

from ..sdk.client import Client
from . import main as _implementation

app = _implementation.app


def main(argv: list[str] | None = None) -> int:
    # Preserve the original public monkeypatch seam while keeping implementation
    # code in its own submodule. Do not retain a caller's temporary factory for
    # later commands invoked directly through the Typer app.
    previous = _implementation.Client
    _implementation.Client = Client
    try:
        return _implementation.main(argv)
    finally:
        _implementation.Client = previous


__all__ = ["Client", "app", "main"]
