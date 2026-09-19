"""Cause rendering on the fail-closed unreachable-API messages (ENG-5197)."""

from typing import get_args

import pytest

from runlayer_cli.hook import messages
from runlayer_cli.hook.failure import FailureContext, FailureKind


def _ctx(**kwargs) -> FailureContext:
    return FailureContext(**kwargs)


class TestUnreachableCauseRendering:
    def test_upload_timeout_names_size_elapsed_and_bounded_rate(self):
        user, agent = messages.tool_api_unreachable(
            tool_name="Edit",
            failure=_ctx(kind="upload_timeout", payload_bytes=8_400_000, elapsed_s=30.0),
        )
        assert "8.4 MB body" in agent
        assert "had not finished sending after 30s" in agent
        # Honesty: the body never finished sending, so the rate is a bound.
        assert "under ~2.2 Mbit/s effective" in agent
        assert "Large tool outputs on slow connections" in agent
        assert user == "Failed to contact Runlayer API (upload of 8.4 MB stalled after 30s)"

    def test_small_body_upload_timeout_states_size_but_never_blames_it(self):
        """A 2 KB upload stalling behind a dead proxy is not a data-volume
        problem; the size is stated as fact, blame and rate are omitted."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="upload_timeout", payload_bytes=2_048, elapsed_s=30.0)
        )
        assert "(2 KB body) had not finished sending" in agent
        assert "Large tool outputs" not in agent
        assert "Mbit/s" not in agent
        assert user == "Failed to contact Runlayer API (upload of 2 KB stalled after 30s)"

    def test_upload_dropped_connection_names_size_without_rate(self):
        """Prod signature: ALB reaps a stalled upload -> client sees a write
        error. Size is evidence; a throughput claim would not be."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="upload_failed", payload_bytes=8_400_000, elapsed_s=42.0)
        )
        assert "connection dropped" in agent
        assert "8.4 MB" in agent
        assert "Mbit/s" not in agent
        assert user == "Failed to contact Runlayer API (upload of 8.4 MB failed after 42s)"

    def test_small_body_upload_failed_does_not_blame_size(self):
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="upload_failed", payload_bytes=500, elapsed_s=5.0)
        )
        assert "(500 B body)" in agent
        assert "Large tool outputs" not in agent

    def test_upload_kind_without_size_still_renders_a_cause(self):
        """A future raise site without payload_bytes must not degrade to the
        opaque legacy message."""
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="upload_timeout", elapsed_s=30.0)
        )
        assert "timed out before it finished sending" in agent

    def test_read_timeout_with_large_body_names_size_but_never_a_rate(self):
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="timeout", payload_bytes=2_000_000, elapsed_s=30.0)
        )
        assert "2.0 MB" in agent
        assert "No complete response arrived within 30s" in agent
        assert "Mbit/s" not in agent
        assert "request body 2.0 MB" in user

    def test_small_body_timeout_does_not_blame_size(self):
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="timeout", payload_bytes=2_048, elapsed_s=30.0)
        )
        assert "2 KB" not in agent
        assert "request body" not in agent
        assert "No complete response arrived within 30s" in agent
        assert user == "Failed to contact Runlayer API"

    def test_connect_failure_does_not_blame_size(self):
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="connect", payload_bytes=8_400_000, elapsed_s=1.2)
        )
        assert "Could not connect to the Runlayer API." in agent
        assert "8.4 MB" not in agent
        assert user == "Failed to contact Runlayer API"

    def test_sub_second_elapsed_keeps_a_decimal(self):
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="timeout", payload_bytes=100, elapsed_s=0.4)
        )
        assert "No complete response arrived within 0.4s" in agent
        assert "within 0s" not in agent

    def test_missing_elapsed_omits_the_time_clause(self):
        """A reset is not a time-limit event; without elapsed there is no
        'after ...' clause at all."""
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="upload_failed", payload_bytes=8_400_000)
        )
        assert "(8.4 MB body) finished sending." in agent
        assert " after " not in agent
        assert "time limit" not in agent

    def test_http_failure_renders_answered_request_not_outage(self):
        """An HTTP response means something answered (403 = key lacks a role,
        429 = throttled); outage framing would misdirect. Attribution stays
        with the request, not definitively the API — behind an intercepting
        proxy the response may come from another hop."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=503, elapsed_s=0.4)
        )
        assert "was answered with HTTP 503" in agent
        assert "not a connectivity problem" in agent
        assert "The Runlayer API responded" not in agent
        assert "Failed to contact" not in agent
        assert "temporarily unreachable" not in agent
        assert user == "Runlayer verification request failed (HTTP 503)"

    def test_http_403_renders_answered_request_too(self):
        """A proxy or WAF can answer 403 per request, so only 401 is treated
        as a credential rejection; 403 keeps the answered-request wording."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=403, elapsed_s=0.2)
        )
        assert "was answered with HTTP 403" in agent
        assert "credentials" not in agent
        assert "Failed to contact" not in user

    def test_http_407_names_the_proxy_not_the_api(self):
        """407 is generated by an HTTP proxy on the path; blaming the Runlayer
        API (or its administrator) would misdirect."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=407, elapsed_s=0.2)
        )
        assert "proxy" in agent
        assert "never reached the Runlayer API" in agent
        assert "The Runlayer API responded" not in agent
        assert user == "HTTP proxy requires authentication (HTTP 407)"

    def test_http_401_renders_credential_rejection_not_unreachable_blame(self):
        """401 means the API was reached and said no. The message must not
        claim the API was unreachable, must not promise a cache side effect
        (inline hooks have no credential cache), and must route the reader
        toward credentials, not outage."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=401, elapsed_s=0.2)
        )
        assert "rejected this machine's credentials" in agent
        assert "credential problem, not an outage" in agent
        assert "Authentication Required" in agent
        assert "Failed to contact" not in agent
        assert "temporarily unreachable" not in agent
        assert "refreshed" not in agent
        assert user == (
            "Runlayer API rejected this machine's credentials (HTTP 401). "
            "Nothing to fix locally — contact your Runlayer administrator"
        )

    def test_managed_credential_rejection_points_at_the_administrator(self):
        """Org-key install: nothing to do locally, where the administrator
        identifies the revoked key (Settings → MDM configuration + audit log),
        and the hostname for the helpdesk ticket."""
        user, agent = messages.api_unreachable(
            tool_name="mcp__jira__search",
            failure=_ctx(kind="http", status_code=401, elapsed_s=0.2),
            hostname="LAPTOP-42",
            managed_credential=True,
        )
        assert user.endswith("(device: LAPTOP-42)")
        assert "- Device hostname: LAPTOP-42" in agent
        assert "Nothing on this machine can fix this" in agent
        assert (
            "identify the revoked organization API key from Settings → MDM "
            "configuration and the audit log" in agent
        )
        assert "re-deploy a current configuration to this device" in agent
        # Product rule (ENG-6549): there is no per-device "credential
        # rejected" marker, so the footer must not send anyone to look for one.
        assert "Shadow → Devices" not in agent
        assert 'Quote the device hostname "LAPTOP-42" when opening' in agent
        assert "Unverified actions are blocked (fail-closed)" in agent
        assert messages.AGENT_GUARDRAILS in agent

    def test_user_key_rejection_points_at_runlayer_login(self):
        """Per-user secret (no org key): signing in again is the fix, so the
        message must not claim nothing can be done locally."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=401),
            hostname="USERBOX",
            managed_credential=False,
        )
        assert user == (
            "Runlayer API rejected this machine's credentials (HTTP 401). "
            "Run 'runlayer login' to refresh them (device: USERBOX)"
        )
        assert "Run 'runlayer login' to refresh this machine's Runlayer credentials" in agent
        assert "Nothing on this machine can fix this" not in agent
        assert "device management" not in agent
        assert "Runlayer administrator" in agent

    def test_credential_rejection_without_hostname_omits_the_line(self):
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=401), hostname=None
        )
        assert "Device hostname" not in agent
        assert "(device:" not in user
        assert "this machine's hostname" in agent

    def test_no_context_renders_legacy_message_unchanged(self):
        user, agent = messages.tool_api_unreachable(tool_name="Bash")
        assert user == "Failed to contact Runlayer API"
        assert (
            "Failed to contact the Runlayer API for local tool verification. "
            "Unverified actions are blocked (fail-closed)." in agent
        )

    @pytest.mark.parametrize("builder", [messages.api_unreachable, messages.tool_api_unreachable])
    def test_agent_guardrails_block_is_intact(self, builder):
        """The agent directive block is a product contract; the cause line
        must not alter it."""
        _, agent = builder(
            failure=_ctx(kind="upload_timeout", payload_bytes=8_400_000, elapsed_s=30.0)
        )
        assert messages.AGENT_GUARDRAILS in agent

    def test_mcp_variant_carries_cause_too(self):
        user, agent = messages.api_unreachable(
            failure=_ctx(kind="upload_timeout", payload_bytes=512_000, elapsed_s=10.0)
        )
        assert "512 KB" in agent
        assert "MCP execution verification" in agent
        assert "stalled after 10s" in user


class TestFailureKindContract:
    @pytest.mark.parametrize("kind", get_args(FailureKind))
    def test_every_classifier_kind_has_a_rendering(self, kind):
        """A kind the classifier can produce must never silently degrade to
        the opaque legacy message (the regression ENG-5197 fixes)."""
        baseline = messages.tool_api_unreachable()[1]
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind=kind, payload_bytes=8_400_000, elapsed_s=30.0, status_code=503)
        )
        assert agent != baseline, f"kind {kind!r} rendered the opaque legacy message"

    def test_http_401_message_never_claims_unreachable(self):
        """Both builders route 401 to the credential-rejection message."""
        for builder in (messages.api_unreachable, messages.tool_api_unreachable):
            user, agent = builder(failure=_ctx(kind="http", status_code=401))
            assert "Failed to contact" not in agent
            assert "Failed to contact" not in user


class TestFormatSize:
    @pytest.mark.parametrize(
        ("n", "expected"),
        [
            (97, "97 B"),
            (2_048, "2 KB"),
            (512_000, "512 KB"),
            (999_999, "1.0 MB"),
            (8_400_000, "8.4 MB"),
        ],
    )
    def test_format(self, n, expected):
        assert messages._format_size(n) == expected
