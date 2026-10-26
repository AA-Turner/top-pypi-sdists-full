"""Per-version copies of Probe's pi package, and what open pi sessions run
(kimi/pi update parity P1, P7).

pi loads Probe's extension once; its shim (`plugins/probe-research-pi/src/
shim.ts`) runs the implementation from a PIN, a copy of the package the
update keeps, and switches to the newest one at a session's next turn. `pi
update` rewrites the clone in place (`git clean -fdx`, then `npm install`),
so a pin is never the clone itself:

    <state>/pi/pins/<version>-<fingerprint>/   the clone's layout, the parts
        plugins/probe-research-pi, -tap, the extension reads: the package, its
        probe-research, -daemon               sibling plugins and node_modules
        node_modules, package.json            (module lookup walks up to it)
    <state>/pi/current                         {"pin", "version", "from", "head"}, renamed into place
    <state>/pi/live/<pid>.json                 each pi process's shim writes its own

`<state>` is `$XDG_STATE_HOME/probe` (`session_marker.state_dir`). A pin is made
only from a clone pi finished updating (no `.<repo>.pi-update-incomplete`
marker), copied whole or not at all (`probe._shared.pins`), and never pruned
while a live pi process names it (`pin`, `fallback_pin`, `resources_pin`,
`pins_used`).

`current` names the clone it came from (`from`: the shim runs a pin only for
that install) and the clone's git commit (`head`: a `pi update` that moved the
clone without a new package version is pinned again).

`sessions_follow()` says whether every open pi session takes the version now
`current` at its next turn with no /reload: each live pi process has a live
record (pre-shim packages, 0.6.3 and before, write none), its shim is new
enough for that version, the skills pi loaded for it read the same in that
version (`_resources`), and the Probe service records its transcript.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import time
from pathlib import Path

from probe._shared import oscompat, pins

PI_DIRNAME = "pi"  # harness-literal-ok: the state folder shim.ts reads (PI_STATE_DIRNAME)
PINS_DIRNAME = "pins"
CURRENT_NAME = "current"
LIVE_DIRNAME = "live"
PACKAGE = "plugins/probe-research-pi"
#: What the extension reads from its install, at its install's relative paths.
SOURCES = (PACKAGE, "plugins/probe-research-tap", "plugins/probe-research", "plugins/probe-research-daemon",
           "node_modules", "package.json")
#: `SHIM_API` an impl needs (`src/impl.ts` REQUIRES_SHIM_API), read from its source.
_REQUIRES = re.compile(r"export\s+const\s+REQUIRES_SHIM_API\s*=\s*(\d+)")
#: The shared-state layout a version reads and the older ones it migrates (`src/extension.ts`).
_SCHEMA = re.compile(r"export\s+const\s+STATE_SCHEMA\s*=\s*(\d+)")
_MIGRATES = re.compile(r"export\s+const\s+MIGRATES_FROM[^=]*=\s*\[([\d,\s]*)\]")
#: pi's own npm package, as it shows in the command line of the node that runs it.
PI_PACKAGE_PATH = "/pi-coding-agent/"  # harness-literal-ok: pi's npm package path, how macOS ps shows a pi
#: package.json's key for what pi loads from a package.
MANIFEST_KEY = "pi"  # harness-literal-ok: package.json's manifest key, not the harness
#: A SKILL.md's frontmatter (`src/resources.ts`).
_FRONTMATTER = re.compile(r"^---\r?\n(.*?)\r?\n---", re.S)


def pi_dir() -> Path:
    from probe.sdk import session_marker

    return session_marker.state_dir() / PI_DIRNAME


def _incomplete(clone: Path) -> bool:
    """pi's own marker for an update it has not finished (`git clean`, then
    `npm install`): beside the clone, `.<repo>.pi-update-incomplete`."""
    name = f".{clone.name}.pi-update-incomplete"
    return (clone.parent / name).exists() or (clone / name).exists()


def _version(package: Path) -> str | None:
    try:
        raw = json.loads((package / "package.json").read_text(encoding="utf-8")).get("version")
    except (OSError, ValueError, AttributeError):
        return None
    return raw if isinstance(raw, str) and re.match(r"^\d+(\.\d+)+$", raw) else None


def read_current() -> dict | None:
    try:
        data = json.loads((pi_dir() / CURRENT_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and isinstance(data.get("pin"), str) else None


def _write_current(pin: str, version: str, clone: Path, head: str | None) -> None:
    target = pi_dir() / CURRENT_NAME
    staging = target.with_name(f".{CURRENT_NAME}.{os.getpid()}.tmp")
    body = {"pin": pin, "version": version, "from": str(clone), "head": head}
    staging.write_text(json.dumps(body), encoding="utf-8")
    os.replace(staging, target)


def _head(clone: Path) -> str | None:
    """The commit pi's clone is at (`pi update` moves it), or None."""
    git = clone / ".git"
    try:
        head = (git / "HEAD").read_text(encoding="utf-8").strip()
        if not head.startswith("ref: "):
            return head or None
        ref = head[5:].strip()
        with contextlib.suppress(OSError):
            return (git / ref).read_text(encoding="utf-8").strip() or None
        for line in (git / "packed-refs").read_text(encoding="utf-8").splitlines():
            sha, _, name = line.partition(" ")
            if name.strip() == ref:
                return sha
    except OSError:
        return None
    return None


