"""browse mode=runs: one run row (the lab's runs, newest first)."""

from __future__ import annotations
from ....shared.reads.search_contract import EntityType
from probe.mcp.tools.browse import _annotate


class RunRowsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    #: Run fields a flat run row keeps: identity, state, where it is filed, and
    #: when. Metrics and config are other reads (`metrics`, `entity`).
    _RUN_ROW_FIELDS = (
        "id",
        "slug",
        "name",
        "status",
        "project_id",
        "experiment_id",
        "group_id",
        "created_at",
        "started_at",
        "ended_at",
        "updated_at",
    )

    #: Excerpt length for a row's free text (a run's description) -- the browse
    #: tree's own `description` excerpt, for the same reason.
    _ROW_TEXT_CHARS = 180

    def _run_row(self, row: dict) -> dict:
        node = {key: row.get(key) for key in self._RUN_ROW_FIELDS}
        if row.get("tags"):
            node["tags"] = row["tags"]
        description = row.get("description")
        if isinstance(description, str) and description:
            node["description"] = description[: self._ROW_TEXT_CHARS]
            if len(description) > self._ROW_TEXT_CHARS:
                node["description_truncated"] = True
        return _annotate(node, EntityType.RUN, api_base_url=self._api_base_url)
