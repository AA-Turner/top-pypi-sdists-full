from __future__ import annotations

"""
Simple clone-and-merge of doc sources into a hub.

For each [[source]] in sources.toml this:
  1. clones (or updates) the source repo,
  2. copies its docs/ → <hub>/docs/<path>/,
  3. reads the source's OWN zensical.toml nav and replaces the matching
     empty placeholder  {"<nav>" = []}  in the hub's zensical.toml.

Deliberately minimal — one level deep, no recursion.
Designed to run on a CI runner or locally (uses GITLAB_TOKEN / CI_JOB_TOKEN
for auth when cloning private repos over HTTPS).

When running on a CI runner (CI env var set) it also stamps each imported
page's frontmatter from the source repo:
  - source_repo_url / source_default_branch / source_file_path (edit/view buttons)
  - git_revision_date_cern / _date_only / _author_cern / git_revision_date (last edit)
  - git_commit_count, git_unique_contributors, git_recent_authors
prepare_directory_pages falls back to these fields for imported pages (which
have no history in the hub repo). Skipped locally so it never rewrites files
in your working tree.

sources.toml entry:
    [[source]]
    path   = "egamma"                                   # placed at docs/egamma/
    gitlab = "https://gitlab.cern.ch/.../egamma"         # repo to clone
    nav    = "EGamma"                                    # hub placeholder {"EGamma" = []} to fill (optional)
                                                         #   or a key path: nav = ["EGamma", "Calibration"]
                                                         #   fills {"Calibration" = []} inside the {"EGamma" = [...]} section
    branch = "main"                                      # optional, defaults to the repo's default branch

Usage:
    python -m atlasdocs_theme.scripts.import_sources [hub_dir]
Pixi:
    pixi run import-sources
"""

import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

SOURCES_TOML  = "sources.toml"
ZENSICAL_TOML = "zensical.toml"
MKDOCS_YML    = "mkdocs.yml"
CACHE_DIR     = ".sources"          # gitignored clone cache
EXCLUDE       = {"__pycache__", ".DS_Store"}
CLONE_TIMEOUT = 600                 # seconds; guards against a hung clone


# ── sources.toml ────────────────────────────────────────────────────────────────

def load_sources(path: Path) -> list[dict]:
    with open(path, "rb") as f:
        data = tomllib.load(f)
    sources = data.get("source", [])
    for s in sources:
        if not s.get("path") or not s.get("gitlab"):
            raise ValueError(f"Each [[source]] needs 'path' and 'gitlab': {s!r}")
    return sources


# ── git ─────────────────────────────────────────────────────────────────────────

def _auth_url(url: str) -> str:
    """Inject CI/local credentials into an HTTPS GitLab URL when available."""
    if not url.startswith("https://"):
        return url
    if token := os.environ.get("GITLAB_TOKEN"):
        return url.replace("https://", f"https://oauth2:{token}@", 1)
    if token := os.environ.get("CI_JOB_TOKEN"):
        return url.replace("https://", f"https://gitlab-ci-token:{token}@", 1)
    return url


def _on_runner() -> bool:
    """True when running in CI (GitLab/GitHub/etc. set CI=true)."""
    return bool(os.environ.get("CI"))


def detect_default_branch(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "symbolic-ref", "--short", "HEAD"],
        capture_output=True, text=True,
    )
    return result.stdout.strip() or "main"


# GIT_TERMINAL_PROMPT=0 → fail fast instead of blocking on a credential prompt
# when a private repo is unreachable (no token).
GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"}


def _git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, env=GIT_ENV, timeout=CLONE_TIMEOUT
    )