def _alive(pid: int) -> bool:
    try:
        oscompat.probe_pid(pid)  # never os.kill(pid, 0): on Windows that kills it
    except ProcessLookupError:
        return False
    except (PermissionError, OSError):
        return True
    return True


def live_records() -> dict[int, dict]:
    """{pid: record} for every live pi process's shim record; a dead one's file
    (a pi killed with SIGKILL) is removed."""
    out: dict[int, dict] = {}
    folder = pi_dir() / LIVE_DIRNAME
    try:
        entries = list(folder.glob("*.json"))
    except OSError:
        return out
    for path in entries:
        if not path.stem.isdigit():
            continue
        pid = int(path.stem)
        if not _alive(pid):
            with contextlib.suppress(OSError):
                path.unlink()
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        if isinstance(data, dict):
            out[pid] = data
    return out


def referenced() -> set[str]:
    """The pins a live pi process still loads from (its `pin`, its `fallback_pin`,
    every one it has run: `pins_used`, as a replaced version may still own a
    watcher or an MCP client) or compares against (`resources_pin`)."""
    names: set[str] = set()
    for record in live_records().values():
        for key in ("pin", "fallback_pin", "resources_pin"):
            if isinstance(record.get(key), str):
                names.add(record[key])
        used = record.get("pins_used")
        if isinstance(used, list):
            names.update(name for name in used if isinstance(name, str))
    return names


def pin_installed(env=None) -> Path | None:
    """Pin the pi package pi has installed (its clone of the mirror) and make it
    `current`; old pins no live pi uses are pruned. None when there is nothing
    to pin (no pi package, a local-path install, an update pi has not finished)
    or a copy could not be made whole (the shim keeps what it runs)."""
    from probe.cli import pi_config

    package = pi_config.installed_package_dir(env)
    if package is None or package.parent.name != "plugins" or not (package / "src" / "impl.ts").is_file():
        return None  # no pi package, a local checkout, or a package from before the shim
    clone = package.parent.parent
    if _incomplete(clone) or not (clone / "node_modules").is_dir():
        return None
    version = _version(package)
    if version is None:
        return None
    head = _head(clone)  # before the copy: a `pi update` that moves it meanwhile makes this pin unusable
    sources = {rel: clone / rel for rel in SOURCES if (clone / rel).exists()}
    store = pi_dir() / PINS_DIRNAME
    try:
        made = pins.make(store, version, sources, default="package", symlinks=True, meta={"from": str(clone)})
    except OSError:
        return None
    if _incomplete(clone) or _head(clone) != head:
        return None  # pi began another update while it was copied: try again later
    current = read_current()
    if (current is None or current.get("pin") != made.name or current.get("head") != head
            or current.get("from") != str(clone)):
        _write_current(made.name, version, clone, head)
    keep = {made}
    pins.prune(store, keep=keep, referenced=referenced())
    return made


