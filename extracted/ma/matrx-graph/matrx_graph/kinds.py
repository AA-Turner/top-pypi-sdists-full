"""Kind catalog — matrx-graph's window into the platform Shape registry.

``content_ir.kind_definition`` is the canonical, cross-platform registry of
named, versioned structures ("kinds" / Shapes). A node declares its I/O as a
kind (``NodeSpec.input_kind`` / ``NodeSpec.output_kind``); this module resolves
the slug to its JSON Schema (``emitted_json_schema``) and validates instances
against it. The pydantic ``input_schema``/``output_schema`` classes remain the
node's *implementation detail*; the kind is the canonical declaration shared
with every other producer/consumer on the platform (agents, tools, renderers).

DB access follows the package's DI seam (``matrx_graph.db._registry``): the
host registers the generated ``kind_definition_manager`` and this module never
imports host code. When the manager is not registered (a standalone graph with
no wiring), resolution raises and the caller fails open — kind validation is
skipped and the miss is logged once (see the failure posture below).

Failure posture — NAMED DEGRADED MODE, always loud, and FATAL under the live
``workflow_io`` enforcement except where the matrix says degraded:
every fail-open is a structured, enumerable ``KindDegradedReason`` (never a
bare silent skip), surfaced on the ``KindCheck`` envelope, in logs (once per
slug, error level, with a grep/queryable ``degraded_reason=<value>`` token),
and persisted wherever verdicts persist (``NodeOutcome.output_kind_degraded``).
  * kind_not_registered   -> slug has no live row in content_ir.kind_definition
  * kind_inactive         -> resolved row has is_active=false. NEVER degraded
                             and NEVER fatal: is_active is the FRONTEND's
                             dual-gate flag and the engine ignores it, in
                             every mode (Arman, 2026-08-25). Retained in the
                             vocabulary only because stored verdicts may carry
                             it; the engine no longer produces it.
  * schema_unavailable    -> row exists but emitted_json_schema is null
  * schema_invalid        -> emitted_json_schema is not a valid Draft 2020-12
                             JSON Schema (metaschema-checked at resolution)
  * catalog_unreachable   -> DB not wired / catalog unreachable (infra outage).
                             A PROGRAMMER error (TypeError, AttributeError, a
                             renamed column, a wrong keyword) never lands here —
                             it re-raises (THE STRICTNESS LAW clause 6).
A missing/broken kind registration is a PLATFORM defect, not user input. With
``workflow_io`` enforcement ON (the live posture since 2026-08-26) it is FATAL:
admission (``Scheduler.run`` and ``resume``) refuses the run, both scheduler
gates raise, and an invalid compiled schema is a ``CompilationError``. Only
``catalog_unreachable`` fails open, and ``kind_inactive`` never fails. With
enforcement rolled back, every reason fails open (mirrors
``validate_instance``'s malformed-schema rule). Either way it screams, and a
skipped check must never be renderable as a pass (``KindCheck.checked=False``
+ the named reason).

Enforcement is a ratcheted rollout carried by :data:`KIND_ENFORCEMENT` — a
CAPS CONSTANT in this file, **never an env var** (Arman, 2026-08-25; see the
constant for the reasoning and `common-docs/policies/env-vars-are-values-not-toggles.md`).
One entry today, ``workflow_io``, ON since 2026-08-26: an output that violates
its kind fails the step as a non-retryable ``KindContractViolation`` (an input
that violates its kind fails pre-execute with or without the flag). When a
family is ON, degraded
reasons escalate per ``degraded_escalation`` — EXCEPT ``catalog_unreachable``
(an infra outage must never masquerade as validation success OR take down
execution) and ``kind_inactive`` (the engine ignores the frontend's flag).
Matrix documented in ``docs/workflow/KIND_ENFORCEMENT.md``.
"""

from __future__ import annotations

import asyncio
import logging
import time
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from matrx_graph.content_ir.markers import normalize_nonidentity_markers, strip_kind_markers
from matrx_graph.executor.schema_validation import schema_validity_errors, validate_instance

logger = logging.getLogger(__name__)

_CACHE_TTL_SECONDS = 300.0


class KindDegradedReason(StrEnum):
    """Enumerable named degraded outcomes for kind validation.

    Every fail-open in the kind pipeline carries exactly one of these — logs,
    the KindCheck envelope, and persisted verdicts all speak this vocabulary,
    so "skipped" is queryable and never renderable as "passed".
    """

    KIND_NOT_REGISTERED = "kind_not_registered"
    KIND_INACTIVE = "kind_inactive"
    SCHEMA_UNAVAILABLE = "schema_unavailable"
    SCHEMA_INVALID = "schema_invalid"
    CATALOG_UNREACHABLE = "catalog_unreachable"


