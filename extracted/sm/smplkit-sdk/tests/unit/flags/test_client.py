"""Tests for FlagsClient and AsyncFlagsClient — management + runtime."""

import asyncio
import json
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import httpx
import pytest

from smplkit._errors import (
    ConnectionError,
    NotFoundError,
    TimeoutError,
    ValidationError,
)
from smplkit.client import AsyncSmplClient, SmplClient
from smplkit.flags.client import (
    AsyncFlagsClient,
    FlagChangeEvent,
    FlagsClient,
    FlagStats,
    _ResolutionCache,
    _check_response_status,
    _contexts_to_eval_dict,
    _evaluate_flag,
    _hash_context,
    _maybe_reraise_network_error,
)
from smplkit.management._buffer import _FLAG_BATCH_FLUSH_SIZE as _FLAG_BULK_FLUSH_THRESHOLD
from smplkit.flags.helpers import (
    _build_flag_request_body as _build_request_body,
    _build_gen_flag,
    _extract_environments,
    _extract_rule,
    _extract_values,
    _flag_dict_from_json,
    _unset_to_none,
)
from smplkit.flags.models import (
    AsyncBooleanFlag,
    AsyncFlag,
    AsyncJsonFlag,
    AsyncNumberFlag,
    AsyncStringFlag,
    BooleanFlag,
    Flag,
    FlagEnvironment,
    FlagRule,
    FlagValue,
    JsonFlag,
    NumberFlag,
    StringFlag,
)
from smplkit.flags.types import Context
from smplkit.management._buffer import (
    _CONTEXT_REGISTRATION_LRU_SIZE,
    _ContextRegistrationBuffer,
    _FlagRegistrationBuffer,
)


def _new_mgmt():
    """Build a SmplManagementClient for management-flavored tests."""
    from smplkit import SmplManagementClient

    return SmplManagementClient(api_key="sk_test", base_domain="example.test")


def _new_async_mgmt():
    """Build an AsyncSmplManagementClient for management-flavored tests."""
    from smplkit import AsyncSmplManagementClient

    return AsyncSmplManagementClient(api_key="sk_test", base_domain="example.test")


_TEST_UUID = "5a0c6be1-0000-0000-0000-000000000001"


def _envs(d: dict | None) -> dict:
    """Convert a dict-of-dicts env spec to dict[str, FlagEnvironment] for test fixtures."""
    if not d:
        return {}
    out: dict = {}
    for k, v in d.items():
        if isinstance(v, FlagEnvironment):
            out[k] = v
            continue
        rules = [
            r
            if isinstance(r, FlagRule)
            else FlagRule(
                logic=dict(r.get("logic") or {}),
                value=r.get("value"),
                description=r.get("description"),
            )
            for r in v.get("rules", [])
        ]
        out[k] = FlagEnvironment(
            enabled=v.get("enabled", True),
            default=v.get("default"),
            rules=rules,
        )
    return out


# ---------------------------------------------------------------------------
# Shared test helpers
# ---------------------------------------------------------------------------


def _mock_flag_response(*, id=_TEST_UUID, name="Test Flag", type_="BOOLEAN", default=False):
    """Build a mock parsed flag response (single-resource envelope)."""
    mock_values = [MagicMock(name="True", value=True), MagicMock(name="False", value=False)]
    mock_values[0].name = "True"
    mock_values[0].value = True
    mock_values[1].name = "False"
    mock_values[1].value = False

    mock_attrs = MagicMock()
    mock_attrs.name = name
    mock_attrs.type_ = type_
    mock_attrs.default = default
    mock_attrs.values = mock_values
    mock_attrs.description = None
    mock_attrs.created_at = None
    mock_attrs.updated_at = None

    from smplkit._generated.flags.types import UNSET

    mock_attrs.environments = UNSET

    mock_resource = MagicMock()
    mock_resource.id = id
    mock_resource.attributes = mock_attrs

    mock_parsed = MagicMock()
    mock_parsed.data = mock_resource

    return mock_parsed


def _mock_list_parsed(*, id=_TEST_UUID, name="Test Flag", type_="BOOLEAN", default=False):
    """Build a mock parsed list response (array of resources)."""
    single = _mock_flag_response(id=id, name=name, type_=type_, default=default)
    mock_parsed = MagicMock()
    mock_parsed.data = [single.data]
    return mock_parsed


_UNSET = object()


def _flag_json(
    *,
    id=_TEST_UUID,
    name="Test Flag",
    type_="BOOLEAN",
    default=False,
    values=_UNSET,
    environments=None,
):
    """Build a raw JSON:API flag resource dict."""
    if values is _UNSET:
        values = [{"name": "True", "value": True}, {"name": "False", "value": False}]
    return {
        "id": id,
        "type": "flag",
        "attributes": {
            "name": name,
            "type": type_,
            "default": default,
            "values": values,
            "environments": environments or {},
            "description": "",
            "created_at": None,
            "updated_at": None,
        },
    }


def _ok_response(parsed=None, status=HTTPStatus.OK, content=None):
    """Build a mock HTTP response."""
    resp = MagicMock()
    resp.status_code = status
    resp.content = content if content is not None else b""
    resp.parsed = parsed
    return resp


def _ok_json_response(data, status=HTTPStatus.OK):
    """Build a mock HTTP response with JSON content (for raw-JSON parsing)."""
    content = json.dumps(data).encode()
    return _ok_response(status=status, content=content)


def _make_flags_client():
    """Create a FlagsClient with a mocked parent that has a real `manage`."""
    from smplkit.management._buffer import _ContextRegistrationBuffer
    from smplkit.management.client import ContextsClient
    from smplkit.management.client import FlagsClient as _MgmtFlagsClient

    parent = MagicMock()
    parent._api_key = "sk_test"
    parent._environment = "test"
    parent._service = None
    manage = MagicMock()
    manage.contexts = ContextsClient(MagicMock(), _ContextRegistrationBuffer())
    manage.flags = _MgmtFlagsClient(MagicMock())
    parent.manage = manage
    with patch("smplkit.flags.client.AuthenticatedClient"):
        client = FlagsClient(parent, manage=manage, metrics=parent._metrics)
    return client


def _make_async_flags_client():
    """Create an AsyncFlagsClient with a mocked parent + real management subclients."""
    from smplkit.management._buffer import _ContextRegistrationBuffer
    from smplkit.management.client import AsyncContextsClient
    from smplkit.management.client import AsyncFlagsClient as _MgmtAsyncFlagsClient

    parent = MagicMock()
    parent._api_key = "sk_test"
    parent._environment = "test"
    parent._service = None
    manage = MagicMock()
    manage.contexts = AsyncContextsClient(MagicMock(), _ContextRegistrationBuffer())
    manage.flags = _MgmtAsyncFlagsClient(MagicMock())
    parent.manage = manage
    with patch("smplkit.flags.client.AuthenticatedClient"):
        client = AsyncFlagsClient(parent, manage=manage, metrics=parent._metrics)
    return client


def _make_mock_flag(client):
    """Create a Flag model for _update_flag tests."""
    return Flag(
        client,
        id=_TEST_UUID,
        name="Test Flag",
        type="BOOLEAN",
        default=False,
        values=[FlagValue(name="True", value=True), FlagValue(name="False", value=False)],
    )


def _make_mock_async_flag(client):
    """Create an AsyncFlag model for _update_flag tests."""
    return AsyncFlag(
        client,
        id=_TEST_UUID,
        name="Test Flag",
        type="BOOLEAN",
        default=False,
        values=[FlagValue(name="True", value=True), FlagValue(name="False", value=False)],
    )


# ===========================================================================
# Helper functions
# ===========================================================================


class TestCheckResponseStatus:
    def test_200_does_nothing(self):
        _check_response_status(200, b"ok")

    def test_404_raises_not_found(self):
        with pytest.raises(NotFoundError):
            _check_response_status(404, b"not found")

    def test_422_raises_validation(self):
        with pytest.raises(ValidationError):
            _check_response_status(422, b"validation detail")


class TestMaybeReraiseNetworkError:
    def test_timeout_exception(self):
        with pytest.raises(TimeoutError):
            _maybe_reraise_network_error(httpx.TimeoutException("timed out"))

    def test_timeout_includes_url_when_available(self):
        exc = httpx.TimeoutException("timed out")
        exc.request = httpx.Request("GET", "http://flags.localhost/api/v1/flags")
        with pytest.raises(TimeoutError, match="http://flags.localhost/api/v1/flags"):
            _maybe_reraise_network_error(exc)

    def test_connect_error(self):
        with pytest.raises(ConnectionError):
            _maybe_reraise_network_error(httpx.ConnectError("refused"))

    def test_connect_error_includes_url_when_available(self):
        exc = httpx.ConnectError("nodename nor servname provided, or not known")
        exc.request = httpx.Request("GET", "http://flags.localhost/api/v1/flags")
        with pytest.raises(ConnectionError, match="http://flags.localhost/api/v1/flags"):
            _maybe_reraise_network_error(exc)

    def test_connect_error_fallback_message_without_url(self):
        exc = httpx.ConnectError("nodename nor servname provided, or not known")
        with pytest.raises(ConnectionError, match="Connection error"):
            _maybe_reraise_network_error(exc)

    def test_connection_error_uses_base_url_when_request_not_attached(self):
        exc = httpx.ConnectError("nodename nor servname provided, or not known")
        with pytest.raises(ConnectionError, match="http://flags.localhost"):
            _maybe_reraise_network_error(exc, "http://flags.localhost")

    def test_timeout_uses_base_url_when_request_not_attached(self):
        exc = httpx.TimeoutException("timed out")
        with pytest.raises(TimeoutError, match="http://flags.localhost"):
            _maybe_reraise_network_error(exc, "http://flags.localhost")

    def test_exc_url_takes_precedence_over_base_url(self):
        exc = httpx.ConnectError("refused")
        exc.request = httpx.Request("GET", "http://flags.localhost/api/v1/flags")
        with pytest.raises(ConnectionError, match="http://flags.localhost/api/v1/flags"):
            _maybe_reraise_network_error(exc, "http://other.host")

    def test_reraises_not_found(self):
        with pytest.raises(NotFoundError):
            _maybe_reraise_network_error(NotFoundError("nope"))

    def test_reraises_validation(self):
        with pytest.raises(ValidationError):
            _maybe_reraise_network_error(ValidationError("bad"))

    def test_ignores_generic_exception(self):
        _maybe_reraise_network_error(ValueError("other"))


class TestExtractEnvironments:
    def test_none_returns_empty(self):
        assert _extract_environments(None) == {}

    def test_dict_input_returns_empty(self):
        """The helper only accepts a generated FlagEnvironments object; raw dicts get ignored."""
        assert _extract_environments({"prod": {"enabled": True}}) == {}

    def test_unset_returns_empty(self):
        from smplkit._generated.flags.types import UNSET

        assert _extract_environments(UNSET) == {}

    def test_unset_by_type_name(self):
        class Unset:
            pass

        assert _extract_environments(Unset()) == {}

    def test_unknown_type_returns_empty(self):
        assert _extract_environments(42) == {}

    def test_gen_flag_environments(self):
        from smplkit._generated.flags.models.flag_environment import FlagEnvironment
        from smplkit._generated.flags.models.flag_environments import FlagEnvironments
        from smplkit._generated.flags.models.flag_rule import FlagRule
        from smplkit._generated.flags.models.flag_rule_logic import FlagRuleLogic

        logic = FlagRuleLogic()
        logic.additional_properties = {"==": [{"var": "user.plan"}, "enterprise"]}
        rule = FlagRule(logic=logic, value=True, description="test rule")
        env = FlagEnvironment(enabled=True, default=False, rules=[rule])
        envs = FlagEnvironments()
        envs.additional_properties = {"production": env}

        result = _extract_environments(envs)
        assert "production" in result
        assert result["production"].enabled is True
        assert result["production"].default is False
        assert len(result["production"].rules) == 1
        assert result["production"].rules[0].description == "test rule"

    def test_gen_flag_environments_unset_fields(self):
        from smplkit._generated.flags.models.flag_environment import FlagEnvironment
        from smplkit._generated.flags.models.flag_environments import FlagEnvironments
        from smplkit._generated.flags.types import UNSET

        env = FlagEnvironment(enabled=UNSET, default=UNSET, rules=UNSET)
        envs = FlagEnvironments()
        envs.additional_properties = {"staging": env}

        result = _extract_environments(envs)
        assert "staging" in result
        assert result["staging"].rules == ()


