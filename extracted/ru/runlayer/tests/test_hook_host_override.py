"""Hook host precedence on managed devices (ENG-6620).

The ``aiwatch`` runtime already resolves host from MDM only. The full
``runlayer`` CLI hook path (``runlayer hook``, ``python -m runlayer_cli.hook``)
reads ``~/.runlayer/config.yaml``, so a user ``default_host`` must not redirect
hook traffic away from the MDM host — nor carry the MDM org key there.
"""

from __future__ import annotations

import io
import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from runlayer_cli import config as config_module, flow_spool, flow_trace
from runlayer_cli.config import Config, hosts_equal, url_to_host_key
from runlayer_cli.hook import (
    credential_state,
    dispatch as hook_dispatch,
    hook_io,
    host_override,
    messages,
    relay,
    transcript_stream,
)
from runlayer_cli.hook.clients import Client, HookResponse
from runlayer_cli.mdm_config import AIWatchMode
from runlayer_cli.runtime import mark_aiwatch_runtime

MANAGED_HOST = "https://prod.example.com"
USER_HOST = "https://staging.example.com"
ORG_KEY = "rl_org_managed"
USER_SECRET = "rl_user_stale"

_PRE_TOOL = {
    "hook_event_name": "PreToolUse",
    "tool_name": "Edit",
    "tool_input": {"file_path": "/tmp/x"},
    "session_id": "sess-host",
}


@pytest.fixture
def config_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "config.yaml"
    monkeypatch.setattr(config_module, "get_config_path", lambda: path)
    return path


@pytest.fixture
def state_dir(isolated_credential_state: Path) -> Path:
    return isolated_credential_state / "state"


def _write_yaml(path: Path, default_host: str, *, secret: str | None = None) -> None:
    host: dict[str, str] = {"url": default_host}
    if secret:
        host["secret"] = secret
    path.write_text(
        yaml.safe_dump(
            {
                "default_host": default_host,
                "hosts": {url_to_host_key(default_host): host},
            }
        )
    )


def _marker(state_dir: Path) -> dict | None:
    path = state_dir / "hook_host_override.json"
    return json.loads(path.read_text()) if path.exists() else None


def _load(managed: dict) -> tuple[str, str]:
    with patch.object(relay, "read_managed_config", return_value=managed):
        return relay._load_credentials_uncached()


class TestPrecedence:
    def test_full_cli_hook_uses_mdm_host_over_user_default_host(
        self, config_file: Path, state_dir: Path
    ):
        """Managed device + user ``default_host`` on another host: hooks still
        go to the MDM host with the org key (never the org key to the user host)."""
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)

        host, secret = _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})

        assert (host, secret) == (MANAGED_HOST, ORG_KEY)
        marker = _marker(state_dir)
        assert marker is not None
        assert marker["user_host"] == USER_HOST
        assert marker["managed_host"] == MANAGED_HOST
        assert marker["at"] == pytest.approx(time.time(), abs=5)

    def test_managed_host_wins_even_without_org_key(self, config_file: Path):
        """No org key: the managed host still wins; the user's secret is not
        for that host, so the relay falls through to enrollment."""
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        with (
            patch.object(
                relay, "read_managed_config", return_value={"host": MANAGED_HOST}
            ),
            patch.object(relay, "_try_lazy_enrollment", return_value=None) as enroll,
        ):
            with pytest.raises(relay.RelayError):
                relay._load_credentials_uncached()
        enroll.assert_called_once()
        assert enroll.call_args.args[0] == MANAGED_HOST

    def test_org_key_never_released_without_managed_host(self, config_file: Path):
        """An org key with no MDM host (malformed profile) is not a licence to
        send it to whatever host the user logged into."""
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)

        host, secret = _load({"org_api_key": ORG_KEY})

        assert (host, secret) == (USER_HOST, USER_SECRET)

    @pytest.mark.parametrize(
        ("managed", "org_key_mode"),
        [
            ({"host": MANAGED_HOST, "org_api_key": ORG_KEY}, True),
            ({"org_api_key": ORG_KEY}, False),
            ({"host": MANAGED_HOST}, False),
            ({}, False),
        ],
    )
    def test_org_key_mode_detectors_follow_release_rule(
        self, monkeypatch, managed: dict, org_key_mode: bool
    ):
        """The 401 copy and the ``device`` block must describe the credential
        actually sent: org-key mode iff the key would be released."""
        monkeypatch.setattr(relay, "read_managed_config", lambda: dict(managed))
        monkeypatch.setattr(relay, "_build_device_context", lambda: {"device_id": "d"})

        assert relay.uses_managed_credential() is org_key_mode
        attached = "device" in json.loads(relay._maybe_attach_device('{"a":1}'))
        assert attached is org_key_mode

    def test_unmanaged_device_unchanged(self, config_file: Path, state_dir: Path):
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)

        host, secret = _load({})

        assert (host, secret) == (USER_HOST, USER_SECRET)
        assert _marker(state_dir) is None

    def test_same_host_is_not_a_deviation(self, config_file: Path, state_dir: Path):
        _write_yaml(config_file, MANAGED_HOST + "/", secret=USER_SECRET)

        host, secret = _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})

        assert (host, secret) == (MANAGED_HOST, ORG_KEY)
        assert _marker(state_dir) is None

    def test_no_host_anywhere_raises(self, config_file: Path):
        with pytest.raises(relay.RelayError) as exc:
            _load({})
        assert exc.value.exit_code == 1


