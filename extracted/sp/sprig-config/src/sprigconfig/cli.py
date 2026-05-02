# sprigconfig/cli.py

import argparse
import json
import sys
from pathlib import Path

from sprigconfig.config_loader import ConfigLoader
from sprigconfig.exceptions import ConfigLoadError
from sprigconfig.lazy_secret import LazySecret
from sprigconfig.help import COMMAND_HELP


def _render_pretty_yaml(data):
    """Render clean, reusable, human-friendly YAML."""
    import yaml

    return yaml.safe_dump(
        data,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        indent=2,
    )


def _extract_data_for_dump(config, reveal_secrets: bool):
    """
    Convert Config → plain dict ready for YAML/JSON output.
    Uses Config.to_dict() to avoid !!python/object wrappers.
    """

    raw = config.to_dict(reveal_secrets=reveal_secrets)

    def walk(node):
        if isinstance(node, LazySecret):
            return node.get() if reveal_secrets else "ENC(**REDACTED**)"
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v) for v in node]
        return node

    return walk(raw)


def run_dump(
    config_dir: Path,
    profile: str,
    reveal_secrets: bool,
    output_file: Path | None,
    output_fmt: str,
    config_fmt: str | None,
):
    """Perform config load + pretty output."""
    try:
        loader = ConfigLoader(config_dir=config_dir, profile=profile, config_format=config_fmt)
        config = loader.load()
    except ConfigLoadError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    output = _extract_data_for_dump(config, reveal_secrets=reveal_secrets)

    if output_fmt == "json":
        rendered = json.dumps(output, indent=2)
    else:
        rendered = _render_pretty_yaml(output)

    if output_file:
        output_file.write_text(rendered, encoding="utf-8")
        print(f"Config written to {output_file}")
    else:
        print(rendered)


def main():
    parser = argparse.ArgumentParser(
        prog="sprigconfig",
        description="SprigConfig command-line utilities",
    )

    sub = parser.add_subparsers(dest="command")

    # ------------------------------------------------------------------
    # dump command
    # ------------------------------------------------------------------
    dump = sub.add_parser(
        "dump",
        help=COMMAND_HELP["dump"]["summary"],
        description=(
            "Load, merge, and pretty-print the final resolved configuration.\n\n"
            "Examples:\n"
            + "\n".join(f"  {ex}" for ex in COMMAND_HELP["dump"]["examples"])
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    dump.add_argument(
        "--config-dir",
        required=True,
        type=Path,
        help="Directory containing application.yml and optional profile overlays",
    )

    dump.add_argument(
        "--profile",
        required=True,
        help="Active profile to load (dev, test, prod, etc.)",
    )

    dump.add_argument(
        "--format",
        choices=["yml", "yaml", "json", "toml"],
        default=None,
        help="Config file format (default: yml, or SPRIGCONFIG_FORMAT env var)",
    )

    dump.add_argument(
        "--secrets",
        action="store_true",
        help="Reveal decrypted LazySecret values (UNSAFE!)",
    )

    dump.add_argument(
        "--output",
        type=Path,
        help="Write output to a file instead of stdout",
    )

    dump.add_argument(
        "--output-format",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format (default: yaml)",
    )

    # ------------------------------------------------------------------
    # Early help handling
    # ------------------------------------------------------------------
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nAvailable commands:")
        for name, meta in COMMAND_HELP.items():
            print(f"  {name:<8} {meta['summary']}")
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "dump":
        dump.print_help()
        print("\nExamples:")
        for ex in COMMAND_HELP["dump"]["examples"]:
            print(f"  {ex}")
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "dump":
        run_dump(
            config_dir=args.config_dir,
            profile=args.profile,
            reveal_secrets=args.secrets,
            output_file=args.output,
            output_fmt=args.output_format,
            config_fmt=args.format,
        )


if __name__ == "__main__":
    main()
