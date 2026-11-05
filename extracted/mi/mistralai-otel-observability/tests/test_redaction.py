"""Built-in operation redaction policy tests."""

import json
import re
from collections.abc import Generator
from contextlib import contextmanager

import pytest
from conftest import SDKHarness, histogram_points, metrics_by_name, point_attributes

from mistralai.observability.otel import (
    CARD_NUMBER_PATTERN,
    DEFAULT_PII_SECRET_PATTERNS,
    DEFAULT_SAFE_ATTRIBUTE_KEYS,
    DEFAULT_TOKEN_PATTERNS,
    EMAIL_PATTERN,
    IPV4_PATTERN,
    AttributeRedactionPolicy,
    CallbackRedactionPolicy,
    OperationDataContext,
    OperationDataTransformer,
    OperationDataValue,
    RegexRedactionPolicy,
)
from mistralai.observability.otel import semconv_constants as c


def _synthetic_secret(*parts: str) -> str:
    """Build non-secret test fixtures without tripping repository scanners."""
    return "".join(parts)


def _transform(
    policy: OperationDataTransformer,
    value: OperationDataValue,
    *,
    field: str = "custom",
) -> OperationDataValue | None:
    return policy.transform(
        value,
        context=OperationDataContext(operation_name="chat", signal="span", field=field),
    )


@contextmanager
def _configured_sdk(*transformers: OperationDataTransformer) -> Generator[SDKHarness]:
    harness = SDKHarness(operation_data_transformers=transformers)
    try:
        yield harness
    finally:
        harness.shutdown()


def test_attribute_policy_redacts_exception_content_before_recording() -> None:
    """The conservative policy should hide exception content but retain its type."""
    with _configured_sdk(AttributeRedactionPolicy()) as harness:
        with pytest.raises(RuntimeError, match="sensitive"), harness.observability.operation("chat"):
            message = "sensitive failure"
            raise RuntimeError(message)

        harness.observability.flush()
        span = harness.span_exporter.get_finished_spans()[0]
        event_attributes = dict(span.events[0].attributes or {})

        assert span.status.description == "[REDACTED]"
        assert event_attributes[c.ATTR_EXCEPTION_MESSAGE] == "[REDACTED]"
        assert event_attributes[c.ATTR_EXCEPTION_STACKTRACE] == "[REDACTED]"
        assert event_attributes[c.ATTR_EXCEPTION_TYPE] == "RuntimeError"


@pytest.mark.parametrize(
    ("policy", "description"),
    [
        (AttributeRedactionPolicy(), "[REDACTED]"),
        (RegexRedactionPolicy(patterns=[re.compile("sensitive")]), "[REDACTED] failure"),
    ],
    ids=["strict", "regex"],
)
def test_redaction_policies_apply_to_payload_error_descriptions(
    policy: OperationDataTransformer, description: str
) -> None:
    """Returned failures use the same status redaction policies as raised exceptions."""
    with _configured_sdk(policy) as harness:
        operation = harness.observability.tool("lookup")
        operation.start(set_current_context=False)
        operation.end(error_type="rejected", error_message="sensitive failure")

        harness.observability.flush()
        [span] = harness.span_exporter.get_finished_spans()
        assert span.status.description == description
        assert dict(span.attributes or {})[c.ATTR_ERROR_TYPE] == "rejected"


