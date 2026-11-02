"""Timezone-aware ISO-8601 Click parameter validation."""

from __future__ import annotations

from datetime import datetime

import click


class TimezoneType(click.ParamType[str]):
    """Accept ISO-8601 timestamps only when they include an offset."""

    name = "timezone-aware ISO-8601 timestamp"

    def convert(
        self,
        value: object,
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> str:
        """Validate one timestamp while preserving its original spelling."""
        if not isinstance(value, str):
            self.fail("must be text", param, ctx)
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            self.fail("must be a valid ISO-8601 timestamp", param, ctx)
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            self.fail("must include a UTC offset", param, ctx)
        return value
