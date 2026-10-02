"""Writers for the SEO agent artifacts — pure data in, rows out. NO AI here.

The host (aidream) runs the system agents and parses their JSON; these
functions persist the parsed artifacts per the keyword-plane contract
(`seo-keyword-agent-guide.md` + `seo-agent-prompt-library.md`). Keeping them in
the package keeps ONE writer per artifact shape, usable by any host, with the
standalone service staying AI-free.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from matrx_orm import ArrayArg, CrossOrgAssociationError, JsonbMerge, call_function, transaction

from .db import PACKAGE_DB_NAME
from .db import models_seo as m
from .db.models_host import WebPage, WebSite
from .facet_registry import (
    FacetVocabulary,
    FacetVocabularyError,
    load_facet_vocabulary,  # noqa: F401  (re-export convenience for hosts)
)
from .keyword_plane import reject_keyword_edge  # noqa: F401  (re-export convenience)

from matrx_orm.session.fallback import SYSTEM_ORGANIZATION_ID  # the org that owns system-tier rows — ONE definition

logger = logging.getLogger(__name__)


async def _link_keyword_to_page_best_effort(
    keyword_id: str,
    page_id: str,
    *,
    org_id: str,
    user_id: str,
    role: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Best-effort page<->keyword association. ``seo.keyword`` rows are
    UNIVERSAL (organization_id defaults to the Matrx System org — see
    ``orm_identity.py``), while ``web.page`` is org-scoped; the shared
    ``matrx_orm.Associations`` engine enforces a single ``org_id`` across
    both endpoints, so a universal keyword can never satisfy it against a
    tenant page's org. FIXED 2026-07-25: the engine now exempts
    system-vocabulary models (``_rls_variant="system"``) from the org-equality
    check, so this link normally succeeds. The wrapper stays best-effort —
    the site_keyword_value write (the DEF-22 deliverable) must never be lost
    over an enrichment edge: log loudly and continue."""
    from .orm_identity import link_keyword_to_page

    try:
        await link_keyword_to_page(
            keyword_id, page_id, org_id=org_id, user_id=user_id, role=role, metadata=metadata
        )
    except CrossOrgAssociationError as exc:
        logger.warning(
            "seo page<->keyword association skipped (universal-keyword vs "
            "org-scoped-page cross-org mismatch — see FOUND_DEFECTS.md): %s",
            exc,
        )


def _now() -> datetime:
    return datetime.now(UTC)


def _emitted_facets(
    result: dict[str, Any], vocabulary: FacetVocabulary, *, universal: bool = True
) -> dict[str, str]:
    """Every (dimension → value) this result actually asserts.

    Platform dimensions ride as top-level keys (they are also the legacy
    columns); a site's own dimensions ride inside ``site_facets`` because a
    shared agent row cannot carry one site's private enums. Both are read the
    same way here and both land in the same fact store.

    ``universal=False`` is THE KI-039 GUARD: a run that received business
    context (guidelines, a site's own dimensions in its prompt) asserts
    site-tier facts ONLY — its platform-dimension answers are discarded here,
    never written, so one tenant's worldview cannot reach the shared row."""
    emitted: dict[str, str] = {}
    platform_dims = vocabulary.platform_dimensions if universal else ()
    for dimension in platform_dims:
        value = result.get(dimension.slug)
        if isinstance(value, str) and value:
            emitted[dimension.slug] = value
    site_facets = result.get("site_facets")
    if isinstance(site_facets, dict):
        # THE CHANNEL IS VALIDATED, not trusted: ``site_facets`` may carry
        # ONLY this run's site dimensions. A platform slug here would resolve
        # cleanly and overwrite a shared universal fact through the side door
        # (adversarial finding, 2026-08-24) — so it fails the ITEM loudly
        # instead of being written or silently dropped.
        site_slugs = {dimension.slug for dimension in vocabulary.site_dimensions}
        for slug, value in site_facets.items():
            if not (isinstance(value, str) and value):
                continue
            if str(slug) not in site_slugs:
                raise FacetVocabularyError(
                    f"site_facets carried {slug!r}, which is not one of this run's site "
                    "dimensions — platform dimensions ride as top-level keys and are "
                    "never accepted through the site channel"
                )
            emitted[str(slug)] = value
    return emitted


async def _write_keyword_facets(
    *,
    keyword_id: str,
    organization_id: str | None,
    emitted: dict[str, str],
    vocabulary: FacetVocabulary,
    confidence: int | None,
    classifier_version: str,
    now: datetime,
    universal: bool = True,
) -> int:
    """Persist this keyword's facts into ``seo.keyword_facet``, idempotently.

    Re-classifying REPLACES a keyword's value on a dimension instead of
    stacking a second one: the existing active row for the same value is
    updated in place (so a re-run is a no-op plus a fresh stamp), and any other
    active row under a ``single``-cardinality dimension is soft-deleted. The
    partial unique index ``keyword_facet_kw_cat_uniq`` is the backstop, not the
    mechanism.

    An unregistered value RAISES (``FacetVocabularyError``) — the caller fails
    that item loudly. Dropping it silently is the exact defect D37 closes."""
    from .db.models_seo import KeywordFacet

    # Resolve EVERYTHING first: a partial write is worse than a refused one.
    resolved: dict[str, str] = {
        dimension: vocabulary.category_id(dimension, value) for dimension, value in emitted.items()
    }
    # What this run is ENTITLED TO RETRACT: every value of every
    # single-cardinality dimension the run actually considered. Scoped to the
    # run's vocabulary, so a dimension outside its scope is never disturbed —
    # and scoped to `source='classifier'` below, so a human ruling always wins.
    superseded_value_ids: set[str] = set()
    retract_scope = vocabulary.dimensions if universal else vocabulary.site_dimensions
    for dimension in retract_scope:
        if dimension.cardinality == "single":
            superseded_value_ids.update(dimension.value_ids().values())

    existing = await KeywordFacet.filter(keyword_id=keyword_id, deleted_at__isnull=True).all()
    existing_by_category = {str(row.category_id): row for row in existing}
    keep = set(resolved.values())

    written = 0
    async with transaction(PACKAGE_DB_NAME):
        for category_id in resolved.values():
            row = existing_by_category.get(category_id)
            if row is not None:
                await row.update(
                    source="classifier",
                    confidence=confidence,
                    classifier_version=classifier_version,
                    updated_at=now,
                )
            else:
                await KeywordFacet.create(
                    id=str(uuid4()),
                    keyword_id=keyword_id,
                    category_id=category_id,
                    organization_id=organization_id,
                    source="classifier",
                    confidence=confidence,
                    classifier_version=classifier_version,
                    created_at=now,
                    updated_at=now,
                )
            written += 1
        # Retract what THIS run superseded — including a dimension it once
        # asserted and has now honestly declined (an incomplete dimension where
        # no listed value is true). A human's ruling is never retracted by a
        # classifier, and a 'multi' dimension's other values are left alone.
        for category_id, row in existing_by_category.items():
            if category_id in keep or category_id not in superseded_value_ids:
                continue
            if str(getattr(row, "source", "")) != "classifier":
                continue
            await row.update(deleted_at=now, updated_at=now)
    return written


