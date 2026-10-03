"""The team note as a synced file: the client write, and the local state machine.

WHAT THESE PROVE, in the order they matter:

  * the reconcile never loses an edit -- not to a dead session, not to a
    concurrent teammate, not to a retry;
  * a retry mints no version, because a stop hook can fire twice and a timed-out
    request can already have committed;
  * a conflict lands IN THE FILE where the agent can resolve it, and does not
    poison the base copy;
  * the old fail-open write verbs are gone from the client surface; the two
    argument-only writes that replaced them use the server-computed routes and
    never queue.
"""

from __future__ import annotations

import contextlib
import json
from pathlib import Path

import pytest
from probe.cli import team_note_file
from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors


@pytest.fixture
def service(client) -> ResearchReadService:
    return ResearchReadService(ResearchOSSource(client))


@pytest.fixture
def where(tmp_path, monkeypatch):
    """A private home and state directory, so the real ones are never touched.

    EVERY harness root, not just Claude Code's. These tests resolve legacy
    per-harness paths (`migrate_legacy_documents`, `parked_copies`), and a root
    left unset resolves to this machine's real `~/.codex` or `~/.pi/agent` --
    where a test would then park, overwrite or delete a researcher's actual team
    note. `HOME` is redirected too, as the backstop for anything that derives a
    path without going through these three.
    """
    for name, sub in (
        ("HOME", "home"),
        ("CLAUDE_CONFIG_DIR", "claude"),
        ("CODEX_HOME", "codex"),
        ("PI_CODING_AGENT_DIR", "pi-agent"),
        ("XDG_STATE_HOME", "state"),
    ):
        (tmp_path / sub).mkdir(exist_ok=True)
        monkeypatch.setenv(name, str(tmp_path / sub))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    return team_note_file.paths(origin="https://example.test", identity="token-abc")


def _seed(where, client):
    """Pull once, so the file and base copy exist."""
    return team_note_file.pull(client, where)


class TestSync:
    def test_a_matching_base_applies(self, client, app):
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        result = client.sync_team_note("start\n\nand more\n", base_version=1)
        assert result["state"] == "applied"
        assert result["version"] == 2
        assert "and more" in app.team_note["body"]

    def test_an_identical_body_mints_no_version(self, client, app):
        """The retry case. A stop hook that fires twice, or a request that timed
        out after committing, must not produce a second version attributed to
        whoever retried last."""
        app.team_note["body"] = "settled\n"
        app.team_note["version"] = 4
        result = client.sync_team_note("settled\n", base_version=4)
        assert result["state"] == "unchanged"
        assert app.team_note["version"] == 4

    def test_a_stale_base_merges_rather_than_refusing(self, client, app):
        """Stale is the NORMAL case: a teammate wrote while this session worked."""
        app.team_note["body"] = "theirs\n"
        app.team_note["version"] = 9
        result = client.sync_team_note("mine\n", base_version=7)
        assert result["state"] == "applied"
        assert result["merged"] is True
        assert "theirs" in result["body"] and "mine" in result["body"]

    def test_a_conflict_carries_the_marked_document(self, client, app):
        app.team_note["body"] = "theirs\n"
        app.team_note["version"] = 9
        app.sync_conflict = True
        with pytest.raises(errors.ConflictError) as raised:
            client.sync_team_note("mine\n", base_version=7)
        assert "<<<<<<<" in raised.value.detail["merged_body"]

    def test_unresolved_markers_are_refused(self, client, app):
        with pytest.raises(errors.RosError):
            client.sync_team_note("<<<<<<< local\nx\n", base_version=0)


class TestHistory:
    def test_versions_list_and_read(self, client, app):
        app.team_note["body"] = ""
        app.team_note["version"] = 0
        client.sync_team_note("first\n", base_version=0)
        client.sync_team_note("first\nsecond\n", base_version=1)
        listing = client.list_team_note_versions()
        assert [row["version"] for row in listing["versions"]] == [2, 1]
        assert client.get_team_note_version(1)["body"] == "first\n"

    def test_the_list_carries_no_bodies(self, client, app):
        """A page of full documents is a megabyte; the reader is choosing one."""
        client.sync_team_note("something\n", base_version=0)
        assert "body" not in client.list_team_note_versions()["versions"][0]

    def test_the_walk_pages_backwards_and_terminates(self, client, app):
        """The SDK's `before` parameter, end to end.

        Bounded loop on purpose: a cursor that fails to advance is the failure
        this is looking for, and `while before` would hang the suite instead of
        reporting it.
        """
        app.team_note["body"] = ""
        app.team_note["version"] = 0
        for n in range(1, 6):
            client.sync_team_note(f"draft {n}\n", base_version=n - 1)

        walked: list[int] = []
        before = None
        for _ in range(10):
            page = client.list_team_note_versions(limit=2, before=before)
            walked += [row["version"] for row in page["versions"]]
            before = page["next_before"]
            if before is None:
                break
        assert walked == [5, 4, 3, 2, 1]
        assert before is None, "the walk must terminate, not loop"


