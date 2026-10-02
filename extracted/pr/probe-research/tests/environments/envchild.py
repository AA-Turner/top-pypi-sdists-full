"""Child-side helpers for the environment suite.

Imported by the customer scripts the tests launch (``PYTHONPATH`` names this
directory, nothing else), and by the tests for the expected values. Stdlib
only at import: ``probe`` is imported where it is used, so the SDK a child
runs is always the one installed in its venv.
"""

from __future__ import annotations

import json
import os
import sys
import time
import warnings

PROJECT = os.environ.get("PROBE_ENV_PROJECT") or "env-matrix"
ART = os.environ.get("PROBE_ENV_ART") or "."
BIG_BYTES = 70 * 1024 * 1024  # over the 64 MiB single-PUT ceiling: multipart


def result(tag: str, **kw) -> None:
    """One machine-readable line the test parses (``envkit.Child.result``).
    Also appended to PROBE_ENV_RESULTS_FILE when set: a process whose stdout
    does not reach the test's (a Ray worker) still reports."""
    line = "PROBE_ENV_RESULT " + json.dumps({"tag": tag, **kw}, default=str)
    print(line, flush=True)
    path = os.environ.get("PROBE_ENV_RESULTS_FILE")
    if path:
        with open(path, "a") as f:
            f.write(line + "\n")


def sdk_info() -> dict:
    import probe

    return {"sdk_version": probe.__version__, "sdk_file": probe.__file__}


def value(key: str, step: int, salt: int = 0) -> float:
    """A deterministic, exactly representable-in-JSON value per (key, step)."""
    h = sum(ord(c) for c in key) + 31 * salt
    return step + ((step * 37 + h) % 1009) / 1009.0


def payload(step: int, prefix: str = "train", salt: int = 0) -> dict:
    """One step's metrics as a customer logs them: a nested dict plus a flat key."""
    return {
        prefix: {
            "loss": value(f"{prefix}/loss", step, salt),
            "acc": value(f"{prefix}/acc", step, salt),
        },
        f"{prefix}_lr": value(f"{prefix}_lr", step, salt),
    }


def expected(steps, prefix: str = "train", salt: int = 0) -> dict:
    """{(step, flattened key): value} for ``payload`` over ``steps``."""
    out = {}
    for step in steps:
        for key in (f"{prefix}/loss", f"{prefix}/acc", f"{prefix}_lr"):
            out[(step, key)] = value(key, step, salt)
    return out


def write_artifacts(tag: str, big: bool) -> dict[str, str]:
    """A small file, and (``big``) a sparse 70 MiB one, under PROBE_ENV_ART --
    outside the run's working folder, so output capture does not re-upload them."""
    base = os.path.join(ART, tag)
    os.makedirs(base, exist_ok=True)
    files = {}
    small = os.path.join(base, "small.json")
    with open(small, "w") as f:
        json.dump({"tag": tag, "at": time.time()}, f)
    files[f"{tag}-small.json"] = small
    if big:
        path = os.path.join(base, "big.bin")
        with open(path, "wb") as f:
            # A random head: byte-identical files from every run would share
            # one content hash, and a real server takes one active upload per
            # hash in a team -- the rest wait on it (409).
            f.write(os.urandom(16) + b"probe-env-matrix\n")
            f.truncate(BIG_BYTES)
        files[f"{tag}-big.bin"] = path
    return files


def customer_loop(
    run,
    *,
    steps,
    prefix: str = "train",
    salt: int = 0,
    tag: str = "job",
    artifacts: bool = True,
    big: bool = False,
    sleep: float = 0.0,
    on_step=None,
) -> dict:
    """The loop every environment runs: log (nested dicts, explicit steps) ->
    update_config -> log_artifact (small, and one > 64 MiB). The caller owns
    init and finish. Returns what it did, for the RESULT line."""
    import probe

    logged = 0
    for step in steps:
        probe.log(payload(step, prefix, salt), step=step)
        logged += 1
        if on_step is not None:
            on_step(step)
        if sleep:
            time.sleep(sleep)
    probe.update_config({"phase": "after-loop", "env_matrix": {"tag": tag, "steps": logged}})
    names = []
    if artifacts:
        for name, path in write_artifacts(tag, big).items():
            probe.log_artifact(name, path=path)
            names.append(name)
    return {"logged_steps": logged, "artifacts": names, "run_id": str(run.id)}


class Warned:
    """Record every warning raised inside the block (SDK warnings included)."""

    def __enter__(self):
        self._cm = warnings.catch_warnings(record=True)
        self.caught = self._cm.__enter__()
        warnings.simplefilter("always")
        return self

    def __exit__(self, *exc):
        return self._cm.__exit__(*exc)

    def texts(self) -> list[str]:
        return [f"{w.category.__name__}: {str(w.message)[:300]}" for w in self.caught]


def rank_env() -> dict:
    return {k: os.environ.get(k) for k in ("RANK", "LOCAL_RANK", "WORLD_SIZE") if os.environ.get(k)}


def flush_stdio() -> None:
    sys.stdout.flush()
    sys.stderr.flush()
