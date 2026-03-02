"""Plato CLI - Backward compatibility wrapper.

This module re-exports from the new cli package location.
"""

# Re-export everything from the new location
from plato.v1.cli import app, cli, main

__all__ = ["app", "main", "cli"]

if __name__ == "__main__":
    main()