@pytest.mark.parametrize(
    "secret",
    [
        pytest.param(_synthetic_secret("AKIA", "IOSFODNN7EXAMPLE"), id="aws-access-key"),
        pytest.param(
            _synthetic_secret("AIza", "abcdefghijklmnopqrstuvwxyz012345678"),
            id="google-api-key",
        ),
        pytest.param(
            _synthetic_secret("eyJhbGciOiJIUzI1NiJ9.", "eyJzdWIiOiIxMjM0NTY3ODkwIn0.abc123"),
            id="jwt",
        ),
        pytest.param(_synthetic_secret("-----BEGIN RSA ", "PRIVATE KEY-----"), id="private-key"),
        pytest.param(_synthetic_secret("sk_live_", "0123456789abcdefghij"), id="stripe-secret-key"),
        pytest.param(
            _synthetic_secret("sk-ant-api03-", "abcdefghijklmnop", "qrstuvwxyz012345"),
            id="anthropic-api-key",
        ),
        pytest.param(
            _synthetic_secret("hf_", "abcdefghijklmnopqrstuvwxyz0123456789"),
            id="hugging-face-token",
        ),
        pytest.param(
            _synthetic_secret("mstrl_", "0123456789abcdefghijklmnopqrstuv", "_ABCDEF"),
            id="mistral-api-key",
        ),
        pytest.param(
            _synthetic_secret("github_pat_", "abcdefghijklmnopqrstuvwxyz"),
            id="github-pat",
        ),
        pytest.param(_synthetic_secret("glpat-", "abcdefghij0123456789ab"), id="gitlab-pat"),
        pytest.param(
            _synthetic_secret("shpat_", "0123456789abcdef0123456789abcdef"),
            id="shopify-token",
        ),
        pytest.param(_synthetic_secret("sq0atp-", "0123456789abcdefghijkl"), id="square-token"),
        pytest.param(_synthetic_secret("PMAK-", "0123456789abcdefghijklmn"), id="postman-key"),
        pytest.param(
            _synthetic_secret("phc_", "abcdefghijklmnopqrstuvwxyz0123456789abcdefg"),
            id="posthog-token",
        ),
        pytest.param(
            _synthetic_secret("SG.abcdefghijklmnopqrstuv.", "abcdefghijklmnopqrstuvwxyz0123456789abcdefg"),
            id="sendgrid-key",
        ),
        pytest.param(_synthetic_secret("pk_live_", "0123456789abcdefghijklmn"), id="stripe-public-key"),
        pytest.param(
            _synthetic_secret(
                "https://hooks.slack.com/services/",
                "T00000000/B00000000/abcdefghijklmnopqrstuvwx",
            ),
            id="slack-webhook",
        ),
    ],
)
def test_default_regex_policy_redacts_secret_catalog(secret: str) -> None:
    """The default regex policy should redact every supported secret format."""
    transformed = _transform(
        RegexRedactionPolicy(),
        {"nested": [f"leak {secret} here"]},
    )

    assert secret not in str(transformed)
    assert "[REDACTED]" in str(transformed)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("reach me at raquel@example.com", "reach me at [REDACTED]", id="email"),
        pytest.param("card 4111-1111-1111-1111", "card [REDACTED]", id="card-number"),
        pytest.param("host 192.168.1.42", "host [REDACTED]", id="ipv4-address"),
    ],
)
def test_default_regex_policy_redacts_pii_catalog(value: str, expected: str) -> None:
    """The default regex policy should redact every supported PII format."""
    assert _transform(RegexRedactionPolicy(), value) == expected


@pytest.mark.parametrize(
    "field",
    [
        c.ATTR_GEN_AI_AGENT_ID,
        c.ATTR_GEN_AI_CONVERSATION_ID,
        c.ATTR_GEN_AI_DATA_SOURCE_ID,
        c.ATTR_GEN_AI_MEMORY_STORE_ID,
        c.ATTR_GEN_AI_MEMORY_RECORD_ID,
        c.ATTR_GEN_AI_RESPONSE_ID,
        c.ATTR_GEN_AI_TOOL_CALL_ID,
        "mistral.connector.id",
        "mistral.conversation.parent.id",
        "mistral.turn.id",
        "mistral.vibe_work.connector.id",
    ],
)
def test_default_regex_policy_preserves_card_like_ids_in_safe_keys(field: str) -> None:
    """Ids whose digit runs look like card numbers should reach the backend intact."""
    identifier = "93436555-6574-4404-bdb9-43bde50280d2"

    assert _transform(RegexRedactionPolicy(), identifier, field=field) == identifier
    assert _transform(RegexRedactionPolicy(), identifier) == "[REDACTED]bdb9-43bde50280d2"


