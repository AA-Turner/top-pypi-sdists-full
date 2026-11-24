"""DecisionsMixin, Client's methods: record, list and remove the choices that changed a project's or an
experiment's work, each linked to what it changed (twin: app/projects/decisions)."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

from probe.foundation.compat.compat import StrEnum

from .... import errors
from ....errors import CapabilityUnavailable

#: The server's 403 code when the team's decisions switch is off (`decisions_customers`).
DECISIONS_OFF = "decisions_off"
#: The server's caps (422 past them), checked here first so the error names the flag.
MAX_TITLE_CHARS = 80
MAX_DETAIL_CHARS = 600
MAX_REJECTED_CHARS = 300
#: What a server that cannot filter decisions is told: it would answer a filtered ask with every row.
_PREDATES_FILTERS = (
    "this Probe server is older than this CLI: update the server, or ask without filters "
    "(no words, --about, --since, --until or --team)"
)


class DecidedBy(StrEnum):
    """Who made the choice: the researcher (chose or approved it) or the agent."""

    RESEARCHER = "researcher"
    AGENT = "agent"


class TargetType(StrEnum):
    """What a decision changed: an experiment (on a project) or a run (on an experiment)."""

    EXPERIMENT = "experiment"
    RUN = "run"


class TargetEffect(StrEnum):
    """How the decision touched its target."""

    STARTED = "started"
    STOPPED = "stopped"
    CHANGED = "changed"
    BASED_ON = "based_on"


@dataclass(frozen=True)
class DecisionTarget:
    """One thing a decision changed: `ref` is an id or slug the server resolves under the scope's project."""

    type: TargetType
    ref: str
    effect: TargetEffect

    @classmethod
    def parse(cls, text: str) -> DecisionTarget:
        """`TYPE:REF=EFFECT` (`run:abc=stopped`) as typed on the command line."""
        head, sep, effect = str(text).strip().rpartition("=")
        kind, colon, ref = head.partition(":")
        if not sep or not colon or not ref.strip():
            raise ValueError(f"{text!r} is not TYPE:REF=EFFECT (e.g. run:<id>=stopped)")
        try:
            target_type = TargetType(kind.strip())
        except ValueError:
            raise ValueError(f"{kind!r} is not a target type: {' | '.join(TargetType)}") from None
        try:
            target_effect = TargetEffect(effect.strip())
        except ValueError:
            raise ValueError(f"{effect!r} is not an effect: {' | '.join(TargetEffect)}") from None
        return cls(type=target_type, ref=ref.strip(), effect=target_effect)

    def to_body(self) -> dict[str, str]:
        return {"type": self.type.value, "ref": self.ref, "effect": self.effect.value}


class DecisionFieldError(ValueError):
    """A `NewDecision` field the server would refuse; `field` names it as the wire does."""

    def __init__(self, field: str, message: str) -> None:
        super().__init__(message)
        self.field = field


@dataclass(frozen=True)
class NewDecision:
    """A decision to record (`POST /v1/projects/{scope}/decisions`): `detail` says why, `rejected` what
    it was chosen over, `follows` the decision it builds on, `evidence` the session event ids behind it."""

    title: str
    detail: str
    decided_by: DecidedBy
    targets: tuple[DecisionTarget, ...]
    rejected: str | None = None
    follows: str | None = None
    also_follows: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, value, cap in (("title", self.title, MAX_TITLE_CHARS), ("detail", self.detail, MAX_DETAIL_CHARS),
                                 ("rejected", self.rejected, MAX_REJECTED_CHARS)):
            if value is not None and len(value) > cap:
                raise DecisionFieldError(name, f"{len(value)} characters; at most {cap}")
        for name, value in (("title", self.title), ("detail", self.detail)):
            if not value.strip():
                raise DecisionFieldError(name, "empty")
        if not self.targets:
            raise DecisionFieldError("targets", "name at least one thing the decision changed")

    def to_body(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "title": self.title,
            "detail": self.detail,
            "decided_by": self.decided_by.value,
            "targets": [target.to_body() for target in self.targets],
        }
        if self.rejected:
            body["rejected"] = self.rejected
        if self.follows:
            body["follows"] = _strip_id_prefix(self.follows)
        if self.also_follows:
            body["also_follows"] = [_strip_id_prefix(ref) for ref in self.also_follows]
        if self.evidence:
            body["evidence"] = list(self.evidence)
        return body


class DecisionsServerTooOld(CapabilityUnavailable):
    """A filtered or team-wide decisions read the server cannot answer: it has no `applied` echo
    (it ignored the filters) or no `GET /v1/decisions` route."""

    def __init__(self) -> None:
        super().__init__("decision filters", _PREDATES_FILTERS)


@dataclass(frozen=True)
class DecisionPage:
    """One page of decisions, oldest first. `applied` echoes the filters the server used (None when
    none were sent); `next_cursor` continues the same read (None at the end)."""

    decisions: list[dict[str, Any]]
    applied: dict[str, Any] | None = None
    next_cursor: str | None = None