class TestManagedSourceProvenance:
    """Through the real plist readers: ``read_managed_config`` merges the
    ``com.runlayer.cli`` and ``com.runlayer.aiwatch`` domains field by field,
    so a CLI-domain ``Host`` must not end up paired with the AI Watch-domain
    org key. The relay would otherwise post the prod key to the other host
    and the host-match gate could not tell (the merged dict already carries
    the other host)."""

    OTHER_HOST = "https://other.example.com"

    @pytest.fixture
    def plists(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        from runlayer_cli import mdm_config, runtime

        cli_plist = tmp_path / "cli.plist"
        aiwatch_plist = tmp_path / "aiwatch.plist"
        monkeypatch.setattr(mdm_config.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(mdm_config, "CLI_MACOS_PLIST_PATHS", (cli_plist,))
        monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (aiwatch_plist,))
        monkeypatch.setattr(runtime, "is_aiwatch_runtime", lambda: False)
        monkeypatch.setattr(mdm_config, "read_backend_config", lambda _key: None)
        return cli_plist, aiwatch_plist

    @staticmethod
    def _write(path: Path, payload: dict) -> None:
        import plistlib

        path.write_bytes(plistlib.dumps(payload))

    @pytest.mark.parametrize("default_host", [None, MANAGED_HOST])
    def test_cli_domain_host_never_carries_aiwatch_org_key(
        self, config_file: Path, plists, default_host: str | None
    ):
        cli_plist, aiwatch_plist = plists
        self._write(cli_plist, {"Host": self.OTHER_HOST})
        self._write(aiwatch_plist, {"Host": MANAGED_HOST, "OrgApiKey": ORG_KEY})
        if default_host:
            _write_yaml(config_file, default_host, secret=USER_SECRET)

        with patch.object(relay, "_try_lazy_enrollment", return_value=None):
            with pytest.raises(relay.RelayError) as exc:
                relay._load_credentials_uncached()

        # The other host wins the merge but has no credential: nothing is sent.
        assert "no secret" in str(exc.value)

    def test_same_host_across_domains_releases_key(self, config_file: Path, plists):
        cli_plist, aiwatch_plist = plists
        self._write(cli_plist, {"Host": MANAGED_HOST + "/"})
        self._write(aiwatch_plist, {"Host": MANAGED_HOST, "OrgApiKey": ORG_KEY})
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)

        assert relay._load_credentials_uncached() == (MANAGED_HOST, ORG_KEY)


def _poster(monkeypatch, managed: dict) -> transcript_stream._HTTPEventPoster:
    """Build the transcript-stream poster against a stub HTTP client so the
    only observable is which host + key it was constructed with."""

    class _Client:
        def close(self):
            pass

    monkeypatch.setattr(transcript_stream, "http_client", lambda: _Client())
    monkeypatch.setattr(transcript_stream, "read_managed_config", lambda: dict(managed))
    monkeypatch.setattr(relay, "read_managed_config", lambda: dict(managed))
    return transcript_stream._HTTPEventPoster(debug=False)


