"""data catalog views: a dataset and its versions, a checkpoint and its saves, the provenance walk."""

from __future__ import annotations
from typing import Any
from ....sdk import errors
from ....shared.reads.search_contract import (
    MissingMarker,
    ProvenanceDirection)
from ...source.catalog import CATALOG_NO_MATCH
from probe.mcp.tools.view import _Req, _ViewData
#: GET /v1/provenance's depth bound (C4): default 4, at most 8 hops.
_PROVENANCE_DEFAULT_DEPTH = 4
_PROVENANCE_MAX_DEPTH = 8


class CatalogViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    # -- the data catalog (C4) ----------------------------------------------

    #: A version's heavy parts, left to `view="versions"`: the frozen step
    #: facts carry up to 64 KiB of config, and the users lists are the reverse
    #: walk. The card counts them instead.
    _CARD_VERSION_OMIT = frozenset({"meta", "step", "users", "checks"})
    #: Kept on the card even when null: "no producer" and "no preview sample"
    #: are answers, and a dropped key reads as a field this server never sends.
    _CARD_VERSION_EXPLICIT = ("producer", "preview_artifact_id")

    @staticmethod
    def _catalog_no_match(entity: dict) -> _ViewData:
        """The dataset exists and the version asked for does not -- the reuse
        check's no_match, never absence: pin a version that exists, or register
        the next one of the SAME name. `highest_version` rides the payload so a
        tight budget cannot cut the ceiling the answer is about."""
        found = entity[CATALOG_NO_MATCH]
        versions = sorted(found.get("versions") or [])
        payload: dict[str, Any] = {
            "requested": entity.get("ref"),
            "satisfied_by": None,
            "highest_version": versions[-1] if versions else None,
            "version_count": len(versions),
            "versions": versions,
        }
        if found.get("message"):
            payload["message"] = found["message"]
        return _ViewData(payload=payload, no_match=True)

    @staticmethod
    def _dataset_version(entity: dict, ref: str | None) -> dict | None:
        """The version the ref selected (`@<N>` / `@v<N>`), else the latest:
        the server's `selected`, which it resolved and sends even when that
        version falls outside the versions list's cap.

        An older server sends no `selected`; then the version is found in the
        list (display only: a selector this does not read, or a version past
        the cap, shows the latest)."""
        selected = entity.get("selected")
        if isinstance(selected, dict):
            return selected
        versions = [v for v in entity.get("versions") or [] if isinstance(v, dict)]
        if not versions:
            return None
        selector = (ref or "").partition("@")[2].strip().lower().removeprefix("v")
        if selector.isdigit():
            for version in versions:
                if version.get("n") == int(selector):
                    return version
        return versions[0]

    def _view_dataset_card(self, entity: dict, request: _Req) -> _ViewData:
        """The entry and ONE version -- the one the ref named, else the latest --
        with its heavy lists counted, not listed."""
        versions = entity.get("versions") or []
        chosen = self._dataset_version(entity, request.ref)
        payload: dict[str, Any] = {"version_count": len(versions)}
        if "versions_truncated" in entity:
            # The list stopped at the server's cap: `version_count` is a floor.
            payload["versions_truncated"] = bool(entity["versions_truncated"])
        if chosen is not None:
            shown = {
                key: value
                for key, value in chosen.items()
                if key not in self._CARD_VERSION_OMIT
                and (value is not None or key in self._CARD_VERSION_EXPLICIT)
            }
            users = chosen.get("users")
            if isinstance(users, dict):
                # The server's exact count when it sends one (the list is capped).
                stored = users.get("stored_count")
                shown["users"] = {
                    "stored": stored if isinstance(stored, int) else len(users.get("stored") or []),
                    **({"truncated": True} if users.get("truncated") else {}),
                }
            if isinstance(chosen.get("checks_count"), int):
                shown["checks"] = chosen["checks_count"]
            elif isinstance(chosen.get("checks"), list):
                shown["checks"] = len(chosen["checks"])
            payload["version"] = shown
        return _ViewData(payload=payload)

    def _view_dataset_versions(self, entity: dict, request: _Req) -> _ViewData:
        """Every version, newest first, whole: producer, frozen step facts,
        change note, sources, users, composition -- up to the server's cap,
        which `versions_truncated` says was reached."""
        payload = (
            {"versions_truncated": bool(entity["versions_truncated"])}
            if "versions_truncated" in entity
            else {}
        )
        return _ViewData(
            payload=payload, rows=list(entity.get("versions") or []), rows_key="versions"
        )

    def _view_checkpoint_card(self, entity: dict, request: _Req) -> _ViewData:
        """The checkpoint's Overview read: its facts ride `entity`; the metrics
        at its step, what it was trained on and who used it ride here. The
        run's other saves are `view="versions"`."""
        return _ViewData(
            payload={
                key: entity[key]
                for key in ("at_step", "inputs_at_save", "inputs_source", "used_by")
                if key in entity
            }
        )

    def _view_checkpoint_saves(self, entity: dict, request: _Req) -> _ViewData:
        """The run's saves as the checkpoint read pages them. Past that page
        the rest is a browse listing, which pages; said, never implied."""
        saves = list(entity.get("saves") or [])
        if not entity.get("saves_next_cursor"):
            return _ViewData(rows=saves, rows_key="saves")
        run = entity.get("run") if isinstance(entity.get("run"), dict) else {}
        run_ref = run.get("ref") or (f"run:{run['id']}" if run.get("id") else None)
        payload = (
            {"more_saves": f'browse(mode="checkpoints", run="{run_ref}")'} if run_ref else {}
        )
        return _ViewData(
            payload=payload,
            rows=saves,
            rows_key="saves",
            missing=[MissingMarker.SAVES_BEYOND_SERVER_PAGE],
        )

    def _view_catalog_lineage(self, entity: dict, request: _Req) -> _ViewData:
        """The provenance walk from a dataset version, source or checkpoint:
        typed nodes (sources included) and edges with roles, provenance and
        the basis of a derived one; `truncated` and `hidden` say what the
        bounds left out. `steps=true` is the methods view instead: the upstream
        chain as ordered steps, source first.

        Rooted at the RESOLVED ref (the version the card shows, `checkpoint:
        <uuid>` for a `@best`), so a version registered between the two reads
        cannot move the walk off the thing the caller is looking at."""
        options = request.filters
        chosen = self._dataset_version(entity, request.ref)
        root = str((chosen or {}).get("ref") or entity.get("ref") or request.ref)
        steps = options.get("steps")
        if steps is not None and not isinstance(steps, bool):
            raise errors.ValidationError("view_options.steps must be true or false", status=422)
        if steps:
            shaping = sorted(key for key in ("direction", "depth") if key in options)
            if shaping:
                raise errors.ValidationError(
                    f"view_options.steps is the upstream methods view and takes no "
                    f"{' or '.join(shaping)}; drop steps for the graph",
                    status=422,
                )
            return _ViewData(payload=self.source.provenance_steps(root))
        direction = options.get("direction", ProvenanceDirection.UPSTREAM)
        try:
            direction = ProvenanceDirection(direction)
        except ValueError:
            raise errors.ValidationError(
                f"view_options.direction must be one of {[d.value for d in ProvenanceDirection]}, "
                f"not {direction!r}",
                status=422,
            ) from None
        depth = options.get("depth", _PROVENANCE_DEFAULT_DEPTH)
        try:
            depth = None if isinstance(depth, bool) else int(depth)
        except (TypeError, ValueError):
            depth = None
        if depth is None or not 1 <= depth <= _PROVENANCE_MAX_DEPTH:
            raise errors.ValidationError(
                f"view_options.depth must be an integer from 1 to {_PROVENANCE_MAX_DEPTH}",
                status=422,
            )
        return _ViewData(
            payload=self.source.provenance(root, direction=direction.value, depth=depth)
        )
