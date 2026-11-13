"""Arms that join this Core install from their own packages (``hugpy-core addon``).

A Media or Video package installed on the same box ships a descriptor,
``/usr/share/hugpy/core-addons.d/<name>.json``, naming its wheel directory and what to install:

    {"addon": "media", "package": "hugpy-media",
     "requirements": ["hugpy-media[extract]"], "wheels": ["/usr/share/hugpy-media/wheels"],
     "verify": ["hugpy_media.routes"], "standalone_unit": "hugpy-media.service"}

``attach`` installs those requirements into the environment this command runs from (Core's own),
offline from the named wheel directories, with every distribution Core already has pinned to its
installed version: an arm is added, nothing Core was installed with is replaced. Core then serves
the arm in-process and the arm's standalone service is switched off. When the arm cannot be added
that way (it needs a newer sibling than this Core carries, or the operator set
``HUGPY_CORE_ADDONS``), nothing is changed and the arm keeps running as its own service, which
Core reaches through ``arms.d``. Either order of installation ends in the same place: the arm's
package calls ``attach`` when it is installed, and Core's package calls ``sync`` when it is.

``HUGPY_CORE_ADDONS`` (environment, or Core's ``core.env``): unset or ``auto`` embeds every
described arm; ``none`` embeds nothing; a comma list embeds only those names.

Standard library only, and runnable by path, so it works before Core's dependencies import.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import time

DESCRIPTOR_DIR = "/usr/share/hugpy/core-addons.d"
CORE_ENV = "/etc/hugpy/core.env"
CORE_WHEELS = "/usr/share/hugpy-core/wheels"
CORE_UNIT = "hugpy-core.service"
EMBEDDED, STANDALONE = "embedded", "standalone"

_INVENTORY = r"""
import json, re
from importlib.metadata import distributions
norm = lambda name: re.sub(r'[-_.]+', '-', name).lower()
rows = {}
for dist in distributions():
    name = dist.metadata['Name']
    if not name:
        continue
    # a requirement behind an extra (hugpy-core's own `media`, `video`) is an offer, not a need
    needs = sorted({norm(re.match(r'[A-Za-z0-9._-]+', line)[0]) for line in (dist.requires or [])
                    if re.match(r'[A-Za-z0-9._-]+', line) and 'extra ==' not in line.partition(';')[2]})
    rows[norm(name)] = {'name': name, 'version': dist.version, 'requires': needs}
print(json.dumps(rows))
"""


class AddonError(RuntimeError):
    """The arm was not added; the message says why. Core's environment is as it was."""


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def requirement_name(requirement: str) -> str:
    return normalize(re.match(r"[A-Za-z0-9._-]+", requirement.strip())[0])


def descriptor_dir() -> Path:
    return Path(os.environ.get("HUGPY_CORE_ADDONS_DIR") or DESCRIPTOR_DIR)


def state_dir() -> Path:
    """Inside Core's environment, so the records go when the environment does."""
    return Path(sys.prefix) / "hugpy-addons"


def load_descriptor(path: Path) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    name = str(doc.get("addon") or "").strip()
    requirements = [str(item) for item in doc.get("requirements") or []]
    wheels = doc.get("wheels") or []
    wheels = [wheels] if isinstance(wheels, str) else [str(item) for item in wheels]
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name) or not requirements or not wheels:
        raise ValueError(f"{path}: an addon descriptor names addon, requirements and wheels")
    return {"addon": name, "package": str(doc.get("package") or f"hugpy-{name}"),
            "requirements": requirements, "wheels": wheels,
            "verify": [str(item) for item in doc.get("verify") or []],
            "standalone_unit": str(doc.get("standalone_unit") or ""), "path": str(path)}


def descriptors() -> dict[str, dict]:
    found = {}
    try:
        paths = sorted(descriptor_dir().glob("*.json"))
    except OSError:
        return found
    for path in paths:
        try:
            doc = load_descriptor(path)
        except (OSError, ValueError, TypeError) as exc:
            print(f"hugpy-core addon: ignoring {path}: {exc}", file=sys.stderr)
            continue
        found[doc["addon"]] = doc
    return found


