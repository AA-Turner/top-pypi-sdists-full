"""FilingMixin, Client's methods: the one read a run's project is picked from, by an agent
(`probe project pick`) or the terminal picker, agent-prompt install D22 (twin: app/projects/filing)."""

from __future__ import annotations

from typing import Any

#: The server's caps on the two query values (`app/projects/filing/router.py`).
REMOTE_MAX_LENGTH = 2048
MATCH_MAX_LENGTH = 200


class FilingMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def fetch_filing_candidates(self, *, remote: str | None = None, match: str | None = None) -> dict:
        """``GET /v1/filing/candidates``: every project this credential can see, up to 200
        (``truncated`` past that), those with runs from ``remote``'s GitHub repo first, then
        the most recently active; the top 20 carry up to 5 open experiments each.

        ``remote`` is a git remote URL, scrubbed of credentials here (the query string lands
        in access logs); one past the server's cap is left out. ``match`` narrows by words
        in the slug, name and description."""
        # Here, not at import: the code-capture package is large, and every Client loads this module.
        from ....capture.code.git_remote import _scrub_remote

        query: dict[str, Any] = {}
        scrubbed = _scrub_remote(remote)
        if scrubbed and len(scrubbed) <= REMOTE_MAX_LENGTH:
            query["remote"] = scrubbed
        if match and match.strip():
            query["match"] = match.strip()[:MATCH_MAX_LENGTH]
        return self.transport.get("/v1/filing/candidates", params=query)