#: Fatal kind enforcement, per contract family. **A CAPS CONSTANT, NEVER AN
#: ENV VAR** (Arman, 2026-08-25 — `common-docs/policies/env-vars-are-values-not-toggles.md`).
#:
#: WHY THIS IS NOT `MATRX_KINDS_ENFORCE_<FAMILY>` ANY MORE
#: -------------------------------------------------------
#: It was, until 2026-08-25. His ruling, verbatim in substance: a lenient
#: setting written in CODE is fine — the next push makes every server, every
#: container, every sandbox and every laptop enforce the identical rule at the
#: identical moment. The same switch read from the ENVIRONMENT means local
#: disagrees with the server, which disagrees with the container, and the
#: divergence is invisible until it produces a bug nobody can reproduce. The
#: leniency was never the problem; the environment was.
#:
#: So flipping one of these is a code push — reviewable, greppable, and
#: uniform everywhere the moment it deploys. Tests override it with
#: ``monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)``; there is no
#: environment read to reach for, which is the point.
#:
#: ONE ENTRY, and it is a ratchet toward deletion. ``action_io`` / ``tool_io``
#: / ``agent_io`` / ``render`` used to have flags here with **zero call sites**
#: — nothing read them, so flipping one changed nothing at all. A knob for
#: behavior that does not exist is not a ratchet, it is scenery, and they were
#: deleted rather than converted. When a family grows real enforcement it is
#: written strict from its first line; if it genuinely needs a ratchet it
#: earns an entry here, deliberately.
KIND_ENFORCEMENT: dict[str, bool] = {
    # The only family with real gates (compile + admission + input + output).
    # FLIPPED ON 2026-08-26 (Arman authorized 2026-08-25: "if those are
    # problematic, let's get rid of them, but then we just need to do the
    # legwork to make sure that nothing breaks"). The legwork, measured before
    # the flip — `scripts/kind_enforcement_blast_radius.py`: 194 bound slugs,
    # 0 fatal bindings; live payload conformance: the 229 would-have-fataled
    # rows in the prior 14 days traced to three causes, all closed (the
    # 192-row pre-stamp ordering bug 6f4f22f49, the stale gather_result schema
    # re-published at v6, and two deliberate red-path test fixtures); post-fix
    # traffic 202 declared-kind outcomes / 0 failures over 8.5h. Pre-flight
    # record: common-docs/projects/archive/kind-directives/PLAN.md § Enforcement
    # pre-flight. Rolling back is editing this line — a code push, uniform
    # everywhere, exactly like the flip.
    #
    # 🚨 A STALE REGISTRY ROW IS THE ONE RECURRING WAY THIS FLAG KILLS A RUN,
    # AND IT HAS NOW HAPPENED TWICE ON THE SAME SLUG. The pre-flight above
    # already names "the stale gather_result schema" as one of its three causes.
    # It recurred on 2026-09-12: commit cf3b9bf3 added `structured_outputs` /
    # `final_texts` / `ai_item_count` to `GatherOutput` at 11:25Z, nobody
    # republished, and at 15:41Z workflow run
    # cd1b75ec-b1af-43d8-be2c-0ee136ec3336 ("Newsroom Desk") died at its gather
    # step: "Additional properties are not allowed ('ai_item_count',
    # 'final_texts', 'structured_outputs' were unexpected)" — the live row was
    # still v6 from 2026-08-23, `additionalProperties: false`.
    #
    # Nothing was watching, because nothing COULD: a pytest run has no database,
    # and the one test that looked like the witness seeded its kind cache from
    # `GatherOutput.model_json_schema()` (model against model, green by
    # construction). The witness now exists —
    # `scripts/check_kind_registry_drift.py` diffs every `@kind` model's schema
    # against its live row, exits UNMEASURED rather than green when it cannot
    # reach the registry, and reports drift in an ENFORCED family here as FATAL.
    # CI runs its `--self-test` (falsifiability, no DB); release.sh runs the
    # live leg. Edit a model whose kind is in an ON family → republish through
    # `scripts/publish_kind_catalog.py --evolve --apply` in the SAME change.
    "workflow_io": True,
}


def kind_enforcement_enabled(family: str) -> bool:
    """Whether fatal kind enforcement is ON for ``family`` (``workflow_io``: ON since 2026-08-26).

    Reads :data:`KIND_ENFORCEMENT`. An unknown family is a caller bug: loud
    ValueError, never a silent False — a typo'd family name must not read as
    "enforcement is off", which is indistinguishable from a working gate.
    """
    if family not in KIND_ENFORCEMENT:
        raise ValueError(
            f"Unknown kind-enforcement family {family!r}. "
            f"Known: {', '.join(sorted(KIND_ENFORCEMENT))}."
        )
    return KIND_ENFORCEMENT[family]


