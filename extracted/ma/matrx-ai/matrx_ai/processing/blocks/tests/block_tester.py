"""
Block parsing test harness.

Runs the Python StreamBlockProcessor against content in test_content.md,
optionally runs the TypeScript frontend parser for comparison, and generates
a PASS/FAIL discrepancy report with colorized terminal output.

── How to use ────────────────────────────────────────────────────────────────

Edit the configuration variables in the __main__ block at the bottom, then:

    python ai/processing/blocks/tests/block_tester.py

── Configuration ─────────────────────────────────────────────────────────────

TEST_MODE           "single"   → test one BLOCK_TYPE from test_content.md
                    "full"     → test the entire test_content.md file

BLOCK_TYPE          which section to extract when TEST_MODE == "single"
                    (matches the <!-- BLOCK_TYPE: <name> --> delimiter)

CHUNK_SIZE          0          → feed full content at once (batch mode)
                    N > 0      → simulate streaming N bytes at a time

SAVE_RESULTS        True       → write a timestamped JSON snapshot to test_results/

COMPARE_WITH_FRONTEND
                    True       → also run the TypeScript parser and compare outputs

MATRX_FRONTEND_ROOT absolute path to the matrx-frontend repo (for the TS bridge)

── Output ────────────────────────────────────────────────────────────────────

Terminal: colorized Python blocks + optional TS comparison + discrepancy table
Snapshot: test_results/YYYY-MM-DD_HH-MM-SS_{block_type}.json
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from typing import Any

from matrx_utils import vcprint

# ---------------------------------------------------------------------------
# Allow running from repo root without installing the package
# ---------------------------------------------------------------------------

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor  # noqa: E402

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CONTENT_FILE = os.path.join(_THIS_DIR, "test_content.md")
RESULTS_DIR = os.path.join(_THIS_DIR, "test_results")
TS_BRIDGE_SCRIPT = os.path.join(_THIS_DIR, "ts_bridge", "parse_blocks.ts")

# ---------------------------------------------------------------------------
# ANSI colours (no external dependency)
# ---------------------------------------------------------------------------

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GREY    = "\033[90m"


_USE_COLOR = True


def _c(code: str, text: str) -> str:
    return f"{code}{text}{C.RESET}" if _USE_COLOR else text


_TYPE_COLORS: dict[str, str] = {
    "text": C.WHITE,
    "code": C.YELLOW,
    "table": C.CYAN,
    "quiz": C.MAGENTA,
    "flashcards": C.GREEN,
    "tasks": C.GREEN,
    "transcript": C.BLUE,
    "thinking": C.GREY,
    "reasoning": C.GREY,
    "consolidated_reasoning": C.GREY,
    "presentation": C.MAGENTA,
    "decision_tree": C.CYAN,
    "comparison_table": C.CYAN,
    "diagram": C.CYAN,
    "math_problem": C.BLUE,
    "cooking_recipe": C.GREEN,
    "timeline": C.BLUE,
    "progress_tracker": C.GREEN,
    "troubleshooting": C.YELLOW,
    "resources": C.BLUE,
    "research": C.BLUE,
    "questionnaire": C.GREEN,
    "decision": C.MAGENTA,
    "image": C.CYAN,
    "video": C.CYAN,
}


def _type_color(t: str) -> str:
    return _TYPE_COLORS.get(t, C.WHITE)


# ---------------------------------------------------------------------------
# Content extraction helpers
# ---------------------------------------------------------------------------

_BLOCK_TYPE_OPEN_RE = re.compile(r'<!--\s*BLOCK_TYPE:\s*(\S+)\s*-->')
_BLOCK_TYPE_CLOSE_RE = re.compile(r'<!--\s*END_BLOCK_TYPE:\s*(\S+)\s*-->')


def extract_section(content: str, block_type: str) -> str | None:
    """
    Extract the content between the first matching BLOCK_TYPE delimiters.

    Returns the raw text between the opening and closing comment tags,
    or None if the section is not found.
    """
    lines = content.splitlines(keepends=True)
    inside = False
    collected: list[str] = []

    for line in lines:
        if not inside:
            m = _BLOCK_TYPE_OPEN_RE.search(line)
            if m and m.group(1) == block_type:
                inside = True
            continue
        m = _BLOCK_TYPE_CLOSE_RE.search(line)
        if m and m.group(1) == block_type:
            break
        collected.append(line)

    return "".join(collected) if collected else None


def list_block_types(content: str) -> list[str]:
    """Return all block type names defined in the corpus."""
    return _BLOCK_TYPE_OPEN_RE.findall(content)


# ---------------------------------------------------------------------------
# Python parser runner
# ---------------------------------------------------------------------------

def run_python_parser(content: str, chunk_size: int = 0) -> list[dict[str, Any]]:
    """
    Run content through StreamBlockProcessor and return the final block states.

    Returns a list of the last event dict for each block (keyed by blockId).
    """
    processor = StreamBlockProcessor()
    all_events: list[dict[str, Any]] = []

    if chunk_size > 0:
        for i in range(0, len(content), chunk_size):
            for event in processor.process_token(content[i : i + chunk_size]):
                all_events.append(event.to_stream_event()["data"])
        for event in processor.finalize():
            all_events.append(event.to_stream_event()["data"])
    else:
        for event in processor.process_token(content):
            all_events.append(event.to_stream_event()["data"])
        for event in processor.finalize():
            all_events.append(event.to_stream_event()["data"])

    # Deduplicate: keep last state per blockId
    seen: dict[str, dict[str, Any]] = {}
    for ev in all_events:
        bid = ev.get("blockId", ev.get("block_id", ""))
        seen[bid] = ev
    return list(seen.values())


# ---------------------------------------------------------------------------
# TypeScript parser runner
# ---------------------------------------------------------------------------

def run_ts_parser(
    content: str,
    matrx_admin_path: str,
) -> list[dict[str, Any]] | None:
    """
    Run content through the TypeScript splitContentIntoBlocksV2 parser.

    Invokes parse_blocks.ts via npx tsx from the matrx-frontend directory so that
    the @/ path alias resolves correctly.

    Returns a list of RenderBlock dicts, or None if the subprocess failed.
    """
    tsconfig = os.path.join(matrx_admin_path, "tsconfig.json")
    if not os.path.isfile(tsconfig):
        print(_c(C.RED, f"[TS] tsconfig not found at: {tsconfig}"))
        print(_c(C.YELLOW, "     Set MATRX_FRONTEND_ROOT correctly to enable TS comparison."))
        return None

    cmd = [
        "npx", "tsx",
        "--tsconfig", tsconfig,
        TS_BRIDGE_SCRIPT,
    ]

    try:
        result = subprocess.run(
            cmd,
            input=content,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=matrx_admin_path,
        )
    except FileNotFoundError:
        print(_c(C.RED, "[TS] ERROR: 'npx' not found. Ensure Node.js is installed and in PATH."))
        return None
    except subprocess.TimeoutExpired:
        print(_c(C.RED, "[TS] ERROR: TypeScript parser timed out after 30s."))
        return None

    if result.stderr:
        for line in result.stderr.strip().splitlines():
            print(_c(C.GREY, f"     [TS stderr] {line}"))

    if result.returncode != 0:
        print(_c(C.RED, f"[TS] ERROR: parse_blocks.ts exited with code {result.returncode}"))
        return None

    try:
        blocks = json.loads(result.stdout)
        return blocks if isinstance(blocks, list) else None
    except json.JSONDecodeError as exc:
        print(_c(C.RED, f"[TS] ERROR: Failed to parse JSON output — {exc}"))
        print(_c(C.GREY, f"     stdout preview: {result.stdout[:300]}"))
        return None


# ---------------------------------------------------------------------------
# Comparison engine
# ---------------------------------------------------------------------------

def _deep_equal(a: Any, b: Any) -> bool:
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def _block_key(block: dict[str, Any]) -> str:
    """A canonical key for matching Python blocks to TS blocks."""
    btype = block.get("type") or block.get("blockType", "")
    content_snip = (block.get("content") or "")[:60]
    return f"{btype}:{content_snip}"


def compare_blocks(
    py_blocks: list[dict[str, Any]],
    ts_blocks: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Compare Python and TypeScript block outputs.

    Returns a report dict with:
        overall         "PASS" | "FAIL" | "IMPROVED"
        block_count     {"python": N, "ts": M, "match": True/False}
        block_results   list of per-block comparison results
        summary         human-readable summary lines
    """
    report: dict[str, Any] = {
        "overall": "PASS",
        "block_count": {
            "python": len(py_blocks),
            "ts": len(ts_blocks),
            "count_match": len(py_blocks) == len(ts_blocks),
        },
        "block_results": [],
        "summary": [],
    }

    if len(py_blocks) != len(ts_blocks):
        report["summary"].append(
            f"Block count differs: Python={len(py_blocks)}, TS={len(ts_blocks)}"
        )
        report["overall"] = "FAIL"

    # Match blocks by position (best effort) or by type+content prefix
    max_len = max(len(py_blocks), len(ts_blocks))
    for idx in range(max_len):
        py_blk = py_blocks[idx] if idx < len(py_blocks) else None
        ts_blk = ts_blocks[idx] if idx < len(ts_blocks) else None

        result: dict[str, Any] = {
            "index": idx,
            "python_type": py_blk.get("type") if py_blk else None,
            "ts_type": ts_blk.get("type") if ts_blk else None,
            "fields": {},
            "verdict": "PASS",
        }

        if py_blk is None:
            result["verdict"] = "FAIL"
            result["note"] = "Python produced no block for this index"
            report["overall"] = "FAIL"
            report["block_results"].append(result)
            continue

        if ts_blk is None:
            # Python produced an extra block — this may be IMPROVED (better inline handling)
            result["verdict"] = "IMPROVED"
            result["note"] = "Python produced extra block (possibly from inline pre/post text split)"
            if report["overall"] == "PASS":
                report["overall"] = "IMPROVED"
            report["block_results"].append(result)
            continue

        # Compare type
        py_type = py_blk.get("type")
        ts_type = ts_blk.get("type")
        type_match = py_type == ts_type
        result["fields"]["type"] = {
            "python": py_type,
            "ts": ts_type,
            "verdict": "PASS" if type_match else "FAIL",
        }
        if not type_match:
            result["verdict"] = "FAIL"
            report["overall"] = "FAIL"

        # Compare content (strip trailing whitespace for lenient comparison)
        py_content = (py_blk.get("content") or "").strip()
        ts_content = (ts_blk.get("content") or "").strip()
        content_match = py_content == ts_content
        result["fields"]["content"] = {
            "verdict": "PASS" if content_match else "WARN",
            "python_len": len(py_content),
            "ts_len": len(ts_content),
        }

        # Compare metadata.isComplete
        py_meta = py_blk.get("metadata") or {}
        ts_meta = ts_blk.get("metadata") or {}
        py_complete = py_meta.get("isComplete")
        ts_complete = ts_meta.get("isComplete")
        complete_match = py_complete == ts_complete
        result["fields"]["metadata.isComplete"] = {
            "python": py_complete,
            "ts": ts_complete,
            "verdict": "PASS" if complete_match else "FAIL",
        }
        if not complete_match:
            result["verdict"] = "FAIL"
            report["overall"] = "FAIL"

        # For decision blocks: compare parsed data structure
        if py_type == "decision" and ts_type == "decision":
            py_data = py_blk.get("data") or py_meta.get("decision")
            ts_decision = ts_meta.get("decision") or ts_blk.get("data")
            if py_data and ts_decision:
                # Compare prompt
                py_prompt = (py_data.get("prompt") or "").strip()
                ts_prompt = (ts_decision.get("prompt") or "").strip()
                result["fields"]["decision.prompt"] = {
                    "python": py_prompt,
                    "ts": ts_prompt,
                    "verdict": "PASS" if py_prompt == ts_prompt else "FAIL",
                }
                if py_prompt != ts_prompt:
                    result["verdict"] = "FAIL"
                    report["overall"] = "FAIL"

                # Compare options count
                py_opts = py_data.get("options", [])
                ts_opts = ts_decision.get("options", [])
                opts_count_match = len(py_opts) == len(ts_opts)
                result["fields"]["decision.options_count"] = {
                    "python": len(py_opts),
                    "ts": len(ts_opts),
                    "verdict": "PASS" if opts_count_match else "FAIL",
                }
                if not opts_count_match:
                    result["verdict"] = "FAIL"
                    report["overall"] = "FAIL"

                # Compare each option label + text
                for oi, (py_opt, ts_opt) in enumerate(
                    zip(py_opts, ts_opts, strict=False)
                ):
                    py_label = (py_opt.get("label") or "").strip()
                    ts_label = (ts_opt.get("label") or "").strip()
                    py_text = (py_opt.get("text") or "").strip()
                    ts_text = (ts_opt.get("text") or "").strip()
                    label_ok = py_label == ts_label
                    text_ok = py_text == ts_text
                    result["fields"][f"option[{oi}].label"] = {
                        "python": py_label,
                        "ts": ts_label,
                        "verdict": "PASS" if label_ok else "FAIL",
                    }
                    result["fields"][f"option[{oi}].text"] = {
                        "python": py_text,
                        "ts": ts_text,
                        "verdict": "PASS" if text_ok else "FAIL",
                    }
                    if not label_ok or not text_ok:
                        result["verdict"] = "FAIL"
                        report["overall"] = "FAIL"

        if result["verdict"] == "FAIL":
            report["overall"] = "FAIL"

        report["block_results"].append(result)

    return report


