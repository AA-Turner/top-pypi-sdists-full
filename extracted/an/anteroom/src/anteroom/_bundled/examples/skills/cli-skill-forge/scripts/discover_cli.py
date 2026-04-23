#!/usr/bin/env python3
"""Discover a CLI help tree and write a cached manifest."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

SECTION_HINTS = (
    "commands:",
    "available commands:",
    "subcommands:",
    "command groups:",
)

OPTION_SECTION_HINTS = (
    "options:",
    "flags:",
    "global options:",
    "available options:",
)

SKIP_SUBCOMMANDS = {"help"}
MAX_CAPTURE_CHARS = 40000


@dataclass
class OptionSpec:
    flags: list[str]
    description: str


@dataclass
class NodeRecord:
    path: list[str]
    command: list[str]
    help_command: list[str]
    help_style: str
    help_flag: str
    returncode: int
    help_file: str
    subcommands: list[str]
    options: list[OptionSpec]
    headline: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, help="Logical tool name for output metadata.")
    parser.add_argument("--output-dir", required=True, help="Directory for manifest, summary, and help files.")
    parser.add_argument("--max-depth", type=int, default=4, help="Maximum subcommand depth to recurse.")
    parser.add_argument(
        "--max-subcommands",
        type=int,
        default=25,
        help="Maximum number of discovered subcommands to recurse into per node.",
    )
    parser.add_argument(
        "--help-style",
        action="append",
        choices=("append-flag", "prepend-help"),
        default=[],
        help="Help invocation style. May be supplied multiple times.",
    )
    parser.add_argument(
        "--help-flag",
        action="append",
        default=[],
        help="Help flag to try for append-flag style. May be supplied multiple times.",
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-help-call timeout in seconds.")
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Base command after --, for example: -- jira --profile corp",
    )
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("missing base command after --")
    if not args.help_style:
        args.help_style = ["append-flag", "prepend-help"]
    if not args.help_flag:
        args.help_flag = ["--help", "-h"]
    return args


def run_capture(command: list[str], timeout: float) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "PAGER": "cat",
        "MANPAGER": "cat",
        "GIT_PAGER": "cat",
    }
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        env=env,
    )


def help_variants(
    base_command: list[str],
    path: list[str],
    styles: list[str],
    flags: list[str],
) -> Iterable[tuple[str, str, list[str]]]:
    for style in styles:
        if style == "append-flag":
            for flag in flags:
                yield style, flag, [*base_command, *path, flag]
        elif style == "prepend-help":
            yield style, "help", [*base_command, "help", *path]


def score_help_output(returncode: int, text: str) -> int:
    score = 0
    lowered = text.lower()
    if text.strip():
        score += 1
    if returncode == 0:
        score += 3
    if "usage" in lowered:
        score += 3
    if "options:" in lowered or "flags:" in lowered:
        score += 2
    if "commands:" in lowered or "subcommands:" in lowered:
        score += 2
    if "unknown command" in lowered or "not found" in lowered:
        score -= 4
    return score


def pick_help_command(
    base_command: list[str],
    path: list[str],
    styles: list[str],
    flags: list[str],
    timeout: float,
) -> tuple[str, str, list[str], subprocess.CompletedProcess[str]]:
    best: tuple[int, str, str, list[str], subprocess.CompletedProcess[str]] | None = None
    for style, flag, command in help_variants(base_command, path, styles, flags):
        try:
            result = run_capture(command, timeout)
        except subprocess.TimeoutExpired as exc:
            result = subprocess.CompletedProcess(command, 124, "", f"Timed out after {timeout}s: {exc}")
        merged = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
        score = score_help_output(result.returncode, merged)
        if best is None or score > best[0]:
            best = (score, style, flag, command, result)
    if best is None:
        raise RuntimeError("no help command candidates were generated")
    _, style, flag, command, result = best
    return style, flag, command, result


def slug_for_path(path: list[str]) -> str:
    if not path:
        return "root"
    return "__".join(re.sub(r"[^A-Za-z0-9._-]+", "-", token) for token in path)


def extract_section_blocks(text: str, headings: tuple[str, ...]) -> list[str]:
    lines = text.splitlines()
    blocks: list[str] = []
    collecting = False
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        lowered = stripped.lower()
        generic_command_heading = (
            bool(stripped)
            and not stripped.startswith("-")
            and (
                "commands" in lowered
                or "subcommands" in lowered
                or "help topics" in lowered
                or "common git commands" in lowered
            )
        )
        if any(lowered == heading for heading in headings) or generic_command_heading:
            if current:
                blocks.append("\n".join(current))
                current = []
            collecting = True
            continue
        if collecting:
            if stripped and stripped.endswith(":") and lowered not in headings:
                if current:
                    blocks.append("\n".join(current))
                    current = []
                collecting = False
                continue
            if not stripped and current:
                blocks.append("\n".join(current))
                current = []
                collecting = False
                continue
            if stripped:
                current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def normalize_subcommand_token(token: str) -> str:
    return token.rstrip(":").strip()


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def looks_like_manpage(text: str) -> bool:
    headline = first_nonempty_line(text)
    return bool(re.match(r"^[A-Z0-9._-]+\(\d+\)", headline))


def extract_subcommands(text: str) -> list[str]:
    candidates: list[str] = []
    blocks = extract_section_blocks(text, SECTION_HINTS)
    for block in blocks:
        for raw_line in block.splitlines():
            line = raw_line.rstrip()
            if not line.strip():
                continue
            match = re.match(r"^\s{2,}([A-Za-z0-9][A-Za-z0-9._:-]*)\b", line)
            if not match:
                continue
            token = normalize_subcommand_token(match.group(1))
            if (
                not token
                or token.startswith("-")
                or token in SKIP_SUBCOMMANDS
                or token.isdigit()
                or token.lower() == "note"
            ):
                continue
            candidates.append(token)
    if not candidates and not looks_like_manpage(text):
        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if not line.strip():
                continue
            token: str | None = None
            for pattern in (
                r"^\s{2,}([A-Za-z0-9][A-Za-z0-9._:-]*)\s{2,}",
                r"^\s{2,}([A-Za-z0-9][A-Za-z0-9._:-]*):\s+",
            ):
                match = re.match(pattern, line)
                if match:
                    token = normalize_subcommand_token(match.group(1))
                    break
            if (
                not token
                or token.startswith("-")
                or token in SKIP_SUBCOMMANDS
                or token.isdigit()
                or token.lower() == "note"
            ):
                continue
            candidates.append(token)
    seen: set[str] = set()
    ordered: list[str] = []
    for token in candidates:
        if token not in seen:
            ordered.append(token)
            seen.add(token)
    return ordered


def extract_options(text: str) -> list[OptionSpec]:
    options: list[OptionSpec] = []
    blocks = extract_section_blocks(text, OPTION_SECTION_HINTS)
    for block in blocks:
        for raw_line in block.splitlines():
            line = raw_line.rstrip()
            if not line.strip():
                continue
            if not re.match(r"^\s*-", line):
                continue
            parts = re.split(r"\s{2,}", line.strip(), maxsplit=1)
            flag_part = parts[0]
            description = parts[1].strip() if len(parts) > 1 else ""
            flags = [piece.strip() for piece in flag_part.split(",") if piece.strip()]
            if flags:
                options.append(OptionSpec(flags=flags, description=description))
    return options


def write_summary(tool: str, base_command: list[str], nodes: list[NodeRecord], output_path: Path) -> None:
    lines = [
        f"# {tool} CLI Summary",
        "",
        f"- Base command: `{' '.join(base_command)}`",
        f"- Captured nodes: {len(nodes)}",
        "",
        "## Commands",
        "",
    ]
    for node in sorted(nodes, key=lambda item: (len(item.path), item.path)):
        path_label = "root" if not node.path else " ".join(node.path)
        lines.append(f"### `{path_label}`")
        lines.append("")
        lines.append(f"- Command: `{' '.join(node.command)}`")
        lines.append(f"- Help: `{' '.join(node.help_command)}`")
        if node.headline:
            lines.append(f"- Headline: {node.headline}")
        if node.subcommands:
            lines.append(f"- Subcommands: {', '.join(f'`{item}`' for item in node.subcommands)}")
        if node.options:
            sample = ", ".join(f"`{' / '.join(opt.flags)}`" for opt in node.options[:8])
            lines.append(f"- Options: {sample}")
        lines.append("")
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    help_dir = output_dir / "help"
    output_dir.mkdir(parents=True, exist_ok=True)
    help_dir.mkdir(parents=True, exist_ok=True)

    queue: list[list[str]] = [[]]
    visited: set[tuple[str, ...]] = set()
    nodes: list[NodeRecord] = []

    while queue:
        path = queue.pop(0)
        path_key = tuple(path)
        if path_key in visited:
            continue
        visited.add(path_key)

        style, flag, help_command, result = pick_help_command(
            base_command=args.command,
            path=path,
            styles=args.help_style,
            flags=args.help_flag,
            timeout=args.timeout,
        )
        merged = ((result.stdout or "") + ("\n" + result.stderr if result.stderr else "")).strip()
        merged = merged[:MAX_CAPTURE_CHARS]
        help_file = help_dir / f"{slug_for_path(path)}.txt"
        help_file.write_text(merged + ("\n" if merged else ""), encoding="utf-8")

        subcommands = extract_subcommands(merged)
        node = NodeRecord(
            path=path,
            command=[*args.command, *path],
            help_command=help_command,
            help_style=style,
            help_flag=flag,
            returncode=result.returncode,
            help_file=str(help_file.relative_to(output_dir)),
            subcommands=subcommands,
            options=extract_options(merged),
            headline=first_nonempty_line(merged),
        )
        nodes.append(node)

        if len(path) >= args.max_depth:
            continue
        for subcommand in subcommands[: args.max_subcommands]:
            next_path = [*path, subcommand]
            if tuple(next_path) not in visited:
                queue.append(next_path)

    manifest = {
        "tool": args.tool,
        "discovered_at": datetime.now(timezone.utc).isoformat(),
        "base_command": args.command,
        "max_depth": args.max_depth,
        "max_subcommands": args.max_subcommands,
        "nodes": [asdict(node) for node in nodes],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_summary(args.tool, args.command, nodes, output_dir / "summary.md")
    print(f"Wrote discovery output to {output_dir}")
    print(f"Nodes captured: {len(nodes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
