"""browse modes datasets / checkpoints / sources: one catalog row, its identity and whether it is hidden."""

from __future__ import annotations
from typing import Any
from .....shared.reads.search_contract import (
    BrowseMode,
    EntityType)


class CatalogRowsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    #: The entity kind each catalog mode lists (a dataset listing also holds
    #: unregistered `artifact:` rows; their ref says so).
    _CATALOG_ROW_NAMES: dict[BrowseMode, str] = {
        BrowseMode.DATASETS: EntityType.DATASET.value,
        BrowseMode.CHECKPOINTS: EntityType.CHECKPOINT.value,
        BrowseMode.SOURCES: EntityType.SOURCE.value,
    }

    @staticmethod
    def _catalog_row_identity(row: dict) -> str:
        return str(row.get("ref") or row.get("id"))

    @staticmethod
    def _catalog_row_hidden(mode: BrowseMode, row: dict, hidden: frozenset[str]) -> bool:
        """Whether a catalog row is the caller's own session's work: what made
        it is something that session created. A checkpoint's run (saved with no
        run: the project or experiment it is filed at); a dataset's newest
        version's producer -- for an unregistered file, the run that logged it,
        and a registered dataset the session wrote the newest version of is one
        it already knows. A source names no run, so none is a session's work."""
        if mode is BrowseMode.CHECKPOINTS:
            maker = row.get("run") or row.get("project")
        elif mode is BrowseMode.DATASETS:
            latest = row.get("latest")
            producer = latest.get("producer") if isinstance(latest, dict) else None
            maker = producer.get("run") if isinstance(producer, dict) else None
        else:
            return False
        ident = maker.get("id") if isinstance(maker, dict) else None
        return isinstance(ident, str) and ident.lower() in hidden

    @classmethod
    def _catalog_row(cls, mode: BrowseMode, row: dict) -> dict:
        """A catalog row with the two addresses every browse row carries.

        `uuid` is `<kind>:<id>`; `slug` the readable form `entity` also takes:
        `dataset:<name>`, `source:<canonical_key>[@<revision>]`. A run-logged
        dataset file nobody registered is an `artifact:<id>` row (`entity`
        opens it as any file). Null keys are dropped, as on every browse row."""
        kind, _, ident = str(row.get("ref") or "").partition(":")
        if not ident:
            kind = cls._CATALOG_ROW_NAMES[mode]
        row_id = row.get("id") or ident
        out: dict[str, Any] = {"entity_type": kind, "uuid": f"{kind}:{row_id}"}
        if kind == EntityType.DATASET and row.get("name"):
            out["slug"] = f"{EntityType.DATASET.value}:{row['name']}"
        elif kind == EntityType.SOURCE and row.get("canonical_key"):
            revision = row.get("revision")
            out["slug"] = f"{EntityType.SOURCE.value}:{row['canonical_key']}" + (
                f"@{revision}" if revision else ""
            )
        out.update(
            {key: value for key, value in row.items() if value is not None and key not in ("ref", "id")}
        )
        return out