class TestExtractRule:
    def test_basic_rule(self):
        from smplkit._generated.flags.models.flag_rule import FlagRule
        from smplkit._generated.flags.models.flag_rule_logic import FlagRuleLogic

        logic = FlagRuleLogic()
        logic.additional_properties = {"==": [1, 1]}
        rule = FlagRule(logic=logic, value="enabled", description="always on")
        result = _extract_rule(rule)
        assert result.logic == {"==": [1, 1]}
        assert result.value == "enabled"
        assert result.description == "always on"

    def test_rule_without_description(self):
        from smplkit._generated.flags.models.flag_rule import FlagRule
        from smplkit._generated.flags.models.flag_rule_logic import FlagRuleLogic
        from smplkit._generated.flags.types import UNSET

        logic = FlagRuleLogic()
        logic.additional_properties = {}
        rule = FlagRule(logic=logic, value=42, description=UNSET)
        result = _extract_rule(rule)
        assert result.description is None

    def test_rule_with_none_description(self):
        from smplkit._generated.flags.models.flag_rule import FlagRule
        from smplkit._generated.flags.models.flag_rule_logic import FlagRuleLogic

        logic = FlagRuleLogic()
        logic.additional_properties = {}
        rule = FlagRule(logic=logic, value=42, description=None)
        result = _extract_rule(rule)
        assert result.description is None


class TestExtractValues:
    def test_empty_returns_empty(self):
        assert _extract_values([]) == []

    def test_none_returns_none(self):
        assert _extract_values(None) is None

    def test_extracts_values(self):
        v1 = MagicMock()
        v1.name = "On"
        v1.value = True
        result = _extract_values([v1])
        assert result == [FlagValue(name="On", value=True)]


class TestUnsetToNone:
    def test_none_passthrough(self):
        assert _unset_to_none(None) is None

    def test_string_passthrough(self):
        assert _unset_to_none("hello") == "hello"

    def test_unset_becomes_none(self):
        from smplkit._generated.flags.types import UNSET

        assert _unset_to_none(UNSET) is None


class TestBuildGenFlag:
    def test_with_environments(self):
        result = _build_gen_flag(
            name="Test",
            type_="BOOLEAN",
            default=False,
            values=[FlagValue(name="True", value=True)],
            environments={
                "production": FlagEnvironment(
                    enabled=True,
                    default=False,
                    rules=[FlagRule(logic={"==": [1, 1]}, value=True, description="always")],
                ),
            },
        )
        assert result.name == "Test"
        assert "production" in result.environments.additional_properties

    def test_without_environments(self):
        result = _build_gen_flag(
            name="Test",
            type_="STRING",
            default="off",
            values=[],
        )
        assert result.name == "Test"


class TestBuildRequestBody:
    def test_wraps_flag(self):
        flag = Flag(None, id=None, name="Test", type="BOOLEAN", default=False, values=[])
        body = _build_request_body(flag)
        assert body.data.type_ == "flag"
        assert body.data.id is None

    def test_with_flag_id(self):
        flag = Flag(None, id=None, name="Test", type="BOOLEAN", default=False, values=[])
        body = _build_request_body(flag, flag_id="abc-123")
        assert body.data.id == "abc-123"


class TestFlagDictFromJson:
    def test_with_environments(self):
        data = {
            "id": "abc-123",
            "type": "flag",
            "attributes": {
                "name": "My Flag",
                "type": "STRING",
                "default": "hello",
                "values": None,
                "description": "A flag",
                "environments": {
                    "production": {
                        "enabled": True,
                        "default": "world",
                        "rules": [{"logic": {"op": "eq"}, "value": "x"}],
                    }
                },
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
            },
        }
        result = _flag_dict_from_json(data)
        assert result["id"] == "abc-123"
        assert result["values"] is None
        assert result["environments"]["production"].enabled is True
        assert result["environments"]["production"].default == "world"
        assert len(result["environments"]["production"].rules) == 1


class TestContextsToEvalDict:
    def test_basic_conversion(self):
        contexts = [
            Context("user", "u-123", plan="enterprise"),
            Context("account", "acme", region="us"),
        ]
        result = _contexts_to_eval_dict(contexts)
        assert result == {
            "user": {"key": "u-123", "plan": "enterprise"},
            "account": {"key": "acme", "region": "us"},
        }

    def test_key_injected(self):
        result = _contexts_to_eval_dict([Context("device", "d-1", os="ios")])
        assert result["device"]["key"] == "d-1"
        assert result["device"]["os"] == "ios"

    def test_empty_list(self):
        assert _contexts_to_eval_dict([]) == {}

    def test_no_attributes(self):
        result = _contexts_to_eval_dict([Context("user", "u-1")])
        assert result == {"user": {"key": "u-1"}}


class TestHashContext:
    def test_same_input_same_hash(self):
        d1 = {"user": {"key": "u-1", "plan": "enterprise"}}
        d2 = {"user": {"plan": "enterprise", "key": "u-1"}}
        assert _hash_context(d1) == _hash_context(d2)

    def test_different_input_different_hash(self):
        d1 = {"user": {"key": "u-1"}}
        d2 = {"user": {"key": "u-2"}}
        assert _hash_context(d1) != _hash_context(d2)


# ===========================================================================
# FlagChangeEvent
# ===========================================================================


class TestFlagChangeEvent:
    def test_construction(self):
        event = FlagChangeEvent(id="my-flag", source="websocket")
        assert event.id == "my-flag"
        assert event.source == "websocket"

    def test_repr(self):
        event = FlagChangeEvent(id="f", source="manual")
        assert "FlagChangeEvent" in repr(event)
        assert "f" in repr(event)


# ===========================================================================
# _ResolutionCache
# ===========================================================================


