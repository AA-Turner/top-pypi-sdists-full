"""Per-launch ephemera: what was true of THIS process start on THIS machine.

Everything here lands in the run's ``metadata["launch"]`` block, never in the
content-addressed execution record -- argv, hostnames, and env values differ per
launch, and hashing them would mint a unique execution record per run and
destroy dedup (design doc D1, docs/2026-08-04-reproducibility-capture-enforcement-design.md).

Every capture is best-effort: failures collect into an ``errors`` list and
capture functions never raise. Absence is recorded, not guessed.

``scrub_argv`` adds positional flag/value handling to the shared SDK
scrubber. The original argv is used only to launch the process; captured
arguments have credential values removed before they enter spans or metadata.
"""
from __future__ import annotations

import getpass
import os
import re
import socket
import subprocess
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

from .redaction import _MODEL_TOKEN_KEYS, is_sensitive_key, scrub_string

LAUNCH_SCHEMA = "probe.launch/1"

#: Secret-shaped flag NAMES, matched as exact dash/underscore segments -- not
#: substrings, so `--tokenizer` and `--max-tokens` are reproduction data, not
#: secrets.
_SECRET_WORDS = frozenset({"key", "token", "secret", "password", "passwd", "credential"})


def _is_secret_flag(arg: str) -> bool:
    """Flag whose NAME contains a secret word as an exact -/_ segment.

    Segments, not substrings: --tokenizer and --max-tokens are reproduction
    data, not secrets. A linear scan, immune to the pathological-backtracking
    hazard a joined regex has on long snake_case tokens -- the prior
    implementation (`(?:\\w+[-_])*?(key|token|...)`) is ambiguous because
    `\\w` includes `_`, so a long `--a_a_a_..._a` argv token could hang
    auto-snapshot capture, which must never block a run.
    """
    if not arg.startswith("-"):
        return False
    name = arg.lstrip("-").split("=", 1)[0]
    if name.lower().replace("-", "_") in _MODEL_TOKEN_KEYS:
        return False
    if is_sensitive_key(name):
        return True
    return any(seg.lower() in _SECRET_WORDS for seg in re.split(r"[-_]", name))


# Secret-shaped bare values (not flag names -- see _is_secret_flag above).
# Redaction is marked, so a reader knows the command line is not verbatim.
# Fixed-prefix alternations with a single greedy class each are linear, no
# ambiguity: this one is safe as a regex.
_SECRET_VALUE = re.compile(
    r"^(sk-[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}"
    r"|AKIA[A-Z0-9]{12,}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]+)"
)


def scrub_argv(argv: list[str]) -> tuple[list[str], bool]:
    """Redact secret-shaped tokens; return (argv, whether anything was redacted)."""
    out: list[str] = []
    scrubbed = False
    redact_next = False
    for arg in argv:
        if redact_next:
            out.append("[redacted]")
            scrubbed = True
            redact_next = False
            continue
        if _is_secret_flag(arg):
            if "=" in arg:
                out.append(arg.split("=", 1)[0] + "=[redacted]")
                scrubbed = True
            else:
                out.append(arg)
                redact_next = True
            continue
        if _SECRET_VALUE.match(arg):
            out.append("[redacted]")
            scrubbed = True
            continue
        clean = scrub_string(arg)
        out.append(clean)
        scrubbed = scrubbed or clean != arg
    return out, scrubbed


#: Process names that identify HOW a run was launched, when seen in the
#: parent chain. Shells are recorded in the chain but are not "launchers".
_LAUNCHERS = ("sbatch", "srun", "slurmstepd", "kubelet", "containerd-shim", "dockerd")