def is_decisions_off(exc: BaseException) -> bool:
    """Is this the team switch's 403 (`decisions_off`), in either shape the server may send it?"""
    if not isinstance(exc, errors.RosError) or exc.status != 403:
        return False
    message = getattr(exc, "server_message", None)
    detail = exc.detail
    codes = (
        getattr(message, "code", None),
        detail.get("code") if isinstance(detail, Mapping) else None,
        detail if isinstance(detail, str) else None,
    )
    return DECISIONS_OFF in codes


class DecisionsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client.

    Sent straight, never queued: a refusal (403 `decisions_off`, a 422 on a target) is the answer the
    caller acts on, and the outbox would replay it. The session the write came from rides the request
    headers like every other write (`X-Probe-Agent-Session`)."""

    def add_decision(self, scope_id: str, decision: NewDecision) -> dict[str, Any]:
        """``POST /v1/projects/{scope}/decisions``: the recorded decision, as the server returns it."""
        return self.transport.post(f"/v1/projects/{_quote(scope_id)}/decisions", decision.to_body())

    def list_decisions(
        self,
        scope_id: str | None = None,
        *,
        since: str | None = None,
        until: str | None = None,
        words: str | Sequence[str] | None = None,
        about: str | None = None,
        should_include_experiments: bool = False,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> DecisionPage:
        """One page of decisions, oldest first: a project's or experiment's
        (``GET /v1/projects/{scope}/decisions``), or the team's with no `scope_id` (``GET /v1/decisions``).

        The server filters; this never does. `words`: ANY word in the title or reason. `about`
        (team only): `experiment:<ref>` or `run:<ref>`, decisions filed under it or naming it.
        `should_include_experiments` (a project only): its experiments' decisions too. A filter or the team
        route on a server that cannot honour it (a `limit` or `cursor` included) raises `DecisionsServerTooOld`."""
        query = _build_list_query(since=since, until=until, words=words, about=about,
                                  should_include_experiments=should_include_experiments)
        if about and scope_id is not None:
            raise errors.ValidationError("about reads team-wide: leave out the project or experiment")
        if should_include_experiments and scope_id is None:
            raise errors.ValidationError("should_include_experiments needs a project")
        if cursor:
            query["cursor"] = cursor
        if limit is not None:
            query["limit"] = int(limit)
        # Any param sent, `limit` and `cursor` too, gets `applied` back: an older server ignores them all.
        needs_echo = bool(query) or scope_id is None
        # Two literal calls, not one built path: tests/test_parity.py reads each route from its call site.
        if scope_id is None:
            with _explain_missing_route():
                answer = self.transport.get("/v1/decisions", params=query or None) or {}
        else:
            answer = self.transport.get(f"/v1/projects/{_quote(scope_id)}/decisions", params=query or None) or {}
        applied = answer.get("applied")
        if needs_echo and not isinstance(applied, Mapping):
            raise DecisionsServerTooOld()
        return DecisionPage(
            decisions=list(answer.get("decisions") or []),
            applied=dict(applied) if isinstance(applied, Mapping) else None,
            next_cursor=answer.get("next_cursor") or None,
        )

    def remove_decision(self, decision_id: str) -> None:
        """``DELETE /v1/decisions/{id}``."""
        self.transport.delete(f"/v1/decisions/{_quote(_strip_id_prefix(decision_id))}")


def _build_list_query(*, since: str | None, until: str | None, words: str | Sequence[str] | None,
                      about: str | None, should_include_experiments: bool) -> dict[str, Any]:
    """The filters as the routes' query params; a blank one is left out."""
    if words is not None and not isinstance(words, str):
        words = " ".join(str(word) for word in words)
    query: dict[str, Any] = {}
    for name, value in (("since", since), ("until", until), ("words", words), ("about", about)):
        if value is not None and str(value).strip():
            query[name] = " ".join(str(value).split()) if name == "words" else str(value).strip()
    if should_include_experiments:
        query["include"] = "experiments"
    return query


@contextmanager
def _explain_missing_route() -> Iterator[None]:
    """The team route's route-absent 404 said as a server too old for it; any other 404 passes."""
    try:
        yield
    except errors.NotFoundError as exc:
        if _route_absent(exc):
            raise DecisionsServerTooOld() from None
        raise


def _strip_id_prefix(ref: str) -> str:
    return str(ref).strip().removeprefix("id:")


def _quote(segment: str) -> str:
    """One path segment; an empty one would reach another route."""
    if not str(segment).strip():
        raise errors.ValidationError("name the project, experiment or decision: an id can't be empty")
    return quote(str(segment).strip(), safe="")


from probe.sdk.client.server_features import _route_absent  # noqa: E402 -- pieces need each other; the front door loads this one first