def pin_due(env=None) -> bool:
    """Is the installed pi package other than the pinned `current` (another
    version, another clone, the clone at another commit, or a pin gone)?"""
    from probe.cli import pi_config

    package = pi_config.installed_package_dir(env)
    if package is None or package.parent.name != "plugins" or not (package / "src" / "impl.ts").is_file():
        return False
    clone = package.parent.parent
    current = read_current()
    if current is None:
        return True
    return (current.get("version") != _version(package) or current.get("from") != str(clone)
            or current.get("head") != _head(clone)
            or not pins.complete(pi_dir() / PINS_DIRNAME, str(current.get("pin"))))


def _requires_shim(pin: str) -> int:
    path = pi_dir() / PINS_DIRNAME / pin / PACKAGE / "src" / "impl.ts"
    try:
        found = _REQUIRES.search(path.read_text(encoding="utf-8"))
    except OSError:
        return 1 << 30
    return int(found.group(1)) if found else 1 << 30  # unreadable: a shim no process has


def _resources(pin: str) -> str | None:
    """What pi reads from a version only when it loads it -- the package
    manifests' pi entries (MANIFEST_KEY), every SKILL.md's frontmatter under the package and
    the MCP manifest -- digested; None when unreadable. A superset of what the
    shim's `resourcesFingerprint` reads (it takes only the listed skills), so a
    change that leaves pi's loaded skills stale is never missed here."""
    root = pi_dir() / PINS_DIRNAME / pin
    package = root / PACKAGE
    try:
        manifest = json.loads((package / "package.json").read_text(encoding="utf-8")).get(MANIFEST_KEY) or {}
        top = json.loads((root / "package.json").read_text(encoding="utf-8")).get(MANIFEST_KEY) or {}
        skills = []
        for path in sorted(package.rglob("SKILL.md")):
            if "node_modules" in path.relative_to(package).parts:
                continue
            found = _FRONTMATTER.match(path.read_text(encoding="utf-8"))
            skills.append([path.relative_to(package).as_posix(), found.group(1) if found else ""])
        mcp_path = manifest.get("mcp") if isinstance(manifest, dict) else None
        mcp = (package / mcp_path).read_text(encoding="utf-8") if isinstance(mcp_path, str) else None
    except (OSError, ValueError, AttributeError, TypeError):
        return None
    material = json.dumps({"package": manifest, "top": top, "skills": skills, "mcp": mcp}, sort_keys=True)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _schemas(pin: str) -> tuple[int, tuple[int, ...]] | None:
    """(STATE_SCHEMA, MIGRATES_FROM) of a pinned version (`src/extension.ts`), or None."""
    path = pi_dir() / PINS_DIRNAME / pin / PACKAGE / "src" / "extension.ts"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    schema = _SCHEMA.search(text)
    migrates = _MIGRATES.search(text)
    if not (schema and migrates):
        return None
    try:
        return int(schema.group(1)), tuple(int(n) for n in migrates.group(1).replace(" ", "").split(",") if n)
    except ValueError:
        return None


def _is_pi(argv: list[str], names) -> bool:
    """Is this command line a pi? Its title (argv[0], or the script a runtime
    runs: `node /usr/local/bin/pi`) is one of `names`, or it runs pi's package."""
    from probe.sdk import session_marker

    title = os.path.basename(session_marker._title_of(argv))  # noqa: SLF001
    return bool(argv) and (title in names or any(PI_PACKAGE_PATH in a for a in argv))


