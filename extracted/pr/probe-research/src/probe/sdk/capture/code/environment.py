"""the run's environment: its virtualenv and resolved packages, OS, CPU/RAM, CUDA stack and GPUs."""

from __future__ import annotations
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
from typing import Any




# THE enumeration -- there is deliberately only one, and it always runs inside
# the TARGET interpreter, even when that is this process.
#
# An in-process variant used to exist alongside this for the SDK path. It was
# deleted rather than kept-and-tested: two implementations of one algorithm
# whose outputs are HASHED into `env_ref` will drift, and the drift surfaces as
# two identical environments comparing unequal -- indistinguishable from a real
# dependency change. Its only unique capability was seeing runtime `sys.path`
# mutations, and those are derivable: the `sys.path.insert` line lives in the
# code the snapshot already captures. The spawn costs ~50ms ONCE per run (a
# snapshot is a launch-time act, not a training-loop one), so there is no hot
# path to protect here -- that constraint belongs to `probe log`.
#
# Written for the oldest interpreter a project venv might hold: `dist.name` is
# 3.10+, `dist.metadata['Name']` is not. First occurrence wins, matching
# `sys.path` shadowing order. No pip required -- `uv venv` installs none.
_ENUMERATE_PROGRAM = r"""
import json, sys
from importlib import metadata

seen = {}
for dist in metadata.distributions():
    try:
        name = dist.metadata["Name"]
    except Exception:
        name = None
    if not name:
        continue
    if name not in seen:
        seen[name] = dist.version or "0"
json.dump(
    {
        "python": ".".join(str(p) for p in sys.version_info[:3]),
        "executable": sys.executable,
        "packages": sorted("%s==%s" % (n, v) for n, v in seen.items()),
    },
    sys.stdout,
)
"""

_ENUMERATE_TIMEOUT = 60.0

# Layout of a venv, POSIX and Windows.
_VENV_BIN = ("bin", "Scripts")
_VENV_PYTHON = ("python", "python3", "python.exe")
# Ordered: a project that has both `.venv` and `venv` almost always maintains
# the first (uv, poetry and pdm all create `.venv`) and keeps the other stale.
_VENV_DIR_NAMES = (".venv", "venv", "env")


def venv_python(venv: str) -> str | None:
    """The interpreter inside ``venv``, or None if it does not look like a venv."""
    for bindir in _VENV_BIN:
        for name in _VENV_PYTHON:
            candidate = os.path.join(venv, bindir, name)
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
    return None


def find_venv(cwd: str | None = None) -> tuple[str | None, str | None]:
    """Locate the virtualenv whose packages belong to the code at ``cwd``.

    Returns ``(venv_root, resolved_via)``, or ``(None, None)``.

    Order, strongest tie to the snapshotted code first:

    1. a venv directory inside the project -- ``.venv`` / ``venv`` / ``env``,
       walking ``cwd`` upward and stopping AT the git toplevel. The snapshot is
       of a repository, so the search is bounded by that repository; without the
       bound a project with no venv would silently adopt one from a parent
       directory that has nothing to do with it.
    2. ``VIRTUAL_ENV`` -- an activated env, including the one ``uv run`` exports.
    3. ``CONDA_PREFIX`` -- conda envs live outside the project by design.
    """
    cwd = os.path.abspath(cwd or os.getcwd())

    top = _git(cwd, "rev-parse", "--show-toplevel", check=False)
    ceiling = os.path.abspath(top) if top else cwd

    directory = cwd
    while True:
        for name in _VENV_DIR_NAMES:
            candidate = os.path.join(directory, name)
            if venv_python(candidate):
                return candidate, "project-venv"
        if os.path.normcase(directory) == os.path.normcase(ceiling):
            break
        parent = os.path.dirname(directory)
        if parent == directory:
            break
        directory = parent

    for var in ("VIRTUAL_ENV", "CONDA_PREFIX"):
        value = os.environ.get(var)
        if value and venv_python(value):
            return os.path.abspath(value), var

    return None, None