class TestTranscriptStreamPrecedence:
    """The live transcript poster resolves host + key like the relay, so one
    session never splits across two hosts (events to the login host, backlog
    flush to the managed host)."""

    def test_poster_uses_mdm_host_and_org_key_over_user_default_host(
        self, config_file: Path, monkeypatch
    ):
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)

        poster = _poster(monkeypatch, {"host": MANAGED_HOST, "org_api_key": ORG_KEY})

        assert poster._hook_client.base_url == MANAGED_HOST
        assert poster._base_headers[transcript_stream.API_KEY_HEADER_NAME] == ORG_KEY
        assert poster._org_key_mode is True

    def test_poster_never_releases_org_key_without_managed_host(
        self, config_file: Path, monkeypatch
    ):
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)

        poster = _poster(monkeypatch, {"org_api_key": ORG_KEY})

        assert poster._hook_client.base_url == USER_HOST
        assert (
            poster._base_headers[transcript_stream.API_KEY_HEADER_NAME] == USER_SECRET
        )
        assert poster._org_key_mode is False

    def test_poster_unmanaged_device_unchanged(self, config_file: Path, monkeypatch):
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)

        poster = _poster(monkeypatch, {})

        assert poster._hook_client.base_url == USER_HOST
        assert (
            poster._base_headers[transcript_stream.API_KEY_HEADER_NAME] == USER_SECRET
        )


class TestHostsEqual:
    """``hosts_equal`` is the case-insensitive host-identity comparison backing
    the managed-host deviation check. It must match the keychain's notion of the
    same host (``url_to_host_key``) while still flagging a scheme or
    non-default-port deviation.
    """

    @pytest.mark.parametrize(
        ("left", "right", "expected"),
        [
            # The bug: a pure case variant of the same backend is the same host.
            ("https://Prod.Example.com", "https://prod.example.com", True),
            ("https://prod.example.com", "https://Prod.Example.com", True),
            ("HTTPS://PROD.EXAMPLE.COM", "https://prod.example.com", True),
            # Trailing slash, with and without case differences.
            ("https://prod.example.com/", "https://prod.example.com", True),
            ("https://Prod.Example.com/", "https://prod.example.com", True),
            # Identical.
            ("https://prod.example.com", "https://prod.example.com", True),
            # Explicit scheme-default port equals no port.
            ("https://prod.example.com:443", "https://prod.example.com", True),
            ("http://prod.example.com:80", "http://prod.example.com", True),
            # Scheme is case-insensitive too.
            ("HTTPS://prod.example.com", "https://prod.example.com", True),
            # Different host is a real deviation.
            ("https://prod.example.com", "https://staging.example.com", False),
            ("https://prod.example.com", "https://app.runlayer.com", False),
            # Non-default port is a real deviation.
            ("https://prod.example.com", "https://prod.example.com:8443", False),
            ("https://prod.example.com:8443", "https://prod.example.com:9443", False),
            # Scheme deviation (http vs https) is a real deviation.
            ("https://prod.example.com", "http://prod.example.com", False),
        ],
    )
    def test_hosts_equal(self, left: str, right: str, expected: bool) -> None:
        assert hosts_equal(left, right) is expected


class TestResolve:
    def test_resolve_normalizes_both_sides(self):
        resolved = host_override.resolve_hook_host(
            Config(default_host=USER_HOST + "/"), {"host": MANAGED_HOST + "/"}
        )
        assert resolved == {
            "host": MANAGED_HOST,
            "managed_host": MANAGED_HOST,
            "user_host": USER_HOST,
            "overridden": True,
        }

    def test_resolve_unmanaged(self):
        resolved = host_override.resolve_hook_host(Config(default_host=USER_HOST), {})
        assert resolved["host"] == USER_HOST
        assert resolved["overridden"] is False

    def test_resolve_case_variant_host_is_not_a_deviation(self):
        """A default_host whose only difference from the MDM host is alphabetic
        case is not a deviation: ``overridden`` is False. The resolved ``host``
        is still the managed host, and ``user_host`` preserves the user's case
        verbatim — only the comparison is case-insensitive."""
        resolved = host_override.resolve_hook_host(
            Config(default_host="https://Prod.Example.com"),
            {"host": "https://prod.example.com"},
        )
        assert resolved == {
            "host": "https://prod.example.com",
            "managed_host": "https://prod.example.com",
            "user_host": "https://Prod.Example.com",
            "overridden": False,
        }


