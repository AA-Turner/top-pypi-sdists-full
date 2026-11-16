"""The reply field GPU readings ride on, the one registry of launch modules and the modules to wrap in them, and
`install`, which the site hook calls as each target module loads."""

from __future__ import annotations

import importlib
import logging
from typing import Any

from probe.foundation.compat.compat import StrEnum

log = logging.getLogger(__name__)

#: The `meta_info` key (engine reply) and `session_metadata` key (session server) a call's GPU trace rides on.
GPU_FIELD = "probe_gpu"
#: `<module>=<kind>,...`: the modules the site hook waits for in a launched process (`launch.py` writes it).
SERVING_ENV = "PROBE_MILES_SERVING"
#: `1`: the engine logs one `probe-gpu-timing` line per finished request (`engine.py`).
TIMING_ENV = "PROBE_MILES_GPU_TIMING"


class ServingKind(StrEnum):
    ENGINE = "engine"  # SGLang's TokenizerManager: readings per request (`engine.py`)
    SESSION = "session"  # Miles' session server cores: readings per session (`session.py`)


#: Launch module (`python -m <it>`) -> {module to wrap in that process: its kind}.
SERVING_MODULES: dict[str, dict[str, ServingKind]] = {
    "sglang.launch_server": {"sglang.srt.managers.tokenizer_manager": ServingKind.ENGINE},
    "miles.rollout.session.server": {"miles.rollout.session.core": ServingKind.SESSION,
                                     "miles.rollout.session.v2.core": ServingKind.SESSION},
}
#: Each kind's installer, `(module beside this one, function)`, imported only when a target loads.
INSTALLERS: dict[ServingKind, tuple[str, str]] = {
    ServingKind.ENGINE: (".engine", "install_engine"),
    ServingKind.SESSION: (".session", "install_session"),
}


def install(kind: str, module: Any) -> None:
    """Wrap ``module`` (just loaded) as ``kind`` says. Never raises: SGLang and the session server run as without
    Probe."""
    try:
        path, name = INSTALLERS[ServingKind(kind)]
        getattr(importlib.import_module(path, __package__), name)(module)
    except Exception:  # noqa: BLE001 -- fail open: the serving process runs as if Probe were absent
        log.warning("Probe could not watch %s for GPU readings; it runs without them",
                    getattr(module, "__name__", module), exc_info=True)
