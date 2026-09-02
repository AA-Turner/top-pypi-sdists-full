from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal

from matrx_ai.agents.conversation_type import (
    SOURCE_FEATURE_TO_TYPE,
    ConversationType,
)
from matrx_ai.db.conversation_gate import (
    _SOURCE_FEATURE_TITLE_LABELS,
    CONVERSATION_STEP_LABEL_KEY,
    _format_auto_title,
    _humanize_source_feature,
    compact_step_label,
    has_auto_title_prefix,
    resolve_step_label_for_title,
)

MediaKind = Literal["image", "video", "audio"]

# Source features that map to an internal (non-standard) conversation_type.
# Derived from the canonical SOURCE_FEATURE_TO_TYPE mapping so there is ONE
# source of truth for "which features are internal" — conversation_type owns it
# now. (Superset of the former hand-maintained set; additionally covers
# workflow / scheduled / system features, which are also internal.)
INTERNAL_SOURCE_FEATURES: frozenset[str] = frozenset(
    feature
    for feature, conv_type in SOURCE_FEATURE_TO_TYPE.items()
    if conv_type != ConversationType.STANDARD.value
)

_LEGACY_GENERIC_AUTO_SUFFIXES: frozenset[str] = frozenset(
    {
        "Conversation",
        "Podcast",
        "Web Research",
        "Matrx Chat",
        "Agent Run",
        "New conversation",
        "Manual chat",
        "Scheduled run",
        "Auto ingest",
        "Rag",
    }
)


@dataclass(frozen=True)
class ConversationBackfillRow:
    id: str
    title: str
    source_feature: str
    parent_conversation_id: str | None
    initial_agent_id: str | None
    initial_agent_version_id: str | None
    last_model_id: str | None
    metadata: dict[str, Any]
    created_at: datetime
    user_id: str
    user_request_id: str | None = None


@dataclass(frozen=True)
class ConversationTitleBackfillPlan:
    conversation_id: str
    old_title: str
    new_title: str
    step_label: str
    reason: str


def is_generic_auto_title(title: str | None, source_feature: str) -> bool:
    if not has_auto_title_prefix(title):
        return False
    suffix = str(title).split(":", 1)[1].strip()
    if suffix in _LEGACY_GENERIC_AUTO_SUFFIXES:
        return True
    if suffix in _SOURCE_FEATURE_TITLE_LABELS.values():
        return True
    if suffix == _humanize_source_feature(source_feature):
        return True
    legacy = source_feature.replace("_", " ").replace("-", " ").strip().title()
    return suffix == legacy


def should_backfill_row(row: ConversationBackfillRow) -> bool:
    if not is_generic_auto_title(row.title, row.source_feature):
        return False
    if row.parent_conversation_id:
        return True
    if row.initial_agent_id or row.initial_agent_version_id:
        return True
    if row.source_feature in INTERNAL_SOURCE_FEATURES:
        return True
    return False


def infer_media_kind(model: Any | None) -> MediaKind | None:
    if model is None:
        return None
    caps = getattr(model, "capabilities", None) or {}
    if not isinstance(caps, dict):
        return None
    outputs = caps.get("output") or []
    if not isinstance(outputs, list):
        return None
    normalized = {str(item).lower() for item in outputs}
    if "video" in normalized:
        return "video"
    if "audio" in normalized:
        return "audio"
    if "image" in normalized:
        return "image"
    return None


def _is_slug_name(name: str) -> bool:
    stripped = name.strip()
    return bool(stripped) and stripped == stripped.lower() and ("_" in stripped or "-" in stripped)


def _podcast_media_label(media_kind: MediaKind, media_index: int | None) -> str:
    if media_kind == "audio":
        return "Podcast Audio"
    if media_kind == "image":
        return f"Podcast Image {media_index or 1}"
    return f"Podcast Video {media_index or 1}"