def records() -> dict[str, dict]:
    found = {}
    for path in sorted(state_dir().glob("*.json")) if state_dir().is_dir() else ():
        try:
            found[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
    return found


def core_env_file(environ=None) -> Path:
    """The configuration file of this box's Core system install (its unit names it)."""
    env = os.environ if environ is None else environ
    if env.get("HUGPY_CORE_ENV_FILE"):
        return Path(env["HUGPY_CORE_ENV_FILE"])
    try:
        import pwd
        from hugpy_core.install import system_layout
        name, units, existing = system_layout.select_identity(env)
        return system_layout.resolve(pwd.getpwnam(name), units, existing, environ=env).config
    except Exception:  # noqa: BLE001 - no system install to ask, or Core's own imports are not there yet
        return Path(CORE_ENV)


def allowed(name: str, environ=None) -> bool:
    """Whether the operator lets this arm be embedded (HUGPY_CORE_ADDONS)."""
    env = os.environ if environ is None else environ
    value = env.get("HUGPY_CORE_ADDONS")
    if value is None:
        try:
            for line in core_env_file(env).read_text(encoding="utf-8").splitlines():
                key, sep, rest = line.partition("=")
                if sep and key.strip() == "HUGPY_CORE_ADDONS":
                    words = shlex.split(rest, comments=True)
                    value = words[0] if words else ""
        except OSError:
            value = None
    value = (value or "auto").strip().lower()
    if value in ("auto", "all"):
        return True
    if value in ("none", "off", "0", "false", "no"):
        return False
    return name in {item.strip() for item in value.split(",")}


def inventory() -> dict[str, dict]:
    """What Core's environment holds now, read by a fresh interpreter (pip just changed it)."""
    result = subprocess.run([sys.executable, "-c", _INVENTORY], capture_output=True, text=True, cwd="/")
    if result.returncode:
        raise AddonError(f"cannot read the environment at {sys.prefix}: {result.stderr.strip()[-400:]}")
    return json.loads(result.stdout)


def pip(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "pip", "--disable-pip-version-check", *args],
                          capture_output=True, text=True, cwd="/")


def wheel_signature(folders) -> list:
    rows = []
    for folder in folders:
        for path in sorted(Path(folder).glob("*.whl")):
            stat = path.stat()
            rows.append([path.name, stat.st_size, stat.st_mtime_ns])
    return rows


def _systemd() -> bool:
    return Path("/run/systemd/system").is_dir()


def _unit_exists(unit: str) -> bool:
    return bool(unit) and _systemd() and subprocess.run(
        ["systemctl", "cat", unit], capture_output=True, text=True).returncode == 0


def standalone(unit: str, on: bool) -> None:
    """Run the arm's own service, or stop it because Core now serves the arm."""
    if _unit_exists(unit):
        subprocess.run(["systemctl", "enable" if on else "disable", "--now", unit], capture_output=True, text=True)


def restart_core() -> None:
    if _systemd():
        subprocess.run(["systemctl", "try-restart", CORE_UNIT], capture_output=True, text=True)


def removable(names, rows: dict[str, dict]) -> list[str]:
    """Of the distributions an addon brought, those nothing that stays still requires."""
    going = {name for name in names if name in rows}
    while True:
        kept = {name for name in going
                if any(name in row["requires"] for other, row in rows.items() if other not in going)}
        if not kept:
            return sorted(going)
        going -= kept


