"""Report a failed analytics query with the reason its receipt records."""

import re
from typing import ClassVar

from labqoat.cli.output.cli_failure import CliFailure
from labqoat.json_document import JsonDocument


class AnalyticsFailure:
    """Turn a terminal failed query into a failure that says why and what to try."""

    HINTS: ClassVar[dict[str, str]] = {
        "query_timeout": "it ran past the query time limit; filter it, select fewer fields, or read the rows in a run",
        "overloaded": "the query service is busy; send it again shortly",
    }

    @staticmethod
    def raise_for(final: JsonDocument) -> None:
        """Raise when the query failed; a succeeded query passes."""
        if final["status"] != "failed":
            return
        receipt = final.get("receipt")
        error = str(receipt.get("error", "")) if isinstance(receipt, dict) else ""
        reason = error.lstrip(":") if re.fullmatch(r":?[a-z][a-z0-9_]{0,63}", error) else ""
        detail = AnalyticsFailure.HINTS.get(reason, reason)
        message = f"analytics query {final['id']} failed" + (f": {detail}" if detail else "")
        raise CliFailure(message, 1, resource_id=str(final["id"]))
