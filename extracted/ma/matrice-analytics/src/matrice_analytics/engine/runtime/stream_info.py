"""Typed parsing of the untyped ``stream_info`` dict -- with every fallback **logged**.

Normative source: ``_contracts/07-tobe-canonical-contract.md`` §5 (surface **S4**) and
``clauding/STAGE_BC_PLAN.md`` §3 (C1).

``stream_info`` is **not ours**.  It arrives from the inference worker as a plain dict whose
shape nobody declared, and ``analytics/engine_session.py:263-389``
(``resolve_camera_fields_from_stream_info``) reverse-engineers it across **five nested
lookup paths in two casings**:

======  ==========================================================  ===============================
Scope   Path                                                        Why it exists
======  ==========================================================  ===============================
1       the root dict                                               the normal case
2       ``camera_info``                                             the pipeline's camera block
3       ``input_settings``                                          the deployment's input block
4       ``input_settings.input_stream.camera_info`` /                the nested stream description
        ``input_streams[0].input_stream.camera_info``
5       ``stream_config`` (root or under ``input_settings``)         the operator's own settings
======  ==========================================================  ===============================

That function *is* the undocumented input contract.  This module replaces it with one that
says out loud which path it took.  :meth:`StreamInfo.from_raw`
(``contract/schemas.py``) already does the typed validation and covers scopes 1-3; this
wraps it so that scopes 4 and 5, the camelCase spellings, and the four legacy repairs
(``topic``-derived camera id, the ``"default"`` camera group, the ObjectId-shaped
``location``, the null-ObjectId ``location_id``) are **flattened first and reported**.

Two rules, both from contract §5:

**A missing required field is a startup error, not a default.**  :class:`StreamInfoError`
lists every missing field *and* every path that was searched for it, because the usual cause
is a worker that renamed a key: an absent ``resolution`` today silently disables zone
processing, which reaches an operator as "the numbers are wrong" rather than "the config is
broken".

**Drift must be visible.**  Every value taken from anywhere but the canonical root
snake_case key is recorded on :class:`StreamInfoParse` and logged at ``INFO``.  A fallback
that fires on every camera for a year is a rename nobody noticed; one that starts firing
after a deploy is a regression, findable in the logs on the day it happens.

This module imports nothing from ``post_processing`` (**PY-20**): the two ObjectId helpers
the legacy path borrows from ``post_processing/utils/post_processing_config_client.py`` are
re-stated here as four lines of regex.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from matrice_analytics.engine.contract.schemas import StreamInfo, StreamInfoError

__all__ = [
    "DISPLAY_FIELDS",
    "FIELD_ALIASES",
    "FieldSource",
    "REQUIRED_FIELDS",
    "StreamInfoError",
    "StreamInfoParse",
    "parse_stream_info",
    "resolve_stream_info",
]

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# The five scopes
# ---------------------------------------------------------------------------

#: Nested containers, in the order they are searched *after* the root dict.  Each entry is a
#: path of mapping keys, or an integer index into a list.  Both casings are listed because
#: the worker sends both and neither is "wrong" -- what is wrong is guessing silently.
_NESTED_SCOPES: Final[tuple[tuple[Any, ...], ...]] = (
    ("camera_info",),
    ("cameraInfo",),
    ("input_settings",),
    ("inputSettings",),
    ("input_settings", "input_stream", "camera_info"),
    ("inputSettings", "inputStream", "cameraInfo"),
    ("input_streams", 0, "input_stream", "camera_info"),
    ("input_streams", 0, "camera_info"),
)

#: The deployment's own ``stream_config`` block, which may sit at the root or under
#: ``input_settings`` (``engine_session.py:245-253``).
_STREAM_CONFIG_SCOPES: Final[tuple[tuple[Any, ...], ...]] = (
    ("stream_config",),
    ("input_settings", "stream_config"),
    ("streamConfig",),
)

DISPLAY_FIELDS: Final[frozenset[str]] = frozenset({"camera_name", "camera_group", "location"})
"""Fields whose value the **operator** chose, so ``stream_config`` outranks the root dict.

``engine_session.py:312-346`` searches ``stream_config`` first for exactly these three and
the root dict first for everything else.  That asymmetry is deliberate and load-bearing: the
pipeline stamps ``camera_name`` with the camera's ObjectId when it does not know the name,
and preferring the root would then publish that id as a display name on every dashboard.
"""

FIELD_ALIASES: Final[dict[str, tuple[str, ...]]] = {
    "camera_id": ("camera_id", "cameraId"),
    "camera_name": ("camera_name", "cameraName", "name"),
    "camera_group": ("camera_group", "cameraGroup"),
    "app_id": ("app_id", "appId", "application_id", "applicationId"),
    "app_deployment_id": ("app_deployment_id", "appDeploymentId", "deployment_id", "deploymentId"),
    "application_name": ("application_name", "applicationName"),
    "application_key_name": ("application_key_name", "applicationKeyName"),
    "application_version": ("application_version", "applicationVersion"),
    "location_id": ("location_id", "locationId"),
    "location": ("location", "location_name", "locationName"),
    "original_fps": ("original_fps", "originalFps", "fps"),
    "resolution": ("resolution", "stream_resolution", "streamResolution"),
    "rtp_number": ("rtp_number", "rtpNumber"),
    "stream_time": ("stream_time", "streamTime"),
    "frame_id": ("frame_id", "frameId"),
    "zone_config": ("zone_config", "zoneConfig"),
}
"""Every spelling of every field the engine reads, first spelling canonical.