def _generic_media_label(
    source_feature: str, media_kind: MediaKind, media_index: int | None
) -> str:
    feature_label = _SOURCE_FEATURE_TITLE_LABELS.get(source_feature) or _humanize_source_feature(
        source_feature
    )
    if media_kind == "audio":
        return f"{feature_label} Audio"
    if media_kind == "image":
        return f"{feature_label} Image {media_index or 1}"
    return f"{feature_label} Video {media_index or 1}"


def resolve_backfill_step_label(
    *,
    source_feature: str,
    agent_name: str | None,
    media_kind: MediaKind | None,
    media_index: int | None,
    metadata: dict[str, Any],
) -> str | None:
    stored = metadata.get(CONVERSATION_STEP_LABEL_KEY)
    if isinstance(stored, str) and stored.strip():
        return compact_step_label(stored.strip())

    agent = (agent_name or "").strip()
    if agent and not _is_slug_name(agent):
        return agent

    if source_feature in {"podcasts", "podcast"} and media_kind is not None:
        return _podcast_media_label(media_kind, media_index)

    if media_kind is not None and media_kind in {"image", "video"}:
        return _generic_media_label(source_feature, media_kind, media_index)

    if media_kind == "audio":
        if source_feature in {"podcasts", "podcast"}:
            return "Podcast Audio"
        return _generic_media_label(source_feature, "audio", None)

    if agent:
        return resolve_step_label_for_title(agent, None)

    return None


def _grouping_key(row: ConversationBackfillRow) -> str:
    if row.parent_conversation_id:
        return f"parent:{row.parent_conversation_id}"
    if row.user_request_id:
        return f"request:{row.user_request_id}"
    day = row.created_at.date().isoformat() if row.created_at else "unknown"
    return f"orphan:{row.user_id}:{row.source_feature}:{day}"


def assign_media_indices(
    rows: list[ConversationBackfillRow],
    model_kind_by_id: dict[str, MediaKind | None],
) -> dict[str, int]:
    buckets: dict[tuple[str, str, MediaKind], list[ConversationBackfillRow]] = defaultdict(list)
    for row in rows:
        kind = model_kind_by_id.get(str(row.last_model_id or ""))
        if kind not in {"image", "video"}:
            continue
        buckets[(_grouping_key(row), row.source_feature, kind)].append(row)

    indices: dict[str, int] = {}
    for bucket_rows in buckets.values():
        bucket_rows.sort(key=lambda r: (r.created_at, r.id))
        for index, row in enumerate(bucket_rows, start=1):
            indices[row.id] = index
    return indices


def build_backfill_plans(
    rows: list[ConversationBackfillRow],
    *,
    agent_name_by_id: dict[str, str],
    version_agent_name_by_id: dict[str, str],
    model_kind_by_id: dict[str, MediaKind | None],
    request_agent_id_by_conversation: dict[str, str] | None = None,
) -> list[ConversationTitleBackfillPlan]:
    request_agent_id_by_conversation = request_agent_id_by_conversation or {}
    candidates = [row for row in rows if should_backfill_row(row)]
    media_indices = assign_media_indices(candidates, model_kind_by_id)

    plans: list[ConversationTitleBackfillPlan] = []
    for row in candidates:
        agent_name: str | None = None
        if row.initial_agent_id:
            agent_name = agent_name_by_id.get(str(row.initial_agent_id))
        elif row.initial_agent_version_id:
            agent_name = version_agent_name_by_id.get(str(row.initial_agent_version_id))
        elif row.id in request_agent_id_by_conversation:
            req_agent_id = request_agent_id_by_conversation[row.id]
            agent_name = agent_name_by_id.get(req_agent_id)

        media_kind = model_kind_by_id.get(str(row.last_model_id or ""))
        media_index = media_indices.get(row.id)

        step_label = resolve_backfill_step_label(
            source_feature=row.source_feature,
            agent_name=agent_name,
            media_kind=media_kind,
            media_index=media_index,
            metadata=row.metadata or {},
        )
        if not step_label:
            continue

        new_title = _format_auto_title(step_label)
        if new_title == row.title:
            continue

        reason_parts: list[str] = []
        if row.metadata.get(CONVERSATION_STEP_LABEL_KEY):
            reason_parts.append("metadata")
        if agent_name:
            reason_parts.append("agent")
        if media_kind:
            reason_parts.append(f"model:{media_kind}")
        if media_index:
            reason_parts.append(f"index:{media_index}")

        plans.append(
            ConversationTitleBackfillPlan(
                conversation_id=row.id,
                old_title=row.title,
                new_title=new_title,
                step_label=step_label,
                reason="+".join(reason_parts) or "inferred",
            )
        )
    return plans


