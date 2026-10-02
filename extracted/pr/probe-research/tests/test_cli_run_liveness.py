"""0205 at the CLI surface: who owns a run, and what a launcher is.

`probe exec` is the honest wrapper -- it opens the run, beats while the child
lives, hands the child its identity, and closes from the real exit code. The
distinction these tests protect is BLOCKING vs SUBMIT: wrapping `sbatch` would
record the scheduler's acceptance as the job's exit code, which is the precise
lie that makes a green run mean nothing.
"""

from __future__ import annotations

import sys

import pytest

from probe import cli
from probe.cli.main import _forwarding_hint, _is_submit_launcher, _launcher_name
from tests.conftest import make_client


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"])
    return app


class TestLauncherDetection:
    """Two questions, and conflating them throws away a real exit code.

    WHICH launcher is this (matching argv[0] alone misses `python -m modal run`,
    `uv run modal run`, `uvx modal run` -- exactly the forms people write), and
    does it BLOCK or SUBMIT. The second is a subcommand distinction: `modal run`
    waits for the job, `modal deploy` returns once the app is published.
    """

    @pytest.mark.parametrize(
        "argv",
        [
            ["modal", "run", "train.py"],
            ["python", "-m", "modal", "run", "train.py"],
            ["python3", "-m", "modal", "run", "train.py"],
            ["uv", "run", "modal", "run", "train.py"],
            ["uvx", "modal", "run", "train.py"],
            ["/opt/homebrew/bin/modal", "run", "train.py"],
        ],
    )
    def test_modal_is_recognised_through_every_wrapper(self, argv) -> None:
        assert _launcher_name(argv) == "modal"

    def test_modal_run_blocks_and_modal_deploy_does_not(self) -> None:
        """The distinction finding 6 was about. `modal run` waits for the job,
        so wrapping it is honest; `modal deploy` returns on publish, so wrapping
        it would record the publish as the training's exit code."""
        assert _is_submit_launcher(["modal", "run", "train.py"]) is False
        assert _forwarding_hint(["modal", "run", "train.py"], "RID", 1) is None

        assert _is_submit_launcher(["modal", "deploy", "app.py"]) is True
        hint = _forwarding_hint(["uv", "run", "modal", "deploy", "app.py"], "RID", 3)
        assert hint and "modal.Secret.from_dict" in hint
        assert "RID" in hint and '"3"' in hint

    def test_a_blocking_launcher_gets_no_hint_and_is_not_a_handoff(self) -> None:
        argv = ["python", "train.py"]
        assert _launcher_name(argv) == "python"
        assert _forwarding_hint(argv, "RID", 1) is None
        assert _is_submit_launcher(argv) is False

    @pytest.mark.parametrize(
        "argv",
        [
            ["sbatch", "job.sh"],
            ["ray", "job", "submit", "--", "python", "train.py"],
            ["kubectl", "apply", "-f", "job.yaml"],
        ],
    )
    def test_submit_launchers_are_flagged(self, argv) -> None:
        assert _is_submit_launcher(argv) is True
        assert _forwarding_hint(argv, "RID", 1) is not None

    def test_a_bare_ray_or_kubectl_is_not_assumed_to_submit(self) -> None:
        """Only the submitting SUBCOMMANDS hand off. `ray status` and `kubectl
        logs` are ordinary blocking commands."""
        assert _is_submit_launcher(["ray", "status"]) is False
        assert _is_submit_launcher(["kubectl", "logs", "pod"]) is False

    def test_an_unknown_launcher_is_never_blocked_by_the_hint(self) -> None:
        """Advisory, never a gate: an unrecognised command still runs."""
        assert _forwarding_hint(["my-custom-launcher", "go"], "RID", 1) is None
        assert _is_submit_launcher(["my-custom-launcher", "go"]) is False