def _enumerate_foreign(python: str) -> tuple[str, list[str]]:
    """``(python_version, packages)`` as reported BY ``python`` itself.

    ``PYTHONHOME`` is dropped because it repoints an interpreter's stdlib at
    another installation's, which breaks a foreign interpreter outright. The
    rest of the environment is inherited on purpose: ``PYTHONPATH`` and user
    site-packages genuinely contribute modules to the run being recorded, so
    isolating them would record an environment nobody actually uses.
    """
    env = {k: v for k, v in os.environ.items() if k != "PYTHONHOME"}
    try:
        proc = subprocess.run(
            [python, "-c", _ENUMERATE_PROGRAM],
            capture_output=True,
            text=True,
            timeout=_ENUMERATE_TIMEOUT,
            env=env,
        )
    except subprocess.TimeoutExpired:
        raise SnapshotError(
            f"{python} did not report its packages within {_ENUMERATE_TIMEOUT}s"
        ) from None
    except OSError as exc:
        raise SnapshotError(f"could not run {python}: {exc}") from exc
    if proc.returncode != 0:
        raise SnapshotError(
            f"{python} could not enumerate its packages: {proc.stderr.strip()[:400]}"
        )
    try:
        payload = json.loads(proc.stdout)
        return payload["python"], list(payload["packages"])
    except (ValueError, KeyError, TypeError) as exc:
        raise SnapshotError(f"{python} returned an unreadable package list: {exc}") from exc


def _is_inside(path: str, root: str) -> bool:
    try:
        return not os.path.relpath(os.path.realpath(path), os.path.realpath(root)).startswith("..")
    except ValueError:  # different drives on Windows
        return False


#: ``resolved_via`` when no environment could be attributed to the project: no
#: venv was found and the running interpreter is foreign to the tree. A NAMED
#: constant because it is a cross-module contract -- `capture_env` produces it
#: and the CLI branches on it to warn -- and a typo on either side would
#: silently restore the confident-wrong capture this value exists to prevent.
UNRESOLVED_FALLBACK = "unresolved-fallback"