def sync_repo(url: str, dest: Path, branch: str | None) -> bool:
    """Clone a repo into dest with full history but only the docs/ tree checked out.

    Blobless clone keeps the full commit graph (needed to stamp each page's
    last-revision date/author) while a docs/-only sparse checkout avoids
    materialising a large code repo's working tree — fast and light on disk.
    """
    auth = _auth_url(url)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    clone = ["-c", "credential.helper=", "clone", "--filter=blob:none", "--no-checkout"]
    if branch:
        clone += ["--branch", branch]
    clone += [auth, str(dest)]
    try:
        r = _git(clone)
        if r.returncode != 0:
            print(f"  WARNING: clone failed — {r.stderr.strip()}")
            return False
        _git(["-C", str(dest), "sparse-checkout", "set", "docs"])
        co = _git(["-C", str(dest), "checkout"])
        if co.returncode != 0:
            print(f"  WARNING: checkout failed — {co.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  WARNING: clone timed out after {CLONE_TIMEOUT}s")
        return False
    return True


# ── docs ──────────────────────────────────────────────────────────────────────

def copy_docs(repo: Path, hub: Path, rel_path: str) -> Path | None:
    """Copy <repo>/docs → <hub>/docs/<rel_path>/. Returns the target dir."""
    docs_src = repo / "docs"
    if not docs_src.is_dir():
        print(f"  WARNING: {docs_src} not found, skipping docs copy")
        return None
    target = hub / "docs" / rel_path.strip("/")
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(docs_src, target, ignore=shutil.ignore_patterns(*EXCLUDE))
    print(f"  copied docs/ → docs/{rel_path.strip('/')}/")
    return target


# ── repo-pointing frontmatter (CI runner only) ──────────────────────────────────

def _clean_repo_url(url: str) -> str:
    return url.removesuffix(".git").rstrip("/")


def repo_history(repo: Path) -> dict[str, dict]:
    """Map docs-relative path → git stats from the source repo.

    Each value: {date, author, count, authors} where `date`/`author` are the
    most recent commit, `count` is the number of commits touching the file, and
    `authors` is the unique contributor list in recency order (name, email).
    """
    r = _git(["-C", str(repo), "log", "--name-only",
              "--pretty=format:\x01%cI\x01%an\x01%ae", "--", "docs/"])
    hist: dict[str, dict] = {}
    if r.returncode != 0:
        return hist
    cur: list[str] | None = None
    for line in r.stdout.splitlines():
        if line.startswith("\x01"):
            parts = line.split("\x01")          # ['', date, name, email]
            cur = parts[1:4] if len(parts) >= 4 else None
        elif cur and line.startswith("docs/"):
            rel = line[len("docs/"):].strip()
            date, name, email = cur
            rec = hist.get(rel)
            if rec is None:                      # newest-first → first sets date/author
                rec = {"date": date, "author": name, "count": 0, "authors": [], "_seen": set()}
                hist[rel] = rec
            rec["count"] += 1
            key = email.lower()
            if key not in rec["_seen"]:
                rec["_seen"].add(key)
                rec["authors"].append((name, email))
    for rec in hist.values():
        rec.pop("_seen", None)
    return hist


def _yaml_str(s: str) -> str:
    return s.replace('"', "'")


def _stamp_one(md: Path, file_rel: str, team: str | None = None,
               repo_url: str | None = None, branch: str | None = None,
               git: dict | None = None) -> None:
    """Add team_name / source_* / git_* to YAML frontmatter — only keys not
    already present, so a source that sets its own values wins."""
    text = md.read_text(encoding="utf-8", errors="replace")
    head = text.split("\n---", 1)[0] if text.startswith("---") else ""

    pairs: list[tuple[str, str]] = []
    if team:
        pairs.append(("team_name", f'"{_yaml_str(team)}"'))           # Team (first column)
    if repo_url:
        pairs += [
            ("source_repo_url", f'"{repo_url}"'),
            ("source_default_branch", f'"{branch}"'),
            ("source_file_path", f'"{file_rel}"'),
        ]
    if git:
        iso = git["date"]
        recent = ", ".join(f'"{_yaml_str(n)} <{_yaml_str(e)}>"' for n, e in git["authors"][:2])
        pairs += [
            ("git_revision_date_cern", f'"{iso[:16].replace("T", " ")}"'),   # Last Edit (display)
            ("git_revision_date_only", f'"{iso[:10]}"'),
            ("git_revision_author_cern", f'"{_yaml_str(git["author"])}"'),
            ("git_revision_date", f'"{iso}"'),                               # full ISO (directory recency)
            ("git_commit_count", str(git["count"])),                        # Commits
            ("git_unique_contributors", str(len(git["authors"]))),          # Authors
            ("git_recent_authors", f'[{recent}]'),                          # Recent Authors
        ]

    new = [f"{k}: {v}" for k, v in pairs if not re.search(rf"(?m)^{re.escape(k)}\s*:", head)]
    if not new:
        return
    block = "\n".join(new) + "\n"
    if text.startswith("---"):
        nl = text.find("\n")
        md.write_text(text[: nl + 1] + block + text[nl + 1 :], encoding="utf-8")
    else:
        md.write_text(f"---\n{block}---\n\n{text}", encoding="utf-8")