class TestTheLocalFile:
    def test_pull_seeds_the_document_and_the_base_copy(self, client, app, where):
        app.team_note["body"] = "# Cluster\n\nGPUs are oversubscribed.\n"
        app.team_note["version"] = 3
        report, injected = team_note_file.pull(client, where)
        assert report.pulled
        assert where.document.read_text() == app.team_note["body"]
        assert where.base.read_text() == app.team_note["body"]
        assert json.loads(where.meta.read_text())["version"] == 3
        assert "oversubscribed" in injected

    def test_an_unchanged_document_is_not_rewritten(self, client, app, where):
        app.team_note["body"] = "steady\n"
        app.team_note["version"] = 2
        _seed(where, client)
        report, _ = team_note_file.pull(client, where)
        assert not report.pulled

    def test_editing_the_file_pushes_on_reconcile(self, client, app, where):
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("start\n\nI learned something.\n")
        report = team_note_file.push(client, where)
        assert report.pushed
        assert "I learned something." in app.team_note["body"]
        # The base copy moved with it, so the next push has nothing to send.
        assert team_note_file.push(client, where).pushed is False

    def test_a_dead_session_pushes_before_the_next_pull_overwrites_it(
        self, client, app, where
    ):
        """THE FAILURE THIS ORDERING EXISTS FOR. A session killed before its stop
        hook left work in the file and nowhere else; pulling first would destroy
        it, and since it never reached the server no history could recover it."""
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("start\n\nwork from a session that died.\n")
        app.team_note["body"] = "start\n\na teammate wrote this.\n"
        app.team_note["version"] = 2

        team_note_file.reconcile(client, where)

        assert "work from a session that died." in app.team_note["body"]
        assert "a teammate wrote this." in app.team_note["body"]

    def test_a_conflict_lands_in_the_file_and_leaves_the_base_alone(
        self, client, app, where
    ):
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        base_before = where.base.read_text()
        where.document.write_text("mine\n")
        app.team_note["version"] = 5
        app.sync_conflict = True

        report = team_note_file.push(client, where)

        assert report.conflicted
        assert "<<<<<<<" in where.document.read_text()
        # Recording the conflicted text as the base would tell the next push that
        # markers were the agreed document.
        assert where.base.read_text() == base_before

    def test_a_pull_never_overwrites_unsynced_edits(self, client, app, where):
        """It MERGES them instead of refusing, and neither side is dropped.

        Refusing was the old answer, and it left a session that could not push
        reading a stale note for the rest of its life. Merging keeps the local
        edit -- inside markers when the two sides genuinely disagree about the
        same lines -- and moves the base to the head, so the next push carries
        the resolution up rather than re-litigating it.
        """
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("edited but not yet sent\n")
        app.team_note["body"] = "something else entirely\n"
        app.team_note["version"] = 2

        report, _ = team_note_file.pull(client, where)

        text = where.document.read_text()
        assert "edited but not yet sent" in text  # the local edit survives
        assert "something else entirely" in text  # so does the head
        assert report.conflicted and "<<<<<<<" in text
        assert where.base.read_text() == "something else entirely\n"
        assert json.loads(where.meta.read_text())["version"] == 2

    def test_a_pull_merges_a_teammate_into_an_unsynced_edit(self, client, app, where):
        """The clean case: different regions, no markers, nothing to resolve."""
        app.team_note["body"] = "# A\n\nalpha\n\n# B\n\nbeta\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("# A\n\nalpha, mine\n\n# B\n\nbeta\n")
        app.team_note["body"] = "# A\n\nalpha\n\n# B\n\nbeta, theirs\n"
        app.team_note["version"] = 2

        report, _ = team_note_file.pull(client, where)

        assert report.pulled and not report.conflicted
        assert where.document.read_text() == "# A\n\nalpha, mine\n\n# B\n\nbeta, theirs\n"
        assert json.loads(where.meta.read_text())["version"] == 2

        # And the merged document is what goes up, as an ordinary write.
        pushed = team_note_file.push(client, where)
        assert pushed.pushed and not pushed.merged
        assert app.team_note["body"] == "# A\n\nalpha, mine\n\n# B\n\nbeta, theirs\n"

    def test_a_document_from_another_tenant_is_never_pushed(self, client, app, where):
        """THE CROSS-TENANT LEAK. The state directory is keyed per backend and
        credential, but the DOCUMENT is one stable path because the instruction
        block has to name it. Switch credential and the new owner sees an empty
        base at version 0 -- so push-before-pull would upload the previous
        tenant's private note into this one as a brand new document."""
        app.team_note["body"] = "tenant A private\n"
        app.team_note["version"] = 4
        _seed(where, client)
        assert where.stamp.read_text().strip() == where.owner

        other = team_note_file.paths(origin="https://other.test", identity="token-B")
        assert other.document == where.document  # same path, different owner
        app.team_note["body"] = ""
        app.team_note["version"] = 0

        report = team_note_file.push(client, other)

        assert not report.pushed
        assert "different backend or credential" in report.detail
        assert app.team_note["body"] == ""

    def test_a_foreign_document_is_parked_rather_than_destroyed(self, client, app, where):
        """It was never this tenant's to keep in front of another team's agent
        -- but it was also never ours to DELETE. Replacing it outright is how a
        researcher who switches context loses whatever they had not yet sent.
        Park it, labelled, and hand the path to the tenant that is here now."""
        app.team_note["body"] = "tenant A private\n"
        app.team_note["version"] = 4
        _seed(where, client)
        where.document.write_text("tenant A private, plus unsent work\n")
        other = team_note_file.paths(origin="https://other.test", identity="token-B")
        app.team_note["body"] = "tenant B note\n"
        app.team_note["version"] = 2

        report, _ = team_note_file.pull(client, other)

        assert report.pulled
        assert other.document.read_text() == "tenant B note\n"
        parked = team_note_file.parked_copies(other)
        assert [p.read_text() for p, _, _ in parked] == ["tenant A private, plus unsent work\n"]
        # Labelled with the credential that wrote it, so nobody is told to fold
        # another tenant's prose into this one.
        assert [owner for _, owner, _ in parked] == [where.owner]
        assert str(parked[0][0]) in report.detail

    def test_our_own_parked_copy_comes_back_when_we_return(self, client, app, where):
        """The resume half. Switching credential parks our unsent work; switching
        back adopts it, and the reconcile that follows sends it."""
        app.team_note["body"] = "ours\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("ours, plus unsent work\n")
        other = team_note_file.paths(origin="https://other.test", identity="token-B")
        app.team_note["body"] = "theirs\n"
        app.team_note["version"] = 2
        team_note_file.pull(client, other)  # parks ours, installs theirs
        assert where.document.read_text() == "theirs\n"

        # Back to the first credential: their note is parked in turn, ours returns.
        app.team_note["body"] = "ours\n"
        app.team_note["version"] = 1
        team_note_file.pull(client, where)
        adopted = team_note_file.adopt(where)

        assert adopted is not None
        assert where.document.read_text() == "ours, plus unsent work\n"
        assert where.stamp.read_text().strip() == where.owner
        # Dirty by construction, so the very next push carries it up.
        assert team_note_file.push(client, where).pushed
        assert app.team_note["body"] == "ours, plus unsent work\n"

    def test_adopt_never_overwrites_work_sitting_in_the_document(self, client, app, where):
        """Trading one unsent edit for another is not a recovery."""
        app.team_note["body"] = "ours\n"
        app.team_note["version"] = 1
        _seed(where, client)
        team_note_file.park(where.document)
        where.document.write_text("newer unsent work\n")

        assert team_note_file.adopt(where) is None
        assert where.document.read_text() == "newer unsent work\n"
        assert len(team_note_file.parked_copies(where)) == 1

    def test_an_unreadable_document_stops_the_reconcile(self, client, app, where, monkeypatch):
        """Corruption is an unknown, not an absence. Reading it as "no local
        edits" makes push send nothing and lets pull overwrite the file."""
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_bytes(b"\xff\xfe not utf-8")

        report = team_note_file.push(client, where)
        assert not report.pushed
        assert "refusing to sync" in report.detail

        pulled, _ = team_note_file.pull(client, where)
        assert not pulled.pulled
        assert where.document.read_bytes() == b"\xff\xfe not utf-8"

    def test_the_document_is_written_private(self, client, app, where):
        """The team's private prose on a machine several agents share."""
        app.team_note["body"] = "secrets\n"
        app.team_note["version"] = 1
        _seed(where, client)
        assert oct(where.document.stat().st_mode)[-3:] == "600"

    def test_state_is_keyed_by_origin_and_credential(self, tmp_path, monkeypatch):
        """Two backends, or two credentials, must never share a base copy: both
        documents sit at their own version 12 and a shared base would hand one
        tenant's text to the other as a merge base."""
        monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
        one = team_note_file.paths(origin="https://a.test", identity="token-a")
        two = team_note_file.paths(origin="https://b.test", identity="token-a")
        three = team_note_file.paths(origin="https://a.test", identity="token-b")
        assert one.base != two.base != three.base
        assert one.base != three.base
        # The DOCUMENT is shared: it is the agent's editing surface, and there is
        # one agent on this machine.
        assert one.document == two.document

    def test_the_document_is_one_path_for_every_harness(self, tmp_path, monkeypatch):
        """THE PING-PONG, made unrepresentable.

        The document used to be `memory_path(source).parent / DOCUMENT_NAME`,
        so Claude Code, Codex and pi each had their own, while the base copy was
        keyed on the credential alone. One base for three documents meant each
        harness read the others' file as unsynced work and pushed a whole
        document over it, every session start, forever (2026-09-07, v765-v770:
        two byte-identical bodies alternating every ~20 minutes).

        Every harness, every harness env override, one path.
        """
        monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
        monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
        monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
        monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi-agent"))

        documents = set()
        for agent_env in (None, "claude_code", "codex", "pi", "something-else"):
            if agent_env is None:
                monkeypatch.delenv("PROBE_AGENT", raising=False)
            else:
                monkeypatch.setenv("PROBE_AGENT", agent_env)
            documents.add(team_note_file.paths().document)

        assert len(documents) == 1
        assert documents.pop() == tmp_path / "state" / "probe" / "team-note" / "probe-team-note.md"

    def test_two_harnesses_never_mint_a_version_by_syncing(self, client, app, where, monkeypatch):
        """THE REGRESSION TEST. One machine, one credential, two harnesses.

        Claude writes and pushes; Codex's session then starts and reconciles.
        Codex must find nothing to say. Before this change it pushed its own
        stale copy back over Claude's, Claude pushed again on its next start,
        and the server minted a version every ~20 minutes with no human editing
        anything.
        """
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 1
        # Same credential, two harnesses: the CLI is invoked with PROBE_AGENT
        # set, exactly as each harness's hook invokes it.
        claude = team_note_file.paths(origin="https://example.test", identity="token-abc")
        monkeypatch.setenv("PROBE_AGENT", "codex")
        codex = team_note_file.paths(origin="https://example.test", identity="token-abc")
        # BOTH harnesses have run here before, which is the state every real
        # machine is in: each one seeded whatever document its own paths named.
        team_note_file.reconcile(client, claude)
        team_note_file.reconcile(client, codex)

        # The Claude session does some work and sends it.
        claude.document.write_text("shared\n\n## from the Claude session\n")
        assert team_note_file.push(client, claude).pushed
        assert app.team_note["version"] == 2
        settled = app.team_note["version"]

        # The Codex session starts. It has nothing of its own to say.
        report, _ = team_note_file.reconcile(client, codex)

        assert not report.pushed
        assert app.team_note["version"] == settled  # nothing minted
        assert app.team_note["body"] == "shared\n\n## from the Claude session\n"
        assert codex.document.read_text() == "shared\n\n## from the Claude session\n"

        # Nor does a second lap of both, which is where the alternation lived.
        team_note_file.reconcile(client, claude)
        team_note_file.reconcile(client, codex)
        team_note_file.reconcile(client, claude)
        assert app.team_note["version"] == settled
        assert app.team_note["body"] == "shared\n\n## from the Claude session\n"


