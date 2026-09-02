"""An MCP tool asked about another project must not use this one's organization.

The configured organization comes from wherever the server was started, and for
a long-lived MCP server that is one directory forever. Saving a BPAI release
summary from a session started in the PF workspace sent BPAI's project id with
PF's organization id — well-formed, and refused with "Project belongs to a
different organization", which reads as a permissions problem rather than the
resolution problem it is.

`project_dir` is the same hint the CLI takes as `--dir`, and it resolves the
organization and the project together so the two can never disagree.
"""

from __future__ import annotations

import textwrap

import pytest

from src.mcp.server import _API, _project_context

SCHEMA = 2


def _workspace(tmp_path, *, org_id, project_id, alias="BPAI"):
    (tmp_path / ".innoday").mkdir()
    (tmp_path / ".innoday" / "project.yml").write_text(
        textwrap.dedent(f"""\
        schema_version: {SCHEMA}
        org:
          alias: bp
          name: Bright Power
          innoday_id: {org_id}
        project:
          alias: {alias}
          name: Bright Power AI
          innoday_id: {project_id}
        """)
    )
    return tmp_path


class TestTheDirectoryDecides:
    def test_the_org_comes_from_the_directory_not_the_config(self, tmp_path):
        ws = _workspace(tmp_path, org_id="org-from-dir", project_id="proj-from-dir")
        assert _API.resolve_org(None, str(ws)) == "org-from-dir"

    def test_the_project_comes_from_it_too(self, tmp_path):
        """Resolved together, so a caller cannot pair one workspace's project
        with another workspace's organization."""
        ws = _workspace(tmp_path, org_id="org-from-dir", project_id="proj-from-dir")
        assert _API.resolve_project(None, str(ws)) == "proj-from-dir"

    def test_an_explicit_argument_still_wins(self, tmp_path):
        ws = _workspace(tmp_path, org_id="org-from-dir", project_id="proj-from-dir")
        assert _API.resolve_org("explicit", str(ws)) == "explicit"
        assert _API.resolve_project("explicit", str(ws)) == "explicit"


class TestABadHintIsNeverFatal:
    """A hint that cannot be read falls through to the configured default.

    Failing the call instead would make a convenience parameter a new way to
    break every tool that accepts it.
    """

    def test_a_directory_with_no_project_file_is_ignored(self, tmp_path):
        assert _project_context(str(tmp_path)) is None

    def test_a_path_that_does_not_exist_is_ignored(self):
        assert _project_context("/nonexistent/path/for/a/test") is None

    def test_no_hint_at_all_is_ignored(self):
        assert _project_context(None) is None

    def test_an_unreadable_file_does_not_raise(self, tmp_path):
        (tmp_path / ".innoday").mkdir()
        (tmp_path / ".innoday" / "project.yml").write_text("{{{ not yaml")
        assert _project_context(str(tmp_path)) is None

    def test_a_legacy_project_file_is_swallowed(self, tmp_path):
        """The one input that genuinely raises, and the reason for the guard.

        `load_project_context` raises `LegacyProjectFileError` on a file that
        predates the schema stamp — a real state in workspaces that have not
        been refreshed. Letting that escape would turn a stale file in some
        unrelated directory into a failed tool call.
        """
        from src.cli.utils.project_context import (
            LegacyProjectFileError,
            load_project_context,
        )

        (tmp_path / ".innoday").mkdir()
        (tmp_path / ".innoday" / "project.yml").write_text(
            "org:\n  slug: bp\n  innoday_id: x\nproject:\n  innoday_id: y\n"
        )
        with pytest.raises(LegacyProjectFileError):
            load_project_context(tmp_path)
        assert _project_context(str(tmp_path)) is None


class TestTheToolAcceptsIt:
    @pytest.mark.parametrize("tool", ["save_project_summary"])
    def test_project_dir_is_a_parameter(self, tool):
        """The tool that actually failed. Without the parameter on the schema,
        the resolver improvement is unreachable from a tool call."""
        import inspect

        import src.mcp.server as server

        fn = getattr(server, tool)
        fn = getattr(fn, "fn", fn)
        assert "project_dir" in inspect.signature(fn).parameters