class TestExecOpensAndOwns:
    def test_exec_can_open_the_run_itself(self, wired, capsys) -> None:
        """Before 0205 `exec` REQUIRED a run someone had already opened -- and
        the only way to open one was the detached create this release is
        retiring."""
        rc = cli.main(
            ["exec", "--project", "p", "--experiment", "e", "--name", "wrapped-run",
             "--", sys.executable, "-c", "pass"]
        )
        assert rc == 0
        opened = [r for r in wired.runs.values() if r["name"] == "wrapped-run"]
        assert len(opened) == 1, "exec must open exactly one run"
        row = opened[0]
        assert row["liveness_mode"] == "wrapped"
        assert row["last_heartbeat_at"] is not None, "a wrapped run is owned at insert"

    def test_the_child_is_handed_the_run_identity(self, wired, tmp_path) -> None:
        """The whole handshake in one assertion: what the child sees is what
        `probe.init()` needs to join the SAME run."""
        out = tmp_path / "seen.txt"
        rc = cli.main(
            ["exec", "--project", "p", "--experiment", "e", "--name", "handshake",
             "--", sys.executable, "-c",
             f"import os,pathlib;pathlib.Path({str(out)!r}).write_text("
             "os.environ['PROBE_RUN_ID']+' '+os.environ['PROBE_RUN_EPOCH'])"]
        )
        assert rc == 0
        run_id, epoch = out.read_text().split()
        assert run_id in wired.runs
        assert epoch == str(wired.runs[run_id].get("write_epoch", 1))

    def test_the_child_exit_code_becomes_the_run_status(self, wired) -> None:
        rc = cli.main(
            ["exec", "--project", "p", "--experiment", "e", "--name", "failing",
             "--", sys.executable, "-c", "raise SystemExit(3)"]
        )
        assert rc == 3, "the wrapper must hand back the child's exit code"
        row = next(r for r in wired.runs.values() if r["name"] == "failing")
        assert row["status"] == "failed"

    def test_exec_can_open_a_retry_of_an_existing_run(self, wired, capsys) -> None:
        """`run child` is the verb being retired, and it was the only CLI way
        to say "this run re-attempts that one". The honest wrapper has to be
        able to say it too, or parentage dies with the deprecated command."""
        cli.main(["run", "start", "--experiment", "e", "--name", "first-try"])
        parent = capsys.readouterr().out.strip().splitlines()[-1]
        rc = cli.main(
            ["exec", "--project", "p", "--experiment", "e", "--parent", parent,
             "--relation", "retry", "--", sys.executable, "-c", "pass"]
        )
        assert rc == 0
        child = next(r for r in wired.runs.values() if r.get("parent_run_id") == parent)
        assert child["parent_relation"] == "retry"
        assert child["name_customized"] is False, "exec never fabricates a name"
        assert child["liveness_mode"] == "wrapped"

    def test_exec_refuses_half_a_parentage(self, wired) -> None:
        """A parent with no relation would be stored under a guessed word."""
        rc = cli.main(
            ["exec", "--project", "p", "--experiment", "e", "--relation", "retry",
             "--", sys.executable, "-c", "pass"]
        )
        assert rc != 0
        assert not [r for r in wired.runs.values() if r.get("parent_relation")]

    def test_a_submit_launcher_hands_the_run_over_instead_of_wrapping_it(
        self, wired, monkeypatch
    ) -> None:
        """`sbatch` returns when the scheduler accepts the job. Wrapping it would
        mark the run completed, exit 0, while the work had not started."""
        rc = cli.main(
            ["exec", "--project", "p", "--experiment", "e", "--name", "queued",
             "--detached-launcher", "--", sys.executable, "-c", "pass"]
        )
        assert rc == 0
        row = next(r for r in wired.runs.values() if r["name"] == "queued")
        assert row["status"] == "created", "a hand-off is not a completed run"
        assert row["liveness_mode"] is None, "nothing owns it yet"
        assert row.get("last_heartbeat_at") is None


class TestDeprecationWarnings:
    """This release warns; the next refuses. Nobody's script breaks on the
    release that tells them."""

    def test_bare_run_start_warns_and_still_works(self, wired, capsys) -> None:
        rc = cli.main(["run", "start", "--experiment", "e", "--name", "r1"])
        captured = capsys.readouterr()
        assert rc == 0, "the deprecation release must not break existing scripts"
        assert captured.out.strip().splitlines()[-1] in wired.runs
        assert "nothing owns" in captured.err
        assert "probe exec" in captured.err
        assert "refused in the next release" in captured.err

    def test_run_child_warns_too(self, wired, capsys) -> None:
        cli.main(["run", "start", "--experiment", "e", "--name", "parent"])
        parent = capsys.readouterr().out.strip().splitlines()[-1]
        rc = cli.main(["run", "child", parent, "--name", "kid", "--relation", "fork"])
        assert rc == 0
        assert "nothing owns" in capsys.readouterr().err

    def test_run_child_needs_no_name(self, wired, capsys) -> None:
        """`--name` was required here long after `run start` stopped requiring
        it, so every retry was hand-named -- `attempt-2` -- and stamped
        name_customized, locked out of the title the server writes for every
        other run. Omitted, the request carries no name and the server mints."""
        cli.main(["run", "start", "--experiment", "e", "--name", "parent"])
        parent = capsys.readouterr().out.strip().splitlines()[-1]
        rc = cli.main(["run", "child", parent, "--relation", "retry"])
        assert rc == 0
        child = next(r for r in wired.runs.values() if r.get("parent_run_id") == parent)
        assert child["name_customized"] is False, (
            "a fabricated name stamps the flag and locks the run out of titling"
        )
        assert child["name"] == child["slug"], "an unnamed run reads as its petname"
        assert child["parent_relation"] == "retry"
