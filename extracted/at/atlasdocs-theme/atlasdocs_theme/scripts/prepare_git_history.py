"""Pre-cache git commit history for all docs/ files.

Reads the existing .git_history_cache.json (source-repo histories written by
import_docs), runs the hub's git log, merges the two, and writes the result
back to .git_history_cache.json.

When running on a CI runner (CI env var set), also stamps every docs/ markdown
file with two frontmatter fields as placeholders until Zensical supports them
natively:

    git_revision_date_cern:   YYYY-MM-DD HH:MM
    git_revision_author_cern: FirstName LastName

Run after combine-docs so that the complete merged history is available to
directory-page generation and the build plugin.

Usage:
    python -m atlasdocs_theme.scripts.prepare_git_history [hub_dir]
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from .fetch_git_history import DEFAULT_CACHE_FILE, LocalGitHistoryProvider

# ── Feature flag ───────────────────────────────────────────────────────────────
# Placeholder: inject git_revision_date_cern / git_revision_author_cern into
# every docs/ markdown file on CI runners.
#
# TO DISABLE: set False + bump theme version. Downstream sites get the change
# by updating their version pin — no CI or pixi edits needed.
#
# TO REMOVE ENTIRELY: when Zensical provides native git-revision frontmatter,
# delete this flag and the entire "Frontmatter injection" section below.
INJECT_GIT_FRONTMATTER: bool = True

# ── Frontmatter injection ──────────────────────────────────────────────────────

def _fmt_revision_date(iso_date: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


def _inject_file(path: Path, rev_date: str, rev_author: str) -> bool:
    """Insert/update git_revision_date_cern and git_revision_author_cern in-place.
    Returns True if the file was rewritten."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False

    new_lines = [
        f'git_revision_date_cern: "{rev_date}"',
        f'git_revision_author_cern: "{rev_author}"',
    ]

    if text.startswith("---"):
        # Locate closing fence — must start at column 0 on its own line
        end = text.find("\n---", 3)
        if end == -1:
            return False
        fm_body = text[3:end]          # between the two ---
        tail    = text[end:]           # \n--- + rest of file

        changed = False
        for line in new_lines:
            key = line.split(":")[0]
            pat = re.compile(rf"^{re.escape(key)}\s*:.*$", re.MULTILINE)
            if pat.search(fm_body):
                new_body = pat.sub(line, fm_body)
                if new_body != fm_body:
                    fm_body = new_body
                    changed = True
            else:
                fm_body = fm_body.rstrip("\n") + "\n" + line
                changed = True

        if not changed:
            return False
        new_text = "---" + fm_body + tail
    else:
        # No frontmatter — prepend a minimal block
        new_text = "---\n" + "\n".join(new_lines) + "\n---\n" + text

    try:
        path.write_text(new_text, encoding="utf-8")
        return True
    except Exception:
        return False


def inject_git_frontmatter(commit_map: dict, docs_path: Path) -> int:
    """Stamp every docs/ markdown file with git revision frontmatter from commit_map."""
    count = 0
    for md_file in sorted(docs_path.rglob("*.md")):
        try:
            rel = str(md_file.relative_to(docs_path)).replace("\\", "/")
        except ValueError:
            continue

        commits = commit_map.get(rel, [])
        if not commits:
            # No hub history for this file — e.g. pages imported from another
            # repo by import_sources, already stamped from THAT repo's history.
            # Skip so we don't overwrite their git_revision_* with empty values.
            continue
        first = commits[0]
        rev_date = _fmt_revision_date(first.get("date", ""))
        rev_author = first.get("author", "")

        if _inject_file(md_file, rev_date, rev_author):
            count += 1

    return count


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    hub_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

    provider = LocalGitHistoryProvider(
        cache_file=hub_dir / DEFAULT_CACHE_FILE.name,
        docs_dir="docs",
        repo_root=str(hub_dir),
    )
    provider.load(docs_dir="docs", repo_root=str(hub_dir))
    provider.save_cache(hub_dir / DEFAULT_CACHE_FILE.name)

    # Frontmatter injection is intentionally NOT called here — this script runs
    # in the fetch stage on most sites, so docs/ changes would be discarded
    # before the build. Injection is called from prepare_directory_pages.main()
    # which runs in the prepare stage where docs/ is preserved as an artifact.


if __name__ == "__main__":
    main()
