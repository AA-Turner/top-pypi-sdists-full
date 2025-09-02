"""Using CLI as main entry point."""
import sys

from .cli import cli

sys.exit(cli(sys.argv[1:]))
