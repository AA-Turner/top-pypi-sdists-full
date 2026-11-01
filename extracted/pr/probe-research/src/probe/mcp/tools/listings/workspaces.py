"""browse mode=workspaces: one workspace row and its sort key."""

from __future__ import annotations


class WorkspaceRowsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    #: Postgres `lower()` under the research databases' C collation lowers ASCII
    #: letters only; Python's `str.lower` would also fold `É`, and sort a row
    #: somewhere the route never puts it.
    _ASCII_LOWER = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")

    @classmethod
    def _workspace_key(cls, row: dict) -> tuple[str, str]:
        """The workspace list's own order, `ORDER BY lower(name), id`
        (app/workspaces/router.py). Code-point order on both halves IS the C
        collation's byte order, and a uuid sorts as its lowercase hex."""
        return (
            str(row.get("name") or "").translate(cls._ASCII_LOWER),
            str(row.get("id") or "").lower(),
        )

    @staticmethod
    def _workspace_row(row: dict) -> dict:
        # `workspace_id` IS the argument browse/search take to scope to
        # it, so the row spells its id that way rather than as an entity address:
        # a workspace is a filing location, not something `entity` opens.
        out = {"workspace_id": row.get("id")}
        out.update(
            {
                key: row[key]
                for key in ("name", "slug", "kind", "project_count")
                if row.get(key) is not None
            }
        )
        return out
