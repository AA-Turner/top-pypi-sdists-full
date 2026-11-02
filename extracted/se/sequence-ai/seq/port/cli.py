"""
`seq port`'s five commands: export, check-model, scaffold, compare and convert - a CPU MuJoCo or
SAPIEN benchmark moved to the GPU. Their own command since 10-18, no longer under `seq benchmark`, whose commands are
every registered benchmark's. Registered here so `seq/cli_parser.py` only mounts them; each
prints what its seq.port function returns (--json: that data as JSON) and exits 1 when what it checked does not hold.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

COMMANDS = ("export", "check-model", "scaffold", "compare", "convert")




WORLDS_HELP = ("the most worlds one call of the GPU benchmark's step plays, its @seq.concurrent(sizes=[N]) (default "
               "64): an eval builds as many as it runs, at most that")


def add_parsers(psub: Any) -> None:
    p = psub.add_parser("export", help="a CPU MuJoCo or SAPIEN benchmark's scenes as a scene bundle, through its own "
                                       "reset (runs here: where its simulator is installed)")
    p.add_argument("target", help="the CPU benchmark: file.py:Class or module:Class")
    p.add_argument("-o", "--out", default="scene", help="the bundle's directory (default scene/)")
    p.add_argument("--trials", type=int, default=None, metavar="N",
                   help="only each task's first N seeds, as seq eval run --trials N runs them (default: every "
                        "seed)")
    p.add_argument("--tasks", default=None, help="only these tasks, comma-separated")
    p.add_argument("--rollout-steps", type=int, default=200,
                   help="physics steps each episode also runs on this MuJoCo, under compare's seeded controls, "
                        "for compare to hold the port to (default 200; 0: none)")

    p = psub.add_parser("check-model", help="compile a scene bundle with the GPU engine's MuJoCo and compare it with "
                                            "the original: masses, options, what the engine cannot run (a SAPIEN "
                                            "bundle: what SAPIEN's GPU pipeline cannot run, and its structures)")
    p.add_argument("scene", help="the scene bundle (seq port export)")
    p.add_argument("--engine", default=None, help="the GPU engine: mujoco-warp or sapien-gpu (default: the one the "
                                                  "bundle's simulator ports to)")

    p = psub.add_parser("scaffold", help="write a vectorized GPU benchmark's skeleton from a scene bundle")
    p.add_argument("scene", help="the scene bundle")
    p.add_argument("--engine", default=None, help="the GPU engine: mujoco-warp or sapien-gpu (default: the one the "
                                                  "bundle's simulator ports to)")
    p.add_argument("-o", "--out", default=None, help="the skeleton's directory (default <benchmark>-gpu/)")
    p.add_argument("--worlds", type=int, default=64, metavar="N", help=WORLDS_HELP)
    p.add_argument("--model", default=None, help="which of the scene's models, when it holds more than one")
    p.add_argument("--no-pins", action="store_true", help="take the GPU engine's defaults instead of pinning the "
                                                          "options check-model finds changed")
    p.add_argument("--force", action="store_true", help="write over a benchmark.py or README.md already there "
                                                        "(what you changed in them is lost)")

    p = psub.add_parser("compare", help="compare the motion, here: the CPU benchmark's exported scene on MuJoCo and "
                                        "the port's on MuJoCo Warp, the same controls, step by step; names the first "
                                        "step and the joint and body that drift apart")
    p.add_argument("scene", help="the CPU benchmark's exported scene (seq port export)")
    p.add_argument("port_scene", nargs="?", default=None, metavar="port-scene",
                   help="the port's scene (default: the same one)")
    p.add_argument("--steps", type=int, default=200, help="physics steps per episode (default 200)")
    p.add_argument("--atol", type=float, default=1e-3,
                   help="how far apart a joint may get, in radians or metres (default 0.001)")
    p.add_argument("--episodes", type=int, default=3, metavar="N", help="the scene's first N episodes (default 3)")
    p.add_argument("--seed", type=int, default=0, help="the controls' seed (default 0)")

    p = psub.add_parser("convert", help="export, check-model and scaffold in one go; then fill in the TODOs and run "
                                        "compare")
    p.add_argument("target", help="the CPU benchmark: file.py:Class or module:Class")
    p.add_argument("--engine", default=None, help="the GPU engine: mujoco-warp or sapien-gpu (default: the one the "
                                                  "benchmark's simulator ports to)")
    p.add_argument("-o", "--out", default=None, help="the skeleton's directory (default <benchmark>-gpu/)")
    p.add_argument("--trials", type=int, default=None, metavar="N",
                   help="only each task's first N seeds, as seq eval run --trials N runs them (default: every "
                        "seed)")
    p.add_argument("--worlds", type=int, default=64, metavar="N", help=WORLDS_HELP)
    p.add_argument("--force", action="store_true", help="write over a benchmark.py or README.md already there "
                                                        "(what you changed in them is lost)")







_YOURS = {"numpy": "pip install mujoco (the version your benchmark uses; it brings numpy)",
          "mujoco": "pip install mujoco (the version your benchmark uses)",
          "sapien": "pip install sapien (the version your benchmark uses)"}
PORT_EXTRA = ('pip install "sequence-ai[port]" (MuJoCo Warp, its MuJoCo and SAPIEN at the versions these commands are '
              'tested with; in an environment of its own when your benchmark needs another MuJoCo)')
_INSTALL = frozenset({"numpy", "mujoco", "mujoco_warp", "warp", "sapien"})


def _install(cmd: str, name: str) -> str:
    """How to install what `seq port <cmd>` did not find."""
    if cmd == "export":
        return _YOURS.get(name, PORT_EXTRA)
    if cmd == "convert":
        if name in _YOURS:
            return _YOURS[name]
        return (f"{PORT_EXTRA} - convert also runs export here; when your benchmark needs another MuJoCo, run seq "
                "port export where it runs, and check-model and scaffold where this is installed")
    return PORT_EXTRA


def run(args: argparse.Namespace) -> int:
    """One porting command; an engine it needs and does not find is said in one line (exit 2), with its install."""
    from seq.errors import SeqAuthoringError

    try:
        return _run(args)
    except ModuleNotFoundError as exc:
        if exc.name not in _INSTALL:
            raise
        raise SeqAuthoringError(f"seq port {args.port_cmd} needs {exc.name} here: "
                                f"{_install(args.port_cmd, exc.name)}") from None


def _run(args: argparse.Namespace) -> int:
    from seq import port

    cmd = args.port_cmd
    say = (lambda msg: print(msg, file=sys.stderr)) if args.json else print
    tasks = [t for t in (getattr(args, "tasks", None) or "").split(",") if t] or None
    if cmd == "export":
        out = port.export(args.target, args.out, trials=args.trials, tasks=tasks, progress=say,
                          rollout_steps=args.rollout_steps)
        what = (f"{len(out['structures'])} structure(s), {len(out['episodes'])} episode(s), SAPIEN "
                f"{out['sapien_version']}" if out["engine"] == "sapien" else
                f"{len(out['models'])} model(s), {len(out['episodes'])} episode(s), MuJoCo {out['mujoco_version']}")
        _done(args, out, [f"scene: {args.out} ({what}) — next: seq port check-model {args.out}"])
        return 0
    if cmd == "check-model":
        report = port.check_model(args.scene, engine=args.engine or _engine_for(args.scene))
        _done(args, report, port.check_lines(report))
        return 0 if report["ok"] else 1
    if cmd == "scaffold":
        engine = args.engine or _engine_for(args.scene)
        check = None if args.no_pins else port.check_model(args.scene, engine=engine)
        out = port.scaffold(args.scene, args.out or _default_out(args.scene), engine=engine, worlds=args.worlds,
                            model=args.model, check=check, force=args.force)
        lines = [f"skeleton: {out['out']}/benchmark.py (model {out['model']}, up to {out['worlds']} world(s) a step "
                 f"call, per world: {', '.join(out['per_world']) or 'nothing'}) — fill in the TODOs, then seq "
                 f"port compare {args.scene}"]
        if out.get("volume"):
            lines.append(f"the scene is past what a deploy ships beside the code: before registering, seq volume put "
                         f"--kind dataset {out['volume']} {out['out']}/scene")
        if out.get("shared"):
            lines.append(f"one value for every world: {', '.join(out['shared'])} (MuJoCo Warp holds no per-world copy)")
        _done(args, out, lines)
        return 0
    if cmd == "compare":
        report = port.compare(args.scene, args.port_scene, steps=args.steps, atol=args.atol,
                             episodes=args.episodes, seed=args.seed)
        _done(args, report, port.compare_lines(report))
        return 0 if report["ok"] else 1
    if cmd == "convert":
        out = port.convert(args.target, engine=args.engine, out=args.out, trials=args.trials, worlds=args.worlds,
                           progress=say, force=args.force)
        _done(args, out, out["lines"])
        return 0 if out["check"]["ok"] else 1
    raise AssertionError(cmd)


def _manifest(scene: str) -> dict:
    """A scene bundle's manifest; a folder that is not one is said so in one line, not as a FileNotFoundError's
    traceback."""
    from seq.port.errors import PortError

    try:
        with open(f"{scene}/manifest.json") as f:
            return json.load(f)
    except (OSError, ValueError):
        raise PortError(f"{scene} is not a scene bundle (no readable manifest.json): make one with seq port "
                        "export") from None


def _engine_for(scene: str) -> str:
    """The GPU engine a bundle's simulator ports to: SAPIEN's GPU pipeline for a SAPIEN scene, MuJoCo Warp otherwise."""
    return "sapien-gpu" if _manifest(scene).get("engine") == "sapien" else "mujoco-warp"


def _default_out(scene: str) -> str:
    return f"{_manifest(scene)['benchmark']['name']}-gpu"


def _done(args: argparse.Namespace, data: Any, text: list[str]) -> None:
    if args.json:
        print(json.dumps(data, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
    else:
        for line in text:
            print(line)