class TestMarker:
    def test_clear_on_convergence(self, config_file: Path, state_dir: Path):
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})
        assert _marker(state_dir) is not None

        _write_yaml(config_file, MANAGED_HOST, secret=USER_SECRET)
        _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})
        assert _marker(state_dir) is None

    def test_case_variant_default_host_writes_no_marker(
        self, config_file: Path, state_dir: Path
    ):
        """A default_host whose only difference from the MDM host is alphabetic
        case is not a deviation, so the marker is never written and hooks still
        authenticate with the managed org key."""
        _write_yaml(config_file, "https://Prod.Example.com", secret=USER_SECRET)

        host, secret = _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})

        assert (host, secret) == (MANAGED_HOST, ORG_KEY)
        assert _marker(state_dir) is None

    def test_case_variant_convergence_clears_marker(
        self, config_file: Path, state_dir: Path
    ):
        """Self-heal: switching default_host from a genuinely different host to
        a case variant of the managed host clears the marker within one load."""
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})
        assert _marker(state_dir) is not None

        _write_yaml(config_file, "https://Prod.Example.com", secret=USER_SECRET)
        host, secret = _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})

        assert (host, secret) == (MANAGED_HOST, ORG_KEY)
        assert _marker(state_dir) is None

    def test_unchanged_marker_not_rewritten_within_an_hour(
        self, config_file: Path, state_dir: Path, monkeypatch
    ):
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        monkeypatch.setattr(time, "time", lambda: 1_000_000.0)
        _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})
        monkeypatch.setattr(time, "time", lambda: 1_000_000.0 + 600)
        _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})
        assert _marker(state_dir)["at"] == 1_000_000.0

        monkeypatch.setattr(time, "time", lambda: 1_000_000.0 + 3601)
        _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})
        assert _marker(state_dir)["at"] == 1_000_000.0 + 3601

    def test_read_marker_shape_and_staleness(self, config_file: Path, monkeypatch):
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        monkeypatch.setattr(time, "time", lambda: 1_700_000_000.0)
        _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})

        assert host_override.read_marker() == {
            "user_host": USER_HOST,
            "managed_host": MANAGED_HOST,
            "last_seen_at": "2023-11-14T22:13:20+00:00",
        }
        monkeypatch.setattr(
            time,
            "time",
            lambda: 1_700_000_000.0 + host_override.MARKER_MAX_AGE_S + 1,
        )
        assert host_override.read_marker() is None

    def test_read_marker_tolerates_garbage(self, state_dir: Path):
        state_dir.mkdir(parents=True)
        (state_dir / "hook_host_override.json").write_text("{not json")
        assert host_override.read_marker() is None

    @pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlink semantics")
    def test_read_marker_refuses_symlink(self, tmp_path: Path, state_dir: Path):
        target = tmp_path / "elsewhere.json"
        target.write_text(
            json.dumps(
                {
                    "at": time.time(),
                    "user_host": USER_HOST,
                    "managed_host": MANAGED_HOST,
                }
            )
        )
        state_dir.mkdir(parents=True)
        (state_dir / "hook_host_override.json").symlink_to(target)
        assert host_override.read_marker() is None

    @pytest.mark.skipif(sys.platform == "win32", reason="POSIX FIFO semantics")
    def test_read_marker_refuses_fifo_without_blocking(self, state_dir: Path):
        """A FIFO planted at the marker path must not park the hook (or a
        scan) in ``open`` waiting for a writer."""
        state_dir.mkdir(parents=True)
        os.mkfifo(state_dir / "hook_host_override.json")
        assert host_override.read_marker() is None
        assert host_override.current() is None

    def test_aiwatch_runtime_never_writes_or_clears(
        self, config_file: Path, state_dir: Path
    ):
        """aiwatch cannot see the YAML, so it must not erase what a full-CLI
        hook recorded — nor record anything itself."""
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})
        before = _marker(state_dir)
        assert before is not None

        mark_aiwatch_runtime()
        with patch.object(
            config_module, "read_managed_config", return_value={"host": MANAGED_HOST}
        ):
            host, secret = _load({"host": MANAGED_HOST, "org_api_key": ORG_KEY})
        assert (host, secret) == (MANAGED_HOST, ORG_KEY)
        assert _marker(state_dir) == before
        assert host_override.current() is None

    def test_current_reports_deviation(self, config_file: Path):
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        with patch.object(
            host_override, "read_managed_config", return_value={"host": MANAGED_HOST}
        ):
            detail = host_override.current()
        assert detail is not None
        assert detail["overridden"] is True

        _write_yaml(config_file, MANAGED_HOST, secret=USER_SECRET)
        with patch.object(
            host_override, "read_managed_config", return_value={"host": MANAGED_HOST}
        ):
            assert host_override.current() is None


