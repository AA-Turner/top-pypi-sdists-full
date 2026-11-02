"""what a reinstall must carry over from the install it replaces: the uv receipt's --with packages, what it had to drop."""

from __future__ import annotations
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from probe.shared.updates import handoff, installs


@dataclass(frozen=True)
class KeptInstall:
    """What a reinstall must carry over from the install it replaces (#2043
    review): the extras it records beyond ours, the packages the user added
    beside it (`uv tool install --with`, `pipx inject`), and its Python.
    `dropped` names what the receipt records that a reinstall cannot restate
    (an editable `--with`, constraints, a receipt it could not read): left out,
    and said, rather than holding every update back (plan A4)."""

    extras: tuple[str, ...] = ()
    with_packages: tuple[str, ...] = ()
    python: str | None = None
    dropped: tuple[str, ...] = ()


#: uv-receipt.toml requirement keys a reinstall can restate. An entry with any
#: other key (an editable path) is left out of the reinstall and named.
_RECEIPT_REQUIREMENT_KEYS = frozenset({"name", "extras", "specifier", "url", "directory", "git"})


def _receipt_requirement(entry: dict) -> str | None:
    """One uv-receipt requirement as the PEP 508 string `--with` takes, or None
    when it has a shape this cannot restate faithfully."""
    if not isinstance(entry, dict) or set(entry) - _RECEIPT_REQUIREMENT_KEYS:
        return None
    name = entry.get("name")
    if not isinstance(name, str) or not name:
        return None
    extras = entry.get("extras") or []
    text = name + (f"[{','.join(extras)}]" if extras else "")
    sources = [k for k in ("url", "directory", "git") if entry.get(k)]
    if len(sources) > 1:
        return None
    if sources:
        where = str(entry[sources[0]])
        if sources[0] == "directory":
            where = Path(where).resolve().as_uri()
        elif sources[0] == "git" and not where.startswith("git+"):
            where = "git+" + where
        return f"{text} @ {where}"
    return text + str(entry.get("specifier") or "")


def kept_from_uv_receipt(prefix: str | Path | None = None) -> KeptInstall | None:
    """What this uv tool install records beside `probe-research`, read from
    its `uv-receipt.toml` (empty when there is none). `uv tool install`
    REPLACES the receipt, so an update that restated only
    `probe-research[all]` uninstalled every `--with` package (`probe import
    wandb` needs one).

    What it cannot restate faithfully (an entry with keys it does not know,
    constraints or overrides, a receipt it cannot read) is left out and named
    in `dropped`: it used to make the whole receipt unrestatable, which held
    every later update on the in-place path for good (plan A4). None only
    for probe-research itself from a path or URL: a checkout or a build of
    someone's own, which no update from the index may replace."""
    from probe.foundation.compat.compat import tomllib

    path = Path(prefix if prefix is not None else sys.prefix) / "uv-receipt.toml"
    dropped: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return KeptInstall()  # no receipt: nothing recorded, nothing to lose
    except OSError as exc:
        text = ""
        dropped.append(f"the uv receipt (unreadable: {type(exc).__name__})")
    try:
        tool = tomllib.loads(text).get("tool") or {}
    except ValueError:
        tool = {}
        dropped.append("the uv receipt (not valid TOML)")
    for key in ("constraints", "overrides", "build-constraint-dependencies"):
        if tool.get(key):
            dropped.append(f"its {key}")
    extras: tuple[str, ...] = ()
    with_packages: list[str] = []
    for entry in tool.get("requirements") or []:
        if isinstance(entry, dict) and entry.get("name") in (DIST, LEGACY_DIST):
            if set(entry) - {"name", "extras", "specifier"}:
                return None  # probe itself from a path or URL: not ours to restate
            extras = tuple(e for e in entry.get("extras") or [] if isinstance(e, str))
            continue
        requirement = _receipt_requirement(entry)
        if requirement is None:
            name = entry.get("name") if isinstance(entry, dict) else None
            dropped.append(f"--with {name}" if isinstance(name, str) and name else "a --with entry")
            continue
        with_packages.append(requirement)
    python = tool.get("python")
    if not isinstance(python, str) or not python or (os.path.isabs(python) and not os.path.exists(python)):
        python = _env_interpreter(path.parent)
    return KeptInstall(extras=extras, with_packages=tuple(with_packages), python=python, dropped=tuple(dropped))


def faithful_kept_from_uv_receipt(prefix: str | Path | None = None) -> KeptInstall | None:
    """`kept_from_uv_receipt`, or None when it would leave anything out: for
    what reinstalls the RUNNING environment in place (the in-place update,
    `npx probe-research`, `probe daemon install`), where nothing stays to
    switch back to and a dropped package is gone. Only a side-by-side install,
    which keeps the running version, goes ahead without what it cannot restate."""
    kept = kept_from_uv_receipt(prefix)
    return None if kept is None or kept.dropped else kept


def dropped_note(kept: KeptInstall | None) -> str:
    """"; not carried over from the uv receipt: ..." for what a reinstall left
    out (`KeptInstall.dropped`), or ""."""
    if kept is None or not kept.dropped:
        return ""
    return (f"; not carried over from the uv receipt (it cannot be restated): {', '.join(kept.dropped)}. "
            "Add it back with your own `uv tool install` if you need it")


