"""The paper command's required source contract and compatibility alias."""

from __future__ import annotations

import contextlib
import importlib
import re

from typer.main import get_command
from typer.testing import CliRunner

cli_main = importlib.import_module("probe.cli.main")


class _PaperClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []
        #: What `get_paper` reports the paper already carries — the left-hand
        #: side of the `tag` verb's read-modify-write.
        self.tags: list[str] = []

    def add_paper(self, project_id: str, **fields):
        self.calls.append((project_id, fields))
        return {"id": "paper-1", "project_id": project_id, **fields}

    def update_paper(self, paper_id: str, **fields):
        self.calls.append((paper_id, fields))
        return {"id": paper_id, **fields}

    def get_paper(self, paper_id: str):
        return {"id": paper_id, "tags": list(self.tags)}


def _install(monkeypatch):
    client = _PaperClient()
    monkeypatch.setattr(
        cli_main, "_client", lambda: contextlib.nullcontext(client)
    )
    monkeypatch.setattr(cli_main, "_project_id", lambda _client, ref: ref)
    return client


def _squashed(output: str) -> str:
    """CLI output with ANSI escapes and ALL whitespace removed.

    CI renders these errors coloured and narrow, so a long flag name is wrapped
    across lines with escape codes around it and a plain `in` check fails there
    while passing locally. TODOS.md records the same trap on a different test.
    Removing every space AND newline makes the assertion survive any wrap point,
    including one mid-token.
    """
    return re.sub(r"\x1b\[[0-9;]*m", "", output).translate(
        {ord(c): None for c in " \t\n\r"}
    )


def test_paper_add_requires_a_source(monkeypatch) -> None:
    _install(monkeypatch)
    result = CliRunner().invoke(
        cli_main.app,
        ["paper", "add", "review", "A title"],
    )

    assert result.exit_code == 2
    add_command = get_command(cli_main.paper_app).commands["add"]
    source_option = next(param for param in add_command.params if param.name == "source")
    assert source_option.required is True
    assert "--source" in source_option.opts


def test_paper_add_accepts_source_and_legacy_url_alias(monkeypatch) -> None:
    for option in ("--source", "--url"):
        client = _install(monkeypatch)
        result = CliRunner().invoke(
            cli_main.app,
            ["paper", "add", "review", "A title", option, "./papers/a.pdf"],
        )

        assert result.exit_code == 0, result.output
        assert client.calls == [
            (
                "review",
                {
                    "title": "A title",
                    "source_url": "./papers/a.pdf",
                    "authors": None,
                    "repo_url": None,
                    "summary_md": None,
                    "discrepancies_md": None,
                    "tags": None,
                    # 0180: absent lineage passes None, which the SDK drops from
                    # the body entirely -- so the server sees no `lineage` key
                    # and the paper stays UNKNOWN rather than claiming a root.
                    "lineage": None,
                },
            )
        ]


def test_paper_update_accepts_source_and_legacy_url_alias(monkeypatch) -> None:
    for option in ("--source", "--url"):
        client = _install(monkeypatch)
        result = CliRunner().invoke(
            cli_main.app,
            ["paper", "update", "paper-1", option, "./papers/b.pdf"],
        )

        assert result.exit_code == 0, result.output
        assert client.calls == [
            (
                "paper-1",
                {
                    "title": None,
                    "source_url": "./papers/b.pdf",
                    "authors": None,
                    "repo_url": None,
                    "summary_md": None,
                    "discrepancies_md": None,
                    "tags": None,
                },
            )
        ]


# --- tags (0176) -------------------------------------------------------------
# `paper tag` is the same read-modify-write verb project/run/experiment have.
# The tests below pin the two things that verb gets wrong when it is rewritten
# per entity: a bare invocation must READ rather than clear, and a positional
# word after options must ADD rather than replace.


def test_paper_add_passes_repeated_tags_through(monkeypatch) -> None:
    client = _install(monkeypatch)
    result = CliRunner().invoke(
        cli_main.app,
        [
            "paper", "add", "review", "A title",
            "--source", "./papers/a.pdf",
            "--tag", "retrieval",
            "--tag", "rl",
        ],
    )

    assert result.exit_code == 0, result.output
    assert client.calls[0][1]["tags"] == ["retrieval", "rl"]


def test_paper_add_without_tags_sends_none_not_an_empty_list(monkeypatch) -> None:
    """`None` is omission and `[]` is "clear them all". An add that sent `[]`
    would be indistinguishable from a deliberate clear at the server, and would
    trip the SDK's write-verification guard for no reason."""
    client = _install(monkeypatch)
    result = CliRunner().invoke(
        cli_main.app,
        ["paper", "add", "review", "A title", "--source", "./papers/a.pdf"],
    )

    assert result.exit_code == 0, result.output
    assert client.calls[0][1]["tags"] is None


def test_paper_tag_bare_lists_without_writing(monkeypatch) -> None:
    client = _install(monkeypatch)
    client.tags = ["retrieval", "rl"]
    result = CliRunner().invoke(cli_main.app, ["paper", "tag", "paper-1"])

    assert result.exit_code == 0, result.output
    assert "retrieval" in result.output
    # Read-only: a bare `tag` must never reach update_paper, or listing a
    # paper's tags would be a write that bumps its `updated_at`.
    assert client.calls == []