class TestNoticeBudget:
    def test_claim_notice_kinds_are_independent(self, monkeypatch, state_dir: Path):
        monkeypatch.setattr(time, "time", lambda: 7200.0)
        assert credential_state.claim_notice("host_override") is True
        assert credential_state.claim_notice("host_override") is False
        # The credential-rejection budget is untouched.
        assert credential_state.claim_notice() is True
        monkeypatch.setattr(time, "time", lambda: 7200.0 + 3600.0)
        assert credential_state.claim_notice("host_override") is True
        assert sorted(p.name for p in state_dir.glob("host_override_notice.*")) == [
            "host_override_notice.3"
        ]
        assert sorted(p.name for p in state_dir.glob("credential_notice.*")) == [
            "credential_notice.2"
        ]


class TestHookResponseNotice:
    def test_claude_code_allow_carries_attached_notice(self):
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        assert resp.has_notice_channel
        resp.attach_notice(lambda: "hello")
        assert json.loads(resp.allow()) == {"systemMessage": "hello"}

    def test_plain_allow_unchanged_without_notice(self):
        assert HookResponse(Client.CLAUDE_CODE, "PreToolUse").allow() is None

    def test_notice_returning_none_is_plain_allow(self):
        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        resp.attach_notice(lambda: None)
        assert resp.allow() is None

    def test_notice_called_only_when_allow_emits(self):
        """The callable is the budget claim: deny / observational answers and
        channel-less clients must never invoke it."""
        calls: list[str] = []

        def notice() -> str:
            calls.append("claimed")
            return "hello"

        resp = HookResponse(Client.CLAUDE_CODE, "PreToolUse")
        resp.attach_notice(notice)
        resp.deny("nope")
        resp.observational()
        assert calls == []

        cursor = HookResponse(Client.CURSOR, "beforeMCPExecution")
        cursor.attach_notice(notice)
        cursor.allow()
        assert calls == []

        resp.allow()
        assert calls == ["claimed"]

    def test_other_clients_have_no_channel(self):
        resp = HookResponse(Client.CURSOR, "beforeMCPExecution")
        assert not resp.has_notice_channel
        before = resp.allow()
        resp.attach_notice(lambda: "hello")
        assert resp.allow() == before


@pytest.fixture
def _flow_state(monkeypatch, tmp_path):
    monkeypatch.setattr(flow_spool, "get_runlayer_dir", lambda: tmp_path / "flows")
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()
    yield
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()


def _run_hook(
    monkeypatch, *, client: Client = Client.CLAUDE_CODE, answer: str = "allow"
) -> None:
    """Drive ``run_hook`` with the real dispatch replaced by one terminal
    response shape (``allow`` or ``observational``)."""
    monkeypatch.setattr(hook_dispatch, "detect_client", lambda: client)
    monkeypatch.setattr(hook_dispatch, "should_noop_for_cursor", lambda c: False)
    monkeypatch.setattr(hook_dispatch, "_resolve_mode", lambda: AIWatchMode.MONITOR)
    monkeypatch.setattr(
        hook_dispatch,
        "_dispatch",
        lambda **kw: hook_dispatch._write(getattr(kw["resp"], answer)()),
    )
    monkeypatch.delenv("HOOK_EVENT_NAME", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(_PRE_TOOL)))
    with hook_io.scoped(hook_io.HookIO()):
        hook_dispatch.run_hook()


