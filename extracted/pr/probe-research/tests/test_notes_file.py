"""The entity-note file model: every path where text can be lost.

Each test here corresponds to a way the design can silently destroy writing, and
two of them are reproductions of bugs an outside review found in the plan before
any code existed (the infinite conflict loop, and A+B+A on retry).
"""

from __future__ import annotations

from pathlib import Path


from probe.cli import notes_file
from probe.cli.note_sync import Paths, read_meta, read_text
from probe.sdk import errors


def _paths(tmp_path: Path) -> Paths:
    d = tmp_path / "notes"
    d.mkdir(parents=True, exist_ok=True)
    return Paths(
        document=d / "note.md",
        base=d / "note.base",
        meta=d / "note.meta.json",
        lock=d / "note.lock",
        owner="https://example.test",
        stamp=d / "note.owner",
    )


def _sender(landed: list, *, version: int = 2, raises: Exception | None = None):
    def send(text, base_version, op_key):
        landed.append({"text": text, "base_version": base_version, "op_key": op_key})
        if raises is not None:
            raise raises
        return version

    return send


def _fetcher(body: str, version: int):
    return lambda: (body, version)


class TestCheckout:
    def test_checkout_writes_the_document_and_its_base(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="hello\n", version=7)
        assert read_text(where.document) == "hello\n"
        assert read_text(where.base) == "hello\n"
        assert read_meta(where.meta)["version"] == 7

    def test_files_are_not_world_readable(self, tmp_path):
        """A note keeps customer and commercial facts verbatim."""
        where = _paths(tmp_path)
        notes_file.checkout(where, body="secret\n", version=1)
        for p in (where.document, where.base, where.meta):
            assert oct(p.stat().st_mode)[-3:] == "600", p

    def test_a_second_checkout_is_refused_while_edits_are_unpushed(self, tmp_path):
        """Entity-addressed paths mean two sessions resolve the same file."""
        where = _paths(tmp_path)
        notes_file.checkout(where, body="hello\n", version=1)
        assert notes_file.claim(where) is None
        where.document.write_text("hello\nmine\n")
        refusal = notes_file.claim(where)
        assert refusal is not None and "--steal" in refusal

    def test_steal_overrides_the_claim(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="hello\n", version=1)
        where.document.write_text("mine\n")
        assert notes_file.claim(where, steal=True) is None