def attach(doc: dict) -> bool:
    """Add one described arm to this environment. True when the environment changed.

    Raises AddonError, leaving the environment as it was, when it cannot be added."""
    name = doc["addon"]
    if not allowed(name):
        raise AddonError(f"{name}: embedding is switched off by HUGPY_CORE_ADDONS")
    folders = [folder for folder in doc["wheels"] if Path(folder).is_dir()]
    if not folders:
        raise AddonError(f"{name}: no wheel directory at {', '.join(doc['wheels'])}")
    if not os.access(Path(sys.prefix), os.W_OK):
        raise AddonError(f"{sys.prefix} is not writable by this user; run as root")
    before = inventory()
    if "hugpy-core" not in before:
        raise AddonError(f"{sys.prefix} holds no hugpy-core; an addon joins a Core install")
    previous = records().get(name) or {}
    signature = wheel_signature(folders)
    own = {requirement_name(item) for item in doc["requirements"]} | set(previous.get("added") or [])
    if Path(CORE_WHEELS).is_dir():
        folders.append(CORE_WHEELS)
    links = [arg for folder in folders for arg in ("--find-links", folder)]
    with tempfile.TemporaryDirectory(prefix="hugpy-core-addon-") as work:
        constraints = Path(work) / "constraints.txt"
        constraints.write_text("".join(f"{row['name']}=={row['version']}\n"
                                       for key, row in sorted(before.items()) if key not in own))
        # Eager, and safe to be: the constraints hold everything Core was installed with, so the
        # only distributions free to move are the arm's own and the ones it added before. Those
        # follow the arm's wheel directory (a newer sibling the arm bundles must land even when
        # the old one still satisfies the arm's requirement).
        result = pip("install", "--no-index", *links, "--constraint", str(constraints),
                     "--upgrade", "--upgrade-strategy", "eager", *doc["requirements"])
    if result.returncode:
        reason = [line for line in (result.stderr or result.stdout).splitlines() if line.strip()]
        raise AddonError(f"{name}: cannot be added to Core {before['hugpy-core']['version']} without replacing "
                         f"what it was installed with: {' '.join(reason[-3:])[-600:]}")
    after = inventory()
    added = sorted((set(after) - set(before)) | (set(previous.get("added") or []) & set(after)))
    changed = after != before
    if changed or previous.get("wheels_signature") != signature:
        # a rebuilt wheel of an unchanged version must still land
        pins = [f"{after[key]['name']}=={after[key]['version']}"
                for key in sorted({requirement_name(item) for item in doc["requirements"]}) if key in after]
        result = pip("install", "--no-index", *links, "--force-reinstall", "--no-deps", *pins)
        if result.returncode:
            raise AddonError(f"{name}: reinstall failed: {(result.stderr or result.stdout).strip()[-400:]}")
        changed = True
    if doc["verify"]:
        check = subprocess.run([sys.executable, "-c", "import importlib, sys\n"
                                "for module in sys.argv[1:]: importlib.import_module(module)", *doc["verify"]],
                               capture_output=True, text=True, cwd="/")
        if check.returncode:
            fresh = removable(set(after) - set(before), after)
            if fresh:
                pip("uninstall", "-y", *(after[key]["name"] for key in fresh))
            (state_dir() / f"{name}.json").unlink(missing_ok=True)
            raise AddonError(f"{name}: installed but does not import in Core's environment: "
                             f"{check.stderr.strip().splitlines()[-1] if check.stderr.strip() else 'no output'}")
    state_dir().mkdir(parents=True, exist_ok=True)
    package = normalize(doc["package"])
    (state_dir() / f"{name}.json").write_text(json.dumps({
        "addon": name, "package": doc["package"], "version": after.get(package, {}).get("version"),
        "added": added, "requirements": doc["requirements"], "descriptor": doc["path"],
        "standalone_unit": doc["standalone_unit"], "wheels_signature": signature,
        "core_version": after["hugpy-core"]["version"],
        "attached_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=2) + "\n")
    standalone(doc["standalone_unit"], False)
    return changed


def detach(name: str, *, removing: bool = False) -> bool:
    """Take an arm back out of this environment. `removing`: its package is leaving the box,
    so its own service is left alone; otherwise the arm returns to running standalone."""
    record = records().get(name)
    if not record:
        return False
    rows = inventory()
    going = removable(record.get("added") or [], rows)
    if going:
        result = pip("uninstall", "-y", *(rows[key]["name"] for key in going))
        if result.returncode:
            raise AddonError(f"{name}: uninstall failed: {(result.stderr or result.stdout).strip()[-400:]}")
    (state_dir() / f"{name}.json").unlink(missing_ok=True)
    if not removing:
        standalone(record.get("standalone_unit") or "", True)
    return True


def attach_or_fall_back(doc: dict) -> tuple[str, bool, str]:
    """(mode, environment changed, note). A refusal leaves the arm on its own service."""
    try:
        return EMBEDDED, attach(doc), ""
    except AddonError as exc:
        changed = False
        if doc["addon"] in records():      # embedded before, no longer fits this Core
            changed = detach(doc["addon"], removing=True)
        standalone(doc["standalone_unit"], True)
        return STANDALONE, changed, str(exc)


def sync() -> tuple[list[dict], bool]:
    """Bring this environment in line with the arms described on the box."""
    rows, changed = [], False
    described = descriptors()
    for name, doc in described.items():
        mode, moved, note = attach_or_fall_back(doc)
        changed |= moved
        rows.append({"addon": name, "mode": mode, "note": note})
    for name in records():
        if name not in described:          # its package was removed without telling Core
            changed |= detach(name, removing=True)
            rows.append({"addon": name, "mode": "removed", "note": "its package is no longer installed"})
    return rows, changed


def status() -> list[dict]:
    described, recorded = descriptors(), records()
    rows = []
    for name in sorted(set(described) | set(recorded)):
        record = recorded.get(name)
        rows.append({"addon": name, "package": (described.get(name) or record)["package"],
                     "mode": EMBEDDED if record else STANDALONE,
                     "version": (record or {}).get("version"), "described": name in described,
                     "embedding_allowed": allowed(name)})
    return rows


def _show(rows) -> None:
    for row in rows:
        note = f"  ({row['note']})" if row.get("note") else ""
        print(f"{row['addon']}: {row['mode']}{note}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="hugpy-core addon", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="verb", required=True)
    for verb, text in (("sync", "attach every described arm, drop the ones whose package is gone"),
                       ("attach", "add one described arm to this Core"),
                       ("detach", "take one arm back out of this Core")):
        command = sub.add_parser(verb, help=text)
        command.add_argument("--no-restart", action="store_true", help="leave hugpy-core running as it is")
        if verb != "sync":
            command.add_argument("name")
        if verb == "detach":
            command.add_argument("--removing", action="store_true",
                                 help="the arm's package is being removed: leave its service alone")
    sub.add_parser("release", help="Core is being removed: return embedded arms to their own services")
    lister = sub.add_parser("list", help="arms described on this box and how each is served")
    lister.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.verb == "list":
            rows = status()
            if args.json:
                print(json.dumps(rows, indent=2))
            elif rows:
                _show(rows)
            else:
                print(f"no addons described in {descriptor_dir()}")
            return 0
        if args.verb == "release":
            for record in records().values():
                standalone(record.get("standalone_unit") or "", True)
            return 0
        if args.verb == "sync":
            rows, changed = sync()
            _show(rows)
            code = 0
        elif args.verb == "attach":
            doc = descriptors().get(args.name)
            if not doc:
                raise AddonError(f"no addon descriptor for {args.name!r} in {descriptor_dir()}")
            mode, changed, note = attach_or_fall_back(doc)
            _show([{"addon": args.name, "mode": mode, "note": note}])
            code = 0 if mode == EMBEDDED else 3
        else:
            changed = detach(args.name, removing=args.removing)
            print(f"{args.name}: {'detached' if changed else 'was not embedded'}")
            code = 0
        if changed and not args.no_restart:
            restart_core()
        return code
    except (AddonError, OSError, ValueError) as exc:
        print(f"hugpy-core addon {args.verb}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
