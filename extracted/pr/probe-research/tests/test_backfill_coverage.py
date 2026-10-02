import os
from types import SimpleNamespace

import pytest

from probe.cli.backfill_coverage import Coverage, CoverageError, Scope, hash_current


SCOPE = Scope("https://example.test", "tenant-a", "workspace-a", "project-a")
PROJECT = {"id": "project-a", "slug": "alpha", "customer_id": "tenant-a", "workspace_id": "workspace-a"}


@pytest.fixture
def source(tmp_path):
    root = tmp_path / "folder"
    root.mkdir()
    (root / "a.md").write_text("before")
    return root


def coverage(tmp_path, root, scope=SCOPE, **kwargs):
    return Coverage.for_folder(root, scope, directory=tmp_path / "state", **kwargs)


def deliver(state, path="a.md", *, reference=False):
    row = next(row for row in state.rows() if row["path"] == path)
    intent = state.intend(row, reference=reference, uri="file:///data/a.md" if reference else None)
    receipt = {"correlation": intent["correlation"], "state": "delivered", "status": "complete",
               "artifact_id": "artifact-a", "anchor": "project", "anchor_id": "project-a",
               "name": path, "content_hash": intent["content_hash"], "size_bytes": intent["size_bytes"],
               "is_reference": reference, "uri": intent["uri"], "readable": not reference}
    state.accept_receipt(intent["correlation"], receipt)
    return intent, receipt


def test_receipt_survives_restart_but_same_stat_rewrite_is_uncovered(tmp_path, source):
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        deliver(state)
        assert state.report()["delivered"] == ["a.md"]
    original = (source / "a.md").stat()
    (source / "a.md").write_text("after!")
    os.utime(source / "a.md", ns=(original.st_atime_ns, original.st_mtime_ns))
    with coverage(tmp_path, source).writer() as state:
        state.observe(source, ["a.md"])
        assert state.report()["changed"] == ["a.md"]
        assert state.report()["delivered"] == []
        with pytest.raises(CoverageError, match="explicit review"):
            state.approve({"a.md": PROJECT})


def test_recovery_of_old_intent_does_not_cover_new_file(tmp_path, source):
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        row = state.rows()[0]
        state.intend(row, reference=False)
        assert state.report()["queued"] == []
        assert state.report()["unresolved"] == ["a.md"]
    (source / "b.md").write_text("newly arrived")
    with coverage(tmp_path, source).writer() as state:
        state.observe(source, ["a.md", "b.md"])
        deliver(state)
        assert state.report()["delivered"] == ["a.md"]
        assert state.report()["new"] == ["b.md"]


@pytest.mark.parametrize("field,value", [("anchor_id", "project-b"), ("content_hash", "bad"),
    ("name", "elsewhere.md"), ("size_bytes", 0), ("is_reference", True),
    ("status", "pending"), ("readable", False), ("artifact_id", None)])
def test_receipt_must_prove_exact_approved_version_and_destination(tmp_path, source, field, value):
    with coverage(tmp_path, source).writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        intent, receipt = deliver(state)
        with pytest.raises(CoverageError, match="does not match"):
            state.accept_receipt(intent["correlation"], {**receipt, field: value})


def test_reference_delivery_never_claims_uploaded_bytes(tmp_path, source):
    with coverage(tmp_path, source).writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        deliver(state, reference=True)
        assert state.report()["references"] == ["a.md"]
        assert state.report()["delivered"] == []


def test_tenant_backend_workspace_and_destination_have_separate_state(tmp_path, source):
    scopes = [SCOPE, Scope("https://other.test", "tenant-a", "workspace-a", "project-a"),
              Scope(SCOPE.backend, "tenant-b", "workspace-a", "project-a"),
              Scope(SCOPE.backend, "tenant-a", "workspace-b", "project-a"),
              Scope(SCOPE.backend, "tenant-a", "workspace-a", "project-b")]
    stores = [coverage(tmp_path, source, scope) for scope in scopes]
    assert len({store.path for store in stores}) == 5
    with stores[0].writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        deliver(state)
    for store in stores[1:]:
        with store.writer() as state:
            assert state.rows() == []


