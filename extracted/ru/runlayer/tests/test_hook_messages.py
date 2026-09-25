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
            failure=_ctx(
                kind="upload_timeout", payload_bytes=8_400_000, elapsed_s=30.0
            ),
        )
        assert "8.4 MB body" in agent
        assert "had not finished sending after 30s" in agent
        # Honesty: the body never finished sending, so the rate is a bound.
        assert "under ~2.2 Mbit/s effective" in agent
        assert "Large tool outputs on slow connections" in agent
        assert (
            user
            == "Failed to contact Runlayer API (upload of 8.4 MB stalled after 30s)"
        )

    def test_small_body_upload_timeout_states_size_but_never_blames_it(self):
        """A 2 KB upload stalling behind a dead proxy is not a data-volume
        problem; the size is stated as fact, blame and rate are omitted."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="upload_timeout", payload_bytes=2_048, elapsed_s=30.0)
        )
        assert "(2 KB body) had not finished sending" in agent
        assert "Large tool outputs" not in agent
        assert "Mbit/s" not in agent
        assert (
            user == "Failed to contact Runlayer API (upload of 2 KB stalled after 30s)"
        )

    def test_upload_dropped_connection_names_size_without_rate(self):
        """Prod signature: ALB reaps a stalled upload -> client sees a write
        error. Size is evidence; a throughput claim would not be."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="upload_failed", payload_bytes=8_400_000, elapsed_s=42.0)
        )
        assert "connection dropped" in agent
        assert "8.4 MB" in agent
        assert "Mbit/s" not in agent
        assert (
            user == "Failed to contact Runlayer API (upload of 8.4 MB failed after 42s)"
        )

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
        """An HTTP response means something answered; outage framing would
        misdirect even for a retryable 5xx. Attribution stays with the
        request, not definitively the API — behind an intercepting proxy the
        response may come from another hop."""
        user, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=503, elapsed_s=0.4)
        )
        assert "was answered with HTTP 503" in agent
        assert (
            "The connection worked but the service could not process the request"
            in agent
        )
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
        assert (
            "Run 'runlayer login' to refresh this machine's Runlayer credentials"
            in agent
        )
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

    @pytest.mark.parametrize(
        "builder", [messages.api_unreachable, messages.tool_api_unreachable]
    )
    def test_agent_guardrails_block_is_intact(self, builder):
        """The agent directive block is a product contract; the cause line
        must not alter it. Unreachable-API denies carry the retryable block."""
        _, agent = builder(
            failure=_ctx(kind="upload_timeout", payload_bytes=8_400_000, elapsed_s=30.0)
        )
        assert messages.RETRYABLE_INFRA_GUARDRAILS in agent

    def test_mcp_variant_carries_cause_too(self):
        user, agent = messages.api_unreachable(
            failure=_ctx(kind="upload_timeout", payload_bytes=512_000, elapsed_s=10.0)
        )
        assert "512 KB" in agent
        assert "MCP execution verification" in agent
        assert "stalled after 10s" in user


