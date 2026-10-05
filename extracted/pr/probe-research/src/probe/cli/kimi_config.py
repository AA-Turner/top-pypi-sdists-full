"""Kimi Code's Probe plugins, installed by writing Kimi's own plugin list.

Kimi Code (2.1.1) can install a plugin only from inside its TUI (`/plugins
install <path>`); there is no shell command, and slash commands are not run in
`kimi -p`. So the wizard does what that command does, recorded from a real run:

  1. copy the plugin folder to `$KIMI_CODE_HOME/plugins/managed/<id>/`;
  2. add `{id, root, source: "local-path", enabled, installedAt, updatedAt,
     originalSource}` to `$KIMI_CODE_HOME/plugins/installed.json`
     (`{"version": 1, "plugins": [...]}`).

Kimi loads the plugin at its next session start (`/new` or `/reload` in a
running TUI). `installed.json` is Kimi's internal file and Kimi ships about
daily, so a file whose `version` is not 1 is never touched: the wizard says to
run `/plugins install <path>` inside Kimi instead, and `probe doctor` reads the
same check. The weekly Kimi canary (`.github/workflows/kimi-canary.yml`) is
what notices a format change first.

The plugin files come from the public mirror (`prbe-ai/research-os-agent`, the
same channel Claude Code, Codex and pi install from), or from a research-os
checkout when this CLI runs from one (`PROBE_KIMI_PLUGIN_SOURCE` overrides:
a folder holding `plugins/<id>/`).

`plugin_cli` routes its install/uninstall/list calls for `kimi_code` here, so
the wizard's install, update, uninstall and daemon-profile flows are the same
code for Claude Code, Codex and Kimi Code. Every function returns a
`claude_cli.Result` and never raises.
"""

from __future__ import annotations

import atexit
import contextlib
import datetime as _dt
import http.client
import io
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import time
import urllib.request
from pathlib import Path

from probe.cli import claude_cli

HARNESS_ID = "kimi_code"
#: The plugins Probe ships to Kimi (the same three folders as everywhere).
PLUGIN_IDS = ("probe-research", "probe-research-daemon", "probe-research-tap")
MIRROR_REPO = "prbe-ai/research-os-agent"
MIRROR_TARBALL = f"https://codeload.github.com/{MIRROR_REPO}/tar.gz/refs/heads/main"
SOURCE_ENV = "PROBE_KIMI_PLUGIN_SOURCE"
#: The only `installed.json` layout this module writes into.
INSTALLED_VERSION = 1
MANIFEST = Path(".kimi-plugin") / "plugin.json"
DOWNLOAD_TIMEOUT_S = 60.0
VERSION_TIMEOUT_S = 15.0

_DOWNLOADED: Path | None = None


def _row():
    from probe.harness import get_registry

    return get_registry().get(HARNESS_ID)


def kimi_home() -> Path:
    home = _row().home_dir()
    assert home is not None  # the Kimi row names its home
    return home


def installed_path() -> Path:
    return kimi_home() / "plugins" / "installed.json"


def managed_root() -> Path:
    return kimi_home() / "plugins" / "managed"


def managed_dir(plugin_id: str) -> Path:
    """Where Kimi's own `/plugins install` would put the plugin."""
    return managed_root() / plugin_id


def versioned_dir(plugin_id: str, version: str) -> Path:
    """Where Probe puts one version of a plugin: a new folder per version, so an
    update never swaps files under a session still running the old one (Claude
    Code and Codex version their plugin folders the same way)."""
    return managed_root() / f"{plugin_id}@{version}"


#: How many versions of a plugin are always kept (the current one and the one
#: before), and how long any other version stays: a long Kimi session may still
#: run one that two updates have since replaced.
KEEP_VERSIONS = 2
KEEP_OLD_VERSIONS_SECONDS = 7 * 86400


def binary_available() -> bool:
    return shutil.which("kimi") is not None


