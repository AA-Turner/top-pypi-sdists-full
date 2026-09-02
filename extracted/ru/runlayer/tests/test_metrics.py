from __future__ import annotations

import httpx
import pytest

from runlayer_cli.metrics import (
    InstallationAnalyticsEvent,
    build_plugin_install_event,
    build_skill_install_event,
)
from runlayer_cli.metrics_flush import flush_installation_events


class _FakeMetricsClient:
    def __init__(self) -> None:
        self.calls: list[list[InstallationAnalyticsEvent]] = []

    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, int]:
        self.calls.append(events)
        return {"recorded": len(events)}


class _FakeFailingClient(_FakeMetricsClient):
    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, int]:
        self.calls.append(events)
        request = httpx.Request(
            "POST", "https://example.com/api/v1/metrics/cli-install-events"
        )
        raise httpx.ReadTimeout("timeout", request=request)


@pytest.mark.asyncio
async def test_flush_installation_events_records_events() -> None:
    client = _FakeMetricsClient()
    events = [
        build_plugin_install_event(
            resource_id="plugin-1",
            client_name="cursor",
            install_scope="project",
            install_mode="native",
        ),
        build_skill_install_event(
            resource_id="skill-1",
            client_name="cursor",
            install_scope="project",
        ),
    ]

    await flush_installation_events(client=client, events=events)

    assert client.calls == [
        [
            {
                "resource_type": "plugin",
                "resource_id": "plugin-1",
                "client_name": "cursor",
                "install_scope": "project",
                "install_mode": "native",
            },
            {
                "resource_type": "skill",
                "resource_id": "skill-1",
                "client_name": "cursor",
                "install_scope": "project",
                "install_mode": "native",
            },
        ]
    ]


@pytest.mark.asyncio
async def test_flush_installation_events_is_noop_without_events() -> None:
    client = _FakeMetricsClient()

    await flush_installation_events(client=client, events=[])

    assert client.calls == []


@pytest.mark.asyncio
async def test_flush_installation_events_ignores_http_errors() -> None:
    client = _FakeFailingClient()
    events = [
        build_plugin_install_event(
            resource_id="plugin-1",
            client_name="cursor",
            install_scope="project",
            install_mode="native",
        )
    ]

    await flush_installation_events(client=client, events=events)

    assert len(client.calls) == 1