def test_moved_folder_requires_explicit_source_id_and_same_scope(tmp_path, source):
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        deliver(state)
    moved = source.rename(source.parent / "remounted")
    assert coverage(tmp_path, source).source_id == store.source_id
    assert Coverage.recovery_candidates(moved, SCOPE, directory=tmp_path / "state") == [
        {"source_id": store.source_id, "paths": [str(source)]}]
    assert coverage(tmp_path, moved).source_id != store.source_id
    adopted = coverage(tmp_path, moved, source_id=store.source_id)
    assert adopted.path == store.path
    assert coverage(tmp_path, moved).source_id == store.source_id
    with adopted.writer() as state:
        state.observe(moved, ["a.md"])
        assert state.report()["delivered"] == ["a.md"]
    with pytest.raises(CoverageError, match="does not exist"):
        coverage(tmp_path, moved, Scope(SCOPE.backend, "other", "workspace-a"), source_id=store.source_id)


def test_concurrent_writer_refuses_promptly(tmp_path, source):
    store = coverage(tmp_path, source)
    with store.writer():
        with pytest.raises(CoverageError, match="already using"):
            with coverage(tmp_path, source).writer():
                pytest.fail("second writer acquired lock")


def test_vanished_file_keeps_historical_receipt_without_remote_delete(tmp_path, source):
    with coverage(tmp_path, source).writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        deliver(state)
        (source / "a.md").unlink()
        state.observe(source, [])
        assert state.report()["vanished"] == ["a.md"]
        assert state.conn.execute("SELECT receipt FROM versions").fetchone()[0]


def test_saved_project_is_revalidated_by_id_before_completion(tmp_path, source):
    with coverage(tmp_path, source).writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        deliver(state)
        client = SimpleNamespace(get_project=lambda project_id: {**PROJECT, "workspace_id": "moved"})
        with pytest.raises(CoverageError, match="no longer"):
            state.validate_destinations(client)


def test_corrupt_state_is_preserved_and_not_reset(tmp_path, source):
    store = coverage(tmp_path, source)
    store.path.write_bytes(b"corrupt state")
    with pytest.raises(Exception, match="not a database"):
        with store.writer():
            pytest.fail("corrupt state was accepted")
    assert store.path.read_bytes() == b"corrupt state"


def test_hash_refuses_external_symlink(source, tmp_path):
    outside = tmp_path / "private"
    outside.write_text("private")
    (source / "leak").symlink_to(outside)
    with pytest.raises(CoverageError, match="escapes"):
        hash_current(source, "leak")


# -- signature cache ---------------------------------------------------------
#
# Re-reading a terabyte to learn that nothing changed is the largest cost in a
# repeat import. These pin when the stored hash may stand in for the file, and
# -- more importantly -- every case where it may not.


def _age(path, seconds=60):
    """Backdate a file out of the settle window, the way a real folder is."""
    stamp = os.stat(path)
    os.utime(path, ns=(stamp.st_atime_ns, stamp.st_mtime_ns - int(seconds * 1e9)))


def test_an_unchanged_file_is_not_read_a_second_time(tmp_path, source):
    _age(source / "a.md")
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        first = state.meta("last_census")
        digest = state.rows_for(["a.md"])["a.md"]["observed_hash"]
        state.observe(source, ["a.md"])
        second = state.meta("last_census")
    assert first["hashed"] == 1 and first["reused"] == 0
    assert second["hashed"] == 0 and second["reused"] == 1
    assert store.path.exists()
    with store.writer() as state:
        assert state.rows_for(["a.md"])["a.md"]["observed_hash"] == digest


def test_changed_bytes_are_read_even_when_the_size_is_identical(tmp_path, source):
    _age(source / "a.md")
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        before = state.rows_for(["a.md"])["a.md"]["observed_hash"]
        (source / "a.md").write_text("AFTER!")  # same length as "before"
        _age(source / "a.md")
        state.observe(source, ["a.md"])
        after = state.rows_for(["a.md"])["a.md"]
        assert state.meta("last_census")["hashed"] == 1
        assert after["observed_hash"] != before


