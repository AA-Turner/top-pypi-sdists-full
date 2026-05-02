"""Config get/set commands."""

from __future__ import annotations

import json
import sys

import click

from ghost_pc.config.schema import GhostConfig


def get_config_value(key: str) -> None:
    """Load config and print a field value."""
    cfg = GhostConfig.load()
    fields = cfg.model_fields

    if key not in fields:
        click.echo(f"Unknown config key: {key}", err=True)
        click.echo(f"Available keys: {', '.join(sorted(fields))}", err=True)
        sys.exit(1)

    value = getattr(cfg, key)

    # Print lists as JSON for easy parsing
    if isinstance(value, list):
        click.echo(json.dumps(value))
    else:
        click.echo(value)


def set_config_value(key: str, value: str) -> None:
    """Load config, update a field, and save."""
    cfg = GhostConfig.load()
    fields = cfg.model_fields

    if key not in fields:
        click.echo(f"Unknown config key: {key}", err=True)
        click.echo(f"Available keys: {', '.join(sorted(fields))}", err=True)
        sys.exit(1)

    field_info = fields[key]
    field_type = field_info.annotation

    # Coerce the value to the right type
    try:
        if field_type is bool:
            coerced = value.lower() in ("true", "1", "yes")
        elif field_type is int:
            coerced = int(value)
        elif field_type == list[str]:
            # Accept comma-separated or JSON array
            if value.startswith("["):
                coerced = json.loads(value)
            else:
                coerced = [v.strip() for v in value.split(",") if v.strip()]
        else:
            coerced = value
    except (ValueError, json.JSONDecodeError) as exc:
        click.echo(f"Invalid value for {key}: {exc}", err=True)
        sys.exit(1)

    setattr(cfg, key, coerced)
    cfg.save()
    click.echo(f"{key} = {getattr(cfg, key)}")
