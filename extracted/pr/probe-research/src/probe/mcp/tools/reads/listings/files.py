"""browse mode=files: one file row (the Shared folder or one workspace's files)."""

from __future__ import annotations
from .....shared.reads.search_contract import EntityType
from probe.mcp.tools.reads.browse import _annotate


class FileRowsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    #: File fields a Shared/workspace row keeps.
    _FILE_ROW_FIELDS = (
        "id",
        "name",
        "kind",
        "size_bytes",
        "content_type",
        "status",
        "created_at",
    )

    def _file_row(self, row: dict) -> dict:
        # No `notes`: files no longer carry notes (an older server may still
        # send one, which is not shown).
        node = {key: row.get(key) for key in self._FILE_ROW_FIELDS}
        return _annotate(node, EntityType.ARTIFACT, api_base_url=self._api_base_url)
