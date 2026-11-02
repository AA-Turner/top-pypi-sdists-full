"""
seq.port — move a CPU MuJoCo or SAPIEN benchmark to the GPU. The functions behind the `seq port`
commands of the same names, returning the data those commands print:

  export(target, out)        the CPU benchmark's scenes, through its own reset, as a scene bundle
  check_model(scene)         the GPU engine's compile against the original: fields, options, what it cannot run
  scaffold(scene, out)       a vectorized GPU benchmark's skeleton; the controller, observation and success are yours
  compare(reference, port)   the same controls on MuJoCo and MuJoCo Warp, step by step: where the motion drifts apart
  convert(target)            export → check_model → scaffold

The platform does the parts every MuJoCo benchmark shares; a benchmark's own logic stays the author's to port.

Imported on first use: the SDK itself needs neither numpy nor MuJoCo, and `seq --help` mounts these commands without
loading either (the porting machine installs them: pip install mujoco, and mujoco-warp for check-model).
"""
from __future__ import annotations

import importlib
import sys
import types
from typing import Any, Callable

_WHERE = {"check_model": ("seq.port.check", "check_model"), "check_lines": ("seq.port.check", "lines"),
          "export": ("seq.port.export", "export"),
          "PortError": ("seq.port.errors", "PortError"), "find_model": ("seq.port.mujoco", "find_model"),
          "compare": ("seq.port.motion", "compare"), "compare_lines": ("seq.port.motion", "lines"),
          "scaffold": ("seq.port.scaffold", "scaffold")}

__all__ = sorted([*_WHERE, "convert"])






_NAMED_LIKE_THEIR_MODULE = frozenset(n for n, (m, _) in _WHERE.items() if m == f"seq.port.{n}")


class _Port(types.ModuleType):
    """This package: a submodule named like a function of it is never set on it, so the name stays the function's,
    looked up (lazily, by __getattr__) each time it is read."""

    def __setattr__(self, name: str, value: Any) -> None:

        if name in _NAMED_LIKE_THEIR_MODULE and isinstance(value, types.ModuleType):
            return
        super().__setattr__(name, value)


sys.modules[__name__].__class__ = _Port


def __getattr__(name: str) -> Any:
    if name in _WHERE:
        module, attr = _WHERE[name]
        return getattr(importlib.import_module(module), attr)
    raise AttributeError(f"module 'seq.port' has no attribute {name!r}")


def convert(target: str, *, engine: str | None = None, out: str | None = None, trials: int | None = None,
            worlds: int = 64, progress: Callable[[str], None] | None = None,
            force: bool = False) -> dict[str, Any]:
    """export → check_model → scaffold, stopping where the benchmark's own logic begins. The scene ends up in
    <out>/scene/; check_model's findings are pinned in the skeleton. Returns the three results and the lines to
    print."""
    import json
    import shutil
    import tempfile

    from seq.port.check import check_model, lines
    from seq.port.export import export
    from seq.port.scaffold import scaffold

    say = progress or (lambda msg: None)


    tmp = tempfile.mkdtemp(prefix="seq-scene-")
    try:
        manifest = export(target, tmp, trials=trials, progress=say)
        out = out or f"{manifest['benchmark']['name']}-gpu"


        engine = engine or ("sapien-gpu" if manifest.get("engine") == "sapien" else "mujoco-warp")
        report = check_model(tmp, engine=engine)
        made = scaffold(tmp, out, engine=engine, worlds=worlds, check=report, force=force)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    text = [*lines(report),
            f"skeleton: {out}/benchmark.py — fill in its TODOs (controller, observation, success), then check its "
            f"motion with seq port compare {out}/scene"]
    return {"export": json.loads(json.dumps(manifest)), "check": report, "scaffold": made, "lines": text}