class TestTheOwnerStamp:
    def test_a_push_never_restamps_a_document_it_did_not_write(
        self, client, app, where, monkeypatch
    ):
        """THE STAMP FOLLOWS THE BYTES.

        The stamp answers "whose text is in this file". Writing it while another
        credential's document sits at that path relabels their note as ours, and
        the next push reads that label as permission to send it. Only reachable
        when someone switches credential mid-sync, which is rare -- and a
        cross-tenant upload is not a thing to leave on a probability argument.
        """
        app.team_note["body"] = "ours\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("ours, edited\n")
        other = team_note_file.paths(origin="https://other.test", identity="token-B")
        real_sync = client.sync_team_note

        def switching_sync(body, *, base_version):
            result = real_sync(body, base_version=base_version)
            # Another credential's session lands its pull while ours is in flight.
            where.document.write_text("THEIR private note\n")
            where.stamp.write_text(other.owner)
            return result

        monkeypatch.setattr(client, "sync_team_note", switching_sync)
        team_note_file.push(client, where)

        assert where.stamp.read_text().strip() == other.owner
        assert where.document.read_text() == "THEIR private note\n"
        # And because the label survived, our next push refuses to send it.
        app.team_note["body"] = "ours\n"
        monkeypatch.setattr(client, "sync_team_note", real_sync)
        report = team_note_file.push(client, where)
        assert not report.pushed
        assert "different backend or credential" in report.detail
        assert app.team_note["body"] == "ours\n"


