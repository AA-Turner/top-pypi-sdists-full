"""CLI for generating Flowtask component documentation.

This module provides a command-line interface for generating documentation
from Flowtask component docstrings.

Usage:
    python -m flowtask.documentation.cli [--output DIR] [--components DIR...]

Examples:
    # Generate docs with defaults
    python -m flowtask.documentation.cli

    # Specify output directory
    python -m flowtask.documentation.cli --output ./docs

    # Scan specific directories
    python -m flowtask.documentation.cli -c flowtask/components plugins/components

    # Verbose output
    python -m flowtask.documentation.cli -v
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from .generator import ComponentDocGenerator


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
    base_dir = get_base_dir()

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
        """
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=base_dir / "documentation",
        help="Output directory for generated docs (default: documentation/)"
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

    return parser.parse_args(args)


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