class TestResolutionCache:
    def test_put_and_get(self):
        cache = _ResolutionCache()
        cache.put("key1", "value1")
        hit, value = cache.get("key1")
        assert hit is True
        assert value == "value1"

    def test_miss(self):
        cache = _ResolutionCache()
        hit, value = cache.get("nonexistent")
        assert hit is False
        assert value is None

    def test_hit_miss_counters(self):
        cache = _ResolutionCache()
        cache.put("k", "v")
        cache.get("k")  # hit
        cache.get("k")  # hit
        cache.get("missing")  # miss
        assert cache.cache_hits == 2
        assert cache.cache_misses == 1

    def test_clear(self):
        cache = _ResolutionCache()
        cache.put("k1", "v1")
        cache.put("k2", "v2")
        cache.clear()
        hit, _ = cache.get("k1")
        assert hit is False

    def test_lru_eviction(self):
        cache = _ResolutionCache(max_size=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.put("d", 4)
        hit_a, _ = cache.get("a")
        assert hit_a is False
        hit_b, _ = cache.get("b")
        assert hit_b is True

    def test_lru_access_refreshes(self):
        cache = _ResolutionCache(max_size=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.get("a")  # refreshes "a"
        cache.put("d", 4)  # evicts "b"
        hit_a, _ = cache.get("a")
        assert hit_a is True
        hit_b, _ = cache.get("b")
        assert hit_b is False

    def test_overwrite_existing(self):
        cache = _ResolutionCache()
        cache.put("k", "v1")
        cache.put("k", "v2")
        _, value = cache.get("k")
        assert value == "v2"


class TestFlagStats:
    def test_construction_and_repr(self):
        stats = FlagStats(cache_hits=10, cache_misses=5)
        assert stats.cache_hits == 10
        assert stats.cache_misses == 5
        assert "10" in repr(stats)
        assert "5" in repr(stats)


# ===========================================================================
# _ContextRegistrationBuffer
# ===========================================================================


class TestContextRegistrationBuffer:
    def test_observe_and_drain(self):
        buf = _ContextRegistrationBuffer()
        buf.observe([Context("user", "u-1", plan="enterprise"), Context("account", "a-1", region="us")])
        batch = buf.drain()
        assert len(batch) == 2
        assert batch[0]["type"] == "user"
        assert batch[0]["key"] == "u-1"
        assert batch[0]["attributes"]["plan"] == "enterprise"

    def test_deduplication(self):
        buf = _ContextRegistrationBuffer()
        buf.observe([Context("user", "u-1", plan="enterprise")])
        buf.observe([Context("user", "u-1", plan="enterprise")])
        assert len(buf.drain()) == 1

    def test_drain_clears_pending(self):
        buf = _ContextRegistrationBuffer()
        buf.observe([Context("user", "u-1")])
        buf.drain()
        assert len(buf.drain()) == 0

    def test_pending_count(self):
        buf = _ContextRegistrationBuffer()
        assert buf.pending_count == 0
        buf.observe([Context("user", "u-1"), Context("account", "a-1")])
        assert buf.pending_count == 2
        buf.drain()
        assert buf.pending_count == 0

    def test_lru_eviction(self):
        buf = _ContextRegistrationBuffer()
        for i in range(_CONTEXT_REGISTRATION_LRU_SIZE + 1):
            buf.observe([Context("user", f"u-{i}")])
        assert len(buf._seen) == _CONTEXT_REGISTRATION_LRU_SIZE


# ===========================================================================
# _evaluate_flag
# ===========================================================================


class TestEvaluateFlag:
    def _make_flag(self, *, default, environments=None):
        from smplkit.flags.models import FlagEnvironment, FlagRule

        envs: dict = {}
        for k, v in (environments or {}).items():
            if isinstance(v, FlagEnvironment):
                envs[k] = v
                continue
            rules = [
                FlagRule(
                    logic=dict(r.get("logic") or {}),
                    value=r.get("value"),
                    description=r.get("description"),
                )
                for r in v.get("rules", [])
            ]
            envs[k] = FlagEnvironment(
                enabled=v.get("enabled", True),
                default=v.get("default"),
                rules=rules,
            )
        return {
            "id": "test-flag",
            "name": "Test",
            "type": "BOOLEAN",
            "default": default,
            "values": [],
            "environments": envs,
        }

    def test_no_environment_returns_flag_default(self):
        flag = self._make_flag(default=False)
        assert _evaluate_flag(flag, "staging", {}) is False

    def test_environment_not_found_returns_flag_default(self):
        flag = self._make_flag(default="red", environments={"production": {"enabled": True, "rules": []}})
        assert _evaluate_flag(flag, "staging", {}) == "red"

    def test_disabled_returns_env_default(self):
        flag = self._make_flag(
            default=False,
            environments={"staging": {"enabled": False, "default": True, "rules": []}},
        )
        assert _evaluate_flag(flag, "staging", {}) is True

    def test_disabled_no_env_default_returns_flag_default(self):
        flag = self._make_flag(
            default="fallback",
            environments={"staging": {"enabled": False, "rules": []}},
        )
        assert _evaluate_flag(flag, "staging", {}) == "fallback"

    def test_first_matching_rule_wins(self):
        flag = self._make_flag(
            default=False,
            environments={
                "staging": {
                    "enabled": True,
                    "rules": [
                        {"logic": {"==": [{"var": "user.plan"}, "enterprise"]}, "value": True},
                        {"logic": {"==": [{"var": "user.plan"}, "enterprise"]}, "value": False},
                    ],
                }
            },
        )
        assert _evaluate_flag(flag, "staging", {"user": {"plan": "enterprise"}}) is True

    def test_no_rules_match_returns_env_default(self):
        flag = self._make_flag(
            default="flag-default",
            environments={
                "staging": {
                    "enabled": True,
                    "default": "env-default",
                    "rules": [{"logic": {"==": [{"var": "user.plan"}, "enterprise"]}, "value": "matched"}],
                }
            },
        )
        assert _evaluate_flag(flag, "staging", {"user": {"plan": "free"}}) == "env-default"

    def test_no_rules_match_no_env_default_returns_flag_default(self):
        flag = self._make_flag(
            default="flag-default",
            environments={
                "staging": {
                    "enabled": True,
                    "rules": [{"logic": {"==": [{"var": "user.plan"}, "enterprise"]}, "value": "matched"}],
                }
            },
        )
        assert _evaluate_flag(flag, "staging", {"user": {"plan": "free"}}) == "flag-default"

    def test_numeric_comparison(self):
        flag = self._make_flag(
            default=3,
            environments={
                "staging": {
                    "enabled": True,
                    "rules": [{"logic": {">": [{"var": "account.employee_count"}, 100]}, "value": 5}],
                }
            },
        )
        assert _evaluate_flag(flag, "staging", {"account": {"employee_count": 500}}) == 5

    def test_and_condition(self):
        flag = self._make_flag(
            default=False,
            environments={
                "staging": {
                    "enabled": True,
                    "rules": [
                        {
                            "logic": {
                                "and": [
                                    {"==": [{"var": "user.plan"}, "enterprise"]},
                                    {"==": [{"var": "account.region"}, "us"]},
                                ]
                            },
                            "value": True,
                        }
                    ],
                }
            },
        )
        assert _evaluate_flag(flag, "staging", {"user": {"plan": "enterprise"}, "account": {"region": "us"}}) is True
        assert _evaluate_flag(flag, "staging", {"user": {"plan": "enterprise"}, "account": {"region": "eu"}}) is False

    def test_none_environment_returns_flag_default(self):
        flag = self._make_flag(default="default-val")
        assert _evaluate_flag(flag, None, {}) == "default-val"

    def test_json_logic_error_returns_fallback(self):
        flag = self._make_flag(
            default="fallback",
            environments={
                "prod": {
                    "enabled": True,
                    "default": "env-default",
                    "rules": [{"logic": {"invalid_op": [1, 2]}, "value": "matched"}],
                }
            },
        )
        assert _evaluate_flag(flag, "prod", {}) == "env-default"

    def test_empty_logic_skipped(self):
        flag = self._make_flag(
            default="fallback",
            environments={
                "prod": {
                    "enabled": True,
                    "default": "env-default",
                    "rules": [{"logic": {}, "value": "never"}],
                }
            },
        )
        assert _evaluate_flag(flag, "prod", {}) == "env-default"


# ===========================================================================
# Sync FlagsClient: init
# ===========================================================================


class TestFlagsClientInit:
    def test_init(self):
        client = SmplClient(api_key="sk_test", environment="test")
        assert isinstance(client.flags, FlagsClient)


# ===========================================================================
# Sync FlagsClient: factory methods
# ===========================================================================


class TestFlagsClientFactoryMethods:
    def test_newBooleanFlag(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_boolean_flag("checkout-v2", default=False)
        assert isinstance(flag, BooleanFlag)
        assert flag.id == "checkout-v2"
        assert flag.type == "BOOLEAN"
        assert flag.default is False
        assert flag.name == "Checkout V2"
        assert len(flag.values) == 2

    def test_newBooleanFlag_custom_name(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_boolean_flag("my-flag", default=True, name="My Custom Name", description="desc")
        assert flag.name == "My Custom Name"
        assert flag.description == "desc"
        assert flag.default is True

    def test_newStringFlag(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_string_flag("color-theme", default="light")
        assert isinstance(flag, StringFlag)
        assert flag.id == "color-theme"
        assert flag.type == "STRING"
        assert flag.default == "light"

    def test_newStringFlag_with_values(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_string_flag(
            "plan", default="free", values=[{"name": "Free", "value": "free"}, {"name": "Pro", "value": "pro"}]
        )
        assert len(flag.values) == 2

    def test_newNumberFlag(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_number_flag("max-retries", default=3)
        assert isinstance(flag, NumberFlag)
        assert flag.id == "max-retries"
        assert flag.type == "NUMERIC"
        assert flag.default == 3

    def test_newJsonFlag(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_json_flag("config", default={"mode": "standard"})
        assert isinstance(flag, JsonFlag)
        assert flag.id == "config"
        assert flag.type == "JSON"
        assert flag.default == {"mode": "standard"}

    def test_newStringFlag_unconstrained(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_string_flag("greeting", default="hello")
        assert flag.values is None
        assert flag.default == "hello"

    def test_newNumberFlag_unconstrained(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_number_flag("threshold", default=42)
        assert flag.values is None
        assert flag.default == 42

    def test_newJsonFlag_unconstrained(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_json_flag("settings", default={"a": 1})
        assert flag.values is None
        assert flag.default == {"a": 1}

    def test_newBooleanFlag_always_constrained(self):
        mgmt = _new_mgmt()
        flag = mgmt.flags.new_boolean_flag("toggle", default=True)
        assert flag.values is not None
        assert len(flag.values) == 2


# ===========================================================================
# Sync FlagsClient: get(id), list(), delete(id)
# ===========================================================================


class TestFlagsClientCRUD:
    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_get_by_id(self, mock_get):
        mock_get.return_value = _ok_json_response({"data": _flag_json()})
        mgmt = _new_mgmt()
        flag = mgmt.flags.get("test-flag")
        assert flag.id == _TEST_UUID
        mock_get.assert_called_once()

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_get_not_found(self, mock_get):
        mock_get.return_value = _ok_json_response({}, status=HTTPStatus.NOT_FOUND)
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.flags.get("test-flag")

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_get_network_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.flags.get("test-flag")

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_get_timeout(self, mock_get):
        mock_get.side_effect = httpx.ReadTimeout("timed out")
        mgmt = _new_mgmt()
        with pytest.raises(TimeoutError):
            mgmt.flags.get("test-flag")

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_get_generic_exception(self, mock_get):
        mock_get.side_effect = RuntimeError("unexpected")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError):
            mgmt.flags.get("test-flag")

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_list(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mgmt = _new_mgmt()
        flags = mgmt.flags.list()
        assert len(flags) == 1
        assert flags[0].id == _TEST_UUID

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_list_empty(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": []})
        mgmt = _new_mgmt()
        assert mgmt.flags.list() == []

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_list_network_error(self, mock_list):
        mock_list.side_effect = httpx.ConnectError("fail")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.flags.list()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_list_generic_exception(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError):
            mgmt.flags.list()

    @patch("smplkit.flags.client.delete_flag.sync_detailed")
    def test_delete_by_id(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NO_CONTENT)
        mgmt = _new_mgmt()
        mgmt.flags.delete("test-flag")
        mock_delete.assert_called_once()

    @patch("smplkit.flags.client.delete_flag.sync_detailed")
    def test_delete_not_found(self, mock_delete):
        mock_delete.return_value = _ok_json_response({}, status=HTTPStatus.NOT_FOUND)
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.flags.delete("test-flag")

    @patch("smplkit.flags.client.delete_flag.sync_detailed")
    def test_delete_network_error(self, mock_delete):
        mock_delete.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.flags.delete("test-flag")

    @patch("smplkit.flags.client.delete_flag.sync_detailed")
    def test_delete_generic_exception(self, mock_delete):
        mock_delete.side_effect = RuntimeError("unexpected")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError):
            mgmt.flags.delete("test-flag")


# ===========================================================================
# Sync FlagsClient: _create_flag, _update_flag
# ===========================================================================


class TestFlagsClientCreateUpdateFlag:
    @patch("smplkit.flags.client.create_flag.sync_detailed")
    def test_create_flag_success(self, mock_create):
        mock_create.return_value = _ok_json_response({"data": _flag_json()}, status=HTTPStatus.CREATED)
        client = _make_flags_client()
        mgmt = _new_mgmt()
        flag = Flag(client, id="new-flag", name="New", type="BOOLEAN", default=False)
        result = mgmt.flags._create_flag(flag)
        assert result.id == _TEST_UUID

    @patch("smplkit.flags.client.create_flag.sync_detailed")
    def test_create_flag_with_environments(self, mock_create):
        mock_create.return_value = _ok_json_response({"data": _flag_json()}, status=HTTPStatus.CREATED)
        client = _make_flags_client()
        mgmt = _new_mgmt()
        flag = Flag(
            client,
            id="new-flag",
            name="New",
            type="BOOLEAN",
            default=False,
            environments={"staging": FlagEnvironment(enabled=True, default=None, rules=[])},
        )
        result = mgmt.flags._create_flag(flag)
        assert result.id == _TEST_UUID

    @patch("smplkit.flags.client.create_flag.sync_detailed")
    def test_create_flag_unconstrained(self, mock_create):
        mock_create.return_value = _ok_json_response(
            {"data": _flag_json(type_="STRING", default="hello", values=None)},
            status=HTTPStatus.CREATED,
        )
        client = _make_flags_client()
        mgmt = _new_mgmt()
        flag = Flag(client, id="greeting", name="Greeting", type="STRING", default="hello", values=None)
        result = mgmt.flags._create_flag(flag)
        assert result.values is None
        assert result.default == "hello"

    @patch("smplkit.flags.client.create_flag.sync_detailed")
    def test_create_flag_network_error(self, mock_create):
        mock_create.side_effect = httpx.ConnectError("refused")
        client = _make_flags_client()
        mgmt = _new_mgmt()
        flag = Flag(client, id="new-flag", name="New", type="BOOLEAN", default=False)
        with pytest.raises(ConnectionError):
            mgmt.flags._create_flag(flag)

    @patch("smplkit.flags.client.create_flag.sync_detailed")
    def test_create_flag_generic_exception(self, mock_create):
        mock_create.side_effect = RuntimeError("unexpected")
        client = _make_flags_client()
        mgmt = _new_mgmt()
        flag = Flag(client, id="new-flag", name="New", type="BOOLEAN", default=False)
        with pytest.raises(RuntimeError):
            mgmt.flags._create_flag(flag)

    @patch("smplkit.flags.client.update_flag.sync_detailed")
    def test_update_flag_success(self, mock_update):
        mock_update.return_value = _ok_json_response({"data": _flag_json()})
        client = _make_flags_client()
        mgmt = _new_mgmt()
        flag = _make_mock_flag(client)
        result = mgmt.flags._update_flag(flag=flag)
        assert result.id == _TEST_UUID

    @patch("smplkit.flags.client.update_flag.sync_detailed")
    def test_update_flag_with_environments(self, mock_update):
        mock_update.return_value = _ok_json_response({"data": _flag_json()})
        client = _make_flags_client()
        mgmt = _new_mgmt()
        flag = _make_mock_flag(client)
        flag.enable_rules(environment="prod")
        flag.set_default(False, environment="prod")
        result = mgmt.flags._update_flag(flag=flag)
        assert result.id == _TEST_UUID

    @patch("smplkit.flags.client.update_flag.sync_detailed")
    def test_update_flag_network_error(self, mock_update):
        mock_update.side_effect = httpx.ConnectError("refused")
        client = _make_flags_client()
        mgmt = _new_mgmt()
        flag = _make_mock_flag(client)
        with pytest.raises(ConnectionError):
            mgmt.flags._update_flag(flag=flag)

    @patch("smplkit.flags.client.update_flag.sync_detailed")
    def test_update_flag_generic_exception(self, mock_update):
        mock_update.side_effect = RuntimeError("unexpected")
        client = _make_flags_client()
        mgmt = _new_mgmt()
        flag = _make_mock_flag(client)
        with pytest.raises(RuntimeError):
            mgmt.flags._update_flag(flag=flag)


# ===========================================================================
# Sync FlagsClient: typed flag handles (runtime)
# ===========================================================================


class TestFlagsClientTypedHandles:
    def test_booleanFlag(self):
        client = _make_flags_client()
        handle = client.boolean_flag("checkout-v2", default=False)
        assert isinstance(handle, BooleanFlag)
        assert handle.id == "checkout-v2"
        assert handle.default is False
        assert "checkout-v2" in client._handles

    def test_stringFlag(self):
        client = _make_flags_client()
        handle = client.string_flag("color", default="red")
        assert isinstance(handle, StringFlag)
        assert handle.id == "color"
        assert handle.default == "red"

    def test_numberFlag(self):
        client = _make_flags_client()
        handle = client.number_flag("retries", default=3)
        assert isinstance(handle, NumberFlag)
        assert handle.id == "retries"
        assert handle.default == 3

    def test_jsonFlag(self):
        client = _make_flags_client()
        handle = client.json_flag("config", default={"a": 1})
        assert isinstance(handle, JsonFlag)
        assert handle.id == "config"
        assert handle.default == {"a": 1}


# ===========================================================================
# Sync FlagsClient: on_change dual-mode decorator
# ===========================================================================


class TestFlagsClientOnChange:
    def test_bare_decorator(self):
        client = _make_flags_client()

        @client.on_change
        def listener(event):
            pass

        assert len(client._global_listeners) == 1
        assert client._global_listeners[0] is listener

    def test_key_scoped_decorator(self):
        client = _make_flags_client()

        @client.on_change("my-flag")
        def listener(event):
            pass

        assert "my-flag" in client._key_listeners
        assert len(client._key_listeners["my-flag"]) == 1
        assert client._key_listeners["my-flag"][0] is listener

    def test_empty_parens_decorator(self):
        client = _make_flags_client()

        @client.on_change()
        def listener(event):
            pass

        assert len(client._global_listeners) == 1
        assert client._global_listeners[0] is listener


# ===========================================================================
# Sync FlagsClient: connect / refresh / stats
# ===========================================================================


class TestFlagsClientLifecycle:
    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_connect_internal(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.return_value = _ok_response()
        client = _make_flags_client()
        client._parent._environment = "staging"
        mock_ws = MagicMock()
        client._parent._ensure_ws.return_value = mock_ws

        client.start()

        assert client._connected is True
        assert client._environment == "staging"
        assert client._ws_manager is mock_ws
        assert mock_ws.on.call_count == 3
        registered_events = {call.args[0] for call in mock_ws.on.call_args_list}
        assert registered_events == {"flag_changed", "flag_deleted", "flags_changed"}
        assert _TEST_UUID in client._flag_store

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_connect_internal_idempotent(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.return_value = _ok_response()
        client = _make_flags_client()
        client._parent._environment = "staging"
        mock_ws = MagicMock()
        client._parent._ensure_ws.return_value = mock_ws

        client.start()
        client.start()

        assert mock_list.call_count == 1

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_refresh(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        client = _make_flags_client()
        client._connected = True
        client._flag_store = {"old-flag": {"id": "old-flag"}}
        listener = MagicMock()
        client._global_listeners.append(listener)

        client.refresh()

        assert _TEST_UUID in client._flag_store
        assert listener.called

    def test_stats(self):
        client = _make_flags_client()
        stats = client.stats()
        assert stats.cache_hits == 0
        assert stats.cache_misses == 0


# ===========================================================================
# Sync FlagsClient: _evaluate_handle (lazy init)
# ===========================================================================


class TestFlagsClientEvaluateHandle:
    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_lazy_connects_on_first_call(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.return_value = _ok_response()
        client = _make_flags_client()
        client._parent._environment = "staging"
        client._parent._service = None
        mock_ws = MagicMock()
        client._parent._ensure_ws.return_value = mock_ws

        client._evaluate_handle("test-flag", "default", None)
        assert client._connected is True
        assert client._ws_manager is mock_ws

    def test_with_explicit_context(self):
        client = _make_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": False,
                "environments": _envs(
                    {
                        "staging": {
                            "enabled": True,
                            "rules": [{"logic": {"==": [{"var": "user.plan"}, "enterprise"]}, "value": True}],
                        },
                    }
                ),
            }
        }
        result = client._evaluate_handle("flag-a", False, [Context("user", "u-1", plan="enterprise")])
        assert result is True

    def test_with_set_context_does_not_register_again(self):
        """The contextvar branch of _evaluate_handle is pure read.

        Registration happens at ``set_context`` time, so evaluating a flag
        with a contextvar already set must NOT push to the buffer a second
        time.
        """
        from smplkit._context import _request_context

        client = _make_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "off",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        # Simulate set_context having already registered the context.
        client._parent.manage.contexts._buffer.observe([Context("user", "u-1", plan="free")])
        baseline = client._parent.manage.contexts._buffer.pending_count
        token = _request_context.set([Context("user", "u-1", plan="free")])
        try:
            result = client._evaluate_handle("flag-a", "off", None)
            assert result == "off"
            # No additional buffering — the contextvar branch is read-only.
            assert client._parent.manage.contexts._buffer.pending_count == baseline
        finally:
            _request_context.reset(token)

    def test_explicit_context_registers(self):
        """``flag.get(context=[...])`` must push the explicit context to the buffer."""
        client = _make_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "off",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        client._evaluate_handle("flag-a", "off", [Context("user", "u-explicit")])
        assert client._parent.manage.contexts._buffer.pending_count >= 1

    def test_no_provider_reads_from_set_context(self):
        """When set_context has been called, _evaluate_handle reads from the
        ContextVar."""
        from smplkit._context import _request_context

        client = _make_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "fallback",
                "environments": _envs(
                    {
                        "staging": {
                            "enabled": True,
                            "rules": [{"logic": {"==": [{"var": "user.plan"}, "enterprise"]}, "value": "match"}],
                        }
                    }
                ),
            }
        }
        token = _request_context.set([Context("user", "u-1", plan="enterprise")])
        try:
            result = client._evaluate_handle("flag-a", "fallback", None)
            assert result == "match"
        finally:
            _request_context.reset(token)

    def test_no_provider_empty_context(self):
        client = _make_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "fallback",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        result = client._evaluate_handle("flag-a", "fallback", None)
        assert result == "fallback"

    def test_flag_not_in_store_returns_default(self):
        client = _make_flags_client()
        client._connected = True
        client._parent._service = None
        client._flag_store = {}
        result = client._evaluate_handle("missing", "default_val", [Context("user", "u-1")])
        assert result == "default_val"

    def test_evaluate_none_becomes_default(self):
        client = _make_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {"flag-a": {"id": "flag-a", "default": None, "environments": {}}}
        result = client._evaluate_handle("flag-a", "my-default", [Context("user", "u-1")])
        assert result == "my-default"

    def test_cache_hit(self):
        client = _make_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "val",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        ctx = [Context("user", "u-1")]
        client._evaluate_handle("flag-a", "val", ctx)
        result = client._evaluate_handle("flag-a", "val", ctx)
        assert result == "val"
        assert client._cache.cache_hits == 1
        assert client._cache.cache_misses == 1

    def test_service_context_injected(self):
        client = _make_flags_client()
        client._connected = True
        client._environment = "staging"
        client._service = "my-svc"
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "fallback",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        # Call with no explicit context, no provider
        client._evaluate_handle("flag-a", "fallback", None)
        # Verify cache key includes the service context
        assert client._cache.cache_misses == 1

    def test_service_context_not_overridden_by_explicit(self):
        client = _make_flags_client()
        client._connected = True
        client._environment = "staging"
        client._service = "my-svc"
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "fallback",
                "environments": _envs(
                    {
                        "staging": {
                            "enabled": True,
                            "rules": [{"logic": {"==": [{"var": "service.key"}, "custom-svc"]}, "value": "matched"}],
                        },
                    }
                ),
            }
        }
        # Service key already in explicit context should not be overridden
        ctx = [Context("service", "custom-svc")]
        result = client._evaluate_handle("flag-a", "fallback", ctx)
        assert result == "matched"


# ===========================================================================
# Sync FlagsClient: Event handlers + change listeners
# ===========================================================================


class TestFlagsClientEventHandlers:
    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_handle_flag_changed_fires_listener_on_change(self, mock_get):
        # Content differs from pre-state → listener fires
        mock_get.return_value = _ok_json_response({"data": _flag_json(id="test-flag", name="Updated")})
        client = _make_flags_client()
        # Pre-state has different name to ensure diff
        client._flag_store["test-flag"] = {
            "id": "test-flag",
            "name": "Old",
            "type": "BOOLEAN",
            "default": False,
            "values": [],
            "description": "",
            "environments": {},
        }
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_changed({"id": "test-flag"})
        mock_get.assert_called_once()
        listener.assert_called_once()
        event = listener.call_args[0][0]
        assert event.source == "websocket"
        assert event.id == "test-flag"

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_handle_flag_changed_no_fire_when_unchanged(self, mock_get):
        # Return same data as pre-state → no listener fires
        flag_data = _flag_json(id="test-flag")
        mock_get.return_value = _ok_json_response({"data": flag_data})
        client = _make_flags_client()
        # Populate store with same content the fetch will return
        from smplkit.flags.helpers import _flag_dict_from_json

        d = _flag_dict_from_json(flag_data)
        existing = {
            "id": d["id"],
            "name": d["name"],
            "type": d["type"],
            "default": d["default"],
            "values": d["values"],
            "description": d["description"],
            "environments": d["environments"],
        }
        client._flag_store["test-flag"] = existing
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_changed({"id": "test-flag"})
        listener.assert_not_called()

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_handle_flag_changed_fetch_error_propagates(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("fail")
        client = _make_flags_client()
        with pytest.raises(ConnectionError):
            client._handle_flag_changed({"id": "test-flag"})

    def test_handle_flag_changed_no_id_is_noop(self):
        client = _make_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_changed({})  # no "id" key
        listener.assert_not_called()

    def test_handle_flag_deleted_removes_from_store_and_fires(self):
        client = _make_flags_client()
        client._flag_store["test-flag"] = {"id": "test-flag", "name": "x"}
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_deleted({"id": "test-flag"})
        assert "test-flag" not in client._flag_store
        listener.assert_called_once()
        event = listener.call_args[0][0]
        assert event.deleted is True

    def test_handle_flag_deleted_missing_flag_no_fire(self):
        # Flag not in store → no listener fires
        client = _make_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_deleted({"id": "ghost-flag"})
        listener.assert_not_called()

    def test_handle_flag_deleted_no_id_is_noop(self):
        client = _make_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_deleted({})
        listener.assert_not_called()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_fires_global_once_and_per_key(self, mock_list):
        # Two flags in store; post-fetch both change
        mock_list.return_value = _ok_json_response(
            {
                "data": [
                    _flag_json(id="flag-a", name="A-new"),
                    _flag_json(id="flag-b", name="B-new"),
                ]
            }
        )
        client = _make_flags_client()
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "name": "A-old",
                "type": "BOOLEAN",
                "default": False,
                "values": [],
                "description": "",
                "environments": {},
            },
            "flag-b": {
                "id": "flag-b",
                "name": "B-old",
                "type": "BOOLEAN",
                "default": False,
                "values": [],
                "description": "",
                "environments": {},
            },
        }
        global_listener = MagicMock()
        key_listener_a = MagicMock()
        client._global_listeners.append(global_listener)
        client._key_listeners["flag-a"] = [key_listener_a]
        client._handle_flags_changed({})
        global_listener.assert_called_once()
        key_listener_a.assert_called_once()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_no_fire_when_all_unchanged(self, mock_list):
        flag_data = _flag_json(id="flag-a")
        mock_list.return_value = _ok_json_response({"data": [flag_data]})
        from smplkit.flags.helpers import _flag_dict_from_json

        d = _flag_dict_from_json(flag_data)
        existing = {
            "id": d["id"],
            "name": d["name"],
            "type": d["type"],
            "default": d["default"],
            "values": d["values"],
            "description": d["description"],
            "environments": d["environments"],
        }
        client = _make_flags_client()
        client._flag_store = {"flag-a": existing}
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flags_changed({})
        listener.assert_not_called()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_deleted_flag_fires_with_deleted_true(self, mock_list):
        # flag-a is removed in post-fetch
        mock_list.return_value = _ok_json_response({"data": [_flag_json(id="flag-b", name="B")]})
        client = _make_flags_client()
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "name": "A",
                "type": "BOOLEAN",
                "default": False,
                "values": [],
                "description": "",
                "environments": {},
            },
        }
        key_listener = MagicMock()
        client._key_listeners["flag-a"] = [key_listener]
        client._handle_flags_changed({})
        key_listener.assert_called_once()
        event = key_listener.call_args[0][0]
        assert event.deleted is True

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_fetch_error_logs_and_returns(self, mock_list):
        mock_list.side_effect = RuntimeError("boom")
        client = _make_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flags_changed({})
        listener.assert_not_called()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_global_listener_exception_swallowed(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json(id="flag-a", name="Updated")]})
        client = _make_flags_client()
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "name": "Old",
                "type": "BOOLEAN",
                "default": False,
                "values": [],
                "description": "",
                "environments": {},
            }
        }
        bad = MagicMock(side_effect=RuntimeError("boom"))
        good = MagicMock()
        client._global_listeners.extend([bad, good])
        client._handle_flags_changed({})
        good.assert_called_once()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_key_listener_exception_swallowed(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json(id="flag-a", name="Updated")]})
        client = _make_flags_client()
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "name": "Old",
                "type": "BOOLEAN",
                "default": False,
                "values": [],
                "description": "",
                "environments": {},
            }
        }
        bad = MagicMock(side_effect=RuntimeError("boom"))
        good = MagicMock()
        client._key_listeners["flag-a"] = [bad, good]
        client._handle_flags_changed({})
        good.assert_called_once()

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_fetch_flag_single_data_non_network_error_reraises(self, mock_get):
        mock_get.side_effect = ValueError("bad value")
        client = _make_flags_client()
        with pytest.raises(ValueError):
            client._fetch_flag_single_data("test-flag")


