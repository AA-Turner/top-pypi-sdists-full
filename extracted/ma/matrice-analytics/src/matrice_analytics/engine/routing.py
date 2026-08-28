"""Which apps run the new engine, and which stay on the legacy flow.

One function -- :func:`route_app` -- answers one question: *for this app, do we run
:class:`~matrice_analytics.engine.runtime.session.Session` or the legacy
``post_processing`` use-case flow?*  It replaces ``analytics/flow.py:140``
``resolve_manifest_for_app()``.

What is kept from the legacy resolver
------------------------------------
* **One function, one answer.**  Callers get a decision, not a policy engine.
* **Env override** ``MATRICE_ANALYTICS_FLOW`` in ``auto`` | ``old`` | ``new``, with ``auto``
  the default.
* **Dynamic resolution.**  Adding an app is publishing its manifest, never editing this file.
  The reference resolves through :func:`~matrice_analytics.engine.manifest.loader.resolve_ref`
  (a folder, a zip URL, or a bare ``app_id`` against ``$MATRICE_APPS_ROOT`` /
  ``$MATRICE_APPS_URL``), and display names are normalised the way the legacy index did --
  ``"People Counting"`` finds ``people_counting``.

What is deliberately **not** inherited
--------------------------------------
The legacy eligibility gate excluded any manifest with a ``volume.counter`` section, on the
grounds that "abline/polygon counters need per-camera zone geometry, which the inference
pipeline does not wire yet".  That single condition excluded **footfall -- the flagship
geometry app -- from the engine that was built for it**, and it excluded it *silently*: the
app kept working on the legacy path, so nothing ever looked broken.  Geometry is now a
first-class input (``StreamInfo.zone_config``, resolved once per camera by
:class:`~matrice_analytics.engine.primitives.geometry.SceneGeometry`, **PY-7**), and
``line_crossing`` / ``zone_occupancy`` are implemented primitives, so the premise is gone.

Also not inherited: the category allow-list (``{VOLUME, INCIDENT, QUALITY, SAFETY}``) and the
two hard-coded deny-lists.  A category set is not a statement about runnability, and the
``license_plate_recognition`` deny-list is now covered by the schema itself -- ``ocr_text`` is
a *rejected* primitive (``models.py`` ``_REJECTED_PRIMITIVES``: "OCR is inference, not
analytics"), so an LPR manifest cannot load and therefore cannot route here.  A gate the
schema already enforces does not need a second copy that can drift.

The gate
--------
An app runs the new engine when **both** hold:

1. its manifest **loads** -- schema-valid, sources resolve, and its ``custom`` code imports;
2. every primitive it names is **registered and implemented** --
   :meth:`~...manifest.models.AppManifest.unimplemented_primitives` plus a lookup in
   :data:`~matrice_analytics.engine.primitives.REGISTRY`.

Anything else refuses **loudly and by name**: the reason says *which* primitive is missing,
never "not eligible".  Under ``MATRICE_ANALYTICS_FLOW=new`` -- an explicit operator override --
a failure raises :class:`RoutingError` instead of falling back, because silently doing the
opposite of what an override asked for is how a "we enabled the new engine last week" turns
into a week of wrong dashboards.  Half-running is never an option: a session that starts
without one of its stages publishes a stream of plausible zeros, and a plausible zero is
indistinguishable from a quiet camera.

Why this file names no legacy use case
--------------------------------------
Two reasons, one of which is a live trap.

**PY-20**: the engine currently loads **zero** legacy modules, and
``tests/unit/engine/test_import_isolation.py`` pins that.  Importing
``matrice_analytics.post_processing`` executes ~180 modules and pulls in torch and cv2.  So
routing decides *whether* legacy is used; it never imports legacy to decide.  The caller --
which is already inside the legacy tree -- does the dispatch.

**PY-22**: the legacy registry's 140 ``(category, name)`` pairs come from two sources that
disagree.  ``post_processor.py:797`` ``_register_use_cases()`` registers 129; the eager block
in ``post_processing/__init__.py`` contributes 11 more that the function never does.  There is
therefore **no authoritative legacy catalogue to compare against**, and this module does not
consult one: the positive gate is the manifest's own existence, and "no manifest" is the
legacy answer regardless of which of the two lists an app appears in.  If some future caller
does need the catalogue, it must state which source it read and why -- and it must not read it
from here.
"""

