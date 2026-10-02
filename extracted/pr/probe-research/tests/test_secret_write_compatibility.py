"""Mandatory scrubbing preserves write confirmation and immutable retry contracts."""

import pytest

from probe.sdk.secret_gate import CredentialBlocked

from probe.sdk import errors, journal as jm
from probe.sdk.client import Client
from probe.sdk.redaction import default_scrub
from probe.sdk.tags import canonical_tags
from tests.test_backfill_delivery import Store


TEXT = "# Context\npassword=Harbor7!8chars\nOrdinary result."


# 0220: a RUN is gone from both of these. It carries no authored document --
# the field was retired rather than renamed -- so there is no write to scrub.
@pytest.mark.parametrize("entity", ["project", "experiment"])
def test_document_write_verifies_redacted_readback(client, app, entity):
    project = client.create_project("safe-project", kind="general")
    experiment = app.seed_experiment("safe-experiment")
    if entity == "project":
        row = client.update_project(project["id"], document=TEXT)
    else:
        row = client.update_experiment(experiment["id"], document=TEXT)
    assert row["document"] == default_scrub(TEXT)


@pytest.mark.parametrize("entity", ["experiment"])
def test_document_create_verifies_redacted_readback(client, app, entity):
    project = client.create_project("safe-project", kind="general")
    row = client.create_experiment("safe-experiment", question="Does it work?",
                                   project_id=project["id"], document=TEXT)
    stored = client.get_experiment(row["id"])
    assert stored["document"] == default_scrub(TEXT)


def test_a_run_has_no_document_to_scrub(client, app):
    """The scrubber's job on a run is now only its notes and tags: the
    authored document is not a field a run has, so an SDK caller cannot put a
    credential in one."""
    import inspect

    for method in (Client.create_run, Client.create_project_run, Client.update_run):
        params = inspect.signature(method).parameters
        assert "summary_markdown" not in params, method.__name__
        assert "document" not in params, method.__name__


def test_notes_replace_verifies_redacted_readback(client):
    project = client.create_project("safe-project", kind="general")
    assert client._set_project_notes(project["id"], TEXT) == default_scrub(TEXT)


def test_summary_verification_still_detects_dropped_write():
    with pytest.raises(errors.RosError, match="did not store"):
        Client._verify_entity_markdown_written("project", TEXT, {"document": ""}, "PATCH")


def test_tag_write_verification_compares_safe_canonical_value():
    tags = ["password=Harbor7!8chars", "Benign Control"]
    Client._verify_tags_written(tags, {"tags": canonical_tags(default_scrub(tags))}, "PATCH")
    with pytest.raises(errors.NotFoundError):
        Client._verify_tags_written(tags, {"tags": ["benign-control"]}, "PATCH")


def test_slug_write_verification_compares_safe_value():
    slug = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
    Client._verify_slug_written(slug, {"slug": default_scrub(slug)})
    with pytest.raises(errors.CapabilityUnavailable) as error:
        Client._verify_slug_written(slug, {"slug": "other"})
    assert slug not in str(error.value)


@pytest.mark.parametrize("delivered", [False, True])
@pytest.mark.parametrize("source_change", ["deleted", "credential"])
def test_upload_correlation_replay_uses_admitted_identity(tmp_path, monkeypatch, delivered, source_change):
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)
    queue = jm.Journal.for_receipts(tmp_path / "outbox", context={"base_url": "http://test"})
    source = tmp_path / "report.txt"
    source.write_text("Ordinary training result.")
    fields = dict(correlation="report:v1", anchor="project", anchor_id="p1",
                  name="report.txt", src_path=str(source))
    queue.append_upload(**fields)
    store = Store()
    if delivered:
        assert jm.drain(queue, client_factory=lambda _: store).delivered == 1
    expected = queue.delivery_state("report:v1")
    if source_change == "deleted":
        source.unlink()
    else:
        source.write_text("password=Harbor7!8chars")
    assert queue.append_upload(**fields) == expected
    assert len(store.calls) == int(delivered)
    with pytest.raises(ValueError, match="different immutable request"):
        queue.append_upload(**{**fields, "name": "different.txt"})
    # A NEW correlation re-reads today's source. That source now carries a
    # credential, and the policy is that this never costs the upload: the op is
    # admitted and the staged bytes carry the replacement, not the password.
    if source_change == "credential":
        op = queue.append_upload(**{**fields, "correlation": "report:v2"})
        assert op is not None
        staged = [p for p in queue.blobs_dir.rglob("*") if p.is_file()]
        assert staged, "a new correlation must stage its own snapshot"
        assert all(b"Harbor7!8chars" not in p.read_bytes() for p in staged)
    else:
        # NAMED, not bare `Exception`: the base class would swallow a TypeError
        # from a renamed kwarg and read as the refusal this pins. A deleted
        # source is an unreadable one, which still refuses -- that is not a
        # credential finding and there is nothing to record for it.
        with pytest.raises(CredentialBlocked, match="could not be inspected"):
            queue.append_upload(**{**fields, "correlation": "report:v2"})
