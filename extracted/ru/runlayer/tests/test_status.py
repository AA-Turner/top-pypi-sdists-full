import json
from unittest.mock import patch

from typer.testing import CliRunner

from runlayer_cli.config import Config, HostConfig
from runlayer_cli.hook_install.check import ClientStatus, InstalledClient
from runlayer_cli.hook_install.clients import Client
from runlayer_cli.hook_install.paths import InstallScope
from runlayer_cli.main import app


runner = CliRunner()


def test_status_json_reports_credentials_enrollment_and_user_hooks(tmp_path):
    first_host = "https://app.runlayer.com"
    second_host = "https://tenant.runlayer.com"
    config = Config(
        default_host=first_host,
        hosts={
            "app.runlayer.com": HostConfig(url=first_host, secret="rl_user_secret"),
            "tenant.runlayer.com": HostConfig(url=second_host),
        },
    )
    first_marker = tmp_path / ".enrolled-app.runlayer.com"
    first_marker.touch()

    def marker_path(host: str):
        if host == first_host:
            return first_marker
        return tmp_path / ".enrolled-tenant.runlayer.com"

    hook_results = [
        InstalledClient(Client.CURSOR, ClientStatus.OK),
        InstalledClient(Client.CLAUDE_CODE, ClientStatus.DRIFTED, "missing hook"),
    ]

    with (
        patch("runlayer_cli.commands.status.__version__", "1.2.3"),
        patch("runlayer_cli.commands.status.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
        patch(
            "runlayer_cli.commands.status.enrollment_marker_path",
            side_effect=marker_path,
        ),
        patch(
            "runlayer_cli.commands.status.resolve_runlayer_hook_command",
            return_value="/usr/local/bin/runlayer hook",
        ),
        patch(
            "runlayer_cli.commands.status.check_all",
            return_value=hook_results,
        ) as check_all,
        patch(
            "runlayer_cli.commands.status._resolve_network_enrichment",
            return_value=(None, None, None),
        ),
    ):
        result = runner.invoke(app, ["status", "--json"])

    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout) == {
        "version": "1.2.3",
        "default_host": first_host,
        "dashboard_url": first_host,
        "hosts": [
            {
                "url": first_host,
                "credential": "ok",
                "enrolled": True,
            },
            {
                "url": second_host,
                "credential": "missing",
                "enrolled": False,
            },
        ],
        "hooks": [
            {"client": "cursor", "status": "ok"},
            {"client": "claude_code", "status": "drifted"},
        ],
        "identity": None,
        "attention": None,
        "admin": None,
    }
    check_all.assert_called_once_with(
        scope=InstallScope.USER,
        expected_hook_command="/usr/local/bin/runlayer hook",
        include_pipeline=False,
    )
    assert "rl_user_secret" not in result.stdout


def test_status_json_handles_empty_configuration():
    with (
        patch("runlayer_cli.commands.status.__version__", "1.2.3"),
        patch("runlayer_cli.commands.status.load_config", return_value=Config()),
        patch(
            "runlayer_cli.commands.status.resolve_runlayer_hook_command",
            return_value="runlayer hook",
        ),
        patch("runlayer_cli.commands.status.check_all", return_value=[]),
    ):
        result = runner.invoke(app, ["status", "--json"])

    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout) == {
        "version": "1.2.3",
        "default_host": None,
        "dashboard_url": None,
        "hosts": [],
        "hooks": [],
        "identity": None,
        "attention": None,
        "admin": None,
    }


