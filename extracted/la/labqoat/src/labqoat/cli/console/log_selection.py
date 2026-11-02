"""Bounded raw-log page and producer-time selection controls."""

from collections.abc import Mapping
from datetime import UTC, datetime, timedelta

import click

from labqoat.cli.observation_deadline import ObservationDeadline


class LogSelection:
    """Resolve relative time once so all pages share the same cursor scope."""

    @staticmethod
    def parameters() -> list[click.Parameter]:
        """Expose explicit tail, complete history, attempt and inclusive time boundaries."""
        return [
            click.Option(["-n", "--tail"], type=click.IntRange(1, 200), help="The newest N lines (default 100)."),
            click.Option(
                ["--all"],
                is_flag=True,
                help="Every line from the start, page by page; can be thousands. Combine with --grep or --level.",
            ),
            click.Option(["--attempt"], default=None, help="Only this attempt's lines."),
            click.Option(
                ["--since"], callback=LogSelection.time, help="From a time or age, such as 10m or 2026-10-24T12:00Z."
            ),
            click.Option(["--until"], callback=LogSelection.time, help="Up to a time or age."),
        ]

    @staticmethod
    def time(_ctx: click.Context, _param: click.Parameter, value: str | None) -> str | None:
        """Normalize an ISO timestamp or relative duration to one timezone-aware UTC bound."""
        if value is None:
            return None
        try:
            instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            seconds = ObservationDeadline.parse(value)
            instant = datetime.now(UTC) - timedelta(seconds=float(seconds or 0))
        if instant.tzinfo is None:
            raise click.BadParameter("Include a UTC offset or Z in timestamps.")
        return instant.astimezone(UTC).isoformat()

    @staticmethod
    def query(values: Mapping[str, object]) -> dict[str, object]:
        """Prefer explicit legacy page limits; default to the latest hundred selected records."""
        if values.get("all") and values.get("tail"):
            raise click.UsageError("--all and --tail cannot be combined.")
        result = {key: values[key] for key in ("attempt", "since", "until") if values.get(key)}
        if not values.get("follow"):
            result["direction"] = "newer" if values.get("all") or values.get("limit") else "older"
            result["limit"] = values.get("tail") or values.get("limit") or 100
        return result