# ---------------------------------------------------------------------------
# Printing helpers
# ---------------------------------------------------------------------------

def _print_separator(label: str = "", char: str = "─", width: int = 80) -> None:
    if label:
        pad = max(0, width - len(label) - 4)
        print(_c(C.DIM, f"── {label} {'─' * pad}"))
    else:
        print(_c(C.DIM, char * width))


def _print_py_block(idx: int, block: dict[str, Any]) -> None:
    btype = block.get("type", "?")
    bid = block.get("blockId", block.get("block_id", "?"))
    status = str(block.get("status", "?")).split(".")[-1]
    has_data = block.get("data") is not None
    meta = block.get("metadata") or {}

    tc = _type_color(btype)
    sc = C.GREEN if "complete" in status else (C.RED if "error" in status else C.YELLOW)

    print(
        f"  {_c(C.BOLD + C.DIM, f'#{idx:>3}')}"
        f"  {_c(C.BOLD, bid)}"
        f"  type={_c(C.BOLD + tc, f'{btype:<24}')}"
        f"  status={_c(sc, f'{status:<10}')}"
        f"  has_data={_c(C.GREEN if has_data else C.DIM, str(has_data))}"
    )

    content = block.get("content")
    if content:
        preview = content.replace("\n", "↵")[:100]
        if len(content) > 100:
            preview += "…"
        print(f"       content ({len(content)} chars): {_c(C.DIM, repr(preview))}")

    if has_data:
        data = block["data"]
        if isinstance(data, dict):
            top_keys = list(data.keys())[:5]
            pairs = []
            for k in top_keys:
                v = data[k]
                if isinstance(v, list):
                    pairs.append(f"{k}=[×{len(v)}]")
                elif isinstance(v, str) and len(v) > 40:
                    pairs.append(f"{k}={repr(v[:37])}…")
                else:
                    pairs.append(f"{k}={repr(v)}")
            extra = f", …+{len(data) - 5} more" if len(data) > 5 else ""
            print(f"       data: {_c(C.CYAN, '{' + ', '.join(pairs) + extra + '}')}")

    if meta:
        print(f"       metadata: {_c(C.DIM, json.dumps(meta)[:120])}")


