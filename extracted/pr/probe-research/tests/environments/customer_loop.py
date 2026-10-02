"""The customer loop every environment test runs, as a customer writes it.

Runs under the RELEASED SDK only -- inside containers, kernels and plain
interpreters that have nothing but ``probe-research`` installed -- so it imports
nothing from the test suite. Its values mirror ``envlib.point_value`` (guarded
by ``test_env_loop_values_match``).

Reports what it did as ``PROBE-ENV {json}`` lines on stdout for the harness.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time

CONFIG = {"lr": 0.1, "model": {"layers": 4, "act": "gelu"}}


def row(step: int) -> dict:
    """One training step's metrics, nested the way customers nest them."""
    return {
        "loss": 1.0 / (step + 1),
        "opt": {"lr": step * 0.001, "betas": {"b1": 0.9 + (step % 7) * 0.001}},
    }


def say(event: str, **fields) -> None:
    print("PROBE-ENV " + json.dumps({"event": event, **fields}, default=str), flush=True)


def _where_the_outbox_is() -> dict:
    """The released SDK's own verdict on its queue's storage (best effort:
    internal API, so a rename must not break the loop)."""
    try:
        from probe.sdk import ephemeral, journal

        directory = str(journal.default_dir())
        return {"dir": directory, **ephemeral.describe(directory)}
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=os.environ.get("PROBE_ENV_PROJECT"))
    ap.add_argument("--name", default="env-loop")
    ap.add_argument("--external-id", default=None)
    ap.add_argument("--steps", default="0:50", help="START:END (END exclusive)")
    ap.add_argument("--ckpt", default=None, help="checkpoint file: resume after its step")
    ap.add_argument("--ckpt-every", type=int, default=50)
    ap.add_argument("--stop-after", type=int, default=None, help="stop logging after this step")
    ap.add_argument("--config", action="store_true")
    ap.add_argument("--small-artifact", action="store_true")
    ap.add_argument("--big-mib", type=int, default=0, help="also log a sparse file this big")
    ap.add_argument("--then", choices=("finish", "wait", "return"), default="finish")
    ap.add_argument("--wait-max", type=float, default=900.0)
    ap.add_argument("--step-sleep", type=float, default=0.0)
    ap.add_argument("--workdir", default=os.getcwd())
    args = ap.parse_args(argv)

    import probe

    try:
        from importlib import metadata

        version = metadata.version("probe-research")
    except Exception:  # noqa: BLE001
        version = getattr(probe, "__version__", "?")
    say(
        "start",
        version=version,
        python=platform.python_version(),
        platform=sys.platform,
        pid=os.getpid(),
        home=os.environ.get("HOME"),
        outbox=_where_the_outbox_is(),
    )

    start, end = (int(x) for x in args.steps.split(":"))
    if args.ckpt and os.path.exists(args.ckpt):
        with open(args.ckpt, encoding="utf-8") as fh:
            start = int(json.load(fh)["step"]) + 1
        say("resumed_from_checkpoint", next_step=start)

    kw = {"project": args.project, "name": args.name}
    if args.external_id:
        kw["external_id"] = args.external_id
    t0 = time.monotonic()
    run = probe.init(**kw)
    say("run", id=run.id, init_seconds=round(time.monotonic() - t0, 2))

    last = None
    for step in range(start, end):
        probe.log(row(step), step=step)
        last = step
        if args.ckpt and (step + 1) % args.ckpt_every == 0:
            tmp = args.ckpt + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump({"step": step}, fh)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, args.ckpt)
            say("ckpt", step=step)
        if args.step_sleep:
            time.sleep(args.step_sleep)
        if args.stop_after is not None and step >= args.stop_after:
            break
    say("logged", first=start, last=last)

    if args.config:
        probe.update_config(CONFIG)
        say("config")
    if args.small_artifact:
        path = os.path.join(args.workdir, "small.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("environment suite artifact\n")
        probe.log_artifact("small.txt", path=path)
        say("artifact", name="small.txt")
    if args.big_mib:
        path = os.path.join(args.workdir, "big.bin")
        with open(path, "wb") as fh:
            # A random head, so no two runs log the same bytes (a real server
            # takes one active upload per content hash in a team).
            fh.write(os.urandom(16))
            fh.truncate(args.big_mib * 1024 * 1024 + 7)
        probe.log_artifact("big.bin", path=path)
        say("artifact", name="big.bin", size=args.big_mib * 1024 * 1024 + 7)

    if args.then == "wait":
        say("ready")
        deadline = time.monotonic() + args.wait_max
        while time.monotonic() < deadline:  # "still training" until someone kills us
            time.sleep(0.5)
        return 3
    if args.then == "return":
        say("returning_without_finish")
        return 0
    t1 = time.monotonic()
    probe.finish()
    say("finished", seconds=round(time.monotonic() - t1, 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