class TestTheInFlightMerge:
    """The server merged while the agent kept typing.

    This interleaving used to delete text: the base advanced to the server's
    merged body while the FILE never received it, so the next push carried the
    omission as an ordinary edit and the server applied it straight.
    """

    def test_a_server_merge_is_rebased_into_a_file_that_moved(self, client, app, where, monkeypatch):
        app.team_note["body"] = "# A\n\nalpha\n\n# B\n\nbeta\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("# A\n\nalpha, mine\n\n# B\n\nbeta\n")

        # A teammate writes between our read and our request landing, so the
        # server merges; and the agent types again while the request is in
        # flight, so the file has moved by the time we commit.
        real_sync = client.sync_team_note

        def racing_sync(body, *, base_version):
            app.team_note["body"] = "# A\n\nalpha\n\n# B\n\nbeta, theirs\n"
            app.team_note["version"] = 2
            result = real_sync(body, base_version=base_version)
            where.document.write_text("# A\n\nalpha, mine\n\n# B\n\nbeta\n\n# C\n\nstill typing\n")
            return result

        monkeypatch.setattr(client, "sync_team_note", racing_sync)
        report = team_note_file.push(client, where)

        assert report.pushed and report.merged
        text = where.document.read_text()
        assert "beta, theirs" in text, "the teammate's paragraph must survive in the file"
        assert "still typing" in text, "and so must what the agent wrote during the request"
        assert "alpha, mine" in text
        # The base is what the server holds, and the file is a descendant of it,
        # so the next push is an ordinary edit rather than a deletion.
        assert where.base.read_text() == app.team_note["body"]
        monkeypatch.setattr(client, "sync_team_note", real_sync)
        team_note_file.push(client, where)
        assert "beta, theirs" in app.team_note["body"]
        assert "still typing" in app.team_note["body"]

    def test_an_unmergeable_rebase_leaves_the_file_alone(self, client, app, where, monkeypatch):
        """Its edits are unsent, not lost; the next reconcile tries again."""
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("mine\n")
        real_sync = client.sync_team_note

        def racing_sync(body, *, base_version):
            app.team_note["body"] = "theirs\n"
            app.team_note["version"] = 2
            result = real_sync(body, base_version=base_version)
            where.document.write_text("mine, still typing\n")
            return result

        monkeypatch.setattr(client, "sync_team_note", racing_sync)
        monkeypatch.setattr(
            team_note_file, "merge3", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("too big"))
        )
        report = team_note_file.push(client, where)

        assert "could not merge" in report.detail
        assert where.document.read_text() == "mine, still typing\n"