def test_a_file_written_this_instant_is_never_taken_from_the_cache(tmp_path, source, monkeypatch):
    """Timestamp resolution is coarse enough that a write can hide inside one.

    The window is moved rather than waited on. Asserting against wall-clock
    freshness makes the test a race: it passes where the fixture and the census
    are milliseconds apart and fails on a loaded CI runner where they are not.
    """
    import probe.cli.backfill_coverage as module

    store = coverage(tmp_path, source)
    _age(source / "a.md")
    with store.writer() as state:
        state.observe(source, ["a.md"])
        assert state.meta("last_census")["hashed"] == 1

        # Everything is inside the settle window: never cached, however many
        # times it is observed.
        monkeypatch.setattr(module, "SIGNATURE_SETTLE_SECONDS", 86_400)
        state.observe(source, ["a.md"])
        assert state.meta("last_census")["hashed"] == 1
        assert state.meta("last_census")["reused"] == 0

        # Settled and unchanged: reused.
        monkeypatch.setattr(module, "SIGNATURE_SETTLE_SECONDS", 0)
        state.observe(source, ["a.md"])
        assert state.meta("last_census")["reused"] == 1
        assert state.meta("last_census")["hashed"] == 0


def test_a_filesystem_without_sub_second_timestamps_is_never_cached(tmp_path, source):
    """exFAT and some network mounts round ctime; there is no signature to keep."""
    from probe.cli.backfill_coverage import signature_of

    whole_second = SimpleNamespace(st_dev=1, st_ino=2, st_size=3,
                                   st_mtime_ns=4_000_000_000, st_ctime_ns=5_000_000_000)
    assert signature_of(whole_second) is None
    sub_second = SimpleNamespace(st_dev=1, st_ino=2, st_size=3,
                                 st_mtime_ns=4_000_000_000, st_ctime_ns=5_000_000_123)
    assert signature_of(sub_second) is not None
    assert signature_of(SimpleNamespace(st_dev=1, st_ino=2, st_size=3,
                                        st_mtime_ns=4, st_ctime_ns=0)) is None


def test_a_replaced_inode_is_read_again(tmp_path, source):
    """Same name, same bytes, different file: a restore or a rename-over."""
    _age(source / "a.md")
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        replacement = tmp_path / "replacement"
        replacement.write_text("before")
        os.replace(replacement, source / "a.md")
        _age(source / "a.md")
        state.observe(source, ["a.md"])
        assert state.meta("last_census")["hashed"] == 1


def test_verified_hash_reports_whether_it_had_to_read(tmp_path, source):
    _age(source / "a.md")
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        digest, size, rehashed = state.verified_hash(source, "a.md")
        assert rehashed is False and size == len("before")
        (source / "a.md").write_text("different")
        _age(source / "a.md")
        again, _, rehashed = state.verified_hash(source, "a.md")
    assert rehashed is True and again != digest


# -- census durability -------------------------------------------------------


def test_a_census_commits_in_batches_so_a_crash_costs_one_batch(tmp_path, source, monkeypatch):
    import probe.cli.backfill_coverage as module

    for index in range(7):
        (source / f"f{index}.txt").write_text(f"row {index}")
    monkeypatch.setattr(module, "OBSERVE_BATCH_FILES", 2)
    paths = ["a.md"] + [f"f{index}.txt" for index in range(7)]
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, paths)
        assert len(state.rows()) == len(paths)


def test_an_interrupted_census_is_visible_and_refuses_to_publish(tmp_path, source, monkeypatch):
    """Half a census reports the un-walked half as vanished. Say so."""
    import probe.cli.backfill_coverage as module

    store = coverage(tmp_path, source)
    with store.writer() as state:
        class LidClosed(Exception):
            """Not an I/O error: a read failure is RECORDED per file and still
            leaves a complete census. Only something that escapes the per-file
            handler can leave the inventory half written."""

        def explode(*args, **kwargs):
            raise LidClosed()

        real = module.hash_current_signed
        monkeypatch.setattr(module, "hash_current_signed", explode)
        with pytest.raises(LidClosed):
            state.observe(source, ["a.md"])
        assert state.observing is True
        assert state.report().partial is True
        with pytest.raises(CoverageError):
            state.write_report()
        # Restore by name, never `monkeypatch.undo()`: the fixture is shared
        # with conftest's HOME isolation and undo would revert that too.
        monkeypatch.setattr(module, "hash_current_signed", real)
        state.observe(source, ["a.md"])
        assert state.observing is False
        assert state.report().partial is False
        assert state.write_report().exists()


