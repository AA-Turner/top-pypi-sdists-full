"""PanesMixin, Client's methods: a project's or experiment's panes, the visuals an agent writes, the
data their recipes read, and which pane is a project's canvas preview (twin: app/projects/panes)."""

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
#: What a server without the check route (404/405) is told: a check never falls back to a PUT, which saves (O1).
_CANNOT_CHECK = "this server can't check a pane without saving it; upgrade the server"
#: The server feature (`/v1/server/features`) and team switch (`/v1/teams/features`) previews need.
PROJECT_PREVIEWS_FEATURE = "project_previews"
#: The server's refusal code for a team without the switch (`pane_api.json` preview_error_codes).
PROJECT_PREVIEWS_OFF = "project_previews_off"
#: What a server without previews is told: an older one would save a `preview` push as a plain pane.
_PREDATES_PREVIEWS = "this Probe server has no project previews yet; upgrade the server"
#: What a team without the switch is told, before anything is sent.
PREVIEWS_OFF_MESSAGE = "project previews are not on for this team: skip the preview; nothing was sent"
#: What a failed read of the team's switches is told: not "off", so the preview is tried again later.
PREVIEWS_UNKNOWN_MESSAGE = "could not check whether project previews are on for this team; nothing was sent: try again later"
#: Refusals of the team-switch read that say what is wrong themselves (a refused key or scope, a
#: workspace limit, a too-old CLI): passed on as they are, since another try would not help.
_SAYS_WHY = (errors.AuthError, errors.ScopeError, errors.ValidationError, errors.ClientTooOldError,
             errors.ServerRefusedError)
#: What a push with `is_preview=True` asks the server to do (`PanePut.preview`).
_PREVIEW_AUTO = "auto"


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
        is_preview: bool = False,
    ) -> dict:
        """``PUT .../panes/{slug}``: save a pane, its whole HTML and recipe. Upserts by slug and the
        last write wins, so saving the same pane again (each run of a sweep) is harmless.
        ``title`` left out is the slug for a new pane, and a re-push keeps the current title;
        ``position`` 0 is first (left out: a new pane goes last, a saved one keeps its place). ``ValidationError`` (422 ``pane_refused``) names the page rule
        the HTML broke (a newer server's ``detail["violations"]`` lists every one, with its line); ``ConflictError`` (409 ``too_many_panes``) at 8 panes. A newer server's answer
        also says ``replaced`` (with ``previous_updated_at``) when the slug was saved before.
        ``is_preview=True`` also makes it the project's canvas preview, in one step and only if nobody
        else chose one (the answer's ``preview``); a refusal (409 ``preview_opted_out``,
        ``preview_chosen``, ``pane_taken``) saves nothing. It needs a server and team with previews,
        checked before anything is sent."""
        body = _build_pane_body(html, recipe, title, position, is_preview)
        if is_preview:
            self.require_project_previews()
        scope_id = self._resolve_pane_scope(scope)
        with _explain_old_server():
            return self.transport.put(f"/v1/projects/{scope_id}/panes/{_quote(slug)}", body)

    def check_pane(
        self,
        scope: str,
        slug: str,
        html: str,
        recipe: Mapping[str, Any],
        *,
        title: str | None = None,
        position: int | None = None,
        is_preview: bool = False,
    ) -> dict:
        """``POST .../panes/{slug}/check``: the checks a save runs, with nothing saved; every problem at
        once, ``{violations: [{line, rule, text}], ...}``. A server without the route (404 or 405)
        raises ``CapabilityUnavailable``, never a PUT in its place: that would save the pane.
        ``is_preview=True`` checks the preview rules too, as ``save_pane(is_preview=True)`` would."""
        body = _build_pane_body(html, recipe, title, position, is_preview)
        if is_preview:
            self.require_project_previews()
        scope_id = self._resolve_pane_scope(scope)
        try:
            return self.transport.post(f"/v1/projects/{scope_id}/panes/{_quote(slug)}/check", body, idempotent=True)
        except errors.RosError as exc:
            if _route_absent(exc) or exc.status == 405:
                raise CapabilityUnavailable("pane check", _CANNOT_CHECK) from None
            raise

    def get_pane(self, scope: str, slug: str) -> dict:
        """``GET .../panes/{slug}``: one pane, with its HTML and recipe."""
        scope_id = self._resolve_pane_scope(scope)
        with _explain_old_server():
            return self.transport.get(f"/v1/projects/{scope_id}/panes/{_quote(slug)}")

    def list_panes(self, scope: str) -> list[dict]:
        """``GET .../panes``: the scope's panes, first to last (``position`` order)."""
        return list(self.read_pane_list(scope).get("panes") or [])

    def read_pane_list(self, scope: str) -> dict:
        """``GET .../panes`` whole: ``{panes, preview}``, the panes first to last and a project's canvas
        preview (None for an experiment, or from a server without previews)."""
        scope_id = self._resolve_pane_scope(scope)
        with _explain_old_server():
            return self.transport.get(f"/v1/projects/{scope_id}/panes") or {}

    # -- a project's canvas preview: which of its own panes fills its box ----

    def get_preview(self, project: str) -> dict:
        """``GET /v1/projects/{id}/preview``: ``{project_id, state: none|selected|cleared, pane, set_via,
        is_explicit, updated_at, can_choose}``; ``can_choose`` says whether this caller's
        ``save_pane(is_preview=True)`` would choose now. An experiment is refused (422
        ``not_a_project``): its project holds the preview."""
        project_id = self._resolve_pane_scope(project)
        with _explain_old_previews():
            return self.transport.get(f"/v1/projects/{project_id}/preview")

    def set_preview(self, project: str, slug: str) -> dict:
        """``PUT /v1/projects/{id}/preview {slug}``: make one of the project's own panes its preview by
        hand. The server refuses it (403 ``preview_agent_managed``) while previews are agent-managed:
        ``save_pane(is_preview=True)`` to ``about`` writes the preview."""
        return self._put_preview(project, str(slug))

    def clear_preview(self, project: str) -> dict:
        """``PUT /v1/projects/{id}/preview {slug: null}``: turn previews off for the project; the panes
        stay, and automation never chooses one again."""
        return self._put_preview(project, None)

    def _put_preview(self, project: str, slug: str | None) -> dict:
        self.require_project_previews()
        project_id = self._resolve_pane_scope(project)
        with _explain_old_previews():
            return self.transport.put(f"/v1/projects/{project_id}/preview", {"slug": slug})

    def require_project_previews(self) -> None:
        """Refuse a preview write before anything is sent: a server without previews (it would save a
        plain pane and drop the choice), or a team without the switch (the server answers 403
        ``project_previews_off``; the same code here). A failed read of the team's switches (the
        network, a 5xx) is neither: ServerError PREVIEWS_UNKNOWN_MESSAGE, worth another try; a refusal
        that says why (`_SAYS_WHY`) is passed on as it is."""
        if not self.supports_feature(PROJECT_PREVIEWS_FEATURE):
            raise CapabilityUnavailable("project previews", _PREDATES_PREVIEWS)
        try:
            team = self._fetch_team_features()
        except _SAYS_WHY:
            raise
        except Exception as exc:  # noqa: BLE001 -- a blip is not "off": the agent would skip the preview for good
            raise errors.ServerError(PREVIEWS_UNKNOWN_MESSAGE, status=getattr(exc, "status", None)) from exc
        if PROJECT_PREVIEWS_FEATURE not in team:
            raise _make_previews_off()

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


