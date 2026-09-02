"""
Opt-in mode for project configuration consumption.

Controls whether ``.agdt/config/project.json`` values are actively applied
to a developer's workflow (``"auto"`` mode) or ignored (``"manual"`` mode).

The ``config_mode`` value is stored as a top-level key in the per-worktree
``state.json``, not in ``project.json`` itself.
"""

from __future__ import annotations

import sys

_VALID_MODES = ("auto", "manual")
_DEFAULT_MODE = "auto"


def get_config_mode() -> str:
    """Return the current ``config_mode`` from per-worktree state.

    Defaults to ``"auto"`` when the key is absent or empty, preserving
    backward compatibility with existing setups.
    """
    from agentic_devtools.state import get_value

    raw = get_value("config_mode")
    if raw is None:
        return _DEFAULT_MODE
    if isinstance(raw, str):
        stripped = raw.strip()
        return stripped if stripped else _DEFAULT_MODE
    # Non-string value (e.g. int from `agdt-set config_mode 0`): convert so
    # validate_config_mode() can surface the error rather than silently
    # treating it as "auto".
    return str(raw).strip()


def validate_config_mode(mode: str) -> str | None:
    """Validate a ``config_mode`` value.

    Returns ``None`` when *mode* is valid.  Returns an error message string
    when *mode* is not one of the accepted values (``"auto"`` or ``"manual"``).
    """
    if mode in _VALID_MODES:
        return None
    return f"Invalid config_mode '{mode}'. Must be one of: {', '.join(repr(m) for m in _VALID_MODES)}"


def config_mode_cmd() -> None:
    """CLI entry point for ``agdt-config-mode``.

    With no arguments: prints the current config_mode.
    With one argument: sets the config_mode after validation.
    """
    import argparse

    from agentic_devtools.state import set_value

    parser = argparse.ArgumentParser(
        prog="agdt-config-mode",
        description="Get or set the project configuration consumption mode.",
    )
    parser.add_argument(
        "mode",
        nargs="?",
        default=None,
        help="New mode to set ('auto' or 'manual'). Omit to display current mode.",
    )
    args = parser.parse_args()

    if args.mode is None:
        # Display current mode
        current = get_config_mode()
        print(f"config_mode: {current}")
    else:
        # Strip whitespace so `agdt-config-mode " manual "` is accepted
        # consistently with get_config_mode()'s own normalization.
        mode = args.mode.strip()
        error = validate_config_mode(mode)
        if error:
            print(error, file=sys.stderr)
            raise SystemExit(1)
        set_value("config_mode", mode)
        print(f"config_mode set to: {mode}")