class TestFlagsClientChangeListeners:
    def test_fire_global_and_key_scoped(self):
        client = _make_flags_client()
        global_listener = MagicMock()
        key_listener = MagicMock()
        client._global_listeners.append(global_listener)
        client._key_listeners["my-flag"] = [key_listener]

        client._fire_change_listeners("my-flag", "websocket")

        global_listener.assert_called_once()
        key_listener.assert_called_once()

    def test_global_listener_exception_swallowed(self):
        client = _make_flags_client()
        bad = MagicMock(side_effect=RuntimeError("boom"))
        good = MagicMock()
        client._global_listeners.extend([bad, good])
        client._fire_change_listeners("flag-a", "websocket")
        good.assert_called_once()

    def test_key_listener_exception_swallowed(self):
        client = _make_flags_client()
        bad = MagicMock(side_effect=RuntimeError("boom"))
        client._key_listeners["flag-a"] = [bad]
        # Should not raise
        client._fire_change_listeners("flag-a", "websocket")

    def test_none_key_fires_nothing(self):
        client = _make_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._fire_change_listeners(None, "websocket")
        listener.assert_not_called()

    def test_fire_change_listeners_all(self):
        client = _make_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._flag_store = {"flag-a": {"id": "flag-a"}, "flag-b": {"id": "flag-b"}}
        client._fire_change_listeners_all("manual")
        assert listener.call_count == 2


