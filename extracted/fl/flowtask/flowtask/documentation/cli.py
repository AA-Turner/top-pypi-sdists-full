"""CLI for generating Flowtask component documentation.

This module provides a command-line interface for generating documentation
from Flowtask component docstrings.

Usage:
    flowtask-docs [--output DIR] [--components DIR...]
    python -m flowtask.documentation.cli [--output DIR] [--components DIR...]

Examples:
    # Generate docs with defaults (writes inside the package)
    flowtask-docs

    # Specify output directory
    flowtask-docs --output ./docs

    # Scan specific directories
    flowtask-docs -c flowtask/components plugins/components

    # Verbose output
    flowtask-docs -v

    # Check-only mode (non-zero exit if regeneration would change files)
    flowtask-docs --check
"""
import argparse
import logging
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

from .generator import ComponentDocGenerator


# Default output ships with the package so the future informational API can
# resolve docs via importlib.resources / relative paths regardless of install
# layout (editable, wheel, site-packages).
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "generated"


def get_base_dir() -> Path:
    """Get the project base directory.

    Returns:
        Path to the project root directory.
    """
    try:
        from navconfig import BASE_DIR
        return Path(BASE_DIR)
    except ImportError:
        # Fallback: use current working directory
        return Path.cwd()


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure logging for the CLI.

    Args:
        verbose: If True, set log level to DEBUG.

    Returns:
        Configured logger instance.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )
    return logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        args: List of arguments (defaults to sys.argv[1:]).

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Generate documentation for Flowtask components",
        prog="flowtask-docs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           Generate docs with defaults
  %(prog)s -o ./docs                 Output to ./docs directory
  %(prog)s -c src/components         Scan specific directory
  %(prog)s -v                        Enable verbose output
  %(prog)s --check                   Fail (exit 2) if regeneration would change files
        """
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=(
            "Output directory for generated docs "
            f"(default: {DEFAULT_OUTPUT_DIR})"
        )
    )

    parser.add_argument(
        "--components", "-c",
        type=Path,
        nargs="+",
        default=None,
        metavar="DIR",
        help="Component directories to scan (default: flowtask/components, plugins/components)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress non-error output"
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Run generation against a temporary directory and exit with code 2 "
            "if the result differs from --output (use in CI / pre-commit)."
        ),
    )

    parser.add_argument(
        "--list-undocumented",
        action="store_true",
        help=(
            "Scan --components paths and print every FlowComponent subclass "
            "whose docstring is missing the ':widths: auto' marker. Useful "
            "for prioritising documentation work. Skips generation entirely."
        ),
    )

    return parser.parse_args(args)


def _compare_doc_trees(committed: Path, fresh: Path) -> List[str]:
    """Compare two documentation trees, ignoring the ``updated_at`` timestamp.

    Walks the freshly-generated tree (``fresh``) and reports any file that is
    missing on the committed side or whose content differs. ``index.json`` is
    compared structurally with ``updated_at`` stripped, since that field is
    purely informational and would otherwise produce false positives on every
    run.

    Args:
        committed: The tree currently on disk (e.g. ``flowtask/documentation/generated``).
        fresh: The tree freshly produced into a temp dir by the generator.

    Returns:
        Sorted list of relative paths (as strings) that differ. Empty list
        means the committed tree is up to date.
    """
    import orjson

    differences: List[str] = []

    if not committed.exists():
        return ["(output directory does not exist)"]

    fresh_files = {p.relative_to(fresh) for p in fresh.rglob("*") if p.is_file()}
    committed_files = {
        p.relative_to(committed) for p in committed.rglob("*") if p.is_file()
    }

    for rel in sorted(fresh_files | committed_files):
        f_path = fresh / rel
        c_path = committed / rel
        if not f_path.exists():
            differences.append(f"unexpected: {rel}")
            continue
        if not c_path.exists():
            differences.append(f"missing:    {rel}")
            continue

        # Normalize index.json — strip the timestamp.
        if rel.name == "index.json":
            try:
                f_data = orjson.loads(f_path.read_bytes())
                c_data = orjson.loads(c_path.read_bytes())
                f_data.pop("updated_at", None)
                c_data.pop("updated_at", None)
                if f_data != c_data:
                    differences.append(f"changed:    {rel}")
                continue
            except orjson.JSONDecodeError:
                pass  # fall through to byte compare

        if f_path.read_bytes() != c_path.read_bytes():
            differences.append(f"changed:    {rel}")

    return differences


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        args: List of command line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    try:
        parsed = parse_args(args)
    except SystemExit as e:
        # argparse calls sys.exit for --help and errors
        return e.code if e.code is not None else 0

    # Setup logging
    if parsed.quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        setup_logging(parsed.verbose)

    logger = logging.getLogger(__name__)

    try:
        # Get base directory for default paths
        base_dir = get_base_dir()

        # Determine component paths
        if parsed.components is None:
            component_paths = [
                base_dir / "flowtask" / "components",
                base_dir / "plugins" / "components"
            ]
        else:
            component_paths = [Path(p) for p in parsed.components]

        # Log configuration
        if not parsed.quiet:
            logger.info(f"Output directory: {parsed.output}")
            logger.info("Scanning directories:")
            for path in component_paths:
                exists = "exists" if path.exists() else "not found"
                logger.info(f"  - {path} ({exists})")

        # --list-undocumented: print every FlowComponent subclass that is
        # missing the documentation marker. Skips generation.
        if parsed.list_undocumented:
            generator = ComponentDocGenerator(output_dir=parsed.output)
            classes = generator.scan_components(component_paths)
            undocumented = sorted(
                cls.__name__
                for cls in classes
                if not generator._is_documentable(cls)
            )
            if not parsed.quiet:
                logger.info(
                    f"{len(undocumented)} of {len(classes)} components "
                    f"lack the ':widths: auto' marker:"
                )
            for name in undocumented:
                print(name)
            return 0

        # --check: generate in a temp dir and compare; never mutate --output
        if parsed.check:
            with tempfile.TemporaryDirectory(prefix="flowtask-docs-check-") as tmp:
                tmp_out = Path(tmp)
                generator = ComponentDocGenerator(output_dir=tmp_out)
                index = generator.generate(component_paths)
                count = len(index.components)

                diffs = _compare_doc_trees(parsed.output, tmp_out)
                if not parsed.quiet:
                    logger.info(f"Checked documentation for {count} components")
                if diffs:
                    logger.error(
                        "Documentation is out of date. "
                        "Run `flowtask-docs` and commit the result. "
                        "Drift:"
                    )
                    for d in diffs[:50]:
                        logger.error(f"  - {d}")
                    if len(diffs) > 50:
                        logger.error(f"  ... and {len(diffs) - 50} more")
                    return 2
                return 0

        # Create generator and run
        generator = ComponentDocGenerator(output_dir=parsed.output)
        index = generator.generate(component_paths)

        # Print summary
        count = len(index.components)
        if not parsed.quiet:
            logger.info(f"Generated documentation for {count} components")
            logger.info(f"Index written to: {parsed.output / 'index.json'}")

            if count > 0 and parsed.verbose:
                logger.debug("Documented components:")
                for name in sorted(index.components.keys()):
                    logger.debug(f"  - {name}")

        return 0

    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130  # Standard exit code for SIGINT

    except Exception as e:
        logger.error(f"Error: {e}")
        if parsed.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