def stamp_sources(target: Path, repo: Path, repo_url: str, branch: str | None,
                  team: str | None = None, with_git: bool = True) -> int:
    """Stamp imported .md files. team_name is always written; source_*/git_* only
    when with_git (CI runner). Returns count of files visited."""
    repo_url = _clean_repo_url(repo_url) if (repo_url and with_git) else None
    hist = repo_history(repo) if with_git else {}
    count = 0
    for md in target.rglob("*.md"):
        rel = md.relative_to(target).as_posix()
        _stamp_one(md, f"docs/{rel}", team=team,
                   repo_url=repo_url, branch=branch,
                   git=hist.get(rel) if with_git else None)
        count += 1
    return count


# ── nav ─────────────────────────────────────────────────────────────────────────

def _prefix(p: str, base: str) -> str:
    if p.startswith(("http://", "https://", "/")):
        return p
    return f"{base.strip('/')}/{p.lstrip('/')}"


def _render_nav(items: list, base: str, indent: int) -> list[str]:
    pad = " " * indent
    lines: list[str] = []
    for item in items:
        if isinstance(item, str):
            lines.append(f'{pad}"{_prefix(item, base)}",')
        elif isinstance(item, dict):
            for title, value in item.items():
                safe = title.replace('"', '\\"')
                if isinstance(value, str):
                    lines.append(f'{pad}{{ "{safe}" = "{_prefix(value, base)}" }},')
                elif isinstance(value, list):
                    lines.append(f'{pad}{{ "{safe}" = [')
                    lines.extend(_render_nav(value, base, indent + 4))
                    lines.append(f"{pad}] }},")
    return lines


def _load_zensical_nav(repo: Path) -> list | None:
    cfg = repo / ZENSICAL_TOML
    if not cfg.is_file():
        return None
    with open(cfg, "rb") as f:
        data = tomllib.load(f)
    return data.get("nav") or data.get("project", {}).get("nav")


def _load_mkdocs_nav(repo: Path) -> list | None:
    """Read nav: from mkdocs.yml, ignoring unknown YAML tags (!ENV, !!python/...)."""
    yml = repo / MKDOCS_YML
    if not yml.is_file():
        return None
    try:
        import yaml
    except ImportError:
        print("  note: PyYAML not installed — cannot read mkdocs.yml nav")
        return None

    class _Loader(yaml.SafeLoader):
        pass

    def _ignore(loader, _suffix, node):
        if isinstance(node, yaml.ScalarNode):
            return loader.construct_scalar(node)
        if isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node)
        if isinstance(node, yaml.MappingNode):
            return loader.construct_mapping(node)
        return None

    _Loader.add_multi_constructor("", _ignore)
    try:
        data = yaml.load(yml.read_text(encoding="utf-8"), Loader=_Loader)
    except Exception as exc:
        print(f"  WARNING: could not parse mkdocs.yml — {exc}")
        return None
    return data.get("nav") if isinstance(data, dict) else None


def _read_source_nav(repo: Path) -> list | None:
    """Nav from the source's own zensical.toml, falling back to mkdocs.yml."""
    if nav := _load_zensical_nav(repo):
        return nav
    if nav := _load_mkdocs_nav(repo):
        print("  nav from mkdocs.yml")
        return nav
    print(f"  note: no {ZENSICAL_TOML}/{MKDOCS_YML} nav found, skipping nav merge")
    return None