def test_paper_tag_adds_removes_and_replaces(monkeypatch) -> None:
    client = _install(monkeypatch)
    client.tags = ["retrieval"]
    result = CliRunner().invoke(cli_main.app, ["paper", "tag", "paper-1", "rl"])
    assert result.exit_code == 0, result.output
    assert client.calls[-1] == ("paper-1", {"tags": ["retrieval", "rl"]})

    client = _install(monkeypatch)
    client.tags = ["retrieval", "rl"]
    result = CliRunner().invoke(
        cli_main.app, ["paper", "tag", "paper-1", "--remove", "rl"]
    )
    assert result.exit_code == 0, result.output
    assert client.calls[-1] == ("paper-1", {"tags": ["retrieval"]})

    client = _install(monkeypatch)
    client.tags = ["retrieval", "rl"]
    result = CliRunner().invoke(
        cli_main.app, ["paper", "tag", "paper-1", "--set", "kv-cache"]
    )
    assert result.exit_code == 0, result.output
    assert client.calls[-1] == ("paper-1", {"tags": ["kv-cache"]})


def test_paper_tag_is_a_no_op_when_nothing_would_change(monkeypatch) -> None:
    """The shared flow's changed-check. Re-adding a tag the paper already has
    must not write, or an idempotent tagging pass would touch every paper."""
    client = _install(monkeypatch)
    client.tags = ["retrieval"]
    result = CliRunner().invoke(cli_main.app, ["paper", "tag", "paper-1", "retrieval"])

    assert result.exit_code == 0, result.output
    assert client.calls == []


# -- --via: the three answers (0180) ----------------------------------------


def test_via_none_declares_a_root(monkeypatch) -> None:
    """`--via none` is a POSITIVE claim, and must not look like silence."""
    client = _install(monkeypatch)
    result = CliRunner().invoke(
        cli_main.app,
        ["paper", "add", "review", "A", "--source", "./a.pdf", "--via", "none"],
    )
    assert result.exit_code == 0, result.output
    assert client.calls[0][1]["lineage"] == {"via": None}


def test_via_a_paper_sends_the_edge(monkeypatch) -> None:
    client = _install(monkeypatch)
    result = CliRunner().invoke(
        cli_main.app,
        [
            "paper", "add", "review", "A", "--source", "./a.pdf",
            "--via", "paper-9",
            "--via-provenance", "observed_call",
            "--via-reason", "followed its references",
        ],
    )
    assert result.exit_code == 0, result.output
    assert client.calls[0][1]["lineage"] == {
        "via": "paper-9",
        "provenance": "observed_call",
        "reason": "followed its references",
    }


def test_via_a_paper_without_provenance_is_refused(monkeypatch) -> None:
    """No default anywhere in the stack: a provenance the CLI picked would be a
    claim nobody made, on the field whose job is to say who made the claim."""
    client = _install(monkeypatch)
    result = CliRunner().invoke(
        cli_main.app,
        ["paper", "add", "review", "A", "--source", "./a.pdf", "--via", "paper-9"],
    )
    assert result.exit_code == 2
    # Squashed, never a bare `in`: see _squashed on why CI wraps this away.
    assert "--via-provenance" in _squashed(result.output)
    # And nothing was sent: the refusal happens before the write.
    assert client.calls == []


def test_omitting_via_records_nothing(monkeypatch) -> None:
    """The third answer. Omission must never become a declared root."""
    client = _install(monkeypatch)
    result = CliRunner().invoke(
        cli_main.app,
        ["paper", "add", "review", "A", "--source", "./a.pdf"],
    )
    assert result.exit_code == 0, result.output
    assert client.calls[0][1]["lineage"] is None


def test_edge_add_refuses_a_paper_edge_without_provenance(monkeypatch) -> None:
    """The generic edge verb can name a paper endpoint, so it must ask too.

    Without this the flag exists and nothing proves it is enforced -- and the
    server's 422 would be the only thing standing between an agent and a paper
    edge with no claim strength on it.
    """
    calls: list[dict] = []

    class _EdgeClient:
        def add_edge(self, **kwargs):
            calls.append(kwargs)
            return {"id": "e1"}

    monkeypatch.setattr(
        cli_main, "_client", lambda: contextlib.nullcontext(_EdgeClient())
    )
    result = CliRunner().invoke(
        cli_main.app,
        [
            "edge", "add",
            "--source", "paper:a",
            "--relation", "discovered_via",
            "--target", "paper:b",
        ],
    )
    assert result.exit_code == 2
    assert "--provenance" in _squashed(result.output)
    assert calls == []


def test_edge_add_passes_provenance_through(monkeypatch) -> None:
    calls: list[dict] = []

    class _EdgeClient:
        def add_edge(self, **kwargs):
            calls.append(kwargs)
            return {"id": "e1"}

    monkeypatch.setattr(
        cli_main, "_client", lambda: contextlib.nullcontext(_EdgeClient())
    )
    result = CliRunner().invoke(
        cli_main.app,
        [
            "edge", "add",
            "--source", "paper:a",
            "--relation", "discovered_via",
            "--target", "paper:b",
            "--provenance", "human",
            "--reason", "I remembered",
        ],
    )
    assert result.exit_code == 0, result.output
    assert calls[0]["provenance"] == "human"
    assert calls[0]["reason"] == "I remembered"


def test_edge_add_still_works_without_provenance_for_runs(monkeypatch) -> None:
    """A run edge carries no provenance and must not be asked for one."""
    calls: list[dict] = []

    class _EdgeClient:
        def add_edge(self, **kwargs):
            calls.append(kwargs)
            return {"id": "e1"}

    monkeypatch.setattr(
        cli_main, "_client", lambda: contextlib.nullcontext(_EdgeClient())
    )
    result = CliRunner().invoke(
        cli_main.app,
        [
            "edge", "add",
            "--source", "run:a",
            "--relation", "consumes",
            "--target", "run:b",
        ],
    )
    assert result.exit_code == 0, result.output
    assert calls[0]["provenance"] is None