from __future__ import annotations

import logging
import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Final, Literal

from matrice_analytics.engine.manifest.loader import AppLoadError, LoadedApp, load_app_bundle
from matrice_analytics.engine.manifest.models import CustomConfig
from matrice_analytics.engine.primitives import REGISTRY

if TYPE_CHECKING:  # pragma: no cover - typing only
    from matrice_analytics.engine.manifest.models import AppManifest

__all__ = [
    "FLOW_ENV_VAR",
    "FLOW_MODES",
    "Engine",
    "FlowMode",
    "RoutingDecision",
    "RoutingError",
    "normalise_app_name",
    "resolve_flow_mode",
    "route_app",
    "unrunnable_primitives",
]

logger = logging.getLogger(__name__)

FLOW_ENV_VAR: Final[str] = "MATRICE_ANALYTICS_FLOW"
"""Same variable name the legacy resolver used, so existing deployments keep working."""

FLOW_MODES: Final[tuple[str, str, str]] = ("auto", "old", "new")

FlowMode = Literal["auto", "old", "new"]
Engine = Literal["new", "legacy"]

#: A bare app id, as ``resolve_ref`` accepts it.  Anything else (a path, a URL, a display
#: name) is handled without normalisation or with :func:`normalise_app_name`.
_BARE_ID_RE: Final[re.Pattern[str]] = re.compile(r"^[a-z][a-z0-9_]*$")


class RoutingError(RuntimeError):
    """The new engine was explicitly requested and cannot run this app.

    Raised only under ``MATRICE_ANALYTICS_FLOW=new``.  In ``auto`` the same condition returns a
    ``legacy`` :class:`RoutingDecision` whose ``reason`` names the cause -- an override,
    though, is an operator saying "use the new engine", and answering that with a silent legacy
    run is the failure mode this whole engine exists to remove.
    """


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    """Which engine runs, and the reason -- in words a log line can carry verbatim."""

    app: str
    """The reference as the caller gave it."""

    engine: Engine
    """``"new"`` for :class:`~matrice_analytics.engine.runtime.session.Session`, else ``"legacy"``."""

    mode: FlowMode
    """The effective ``MATRICE_ANALYTICS_FLOW`` mode."""

    reason: str
    """Why.  Always populated, and always specific: it names the primitive, not "not eligible"."""

    ref: str = ""
    """The reference that actually loaded, when ``engine == "new"``.  A caller can hand this
    straight back to :func:`~matrice_analytics.engine.manifest.loader.load_app_bundle`."""

    loaded: LoadedApp | None = None
    """The already-loaded bundle, when ``engine == "new"``.

    Returned so the caller does not load the app a second time -- and so it cannot load a
    *different* one between the decision and the run.
    """

    problems: tuple[str, ...] = ()
    """Every reason the new engine was refused, not just the first."""

    @property
    def use_new_engine(self) -> bool:
        return self.engine == "new"

    def __str__(self) -> str:
        return f"app {self.app!r}: {self.engine.upper()} engine (mode={self.mode}) -- {self.reason}"


def resolve_flow_mode(env: Mapping[str, str] | None = None) -> FlowMode:
    """Read ``MATRICE_ANALYTICS_FLOW``.

    Args:
        env: Environment to read.  Defaults to :data:`os.environ`; injectable so a test does
            not have to mutate process state.

    Returns:
        ``"auto"`` (the default), ``"old"`` or ``"new"``.

    Raises:
        RoutingError: The variable is set to something else.  Deliberately fatal: the legacy
            resolver lower-cased the value and fell through to ``auto``, so
            ``MATRICE_ANALYTICS_FLOW=newx`` meant "auto" and an operator who thought they had
            switched engines had not.  A typo in a routing switch must not be a silent no-op.
    """
    source = os.environ if env is None else env
    raw = str(source.get(FLOW_ENV_VAR, "") or "").strip().lower()
    if not raw:
        return "auto"
    if raw not in FLOW_MODES:
        raise RoutingError(
            f"{FLOW_ENV_VAR}={raw!r} is not a flow mode. Use one of: {', '.join(FLOW_MODES)} "
            f"('auto' = route an app whose manifest loads and whose primitives all exist; 'old' = "
            f"always legacy; 'new' = require the new engine and fail loudly if it cannot run)."
        )
    return raw  # type: ignore[return-value]