def replace_placeholder(content: str, key: str, nav: list, base: str) -> str:
    """Replace an empty  {"key" = []}  placeholder with the source's nav."""
    pattern = re.compile(
        r'^(?P<indent>[ \t]*)\{\s*"?' + re.escape(key) + r'"?\s*=\s*\[\s*\]\s*\},?',
        re.MULTILINE,
    )

    def repl(m: re.Match) -> str:
        indent = m.group("indent")
        inner = "\n".join(_render_nav(nav, base, len(indent) + 4))
        return f'{indent}{{ "{key}" = [\n{inner}\n{indent}] }},'

    patched, n = pattern.subn(repl, content)
    if n == 0:
        print(f'  WARNING: placeholder {{"{key}" = []}} not found in hub {ZENSICAL_TOML}')
    else:
        print(f'  filled nav placeholder "{key}"')
    return patched


def _array_inner_span(text: str, key: str) -> tuple[int, int] | None:
    """Indices (start, end) of the inner content of  {"key" = [ ... ]}  in text."""
    m = re.search(r'\{\s*"?' + re.escape(key) + r'"?\s*=\s*\[', text)
    if not m:
        return None
    depth, i = 1, m.end()
    while i < len(text) and depth:
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
        i += 1
    return (m.end(), i - 1) if depth == 0 else None


def fill_nav(content: str, keys: list[str], nav: list, base: str) -> str:
    """Fill an empty placeholder addressed by a key path.

    keys == ["Calibration"]            → fill {"Calibration" = []} anywhere
    keys == ["EGamma", "Calibration"]  → fill {"Calibration" = []} *inside* the
                                          {"EGamma" = [ ... ]} section only
    """
    if len(keys) == 1:
        return replace_placeholder(content, keys[0], nav, base)
    span = _array_inner_span(content, keys[0])
    if span is None:
        print(f'  WARNING: nav section "{keys[0]}" not found in hub {ZENSICAL_TOML}')
        return content
    s, e = span
    return content[:s] + fill_nav(content[s:e], keys[1:], nav, base) + content[e:]


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    hub = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

    sources_file = hub / SOURCES_TOML
    if not sources_file.is_file():
        print(f"Error: {SOURCES_TOML} not found in {hub}", file=sys.stderr)
        sys.exit(1)

    try:
        sources = load_sources(sources_file)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    hub_toml = hub / ZENSICAL_TOML
    content = hub_toml.read_text(encoding="utf-8") if hub_toml.is_file() else None

    cache = hub / CACHE_DIR
    cache.mkdir(exist_ok=True)

    stamp = _on_runner()
    print(f"Repo-pointing frontmatter: {'ON (CI runner)' if stamp else 'OFF (local)'}")

    imported = 0
    for s in sources:
        path, url = s["path"], s["gitlab"]
        print(f"\n→ {path}  ({url})")

        repo = cache / re.sub(r"[^A-Za-z0-9_.-]", "_", path.strip("/"))
        if not sync_repo(url, repo, s.get("branch")):
            print(f"  SKIPPED {path}")
            continue

        target = copy_docs(repo, hub, path)
        if target is None:
            continue
        imported += 1

        team = s.get("team") or s.get("name")
        if team or stamp:
            branch = (s.get("branch") or detect_default_branch(repo)) if stamp else None
            n = stamp_sources(target, repo, url, branch, team=team, with_git=stamp)
            note = ", ".join(([f"team='{team}'"] if team else [])
                             + ([f"git @ {branch}"] if stamp else []))
            print(f"  stamped {n} page(s)" + (f" ({note})" if note else ""))

        nav_key = s.get("nav")
        if nav_key and content is not None:
            nav = _read_source_nav(repo)
            if nav:
                keys = nav_key if isinstance(nav_key, list) else [nav_key]
                content = fill_nav(content, [str(k) for k in keys], nav, path)

    if content is not None:
        hub_toml.write_text(content, encoding="utf-8")
        print(f"\nUpdated {hub_toml.name}")

    print(f"Done. Imported {imported} source(s).")


if __name__ == "__main__":
    main()
