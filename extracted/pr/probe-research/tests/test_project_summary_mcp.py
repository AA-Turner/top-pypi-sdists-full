"""The MCP contract for dashboard-visible entity Markdown."""

from __future__ import annotations

from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource


def _service(client) -> ResearchReadService:
    return ResearchReadService(ResearchOSSource(client))


def test_project_summary_is_a_discoverable_purpose_shaped_view(client) -> None:
    project = client.create_project(
        "visible-summary",
        kind="general",
        document="# Stable context\n\nUse the small model.",
    )
    service = _service(client)

    card = service.get_entity(f"project:{project['id']}")
    assert "summary" in card["data"]["available_views"]

    summary = service.get_entity(f"project:{project['id']}", view="summary")["data"][
        "project_summary"
    ]
    assert summary["document"].startswith("# Stable context")
    assert set(summary) == {"document"}


def test_blank_project_summary_is_an_explicit_empty_editable_document(client) -> None:
    project = client.create_project("blank-summary", kind="general")
    summary = _service(client).get_entity(f"project:{project['id']}", view="summary")["data"][
        "project_summary"
    ]

    assert summary["document"] == ""
    assert set(summary) == {"document"}


def test_experiment_and_run_summary_views_are_discoverable(client) -> None:
    project = client.create_project("entity-summary-project", kind="general")
    experiment = client.create_experiment(
        "entity-summary-experiment",
        question="h",
        project_id=project["id"],
        document="# Experiment protocol",
    )
    run = client.create_run(experiment["id"], "documented run", heartbeat=False)
    service = _service(client)

    experiment_card = service.get_entity(f"experiment:{experiment['id']}")
    run_card = service.get_entity(f"run:{run.id}")
    assert "summary" in experiment_card["data"]["available_views"]
    # 0220: a RUN has no `summary` view. It was never on the Overview page
    # lane, so when the column went there was nothing left to read -- and a
    # view that answers "" for ever is worse than one not offered, because an
    # agent spends a call finding out.
    assert "summary" not in run_card["data"]["available_views"]

    experiment_summary = service.get_entity(
        f"experiment:{experiment['id']}", view="summary"
    )["data"]["experiment_summary"]
    assert experiment_summary["document"] == "# Experiment protocol"
    assert set(experiment_summary) == {"document"}
