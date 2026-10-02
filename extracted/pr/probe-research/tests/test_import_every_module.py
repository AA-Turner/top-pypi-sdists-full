"""Every module of the package imports (#2043 review, for the Python 3.10 leg).

`test_py310_compat.py` greps for three 3.11-only forms; nothing ran ruff on
`agent/` in CI, so any other 3.11-only name or syntax reached 3.10 users as an
ImportError in whichever module used it. This imports every module, in a
fresh interpreter so no test's imports hide a broken one, and allows a failure
only when the missing module is an optional dependency this environment was
not installed with.
"""

from __future__ import annotations

import json
import subprocess
import sys

#: Top-level modules only an extra (or a trainer integration) brings. A module
#: that fails for want of one of these is not broken on this interpreter.
OPTIONAL = frozenset(
    {
        "pydantic_ai",
        "logfire",
        "lightning",
        "lightning_fabric",
        "pytorch_lightning",
        "torch",
        "transformers",
        "uvicorn",
        "wandb",
    }
)

_WALK = r"""
import importlib, json, pkgutil, warnings
warnings.simplefilter("ignore")
import probe
failures = []
count = 0
for info in pkgutil.walk_packages(probe.__path__, "probe."):
    if info.name.endswith("__main__"):
        continue
    try:
        importlib.import_module(info.name)
        count += 1
    except BaseException as exc:
        failures.append([info.name, type(exc).__name__, getattr(exc, "name", None), str(exc)[:300]])
print(json.dumps({"imported": count, "failures": failures}))
"""


def test_every_module_imports_on_this_interpreter():
    done = subprocess.run([sys.executable, "-c", _WALK], capture_output=True, text=True, timeout=300)
    assert done.returncode == 0, done.stderr[-2000:]
    result = json.loads(done.stdout.strip().splitlines()[-1])
    # An integration re-raises the missing extra as a plain ImportError with a
    # friendlier message (probe.integrations.lightning / .huggingface), keeping `name`.
    broken = [
        failure
        for failure in result["failures"]
        if not (
            failure[1] in ("ModuleNotFoundError", "ImportError")
            and (failure[2] or "").split(".")[0] in OPTIONAL
        )
    ]
    assert broken == [], f"{sys.version.split()[0]}: modules that do not import: {broken}"
    assert result["imported"] > 150  # the walk really walked the package