def degraded_escalation(reason: KindDegradedReason) -> Literal["fatal", "degraded"]:
    """The escalation matrix for a degraded reason under an ENFORCED family.

    (When the family's flag is OFF, every reason stays "degraded" — loud,
    never blocking; callers only consult this matrix after checking
    ``kind_enforcement_enabled``.)

    | reason              | flag OFF          | flag ON   |
    |---------------------|-------------------|-----------|
    | kind_not_registered | degraded (loud)   | FATAL     |
    | kind_inactive       | not degraded¹     | not fatal¹|
    | schema_unavailable  | degraded (loud)   | FATAL     |
    | schema_invalid      | degraded (loud)   | FATAL     |
    | catalog_unreachable | degraded (loud)   | degraded² |

    ¹ **THE ENGINE IGNORES ``is_active``, IN BOTH COLUMNS** (Arman,
      2026-08-25). It is the FRONTEND's dual-gate flag — the server serves it
      verbatim and the client decides whether to trust a custom renderer
      (``aidream/services/runtime/kind_catalog.py``). The engine has never
      honored it, and 411 of 868 live rows carry ``is_active=false``.
      Until 2026-08-25 this row said FATAL, which meant flipping enforcement
      on would have made the engine start honoring a flag it had ignored for
      its entire life, killing runs on 5 bound node types for a reason that
      has nothing to do with whether the data is correct. That is a semantic
      change smuggled in on a toggle, so it is gone: inactive is never fatal
      here and never fatal at the three scheduler gates.
      The member survives because stored ``NodeOutcome.output_kind_degraded``
      rows may carry it; the engine no longer produces it.
    ² an infra outage must never masquerade as validation success OR take
      down execution — it stays loudly degraded even when enforced.
    """
    if reason in (
        KindDegradedReason.CATALOG_UNREACHABLE,
        KindDegradedReason.KIND_INACTIVE,
    ):
        return "degraded"
    return "fatal"


class KindEntry(BaseModel):
    """Resolved view of one kind — just what the engine needs.

    ``is_active`` mirrors the registry row's frontend dual-gate flag — the
    engine ignores it everywhere: validation, binding admission and both
    gates (ratified 2026-08-25). ``schema_errors`` holds Draft 2020-12 metaschema
    findings for ``json_schema`` computed once at resolution; non-empty means
    the registration itself is broken (degraded reason ``schema_invalid``).
    """

    model_config = ConfigDict(frozen=True)

    slug: str
    version: int
    label: str = ""
    json_schema: dict[str, Any] | None = None
    is_active: bool = True
    schema_errors: tuple[str, ...] = ()
    #: The registry row id. Carried because ``content_ir.kind_edge`` addresses
    #: kinds by ROW ID, so composition lookup would otherwise need a second
    #: query for something this resolution already read.
    id: str = ""
    #: ``metadata.disposition`` of the row (``record`` | ``envelope`` | ``receipt`` |
    #: ``proposal`` | ``prose``), or None when undeclared. Read so a schema consumer can tell a
    #: ``record`` kind — the ones that take the control keys (``kind_control_keys``) — without a
    #: second query.
    disposition: str | None = None


_cache: dict[str, tuple[float, KindEntry | None]] = {}
# The whole live slug set, with each slug's version. Same TTL and the same
# invalidation as the per-slug cache. It exists because a SYNC consumer (the
# chat block detector) has to answer "is this __kind a registered kind?" while a
# token stream is mid-flight, and it cannot await a per-slug lookup to find out.
_registry_cache: tuple[float, tuple[tuple[str, int, dict[str, Any] | None], ...]] | None = None
# Each listed slug's declared disposition, from the SAME listing query (``metadata``), so the
# sync stream catalog can apply the control keys to ``record`` kinds without a second read.
_registry_dispositions: dict[str, str | None] = {}
# Declared composition per slug (content_ir.kind_edge), same TTL as the
# kind cache, and a permanent id->slug map (kind ids are immutable).
_edge_cache: dict[str, tuple[float, tuple[tuple[str, str], ...]]] = {}
_id_to_slug: dict[str, str] = {}
_cache_lock = asyncio.Lock()
_warned_slugs: set[str] = set()
# The host may name its canonical organization for platform-owned kinds.  The
# package deliberately does not import a host constant: standalone installs
# still resolve public rows, while aidream injects its system organization at
# startup.  Without this seam, the publisher can reconcile the system row
# while the stream catalog non-deterministically picks a same-slug public row
# from another organization.
_canonical_kind_organization_id: str | None = None


def configure_canonical_kind_organization(organization_id: str | None) -> None:
    """Prefer this organization's public row when a kind slug collides.

    Platform kinds are global vocabulary.  Hosts that keep that vocabulary in
    a designated organization must inject it, so the producer catalog and the
    publisher's source-of-truth row cannot disagree.  Changing the preference
    invalidates every process cache immediately; waiting five minutes after a
    registry repair would preserve precisely the stale-schema failure this
    seam prevents.
    """
    global _canonical_kind_organization_id
    normalized = str(organization_id) if organization_id else None
    if _canonical_kind_organization_id == normalized:
        return
    _canonical_kind_organization_id = normalized
    invalidate_kind_catalog_cache()


def _catalog_row_sort_key(row: Any) -> tuple[bool, bool]:
    """Rank a live kind row: canonical public, other public, then private."""
    is_public = bool(getattr(row, "published_to_web", False))
    is_canonical = (
        _canonical_kind_organization_id is not None
        and str(getattr(row, "organization_id", "") or "")
        == _canonical_kind_organization_id
    )
    return (not is_public, not is_canonical)


