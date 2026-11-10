"""PanesMixin, Client's methods: a project's or experiment's panes, the visuals an agent writes, and the
data their recipes read (twin: app/projects/panes)."""

from __future__ import annotations
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from typing import Any
from urllib.parse import quote

from .... import errors
from ....errors import CapabilityUnavailable

#: What a server without the pane routes (a route-absent 404) is told.
_PREDATES_PANES = (
    "this Probe server has no panes yet (PUT/GET /v1/projects/{id}/panes); "
    "upgrade the server, or keep the previous probe release until it is"
)


class PanesMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- panes (agent-written visuals, project and experiment) -----------------
    #
    # `scope` is the project or experiment a pane is filed under: its uuid
    # (`id:<uuid>` too) or its slug. Both kinds are served at
    # `/v1/projects/{id}`. The server checks and resolves everything: the HTML
    # (the page rules), the recipe and the runs; this only carries them.

    def save_pane(
        self,
        scope: str,
        slug: str,
        html: str,
        recipe: Mapping[str, Any],
        *,
        title: str | None = None,
        position: int | None = None,
    ) -> dict:
        """``PUT .../panes/{slug}``: save a pane, its whole HTML and recipe. Upserts by slug and the
        last write wins, so saving the same pane again (each run of a sweep) is harmless.
        ``title`` defaults to the slug; ``position`` 0 is first (left out: a new pane goes last, a
        saved one keeps its place). ``ValidationError`` (422 ``pane_refused``) names the page rule
        the HTML broke; ``ConflictError`` (409 ``too_many_panes``) at 8 panes."""
        body: dict[str, Any] = {"html": html, "recipe": dict(recipe)}
        if title is not None:
            body["title"] = title
        if position is not None:
            body["position"] = int(position)
        scope_id = self._resolve_pane_scope(scope)
        with _explain_old_server():
            return self.transport.put(f"/v1/projects/{scope_id}/panes/{_quote(slug)}", body)

    def get_pane(self, scope: str, slug: str) -> dict:
        """``GET .../panes/{slug}``: one pane, with its HTML and recipe."""
        scope_id = self._resolve_pane_scope(scope)
        with _explain_old_server():
            return self.transport.get(f"/v1/projects/{scope_id}/panes/{_quote(slug)}")

    def list_panes(self, scope: str) -> list[dict]:
        """``GET .../panes``: the scope's panes, first to last (``position`` order)."""
        scope_id = self._resolve_pane_scope(scope)
        with _explain_old_server():
            answer = self.transport.get(f"/v1/projects/{scope_id}/panes")
        return list(answer.get("panes") or [])

    def delete_pane(self, scope: str, slug: str) -> None:
        """``DELETE .../panes/{slug}``: for good (panes keep no versions and no trash)."""
        scope_id = self._resolve_pane_scope(scope)
        with _explain_old_server():
            self.transport.delete(f"/v1/projects/{scope_id}/panes/{_quote(slug)}")

    def read_pane_data(
        self,
        scope: str,
        slug_or_recipe: str | Mapping[str, Any],
        run_ids: Sequence[str] | None = None,
    ) -> dict:
        """A recipe's data, resolved fresh: ``{runs, entries: {<recipe id>: {source, state, rows,
        ...}}, elapsed_ms}``. A slug reads a saved pane's (``GET .../panes/{slug}/data``); a recipe
        dict one not saved yet (``POST .../panes:resolve``), to see its shape while writing it.
        ``run_ids`` binds ``"runs": "scope"`` to those runs (a compare selection), each inside
        the scope; one id may be passed bare."""
        if isinstance(run_ids, str):
            run_ids = [run_ids]
        ids = [str(run_id) for run_id in run_ids] if run_ids else None
        scope_id = self._resolve_pane_scope(scope)
        with _explain_old_server():
            if isinstance(slug_or_recipe, str):
                query = {"run_ids": ",".join(ids)} if ids else None
                slug = _quote(slug_or_recipe)
                return self.transport.get(f"/v1/projects/{scope_id}/panes/{slug}/data", params=query)
            body: dict[str, Any] = {"recipe": dict(slug_or_recipe)}
            if ids:
                body["run_ids"] = ids
            return self.transport.post(f"/v1/projects/{scope_id}/panes:resolve", body, idempotent=True)

    def _resolve_pane_scope(self, scope: str) -> str:
        """The id a project or experiment is served at: its uuid as is (``id:`` dropped), a slug
        through ``GET /v1/scopes?slug=``."""
        ref = str(scope).strip()
        bare = ref.removeprefix("id:")
        if not (ref.startswith("id:") or _is_uuid(bare)):
            found = self.get_scope_by_slug(ref)
            if found.get("kind") not in ("project", "experiment"):
                raise errors.NotFoundError(f"no project or experiment {ref!r}")
            bare = str(found["id"])
        return _quote(bare)


def _quote(segment: str) -> str:
    """One path segment, `/` and all escaped: a slug never reaches another route. An empty one would
    reach no route at all, which reads as a server without panes, so it is refused here."""
    if not str(segment).strip():
        raise errors.ValidationError("name the project or experiment and the pane: an id or slug can't be empty")
    return quote(str(segment), safe="")


@contextmanager
def _explain_old_server() -> Iterator[None]:
    """A route-absent 404 (no pane routes at all) said as a server older than panes."""
    try:
        yield
    except errors.NotFoundError as exc:
        if _route_absent(exc):
            raise CapabilityUnavailable("panes", _PREDATES_PANES) from None
        raise


from probe.sdk.client.ids import _is_uuid  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.server_features import _route_absent  # noqa: E402 -- pieces need each other; the front door loads this one first
