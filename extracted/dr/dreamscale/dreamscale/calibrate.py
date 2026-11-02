"""SO-101 calibration flow for `dreamscale robots so101 calibrate`.

Auto-offered when doctor finds missing/stale calibration.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from dreamscale import errors
from dreamscale.config import load_config
from dreamscale.doctor import calibration_format


def _default_robot_factory() -> Any:
    from dreamscale.hardware.lerobot_so101 import create_so101
    from dreamscale.optional import require_so101_extra

    require_so101_extra()
    config = load_config()
    if config.robot_port is None:
        raise errors.catalog("robot_port_not_found", port="(none configured)")
    return create_so101(port=config.robot_port,
                        calibration_path=config.calibration_path,
                        include_camera=False)  # calibration needs no camera


def run_calibrate(*, robot_factory: Callable[[], Any] = _default_robot_factory,
                  print_fn: Callable[[str], None] = print) -> Path:
    config = load_config()
    target = Path(config.calibration_path).expanduser()
    print_fn("Calibrating your SO-101 — about 2 minutes, guided.")
    print_fn("  1. Clear the table around the arm.")
    print_fn("  2. You'll move the arm to the MIDDLE of its range, then sweep each joint.")
    print_fn("  3. The prompts below come from LeRobot's calibration flow — follow them.")
    robot = robot_factory()
    robot.connect()
    try:
        robot.calibrate()
    finally:
        robot.disconnect()
    if calibration_format(target) != "v3":
        raise errors.catalog(
            "calibration_mismatch",
            detail=f"calibration did not produce a v3.0 file at {target}")
    print_fn(f"✓ Calibration saved to {target}")
    return target
