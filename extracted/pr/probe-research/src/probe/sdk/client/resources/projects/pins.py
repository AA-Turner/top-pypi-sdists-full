"""PinsMixin, Client's methods: pin a view to the top of a project's page for the whole team, list and
unpin them; the views a coding agent may pin (twin: app/projects/pins)."""

from __future__ import annotations
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import quote

from probe.generated.pins import MAX_METRIC_KIND_CHARS, PinAnchorKind, PinKind, PinMetricKind

from .... import errors
from ....errors import CapabilityUnavailable

#: The feature `GET /v1/server/features` lists on a server with the pins routes.
PINS_FEATURE = "pins"
#: What a server without them is told (a 404 on the route reads like an unknown project).
_PREDATES_PINS = "This Probe server doesn't support pins yet."


@dataclass(frozen=True)
class PinScope:
    """Where a view lives, as the caller named it: its project (which holds the pin) and the anchor,
    the project itself or one of its experiments."""

    name: str
    project_id: str
    anchor_kind: PinAnchorKind
    anchor_id: str

    def to_anchor(self) -> dict[str, str]:
        """The ref's `anchor`: `{kind, id}`."""
        return {"kind": self.anchor_kind.value, "id": self.anchor_id}


class PinnedView:
    """A view to pin (the dashboard's `ViewRef`): each kind builds its ref for the scope it is on."""

    def build_ref(self, client: Any, scope: PinScope) -> dict[str, Any]:
        """The ref `POST .../pins` takes for this view on `scope`."""
        raise NotImplementedError


@dataclass(frozen=True)
class PaneView(PinnedView):
    """A pane on the scope, by its slug (the pin keeps the pane's id: a rename of the slug keeps it).
    ``pane_id``, when you hold it (``save_pane`` returns it), pins that pane without reading it again."""

    slug: str
    pane_id: str | None = None

    def build_ref(self, client: Any, scope: PinScope) -> dict[str, Any]:
        if self.pane_id:
            return {"kind": PinKind.PANE.value, "pane_id": str(self.pane_id)}
        try:
            pane = client.get_pane(scope.anchor_id, self.slug)
        except errors.NotFoundError:
            raise errors.NotFoundError(f"no pane {self.slug!r} on {scope.name!r}") from None
        return {"kind": PinKind.PANE.value, "pane_id": str(pane["id"])}


@dataclass(frozen=True)
class ChartView(PinnedView):
    """One metric's line chart over the scope's runs. `kind` is the metric's, as it was logged:
    `model` (what your code logs), `hardware` (Probe's `hw/`), `system` (a W&B system rail) or your
    own (sent lowercase, as the server keys it). The server checks a run there draws it."""

    metric: str
    kind: str = PinMetricKind.MODEL.value

    def __post_init__(self) -> None:
        if not str(self.metric).strip():
            raise ValueError("name the chart's metric key, e.g. 'train/loss'")
        if not 0 < len(str(self.kind).strip()) <= MAX_METRIC_KIND_CHARS:
            raise ValueError(f"a chart's metric kind is 1 to {MAX_METRIC_KIND_CHARS} characters, e.g. 'model'")

    def build_ref(self, client: Any, scope: PinScope) -> dict[str, Any]:
        return {"kind": PinKind.METRIC_CHART.value, "anchor": scope.to_anchor(),
                "metric_kind": str(self.kind).strip().lower(), "metric_key": self.metric}


@dataclass(frozen=True)
class KeyMetricsView(PinnedView):
    """The scope's whole Key metrics block."""

    def build_ref(self, client: Any, scope: PinScope) -> dict[str, Any]:
        return {"kind": PinKind.KEY_METRICS.value, "anchor": scope.to_anchor()}


@dataclass(frozen=True)
class ParallelView(PinnedView):
    """The scope's parallel coordinates plot."""

    def build_ref(self, client: Any, scope: PinScope) -> dict[str, Any]:
        return {"kind": PinKind.PARALLEL_COORDINATES.value, "anchor": scope.to_anchor()}