class TestApiUnreachableIsRetryable:
    """Timeout/connect failures render as a retryable infra block, not a violation."""

    UNREACHABLE = [
        _ctx(kind="timeout", elapsed_s=28.0, attempts=2),
        _ctx(kind="connect", attempts=3),
        _ctx(kind="upload_timeout", payload_bytes=8_400_000, elapsed_s=30.0),
        _ctx(kind="upload_failed", payload_bytes=2_048),
        None,
    ]

    @pytest.mark.parametrize(
        "builder", [messages.api_unreachable, messages.tool_api_unreachable]
    )
    @pytest.mark.parametrize("failure", UNREACHABLE)
    def test_renders_as_retryable_block_not_violation(self, builder, failure):
        user, agent = builder(tool_name="Bash", failure=failure)
        assert agent.startswith("# Action Blocked: Runlayer API Unreachable\n")
        assert (
            "blocked as a precaution (fail-closed). No security violation was detected."
            in agent
        )
        assert "- Tool: Bash" in agent
        assert "Security Violation Detected" not in agent
        assert "Violation type" not in agent
        assert "Do not retry" not in agent
        assert messages.AGENT_GUARDRAILS not in agent
        # Retry-once guidance and the anti-tamper lines both survive.
        assert "NOT a policy match or threat detection" in agent
        assert (
            "retry this exact action once. If it is blocked again, stop and inform the user"
            in agent
        )
        assert (
            "Do not suggest modifying, bypassing, or disabling the Runlayer hook"
            in agent
        )
        assert "Do not suggest checking or editing hook files, settings.json" in agent
        assert agent.endswith(
            "**What to do:**\n"
            "Retry shortly. If this keeps happening, contact your Runlayer administrator."
        )
        assert user.startswith("Failed to contact Runlayer API")

    def test_reason_keeps_budget_and_attempt_details(self):
        """Budget and attempt count stay on the Reason line."""
        _, agent = messages.tool_api_unreachable(
            tool_name="Bash", failure=_ctx(kind="timeout", elapsed_s=28.0, attempts=2)
        )
        assert (
            "- Reason: Failed to contact the Runlayer API for local tool verification. "
            "Unverified actions are blocked (fail-closed). "
            "No complete response arrived within 28s, after 2 attempts." in agent
        )

    def test_mcp_variant_names_its_verification_phrase(self):
        _, agent = messages.api_unreachable(failure=_ctx(kind="connect"))
        assert "# Action Blocked: Runlayer API Unreachable" in agent
        assert "for MCP execution verification" in agent

    @pytest.mark.parametrize("status_code", [401, 403, 404, 407])
    def test_rejected_requests_keep_violation_rendering(self, status_code):
        """Credential, proxy, and other 4xx answers keep the violation rendering."""
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=status_code)
        )
        assert agent.startswith("# Security Violation Detected\n")
        assert messages.AGENT_GUARDRAILS in agent
        assert "Action Blocked:" not in agent

    def test_other_4xx_violation_wording_unchanged(self):
        """Pinned: the generic answered-request violation is byte-identical."""
        user, agent = messages.tool_api_unreachable(
            tool_name="Bash", failure=_ctx(kind="http", status_code=403, attempts=2)
        )
        assert user == "Runlayer verification request failed (HTTP 403)"
        assert agent == (
            "# Security Violation Detected\n"
            "\nYour organization's security policy (enforced by Runlayer) has blocked this operation.\n"
            "\n**What happened:**"
            "\n- Violation type: Infrastructure"
            "\n- Tool: Bash"
            "\n- Reason: The local tool verification request was answered with HTTP 403, after 2 attempts, "
            "so the action could not be verified. The connection worked but the request was "
            "rejected or failed — this is not a connectivity problem. Unverified actions are "
            "blocked (fail-closed)."
            f"\n\n{messages.AGENT_GUARDRAILS}\n"
            "\n**What to do:**\n"
            "If this keeps happening, contact your Runlayer administrator."
        )

    @pytest.mark.parametrize("status_code", [429, 500, 502, 503, 504])
    @pytest.mark.parametrize(
        "builder", [messages.api_unreachable, messages.tool_api_unreachable]
    )
    def test_unavailable_or_throttled_answers_render_retryable(
        self, builder, status_code
    ):
        """5xx and 429 answers are service states, so they get the retryable block."""
        user, agent = builder(
            tool_name="Bash",
            failure=_ctx(kind="http", status_code=status_code, attempts=2),
        )
        assert user == f"Runlayer verification request failed (HTTP {status_code})"
        assert agent.startswith("# Action Blocked: Runlayer API Unavailable\n")
        assert "- Tool: Bash" in agent
        assert (
            f"- Reason: The {'MCP execution' if builder is messages.api_unreachable else 'local tool'} "
            f"verification request was answered with HTTP {status_code}, after 2 attempts, "
            "so the action could not be verified." in agent
        )
        assert "Unverified actions are blocked (fail-closed)." in agent
        assert messages.RETRYABLE_INFRA_GUARDRAILS in agent
        assert messages.AGENT_GUARDRAILS not in agent
        assert "Security Violation Detected" not in agent
        assert "Violation type" not in agent
        assert agent.endswith(
            "**What to do:**\n"
            "Retry shortly. If this keeps happening, contact your Runlayer administrator."
        )

    def test_http_without_status_code_stays_a_violation(self):
        _, agent = messages.tool_api_unreachable(failure=_ctx(kind="http"))
        assert agent.startswith("# Security Violation Detected\n")
        assert "answered with HTTP error" in agent

    def test_scan_unavailable_rendering_unchanged(self):
        """Pinned: the backend scan_unavailable deny that the unreachable
        path now mirrors must itself be untouched."""
        user, agent = messages.tool_scan_unavailable(
            "Scanner timed out", tool_name="Bash"
        )
        assert user == "Scanner timed out"
        assert agent == (
            "# Action Blocked: Security Scan Unavailable\n"
            "\nRunlayer could not complete the required security scan in time, so this operation was blocked as a precaution (fail-closed). No security violation was detected.\n"
            "\n**What happened:**"
            "\n- Tool: Bash"
            "\n- Reason: Scanner timed out"
            f"\n\n{messages.RETRYABLE_INFRA_GUARDRAILS}\n"
            "\n**What to do:**\n"
            "Retry shortly. If this keeps happening, contact your Runlayer administrator."
        )