class TestLegacyMigration:
    """Per-harness documents from the old layout: parked, never pushed."""

    def _legacy(self, source: str) -> Path:
        from probe.cli import agent_rules

        path = agent_rules.memory_path(source).parent / team_note_file.DOCUMENT_NAME
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def test_a_legacy_copy_the_server_already_has_is_removed(self, client, app, where):
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 3
        _seed(where, client)
        legacy = self._legacy("codex")
        legacy.write_text("shared\n")

        kept = team_note_file.migrate_legacy_documents(where)

        assert kept == []
        assert not legacy.exists()
        assert team_note_file.parked_copies(where) == []

    def test_a_legacy_copy_with_unsent_work_is_parked_not_pushed(self, client, app, where):
        """Its true merge base is unknowable here. Pushing it against OUR base
        version reads the other harness's sections as deletions -- which is the
        bug this whole change exists to end."""
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 3
        _seed(where, client)
        legacy = self._legacy("codex")
        legacy.write_text("shared\n\n## only in the Codex copy\n")

        kept = team_note_file.migrate_legacy_documents(where)

        assert len(kept) == 1
        assert not legacy.exists()
        assert kept[0].read_text() == "shared\n\n## only in the Codex copy\n"
        assert app.team_note["body"] == "shared\n"  # nothing sent
        assert app.team_note["version"] == 3  # nothing minted

    def test_every_harness_root_is_swept_including_env_overrides(self, client, app, where):
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 3
        _seed(where, client)
        for source in ("claude_code", "codex", "pi"):
            self._legacy(source).write_text(f"unsent, from {source}\n")

        kept = team_note_file.migrate_legacy_documents(where)

        assert len(kept) == 3
        assert {p.read_text() for p in kept} == {
            "unsent, from claude_code\n",
            "unsent, from codex\n",
            "unsent, from pi\n",
        }

    def test_parking_twice_never_clobbers_the_first_copy(self, client, app, where):
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 3
        _seed(where, client)
        legacy = self._legacy("codex")

        legacy.write_text("first\n")
        team_note_file.migrate_legacy_documents(where)
        legacy.write_text("second\n")
        team_note_file.migrate_legacy_documents(where)

        bodies = sorted(p.read_text() for p, _, _ in team_note_file.parked_copies(where))
        assert bodies == ["first\n", "second\n"]

    def test_an_unreadable_legacy_copy_is_kept(self, client, app, where):
        """Unreadable is an unknown, not an absence."""
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 3
        _seed(where, client)
        legacy = self._legacy("codex")
        legacy.write_bytes(b"\xff\xfe not utf-8")

        kept = team_note_file.migrate_legacy_documents(where)

        assert len(kept) == 1
        assert kept[0].read_bytes() == b"\xff\xfe not utf-8"

    def test_a_write_racing_the_migration_is_caught_next_time(self, client, app, where):
        """The rename is the compare-and-swap: an agent still holding the old
        path writes a FRESH file, which the next sweep parks in turn."""
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 3
        _seed(where, client)
        legacy = self._legacy("codex")
        legacy.write_text("shared\n")

        team_note_file.migrate_legacy_documents(where)
        legacy.write_text("shared\n\n## typed a moment too late\n")
        kept = team_note_file.migrate_legacy_documents(where)

        assert len(kept) == 1
        assert kept[0].read_text() == "shared\n\n## typed a moment too late\n"

    def test_a_vanished_legacy_file_is_not_an_error(self, client, app, where, monkeypatch):
        """Two harness sessions starting together race here."""
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 3
        _seed(where, client)
        legacy = self._legacy("codex")
        legacy.write_text("gone in a moment\n")

        def vanished(src, dst):
            raise FileNotFoundError(src)

        # The park reserves its name with `link` and falls back to `replace`;
        # a file that disappeared under either must read as "someone else got
        # there first", never as an error.
        monkeypatch.setattr(team_note_file.os, "link", vanished)
        monkeypatch.setattr(team_note_file.os, "replace", vanished)
        assert team_note_file.migrate_legacy_documents(where) == []

    def test_the_new_document_is_never_parked_by_the_sweep(self, client, app, where, monkeypatch):
        """A harness root that happens to BE the state dir must not eat the
        document the sweep exists to protect."""
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 3
        _seed(where, client)
        monkeypatch.setenv("CODEX_HOME", str(where.document.parent))

        assert team_note_file.migrate_legacy_documents(where) == []
        assert where.document.read_text() == "shared\n"


class TestTheRemovedVerbs:
    """The OLD append/edit are gone: client routes `/v1/team-note/append|edit`
    (404 now), sent fail-open, so a refusal was journaled and the CLI printed
    success. `append_team_note` / `edit_team_note` are back for a caller with no
    file (`probe notes append|edit --team`), on the SERVER-computed routes, and
    may never be the fail-open kind again."""

    def test_the_old_routes_are_never_called(self, client, app):
        app.team_note["body"] = "GPUs are oversubscribed.\n"
        client.append_team_note("Cap vitest at 2 threads.")
        client.edit_team_note("oversubscribed", "free after 6pm")
        paths = [r.url.path for r in app.requests if r.method == "POST"]
        assert paths == ["/v1/team-note/apply/paragraph", "/v1/team-note/apply/span"]

    def test_a_refusal_raises_and_is_never_queued(self, app, tmp_path):
        from tests.conftest import make_client

        queued = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
        app.team_note["body"] = "a\na\n"
        with pytest.raises(errors.ConflictError) as refused:
            queued.edit_team_note("a", "b")
        assert refused.value.detail["match_count"] == 2
        # Sent at once even under async writes, so the version comes back.
        assert queued.append_team_note("c")["version"] == 1
        assert not queued.journal.pending()


