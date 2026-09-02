"""`board set-cred` resolving from the cwd, and the new `innoday timeline` reader.

Both exist because a value the tool already knows should not be something the
operator has to restate: `set-credential` demanded a board UUID and a board type
during a *credential rotation*, which is exactly when a copy-paste error is most
expensive; and the timeline had rows since PF-102 with no client at all, which is
how "summaries never reached the timeline" stayed invisible.
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from unittest.mock import patch

import pytest

# ------------------------------------------------------------------ set-cred


def _config():
    class C:
        def get_user_id(self):
            return "user-1"

        def get_current_organization(self):
            return "hs"

        def get_organization_id(self, alias):
            return "org-1"

        def get_current_project_id(self):
            return "proj-1"

        def get_organization_integration(self, alias, t):
            return None

    return C()


def _client(boards, patch_status=200):
    """A client whose GET /boards returns `boards` and whose PATCH succeeds."""

    class Resp:
        def __init__(self, status, payload):
            self.status_code = status
            self._payload = payload
            self.content = b"{}"
            self.text = "{}"

        def json(self):
            return self._payload

    class C:
        def __init__(self):
            self.patched = []

        async def get(self, path, params=None):
            return Resp(200, boards)

        async def patch(self, path, headers=None, **kw):
            self.patched.append((path, headers))
            return Resp(
                patch_status,
                {"board_type": "linear", "updated_at": "2026-08-08T00:00:00"},
            )

    return C()


LINEAR_BOARD = [
    {
        "id": "board-77",
        "project_id": "proj-1",
        "board_name": "Bright Power (BPAI)",
        "board_type": "linear",
    }
]


@pytest.mark.asyncio
async def test_set_cred_needs_neither_board_id_nor_type():
    """The whole point: `--token` alone, standing in the project directory.

    Previously both `--board-id` and `--type` were `required=True`, so rotating
    a credential meant pasting a UUID and restating a type the board record
    already holds.
    """
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(
        board_command="set-cred",
        board_id=None,
        type=None,
        email=None,
        api_token=None,
        api_key=None,
        token="lin_api_xxx",
    )
    client = _client(LINEAR_BOARD)

    rc = await BoardCommands._handle_set_credential(args, client, _config())

    assert rc == 0
    assert client.patched, "no PATCH was issued"
    path, headers = client.patched[0]
    assert "board-77" in path, "did not target the cwd project's board"
    # The linear shape is the bare token — proof the type came from the record.
    assert headers["X-Integration-Token"] == "lin_api_xxx"


@pytest.mark.asyncio
async def test_an_explicit_board_id_still_wins_and_supplies_its_type():
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(
        board_command="set-cred",
        board_id="board-77",
        type=None,
        email=None,
        api_token=None,
        api_key=None,
        token="lin_api_xxx",
    )
    client = _client(LINEAR_BOARD)

    rc = await BoardCommands._handle_set_credential(args, client, _config())

    assert rc == 0
    assert "board-77" in client.patched[0][0]


@pytest.mark.asyncio
async def test_a_jira_board_still_demands_both_jira_fields():
    """Type inference must not weaken the per-type field requirements.

    A Jira credential is `email:token`; inferring the type from the record is
    only about not retyping it, never about accepting half a credential.
    """
    from src.cli.commands.boards import BoardCommands

    jira_board = [
        {
            "id": "board-88",
            "project_id": "proj-1",
            "board_name": "ITPT",
            "board_type": "jira",
        }
    ]
    args = argparse.Namespace(
        board_command="set-cred",
        board_id=None,
        type=None,
        email=None,  # missing
        api_token="tok",
        api_key=None,
        token=None,
    )
    client = _client(jira_board)

    rc = await BoardCommands._handle_set_credential(args, client, _config())

    assert rc == 1
    assert not client.patched


@pytest.mark.asyncio
async def test_no_board_on_the_project_aborts_rather_than_guessing():
    from src.cli.commands.boards import BoardCommands

    args = argparse.Namespace(
        board_command="set-cred",
        board_id=None,
        type=None,
        email=None,
        api_token=None,
        api_key=None,
        token="x",
    )
    client = _client([])

    rc = await BoardCommands._handle_set_credential(args, client, _config())

    assert rc == 1
    assert not client.patched


def test_set_credential_survives_as_an_alias():
    """The old name is in the docs and in people's shell history.

    An argparse alias costs nothing next to a command that silently vanished.
    """
    from src.cli.commands.boards import BoardCommands

    parser = argparse.ArgumentParser()
    BoardCommands.setup_parser(parser)

    for name in ("set-cred", "set-credential"):
        args = parser.parse_args([name, "--token", "x"])
        assert args.board_command == name
        assert args.board_id is None
        assert args.type is None


# ------------------------------------------------------------------ timeline


class TestRenderTimeline:
    """The renderer is pure, so the layout rules are testable without a server."""

    def test_an_empty_feed_says_so_rather_than_printing_a_bare_header(self):
        from src.cli.commands.timeline import render_timeline

        out = render_timeline([], project_label="PF", verbose=False)
        assert "Nothing on this project's timeline yet" in out

    def test_an_entry_shows_its_type_title_and_summary(self):
        from src.cli.commands.timeline import render_timeline

        out = render_timeline(
            [
                {
                    "event_type": "scrum_summary",
                    "title": "Scrum summary (3d)",
                    "summary": "A scrum summary covering the last 3d was written.",
                    "occurred_at": "2026-08-08T12:07:30+00:00",
                    "created_by": "agent",
                }
            ],
            project_label="PF",
            verbose=False,
        )
        assert "scrum summary" in out
        assert "Scrum summary (3d)" in out
        assert "covering the last 3d" in out
        assert "by agent" in out

    def test_system_authorship_is_not_worth_a_line(self):
        """Almost every entry is written by `system`; saying so every time is noise."""
        from src.cli.commands.timeline import render_timeline

        out = render_timeline(
            [
                {
                    "event_type": "ticket_sync",
                    "title": "PixelFuel (PF) synced",
                    "summary": "42 tickets updated.",
                    "occurred_at": "2026-08-08T12:00:00+00:00",
                    "created_by": "system",
                }
            ],
            project_label="PF",
            verbose=False,
        )
        assert "by system" not in out

    def test_metadata_appears_only_with_verbose(self):
        from src.cli.commands.timeline import render_timeline

        entry = {
            "event_type": "release",
            "title": "Release v1.8.0 created",
            "summary": "s",
            "occurred_at": "2026-08-08T12:00:00+00:00",
            "created_by": "system",
            "metadata": {"version": "v1.8.0"},
        }
        assert "v1.8.0'" not in render_timeline(
            [entry], project_label="PF", verbose=False
        )
        assert "version" in render_timeline([entry], project_label="PF", verbose=True)

    def test_a_junk_timestamp_does_not_raise(self):
        from src.cli.commands.timeline import render_timeline

        out = render_timeline(
            [
                {
                    "event_type": "release",
                    "title": "t",
                    "summary": "s",
                    "occurred_at": "not-a-date",
                    "created_by": "system",
                }
            ],
            project_label="PF",
            verbose=False,
        )
        assert "t" in out


class TestAge:
    def test_relative_not_absolute(self):
        """A timeline answers "how recently", so don't make the reader subtract."""
        from datetime import datetime, timedelta, timezone

        from src.cli.commands.timeline import _age

        now = datetime.now(timezone.utc)
        assert _age((now - timedelta(minutes=5)).isoformat()).endswith("m ago")
        assert _age((now - timedelta(hours=5)).isoformat()).endswith("h ago")
        assert _age((now - timedelta(days=5)).isoformat()).endswith("d ago")

    def test_unusable_input_is_empty_not_an_exception(self):
        from src.cli.commands.timeline import _age

        assert _age(None) == ""
        assert _age("") == ""
        assert _age("garbage") == ""


