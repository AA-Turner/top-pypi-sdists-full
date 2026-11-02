"""Read credential values from a direct argument, environment, or files."""

import os
from pathlib import Path
import click


class SecretInput:
    """Collect credential values without exposing them in diagnostic messages."""

    @staticmethod
    def read(name: str, value: str | None, environment: tuple[str, ...], files: tuple[str, ...]) -> dict[str, str]:
        """Map a direct value to its name or collect a bundle from explicit sources."""
        if value is not None:
            if environment or files:
                raise click.UsageError("Use VALUE by itself, or use --env/--file sources.")
            return {name: value}
        values: dict[str, str] = {}
        for key in environment:
            if key not in os.environ:
                raise click.UsageError(f"Environment variable {key} is not set.")
            values[key] = os.environ[key]
        for item in files:
            key, separator, path = item.partition("=")
            if not separator or not key or not path:
                raise click.UsageError("Use --file KEY=PATH.")
            values[key] = Path(path).read_text(encoding="utf-8")
        if not values:
            raise click.UsageError("Provide VALUE, --env KEY, or --file KEY=PATH.")
        return values
