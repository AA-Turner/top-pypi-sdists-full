"""Per-run tokens on the client (~/plans/per-run-token): what `probe exec` hands a
remote job, `probe run token`, how `probe.init()` joins the run a token records,
and that every scrubber hides one.

The server half (minting, the route list, the expiry alert) is research-os's
tests/integration/test_run_token_isolation.py and test_run_token_sdk_e2e.py.
"""

from __future__ import annotations

import base64
import json
import sys
import uuid
from types import SimpleNamespace

import pytest
import typer

from probe import cli
from probe.cli.main import _forwarding_hint, _parse_duration
from probe.sdk import errors, fluent
from probe.sdk.client import Client
from probe.sdk.config import env_run_id, run_token_run_id
from tests.conftest import make_client


def _token(rid: str) -> str:
    """A run token's shape: the client reads `rid` and never verifies."""

    def seg(obj: dict) -> str:
        return base64.urlsafe_b64encode(json.dumps(obj).encode()).rstrip(b"=").decode()

    claims = {"aud": "research-os:run", "sub": "cust", "uid": str(uuid.uuid4()), "rid": rid,
              "gen": 1, "mem": 1, "scopes": ["read", "write"], "jti": uuid.uuid4().hex,
              "iat": 1, "exp": 2}
    return f"probe_run_{seg({'alg': 'ES256', 'kid': 'k', 'typ': 'JWT'})}.{seg(claims)}.{'s' * 86}"


@pytest.mark.parametrize(
    ("text", "seconds"),
    [("36h", 129600), ("7d", 604800), ("2w", 1209600), ("90m", 5400), ("3600s", 3600),
     ("60", 60), (" 7D ", 604800)],
)
def test_a_duration_reads_as_seconds(text, seconds):
    assert _parse_duration(text) == seconds


@pytest.mark.parametrize("text", ["", "abc", "0", "0d", "-5", "7y", "1.5h"])
def test_a_bad_duration_is_refused(text):
    with pytest.raises(typer.BadParameter):
        _parse_duration(text)


def test_the_run_is_read_from_a_run_token_and_from_nothing_else():
    rid = str(uuid.uuid4())
    assert run_token_run_id(_token(rid)) == rid
    assert run_token_run_id("probe_pat_" + "0" * 32) is None
    assert run_token_run_id("probe_run_not.a.jwt") is None
    assert run_token_run_id(None) is None


class TestAJobJoinsTheRunItsTokenRecords:
    def _client(self):
        return SimpleNamespace(settings=SimpleNamespace(token=None))

    def test_a_job_given_only_the_token_attaches_to_its_run(self, monkeypatch):
        rid = str(uuid.uuid4())
        monkeypatch.setenv("PROBE_TOKEN", _token(rid))
        monkeypatch.delenv("PROBE_RUN_ID", raising=False)
        assert fluent._adopt_run_token("", self._client()) == rid
        import os

        # Exported only once attached (`_attach_from_env`), never before.
        assert "PROBE_RUN_ID" not in os.environ

    def test_another_runs_id_is_refused_before_any_write(self, monkeypatch):
        monkeypatch.setenv("PROBE_TOKEN", _token(str(uuid.uuid4())))
        with pytest.raises(errors.ValidationError, match="records that run only"):
            fluent._adopt_run_token(str(uuid.uuid4()), self._client())

    def test_its_own_id_and_a_slug_pass_through(self, monkeypatch):
        rid = str(uuid.uuid4())
        monkeypatch.setenv("PROBE_TOKEN", _token(rid))
        assert fluent._adopt_run_token(rid.upper(), self._client()) == rid.upper()
        assert fluent._adopt_run_token("brave-otter-12", self._client()) == "brave-otter-12"

    def test_a_token_only_attach_exports_the_run_once_and_never_as_the_users_choice(self, monkeypatch):
        import os

        rid, other = str(uuid.uuid4()), str(uuid.uuid4())
        monkeypatch.setenv("PROBE_RUN_ID", "restore-me")
        monkeypatch.delenv("PROBE_RUN_ID")
        monkeypatch.setattr(fluent, "_EXPORTED_RUN_ID", None)
        attached: list[str] = []

        class FakeClient:
            settings = SimpleNamespace(token=_token(rid))

            def attach_run(self, run_id, **_kw):
                attached.append(run_id)
                return SimpleNamespace(id=run_id, slug="brave-otter-12")

        fluent._attach_from_env(FakeClient(), {})
        assert attached == [rid] and os.environ["PROBE_RUN_ID"] == rid
        # A later init() under another run's token reads that export as its own.
        FakeClient.settings = SimpleNamespace(token=_token(other))
        assert fluent._adopt_run_token(os.environ["PROBE_RUN_ID"], FakeClient()) == other
        with pytest.raises(errors.ValidationError, match="per-run token"):
            fluent._attach_from_env(FakeClient(), {"experiment": "e"})

    def test_any_other_credential_leaves_the_run_alone(self, monkeypatch):
        monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "0" * 32)
        monkeypatch.delenv("PROBE_RUN_ID", raising=False)
        assert fluent._adopt_run_token("", self._client()) == ""

    def test_the_clients_own_credential_wins_over_the_environments(self, monkeypatch):
        monkeypatch.setenv("PROBE_TOKEN", _token(str(uuid.uuid4())))
        client = SimpleNamespace(settings=SimpleNamespace(token="probe_pat_" + "0" * 32))
        assert fluent._adopt_run_token("", client) == ""

    def test_integrations_see_the_tokens_run_as_chosen_by_a_launcher(self, monkeypatch):
        rid = str(uuid.uuid4())
        monkeypatch.delenv("PROBE_RUN_ID", raising=False)
        monkeypatch.setenv("PROBE_TOKEN", _token(rid))
        assert env_run_id() == rid
        monkeypatch.setenv("PROBE_RUN_ID", "named")
        assert env_run_id() == "named"
        monkeypatch.delenv("PROBE_RUN_ID")
        monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "0" * 32)
        assert env_run_id() == ""