def _select_catalog_row(rows: list[Any]) -> Any:
    """Choose the one deterministic row used by every engine catalog path."""
    return min(rows, key=_catalog_row_sort_key)


def _manager() -> Any:
    # Resolve the host-registered manager via the package's DI seam ONLY.
    # matrx-graph must never import host `db` code (package-boundary gate) — the
    # old ``except: from db.managers…`` fallback was a boundary violation AND dead
    # in the aidream host (which registers ``kind_definition_manager`` via
    # db_requirements). When the host never wired it, ``get_instance`` raises and
    # the caller (``get_kind``) treats it as "DB not configured": logs once, skips
    # kind validation, fails open — exactly this module's documented posture.
    from matrx_graph.db._registry import get_instance

    return get_instance("kind_definition_manager")


#: THE OUTAGE PATH IS NOT AN EXCEPTION AN AGENT MAY TAKE — THE STRICTNESS LAW
#: clause 6 (Arman, 2026-08-23). ``catalog_unreachable`` exists so a platform
#: outage never punishes a user, and it is the ONE degraded reason that stays
#: degraded even under enforcement. That made a bare ``except Exception`` the
#: softest landing in the whole kind pipeline: a typo in the manager call, a
#: renamed column, a wrong keyword — every one of them became "infra outage,
#: validation skipped, run continues", indistinguishable in the logs from a
#: real one. An agent did not have to CHOOSE this hatch; writing bad code was
#: enough.
#:
#: So the path now requires a PROVEN-UNREACHABLE dependency. These are the
#: errors that mean the code is wrong, not the dependency down; they re-raise,
#: loudly, at the call site that wrote them.
_PROGRAMMER_ERRORS: tuple[type[BaseException], ...] = (
    TypeError,
    AttributeError,
    NameError,
    ImportError,
    IndexError,
    KeyError,
    AssertionError,
    NotImplementedError,
    SyntaxError,
)


def _is_unreachable_dependency(exc: BaseException) -> bool:
    """True only when the CATALOG is unreachable, never when the code is wrong.

    Deliberately a deny-list, not an allow-list: the driver stack under the
    registered manager is the host's choice, so an allow-list of DB exception
    classes would silently reclassify a real outage as a crash the first time
    the host changed drivers. A deny-list fails in the safe direction — an
    unrecognized error is still treated as an outage — while making the named
    ways of writing bad code impossible to hide behind it.
    """
    return not isinstance(exc, _PROGRAMMER_ERRORS)


def _raise_if_programmer_error(exc: BaseException, *, what: str) -> None:
    if _is_unreachable_dependency(exc):
        return
    raise RuntimeError(
        f"kind catalog: {what} raised {type(exc).__name__}, which is a DEFECT IN THIS "
        f"CODE, not an unreachable catalog. It is NOT degraded to "
        f"'{KindDegradedReason.CATALOG_UNREACHABLE.value}' — that path is reserved for a "
        "proven-unreachable dependency (THE STRICTNESS LAW clause 6). Fix the call."
    ) from exc


def _warn_once(slug: str, message: str) -> None:
    if slug not in _warned_slugs:
        _warned_slugs.add(slug)
        logger.error(message)


def _degraded_reason_for(entry: KindEntry | None) -> KindDegradedReason | None:
    """Derive the cachable degraded reason from a resolved entry.

    ``kind_inactive`` is deliberately NOT derived here — the engine validates
    inactive kinds by ratified design; inactivity only escalates at binding
    admission under an enforced family (see ``degraded_escalation``).
    ``catalog_unreachable`` never reaches this function (transient, uncached).
    """
    if entry is None:
        return KindDegradedReason.KIND_NOT_REGISTERED
    if entry.json_schema is None:
        return KindDegradedReason.SCHEMA_UNAVAILABLE
    if entry.schema_errors:
        return KindDegradedReason.SCHEMA_INVALID
    return None


