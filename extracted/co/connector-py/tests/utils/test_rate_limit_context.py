"""Tests for connector.utils.rate_limit_context."""

import pytest
from connector.utils.rate_limit_context import (
    RATE_LIMIT_CONTEXT,
    RATE_LIMIT_RESULT_CONTEXT,
    RateLimitExecutionContext,
)
from connector_sdk_types.generated import (
    RateLimitMode,
    RateLimitStateSnapshot,
    StandardCapabilityName,
)


class TestRateLimitExecutionContext:
    def test_required_fields_only(self):
        ctx = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=None,
        )
        assert ctx.capability_name == StandardCapabilityName.LIST_ACCOUNTS
        assert ctx.capability_level == "read"
        assert ctx.caller_override_mode is None

    def test_optional_fields_default_to_none(self):
        ctx = RateLimitExecutionContext(
            capability_name="custom_capability",
            capability_level="write",
            caller_override_mode=None,
        )
        assert ctx.capability_override_mode is None
        assert ctx.last_known_state is None
        assert ctx.deadline is None

    def test_all_fields_set(self):
        snapshot = RateLimitStateSnapshot(
            remaining=10, limit=100, window_seconds=60, current_delay=0
        )
        state_map = {"myapp": snapshot}
        ctx = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=RateLimitMode.BYPASS,
            capability_override_mode=RateLimitMode.ENFORCE,
            last_known_state=state_map,
            deadline=9999.0,
        )
        assert ctx.caller_override_mode == RateLimitMode.BYPASS
        assert ctx.capability_override_mode == RateLimitMode.ENFORCE
        assert ctx.last_known_state == state_map
        assert ctx.deadline == 9999.0

    def test_accepts_string_capability_name(self):
        ctx = RateLimitExecutionContext(
            capability_name="my_custom_cap",
            capability_level="write",
            caller_override_mode=None,
        )
        assert ctx.capability_name == "my_custom_cap"

    def test_frozen_prevents_mutation(self):
        ctx = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=None,
        )
        with pytest.raises((AttributeError, TypeError)):
            ctx.capability_level = "write"  # type: ignore[misc]

    def test_equality(self):
        ctx1 = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=None,
        )
        ctx2 = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=None,
        )
        assert ctx1 == ctx2

    def test_inequality_on_different_level(self):
        ctx1 = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=None,
        )
        ctx2 = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="write",
            caller_override_mode=None,
        )
        assert ctx1 != ctx2


class TestRateLimitContextVar:
    def test_default_is_none(self):
        token = RATE_LIMIT_CONTEXT.set(None)
        try:
            assert RATE_LIMIT_CONTEXT.get() is None
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    def test_can_set_and_get_context(self):
        ctx = RateLimitExecutionContext(
            capability_name=StandardCapabilityName.LIST_ACCOUNTS,
            capability_level="read",
            caller_override_mode=None,
        )
        token = RATE_LIMIT_CONTEXT.set(ctx)
        try:
            assert RATE_LIMIT_CONTEXT.get() == ctx
        finally:
            RATE_LIMIT_CONTEXT.reset(token)

    def test_context_var_name(self):
        assert RATE_LIMIT_CONTEXT.name == "rate_limit_context"


class TestRateLimitResultContextVar:
    def test_default_is_none(self):
        token = RATE_LIMIT_RESULT_CONTEXT.set(None)
        try:
            assert RATE_LIMIT_RESULT_CONTEXT.get() is None
        finally:
            RATE_LIMIT_RESULT_CONTEXT.reset(token)

    def test_can_set_and_get_state_map(self):
        snapshot = RateLimitStateSnapshot(remaining=5, limit=50, window_seconds=30, current_delay=1)
        state_map = {"myapp": snapshot}
        token = RATE_LIMIT_RESULT_CONTEXT.set(state_map)
        try:
            assert RATE_LIMIT_RESULT_CONTEXT.get() == state_map
        finally:
            RATE_LIMIT_RESULT_CONTEXT.reset(token)

    def test_context_var_name(self):
        assert RATE_LIMIT_RESULT_CONTEXT.name == "rate_limit_result_context"
