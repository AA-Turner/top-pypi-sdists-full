"""Owner-aligned dashboard memory-layer projections."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from packages.operator import DashboardDetailItem, DashboardMemoryLayer
from packages.skills import operator_skill_catalog_entries

from .api_runtime_support import _optional_datetime


def _relative_age(value: datetime | None, *, now: datetime) -> str:
    if value is None:
        return "n/a"
    delta_seconds = max(0, int((now - value).total_seconds()))
    if delta_seconds < 5:
        return "now"
    if delta_seconds < 3600:
        return f"{max(1, delta_seconds // 60)}m ago"
    if delta_seconds < 86_400:
        return f"{max(1, delta_seconds // 3600)}h ago"
    if delta_seconds < 604_800:
        return f"{max(1, delta_seconds // 86_400)}d ago"
    return value.astimezone().strftime("%b %d %H:%M")


def _display_timestamp(value: datetime | None, *, now: datetime) -> str:
    if value is None:
        return "n/a"
    return f"{_relative_age(value, now=now)} ({value.astimezone().strftime('%Y-%m-%d %H:%M')})"


def _table_count_and_latest(
    app: Any,
    *,
    table: str,
    timestamp_sql: str = "COALESCE(updated_at, created_at)",
) -> tuple[int, datetime | None]:
    with app.repository.connection() as connection:
        row = connection.execute(
            f"SELECT COUNT(*) AS count, MAX({timestamp_sql}) AS latest FROM {table}"
        ).fetchone()
    if row is None:
        return (0, None)
    return (int(row["count"]), _optional_datetime(row["latest"]))


def _scalar_count(app: Any, query: str, params: tuple[object, ...] = ()) -> int:
    with app.repository.connection() as connection:
        row = connection.execute(query, params).fetchone()
    if row is None:
        return 0
    return int(row[0])


def _table_count(app: Any, *, table: str) -> int:
    return _scalar_count(app, f"SELECT COUNT(*) FROM {table}")


def _latest_defined_datetime(*values: datetime | None) -> datetime | None:
    resolved = tuple(value for value in values if value is not None)
    if not resolved:
        return None
    return max(resolved)


def _path_updated_at(path: Path) -> datetime | None:
    try:
        stat = path.expanduser().resolve().stat()
    except (FileNotFoundError, OSError):
        return None
    return datetime.fromtimestamp(stat.st_mtime, tz=UTC)


def _memory_layer_record(
    *,
    layer: str,
    owner: str,
    latest_mutation: datetime | None,
    volume: str,
    provenance: str,
    index_status: str,
    note: str,
    tone: str,
    stats: tuple[DashboardDetailItem, ...],
    now: datetime,
) -> DashboardMemoryLayer:
    return DashboardMemoryLayer(
        layer=layer,
        owner=owner,
        freshness=_relative_age(latest_mutation, now=now),
        last_mutation=_display_timestamp(latest_mutation, now=now),
        volume=volume,
        provenance=provenance,
        index_status=index_status,
        note=note,
        tone=tone,
        stats=stats,
    )


def _profile_memory_layer(app: Any, *, now: datetime) -> DashboardMemoryLayer:
    profiles, profiles_updated_at = _table_count_and_latest(app, table="profiles")
    identities, identities_updated_at = _table_count_and_latest(app, table="clone_identities")
    user_cards, user_cards_updated_at = _table_count_and_latest(app, table="user_cards")
    relationships, relationships_updated_at = _table_count_and_latest(
        app,
        table="relationship_memories",
    )
    latest_mutation = _latest_defined_datetime(
        profiles_updated_at,
        identities_updated_at,
        user_cards_updated_at,
        relationships_updated_at,
    )
    counts = (profiles, identities, user_cards, relationships)
    if not any(counts):
        tone = "neutral"
        note = "No profile rows are persisted yet; the ProfileGraph owner is still empty."
    elif len({profiles, identities, user_cards, relationships}) != 1:
        tone = "attention"
        note = (
            "ProfileGraph row families are out of sync; review the profile, identity, "
            "user-card, and relationship writers together."
        )
    else:
        tone = "healthy"
        note = (
            "ProfileGraph reads cleanly from aligned profile, identity, user-card, "
            "and relationship rows."
        )
    return _memory_layer_record(
        layer="ProfileGraph",
        owner="profile",
        latest_mutation=latest_mutation,
        volume=f"{profiles} profile row(s) across {identities} identity row(s)",
        provenance="profiles, clone_identities, user_cards, relationship_memories",
        index_status="Direct row read; no derived index or rebuild queue.",
        note=note,
        tone=tone,
        stats=(
            DashboardDetailItem("Profiles", str(profiles)),
            DashboardDetailItem("Clone identities", str(identities)),
            DashboardDetailItem("User cards", str(user_cards)),
            DashboardDetailItem("Relationship rows", str(relationships)),
        ),
        now=now,
    )


def _activity_memory_layer(app: Any, *, now: datetime) -> DashboardMemoryLayer:
    sessions, sessions_updated_at = _table_count_and_latest(
        app,
        table="sessions",
        timestamp_sql="COALESCE(updated_at, started_at)",
    )
    graphs, graphs_updated_at = _table_count_and_latest(
        app,
        table="activity_graphs",
        timestamp_sql="COALESCE(updated_at, created_at)",
    )
    goals, goals_updated_at = _table_count_and_latest(
        app,
        table="activity_nodes",
        timestamp_sql="COALESCE(updated_at, created_at)",
    )
    active_goals = _scalar_count(
        app,
        "SELECT COUNT(*) FROM activity_nodes WHERE status = ?",
        ("active",),
    )
    latest_mutation = _latest_defined_datetime(
        sessions_updated_at,
        graphs_updated_at,
        goals_updated_at,
    )
    if graphs == 0 and goals == 0:
        tone = "neutral"
        note = "No activity graph rows are persisted yet."
    elif graphs == 0 or goals == 0:
        tone = "attention"
        note = "ActivityGraph is only partially materialized; inspect session-to-goal reconciliation."
    elif active_goals == 0:
        tone = "attention"
        note = "ActivityGraph rows exist, but no goal is currently marked active."
    else:
        tone = "healthy"
        note = "ActivityGraph rows, active-goal selection, and session continuity are aligned."
    return _memory_layer_record(
        layer="ActivityGraph",
        owner="activity",
        latest_mutation=latest_mutation,
        volume=f"{goals} goal row(s) across {graphs} graph row(s)",
        provenance="sessions, activity_graphs, activity_nodes",
        index_status="Direct graph rows; no separate rebuild index.",
        note=note,
        tone=tone,
        stats=(
            DashboardDetailItem("Sessions", str(sessions)),
            DashboardDetailItem("Graphs", str(graphs)),
            DashboardDetailItem("Goals", str(goals)),
            DashboardDetailItem("Active goals", str(active_goals)),
        ),
        now=now,
    )


def _evidence_memory_layer(app: Any, *, now: datetime) -> DashboardMemoryLayer:
    total_memories, memories_updated_at = _table_count_and_latest(
        app,
        table="memories",
        timestamp_sql="COALESCE(updated_at, created_at)",
    )
    artifacts, artifacts_updated_at = _table_count_and_latest(
        app,
        table="artifacts",
        timestamp_sql="COALESCE(updated_at, created_at)",
    )
    index_policy = app.memory_runtime.index_policy()
    invalidated = len(index_policy.invalidated_evidence_ids)
    latest_mutation = _latest_defined_datetime(memories_updated_at, artifacts_updated_at)
    if index_policy.tracked_evidence_count == 0 and artifacts == 0:
        tone = "neutral"
        note = "No evidence rows are persisted yet."
    elif index_policy.rebuild_required:
        tone = "attention"
        note = index_policy.invalidation_reason
    else:
        tone = "healthy"
        note = "Derived lexical and vector views match the active canonical evidence rows."
    return _memory_layer_record(
        layer="EvidenceGraph",
        owner="evidence",
        latest_mutation=latest_mutation,
        volume=(
            f"{index_policy.tracked_evidence_count} active memory row(s), "
            f"{artifacts} artifact row(s)"
        ),
        provenance="memories, artifacts, lexical views, shared embedding cache",
        index_status=(
            index_policy.rebuild_plan.summary
            if index_policy.rebuild_plan is not None
            else index_policy.invalidation_reason
        ),
        note=note,
        tone=tone,
        stats=(
            DashboardDetailItem("Active memories", str(index_policy.tracked_evidence_count)),
            DashboardDetailItem("Total memories", str(total_memories)),
            DashboardDetailItem("Artifacts", str(artifacts)),
            DashboardDetailItem("Invalidated entries", str(invalidated)),
        ),
        now=now,
    )


def _procedure_memory_layer(app: Any, *, now: datetime) -> DashboardMemoryLayer:
    libraries, libraries_updated_at = _table_count_and_latest(
        app,
        table="procedure_libraries",
        timestamp_sql="COALESCE(updated_at, created_at)",
    )
    procedures, procedures_updated_at = _table_count_and_latest(
        app,
        table="procedures",
        timestamp_sql="COALESCE(updated_at, created_at)",
    )
    steps = _table_count(app, table="procedure_steps")
    verification_bundles, bundles_updated_at = _table_count_and_latest(
        app,
        table="verification_bundles",
        timestamp_sql="COALESCE(updated_at, verified_at, created_at)",
    )
    unverified = _scalar_count(
        app,
        """
        SELECT COUNT(*)
        FROM procedures
        WHERE verification_bundle_id IS NULL OR TRIM(verification_bundle_id) = ''
        """,
    )
    latest_mutation = _latest_defined_datetime(
        libraries_updated_at,
        procedures_updated_at,
        bundles_updated_at,
    )
    if procedures == 0 and verification_bundles == 0:
        tone = "neutral"
        note = "No procedures have been promoted into the ProcedureLibrary yet."
    elif libraries == 0:
        tone = "attention"
        note = "Procedure rows exist without a library anchor; inspect promotion writes."
    elif unverified:
        tone = "attention"
        note = (
            f"{unverified} procedure row(s) are missing verification bundles and need review "
            "before they can be trusted as overlays."
        )
    else:
        tone = "healthy"
        note = "ProcedureLibrary rows, steps, and verification bundles are aligned."
    return _memory_layer_record(
        layer="ProcedureLibrary",
        owner="procedure",
        latest_mutation=latest_mutation,
        volume=f"{procedures} procedure row(s), {steps} step row(s)",
        provenance="procedure_libraries, procedures, procedure_steps, verification_bundles",
        index_status="Direct row read; no background rebuild contract.",
        note=note,
        tone=tone,
        stats=(
            DashboardDetailItem("Libraries", str(libraries)),
            DashboardDetailItem("Procedures", str(procedures)),
            DashboardDetailItem("Steps", str(steps)),
            DashboardDetailItem("Verification bundles", str(verification_bundles)),
        ),
        now=now,
    )


def _capability_memory_layer(app: Any, *, now: datetime) -> DashboardMemoryLayer:
    skill_entries = operator_skill_catalog_entries(install_root=app.config.install_root)
    auth_profiles, auth_profiles_updated_at = _table_count_and_latest(
        app,
        table="auth_profiles",
        timestamp_sql="COALESCE(updated_at, created_at)",
    )
    builtin_skills = sum(1 for entry in skill_entries if entry.source_id == "builtin")
    installed_skills = sum(1 for entry in skill_entries if entry.source_id == "aegis-installed")
    authored_skills = sum(1 for entry in skill_entries if entry.source_id == "aegis-authored")
    default_enabled = sum(1 for entry in skill_entries if entry.default_enabled)
    latest_skill_mutation = _latest_defined_datetime(
        *(_path_updated_at(Path(entry.entry_path)) for entry in skill_entries)
    )
    latest_mutation = _latest_defined_datetime(latest_skill_mutation, auth_profiles_updated_at)
    if not skill_entries and auth_profiles == 0:
        tone = "neutral"
        note = "No capability shelves or persisted provider profiles are materialized yet."
    elif installed_skills == 0 and authored_skills == 0 and auth_profiles == 0:
        tone = "neutral"
        note = "CapabilityRegistry currently reflects shipped builtin skill truth only."
    else:
        tone = "healthy"
        note = (
            "CapabilityRegistry mirrors builtin skill truth, operator-owned install shelves, "
            "and persisted provider profiles without reopening model-facing install/search."
        )
    return _memory_layer_record(
        layer="CapabilityRegistry",
        owner="capability",
        latest_mutation=latest_mutation,
        volume=f"{len(skill_entries)} skill package(s), {auth_profiles} provider profile(s)",
        provenance="builtin, installed, authored skill shelves plus auth_profiles",
        index_status="Direct package scan and auth-profile rows; no background registry rebuild.",
        note=note,
        tone=tone,
        stats=(
            DashboardDetailItem("Builtin skills", str(builtin_skills)),
            DashboardDetailItem("Installed skills", str(installed_skills)),
            DashboardDetailItem("Authored skills", str(authored_skills)),
            DashboardDetailItem("Default-enabled", str(default_enabled)),
            DashboardDetailItem("Provider profiles", str(auth_profiles)),
        ),
        now=now,
    )


def build_dashboard_memory_layers(app: Any, *, now: datetime) -> tuple[DashboardMemoryLayer, ...]:
    return (
        _profile_memory_layer(app, now=now),
        _activity_memory_layer(app, now=now),
        _evidence_memory_layer(app, now=now),
        _procedure_memory_layer(app, now=now),
        _capability_memory_layer(app, now=now),
    )


__all__ = ["build_dashboard_memory_layers"]