def _is_uuid(value: str) -> bool:
    """True only for a canonical UUID string — the shape ``seo.keyword.id`` holds."""
    try:
        return str(UUID(value)) == value
    except ValueError:
        return False


async def apply_keyword_classifications(
    batch: dict[str, Any],
    *,
    vocabulary: FacetVocabulary | None = None,
    universal: bool = True,
    allowed_keyword_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Persist a ``keyword_classification_batch_v1`` artifact.

    ONE store for the facts, plus the envelope:

    * ``seo.keyword_facet`` — THE fact store, and the ONLY place a fact lands.
      One row per (keyword, registered facet value), resolved through the
      registry the user controls, carrying source/confidence/classifier_version.
      Idempotent: re-classifying replaces a dimension's value rather than
      duplicating it.
    * the classification ENVELOPE on ``seo.keyword``
      (``classification_confidence`` / ``classification_detail`` /
      ``classified_at`` / ``classifier_version``) — metadata ABOUT the run, not
      a copy of its facts. ``fn_refresh_keyword_classification_queue`` compares
      ``classifier_version`` with ``<``, so this stamp is what keeps the
      backfill moving.

    🚨 **The 13 legacy mirror columns are NO LONGER WRITTEN (KI-035,
    2026-08-25).** They were a second copy of facts the fact store already
    held — proven redundant across all 2,740 classified keywords — and every
    reader in both repos now goes through ``seo.keyword_universal_facet``
    (frontend: ``features/marketing/seo/keyword/universal-facets.ts``; here:
    :mod:`matrx_seo.universal_facets`). The columns themselves survive until
    Arman rules on the DROP; nothing writes them, so they are frozen. Never
    re-add a mirror write.

    ``vocabulary`` is REQUIRED in practice — it is the run's live registry
    snapshot. It is optional in the signature only so a caller that genuinely
    has none can say so explicitly; that caller writes NO fact rows at all, and
    this writer says so in its summary rather than pretending the fact store
    was updated.

    Items with ``error`` set are skipped (reported, never fabricated). An item
    naming a value the registry does not contain is a DEFECT: it fails that
    item loudly, is counted in ``rejected_unknown_value``, and its message
    names the dimension, the value, and the fix.

    ``universal=False`` is THE KI-039 GUARD (register law, 2026-08-24): the
    batch came from a run that received business context, so it may write
    SITE-TIER facts only — platform facet rows are discarded and
    ``classifier_version`` is NOT stamped (the keyword remains eligible for the
    context-free universal sweep).

    ``allowed_keyword_ids`` is the set of ids the caller actually SENT. 🚨 A
    model echoes a UUID back imperfectly — live 2026-09-15…18 it returned
    ``9493a48e-de8-4da8-…`` (a dropped character) and ``3f9c52e5-整治4d94-…``,
    and the lookup raised ``ParameterError: invalid input syntax for type
    uuid``, which aborted the WHOLE batch mid-write and ended the nightly
    backfill early four nights running. An id the caller did not send — or one
    that is not even a UUID — is reported in ``missing_keyword_ids`` and never
    reaches the database; the rest of the batch lands. The keyword the model
    mangled stays unclassified, so the ledger settle requeues it with the
    attempt charged: row-level evidence, never a batch-wide abort."""
    classifier_version = str(batch.get("classifier_version") or "").strip()
    if not classifier_version:
        raise ValueError("classification batch is missing classifier_version")
    updated, skipped_error, missing = 0, 0, []
    facet_rows_written = 0
    rejected: list[str] = []
    now = _now()
    for result in batch.get("results") or []:
        if not isinstance(result, dict):
            continue
        if result.get("error"):
            skipped_error += 1
            continue
        keyword_id = str(result.get("keyword_id") or "").strip().lower()
        if not _is_uuid(keyword_id) or (
            allowed_keyword_ids is not None and keyword_id not in allowed_keyword_ids
        ):
            missing.append(keyword_id or "(blank)")
            continue
        row = await m.Keyword.load_by_id_or_none(keyword_id)
        if row is None:
            missing.append(keyword_id or "(blank)")
            continue
        confidence = result.get("overall_confidence")
        if vocabulary is not None:
            try:
                emitted = _emitted_facets(result, vocabulary, universal=universal)
                facet_rows_written += await _write_keyword_facets(
                    keyword_id=str(row.id),
                    organization_id=str(row.organization_id) if row.organization_id else None,
                    emitted=emitted,
                    vocabulary=vocabulary,
                    confidence=confidence if isinstance(confidence, int) else None,
                    classifier_version=classifier_version,
                    now=now,
                    universal=universal,
                )
            except FacetVocabularyError as exc:
                # LOUD, and the keyword is left untouched: half a classification
                # is not a classification.
                rejected.append(f"{keyword_id}: {exc}")
                logger.error(
                    "keyword classification REJECTED for %s (%s): %s",
                    keyword_id,
                    row.phrase,
                    exc,
                )
                continue
        if not universal:
            # KI-039: no envelope, no version stamp — the keyword stays
            # eligible for the context-free universal sweep.
            updated += 1
            continue
        detail = {
            "per_fact_confidence": result.get("per_fact_confidence") or {},
            "secondary_interpretation": result.get("secondary_interpretation") or {},
            "standards": result.get("standards") or [],
        }
        await row.update(
            classification_confidence=confidence,
            classification_detail=detail,
            classified_at=now,
            classifier_version=classifier_version,
            updated_at=now,
        )
        updated += 1
    summary = {
        "classifier_version": classifier_version,
        "updated": updated,
        "skipped_error": skipped_error,
        "missing_keyword_ids": missing,
        "facet_rows_written": facet_rows_written,
        "facet_store_written": vocabulary is not None,
        "rejected_unknown_value": rejected,
        "site_tier_only": not universal,
    }
    if missing:
        logger.error("keyword classification referenced unknown keyword ids: %s", missing)
    if rejected:
        logger.error(
            "keyword classification emitted %d value(s) that are not in the facet registry: %s",
            len(rejected),
            rejected,
        )
    logger.info("seo keyword classification applied: %s", summary)
    return summary


async def apply_keyword_serp_intent_analysis(
    keyword_id: str,
    artifact: dict[str, Any],
) -> None:
    """Persist the latest SERP-informed intent analysis without changing the
    intrinsic 13-field classification.

    The enhancement is a named projection inside ``classification_detail``.
    ``JsonbMerge`` makes the top-level merge atomic, so a concurrent intrinsic
    classifier cannot erase the analysis (and this writer cannot erase the
    classifier's confidence/standards envelope). ``seo.keyword`` is versioned,
    so the previous projection remains recoverable in ``history.row_versions``.
    """
    row = await m.Keyword.load_by_id_or_none(keyword_id)
    if row is None or row.deleted_at is not None:
        raise ValueError(f"SERP intent analysis references unknown keyword {keyword_id!r}")
    await row.update(
        classification_detail=JsonbMerge(
            "classification_detail", {"serp_intent_analysis": artifact}
        ),
        updated_at=_now(),
    )


async def _resolve_topic_ids(
    batch: dict[str, Any], *, assigner_version: str
) -> tuple[dict[str, str], list[str]]:
    """Create proposed topics (temp_id/slug graph order) and return
    slug-or-temp_id → topic_id for every referenced node."""
    existing = {str(t.slug): str(t.id) for t in await m.Topic.filter_items(deleted_at=None)}
    resolve: dict[str, str] = dict(existing)
    created: list[str] = []
    pending = [p for p in (batch.get("new_topics") or []) if isinstance(p, dict)]
    for _ in range(len(pending) + 1):
        still_pending = []
        for proposal in pending:
            parent_ref = str(proposal.get("parent_slug") or "")
            parent_id = resolve.get(parent_ref)
            if parent_ref and parent_id is None:
                still_pending.append(proposal)
                continue
            slug = str(proposal.get("slug") or "").strip()
            if not slug or slug in resolve:
                for key in (proposal.get("temp_id"), slug):
                    if key and slug in resolve:
                        resolve[str(key)] = resolve[slug]
                continue
            row = await m.Topic.create(
                id=str(uuid4()),
                # A topic the agent proposes joins the SHARED taxonomy (looked up by
                # slug with no organization filter): the system tier, named —
                # never the column default.
                organization_id=SYSTEM_ORGANIZATION_ID,
                name=str(proposal.get("name") or slug),
                slug=slug,
                node_type=str(proposal.get("node_type") or "service"),
                description=proposal.get("description"),
                aliases=proposal.get("aliases") or [],
                volatility=str(proposal.get("volatility") or "moderate"),
                is_builtin=False,
                parent_id=parent_id,
                metadata={
                    "proposed_by": assigner_version,
                    "justified_by_keyword_ids": proposal.get("justified_by_keyword_ids") or [],
                },
                created_at=_now(),
                updated_at=_now(),
            )
            resolve[slug] = str(row.id)
            if proposal.get("temp_id"):
                resolve[str(proposal["temp_id"])] = str(row.id)
            created.append(slug)
        if not still_pending:
            break
        pending = still_pending
    return resolve, created


# THE AGENT PROVENANCE VALUE for `seo.keyword_topic.assigned_by`. The version that
# produced the placement rides `metadata.placement.assigner_version`, so the column
# answers the ONE question every reader asks of it — machine or expert? — with a
# stable token. `'human'` is what `seo.gsc_set_keyword_topic` writes.
AGENT_PLACEMENT_SOURCE = "agent"

# THE LADDER TIER (P30 / KI-050) this writer answers for. `seo.keyword_topic.
# scope_tier` is NOT NULL with no database default (migration
# seo_keyword_placement_scope_tiers.sql), so every writer must supply it
# explicitly or the insert fails outright — an agent placement always states
# the SYSTEM tier, the lowest rung any site/brand/organization override wins
# over.
AGENT_SCOPE_TIER = "system"

# The two topic node types that are company offerings (brand-offerings cutover,
# matrx-frontend docs/db_rebuild/proposals/brand-offerings-cutover.md, D5). Every
# other node type is genuine taxonomy and stays on seo.keyword_topic.
OFFERING_NODE_TYPES = frozenset({"product", "service"})


async def _site_organization_id(site_id: str) -> str:
    site = await WebSite.load_by_id_or_none(site_id)
    if site is None or site.deleted_at is not None:
        raise ValueError(
            f"site {site_id} is not a live site, so its canonical offering rows cannot be written"
        )
    return str(site.organization_id)


async def _topic_node_types(topic_ids: set[str]) -> dict[str, str]:
    kinds: dict[str, str] = {}
    for topic_id in topic_ids:
        topic = await m.Topic.get_or_none(id=topic_id)
        kinds[topic_id] = str(topic.node_type) if topic is not None else ""
    return kinds


async def _site_available_offering(site_id: str, topic_id: str) -> str | None:
    """This site's brand offering for an offering topic, ONLY when the site
    offers it now. Every product/service ``seo.topic`` id is also its
    ``web.offering_template`` id (guarded in migration
    ``brand_offerings_step6g_assigner_proposes_availability.sql``). ``None``
    means the site does not offer it, and an agent never changes that (D2)."""
    offering_id = await call_function(
        PACKAGE_DB_NAME, "seo", "fn_site_available_offering_for_template", site_id, topic_id
    )
    return str(offering_id) if offering_id else None


async def _propose_offering(
    site_id: str,
    topic_id: str,
    *,
    keyword_ids: list[str],
    value_add: float | None,
    agent_name: str,
    provenance: dict[str, Any],
) -> str:
    """D2 (explicit availability): an agent that wants an offering the site does
    not offer PROPOSES it in the one approval queue
    (``seo.propose_site_offering_from_template``, one pending row per site and
    offering, keywords merged across runs, never re-opened once a person ruled).
    Returns the proposal's status."""
    rows = await call_function(
        PACKAGE_DB_NAME,
        "seo",
        "propose_site_offering_from_template",
        site_id,
        topic_id,
        ArrayArg(keyword_ids, "uuid"),
        value_add,
        agent_name,
        None,
        provenance,
        mode="rows",
    )
    return str(rows[0]["status"]) if rows else "not_recorded"


def _proposal_skip_reason(exc: BaseException) -> str:
    """The recorded reason one offering proposal could not be made.

    🚨 ONE UNRESOLVABLE ITEM NEVER FAILS THE SITE. From 2026-09-15 the assigner
    grew five product/service topics lazily (``metadata.proposed_by =
    'topicassign-v1'``). The "every product/service topic id is also its
    ``web.offering_template`` id" identity this path relies on was only ever
    checked ONCE, by the step-6g migration's guard, and the brand-offerings
    model is being collapsed into the topical map (Arman, 2026-09-17), so no
    template is minted for a new topic. ``propose_site_offering_from_template``
    then raised ``offering_template_not_found`` for that one topic, the raise
    escaped the whole batch, the claim was settled as a batch-wide failure and
    requeued untouched, and the same top-demand keywords of the platform's
    largest site were reclaimed and failed again every night from 2026-09-21.
    The proposal is skipped for that topic, the reason is recorded in the
    summary, and every other write of the batch (placements, map homes) lands.
    """
    text = f"{type(exc).__name__}: {exc}"
    code = (
        "offering_template_not_found"
        if "offering_template_not_found" in text
        else "proposal_failed"
    )
    return f"{code}: {text}"[:300]


_EMPTY_MAP_HOME_COUNTS: dict[str, int] = {
    "map_homed": 0,
    "map_home_created": 0,
    "map_home_moved": 0,
    "map_home_kept": 0,
    "map_home_kept_human": 0,
    "map_home_no_map": 0,
    "map_home_no_offering": 0,
}


async def _set_map_homes(site_id: str, keyword_ids: list[str]) -> dict[str, int]:
    """THE THIRD WRITE — the topical map's keyword home topic.

    The topical map (``seo.map_topic``) is the platform's single topic primitive
    (Arman, 2026-09-17). Migration 21 copied the 161 live brand offerings into
    the nine real brands' maps and set 452 keyword homes ONCE, from each
    keyword's primary offering. Nothing kept them current, so every placement
    this job made afterwards was invisible to the map and the map started going
    stale the day after it was populated.

    ``seo.set_site_keyword_map_home`` (migration 23) derives the home the same
    way migration 21 did, fills it only where it is unset or where THIS writer
    set it before, and never touches a home a person chose. A site whose brand
    has no map yet is a no-op that SAYS SO — it is not silently skipped.
    """
    if not keyword_ids:
        return dict(_EMPTY_MAP_HOME_COUNTS)
    rows = await call_function(
        PACKAGE_DB_NAME,
        "seo",
        "set_site_keyword_map_home",
        site_id,
        ArrayArg(sorted(set(keyword_ids)), "uuid"),
        mode="rows",
    )
    if not rows:
        return dict(_EMPTY_MAP_HOME_COUNTS)
    row = rows[0]
    counts = {
        "map_homed": int(row["homed"]),
        "map_home_created": int(row["created"]),
        "map_home_moved": int(row["moved"]),
        "map_home_kept": int(row["kept"]),
        "map_home_kept_human": int(row["kept_human"]),
        "map_home_no_map": int(row["no_map"]),
        "map_home_no_offering": int(row["no_offering"]),
    }
    if counts["map_home_no_map"]:
        logger.warning(
            "topical map: site %s has no map bound, so %d keyword placements got no "
            "home topic. The map will under-report until this site's brand has a map "
            "and the site carries a `uses` edge to it (seo.set_site_map).",
            site_id,
            counts["map_home_no_map"],
        )
    return counts


async def _write_canonical_placements(
    site_id: str, placements: list[dict[str, Any]]
) -> dict[str, Any]:
    """TRANSITION (brand-offerings cutover): the value resolver reads a site's
    keyword placements from ``seo.site_keyword_offering``. An agent placement made
    for a site is ALSO written there, through THE placement writer
    (``seo.write_site_keyword_offering``), which enforces availability,
    organization scope and P12 (a human ruling is never overwritten) in the
    database. An offering topic maps to the site's brand offering only when the
    site offers it. When it does not, nothing is placed and the offering is
    PROPOSED with the keywords the assigner chose (D2: an agent never makes an
    offering available on a site). A taxonomy placement takes the keyword off
    the site's offerings. Deleted when the assigner proposes brand offerings
    directly."""
    counts: dict[str, Any] = {
        "canonical_written": 0,
        "canonical_removed": 0,
        "canonical_human_protected": 0,
        "offering_proposals": 0,
        "keywords_awaiting_offering": 0,
        "offering_proposals_skipped": 0,
        "keywords_unproposable": 0,
        "offering_proposal_skips": [],
        **_EMPTY_MAP_HOME_COUNTS,
    }
    if not placements:
        return counts
    organization_id = await _site_organization_id(site_id)
    kinds = await _topic_node_types({p["topic_id"] for p in placements})
    offering_for: dict[str, str | None] = {}
    awaiting: dict[str, list[str]] = {}
    assigner_versions: set[str] = set()
    groups: dict[tuple[str | None, int | None, bool], list[str]] = {}
    group_placement: dict[tuple[str | None, int | None, bool], dict[str, Any]] = {}
    for placement in placements:
        topic_id = placement["topic_id"]
        offering_id: str | None = None
        if kinds.get(topic_id) in OFFERING_NODE_TYPES:
            if topic_id not in offering_for:
                offering_for[topic_id] = await _site_available_offering(site_id, topic_id)
            offering_id = offering_for[topic_id]
            if offering_id is None:
                awaiting.setdefault(topic_id, []).append(placement["keyword_id"])
                version = placement["placement"].get("assigner_version")
                if version:
                    assigner_versions.add(str(version))
                continue
        key = (offering_id, placement["confidence"], bool(placement["placement"].get("confirmed")))
        groups.setdefault(key, []).append(placement["keyword_id"])
        group_placement[key] = placement["placement"]
    placed_keyword_ids: list[str] = []
    for key, keyword_ids in groups.items():
        offering_id, confidence, _confirmed = key
        if offering_id is not None:
            placed_keyword_ids.extend(keyword_ids)
        rows = await call_function(
            PACKAGE_DB_NAME,
            "seo",
            "write_site_keyword_offering",
            organization_id,
            site_id,
            ArrayArg(keyword_ids, "uuid"),
            offering_id,
            None,
            AGENT_PLACEMENT_SOURCE,
            confidence,
            group_placement[key],
            mode="rows",
        )
        for row in rows:
            counts["canonical_written"] += int(row["written"])
            counts["canonical_removed"] += int(row["removed"])
            counts["canonical_human_protected"] += int(row["human_protected"])
    for topic_id, keyword_ids in awaiting.items():
        try:
            status = await _propose_offering(
                site_id,
                topic_id,
                keyword_ids=keyword_ids,
                value_add=None,
                agent_name="Offering assigner",
                provenance={"assignerVersions": sorted(assigner_versions)},
            )
        except Exception as exc:  # noqa: BLE001 — one topic's proposal never fails the batch
            reason = _proposal_skip_reason(exc)
            counts["offering_proposals_skipped"] += 1
            counts["keywords_unproposable"] += len(keyword_ids)
            counts["offering_proposal_skips"].append(
                {"topic_id": topic_id, "keyword_count": len(keyword_ids), "reason": reason}
            )
            logger.warning(
                "offering assigner: site %s topic %s proposal SKIPPED (%s); its %d keywords "
                "keep their tree placement and get no site placement",
                site_id,
                topic_id,
                reason,
                len(keyword_ids),
            )
            continue
        if status in ("created", "already_pending"):
            counts["offering_proposals"] += 1
            counts["keywords_awaiting_offering"] += len(keyword_ids)
        else:
            logger.info(
                "offering assigner: site %s topic %s not proposed (%s); %d keywords left unplaced",
                site_id,
                topic_id,
                status,
                len(keyword_ids),
            )
    counts.update(await _set_map_homes(site_id, placed_keyword_ids))
    return counts


async def apply_topic_assignments(
    batch: dict[str, Any],
    *,
    confidence_floor: int = 0,
    allowed_keyword_ids: set[str] | None = None,
    site_id: str | None = None,
) -> dict[str, Any]:
    """Persist a ``topic_assignment_batch_v1`` artifact: lazily create proposed
    topic nodes, then pin keywords (exactly one primary; transactional primary
    swap; secondaries sparse). The whole batch — topic creation, old-primary
    demotion, and link upserts — runs inside ONE ORM transaction, so a failure
    mid-batch can never leave a keyword's old primary demoted without its
    replacement landing (all-or-nothing).

    🚨 P12 — AGENTS APPLY, HUMANS WIN. A keyword whose current primary link was
    placed by a person (``assigned_by = 'human'``, what ``gsc_set_keyword_topic``
    writes) is SKIPPED entirely and counted as ``human_protected``. The assigner
    may not demote, re-point, or re-confirm an expert's ruling — not on this path
    and not on any other.

    ``confidence_floor`` splits what lands into rulings and PROPOSALS. A placement
    at or above the floor is applied confirmed; one below it is applied with
    ``metadata.placement.confirmed = false`` and shows up in the topics screen's
    proposed queue until a human confirms or replaces it. It still lands, because
    a candidate the expert can see and correct beats an empty tree — the same
    posture the auto-applied class rules take with
    ``site_keyword_value.metadata.classification``.

    ``site_id`` names the site the batch was run for. When it is given, every
    primary placement is also written as that site's canonical placement
    (``_write_canonical_placements``), because the value resolver reads only the
    canonical model. A run with no site has no site placement to write and says
    so in the summary.
    """
    assigner_version = str(batch.get("assigner_version") or "").strip()
    if not assigner_version:
        raise ValueError("topic assignment batch is missing assigner_version")
    assignments = batch.get("assignments") or []
    invalid_keyword_ids: list[str] = []
    for assignment in assignments:
        if not isinstance(assignment, dict) or assignment.get("error"):
            continue
        keyword_id = str(assignment.get("keyword_id") or "").strip()
        if not keyword_id or (
            allowed_keyword_ids is not None and keyword_id not in allowed_keyword_ids
        ):
            invalid_keyword_ids.append(keyword_id or "<missing>")
    if invalid_keyword_ids:
        raise ValueError(
            "topic assignment batch contains keyword ids outside its offered batch: "
            + ", ".join(sorted(set(invalid_keyword_ids)))
        )
    assigned, unknown_topic, skipped_error = 0, [], 0
    human_protected, proposals = 0, 0
    canonical_placements: list[dict[str, Any]] = []
    now = _now()
    async with transaction(PACKAGE_DB_NAME):
        resolve, created_topics = await _resolve_topic_ids(batch, assigner_version=assigner_version)
        for assignment in assignments:
            if not isinstance(assignment, dict):
                continue
            if assignment.get("error"):
                skipped_error += 1
                continue
            keyword_id = str(assignment.get("keyword_id") or "")
            current_primaries = await m.KeywordTopic.filter_items(
                keyword_id=keyword_id, is_primary=True
            )
            # P12: an expert ruling is untouchable. Checked BEFORE anything is
            # written, so a protected keyword costs no demotion and no upsert.
            if any(str(link.assigned_by or "") == "human" for link in current_primaries):
                human_protected += 1
                continue
            confidence = assignment.get("confidence")
            try:
                confidence_value = int(confidence) if confidence is not None else None
            except (TypeError, ValueError):
                confidence_value = None
            # No stated confidence reads as "unsure", never as "certain": an
            # unlabelled machine ruling is exactly what the proposal queue exists
            # to catch.
            confirmed = confidence_value is not None and confidence_value >= confidence_floor
            placement = {
                "origin": "agent",
                "confirmed": confirmed,
                "confidence": confidence_value,
                "assigner_version": assigner_version,
                "applied_at": now.isoformat(),
            }
            refs = [(str(assignment.get("primary_topic") or ""), True)] + [
                (str(slug), False) for slug in assignment.get("secondary_topics") or []
            ]
            for ref, is_primary in refs:
                topic_id = resolve.get(ref)
                if topic_id is None:
                    if ref:
                        unknown_topic.append(ref)
                    continue
                if is_primary:
                    for old in current_primaries:
                        if str(old.topic_id) != topic_id:
                            await old.update(is_primary=False, updated_at=now)
                existing = await m.KeywordTopic.get_or_none(
                    keyword_id=keyword_id, topic_id=topic_id
                )
                if existing is None:
                    await m.KeywordTopic.create(
                        id=str(uuid4()),
                        # THE LADDER TIER, explicit (P30 / register KI-050): an
                        # agent placement is the SYSTEM tier and always carries
                        # the Matrx System org. Never rely on the model default
                        # here — ORM context injection can override it with the
                        # request envelope's org, which stamps the operator's
                        # org onto platform opinion.
                        organization_id=SYSTEM_ORGANIZATION_ID,
                        keyword_id=keyword_id,
                        topic_id=topic_id,
                        is_primary=is_primary,
                        confidence=confidence_value,
                        assigned_by=AGENT_PLACEMENT_SOURCE,
                        scope_tier=AGENT_SCOPE_TIER,
                        metadata={"placement": placement},
                        created_at=now,
                        updated_at=now,
                    )
                else:
                    await existing.update(
                        is_primary=is_primary or existing.is_primary,
                        confidence=confidence_value,
                        assigned_by=AGENT_PLACEMENT_SOURCE,
                        scope_tier=AGENT_SCOPE_TIER,
                        metadata=JsonbMerge({"placement": placement}),
                        updated_at=now,
                    )
                if is_primary:
                    assigned += 1
                    if not confirmed:
                        proposals += 1
                    canonical_placements.append(
                        {
                            "keyword_id": keyword_id,
                            "topic_id": topic_id,
                            "confidence": confidence_value,
                            "placement": placement,
                        }
                    )
    if site_id:
        canonical = await _write_canonical_placements(site_id, canonical_placements)
    else:
        canonical = {
            "canonical_written": 0,
            "canonical_removed": 0,
            "canonical_human_protected": 0,
            "offering_proposals_skipped": 0,
            "keywords_unproposable": 0,
            "offering_proposal_skips": [],
            **_EMPTY_MAP_HOME_COUNTS,
        }
        if canonical_placements:
            logger.warning(
                "topic assignment ran with no site: %d placements were written to the "
                "shared topic tree only and are not any site's placement",
                len(canonical_placements),
            )
    summary = {
        **canonical,
        "canonical_site_id": site_id,
        "assigner_version": assigner_version,
        "topics_created": created_topics,
        "keywords_assigned": assigned,
        "keywords_proposed": proposals,
        "human_protected": human_protected,
        "confidence_floor": confidence_floor,
        "skipped_error": skipped_error,
        "unassignable": len(batch.get("unassignable") or []),
        "unknown_topic_refs": sorted(set(unknown_topic)),
    }
    if unknown_topic:
        logger.error(
            "topic assignment referenced unknown topic slugs: %s",
            summary["unknown_topic_refs"],
        )
    return summary


async def apply_site_topic_valuations(
    artifact: dict[str, Any],
    *,
    site_id: str,
    organization_id: str,
    created_by: str,
) -> dict[str, Any]:
    """Persist a ``site_topic_valuation_v1`` artifact into seo.site_topic_value
    (upsert on (site_id, topic)); confidence + valuer version ride metadata."""
    valuer_version = str(artifact.get("valuer_version") or "").strip()
    if not valuer_version:
        raise ValueError("site topic valuation is missing valuer_version")
    topics = await m.Topic.filter_items(deleted_at=None)
    slugs = {str(t.slug): str(t.id) for t in topics}
    kinds = {str(t.id): str(t.node_type or "") for t in topics}
    written, unknown = 0, []
    canonical_worth = 0
    offering_proposals = 0
    offering_proposal_skips: list[dict[str, str]] = []
    now = _now()
    for valuation in artifact.get("valuations") or []:
        if not isinstance(valuation, dict):
            continue
        topic_id = slugs.get(str(valuation.get("topic_slug") or ""))
        if topic_id is None:
            unknown.append(str(valuation.get("topic_slug") or "(blank)"))
            continue
        offering_match = valuation.get("offering_match", valuation.get("service_match"))
        offering_match = {
            "core_service": "core_offering",
            "adjacent_service": "adjacent_offering",
        }.get(offering_match, offering_match)
        fields = {
            # Wire adaptation, not a legacy shim: the column is offering_match
            # (KI-047); a pinned valuation agent may still emit the old key
            # until its prompt is re-versioned, so both spellings and the two
            # renamed enum values are adapted and ONE canonical column is written.
            "offering_match": offering_match,
            "lead_quality": valuation.get("lead_quality"),
            "audience_fit": valuation.get("audience_fit"),
            "capacity_appetite": valuation.get("capacity_appetite"),
            "brand_fit": valuation.get("brand_fit"),
            "weight": valuation.get("weight"),
            "notes": valuation.get("notes"),
            "metadata": {
                "confidence": valuation.get("confidence"),
                "valuer_version": valuer_version,
            },
            "updated_at": now,
        }
        existing = await m.SiteTopicValue.get_or_none(site_id=site_id, topic_id=topic_id)
        if existing is None:
            await m.SiteTopicValue.create(
                id=str(uuid4()),
                organization_id=organization_id,
                site_id=site_id,
                topic_id=topic_id,
                created_by=created_by,
                created_at=now,
                **fields,
            )
        else:
            await existing.update(**fields)
        written += 1
        if kinds.get(topic_id) in OFFERING_NODE_TYPES:
            # TRANSITION (brand-offerings cutover, D9): offering worth is read from
            # seo.site_offering_value and written through THE worth writer. A
            # valuation with no weight meant 50 points to the resolver, so 50 is
            # written and the row says where it came from.
            offering_id = await _site_available_offering(site_id, topic_id)
            if offering_id is None:
                # D2: the site does not offer it. A valuation that says the
                # business does not offer or avoids it proposes nothing; any
                # other valuation proposes offering it, with its points.
                negative = fields["lead_quality"] == "negative_value" or fields[
                    "offering_match"
                ] in ("not_offered", "actively_avoided")
                if not negative:
                    try:
                        status = await _propose_offering(
                            site_id,
                            topic_id,
                            keyword_ids=[],
                            value_add=fields["weight"],
                            agent_name="Site valuer",
                            provenance={"valuerVersion": valuer_version},
                        )
                    except Exception as exc:  # noqa: BLE001 — one topic never fails the valuation
                        reason = _proposal_skip_reason(exc)
                        offering_proposal_skips.append({"topic_id": topic_id, "reason": reason})
                        logger.warning(
                            "site valuer: site %s topic %s proposal SKIPPED (%s)",
                            site_id,
                            topic_id,
                            reason,
                        )
                        continue
                    if status in ("created", "already_pending"):
                        offering_proposals += 1
                continue
            await call_function(
                PACKAGE_DB_NAME,
                "seo",
                "write_site_offering_value",
                organization_id,
                site_id,
                offering_id,
                fields["weight"] if fields["weight"] is not None else 50,
                fields["lead_quality"],
                fields["offering_match"],
                fields["notes"],
                False,
                fields["audience_fit"],
                fields["capacity_appetite"],
                fields["brand_fit"],
                {
                    "confidence": valuation.get("confidence"),
                    "valuer_version": valuer_version,
                    "worth_points_from_resolver_default": fields["weight"] is None,
                },
            )
            canonical_worth += 1
    summary = {
        "valuer_version": valuer_version,
        "valuations_written": written,
        "canonical_worth_written": canonical_worth,
        "offering_proposals": offering_proposals,
        "offering_proposal_skips": offering_proposal_skips,
        "unknown_topic_slugs": sorted(set(unknown)),
        "open_questions": [
            q.get("question") for q in artifact.get("open_questions") or [] if isinstance(q, dict)
        ],
    }
    if unknown:
        logger.error(
            "site valuation referenced unknown topic slugs: %s",
            summary["unknown_topic_slugs"],
        )
    return summary


async def _upsert_site_keyword_value(
    *,
    site_id: str,
    keyword_id: str,
    organization_id: str,
    created_by: str,
    fields: dict[str, Any],
) -> str:
    """Get-or-create the one seo.site_keyword_value row for (site_id,
    keyword_id) and apply ``fields``. The one write path both page-analysis
    writers below use — DEF-22's un-degrade point for
    ``v_site_keyword_performance``."""
    now = _now()
    existing = await m.SiteKeywordValue.get_or_none(site_id=site_id, keyword_id=keyword_id)
    if existing is None:
        row = await m.SiteKeywordValue.create(
            id=str(uuid4()),
            organization_id=organization_id,
            site_id=site_id,
            keyword_id=keyword_id,
            created_by=created_by,
            created_at=now,
            updated_at=now,
            **fields,
        )
        return str(row.id)
    await existing.update(updated_at=now, **fields)
    return str(existing.id)


async def apply_page_keyword_analysis(
    artifact: dict[str, Any],
    *,
    site_id: str,
    page_id: str,
    organization_id: str,
    created_by: str,
) -> dict[str, Any]:
    """Persist a ``page_keyword_analysis_v1`` artifact (Page Analyzer):
    intake every referenced keyword, value the page's primary + supporting
    keywords on ``seo.site_keyword_value`` (content_role + workflow_status),
    and link page<->keyword through ``platform.associations``. Discovered
    keywords are intake-only (no site value yet — same posture as fresh
    research output; they surface for a later classify/assign/map pass)."""
    from .orm_identity import upsert_keywords

    analyzer_version = str(artifact.get("analyzer_version") or "").strip()
    if not analyzer_version:
        raise ValueError("page analysis artifact is missing analyzer_version")

    primary = artifact.get("inferred_primary_keyword") or {}
    supported = [k for k in artifact.get("supported_keywords") or [] if isinstance(k, dict)]
    discovered = [k for k in artifact.get("discovered_keywords") or [] if isinstance(k, dict)]

    primary_phrase = str(primary.get("phrase") or "").strip()
    phrases: list[str] = []
    if primary_phrase:
        phrases.append(primary_phrase)
    phrases.extend(str(k.get("phrase") or "").strip() for k in supported)
    phrases.extend(str(k.get("phrase") or "").strip() for k in discovered)
    phrases = [p for p in dict.fromkeys(phrases) if p]

    resolved = await upsert_keywords([(p, "en") for p in phrases]) if phrases else []
    keyword_id_by_phrase = {
        phrase: kid for phrase, (kid, _created) in zip(phrases, resolved, strict=True)
    }

    content_role = artifact.get("content_role")
    funnel_position = artifact.get("funnel_position")
    declared_vs_actual = artifact.get("declared_vs_actual") or {}
    gaps = artifact.get("gaps") or []
    cannibalization_risk = artifact.get("cannibalization_risk") or []
    # "targeted" = the live page targets this keyword — the DB check constraint's
    # ladder (candidate|targeted|in_progress|ranking|ignored|suppressed) has no
    # "mapped" value; writing it 500'd the first real Page Analyzer run (2026-07-26).
    workflow_status = "targeted" if declared_vs_actual.get("status") == "aligned" else "candidate"

    async def _value_and_link(phrase: str, evidence: Any, confidence: Any, role: str) -> str | None:
        keyword_id = keyword_id_by_phrase.get(phrase)
        if keyword_id is None:
            return None
        await _upsert_site_keyword_value(
            site_id=site_id,
            keyword_id=keyword_id,
            organization_id=organization_id,
            created_by=created_by,
            fields={
                "content_role": content_role,
                "workflow_status": workflow_status,
                "metadata": {
                    "analyzer_version": analyzer_version,
                    "evidence": evidence,
                    "confidence": confidence,
                    "funnel_position": funnel_position,
                    "declared_vs_actual": declared_vs_actual,
                    "gaps": gaps,
                    "cannibalization_risk": cannibalization_risk,
                    "page_id": page_id,
                    "page_url": artifact.get("page_url"),
                },
            },
        )
        await _link_keyword_to_page_best_effort(
            keyword_id,
            page_id,
            org_id=organization_id,
            user_id=created_by,
            role=role,
            metadata={
                "evidence": evidence,
                "confidence": confidence,
                "analyzer_version": analyzer_version,
            },
        )
        return keyword_id

    primary_keyword_id = None
    if primary_phrase:
        primary_keyword_id = await _value_and_link(
            primary_phrase, primary.get("evidence"), primary.get("confidence"), "primary_target"
        )

    supporting_ids: list[str] = []
    for item in supported:
        phrase = str(item.get("phrase") or "").strip()
        if not phrase:
            continue
        kid = await _value_and_link(
            phrase, item.get("evidence"), item.get("confidence"), "supporting_target"
        )
        if kid:
            supporting_ids.append(kid)

    discovered_ids: list[str] = []
    for item in discovered:
        phrase = str(item.get("phrase") or "").strip()
        keyword_id = keyword_id_by_phrase.get(phrase)
        if keyword_id is None:
            continue
        await _link_keyword_to_page_best_effort(
            keyword_id,
            page_id,
            org_id=organization_id,
            user_id=created_by,
            role="discovered",
            metadata={"evidence": item.get("evidence"), "confidence": item.get("confidence")},
        )
        discovered_ids.append(keyword_id)

    summary = {
        "analyzer_version": analyzer_version,
        "primary_keyword_id": primary_keyword_id,
        "supporting_keyword_ids": supporting_ids,
        "discovered_keyword_ids": discovered_ids,
        "content_role": content_role,
        "funnel_position": funnel_position,
        "declared_vs_actual": declared_vs_actual,
        "gaps": gaps,
        "cannibalization_risk": cannibalization_risk,
    }
    logger.info("seo page analysis applied: page=%s %s", page_id, summary)
    return summary


async def apply_page_keyword_map(
    artifact: dict[str, Any],
    *,
    site_id: str,
    organization_id: str,
    created_by: str,
) -> dict[str, Any]:
    """Persist a ``page_keyword_map_v1`` artifact (Page↔Keyword Mapper): the
    ONE writer that populates ``seo.site_keyword_value.workflow_status`` /
    ``content_role`` / ``priority_score`` at scale (DEF-22 — un-degrades
    ``v_site_keyword_performance``), links primary/supporting keywords to
    existing pages via ``platform.associations``, suppresses skipped
    keywords, and records proposed-but-not-yet-created pages for review
    (this writer never creates a ``web.page`` row — that stays a deliberate
    human/content-pipeline action)."""
    from .orm_identity import upsert_keyword

    mapper_version = str(artifact.get("mapper_version") or "").strip()
    if not mapper_version:
        raise ValueError("page-keyword map artifact is missing mapper_version")
    topic_slug = artifact.get("topic_slug")

    pages_mapped = 0
    keywords_assigned = 0
    unresolved_pages: list[str] = []
    proposed_pages: list[dict[str, Any]] = []

    for plan in artifact.get("page_plans") or []:
        if not isinstance(plan, dict):
            continue
        page_ref = plan.get("page") or {}
        existing_url = page_ref.get("existing_url")
        page_id: str | None = None
        is_proposed = False
        if existing_url:
            page_row = await WebPage.get_or_none(site_id=site_id, url=existing_url, deleted_at=None)
            if page_row is None:
                unresolved_pages.append(str(existing_url))
            else:
                page_id = str(page_row.id)
        else:
            is_proposed = True
            proposed = page_ref.get("proposed") or {}
            proposed_pages.append(
                {
                    "title": proposed.get("title"),
                    "url_slug": proposed.get("url_slug"),
                    "reason": proposed.get("reason"),
                    "primary_keyword": plan.get("primary_keyword"),
                    "supporting_keywords": plan.get("supporting_keywords") or [],
                    "content_role": plan.get("content_role"),
                    "brief": plan.get("brief"),
                }
            )

        content_role = plan.get("content_role")
        confidence = plan.get("confidence")
        phrases = [str(plan.get("primary_keyword") or "").strip()] + [
            str(p).strip() for p in plan.get("supporting_keywords") or []
        ]
        for idx, phrase in enumerate(p for p in phrases if p):
            keyword_id, _created = await upsert_keyword(phrase, "en")
            role = "primary" if idx == 0 else "supporting"
            await _upsert_site_keyword_value(
                site_id=site_id,
                keyword_id=keyword_id,
                organization_id=organization_id,
                created_by=created_by,
                fields={
                    "content_role": content_role,
                    "workflow_status": "targeted" if page_id else "candidate",
                    "priority_score": confidence,
                    "priority_computed_at": _now(),
                    "metadata": {
                        "mapper_version": mapper_version,
                        "topic_slug": topic_slug,
                        "page_id": page_id,
                        "existing_url": existing_url,
                        "brief": plan.get("brief"),
                        "role": role,
                    },
                },
            )
            keywords_assigned += 1
            if page_id:
                await _link_keyword_to_page_best_effort(
                    keyword_id,
                    page_id,
                    org_id=organization_id,
                    user_id=created_by,
                    role=role,
                    metadata={"mapper_version": mapper_version, "confidence": confidence},
                )
        if page_id or is_proposed:
            pages_mapped += 1

    keywords_suppressed = 0
    for skipped in artifact.get("skipped") or []:
        if not isinstance(skipped, dict):
            continue
        phrase = str(skipped.get("phrase") or "").strip()
        if not phrase:
            continue
        keyword_id, _created = await upsert_keyword(phrase, "en")
        await _upsert_site_keyword_value(
            site_id=site_id,
            keyword_id=keyword_id,
            organization_id=organization_id,
            created_by=created_by,
            fields={
                "workflow_status": "suppressed",
                "suppression_reason": skipped.get("reason"),
                "metadata": {"mapper_version": mapper_version, "topic_slug": topic_slug},
            },
        )
        keywords_suppressed += 1

    summary = {
        "mapper_version": mapper_version,
        "topic_slug": topic_slug,
        "pages_mapped": pages_mapped,
        "keywords_assigned": keywords_assigned,
        "keywords_suppressed": keywords_suppressed,
        "unresolved_pages": sorted(set(unresolved_pages)),
        "proposed_pages": proposed_pages,
        "conflicts": artifact.get("conflicts") or [],
    }
    if unresolved_pages:
        logger.error(
            "page-keyword map referenced unresolved existing pages: %s", summary["unresolved_pages"]
        )
    logger.info("seo page-keyword map applied: site=%s %s", site_id, summary)
    return summary


__all__ = [
    "AGENT_PLACEMENT_SOURCE",
    "FacetVocabulary",
    "FacetVocabularyError",
    "load_facet_vocabulary",
    "apply_keyword_classifications",
    "apply_keyword_serp_intent_analysis",
    "apply_page_keyword_analysis",
    "apply_page_keyword_map",
    "apply_site_topic_valuations",
    "apply_topic_assignments",
]