def _print_ts_block(idx: int, block: dict[str, Any]) -> None:
    btype = block.get("type", "?")
    tc = _type_color(btype)
    meta = block.get("metadata") or {}
    content = block.get("content") or ""

    print(
        f"  {_c(C.DIM, f'TS #{idx:>3}')}"
        f"  type={_c(C.BOLD + tc, f'{btype:<24}')}"
        f"  content_len={len(content)}"
    )

    if meta:
        print(f"       metadata: {_c(C.DIM, json.dumps(meta)[:120])}")


def _print_comparison_report(report: dict[str, Any]) -> None:
    overall = report["overall"]
    overall_color = C.GREEN if overall == "PASS" else (C.YELLOW if overall == "IMPROVED" else C.RED)

    _print_separator("Comparison Report")
    print(
        f"\n  Overall verdict: {_c(C.BOLD + overall_color, overall)}\n"
        f"  Block count — Python: {report['block_count']['python']}, "
        f"TS: {report['block_count']['ts']}, "
        f"match: {_c(C.GREEN if report['block_count']['count_match'] else C.RED, str(report['block_count']['count_match']))}"
    )

    for br in report["block_results"]:
        verdict = br["verdict"]
        vc = C.GREEN if verdict == "PASS" else (C.YELLOW if verdict == "IMPROVED" else C.RED)
        note = br.get("note", "")
        print(
            f"\n  Block [{br['index']}] "
            f"py_type={_c(_type_color(br['python_type'] or ''), br['python_type'] or 'N/A'):<28} "
            f"ts_type={_c(_type_color(br['ts_type'] or ''), br['ts_type'] or 'N/A'):<28} "
            f"→ {_c(C.BOLD + vc, verdict)}"
            + (f"  ⚑ {note}" if note else "")
        )
        for field, fdata in br.get("fields", {}).items():
            fv = fdata.get("verdict", "?")
            fc = C.GREEN if fv == "PASS" else (C.YELLOW if fv == "WARN" else C.RED)
            py_val = fdata.get("python")
            ts_val = fdata.get("ts")
            if py_val is not None and ts_val is not None and py_val != ts_val:
                print(
                    f"       {_c(fc, f'{field:<30}')} "
                    f"Python={_c(C.CYAN, repr(str(py_val)[:40]))}"
                    f"  TS={_c(C.MAGENTA, repr(str(ts_val)[:40]))}"
                )
            else:
                print(f"       {_c(fc, f'{field:<30}')} {_c(fc, fv)}")

    print()
    for line in report.get("summary", []):
        print(f"  {_c(C.YELLOW, '⚠')} {line}")
    print()