class TestFailureKindContract:
    @pytest.mark.parametrize("kind", get_args(FailureKind))
    def test_every_classifier_kind_has_a_rendering(self, kind):
        """A kind the classifier can produce must never silently degrade to
        the opaque legacy message (the regression ENG-5197 fixes)."""
        baseline = messages.tool_api_unreachable()[1]
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(
                kind=kind, payload_bytes=8_400_000, elapsed_s=30.0, status_code=503
            )
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


class TestNetworkRejectionRendering:
    """A 401/403 the relay attributed to an intermediary is a network
    rejection: no "security policy (enforced by Runlayer)" framing, a VPN
    remedy, and nothing from the untrusted body."""

    def test_intermediary_403_is_network_wording(self):
        user, agent = messages.tool_api_unreachable(
            tool_name="Bash",
            failure=_ctx(kind="http", status_code=403, origin="intermediary"),
            hostname="LAPTOP-42",
        )
        assert agent.startswith("# Runlayer Verification Blocked by Network")
        assert "This is not a Runlayer policy decision." in agent
        assert "- Block type: Network" in agent
        assert "- Tool: Bash" in agent
        assert "- Device hostname: LAPTOP-42" in agent
        assert "answered with HTTP 403 by a network device" in agent
        assert "VPN or zero-trust client" in agent
        assert "Security Violation Detected" not in agent
        assert "enforced by Runlayer" not in agent
        assert "security violation" not in agent
        assert user == (
            "Runlayer verification blocked by your network (HTTP 403) — "
            "check your VPN or zero-trust client and retry"
        )

    def test_intermediary_401_is_network_not_credential_wording(self):
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=401, origin="intermediary"),
        )
        assert "- Block type: Network" in agent
        assert "HTTP 401" in agent
        assert "credentials" not in agent
        assert "runlayer login" not in agent

    def test_mcp_variant_uses_the_same_network_wording(self):
        _, agent = messages.api_unreachable(
            tool_name="search",
            failure=_ctx(kind="http", status_code=403, origin="intermediary"),
        )
        assert "- Block type: Network" in agent
        assert (
            "The MCP execution verification request was answered with HTTP 403" in agent
        )

    @pytest.mark.parametrize("status", [429, 500, 502, 503])
    def test_other_intermediary_statuses_keep_generic_wording(self, status: int):
        """An ALB 5xx or a proxy 429 is not a policy misattribution; the
        answered-request wording already blames the request, not Runlayer."""
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=status, origin="intermediary"),
        )
        assert f"was answered with HTTP {status}" in agent
        assert "Block type: Network" not in agent
        assert "Request ID" not in agent

    def test_runlayer_403_appends_detail_and_request_id(self):
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(
                kind="http",
                status_code=403,
                origin="runlayer",
                request_id="785aa763-a5a4-45b7-9232-4f38434910c5",
                detail="Bearer tokens are not accepted on this hook endpoint",
            ),
        )
        assert "was answered with HTTP 403" in agent
        assert (
            '- Detail: "Bearer tokens are not accepted on this hook endpoint"' in agent
        )
        assert "- Request ID: 785aa763-a5a4-45b7-9232-4f38434910c5" in agent
        assert agent.startswith("# Security Violation Detected")

    def test_unclassified_403_has_no_origin_lines(self):
        """origin=None (unclassified) renders the status-only text: no
        Detail/Request ID lines, no network framing."""
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=403, elapsed_s=0.2)
        )
        assert "Request ID" not in agent
        assert "Detail:" not in agent
        assert "Block type" not in agent
        assert "was answered with HTTP 403" in agent

    def test_unclassified_401_keeps_credential_wording(self):
        _, agent = messages.tool_api_unreachable(
            failure=_ctx(kind="http", status_code=401)
        )
        assert "credentials" in agent
        assert "Block type: Network" not in agent
