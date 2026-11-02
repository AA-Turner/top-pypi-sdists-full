"""
Console-script entry for `seq`, kept OUTSIDE the `seq` package on purpose.

WHY a separate top-level module: `seq.cli:main` cannot be the entry point if `seq` is to answer a Python too old for it,
because importing `seq.cli` first imports the `seq` package, whose modules import `sequence_base` at load. On Python
3.9 — a robot's interpreter — `pip install sequence-ai` installs the httpx-only client and not `sequence_base` (that
dependency is marked for 3.10+), so the import would surface as a raw `ModuleNotFoundError` traceback before any of our
code runs. This launcher imports nothing heavy: it says what `seq` needs and what works on this interpreter instead.


The console script is installed by every `pip install sequence-ai`, so `seq` exists on PATH on the robot too — which
is who reaches the version check.

"""
from __future__ import annotations

import sys




_SEQ_DEPS = {"sequence_base", "pydantic", "pydantic_core"}


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < (3, 10):
        sys.stderr.write(
            "error: the `seq` CLI needs Python 3.10+ (this is %d.%d).\n" % tuple(sys.version_info[:2])
            + "The robot client works here: `import sequence_ai`, then `sequence_ai.connect(...)`.\n"
            + "For `seq`, use a Python 3.10+ environment and `pip install sequence-ai` there.\n"
        )
        return 1
    try:
        from seq.cli import main as _cli
    except ModuleNotFoundError as exc:
        missing = (exc.name or "").split(".")[0]
        if missing in _SEQ_DEPS:
            sys.stderr.write(
                f"error: `seq` cannot import {missing}, which `pip install sequence-ai` installs on Python 3.10+. "
                "Reinstall it:\n    pip install --force-reinstall sequence-ai\n"
            )
            return 1
        raise
    return _cli(argv)


if __name__ == "__main__":
    raise SystemExit(main())