@pytest.mark.asyncio
async def test_timeline_command_requires_a_project():
    from src.cli.commands.timeline import TimelineCommands

    class C:
        def get_current_organization(self):
            return "hs"

        def get_organization_id(self, alias):
            return "org-1"

        def get_current_project_id(self):
            return None

    args = argparse.Namespace(
        timeline_project=None,
        timeline_event=None,
        timeline_limit=20,
        timeline_verbose=False,
        timeline_json=False,
    )
    rc = await TimelineCommands.execute(args, C())
    assert rc == 1


@pytest.mark.asyncio
async def test_timeline_command_clamps_the_limit_to_the_api_ceiling():
    """The route rejects >200 with a 422; clamping beats a confusing error."""
    from src.cli.commands.timeline import TimelineCommands

    class C:
        def get_current_organization(self):
            return "hs"

        def get_organization_id(self, alias):
            return "org-1"

        def get_current_project_id(self):
            return "proj-1"

    seen = {}

    class Resp:
        status_code = 200
        text = "{}"

        def json(self):
            return {"entries": [], "next_cursor": None}

    class Client:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def get(self, path, params=None):
            seen.update(params or {})
            return Resp()

    args = argparse.Namespace(
        timeline_project="PF",
        timeline_event=None,
        timeline_limit=9999,
        timeline_verbose=False,
        timeline_json=False,
    )
    with patch("src.cli.commands.timeline.InnoDayAPIClient", return_value=Client()):
        rc = await TimelineCommands.execute(args, C())

    assert rc == 0
    assert seen["limit"] == 200


