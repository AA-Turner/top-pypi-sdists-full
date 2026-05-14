"""Specialized prompts per file type.

The generic `build_file_prompt` in `principal_engineer` is fine for
"give me a python file." But to get principal-engineer-quality output
we need per-file-type prompts that ENCODE the patterns: a model file
prompt mentions SQLModel/Base/timestamps/indexes; an API file prompt
mentions Depends/response_model/error mapping; a hook file prompt
mentions React Query keys + optimistic updates.

The prompt builder picks the right specialization based on the file
path. Falls back to the generic builder for paths it doesn't recognize.
"""

from __future__ import annotations

import re
from typing import Sequence

from sage.core.principal_engineer import (
    CURRENT_VERSIONS,
    FileSpec,
    build_file_prompt as _generic_build_file_prompt,
)


# ──────────────────────── path classification ───────────────────────────


def _classify_path(path: str) -> str:
    """Return a tag like 'model' / 'schema' / 'api' / 'rn_screen' for a path."""
    p = path.replace("\\", "/")

    # Backend
    if "/app/models/" in p:
        return "model"
    if "/app/schemas/" in p:
        return "schema"
    if "/app/repositories/" in p:
        return "repository"
    if "/app/services/" in p:
        return "service"
    if "/app/api/" in p:
        return "api"
    if "/app/tasks/" in p and not p.endswith("celery_app.py"):
        return "celery_task"
    if p.endswith("celery_app.py"):
        return "celery_app"
    if p.endswith("/db/base.py"):
        return "db_base"
    if p.endswith("/db/session.py"):
        return "db_session"
    if p.endswith("/db/seed.py"):
        return "db_seed"
    if p.endswith("/core/config.py"):
        return "config"
    if p.endswith("/core/logging.py"):
        return "logging"
    if p.endswith("/core/security.py"):
        return "security"
    if p.endswith("/core/exceptions.py"):
        return "exceptions"
    if p.endswith("/core/exception_handlers.py"):
        return "exception_handlers"
    if p.endswith("/auth/dependencies.py"):
        return "auth_deps"
    if p.endswith("/auth/oauth.py"):
        return "oauth"
    if "/middleware/" in p:
        return "middleware"
    if "/webhooks/dispatcher.py" in p:
        return "webhook_dispatcher"
    if "/webhooks/handlers.py" in p:
        return "webhook_handlers"
    if "/ai/client.py" in p:
        return "ai_client"
    if "/ai/prompts.py" in p:
        return "ai_prompts"
    if "/ai/" in p:
        return "ai_module"
    if "/observability/" in p:
        return "observability"
    if p.endswith("alembic/env.py"):
        return "alembic_env"

    # Backend tests
    if "/tests/" in p:
        return "backend_test"

    # Frontend (React Native + Web). Paths are repo-relative so they
    # start with `frontend/`, NOT `/frontend/`.
    if p.startswith("frontend/"):
        if "/src/types/" in p:
            return "rn_types"
        if ".api.ts" in p:
            return "rn_api_client"
        if "/src/hooks/" in p:
            return "rn_hook"
        if ".store.ts" in p:
            return "rn_store"
        if "/src/components/ui/" in p:
            return "rn_ui_kit"
        if "/src/components/" in p:
            return "rn_component"
        if "/__tests__/" in p:
            return "rn_test"
        if "/src/shared/" in p:
            return "rn_shared"
        # Anything under frontend/app/ that hasn't matched above is a screen.
        # _layout.tsx files are layouts; (auth)/* are auth screens.
        if "/app/" in p and "_layout.tsx" in p:
            return "rn_layout"
        if "/app/" in p and "/(auth)/" in p:
            return "rn_auth_screen"
        if "/app/" in p:
            return "rn_screen"

    # Infra
    if p.endswith("docker-compose.yml") or p.endswith("Dockerfile"):
        return "docker"
    if "/deploy/k8s/" in p:
        return "k8s"
    if "/deploy/terraform/" in p:
        return "terraform"

    return "generic"


# ──────────────────────── per-type prompt fragments ─────────────────────