A value found under anything but ``names[0]`` at the root scope is a **fallback** and is
logged.  ``app_id`` accepting ``application_id`` is the awkward one: S1 spells it ``app_id``
and S2 spells it ``application_id`` (both frozen, different Go DTOs), so the input carries
whichever the sender's own surface used.
"""

REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "camera_id",
    "camera_name",
    "app_id",
    "app_deployment_id",
    "application_name",
    "application_key_name",
    "application_version",
)
"""Fields with no defensible default (contract §5).

Same set as :meth:`StreamInfo.from_raw` checks, re-stated so the error can name the paths
searched.  ``resolution`` is not here because it is required *conditionally* -- only when the
camera has zone geometry -- which :class:`StreamInfo` enforces itself.

``original_fps`` is **not** here, since INF-2606.  It was, on the grounds that the engine
divides by it; it does not, and has not since **PY-13** moved every duration onto
``frame_ts`` deltas.  The requirement was load-bearing in the wrong direction: py_inference
withholds the field rather than publish a rate it cannot vouch for (correctly -- a wrong
rate is silently wrong output), so requiring it turned "we do not know the frame rate" into
"this camera produces nothing", permanently, for a value no primitive reads.  A missing
rate now resolves to ``0.0`` and rides the S3 echo as the honest "unknown" that model has
always defaulted to.
"""

_UNKNOWN_LOCATION_LABELS: Final[frozenset[str]] = frozenset({"unknown location", "unknown", "n/a", "none"})
"""Placeholder location names that mean "we do not know", normalised to ``""``.

