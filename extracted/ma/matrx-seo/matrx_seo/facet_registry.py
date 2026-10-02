"""THE keyword-facet vocabulary, read from the registry a human controls.

WHY THIS FILE EXISTS (Arman's ruling, 2026-08-21): *"It's gotta be
deterministic, reliable, consistent, controlled. Otherwise, it's just ChatGPT
with a lot more hassle."* The dimensions a classifier applies are governed
data, not something living in an agent's head. Until D37 the vocabulary was
frozen in three places at once — a CHECK array in DDL, a hardcoded tuple in
``artifact_writers``, and a JSON-Schema enum on the agent row — so a dimension
a business invented was invisible to the classifier forever.

There is now exactly ONE authority: ``platform.categories`` under
``dimension='seo_facet'`` (parent row = the dimension, child row = one of its
values, child slug = ``dimension:value``). Everything the classifier is told,
and everything it is allowed to write, is BUILT FROM THIS TABLE at run time:

  * the vocabulary section of the prompt  → :meth:`FacetVocabulary.prompt_text`
  * the JSON-Schema the model must satisfy → :meth:`FacetVocabulary.output_schema`
  * the ``seo.keyword_facet`` rows written  → :meth:`FacetVocabulary.category_id`

SCOPE. A ``platform`` dimension is a universal fact every tenant shares. A
``site`` dimension (``metadata->>'site_id'``) belongs to one business and is
loaded only when a run names that site — which is the whole point: a dimension
a business invented this afternoon is a dimension the classifier applies this
evening.

THE REVISION. ``FacetVocabulary.platform_revision`` is the newest write time
across the PLATFORM half of the registry, fixed-width so plain string ordering
is time ordering. It is what makes ``classifier_version`` move when the
vocabulary moves, which is what re-queues affected keywords through the
existing ``seo.keyword_classification_queue`` ``target_version`` machinery.
Site dimensions deliberately do NOT move it — one business editing its private
vocabulary must not re-queue the global corpus.

AI-free, like the rest of the package: this reads rows and shapes text. The
host decides when to run an agent.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from .db.models_host import PlatformCategory

logger = logging.getLogger(__name__)

FACET_DIMENSION = "seo_facet"

#: The 13 UNIVERSAL dimensions — the facts a keyword carries with no site in
#: context, named ONCE here. They were also plain mirror columns on
#: ``seo.keyword`` until KI-035 stopped writing them (2026-08-25); the fact
#: store ``seo.keyword_facet`` is now the only place they live, read through
#: :mod:`matrx_seo.universal_facets`. This tuple names the DIMENSIONS — it does
#: NOT define the vocabulary of values each one allows.
UNIVERSAL_FACET_DIMENSIONS: tuple[str, ...] = (
    "intent_class",
    "fulfillment_mode",
    "audience_type",
    "funnel_stage",
    "transaction_direction",
    "local_intent",
    "urgency",
    "comparison_intent",
    "price_sensitivity",
    "query_form",
    "specificity",
    "brand_presence",
    "compliance_framing",
)


class FacetVocabularyError(RuntimeError):
    """The registry cannot describe a usable vocabulary, or the model named
    something the registry does not contain. Never downgraded to a warning:
    a silently-dropped dimension is exactly the defect D37 closes."""


@dataclass(frozen=True, slots=True)
class FacetValue:
    value: str
    label: str
    description: str | None
    category_id: str
    position: int | None
    #: The honest-decline member ("not clear"). Marked in the registry as
    #: ``metadata.abstain = true``; seeded automatically on dimension creation
    #: and protected from retirement (migration
    #: matrx-frontend/migrations/seo_facet_dimension_abstain.sql).
    abstain: bool = False


@dataclass(frozen=True, slots=True)
class FacetDimension:
    slug: str
    label: str
    description: str | None
    scope: str  # 'platform' | 'site'
    cardinality: str  # 'single' | 'multi'
    site_id: str | None
    category_id: str
    values: tuple[FacetValue, ...]
    #: Registry flag ``metadata.ai_classifiable`` (default true). False = the
    #: dimension is stamped by matchers / humans / derivation only (C3).
    ai_classifiable: bool = True

    @property
    def is_platform(self) -> bool:
        return self.scope == "platform"

    @property
    def real_values(self) -> tuple[FacetValue, ...]:
        """The values that assert something. The abstain member is a way to say
        nothing, so it is never one of the choices being counted."""
        return tuple(value for value in self.values if not value.abstain)

    @property
    def is_ready(self) -> bool:
        """THE HARD GATE, and it is structural, not editorial.

        Fewer than two real choices is the garbage case found by driving this
        live: ``equipment_class`` shipped with the single value ``crt_monitor``
        and the structured-output contract obliged the model to stamp it on
        keywords that had nothing to do with a CRT. It was not hallucinating —
        it was obeying a vocabulary that gave it no honest move.

        Same rule as ``seo.facet_dimension_readiness``'s ``is_ready``; the DB
        reports it to humans, this reports it to the classifier. A dimension
        that cannot be answered honestly is not offered at all."""
        return len(self.real_values) >= 2

    @property
    def can_abstain(self) -> bool:
        """A QUALITY flag, never a gate — deliberately not merged with
        ``is_ready``. Six platform dimensions have no "not clear" member, and
        gating on this would silently switch off classification that has worked
        for months. Whether they SHOULD gain one is a vocabulary judgement that
        belongs to the person who owns the vocabulary."""
        return any(value.abstain for value in self.values)

    def value_ids(self) -> dict[str, str]:
        return {value.value: value.category_id for value in self.values}


def _revision_stamp(moments: list[datetime | None]) -> str:
    """Fixed-width UTC stamp of the newest write. Fixed width matters: the
    classification queue compares ``classifier_version`` with plain ``<``, so a
    hash (unordered) would let a vocabulary change fail to re-queue anything."""
    real = [moment for moment in moments if moment is not None]
    if not real:
        return "00000000000000"
    newest = max(real)
    return newest.strftime("%Y%m%d%H%M%S")


def _semantic_fingerprint(dimensions: tuple["FacetDimension", ...]) -> str:
    """Hash of exactly what the classifier can SEE — the inputs to
    ``prompt_text`` and ``output_schema`` for the PLATFORM half of the
    vocabulary. A registry write that changes none of these (a color, an
    icon, a display label no prompt renders) hashes identically and
    therefore never moves ``classifier_version``. THE LANDMINE this closes
    (2026-08-24): revision was max(updated_at), so a typo fix re-queued the
    entire classified corpus for re-classification."""
    payload = [
        {
            "slug": dim.slug,
            "description": dim.description,
            "cardinality": dim.cardinality,
            "values": [
                {"value": v.value, "description": v.description, "abstain": v.abstain}
                for v in dim.values
            ],
        }
        for dim in dimensions
        if dim.is_platform
    ]
    canonical = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


async def _resolve_platform_revision(
    dimensions: tuple["FacetDimension", ...], legacy_stamp: str
) -> str:
    """Mint (or fetch) the fixed-width revision for this semantic shape.

    One row per distinct shape, minted the FIRST time it is observed —
    string ordering stays time ordering for the queue's ``<`` comparison.
    Bootstrap: the very first shape ever recorded adopts ``legacy_stamp``
    (the old max-updated_at value), so deploying the ledger does not itself
    mint a new version and re-queue anything."""
    from .db.models_seo import ClassifierRevisionLedger

    fingerprint = _semantic_fingerprint(dimensions)
    row = await ClassifierRevisionLedger.load_by_id_or_none(fingerprint)
    if row is not None:
        return str(row.revision)
    seen_any = await ClassifierRevisionLedger.filter().limit(1).all()
    minted = legacy_stamp if not seen_any else datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    try:
        await ClassifierRevisionLedger.create(
            semantic_hash=fingerprint, revision=minted, first_seen_at=datetime.now(UTC)
        )
    except Exception:  # noqa: BLE001 — concurrent mint of the same shape
        existing = await ClassifierRevisionLedger.load_by_id_or_none(fingerprint)
        if existing is not None:
            return str(existing.revision)
        raise
    return minted


@dataclass(frozen=True, slots=True)
class FacetVocabulary:
    """One resolved vocabulary: every dimension a given run may apply."""

    #: The dimensions this run WILL apply — ready ones only. Every consumer
    #: (prompt, output schema, value resolution, progress provenance) reads
    #: this one tuple, so the gate is applied in exactly one place.
    dimensions: tuple[FacetDimension, ...]
    #: Registered but NOT offered this run, with the reason. Reported, never
    #: silent: a dimension a user created and cannot see being applied must be
    #: explainable without reading code.
    skipped: tuple[tuple[str, str], ...]
    platform_revision: str
    site_id: str | None

    # ── lookup ──────────────────────────────────────────────────────────────

    @property
    def platform_dimensions(self) -> tuple[FacetDimension, ...]:
        return tuple(d for d in self.dimensions if d.is_platform)

    @property
    def site_dimensions(self) -> tuple[FacetDimension, ...]:
        return tuple(d for d in self.dimensions if not d.is_platform)

    def dimension(self, slug: str) -> FacetDimension | None:
        for candidate in self.dimensions:
            if candidate.slug == slug:
                return candidate
        return None

    def category_id(self, dimension: str, value: str) -> str:
        """Resolve ``dimension`` + ``value`` to its registry row id.

        RAISES on anything unknown. A model that invents a value must fail the
        item loudly — writing 12 of 13 dimensions and swallowing the 13th is
        how a vocabulary silently stops meaning anything."""
        found = self.dimension(dimension)
        if found is None:
            raise FacetVocabularyError(
                f"the model emitted dimension {dimension!r}, which is not in the facet "
                f"registry for this run (known: {', '.join(d.slug for d in self.dimensions)})"
            )
        resolved = found.value_ids().get(value)
        if resolved is None:
            raise FacetVocabularyError(
                f"the model emitted {dimension}={value!r}, which is not a registered value "
                f"of that dimension (allowed: {', '.join(v.value for v in found.values)}). "
                "Add it to the dimension first — that is a click, not a migration."
            )
        return resolved

    # ── what the classifier is TOLD ─────────────────────────────────────────

    def prompt_text(self) -> str:
        """The vocabulary section of the classifier prompt, rendered from the
        registry. This is the ONLY place the agent learns its dimensions —
        the agent row carries no copy to go stale."""
        if not self.dimensions:
            raise FacetVocabularyError(
                "the facet registry offers no READY dimensions, so there is nothing to "
                "classify honestly (a dimension needs at least two real, non-abstain values)"
            )
        lines: list[str] = []
        for index, dim in enumerate(self.dimensions, start=1):
            rendered = []
            for value in dim.values:
                note = f" ({value.description})" if value.description else ""
                if value.abstain:
                    note = f"{note} — THE HONEST DECLINE: choose this instead of guessing"
                rendered.append(f"{value.value}{note}")
            values = " | ".join(rendered)
            note = f" — {dim.description}" if dim.description else ""
            owner = "" if dim.is_platform else "  [this site's own dimension]"
            lines.append(f"{index}. {dim.slug}{note}: {values}{owner}")
        header = (
            f"THE DIMENSIONS ({len(self.dimensions)} of them). This list is governed data, "
            "read live from the platform's facet registry. Classify every keyword on EVERY "
            "dimension named here, and use ONLY the values listed for it — a value that is "
            "not listed does not exist. Where a dimension offers an honest decline, a "
            "confident wrong answer is worse than declining: take it when the words do not "
            "say."
        )
        return f"{header}\n\n" + "\n".join(lines)

    # ── what the classifier is ALLOWED TO SAY ───────────────────────────────

    def output_schema(self) -> dict[str, Any]:
        """Regenerate ``keyword_classification_batch_v1``'s JSON Schema from
        the registry: one enum-constrained property per PLATFORM dimension,
        plus a ``site_facets`` object for a site's own dimensions (whose
        allowed values are named in the prompt and enforced at the write —
        a shared agent row cannot carry one site's private enums)."""
        platform = self.platform_dimensions
        if not platform:
            raise FacetVocabularyError(
                "the facet registry has no READY platform dimensions (a dimension needs at "
                "least two real, non-abstain values); refusing to publish an output schema "
                "that would let the classifier say anything at all"
            )
        slugs = [dim.slug for dim in platform]
        properties: dict[str, Any] = {
            "__kind": {"type": "string", "description": "Always keyword_classification_v1"},
            "keyword_id": {
                "type": "string",
                "description": "The keyword_id copied verbatim from the input",
            },
            "phrase": {"type": "string"},
        }
        for dim in platform:
            properties[dim.slug] = {
                "type": "string",
                "enum": [value.value for value in dim.values],
                **({"description": dim.description} if dim.description else {}),
            }
        properties["site_facets"] = {
            "type": ["object", "null"],
            "description": (
                "Values for this site's OWN dimensions, keyed by dimension slug. "
                "Only the dimensions named as this site's own in the prompt; omit or "
                "null when the run has none."
            ),
            "additionalProperties": {"type": ["string", "null"]},
        }
        properties["overall_confidence"] = {
            "type": "integer",
            "description": "0-100 confidence in the dominant interpretation",
        }
        properties["per_fact_confidence"] = {
            "type": "object",
            "required": slugs,
            "properties": {slug: {"type": "integer"} for slug in slugs},
            "additionalProperties": False,
        }
        properties["secondary_interpretation"] = {
            "type": "object",
            "description": (
                "Runner-up value per dimension; null where there is no real rival reading"
            ),
            "properties": {slug: {"type": ["string", "null"]} for slug in slugs},
            "additionalProperties": False,
        }
        properties["standards"] = {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Exact standards named by the query when a compliance dimension is not none"
            ),
        }
        properties["error"] = {
            "type": ["string", "null"],
            "description": "Non-null ONLY when this keyword could not be classified",
        }
        return {
            "type": "object",
            "required": ["__kind", "classifier_version", "results"],
            "additionalProperties": False,
            "properties": {
                "__kind": {
                    "type": "string",
                    "description": "Always keyword_classification_batch_v1",
                },
                "classifier_version": {
                    "type": "string",
                    "description": "Echo of the classifier_version input",
                },
                "results": {
                    "type": "array",
                    "description": "One result per input keyword",
                    "items": {
                        "type": "object",
                        "required": [
                            "__kind",
                            "keyword_id",
                            "phrase",
                            *slugs,
                            "overall_confidence",
                            "per_fact_confidence",
                            "secondary_interpretation",
                            "standards",
                            "error",
                        ],
                        "properties": properties,
                        "additionalProperties": False,
                    },
                },
            },
        }