def _env_interpreter(prefix: Path) -> str | None:
    """The exact interpreter this tool environment runs on (`pyvenv.cfg`'s
    `home` + `pythonX.Y`), or None. A receipt that records no Python lets uv
    choose one: `--force`, and a plain install on uv before 0.10, rebuild the
    environment on the NEWEST Python uv has, deleting `lib/pythonX.Y` under every
    running `probe` (2026-10-12: 3.13 -> 3.14 under a live daemon worker). Only
    the exact path keeps it: `--python 3.12` let uv pick its managed 3.12 over the
    system one the environment ran on, and rebuild just the same."""
    try:
        text = (prefix / "pyvenv.cfg").read_text(encoding="utf-8")
    except OSError:
        return None
    fields = {}
    for line in text.splitlines():
        key, sep, value = line.partition("=")
        if sep:
            fields[key.strip()] = value.strip()
    home = fields.get("home")
    if not home:
        return None
    found = re.match(r"(\d+)\.(\d+)", fields.get("version_info") or fields.get("version") or "")
    if not found:
        return None
    # Only the versioned name: a bare `python3` there may be another version by
    # now. Without it (Windows' `python.exe` among them) no pin, as before.
    candidate = Path(home) / f"python{found.group(1)}.{found.group(2)}"
    return str(candidate) if candidate.exists() else None


def uv_tool_install_command(
    kept: KeptInstall,
    *,
    force: bool = False,
    version: str = "",
    legacy: bool = False,
    refresh: bool = False,
) -> list[str]:
    """`uv tool install` of `probe-research[all,...]` that keeps ``kept``.
    ``version`` is appended to the spec (`@latest`, `==1.2.3`). A legacy
    probe-agent install's extras are its own, so only its packages carry.
    ``refresh`` re-reads the package index for probe-research instead of uv's
    cached copy, which can predate a release by minutes."""
    command = ["uv", "tool", "install"]
    if force:
        command.append("--force")
    if refresh:
        command += ["--refresh-package", DIST]
    command.append(_dist(() if legacy else kept.extras) + version)
    for requirement in kept.with_packages:
        command += ["--with", requirement]
    if kept.python:
        command += ["--python", kept.python]
    return command


def dropped_with_command(prefix: str | Path | None = None) -> tuple[list[str], str] | None:
    """`(what is left out, command)`: the `--with` packages an update had to
    leave out (`active.json` `dropped_with`) that the running version env
    still lacks, and the exact Python pin it ran on before (`dropped_python`)
    when it runs on another now, with the exact `uv tool install` that puts
    them back, with everything it has now. None when there is nothing (or
    this is not a version env)."""
    import shlex

    from probe import __version__

    root = installs.versions_root_of(None if prefix is None else str(prefix))
    if root is None:
        return None
    try:
        record = json.loads((root / installs.ACTIVE_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict):
        return None
    dropped = record.get("dropped_with") if isinstance(record.get("dropped_with"), list) else []
    pin = record.get("dropped_python") if isinstance(record.get("dropped_python"), str) else None
    kept = kept_from_uv_receipt(prefix) or KeptInstall()
    present = {handoff.requirement_name(requirement) for requirement in kept.with_packages}
    missing = [str(item) for item in dropped if handoff.requirement_name(str(item)) not in present]
    pin = pin if pin and pin != kept.python else None
    if not missing and not pin:
        return None
    command = ["uv", "tool", "install", f"{_dist(kept.extras)}=={__version__}"]
    for requirement in (*kept.with_packages, *missing):
        command += ["--with", requirement]
    if pin or kept.python:
        command += ["--python", pin or kept.python]
    return [*missing, *([f"Python {pin}"] if pin else [])], shlex.join(command)


def record_left_out(old: KeptInstall | None, new_env: Path, tools: Path, dropped: list) -> tuple[list, str | None]:
    """What a switch to `new_env` leaves out of the install it replaces,
    derived from the receipts, never from what one install remembered: the
    `--with` packages the old receipt (`old`) had, earlier records
    (`installs.dropped_with`) and this install's own drops (`dropped`), less
    what `new_env`'s receipt has; and the old exact Python pin when
    `new_env` runs on another. Recorded (`installs.record_dropped_with`): an
    entry goes only once the new receipt has it again (an env kept from an
    earlier install whose drops were never recorded loses nothing). Returns
    `(packages left out, Python pin left out)`."""
    new = kept_from_uv_receipt(new_env) or KeptInstall()
    present = {handoff.requirement_name(item) for item in new.with_packages}
    missing: dict = {}
    for item in [*(old.with_packages if old else ()), *installs.dropped_with(tools), *dropped]:
        name = handoff.requirement_name(item)
        if name not in present:
            missing.setdefault(name, item)
    pin = None
    for candidate in ((old.python if old else None), installs.dropped_python(tools)):
        if isinstance(candidate, str) and candidate and candidate != new.python:
            pin = candidate
            break
    installs.record_dropped_with(list(missing.values()), tools, python=pin)
    return list(missing.values()), pin
from probe.cli.install.updater.cli_install import _dist  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.updater.updater import DIST, LEGACY_DIST  # noqa: E402 -- pieces need each other; the front door loads this one first