def _last_flow_steps() -> list[str]:
    envelope = flow_spool.spool_drain()
    flows = envelope["flows"] if envelope else []
    return [step["name"] for step in flows[-1]["steps"]]


@pytest.mark.usefixtures("_flow_state")
class TestRunHookNotice:
    def test_notice_once_per_hour_and_flow_marker(
        self, config_file: Path, monkeypatch, capsys
    ):
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        monkeypatch.setattr(
            host_override, "read_managed_config", lambda: {"host": MANAGED_HOST}
        )

        _run_hook(monkeypatch)
        assert json.loads(capsys.readouterr().out) == {
            "systemMessage": messages.host_override_notice(USER_HOST, MANAGED_HOST)
        }
        assert "host_override" in _last_flow_steps()

        # Rate-limited: same hour, plain allow.
        _run_hook(monkeypatch)
        assert capsys.readouterr().out == ""
        assert "host_override" in _last_flow_steps()

    def test_observational_answer_keeps_budget_for_next_allow(
        self, config_file: Path, monkeypatch, capsys, state_dir: Path
    ):
        """First hook of the hour ends observational (PostToolUse-style, no
        notice channel on that shape): the budget must not be spent, so the
        following allow still shows the notice."""
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        monkeypatch.setattr(
            host_override, "read_managed_config", lambda: {"host": MANAGED_HOST}
        )

        _run_hook(monkeypatch, answer="observational")
        assert capsys.readouterr().out == ""
        assert not list(state_dir.glob("host_override_notice.*"))
        assert "host_override" in _last_flow_steps()

        _run_hook(monkeypatch)
        assert json.loads(capsys.readouterr().out) == {
            "systemMessage": messages.host_override_notice(USER_HOST, MANAGED_HOST)
        }
        assert len(list(state_dir.glob("host_override_notice.*"))) == 1

    def test_credential_rejected_allow_never_carries_host_notice(
        self, config_file: Path, monkeypatch, capsys, state_dir: Path
    ):
        """Monitor negative cache: the cached allow must not claim hooks still
        report to the MDM host while monitoring is offline, and must not spend
        the host-override budget. The flow marker is still stamped."""
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        monkeypatch.setattr(
            host_override, "read_managed_config", lambda: {"host": MANAGED_HOST}
        )
        monkeypatch.setattr(
            hook_dispatch, "_monitor_credentials_rejected", lambda: True
        )
        # Credential notice already spent this hour → silent cached allow.
        assert credential_state.claim_notice() is True

        _run_hook(monkeypatch)

        assert capsys.readouterr().out == ""
        assert not list(state_dir.glob("host_override_notice.*"))
        steps = _last_flow_steps()
        assert "host_override" in steps
        assert "credential_rejected_cached" in steps

    def test_no_notice_when_hosts_agree(self, config_file: Path, monkeypatch, capsys):
        _write_yaml(config_file, MANAGED_HOST, secret=USER_SECRET)
        monkeypatch.setattr(
            host_override, "read_managed_config", lambda: {"host": MANAGED_HOST}
        )
        _run_hook(monkeypatch)
        assert capsys.readouterr().out == ""
        assert "host_override" not in _last_flow_steps()

    def test_channel_less_client_keeps_budget(
        self, config_file: Path, monkeypatch, capsys, state_dir: Path
    ):
        """Cursor cannot show the notice, so the hourly claim is not spent."""
        _write_yaml(config_file, USER_HOST, secret=USER_SECRET)
        monkeypatch.setattr(
            host_override, "read_managed_config", lambda: {"host": MANAGED_HOST}
        )
        _run_hook(monkeypatch, client=Client.CURSOR)
        capsys.readouterr()
        assert not list(state_dir.glob("host_override_notice.*"))
        assert "host_override" in _last_flow_steps()