``engine_session.py:34`` carries the first of these; the others are the spellings seen
alongside it.  Publishing the placeholder puts the literal string "Unknown Location" on
business-metrics rows, which are *not* backfilled server-side.
"""

_OBJECT_ID_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{24}$", re.IGNORECASE)
_NULL_OBJECT_ID: Final[str] = "0" * 24
_TOPIC_SUFFIX: Final[str] = "_input_topic"


# ---------------------------------------------------------------------------
# What the parse produced, and from where
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FieldSource:
    """Where one field's value came from.

    Attributes:
        field: The canonical field name, e.g. ``"camera_name"``.
        path: The dotted path it was read from -- ``""`` for the root dict,
            ``"input_settings.stream_config"`` for a nested scope, or a named repair such as
            ``"topic"``.  Combined with :attr:`alias` this is enough to reproduce the lookup.
        alias: The key that actually held it, e.g. ``"cameraName"``.
        fallback: ``True`` when this was *not* the canonical spelling at the root scope --
            i.e. when the input drifted from what the contract declares.
    """

    field: str
    path: str
    alias: str
    fallback: bool

    @property
    def where(self) -> str:
        """Human-readable ``path.alias``, for a log line or an error message."""
        return f"{self.path}.{self.alias}" if self.path else self.alias


@dataclass(frozen=True, slots=True)
class StreamInfoParse:
    """A validated :class:`StreamInfo` plus the audit trail of how it was found.

    The audit trail is the whole point of this module: it turns "the input shape drifted"
    from an invisible condition into :attr:`fallbacks`, which a caller can log once per
    session, assert on in a test, or surface on a health endpoint.
    """

    stream: StreamInfo
    """The validated typed input (surface S4)."""

    sources: tuple[FieldSource, ...]
    """One entry per field that was found, in :data:`FIELD_ALIASES` order."""

    searched: tuple[str, ...]
    """Every scope path that was searched, in precedence order -- for error messages."""

    @property
    def fallbacks(self) -> tuple[FieldSource, ...]:
        """The subset of :attr:`sources` that did not come from the canonical root key."""
        return tuple(source for source in self.sources if source.fallback)

    def describe(self) -> str:
        """One line per fallback, suitable for a log or a test failure message."""
        if not self.fallbacks:
            return "stream_info: every field came from its canonical root key"
        return "stream_info fallbacks:\n  - " + "\n  - ".join(
            f"{source.field} <- {source.where}" for source in self.fallbacks
        )


# ---------------------------------------------------------------------------
# Scope collection
# ---------------------------------------------------------------------------


def _walk(raw: Mapping[str, Any], path: Sequence[Any]) -> Mapping[str, Any] | None:
    """Follow ``path`` through nested mappings and lists, or return ``None``."""
    node: Any = raw
    for step in path:
        if isinstance(step, int):
            if not isinstance(node, Sequence) or isinstance(node, (str, bytes)):
                return None
            if step >= len(node):
                return None
            node = node[step]
        else:
            if not isinstance(node, Mapping):
                return None
            node = node.get(step)
    return node if isinstance(node, Mapping) else None


def _dotted(path: Sequence[Any]) -> str:
    """``("input_streams", 0, "camera_info")`` -> ``"input_streams[0].camera_info"``."""
    out = ""
    for step in path:
        if isinstance(step, int):
            out += f"[{step}]"
        else:
            out = f"{out}.{step}" if out else str(step)
    return out


def _scopes(raw: Mapping[str, Any]) -> tuple[list[tuple[str, Mapping[str, Any]]], ...]:
    """Build the id-first and display-first scope lists that are actually present.

    Returns:
        ``(id_scopes, display_scopes)``.  ``id_scopes`` is root-first;
        ``display_scopes`` puts ``stream_config`` ahead of the root (see
        :data:`DISPLAY_FIELDS`).  Only scopes that exist in *this* dict are included, so a
        log line naming a scope means the scope was really there.
    """
    stream_config: list[tuple[str, Mapping[str, Any]]] = []
    for path in _STREAM_CONFIG_SCOPES:
        node = _walk(raw, path)
        if node is not None:
            stream_config.append((_dotted(path), node))

    nested: list[tuple[str, Mapping[str, Any]]] = []
    for path in _NESTED_SCOPES:
        node = _walk(raw, path)
        if node is not None:
            nested.append((_dotted(path), node))

    root: list[tuple[str, Mapping[str, Any]]] = [("", raw)]
    return (root + nested + stream_config, stream_config + nested + root)


# ---------------------------------------------------------------------------
# The parse
# ---------------------------------------------------------------------------


def resolve_stream_info(raw: Mapping[str, Any] | None) -> StreamInfoParse:
    """Parse ``stream_info`` into a validated :class:`StreamInfo`, reporting every fallback.

    Args:
        raw: The ``stream_info`` dict the inference worker handed to the session.  ``None``
            or a non-mapping is an error, not an empty default -- a session with no stream
            info has no camera to attribute its numbers to.

    Returns:
        The :class:`StreamInfoParse`: the typed value plus where each field came from.

    Raises:
        StreamInfoError: A required field (:data:`REQUIRED_FIELDS`) is absent from every
            scope, or the assembled value fails :class:`StreamInfo` validation -- most often
            ``resolution`` missing while ``zone_config`` declares zones, which must fail
            loudly rather than silently disable zone processing (contract §5).
    """
    if raw is None:
        raise StreamInfoError(
            [
                "stream_info is None. Every published number is attributed to a camera, an "
                "app and a deployment; with no stream_info there is nothing to attribute it "
                "to, so this is a startup error rather than an empty default (contract §5)."
            ]
        )
    if not isinstance(raw, Mapping):
        raise StreamInfoError([f"stream_info must be a mapping, got {type(raw).__name__} ({raw!r:.80})"])

    id_scopes, display_scopes = _scopes(raw)
    fields: dict[str, Any] = {}
    sources: list[FieldSource] = []

    for field, aliases in FIELD_ALIASES.items():
        scopes = display_scopes if field in DISPLAY_FIELDS else id_scopes
        found = _lookup(scopes, aliases)
        if found is None:
            continue
        path, alias, value = found
        fields[field] = value
        sources.append(
            FieldSource(
                field=field,
                path=path,
                alias=alias,
                fallback=bool(path) or alias != aliases[0],
            )
        )

    _repair(raw, fields, sources)

    missing = [name for name in REQUIRED_FIELDS if _is_blank(fields.get(name))]
    if missing:
        searched = ", ".join(repr(path) or "'' (root)" for path, _ in id_scopes)
        raise StreamInfoError(
            [
                f"required field {name!r} is missing; searched {searched} for "
                f"{', '.join(repr(alias) for alias in FIELD_ALIASES[name])}"
                for name in missing
            ]
        )

    parse = StreamInfoParse(
        stream=StreamInfo.from_raw({k: v for k, v in fields.items() if v is not None}),
        sources=tuple(sources),
        searched=tuple(path for path, _ in id_scopes),
    )

    for source in parse.fallbacks:
        # INFO, not DEBUG: a fallback is the input drifting from the declared contract, and
        # the whole reason C1 exists is that today it happens silently.  Parsing is a
        # per-session operation, so this is one line per camera per start, not per frame.
        #
        # Per-session applies to the *identity* fields only.  The three media anchors
        # (`frame_id`, `stream_time`, `rtp_number`) change every frame and are refreshed on a
        # copy by `Session._frame_stream`, not re-parsed here.  Do not read "per-session"
        # above as licence to freeze them -- that is exactly how `rtp_number` came to be
        # pinned to the session's first frame, giving every alert on a camera the same
        # thumbnail.
        logger.info(
            "stream_info: %s resolved from the non-canonical path %r "
            "(canonical: root %r) -- the sender's shape has drifted from contract §5",
            source.field,
            source.where,
            FIELD_ALIASES[source.field][0],
        )
    return parse


def parse_stream_info(raw: Mapping[str, Any] | None) -> StreamInfo:
    """:func:`resolve_stream_info` when the caller only wants the value.

    Args:
        raw: The untyped ``stream_info`` dict.

    Returns:
        The validated :class:`StreamInfo`.

    Raises:
        StreamInfoError: As :func:`resolve_stream_info`.
    """
    return resolve_stream_info(raw).stream


# ---------------------------------------------------------------------------
# Lookup and the four legacy repairs
# ---------------------------------------------------------------------------


def _lookup(scopes: Sequence[tuple[str, Mapping[str, Any]]], aliases: Sequence[str]) -> tuple[str, str, Any] | None:
    """First non-blank value for ``aliases``, scanning scopes in precedence order.

    Scope order dominates alias order: a canonical spelling in a later scope loses to an
    alias in an earlier one, which is what ``engine_session.py`` does and what makes
    ``stream_config.cameraName`` beat a root ``camera_name`` holding an ObjectId.
    """
    for path, scope in scopes:
        for alias in aliases:
            if alias in scope and not _is_blank(scope[alias]):
                return (path, alias, scope[alias])
    return None


def _is_blank(value: Any) -> bool:
    """Whether a looked-up value counts as absent.

    ``None`` and a whitespace-only string are absent; ``0`` and ``False`` are *values* --
    treating a zero as missing is how a legitimately zero ``original_fps`` would get
    silently replaced by a default (and then divided by).
    """
    if value is None:
        return True
    return isinstance(value, str) and not value.strip()


def _repair(raw: Mapping[str, Any], fields: dict[str, Any], sources: list[FieldSource]) -> None:
    """Apply the four repairs the legacy resolver performs, each recorded as a source.

    They are repairs rather than lookups: each one *changes* a value, so each is worth a
    log line of its own.  All four are ported from
    ``analytics/engine_session.py:296-381``.
    """

    def record(field: str, path: str, alias: str) -> None:
        sources.append(FieldSource(field=field, path=path, alias=alias, fallback=True))

    # 1. camera_id from the input topic name, `<camera_id>_input_topic`.  The last resort:
    #    without a camera id the row is ingested with teamId='' and is invisible to every
    #    dashboard, so a topic-derived id beats no id at all.
    if _is_blank(fields.get("camera_id")):
        topic = raw.get("topic")
        if isinstance(topic, str) and topic.strip().endswith(_TOPIC_SUFFIX):
            derived = topic.strip()[: -len(_TOPIC_SUFFIX)].strip()
            if derived:
                fields["camera_id"] = derived
                record("camera_id", "topic", _TOPIC_SUFFIX)

    camera_id = str(fields.get("camera_id") or "").strip()

    # 2. camera_group: '' or a copy of the camera id becomes 'default'.  A group equal to
    #    the camera id makes the grouping UI show one group per camera, which is the same as
    #    no grouping but noisier.
    group = str(fields.get("camera_group") or "").strip()
    if not group or (camera_id and group == camera_id):
        if group:
            record("camera_group", "(repair)", "default")
        fields["camera_group"] = "default"

    # 3. A location that is really an ObjectId is a location *id*.  The pipeline sends one
    #    or the other in the same key depending on which service filled it in; publishing
    #    the id as a display name puts a raw ObjectId on the dashboard, and losing it as an
    #    id gives every row _idLocation = '' (FROZEN-1).
    location = str(fields.get("location") or "").strip()
    if location.lower() in _UNKNOWN_LOCATION_LABELS:
        fields["location"] = ""
        record("location", "(repair)", "unknown-placeholder")
        location = ""
    if location and _OBJECT_ID_RE.match(location):
        if _is_blank(fields.get("location_id")) and location.lower() != _NULL_OBJECT_ID:
            fields["location_id"] = location
            record("location_id", "(repair)", "location-was-an-objectid")
        fields["location"] = ""

    # 4. The all-zero ObjectId is the "unset" placeholder, not a location.
    location_id = str(fields.get("location_id") or "").strip()
    if location_id.lower() == _NULL_OBJECT_ID:
        fields["location_id"] = ""
        record("location_id", "(repair)", "null-objectid")