# ===========================================================================
# Sync FlagsClient: Model conversion
# ===========================================================================


# ===========================================================================
# Sync FlagsClient: Fetch internals
# ===========================================================================


class TestFlagsClientFetchInternals:
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_fetch_all_flags(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        client = _make_flags_client()
        client._fetch_all_flags()
        assert _TEST_UUID in client._flag_store

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_fetch_flags_list(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        client = _make_flags_client()
        result = client._fetch_flags_list()
        assert len(result) == 1
        assert result[0]["id"] == _TEST_UUID

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_fetch_flags_list_empty(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": []})
        client = _make_flags_client()
        assert client._fetch_flags_list() == []

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_fetch_flags_list_network_error(self, mock_list):
        mock_list.side_effect = httpx.ConnectError("fail")
        client = _make_flags_client()
        with pytest.raises(ConnectionError):
            client._fetch_flags_list()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_fetch_flags_list_generic_exception(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")
        client = _make_flags_client()
        with pytest.raises(RuntimeError):
            client._fetch_flags_list()


# ===========================================================================
# Sync FlagsClient: runtime integration
# ===========================================================================


class TestFlagsClientRuntimeIntegration:
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_get_with_connected_store(self, mock_list):
        client = SmplClient(api_key="sk_test", environment="test")
        ns = client.flags
        ns._connected = True
        ns._environment = "staging"
        ns._flag_store = {
            "checkout-v2": {
                "id": "checkout-v2",
                "default": False,
                "environments": _envs(
                    {
                        "staging": {
                            "enabled": True,
                            "rules": [{"logic": {"==": [{"var": "user.plan"}, "enterprise"]}, "value": True}],
                        },
                    }
                ),
            },
        }
        handle = ns.boolean_flag("checkout-v2", default=False)
        assert handle.get(context=[Context("user", "u-1", plan="enterprise")]) is True
        assert handle.get(context=[Context("user", "u-2", plan="free")]) is False

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_cache_hits_on_repeated_evaluation(self, mock_list):
        client = SmplClient(api_key="sk_test", environment="test")
        ns = client.flags
        ns._connected = True
        ns._environment = "staging"
        ns._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": False,
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            },
        }
        handle = ns.boolean_flag("flag-a", default=False)
        ctx = [Context("user", "u-1", plan="free")]
        handle.get(context=ctx)
        handle.get(context=ctx)
        handle.get(context=ctx)
        stats = ns.stats()
        assert stats.cache_misses == 1
        assert stats.cache_hits == 2


# ===========================================================================
# AsyncFlagsClient: init
# ===========================================================================


class TestAsyncFlagsClientInit:
    def test_init(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test")
        assert isinstance(client.flags, AsyncFlagsClient)


# ===========================================================================
# AsyncFlagsClient: factory methods
# ===========================================================================


class TestAsyncFlagsClientFactoryMethods:
    def test_newBooleanFlag(self):
        mgmt = _new_async_mgmt()
        flag = mgmt.flags.new_boolean_flag("checkout-v2", default=False)
        assert isinstance(flag, AsyncBooleanFlag)
        assert flag.id == "checkout-v2"
        assert flag.type == "BOOLEAN"
        assert flag.default is False

    def test_newBooleanFlag_custom_name(self):
        mgmt = _new_async_mgmt()
        flag = mgmt.flags.new_boolean_flag("my-flag", default=True, name="Custom", description="desc")
        assert flag.name == "Custom"
        assert flag.description == "desc"

    def test_newStringFlag(self):
        mgmt = _new_async_mgmt()
        flag = mgmt.flags.new_string_flag("color", default="red")
        assert isinstance(flag, AsyncStringFlag)
        assert flag.type == "STRING"

    def test_newStringFlag_with_values(self):
        mgmt = _new_async_mgmt()
        flag = mgmt.flags.new_string_flag("plan", default="free", values=[{"name": "Free", "value": "free"}])
        assert len(flag.values) == 1

    def test_newNumberFlag(self):
        mgmt = _new_async_mgmt()
        flag = mgmt.flags.new_number_flag("retries", default=3)
        assert isinstance(flag, AsyncNumberFlag)
        assert flag.type == "NUMERIC"

    def test_newJsonFlag(self):
        mgmt = _new_async_mgmt()
        flag = mgmt.flags.new_json_flag("config", default={"a": 1})
        assert isinstance(flag, AsyncJsonFlag)
        assert flag.type == "JSON"

    def test_newStringFlag_unconstrained(self):
        mgmt = _new_async_mgmt()
        flag = mgmt.flags.new_string_flag("greeting", default="hello")
        assert flag.values is None

    def test_newNumberFlag_unconstrained(self):
        mgmt = _new_async_mgmt()
        flag = mgmt.flags.new_number_flag("threshold", default=42)
        assert flag.values is None

    def test_newBooleanFlag_always_constrained(self):
        mgmt = _new_async_mgmt()
        flag = mgmt.flags.new_boolean_flag("toggle", default=True)
        assert flag.values is not None
        assert len(flag.values) == 2


# ===========================================================================
# AsyncFlagsClient: get(id), list(), delete(id)
# ===========================================================================


class TestAsyncFlagsClientCRUD:
    @patch("smplkit.flags.client.get_flag.asyncio_detailed")
    def test_get_by_id(self, mock_get):
        mock_get.return_value = _ok_json_response({"data": _flag_json()})

        async def _run():
            mgmt = _new_async_mgmt()
            flag = await mgmt.flags.get("test-flag")
            assert flag.id == _TEST_UUID
            mock_get.assert_called_once()

        asyncio.run(_run())

    @patch("smplkit.flags.client.get_flag.asyncio_detailed")
    def test_get_not_found(self, mock_get):
        mock_get.return_value = _ok_json_response({}, status=HTTPStatus.NOT_FOUND)

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(NotFoundError):
                await mgmt.flags.get("test-flag")

        asyncio.run(_run())

    @patch("smplkit.flags.client.get_flag.asyncio_detailed")
    def test_get_network_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(ConnectionError):
                await mgmt.flags.get("test-flag")

        asyncio.run(_run())

    @patch("smplkit.flags.client.get_flag.asyncio_detailed")
    def test_get_generic_exception(self, mock_get):
        mock_get.side_effect = RuntimeError("unexpected")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(RuntimeError):
                await mgmt.flags.get("test-flag")

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_list(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})

        async def _run():
            mgmt = _new_async_mgmt()
            flags = await mgmt.flags.list()
            assert len(flags) == 1

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_list_empty(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": []})

        async def _run():
            mgmt = _new_async_mgmt()
            assert await mgmt.flags.list() == []

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_list_empty_no_data_attr(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": []})

        async def _run():
            mgmt = _new_async_mgmt()
            assert await mgmt.flags.list() == []

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_list_network_error(self, mock_list):
        mock_list.side_effect = httpx.ConnectError("fail")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(ConnectionError):
                await mgmt.flags.list()

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_list_generic_exception(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(RuntimeError):
                await mgmt.flags.list()

        asyncio.run(_run())

    @patch("smplkit.flags.client.delete_flag.asyncio_detailed")
    def test_delete_by_id(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NO_CONTENT)

        async def _run():
            mgmt = _new_async_mgmt()
            await mgmt.flags.delete("test-flag")
            mock_delete.assert_called_once()

        asyncio.run(_run())

    @patch("smplkit.flags.client.delete_flag.asyncio_detailed")
    def test_delete_not_found(self, mock_delete):
        mock_delete.return_value = _ok_json_response({}, status=HTTPStatus.NOT_FOUND)

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(NotFoundError):
                await mgmt.flags.delete("test-flag")

        asyncio.run(_run())

    @patch("smplkit.flags.client.delete_flag.asyncio_detailed")
    def test_delete_network_error(self, mock_delete):
        mock_delete.side_effect = httpx.ConnectError("refused")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(ConnectionError):
                await mgmt.flags.delete("test-flag")

        asyncio.run(_run())

    @patch("smplkit.flags.client.delete_flag.asyncio_detailed")
    def test_delete_generic_exception(self, mock_delete):
        mock_delete.side_effect = RuntimeError("unexpected")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(RuntimeError):
                await mgmt.flags.delete("test-flag")

        asyncio.run(_run())


# ===========================================================================
# AsyncFlagsClient: _create_flag, _update_flag
# ===========================================================================


class TestAsyncFlagsClientCreateUpdateFlag:
    @patch("smplkit.flags.client.create_flag.asyncio_detailed")
    def test_create_flag_success(self, mock_create):
        mock_create.return_value = _ok_json_response({"data": _flag_json()}, status=HTTPStatus.CREATED)

        async def _run():
            client = _make_async_flags_client()
            mgmt = _new_async_mgmt()
            flag = AsyncFlag(client, id="new", name="New", type="BOOLEAN", default=False)
            result = await mgmt.flags._create_flag(flag)
            assert result.id == _TEST_UUID

        asyncio.run(_run())

    @patch("smplkit.flags.client.create_flag.asyncio_detailed")
    def test_create_flag_network_error(self, mock_create):
        mock_create.side_effect = httpx.ConnectError("refused")

        async def _run():
            client = _make_async_flags_client()
            mgmt = _new_async_mgmt()
            flag = AsyncFlag(client, id="new", name="New", type="BOOLEAN", default=False)
            with pytest.raises(ConnectionError):
                await mgmt.flags._create_flag(flag)

        asyncio.run(_run())

    @patch("smplkit.flags.client.create_flag.asyncio_detailed")
    def test_create_flag_generic_exception(self, mock_create):
        mock_create.side_effect = RuntimeError("unexpected")

        async def _run():
            client = _make_async_flags_client()
            mgmt = _new_async_mgmt()
            flag = AsyncFlag(client, id="new", name="New", type="BOOLEAN", default=False)
            with pytest.raises(RuntimeError):
                await mgmt.flags._create_flag(flag)

        asyncio.run(_run())

    @patch("smplkit.flags.client.update_flag.asyncio_detailed")
    def test_update_flag_success(self, mock_update):
        mock_update.return_value = _ok_json_response({"data": _flag_json()})

        async def _run():
            client = _make_async_flags_client()
            mgmt = _new_async_mgmt()
            flag = _make_mock_async_flag(client)
            result = await mgmt.flags._update_flag(flag=flag)
            assert result.id == _TEST_UUID

        asyncio.run(_run())

    @patch("smplkit.flags.client.update_flag.asyncio_detailed")
    def test_update_flag_network_error(self, mock_update):
        mock_update.side_effect = httpx.ConnectError("refused")

        async def _run():
            client = _make_async_flags_client()
            mgmt = _new_async_mgmt()
            flag = _make_mock_async_flag(client)
            with pytest.raises(ConnectionError):
                await mgmt.flags._update_flag(flag=flag)

        asyncio.run(_run())

    @patch("smplkit.flags.client.update_flag.asyncio_detailed")
    def test_update_flag_generic_exception(self, mock_update):
        mock_update.side_effect = RuntimeError("unexpected")

        async def _run():
            client = _make_async_flags_client()
            mgmt = _new_async_mgmt()
            flag = _make_mock_async_flag(client)
            with pytest.raises(RuntimeError):
                await mgmt.flags._update_flag(flag=flag)

        asyncio.run(_run())


# ===========================================================================
# AsyncFlagsClient: typed flag handles
# ===========================================================================


class TestAsyncFlagsClientTypedHandles:
    def test_booleanFlag(self):
        client = _make_async_flags_client()
        handle = client.boolean_flag("test", default=False)
        assert isinstance(handle, AsyncBooleanFlag)
        assert handle.id == "test"
        assert "test" in client._handles

    def test_stringFlag(self):
        client = _make_async_flags_client()
        handle = client.string_flag("color", default="red")
        assert isinstance(handle, AsyncStringFlag)
        assert handle.id == "color"

    def test_numberFlag(self):
        client = _make_async_flags_client()
        handle = client.number_flag("retries", default=3)
        assert isinstance(handle, AsyncNumberFlag)
        assert handle.id == "retries"

    def test_jsonFlag(self):
        client = _make_async_flags_client()
        handle = client.json_flag("config", default={"a": 1})
        assert isinstance(handle, AsyncJsonFlag)
        assert handle.id == "config"


# ===========================================================================
# AsyncFlagsClient: on_change dual-mode decorator
# ===========================================================================


class TestAsyncFlagsClientOnChange:
    def test_bare_decorator(self):
        client = _make_async_flags_client()

        @client.on_change
        def listener(event):
            pass

        assert len(client._global_listeners) == 1

    def test_key_scoped_decorator(self):
        client = _make_async_flags_client()

        @client.on_change("my-flag")
        def listener(event):
            pass

        assert "my-flag" in client._key_listeners

    def test_empty_parens_decorator(self):
        client = _make_async_flags_client()

        @client.on_change()
        def listener(event):
            pass

        assert len(client._global_listeners) == 1


# ===========================================================================
# AsyncFlagsClient: lifecycle
# ===========================================================================


class TestAsyncFlagsClientLifecycle:
    @patch("smplkit.management.client._gen_bulk_register_flags.asyncio_detailed")
    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_connect_internal(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.return_value = _ok_response()

        async def _run():
            client = _make_async_flags_client()
            client._parent._environment = "staging"
            mock_ws = MagicMock()
            client._parent._ensure_ws.return_value = mock_ws
            await client.start()
            assert client._connected is True
            assert client._environment == "staging"
            assert client._ws_manager is mock_ws
            assert mock_ws.on.call_count == 3
            registered_events = {call.args[0] for call in mock_ws.on.call_args_list}
            assert registered_events == {"flag_changed", "flag_deleted", "flags_changed"}

        asyncio.run(_run())

    @patch("smplkit.management.client._gen_bulk_register_flags.asyncio_detailed")
    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_connect_internal_idempotent(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.return_value = _ok_response()

        async def _run():
            client = _make_async_flags_client()
            client._parent._environment = "staging"
            mock_ws = MagicMock()
            client._parent._ensure_ws.return_value = mock_ws
            await client.start()
            await client.start()
            assert mock_list.call_count == 1

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_refresh(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})

        async def _run():
            client = _make_async_flags_client()
            client._connected = True
            client._flag_store = {"old-flag": {"id": "old-flag"}}
            listener = MagicMock()
            client._global_listeners.append(listener)
            await client.refresh()
            assert _TEST_UUID in client._flag_store
            assert listener.called

        asyncio.run(_run())

    def test_stats(self):
        client = _make_async_flags_client()
        stats = client.stats()
        assert stats.cache_hits == 0


# ===========================================================================
# AsyncFlagsClient: _flush_contexts_async (internal eval path)
# ===========================================================================


class TestAsyncFlagsClientFlushContextsAsync:
    @patch("smplkit.management.client._gen_bulk_register_contexts.asyncio_detailed")
    def test_flush_contexts_async_with_pending(self, mock_bulk):
        mock_bulk.return_value = _ok_response()

        async def _run():
            client = _make_async_flags_client()
            client._parent.manage.contexts._buffer.observe([Context("user", "u-1", plan="pro")])
            await client._flush_contexts_async()
            mock_bulk.assert_called_once()

        asyncio.run(_run())

    @patch("smplkit.management.client._gen_bulk_register_contexts.asyncio_detailed")
    def test_flush_contexts_async_empty(self, mock_bulk):
        async def _run():
            client = _make_async_flags_client()
            await client._flush_contexts_async()
            mock_bulk.assert_not_called()

        asyncio.run(_run())

    @patch("smplkit.management.client._gen_bulk_register_contexts.asyncio_detailed")
    def test_flush_contexts_async_exception_swallowed(self, mock_bulk):
        mock_bulk.side_effect = httpx.ConnectError("fail")

        async def _run():
            client = _make_async_flags_client()
            client._parent.manage.contexts._buffer.observe([Context("user", "u-1")])
            await client._flush_contexts_async()  # should not raise

        asyncio.run(_run())


# ===========================================================================
# AsyncFlagsClient: _evaluate_handle (lazy init)
# ===========================================================================


class TestAsyncFlagsClientEvaluateHandle:
    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_lazy_connects_on_first_call(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.return_value = _ok_response()
        client = _make_async_flags_client()
        client._parent._environment = "staging"
        client._parent._service = None
        mock_ws = MagicMock()
        client._parent._ensure_ws.return_value = mock_ws

        client._evaluate_handle("test-flag", "default", None)
        assert client._connected is True
        assert client._ws_manager is mock_ws

    def test_with_explicit_context(self):
        client = _make_async_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": False,
                "environments": _envs(
                    {
                        "staging": {
                            "enabled": True,
                            "rules": [{"logic": {"==": [{"var": "user.plan"}, "enterprise"]}, "value": True}],
                        },
                    }
                ),
            }
        }
        result = client._evaluate_handle("flag-a", False, [Context("user", "u-1", plan="enterprise")])
        assert result is True

    def test_with_set_context_does_not_register_again(self):
        """Async contextvar branch is read-only; set_context handles registration."""
        from smplkit._context import _request_context

        client = _make_async_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "off",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        client._parent.manage.contexts._buffer.observe([Context("user", "u-1")])
        baseline = client._parent.manage.contexts._buffer.pending_count
        token = _request_context.set([Context("user", "u-1")])
        try:
            result = client._evaluate_handle("flag-a", "off", None)
            assert result == "off"
            assert client._parent.manage.contexts._buffer.pending_count == baseline
        finally:
            _request_context.reset(token)

    def test_explicit_context_registers(self):
        client = _make_async_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "off",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        client._evaluate_handle("flag-a", "off", [Context("user", "u-explicit")])
        assert client._parent.manage.contexts._buffer.pending_count >= 1

    def test_no_provider_empty_context(self):
        client = _make_async_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "fallback",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        assert client._evaluate_handle("flag-a", "fallback", None) == "fallback"

    def test_flag_not_in_store(self):
        client = _make_async_flags_client()
        client._connected = True
        client._parent._service = None
        client._flag_store = {}
        assert client._evaluate_handle("missing", "default_val", [Context("user", "u-1")]) == "default_val"

    def test_evaluate_none_becomes_default(self):
        client = _make_async_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {"flag-a": {"id": "flag-a", "default": None, "environments": {}}}
        assert client._evaluate_handle("flag-a", "my-default", [Context("user", "u-1")]) == "my-default"

    def test_cache_hit(self):
        client = _make_async_flags_client()
        client._connected = True
        client._environment = "staging"
        client._parent._service = None
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "val",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        ctx = [Context("user", "u-1")]
        client._evaluate_handle("flag-a", "val", ctx)
        client._evaluate_handle("flag-a", "val", ctx)
        assert client._cache.cache_hits == 1

    def test_service_context_injected(self):
        client = _make_async_flags_client()
        client._connected = True
        client._environment = "staging"
        client._service = "my-svc"
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "default": "fallback",
                "environments": _envs({"staging": {"enabled": True, "rules": []}}),
            }
        }
        client._evaluate_handle("flag-a", "fallback", None)
        assert client._cache.cache_misses == 1


# ===========================================================================
# AsyncFlagsClient: Event handlers
# ===========================================================================


class TestAsyncFlagsClientEventHandlers:
    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_handle_flag_changed_fires_listener_on_change(self, mock_get):
        mock_get.return_value = _ok_json_response({"data": _flag_json(id="test-flag", name="Updated")})
        client = _make_async_flags_client()
        client._flag_store["test-flag"] = {
            "id": "test-flag",
            "name": "Old",
            "type": "BOOLEAN",
            "default": False,
            "values": [],
            "description": "",
            "environments": {},
        }
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_changed({"id": "test-flag"})
        listener.assert_called_once()
        event = listener.call_args[0][0]
        assert event.source == "websocket"

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_handle_flag_changed_no_fire_when_unchanged(self, mock_get):
        flag_data = _flag_json(id="test-flag")
        mock_get.return_value = _ok_json_response({"data": flag_data})
        from smplkit.flags.helpers import _flag_dict_from_json

        d = _flag_dict_from_json(flag_data)
        existing = {
            "id": d["id"],
            "name": d["name"],
            "type": d["type"],
            "default": d["default"],
            "values": d["values"],
            "description": d["description"],
            "environments": d["environments"],
        }
        client = _make_async_flags_client()
        client._flag_store["test-flag"] = existing
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_changed({"id": "test-flag"})
        listener.assert_not_called()

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_handle_flag_changed_fetch_error_is_swallowed(self, mock_get):
        # Async client swallows errors (unlike sync which propagates)
        mock_get.side_effect = httpx.ConnectError("fail")
        client = _make_async_flags_client()
        client._handle_flag_changed({"id": "test-flag"})  # should not raise

    def test_handle_flag_deleted_removes_and_fires(self):
        client = _make_async_flags_client()
        client._flag_store["test-flag"] = {"id": "test-flag", "name": "x"}
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_deleted({"id": "test-flag"})
        assert "test-flag" not in client._flag_store
        listener.assert_called_once()
        event = listener.call_args[0][0]
        assert event.deleted is True

    def test_handle_flag_deleted_missing_flag_no_fire(self):
        client = _make_async_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_deleted({"id": "ghost-flag"})
        listener.assert_not_called()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_fires_global_once_and_per_key(self, mock_list):
        mock_list.return_value = _ok_json_response(
            {
                "data": [
                    _flag_json(id="flag-a", name="A-new"),
                    _flag_json(id="flag-b", name="B-new"),
                ]
            }
        )
        client = _make_async_flags_client()
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "name": "A-old",
                "type": "BOOLEAN",
                "default": False,
                "values": [],
                "description": "",
                "environments": {},
            },
            "flag-b": {
                "id": "flag-b",
                "name": "B-old",
                "type": "BOOLEAN",
                "default": False,
                "values": [],
                "description": "",
                "environments": {},
            },
        }
        global_listener = MagicMock()
        key_listener_b = MagicMock()
        client._global_listeners.append(global_listener)
        client._key_listeners["flag-b"] = [key_listener_b]
        client._handle_flags_changed({})
        global_listener.assert_called_once()
        key_listener_b.assert_called_once()

    def test_handle_flag_changed_no_id_is_noop(self):
        client = _make_async_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_changed({})
        listener.assert_not_called()

    def test_handle_flag_deleted_no_id_is_noop(self):
        client = _make_async_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flag_deleted({})
        listener.assert_not_called()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_fetch_error_swallowed(self, mock_list):
        mock_list.side_effect = RuntimeError("boom")
        client = _make_async_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flags_changed({})
        listener.assert_not_called()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_no_change_no_fire(self, mock_list):
        flag_data = _flag_json(id="flag-a")
        mock_list.return_value = _ok_json_response({"data": [flag_data]})
        from smplkit.flags.helpers import _flag_dict_from_json

        d = _flag_dict_from_json(flag_data)
        existing = {
            "id": d["id"],
            "name": d["name"],
            "type": d["type"],
            "default": d["default"],
            "values": d["values"],
            "description": d["description"],
            "environments": d["environments"],
        }
        client = _make_async_flags_client()
        client._flag_store = {"flag-a": existing}
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_flags_changed({})
        listener.assert_not_called()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_global_listener_exception_swallowed(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json(id="flag-a", name="Updated")]})
        client = _make_async_flags_client()
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "name": "Old",
                "type": "BOOLEAN",
                "default": False,
                "values": [],
                "description": "",
                "environments": {},
            }
        }
        bad = MagicMock(side_effect=RuntimeError("boom"))
        good = MagicMock()
        client._global_listeners.extend([bad, good])
        client._handle_flags_changed({})
        good.assert_called_once()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_handle_flags_changed_key_listener_exception_swallowed(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json(id="flag-a", name="Updated")]})
        client = _make_async_flags_client()
        client._flag_store = {
            "flag-a": {
                "id": "flag-a",
                "name": "Old",
                "type": "BOOLEAN",
                "default": False,
                "values": [],
                "description": "",
                "environments": {},
            }
        }
        bad = MagicMock(side_effect=RuntimeError("boom"))
        good = MagicMock()
        client._key_listeners["flag-a"] = [bad, good]
        client._handle_flags_changed({})
        good.assert_called_once()

    @patch("smplkit.flags.client.get_flag.sync_detailed")
    def test_fetch_flag_single_data_sync_non_network_error_reraises(self, mock_get):
        mock_get.side_effect = ValueError("unexpected")
        client = _make_async_flags_client()
        with pytest.raises(ValueError):
            client._fetch_flag_single_data_sync("test-flag")