_PATTERNS: dict[str, str] = {
    "model": """
## Patterns for SQLModel domain entities

- Inherit from `app.db.base.Base` for declarative metadata access.
- Mark `table=True` and ALL columns with proper Field(...) defaults.
- ALWAYS include: id (Optional[int], primary_key=True), tenant_id (FK,
  indexed), created_at, updated_at (defaults via sa_column with
  server_default=func.now() / onupdate=func.now()), deleted_at (Optional,
  nullable, for soft-delete).
- Relationships: use `Relationship(back_populates=...)` not raw FKs only.
- Add `__table_args__ = (Index("ix_…"),)` for lookup columns.
- NO business logic on the model — that lives in the service.
- Imports: `from sqlmodel import SQLModel, Field, Relationship`, datetime,
  Optional, app.db.base.Base. NO FastAPI imports.
""",

    "schema": """
## Patterns for Pydantic v2 schemas

- Base class per resource, then `…Create`, `…Update` (all Optional),
  `…Read` (with id + timestamps), `…List` envelope `{items, total, page,
  page_size}` for paginated responses.
- ALWAYS include `model_config = ConfigDict(from_attributes=True)` on
  the Read schemas so they load from ORM instances.
- Field validators via `@field_validator` for business rules (e.g.
  email format, slug regex, length limits).
- Examples in `model_config = ConfigDict(json_schema_extra=…)` for nice
  OpenAPI docs.
- NO ORM imports. Pure Pydantic.
""",

    "repository": """
## Patterns for async repositories

- Class named e.g. `CampaignRepository` taking `session: AsyncSession`
  in __init__.
- Methods: `get_by_id(id) -> Model | None`, `list_paginated(page, size,
  filters) -> tuple[list[Model], int]`, `create(model) -> Model`,
  `update(id, patch) -> Model`, `soft_delete(id) -> None`.
- ALWAYS filter queries by `tenant_id = current_tenant_id()` from
  app.middleware.tenant. NEVER trust user-supplied tenant_id.
- ALWAYS filter out soft-deleted rows unless explicitly requested.
- Wrap session ops in try/except SQLAlchemyError → re-raise as
  app.core.exceptions.IntegrationError.
- NO FastAPI imports. Pure data access.
""",

    "service": """
## Patterns for service layer

- Class named e.g. `CampaignService` taking a repository instance and
  any external clients via __init__.
- Methods return domain objects (Pydantic Read schemas or model dicts).
  NEVER HTTPException — raise typed app.core.exceptions instead.
- Business rules live HERE: validation across multiple fields,
  authorization beyond resource ownership, side effects (emit Celery
  task, send email, charge Stripe).
- For AI features, inject the AI client and prompts module — don't
  hardcode openai/anthropic SDK calls.
- Logging via app.core.logging.get_logger(__name__).
""",

    "api": """
## Patterns for FastAPI routers

- `router = APIRouter(prefix="/{plural}", tags=["{Plural}"])`.
- ALWAYS specify `response_model=…`, `status_code=…`, and include
  `summary` + `description` for OpenAPI.
- Inject:
    `current_user: User = Depends(get_current_user)`
    `tenant_id: int = Depends(get_current_tenant_id)`
    `service: {Class}Service = Depends({class}_service)`
- Endpoints: GET /(list, with pagination query params), GET /{id},
  POST /, PATCH /{id}, DELETE /{id}, plus feature-specific actions.
- Map service exceptions via the global handler — DO NOT translate
  in-router unless adding a domain-specific status.
- For paginated lists, use a single `Pagination` query model with
  page + page_size defaults.
""",

    "celery_task": """
## Patterns for Celery tasks

- `from app.tasks.celery_app import celery_app` then `@celery_app.task(
  bind=True, max_retries=3, default_retry_delay=60)`.
- Task functions take primitive args only (ids, dicts) — NEVER ORM
  instances or session refs.
- Open a fresh DB session inside the task via async_session_factory().
- Idempotent: re-running the task with the same args should be safe.
- On transient errors (network, rate-limit), raise self.retry(exc=…).
- Log start + end with task_id; structured logging picks it up.
""",

    "ai_client": """
## Patterns for the LLM client

- Single class `LLMClient` with `generate(prompt, model='openai:gpt-4o',
  temperature=0.7, max_tokens=2000) -> str`.
- Provider routed via prefix: 'openai:' → OpenAI SDK, 'anthropic:' →
  Anthropic SDK. Read keys from settings.
- httpx-style retries with exponential backoff on RateLimitError,
  TimeoutError, transient 5xx.
- Track tokens via app.observability.metrics.ai_tokens_total counter
  labelled by model + tenant_id.
- Sync wrapper acceptable but prefer an `agenerate` async variant.
""",

    "rn_screen": """
## Patterns for Expo-router screens

- Function component that takes no props; reads params via
  `useLocalSearchParams<{id: string}>()`.
- Renders a header (set via `<Stack.Screen options={{title: '…'}} />`
  inside the component).
- Uses StyleSheet.create with theme tokens from src/shared/theme.
- NO HTML elements (no <div>, <button>) — RN primitives ONLY:
  View, Text, Pressable, FlatList, ScrollView, TextInput.
- Loading state: ActivityIndicator. Empty: <EmptyState>. Error: Text
  in danger color + retry Pressable.
""",

    "rn_component": """
## Patterns for RN feature components

- Forward refs where the parent may need them.
- Props typed via an interface — NEVER inline anonymous types.
- StyleSheet.create at the bottom with named keys. Theme tokens via
  `import { theme } from '../../shared/theme'`.
- Memoize via React.memo if the component renders inside a FlatList.
- accessibility: accessibilityRole + accessibilityLabel on every Pressable.
""",

    "rn_hook": """
## Patterns for React Query hooks

- Export `XKeys = { all: ['x'] as const, list: (filters) => [...XKeys.all, 'list', filters] as const, detail: (id) => [...XKeys.all, 'detail', id] as const }`.
- `useXList(filters)` → useQuery with that key + the API client.
- Mutations: `useCreateX`, `useUpdateX`, `useDeleteX` invalidate
  XKeys.all on success.
- Optimistic updates for mutations that obviously fit (toggle, like).
- Errors propagate; the screen renders them.
""",

    "rn_api_client": """
## Patterns for the API client module

- `import { api } from '../shared/api'` then export typed functions:
  `list`, `get`, `create`, `update`, `remove`. Each returns a Promise
  of the schema type.
- ALWAYS use the path constants (/api/v1/…) — never hardcode the host.
""",

    "rn_store": """
## Patterns for Zustand stores

- `import { create } from 'zustand'` and a single `useXStore` export.
- State holds EPHEMERAL UI state only: filters, selection, modal open.
  Server data lives in React Query — never duplicate it here.
- Actions defined as methods on the store object. Use `set()` directly
  for simple updates, `set(produce(state => …))` (immer) for nested.
""",
}