def capture_env(
    cwd: str | None = None,
    *,
    venv: str | None = None,
    detect_venv: bool = False,
    strict: bool = True,
) -> dict[str, Any]:
    """Resolved dependency list for the reproducibility manifest.

    Stores the PACKAGES THEMSELVES, not just a digest of them. An earlier
    implementation kept only ``packages_sha256`` + a count, which can tell you
    that two runs differed and can never tell you what either one used -- the
    same failure shape as recording a commit SHA whose objects are gone.

    WHICH environment gets recorded is the whole problem this signature exists to
    solve. Enumerating the calling process is right for the SDK, whose
    ``run.snapshot()`` runs inside the training venv, and wrong for the CLI,
    which is a uv-tool install with its own interpreter and its own ~40
    packages. Recording those is not a degraded capture; it is a confident,
    plausible, WRONG one, and it is exactly the "different venvs" failure the
    execution record exists to eliminate.

    Resolution order:

    - ``venv`` -- an explicit path always wins.
    - ``detect_venv`` -- resolve the project's venv via :func:`find_venv`. This
      is the out-of-process caller's mode: the CLI is not the thing that runs
      the code, so its own interpreter is evidence of nothing.
    - neither -- the current interpreter, enumerated in-process. The default,
      because an in-process caller IS the environment being recorded.

    A resolved venv is read by running ``importlib.metadata`` under ITS
    interpreter, so the answer comes from the environment itself rather than
    from a guess about its layout, and no ``pip`` is required (``uv venv``
    installs none).

    ``strict`` (the default) covers two distinct failures, both of which used to
    pass silently:

    - the dependency set cannot be resolved, or resolves to nothing;
    - ``detect_venv`` found no project venv and the running interpreter is
      foreign to ``cwd`` -- i.e. we are about to record the wrong environment.

    The returned mapping carries ``venv`` / ``python_executable`` /
    ``resolved_via`` so that a capture which picked the wrong environment is
    visible rather than indistinguishable from a correct one. Those three are
    PROVENANCE, not identity: split them off with
    :func:`split_env_provenance` before the result reaches an execution record.
    """
    resolved_via = "interpreter"
    venv_root: str | None = None

    if venv is not None:
        venv_root, resolved_via = os.path.abspath(venv), "explicit"
        if venv_python(venv_root) is None:
            raise SnapshotError(f"{venv} is not a virtualenv (no bin/python inside)")
    elif detect_venv:
        venv_root, found_via = find_venv(cwd)
        if venv_root is not None:
            resolved_via = found_via or "project-venv"

    python_exe = sys.executable
    if venv_root is not None:
        python_exe = venv_python(venv_root) or sys.executable
    elif detect_venv:
        # No project venv, so the only candidate left is the interpreter running
        # this code -- acceptable only when it lives in the tree being recorded
        # (probe pip-installed into the project's own env). Anything else is the
        # caller's own toolchain, and recording it is the bug, not a fallback.
        root = cwd or os.getcwd()
        top = _git(root, "rev-parse", "--show-toplevel", check=False) or root
        if _is_inside(sys.prefix, top):
            resolved_via = "interpreter"
        elif strict:
            raise SnapshotError(
                f"no virtualenv found for {os.path.abspath(root)}, and the running "
                f"interpreter ({sys.prefix}) is outside it -- refusing to record "
                "this process's own packages as the project's. Pass --venv PATH "
                "(SDK: venv=...), or activate the environment the code runs in."
            )
        else:
            resolved_via = UNRESOLVED_FALLBACK

    info: dict[str, Any] = {
        "python": sys.version.split()[0],
        "python_executable": python_exe,
        "venv": venv_root,
        "resolved_via": resolved_via,
    }

    # The branch above has ALREADY decided this interpreter is foreign to the
    # project ("recording it is the bug, not a fallback"). Enumerating it anyway
    # is what non-strict callers used to do, and it produced a full, plausible,
    # entirely WRONG dependency list -- the CLI's own typer/rich rather than the
    # project's torch/transformers -- which is indistinguishable downstream from
    # a correct capture. Strict raises; non-strict now records the provenance and
    # nothing else, because a known-wrong answer is worse than a missing one.
    #
    # `python` goes too: this interpreter's version is no more the project's than
    # its packages are. What survives is ``resolved_via=UNRESOLVED_FALLBACK``,
    # which says why the environment is absent.
    if resolved_via == UNRESOLVED_FALLBACK:
        info.pop("python", None)
        return info

    # A frozen build (PyInstaller and friends) rewrites sys.executable to the
    # bundled application, which does not understand `-c` -- it would re-run the
    # app. Refuse instead of enumerating whatever that produces.
    if getattr(sys, "frozen", False) and python_exe == sys.executable:
        raise SnapshotError(
            "cannot enumerate packages from a frozen interpreter "
            f"({sys.executable}); pass --venv PATH (SDK: venv=...) naming the "
            "environment whose packages should be recorded"
        )

    try:
        info["python"], packages = _enumerate_foreign(python_exe)
    except SnapshotError:
        raise
    except Exception as exc:  # noqa: BLE001 - surfaced, never swallowed
        if strict:
            raise SnapshotError(f"could not resolve installed distributions: {exc}") from exc
        return info

    if not packages and strict:
        raise SnapshotError(
            f"resolved zero installed distributions from {python_exe}; refusing to "
            "record an empty dependency set as if it were captured"
        )

    info["packages"] = packages
    info["package_count"] = len(packages)
    # NOTE: the digest domain covers sorted `name==version` lines from
    # importlib.metadata, not raw `pip freeze` stdout. Do not compare values
    # across that upgrade boundary.
    info["packages_sha256"] = hashlib.sha256("\n".join(packages).encode()).hexdigest()
    return info