@pytest.mark.parametrize("version", ["1.2.3.4", "20261028081500"])
def test_default_regex_policy_preserves_agent_versions(version: str) -> None:
    """Dotted and timestamp versions should not look like IPs or card numbers."""
    assert _transform(RegexRedactionPolicy(), version, field=c.ATTR_GEN_AI_AGENT_VERSION) == version
    assert _transform(RegexRedactionPolicy(), version) == "[REDACTED]"


@pytest.mark.parametrize("field", sorted(DEFAULT_SAFE_ATTRIBUTE_KEYS))
def test_default_regex_policy_still_scans_safe_keys_for_tokens(field: str) -> None:
    """Safe keys skip PII patterns only, so a secret pasted into an id is still removed."""
    secret = _synthetic_secret("Bearer ", "abc.def")

    assert _transform(RegexRedactionPolicy(), secret, field=field) == "[REDACTED]"


def test_default_regex_policy_redacts_bytes_before_otel_normalization() -> None:
    """Byte values should not bypass the regex policy before OTel decodes them."""
    secret = _synthetic_secret("Bearer ", "abc.def")

    assert _transform(RegexRedactionPolicy(), secret.encode()) == "[REDACTED]"
    assert _transform(AttributeRedactionPolicy(), secret.encode(), field=c.ATTR_GEN_AI_REQUEST_MODEL) == "[REDACTED]"


def test_regex_redaction_is_enabled_by_default() -> None:
    """SDK configuration should redact known patterns unless explicitly disabled."""
    secret = _synthetic_secret("Bearer ", "abc.def")
    harness = SDKHarness()
    try:
        with harness.observability.operation("chat") as operation:
            operation.log(secret)

        harness.observability.flush()
        assert harness.log_exporter.get_finished_logs()[0].log_record.body == "[REDACTED]"
    finally:
        harness.shutdown()


def test_default_regex_redaction_can_be_disabled_explicitly() -> None:
    """An explicit empty transformer sequence should preserve raw operation data."""
    secret = _synthetic_secret("Bearer ", "abc.def")
    harness = SDKHarness(operation_data_transformers=())
    try:
        with harness.observability.operation("chat") as operation:
            operation.log(secret)

        harness.observability.flush()
        assert harness.log_exporter.get_finished_logs()[0].log_record.body == secret
    finally:
        harness.shutdown()


def test_default_regex_policy_does_not_guess_free_form_passwords() -> None:
    """The content-oriented policy should not imply semantic secret detection."""
    value = "Hello, my password is dsa8f7sdi8972-."

    assert _transform(RegexRedactionPolicy(), value, field=c.ATTR_GEN_AI_INPUT_MESSAGES) == value


def test_attribute_policy_redacts_sensitive_structured_fields_wholesale() -> None:
    """The conservative policy should hide free-form secrets in content fields."""
    policy = AttributeRedactionPolicy()

    transformed = _transform(
        policy,
        [{"role": "user", "content": "Hello, my password is dsa8f7sdi8972-."}],
        field=c.ATTR_GEN_AI_INPUT_MESSAGES,
    )

    assert transformed == "[REDACTED]"
    assert _transform(policy, None, field=c.ATTR_GEN_AI_INPUT_MESSAGES) is None


def test_attribute_policy_preserves_safe_fields_and_scans_tokens() -> None:
    """Safe metadata should remain useful while known tokens are still removed."""
    policy = AttributeRedactionPolicy()

    assert _transform(policy, "mistral-large", field=c.ATTR_GEN_AI_REQUEST_MODEL) == "mistral-large"
    assert _transform(policy, "Bearer abc.def", field=c.ATTR_GEN_AI_REQUEST_MODEL) == "[REDACTED]"