def row_from_orm(conv: Any) -> ConversationBackfillRow:
    return ConversationBackfillRow(
        id=str(conv.id),
        title=str(getattr(conv, "title", "") or ""),
        source_feature=str(getattr(conv, "source_feature", "") or ""),
        parent_conversation_id=(
            str(conv.parent_conversation_id)
            if getattr(conv, "parent_conversation_id", None)
            else None
        ),
        initial_agent_id=str(conv.initial_agent_id)
        if getattr(conv, "initial_agent_id", None)
        else None,
        initial_agent_version_id=(
            str(conv.initial_agent_version_id)
            if getattr(conv, "initial_agent_version_id", None)
            else None
        ),
        last_model_id=str(conv.last_model_id) if getattr(conv, "last_model_id", None) else None,
        metadata=dict(getattr(conv, "metadata", None) or {}),
        created_at=getattr(conv, "created_at", datetime.min),
        user_id=str(getattr(conv, "created_by", None) or getattr(conv, "user_id", "") or ""),
        user_request_id=None,
    )


async def enrich_rows_from_cx_request(
    rows: list[ConversationBackfillRow],
) -> tuple[list[ConversationBackfillRow], dict[str, str]]:
    from matrx_ai.db._registry import get_model

    Request = get_model("Request")
    UserRequest = get_model("UserRequest")

    conv_ids = [row.id for row in rows]
    if not conv_ids:
        return rows, {}

    requests = await Request.filter(conversation_id__in=conv_ids).order_by("created_at").all()
    user_request_by_conv: dict[str, str] = {}
    for req in requests:
        cid = str(req.conversation_id)
        if cid not in user_request_by_conv:
            user_request_by_conv[cid] = str(req.user_request_id)

    enriched: list[ConversationBackfillRow] = []
    for row in rows:
        enriched.append(
            ConversationBackfillRow(
                **{
                    **row.__dict__,
                    "user_request_id": user_request_by_conv.get(row.id),
                }
            )
        )

    user_request_ids = set(user_request_by_conv.values())
    request_agent_by_conv: dict[str, str] = {}
    if user_request_ids:
        user_requests = await UserRequest.filter(id__in=list(user_request_ids)).all()
        agent_by_request = {
            str(ur.id): str(ur.agent_id) for ur in user_requests if getattr(ur, "agent_id", None)
        }
        for conv_id, request_id in user_request_by_conv.items():
            agent_id = agent_by_request.get(request_id)
            if agent_id:
                request_agent_by_conv[conv_id] = agent_id

    return enriched, request_agent_by_conv