async def resolve_kind(slug: str) -> tuple[KindEntry | None, KindDegradedReason | None]:
    """Resolve a kind slug to ``(entry, degraded_reason)``.

    ``degraded_reason`` names why validation against this kind cannot run
    (``None`` = fully usable). ``catalog_unreachable`` is transient infra —
    it is logged loudly once per slug and NOT cached, so recovery is
    immediate once the catalog is back. All other outcomes are process-cached
    (TTL 5min); ``invalidate_kind_catalog_cache()`` clears the cache after a
    registry mutation.
    """
    cached = _cache.get(slug)
    if cached is not None and (time.monotonic() - cached[0]) < _CACHE_TTL_SECONDS:
        return cached[1], _degraded_reason_for(cached[1])
    async with _cache_lock:
        cached = _cache.get(slug)
        if cached is not None and (time.monotonic() - cached[0]) < _CACHE_TTL_SECONDS:
            return cached[1], _degraded_reason_for(cached[1])
        try:
            mgr = _manager()
            rows = await mgr.load_items(kind=slug)
        except Exception as exc:  # noqa: BLE001 — DB-not-wired is a platform defect
            _raise_if_programmer_error(exc, what=f"lookup for '{slug}'")
            _warn_once(
                slug,
                f"kind catalog: lookup for '{slug}' failed (catalog unreachable, "
                f"not a code defect) — kind validation is SKIPPED for this slug "
                f"(degraded_reason={KindDegradedReason.CATALOG_UNREACHABLE.value}). "
                f"This is a platform wiring/infra defect, not user input. err={exc}",
            )
            return None, KindDegradedReason.CATALOG_UNREACHABLE
        live = [r for r in rows or [] if getattr(r, "deleted_at", None) is None]
        entry: KindEntry | None = None
        if live:
            if len(live) > 1:
                # (organization_id, kind) is unique, so >1 row means multiple
                # orgs define the slug.  The host-injected canonical public
                # row wins, then another public row.  This MUST match the
                # list snapshot consumed by the synchronous stream detector.
                logger.warning(
                    "kind catalog: %d live rows for kind '%s' across orgs; "
                    "using the canonical/public one. Org-scoped kind resolution "
                    "is not implemented in the engine yet.",
                    len(live),
                    slug,
                )
            row = _select_catalog_row(live)
            schema = getattr(row, "emitted_json_schema", None)
            json_schema = schema if isinstance(schema, dict) else None
            # Metaschema-check ONCE at resolution (cached with the entry) so a
            # structurally broken registration is the named degraded reason
            # ``schema_invalid`` instead of a per-validation runtime surprise.
            errors = tuple(schema_validity_errors(json_schema)) if json_schema is not None else ()
            entry = KindEntry(
                id=str(getattr(row, "id", "") or ""),
                slug=slug,
                version=int(getattr(row, "version", 1) or 1),
                label=str(getattr(row, "label", "") or ""),
                json_schema=json_schema,
                is_active=bool(getattr(row, "is_active", True)),
                schema_errors=errors,
                disposition=_row_disposition(row),
            )
            if errors:
                _warn_once(
                    slug,
                    f"kind catalog: kind '{slug}' has a MALFORMED "
                    f"emitted_json_schema (not a valid Draft 2020-12 JSON "
                    f"Schema) — validation SKIPPED "
                    f"(degraded_reason={KindDegradedReason.SCHEMA_INVALID.value}). "
                    f"Fix the registration. Findings: {'; '.join(errors)}",
                )
        _cache[slug] = (time.monotonic(), entry)
        return entry, _degraded_reason_for(entry)


def declared_output_kind(data: Any, spec_output_kind: str | None) -> str | None:
    """THE source step's declared output kind: ``data.output_kind`` when authored, else the
    step type's own kind (``NodeSpec.output_kind``).

    One resolver for compile (``CompiledNode.output_kind``, what the run judges a mapping
    against) and the save gate (``content_ir.authoring_gate.kind_mapping_problems``), so a
    mapping off a typed action is judged the same way at save and at run time. Validation
    of a malformed authored value stays compile's (it raises); here it is simply absent."""
    raw = data.get("output_kind") if isinstance(data, dict) else None
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    return spec_output_kind.strip() if isinstance(spec_output_kind, str) and spec_output_kind.strip() else None


def cached_kind_schema(slug: str | None) -> dict[str, Any] | None:
    """The kind's schema if this process already resolved it, else None. Never reads the DB.

    For SYNC consumers on a path where the kind was just resolved (the scheduler routes a
    step's output right after checking it against its kind). None means "not known here",
    never "no such field" — callers treat it as unprovable."""
    if not slug:
        return None
    hit = _cache.get(slug)
    # Same 5-minute TTL as resolve_kind: a stale entry is "not known here", never a verdict.
    if hit is None or (time.monotonic() - hit[0]) >= _CACHE_TTL_SECONDS:
        return None
    entry = hit[1]
    if entry is None or entry.schema_errors or not isinstance(entry.json_schema, dict):
        return None
    return entry.json_schema


async def get_kind(slug: str) -> KindEntry | None:
    """Resolve a kind slug to its registry entry, or None when unregistered.

    Thin wrapper over ``resolve_kind`` — use that when the caller must tell
    WHY resolution degraded (named reason) instead of just getting None.
    """
    entry, _reason = await resolve_kind(slug)
    return entry


