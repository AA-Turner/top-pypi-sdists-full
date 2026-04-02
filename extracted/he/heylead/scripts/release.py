#!/usr/bin/env python3
"""HeyLead release script — bump version, generate changelog, commit & tag.

Usage:
    python scripts/release.py patch       # 0.9.19 → 0.9.20
    python scripts/release.py minor       # 0.9.19 → 0.10.0
    python scripts/release.py major       # 0.9.19 → 1.0.0
    python scripts/release.py 1.0.0       # explicit version
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ── Helpers ──────────────────────────────────────────


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


# ── Version ──────────────────────────────────────────


def current_version() -> tuple[int, int, int]:
    text = (ROOT / "pyproject.toml").read_text()
    m = re.search(r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"', text, re.MULTILINE)
    if not m:
        sys.exit("Cannot parse version from pyproject.toml")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def resolve_version(arg: str) -> str:
    if re.fullmatch(r"\d+\.\d+\.\d+", arg):
        return arg
    major, minor, patch = current_version()
    if arg == "patch":
        return f"{major}.{minor}.{patch + 1}"
    if arg == "minor":
        return f"{major}.{minor + 1}.0"
    if arg == "major":
        return f"{major + 1}.0.0"
    sys.exit(f"Invalid argument: {arg!r}. Use X.Y.Z, patch, minor, or major.")


# ── Preconditions ────────────────────────────────────


def check_preconditions():
    r = run(["git", "rev-parse", "--git-dir"])
    if r.returncode != 0:
        sys.exit("Not a git repository.")
    r = run(["git", "status", "--porcelain"])
    if r.stdout.strip():
        sys.exit("Working tree is dirty. Commit or stash changes first.")


# ── Changelog generation ────────────────────────────


def last_tag() -> str | None:
    r = run(["git", "describe", "--tags", "--abbrev=0"])
    return r.stdout.strip() if r.returncode == 0 else None


def collect_commits(since_tag: str | None) -> list[str]:
    if since_tag:
        r = run(["git", "log", f"{since_tag}..HEAD", "--format=%s"])
    else:
        r = run(["git", "log", "--format=%s"])
    lines = r.stdout.strip().splitlines() if r.stdout.strip() else []
    skip = re.compile(r"^chore:", re.IGNORECASE)
    return [line for line in lines if not skip.match(line)]


def format_changelog(version: str, commits: list[str]) -> str:
    today = date.today().isoformat()
    lines = [f"## v{version} ({today})"]
    for msg in commits:
        m = re.match(r"^(feat|fix|refactor|docs|test|perf|ci):\s*", msg, re.IGNORECASE)
        if m:
            prefix_type = m.group(1).lower()
            body = msg[m.end():]
        else:
            prefix_type = ""
            body = msg
        # Strip trailing version annotations like (v0.9.19)
        body = re.sub(r"\s*\(v[\d.]+\)\s*$", "", body)
        if not body:
            continue
        if prefix_type == "feat":
            lines.append(f"- New: {body}")
        elif prefix_type == "fix":
            lines.append(f"- Fix: {body}")
        else:
            lines.append(f"- {body}")
    if len(lines) == 1:
        lines.append("- Release version bump")
    return "\n".join(lines)


# ── File updaters ────────────────────────────────────


def update_pyproject(ver: str):
    p = ROOT / "pyproject.toml"
    text = p.read_text()
    text = re.sub(
        r'^(version\s*=\s*)"[^"]+"',
        rf'\g<1>"{ver}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    p.write_text(text)


def update_init(ver: str):
    p = ROOT / "src" / "heylead" / "__init__.py"
    text = p.read_text()
    text = re.sub(
        r'^(__version__\s*=\s*)"[^"]+"',
        rf'\g<1>"{ver}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    p.write_text(text)


def update_clawhub(ver: str):
    p = ROOT / "clawhub.json"
    data = json.loads(p.read_text())
    data["version"] = ver
    p.write_text(json.dumps(data, indent=2) + "\n")


def update_server_json(ver: str):
    p = ROOT / "server.json"
    data = json.loads(p.read_text())
    data["version"] = ver
    for pkg in data.get("packages", []):
        pkg["version"] = ver
    p.write_text(json.dumps(data, indent=2) + "\n")


def update_changelog(entry: str):
    p = ROOT / "src" / "heylead" / "server.py"
    text = p.read_text()
    marker = "# HeyLead Changelog"
    idx = text.index(marker)
    eol = text.index("\n", idx)
    # Insert new entry after the header line
    text = text[: eol + 1] + f"\n{entry}\n" + text[eol + 1:]
    p.write_text(text)


# ── Git operations ───────────────────────────────────


def show_diff_and_confirm() -> bool:
    r = run(["git", "diff"])
    print(r.stdout)
    answer = input("\nLooks good? Commit and tag? [y/N] ").strip().lower()
    if answer != "y":
        print("Aborted. Reverting changes...")
        run(["git", "checkout", "."])
        return False
    return True


def commit_and_tag(ver: str):
    files = [
        "pyproject.toml",
        "src/heylead/__init__.py",
        "clawhub.json",
        "server.json",
        "src/heylead/server.py",
    ]
    run(["git", "add"] + files)
    r = run(["git", "commit", "-m", f"chore: release v{ver}"])
    if r.returncode != 0:
        sys.exit(f"Commit failed:\n{r.stderr}")
    r = run(["git", "tag", f"v{ver}"])
    if r.returncode != 0:
        sys.exit(f"Tag failed:\n{r.stderr}")
    print(f"\n✓ Committed and tagged v{ver}")
    print(f"\nNext steps:")
    print(f"  git push && git push --tags")
    print(f"  Then create a GitHub Release to trigger PyPI publish.")


# ── Main ─────────────────────────────────────────────


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: python {sys.argv[0]} <version|patch|minor|major>")

    check_preconditions()

    ver = resolve_version(sys.argv[1])
    old = ".".join(str(x) for x in current_version())
    print(f"Releasing: v{old} → v{ver}\n")

    tag = last_tag()
    commits = collect_commits(tag)
    print(f"{len(commits)} commits since {tag or 'beginning'}:")
    for c in commits:
        print(f"  • {c}")

    entry = format_changelog(ver, commits)
    print(f"\nChangelog entry:\n{entry}\n")

    update_pyproject(ver)
    update_init(ver)
    update_clawhub(ver)
    update_server_json(ver)
    update_changelog(entry)
    print("Updated 5 files.\n")

    if show_diff_and_confirm():
        commit_and_tag(ver)


if __name__ == "__main__":
    main()
