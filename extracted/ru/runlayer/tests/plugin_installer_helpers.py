"""Shared factories and fakes for the plugin installer tests."""

from __future__ import annotations

import datetime

from runlayer_cli.api import (
    PluginDetail,
    PluginSkillRef,
    SkillDetail,
    SkillFileDetail,
    SkillFileMetadata,
)
from runlayer_cli.metrics import InstallationAnalyticsEvent
from runlayer_cli.plugins.installer import PluginLockEntry


def plugin(
    *,
    id: str = "p1",
    name: str = "my-plugin",
    install_name: str | None = None,
    namespace: str | None = "org/repo",
    servers: list[dict] | None = None,
    skills: list[PluginSkillRef] | None = None,
    use_dynamic_tools: bool = False,
    updated_at: datetime.datetime | None = None,
) -> PluginDetail:
    return PluginDetail(
        id=id,
        name=name,
        install_name=install_name,
        namespace=namespace,
        servers=(
            servers
            if servers is not None
            else [{"server_id": "srv-1", "name": "My Server"}]
        ),
        skills=skills if skills is not None else [],
        use_dynamic_tools=use_dynamic_tools,
        updated_at=updated_at
        or datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
    )


def lock_entry(
    name: str = "my-plugin",
    *,
    client: str = "claude_code",
    install_mode: str = "native",
    use_dynamic_tools: bool = False,
) -> PluginLockEntry:
    return PluginLockEntry(
        name=name,
        id="p1",
        namespace="org/repo",
        updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
        use_dynamic_tools=use_dynamic_tools,
        client=client,
        install_mode=install_mode,
        server_ids=["srv-1"],
    )


class FakeClientSinglePlugin:
    def __init__(self) -> None:
        self.installation_events: list[InstallationAnalyticsEvent] = []

    def list_plugins_detailed(
        self,
        namespace: str | None = None,
        *,
        filter: str = "created_by_me",
        query: str | None = None,
    ):
        return [plugin()]

    def get_plugin(self, plugin_id: str) -> PluginDetail:
        return plugin(id=plugin_id)

    def get_skill(self, skill_id: str) -> SkillDetail:
        return SkillDetail(
            id=skill_id,
            name="test-skill",
            files=[
                SkillFileMetadata(
                    id="f1",
                    skill_id=skill_id,
                    title="SKILL.md",
                    updated_at=datetime.datetime(
                        2024, 1, 1, tzinfo=datetime.timezone.utc
                    ),
                )
            ],
        )

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        return SkillFileDetail(
            id=file_id,
            skill_id=skill_id,
            title="SKILL.md",
            content=f"# {skill_id}",
        )

    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, int]:
        self.installation_events = events
        return {"recorded": len(events)}