async def resolve_kind_edges(slug: str) -> tuple[tuple[str, str], ...]:
    """The composition ``content_ir.kind_edge`` DECLARES for ``slug``.

    Returns ``(field_name, child_slug)`` pairs, ordered by the row's declared
    ``position`` then field name. This is the Kind Availability Index's first
    nesting source and it is NOT redundant with the emitted schema: measured on
    the live registry (2026-08-20), 51 parent kinds declare composition here
    while pinning ``__kind`` on nothing — every kind registered before
    ``KindModel`` existed. Without this, the picker shows those kinds as
    featureless blobs.

    Same failure posture as ``resolve_kind``: a DB that is not wired is a
    platform defect, logged once, and yields an EMPTY tuple rather than
    raising — a picker that dies because a registry read failed is worse than
    a picker showing the schema-only view and saying so.
    """
    cached = _edge_cache.get(slug)
    if cached is not None and (time.monotonic() - cached[0]) < _CACHE_TTL_SECONDS:
        return cached[1]
    async with _cache_lock:
        cached = _edge_cache.get(slug)
        if cached is not None and (time.monotonic() - cached[0]) < _CACHE_TTL_SECONDS:
            return cached[1]
        entry, _reason = await resolve_kind(slug)
        if entry is None:
            return ()
        try:
            from matrx_graph.db._registry import get_instance

            rows = await get_instance("kind_edge_manager").load_items(parent_definition_id=entry.id)
        except Exception as exc:  # noqa: BLE001 — DB-not-wired is a platform defect
            _raise_if_programmer_error(exc, what=f"composition lookup for '{slug}'")
            _warn_once(
                f"__edges__{slug}",
                f"kind catalog: composition lookup for '{slug}' failed (DB not "
                f"configured or query error) — the availability index will show "
                f"only kinds whose schema pins __kind, so kinds registered "
                f"before KindModel will look empty. err={exc}",
            )
            return ()
        live = [r for r in rows or [] if getattr(r, "deleted_at", None) is None]
        pairs: list[tuple[str, str, int]] = []
        for row in live:
            child, _child_reason = await _resolve_kind_by_id(str(row.child_definition_id))
            if not child:
                continue
            position = getattr(row, "position", None)
            pairs.append(
                (str(row.field_name or ""), child, position if isinstance(position, int) else 0)
            )
        pairs.sort(key=lambda p: (p[2], p[0], p[1]))
        resolved = tuple((field, child) for field, child, _ in pairs)
        _edge_cache[slug] = (time.monotonic(), resolved)
        return resolved


async def _resolve_kind_by_id(definition_id: str) -> tuple[str, KindDegradedReason | None]:
    """A kind_edge child id -> its slug. Cached for the process lifetime.

    Edges reference kinds by ROW ID, so the index needs the reverse of the
    slug lookup. Kind ids are immutable, so this cache never expires — a
    re-registration mints a new row.
    """
    slug = _id_to_slug.get(definition_id)
    if slug is not None:
        return slug, None
    try:
        from matrx_graph.db._registry import get_instance

        rows = await get_instance("kind_definition_manager").load_items(id=definition_id)
    except Exception as exc:  # noqa: BLE001
        _raise_if_programmer_error(exc, what=f"id lookup for {definition_id}")
        return "", KindDegradedReason.CATALOG_UNREACHABLE
    live = [r for r in rows or [] if getattr(r, "deleted_at", None) is None]
    if not live:
        return "", KindDegradedReason.KIND_NOT_REGISTERED
    slug = str(getattr(live[0], "kind", "") or "")
    if slug:
        _id_to_slug[definition_id] = slug
    return slug, None


async def list_registered_kinds() -> tuple[tuple[str, int, dict[str, Any] | None], ...] | None:
    """Every live kind as ``(slug, version, emitted_json_schema)``, or None when unreachable.

    ``None`` and ``()`` mean DIFFERENT things and a caller must not conflate them: ``()`` is
    "the registry is reachable and holds no live kinds", ``None`` is "we could not ask". A
    consumer that treated an outage as an empty registry would silently declassify every kind
    block on the platform for the length of the outage.

    ONE query, and only the columns a consumer of this listing reads. Two things are
    deliberately NOT done here, both because they cost the whole registry to serve one slug:

    * the rows do NOT populate the per-slug ``_cache`` -- an entry there carries a
      metaschema verdict, and computing 1100 of them took **3.3 seconds** measured on the
      live registry, paid by the first chat stream of every process. ``resolve_kind`` still
      does the full job, per slug, for the slug somebody actually asked about.
    * ``is_active`` is not filtered: it is the FRONTEND's dual-gate flag and the engine
      ignores it in every mode (Arman, 2026-08-25) -- the same rule ``resolve_kind`` follows.

    So a schema from this listing is UNVERIFIED as a schema. That is safe for its consumers,
    which validate an instance against it and treat a malformed schema as "do not stamp".
    """
    global _registry_cache
    cached = _registry_cache
    if cached is not None and (time.monotonic() - cached[0]) < _CACHE_TTL_SECONDS:
        return cached[1]
    async with _cache_lock:
        cached = _registry_cache
        if cached is not None and (time.monotonic() - cached[0]) < _CACHE_TTL_SECONDS:
            return cached[1]
        try:
            mgr = _manager()
            model = getattr(mgr, "model", None)
            if model is not None and hasattr(model, "filter"):
                # Only the columns read below. The registry also carries `data`,
                # `sample_data`, `emitted_block_schema` and `variants` -- large jsonb nobody
                # here looks at.
                rows = await (
                    model.filter(deleted_at__isnull=True)
                    .only(
                        "kind",
                        "version",
                        "emitted_json_schema",
                        "published_to_web",
                        "organization_id",
                        "metadata",
                    )
                    .all()
                )
            else:
                rows = await mgr.load_items()
        except Exception as exc:  # noqa: BLE001 -- DB-not-wired is a platform defect
            _raise_if_programmer_error(exc, what="registry listing")
            _warn_once(
                "__registry__",
                f"kind catalog: listing the registry failed (catalog unreachable, not a "
                f"code defect) -- every ``__kind`` body stays a plain code block until it "
                f"recovers (degraded_reason={KindDegradedReason.CATALOG_UNREACHABLE.value}). "
                f"err={exc}",
            )
            return None

        by_slug: dict[str, list[Any]] = {}
        for row in rows or []:
            if getattr(row, "deleted_at", None) is not None:
                continue
            slug = str(getattr(row, "kind", "") or "")
            if not slug:
                continue
            by_slug.setdefault(slug, []).append(row)

        live: dict[str, tuple[int, dict[str, Any] | None]] = {}
        dispositions: dict[str, str | None] = {}
        for slug, candidates in by_slug.items():
            # Keep the sync stream listing aligned with ``resolve_kind``.  A
            # publisher reconciles the canonical organization row; accepting a
            # different public duplicate here makes a clean publisher dry-run
            # lie about the schema the stream will validate.
            row = _select_catalog_row(candidates)
            schema = getattr(row, "emitted_json_schema", None)
            live[slug] = (
                int(getattr(row, "version", 1) or 1),
                schema if isinstance(schema, dict) else None,
            )
            dispositions[slug] = _row_disposition(row)

        listed = tuple(sorted((slug, version, schema) for slug, (version, schema) in live.items()))
        _registry_dispositions.clear()
        _registry_dispositions.update(dispositions)
        _registry_cache = (time.monotonic(), listed)
        return listed