def kimi_version() -> tuple[int, int, int] | None:
    """`kimi --version`, parsed; None when Kimi is missing or says nothing."""
    from probe.sdk.agent_session import parse_version

    binary = shutil.which("kimi")
    if binary is None:
        return None
    try:
        done = subprocess.run(  # noqa: S603 - fixed binary, no shell
            [binary, "--version"],
            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=VERSION_TIMEOUT_S, check=False,
            env={**os.environ, "KIMI_CODE_NO_AUTO_UPDATE": "1"},
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return parse_version((done.stdout or "").strip().splitlines()[-1] if (done.stdout or "").strip() else "")


def version_floor_problem() -> str | None:
    """Why this Kimi is too old for Probe, or None (also None when unknown)."""
    floor = _row().min_version
    current = kimi_version()
    if floor is None or current is None or current >= floor:
        return None
    want = ".".join(str(part) for part in floor)
    have = ".".join(str(part) for part in current)
    return f"Kimi Code {have} is older than {want}; run `kimi upgrade` (or `npm i -g @moonshot-ai/kimi-code`)"


def _manual_step(plugin_id: str) -> str:
    return (
        f"clone https://github.com/{MIRROR_REPO} and, inside Kimi Code, run: "
        f"/plugins install <clone>/plugins/{plugin_id}"
    )


@contextlib.contextmanager
def _locked():
    """One Probe writer of Kimi's plugin list at a time (two wizards, or an
    auto-update beside a wizard). Kimi itself writes it only on /plugins."""
    path = kimi_home() / "plugins" / ".probe-installed.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+") as handle:
        try:
            import fcntl  # noqa: PLC0415 -- POSIX; Windows runs unlocked

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        except (ImportError, OSError):
            pass
        yield


def _read_installed() -> tuple[dict | None, str | None]:
    """(document, None), or (None, why it must not be touched)."""
    path = installed_path()
    if not path.exists():
        return {"version": INSTALLED_VERSION, "plugins": []}, None
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, f"{path} is unreadable ({exc})"
    if not isinstance(doc, dict) or doc.get("version") != INSTALLED_VERSION or not isinstance(doc.get("plugins"), list):
        return None, f"{path} has a layout this Probe does not know (version {doc.get('version') if isinstance(doc, dict) else '?'})"
    return doc, None


def _write_installed(doc: dict) -> None:
    path = installed_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".installed-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(doc, indent=2) + "\n")
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _checkout_source() -> Path | None:
    """`<checkout>/agent` when this CLI runs from a research-os checkout."""
    here = Path(__file__).resolve()
    for ancestor in here.parents:
        candidate = ancestor / "plugins" / "probe-research" / MANIFEST
        if candidate.is_file() and (ancestor / "src" / "probe").is_dir():
            return ancestor
    return None


def _cleanup_download() -> None:
    if _DOWNLOADED is not None:
        shutil.rmtree(_DOWNLOADED.parent, ignore_errors=True)


def _download_mirror() -> Path:
    """The mirror's main branch, unpacked once per process (a folder holding
    `plugins/<id>/`). Raises OSError on any failure."""
    global _DOWNLOADED
    if _DOWNLOADED is not None and _DOWNLOADED.is_dir():
        return _DOWNLOADED
    scratch = Path(tempfile.mkdtemp(prefix="probe-kimi-plugins-"))
    try:
        _DOWNLOADED = _fetch_into(scratch)
    except BaseException:
        shutil.rmtree(scratch, ignore_errors=True)
        raise
    atexit.register(_cleanup_download)
    return _DOWNLOADED