def test_attribute_policy_preserves_system_instruction_strings() -> None:
    """System prompts should remain visible while known tokens are still scanned."""
    system_prompt = "You are a helpful assistant."
    prompt_with_token = "Use Bearer abc.def to authenticate."
    policy = AttributeRedactionPolicy()

    assert _transform(policy, system_prompt, field=c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS) == system_prompt
    assert _transform(policy, prompt_with_token, field=c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS) == (
        "Use [REDACTED] to authenticate."
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        (c.ATTR_GEN_AI_TOKEN_TYPE, c.TOKEN_TYPE_INPUT),
        (c.ATTR_GEN_AI_OUTPUT_TYPE, "text"),
        (c.ATTR_GEN_AI_PROMPT_NAME, "customer-support"),
        (c.ATTR_GEN_AI_PROMPT_VERSION, "v2"),
        (c.ATTR_GEN_AI_REQUEST_MAX_TOKENS, 512),
        ("mistral.obs.features.judge", ("toxicity", "groundedness")),
    ],
)
def test_attribute_policy_preserves_sdk_metadata(field: str, value: str | int | tuple[str, ...]) -> None:
    """SDK metadata should not be redacted because its key contains a sensitive fragment."""
    assert _transform(AttributeRedactionPolicy(), value, field=field) == value


def test_attribute_policy_redacts_request_stop_sequences() -> None:
    """Stop sequences may contain user-controlled request content."""
    assert (
        _transform(
            AttributeRedactionPolicy(),
            ("customer-secret",),
            field=c.ATTR_GEN_AI_REQUEST_STOP_SEQUENCES,
        )
        == "[REDACTED]"
    )


def test_attribute_policy_keeps_token_metric_series_distinct() -> None:
    """Metric attributes should be redacted without merging input and output series."""
    redactor = RegexRedactionPolicy([re.compile("secret")])
    with _configured_sdk(redactor, AttributeRedactionPolicy()) as harness:
        with harness.observability.operation("chat") as operation:
            operation.token_usage(input_tokens=3, output_tokens=5, attributes={"custom.metric": "metric-secret"})

        harness.observability.flush()
        metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
        token_points = histogram_points(metrics[c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE])

        assert {point_attributes(point)[c.ATTR_GEN_AI_TOKEN_TYPE]: point.sum for point in token_points} == {
            c.TOKEN_TYPE_INPUT: 3,
            c.TOKEN_TYPE_OUTPUT: 5,
        }
        assert all(point_attributes(point)["custom.metric"] == "metric-[REDACTED]" for point in token_points)


def test_attribute_policy_preserves_span_names_and_redacts_status_descriptions() -> None:
    """The conservative policy should preserve span names and hide error descriptions."""
    policy = AttributeRedactionPolicy()

    assert _transform(policy, "chat user@example.com", field="span.name") == "chat user@example.com"
    assert _transform(policy, "failed for user@example.com", field="status.description") == "[REDACTED]"


def test_callback_policy_can_transform_or_drop_fields() -> None:
    """Callback policies should support transforming or dropping individual fields."""
    policy = CallbackRedactionPolicy(lambda key, value: None if key == "drop" else value)

    assert _transform(policy, "secret", field="drop") is None
    assert _transform(policy, "safe", field="keep") == "safe"


def test_callback_policy_preserves_span_names() -> None:
    """Callbacks should not replace SDK-controlled span names."""
    policy = CallbackRedactionPolicy(lambda key, value: f"transformed:{key}:{value}")

    assert _transform(policy, "original", field="span.name") == "original"


def test_callback_policy_redacts_failure_descriptions() -> None:
    """Callbacks see error messages, which often carry request or response content."""
    policy = CallbackRedactionPolicy(
        lambda key, value: "[REDACTED]" if key == "status.description" else value,
    )
    with _configured_sdk(policy) as harness:
        with pytest.raises(RuntimeError, match="sensitive"), harness.observability.operation("chat"):
            message = "sensitive failure"
            raise RuntimeError(message)

        harness.observability.flush()
        span = harness.span_exporter.get_finished_spans()[0]

    assert span.status.description == "[REDACTED]"


def test_individual_pii_patterns_recompose_the_defaults() -> None:
    """The exported PII patterns let a host drop one heuristic and keep the rest."""
    policy = RegexRedactionPolicy([*DEFAULT_TOKEN_PATTERNS, EMAIL_PATTERN, IPV4_PATTERN])

    assert (*DEFAULT_TOKEN_PATTERNS, EMAIL_PATTERN, CARD_NUMBER_PATTERN, IPV4_PATTERN) == DEFAULT_PII_SECRET_PATTERNS
    assert _transform(policy, "order 1234567890123 for jane.doe@example.com") == "order 1234567890123 for [REDACTED]"


