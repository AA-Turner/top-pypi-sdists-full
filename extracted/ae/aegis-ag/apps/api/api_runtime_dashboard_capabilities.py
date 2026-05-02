"""Capability-registry projections for the operator dashboard."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from packages.auth import AuthProfile
from packages.models.provider_catalog import provider_definition
from packages.operator import (
    DashboardCapabilityRecord,
    DashboardControlRecord,
    DashboardDetailItem,
    DashboardProviderProfileRecord,
)
from packages.skills import (
    installed_skill_provenance_from_metadata,
    operator_skill_catalog_entries,
    public_skill_source_descriptor_from_metadata,
)


def _skill_state(entry: Any) -> str:
    return "enabled" if entry.default_enabled else "disabled"


def _skill_provenance(entry: Any) -> str:
    descriptor = public_skill_source_descriptor_from_metadata(entry.metadata)
    install = installed_skill_provenance_from_metadata(entry.metadata)
    parts: list[str] = []
    if descriptor is not None:
        parts.append(descriptor.install_reference)
        parts.append(descriptor.trust_level)
    else:
        parts.append(entry.reference)
        parts.append(entry.source_kind)
    if install is not None and install.install_action:
        parts.append(install.install_action)
    return " / ".join(part for part in parts if part)


def _skill_details(entry: Any) -> tuple[DashboardDetailItem, ...]:
    descriptor = public_skill_source_descriptor_from_metadata(entry.metadata)
    install = installed_skill_provenance_from_metadata(entry.metadata)
    trust_level = descriptor.trust_level if descriptor is not None else (
        "builtin" if entry.source_id == "builtin" else "trusted"
    )
    install_reference = (
        descriptor.install_reference
        if descriptor is not None
        else str(entry.metadata.get("install_reference") or entry.reference)
    )
    details = [
        DashboardDetailItem("Version", str(entry.version or "n/a")),
        DashboardDetailItem("Category", str(entry.metadata.get("category") or "root")),
        DashboardDetailItem("Trust", trust_level),
        DashboardDetailItem("Install ref", install_reference),
        DashboardDetailItem("Storage", str(entry.storage_tier or "n/a")),
        DashboardDetailItem("Default", "enabled" if entry.default_enabled else "disabled"),
        DashboardDetailItem(
            "Prompt index",
            "yes" if entry.visibility.include_in_prompt_index else "no",
        ),
    ]
    slash_command = str(entry.metadata.get("slash_command") or "").strip()
    if slash_command:
        details.append(DashboardDetailItem("Command", slash_command))
    if install is not None and install.install_requester:
        details.append(DashboardDetailItem("Requester", install.install_requester))
    installed_at = str(entry.metadata.get("installed_at") or "").strip()
    if installed_at:
        details.append(DashboardDetailItem("Installed", installed_at))
    return tuple(details)


def _skill_rows(app: Any) -> tuple[DashboardCapabilityRecord, ...]:
    rows: list[DashboardCapabilityRecord] = []
    for entry in operator_skill_catalog_entries(install_root=app.config.install_root):
        descriptor = public_skill_source_descriptor_from_metadata(entry.metadata)
        trust_level = descriptor.trust_level if descriptor is not None else (
            "builtin" if entry.source_id == "builtin" else "trusted"
        )
        tone = "healthy" if trust_level in {"builtin", "trusted"} else "attention"
        rows.append(
            DashboardCapabilityRecord(
                capability=entry.display_name,
                source=entry.source_label,
                state=_skill_state(entry),
                provenance=_skill_provenance(entry),
                note=entry.summary or "Packaged capability entry.",
                tone=tone,
                details=_skill_details(entry),
            )
        )
    return tuple(rows)


def _profile_secret_status(app: Any, profile: AuthProfile) -> tuple[str, str]:
    if not profile.secret_references:
        return ("not-required", "profile")
    try:
        bundle = app.model_provider.credential_resolver.resolve(profile)
    except LookupError:
        return ("missing", "missing")
    sources = tuple(dict.fromkeys(bundle.value_sources.values()))
    source_summary = ", ".join(source for source in sources if source) or "encrypted-local-store"
    return ("stored", source_summary)


def _profile_role_state(app: Any, profile: AuthProfile, *, secret_status: str) -> str:
    if secret_status == "missing":
        return "needs-secret"
    roles: list[str] = []
    if app.model_provider.strong_provider_profile_id == profile.profile_id:
        roles.append("strong")
    if app.model_provider.weak_provider_profile_id == profile.profile_id:
        roles.append("weak")
    if roles:
        return "active " + "+".join(roles)
    return "configured"


def _profile_details(
    *,
    profile: AuthProfile,
    transport: str,
    secret_source: str,
    reasoning: str,
    base_url: str | None,
) -> tuple[DashboardDetailItem, ...]:
    details = [
        DashboardDetailItem("Transport", transport),
        DashboardDetailItem("Secret source", secret_source),
        DashboardDetailItem("Reasoning", reasoning),
    ]
    if base_url:
        details.append(DashboardDetailItem("Base URL", base_url))
    return tuple(details)


def _provider_profile_rows(app: Any) -> tuple[DashboardProviderProfileRecord, ...]:
    rows: list[DashboardProviderProfileRecord] = []
    profiles = sorted(
        app.auth_store.list(),
        key=lambda profile: (profile.provider_id, -profile.priority, profile.profile_id),
    )
    for profile in profiles:
        definition = provider_definition(profile.provider_id)
        secret_status, secret_source = _profile_secret_status(app, profile)
        state = _profile_role_state(app, profile, secret_status=secret_status)
        tone = "attention" if secret_status == "missing" else (
            "healthy" if state.startswith("active") else "neutral"
        )
        transport = profile.transport_id
        display_name = definition.display_name if definition is not None else profile.provider_id
        unsupported = ""
        reasoning = "unavailable"
        note = "Provider profile is available for governed operator routing."
        try:
            resolution = app.model_provider.runtime_resolver.resolve(
                profile.provider_id,
                model_id=profile.default_model,
                base_url=profile.base_url,
            )
            transport = resolution.transport_display_name
            reasoning = "ready" if resolution.supports_reasoning else "unavailable"
            unsupported = str(resolution.provider_metadata.get("unsupported_capabilities") or "").strip()
        except Exception:
            if definition is not None:
                unsupported = str(definition.metadata.get("unsupported_capabilities") or "").strip()
        if unsupported:
            note = f"{transport} keeps {unsupported.replace(',', ', ')} outside the supported runtime path."
        elif definition is not None:
            note = definition.catalog_summary
        rows.append(
            DashboardProviderProfileRecord(
                provider=display_name,
                profile=profile.profile_id,
                state=state,
                auth=f"{profile.auth_method} / {secret_status}",
                model=str(profile.default_model or "n/a"),
                note=note,
                tone=tone,
                details=_profile_details(
                    profile=profile,
                    transport=transport,
                    secret_source=secret_source,
                    reasoning=reasoning,
                    base_url=profile.base_url,
                ),
            )
        )
    return tuple(rows)


def _control_rows(
    *,
    skill_rows: tuple[DashboardCapabilityRecord, ...],
    provider_rows: tuple[DashboardProviderProfileRecord, ...],
    active_provider: Mapping[str, object],
) -> tuple[DashboardControlRecord, ...]:
    builtin_count = sum(1 for row in skill_rows if row.source == "Built In")
    installed_count = sum(1 for row in skill_rows if row.source == "Aegis Installed")
    authored_count = sum(1 for row in skill_rows if row.source == "Aegis Authored")
    prompt_visible = sum(
        1
        for row in skill_rows
        if any(detail.label == "Prompt index" and detail.value == "yes" for detail in row.details)
    )
    missing_secrets = sum(1 for row in provider_rows if row.state == "needs-secret")
    active_provider_label = str(
        active_provider.get("display_name") or active_provider.get("provider_id") or "preview"
    )
    return (
        DashboardControlRecord(
            control="Skill package lifecycle",
            surface="builtin / installed / authored shelves",
            state="governed",
            boundary="operator-owned shelves only",
            note=(
                "Capability inventory is read from the canonical skill catalog, while model-facing "
                "remote install and search remain closed."
            ),
            tone="healthy",
            details=(
                DashboardDetailItem("Builtin", str(builtin_count)),
                DashboardDetailItem("Installed", str(installed_count)),
                DashboardDetailItem("Authored", str(authored_count)),
            ),
        ),
        DashboardControlRecord(
            control="Provider profile lifecycle",
            surface="auth_profiles + provider doctor",
            state="review" if missing_secrets else "governed",
            boundary="secrets stay in the encrypted local vault",
            note=(
                "Configured provider profiles and readiness are visible here without returning raw "
                "credential material to the dashboard."
            ),
            tone="attention" if missing_secrets else "healthy",
            details=(
                DashboardDetailItem("Profiles", str(len(provider_rows))),
                DashboardDetailItem("Missing secrets", str(missing_secrets)),
                DashboardDetailItem("Active provider", active_provider_label),
            ),
        ),
        DashboardControlRecord(
            control="Capability disclosure boundary",
            surface="CapabilityRegistry + frozen prompt index",
            state="bounded",
            boundary="full skill bodies stay gated until viewed",
            note=(
                "The operator dashboard reflects installed state and governed metadata while the "
                "public SkillHub remains the static release-facing catalog."
            ),
            tone="neutral",
            details=(
                DashboardDetailItem("Prompt-visible", str(prompt_visible)),
                DashboardDetailItem("Public site", "static catalog"),
                DashboardDetailItem("Dashboard", "installed-state only"),
            ),
        ),
    )


def build_dashboard_capability_registry(
    app: Any,
    *,
    active_provider: Mapping[str, object],
) -> tuple[
    tuple[DashboardCapabilityRecord, ...],
    tuple[DashboardProviderProfileRecord, ...],
    tuple[DashboardControlRecord, ...],
]:
    skill_rows = _skill_rows(app)
    provider_rows = _provider_profile_rows(app)
    controls = _control_rows(
        skill_rows=skill_rows,
        provider_rows=provider_rows,
        active_provider=active_provider,
    )
    return skill_rows, provider_rows, controls


__all__ = ["build_dashboard_capability_registry"]