# ──────────────────────── per-file prompt builder ───────────────────────


def build_specialized_prompt(
    task: str,
    spec: FileSpec,
    tree: Sequence[str],
    stack_label: str,
    *,
    sibling_excerpts: dict[str, str] | None = None,
) -> str:
    """Generic build_file_prompt + per-type pattern injection + sibling context.

    `sibling_excerpts` is `{path: file_content}` for files already
    written that the current file should be consistent with (the model
    file for a schema, the schema for an API, etc.).
    """
    # Reuse the generic builder for the spine
    lang_key = "python" if spec.language == "python" else "node"
    versions = CURRENT_VERSIONS.get(lang_key, CURRENT_VERSIONS["python"])
    base = _generic_build_file_prompt(task, spec, list(tree), stack_label, versions)

    kind = _classify_path(spec.path)
    pattern = _PATTERNS.get(kind, "").strip()

    parts = [base]
    if pattern:
        parts.append("\n" + pattern)

    if sibling_excerpts:
        # Cap each excerpt at 1500 chars to keep total prompt size manageable
        excerpts = "\n\n".join(
            f"### {path}\n```\n{content[:1500]}\n```"
            for path, content in sibling_excerpts.items()
        )
        parts.append(
            "\n\n## Existing sibling files (you MUST stay consistent with these)\n"
            + excerpts
        )

    parts.append(
        "\n\n## Final reminder\n"
        "Output ONLY the file contents. No prose, no `<thinking>` tags, "
        "no markdown fences. The first line of your output must be the "
        "first real line of the file."
    )

    return "\n".join(parts)


__all__ = ["build_specialized_prompt"]