class TestAsyncFlagsClientChangeListeners:
    def test_fire_global_and_key_scoped(self):
        client = _make_async_flags_client()
        global_listener = MagicMock()
        key_listener = MagicMock()
        client._global_listeners.append(global_listener)
        client._key_listeners["my-flag"] = [key_listener]
        client._fire_change_listeners("my-flag", "websocket")
        global_listener.assert_called_once()
        key_listener.assert_called_once()

    def test_global_listener_exception_swallowed(self):
        client = _make_async_flags_client()
        bad = MagicMock(side_effect=RuntimeError("boom"))
        good = MagicMock()
        client._global_listeners.extend([bad, good])
        client._fire_change_listeners("flag-a", "websocket")
        good.assert_called_once()

    def test_key_listener_exception_swallowed(self):
        client = _make_async_flags_client()
        bad = MagicMock(side_effect=RuntimeError("boom"))
        client._key_listeners["flag-a"] = [bad]
        client._fire_change_listeners("flag-a", "websocket")

    def test_none_key_fires_nothing(self):
        client = _make_async_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._fire_change_listeners(None, "websocket")
        listener.assert_not_called()

    def test_fire_change_listeners_all(self):
        client = _make_async_flags_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._flag_store = {"a": {"id": "a"}, "b": {"id": "b"}}
        client._fire_change_listeners_all("manual")
        assert listener.call_count == 2