class TestTheBrief:
    def test_the_brief_is_what_a_session_is_given(self, client, app):
        app.team_note["body"] = "## Cluster\n\nGPUs are oversubscribed.\n"
        brief = client.get_team_note_brief()
        assert "GPUs are oversubscribed" in brief["text"]
        assert brief["truncated"] is False

    def test_the_mcp_reads_it_as_a_singleton(self, service, app):
        app.team_note["body"] = "## Cluster\n\nGPUs are oversubscribed.\n"
        result = service.get_entity("team-note", view="card", token_budget=50_000)
        assert "GPUs are oversubscribed" in str(result["data"])

    def test_an_empty_team_note_says_so_in_words(self, service, app):
        app.team_note["body"] = ""
        result = service.get_entity("team-note", view="card", token_budget=50_000)
        payload = str(result["data"])
        assert "empty" in payload
        assert result["data"]["entity"]["body"] == ""


class _DoctorSettings:
    """The two attributes `paths_for` reads, pointed at the test's own state."""

    def __init__(self, where):
        self.base_url = "https://example.test"
        self.token = "token-abc"


class TestTheDoctorRow:
    """`probe doctor` is where a person finds parked copies.

    The session-start hook tells the MODEL; a headless machine, or a researcher
    wondering why the note looks thin, needs somewhere to look. Nothing else
    reports these, and a parked copy nobody knows about is text lost in
    practice even though it is safe on disk.
    """

    def test_parked_copies_are_listed_with_whose_they_are(self, client, app, where, monkeypatch):
        from probe.cli import doctor

        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 2
        _seed(where, client)
        where.document.write_text("mine, unsent\n")
        team_note_file.park(where.document)
        other = team_note_file.paths(origin="https://other.test", identity="token-B")
        where.document.write_text("theirs, unsent\n")
        where.stamp.write_text(other.owner)
        team_note_file.park(where.document)

        # `_team_note_rows` imports `resolve` inside the function, so the patch
        # has to land on the module it imports FROM.
        from probe.sdk import config as sdk_config

        monkeypatch.setattr(sdk_config, "resolve", lambda **_: _DoctorSettings(where))
        rows = doctor._team_note_rows()

        parked = [row for row in rows if "Parked copy" in row]
        assert len(parked) == 2
        assert any("unsent work" in row for row in parked)
        assert any("another team's note" in row for row in parked)

    def test_no_parked_copies_means_no_rows(self, client, app, where, monkeypatch):
        from probe.cli import doctor

        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 2
        _seed(where, client)

        # `_team_note_rows` imports `resolve` inside the function, so the patch
        # has to land on the module it imports FROM.
        from probe.sdk import config as sdk_config

        monkeypatch.setattr(sdk_config, "resolve", lambda **_: _DoctorSettings(where))
        rows = doctor._team_note_rows()

        assert not [row for row in rows if "Parked copy" in row]
        assert any("Unsynced edits" in row and "none" in row for row in rows)


class TestTheBriefIsNotTheBytes:
    """`brief()` returns `body.strip()`, so it is a VIEW, not the document.

    Recording that view as the base copy makes the document's first line read as
    changed on both sides of a later merge, and diff3 reports a conflict for two
    edits that never overlapped. Caught against a live server: a teammate's
    paragraph and this session's paragraph, appended at the same point, came
    back as conflict markers and neither reached the team.
    """

    def test_a_dirty_file_merges_against_the_real_bytes_not_the_brief(self, client, app, where):
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        # The seed came from the brief, which strips -- so re-point the local
        # state at exactly what a real server would have handed back.
        where.base.write_text("start")
        where.document.write_text("start")

        where.document.write_text("start\n\nthis session's finding.\n")
        app.team_note["body"] = "start\n\na teammate's finding.\n"
        app.team_note["version"] = 2

        report, _ = team_note_file.pull(client, where)

        text = where.document.read_text()
        assert not report.conflicted, text
        assert "this session's finding." in text
        assert "a teammate's finding." in text
        # And the base is the server's bytes, trailing newline included.
        assert where.base.read_text() == "start\n\na teammate's finding.\n"

    def test_a_clean_seed_still_costs_one_request(self, client, app, where):
        """The extra fetch is for files with work in them, not for every start."""
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        calls = []
        real_full = client.get_team_note
        client.get_team_note = lambda: (calls.append(1), real_full())[1]
        try:
            team_note_file.pull(client, where)  # first seed: no base yet, fetches
            before = len(calls)
            app.team_note["body"] = "start\n\nmore\n"
            app.team_note["version"] = 2
            team_note_file.pull(client, where)  # clean file: brief is enough
            assert len(calls) == before
        finally:
            client.get_team_note = real_full