def normalise_app_name(name: str) -> str:
    """A deployment's ``app_name`` as an app id.

    The same normalisation the legacy resolver's display-name index used
    (``flow.py:_normalize``): lower-cased, with spaces and hyphens folded to underscores, so a
    deployment carrying ``"People Counting"`` resolves ``people_counting``.  Kept because that
    join is real -- ``app_name`` is a display string in some deployment records and an id in
    others.
    """
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def unrunnable_primitives(manifest: AppManifest, loaded: LoadedApp | None = None) -> tuple[str, ...]:
    """Every reason this build cannot run ``manifest``'s pipeline, one string each.

    Three conditions, all of which the runtime would otherwise discover at session start:

    * a primitive the manifest schema knows but the engine has not built
      (``IMPLEMENTED = False`` -- the schema deliberately validates apps ahead of the runtime,
      ``08`` §2);
    * a primitive with no entry in :data:`~matrice_analytics.engine.primitives.REGISTRY` --
      possible when a build ships a partial primitive set;
    * a ``custom`` stage whose implementation was not imported.  Only the loader imports an
      app's Python, so this is really "you were handed a manifest, not a bundle".

    Args:
        manifest: The validated manifest.
        loaded: The bundle it came from, when there is one.  Without it, ``custom`` stages
            cannot be checked and are reported as such.

    Returns:
        Human-readable problems, each naming the offending stage and primitive.  Empty means
        the pipeline is runnable.
    """
    problems: list[str] = []
    unimplemented = manifest.unimplemented_primitives()
    if unimplemented:
        problems.append(
            f"primitive(s) {', '.join(unimplemented)} are declared but not implemented by this "
            f"engine build (08 §2: the manifest schema validates apps ahead of the runtime)"
        )
    custom = dict(loaded.custom) if loaded is not None else {}
    for stage in manifest.pipeline:
        if stage.PRIMITIVE in unimplemented:
            # Already reported above. An unimplemented primitive is also unregistered by
            # construction, and saying it twice buries the other problems in a long list.
            continue
        if isinstance(stage, CustomConfig):
            if stage.stage_name not in custom:
                problems.append(
                    f"stage {stage.stage_name!r} is custom code ({stage.impl!r}) whose implementation "
                    f"was not imported; only load_app_bundle() imports an app's Python"
                )
            continue
        if stage.PRIMITIVE not in REGISTRY:
            problems.append(
                f"stage {stage.stage_name!r} names primitive {stage.PRIMITIVE!r}, which is not "
                f"registered in this build. Registered: {', '.join(REGISTRY.names()) or '(none)'}"
            )
    return tuple(problems)