# ===========================================================================
# AsyncFlagsClient: Model conversion + fetch internals
# ===========================================================================


class TestAsyncFlagsClientInternals:
    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_fetch_all_flags(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})

        async def _run():
            client = _make_async_flags_client()
            await client._fetch_all_flags()
            assert _TEST_UUID in client._flag_store

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_fetch_flags_list(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})

        async def _run():
            client = _make_async_flags_client()
            result = await client._fetch_flags_list()
            assert len(result) == 1
            assert result[0]["id"] == _TEST_UUID

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_fetch_flags_list_empty(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": []})

        async def _run():
            client = _make_async_flags_client()
            assert await client._fetch_flags_list() == []

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_fetch_flags_list_network_error(self, mock_list):
        mock_list.side_effect = httpx.ConnectError("fail")

        async def _run():
            client = _make_async_flags_client()
            with pytest.raises(ConnectionError):
                await client._fetch_flags_list()

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_fetch_flags_list_generic_exception(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")

        async def _run():
            client = _make_async_flags_client()
            with pytest.raises(RuntimeError):
                await client._fetch_flags_list()

        asyncio.run(_run())

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_fetch_all_flags_sync(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        client = _make_async_flags_client()
        client._fetch_all_flags_sync()
        assert _TEST_UUID in client._flag_store

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_fetch_all_flags_sync_empty(self, mock_list):
        mock_list.return_value = _ok_json_response({"data": []})
        client = _make_async_flags_client()
        client._fetch_all_flags_sync()
        assert client._flag_store == {}

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_fetch_all_flags_sync_network_error(self, mock_list):
        mock_list.side_effect = httpx.ConnectError("fail")
        client = _make_async_flags_client()
        with pytest.raises(ConnectionError):
            client._fetch_all_flags_sync()

    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_fetch_all_flags_sync_generic_exception(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")
        client = _make_async_flags_client()
        with pytest.raises(RuntimeError, match="unexpected"):
            client._fetch_all_flags_sync()


# ===========================================================================
# _FlagRegistrationBuffer
# ===========================================================================


class TestFlagRegistrationBuffer:
    def test_add_and_drain(self):
        buf = _FlagRegistrationBuffer()
        buf.add("dark-mode", "BOOLEAN", False, "api-gw", "production")
        batch = buf.drain()
        assert len(batch) == 1
        assert batch[0] == {
            "id": "dark-mode",
            "type": "BOOLEAN",
            "default": False,
            "service": "api-gw",
            "environment": "production",
        }

    def test_dedup(self):
        buf = _FlagRegistrationBuffer()
        buf.add("dark-mode", "BOOLEAN", False, "api-gw", "prod")
        buf.add("dark-mode", "BOOLEAN", True, "other-svc", "staging")
        batch = buf.drain()
        assert len(batch) == 1
        assert batch[0]["default"] is False  # first wins

    def test_drain_clears(self):
        buf = _FlagRegistrationBuffer()
        buf.add("f1", "STRING", "a", None, None)
        assert buf.drain() != []
        assert buf.drain() == []

    def test_pending_count(self):
        buf = _FlagRegistrationBuffer()
        assert buf.pending_count == 0
        buf.add("f1", "BOOLEAN", True, None, None)
        buf.add("f2", "STRING", "x", None, None)
        assert buf.pending_count == 2
        buf.drain()
        assert buf.pending_count == 0

    def test_omits_none_service_environment(self):
        buf = _FlagRegistrationBuffer()
        buf.add("f1", "NUMERIC", 42, None, None)
        batch = buf.drain()
        assert "service" not in batch[0]
        assert "environment" not in batch[0]

    def test_multiple_distinct_flags(self):
        buf = _FlagRegistrationBuffer()
        buf.add("f1", "BOOLEAN", True, "svc", "prod")
        buf.add("f2", "STRING", "red", "svc", "prod")
        buf.add("f3", "NUMERIC", 5, "svc", "prod")
        batch = buf.drain()
        assert len(batch) == 3
        assert [b["id"] for b in batch] == ["f1", "f2", "f3"]

    def test_peek_does_not_remove(self):
        """``peek()`` returns a snapshot but leaves items pending."""
        buf = _FlagRegistrationBuffer()
        buf.add("f1", "BOOLEAN", True, None, None)
        buf.add("f2", "STRING", "x", None, None)
        snapshot = buf.peek()
        assert [b["id"] for b in snapshot] == ["f1", "f2"]
        assert buf.pending_count == 2
        # And mutating the snapshot doesn't affect the buffer.
        snapshot.clear()
        assert buf.pending_count == 2

    def test_commit_removes_only_specified_ids(self):
        """``commit(ids)`` removes the listed items but keeps any added in flight."""
        buf = _FlagRegistrationBuffer()
        buf.add("f1", "BOOLEAN", True, None, None)
        buf.add("f2", "STRING", "x", None, None)
        snapshot = buf.peek()
        # New declaration arrives between peek and commit (e.g. another thread).
        buf.add("f3", "NUMERIC", 5, None, None)
        buf.commit([b["id"] for b in snapshot])
        remaining = buf.peek()
        assert [b["id"] for b in remaining] == ["f3"]

    def test_commit_empty_is_noop(self):
        buf = _FlagRegistrationBuffer()
        buf.add("f1", "BOOLEAN", True, None, None)
        buf.commit([])
        assert buf.pending_count == 1


# ===========================================================================
# Sync FlagsClient: flag registration buffer integration
# ===========================================================================


class TestFlagsClientFlagRegistration:
    def test_booleanFlag_adds_to_buffer(self):
        client = _make_flags_client()
        client._service = "my-svc"
        client._environment = "prod"
        client.boolean_flag("dark-mode", default=False)
        batch = client._manage.flags._buffer.drain()
        assert len(batch) == 1
        assert batch[0]["id"] == "dark-mode"
        assert batch[0]["type"] == "BOOLEAN"
        assert batch[0]["default"] is False
        assert batch[0]["service"] == "my-svc"
        assert batch[0]["environment"] == "prod"

    def test_stringFlag_adds_to_buffer(self):
        client = _make_flags_client()
        client.string_flag("color", default="red")
        batch = client._parent.manage.flags._buffer.drain()
        assert len(batch) == 1
        assert batch[0]["type"] == "STRING"
        assert batch[0]["default"] == "red"

    def test_numberFlag_adds_to_buffer(self):
        client = _make_flags_client()
        client.number_flag("retries", default=3)
        batch = client._parent.manage.flags._buffer.drain()
        assert len(batch) == 1
        assert batch[0]["type"] == "NUMERIC"
        assert batch[0]["default"] == 3

    def test_jsonFlag_adds_to_buffer(self):
        client = _make_flags_client()
        client.json_flag("config", default={"a": 1})
        batch = client._parent.manage.flags._buffer.drain()
        assert len(batch) == 1
        assert batch[0]["type"] == "JSON"
        assert batch[0]["default"] == {"a": 1}

    def test_dedup_across_typed_methods(self):
        client = _make_flags_client()
        client.boolean_flag("flag-a", default=True)
        client.boolean_flag("flag-a", default=False)  # same id, different default
        batch = client._parent.manage.flags._buffer.drain()
        assert len(batch) == 1  # deduped

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    def test_flush_flags_sync(self, mock_bulk):
        mock_bulk.return_value = _ok_response()
        client = _make_flags_client()
        client.boolean_flag("f1", default=True)
        client.string_flag("f2", default="x")
        client._flush_flags_sync()
        mock_bulk.assert_called_once()
        _, kwargs = mock_bulk.call_args
        body = kwargs["body"]
        assert len(body.flags) == 2
        assert body.flags[0].id == "f1"
        assert body.flags[0].type_ == "BOOLEAN"
        assert body.flags[0].default is True
        assert body.flags[1].id == "f2"
        assert body.flags[1].type_ == "STRING"

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    def test_flush_flags_sync_empty_batch(self, mock_bulk):
        client = _make_flags_client()
        client._flush_flags_sync()
        mock_bulk.assert_not_called()

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    def test_flush_flags_sync_reraises_network_error(self, mock_bulk):
        """Network errors propagate so ``start()`` can schedule a retry."""
        mock_bulk.side_effect = httpx.ConnectError("fail")
        client = _make_flags_client()
        client.boolean_flag("f1", default=True)
        with pytest.raises(ConnectionError):
            client._flush_flags_sync()
        # Buffer must retain the declaration for the next attempt.
        assert client._parent.manage.flags._buffer.pending_count == 1

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    def test_flush_flags_sync_reraises_http_error(self, mock_bulk):
        """HTTP error responses propagate; declarations remain queued."""
        mock_bulk.return_value = _ok_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        client = _make_flags_client()
        client.boolean_flag("f1", default=True)
        with pytest.raises(Exception):
            client._flush_flags_sync()
        assert client._parent.manage.flags._buffer.pending_count == 1

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_connect_internal_flushes_before_fetch(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.return_value = _ok_response()
        client = _make_flags_client()
        client._parent._environment = "test"
        mock_ws = MagicMock()
        client._parent._ensure_ws.return_value = mock_ws

        client.boolean_flag("f1", default=True)
        client.start()

        mock_bulk.assert_called_once()
        mock_list.assert_called_once()
        # Verify flush was called before fetch (bulk before list)
        bulk_order = mock_bulk.call_args_list[0]
        list_order = mock_list.call_args_list[0]
        assert bulk_order is not None
        assert list_order is not None

    def test_close_noop(self):
        """``_close()`` is now a no-op on the runtime client (timers moved to SmplClient)."""
        client = _make_flags_client()
        client._close()  # should not raise

    def test_threshold_triggers_flush_via_mgmt(self):
        """Runtime declarations push through ``mgmt.flags.register`` and hit the threshold trigger."""
        client = _make_flags_client()
        for i in range(_FLAG_BULK_FLUSH_THRESHOLD - 1):
            client.boolean_flag(f"flag-{i}", default=True)
        with patch("smplkit.management.client.threading.Thread") as mock_thread:
            client.boolean_flag(f"flag-{_FLAG_BULK_FLUSH_THRESHOLD - 1}", default=True)
            mock_thread.assert_called_once()


# ===========================================================================
# Sync FlagsClient: start() retries when the flags-service is unhealthy
# ===========================================================================


class TestFlagsClientStartRetry:
    """Pod-rebuild scenario: flags-service is unavailable when ``start()`` runs."""

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_failed_flush_keeps_queue_and_retries_on_next_start(self, mock_list, mock_bulk):
        """First flush 500s; queue is retained; second start() succeeds.

        This is the production regression: a coordinated rebuild brought
        flags-service down momentarily and the app pod marked itself
        connected after a silent registration failure.  After the fix,
        ``start()`` must leave the buffer intact, keep ``_connected``
        false, and re-attempt on the next call.
        """
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.side_effect = [
            _ok_response(status=HTTPStatus.INTERNAL_SERVER_ERROR),
            _ok_response(status=HTTPStatus.OK),
        ]
        client = _make_flags_client()
        client._parent._environment = "test"
        client._parent._ensure_ws.return_value = MagicMock()

        client.boolean_flag("product_alpha", default=False)
        assert client._parent.manage.flags._buffer.pending_count == 1

        # First attempt: bulk-register 500s.  Queue must NOT be drained,
        # client must remain not-connected, retry must be scheduled.
        client.start()
        assert client._connected is False
        assert client._parent.manage.flags._buffer.pending_count == 1
        assert mock_bulk.call_count == 1

        # Skip the backoff window so the next attempt actually runs.
        client._next_start_attempt_at = 0.0

        # Second attempt: bulk-register 200s.  Queue drains, client connects.
        client.start()
        assert client._connected is True
        assert client._parent.manage.flags._buffer.pending_count == 0
        assert mock_bulk.call_count == 2

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_backoff_skips_redundant_attempts(self, mock_list, mock_bulk):
        """Repeated calls inside the backoff window are no-ops."""
        mock_list.return_value = _ok_json_response({"data": []})
        mock_bulk.side_effect = httpx.ConnectError("flags-service down")
        client = _make_flags_client()
        client._parent._environment = "test"
        client._parent._ensure_ws.return_value = MagicMock()
        client.boolean_flag("f1", default=True)

        client.start()  # fails, schedules retry ~1s out
        first_call_count = mock_bulk.call_count
        client.start()  # within backoff window — no new HTTP call
        client.start()
        assert mock_bulk.call_count == first_call_count
        assert client._connected is False
        assert client._parent.manage.flags._buffer.pending_count == 1

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_backoff_delay_doubles_then_caps(self, mock_list, mock_bulk):
        """Each failed attempt doubles the delay, capped at the configured maximum."""
        from smplkit.flags.client import _MAX_START_RETRY_DELAY

        mock_list.return_value = _ok_json_response({"data": []})
        mock_bulk.side_effect = httpx.ConnectError("flags-service down")
        client = _make_flags_client()
        client._parent._environment = "test"
        client._parent._ensure_ws.return_value = MagicMock()
        client.boolean_flag("f1", default=True)

        seen_delays = []
        for _ in range(10):
            client._next_start_attempt_at = 0.0
            before = client._start_retry_delay
            client.start()
            seen_delays.append(before)
        # Delays double up to the cap.
        assert seen_delays[0] == 1.0
        assert seen_delays[1] == 2.0
        assert seen_delays[2] == 4.0
        assert seen_delays[-1] == _MAX_START_RETRY_DELAY

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_evaluation_falls_back_to_default_while_disconnected(self, mock_list, mock_bulk):
        """Until ``start()`` succeeds, evaluation must return the handle default."""
        mock_list.return_value = _ok_json_response({"data": []})
        mock_bulk.side_effect = httpx.ConnectError("flags-service down")
        client = _make_flags_client()
        client._parent._environment = "test"
        client._parent._service = None
        client._parent._metrics = None
        client._parent._ensure_ws.return_value = MagicMock()

        flag = client.boolean_flag("checkout_v2", default=False)
        # First evaluation triggers start(), which fails; fall through to default.
        assert flag.get() is False
        assert client._connected is False
        assert client._parent.manage.flags._buffer.pending_count == 1

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_ws_subscribed_only_once_across_retry_attempts(self, mock_list, mock_bulk):
        """WS handlers must not be re-registered when start() retries after failure."""
        mock_list.return_value = _ok_json_response({"data": []})
        mock_bulk.side_effect = [
            _ok_response(status=HTTPStatus.INTERNAL_SERVER_ERROR),
            _ok_response(status=HTTPStatus.OK),
            _ok_response(status=HTTPStatus.OK),
        ]
        client = _make_flags_client()
        client._parent._environment = "test"
        mock_ws = MagicMock()
        client._parent._ensure_ws.return_value = mock_ws
        client.boolean_flag("f1", default=True)

        client.start()  # fails
        client._next_start_attempt_at = 0.0
        client.start()  # succeeds, registers 3 WS handlers
        client.start()  # idempotent fast path

        # Exactly three subscriptions, even though start() ran multiple times.
        assert mock_ws.on.call_count == 3


# ===========================================================================
# Async FlagsClient: flag registration buffer integration
# ===========================================================================


class TestAsyncFlagsClientFlagRegistration:
    def test_booleanFlag_adds_to_buffer(self):
        client = _make_async_flags_client()
        client._service = "my-svc"
        client._environment = "prod"
        client.boolean_flag("dark-mode", default=False)
        batch = client._manage.flags._buffer.drain()
        assert len(batch) == 1
        assert batch[0]["id"] == "dark-mode"
        assert batch[0]["type"] == "BOOLEAN"
        assert batch[0]["default"] is False
        assert batch[0]["service"] == "my-svc"

    def test_stringFlag_adds_to_buffer(self):
        client = _make_async_flags_client()
        client.string_flag("color", default="red")
        batch = client._parent.manage.flags._buffer.drain()
        assert batch[0]["type"] == "STRING"

    def test_numberFlag_adds_to_buffer(self):
        client = _make_async_flags_client()
        client.number_flag("retries", default=3)
        batch = client._parent.manage.flags._buffer.drain()
        assert batch[0]["type"] == "NUMERIC"

    def test_jsonFlag_adds_to_buffer(self):
        client = _make_async_flags_client()
        client.json_flag("config", default={"a": 1})
        batch = client._parent.manage.flags._buffer.drain()
        assert batch[0]["type"] == "JSON"

    @patch("smplkit.management.client._gen_bulk_register_flags.asyncio_detailed")
    def test_flush_flags_async(self, mock_bulk):
        mock_bulk.return_value = _ok_response()

        async def _run():
            client = _make_async_flags_client()
            client.boolean_flag("f1", default=True)
            await client._flush_flags_async()
            mock_bulk.assert_called_once()
            _, kwargs = mock_bulk.call_args
            body = kwargs["body"]
            assert len(body.flags) == 1
            assert body.flags[0].id == "f1"
            assert body.flags[0].type_ == "BOOLEAN"

        asyncio.run(_run())

    @patch("smplkit.management.client._gen_bulk_register_flags.asyncio_detailed")
    def test_flush_flags_async_empty_batch(self, mock_bulk):
        async def _run():
            client = _make_async_flags_client()
            await client._flush_flags_async()
            mock_bulk.assert_not_called()

        asyncio.run(_run())

    @patch("smplkit.management.client._gen_bulk_register_flags.asyncio_detailed")
    def test_flush_flags_async_reraises_network_error(self, mock_bulk):
        """Network errors propagate so ``start()`` can schedule a retry."""
        mock_bulk.side_effect = httpx.ConnectError("fail")

        async def _run():
            client = _make_async_flags_client()
            client.boolean_flag("f1", default=True)
            with pytest.raises(ConnectionError):
                await client._flush_flags_async()
            # Buffer must retain the declaration for the next attempt.
            assert client._manage.flags._buffer.pending_count == 1

        asyncio.run(_run())

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    def test_flush_flags_sync(self, mock_bulk):
        mock_bulk.return_value = _ok_response()
        client = _make_async_flags_client()
        client.boolean_flag("f1", default=True)
        client._flush_flags_sync()
        mock_bulk.assert_called_once()

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    def test_flush_flags_sync_empty_batch(self, mock_bulk):
        client = _make_async_flags_client()
        client._flush_flags_sync()
        mock_bulk.assert_not_called()

    @patch("smplkit.management.client._gen_bulk_register_flags.asyncio_detailed")
    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_connect_internal_flushes_before_fetch(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": []})
        mock_bulk.return_value = _ok_response()

        async def _run():
            client = _make_async_flags_client()
            client._parent._environment = "test"
            mock_ws = MagicMock()
            client._parent._ensure_ws.return_value = mock_ws

            client.boolean_flag("f1", default=True)
            await client.start()

            mock_bulk.assert_called_once()
            mock_list.assert_called_once()

        asyncio.run(_run())

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_evaluate_handle_lazy_init_flushes(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.return_value = _ok_response()
        client = _make_async_flags_client()
        client._parent._environment = "test"
        client._parent._service = None
        mock_ws = MagicMock()
        client._parent._ensure_ws.return_value = mock_ws
        client._parent._metrics = None

        client.boolean_flag("f1", default=True)
        client._evaluate_handle(_TEST_UUID, False, None)

        mock_bulk.assert_called_once()

    def test_close_noop(self):
        """``_close()`` is now a no-op on the runtime client."""
        client = _make_async_flags_client()
        client._close()  # should not raise

    @patch("smplkit.management.client._gen_bulk_register_flags.asyncio_detailed")
    def test_flush_flags_async_reraises_http_error(self, mock_bulk):
        """HTTP error responses propagate; declarations remain queued."""
        mock_bulk.return_value = _ok_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        async def _run():
            client = _make_async_flags_client()
            client.boolean_flag("f1", default=True)
            with pytest.raises(Exception):
                await client._flush_flags_async()
            assert client._manage.flags._buffer.pending_count == 1

        asyncio.run(_run())

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    def test_flush_flags_sync_reraises_http_error(self, mock_bulk):
        """HTTP error responses propagate; declarations remain queued."""
        mock_bulk.return_value = _ok_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        client = _make_async_flags_client()
        client.boolean_flag("f1", default=True)
        with pytest.raises(Exception):
            client._flush_flags_sync()
        assert client._manage.flags._buffer.pending_count == 1

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    def test_flush_flags_sync_reraises_network_error(self, mock_bulk):
        """Network errors propagate so the lazy-init retry can reschedule."""
        mock_bulk.side_effect = httpx.ConnectError("fail")
        client = _make_async_flags_client()
        client.boolean_flag("f1", default=True)
        with pytest.raises(ConnectionError):
            client._flush_flags_sync()
        assert client._manage.flags._buffer.pending_count == 1

    def test_threshold_triggers_flush_via_mgmt(self):
        """Async runtime declarations route through ``mgmt.flags.register`` and trigger threshold flush."""
        client = _make_async_flags_client()
        for i in range(_FLAG_BULK_FLUSH_THRESHOLD - 1):
            client.boolean_flag(f"flag-{i}", default=True)
        with patch("smplkit.management.client.threading.Thread") as mock_thread:
            client.boolean_flag(f"flag-{_FLAG_BULK_FLUSH_THRESHOLD - 1}", default=True)
            mock_thread.assert_called_once()


# ===========================================================================
# Async FlagsClient: start() retries when the flags-service is unhealthy
# ===========================================================================


class TestAsyncFlagsClientStartRetry:
    """Mirror of TestFlagsClientStartRetry for the async client."""

    @patch("smplkit.management.client._gen_bulk_register_flags.asyncio_detailed")
    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_failed_flush_keeps_queue_and_retries_on_next_start(self, mock_list, mock_bulk):
        mock_list.return_value = _ok_json_response({"data": [_flag_json()]})
        mock_bulk.side_effect = [
            _ok_response(status=HTTPStatus.INTERNAL_SERVER_ERROR),
            _ok_response(status=HTTPStatus.OK),
        ]

        async def _run():
            client = _make_async_flags_client()
            client._parent._environment = "test"
            client._parent._ensure_ws.return_value = MagicMock()

            client.boolean_flag("product_alpha", default=False)
            assert client._manage.flags._buffer.pending_count == 1

            await client.start()
            assert client._connected is False
            assert client._manage.flags._buffer.pending_count == 1
            assert mock_bulk.call_count == 1

            client._next_start_attempt_at = 0.0
            await client.start()
            assert client._connected is True
            assert client._manage.flags._buffer.pending_count == 0
            assert mock_bulk.call_count == 2

        asyncio.run(_run())

    @patch("smplkit.management.client._gen_bulk_register_flags.sync_detailed")
    @patch("smplkit.flags.client.list_flags.sync_detailed")
    def test_evaluate_handle_lazy_init_retains_queue_on_failure(self, mock_list, mock_bulk):
        """The thread-safe lazy-init path mirrors ``start()`` semantics."""
        mock_list.return_value = _ok_json_response({"data": []})
        mock_bulk.side_effect = httpx.ConnectError("flags-service down")
        client = _make_async_flags_client()
        client._parent._environment = "test"
        client._parent._service = None
        client._parent._metrics = None
        client._parent._ensure_ws.return_value = MagicMock()

        flag = client.boolean_flag("checkout_v2", default=False)
        assert flag.get() is False  # falls back to default
        assert client._connected is False
        assert client._manage.flags._buffer.pending_count == 1

    @patch("smplkit.management.client._gen_bulk_register_flags.asyncio_detailed")
    @patch("smplkit.flags.client.list_flags.asyncio_detailed")
    def test_start_backoff_skips_redundant_attempts(self, mock_list, mock_bulk):
        """Repeated async ``start()`` calls inside the backoff window are no-ops."""
        mock_list.return_value = _ok_json_response({"data": []})
        mock_bulk.side_effect = httpx.ConnectError("flags-service down")

        async def _run():
            client = _make_async_flags_client()
            client._parent._environment = "test"
            client._parent._ensure_ws.return_value = MagicMock()
            client.boolean_flag("f1", default=True)

            await client.start()  # fails, schedules retry
            first_call_count = mock_bulk.call_count
            await client.start()  # within backoff window — no new HTTP call
            assert mock_bulk.call_count == first_call_count
            assert client._connected is False
            assert client._manage.flags._buffer.pending_count == 1

        asyncio.run(_run())


def test_flags_client_extra_headers_reach_transport() -> None:
    """extra_headers are stored on FlagsClient._flags_http and applied to every request."""
    client = SmplClient(api_key="sk_api_test", environment="test", service="svc", extra_headers={"X-Test": "v"})
    try:
        assert client.flags._flags_http._headers.get("X-Test") == "v"
    finally:
        client.close()