class TestAdoptRefusesLegacyCopies:
    """A legacy copy carries OUR stamp -- the old CLI wrote it.

    Which means "is this ours?" is not enough to decide whether to take one
    back. Its merge base is unknowable: a per-harness copy can be missing whole
    sections the other harness contributed, and merging it against our base
    reads those as DELETIONS. Adopting one would hand exactly that document to
    the next push. Only work we parked ourselves, from this same path, is
    adoptable.
    """

    def test_a_legacy_copy_is_never_adopted_even_though_it_is_stamped_ours(
        self, client, app, where
    ):
        from probe.cli import agent_rules

        app.team_note["body"] = "shared\n\n## kept by the other harness\n"
        app.team_note["version"] = 3
        _seed(where, client)

        legacy = agent_rules.memory_path("codex").parent / team_note_file.DOCUMENT_NAME
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_text("shared\n")  # stale: the section never reached this copy
        legacy.with_name(legacy.name + ".owner").write_text(where.owner)

        team_note_file.migrate_legacy_documents(where)
        parked = team_note_file.parked_copies(where)
        assert [kind for _, _, kind in parked] == ["legacy"]
        assert [owner for _, owner, _ in parked] == [where.owner], "stamped ours, and still not ours to send"

        assert team_note_file.adopt(where) is None
        assert where.document.read_text() == "shared\n\n## kept by the other harness\n"

        # And a full reconcile does not quietly send it either.
        team_note_file.reconcile(client, where)
        assert "kept by the other harness" in app.team_note["body"]
        assert app.team_note["version"] == 3

    def test_our_own_parked_work_is_still_adopted(self, client, app, where):
        """The other half of the rule: `unsynced` parks ARE ours to take back."""
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("shared\n\nmine, unsent\n")
        parked = team_note_file.park(where.document, kind="unsynced")
        assert team_note_file.parked_kind(parked) == "unsynced"

        assert team_note_file.adopt(where) == parked
        assert where.document.read_text() == "shared\n\nmine, unsent\n"


class TestAFailedMergeDoesNotAdvanceTheBase:
    """The base copy is a CLAIM ABOUT THE FILE, not about the server.

    When a local merge cannot be written -- the document is past the merge's
    line cap, or it moved again inside the lock -- the file is still derived
    from the OLD base. Recording the server's head there anyway tells the next
    push "this file is a descendant of the head", and the server applies the
    head's own paragraphs back as deletions. That is the same shape as the bug
    this whole change exists to fix, one layer down.
    """

    @staticmethod
    @contextlib.contextmanager
    def _unmergeable():
        """A merge that cannot run, lifted at the end of the `with`.

        NOT `monkeypatch.undo()`: the `monkeypatch` fixture is one instance per
        test, shared with conftest's autouse home isolation, so undoing here
        would also hand the rest of the test the real `~`.
        """
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(
                team_note_file,
                "merge3",
                lambda *a, **k: (_ for _ in ()).throw(RuntimeError("too big")),
            )
            yield

    def test_pull_keeps_the_old_base_so_the_next_push_still_merges(
        self, client, app, where, monkeypatch
    ):
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("start\n\nmine, unsent\n")
        app.team_note["body"] = "start\n\na teammate's paragraph\n"
        app.team_note["version"] = 2

        with self._unmergeable():
            report, _ = team_note_file.pull(client, where)

        assert "could not merge" in report.detail
        assert where.base.read_text() == "start\n", "the base still describes the FILE"
        assert json.loads(where.meta.read_text())["version"] == 1

        # And because the base stayed put, the next push is a merge, not a
        # deletion: the teammate's paragraph survives.
        team_note_file.push(client, where)
        assert "a teammate's paragraph" in app.team_note["body"]
        assert "mine, unsent" in app.team_note["body"]

    def test_push_keeps_the_old_base_when_the_rebase_cannot_be_written(
        self, client, app, where, monkeypatch
    ):
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("start\n\nmine\n")
        real_sync = client.sync_team_note

        def racing_sync(body, *, base_version):
            app.team_note["body"] = "start\n\na teammate's paragraph\n"
            app.team_note["version"] = 2
            result = real_sync(body, base_version=base_version)
            where.document.write_text("start\n\nmine, still typing\n")
            return result

        monkeypatch.setattr(client, "sync_team_note", racing_sync)
        with self._unmergeable():
            report = team_note_file.push(client, where)

        assert "could not merge" in report.detail
        assert where.base.read_text() == "start\n", "the base still describes the FILE"

        monkeypatch.setattr(client, "sync_team_note", real_sync)
        team_note_file.push(client, where)
        assert "a teammate's paragraph" in app.team_note["body"]
        assert "still typing" in app.team_note["body"]


class TestParkingIsBounded:
    def test_an_identical_copy_is_not_parked_twice(self, client, app, where):
        """Two credentials alternating on one machine park each other on every
        sync. Without this the directory grows by a full copy of the note per
        turn, forever, and `probe doctor` lists all of them."""
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 1
        _seed(where, client)

        for _ in range(3):
            where.document.write_text("the same unsent text\n")
            team_note_file.park(where.document)

        parked = team_note_file.parked_copies(where)
        assert len(parked) == 1
        assert parked[0][0].read_text() == "the same unsent text\n"

    def test_a_different_copy_is_still_parked(self, client, app, where):
        app.team_note["body"] = "shared\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("first\n")
        team_note_file.park(where.document)
        where.document.write_text("second\n")
        team_note_file.park(where.document)

        assert sorted(p.read_text() for p, _, _ in team_note_file.parked_copies(where)) == [
            "first\n",
            "second\n",
        ]


