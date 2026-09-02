"""Redaction helpers for the agent report: scrub paths/tokens before submit."""

from __future__ import annotations

import pytest

from runlayer_cli.scan.agents.redact import redact_basename, sanitize_path


class TestSanitizePath:
    @pytest.mark.parametrize("value", [None, ""])
    def test_empty_passthrough(self, value):
        assert sanitize_path(value) == value

    def test_plain_token_unchanged(self):
        # A dependency name / import / symbol carries nothing to scrub.
        assert sanitize_path("langchain") == "langchain"
        assert sanitize_path("from langchain.agents import AgentExecutor") == (
            "from langchain.agents import AgentExecutor"
        )

    def test_macos_home_username_redacted(self):
        assert (
            sanitize_path("/Users/alice/proj/agent") == "/Users/<redacted>/proj/agent"
        )

    def test_linux_home_username_redacted(self):
        assert sanitize_path("/home/bob/src/app") == "/home/<redacted>/src/app"

    def test_windows_home_username_redacted(self):
        assert sanitize_path(r"C:\Users\carol\proj") == r"C:\Users\<redacted>\proj"

    def test_home_match_is_case_insensitive(self):
        assert sanitize_path("/users/dave/x") == "/users/<redacted>/x"

    def test_non_home_path_unchanged(self):
        # A system path with no account segment is left intact.
        assert sanitize_path("/usr/local/bin/openclaw") == "/usr/local/bin/openclaw"

    def test_home_lookalike_segment_not_touched(self):
        # "homeservice" is not the home root, so nothing is redacted.
        assert sanitize_path("/opt/homeservice/data") == "/opt/homeservice/data"

    def test_url_credentials_stripped(self):
        assert sanitize_path("https://user:pass@host/mcp") == "https://host/mcp"
        assert sanitize_path("http://token@localhost:8080") == "http://localhost:8080"

    def test_url_credentials_and_home_both_scrubbed(self):
        assert sanitize_path("ssh://u:p@host/home/alice/repo") == (
            "ssh://host/home/<redacted>/repo"
        )


class TestKnownUsernameRedaction:
    """The scan's own username, redacted as a whole path segment anywhere."""

    def test_username_outside_home_layout_redacted(self):
        # The home-segment fallback misses this; the known username catches it.
        assert sanitize_path("/opt/work/alice/agent", usernames=["alice"]) == (
            "/opt/work/<redacted>/agent"
        )

    def test_username_only_matches_full_segment(self):
        # "alice" is a prefix here, not the whole component -> left intact.
        assert sanitize_path("/opt/alice-cache/data", usernames=["alice"]) == (
            "/opt/alice-cache/data"
        )

    def test_username_as_whole_value_redacted(self):
        assert sanitize_path("alice", usernames=["alice"]) == "<redacted>"

    def test_username_match_is_case_insensitive(self):
        assert sanitize_path("/data/ALICE/x", usernames=["alice"]) == (
            "/data/<redacted>/x"
        )

    def test_without_username_non_home_path_unredacted(self):
        # Documents the fallback limit: no known user -> only home layout scrubbed.
        assert sanitize_path("/opt/work/alice/agent") == "/opt/work/alice/agent"

    def test_home_layout_scrubbed_before_username_pass(self):
        assert sanitize_path("/Users/alice/proj", usernames=["alice"]) == (
            "/Users/<redacted>/proj"
        )

    def test_empty_username_entries_ignored(self):
        assert sanitize_path("/opt/work/alice/x", usernames=["", None]) == (  # type: ignore[list-item]
            "/opt/work/alice/x"
        )


class TestSecretRedaction:
    """Defense-in-depth credential/secret token masking (backend-mirrored)."""

    def test_github_token_masked(self):
        token = "ghp_" + "a" * 36
        assert sanitize_path(f"/repo/{token}/x") == "/repo/<redacted>/x"

    def test_aws_access_key_masked(self):
        assert sanitize_path("AKIAIOSFODNN7EXAMPLE") == "<redacted>"

    def test_sk_key_masked(self):
        assert sanitize_path("sk-live-0123456789abcdefghij") == "<redacted>"

    def test_slack_token_masked(self):
        assert sanitize_path("xoxb-1234567890-abcdefghijkl") == "<redacted>"

    def test_jwt_masked(self):
        jwt = (
            "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0."
            "dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
        )
        assert sanitize_path(jwt) == "<redacted>"

    def test_password_kv_masks_value_keeps_key(self):
        assert sanitize_path("password=supersecret1") == "password=<redacted>"

    def test_api_key_kv_masks_value_keeps_key(self):
        assert sanitize_path("api_key=0123456789abcdef") == "api_key=<redacted>"

    def test_registry_tokens_pass_through(self):
        # Import/symbol/dependency evidence must never be mangled as a "secret".
        assert sanitize_path("langchain") == "langchain"
        assert sanitize_path("openai(") == "openai("
        assert sanitize_path("from langchain.agents import AgentExecutor") == (
            "from langchain.agents import AgentExecutor"
        )

    def test_ordinary_path_segment_not_flagged(self):
        # "task-runner" starts with letters but isn't an sk-/token secret.
        assert sanitize_path("/srv/task-runner/main") == "/srv/task-runner/main"


class TestRedactBasename:
    @pytest.mark.parametrize("value", [None, ""])
    def test_empty_passthrough(self, value):
        assert redact_basename(value) == value

    def test_posix_path_reduced(self):
        assert redact_basename("/Users/alice/proj/agent.py") == "agent.py"

    def test_windows_path_reduced_on_posix_host(self):
        # A Windows-style source path collapses even when parsed on POSIX.
        assert redact_basename(r"C:\Users\bob\proj\main.ts") == "main.ts"

    def test_bare_basename_unchanged(self):
        assert redact_basename("pyproject.toml") == "pyproject.toml"

    def test_install_marker_label_unchanged(self):
        # Install evidence sources are labels ("cli", "gateway"), not paths.
        assert redact_basename("cli") == "cli"
