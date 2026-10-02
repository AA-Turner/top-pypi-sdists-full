"""Canonical ORM-backed SEO identity + host-binding resolvers.

Keywords are UNIVERSAL rows — one row per (normalized_phrase, language),
shared by everyone, minted ONLY through ``seo.fn_upsert_keyword`` (identity
upsert; the DB owns normalization via ``seo.fn_normalize_phrase``). Never a
raw keyword INSERT, never an explicit organization_id (the Matrx System org
default owns it), and never a write to the retired ``intent``/``category``
columns — the classifier pipeline owns the 13 classification columns.

Observation-plane identity rows (``seo.location`` / ``seo.rank_target``) are
get-or-created against their live natural-unique tuples. Host bindings resolve
canonical ``web.site`` / ``web.page`` rows through package-owned read-only
models and FAIL CLOSED on a cross-org mismatch. Keyword→project linkage goes
through the platform association engine — never a join table, never a project
FK.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from matrx_orm import (
    Associations,
    EntityRef,
    EntityRegistry,
    platform_access_check,
)
from matrx_orm.operations.db_functions import call_db_function

from .contracts import (
    CollectionRequest,
    HostBindingRequest,
    ResolvedHostBinding,
    ResolvedSeoIdentity,
    SeoIdentityRequest,
)
from .db import models_seo as m
from .db.models_host import PlatformAssociation, WebPage, WebSite, WorkspaceProject

_WHITESPACE = re.compile(r"\s+")

KEYWORD_ENTITY_TOKEN = "seo_keyword"
PROJECT_ENTITY_TOKEN = "project"
KEYWORD_PROJECT_ROLE = "seo_keyword"
PAGE_ENTITY_TOKEN = "web_page"


def normalize_keyword_phrase(phrase: str) -> str:
    """Exact Python mirror of ``seo.fn_normalize_phrase``:
    ``lower(regexp_replace(btrim(p), '\\s+', ' ', 'g'))``. No stemming, no
    punctuation handling — used only where a DB round-trip is unavailable
    (in-memory paths, staleness pre-filters). Keyword CREATION always goes
    through ``seo.fn_upsert_keyword``."""
    normalized = _WHITESPACE.sub(" ", phrase.strip().lower())
    if not normalized:
        raise ValueError("SEO keyword phrase must be nonblank")
    return normalized


def _now() -> datetime:
    return datetime.now(UTC)


async def upsert_keyword(phrase: str, language: str = "en") -> tuple[str, bool]:
    """THE keyword intake path: ``seo.fn_upsert_keyword(phrase, language)``.
    Returns ``(keyword_id, created)``. Service-role write; universal row."""
    if not phrase.strip():
        raise ValueError("SEO keyword phrase must be nonblank")
    rows = await call_db_function(m.Keyword, "seo.fn_upsert_keyword", phrase, language)
    if not rows:
        raise RuntimeError(f"seo.fn_upsert_keyword returned no row for {phrase!r}")
    row = rows[0]
    return str(row["o_id"]), bool(row["o_created"])


async def upsert_keywords(
    items: list[tuple[str, str]],
) -> list[tuple[str, bool]]:
    """Batch keyword intake through one DB round trip.

    ``seo.fn_upsert_keywords`` preserves input order and delegates every item
    to the canonical single-keyword function, so normalization and identity
    ownership remain database-defined.
    """
    if not items:
        return []
    if any(not phrase.strip() for phrase, _language in items):
        raise ValueError("SEO keyword phrase must be nonblank")
    payload = [{"phrase": phrase, "language": language} for phrase, language in items]
    rows = await call_db_function(m.Keyword, "seo.fn_upsert_keywords", payload)
    if len(rows) != len(items):
        raise RuntimeError(
            f"seo.fn_upsert_keywords returned {len(rows)} rows for {len(items)} inputs"
        )
    ordered = sorted(rows, key=lambda row: int(row["input_index"]))
    expected_indexes = list(range(len(items)))
    actual_indexes = [int(row["input_index"]) for row in ordered]
    if actual_indexes != expected_indexes:
        raise RuntimeError(
            f"seo.fn_upsert_keywords returned invalid input indexes: {actual_indexes!r}"
        )
    return [(str(row["o_id"]), bool(row["o_created"])) for row in ordered]


class OrmSeoIdentityResolver:
    async def resolve(
        self, request: CollectionRequest, identity: SeoIdentityRequest
    ) -> ResolvedSeoIdentity:
        keyword_id, _created = await upsert_keyword(identity.keyword, identity.language)
        return await self._resolve_with_keyword_id(request, identity, keyword_id)

    async def _resolve_with_keyword_id(
        self,
        request: CollectionRequest,
        identity: SeoIdentityRequest,
        keyword_id: str,
    ) -> ResolvedSeoIdentity:
        now = _now()
        location_id: str | None = None
        if any(
            value is not None
            for value in (
                identity.country_code,
                identity.region,
                identity.city,
                identity.postal_code,
                identity.latitude,
                identity.longitude,
                identity.timezone,
            )
        ):
            location, _ = await m.Location.get_or_create(
                defaults={"id": str(uuid4()), "created_at": now},
                country_code=identity.country_code,
                region=identity.region,
                city=identity.city,
                postal_code=identity.postal_code,
                latitude=identity.latitude,
                longitude=identity.longitude,
                timezone=identity.timezone,
            )
            location_id = str(location.id)

        rank_target_id: str | None = None
        # DEF-25 (2026-07-24, follow-on to DEF-7/DEF-18): a `rank_target` row
        # is NEVER minted without a real `site_id`. `site_id` comes from the
        # request's canonical attribution authority — when the caller genuinely
        # has no site (an ad-hoc keyword→domain lab check, no `host_site_id`),
        # this is observation-only: no rank_target is created, and the SERP
        # snapshot alone is persisted by the provider adapter. This makes the
        # "no NULL-site rank_target" invariant structural, not caller-trusted.
        if identity.engine and request.site_id:
            rank_target, _ = await m.RankTarget.get_or_create(
                defaults={
                    "id": str(uuid4()),
                    "target_page_id": identity.target_page_id,
                    "settings": identity.settings,
                    "is_active": True,
                    "created_by": request.created_by,
                    "created_at": now,
                    "updated_at": now,
                    "metadata": {},
                },
                organization_id=request.organization_id,
                keyword_id=keyword_id,
                engine=identity.engine,
                language=identity.language,
                device=identity.device,
                search_type=identity.search_type,
                location_id=location_id,
                target_domain=identity.target_domain,
                site_id=request.site_id,
                deleted_at=None,
            )
            rank_target_id = str(rank_target.id)

        return ResolvedSeoIdentity(
            keyword_id=keyword_id,
            location_id=location_id,
            rank_target_id=rank_target_id,
        )

    async def resolve_many(
        self, request: CollectionRequest, identities: list[SeoIdentityRequest]
    ) -> list[ResolvedSeoIdentity]:
        keyword_results = await upsert_keywords(
            [(identity.keyword, identity.language) for identity in identities]
        )
        return [
            await self._resolve_with_keyword_id(request, identity, keyword_id)
            for identity, (keyword_id, _created) in zip(identities, keyword_results, strict=True)
        ]


class OrmHostBindingResolver:
    async def resolve(
        self, request: CollectionRequest, binding: HostBindingRequest
    ) -> ResolvedHostBinding:
        if binding.resource_kind == "web_site":
            site = await WebSite.load_by_id_or_none(binding.resource_id)
            if site is None:
                raise ValueError(
                    f"SEO host binding failed: web.site {binding.resource_id} does not exist"
                )
            if str(site.organization_id) != request.organization_id:
                raise ValueError(
                    f"SEO host binding refused: web.site {binding.resource_id} belongs to "
                    f"org {site.organization_id}, not {request.organization_id}"
                )
            return ResolvedHostBinding(
                site_id=str(site.id),
                page_id=None,
                canonical_url=str(site.root_url),
            )
        page = await WebPage.load_by_id_or_none(binding.resource_id)
        if page is None:
            raise ValueError(
                f"SEO host binding failed: web.page {binding.resource_id} does not exist"
            )
        if str(page.organization_id) != request.organization_id:
            raise ValueError(
                f"SEO host binding refused: web.page {binding.resource_id} belongs to "
                f"org {page.organization_id}, not {request.organization_id}"
            )
        return ResolvedHostBinding(
            site_id=str(page.site_id),
            page_id=str(page.id),
            canonical_url=str(page.url),
        )


def _keyword_project_associations() -> Associations:
    registry = EntityRegistry(
        token_map={
            KEYWORD_ENTITY_TOKEN: m.Keyword,
            PROJECT_ENTITY_TOKEN: WorkspaceProject,
        }
    )
    return Associations(
        association_model=PlatformAssociation,
        registry=registry,
        org_field="organization_id",
        # THE access policy for edge endpoints — iam.has_access_for, the same
        # function RLS and the file-access gate consult. Required whenever a
        # real person is behind the write: the engine refuses to authorize an
        # attended write by comparing organization columns, because a person
        # belongs to several organizations on purpose and org-equality denies
        # her her own rows. See matrx_orm.associations (module docstring).
        access_check=platform_access_check,
    )


async def link_keyword_to_project(
    keyword_id: str,
    project_id: str,
    *,
    org_id: str,
    user_id: str,
    settings: dict[str, Any] | None = None,
) -> Any:
    """Associate a seo.keyword with a workspace project through the canonical
    platform.associations edge (role-in-identity). ``settings`` is the keyword
    portfolio document stored as the edge's metadata."""
    return await _keyword_project_associations().associate(
        EntityRef(KEYWORD_ENTITY_TOKEN, keyword_id),
        EntityRef(PROJECT_ENTITY_TOKEN, project_id),
        org_id=org_id,
        role=KEYWORD_PROJECT_ROLE,
        metadata=settings,
        created_by=user_id,
    )