async def load_agent_name_lookups(
    rows: list[ConversationBackfillRow],
) -> tuple[dict[str, str], dict[str, str], dict[str, MediaKind | None]]:
    from matrx_ai.db._registry import get_model

    Definition = get_model("Definition")
    DefinitionVersion = get_model("DefinitionVersion")
    ModelDefinition = get_model("AiModel")

    agent_ids = {row.initial_agent_id for row in rows if row.initial_agent_id}
    version_ids = {row.initial_agent_version_id for row in rows if row.initial_agent_version_id}
    model_ids = {row.last_model_id for row in rows if row.last_model_id}

    agent_name_by_id: dict[str, str] = {}
    if agent_ids:
        agents = await Definition.filter(id__in=list(agent_ids)).all()
        for agent in agents:
            agent_name_by_id[str(agent.id)] = str(getattr(agent, "name", "") or "")

    version_agent_name_by_id: dict[str, str] = {}
    if version_ids:
        versions = await DefinitionVersion.filter(id__in=list(version_ids)).all()
        version_agent_ids = {
            str(version.agent_id) for version in versions if getattr(version, "agent_id", None)
        }
        missing_agent_ids = version_agent_ids - set(agent_name_by_id)
        if missing_agent_ids:
            extra_agents = await Definition.filter(id__in=list(missing_agent_ids)).all()
            for agent in extra_agents:
                agent_name_by_id[str(agent.id)] = str(getattr(agent, "name", "") or "")

        for version in versions:
            version_name = str(getattr(version, "name", "") or "").strip()
            agent_id = str(version.agent_id) if getattr(version, "agent_id", None) else ""
            agent_name = agent_name_by_id.get(agent_id, "")
            version_agent_name_by_id[str(version.id)] = version_name or agent_name

    model_kind_by_id: dict[str, MediaKind | None] = {}
    if model_ids:
        models = await ModelDefinition.filter(id__in=list(model_ids)).all()
        for model in models:
            model_kind_by_id[str(model.id)] = infer_media_kind(model)

    return agent_name_by_id, version_agent_name_by_id, model_kind_by_id


async def fetch_auto_titled_conversations(
    *,
    limit: int | None = None,
    source_features: set[str] | None = None,
) -> list[ConversationBackfillRow]:
    from matrx_ai.db._registry import get_model

    Conversation = get_model("Conversation")

    auto_rows = await Conversation.filter(title__startswith="Auto:").order_by("created_at").all()
    legacy_rows = (
        await Conversation.filter(title__startswith="AUTO:").order_by("created_at").all()
    )
    merged: dict[str, Any] = {}
    for row in [*auto_rows, *legacy_rows]:
        merged[str(row.id)] = row
    rows = list(merged.values())
    if source_features:
        rows = [row for row in rows if getattr(row, "source_feature", "") in source_features]
    rows.sort(key=lambda row: getattr(row, "created_at", datetime.min))
    if limit is not None:
        rows = rows[:limit]
    return [row_from_orm(row) for row in rows]


async def fetch_generic_auto_conversations(
    *,
    limit: int | None = None,
    source_features: set[str] | None = None,
) -> list[ConversationBackfillRow]:
    rows = await fetch_auto_titled_conversations(
        limit=limit,
        source_features=source_features,
    )
    return [row for row in rows if is_generic_auto_title(row.title, row.source_feature)]


def build_compact_title_plans(
    rows: list[ConversationBackfillRow],
) -> list[ConversationTitleBackfillPlan]:
    plans: list[ConversationTitleBackfillPlan] = []
    for row in rows:
        if not has_auto_title_prefix(row.title):
            continue
        compacted = compact_step_label(row.title)
        new_title = _format_auto_title(compacted)
        if new_title == row.title:
            continue
        plans.append(
            ConversationTitleBackfillPlan(
                conversation_id=row.id,
                old_title=row.title,
                new_title=new_title,
                step_label=compacted,
                reason="compact",
            )
        )
    return plans


async def apply_backfill_plans(
    plans: list[ConversationTitleBackfillPlan],
    *,
    dry_run: bool,
) -> int:
    if dry_run or not plans:
        return 0

    from matrx_ai.db.cx_managers import cxm

    updated = 0
    for plan in plans:
        patch_metadata = {CONVERSATION_STEP_LABEL_KEY: plan.step_label}
        existing = await cxm.conversation.load_conversation_by_id(plan.conversation_id)
        metadata = dict(getattr(existing, "metadata", None) or {})
        metadata.update(patch_metadata)
        await cxm.conversation.update_conversation(
            plan.conversation_id,
            title=plan.new_title,
            metadata=metadata,
        )
        updated += 1
    return updated