# ---------------------------------------------------------------------------
# Snapshot saver
# ---------------------------------------------------------------------------

def save_snapshot(
    block_type: str,
    content: str,
    py_blocks: list[dict[str, Any]],
    ts_blocks: list[dict[str, Any]] | None,
    report: dict[str, Any] | None,
) -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ts_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fname = f"{ts_str}_{block_type}.json"
    fpath = os.path.join(RESULTS_DIR, fname)

    snapshot = {
        "timestamp": ts_str,
        "block_type": block_type,
        "content_length": len(content),
        "python_blocks": py_blocks,
        "ts_blocks": ts_blocks,
        "comparison_report": report,
    }
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    return fpath


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_test(
    content: str,
    block_type: str,
    chunk_size: int = 0,
    save_results: bool = True,
    compare_with_frontend: bool = True,
    matrx_admin_path: str = "",
) -> None:
    """
    Run the full test pipeline for the given content and block_type label.
    """
    print(_c(C.BOLD + C.CYAN, f"\n{'═' * 80}"))
    print(_c(C.BOLD + C.CYAN, f"  Block Tester — block_type={block_type}  chunk_size={chunk_size}"))
    print(_c(C.BOLD + C.CYAN, f"{'═' * 80}\n"))
    print(_c(C.DIM, f"Content: {len(content)} chars"))

    # ── Python pass ──────────────────────────────────────────────────────────
    _print_separator("Python StreamBlockProcessor")
    py_blocks = run_python_parser(content, chunk_size)
    print(_c(C.BOLD, f"\nFinal blocks ({len(py_blocks)}):"))
    for idx, blk in enumerate(py_blocks):
        _print_py_block(idx, blk)

    # Deep-print decision block data via vcprint
    decision_blocks = [b for b in py_blocks if b.get("type") == "decision"]
    if decision_blocks:
        for db in decision_blocks:
            vcprint(db, title=f"decision block (Python)", color="magenta")

    # ── TypeScript pass ───────────────────────────────────────────────────────
    ts_blocks: list[dict[str, Any]] | None = None
    if compare_with_frontend:
        _print_separator("TypeScript splitContentIntoBlocksV2")
        ts_blocks = run_ts_parser(content, matrx_admin_path)
        if ts_blocks is not None:
            print(_c(C.BOLD, f"\nTS blocks ({len(ts_blocks)}):"))
            for idx, blk in enumerate(ts_blocks):
                _print_ts_block(idx, blk)
            ts_decision = [b for b in ts_blocks if b.get("type") == "decision"]
            if ts_decision:
                for db in ts_decision:
                    vcprint(db, title=f"decision block (TypeScript)", color="cyan")
        else:
            print(_c(C.YELLOW, "TS comparison skipped (parse_blocks.ts failed — see errors above)"))

    # ── Comparison ────────────────────────────────────────────────────────────
    report: dict[str, Any] | None = None
    if compare_with_frontend and ts_blocks is not None:
        report = compare_blocks(py_blocks, ts_blocks)
        _print_comparison_report(report)

    # ── Save snapshot ─────────────────────────────────────────────────────────
    if save_results:
        fpath = save_snapshot(block_type, content, py_blocks, ts_blocks, report)
        print(_c(C.DIM, f"Snapshot saved → {fpath}"))

    # Final verdict banner
    if report:
        overall = report["overall"]
        color = C.GREEN if overall == "PASS" else (C.YELLOW if overall == "IMPROVED" else C.RED)
        print(_c(C.BOLD + color, f"\n{'═' * 40}"))
        print(_c(C.BOLD + color, f"  RESULT: {overall}"))
        print(_c(C.BOLD + color, f"{'═' * 40}\n"))
    else:
        print(_c(C.DIM, "\n(No TS comparison — Python output above is the result.)\n"))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ── Configure here ────────────────────────────────────────────────────────
    TEST_MODE             = "single"    # "single" | "full"
    BLOCK_TYPE            = "decision_variant_b"  # section name in test_content.md
    CHUNK_SIZE            = 0           # 0 = batch; N = streaming simulation (bytes)
    SAVE_RESULTS          = True
    COMPARE_WITH_FRONTEND = True
    MATRX_FRONTEND_ROOT   = os.environ.get(
        "MATRX_FRONTEND_ROOT", "/Users/armanisadeghi/code/matrx-frontend"
    )
    # ─────────────────────────────────────────────────────────────────────────

    if not os.path.exists(TEST_CONTENT_FILE):
        print(_c(C.RED, f"ERROR: test_content.md not found at: {TEST_CONTENT_FILE}"))
        sys.exit(1)

    with open(TEST_CONTENT_FILE, "r", encoding="utf-8") as f:
        corpus = f.read()

    if TEST_MODE == "single":
        section = extract_section(corpus, BLOCK_TYPE)
        if section is None:
            print(_c(C.RED, f"ERROR: Section '<!-- BLOCK_TYPE: {BLOCK_TYPE} -->' not found in test_content.md"))
            available = list_block_types(corpus)
            print(_c(C.YELLOW, f"Available sections: {available}"))
            sys.exit(1)
        run_test(
            content=section,
            block_type=BLOCK_TYPE,
            chunk_size=CHUNK_SIZE,
            save_results=SAVE_RESULTS,
            compare_with_frontend=COMPARE_WITH_FRONTEND,
            matrx_admin_path=MATRX_FRONTEND_ROOT,
        )
    else:
        # Full corpus — test every section individually
        available = list_block_types(corpus)
        print(_c(C.BOLD, f"\nFull mode: testing {len(available)} sections\n"))
        for bt in available:
            section = extract_section(corpus, bt)
            if section:
                run_test(
                    content=section,
                    block_type=bt,
                    chunk_size=CHUNK_SIZE,
                    save_results=SAVE_RESULTS,
                    compare_with_frontend=COMPARE_WITH_FRONTEND,
                    matrx_admin_path=MATRX_FRONTEND_ROOT,
                )
