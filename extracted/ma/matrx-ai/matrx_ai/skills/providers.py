"""SkillProvider — the read API the resolver / tools call against.

Two implementations are planned:

* ``DbSkillProvider`` (ship-now) — reads ``skill.definition`` via the
  host-injected ORM models (see ``matrx_ai.configure(db_models=...)``).
* ``FileSkillProvider`` (Phase 2) — walks a directory of SKILL.md folders.
  Used only for *ingestion* into the DB (SK-S2 / A2 — DB is source of truth).

Hard rules: SK-S9 (no raw SQL — go through generated managers),
SK-R10 (UUIDs everywhere), SK-S10 (crash loudly on missing model wiring).
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Literal, Protocol
from uuid import UUID

from matrx_utils import vcprint

from matrx_ai.skills.models import SkillBody, SkillHint

# Skill categories live in the consolidated, dimension-based category table
# (platform.categories, 2026-06-28 canonical reorg) alongside every other
# category family. The skill subset is the rows where dimension == "skill";
# every category read this provider issues is scoped to it.
_SKILL_DIMENSION = "skill"
SkillCatalogScope = Literal["owned", "visible"]

# ---------------------------------------------------------------------------
# Process-level skill catalog cache
# ---------------------------------------------------------------------------
# WHY this exists: the resolver renders the "skills exist, here's how to
# search" overview on EVERY chat turn — even for an agent with zero configured
# skills (the overview is the discovery hint). That means category_overview()
# ran ~5 *filtered* queries (categories + system/public/user skill slices) per
# turn. The ORM's per-record SHORT_TERM cache only serves load_by_id()/get()
# (primary-key lookups); filter_items() reads bypass it and hit Postgres every
# call. Across a remote pooler that was ~0.5s/turn of turn-invariant work.
#
# The catalog is overwhelmingly stable: system + public skills + the category
# tree are global and change rarely; a user's own skills change only when that
# user edits them. So cache the *whole* visible universe process-wide and slice
# it in memory — exactly the "load them all and cache" shape the ORM record
# cache can't give us. Keyed with a short TTL so edits surface without an
# explicit bust; call invalidate_skill_catalog_cache() to drop it immediately.
_CATALOG_TTL_SECONDS = 300.0
_SYSTEM_PUBLIC_KEY = "__system_public__"

_catalog_lock = asyncio.Lock()
# dimension -> (loaded_at_monotonic, rows)
_categories_cache: dict[str, tuple[float, list[Any]]] = {}
# _SYSTEM_PUBLIC_KEY or user_id(str) -> (loaded_at_monotonic, rows)
_skills_cache: dict[str, tuple[float, list[Any]]] = {}


def _cache_fresh(entry: tuple[float, Any] | None) -> bool:
    return entry is not None and (time.monotonic() - entry[0]) < _CATALOG_TTL_SECONDS


def invalidate_skill_catalog_cache() -> None:
    """Drop the process-level skill catalog cache (categories + skill slices).

    Call after a skill or skill-category create/update/delete so the next read
    reloads. Cheap; the next resolver pass refills lazily.
    """
    _categories_cache.clear()
    _skills_cache.clear()


async def preload_skill_catalog() -> None:
    """Warm the global (system + public) skill slice + the category tree at
    startup so the first real chat turn never pays the cold catalog load.

    Best-effort: never raises (a missing DB wiring at boot must not crash the
    server). Per-user slices still fill lazily on first use.
    """
    try:
        provider = DbSkillProvider()
        await provider._load_category_rows()
        await provider._get_system_public_rows()
        vcprint("[skills] catalog preloaded (categories + system/public)", color="green")
    except Exception as exc:
        vcprint(f"[skills] catalog preload skipped (non-fatal): {exc!r}", color="yellow")


class SkillProvider(Protocol):
    """Read API every skill consumer goes through."""

    async def list_hints(
        self,
        *,
        user_id: UUID | None = None,
        category_key: str | None = None,
        limit: int = 50,
        scope: SkillCatalogScope = "visible",
    ) -> list[SkillHint]: ...

    async def get_by_id(
        self,
        skill_uuid: UUID,
        *,
        user_id: UUID | None = None,
    ) -> SkillBody | None: ...

    async def get_many_by_ids(
        self,
        skill_uuids: list[UUID],
        *,
        user_id: UUID | None = None,
    ) -> list[SkillBody]: ...

    async def search(
        self,
        query: str,
        *,
        category_key: str | None = None,
        user_id: UUID | None = None,
        limit: int = 10,
    ) -> list[SkillHint]: ...

    async def category_overview(
        self,
        *,
        user_id: UUID | None = None,
    ) -> list[tuple[str, str, int]]:
        """Top-level categories: (key, description, active_skill_count)."""
        ...


# ---------------------------------------------------------------------------
# DbSkillProvider
# ---------------------------------------------------------------------------


def _row_to_hint(row: Any, category_path: list[str]) -> SkillHint:
    from matrx_ai.skills.models import SkillHint

    allowed = getattr(row, "allowed_tools", None) or []
    return SkillHint(
        id=UUID(str(row.id)),
        skill_id=row.skill_id,
        label=row.label,
        description=row.description,
        skill_type=str(row.skill_type) if row.skill_type is not None else "reference",
        category_path=category_path,
        has_resources=False,  # filled in lazily by callers that need it
        has_allowed_tools=bool(allowed),
    )


def _row_to_body(row: Any, category_path: list[str]) -> SkillBody:
    raw_allowed = getattr(row, "allowed_tools", None) or []
    allowed: list[UUID] = []
    if isinstance(raw_allowed, list):
        for entry in raw_allowed:
            if isinstance(entry, UUID):
                allowed.append(entry)
            elif isinstance(entry, str):
                try:
                    allowed.append(UUID(entry))
                except ValueError:
                    # Bad data — skip silently here; startup_check is the
                    # canonical place that flags this loudly (SK-R15).
                    continue

    raw_triggers = getattr(row, "trigger_patterns", None) or []
    triggers: list[str] = (
        [str(t) for t in raw_triggers if isinstance(t, str)]
        if isinstance(raw_triggers, list)
        else []
    )

    return SkillBody(
        id=UUID(str(row.id)),
        skill_id=row.skill_id,
        label=row.label,
        description=row.description,
        skill_type=str(row.skill_type) if row.skill_type is not None else "reference",
        body=row.body or "",
        category_path=category_path,
        allowed_tools=allowed,
        trigger_patterns=triggers,
        disable_auto_invocation=bool(getattr(row, "disable_auto_invocation", False)),
        version=getattr(row, "version", None),
    )


class DbSkillProvider:
    """Postgres-backed provider. Reads via matrx-orm-generated managers.

    Ownership filter: when ``user_id`` is passed, results are scoped to
    skills the user owns (``created_by``) OR system skills (``is_system=true``)
    OR public skills (``visibility='public'``). Mirrors ``_visible_rows`` in
    ``aidream/api/routers/skills.py``.
    """

    def __init__(self) -> None:
        self._category_cache: dict[UUID, list[str]] = {}
        self._categories_loaded: bool = False

    # ---- lazy manager handles -------------------------------------------------

    @staticmethod
    def _defs_manager() -> Any:
        # No aidream fallback import: on a client host the old
        # ``from db.managers...`` except-path turned a clean registry error
        # into an uncaught ModuleNotFoundError that hard-crashed the skill
        # tool. The host injects ``skl_definitions_manager`` via
        # db_requirements; a missing registration raises the registry's own
        # descriptive error (SK-S10: crash loudly on missing wiring).
        from matrx_ai.db._registry import get_instance

        return get_instance("skl_definitions_manager")

    @staticmethod
    def _categories_manager() -> Any:
        from matrx_ai.db._registry import get_instance

        return get_instance("skl_categories_manager")

    # DELETED — skill.resource table retired; attachments use platform.associations.

    # ---- category path resolution --------------------------------------------

    async def _load_category_rows(self) -> list[Any]:
        """Live (non-deleted) skill-dimension category rows, process-cached.

        Shared by _ensure_categories (path map) and category_overview
        (top-level buckets) so the category table is read at most once per TTL
        window instead of twice per request.
        """
        cached = _categories_cache.get(_SKILL_DIMENSION)
        if _cache_fresh(cached):
            return cached[1]
        async with _catalog_lock:
            cached = _categories_cache.get(_SKILL_DIMENSION)
            if _cache_fresh(cached):
                return cached[1]
            mgr = self._categories_manager()
            rows = await mgr.load_items(dimension=_SKILL_DIMENSION)
            rows = [r for r in rows if getattr(r, "deleted_at", None) is None]
            _categories_cache[_SKILL_DIMENSION] = (time.monotonic(), rows)
            return rows

    async def _ensure_categories(self) -> None:
        if self._categories_loaded:
            return
        rows = await self._load_category_rows()
        by_id: dict[UUID, Any] = {UUID(str(r.id)): r for r in rows}

        def walk(cat_uuid: UUID) -> list[str]:
            chain: list[str] = []
            seen: set[UUID] = set()
            cur = by_id.get(cat_uuid)
            while cur is not None:
                if UUID(str(cur.id)) in seen:
                    break  # defensive: no cycles
                seen.add(UUID(str(cur.id)))
                chain.append(cur.slug or cur.name)
                parent_raw = getattr(cur, "parent_id", None)
                if parent_raw is None:
                    break
                cur = by_id.get(UUID(str(parent_raw)))
            chain.reverse()
            return chain

        self._category_cache = {cid: walk(cid) for cid in by_id}
        self._categories_loaded = True

    def _category_path(self, category_id: Any) -> list[str]:
        if category_id is None:
            return []
        try:
            cuid = UUID(str(category_id))
        except (ValueError, TypeError):
            return []
        return self._category_cache.get(cuid, [])

    # ---- public API -----------------------------------------------------------

    def _ownership_predicate(self, user_id: UUID | None) -> dict[str, Any]:
        # filter_items doesn't natively express OR, so callers that need
        # the full visible set fetch system+public+user separately and
        # union them. This helper returns the *user-owned* slice only.
        if user_id is None:
            return {"is_active": True}
        return {"is_active": True, "created_by": str(user_id)}

    async def _get_system_public_rows(self) -> list[Any]:
        """Global system + public active skills, process-cached (user-agnostic)."""
        cached = _skills_cache.get(_SYSTEM_PUBLIC_KEY)
        if _cache_fresh(cached):
            return cached[1]
        async with _catalog_lock:
            cached = _skills_cache.get(_SYSTEM_PUBLIC_KEY)
            if _cache_fresh(cached):
                return cached[1]
            mgr = self._defs_manager()
            # `is_system` is a curation flag ("platform-maintained, not
            # user-authored") — NOT a visibility override. Filesystem ingest
            # (`ingest_filesystem`) writes every row with is_system=true, so
            # without the visibility check here every ingested dev-tooling
            # skill (default visibility='internal') would leak into every
            # user's agent catalog. Only public system skills belong here;
            # internal ones stay admin-only, same as the RLS/`has_access`
            # semantics on the direct-Supabase read path.
            system_rows = await mgr.filter_items(
                is_active=True, is_system=True, visibility="public"
            )
            public_rows = await mgr.filter_items(is_active=True, visibility="public")
            seen: set[str] = set()
            rows: list[Any] = []
            for row in [*system_rows, *public_rows]:
                rid = str(row.id)
                if rid in seen:
                    continue
                seen.add(rid)
                rows.append(row)
            _skills_cache[_SYSTEM_PUBLIC_KEY] = (time.monotonic(), rows)
            return rows

    async def _get_user_rows(self, user_id: UUID) -> list[Any]:
        """A single user's own active skills, process-cached per user_id."""
        key = str(user_id)
        cached = _skills_cache.get(key)
        if _cache_fresh(cached):
            return cached[1]
        async with _catalog_lock:
            cached = _skills_cache.get(key)
            if _cache_fresh(cached):
                return cached[1]
            mgr = self._defs_manager()
            rows = await mgr.filter_items(is_active=True, created_by=key)
            _skills_cache[key] = (time.monotonic(), rows)
            return rows

    async def _fetch_visible(
        self,
        *,
        user_id: UUID | None,
        category_id: Any = None,
        scope: SkillCatalogScope = "visible",
    ) -> list[Any]:
        # Read the whole visible universe from the process cache (system/public
        # global + this user's slice) and filter category_id in memory — the
        # filtered query path the ORM record-cache can't serve is gone.
        if scope not in ("owned", "visible"):
            raise ValueError(f"unsupported skill catalog scope: {scope!r}")
        user_rows = await self._get_user_rows(user_id) if user_id is not None else []
        system_public = await self._get_system_public_rows() if scope == "visible" else []

        cat = str(category_id) if category_id is not None else None

        # Dedup by id, preserving stable order: system/public → owned.
        seen: set[str] = set()
        out: list[Any] = []
        for row in [*system_public, *user_rows]:
            row_id = str(row.id)
            if row_id in seen:
                continue
            if cat is not None and str(getattr(row, "category_id", "")) != cat:
                continue
            seen.add(row_id)
            out.append(row)
        return out

    async def list_hints(
        self,
        *,
        user_id: UUID | None = None,
        category_key: str | None = None,
        limit: int = 50,
        scope: SkillCatalogScope = "visible",
    ) -> list[SkillHint]:
        await self._ensure_categories()

        category_id: Any = None
        if category_key is not None:
            cmgr = self._categories_manager()
            matches = await cmgr.filter_items(dimension=_SKILL_DIMENSION, slug=category_key)
            if not matches:
                return []
            category_id = matches[0].id

        rows = await self._fetch_visible(
            user_id=user_id,
            category_id=category_id,
            scope=scope,
        )
        hints = [
            _row_to_hint(row, self._category_path(getattr(row, "category_id", None)))
            for row in rows
        ]

        # Stable sort by category_path, then sort_order, then label so the
        # agent sees a deterministic listing.
        hints.sort(key=lambda h: (h.category_path, h.label.lower()))
        return hints[:limit]

    async def get_by_id(
        self,
        skill_uuid: UUID,
        *,
        user_id: UUID | None = None,
    ) -> SkillBody | None:
        await self._ensure_categories()
        mgr = self._defs_manager()
        try:
            row = await mgr.load_by_id(str(skill_uuid))
        except Exception:
            return None
        if row is None or not getattr(row, "is_active", True):
            return None

        # Ownership gate — same shape as the universe in _fetch_visible.
        # `is_system` alone doesn't grant visibility (see _get_system_public_rows) —
        # a non-owner needs the row to actually be public.
        if user_id is not None:
            is_owner = str(getattr(row, "created_by", "") or "") == str(user_id)
            is_public = getattr(row, "visibility", None) == "public"
            if not (is_owner or is_public):
                return None

        return _row_to_body(row, self._category_path(getattr(row, "category_id", None)))

    async def get_many_by_ids(
        self,
        skill_uuids: list[UUID],
        *,
        user_id: UUID | None = None,
    ) -> list[SkillBody]:
        out: list[SkillBody] = []
        for uid in skill_uuids:
            body = await self.get_by_id(uid, user_id=user_id)
            if body is not None:
                out.append(body)
        return out

    async def search(
        self,
        query: str,
        *,
        category_key: str | None = None,
        user_id: UUID | None = None,
        limit: int = 10,
    ) -> list[SkillHint]:
        hints = await self.list_hints(user_id=user_id, category_key=category_key, limit=10_000)
        q = query.strip().lower()
        if not q:
            return hints[:limit]

        # Score: label match > description match > body match (body fetched lazily
        # to keep list_hints lightweight). v1 is keyword + token containment;
        # semantic mode can ride the same signature later.
        scored: list[tuple[int, SkillHint]] = []
        for h in hints:
            score = 0
            label_lower = h.label.lower()
            desc_lower = h.description.lower()
            if q in label_lower:
                score += 10
            if q in desc_lower:
                score += 4
            if any(tok in label_lower for tok in q.split()):
                score += 2
            if any(tok in desc_lower for tok in q.split()):
                score += 1
            if score > 0:
                scored.append((score, h))

        # If nothing matched yet, fall back to body scan for the top candidates.
        if not scored:
            for h in hints[:50]:
                body = await self.get_by_id(h.id, user_id=user_id)
                if body and q in body.body.lower():
                    scored.append((1, h))

        scored.sort(key=lambda pair: (-pair[0], pair[1].label.lower()))
        return [h for _, h in scored[:limit]]

    async def category_overview(
        self,
        *,
        user_id: UUID | None = None,
    ) -> list[tuple[str, str, int]]:
        await self._ensure_categories()
        cats = await self._load_category_rows()

        # Top-level only — parent_id IS NULL.
        top = [c for c in cats if getattr(c, "parent_id", None) in (None, "")]
        top.sort(key=lambda c: (getattr(c, "position", 0) or 0, c.name))

        hints = await self.list_hints(user_id=user_id, limit=10_000)
        # Bucket counts by the *first* segment of category_path.
        counts: dict[str, int] = {}
        for h in hints:
            if h.category_path:
                counts[h.category_path[0]] = counts.get(h.category_path[0], 0) + 1

        out: list[tuple[str, str, int]] = []
        for c in top:
            key = c.slug or c.name
            count = counts.get(key, 0)
            if count == 0:
                continue
            description = ""
            meta = getattr(c, "metadata", None)
            if isinstance(meta, dict):
                description = str(meta.get("description") or "")
            out.append((key, description, count))
        return out
