"""Usage manager (IstariAdmin surface).

``Usage`` provides access to customer usage metrics.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from istari_digital_client.sdk._base import _Manager


class Usage(_Manager):
    """Read usage and billing metrics (storage, consumption, cost).

    Aliases: usage billing consumption cost spend


    Reached via ``admin.usage``. Provides read-only access to usage data
    for billing and monitoring purposes.

    Usage::

        from datetime import date

        # Get usage metrics for a date range
        metrics = admin.usage.metrics(
            start=date(2024, 1, 1),
            end=date(2024, 1, 31),
        )
        print(f"Storage used: {metrics.storage_bytes}")
    """

    def metrics(self, *, start: date, end: date) -> Any:
        """Get usage and billing metrics (storage, consumption) for a date range.

        Aliases: usage billing consumption cost spend


        Args:
            start: Start date (YYYY-MM-DD).
            end: End date (YYYY-MM-DD).

        Returns:
            Usage metrics for the specified date range.
        """
        return self._call(
            self._engine.v2_api.customer_usage_metrics,
            start=start,
            end=end,
        )
