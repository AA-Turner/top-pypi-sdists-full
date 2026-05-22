"""Rich per-feature file plans.

Replaces `project_layout.assign_paths` which produced a junior-dev
scaffold (one API + one service + one test). A principal engineer
builds the full vertical slice per feature:

  Backend feature (e.g. campaign_builder):
    backend/app/models/campaign.py             — SQLModel domain entity
    backend/app/schemas/campaign.py            — Pydantic request/response
    backend/app/repositories/campaign.py       — Data access layer
    backend/app/services/campaign.py           — Business logic
    backend/app/api/v1/campaigns.py            — FastAPI router (CRUD + actions)
    backend/app/tasks/campaign.py              — Celery background tasks (if applicable)
    backend/tests/unit/test_campaign_service.py
    backend/tests/unit/test_campaign_repository.py
    backend/tests/integration/test_campaigns_api.py

  Frontend feature (e.g. user_dashboard):
    frontend/app/(tabs)/dashboard/index.tsx      — List screen
    frontend/app/(tabs)/dashboard/[id].tsx       — Detail screen
    frontend/app/(tabs)/dashboard/_layout.tsx    — Stack layout
    frontend/src/components/dashboard/Card.tsx
    frontend/src/components/dashboard/List.tsx
    frontend/src/components/dashboard/Form.tsx
    frontend/src/hooks/useDashboard.ts           — React Query hooks
    frontend/src/services/dashboard.api.ts       — API client
    frontend/src/types/dashboard.ts              — TS types
    frontend/src/stores/dashboard.store.ts       — Zustand slice (if stateful)
    frontend/__tests__/components/dashboard/Card.test.tsx
    frontend/__tests__/hooks/useDashboard.test.ts

This is what the user means by "principal engineering level, not junior dev."
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

from sage.core.project_layout import FileSlot, Language
from sage.core.spec_decomposer import Feature


def _slug_to_module(slug: str) -> str:
    """campaign_builder → campaign (drop generic suffix); fall back to slug."""
    for suffix in ("_builder", "_generator", "_manager", "_engine", "_system",
                   "_analyzer", "_connector", "_formatter", "_optimizer"):
        if slug.endswith(suffix):
            return slug[: -len(suffix)]
    return slug


def _slug_to_class(slug: str) -> str:
    """campaign_builder → CampaignBuilder (PascalCase for class names)."""
    return "".join(p.capitalize() for p in slug.split("_"))


def _slug_to_plural(slug: str) -> str:
    """campaign → campaigns (rough English plural for API route names)."""
    if slug.endswith("y") and not slug.endswith(("ay", "ey", "oy", "uy")):
        return slug[:-1] + "ies"
    if slug.endswith(("s", "x", "ch", "sh")):
        return slug + "es"
    return slug + "s"


# ──────────────────────── backend feature plan ──────────────────────────


_BACKEND_FILE_BLUEPRINTS: tuple[tuple[str, str, bool], ...] = (
    # (path_template, role, is_test)
    (
        "backend/app/models/{module}.py",
        "SQLModel/SQLAlchemy domain entity for {feature}. Includes timestamps, "
        "soft-delete column, tenant_id FK for multi-tenancy, and indexes on "
        "lookup columns. Use SQLModel(table=True) with lowercase __tablename__. "
        "CRITICAL: NEVER use Field(onupdate=...) — SQLModel does not support it. "
        "NEVER import AsyncSession from sqlmodel — import it from sqlalchemy.ext.asyncio. "
        "NEVER import create_async_engine from sqlmodel — use sqlalchemy.ext.asyncio.",
        False,
    ),
    (
        "backend/app/schemas/{module}.py",
        "Pydantic v2 request + response schemas for {feature}. Includes "
        "{Class}Create, {Class}Update, {Class}Read, {Class}List with pagination "
        "envelope. Field validators for business rules. Examples for OpenAPI.",
        False,
    ),
    (
        "backend/app/repositories/{module}.py",
        "Async data-access layer for {feature}. Implements get_by_id, list_paginated, "
        "create, update, soft_delete. Uses AsyncSession via Depends(get_session) from app.api.deps. "
        "Import AsyncSession from sqlalchemy.ext.asyncio, NOT from sqlmodel. "
        "Filters by current_tenant_id from request context. No FastAPI imports.",
        False,
    ),
    (
        "backend/app/services/{module}.py",
        "Business logic for {feature}. Composes the repository + AI prompt engine + "
        "external integrations as needed. Returns domain results, raises typed "
        "exceptions (NotFoundError, PermissionError, ValidationError) — no HTTPException.",
        False,
    ),
    (
        "backend/app/api/v1/{module}.py",
        "FastAPI router for /api/v1/{plural}. "
        "CRITICAL: Name the router object exactly `router = APIRouter()`. "
        "Use the EXACT filename `{module}.py` — do not change the name. "
        "Import AsyncSession from sqlalchemy.ext.asyncio, NOT from sqlmodel. "
        "Use Depends(get_db) from app.api.deps. Full CRUD + feature actions.",
        False,
    ),
    (
        "backend/tests/unit/test_{module}_service.py",
        "pytest unit tests for {Class}Service. Mocks the repository + integrations. "
        "CRITICAL: async test functions MUST be `async def test_...` with @pytest.mark.asyncio. "
        "Do NOT put import statements inside function bodies. "
        "All imports must be at the top of the file.",
        True,
    ),
    (
        "backend/tests/unit/test_{module}_repository.py",
        "pytest async tests for {Class}Repository using an in-memory SQLite session. "
        "Covers: create + roundtrip, pagination, soft-delete behaviour. "
        "CRITICAL: async test functions MUST be `async def test_...` with @pytest.mark.asyncio. "
        "Do NOT put import statements inside function bodies.",
        True,
    ),
    (
        "backend/tests/integration/test_{plural}_api.py",
        "pytest integration tests against the FastAPI TestClient for /api/v1/{plural}. "
        "Covers: 201 on POST, 200 on GET, 404 on missing, 401 unauthenticated. "
        "CRITICAL: async test functions MUST be `async def test_...` with @pytest.mark.asyncio. "
        "Import from app.api.v1.{module} using the exact module name.",
        True,
    ),
)


# Features that need background workers get a tasks module too
_BACKGROUND_TASK_KEYWORDS: tuple[str, ...] = (
    "scheduled", "auto", "automation", "agent", "optimizer", "analyzer",
    "calendar", "monitor", "fetch", "sync", "ingest", "background",
    "worker", "queue", "process", "batch",
)


def _needs_background_task(feature: Feature) -> bool:
    text = (feature.name + " " + feature.description + " " + " ".join(feature.acceptance)).lower()
    return any(k in text for k in _BACKGROUND_TASK_KEYWORDS)


def _backend_files_for(feature: Feature) -> list[FileSlot]:
    module = _slug_to_module(feature.name)
    cls = _slug_to_class(feature.name)
    plural = _slug_to_plural(module)
    out: list[FileSlot] = []
    for path_tmpl, role_tmpl, is_test in _BACKEND_FILE_BLUEPRINTS:
        path = path_tmpl.format(module=module, plural=plural)
        role = role_tmpl.format(
            feature=feature.description or feature.name,
            module=module,
            plural=plural,
            Class=cls,
            **{"class": cls.lower()},
        )
        out.append(
            FileSlot(
                path=path,
                role=role,
                language="python",
                feature=feature.name,
                is_test=is_test,
            )
        )
    if _needs_background_task(feature):
        out.append(
            FileSlot(
                path=f"backend/app/tasks/{module}.py",
                role=(
                    f"Celery tasks for {feature.description or feature.name}. "
                    f"Defines @celery_app.task functions invoked by services or "
                    f"scheduled in celery_beat. Each task imports its own session, "
                    f"never reuses request-scoped state."
                ),
                language="python",
                feature=feature.name,
                is_test=False,
            )
        )
        out.append(
            FileSlot(
                path=f"backend/tests/unit/test_{module}_tasks.py",
                role=(
                    f"pytest tests for Celery tasks in app/tasks/{module}.py. "
                    f"Runs tasks synchronously via CELERY_TASK_ALWAYS_EAGER, "
                    f"asserts side effects on a test DB."
                ),
                language="python",
                feature=feature.name,
                is_test=True,
            )
        )
    return out


# ──────────────────────── frontend feature plan ─────────────────────────


_RNW_FRONTEND_BLUEPRINTS: tuple[tuple[str, str, bool], ...] = (
    (
        "frontend/src/types/{module}.ts",
        "TypeScript types for {feature}. {Class}, {Class}Create, {Class}Update, "
        "{Class}List with pagination, plus enums and union types referenced by "
        "components. Imports nothing from runtime — types only.",
        False,
    ),
    (
        "frontend/src/services/{module}.api.ts",
        "Axios-based API client for /api/v1/{plural}. Functions: list(), get(id), "
        "create(body), update(id, body), remove(id) plus feature-specific actions. "
        "Uses the shared `api` axios instance (./shared/api). Returns typed promises.",
        False,
    ),
    (
        "frontend/src/hooks/use{Class}.ts",
        "React Query hooks for {feature}: use{Class}List (with pagination), "
        "use{Class}Detail(id), useCreate{Class}, useUpdate{Class}, useDelete{Class}. "
        "Query keys exported as constants. Optimistic updates on mutations.",
        False,
    ),
    (
        "frontend/src/stores/{module}.store.ts",
        "Zustand store for ephemeral UI state related to {feature}: filters, "
        "selection, modal open/closed. Persistent data lives in React Query, "
        "this is purely UI state.",
        False,
    ),
    (
        "frontend/src/components/{module}/{Class}Card.tsx",
        "React Native card component for a single {feature} item. Pressable, "
        "shows summary fields, navigates to detail screen via expo-router. "
        "Uses StyleSheet.create with named tokens. NO HTML — RN primitives only.",
        False,
    ),
    (
        "frontend/src/components/{module}/{Class}List.tsx",
        "React Native FlatList of {Class}Card with pull-to-refresh, "
        "empty state, error state, loading skeleton. Consumes use{Class}List. "
        "Responsive via useWindowDimensions.",
        False,
    ),
    (
        "frontend/src/components/{module}/{Class}Form.tsx",
        "React Native form for creating/editing {feature}. Uses react-hook-form "
        "+ zod for validation. Submit button shows ActivityIndicator while pending. "
        "Field-level error Text below each input.",
        False,
    ),
    (
        "frontend/app/(tabs)/{plural}/_layout.tsx",
        "Expo-router Stack layout for the {plural} route group. Title, "
        "headerShown, screenOptions for consistent styling.",
        False,
    ),
    (
        "frontend/app/(tabs)/{plural}/index.tsx",
        "Expo-router list screen for {feature}. Renders <{Class}List/>. "
        "Has a + button in header that navigates to ./new.",
        False,
    ),
    (
        "frontend/app/(tabs)/{plural}/[id].tsx",
        "Expo-router detail screen for {feature}. Uses useLocalSearchParams "
        "for the id, fetches via use{Class}Detail, renders Edit button "
        "that opens <{Class}Form/> in a modal or inline.",
        False,
    ),
    (
        "frontend/__tests__/components/{module}/{Class}Card.test.tsx",
        "@testing-library/react-native tests for {Class}Card. Renders sample "
        "data, asserts visible fields, asserts onPress fires the navigation.",
        True,
    ),
    (
        "frontend/__tests__/hooks/use{Class}.test.tsx",
        "Tests for use{Class}List + useCreate{Class}. Uses QueryClientProvider "
        "wrapper, msw to mock API, asserts loading/success/error states.",
        True,
    ),
)


def _frontend_files_for(
    feature: Feature, frontend: str
) -> list[FileSlot]:
    if frontend != "react-native-web":
        # For other frontends produce a thinner default — extend later
        return _frontend_files_default(feature)
    module = _slug_to_module(feature.name)
    cls = _slug_to_class(feature.name)
    plural = _slug_to_plural(module)
    out: list[FileSlot] = []
    for path_tmpl, role_tmpl, is_test in _RNW_FRONTEND_BLUEPRINTS:
        path = path_tmpl.format(module=module, plural=plural, Class=cls)
        role = role_tmpl.format(
            feature=feature.description or feature.name,
            module=module,
            plural=plural,
            Class=cls,
        )
        out.append(
            FileSlot(
                path=path,
                role=role,
                language="typescript",
                feature=feature.name,
                is_test=is_test,
            )
        )
    return out


def _frontend_files_default(feature: Feature) -> list[FileSlot]:
    module = _slug_to_module(feature.name)
    cls = _slug_to_class(feature.name)
    return [
        FileSlot(
            path=f"frontend/src/types/{module}.ts",
            role=f"TypeScript types for {feature.description or feature.name}",
            language="typescript",
            feature=feature.name,
        ),
        FileSlot(
            path=f"frontend/src/services/{module}.api.ts",
            role=f"API client for {feature.description or feature.name}",
            language="typescript",
            feature=feature.name,
        ),
        FileSlot(
            path=f"frontend/src/components/{cls}.tsx",
            role=f"Component for {feature.description or feature.name}",
            language="typescript",
            feature=feature.name,
        ),
        FileSlot(
            path=f"frontend/__tests__/{cls}.test.tsx",
            role=f"Tests for {cls}",
            language="typescript",
            feature=feature.name,
            is_test=True,
        ),
    ]


# ──────────────────────── shared / infra features ───────────────────────


def _shared_files_for(feature: Feature) -> list[FileSlot]:
    module = _slug_to_module(feature.name)
    return [
        FileSlot(
            path=f"shared/types/{module}.ts",
            role=f"Cross-tier types for {feature.description or feature.name}.",
            language="typescript",
            feature=feature.name,
        ),
        FileSlot(
            path=f"backend/app/lib/{module}.py",
            role=f"Shared Python utilities for {feature.description or feature.name}.",
            language="python",
            feature=feature.name,
        ),
        FileSlot(
            path=f"backend/tests/unit/test_lib_{module}.py",
            role=f"Tests for the {module} library.",
            language="python",
            feature=feature.name,
            is_test=True,
        ),
    ]


def _infra_files_for(feature: Feature) -> list[FileSlot]:
    # Infra features (background_workers, secure_secrets, etc.) are
    # handled by architecture_modules — return empty so we don't
    # duplicate the cross-cutting layer.
    return []


# ──────────────────────── public entry ─────────────────────────────────


def files_for_feature(
    feature: Feature,
    *,
    frontend: str | None,
    backend: str | None,
) -> list[FileSlot]:
    """Return the FULL file set for one feature.

    Backend features: 8–10 files (model, schema, repo, service, api, tests x3,
    plus tasks + test if background work is implied).
    Frontend features: 12 files (types, api, hooks, store, 3 components,
    layout + 2 screens, 2 tests).
    """
    if feature.layer == "backend" and backend in {"fastapi", "django", "flask"}:
        return _backend_files_for(feature)
    if feature.layer == "frontend" and frontend:
        return _frontend_files_for(feature, frontend)
    if feature.layer == "shared":
        return _shared_files_for(feature)
    if feature.layer == "infra":
        return _infra_files_for(feature)
    return []


__all__ = ["files_for_feature"]
