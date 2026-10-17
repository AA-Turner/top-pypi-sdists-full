"""`notes` on runs (research-os 0096), through the SDK. Run groups carried them
too until sweep groups stopped carrying notes: their `notes=` is now dropped.

The regen alone did not make this field reachable. The SDK builds its request
bodies as hand-written dicts rather than from the generated models, so a widened
schema shows up in `probe._generated.models` and nowhere a caller can touch. The
tests below are about the WIRING, not the types.

`notes` is not a second `description`. A description says what the run is; notes
is what a later reader should distrust about it ("suspect, the dataloader was
stale"). With one field the two compete, which is why the server carries both.
"""

from __future__ import annotations

import pytest


def test_create_run_sends_notes_and_leaves_description_alone(client, app):
    exp = app.seed_experiment("e")
    run = client.create_run(
        exp["id"],
        "baseline",
        description="GRPO on bird-sql, 3 epochs",
        notes="suspect: the dataloader was stale for the first 400 steps",
        heartbeat=False,
    )
    row = client.get_run(run.id)
    assert row["description"] == "GRPO on bird-sql, 3 epochs"
    assert row["notes"] == "suspect: the dataloader was stale for the first 400 steps"


def test_create_project_run_sends_notes(client, app):
    """The project-direct door is a separate body-builder call site; wiring one
    and not the other is the obvious way for this to be half-done."""
    project = client.create_project("p", kind="general")
    run = client.create_project_run(
        project["id"], "direct", notes="ran against the stale shard", heartbeat=False
    )
    assert client.get_run(run.id)["notes"] == "ran against the stale shard"


def test_update_run_writes_notes_post_hoc_without_touching_description(client, app):
    """The door that matters most: a run's caveat is nearly always learned after
    the run has finished."""
    exp = app.seed_experiment("e")
    run = client.create_run(exp["id"], "r", description="what it is", heartbeat=False)

    client.update_run(run.id, notes="numbers stand after the re-run")
    row = client.get_run(run.id)
    assert row["notes"] == "numbers stand after the re-run"
    assert row["description"] == "what it is"


def test_update_run_requires_at_least_one_field(client, app):
    exp = app.seed_experiment("e")
    run = client.create_run(exp["id"], "r", heartbeat=False)
    with pytest.raises(
        ValueError, match="name/description/notes"
    ):
        client.update_run(run.id)


def test_group_notes_are_accepted_warned_about_and_never_sent(client, app):
    """Sweep groups no longer carry notes. A script that still passes `notes=`
    keeps working: the group is created (or left as it is), a UserWarning
    says why, and no request carries `notes`."""
    exp = app.seed_experiment("e")
    before = len(app.requests)
    with pytest.warns(UserWarning, match="notes on sweep groups were removed"):
        group = client.create_group(exp["id"], "lr-sweep", notes="varies lr over 5 values")
    assert group["name"] == "lr-sweep"
    assert not app.groups[group["id"]].get("notes")

    with pytest.warns(UserWarning, match="use the experiment's notes"):
        same = client.update_group(group["id"], notes="abandoned")
    assert same["id"] == group["id"] and same["name"] == "lr-sweep"
    assert not [r for r in app.requests[before:] if r.method == "PATCH"]

    with pytest.warns(UserWarning):
        renamed = client.update_group(group["id"], name="lr-sweep-2", notes="abandoned")
    assert renamed["name"] == "lr-sweep-2"
    for request in app.requests[before:]:
        assert b"notes" not in request.read()


def test_a_group_patch_sends_only_the_fields_passed(client, app):
    """The generated model carries a default for the removed notes write
    (`force`); a PATCH that sent it would read to the server as a notes write
    and be refused as one."""
    import json

    exp = app.seed_experiment("e")
    group = client.create_group(exp["id"], "g")
    before = len(app.requests)
    client.update_group(group["id"], spec={"lr": [1e-4, 3e-4]})
    [patch] = [r for r in app.requests[before:] if r.method == "PATCH"]
    assert json.loads(patch.read()) == {"spec": {"lr": [1e-4, 3e-4]}}


def test_update_group_requires_at_least_one_field(client, app):
    exp = app.seed_experiment("e")
    group = client.create_group(exp["id"], "g")
    with pytest.raises(ValueError, match="name/spec"):
        client.update_group(group["id"])


def test_omitting_notes_sends_no_key_at_all(client, app):
    """Absent must mean "leave alone", never "clear" -- so the field has to be
    absent from the BODY, not present as null. A PATCH sending {"notes": None}
    would read as an explicit clear on a server that honours nulls."""
    exp = app.seed_experiment("e")
    run = client.create_run(exp["id"], "r", heartbeat=False)
    before = len(app.requests)
    client.update_run(run.id, name="renamed")
    sent = app.requests[before].read().decode()
    assert "notes" not in sent


@pytest.mark.parametrize(
    "call",
    [
        "create_run",
        "create_project_run",
        "update_run",
    ],
)
def test_a_pre_0096_backend_drops_notes_and_the_sdk_says_so(call, app, client):
    """The silent drop this warning exists for: none of these schemas forbid extra
    fields, so an older backend ACCEPTS `notes`, ignores it, and answers 2xx. The
    caveat vanishes and the caller is told it succeeded.

    It warns rather than raises because create has already made the entity by the
    time the response is in hand -- raising there would leave a run on the server
    and an exception in the caller's lap, which is worse than a dropped note.
    """
    app.stores_entity_notes = False
    project = client.create_project("p", kind="general")
    exp = app.seed_experiment("e", project_id=project["id"])

    with pytest.warns(UserWarning, match="predates `notes`"):
        if call == "create_run":
            client.create_run(exp["id"], "r", notes="lost", heartbeat=False)
        elif call == "create_project_run":
            client.create_project_run(project["id"], "r", notes="lost", heartbeat=False)
        else:
            run = client.create_run(exp["id"], "r", heartbeat=False)
            client.update_run(run.id, notes="lost")


def test_no_warning_when_the_backend_stores_notes(client, recwarn, app):
    exp = app.seed_experiment("e")
    client.create_run(exp["id"], "r", notes="kept", heartbeat=False)
    assert not [w for w in recwarn if "predates `notes`" in str(w.message)]


def test_no_warning_when_the_caller_sent_no_notes(recwarn, app, client):
    """A pre-0096 backend is only a problem for a caller that actually wrote a
    note. Warning on every run creation against an old backend would be noise."""
    app.stores_entity_notes = False
    exp = app.seed_experiment("e")
    client.create_run(exp["id"], "r", heartbeat=False)
    assert not [w for w in recwarn if "predates `notes`" in str(w.message)]
