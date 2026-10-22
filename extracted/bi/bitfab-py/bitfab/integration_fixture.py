"""Framework state recorded on a trace's root span for replay to restore."""

from __future__ import annotations

from typing import Any

INTEGRATION_FIXTURE_CONTEXT_KEY = "__bitfabIntegrationFixture"
INTEGRATION_FIXTURE_VERSION = 1


def create_integration_fixture_context(name: str, value: Any) -> dict[str, Any]:
    return {
        INTEGRATION_FIXTURE_CONTEXT_KEY: {
            "version": INTEGRATION_FIXTURE_VERSION,
            "name": name,
            "value": value,
        }
    }


def has_integration_fixture(span_data: dict[str, Any], name: str) -> bool:
    return name in (extract_integration_fixtures(span_data) or {})


def extract_integration_fixtures(span_data: dict[str, Any]) -> dict[str, Any] | None:
    contexts = span_data.get("contexts")
    if not isinstance(contexts, list):
        return None
    fixtures: dict[str, Any] = {}
    for context in contexts:
        fixture = (
            context.get(INTEGRATION_FIXTURE_CONTEXT_KEY)
            if isinstance(context, dict)
            else None
        )
        if (
            isinstance(fixture, dict)
            and fixture.get("version") == INTEGRATION_FIXTURE_VERSION
            and isinstance(fixture.get("name"), str)
        ):
            fixtures.setdefault(fixture["name"], fixture.get("value"))
    return fixtures or None
