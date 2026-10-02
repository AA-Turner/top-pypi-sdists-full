# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ExperimentAssignmentParams", "Context"]


class ExperimentAssignmentParams(TypedDict, total=False):
    token: Required[str]
    """
    The experiment token (`exp_*`) for the experiment settings holding this
    experiment. Available from the dashboard.
    """

    visitor_id: Required[str]
    """
    Stable identifier for the visitor — typically the Ours visitor id from your
    browser cookie, or your own server-side user id if you keep the same id
    consistent across browser and server.
    """

    context: Optional[Context]
    """Optional page context for URL + query-param eligibility.

    Variant bucketing is deterministic on `visitor_id` regardless of context.
    """

    track_impression: Optional[bool]
    """
    When true (default), an `$experiment_impression` event is enqueued and the
    visitor's `experiment_assignments` map is updated. Set to false to read the
    assignment without recording an impression — useful for in-test diagnostics.
    """


class Context(TypedDict, total=False):
    """Optional page context for URL + query-param eligibility.

    Variant bucketing is deterministic on `visitor_id` regardless of context.
    """

    search: Optional[str]
    """The current query string (e.g.

    `?utm_source=meta`). When provided, the experiment's query-param conditions are
    evaluated for eligibility. If omitted, the query string is parsed from `url`.
    """

    url: Optional[str]
    """The current page URL.

    When provided, the experiment's URL patterns are evaluated for eligibility —
    visitors on non-matching URLs are returned `in_experiment: false`. Omit when the
    caller is pre-gating the request.
    """