def _row_disposition(row: Any) -> str | None:
    """A registry row's declared ``metadata.disposition``, or None when undeclared."""
    metadata = getattr(row, "metadata", None)
    if not isinstance(metadata, dict):
        return None
    value = metadata.get("disposition")
    return value if isinstance(value, str) and value else None


def listed_kind_disposition(slug: str) -> str | None:
    """The disposition the last ``list_registered_kinds`` listing read for ``slug``.

    None when the slug was not listed, the listing never ran, or the kind is undeclared — a
    caller that needs "is this a record kind" treats every None as "no".
    """
    return _registry_dispositions.get(slug)


def invalidate_kind_catalog_cache() -> None:
    """Clear the process-wide kind cache (call after any registry mutation)."""
    global _registry_cache
    _registry_cache = None
    _registry_dispositions.clear()
    _cache.clear()
    _edge_cache.clear()
    _id_to_slug.clear()
    _warned_slugs.clear()


class KindCheck(BaseModel):
    """Result of one kind validation, distinguishing a PASS from a loud-skip.

    ``checked=False`` means the validation never ran; ``degraded_reason``
    names exactly why (the enumerable ``KindDegradedReason`` vocabulary —
    unregistered slug, missing/invalid emitted schema, unreachable catalog).
    Consumers must render that as "unchecked", never as a pass.
    ``checked=True`` + empty ``errors`` is a real verified pass.

    ``kind_version`` / ``kind_active`` carry the resolved registry row's
    version and dual-gate flag (``None`` when the row never resolved) so
    verdict persistence is version-addressable and fatal enforcement can
    reject inactive bindings without a second lookup.
    """

    model_config = ConfigDict(frozen=True)

    checked: bool
    errors: list[str] = []
    degraded_reason: KindDegradedReason | None = None
    kind_version: int | None = None
    kind_active: bool | None = None


async def check_against_kind(value: Any, slug: str) -> KindCheck:
    """Validate ``value`` against the kind's registered JSON Schema, keeping
    the "did validation actually run?" truth instead of discarding it.

    Unknown slug / missing or malformed schema / unreachable catalog fail
    OPEN with one loud log per slug (platform defect, not user input) and
    return ``checked=False`` with the named ``degraded_reason`` — the caller
    decides whether its context makes errors fatal (input contract) or
    diagnostic (output contract), and surfaces the skip as neutral, never as
    a pass. Fatal-enforcement escalation is the CALLER's job (scheduler /
    tool dispatch), driven by ``kind_enforcement_enabled`` +
    ``degraded_escalation``.
    """
    entry, reason = await resolve_kind(slug)
    if entry is None:
        if reason is KindDegradedReason.KIND_NOT_REGISTERED:
            _warn_once(
                slug,
                f"kind catalog: kind '{slug}' is not registered in "
                f"content_ir.kind_definition — validation SKIPPED "
                f"(degraded_reason={reason.value}). Register the kind (it is "
                f"declared by a NodeSpec) or fix the wiring.",
            )
        # catalog_unreachable already screamed inside resolve_kind.
        return KindCheck(checked=False, degraded_reason=reason)
    if entry.json_schema is None:
        _warn_once(
            slug,
            f"kind catalog: kind '{slug}' has no emitted_json_schema — "
            f"validation SKIPPED "
            f"(degraded_reason={KindDegradedReason.SCHEMA_UNAVAILABLE.value}). "
            f"Emit the schema for this kind.",
        )
        return KindCheck(
            checked=False,
            degraded_reason=KindDegradedReason.SCHEMA_UNAVAILABLE,
            kind_version=entry.version,
            kind_active=entry.is_active,
        )
    if entry.schema_errors:
        # resolve_kind already screamed once with the metaschema findings.
        return KindCheck(
            checked=False,
            degraded_reason=KindDegradedReason.SCHEMA_INVALID,
            kind_version=entry.version,
            kind_active=entry.is_active,
        )
    # VALIDATION TOLERANCE, NEVER STORAGE. ``emitted_json_schema`` is the
    # __kind-free wire export; a producer bound to this kind answers with the
    # __kind-injected block export. A LOCAL reduced copy is what gets validated
    # (schema-aware, so a kind that declares __kind for real keeps it) — the
    # caller's value is never mutated and never returned reduced, because the
    # marker is part of the data (KINDS_EVERYWHERE_PLAN §4.2). Only a verdict
    # leaves here. See matrx_graph.content_ir.markers.
    return KindCheck(
        checked=True,
        # Junk on a plain sub-structure's marker (``const ""``) is normalized
        # in the local copy, never refused: old rows written under the free-
        # string schema still read.
        errors=validate_instance(
            entry.json_schema,
            strip_kind_markers(
                normalize_nonidentity_markers(value, entry.json_schema), entry.json_schema
            ),
        ),
        kind_version=entry.version,
        kind_active=entry.is_active,
    )


