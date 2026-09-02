from __future__ import annotations

from typing import Literal, Protocol, TypedDict


class InstallationAnalyticsEvent(TypedDict):
    resource_type: Literal["plugin", "skill"]
    resource_id: str
    client_name: str
    install_scope: Literal["project", "global"]
    install_mode: str | None


class InstallationMetricsClient(Protocol):
    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> object: ...


def build_plugin_install_event(
    *,
    resource_id: str,
    client_name: str,
    install_scope: Literal["project", "global"],
    install_mode: str | None,
) -> InstallationAnalyticsEvent:
    return {
        "resource_type": "plugin",
        "resource_id": resource_id,
        "client_name": client_name,
        "install_scope": install_scope,
        "install_mode": install_mode,
    }


def build_skill_install_event(
    *,
    resource_id: str,
    client_name: str,
    install_scope: Literal["project", "global"],
    install_mode: str | None = "native",
) -> InstallationAnalyticsEvent:
    return {
        "resource_type": "skill",
        "resource_id": resource_id,
        "client_name": client_name,
        "install_scope": install_scope,
        "install_mode": install_mode,
    }
