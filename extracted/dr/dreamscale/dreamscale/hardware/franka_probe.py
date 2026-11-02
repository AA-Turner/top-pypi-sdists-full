"""Read-only Franka probe, run in its own process by doctor: never moves anything.

    python -m dreamscale.hardware.franka_probe HOST [--gripper]

Prints one JSON object: the FCI protocol versions, arm mode, errors and joints, and
with --gripper the Hand's width. A native crash or hang stays in this process.
"""

from __future__ import annotations

import json
import sys


def probe(host: str, *, gripper: bool, franky=None) -> dict:
    from .franka_arm import _errors_text, installed_libfranka, parse_versions

    fk = franky
    if fk is None:
        import franky as fk
    result = {"libfranka": installed_libfranka()}
    try:
        robot = fk.Robot(host, realtime_config=fk.RealtimeConfig.Ignore)
    except fk.IncompatibleVersionException as exc:
        versions = parse_versions(exc)
        return {**result, "status": "incompatible", "detail": str(exc),
                **({"server": versions[0], "library": versions[1]} if versions else {})}
    except fk.NetworkException as exc:
        return {**result, "status": "unreachable", "detail": str(exc)}
    state = robot.state
    result.update(
        status="connected",
        mode=getattr(state.robot_mode, "name", str(state.robot_mode)),
        errors=_errors_text(state.current_errors),
        q=[float(v) for v in state.q],
        success_rate=float(state.control_command_success_rate),
    )
    if gripper:
        try:
            hand = fk.Gripper(host)
            result["gripper"] = {
                "width": float(hand.width), "max_width": float(hand.max_width),
                "server": int(hand.server_version),
            }
        except fk.Exception as exc:
            result["gripper"] = {"error": str(exc)}
    return result


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    gripper = "--gripper" in args
    hosts = [a for a in args if not a.startswith("--")]
    if len(hosts) != 1:
        print("usage: python -m dreamscale.hardware.franka_probe HOST [--gripper]",
              file=sys.stderr)
        return 2
    try:
        result = probe(hosts[0], gripper=gripper)
    except ImportError as exc:
        result = {"status": "missing", "detail": str(exc)}
    print(json.dumps(result), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