def test_the_modal_hint_carries_the_token_once_one_was_minted():
    argv = ["modal", "deploy", "app.py"]
    minted = _forwarding_hint(argv, "RID", 3, token_minted=True)
    # Read from the launcher's environment, locally only: never a pasted literal.
    assert minted and '"PROBE_TOKEN"' in minted and "from_local_environ" in minted
    assert "from_name" not in minted
    # Ray's driver runs on the head node, without the launcher's environment.
    ray = _forwarding_hint(["ray", "job", "submit", "--", "python", "t.py"], "RID", 3, token_minted=True)
    assert ray and "<the PROBE_TOKEN above>" in ray and '"RID"' in ray and '"3"' in ray
    assert "from_name" in (_forwarding_hint(argv, "RID", 3) or "")
    for other in (["sbatch", "job.sh"], ["ray", "job", "submit", "--", "python", "t.py"],
                  ["kubectl", "apply", "-f", "job.yaml"]):
        assert "PROBE_TOKEN" in (_forwarding_hint(other, "RID", 3, token_minted=True) or ""), other


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"])
    return app


@pytest.fixture
def server_tokens(monkeypatch):
    """The four token routes, as the server answers them."""
    calls: list[tuple] = []
    rid = str(uuid.uuid4())

    def mint(self, run_id, *, ttl_seconds=None):
        calls.append(("mint", run_id, ttl_seconds))
        return {"token": _token(rid), "run_id": rid, "expires_at": "2026-11-02T10:00:00+00:00",
                "ttl_seconds": ttl_seconds or 2592000, "gen": 1}

    def extend(self, run_id, *, ttl_seconds):
        calls.append(("extend", run_id, ttl_seconds))
        return {"run_id": rid, "expires_at": "2026-11-09T10:00:00+00:00", "ttl_seconds": ttl_seconds,
                "gen": 1}

    monkeypatch.setattr(Client, "mint_run_token", mint)
    monkeypatch.setattr(Client, "extend_run_tokens", extend)
    return calls


class TestProbeRunToken:
    def test_the_token_goes_to_stdout_alone(self, wired, server_tokens, capsys):
        assert cli.main(["run", "token", "brave-otter-12", "--ttl", "36h"]) == 0
        out = capsys.readouterr()
        assert out.out.strip().startswith("probe_run_") and len(out.out.strip().splitlines()) == 1
        assert "records this run only" in out.err
        assert server_tokens == [("mint", "brave-otter-12", 129600)]

    def test_extend_moves_the_expiry_and_prints_no_token(self, wired, server_tokens, capsys):
        assert cli.main(["run", "token", "brave-otter-12", "--extend", "7d"]) == 0
        out = capsys.readouterr()
        assert "probe_run_" not in out.out + out.err and "2026-11-09 10:00 UTC" in out.err
        assert server_tokens == [("extend", "brave-otter-12", 604800)]

    def test_two_actions_at_once_are_refused(self, wired, server_tokens):
        assert cli.main(["run", "token", "brave-otter-12", "--extend", "7d", "--revoke-all"]) != 0
        assert server_tokens == []


