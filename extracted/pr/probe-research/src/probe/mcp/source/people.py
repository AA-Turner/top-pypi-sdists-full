"""people reads: the team roster (`GET /v1/people`) and the person and time filters every authored listing takes."""

from __future__ import annotations
import json
import time
from typing import Any
from dataclasses import dataclass, fields

from ...sdk import errors
from ...sdk.client import PEOPLE_FILTERS_FEATURE, SEARCH_PEOPLE_FILTERS_FEATURE
from ...shared.reads.search_contract import BrowseOrder

#: How long a server's "no such feature" answer is believed before asking again. The SDK caches its answer
#: for the client's life, and a hosted client lives as long as its pod: without this, a feature switched on
#: after the MCP started (`search_people_filters`, D12) stayed refused until the next MCP deploy.
_FEATURE_RECHECK_SECONDS = 60.0


@dataclass(frozen=True)
class PeopleFilters:
    """`owner`, `since`, `until` and `order="recent"` on one listing, passed to its route as given: the server
    matches the person and reads the dates (people and time filters D2). Empty fields are not sent."""

    owner: str | None = None
    since: str | None = None
    until: str | None = None
    order: str | None = None

    @property
    def is_set(self) -> bool:
        return any(getattr(self, field.name) for field in fields(self))

    @property
    def is_recent(self) -> bool:
        """Newest activity first: the listing's own keyset order no longer holds."""
        return self.order == BrowseOrder.RECENT

    def to_query(self) -> dict[str, str]:
        """The route's query params: only the filters given."""
        return {field.name: value for field in fields(self) if (value := getattr(self, field.name))}


#: The headers a route whose body is a bare list answers its owner echo in (`app/accounts/people` S1).
OWNER_MATCHED_HEADER = "X-Probe-Owner-Matched"
UNOWNED_COUNT_HEADER = "X-Probe-Unowned-Count"


#: The header a bare-list route answers a name `query`'s one-line note in (`app/shared/name_match.py`).
QUERY_NOTE_HEADER = "X-Probe-Query-Note"


def read_query_note_header(headers: Any) -> dict[str, str]:
    """`{query_note}` from a bare-list route's headers (ASCII JSON); a malformed one is left out."""
    try:
        note = json.loads(headers.get(QUERY_NOTE_HEADER) or "null")
    except ValueError:
        return {}
    return {"query_note": note} if isinstance(note, str) and note else {}


def read_owner_headers(headers: Any) -> dict[str, Any]:
    """`{owner_matched, unowned_count}` from a bare-list route's headers; a malformed one is left out."""
    echo: dict[str, Any] = {}
    try:
        matched = json.loads(headers.get(OWNER_MATCHED_HEADER) or "null")
    except ValueError:
        matched = None
    if isinstance(matched, list):
        echo["owner_matched"] = matched
    count = headers.get(UNOWNED_COUNT_HEADER)
    if isinstance(count, str) and count.isdigit():
        echo["unowned_count"] = int(count)
    return echo


class PeopleReadsMixin:
    """Part of ResearchOSSource: its methods run with `self` the ResearchOSSource; compose() folds them into ResearchOSSource."""

    def fetch_people(self, query: str | None = None) -> list[dict]:
        """``GET /v1/people``: every active teammate, `{user_id, name, email, role, joined_at}`; with `query`,
        the ones it names, best first. No feature switch: an older server ignores `query` and lists everyone."""
        answer = self.client.transport.get("/v1/people", params={"query": query} if query else None)
        return [row for row in (answer or {}).get("people") or [] if isinstance(row, dict)]

    def has_feature(self, name: str) -> bool:
        """Whether the server declares `name` in `GET /v1/server/features`. A "no" is asked again after
        `_FEATURE_RECHECK_SECONDS`; a "yes" is kept (a server does not lose a feature mid-deploy)."""
        cached = getattr(self.client, "_server_features_cache", None)
        now = time.monotonic()
        if cached is not None and name not in cached:
            if now - getattr(self, "_features_read_at", float("-inf")) >= _FEATURE_RECHECK_SECONDS:
                self.client._server_features_cache = None
                cached = None
        if cached is None:
            self._features_read_at = now
        return self.client.supports_feature(name)

    def require_people_filters(self, asked: list[str], *, is_search: bool = False) -> None:
        """Refuse `asked` (argument or mode names) when the server does not declare the feature behind them:
        an older server drops an unknown filter and answers everything, which reads as that person's work."""
        if not asked:
            return
        feature = SEARCH_PEOPLE_FILTERS_FEATURE if is_search else PEOPLE_FILTERS_FEATURE
        if self.has_feature(feature):
            return
        tool = "search" if is_search else "browse"
        raise errors.CapabilityUnavailable(
            feature,
            f"{tool}: {', '.join(asked)} is not available on this server yet. Leave "
            f"{'it' if len(asked) == 1 else 'them'} out; the rest of {tool} works.",
        )
