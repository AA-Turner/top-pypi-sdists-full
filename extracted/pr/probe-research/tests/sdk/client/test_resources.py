"""The resource API (`client.runs`, `client.projects`) answers with the server's response models,
while the flat methods customers already call keep returning the same dicts (eng review O4)."""

from __future__ import annotations

import warnings

import httpx
import pytest

from probe.generated.models import ProjectDetailOut, ProjectOut, RunDetailOut, RunPageDetailOut, SpanOut
from probe.sdk.client.client import Client
from probe.sdk.client.resource import Resource
from probe.sdk.client.resources.projects.projects import ProjectsResource
from probe.sdk.client.resources.runs.runs import RunsResource
from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.transport.transport import Page, Transport
from probe.sdk.settings.settings import Settings

RUN_ID = "11111111-1111-4111-8111-111111111111"
PROJECT_ID = "22222222-2222-4222-8222-222222222222"
WHEN = "2026-10-31T12:00:00Z"
RUN = {
    "id": RUN_ID, "customer_id": "acme", "experiment_id": None, "project_id": PROJECT_ID, "name": "r1",
    "source": "sdk", "status": "running", "summary": {"loss": 0.1}, "created_at": WHEN, "updated_at": WHEN,
    "added_by_a_newer_server": True,
}
PROJECT = {
    "id": PROJECT_ID, "customer_id": "acme", "workspace_id": None, "name": "p", "slug": "p",
    "created_at": WHEN, "updated_at": WHEN,
}
SPAN = {
    "id": "33333333-3333-4333-8333-333333333333", "customer_id": "acme", "run_id": RUN_ID, "span_type": "step",
    "status": "ok", "summary": {}, "started_at": WHEN, "created_at": WHEN,
}


def _answer(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    if path == f"/v1/runs/{RUN_ID}":
        return httpx.Response(200, json=RUN)
    if path == "/v1/runs":
        return httpx.Response(200, json=[RUN], headers={"X-Next-Cursor": "c2"})
    if path == f"/v1/runs/{RUN_ID}/spans":
        return httpx.Response(200, json=[SPAN])
    if path == f"/v1/projects/{PROJECT_ID}":
        return httpx.Response(200, json=PROJECT)
    if path == "/v1/projects":
        return httpx.Response(200, json=[PROJECT])
    return httpx.Response(404, json={"detail": "Not Found"})


@pytest.fixture
def client(tmp_path) -> Client:
    settings = Settings(base_url="http://test", token="ros_pat_deadbeef", ingest_token="ros_ing_cafef00d",
                        hmac_secret="s3cr3t", workspace="ws-mine")
    transport = Transport(settings, client=httpx.Client(base_url="http://test",
                                                        transport=httpx.MockTransport(_answer)))
    journal = Journal(str(tmp_path / "outbox"), context={"name": None, "base_url": settings.base_url})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        made = Client(settings=settings, transport=transport, journal=journal, async_writes=False, auto_drain=False)
    yield made
    made.close()


def test_the_flat_names_still_return_dicts(client) -> None:
    assert client.get_run(RUN_ID) == RUN
    assert client.get_project(PROJECT_ID) == PROJECT
    assert client.run_spans(RUN_ID) == [SPAN]
    page = client.list_runs()
    assert isinstance(page, Page) and page.items == [RUN]


def test_the_resource_reads_are_the_servers_response_models(client) -> None:
    run = client.runs.get(RUN_ID)
    assert isinstance(run, RunPageDetailOut) and str(run.id) == RUN_ID and run.summary == {"loss": 0.1}
    assert client.projects.get(PROJECT_ID) == ProjectDetailOut.model_validate(PROJECT)
    assert client.runs.list_spans(RUN_ID) == [SpanOut.model_validate(SPAN)]


def test_a_typed_page_keeps_its_cursor(client) -> None:
    runs = client.runs.list()
    assert isinstance(runs, Page) and [type(r) for r in runs.items] == [RunDetailOut]
    assert runs.next_cursor == "c2" == client.list_runs().next_cursor
    assert [type(p) for p in client.projects.list().items] == [ProjectOut]


def test_a_field_a_newer_server_adds_is_ignored(client) -> None:
    assert not hasattr(client.runs.get(RUN_ID), "added_by_a_newer_server")


def test_the_typed_reads_go_through_the_flat_methods(client, monkeypatch) -> None:
    """An instance patch, or a subclass's override, of the flat name is what the resource reads."""
    renamed = {**RUN, "name": "patched"}
    monkeypatch.setattr(client, "get_run", lambda run_id: renamed)
    assert client.runs.get(RUN_ID).name == "patched"


def test_each_access_builds_a_light_resource_that_holds_no_cycle(client) -> None:
    assert isinstance(client.runs, RunsResource) and isinstance(client.projects, ProjectsResource)
    assert client.runs is not client.runs  # nothing cached on the client: it is freed at once, as before
    assert isinstance(client.runs, Resource) and not hasattr(client.runs, "__dict__")