_SHOW_TOKEN = "import os; print('CHILD_TOKEN=' + os.environ.get('PROBE_TOKEN', '')[:10])"


class TestTheHandOffHandsTheJobItsToken:
    def _handoff(self, *extra, code="pass"):
        return cli.main(["exec", "--project", "p", "--experiment", "e", "--detached-launcher", *extra,
                         "--", sys.executable, "-c", code])

    def test_the_launcher_runs_with_the_runs_token_not_the_researchers(
        self, wired, server_tokens, capfd, monkeypatch
    ):
        monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "a" * 32)
        assert self._handoff(code=_SHOW_TOKEN) == 0
        assert "CHILD_TOKEN=probe_run_" in capfd.readouterr().out

    def test_a_blocking_launcher_given_a_ttl_runs_with_the_runs_token(
        self, wired, server_tokens, capfd, monkeypatch
    ):
        monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "a" * 32)
        rc = cli.main(["exec", "--project", "p", "--experiment", "e", "--name", "blocking",
                       "--token-ttl", "1d", "--", sys.executable, "-c", _SHOW_TOKEN])
        out = capfd.readouterr()
        assert rc == 0 and "CHILD_TOKEN=probe_run_" in out.out
        assert server_tokens[0][2] == 86400
        row = next(r for r in wired.runs.values() if r["name"] == "blocking")
        assert row["status"] == "completed", "the wrapper still records the exit code"

    def test_a_bad_ttl_is_refused_before_any_run_opens(self, wired, server_tokens):
        before = len(wired.runs)
        assert self._handoff("--token-ttl", "7y") != 0
        assert len(wired.runs) == before and server_tokens == []

    def test_the_job_gets_a_token_for_this_run_with_the_life_asked_for(
        self, wired, server_tokens, capsys
    ):
        assert self._handoff("--token-ttl", "2d") == 0
        err = capsys.readouterr().err
        assert "PROBE_TOKEN=probe_run_" in err and "from your secret store" not in err
        assert "--extend 7d" in err and "default 30 days" not in err
        assert server_tokens[0][0] == "mint" and server_tokens[0][2] == 172800

    def test_without_a_ttl_it_says_the_default_and_how_to_set_one(self, wired, server_tokens, capsys):
        assert self._handoff() == 0
        err = capsys.readouterr().err
        assert "default 30 days" in err and "--token-ttl" in err

    @pytest.mark.parametrize(
        ("status", "detail", "child"),
        [(404, "Not Found", "probe_pat_"),  # an older server: the old hand-off, unchanged
         (500, "boom", "")],  # a failed mint: fail closed, never the researcher's key
    )
    def test_the_launcher_never_gets_the_researchers_key_when_a_mint_fails(
        self, wired, capfd, monkeypatch, status, detail, child
    ):
        def mint(self, run_id, *, ttl_seconds=None):
            raise errors.error_for(status, detail)

        monkeypatch.setattr(Client, "mint_run_token", mint)
        monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "a" * 32)
        assert self._handoff(code=_SHOW_TOKEN) == 0
        assert f"CHILD_TOKEN={child}\n" in capfd.readouterr().out

    @pytest.mark.parametrize(
        ("detail", "predates"), [("Not Found", True), ("run not found", False)]
    )
    def test_a_server_without_per_run_tokens_keeps_the_old_hand_off(
        self, wired, capsys, monkeypatch, detail, predates
    ):
        # An older server has no token route: FastAPI's bare `Not Found`. Any
        # other 404 is not a reason to send the agent for an account-wide key.
        def mint(self, run_id, *, ttl_seconds=None):
            raise errors.error_for(404, detail)

        monkeypatch.setattr(Client, "mint_run_token", mint)
        assert self._handoff() == 0
        err = capsys.readouterr().err
        assert "PROBE_TOKEN from your secret store" in err and "probe_run_" not in err
        assert ("predates per-run tokens" in err) is predates


def test_every_scrubber_hides_a_run_token():
    from probe.sdk.logstream import redact as log_redact
    from probe.tap_core.secrets import redact

    token = _token(str(uuid.uuid4()))
    for text in (token, f"PROBE_TOKEN={token}", repr({"PROBE_TOKEN": token}),
                 f"export PROBE_TOKEN='{token}'"):
        cleaned, _ = redact(text)
        assert token not in cleaned, text
        assert token not in log_redact(text), text