def test_hashing_threads_produce_what_one_thread_would(tmp_path, source):
    for index in range(12):
        (source / f"n{index}.bin").write_bytes(bytes([index]) * (1024 * index + 7))
    paths = ["a.md"] + [f"n{index}.bin" for index in range(12)]
    serial = coverage(tmp_path / "one", source)
    parallel = coverage(tmp_path / "many", source)
    with serial.writer() as state:
        state.observe(source, paths, workers=1)
        expected = {row["path"]: row["observed_hash"] for row in state.rows()}
    with parallel.writer() as state:
        state.observe(source, paths, workers=6)
        assert {row["path"]: row["observed_hash"] for row in state.rows()} == expected


def test_an_unreadable_file_does_not_lose_its_neighbours(tmp_path, source):
    (source / "locked.txt").write_text("secret")
    os.chmod(source / "locked.txt", 0o000)
    try:
        store = coverage(tmp_path, source)
        with store.writer() as state:
            state.observe(source, ["a.md", "locked.txt"])
            rows = state.rows_for(["a.md", "locked.txt"])
            assert rows["a.md"]["observed_hash"]
            assert rows["locked.txt"]["observation_error"]
            assert "locked.txt" in state.report()["unresolved"]
    finally:
        os.chmod(source / "locked.txt", 0o600)


# -- rows_for ----------------------------------------------------------------


def test_rows_for_returns_only_what_was_asked_for(tmp_path, source):
    for index in range(600):
        (source / f"many{index}.txt").write_text(str(index))
    paths = ["a.md"] + [f"many{index}.txt" for index in range(600)]
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, paths)
        subset = state.rows_for(["many5.txt", "many599.txt", "a.md", "many5.txt"])
        assert sorted(subset) == ["a.md", "many5.txt", "many599.txt"]
        assert state.rows_for(["absent.txt"]) == {}
        assert state.rows_for([]) == {}


# -- dead units --------------------------------------------------------------


def test_a_dead_file_is_reported_apart_from_one_someone_skipped(tmp_path, source):
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        assert state.mark_dead(["a.md"], "unit-7: the agent never answered") == ["a.md"]
        report = state.report()
        assert report["dead"] == ["a.md"]
        assert report["excluded"] == [] and report["unresolved"] == []
        assert "unit-7" in state.dead_reasons()["a.md"]


def test_a_delivered_file_is_never_marked_dead(tmp_path, source):
    """`exclusion` is read before the receipt; this column is read after it."""
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        deliver(state)
        assert state.mark_dead(["a.md"], "unit-7: died") == []
        assert state.report()["delivered"] == ["a.md"]


def test_an_explicit_retry_puts_dead_files_back_in_front_of_the_review(tmp_path, source):
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        state.mark_dead(["a.md"], "unit-7: died")
        assert state.clear_dead(["a.md"]) == 1
        assert state.report()["dead"] == []
        state.mark_dead(["a.md"], "unit-8: died again")
        assert state.clear_dead() == 1


def test_re_approving_a_path_revives_it_without_an_explicit_retry(tmp_path, source):
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        state.mark_dead(["a.md"], "unit-7: died")
        state.approve({"a.md": PROJECT})
        assert state.report()["dead"] == []


# -- migration ---------------------------------------------------------------