class TestPushRefusals:
    def test_a_file_with_conflict_markers_is_never_sent(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.document.write_text("<<<<<<< ours\na\n=======\nb\n>>>>>>> theirs\n")
        landed = []
        report = notes_file.push(where, send=_sender(landed), fetch=_fetcher("", 1))
        assert report.conflicted and not landed
        assert "unresolved conflict markers" in report.detail

    def test_a_missing_base_refuses_rather_than_guessing(self, tmp_path):
        """No ancestor means no three-way merge; both alternatives lose text."""
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.base.unlink()
        where.document.write_text("mine\n")
        landed = []
        report = notes_file.push(where, send=_sender(landed), fetch=_fetcher("", 1))
        assert not landed and not report.pushed
        assert "no base copy" in report.detail and "--force" in report.detail

    def test_force_sends_without_a_base_and_without_a_precondition(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.base.unlink()
        where.document.write_text("mine\n")
        landed = []
        report = notes_file.push(where, send=_sender(landed), fetch=_fetcher("", 1), force=True)
        assert report.pushed and landed[0]["base_version"] is None

    def test_an_unedited_file_sends_nothing(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=3)
        landed = []
        report = notes_file.push(where, send=_sender(landed), fetch=_fetcher("", 3))
        assert not landed and report.detail == "no local edits"


class TestTheBaseAdvancesOnlyOnALandedWrite:
    """A base recording a head the file never got deletes that head's text."""

    def test_a_landed_push_advances_the_base_to_what_was_sent(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.document.write_text("a\nmine\n")
        report = notes_file.push(where, send=_sender([], version=2), fetch=_fetcher("", 2))
        assert report.pushed and report.version == 2
        assert read_text(where.base) == "a\nmine\n"
        assert read_meta(where.meta)["version"] == 2

    def test_a_failed_push_leaves_the_base_exactly_where_it_was(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.document.write_text("a\nmine\n")
        report = notes_file.push(
            where,
            send=_sender([], raises=errors.RosError("network down")),
            fetch=_fetcher("", 1),
        )
        assert not report.pushed
        assert read_text(where.base) == "a\n"
        assert read_meta(where.meta)["version"] == 1

    def test_the_next_push_after_a_failure_still_merges(self, tmp_path):
        """The stale base is the point: it makes the retry a merge, not a replace."""
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.document.write_text("a\nmine\n")
        notes_file.push(
            where, send=_sender([], raises=errors.RosError("down")), fetch=_fetcher("", 1)
        )
        landed = []
        notes_file.push(where, send=_sender(landed, version=2), fetch=_fetcher("", 2))
        assert landed[0]["base_version"] == 1


class TestTheConflictLoop:
    """Reproduction: resolving a conflict used to raise the same conflict forever."""

    def test_a_conflict_advances_the_base_to_the_head_it_merged_onto(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="start\n", version=1)
        where.document.write_text("mine\n")
        report = notes_file.push(
            where,
            send=_sender([], raises=errors.ConflictError("moved")),
            fetch=_fetcher("theirs\n", 5),
        )
        assert report.conflicted
        # THE FIX: the base is the head, not the pre-conflict text.
        assert read_text(where.base) == "theirs\n"
        assert read_meta(where.meta)["version"] == 5

    def test_a_resolved_conflict_pushes_cleanly_instead_of_conflicting_again(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="start\n", version=1)
        where.document.write_text("mine\n")
        notes_file.push(
            where,
            send=_sender([], raises=errors.ConflictError("moved")),
            fetch=_fetcher("theirs\n", 5),
        )
        where.document.write_text("resolved\n")  # the human fixes the markers
        landed = []
        report = notes_file.push(where, send=_sender(landed, version=6), fetch=_fetcher("", 6))
        assert report.pushed, "a resolved conflict must land, not re-conflict"
        assert landed[0]["base_version"] == 5

    def test_a_clean_merge_does_not_claim_to_have_pushed(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.document.write_text("a\nmine\n")
        report = notes_file.push(
            where,
            send=_sender([], raises=errors.ConflictError("moved")),
            fetch=_fetcher("a\ntheirs\n", 4),
        )
        assert report.merged and not report.pushed
        assert "push again" in report.detail


class TestTheOpKeyClientHalf:
    """The CLIENT half of idempotency, which is all that exists today.

    A lost response plus a concurrent write can still give A+B+A, because the
    server does not read the key yet (TODOS.md). These pin that the key is
    stable and durable, so the server half can land without touching the client
    -- they do NOT pin that a retry is safe, and must not be read as if they did.
    """

    def test_a_retry_after_a_lost_response_reuses_its_key(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.document.write_text("a\nmine\n")
        first = []
        notes_file.push(
            where,
            send=_sender(first, raises=errors.RosError("response lost")),
            fetch=_fetcher("", 1),
        )
        second = []
        notes_file.push(where, send=_sender(second, version=2), fetch=_fetcher("", 2))
        assert first[0]["op_key"] == second[0]["op_key"], "a replay must be recognisable"

    def test_the_key_is_persisted_before_the_send(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.document.write_text("a\nmine\n")
        seen = {}

        def send(text, base_version, op_key):
            seen["on_disk"] = read_meta(where.meta).get("op_key")
            seen["sent"] = op_key
            return 2

        notes_file.push(where, send=send, fetch=_fetcher("", 2))
        assert seen["on_disk"] == seen["sent"], "a key minted only in memory is lost on a crash"

    def test_a_landed_push_clears_the_key(self, tmp_path):
        where = _paths(tmp_path)
        notes_file.checkout(where, body="a\n", version=1)
        where.document.write_text("a\nmine\n")
        notes_file.push(where, send=_sender([], version=2), fetch=_fetcher("", 2))
        assert not read_meta(where.meta).get("op_key")


class TestTheClientPathIsActuallyCallable:
    """The seam my fakes hid: unit tests stubbed `send`, integration tests spoke
    HTTP, and NOTHING called `_replace_notes` through a real Client. A `sync=True`
    that `_write_notes` did not accept therefore shipped, and `probe notes push`
    raised TypeError on every invocation."""

    def test_replace_notes_reaches_the_transport(self, tmp_path):
        from conftest import FakeApp, make_client

        app = FakeApp()
        c = make_client(app, tmp_spool=tmp_path / "spool")
        project = c.create_project("p", kind="general")

        row = c._replace_notes(
            "project", project["id"], "hello\n", base_version=None, op_key="k"
        )

        assert row is not None, "a replace must reach the server, not journal"

    def test_replace_notes_is_synchronous_even_under_async_writes(self, tmp_path):
        """sync is separate from strict and not implied by it."""
        from conftest import FakeApp, make_client

        app = FakeApp()
        c = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
        project = c.create_project("p", kind="general")

        assert (
            c._replace_notes("project", project["id"], "x\n", base_version=None, op_key="k")
            is not None
        )