class TestResumingDoesNotDeleteWhatLandedMeanwhile:
    """A parked copy is old text. The world moved while it sat there.

    Restoring it against the base the machine holds NOW makes every paragraph
    that landed in between look like a deletion by the person resuming -- they
    switched credential for an afternoon and came back to find a teammate's
    section gone. The ancestor parked beside the text is what keeps the resume
    an ordinary three-way merge.
    """

    def test_a_teammates_paragraph_survives_a_resume(self, client, app, where):
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("start\n\nmine, unsent\n")

        # Another credential takes the machine; our work is parked with the
        # base it was edited from.
        other = team_note_file.paths(origin="https://other.test", identity="token-B")
        app.team_note["body"] = "theirs\n"
        app.team_note["version"] = 9
        team_note_file.pull(client, other)

        # A teammate writes to OUR note while we are away.
        app.team_note["body"] = "start\n\na teammate's paragraph\n"
        app.team_note["version"] = 2

        # We come back and reconcile.
        team_note_file.reconcile(client, where)

        body = app.team_note["body"]
        assert "a teammate's paragraph" in body, "the resume must not delete what landed meanwhile"
        assert "mine, unsent" in body, "and it must still carry our work"

    def test_a_parked_copy_with_no_ancestor_is_left_for_a_person(self, client, app, where):
        """An older CLI parked it without one. Guessing an ancestor is how the
        deletion above happens, so this refuses and says so instead."""
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("mine, unsent\n")
        parked = team_note_file.park(where.document)
        parked.with_name(parked.name + ".base").unlink()

        assert team_note_file.adopt(where) is None
        assert parked.read_text() == "mine, unsent\n"
        assert [p for p, _, _ in team_note_file.parked_copies(where)] == [parked]


class TestOverlappingSyncs:
    def test_a_pull_defers_to_a_newer_one_that_landed_meanwhile(self, client, app, where):
        """Two reconciles overlap; the slower one must not undo the faster.

        Its base and version were read before the network call. Writing them
        afterwards merges against an ancestor that is no longer current --
        which duplicates the paragraphs the other sync already merged -- and
        then stamps the older version number over the newer one.
        """
        app.team_note["body"] = "start\n"
        app.team_note["version"] = 1
        _seed(where, client)
        where.document.write_text("start\n\nmine\n")
        app.team_note["body"] = "start\n\nremote\n"
        app.team_note["version"] = 2

        real_brief = client.get_team_note_brief

        def slow_brief():
            answer = real_brief()
            # Another session completes a full reconcile while we are in flight.
            app.team_note["body"] = "start\n\nremote\n\nmine\n"
            app.team_note["version"] = 3
            team_note_file._commit(
                where, body=app.team_note["body"], version=3, write_document=True
            )
            return answer

        client.get_team_note_brief = slow_brief
        try:
            report, _ = team_note_file.pull(client, where)
        finally:
            client.get_team_note_brief = real_brief

        assert "newer version" in report.detail
        assert json.loads(where.meta.read_text())["version"] == 3
        assert where.document.read_text().count("mine") == 1, "no duplicated paragraph"


# --- the churn-guard baseline health.json records for the audit trigger -----


def _sha(document: str) -> str:
    import hashlib

    return hashlib.sha256(document.strip().encode("utf-8")).hexdigest()


def test_the_first_sighting_records_no_hash() -> None:
    """THE SUPPRESSION BUG THIS PREVENTS, found in review.

    Every existing machine reaches the first render after this ships with no
    `audit` key. Hashing the document THEN would file however many weeks of
    un-audited appends under the OLD stamp as "what the last audit produced",
    and the very next audit would be told nothing had changed and to skip its
    tightening. A hash is only ever written when a stamp CHANGE is observed,
    because that is the only evidence available here that an audit ran.
    """
    from probe.cli import team_note_file as tnf

    first = tnf._audit_baseline("<!-- audited 2026-09-01 -->\nweeks of appends", None)
    assert first == {"stamp": "2026-09-01"}
    assert "content_sha256" not in first


def test_the_baseline_follows_the_stamp_not_the_render() -> None:
    """Refreshing the hash on every render would answer "changed since the last
    RENDER" -- nearly always no, since renders happen at every session start --
    and tightening would be suppressed forever."""
    from probe.cli import team_note_file as tnf

    body = "<!-- audited 2026-09-01 -->\nbody"
    seen = tnf._audit_baseline(body, None)

    # Someone appends. Same stamp, so nothing may move.
    assert tnf._audit_baseline(body + "\nmore", seen) == seen

    # A new audit stamps it. NOW the hash is written, and it is this audit's output.
    audited = "<!-- audited 2026-09-08 -->\nbody\nmore"
    moved = tnf._audit_baseline(audited, seen)
    assert moved["stamp"] == "2026-09-08"
    assert moved["content_sha256"] == _sha(audited)


def test_the_hash_is_taken_over_the_stripped_document() -> None:
    """The render strips before it renders, and the hook must strip before it
    compares. They hashed different bytes in review: `_topped_up` guarantees a
    trailing newline on every paragraph write, so the guard would have been dead
    on any tenant that ever used that door -- silently, by tightening every
    cycle forever."""
    from probe.cli import team_note_file as tnf

    seen = {"stamp": "2026-09-01"}
    audited = "<!-- audited 2026-09-08 -->\nbody"
    assert (
        tnf._audit_baseline(audited + "\n\n", seen)["content_sha256"]
        == tnf._audit_baseline(audited, seen)["content_sha256"]
        == _sha(audited)
    )


def test_an_unstamped_note_records_no_baseline() -> None:
    """There is no audit to be unchanged since."""
    from probe.cli import team_note_file as tnf

    assert tnf._audit_baseline("no stamp here", None) == {}
