"""Project Management CLI commands for Plato simulator workflow.

This module re-exports from plato.cli.pm for backwards compatibility.
"""

# Re-export from main CLI for backwards compatibility
from plato.cli.pm import (
    list_app,
    pm_app,
    review_app,
    submit_app,
)

__all__ = ["pm_app", "list_app", "review_app", "submit_app"]