def ppid_from_stat(text: str) -> int:
    """The parent pid out of one `/proc/<pid>/stat` line.

    `comm` is the second field, parenthesised, and MAY CONTAIN SPACES -- a real
    kernel does not escape them, so `tmux: server` and `Web Content` both land as
    `(tmux: server)`. Splitting the whole line on whitespace therefore shifts
    every field after it, and the naive `split()[3]` reads the STATE CHARACTER
    instead of the ppid: `int('S')` raises, one hop into a chain walk that is
    supposed to be best-effort.

    Everything after the LAST `)` is fixed-width and space-free, so parse from
    there: `state` then `ppid`. Raises ValueError/IndexError on anything that is
    not a stat line, which the caller treats as "this hop is unreadable".
    """
    after_comm = text.rsplit(")", 1)[1]
    return int(after_comm.split()[1])


def _parent_chain(max_hops: int = 10) -> tuple[list[str], str | None]:
    """Walk parent processes to a recognized launcher. Best-effort, bounded."""
    chain: list[str] = []
    launcher: str | None = None
    pid = os.getppid()
    for _ in range(max_hops):
        if pid <= 1:
            break
        name = None
        try:  # Linux
            with open(f"/proc/{pid}/comm") as fh:
                name = fh.read().strip()
            with open(f"/proc/{pid}/stat") as fh:
                pid = ppid_from_stat(fh.read())
        # A malformed stat line is NOT an OSError, and letting one escape here
        # cost the whole `process` slot rather than one hop. Fall through to the
        # `ps` tier, which answers on Linux too.
        except (OSError, ValueError, IndexError):
            try:  # macOS / no procfs
                out = subprocess.run(
                    ["ps", "-ww", "-o", "ppid=,comm=", "-p", str(pid)],
                    capture_output=True, text=True, timeout=2,
                )
                parts = out.stdout.split(None, 1)
                if len(parts) != 2:
                    break
                name = os.path.basename(parts[1].strip())
                pid = int(parts[0])
            except (OSError, ValueError, subprocess.TimeoutExpired):
                break
        if not name:
            break
        chain.append(name)
        if launcher is None and any(name.startswith(prefix) for prefix in _LAUNCHERS):
            launcher = name
    return chain, launcher


#: The command and folder a run is being opened FOR, when that is not this
#: process's own (`probe exec` opens the run, then launches the child): what
#: `process_identity` reads before the launch block exists.
_LAUNCHING: ContextVar[tuple[list[str], str | None] | None] = ContextVar("probe_launching", default=None)


@contextmanager
def launching(argv: list[str] | None, cwd: str | None = None) -> Iterator[None]:
    """Name the command (and folder) a run is opened for, while it is opened."""
    token = _LAUNCHING.set((list(argv), cwd) if argv else None)
    try:
        yield
    finally:
        _LAUNCHING.reset(token)


def process_identity(
    argv: list[str] | None = None, cwd: str | None = None
) -> tuple[dict[str, Any], list[str]]:
    """WHAT was launched WHERE: `argv` (scrubbed), `cwd` and `entrypoint`, by the
    exact rules the launch block stores them (`capture_process` uses this), so
    the retry detector can compare a run about to open with a stored one. With
    no `argv`, the command named by `launching()`, else this process's."""
    errors: list[str] = []
    if argv is None:
        named = _LAUNCHING.get()
        if named is not None:
            argv, cwd = named[0], cwd if cwd is not None else named[1]
    raw = list(argv) if argv is not None else list(sys.argv)
    scrubbed_argv, scrubbed = scrub_argv(raw)
    info: dict[str, Any] = {"argv": scrubbed_argv, "argv_scrubbed": scrubbed}
    # The same rule as the parent chain below: one unreadable thing costs one
    # field, never the slot. `os.getcwd()` raises FileNotFoundError when the
    # launch directory has been unlinked underneath the process -- a scratch
    # mount cleaned mid-job, a container dir replaced -- and an explicit relative
    # `cwd` does NOT dodge it, because `abspath` calls `getcwd()` itself to
    # resolve one. Unguarded, that lands as `missing: [launch_process]` exactly
    # like the /proc parse did.
    try:
        info["cwd"] = os.path.abspath(cwd or os.getcwd())
    except OSError as exc:
        errors.append(f"cwd: {exc}")
        if cwd:
            info["cwd"] = cwd  # unresolved, but it is what the caller named
    entry = raw[0] if raw else None
    if entry:
        info["entrypoint"] = os.path.abspath(entry) if os.path.exists(entry) else entry
    return info, errors