def _fetch_into(scratch: Path) -> Path:
    from probe.sdk.tls import ssl_context

    try:
        with urllib.request.urlopen(  # noqa: S310 - fixed https URL
            MIRROR_TARBALL, timeout=DOWNLOAD_TIMEOUT_S, context=ssl_context()
        ) as response:
            data = response.read()
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            members = [m for m in archive.getmembers() if "/plugins/" in f"/{m.name}"]
            for member in members:
                # Refused outright, whatever the Python: links, absolute paths, `..`.
                if member.issym() or member.islnk() or Path(member.name).is_absolute() or ".." in Path(member.name).parts:
                    raise OSError(f"refusing archive member {member.name!r}")
            try:
                archive.extractall(scratch, members=members, filter="data")
            except TypeError:  # Python without extraction filters: checked above
                archive.extractall(scratch, members=members)  # noqa: S202
    except (EOFError, http.client.HTTPException, tarfile.TarError, ValueError) as exc:
        raise OSError(f"the mirror download failed: {type(exc).__name__}: {exc}") from exc
    roots = [p for p in scratch.iterdir() if p.is_dir()]
    if len(roots) != 1 or not (roots[0] / "plugins").is_dir():
        raise OSError("the mirror archive has no plugins/ folder")
    return roots[0]


def _source() -> tuple[Path, str]:
    """(folder holding plugins/<id>, how to name it as `originalSource`)."""
    override = (os.environ.get(SOURCE_ENV) or "").strip()
    if override:
        root = Path(override).expanduser().resolve()
        if not (root / "plugins").is_dir():
            raise OSError(f"{SOURCE_ENV}={root} has no plugins/ folder")
        return root, str(root / "plugins")
    checkout = _checkout_source()
    if checkout is not None:
        return checkout, str(checkout / "plugins")
    return _download_mirror(), f"https://github.com/{MIRROR_REPO}"


def _record_root(plugin_id: str) -> Path | None:
    doc, refused = _read_installed()
    if refused:
        return None
    for record in doc["plugins"]:
        if isinstance(record, dict) and record.get("id") == plugin_id and isinstance(record.get("root"), str):
            return Path(record["root"])
    return None


def plugin_version(plugin_id: str, root: Path | None = None) -> str | None:
    """The version of an installed (or source) Kimi plugin, from its manifest."""
    base = root if root is not None else (_record_root(plugin_id) or managed_dir(plugin_id))
    try:
        version = json.loads((base / MANIFEST).read_text(encoding="utf-8")).get("version")
    except (OSError, ValueError):
        return None
    return version if isinstance(version, str) else None


def _now() -> str:
    """Kimi's own timestamp spelling: `2026-10-05T03:24:02.408Z`."""
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _copy_plugin(source: Path, target: Path) -> None:
    """A complete copy of `source` at `target`. An existing `target` (the same
    version, installed before) is left as it is: version folders never change."""
    if (target / MANIFEST).is_file():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.with_name(f".{target.name}.staging-{os.getpid()}")
    shutil.rmtree(staging, ignore_errors=True)
    shutil.copytree(source, staging, ignore=shutil.ignore_patterns("__pycache__", "node_modules", "*.pyc"))
    shutil.rmtree(target, ignore_errors=True)
    os.replace(staging, target)
    os.utime(target)  # its install time (copytree copied the source's mtime)


def _prune_versions(plugin_id: str, keep: Path) -> None:
    """Drop all but the newest KEEP_VERSIONS version folders of a plugin."""
    def version_key(folder: Path) -> tuple:
        # Newest by version, not mtime: copytree copies the source's mtimes.
        parts = folder.name.rpartition("@")[2].split(".")
        return tuple(int(x) if x.isdigit() else -1 for x in parts)

    folders = sorted(
        (p for p in managed_root().glob(f"{plugin_id}@*") if p.is_dir() and p != keep),
        key=version_key,
        reverse=True,
    )
    cutoff = time.time() - KEEP_OLD_VERSIONS_SECONDS
    for old in folders[KEEP_VERSIONS - 1:]:
        if old.stat().st_mtime < cutoff:
            shutil.rmtree(old, ignore_errors=True)


