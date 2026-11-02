"""Command-line interface for textcharts.

Thin wrapper around the shared command layer. All chart logic, validation,
and rendering is delegated to textcharts.commands.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from textcharts.commands import execute_command, list_commands
from textcharts.commands.parsers import ParseError
from textcharts.commands.registry import REGISTRY, describe_command


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser dynamically from the command registry."""
    parser = argparse.ArgumentParser(
        prog="textcharts",
        description="Beautiful terminal charts — 15 chart types with zero dependencies.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Chart type or meta-command")

    # Meta-command: list
    subparsers.add_parser("list", help="List all available chart types")

    # Chart subcommands — auto-generated from registry
    for name, cmd_info in sorted(REGISTRY.items()):
        desc = describe_command(name)
        sub = subparsers.add_parser(
            name,
            help=cmd_info.description,
            description=_format_description(desc),
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Common options
        sub.add_argument("-f", "--file", metavar="PATH", help="Read JSON data from file (default: stdin)")
        sub.add_argument("--title", help="Chart title")
        sub.add_argument("--subtitle", help="Subtitle line displayed below the title")
        sub.add_argument("--width", type=int, help="Chart width in characters")
        sub.add_argument("--height", type=int, help="Chart height in rows")
        sub.add_argument("--color", dest="use_color", action="store_true", default=None, help="Enable color (default)")
        sub.add_argument("--no-color", dest="use_color", action="store_false", help="Disable color output")
        sub.add_argument("--unicode", dest="use_unicode", action="store_true", default=None, help="Enable Unicode")
        sub.add_argument("--no-unicode", dest="use_unicode", action="store_false", help="Disable Unicode")
        sub.add_argument("--theme", choices=["light", "dark"], help="Color theme")
        sub.add_argument("--outlier-cap", dest="outlier_cap", type=float, help="Fixed scale cap for outliers")

        # Chart-specific parameters (skip any that shadow common options)
        common_names = {"width", "height", "use_color", "use_unicode", "theme", "title", "file"}
        for param in desc["chart_params"]:
            if param["name"] not in common_names:
                _add_param_argument(sub, param)

    return parser


def _format_description(desc: dict[str, Any]) -> str:
    """Format a rich description for --help including data format, fields, and example."""
    lines = [desc["description"], ""]
    lines.append(f"Input format: {desc['data_format']}")
    lines.append("")
    lines.append("Data fields:")
    for field in desc["data_fields"]:
        req = "(required)" if field["required"] else "(optional)"
        default = f" [default: {field['default']}]" if "default" in field else ""
        lines.append(f"  {field['name']:20s} {field['type']:8s} {req} {field['description']}{default}")

    # Generate minimal JSON example from required fields
    example = _generate_example(desc)
    if example:
        lines.append("")
        lines.append("Example:")
        lines.append(f"  echo '{example}' | textcharts {desc['name']}")
    return "\n".join(lines)


def _generate_example(desc: dict[str, Any]) -> str | None:
    """Generate a minimal JSON example from required data fields."""
    required_fields = [f for f in desc["data_fields"] if f["required"]]
    if not required_fields:
        return None

    sample_values = {"string": '"example"', "number": "42", "integer": "10", "boolean": "true", "array": "[1, 2, 3]"}

    if desc["data_format"] == "list of objects":
        item = ", ".join(f'"{f["name"]}": {sample_values.get(f["type"], "null")}' for f in required_fields)
        return f'[{{{item}}}]'
    else:
        pairs = ", ".join(f'"{f["name"]}": {sample_values.get(f["type"], "null")}' for f in required_fields)
        return f'{{{pairs}}}'


def _add_param_argument(parser: argparse.ArgumentParser, param: dict[str, Any]) -> None:
    """Add a chart-specific parameter as a CLI argument."""
    flag = f"--{param['name'].replace('_', '-')}"
    kwargs: dict[str, Any] = {"help": param["description"], "dest": param["name"]}

    if param["type"] == "boolean":
        # For boolean params, add --flag/--no-flag pair
        kwargs.pop("help")
        kwargs.pop("dest")
        parser.add_argument(flag, dest=param["name"], action="store_true", default=None, help=param["description"])
        no_flag = f"--no-{param['name'].replace('_', '-')}"
        parser.add_argument(no_flag, dest=param["name"], action="store_false", help=f"Disable {param['description']}")
    elif param["type"] == "integer":
        kwargs["type"] = int
        if "enum" in param:
            kwargs["choices"] = [int(v) for v in param["enum"]]
        parser.add_argument(flag, **kwargs)
    elif param["type"] == "number":
        kwargs["type"] = float
        parser.add_argument(flag, **kwargs)
    else:
        if "enum" in param:
            kwargs["choices"] = param["enum"]
        parser.add_argument(flag, **kwargs)


def _read_input(args: argparse.Namespace) -> Any:
    """Read and parse JSON input from file or stdin."""
    if hasattr(args, "file") and args.file:
        try:
            with open(args.file) as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON in {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

    if sys.stdin.isatty():
        print("Error: no input data. Pipe JSON via stdin or use --file/-f.", file=sys.stderr)
        sys.exit(1)

    raw = sys.stdin.read()
    if not raw.strip():
        print("Error: empty input on stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON on stdin: {e}", file=sys.stderr)
        sys.exit(1)


def _run_list() -> None:
    """Print all available chart types."""
    commands = list_commands()
    max_name_len = max(len(name) for name, _ in commands)
    for name, description in commands:
        print(f"  {name:<{max_name_len}}  {description}")


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "list":
        _run_list()
        return

    # Read input data
    data = _read_input(args)

    # Build options dict from common args
    options: dict[str, Any] = {}
    for key in ("width", "height", "use_color", "use_unicode", "theme", "outlier_cap"):
        val = getattr(args, key, None)
        if val is not None:
            options[key] = val

    # Collect chart-specific kwargs
    desc = describe_command(args.command)
    chart_kwargs: dict[str, Any] = {}
    for param in desc["chart_params"]:
        val = getattr(args, param["name"], None)
        if val is not None:
            chart_kwargs[param["name"]] = val

    try:
        result = execute_command(
            args.command,
            data,
            title=getattr(args, "title", None),
            subtitle=getattr(args, "subtitle", None),
            options=options if options else None,
            **chart_kwargs,
        )
        print(result)
    except (ParseError, KeyError, ValueError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