class TestTimelineLabelsTheProjectItIsShowing:
    """The header names the project. Two different flags could make it name a
    different one than the events came from — and a timeline that attributes
    one client's work to another client's project is not mislabelled, it is
    wrong. `summary` fixed both of these; `timeline` had not."""

    @staticmethod
    def _run(monkeypatch, *, args_extra, context, project_id):
        import src.cli.commands.timeline as tl

        seen = {}

        def fake_load(start=None):
            seen["start"] = start
            return context

        class Resp:
            status_code = 200
            text = "{}"

            def json(self):
                return {"entries": [], "next_cursor": None}

        class Client:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            async def get(self, path, params=None):
                return Resp()

        def fake_render(entries, *, project_label, verbose):
            seen["label"] = project_label

        monkeypatch.setattr(tl, "load_project_context", fake_load)
        monkeypatch.setattr(tl, "render_timeline", fake_render)
        monkeypatch.setattr(tl, "InnoDayAPIClient", lambda config: Client())

        class C:
            def get_current_organization(self):
                return "hs"

            def get_organization_id(self, alias):
                return "org-1"

            def get_current_project_id(self):
                return project_id

        base = dict(
            timeline_project=None,
            timeline_event=None,
            timeline_limit=20,
            timeline_verbose=False,
            timeline_json=False,
        )
        base.update(args_extra)
        rc = asyncio.run(tl.TimelineCommands.execute(argparse.Namespace(**base), C()))
        assert rc == 0
        return seen

    def test_the_context_directory_reaches_the_label_lookup(self, monkeypatch):
        """`--dir` is the automation path. `config` honours it; this lookup read
        the cwd, so `innoday --dir <bpai> timeline` printed BPAI's events under
        the working directory's name."""
        seen = self._run(
            monkeypatch,
            args_extra={"dir": "/somewhere/bpai"},
            context={"project_id": "proj-bpai", "project_alias": "BPAI"},
            project_id="proj-bpai",
        )
        assert seen["start"] == Path("/somewhere/bpai")
        assert seen["label"] == "BPAI"

    def test_no_context_directory_still_means_the_cwd(self, monkeypatch):
        """Passing None keeps `load_project_context`'s own default, so the
        ordinary cd-into-the-workspace path is untouched."""
        seen = self._run(
            monkeypatch,
            args_extra={},
            context={"project_id": "proj-1", "project_alias": "PF"},
            project_id="proj-1",
        )
        assert seen["start"] is None
        assert seen["label"] == "PF"

    def test_the_global_project_flag_is_not_relabelled_by_the_cwd(self, monkeypatch):
        """There are two `--project` flags. The old guard checked the
        subcommand's alone, so the global one — which reaches `config` — left the
        label falling through to the working directory: BPAI's timeline titled
        PF. Matching on the id closes it, whichever flag was used."""
        seen = self._run(
            monkeypatch,
            args_extra={},
            context={"project_id": "proj-pf", "project_alias": "PF"},
            project_id="proj-bpai",
        )
        assert seen["label"] == "proj-bpai"
