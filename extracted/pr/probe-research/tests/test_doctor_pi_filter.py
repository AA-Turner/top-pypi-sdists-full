"""Doctor names the one condition that made strand-ai invisible.

A pi settings.json that filters our extension out loads the package's skills
and its MCP manifest but never `index.ts` -- so tracking reports on, the MCP
tools answer, and nothing captures. Every other signal reads healthy, which is
why this row has to exist: it is the only place the filter becomes visible.
"""

from __future__ import annotations

import json

import pytest

from probe.cli import doctor, pi_config


@pytest.fixture
def pi_agent(tmp_path, monkeypatch):
    d = tmp_path / "pi-agent"
    d.mkdir()
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(d))
    monkeypatch.setenv("PROBE_AGENT", "pi")
    # `_pi_capture_rows` reads project-scope settings from the process cwd, and
    # the session row only when a session id is in the environment. Pin both,
    # so the suite answers the same in a checkout as on a bare CI runner.
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PI_SESSION_ID", raising=False)
    return d


def _write(path, packages):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"packages": packages}), encoding="utf-8")


def test_filtered_extension_is_reported(pi_agent):
    _write(
        pi_agent / "settings.json",
        [{"source": pi_config.MIRROR_GIT_SOURCE, "extensions": []}],
    )
    rows = doctor._pi_capture_rows()
    assert any("filtered out" in row for row in rows)
    assert any("global" in row for row in rows)


def test_a_normal_install_reports_no_warning(pi_agent):
    _write(pi_agent / "settings.json", [pi_config.MIRROR_GIT_SOURCE])
    rows = doctor._pi_capture_rows()
    assert not any("filtered out" in row for row in rows)


def test_a_pinned_entry_point_is_not_cried_wolf_over(pi_agent):
    """`+path` force-INCLUDES in pi's filter vocabulary -- this install loads."""
    _write(
        pi_agent / "settings.json",
        [
            {
                "source": pi_config.MIRROR_GIT_SOURCE,
                "extensions": ["+plugins/probe-research-pi/index.ts"],
            }
        ],
    )
    assert not any("filtered out" in row for row in doctor._pi_capture_rows())


def test_the_project_scope_is_named_when_the_project_entry_wins(pi_agent, tmp_path):
    """Which file to edit. "global" would send someone to the wrong one."""
    _write(pi_agent / "settings.json", [pi_config.MIRROR_GIT_SOURCE])
    _write(
        tmp_path / ".pi" / "settings.json",
        [{"source": pi_config.MIRROR_GIT_SOURCE, "extensions": []}],
    )
    rows = doctor._pi_capture_rows()
    assert any("filtered out" in row and "project" in row for row in rows)


def test_the_session_row_states_the_closed_vocabulary_reason(pi_agent, tmp_path, monkeypatch):
    """The second half: is a daemon live for THIS session, and if not, why."""
    from probe.cli import capture_state

    _write(pi_agent / "settings.json", [pi_config.MIRROR_GIT_SOURCE])
    monkeypatch.setenv("PI_SESSION_ID", "sess-abc")
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(tmp_path / "no-tap-here"))

    rows = doctor._pi_capture_rows()

    session_rows = [row for row in rows if "Capture (this session)" in row]
    assert len(session_rows) == 1
    assert "not installed" in session_rows[0]
    assert any(reason in session_rows[0] for reason in capture_state.REASONS)


def test_a_machine_with_no_pi_install_says_nothing(pi_agent):
    _write(pi_agent / "settings.json", [])
    assert doctor._pi_capture_rows() == []


def test_the_report_carries_the_filter_row(pi_agent):
    """End to end through `render`, where a person actually reads it."""
    from probe.cli.capabilities import Capabilities

    _write(
        pi_agent / "settings.json",
        [{"source": pi_config.MIRROR_GIT_SOURCE, "extensions": []}],
    )
    report = doctor.render(Capabilities(agent_source="pi"))
    assert "filtered out" in report
    # The honest not-tracked line stays: it answers a different question.
    assert "not tracked by doctor" in report