# How the environment was FOUND, as against what the environment IS. Machine
# -specific by nature: the same packages live at /Users/x/p/.venv on a laptop
# and /workspace/p/.venv on a training box.
ENV_PROVENANCE_KEYS = ("venv", "python_executable", "resolved_via")


def split_env_provenance(info: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Split :func:`capture_env` output into ``(identity, provenance)``.

    The execution record's ``content_hash`` covers the WHOLE ``deps`` section
    (research-os ``app/execution/service.py`` ``canonical_hash``, which
    json-dumps every section sorted). Any machine-specific value inside it makes
    two genuinely identical environments at different paths hash differently --
    and ``env_ref`` equality is precisely what a reader compares to ask "did
    these two runs use the same environment?". Recording the venv path there
    would answer "no" to a "yes", which is the same confidently-wrong shape this
    module exists to eliminate.

    So identity (python + packages) is hashed, and provenance rides on the
    ``code-snapshot`` artifact meta, which ``Client.check_run`` already reads.
    """
    provenance = {k: info[k] for k in ENV_PROVENANCE_KEYS if k in info}
    identity = {k: v for k, v in info.items() if k not in ENV_PROVENANCE_KEYS}
    return identity, provenance


def capture_gpu() -> list[dict[str, Any]]:
    """Best-effort in-container GPU inventory via nvidia-smi (RunPod path)."""
    query = "index,name,memory.total,driver_version"
    try:
        proc = subprocess.run(
            ["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if proc.returncode != 0:
        return []
    gpus: list[dict[str, Any]] = []
    for line in proc.stdout.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 4:
            gpus.append(
                {
                    "index": parts[0],
                    "name": parts[1],
                    "memory_total_mib": parts[2],
                    "driver_version": parts[3],
                }
            )
    return gpus


def capture_system() -> dict[str, Any]:
    """Machine-stable identity: OS, CPU/RAM, CUDA stack. Joins the GPU inventory
    under ``execution_records.hardware`` — hashed into env identity, which is
    correct because two runs on identical nodes must still share one record.
    Per-launch facts (hostname, env values) belong in the launch block instead."""
    info: dict[str, Any] = {
        "os": {
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python_implementation": platform.python_implementation(),
        },
        "cpu": {"count": os.cpu_count() or 0},
    }
    try:
        with open("/etc/os-release") as fh:
            for line in fh:
                if line.startswith("PRETTY_NAME="):
                    info["os"]["distro"] = line.split("=", 1)[1].strip().strip('"')
                    break
    except OSError:
        pass
    libc = platform.libc_ver()
    if libc[0]:
        info["os"]["libc"] = f"{libc[0]} {libc[1]}"
    try:
        names = os.sysconf_names
        if "SC_PAGE_SIZE" in names and "SC_PHYS_PAGES" in names:
            info["cpu"]["mem_total_bytes"] = (
                os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
            )
    except (OSError, ValueError, AttributeError):
        pass
    torch = sys.modules.get("torch")
    if torch is not None:
        try:
            runtime = getattr(getattr(torch, "version", None), "cuda", None)
            if runtime:
                cuda: dict[str, Any] = {"runtime": runtime}
                cudnn = torch.backends.cudnn.version()
                if cudnn:
                    cuda["cudnn"] = cudnn
                info["cuda"] = cuda
        except Exception:
            pass
    else:
        try:
            out = subprocess.run(
                ["nvcc", "--version"], capture_output=True, text=True, timeout=5
            )
            m = re.search(r"release ([\d.]+)", out.stdout)
            if m:
                info["cuda"] = {"runtime": m.group(1)}
        except (OSError, subprocess.TimeoutExpired):
            pass
    return info
from probe.sdk.capture.code.code import SnapshotError  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.code.git import _git  # noqa: E402 -- pieces need each other; the front door loads this one first