def test_a_store_from_the_previous_schema_opens_and_keeps_its_receipts(tmp_path, source):
    import sqlite3

    import probe.cli.backfill_coverage as module

    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        state.approve({"a.md": PROJECT})
        intent, _ = deliver(state)

    # Rewind the store to exactly what a v2 build would have left behind.
    connection = sqlite3.connect(store.path)
    with connection:
        connection.execute("UPDATE files SET signature=NULL, dead=NULL")
        identity = {"schema": "probe.backfill.coverage/2",
                    "scope": {"backend": SCOPE.backend, "customer_id": SCOPE.customer_id,
                              "workspace_id": SCOPE.workspace_id, "project_id": SCOPE.project_id},
                    "source_id": store.source_id}
        import json as _json
        connection.execute("UPDATE meta SET value=? WHERE key='identity'",
                           (_json.dumps(identity),))
    connection.close()

    reopened = coverage(tmp_path, source, source_id=store.source_id)
    with reopened.writer() as state:
        assert state.meta("identity")["schema"] == module.SCHEMA
        assert state.meta("migrated_from")["schema"] == "probe.backfill.coverage/2"
        assert state.report()["delivered"] == ["a.md"]
        assert state.rows_for(["a.md"])["a.md"]["signature"] is None
        state.observe(source, ["a.md"])
        assert state.meta("last_census")["hashed"] == 1


def test_a_store_from_another_destination_is_still_refused(tmp_path, source):
    import json as _json
    import sqlite3

    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
    connection = sqlite3.connect(store.path)
    with connection:
        identity = {"schema": "probe.backfill.coverage/2",
                    "scope": {"backend": "https://elsewhere.test", "customer_id": "tenant-b",
                              "workspace_id": "workspace-b", "project_id": None},
                    "source_id": store.source_id}
        connection.execute("UPDATE meta SET value=? WHERE key='identity'", (_json.dumps(identity),))
    connection.close()
    with pytest.raises(CoverageError):
        with coverage(tmp_path, source, source_id=store.source_id).writer():
            pass


def test_an_unknown_future_schema_is_preserved_not_migrated(tmp_path, source):
    import json as _json
    import sqlite3

    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
    connection = sqlite3.connect(store.path)
    with connection:
        identity = {"schema": "probe.backfill.coverage/99",
                    "scope": {"backend": SCOPE.backend, "customer_id": SCOPE.customer_id,
                              "workspace_id": SCOPE.workspace_id, "project_id": SCOPE.project_id},
                    "source_id": store.source_id}
        connection.execute("UPDATE meta SET value=? WHERE key='identity'", (_json.dumps(identity),))
    connection.close()
    with pytest.raises(CoverageError):
        with coverage(tmp_path, source, source_id=store.source_id).writer():
            pass


# -- census progress ---------------------------------------------------------
#
# The census is the longest silent stretch of a first import. A bar that does
# not move for twenty minutes is indistinguishable from a hang.


def test_a_census_reports_as_it_goes_and_reaches_the_total(tmp_path, source, monkeypatch):
    import probe.cli.backfill_coverage as module

    monkeypatch.setattr(module, "OBSERVE_BATCH_FILES", 3)
    for index in range(9):
        (source / f"n{index}.txt").write_text("x" * (index + 1))
    paths = ["a.md"] + [f"n{index}.txt" for index in range(9)]
    seen = []
    with coverage(tmp_path, source).writer() as state:
        state.observe(source, paths, workers=1, progress=lambda **kw: seen.append(kw))
    assert seen, "a long census must report before it finishes"
    assert [s["completed"] for s in seen] == sorted(s["completed"] for s in seen)
    assert seen[-1] == {"completed": len(paths), "total": len(paths), "reused": 0}


def test_the_report_says_how_much_was_already_verified(tmp_path, source):
    """The number that makes a repeat import feel different from a first one."""
    _age(source / "a.md")
    store = coverage(tmp_path, source)
    with store.writer() as state:
        state.observe(source, ["a.md"])
        seen = []
        state.observe(source, ["a.md"], progress=lambda **kw: seen.append(kw))
    assert seen[-1]["reused"] == 1 and seen[-1]["completed"] == 1


def test_a_census_with_no_progress_callback_still_works(tmp_path, source):
    with coverage(tmp_path, source).writer() as state:
        state.observe(source, ["a.md"], progress=None)
        assert state.report()["new"] == ["a.md"]


def test_an_empty_folder_reports_nothing_rather_than_zero_of_zero(tmp_path, source):
    seen = []
    with coverage(tmp_path, source).writer() as state:
        state.observe(source, [], progress=lambda **kw: seen.append(kw))
    assert seen == []