def _build_pane_body(
    html: str, recipe: Mapping[str, Any], title: str | None, position: int | None, is_preview: bool = False
) -> dict[str, Any]:
    """What a save and a check send: the HTML and recipe, the title and place when named, and
    ``preview: "auto"`` when the pane should also be its project's preview."""
    body: dict[str, Any] = {"html": html, "recipe": dict(recipe)}
    if title is not None:
        body["title"] = title
    if position is not None:
        body["position"] = int(position)
    if is_preview:
        body["preview"] = _PREVIEW_AUTO
    return body


def _make_previews_off() -> errors.ScopeError:
    """The team-switch refusal, typed as the server's (403 ``project_previews_off``), so ``--json``
    prints the same code whichever side refused."""
    from probe.foundation.server_messages.server_messages import ServerMessage

    detail = {"code": PROJECT_PREVIEWS_OFF, "message": PREVIEWS_OFF_MESSAGE}
    error = errors.ScopeError(PREVIEWS_OFF_MESSAGE, status=403, detail=detail)
    error.server_message = ServerMessage(text=PREVIEWS_OFF_MESSAGE, status=403, code=PROJECT_PREVIEWS_OFF)
    return error


def _quote(segment: str) -> str:
    """One path segment, `/` and all escaped: a slug never reaches another route. An empty one would
    reach no route at all, which reads as a server without panes, so it is refused here."""
    if not str(segment).strip():
        raise errors.ValidationError("name the project or experiment and the pane: an id or slug can't be empty")
    return quote(str(segment), safe="")


@contextmanager
def _explain_old_previews() -> Iterator[None]:
    """A route-absent 404 on the preview route said as a server older than previews."""
    try:
        yield
    except errors.NotFoundError as exc:
        if _route_absent(exc):
            raise CapabilityUnavailable("project previews", _PREDATES_PREVIEWS) from None
        raise


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
