"""
Stream debug script — reads test_input.txt and runs it through StreamBlockProcessor.

Usage:
    1. Paste any LLM response content into test_input.txt (same directory as this file)
    2. Run: python ai/processing/blocks/tests/stream_debug.py

    Optional flags:
        --chunk-size N   Simulate streaming by feeding N bytes at a time (default: 0 = whole file at once)
        --json           Print each event as raw JSON instead of the human-readable summary
        --final-only     Only print the final complete state of each block, not every streaming event
        --no-color       Disable ANSI colour output
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from matrx_utils import vcprint, clear_terminal
# ---------------------------------------------------------------------------
# Allow running from the repo root without installing the package
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor  # noqa: E402

INPUT_FILE = os.path.join(os.path.dirname(__file__), "test_input.txt")


# ---------------------------------------------------------------------------
# ANSI colours
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
    if not _USE_COLOR:
        return text
    return f"{code}{text}{C.RESET}"


# ---------------------------------------------------------------------------
# Type → colour mapping so different block types stand out
# ---------------------------------------------------------------------------

_TYPE_COLORS: dict[str, str] = {
    "text":                 C.WHITE,
    "code":                 C.YELLOW,
    "table":                C.CYAN,
    "quiz":                 C.MAGENTA,
    "flashcards":           C.GREEN,
    "tasks":                C.GREEN,
    "transcript":           C.BLUE,
    "thinking":             C.GREY,
    "reasoning":            C.GREY,
    "consolidated_reasoning": C.GREY,
    "presentation":         C.MAGENTA,
    "decision_tree":        C.CYAN,
    "comparison_table":     C.CYAN,
    "diagram":              C.CYAN,
    "math_problem":         C.BLUE,
    "cooking_recipe":       C.GREEN,
    "timeline":             C.BLUE,
    "progress_tracker":     C.GREEN,
    "troubleshooting":      C.YELLOW,
    "resources":            C.BLUE,
    "research":             C.BLUE,
    "questionnaire":        C.GREEN,
}


def _type_color(block_type: str) -> str:
    return _TYPE_COLORS.get(block_type, C.WHITE)


# ---------------------------------------------------------------------------
# Pretty-print a single stream event
# ---------------------------------------------------------------------------

def _status_color(status: str) -> str:
    if "complete" in status:
        return C.GREEN
    if "error" in status:
        return C.RED
    return C.YELLOW  # streaming


def _format_event(event_num: int, data: dict, chunk_offset: int | None) -> str:
    block_id    = data.get("blockId", data.get("block_id", "?"))
    block_index = data.get("blockIndex", data.get("block_index", "?"))
    btype       = data.get("type", "?")
    status_raw  = str(data.get("status", "?"))
    status      = status_raw.split(".")[-1]  # strip enum prefix

    content     = data.get("content")
    has_data    = data.get("data") is not None

    tc = _type_color(btype)
    sc = _status_color(status)

    # Header line
    offset_str = f"  @byte {chunk_offset}" if chunk_offset is not None else ""
    header = (
        f"{_c(C.BOLD + C.DIM, f'#{event_num:>4}')}"
        f"  {_c(C.BOLD, f'blk[{block_index}] {block_id}')}"
        f"  type={_c(C.BOLD + tc, f'{btype:<22}')}"
        f"  status={_c(sc, f'{status:<10}')}"
        f"  has_data={_c(C.GREEN if has_data else C.DIM, str(has_data))}"
        f"{_c(C.DIM, offset_str)}"
    )

    lines = [header]

    # Content preview (up to 120 chars, show length)
    if content is not None:
        clen = len(content)
        preview = content.replace("\n", "↵").replace("\t", "→")
        if len(preview) > 120:
            preview = preview[:117] + "…"
        lines.append(
            f"       content ({clen} chars): {_c(C.DIM, repr(preview))}"
        )

    # Parsed data summary
    if has_data:
        pdata = data["data"]
        if isinstance(pdata, dict):
            top_keys = list(pdata.keys())[:6]
            kv_pairs = []
            for k in top_keys:
                v = pdata[k]
                if isinstance(v, list):
                    kv_pairs.append(f"{k}=[…×{len(v)}]")
                elif isinstance(v, str) and len(v) > 40:
                    kv_pairs.append(f"{k}={repr(v[:37])}…")
                else:
                    kv_pairs.append(f"{k}={repr(v)}")
            summary = ", ".join(kv_pairs)
            if len(pdata) > 6:
                summary += f", …+{len(pdata) - 6} more"
            lines.append(f"       data: {_c(C.CYAN, '{' + summary + '}')}")

    # Metadata (only if non-empty and not just the language echo)
    meta = data.get("metadata", {})
    if meta:
        lines.append(f"       metadata: {_c(C.DIM, json.dumps(meta))}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core runner
# ---------------------------------------------------------------------------

def run(
    content: str,
    chunk_size: int = 0,
    print_json: bool = False,
    final_only: bool = False,
) -> None:
    processor = StreamBlockProcessor()
    event_num = 0
    all_events: list[tuple[int, dict, int | None]] = []  # (event_num, data, byte_offset)

    def _collect(events, offset: int | None = None) -> None:
        nonlocal event_num
        for event in events:
            event_num += 1
            data = event.to_stream_event()["data"]
            all_events.append((event_num, data, offset))

    if chunk_size > 0:
        print(_c(C.BOLD + C.CYAN, f"\n── Streaming mode: {chunk_size}-byte chunks ──\n"))
        for i in range(0, len(content), chunk_size):
            chunk = content[i : i + chunk_size]
            _collect(processor.process_token(chunk), offset=i)
        _collect(processor.finalize(), offset=len(content))
    else:
        print(_c(C.BOLD + C.CYAN, "\n── Batch mode: full content at once ──\n"))
        _collect(processor.process_token(content))
        _collect(processor.finalize())

    # -----------------------------------------------------------------------
    # If final_only, keep only the last event per blockId
    # -----------------------------------------------------------------------
    if final_only:
        seen: dict[str, tuple[int, dict, int | None]] = {}
        for entry in all_events:
            bid = entry[1].get("blockId", entry[1].get("block_id", ""))
            seen[bid] = entry
        all_events = list(seen.values())
        print(_c(C.BOLD + C.CYAN, f"── Final state only: {len(all_events)} block(s) ──\n"))
    else:
        print(_c(C.BOLD + C.CYAN, f"── Total events: {len(all_events)} ──\n"))

    for ev_num, data, offset in all_events:
        if print_json:
            print(json.dumps({"event": "render_block", "data": data}, indent=2))
            print()
        else:
            print(_format_event(ev_num, data, offset if chunk_size > 0 else None))

    # -----------------------------------------------------------------------
    # Summary footer
    # -----------------------------------------------------------------------
    print()
    print(_c(C.BOLD, "── Summary ──"))
    block_ids_seen: dict[str, dict] = {}
    for _, data, _ in all_events:
        bid = data.get("blockId", data.get("block_id", "?"))
        block_ids_seen[bid] = data  # last state wins

    for bid, data in block_ids_seen.items():
        btype   = data.get("type", "?")
        status  = str(data.get("status", "?")).split(".")[-1]
        clen    = len(data.get("content") or "")
        has_data = data.get("data") is not None
        tc = _type_color(btype)
        sc = _status_color(status)
        print(
            f"  {_c(C.BOLD, bid):<12}"
            f"  type={_c(C.BOLD + tc, btype):<30}"
            f"  {_c(sc, status):<12}"
            f"  content_len={clen}"
            f"  has_data={has_data}"
        )

    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    global _USE_COLOR

    parser = argparse.ArgumentParser(
        description="Debug the StreamBlockProcessor against content in test_input.txt"
    )
    parser.add_argument(
        "--chunk-size", "-c",
        type=int,
        default=0,
        metavar="N",
        help="Feed content N bytes at a time to simulate streaming (0 = all at once)",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Print raw JSON for each event instead of the formatted summary",
    )
    parser.add_argument(
        "--final-only", "-f",
        action="store_true",
        help="Print only the final state of each block (skip intermediate streaming events)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colour output",
    )
    parser.add_argument(
        "--input", "-i",
        default=INPUT_FILE,
        help=f"Path to input file (default: {INPUT_FILE})",
    )
    args = parser.parse_args()

    if args.no_color:
        _USE_COLOR = False

    input_path = args.input
    if not os.path.exists(input_path):
        # Create an empty placeholder so the user knows where to put content
        with open(input_path, "w") as f:
            f.write("# Paste your LLM response content here and re-run the script.\n")
        print(f"Created empty input file: {input_path}")
        print("Paste your content there, then run the script again.")
        sys.exit(0)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print(f"Input file is empty: {input_path}")
        print("Paste some content there and re-run.")
        sys.exit(0)

    print(_c(C.BOLD, f"Input: {input_path}  ({len(content)} chars)"))

    run(
        content=content,
        chunk_size=args.chunk_size,
        print_json=args.json,
        final_only=args.final_only,
    )


if __name__ == "__main__":
    clear_terminal()
    main()
