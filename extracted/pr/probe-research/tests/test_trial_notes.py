"""The first-class Trial read and its concurrency-safe notes mutations."""

from __future__ import annotations

import json
import uuid

import pytest

from probe import cli
from probe.cli.main import _NOTE_TARGETS
from probe.models import TrialListOut, TrialOut, TrialPatch
from probe.sdk.client import Client
from probe.sdk.errors import RosError
from tests.conftest import make_client


def _seed_trial(
    app,
    *,
    run_id: str | None = None,
    name: str = "prompt-incident-debug",
    created_at: str = "2026-08-23T20:00:00Z",
) -> dict:
    trial_id = str(uuid.uuid4())
    row = {
        "id": trial_id,
        "rollout_span_id": trial_id,
        "customer_id": "lab-42",
        "run_id": run_id or str(uuid.uuid4()),
        "name": name,
        "name_customized": False,
        "description": None,
        "description_customized": False,
        "status": "completed",
        "step_index": 101,
        "started_at": "2026-08-23T20:00:00Z",
        "ended_at": "2026-08-23T20:02:00Z",
        "provider": "harbor",
        "attributes": {},
        "dimensions": {},
        "summary": None,
        "metadata": {},
        "created_at": created_at,
        "updated_at": "2026-08-23T20:02:00Z",
    }
    app.trials[trial_id] = row
    return row


def test_generated_trial_models_pin_the_read_and_authored_contract():
    """The GENERATED models, which is a different claim from the app's schemas.

    `agent/schema/openapi.json` is a checked-in snapshot, so it can sit stale
    while the backend moves -- and it DID here: the notes carrier was removed
    from `app/trials/schemas.py` a release before this file was regenerated, and
    for that window the SDK's own `TrialPatch` still advertised `notes`,
    `notes_append` and `notes_edit` to anyone building one. Pinning the absence
    from the generated side is what makes a missed `make regen` fail loudly.
    """
    assert {"id", "rollout_span_id", "run_id", "name"} <= TrialListOut.model_fields.keys()
    assert {"id", "rollout_span_id", "run_id"} <= TrialOut.model_fields.keys()
    assert {"name", "description"} <= TrialPatch.model_fields.keys()
    notes_fields = {"notes", "notes_append", "notes_edit"}
    assert not notes_fields & TrialPatch.model_fields.keys()
    assert not {f for f in TrialOut.model_fields if f.startswith("notes")}


def test_get_trial_reads_the_authenticated_trial_route(client, app):
    trial = _seed_trial(app)

    row = client.get_trial(trial["id"])

    assert row["name"] == "prompt-incident-debug"
    assert app.requests[-1].method == "GET"
    assert app.requests[-1].url.path == f"/v1/trials/{trial['id']}"


def test_list_run_trials_preserves_the_authenticated_cursor(client, app):
    run_id = str(uuid.uuid4())
    _seed_trial(
        app,
        run_id=run_id,
        name="older-trial",
        created_at="2026-08-23T20:00:00Z",
    )
    _seed_trial(
        app,
        run_id=run_id,
        name="newer-trial",
        created_at="2026-08-23T20:01:00Z",
    )
    _seed_trial(app, name="other-run")

    first = client.list_run_trials(run_id, limit=1)
    second = client.list_run_trials(run_id, cursor=first.next_cursor, limit=1)
    terminal = client.list_run_trials(run_id, cursor=second.next_cursor, limit=1)

    assert [row["name"] for row in first.items] == ["newer-trial"]
    assert "notes" not in first.items[0]
    assert [row["name"] for row in second.items] == ["older-trial"]
    assert first.next_cursor == "1"
    assert second.next_cursor == "2"
    assert terminal.items == []
    assert terminal.next_cursor is None
    assert app.requests[-1].url.path == f"/v1/runs/{run_id}/trials"
    assert app.requests[-1].url.params["cursor"] == "2"


def test_a_trial_has_no_agent_notes_door_and_that_is_deliberate(client, app):
    """THE ONE CARRIER AGENTS READ AND DO NOT WRITE.

    `PATCH /v1/trials/{id}` takes all three notes writes and the dashboard offers
    the editor, so this asymmetry is a decision and not an unfinished route. A
    trial is materialized by a database trigger on any rollout span (0135), so no
    agent has a moment at which annotating one is the natural act -- and there is
    one trial per rollout, so a 500-rollout run offers 500 documents for an
    observation that belongs once on the run.

    Asserted rather than left to the absence of a test: the previous version of
    this file exercised `_replace_notes("trial", ..., base_version=None, op_key="t")`, and without something
    saying why it went away the next reader restores it as a regression.
    """
    trial = _seed_trial(app)

    assert "trial" not in Client.NOTES_ENTITIES
    with pytest.raises(RosError, match="'trial' carries no notes"):
        client._replace_notes("trial", trial["id"], "retry budget was too high", base_version=None, op_key="t")
    assert not [
        request
        for request in app.requests
        if request.method == "PATCH" and request.url.path == f"/v1/trials/{trial['id']}"
    ]


def test_the_title_and_description_are_still_agent_writable(client, app):
    """The half that stays. A trial's displayed name is whatever the training
    script passed as `run.span("rollout", name=...)` -- a Harbor join key, most
    often -- so renaming one is the write that earns its place here."""
    trial = _seed_trial(app)

    updated = client.update_trial(
        trial["id"], name="Retry-budget blowup", description="Bounded retries."
    )

    assert updated["name"] == "Retry-budget blowup"
    assert updated["description"] == "Bounded retries."
    writes = [
        request
        for request in app.requests
        if request.method == "PATCH" and request.url.path == f"/v1/trials/{trial['id']}"
    ]
    assert len(writes) == 1


def test_the_cli_notes_verbs_refuse_a_trial_target(app, tmp_path, monkeypatch, capsys):
    """`--trial` is GONE from `notes append`/`notes edit`, not merely unused.

    An accepted-but-ignored flag would be the worst of the three options: the
    agent is told the note landed and it did not. Typer rejects an undeclared
    option outright, which is the refusal this asserts.
    """
    monkeypatch.setattr(
        cli,
        "Client",
        lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"),
    )
    trial = _seed_trial(app)

    assert "trial" not in _NOTE_TARGETS
    assert cli.main(["notes", "append", "--trial", trial["id"], "a note"]) != 0
    # The row has no `notes` key AT ALL, which is stronger than a null one: the
    # column is gone (0145), so a write that somehow landed would have to invent
    # the field rather than fill a waiting blank.
    assert "notes" not in app.trials[trial["id"]]


def test_the_cli_can_still_read_and_retitle_a_trial(app, tmp_path, monkeypatch, capsys):
    trial = _seed_trial(app)
    monkeypatch.setattr(
        cli,
        "Client",
        lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"),
    )

    assert cli.main(["trial", "get", trial["id"]]) == 0
    assert json.loads(capsys.readouterr().out)["id"] == trial["id"]

    assert cli.main(["trial", "set", trial["id"], "--name", "Retry-budget blowup"]) == 0
    assert json.loads(capsys.readouterr().out)["name"] == "Retry-budget blowup"
    assert app.trials[trial["id"]]["name"] == "Retry-budget blowup"