def route_app(
    app: str | os.PathLike[str] | None,
    *,
    mode: FlowMode | None = None,
    env: Mapping[str, str] | None = None,
    loader: Callable[[str], LoadedApp] = load_app_bundle,
) -> RoutingDecision:
    """Decide which engine runs ``app``.

    Args:
        app: What the deployment knows the app as -- a bare id (``people_counting``), a display
            name (``"People Counting"``), an app folder path, or a zip URL.  ``None`` or empty
            routes to legacy: an unnamed app cannot have a manifest.
        mode: Override the env var, for a caller that already has a policy.
        env: Environment to read ``MATRICE_ANALYTICS_FLOW`` from.  Injectable for tests.
        loader: The app loader.  Injectable so a caller can supply a cached or pre-warmed one;
            defaults to :func:`~matrice_analytics.engine.manifest.loader.load_app_bundle`,
            which resolves paths, URLs and bare ids and validates the manifest.

    Returns:
        The :class:`RoutingDecision`.  When ``engine == "new"`` it carries the already-loaded
        bundle, so the caller runs exactly the app that was approved.

    Raises:
        RoutingError: ``mode``/``MATRICE_ANALYTICS_FLOW`` is ``new`` and the app cannot run on
            the new engine, or the env var holds an unknown value.
    """
    effective: FlowMode = resolve_flow_mode(env) if mode is None else mode
    reference = "" if app is None else os.fspath(app).strip()

    if effective == "old":
        return _legacy(reference, effective, f"{FLOW_ENV_VAR}=old forces the legacy flow")

    if not reference:
        return _legacy(reference, effective, "no app name was given, so no manifest can be resolved")

    loaded: LoadedApp | None = None
    # A reference can be a presigned URL, whose query string is a bearer credential. Every place a
    # reference is quoted here ends up in a log line or an exception message, so quote the redacted
    # form -- it still identifies the object, which is the part anyone diagnosing this needs.
    from .manifest.loader import redact_url

    safe_reference = redact_url(reference)

    attempts: list[str] = []
    failures: list[str] = []
    for candidate in _candidate_refs(reference):
        attempts.append(redact_url(candidate))
        try:
            loaded = loader(candidate)
        except AppLoadError as exc:
            failures.append(f"{redact_url(candidate)!r}: {type(exc).__name__}: {exc}")
            continue
        except Exception as exc:  # noqa: BLE001 - an unexpected loader failure is still a routing input
            failures.append(f"{redact_url(candidate)!r}: unexpected {type(exc).__name__}: {exc}")
            continue
        break

    if loaded is None:
        reason = (
            f"no loadable manifest for {safe_reference!r} (tried {', '.join(repr(a) for a in attempts)}); "
            f"an app with no manifest is a legacy app by definition"
        )
        if effective == "new":
            raise RoutingError(
                f"{FLOW_ENV_VAR}=new requires app {safe_reference!r} to run on the new engine, but "
                f"{reason}.\n  - " + "\n  - ".join(failures)
            )
        logger.info("routing app %r: LEGACY -- %s", safe_reference, reason)
        return _legacy(reference, effective, reason, problems=tuple(failures))

    problems = unrunnable_primitives(loaded.manifest, loaded)
    if problems:
        reason = (
            f"app {loaded.manifest.app.id!r} loads, but this engine build cannot run its pipeline: "
            + "; ".join(problems)
        )
        if effective == "new":
            raise RoutingError(
                f"{FLOW_ENV_VAR}=new requires app {reference!r} to run on the new engine, but "
                f"{reason}. Refusing rather than starting a session with a missing stage: that "
                f"publishes plausible zeros, and a plausible zero is indistinguishable from a quiet "
                f"camera (09 §5)."
            )
        logger.warning("routing app %r: LEGACY -- %s", reference, reason)
        return _legacy(reference, effective, reason, problems=problems)

    reason = (
        f"manifest {loaded.manifest.app.id!r} v{loaded.manifest.app.version} loaded from "
        f"{loaded.root} and every primitive it names is registered and implemented"
    )
    logger.info(
        "routing app %r: NEW engine -- app=%s v%s stages=%s",
        reference,
        loaded.manifest.app.id,
        loaded.manifest.app.version,
        [stage.stage_name for stage in loaded.manifest.pipeline],
    )
    return RoutingDecision(
        app=reference,
        engine="new",
        mode=effective,
        reason=reason,
        ref=attempts[-1],
        loaded=loaded,
    )


def _legacy(
    app: str, mode: FlowMode, reason: str, *, problems: tuple[str, ...] = ()
) -> RoutingDecision:
    return RoutingDecision(app=app, engine="legacy", mode=mode, reason=reason, problems=problems)


def _candidate_refs(reference: str) -> tuple[str, ...]:
    """The references to try, in order.

    A path or a URL is used verbatim -- normalising a filesystem path would be wrong.  A bare
    name is tried as given and then normalised, which is the legacy display-name index
    (``"People Counting"`` -> ``people_counting``) without the index: ``resolve_ref`` already
    knows how to find an id under ``$MATRICE_APPS_ROOT`` / ``$MATRICE_APPS_URL``, so a scan of
    a config directory is one fewer thing to keep in step.
    """
    if _looks_like_a_location(reference):
        return (reference,)
    candidates = [reference]
    normalised = normalise_app_name(reference)
    if normalised != reference and _BARE_ID_RE.match(normalised):
        candidates.append(normalised)
    return tuple(candidates)


def _looks_like_a_location(reference: str) -> bool:
    """Whether the reference is a path or a URL rather than an app name."""
    lowered = reference.lower()
    if lowered.startswith(("http://", "https://", "file://")):
        return True
    return "/" in reference or "\\" in reference or reference.startswith((".", "~"))