def capture_process(
    argv: list[str] | None = None, cwd: str | None = None
) -> tuple[dict[str, Any], list[str]]:
    """Identity of this launch: command, place, machine, user, lineage."""
    identity, errors = process_identity(list(argv) if argv is not None else list(sys.argv), cwd)
    info: dict[str, Any] = {
        "argv": identity["argv"],
        "argv_scrubbed": identity["argv_scrubbed"],
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    for key in ("cwd", "entrypoint"):
        if key in identity:
            info[key] = identity[key]
    try:
        info["hostname"] = socket.gethostname()
    except OSError as exc:
        errors.append(f"hostname: {exc}")
    try:
        info["user"] = getpass.getuser()
    except Exception as exc:  # getuser can raise KeyError on daemon UIDs
        errors.append(f"user: {exc}")
    # Guarded like hostname and user above, and for the reason this module's
    # docstring gives: a capture function must not raise. `_parent_chain` reads
    # process-table text from the kernel, the least predictable input here, and
    # when it threw the caller's per-slot `except` dropped the ENTIRE `process`
    # block -- so `run check` reported `missing: [launch_process]` for a run whose
    # argv, cwd and hostname had all been captured perfectly. One unreadable
    # parent must cost the parent chain, nothing more.
    try:
        chain, launcher = _parent_chain()
    except Exception as exc:  # noqa: BLE001 -- see above
        chain, launcher = [], None
        errors.append(f"parent_chain: {exc}")
    if chain:
        info["parent_chain"] = chain
    if launcher:
        info["launcher"] = launcher
    return info, errors


#: Values captured only for these names — everything else is name-only.
#: Extensible per-site via PROBE_ENV_ALLOWLIST="+VAR1,VAR2". NCCL_* is
#: value-captured wholesale: knob names are the reproduction surface there.
ENV_ALLOWLIST = frozenset({
    "CUDA_VISIBLE_DEVICES", "WORLD_SIZE", "RANK", "LOCAL_RANK",
    "MASTER_ADDR", "MASTER_PORT", "OMP_NUM_THREADS", "PYTHONHASHSEED",
    "SLURM_JOB_ID", "SLURM_ARRAY_TASK_ID",
})


def _allowlist() -> frozenset[str]:
    extra = os.environ.get("PROBE_ENV_ALLOWLIST", "")
    names = {v.strip() for v in extra.lstrip("+").split(",") if v.strip()}
    return ENV_ALLOWLIST | names


def _detect_container(_dockerenv_path: str = "/.dockerenv") -> dict[str, Any] | None:
    """Container context, provenance-tagged. Image identity is PROVENANCE, not
    correctness (design doc D1 / the 2026-07-29 begin-state-bytes decision)."""
    via = None
    if os.environ.get("KUBERNETES_SERVICE_HOST"):
        via = "kubernetes"
    elif os.path.exists(_dockerenv_path):
        via = "dockerenv"
    else:
        try:
            with open("/proc/1/cgroup") as fh:
                text = fh.read()
            if any(marker in text for marker in ("docker", "containerd", "kubepods")):
                via = "cgroup"
        except OSError:
            pass
    if via is None:
        return None
    info: dict[str, Any] = {"detected_via": via}
    image = os.environ.get("PROBE_CONTAINER_IMAGE") or os.environ.get("IMAGE")
    if image:
        info["image"] = image
    if via == "kubernetes" and os.environ.get("HOSTNAME"):
        info["pod"] = os.environ["HOSTNAME"]
    return info


def capture_runtime(
    _dockerenv_path: str = "/.dockerenv",
) -> tuple[dict[str, Any], list[str]]:
    """Env-var names (all), values (allowlist + NCCL_* only), container context."""
    errors: list[str] = []
    allow = _allowlist()
    names = sorted(os.environ)
    info: dict[str, Any] = {
        "env_names": names,
        "env_values": {
            k: os.environ[k] for k in names if k in allow or k.startswith("NCCL_")
        },
    }
    container = _detect_container(_dockerenv_path)
    if container:
        info["container"] = container
    return info, errors


_ARGV_SEED = re.compile(r"^--?([\w-]*seed[\w-]*?)(?:=(.*))?$", re.IGNORECASE)


def capture_determinism(
    argv: list[str] | None = None, config: dict[str, Any] | None = None
) -> tuple[dict[str, Any], list[str]]:
    """Seed evidence with provenance. `detected` = observed from the outside
    (env, argv, an already-imported framework); `declared` = the caller put it
    in config. Absence of seeds is recorded as an empty list — honest, not an
    error."""
    errors: list[str] = []
    seeds: list[dict[str, Any]] = []
    # Declared (config) entries are appended before detected (env/argv/framework)
    # ones, so a name shared by both -- e.g. a `seed` in config that also shows
    # up on the command line -- resolves to the detected value when a caller
    # dedupes by name: what actually governed the run outranks what was merely
    # configured for it.
    for key, value in sorted((config or {}).items()):
        if key == "seeds" and isinstance(value, dict):
            for sub, sval in sorted(value.items()):
                seeds.append({
                    "name": f"seeds.{sub}", "value": sval,
                    "provenance": "declared", "source": "config",
                })
        elif re.search(r"(^|_)seed(s)?$", key, re.IGNORECASE):
            seeds.append({
                "name": key, "value": value,
                "provenance": "declared", "source": "config",
            })
    hashseed = os.environ.get("PYTHONHASHSEED")
    if hashseed is not None:
        seeds.append({
            "name": "PYTHONHASHSEED", "value": hashseed,
            "provenance": "detected", "source": "env",
        })
    # Scrubbed first: a flag matching BOTH the seed pattern and a secret
    # segment (`--seed-key`) must not land its raw value here -- `[redacted]`
    # is the honest record, same as the launch block's `process.argv`.
    args, _ = scrub_argv(list(argv) if argv is not None else list(sys.argv))
    for i, arg in enumerate(args):
        m = _ARGV_SEED.match(arg)
        if not m:
            continue
        value = m.group(2)
        if value is None and i + 1 < len(args) and not args[i + 1].startswith("-"):
            value = args[i + 1]
        seeds.append({
            "name": m.group(1), "value": value,
            "provenance": "detected", "source": "argv",
        })
    # Frameworks are read from sys.modules, NEVER imported: importing torch
    # costs seconds and pulls CUDA context into a process that may not want it.
    torch = sys.modules.get("torch")
    if torch is not None:
        try:
            seeds.append({
                "name": "torch.initial_seed", "value": int(torch.initial_seed()),
                "provenance": "detected", "source": "torch",
            })
        except Exception as exc:
            errors.append(f"torch seed: {exc}")
    if "numpy" in sys.modules:
        seeds.append({
            "name": "numpy.random", "value": None,
            "provenance": "detected", "source": "numpy",
            "note": "generator present; state not captured",
        })
    return {"seeds": seeds}, errors


def build_launch_block(
    *,
    argv: list[str] | None = None,
    cwd: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compose the launch block. NEVER raises — a capture bug must not take
    down the run it is documenting (design principle: block claims, not runs)."""
    from probe import __version__

    errors: list[str] = []
    block: dict[str, Any] = {"schema": LAUNCH_SCHEMA, "probe_version": __version__}
    try:
        block["process"], errs = capture_process(argv=argv, cwd=cwd)
        errors += errs
    except Exception as exc:
        errors.append(f"process: {exc}")
    try:
        block["runtime"], errs = capture_runtime()
        errors += errs
    except Exception as exc:
        errors.append(f"runtime: {exc}")
    try:
        block["determinism"], errs = capture_determinism(argv=argv, config=config)
        errors += errs
    except Exception as exc:
        errors.append(f"determinism: {exc}")
    if errors:
        block["errors"] = errors
    return block