def test_callback_policy_receives_whole_structured_values_by_default() -> None:
    """Without recursion, the callback receives the whole field value."""
    seen: list[OperationDataValue] = []
    policy = CallbackRedactionPolicy(lambda key, value: seen.append(value) or value)
    messages = [{"role": "user", "parts": [{"type": "text", "content": "hi"}]}]

    assert _transform(policy, messages, field=c.ATTR_GEN_AI_INPUT_MESSAGES) == messages
    assert seen == [messages]


def test_callback_policy_edits_in_place_do_not_reach_the_caller() -> None:
    """A callback that edits a structured value in place changes the recorded value, not the caller's."""

    def drop_secrets(_key: str, value: OperationDataValue) -> OperationDataValue:
        if isinstance(value, dict):
            value.pop("secret", None)
            if isinstance(account := value.get("account"), dict):
                account.pop("secret", None)
        return value

    policy = CallbackRedactionPolicy(drop_secrets)
    result = {"secret": "s3cr3t", "account": {"id": "acct-42", "secret": "s3cr3t"}}

    assert _transform(policy, result, field=c.ATTR_GEN_AI_TOOL_CALL_RESULT) == {"account": {"id": "acct-42"}}
    assert result == {"secret": "s3cr3t", "account": {"id": "acct-42", "secret": "s3cr3t"}}


def test_recursive_callback_policy_masks_and_drops_nested_leaves() -> None:
    """A recursive callback rewrites or drops each leaf, decoded from bytes, and keeps existing ``None`` values."""
    keys: set[str] = set()

    def mask(key: str, value: OperationDataValue) -> OperationDataValue | None:
        keys.add(key)
        if value == "drop me":
            return None
        return value.replace("ACME-42", "[REDACTED]") if isinstance(value, str) else value

    policy = CallbackRedactionPolicy(mask, recursive=True)
    messages = [
        {"role": "user", "parts": [{"type": "text", "content": "ticket ACME-42"}, "drop me", b"bytes ACME-42"]},
        {"role": "assistant", "parts": ({"type": "text", "content": None, "tokens": 3},)},
    ]

    assert _transform(policy, messages, field=c.ATTR_GEN_AI_INPUT_MESSAGES) == [
        {"role": "user", "parts": [{"type": "text", "content": "ticket [REDACTED]"}, "bytes [REDACTED]"]},
        {"role": "assistant", "parts": ({"type": "text", "content": None, "tokens": 3},)},
    ]
    assert _transform(policy, "drop me", field="custom") is None
    assert keys == {c.ATTR_GEN_AI_INPUT_MESSAGES, "custom"}


def test_recursive_callback_policy_masks_message_text_on_spans() -> None:
    """A recursive callback reaches message text before the SDK serializes it."""
    policy = CallbackRedactionPolicy(
        lambda key, value: value.replace("ACME-42", "[REDACTED]") if isinstance(value, str) else value,
        recursive=True,
    )
    with _configured_sdk(policy) as harness:
        with harness.observability.operation("chat", include_content=True) as operation:
            operation.completion(input_messages=[{"role": "user", "content": "ticket ACME-42"}])

        harness.observability.flush()
        span = harness.span_exporter.get_finished_spans()[0]

    assert json.loads(str(dict(span.attributes or {})[c.ATTR_GEN_AI_INPUT_MESSAGES])) == [
        {"content": "ticket [REDACTED]", "role": "user"}
    ]


def test_builtin_policies_satisfy_the_transformer_protocol_at_runtime() -> None:
    """Hosts can check a policy with ``isinstance`` instead of duck typing."""
    for policy in (RegexRedactionPolicy(), AttributeRedactionPolicy(), CallbackRedactionPolicy(lambda _k, v: v)):
        assert isinstance(policy, OperationDataTransformer)

    def mask(_key: str, value: OperationDataValue) -> OperationDataValue:
        return value

    assert not isinstance(mask, OperationDataTransformer)