@dataclass(frozen=True)
class Pin:
    """One pin as the server keeps it (`PinOut`): the view's ref and where it lives, oldest first. A
    pane pin also names its pane's slug."""

    id: str
    project_id: str
    kind: str
    ref: Mapping[str, Any] = field(hash=False)  # a dict: hashing a Pin hashes the rest
    ref_key: str
    anchor_kind: str
    anchor_id: str
    position: int
    created_at: str
    pane_slug: str | None = None

    @classmethod
    def from_answer(cls, answer: Mapping[str, Any]) -> Pin:
        """A pin from the server's JSON."""
        anchor = answer.get("anchor") or {}
        return cls(
            id=str(answer["id"]), project_id=str(answer["project_id"]), kind=str(answer["kind"]),
            ref=dict(answer.get("ref") or {}), ref_key=str(answer.get("ref_key") or ""),
            anchor_kind=str(anchor.get("kind") or ""), anchor_id=str(anchor.get("id") or ""),
            position=int(answer.get("position") or 0), created_at=str(answer.get("created_at") or ""),
            pane_slug=answer.get("pane_slug"),
        )

    def to_dict(self) -> dict[str, Any]:
        """The server's shape again, for printing."""
        return {
            "id": self.id, "project_id": self.project_id, "kind": self.kind, "ref": dict(self.ref),
            "ref_key": self.ref_key, "anchor": {"kind": self.anchor_kind, "id": self.anchor_id},
            "pane_slug": self.pane_slug, "position": self.position, "created_at": self.created_at,
        }


class PinsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- pins (a project's Pinned area, shared by the team) ---------------------
    #
    # A pin lives on a PROJECT (`/v1/projects/{P}/pins`); a view on one of its
    # experiments is pinned there with that experiment as its anchor. `scope` is
    # a project or experiment slug, or its uuid (`id:<uuid>` too). Pin only
    # when the researcher asks: pins sit at the top of the project for everyone.

    def add_pin(self, scope: str, view: PinnedView) -> Pin:
        """``POST /v1/projects/{P}/pins``: pin ``view`` (a ``PaneView``, ``ChartView``,
        ``KeyMetricsView`` or ``ParallelView``) of ``scope`` to its project. Pinning a view again
        returns its existing pin. ``ValidationError``: 422 ``pins_full`` at the cap (24),
        ``unknown_metric`` for a chart no run there draws; ``NotFoundError`` for a pane, project or
        experiment that isn't there."""
        if not isinstance(view, PinnedView):
            raise TypeError("pin a PaneView, ChartView, KeyMetricsView or ParallelView")
        self._require_pins()
        found = self._resolve_pin_scope(scope)
        ref = view.build_ref(self, found)
        answer = self.transport.post(f"/v1/projects/{found.project_id}/pins", {"ref": ref}, idempotent=True)
        return Pin.from_answer(answer)

    def list_pins(self, project: str) -> list[Pin]:
        """``GET /v1/projects/{P}/pins``: the project's pins, oldest first (an experiment names its
        project's)."""
        self._require_pins()
        project_id = self._resolve_pin_scope(project).project_id
        answer = self.transport.get(f"/v1/projects/{project_id}/pins")
        return [Pin.from_answer(row) for row in (answer or {}).get("pins") or []]

    def remove_pin(self, project: str, pin_id: str) -> None:
        """``DELETE /v1/projects/{P}/pins/{pin_id}``: unpin; the view itself stays. ``NotFoundError``
        (``pin_not_found``) for a pin that isn't on the project."""
        bare = str(pin_id).strip().removeprefix("id:")
        if not _is_uuid(bare):
            raise errors.ValidationError(f"a pin id is a uuid (`probe pin list` prints them), not {pin_id!r}")
        self._require_pins()
        project_id = self._resolve_pin_scope(project).project_id
        self.transport.delete(f"/v1/projects/{project_id}/pins/{quote(bare, safe='')}")

    def _require_pins(self) -> None:
        """Ask the server first: a 404 on the pins route can't be told from an unknown project."""
        if not self.supports_feature(PINS_FEATURE):
            raise CapabilityUnavailable(PINS_FEATURE, _PREDATES_PINS)

    def _resolve_pin_scope(self, scope: str) -> PinScope:
        """The project that holds a scope's pins and the anchor its views live on: one
        ``GET /v1/scopes``: by id for ``id:<uuid>`` or a bare uuid in its printed form (`_id_ref`;
        a 32-hex slug stays a slug), else by slug (``slug:`` taken off, whatever follows)."""
        name = str(scope).strip()
        is_id = _id_ref(name)
        bare = name.removeprefix("id:") if is_id else name.removeprefix("slug:")
        if not bare:
            raise errors.ValidationError("name the project or experiment: a slug or id:<uuid>")
        try:
            if is_id:
                found = self.get_scope(quote(bare, safe=""))
            else:
                found = self.get_scope_by_slug(bare)
        except errors.NotFoundError:
            raise errors.NotFoundError(f"no project or experiment {name!r}") from None
        try:
            anchor_kind = PinAnchorKind(found.get("kind"))
        except ValueError:
            raise errors.ValidationError(f"{name!r} is a {found.get('kind')}: name a project or an experiment") from None
        return PinScope(name=name, project_id=str(found["project_id"]), anchor_kind=anchor_kind,
                        anchor_id=str(found["id"]))


from probe.sdk.client.ids import _id_ref, _is_uuid  # noqa: E402 -- pieces need each other; the front door loads this one first