async def unlink_keyword_from_project(
    keyword_id: str,
    project_id: str,
    *,
    org_id: str,
) -> int:
    return await _keyword_project_associations().dissociate(
        EntityRef(KEYWORD_ENTITY_TOKEN, keyword_id),
        EntityRef(PROJECT_ENTITY_TOKEN, project_id),
        org_id=org_id,
        role=KEYWORD_PROJECT_ROLE,
    )


def _keyword_page_associations() -> Associations:
    registry = EntityRegistry(
        token_map={
            KEYWORD_ENTITY_TOKEN: m.Keyword,
            PAGE_ENTITY_TOKEN: WebPage,
        }
    )
    return Associations(
        association_model=PlatformAssociation,
        registry=registry,
        org_field="organization_id",
        access_check=platform_access_check,
    )


async def link_keyword_to_page(
    keyword_id: str,
    page_id: str,
    *,
    org_id: str,
    user_id: str,
    role: str,
    metadata: dict[str, Any] | None = None,
) -> Any:
    """Associate a seo.keyword with a web.page through the canonical
    platform.associations edge — the page-analysis/mapper analog of
    ``link_keyword_to_project``. ``role`` distinguishes the relationship
    (e.g. ``primary_target`` / ``supporting_target`` / ``discovered``)."""
    return await _keyword_page_associations().associate(
        EntityRef(KEYWORD_ENTITY_TOKEN, keyword_id),
        EntityRef(PAGE_ENTITY_TOKEN, page_id),
        org_id=org_id,
        role=role,
        metadata=metadata,
        created_by=user_id,
    )


__all__ = [
    "KEYWORD_ENTITY_TOKEN",
    "KEYWORD_PROJECT_ROLE",
    "PAGE_ENTITY_TOKEN",
    "PROJECT_ENTITY_TOKEN",
    "OrmHostBindingResolver",
    "OrmSeoIdentityResolver",
    "link_keyword_to_page",
    "link_keyword_to_project",
    "normalize_keyword_phrase",
    "unlink_keyword_from_project",
    "upsert_keyword",
    "upsert_keywords",
]
