"""Rebuild the golden-master config corpus from a portal export.

Reads a JSON export of production configs (one current snapshot per repo, pulled
via `plain portal` — see tests/corpus/README.md) and writes tests/corpus/,
deduplicating by the whole config-set: two repos whose {path: content} sets are
identical compile to the same result, so only one representative is kept.

Usage:
    uv run python scripts/build_corpus.py /path/to/config_corpus.json
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent / "tests" / "corpus"


def slugify(full_name: str) -> str:
    # owner/repo -> owner__repo, keep only filesystem-safe chars
    return re.sub(r"[^A-Za-z0-9._-]", "-", full_name.replace("/", "__"))


def main(export_path: Path) -> None:
    repos = json.loads(export_path.read_text())["repos"]

    # Group repos by their exact config-set (paths + contents). compiled() is a
    # pure function of this set, so identical sets are redundant test cases.
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in repos:
        key = tuple(
            (c["path"], c["content"])
            for c in sorted(r["configs"], key=lambda c: c["path"])
        )
        groups[key].append(r)

    # Clear previously-generated content but keep the hand-written README.
    CORPUS.mkdir(parents=True, exist_ok=True)
    for entry in CORPUS.iterdir():
        if entry.name == "README.md":
            continue
        shutil.rmtree(entry) if entry.is_dir() else entry.unlink()

    manifest = []
    files_written = 0
    repos_represented = 0
    for key, members in groups.items():
        # Deterministic representative: the member whose full_name sorts first.
        rep = min(members, key=lambda r: r["full_name"])
        slug = slugify(rep["full_name"])

        for path, content in key:
            dest = CORPUS / slug / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
            files_written += 1
        repos_represented += len(members)

        manifest.append(
            {
                "dir": slug,
                "full_name": rep["full_name"],
                "host_type": rep["host_type"],
                "host_public": rep["host_public"],
                "sha": rep["sha"],
                "config_paths": [p for p, _ in key],
                "represents_n_repos": len(members),
            }
        )

    manifest.sort(key=lambda m: m["dir"])
    (CORPUS / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )

    print(f"unique config-sets  : {len(manifest)}")
    print(f"repos represented   : {repos_represented}")
    print(f"config files written: {files_written}")
    print(f"corpus dir          : {CORPUS}")
    print("\nNow regenerate snapshots:")
    print("  uv run pytest tests/test_corpus.py --insta update")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: build_corpus.py <config_corpus.json>")
    main(Path(sys.argv[1]))