def _pi_pids(titles) -> set[int] | None:
    """Every live pi process, or None when processes cannot be listed here: one
    titled one of `titles` (pi's `binary`) or its RPC mode's `<binary>-rpc`
    (pi sets `process.title`, which Linux's /proc shows), or one whose command
    line runs pi's package (macOS `ps` keeps the `node .../cli.js` it started
    as). A pi with no shim record (0.6.3 and before) is found either way."""
    wanted = tuple(t for t in titles if t)
    if not wanted:
        return set()
    names = set(wanted) | {f"{t}-rpc" for t in wanted}


    if os.path.isdir("/proc/self"):
        found = set()
        for name in os.listdir("/proc"):
            if not name.isdigit():
                continue
            try:
                with open(f"/proc/{name}/cmdline", "rb") as handle:
                    argv = [a.decode("utf-8", "replace") for a in handle.read().split(b"\0") if a]
            except OSError:
                continue
            if _is_pi(argv, names):
                found.add(int(name))
        return found
    import subprocess  # noqa: PLC0415

    try:
        out = subprocess.run(["ps", "-A", "-ww", "-o", "pid=,command="], capture_output=True, text=True,  # noqa: S603,S607
                             timeout=5, check=False).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    found = set()
    for line in out.splitlines():
        pid, _, command = line.strip().partition(" ")
        if pid.isdigit() and (_is_pi(command.split(), names) or _ends_in_pi(command, names)):
            found.add(int(pid))
    return found if out.strip() else None


def _ends_in_pi(command: str, names) -> bool:
    """macOS `ps` gives no argv boundaries, so a folder with a space in it splits
    the command: a path component named one of `names` ending a word still
    counts (a bin path under a home folder with a space). A false match only
    says /reload."""
    return any(re.search(rf"/{re.escape(name)}(?:\s|$)", command) for name in names)


def _same_install(install: object, made_from: object) -> bool:
    return (isinstance(install, str) and isinstance(made_from, str)
            and os.path.realpath(install) == os.path.realpath(made_from))


def why_not(record: dict | None, current: dict | None) -> str | None:
    """None when this live pi process takes `current` at its next turn with no
    /reload; else why not."""
    if record is None:
        return "its Probe package predates the shim (0.6.3 or older)"
    if current is None:
        return "no pinned version to switch to"
    pin = current["pin"]
    if pin in (record.get("bad_pins") or []):
        return f"version {current.get('version')} failed to load there"
    if not _same_install(record.get("install"), current.get("from")):
        return "it runs Probe from another install than the one updated"
    if record.get("shim_reload_needed") or _requires_shim(pin) > int(record.get("shim_api") or 0):
        return "the new version needs a newer shim"
    schemas = _schemas(pin)
    state = record.get("state_schema")
    if schemas is None or (state != schemas[0] and state not in schemas[1]):
        return "the new version cannot take over its state"
    if record.get("skills_reload_needed"):
        return "its skills changed"
    loaded = record.get("resources_pin")
    if loaded != pin:
        before = _resources(loaded) if isinstance(loaded, str) else None
        if before is None or before != _resources(pin):
            return "its skills change with this version"
    if not record.get("recorded"):
        return "its transcript is still on its own tap watch"
    return None


def sessions_follow(titles) -> bool:
    """Do all open pi sessions (processes titled one of `titles`, the registry's
    pi `binary`) take the pinned `current` version at their next turn with no
    /reload? False when any cannot be proven, or processes cannot
    be listed here. Never raises."""
    if os.name == "nt":
        return False
    try:
        pids = _pi_pids(titles)
        if pids is None:
            return False
        records = live_records()
        current = read_current()
        # A pi titled otherwise (`pi-rpc`, one embedded in another program, a
        # node path in macOS `ps`) still has its shim's record: read them all.
        return all(why_not(records.get(pid), current) is None for pid in pids | set(records))
    except Exception:  # noqa: BLE001 - unproven: the reload line
        return False


def main() -> int:
    """`python -m probe.cli.pi_pins`: pin the installed package (pi's session
    start spawns it detached when `pin_due`)."""
    started = time.monotonic()
    made = pin_installed()
    print(json.dumps({"pin": made.name if made else None, "seconds": round(time.monotonic() - started, 2)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