def test_status_json_includes_identity_attention_and_admin_when_signed_in():
    host = "https://ecs.prod.runlayer.com"
    config = Config(
        default_host=host,
        hosts={"ecs.prod.runlayer.com": HostConfig(url=host, secret="rl_user_secret")},
    )
    identity = {
        "display_name": "Tyler Berry",
        "email": "tyler@runlayer.com",
        "role": "Super Admin",
        "space": "Runlayer",
        "can_manage_user_mcp_access": True,
    }
    attention = {
        "accounts_needing_reconnect": 1,
        "accounts": [
            {"account_id": "a1", "server_id": "s1", "label": "Slack"},
        ],
        "approval_requests_pending": 1,
        "approval_requests": [
            {
                "id": "approval-1",
                "title": "Approval needed: A -> b",
                "can_decide_inline": True,
            }
        ],
    }
    admin = {
        "sessions": [
            {
                "id": "sess-1",
                "title": "Debug OAuth",
                "client": "cursor",
                "started_at": "2026-08-04T12:00:00Z",
            }
        ],
        "access_requests": [
            {
                "id": "ar-1",
                "requester": "Alex Kim",
                "resource": "Slack",
                "summary": "Alex Kim requested Slack",
            }
        ],
    }
    with (
        patch("runlayer_cli.commands.status.__version__", "1.2.3"),
        patch("runlayer_cli.commands.status.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
        patch(
            "runlayer_cli.commands.status.enrollment_marker_path"
        ) as enrollment_marker_path,
        patch(
            "runlayer_cli.commands.status.resolve_runlayer_hook_command",
            return_value="runlayer hook",
        ),
        patch("runlayer_cli.commands.status.check_all", return_value=[]),
        patch(
            "runlayer_cli.commands.status._resolve_network_enrichment",
            return_value=(identity, attention, admin),
        ) as resolve_enrichment,
    ):
        enrollment_marker_path.return_value.exists.return_value = False
        result = runner.invoke(app, ["status", "--json"])

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["identity"] == identity
    assert payload["attention"] == attention
    assert payload["admin"] == admin
    resolve_enrichment.assert_called_once()
    assert "rl_user_secret" not in result.stdout


def test_identity_from_user_payload_prefers_full_name_and_role_name():
    from runlayer_cli.commands.status import _identity_from_user_payload

    identity = _identity_from_user_payload(
        {
            "email": "tyler@runlayer.com",
            "full_name": "Tyler Berry",
            "roles": [{"name": "Super Admin", "role_type": "super_admin"}],
        },
        host="https://ecs.prod.runlayer.com",
    )
    assert identity == {
        "display_name": "Tyler Berry",
        "email": "tyler@runlayer.com",
        "role": "Super Admin",
        "space": "Runlayer",
        "can_manage_user_mcp_access": False,
    }


def test_identity_exposes_manage_user_mcp_access_capability():
    from runlayer_cli.commands.status import _identity_from_user_payload

    admin = _identity_from_user_payload(
        {
            "email": "admin@runlayer.com",
            "capabilities": ["use_assigned_mcps", "manage_user_mcp_access"],
        },
        host="https://ecs.prod.runlayer.com",
    )
    member = _identity_from_user_payload(
        {
            "email": "member@runlayer.com",
            "capabilities": ["use_assigned_mcps"],
        },
        host="https://ecs.prod.runlayer.com",
    )
    assert admin is not None and admin["can_manage_user_mcp_access"] is True
    assert member is not None and member["can_manage_user_mcp_access"] is False


def test_accounts_needing_reconnect_mirrors_web_needs_reconnect():
    from runlayer_cli.commands.status import _accounts_needing_reconnect

    assert _accounts_needing_reconnect(
        [
            {
                "id": "1",
                "server_id": "s",
                "label": "never connected",
                "session_healthy": None,
            },
            {
                "id": "2",
                "server_id": "s",
                "label": "ok",
                "session_healthy": True,
            },
            {
                "id": "3",
                "server_id": "s1",
                "label": "bad",
                "session_healthy": False,
            },
            {
                "id": "4",
                "server_id": "s2",
                "label": "also bad",
                "session_healthy": False,
            },
            "not-a-dict",
        ]
    ) == [
        {"account_id": "3", "server_id": "s1", "label": "bad"},
        {"account_id": "4", "server_id": "s2", "label": "also bad"},
    ]
    assert _accounts_needing_reconnect(None) == []
    assert _accounts_needing_reconnect({"data": []}) == []


def test_approval_requests_pending_parses_pending_rows_only():
    from runlayer_cli.commands.status import _approval_requests_pending

    assert _approval_requests_pending(
        {
            "data": [
                {
                    "id": "req-1",
                    "status": "pending",
                    "can_decide_inline": True,
                    "initial_content": {
                        "title": "Approval required",
                        "body_markdown": "",
                    },
                    "tool_call": {
                        "server_name": "Slack",
                        "tool_name": "post_message",
                    },
                },
                {"id": "req-missing", "status": "pending"},
                {"id": "req-review", "status": "pending", "can_decide_inline": False},
                {"id": "req-2", "status": "approved"},
                {"id": "", "status": "pending"},
                "not-a-dict",
            ],
            "count": 1,
        }
    ) == [
        {
            "id": "req-1",
            "title": "Approval needed: Slack -> post_message",
            "can_decide_inline": True,
        },
        {"id": "req-missing", "title": "", "can_decide_inline": False},
        {"id": "req-review", "title": "", "can_decide_inline": False},
    ]
    assert _approval_requests_pending(None) == []
    assert _approval_requests_pending([]) == []


def test_approval_title_tolerates_a_backend_without_one():
    from runlayer_cli.commands.status import _approval_title

    assert _approval_title({"title": "  Approval needed: A -> b  "}) == (
        "Approval needed: A -> b"
    )
    assert _approval_title({"title": ""}) == ""
    assert _approval_title({"body_markdown": "x"}) == ""
    assert _approval_title({"title": 7}) == ""
    assert _approval_title(None) == ""
    assert _approval_title("not-a-dict") == ""


def test_fetch_attention_returns_accounts_when_reconnect_needed():
    from runlayer_cli.commands.status import _fetch_attention

    def fake_get_json(host, secret, path):
        if path == "/api/v1/accounts":
            return [
                {
                    "id": "acc-1",
                    "server_id": "srv-1",
                    "label": "Slack",
                    "session_healthy": False,
                },
                {
                    "id": "acc-2",
                    "server_id": "srv-2",
                    "label": "GitHub",
                    "session_healthy": True,
                },
            ]
        if path == "/api/v1/approvals":
            return {"data": [], "count": 0}
        raise AssertionError(path)

    with patch("runlayer_cli.commands.status._get_json", side_effect=fake_get_json):
        attention = _fetch_attention("https://ecs.prod.runlayer.com", "rl_user_secret")

    assert attention == {
        "accounts_needing_reconnect": 1,
        "accounts": [
            {
                "account_id": "acc-1",
                "server_id": "srv-1",
                "label": "Slack",
            },
        ],
        "approval_requests_pending": 0,
        "approval_requests": [],
    }


def test_fetch_attention_returns_approvals_when_pending():
    from runlayer_cli.commands.status import _fetch_attention

    def fake_get_json(host, secret, path):
        if path == "/api/v1/accounts":
            return []
        if path == "/api/v1/approvals":
            return {
                "data": [
                    {
                        "id": "req-1",
                        "status": "pending",
                        "can_decide_inline": True,
                    },
                    {"id": "req-2", "status": "approved"},
                ],
                "count": 1,
            }
        raise AssertionError(path)

    with patch("runlayer_cli.commands.status._get_json", side_effect=fake_get_json):
        attention = _fetch_attention("https://ecs.prod.runlayer.com", "rl_user_secret")

    assert attention == {
        "accounts_needing_reconnect": 0,
        "accounts": [],
        "approval_requests_pending": 1,
        "approval_requests": [{"id": "req-1", "title": "", "can_decide_inline": True}],
    }


def test_fetch_attention_returns_none_when_healthy_or_soft_fail():
    from runlayer_cli.commands.status import _fetch_attention

    with patch(
        "runlayer_cli.commands.status._get_json",
        return_value=[{"session_healthy": True}, {"session_healthy": None}],
    ):
        assert _fetch_attention("https://ecs.prod.runlayer.com", "secret") is None

    with patch("runlayer_cli.commands.status._get_json", return_value=None):
        assert _fetch_attention("https://ecs.prod.runlayer.com", "secret") is None


def test_resolve_enrichment_returns_identity_and_attention():
    from runlayer_cli.commands.status import _resolve_network_enrichment

    me = {
        "email": "admin@runlayer.com",
        "full_name": "Admin",
        "roles": [{"name": "Super Admin"}],
        "capabilities": ["manage_user_mcp_access", "use_assigned_mcps"],
    }
    attention = {
        "accounts_needing_reconnect": 0,
        "accounts": [],
        "approval_requests_pending": 1,
        "approval_requests": [{"id": "req-1", "title": "", "can_decide_inline": True}],
    }
    admin = {"sessions": [], "access_requests": []}
    with (
        patch("runlayer_cli.commands.status._fetch_me", return_value=me),
        patch(
            "runlayer_cli.commands.status._fetch_attention",
            return_value=attention,
        ),
        patch(
            "runlayer_cli.commands.status._fetch_admin",
            return_value=admin,
        ) as fetch_admin,
    ):
        identity, got_attention, got_admin = _resolve_network_enrichment(
            default_host="https://ecs.prod.runlayer.com",
            hosts=[
                {
                    "url": "https://ecs.prod.runlayer.com",
                    "credential": "ok",
                    "enrolled": False,
                }
            ],
            secret_for_host="rl_user_secret",
        )

    assert identity is not None
    assert identity["can_manage_user_mcp_access"] is True
    assert got_attention == attention
    assert got_admin == admin
    fetch_admin.assert_called_once()


def test_resolve_enrichment_skips_admin_without_capability():
    from runlayer_cli.commands.status import _resolve_network_enrichment

    me = {
        "email": "member@runlayer.com",
        "full_name": "Member",
        "roles": [{"name": "Member"}],
        "capabilities": ["use_assigned_mcps"],
    }
    with (
        patch("runlayer_cli.commands.status._fetch_me", return_value=me),
        patch("runlayer_cli.commands.status._fetch_attention", return_value=None),
        patch("runlayer_cli.commands.status._fetch_admin") as fetch_admin,
    ):
        identity, attention, admin = _resolve_network_enrichment(
            default_host="https://ecs.prod.runlayer.com",
            hosts=[
                {
                    "url": "https://ecs.prod.runlayer.com",
                    "credential": "ok",
                    "enrolled": False,
                }
            ],
            secret_for_host="rl_user_secret",
        )

    assert identity is not None
    assert attention is None
    assert admin is None
    fetch_admin.assert_not_called()


def test_parse_admin_sessions_reads_session_list_response_shape():
    from runlayer_cli.commands.status import _parse_admin_sessions

    parsed = _parse_admin_sessions(
        {
            "data": [
                {
                    "session_id": "sess-1",
                    "title": "Debug OAuth",
                    "client": "cursor",
                    "started_at": "2026-08-04T12:00:00Z",
                },
                {
                    "session_id": "sess-2",
                    "title": None,
                    "client": "claude_code",
                    "started_at": "2026-08-04T10:00:00Z",
                },
            ],
            "total": 2,
        }
    )
    assert parsed == [
        {
            "id": "sess-1",
            "title": "Debug OAuth",
            "client": "cursor",
            "started_at": "2026-08-04T12:00:00Z",
        },
        {
            "id": "sess-2",
            "title": "Untitled session",
            "client": "claude_code",
            "started_at": "2026-08-04T10:00:00Z",
        },
    ]


def test_parse_admin_sessions_ignores_summaries_key_mismatch():
    from runlayer_cli.commands.status import _parse_admin_sessions

    # Wrong envelope (summaries) + wrong id field must not falsely populate.
    assert (
        _parse_admin_sessions(
            {
                "summaries": [
                    {
                        "id": "sess-1",
                        "title": "Nope",
                        "client": "cursor",
                        "started_at": "2026-08-04T12:00:00Z",
                    }
                ]
            }
        )
        == []
    )


def test_parse_admin_sessions_caps_at_three_rows():
    from runlayer_cli.commands.status import _parse_admin_sessions

    rows = [
        {
            "session_id": f"sess-{index}",
            "title": f"Session {index}",
            "client": "cursor",
            "started_at": "2026-08-04T12:00:00Z",
        }
        for index in range(10)
    ]
    assert len(_parse_admin_sessions({"data": rows})) == 3


def test_parse_admin_access_requests_reads_access_rows_and_server_name():
    from runlayer_cli.commands.status import _parse_admin_access_requests

    parsed = _parse_admin_access_requests(
        {
            "data": [
                {
                    "type": "access",
                    "data": {
                        "id": "ar-1",
                        "requested_by_name": "Alex Kim",
                        "requested_by_email": "alex@example.com",
                    },
                    "server": {"name": "Slack"},
                },
                # Non-access rows share the queue and must be skipped.
                {"type": "server", "data": {"id": "sr-1"}},
            ],
            "count": 2,
        }
    )
    assert parsed == [
        {
            "id": "ar-1",
            "requester": "Alex Kim",
            "resource": "Slack",
            "summary": "Alex Kim requested Slack",
        }
    ]


def test_parse_admin_access_requests_falls_back_to_email_then_placeholder():
    from runlayer_cli.commands.status import _parse_admin_access_requests

    parsed = _parse_admin_access_requests(
        {
            "data": [
                {
                    "type": "access",
                    "data": {"id": "ar-1", "requested_by_email": "alex@example.com"},
                    "server": {"name": "Slack"},
                },
                {"type": "access", "data": {"id": "ar-2"}},
            ]
        }
    )
    assert [(row["requester"], row["resource"]) for row in parsed] == [
        ("alex@example.com", "Slack"),
        ("Someone", "connector"),
    ]


def test_parse_admin_access_requests_skips_rows_without_id_and_caps_at_five():
    from runlayer_cli.commands.status import _parse_admin_access_requests

    assert (
        _parse_admin_access_requests(
            {"data": [{"type": "access", "data": {"id": " "}}]}
        )
        == []
    )
    rows = [
        {
            "type": "access",
            "data": {"id": f"ar-{index}", "requested_by_name": "Alex"},
            "server": {"name": "Slack"},
        }
        for index in range(10)
    ]
    assert len(_parse_admin_access_requests({"data": rows})) == 5


def test_fetch_admin_queries_sessions_and_pending_access_requests():
    from runlayer_cli.commands.status import _fetch_admin

    def fake_get_json(host, secret, path, params=None):
        if path == "/api/v1/sessions/":
            # VIEW_ORG_AUDIT_LOGS users get org-wide sessions unless actor_id
            # scopes the list — tray Recent must always pass the signed-in user.
            assert params == {"limit": 3, "actor_id": "user-me"}
            return {
                "data": [
                    {
                        "session_id": "sess-1",
                        "title": "Debug OAuth",
                        "client": "cursor",
                        "started_at": "2026-08-04T12:00:00Z",
                    }
                ]
            }
        assert path == "/api/v1/admin/requests"
        assert params == {
            "status": "pending",
            "request_type": "access",
            "limit": 5,
        }
        return {
            "data": [
                {
                    "type": "access",
                    "data": {"id": "ar-1", "requested_by_name": "Alex Kim"},
                    "server": {"name": "Slack"},
                }
            ]
        }

    with patch("runlayer_cli.commands.status._get_json", side_effect=fake_get_json):
        admin = _fetch_admin(
            "https://ecs.prod.runlayer.com", "secret", actor_id="user-me"
        )

    assert admin is not None
    assert [session["id"] for session in admin["sessions"]] == ["sess-1"]
    assert [request["id"] for request in admin["access_requests"]] == ["ar-1"]


def test_fetch_admin_scopes_sessions_to_actor_id():
    """Superadmins (VIEW_ORG_AUDIT_LOGS) must not see other users' sessions."""
    from runlayer_cli.commands.status import _fetch_admin

    seen: dict[str, object] = {}

    def fake_get_json(host, secret, path, params=None):
        if path == "/api/v1/sessions/":
            seen["sessions_params"] = params
        return {"data": []}

    with patch("runlayer_cli.commands.status._get_json", side_effect=fake_get_json):
        _fetch_admin("https://ecs.prod.runlayer.com", "secret", actor_id="user-me")

    assert seen["sessions_params"] == {"limit": 3, "actor_id": "user-me"}


def test_fetch_admin_skips_sessions_without_actor_id():
    """No resolved actor ⇒ no sessions call at all, never an org-wide one."""
    from runlayer_cli.commands.status import _fetch_admin

    paths: list[str] = []

    def fake_get_json(host, secret, path, params=None):
        paths.append(path)
        return {"data": []}

    with patch("runlayer_cli.commands.status._get_json", side_effect=fake_get_json):
        admin = _fetch_admin("https://ecs.prod.runlayer.com", "secret", actor_id=None)

    # Requests stand on their own; only the sessions GET is actor-gated.
    assert paths == ["/api/v1/admin/requests"]
    assert admin == {"sessions": [], "access_requests": []}


def test_fetch_admin_soft_fails_to_none_only_when_both_endpoints_fail():
    from runlayer_cli.commands.status import _fetch_admin

    with patch("runlayer_cli.commands.status._get_json", return_value=None):
        assert (
            _fetch_admin("https://ecs.prod.runlayer.com", "secret", actor_id="user-me")
            is None
        )

    # One soft-fail must not hide the other surface.
    def only_requests(host, secret, path, params=None):
        if path == "/api/v1/sessions/":
            return None
        return {
            "data": [
                {
                    "type": "access",
                    "data": {"id": "ar-1", "requested_by_name": "Alex Kim"},
                    "server": {"name": "Slack"},
                }
            ]
        }

    with patch("runlayer_cli.commands.status._get_json", side_effect=only_requests):
        admin = _fetch_admin(
            "https://ecs.prod.runlayer.com", "secret", actor_id="user-me"
        )

    assert admin == {
        "sessions": [],
        "access_requests": [
            {
                "id": "ar-1",
                "requester": "Alex Kim",
                "resource": "Slack",
                "summary": "Alex Kim requested Slack",
            }
        ],
    }


def test_resolve_enrichment_scopes_sessions_to_signed_in_user():
    from runlayer_cli.commands.status import _resolve_network_enrichment

    me = {
        "id": "user-me",
        "email": "admin@runlayer.com",
        "full_name": "Admin",
        "roles": [{"name": "Super Admin"}],
        "capabilities": ["manage_user_mcp_access", "view_org_audit_logs"],
    }
    seen: dict[str, object] = {}

    def fake_get_json(host, secret, path, params=None):
        if path == "/api/v1/sessions/":
            seen["sessions_params"] = params
        return {"data": []}

    with (
        patch("runlayer_cli.commands.status._fetch_me", return_value=me),
        patch("runlayer_cli.commands.status._fetch_attention", return_value=None),
        patch("runlayer_cli.commands.status._get_json", side_effect=fake_get_json),
    ):
        _resolve_network_enrichment(
            default_host="https://ecs.prod.runlayer.com",
            hosts=[
                {
                    "url": "https://ecs.prod.runlayer.com",
                    "credential": "ok",
                    "enrolled": False,
                }
            ],
            secret_for_host="rl_user_secret",
        )

    assert seen["sessions_params"] == {"limit": 3, "actor_id": "user-me"}


def test_reconnect_account_opens_authorization_url():
    host = "https://ecs.prod.runlayer.com"
    config = Config(
        default_host=host,
        hosts={"ecs.prod.runlayer.com": HostConfig(url=host, secret="rl_user_secret")},
    )

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"authorization_url": "https://idp.example/authorize?x=1"}

    class FakeClient:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def post(self, url, params=None):
            assert url == f"{host}/api/v1/servers/srv-1/oauth/initiate"
            assert params == {"account_id": "acc-1"}
            return FakeResponse()

    with (
        patch(
            "runlayer_cli.commands.reconnect_account.load_config",
            return_value=config,
        ),
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
        patch(
            "runlayer_cli.commands.reconnect_account.http_client",
            return_value=FakeClient(),
        ),
        patch(
            "runlayer_cli.commands.reconnect_account.webbrowser.open",
            return_value=True,
        ) as open_browser,
    ):
        result = runner.invoke(
            app,
            [
                "__reconnect-account",
                "--server-id",
                "srv-1",
                "--account-id",
                "acc-1",
            ],
        )

    assert result.exit_code == 0, result.output
    open_browser.assert_called_once_with("https://idp.example/authorize?x=1")
    assert "rl_user_secret" not in result.output


def test_status_human_output_never_prints_secret():
    host = "https://app.runlayer.com"
    config = Config(
        default_host=host,
        hosts={"app.runlayer.com": HostConfig(url=host, secret="rl_user_secret")},
    )
    with (
        patch("runlayer_cli.commands.status.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
        patch(
            "runlayer_cli.commands.status.enrollment_marker_path"
        ) as enrollment_marker_path,
        patch(
            "runlayer_cli.commands.status.resolve_runlayer_hook_command",
            return_value="runlayer hook",
        ),
        patch("runlayer_cli.commands.status.check_all", return_value=[]),
        patch(
            "runlayer_cli.commands.status._resolve_network_enrichment",
            return_value=(None, None, None),
        ),
    ):
        enrollment_marker_path.return_value.exists.return_value = False
        result = runner.invoke(app, ["status"])

    assert result.exit_code == 0, result.output
    assert host in result.stdout
    assert "Authenticated" in result.stdout
    assert "rl_user_secret" not in result.stdout
