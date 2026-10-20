#!/app/.venv/bin/python
"""What a person would miss if an upgrade lost it: one JSON snapshot of this machine.

The carry-over check (aidream ``scripts/check_cloud_computer_carryover.py``) runs
this on a machine before a save-and-stop and again after the wake on the new
build, and requires the two to match (owner ruling 16, "Upgrades keep
everything"). Facts only; the comparison and its explicit list of volatile
fields live in aidream ``services/cloud_browser/carryover.py``.

    cloud-computer-carryover snapshot [--auth-domain example.com ...]

Values are counts, names and hashes, never cookie values or file contents.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

#: The image's one user home; ``--home`` points a test at another tree.
HOME = Path("/home/browser-worker")
SHARE = Path("/usr/local/share/cloud-computer")
#: Home paths that are caches or session plumbing, never the person's things.
HOME_SKIP = (
    ".cache",
    ".matrx/profiles",  # Chrome: compared on its own below
    ".matrx/system",  # software: compared on its own below
    ".local/share/recently-used.xbel",
    ".Xauthority",
    ".dbus",
    ".pki/nssdb/pkcs11.txt",
    ".config/pulse",
)
#: Larger files are compared by size only (hashing gigabytes on EFS is slow).
HASH_LIMIT_BYTES = 64 * 1024 * 1024
DESKTOP_FILES = (
    ".config/openbox/rc.xml",
    ".config/tint2/tint2rc",
    ".config/pcmanfm/cloud-computer/desktop-items-0.conf",
    ".config/pcmanfm/cloud-computer/pcmanfm.conf",
    ".config/libfm/libfm.conf",
    ".config/lxterminal/lxterminal.conf",
    ".config/gtk-3.0/settings.ini",
)
CHROME_BINARIES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _json_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def _skipped(rel: str) -> bool:
    return any(rel == s or rel.startswith(s + "/") for s in HOME_SKIP)


def home_manifest() -> dict[str, str]:
    out: dict[str, str] = {}
    for root, dirs, files in os.walk(HOME):
        rel_root = os.path.relpath(root, HOME)
        rel_root = "" if rel_root == "." else rel_root
        dirs[:] = [d for d in dirs if not _skipped(os.path.join(rel_root, d))]
        for name in files:
            rel = os.path.join(rel_root, name)
            if _skipped(rel):
                continue
            path = Path(root) / name
            try:
                if path.is_symlink():
                    out[rel] = "link:" + os.readlink(path)
                    continue
                size = path.stat().st_size
                out[rel] = f"size:{size}" if size > HASH_LIMIT_BYTES else _sha(path)
            except OSError as exc:
                out[rel] = f"unreadable:{exc.errno}"
    return out


def _user_data_dirs() -> list[Path]:
    seen: list[Path] = []
    for base in (Path("/profiles"), HOME / ".matrx/profiles"):
        if not base.exists():
            continue
        for candidate in sorted(base.iterdir()):
            real = candidate.resolve()
            if (real / "Default").is_dir() and real not in seen:
                seen.append(real)
    return seen


def _cookies(default: Path, auth_domains: list[str]) -> dict[str, object]:
    db = default / "Cookies"
    if not db.exists():
        db = default / "Network" / "Cookies"
    if not db.exists():
        return {"present": False}
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "Cookies"
        shutil.copy2(db, copy)
        for suffix in ("-wal", "-journal"):
            side = Path(str(db) + suffix)
            if side.exists():
                shutil.copy2(side, Path(str(copy) + suffix))
        con = sqlite3.connect(f"file:{copy}?mode=ro", uri=True)
        try:
            rows = con.execute(
                "select host_key, name, has_expires, expires_utc from cookies"
            ).fetchall()
        finally:
            con.close()
    per_domain: dict[str, int] = {}
    persistent: dict[str, int] = {}
    names: dict[str, list[str]] = {}
    for host, name, has_expires, _expires in rows:
        domain = host.lstrip(".")
        per_domain[domain] = per_domain.get(domain, 0) + 1
        if has_expires:
            persistent[domain] = persistent.get(domain, 0) + 1
        for wanted in auth_domains:
            if domain == wanted or domain.endswith("." + wanted):
                names.setdefault(wanted, []).append(name)
    return {
        "present": True,
        "total": len(rows),
        "persistent_by_domain": dict(sorted(persistent.items())),
        "by_domain": dict(sorted(per_domain.items())),
        "auth_cookie_names": {d: sorted(set(names.get(d, []))) for d in auth_domains},
    }


def _bookmarks(default: Path) -> dict[str, object]:
    path = default / "Bookmarks"
    if not path.exists():
        return {"present": False, "count": 0}
    data = json.loads(path.read_text())
    items: list[list[str]] = []

    def walk(node: dict, trail: str) -> None:
        if node.get("type") == "url":
            items.append([trail, node.get("name", ""), node.get("url", "")])
        for child in node.get("children") or []:
            walk(child, f"{trail}/{node.get('name', '')}")

    for key, root in (data.get("roots") or {}).items():
        if isinstance(root, dict):
            walk(root, key)
    items.sort()
    return {"present": True, "count": len(items), "sha256": _json_sha(items)}


#: Preferences keys Chrome rewrites on every launch (explicit, reviewed).
VOLATILE_PREFERENCE_KEYS = (
    "profile.exit_type",
    "profile.exited_cleanly",
    "profile.last_engagement_time",
    "session",
    "sessions",
    "browser.window_placement",
    "protection",
    "updateclientdata",
    "gcm",
    "invalidation",
    "media.engagement",
    "optimization_guide",
    "segmentation_platform",
    "net.network_qualities",
    "variations_seed",
    "web_apps.last_preinstall_synchronize_version",
    "extensions.last_chrome_version",
    "in_product_help",
    "privacy_sandbox",
    "signin.accounts_metadata_dict",
    "profile.content_settings.exceptions.site_engagement",
    "profile.content_settings.exceptions.media_engagement",
    "profile.content_settings.exceptions.app_banner",
    "profile.content_settings.exceptions.client_hints",
    "profile.content_settings.exceptions.cookie_controls_metadata",
    "profile.content_settings.exceptions.permission_autoblocking_data",
    "profile.content_settings.exceptions.http_allowed",
    "account_tracker_service_last_update",
    "countryid_at_install",
    "default_search_provider_data.template_url_data.last_modified",
)


def _drop(prefs: dict, dotted: str) -> None:
    parts = dotted.split(".")
    node = prefs
    for part in parts[:-1]:
        node = node.get(part) if isinstance(node, dict) else None
        if not isinstance(node, dict):
            return
    node.pop(parts[-1], None)


def _extensions(user_data: Path, default: Path) -> list[str]:
    ids: set[str] = set()
    ext_dir = default / "Extensions"
    if ext_dir.is_dir():
        ids.update(p.name for p in ext_dir.iterdir() if p.is_dir() and len(p.name) == 32)
    for name in ("Secure Preferences", "Preferences"):
        path = default / name
        if path.exists():
            try:
                settings = (json.loads(path.read_text()).get("extensions") or {}).get("settings") or {}
            except ValueError:
                continue
            for ext_id, value in settings.items():
                # location 5 = component (Chrome's own, changes with the build).
                if isinstance(value, dict) and value.get("location") not in (5, 10):
                    ids.add(ext_id)
    return sorted(ids)


#: Fields Chrome stamps on a site permission each visit (not the person's choice).
CONTENT_SETTING_METADATA = ("last_modified", "last_visit", "expiration", "lifetime", "last_used")


def preference_map(prefs: dict) -> dict[str, str]:
    """``dotted.key`` (up to three levels) -> short hash. Site permissions keep
    only the site and its setting, without the per-visit stamps."""
    out: dict[str, str] = {}
    exceptions = ((prefs.get("profile") or {}).get("content_settings") or {}).get("exceptions") or {}
    for kind, sites in exceptions.items():
        if isinstance(sites, dict):
            kept = {
                site: {k: v for k, v in value.items() if k not in CONTENT_SETTING_METADATA}
                if isinstance(value, dict) else value
                for site, value in sites.items()
            }
            out[f"profile.content_settings.exceptions.{kind}"] = _json_sha(kept)[:16]

    def walk(node: object, key: str, depth: int) -> None:
        if key == "profile.content_settings.exceptions" or key == "extensions":
            return
        if isinstance(node, dict) and depth < 3 and node:
            for k, v in node.items():
                walk(v, f"{key}.{k}" if key else k, depth + 1)
        else:
            out[key] = _json_sha(node)[:16]

    walk(prefs, "", 0)
    return out


def chrome_profiles(auth_domains: list[str]) -> list[dict[str, object]]:
    out = []
    for user_data in _user_data_dirs():
        default = user_data / "Default"
        prefs_path = default / "Preferences"
        prefs_sha = None
        prefs_map: dict[str, str] = {}
        if prefs_path.exists():
            try:
                prefs = json.loads(prefs_path.read_text())
                for key in VOLATILE_PREFERENCE_KEYS:
                    _drop(prefs, key)
                prefs.pop("extensions", None)  # compared as the extension list
                prefs_sha = _json_sha(prefs)
                prefs_map = preference_map(json.loads(prefs_path.read_text()))
            except ValueError:
                prefs_sha = "unparseable"
        last_version = user_data / "Last Version"
        out.append(
            {
                "profile": user_data.name,
                "last_version": last_version.read_text().strip() if last_version.exists() else None,
                "cookies": _cookies(default, auth_domains),
                "extensions": _extensions(user_data, default),
                "bookmarks": _bookmarks(default),
                "preferences_sha256": prefs_sha,
                # Per-setting hashes: the check names WHICH setting changed and
                # holds the one list of settings Chrome rewrites on its own.
                "preferences": prefs_map,
            }
        )
    return out


def chrome_binary_version() -> str | None:
    for name in CHROME_BINARIES:
        path = shutil.which(name)
        if path:
            try:
                text = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=20).stdout
            except (OSError, subprocess.SubprocessError):
                continue
            words = [w for w in text.split() if w[:1].isdigit()]
            if words:
                return words[0]
    return None


def software() -> dict[str, object]:
    installed = subprocess.run(
        ["dpkg-query", "-W", "-f", "${Package}\t${db:Status-Abbrev}\n"], capture_output=True, text=True
    ).stdout
    packages = sorted(line.split("\t")[0] for line in installed.splitlines() if "\tii" in line)
    image = SHARE / "image-packages.txt"
    image_set = set(image.read_text().split()) if image.exists() else set()
    manual = subprocess.run(["apt-mark", "showmanual"], capture_output=True, text=True).stdout.split()
    files_txt = HOME / ".matrx/system/files.txt"
    recorded_files = files_txt.read_text().split("\n") if files_txt.exists() else []
    present_files = sorted(f for f in recorded_files if f and os.path.lexists(f))
    status = Path("/run/cloud-computer/software.json")
    return {
        "installed_packages": packages,
        "person_packages": sorted(set(manual) - image_set),
        "person_files_present": present_files,
        "replay": json.loads(status.read_text()) if status.exists() else None,
    }


def desktop() -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    for rel in DESKTOP_FILES:
        path = HOME / rel
        out[rel] = _sha(path) if path.is_file() else None
    return out


def snapshot(auth_domains: list[str]) -> dict[str, object]:
    build = Path("/usr/local/share/cloud-computer/build")
    return {
        "build": build.read_text().strip() if build.exists() else None,
        "chrome_binary_version": chrome_binary_version(),
        "chrome_profiles": chrome_profiles(auth_domains),
        "home": home_manifest(),
        "desktop": desktop(),
        "software": software(),
    }


def main() -> int:
    global HOME
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["snapshot"])
    ap.add_argument("--auth-domain", action="append", default=[])
    ap.add_argument("--home", default=str(HOME))
    args = ap.parse_args()
    HOME = Path(args.home)
    json.dump(snapshot(args.auth_domain), sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