async def validate_against_kind(value: Any, slug: str) -> list[str]:
    """Validate ``value`` against the kind's registered JSON Schema.

    Returns per-field error strings (``[]`` = valid). Unknown slug / missing
    schema / unwired DB fail OPEN with one loud log per slug (platform defect,
    not user input) — indistinguishable from a pass here; use
    ``check_against_kind`` when the caller must tell a skip from a pass.
    """
    return (await check_against_kind(value, slug)).errors


async def structured_kind_schema(slug: str) -> dict[str, Any] | None:
    """The value contract a STRUCTURED kind gives one input value (resolving the kind now), or
    None when the kind's value is plain or the catalog cannot say (gap 8; the plain/structured
    rule is ``types.input_surface.structured_value_schema``)."""
    from matrx_graph.types.input_surface import structured_value_schema

    entry, _reason = await resolve_kind(slug)
    if entry is None or entry.schema_errors:
        return None
    return structured_value_schema(entry.json_schema)


def _value_word(value: Any) -> str:
    if isinstance(value, str):
        return "text"
    if isinstance(value, bool):
        return "yes/no"
    if isinstance(value, int | float):
        return "a number"
    if isinstance(value, list):
        return "a list"
    return type(value).__name__


async def input_kind_problems(name: str, value: Any, slug: str, *, multiple: bool) -> list[str]:
    """Every way a landed input value misses its structured kind — ``[]`` when it fits.

    ``None``/``""`` is no value (the sourcing rules decide whether that blocks). With
    ``multiple`` the value is a list and each item is judged; every problem names the input,
    the item and the kind, e.g. ``candidates[1]: 'name' is a required property (kind
    'company_candidate')``."""
    if value is None or value == "":
        return []
    if multiple:
        if not isinstance(value, list):
            return [f"{name}: should be a list of '{slug}' values, got {_value_word(value)}"]
        items = [(f"{name}[{i}]", item) for i, item in enumerate(value)]
    else:
        items = [(name, value)]
    problems: list[str] = []
    for label, item in items:
        if not isinstance(item, dict):
            problems.append(f"{label}: should be one '{slug}' value (an object), got {_value_word(item)}")
            continue
        # The declaration supplies the identity: a typed value carries no marker of its own
        # (the same rule as a step's declared input kind); a marker it DOES carry is judged.
        judged = item if "__kind" in item else {"__kind": slug, **item}
        for err in await validate_against_kind(judged, slug):
            where, _, message = err.partition(": ")
            at = label if where == "(value)" else f"{label}.{where}"
            problems.append(f"{at}: {message} (kind '{slug}')")
    return problems


async def warm_input_kinds(definition: Any) -> None:
    """Resolve every kind a workflow's inputs declare, so a synchronous compile right after
    gives a structured input its kind's contract instead of the flagged plain fallback.

    Call before ``compile_graph`` wherever the compiled input surface is SERVED (the run form).
    A run never needs it: it judges landed values against the kind itself."""
    from matrx_graph.types.input_surface import structured_input_kind

    slugs: set[str] = set()
    for node in getattr(definition, "nodes", None) or []:
        if getattr(node, "spec_type", None) != "io.user_input":
            continue
        config = getattr(node, "config", None)
        fields = config.get("fields") if isinstance(config, dict) else None
        for fld in fields if isinstance(fields, list) else []:
            if isinstance(fld, dict):
                slug = structured_input_kind(fld.get("kind"), fld.get("type") or "text")
                if slug:
                    slugs.add(slug)
    for var in getattr(definition, "variables", None) or []:
        slug = structured_input_kind(getattr(var, "kind", ""), var.effective_type())
        if slug:
            slugs.add(slug)
    for slug in sorted(slugs):
        await resolve_kind(slug)