def _meta(row: Any) -> dict[str, Any]:
    raw = getattr(row, "metadata", None)
    return raw if isinstance(raw, dict) else {}


async def load_facet_vocabulary(site_id: str | None = None) -> FacetVocabulary:
    """Read the live vocabulary: every platform dimension, plus ``site_id``'s
    own dimensions when a site is in play.

    Two queries, no joins, no raw SQL — the registry is small (13 dimensions /
    45 values today) and this runs once per classifier run, not per keyword."""
    rows = await PlatformCategory.filter(dimension=FACET_DIMENSION, deleted_at__isnull=True).all()
    parents = [row for row in rows if getattr(row, "parent_id", None) is None]
    children_by_parent: dict[str, list[Any]] = {}
    for row in rows:
        parent_id = getattr(row, "parent_id", None)
        if parent_id is None:
            continue
        children_by_parent.setdefault(str(parent_id), []).append(row)

    dimensions: list[FacetDimension] = []
    platform_moments: list[datetime | None] = []
    for parent in parents:
        meta = _meta(parent)
        scope = str(meta.get("scope") or "platform")
        dim_site = meta.get("site_id")
        dim_site = str(dim_site) if dim_site else None
        if scope != "platform" and (site_id is None or dim_site != site_id):
            continue

        values: list[FacetValue] = []
        for child in sorted(
            children_by_parent.get(str(parent.id), []),
            key=lambda row: (
                getattr(row, "position", None) is None,
                getattr(row, "position", None) or 0,
                str(getattr(row, "name", "")),
            ),
        ):
            child_meta = _meta(child)
            slug = str(child.slug)
            key = str(child_meta.get("value") or (slug.split(":", 1)[1] if ":" in slug else slug))
            values.append(
                FacetValue(
                    value=key,
                    label=str(child.name),
                    description=(
                        str(child_meta["description"]) if child_meta.get("description") else None
                    ),
                    category_id=str(child.id),
                    position=getattr(child, "position", None),
                    abstain=bool(child_meta.get("abstain")),
                )
            )
            if scope == "platform":
                platform_moments.extend(
                    [getattr(child, "updated_at", None), getattr(child, "created_at", None)]
                )
        if scope == "platform":
            platform_moments.extend(
                [getattr(parent, "updated_at", None), getattr(parent, "created_at", None)]
            )
        dimensions.append(
            FacetDimension(
                slug=str(parent.slug),
                label=str(parent.name),
                description=(str(meta["description"]) if meta.get("description") else None),
                scope=scope,
                cardinality=str(meta.get("cardinality") or "single"),
                site_id=dim_site,
                category_id=str(parent.id),
                values=tuple(values),
                ai_classifiable=meta.get("ai_classifiable", True) is not False,
            )
        )

    # THE GATE, applied in exactly ONE place. A dimension that cannot be
    # answered honestly is not offered to the classifier at all — not to the
    # prompt, not to the output schema, not to value resolution. Registry
    # readiness replaced a sentence in the prompt, because prompt text is the
    # agent's opinion and this has to be a rule. Same predicate as
    # `seo.facet_dimension_readiness`.
    ready: list[FacetDimension] = []
    skipped: list[tuple[str, str]] = []
    for dimension in dimensions:
        # A dimension the registry marks NOT AI-classifiable is never offered:
        # its values are site-relative (traffic_class: brand / mismatch depend
        # on WHICH business) and are stamped by site matchers, human rulings and
        # derived defaults — never by the universal classifier (P10, C3).
        if not dimension.ai_classifiable:
            skipped.append((dimension.slug, "not offered: registry marks it not AI-classifiable"))
            continue
        if dimension.is_ready:
            ready.append(dimension)
            continue
        skipped.append(
            (
                dimension.slug,
                f"not offered: {len(dimension.real_values)} real value(s); a dimension "
                "needs at least two, or the classifier is forced to stamp the only one "
                "it has on everything",
            )
        )
    if skipped:
        logger.warning(
            "seo facet registry: %d dimension(s) are registered but NOT being applied — %s",
            len(skipped),
            "; ".join(f"{slug} ({reason})" for slug, reason in skipped),
        )
    dimensions = ready

    # Platform dimensions first, in a stable order, so the prompt and the
    # schema do not churn for a reason that is not a vocabulary change.
    dimensions.sort(key=lambda dim: (0 if dim.is_platform else 1, dim.slug))
    offered = tuple(dimensions)
    return FacetVocabulary(
        dimensions=offered,
        skipped=tuple(sorted(skipped)),
        platform_revision=await _resolve_platform_revision(
            offered, _revision_stamp(platform_moments)
        ),
        site_id=site_id,
    )


__all__ = [
    "FACET_DIMENSION",
    "UNIVERSAL_FACET_DIMENSIONS",
    "FacetDimension",
    "FacetValue",
    "FacetVocabulary",
    "FacetVocabularyError",
    "load_facet_vocabulary",
]
