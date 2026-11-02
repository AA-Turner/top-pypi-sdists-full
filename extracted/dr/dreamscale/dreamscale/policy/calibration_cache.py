"""Network calibration kept with a keep-warm session (~/.dreamscale/calibration.json).

A keep-warm reclaim returns the same session, worker and robot computer, so the
profile measured by the previous task still describes this route. One entry: the
latest calibrated session. Any read or write failure means "calibrate again".
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from dataclasses import fields
from pathlib import Path

from dreamscale.config import dreamscale_home
from dreamscale.policy.runtime.calibration import NetworkCalibrationProfile

# A deployment kept warm holds one server for up to 24 h; reconnecting to it reuses an
# explicitly requested calibration for that long (calibration is off by default).
CALIBRATION_REUSE_TTL_S = 24 * 3600


def calibration_cache_path() -> Path:
    return dreamscale_home() / "calibration.json"


def load_session_calibration(
    *,
    session_id: str,
    route: dict[str, str | None],
    now: float | None = None,
) -> NetworkCalibrationProfile | None:
    try:
        data = json.loads(calibration_cache_path().read_text())
        if (
            data.get("session_id") != session_id
            or data.get("route") != route
            or (now if now is not None else time.time()) - float(data["saved_at"])
            > CALIBRATION_REUSE_TTL_S
        ):
            return None
        raw = data["profile"]
        return NetworkCalibrationProfile(
            **{field.name: raw[field.name] for field in fields(NetworkCalibrationProfile)}
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


def save_session_calibration(
    *,
    session_id: str,
    route: dict[str, str | None],
    profile: NetworkCalibrationProfile,
) -> None:
    data = {
        "session_id": session_id,
        "route": route,
        "saved_at": time.time(),
        "profile": profile.payload(),
    }
    path = calibration_cache_path()
    try:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".calibration-", suffix=".json")
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w") as handle:
                json.dump(data, handle)
            os.replace(tmp, path)
        finally:
            Path(tmp).unlink(missing_ok=True)
    except OSError:
        pass
