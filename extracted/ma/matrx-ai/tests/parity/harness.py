"""Python <-> TypeScript block-splitter parity harness.

Feeds committed adversarial markdown fixtures through BOTH production
splitters and diffs the structured results field by field:

  * Python : ``matrx_ai.processing.blocks.block_detector.split_content_into_blocks``
  * TS     : ``splitContentIntoBlocksV2`` (matrx-frontend content-splitter-v2.ts),
             reached through the committed bridge script
             ``matrx_ai/processing/blocks/tests/ts_bridge/parse_blocks.ts``.

The frontend is the richer, currently-live implementation: a difference is a
Python defect until proven otherwise. Run it directly for a human report::

    uv run python packages/matrx-ai/tests/parity/harness.py
    uv run python packages/matrx-ai/tests/parity/harness.py --fixture 03_fences_and_languages.md

``test_ts_parser_parity.py`` is the CI face of the same code.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

FIXTURE_DIR = Path(__file__).parent / "fixtures"

# Metadata keys the frontend attaches that Python has no counterpart for BY
# DESIGN. Every entry is a deliberate, named exclusion — never a silent skip.
# Key is (block_type, metadata_key); block_type "*" means every block type.
FE_ONLY_METADATA_KEYS: dict[tuple[str, str], str] = {
    (
        "*",
        "__ir",
    ): "content-ir canonical envelope; built from the FE kind registry (registry-backed, not a detection fact)",
    ("*", "cacheKey"): "FE streaming render cache key; render-loop concern with no server meaning",
}


# Metadata keys PYTHON attaches that the frontend has no counterpart for BY
# DESIGN — server-side enrichment the frontend re-derives itself and ignores.
# Same rule as above: declared, named, reasoned; never a silent skip.
# Every entry is scoped to the ONE block type it belongs to — a bare key name
# would blanket-hide real drift on other block types.
PY_ONLY_METADATA_KEYS: dict[tuple[str, str], str] = {
    (
        "matrx",
        "matrxVersion",
    ): "decoded envelope sentinel, so a server consumer routes without a second parse",
    ("matrx", "envelopeType"): "decoded envelope `type` control field",
    ("matrx", "itemCount"): "decoded envelope item count",
    ("matrx", "kind"): "decoded envelope `kind` control field",
    ("matrx", "isComplete"): "server-side completeness flag, uniform with every other Python block",
}


# Fixtures that MUST diverge, with the recorded reason. Each is an open finding
# reported to Arman, never a silently tolerated difference: the gate asserts the
# divergence is STILL THERE, so the day either side changes, this fails loudly
# and the finding gets re-decided instead of quietly resolving itself.
EXPECTED_DIVERGENT_FIXTURES: dict[str, str] = {}


def _repo_root() -> Path:
    # .../aidream/packages/matrx-ai/tests/parity/harness.py -> .../aidream
    return Path(__file__).resolve().parents[4]


def frontend_root() -> Path | None:
    env = os.environ.get("MATRX_FRONTEND_ROOT")
    if env:
        p = Path(env)
        return p if (p / "tsconfig.json").is_file() else None
    p = _repo_root().parent / "matrx-frontend"
    return p if (p / "tsconfig.json").is_file() else None


def bridge_script() -> Path:
    return (
        _repo_root()
        / "packages/matrx-ai/matrx_ai/processing/blocks/tests/ts_bridge/parse_blocks.ts"
    )


class BridgeUnavailable(RuntimeError):
    """The TS side cannot be executed here — parity is UNVERIFIED, never 'passing'."""


def run_python(content: str) -> list[dict[str, Any]]:
    from matrx_ai.processing.blocks.block_detector import split_content_into_blocks

    out: list[dict[str, Any]] = []
    for b in split_content_into_blocks(content):
        out.append(
            {
                "type": b.type,
                "content": b.content,
                "language": b.language,
                "src": b.src,
                "alt": b.alt,
                "metadata": dict(b.metadata or {}),
            }
        )
    return out


def _normalize(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "type": b.get("type"),
            "content": b.get("content", ""),
            "language": b.get("language"),
            "src": b.get("src"),
            "alt": b.get("alt"),
            "metadata": dict(b.get("metadata") or {}),
        }
        for b in raw
    ]


def run_typescript_batch(paths: list[Path], fe_root: Path) -> dict[str, list[dict[str, Any]]]:
    """Run the TS splitter over every path in ONE tsx startup.

    Output goes through a file, never stdout: imported frontend modules print
    parser diagnostics, so stdout is not a reliable JSON channel.
    """
    if shutil.which("npx") is None:
        raise BridgeUnavailable("npx not on PATH")
    script = bridge_script()
    if not script.is_file():
        raise BridgeUnavailable(f"bridge script missing: {script}")
    if len(paths) < 2:
        # The bridge only enters batch mode with 2+ paths; duplicate the single
        # path so the shape is uniform (the duplicate collapses on the key).
        paths = paths * 2

    with tempfile.TemporaryDirectory() as tmp:
        out_file = Path(tmp) / "blocks.json"
        proc = subprocess.run(
            [
                "npx",
                "tsx",
                "--tsconfig",
                str(fe_root / "tsconfig.json"),
                str(script),
                *[str(p.resolve()) for p in paths],
                "--out",
                str(out_file),
            ],
            cwd=str(fe_root),
            capture_output=True,
            text=True,
            timeout=900,
        )
        if proc.returncode != 0:
            raise BridgeUnavailable(f"TS bridge exited {proc.returncode}\n{proc.stderr[-4000:]}")
        if not out_file.is_file():
            raise BridgeUnavailable(f"TS bridge wrote no output file\n{proc.stderr[-4000:]}")
        raw = json.loads(out_file.read_text())

    return {key: _normalize(blocks) for key, blocks in raw.items()}


@dataclass
class Difference:
    fixture: str
    index: int | None
    field: str
    python: Any
    typescript: Any

    def render(self) -> str:
        loc = f"block[{self.index}]" if self.index is not None else "document"
        return (
            f"  {self.fixture} {loc}.{self.field}\n"
            f"      python = {self.python!r}\n"
            f"      typescript = {self.typescript!r}"
        )


def _comparable_metadata(md: dict[str, Any], block_type: str | None) -> dict[str, Any]:
    declared = set(FE_ONLY_METADATA_KEYS) | set(PY_ONLY_METADATA_KEYS)
    excluded = {key for (bt, key) in declared if bt in ("*", block_type)}
    return {k: v for k, v in md.items() if k not in excluded}


def diff_blocks(
    fixture: str,
    py: list[dict[str, Any]],
    ts: list[dict[str, Any]],
) -> list[Difference]:
    diffs: list[Difference] = []

    if len(py) != len(ts):
        diffs.append(
            Difference(
                fixture,
                None,
                "block_count",
                len(py),
                len(ts),
            )
        )
        diffs.append(
            Difference(
                fixture,
                None,
                "block_types",
                [b["type"] for b in py],
                [b["type"] for b in ts],
            )
        )
        return diffs

    for idx, (p, t) in enumerate(zip(py, ts)):
        for field in ("type", "content", "language", "src", "alt"):
            if p[field] != t[field]:
                diffs.append(Difference(fixture, idx, field, p[field], t[field]))

        pm = _comparable_metadata(p["metadata"], p["type"])
        tm = _comparable_metadata(t["metadata"], t["type"])
        # Compare only keys BOTH sides claim to produce plus keys either side
        # produces that the other silently omits — an omitted key is drift too.
        for key in sorted(set(pm) | set(tm)):
            if pm.get(key, "<absent>") != tm.get(key, "<absent>"):
                diffs.append(
                    Difference(
                        fixture,
                        idx,
                        f"metadata.{key}",
                        pm.get(key, "<absent>"),
                        tm.get(key, "<absent>"),
                    )
                )
    return diffs


def fixtures() -> list[Path]:
    return sorted(FIXTURE_DIR.glob("*.md"))


def compare_all(paths: list[Path], fe_root: Path) -> dict[str, list[Difference]]:
    ts_by_path = run_typescript_batch(paths, fe_root)
    results: dict[str, list[Difference]] = {}
    for path in paths:
        key = str(path.resolve())
        if key not in ts_by_path:
            raise BridgeUnavailable(f"TS bridge returned no result for {key}")
        results[path.name] = diff_blocks(path.name, run_python(path.read_text()), ts_by_path[key])
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fixture", help="run one fixture by file name")
    args = ap.parse_args()

    fe = frontend_root()
    if fe is None:
        print(
            "PARITY UNVERIFIED: matrx-frontend not found "
            "(set MATRX_FRONTEND_ROOT or check out the sibling repo).",
            file=sys.stderr,
        )
        return 2

    targets = fixtures()
    if args.fixture:
        targets = [p for p in targets if p.name == args.fixture]
        if not targets:
            print(f"no such fixture: {args.fixture}", file=sys.stderr)
            return 2

    try:
        results = compare_all(targets, fe)
    except BridgeUnavailable as exc:
        print(f"PARITY UNVERIFIED: {exc}", file=sys.stderr)
        return 2

    total = 0
    for path in targets:
        diffs = results[path.name]
        expected = path.name in EXPECTED_DIVERGENT_FIXTURES
        if expected:
            status = "KNOWN" if diffs else "RESOLVED?"
        else:
            status = "OK" if not diffs else f"{len(diffs)} DIFF"
            total += len(diffs)
        print(f"[{status:>9}] {path.name}")
        for d in diffs:
            print(d.render())
        if expected:
            print(f"      RECORDED: {EXPECTED_DIVERGENT_FIXTURES[path.name]}")
            if not diffs:
                print(
                    "      !! the recorded divergence is GONE — re-decide the "
                    "finding, do not just delete this entry."
                )
                total += 1

    print(f"\n{total} difference(s) across {len(targets)} fixture(s).")
    print("\nDeclared, deliberate metadata exclusions (never silent):")
    for label, table in (
        ("FE-only", FE_ONLY_METADATA_KEYS),
        ("Python-only", PY_ONLY_METADATA_KEYS),
    ):
        for (block_type, key), why in table.items():
            print(f"  [{label}] {block_type}.{key} — {why}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