def install_plugin(plugin_id: str) -> claude_cli.Result:
    """Install (or update in place) one Probe plugin into Kimi Code."""
    command = f"kimi /plugins install {plugin_id}"
    if plugin_id not in PLUGIN_IDS:
        return claude_cli.Result(ok=False, detail=f"{plugin_id!r} is not a Probe plugin", command=command)
    if not binary_available():
        return claude_cli.Result(ok=False, detail="`kimi` not found on PATH", reachable=False, command=command)
    too_old = version_floor_problem()
    if too_old:
        return claude_cli.Result(ok=False, detail=too_old, command=command)
    try:
        root, origin = _source()
        source = root / "plugins" / plugin_id
        version = plugin_version(plugin_id, source)
        if not version:
            return claude_cli.Result(
                ok=False, detail=f"{source} has no {MANIFEST} (the plugin predates Kimi Code support)", command=command
            )
        with _locked():
            doc, refused = _read_installed()
            if refused:
                return claude_cli.Result(ok=False, detail=f"{refused}; {_manual_step(plugin_id)}", command=command)
            target = versioned_dir(plugin_id, version)
            _copy_plugin(source, target)
            now = _now()
            previous = next(
                (p for p in doc["plugins"] if isinstance(p, dict) and p.get("id") == plugin_id), None
            )
            record = {
                **(previous or {}),  # keep fields a newer Kimi writes that Probe does not know
                "id": plugin_id,
                "root": str(target),
                "source": "local-path",
                "enabled": True,
                "installedAt": (previous or {}).get("installedAt") or now,
                "updatedAt": now,
                "originalSource": f"{origin}/{plugin_id}" if not origin.startswith("https://") else origin,
            }
            doc["plugins"] = [
                p for p in doc["plugins"] if not (isinstance(p, dict) and p.get("id") == plugin_id)
            ] + [record]
            _write_installed(doc)
            _prune_versions(plugin_id, target)
    except (OSError, ValueError) as exc:
        return claude_cli.Result(ok=False, detail=f"could not install {plugin_id}: {exc}", command=command)
    version = plugin_version(plugin_id) or "?"
    return claude_cli.Result(ok=True, detail=f"installed {plugin_id} {version} into Kimi Code", command=command)


def uninstall_plugin(plugin_id: str) -> claude_cli.Result:
    """Remove one Probe plugin from Kimi Code: its record and its copy only."""
    command = f"kimi /plugins remove {plugin_id}"
    if plugin_id not in PLUGIN_IDS:
        return claude_cli.Result(ok=False, detail=f"{plugin_id!r} is not a Probe plugin", command=command)
    try:
        with _locked():
            doc, refused = _read_installed()
            if refused:
                return claude_cli.Result(
                    ok=False, detail=f"{refused}; inside Kimi Code run: /plugins remove {plugin_id}", command=command
                )
            kept = [p for p in doc["plugins"] if not (isinstance(p, dict) and p.get("id") == plugin_id)]
            if len(kept) != len(doc["plugins"]):
                doc["plugins"] = kept
                _write_installed(doc)
            for folder in (managed_dir(plugin_id), *managed_root().glob(f"{plugin_id}@*")):
                if folder.is_dir() and folder.parent == managed_root():
                    shutil.rmtree(folder)
    except OSError as exc:
        return claude_cli.Result(ok=False, detail=f"could not remove {plugin_id}: {exc}", command=command)
    return claude_cli.Result(ok=True, detail=f"removed {plugin_id} from Kimi Code", command=command)


def list_plugins() -> claude_cli.Result:
    """One line per plugin Kimi Code has installed: `<id> <version> enabled|disabled`."""
    command = "kimi /plugins list"
    doc, refused = _read_installed()
    if refused:
        return claude_cli.Result(ok=False, detail=refused, command=command)
    lines = []
    for plugin in doc["plugins"]:
        if not isinstance(plugin, dict) or not isinstance(plugin.get("id"), str):
            continue
        root = plugin.get("root")
        version = plugin_version(plugin["id"], Path(root)) if isinstance(root, str) else None
        state = "enabled" if plugin.get("enabled") is not False else "disabled"
        if state == "enabled":
            lines.append(f"{plugin['id']} {version or '?'} {state}")
    return claude_cli.Result(ok=True, detail="\n".join(lines), command=command)


def refresh() -> claude_cli.Result:
    """Kimi has no catalog to refresh: every install copies current files."""
    return claude_cli.Result(ok=True, detail="Kimi Code installs from the mirror directly; nothing to refresh")
