"""Tests for smplkit.platform.clients — all sync and async sub-clients."""

from __future__ import annotations

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from smplkit.errors import NotFoundError, ValidationError
from smplkit.flags.types import AsyncContext, Context
from smplkit._buffer import _ContextRegistrationBuffer
from smplkit.platform.clients import (
    AsyncContextsClient,
    AsyncContextTypesClient,
    AsyncEnvironmentsClient,
    AsyncServicesClient,
    ContextsClient,
    ContextTypesClient,
    EnvironmentsClient,
    ServicesClient,
    _build_bulk_register_body,
    _check_status,
    _ct_from_parsed,
    _ct_resource_from_dict,
    _ct_to_resource,
    _ctx_entity_from_dict,
    _ctx_entity_from_parsed,
    _env_from_parsed,
    _env_resource_from_dict,
    _env_to_resource,
    _is_unset,
    _split_context_id,
    _svc_from_parsed,
    _svc_resource_from_dict,
    _svc_to_resource,
)
from smplkit.platform.models import (
    AsyncContextType,
    AsyncEnvironment,
    AsyncService,
    ContextType,
    Environment,
    Service,
)
from smplkit.platform.types import Color, EnvironmentClassification


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ok_resp(status: int = 200, body: bytes = b"{}"):
    resp = MagicMock()
    resp.status_code = status
    resp.content = body
    resp.parsed = None
    return resp


def _ok_json_resp(data: dict, status: int = 200):
    resp = _ok_resp(status=status, body=json.dumps(data).encode())
    return resp


def _parsed_env_resp(id="env-1", name="production", color=None, classification="STANDARD"):
    attrs = MagicMock()
    attrs.name = name
    attrs.color = color
    attrs.classification = classification
    attrs.created_at = "2026-01-01T00:00:00Z"
    attrs.updated_at = None

    resource = MagicMock()
    resource.id = id
    resource.attributes = attrs

    parsed = MagicMock()
    parsed.data = resource
    return parsed


def _parsed_ct_resp(id="ct-1", name="user", attributes=None):
    attr_meta = MagicMock()
    attr_meta.additional_properties = attributes or {}

    attrs = MagicMock()
    attrs.name = name
    attrs.attributes = attr_meta
    attrs.created_at = "2026-01-01T00:00:00Z"
    attrs.updated_at = None
    attrs.id = id

    resource = MagicMock()
    resource.id = id
    resource.attributes = attrs

    parsed = MagicMock()
    parsed.data = resource
    return parsed


def _parsed_ctx_resp(composite_id="user:u-1", name=None, attributes=None):
    attrs = MagicMock()
    attrs.name = name
    attrs.attributes = attributes or {}
    attrs.created_at = "2026-01-01T00:00:00Z"
    attrs.updated_at = None

    resource = MagicMock()
    resource.id = composite_id
    resource.attributes = attrs

    parsed = MagicMock()
    parsed.data = resource
    return parsed


def _make_env_client():
    app_http = MagicMock()
    return EnvironmentsClient(app_http)


def _make_async_env_client():
    app_http = MagicMock()
    return AsyncEnvironmentsClient(app_http)


def _make_svc_client():
    app_http = MagicMock()
    return ServicesClient(app_http)


def _make_async_svc_client():
    app_http = MagicMock()
    return AsyncServicesClient(app_http)


def _parsed_svc_resp(id="svc-1", name="User Service"):
    attrs = MagicMock()
    attrs.name = name
    attrs.created_at = "2026-01-01T00:00:00Z"
    attrs.updated_at = None

    resource = MagicMock()
    resource.id = id
    resource.attributes = attrs

    parsed = MagicMock()
    parsed.data = resource
    return parsed


def _make_ct_client():
    app_http = MagicMock()
    return ContextTypesClient(app_http)


def _make_async_ct_client():
    app_http = MagicMock()
    return AsyncContextTypesClient(app_http)


def _make_contexts_client():
    app_http = MagicMock()
    buf = _ContextRegistrationBuffer()
    return ContextsClient(app_http, buf)


def _make_async_contexts_client():
    app_http = MagicMock()
    buf = _ContextRegistrationBuffer()
    return AsyncContextsClient(app_http, buf)


# ---------------------------------------------------------------------------
# Standalone helpers
# ---------------------------------------------------------------------------


class TestSplitContextId:
    def test_composite_form(self):
        t, k = _split_context_id("user:u-1", None)
        assert t == "user"
        assert k == "u-1"

    def test_two_arg_form(self):
        t, k = _split_context_id("user", "u-1")
        assert t == "user"
        assert k == "u-1"

    def test_composite_missing_colon_raises(self):
        with pytest.raises(ValueError, match="type:key"):
            _split_context_id("nocolon", None)

    def test_composite_with_colon_in_key(self):
        t, k = _split_context_id("user:u:1:extra", None)
        assert t == "user"
        assert k == "u:1:extra"


class TestIsUnset:
    def test_unset_type(self):
        from smplkit._generated.app.types import UNSET

        assert _is_unset(UNSET) is True

    def test_regular_value(self):
        assert _is_unset(None) is False
        assert _is_unset("hello") is False
        assert _is_unset(0) is False


class TestCheckStatus:
    def test_ok_does_not_raise(self):
        _check_status(200, b"")

    def test_404_raises_not_found(self):
        from smplkit.errors import NotFoundError

        with pytest.raises(NotFoundError):
            _check_status(404, b'{"errors":[{"status":"404","title":"Not Found"}]}')

    def test_500_raises(self):
        from smplkit.errors import Error

        with pytest.raises(Error):
            _check_status(500, b'{"errors":[{"status":"500","title":"Server Error"}]}')


class TestEnvToResource:
    def test_basic(self):
        env = Environment(name="production", color="#ff0000", classification=EnvironmentClassification.STANDARD)
        body = _env_to_resource(env)
        assert body.data.attributes.name == "production"
        assert body.data.attributes.color == "#ff0000"
        assert body.data.attributes.classification == "STANDARD"

    def test_ad_hoc_classification(self):
        env = Environment(name="preview", classification=EnvironmentClassification.AD_HOC)
        body = _env_to_resource(env)
        assert body.data.attributes.classification == "AD_HOC"


class TestEnvFromParsed:
    def test_sync(self):
        parsed = _parsed_env_resp()
        result = _env_from_parsed(parsed, sync_client=MagicMock(), async_client=None)
        assert isinstance(result, Environment)
        assert result.id == "env-1"
        assert result.name == "production"
        assert result.classification == EnvironmentClassification.STANDARD

    def test_async(self):
        parsed = _parsed_env_resp(classification="AD_HOC")
        result = _env_from_parsed(parsed, sync_client=None, async_client=MagicMock())
        assert isinstance(result, AsyncEnvironment)
        assert result.classification == EnvironmentClassification.AD_HOC

    def test_unset_color_normalized_to_none(self):
        from smplkit._generated.app.types import UNSET

        parsed = _parsed_env_resp(color=UNSET)
        result = _env_from_parsed(parsed, sync_client=MagicMock(), async_client=None)
        assert result.color is None


class TestEnvResourceFromDict:
    def test_sync(self):
        item = {
            "id": "env-1",
            "attributes": {
                "name": "production",
                "color": "#ff0000",
                "classification": "STANDARD",
                "created_at": "2026-01-01",
            },
        }
        result = _env_resource_from_dict(item, sync_client=MagicMock())
        assert isinstance(result, Environment)
        assert result.id == "env-1"
        assert result.color == Color("#ff0000")

    def test_async_ad_hoc(self):
        item = {
            "id": "env-2",
            "attributes": {"name": "preview", "classification": "AD_HOC"},
        }
        result = _env_resource_from_dict(item, async_client=MagicMock())
        assert isinstance(result, AsyncEnvironment)
        assert result.classification == EnvironmentClassification.AD_HOC

    def test_missing_attrs(self):
        result = _env_resource_from_dict({}, sync_client=MagicMock())
        assert result.id is None
        assert result.name == ""


class TestCtToResource:
    def test_basic(self):
        ct = ContextType(id="ct-1", name="user", attributes={"plan": {"type": "string"}})
        body = _ct_to_resource(ct)
        assert body.data.id == "ct-1"
        assert body.data.attributes.name == "user"

    def test_attributes_set(self):
        ct = ContextType(id="ct-1", name="user", attributes={"plan": {}})
        body = _ct_to_resource(ct)
        assert body.data.attributes.attributes.additional_properties == {"plan": {}}


class TestCtFromParsed:
    def test_sync(self):
        parsed = _parsed_ct_resp(attributes={"plan": {"type": "string"}})
        result = _ct_from_parsed(parsed, sync_client=MagicMock(), async_client=None)
        assert isinstance(result, ContextType)
        assert result.attributes == {"plan": {"type": "string"}}

    def test_async(self):
        parsed = _parsed_ct_resp()
        result = _ct_from_parsed(parsed, sync_client=None, async_client=MagicMock())
        assert isinstance(result, AsyncContextType)

    def test_null_attr_meta(self):
        parsed = _parsed_ct_resp()
        parsed.data.attributes.attributes = None
        result = _ct_from_parsed(parsed, sync_client=MagicMock(), async_client=None)
        assert result.attributes == {}

    def test_unset_attr_meta(self):
        from smplkit._generated.app.types import UNSET

        parsed = _parsed_ct_resp()
        parsed.data.attributes.attributes = UNSET
        result = _ct_from_parsed(parsed, sync_client=MagicMock(), async_client=None)
        assert result.attributes == {}


class TestCtResourceFromDict:
    def test_with_attributes(self):
        item = {
            "id": "ct-1",
            "attributes": {
                "name": "user",
                "attributes": {"plan": {"type": "string"}},
                "created_at": "2026-01-01",
            },
        }
        result = _ct_resource_from_dict(item, sync_client=MagicMock())
        assert isinstance(result, ContextType)
        assert result.attributes["plan"] == {"type": "string"}

    def test_async(self):
        item = {"id": "ct-2", "attributes": {"name": "account"}}
        result = _ct_resource_from_dict(item, async_client=MagicMock())
        assert isinstance(result, AsyncContextType)

    def test_non_dict_attribute_values(self):
        item = {
            "id": "ct-3",
            "attributes": {"name": "x", "attributes": {"plan": "not-a-dict"}},
        }
        result = _ct_resource_from_dict(item, sync_client=MagicMock())
        assert result.attributes["plan"] == {}


class TestCtxEntityFromParsed:
    def test_sync(self):
        parsed = _parsed_ctx_resp("user:u-1", name="Alice")
        result = _ctx_entity_from_parsed(parsed, sync=True)
        assert isinstance(result, Context)
        assert result.type == "user"
        assert result.key == "u-1"
        assert result.name == "Alice"

    def test_async(self):
        parsed = _parsed_ctx_resp("account:acme")
        result = _ctx_entity_from_parsed(parsed, sync=False)
        assert isinstance(result, AsyncContext)
        assert result.type == "account"
        assert result.key == "acme"

    def test_no_colon_in_id(self):
        parsed = _parsed_ctx_resp("nocolon")
        result = _ctx_entity_from_parsed(parsed, sync=True)
        assert result.type == "nocolon"
        assert result.key == ""

    def test_dict_attributes(self):
        parsed = _parsed_ctx_resp("user:u-1")
        parsed.data.attributes.attributes = {"plan": "pro"}
        result = _ctx_entity_from_parsed(parsed, sync=True)
        assert result.attributes == {"plan": "pro"}

    def test_unset_attributes(self):
        from smplkit._generated.app.types import UNSET

        parsed = _parsed_ctx_resp("user:u-1")
        parsed.data.attributes.attributes = UNSET
        result = _ctx_entity_from_parsed(parsed, sync=True)
        assert result.attributes == {}

    def test_object_with_additional_properties(self):
        attr_obj = MagicMock()
        attr_obj.additional_properties = {"plan": "pro"}
        parsed = _parsed_ctx_resp("user:u-1")
        parsed.data.attributes.attributes = attr_obj
        result = _ctx_entity_from_parsed(parsed, sync=True)
        assert result.attributes == {"plan": "pro"}


class TestCtxEntityFromDict:
    def test_sync(self):
        item = {
            "id": "user:u-1",
            "attributes": {"name": "Alice", "attributes": {"plan": "pro"}},
        }
        result = _ctx_entity_from_dict(item)
        assert isinstance(result, Context)
        assert result.type == "user"
        assert result.key == "u-1"
        assert result.attributes == {"plan": "pro"}

    def test_async(self):
        item = {"id": "account:acme", "attributes": {}}
        result = _ctx_entity_from_dict(item, async_=True)
        assert isinstance(result, AsyncContext)

    def test_no_colon(self):
        result = _ctx_entity_from_dict({"id": "nocolon", "attributes": {}})
        assert result.type == "nocolon"
        assert result.key == ""

    def test_non_dict_raw_attrs(self):
        item = {"id": "user:u-1", "attributes": {"attributes": "not-a-dict"}}
        result = _ctx_entity_from_dict(item)
        assert result.attributes == {}


class TestBuildBulkRegisterBody:
    def test_basic(self):
        items = [
            {"type": "user", "key": "u-1", "attributes": {"plan": "pro"}},
        ]
        body = _build_bulk_register_body(items)
        assert len(body.contexts) == 1
        assert body.contexts[0].type_ == "user"
        assert body.contexts[0].key == "u-1"
        assert body.contexts[0].attributes.additional_properties == {"plan": "pro"}

    def test_no_attributes(self):
        items = [{"type": "user", "key": "u-2"}]
        body = _build_bulk_register_body(items)
        assert body.contexts[0].attributes.additional_properties == {}


# ---------------------------------------------------------------------------
# EnvironmentsClient (sync)
# ---------------------------------------------------------------------------


class TestEnvironmentsClient:
    def test_new(self):
        client = _make_env_client()
        env = client.new("env-1", name="production", color="#ff0000")
        assert isinstance(env, Environment)
        assert env.id == "env-1"
        assert env.name == "production"
        assert env.color == Color("#ff0000")

    @patch("smplkit.platform.clients._gen_list_environments.sync_detailed")
    def test_list(self, mock_list):
        data = [
            {"id": "env-1", "attributes": {"name": "production", "classification": "STANDARD"}},
        ]
        mock_list.return_value = _ok_json_resp({"data": data})
        client = _make_env_client()
        result = client.list()
        assert len(result) == 1
        assert result[0].name == "production"

    @patch("smplkit.platform.clients._gen_get_environment.sync_detailed")
    def test_get(self, mock_get):
        parsed = _parsed_env_resp()
        mock_get.return_value = _ok_resp()
        mock_get.return_value.parsed = parsed
        client = _make_env_client()
        env = client.get("env-1")
        assert env.id == "env-1"

    @patch("smplkit.platform.clients._gen_get_environment.sync_detailed")
    def test_get_not_found(self, mock_get):
        mock_get.return_value = _ok_resp()
        mock_get.return_value.parsed = None
        client = _make_env_client()
        with pytest.raises(NotFoundError):
            client.get("nonexistent")

    @patch("smplkit.platform.clients._gen_delete_environment.sync_detailed")
    def test_delete(self, mock_delete):
        mock_delete.return_value = _ok_resp(204, b"")
        client = _make_env_client()
        client.delete("env-1")
        mock_delete.assert_called_once()

    @patch("smplkit.platform.clients._gen_create_environment.sync_detailed")
    def test_create(self, mock_create):
        parsed = _parsed_env_resp()
        mock_create.return_value = _ok_resp(201)
        mock_create.return_value.parsed = parsed
        client = _make_env_client()
        env = Environment(name="production")
        result = client._create(env)
        assert result.id == "env-1"

    @patch("smplkit.platform.clients._gen_create_environment.sync_detailed")
    def test_create_null_parsed_raises(self, mock_create):
        mock_create.return_value = _ok_resp(201)
        mock_create.return_value.parsed = None
        client = _make_env_client()
        env = Environment(name="production")
        with pytest.raises(ValidationError):
            client._create(env)

    @patch("smplkit.platform.clients._gen_update_environment.sync_detailed")
    def test_update(self, mock_update):
        parsed = _parsed_env_resp()
        mock_update.return_value = _ok_resp()
        mock_update.return_value.parsed = parsed
        client = _make_env_client()
        env = Environment(client, id="env-1", name="production", created_at="2026-01-01")
        result = client._update(env)
        assert result.id == "env-1"

    def test_update_null_id_raises(self):
        client = _make_env_client()
        env = Environment(client, name="production", created_at="2026-01-01")
        env.id = None
        with pytest.raises(ValueError, match="no id"):
            client._update(env)

    @patch("smplkit.platform.clients._gen_update_environment.sync_detailed")
    def test_update_null_parsed_raises(self, mock_update):
        mock_update.return_value = _ok_resp()
        mock_update.return_value.parsed = None
        client = _make_env_client()
        env = Environment(client, id="env-1", name="production", created_at="2026-01-01")
        with pytest.raises(ValidationError):
            client._update(env)


# ---------------------------------------------------------------------------
# AsyncEnvironmentsClient
# ---------------------------------------------------------------------------


class TestAsyncEnvironmentsClient:
    def test_new(self):
        client = _make_async_env_client()
        env = client.new("env-1", name="staging")
        assert isinstance(env, AsyncEnvironment)

    @patch("smplkit.platform.clients._gen_list_environments.asyncio_detailed")
    def test_list(self, mock_list):
        data = [{"id": "env-1", "attributes": {"name": "staging", "classification": "AD_HOC"}}]
        mock_list.return_value = _ok_json_resp({"data": data})

        async def _run():
            mock_list.return_value = _ok_json_resp({"data": data})
            mock_coro = AsyncMock(return_value=_ok_json_resp({"data": data}))
            with patch("smplkit.platform.clients._gen_list_environments.asyncio_detailed", mock_coro):
                client = _make_async_env_client()
                result = await client.list()
                assert len(result) == 1
                assert result[0].classification == EnvironmentClassification.AD_HOC

        asyncio.run(_run())

    @patch("smplkit.platform.clients._gen_get_environment.asyncio_detailed")
    def test_get(self, mock_get):
        async def _run():
            parsed = _parsed_env_resp()
            resp = _ok_resp()
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_get_environment.asyncio_detailed", mock_coro):
                client = _make_async_env_client()
                env = await client.get("env-1")
                assert env.id == "env-1"
                assert isinstance(env, AsyncEnvironment)

        asyncio.run(_run())

    def test_get_not_found(self):
        async def _run():
            resp = _ok_resp()
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_get_environment.asyncio_detailed", mock_coro):
                client = _make_async_env_client()
                with pytest.raises(NotFoundError):
                    await client.get("nope")

        asyncio.run(_run())

    def test_delete(self):
        async def _run():
            mock_coro = AsyncMock(return_value=_ok_resp(204, b""))
            with patch("smplkit.platform.clients._gen_delete_environment.asyncio_detailed", mock_coro):
                client = _make_async_env_client()
                await client.delete("env-1")

        asyncio.run(_run())

    def test_create(self):
        async def _run():
            parsed = _parsed_env_resp()
            resp = _ok_resp(201)
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_create_environment.asyncio_detailed", mock_coro):
                client = _make_async_env_client()
                env = AsyncEnvironment(name="production")
                result = await client._create(env)
                assert result.id == "env-1"

        asyncio.run(_run())

    def test_create_null_parsed_raises(self):
        async def _run():
            resp = _ok_resp(201)
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_create_environment.asyncio_detailed", mock_coro):
                client = _make_async_env_client()
                env = AsyncEnvironment(name="production")
                with pytest.raises(ValidationError):
                    await client._create(env)

        asyncio.run(_run())

    def test_update(self):
        async def _run():
            parsed = _parsed_env_resp()
            resp = _ok_resp()
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_update_environment.asyncio_detailed", mock_coro):
                client = _make_async_env_client()
                env = AsyncEnvironment(client, id="env-1", name="production", created_at="2026-01-01")
                result = await client._update(env)
                assert result.id == "env-1"

        asyncio.run(_run())

    def test_update_null_id_raises(self):
        async def _run():
            client = _make_async_env_client()
            env = AsyncEnvironment(client, name="production", created_at="2026-01-01")
            env.id = None
            with pytest.raises(ValueError, match="no id"):
                await client._update(env)

        asyncio.run(_run())

    def test_update_null_parsed_raises(self):
        async def _run():
            resp = _ok_resp()
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_update_environment.asyncio_detailed", mock_coro):
                client = _make_async_env_client()
                env = AsyncEnvironment(client, id="env-1", name="production", created_at="2026-01-01")
                with pytest.raises(ValidationError):
                    await client._update(env)

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# Services helpers
# ---------------------------------------------------------------------------


class TestSvcToResource:
    def test_basic(self):
        svc = Service(id="user_service", name="User Service")
        body = _svc_to_resource(svc)
        assert body.data.id == "user_service"
        assert body.data.attributes.name == "User Service"
        assert body.data.type_ == "service"


class TestSvcFromParsed:
    def test_sync(self):
        parsed = _parsed_svc_resp()
        result = _svc_from_parsed(parsed, sync_client=MagicMock(), async_client=None)
        assert isinstance(result, Service)
        assert result.id == "svc-1"
        assert result.name == "User Service"

    def test_async(self):
        parsed = _parsed_svc_resp()
        result = _svc_from_parsed(parsed, sync_client=None, async_client=MagicMock())
        assert isinstance(result, AsyncService)
        assert result.id == "svc-1"


class TestSvcResourceFromDict:
    def test_sync(self):
        item = {
            "id": "user_service",
            "attributes": {
                "name": "User Service",
                "created_at": "2026-01-01",
            },
        }
        result = _svc_resource_from_dict(item, sync_client=MagicMock())
        assert isinstance(result, Service)
        assert result.id == "user_service"
        assert result.name == "User Service"

    def test_async(self):
        item = {"id": "svc-2", "attributes": {"name": "Billing Service"}}
        result = _svc_resource_from_dict(item, async_client=MagicMock())
        assert isinstance(result, AsyncService)
        assert result.name == "Billing Service"

    def test_missing_attrs(self):
        result = _svc_resource_from_dict({}, sync_client=MagicMock())
        assert result.id is None
        assert result.name == ""


# ---------------------------------------------------------------------------
# ServicesClient (sync)
# ---------------------------------------------------------------------------


class TestServicesClient:
    def test_new(self):
        client = _make_svc_client()
        svc = client.new("user_service", name="User Service")
        assert isinstance(svc, Service)
        assert svc.id == "user_service"
        assert svc.name == "User Service"
        assert svc.created_at is None

    @patch("smplkit.platform.clients._gen_list_services.sync_detailed")
    def test_list(self, mock_list):
        data = [
            {"id": "svc-1", "attributes": {"name": "User Service"}},
            {"id": "svc-2", "attributes": {"name": "Billing"}},
        ]
        mock_list.return_value = _ok_json_resp({"data": data})
        client = _make_svc_client()
        result = client.list()
        assert len(result) == 2
        assert result[0].name == "User Service"
        assert result[1].id == "svc-2"

    @patch("smplkit.platform.clients._gen_list_services.sync_detailed")
    def test_list_with_pagination(self, mock_list):
        mock_list.return_value = _ok_json_resp({"data": []})
        client = _make_svc_client()
        client.list(page_number=2, page_size=50)
        _, kwargs = mock_list.call_args
        assert kwargs["pagenumber"] == 2
        assert kwargs["pagesize"] == 50

    @patch("smplkit.platform.clients._gen_get_service.sync_detailed")
    def test_get(self, mock_get):
        parsed = _parsed_svc_resp()
        mock_get.return_value = _ok_resp()
        mock_get.return_value.parsed = parsed
        client = _make_svc_client()
        svc = client.get("svc-1")
        assert svc.id == "svc-1"

    @patch("smplkit.platform.clients._gen_get_service.sync_detailed")
    def test_get_not_found(self, mock_get):
        mock_get.return_value = _ok_resp()
        mock_get.return_value.parsed = None
        client = _make_svc_client()
        with pytest.raises(NotFoundError):
            client.get("nope")

    @patch("smplkit.platform.clients._gen_delete_service.sync_detailed")
    def test_delete(self, mock_delete):
        mock_delete.return_value = _ok_resp(204, b"")
        client = _make_svc_client()
        client.delete("svc-1")
        mock_delete.assert_called_once()

    @patch("smplkit.platform.clients._gen_create_service.sync_detailed")
    def test_create(self, mock_create):
        parsed = _parsed_svc_resp()
        mock_create.return_value = _ok_resp(201)
        mock_create.return_value.parsed = parsed
        client = _make_svc_client()
        svc = Service(id="user_service", name="User Service")
        result = client._create(svc)
        assert result.id == "svc-1"

    @patch("smplkit.platform.clients._gen_create_service.sync_detailed")
    def test_create_conflict_raises(self, mock_create):
        from smplkit.errors import ConflictError

        mock_create.return_value = _ok_resp(
            409, b'{"errors":[{"status":"409","title":"Conflict","detail":"service exists"}]}'
        )
        mock_create.return_value.parsed = None
        client = _make_svc_client()
        svc = Service(id="user_service", name="User Service")
        with pytest.raises(ConflictError):
            client._create(svc)

    @patch("smplkit.platform.clients._gen_create_service.sync_detailed")
    def test_create_null_parsed_raises(self, mock_create):
        mock_create.return_value = _ok_resp(201)
        mock_create.return_value.parsed = None
        client = _make_svc_client()
        svc = Service(id="user_service", name="User Service")
        with pytest.raises(ValidationError):
            client._create(svc)

    @patch("smplkit.platform.clients._gen_update_service.sync_detailed")
    def test_update(self, mock_update):
        parsed = _parsed_svc_resp()
        mock_update.return_value = _ok_resp()
        mock_update.return_value.parsed = parsed
        client = _make_svc_client()
        svc = Service(client, id="svc-1", name="Renamed", created_at="2026-01-01")
        result = client._update(svc)
        assert result.id == "svc-1"

    def test_update_null_id_raises(self):
        client = _make_svc_client()
        svc = Service(client, name="x", created_at="2026-01-01")
        svc.id = None
        with pytest.raises(ValueError, match="no id"):
            client._update(svc)

    @patch("smplkit.platform.clients._gen_update_service.sync_detailed")
    def test_update_null_parsed_raises(self, mock_update):
        mock_update.return_value = _ok_resp()
        mock_update.return_value.parsed = None
        client = _make_svc_client()
        svc = Service(client, id="svc-1", name="x", created_at="2026-01-01")
        with pytest.raises(ValidationError):
            client._update(svc)


# ---------------------------------------------------------------------------
# AsyncServicesClient
# ---------------------------------------------------------------------------


class TestAsyncServicesClient:
    def test_new(self):
        client = _make_async_svc_client()
        svc = client.new("user_service", name="User Service")
        assert isinstance(svc, AsyncService)

    def test_list(self):
        async def _run():
            data = [{"id": "svc-1", "attributes": {"name": "User Service"}}]
            mock_coro = AsyncMock(return_value=_ok_json_resp({"data": data}))
            with patch("smplkit.platform.clients._gen_list_services.asyncio_detailed", mock_coro):
                client = _make_async_svc_client()
                result = await client.list()
                assert len(result) == 1
                assert isinstance(result[0], AsyncService)

        asyncio.run(_run())

    def test_get(self):
        async def _run():
            parsed = _parsed_svc_resp()
            resp = _ok_resp()
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_get_service.asyncio_detailed", mock_coro):
                client = _make_async_svc_client()
                svc = await client.get("svc-1")
                assert svc.id == "svc-1"
                assert isinstance(svc, AsyncService)

        asyncio.run(_run())

    def test_get_not_found(self):
        async def _run():
            resp = _ok_resp()
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_get_service.asyncio_detailed", mock_coro):
                client = _make_async_svc_client()
                with pytest.raises(NotFoundError):
                    await client.get("nope")

        asyncio.run(_run())

    def test_delete(self):
        async def _run():
            mock_coro = AsyncMock(return_value=_ok_resp(204, b""))
            with patch("smplkit.platform.clients._gen_delete_service.asyncio_detailed", mock_coro):
                client = _make_async_svc_client()
                await client.delete("svc-1")

        asyncio.run(_run())

    def test_create(self):
        async def _run():
            parsed = _parsed_svc_resp()
            resp = _ok_resp(201)
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_create_service.asyncio_detailed", mock_coro):
                client = _make_async_svc_client()
                svc = AsyncService(id="user_service", name="User Service")
                result = await client._create(svc)
                assert result.id == "svc-1"

        asyncio.run(_run())

    def test_create_conflict_raises(self):
        from smplkit.errors import ConflictError

        async def _run():
            resp = _ok_resp(409, b'{"errors":[{"status":"409","title":"Conflict"}]}')
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_create_service.asyncio_detailed", mock_coro):
                client = _make_async_svc_client()
                svc = AsyncService(id="user_service", name="User Service")
                with pytest.raises(ConflictError):
                    await client._create(svc)

        asyncio.run(_run())

    def test_create_null_parsed_raises(self):
        async def _run():
            resp = _ok_resp(201)
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_create_service.asyncio_detailed", mock_coro):
                client = _make_async_svc_client()
                svc = AsyncService(id="user_service", name="User Service")
                with pytest.raises(ValidationError):
                    await client._create(svc)

        asyncio.run(_run())

    def test_update(self):
        async def _run():
            parsed = _parsed_svc_resp()
            resp = _ok_resp()
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_update_service.asyncio_detailed", mock_coro):
                client = _make_async_svc_client()
                svc = AsyncService(client, id="svc-1", name="Renamed", created_at="2026-01-01")
                result = await client._update(svc)
                assert result.id == "svc-1"

        asyncio.run(_run())

    def test_update_null_id_raises(self):
        async def _run():
            client = _make_async_svc_client()
            svc = AsyncService(client, name="x", created_at="2026-01-01")
            svc.id = None
            with pytest.raises(ValueError, match="no id"):
                await client._update(svc)

        asyncio.run(_run())

    def test_update_null_parsed_raises(self):
        async def _run():
            resp = _ok_resp()
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_update_service.asyncio_detailed", mock_coro):
                client = _make_async_svc_client()
                svc = AsyncService(client, id="svc-1", name="x", created_at="2026-01-01")
                with pytest.raises(ValidationError):
                    await client._update(svc)

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# ContextTypesClient (sync)
# ---------------------------------------------------------------------------


class TestContextTypesClient:
    def test_new(self):
        client = _make_ct_client()
        ct = client.new("user", name="User", attributes={"plan": {}})
        assert isinstance(ct, ContextType)
        assert ct.id == "user"
        assert ct.name == "User"

    def test_new_default_name(self):
        client = _make_ct_client()
        ct = client.new("user")
        assert ct.name == "user"

    @patch("smplkit.platform.clients._gen_list_context_types.sync_detailed")
    def test_list(self, mock_list):
        data = [{"id": "ct-1", "attributes": {"name": "user", "attributes": {"plan": {"type": "str"}}}}]
        mock_list.return_value = _ok_json_resp({"data": data})
        client = _make_ct_client()
        result = client.list()
        assert len(result) == 1
        assert result[0].name == "user"
        assert result[0].attributes == {"plan": {"type": "str"}}

    @patch("smplkit.platform.clients._gen_get_context_type.sync_detailed")
    def test_get(self, mock_get):
        parsed = _parsed_ct_resp()
        resp = _ok_resp()
        resp.parsed = parsed
        mock_get.return_value = resp
        client = _make_ct_client()
        ct = client.get("ct-1")
        assert ct.id == "ct-1"

    @patch("smplkit.platform.clients._gen_get_context_type.sync_detailed")
    def test_get_not_found(self, mock_get):
        resp = _ok_resp()
        resp.parsed = None
        mock_get.return_value = resp
        client = _make_ct_client()
        with pytest.raises(NotFoundError):
            client.get("nope")

    @patch("smplkit.platform.clients._gen_delete_context_type.sync_detailed")
    def test_delete(self, mock_delete):
        mock_delete.return_value = _ok_resp(204, b"")
        client = _make_ct_client()
        client.delete("ct-1")
        mock_delete.assert_called_once()

    @patch("smplkit.platform.clients._gen_create_context_type.sync_detailed")
    def test_create(self, mock_create):
        parsed = _parsed_ct_resp()
        resp = _ok_resp(201)
        resp.parsed = parsed
        mock_create.return_value = resp
        client = _make_ct_client()
        ct = ContextType(name="user")
        result = client._create(ct)
        assert result.id == "ct-1"

    @patch("smplkit.platform.clients._gen_create_context_type.sync_detailed")
    def test_create_null_parsed_raises(self, mock_create):
        resp = _ok_resp(201)
        resp.parsed = None
        mock_create.return_value = resp
        client = _make_ct_client()
        ct = ContextType(name="user")
        with pytest.raises(ValidationError):
            client._create(ct)

    @patch("smplkit.platform.clients._gen_update_context_type.sync_detailed")
    def test_update(self, mock_update):
        parsed = _parsed_ct_resp()
        resp = _ok_resp()
        resp.parsed = parsed
        mock_update.return_value = resp
        client = _make_ct_client()
        ct = ContextType(client, id="ct-1", name="user", created_at="2026-01-01")
        result = client._update(ct)
        assert result.id == "ct-1"

    def test_update_null_id_raises(self):
        client = _make_ct_client()
        ct = ContextType(client, name="user")
        ct.id = None
        with pytest.raises(ValueError, match="no id"):
            client._update(ct)

    @patch("smplkit.platform.clients._gen_update_context_type.sync_detailed")
    def test_update_null_parsed_raises(self, mock_update):
        resp = _ok_resp()
        resp.parsed = None
        mock_update.return_value = resp
        client = _make_ct_client()
        ct = ContextType(client, id="ct-1", name="user", created_at="2026-01-01")
        with pytest.raises(ValidationError):
            client._update(ct)


# ---------------------------------------------------------------------------
# AsyncContextTypesClient
# ---------------------------------------------------------------------------


class TestAsyncContextTypesClient:
    def test_new(self):
        client = _make_async_ct_client()
        ct = client.new("user", name="User")
        assert isinstance(ct, AsyncContextType)

    def test_list(self):
        async def _run():
            data = [{"id": "ct-1", "attributes": {"name": "user"}}]
            mock_coro = AsyncMock(return_value=_ok_json_resp({"data": data}))
            with patch("smplkit.platform.clients._gen_list_context_types.asyncio_detailed", mock_coro):
                client = _make_async_ct_client()
                result = await client.list()
                assert len(result) == 1

        asyncio.run(_run())

    def test_get(self):
        async def _run():
            parsed = _parsed_ct_resp()
            resp = _ok_resp()
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_get_context_type.asyncio_detailed", mock_coro):
                client = _make_async_ct_client()
                ct = await client.get("ct-1")
                assert isinstance(ct, AsyncContextType)

        asyncio.run(_run())

    def test_get_not_found(self):
        async def _run():
            resp = _ok_resp()
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_get_context_type.asyncio_detailed", mock_coro):
                client = _make_async_ct_client()
                with pytest.raises(NotFoundError):
                    await client.get("nope")

        asyncio.run(_run())

    def test_delete(self):
        async def _run():
            mock_coro = AsyncMock(return_value=_ok_resp(204, b""))
            with patch("smplkit.platform.clients._gen_delete_context_type.asyncio_detailed", mock_coro):
                client = _make_async_ct_client()
                await client.delete("ct-1")

        asyncio.run(_run())

    def test_create(self):
        async def _run():
            parsed = _parsed_ct_resp()
            resp = _ok_resp(201)
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_create_context_type.asyncio_detailed", mock_coro):
                client = _make_async_ct_client()
                ct = AsyncContextType(name="user")
                result = await client._create(ct)
                assert result.id == "ct-1"

        asyncio.run(_run())

    def test_create_null_parsed_raises(self):
        async def _run():
            resp = _ok_resp(201)
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_create_context_type.asyncio_detailed", mock_coro):
                client = _make_async_ct_client()
                ct = AsyncContextType(name="user")
                with pytest.raises(ValidationError):
                    await client._create(ct)

        asyncio.run(_run())

    def test_update(self):
        async def _run():
            parsed = _parsed_ct_resp()
            resp = _ok_resp()
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_update_context_type.asyncio_detailed", mock_coro):
                client = _make_async_ct_client()
                ct = AsyncContextType(client, id="ct-1", name="user", created_at="2026-01-01")
                result = await client._update(ct)
                assert isinstance(result, AsyncContextType)

        asyncio.run(_run())

    def test_update_null_id_raises(self):
        async def _run():
            client = _make_async_ct_client()
            ct = AsyncContextType(client, name="user")
            ct.id = None
            with pytest.raises(ValueError, match="no id"):
                await client._update(ct)

        asyncio.run(_run())

    def test_update_null_parsed_raises(self):
        async def _run():
            resp = _ok_resp()
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_update_context_type.asyncio_detailed", mock_coro):
                client = _make_async_ct_client()
                ct = AsyncContextType(client, id="ct-1", name="user", created_at="2026-01-01")
                with pytest.raises(ValidationError):
                    await client._update(ct)

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# ContextsClient (sync)
# ---------------------------------------------------------------------------


class TestContextsClient:
    def test_register_queues_to_buffer(self):
        client = _make_contexts_client()
        client.register(Context("user", "u-1", plan="pro"))
        assert client._buffer.pending_count == 1

    def test_register_list(self):
        client = _make_contexts_client()
        client.register([Context("user", "u-1"), Context("account", "acme")])
        assert client._buffer.pending_count == 2

    @patch("smplkit.platform.clients._gen_bulk_register_contexts.sync_detailed")
    def test_register_with_flush(self, mock_bulk):
        mock_bulk.return_value = _ok_resp()
        client = _make_contexts_client()
        client.register(Context("user", "u-1"), flush=True)
        mock_bulk.assert_called_once()
        assert client._buffer.pending_count == 0

    @patch("smplkit.platform.clients._gen_bulk_register_contexts.sync_detailed")
    def test_flush_empty_does_nothing(self, mock_bulk):
        client = _make_contexts_client()
        client.flush()
        mock_bulk.assert_not_called()

    @patch("smplkit.platform.clients._gen_bulk_register_contexts.sync_detailed")
    def test_flush_sends_batch(self, mock_bulk):
        mock_bulk.return_value = _ok_resp()
        client = _make_contexts_client()
        client._buffer.observe([Context("user", "u-1", plan="pro")])
        client.flush()
        mock_bulk.assert_called_once()
        _, kwargs = mock_bulk.call_args
        assert kwargs["body"].contexts[0].type_ == "user"

    @patch("smplkit.platform.clients._gen_list_contexts.sync_detailed")
    def test_list(self, mock_list):
        data = [{"id": "user:u-1", "attributes": {"name": "Alice"}}]
        mock_list.return_value = _ok_json_resp({"data": data})
        client = _make_contexts_client()
        result = client.list("user")
        assert len(result) == 1
        assert result[0].type == "user"
        assert result[0].key == "u-1"

    @patch("smplkit.platform.clients._gen_get_context.sync_detailed")
    def test_get_composite_id(self, mock_get):
        parsed = _parsed_ctx_resp("user:u-1")
        resp = _ok_resp()
        resp.parsed = parsed
        mock_get.return_value = resp
        client = _make_contexts_client()
        entity = client.get("user:u-1")
        assert entity.type == "user"
        mock_get.assert_called_once_with("user:u-1", client=client._app_http)

    @patch("smplkit.platform.clients._gen_get_context.sync_detailed")
    def test_get_two_args(self, mock_get):
        parsed = _parsed_ctx_resp("user:u-1")
        resp = _ok_resp()
        resp.parsed = parsed
        mock_get.return_value = resp
        client = _make_contexts_client()
        entity = client.get("user", "u-1")
        assert entity.key == "u-1"

    @patch("smplkit.platform.clients._gen_get_context.sync_detailed")
    def test_get_not_found(self, mock_get):
        resp = _ok_resp()
        resp.parsed = None
        mock_get.return_value = resp
        client = _make_contexts_client()
        with pytest.raises(NotFoundError):
            client.get("user:u-999")

    @patch("smplkit.platform.clients._gen_delete_context.sync_detailed")
    def test_delete_composite(self, mock_delete):
        mock_delete.return_value = _ok_resp(204, b"")
        client = _make_contexts_client()
        client.delete("user:u-1")
        mock_delete.assert_called_once_with("user:u-1", client=client._app_http)

    @patch("smplkit.platform.clients._gen_delete_context.sync_detailed")
    def test_delete_two_args(self, mock_delete):
        mock_delete.return_value = _ok_resp(204, b"")
        client = _make_contexts_client()
        client.delete("account", "acme")
        mock_delete.assert_called_once_with("account:acme", client=client._app_http)

    @patch("smplkit.platform.clients._gen_update_context.sync_detailed")
    def test_save_context(self, mock_update):
        parsed = _parsed_ctx_resp("user:u-1", name="Alice")
        resp = _ok_resp()
        resp.parsed = parsed
        mock_update.return_value = resp

        client = _make_contexts_client()
        ctx = Context("user", "u-1", {"plan": "pro"}, name="Alice")
        ctx._client = client
        ctx.save()
        mock_update.assert_called_once()
        args, kwargs = mock_update.call_args
        assert args[0] == "user:u-1"
        assert kwargs["body"].data.attributes.context_type == "user"
        assert kwargs["body"].data.attributes.name == "Alice"

    def test_save_without_client_raises(self):
        ctx = Context("user", "u-1")
        with pytest.raises(RuntimeError, match="cannot save"):
            ctx.save()

    @patch("smplkit.platform.clients._gen_update_context.sync_detailed")
    def test_save_validation_error_when_parsed_is_none(self, mock_update):
        resp = _ok_resp()
        resp.parsed = None
        mock_update.return_value = resp

        client = _make_contexts_client()
        ctx = Context("user", "u-1")
        ctx._client = client
        with pytest.raises(ValidationError):
            ctx.save()

    def test_delete_via_active_record(self):
        client = MagicMock()
        ctx = Context("user", "u-1")
        ctx._client = client
        ctx.delete()
        client.delete.assert_called_once_with("user:u-1")

    def test_delete_without_client_raises(self):
        ctx = Context("user", "u-1")
        with pytest.raises(RuntimeError, match="cannot delete"):
            ctx.delete()


# ---------------------------------------------------------------------------
# AsyncContextsClient
# ---------------------------------------------------------------------------


class TestAsyncContextsClient:
    def test_register_queues(self):
        client = _make_async_contexts_client()
        client.register(Context("user", "u-1"))
        assert client._buffer.pending_count == 1

    def test_register_list(self):
        client = _make_async_contexts_client()
        client.register([Context("user", "u-1"), Context("account", "acme")])
        assert client._buffer.pending_count == 2

    def test_register_then_flush(self):
        async def _run():
            mock_coro = AsyncMock(return_value=_ok_resp())
            with patch("smplkit.platform.clients._gen_bulk_register_contexts.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                client.register(Context("user", "u-1"))
                await client.flush()
                mock_coro.assert_called_once()

        asyncio.run(_run())

    def test_flush_empty_does_nothing(self):
        async def _run():
            mock_coro = AsyncMock(return_value=_ok_resp())
            with patch("smplkit.platform.clients._gen_bulk_register_contexts.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                await client.flush()
                mock_coro.assert_not_called()

        asyncio.run(_run())

    def test_flush_sends_batch(self):
        async def _run():
            mock_coro = AsyncMock(return_value=_ok_resp())
            with patch("smplkit.platform.clients._gen_bulk_register_contexts.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                client._buffer.observe([Context("user", "u-1")])
                await client.flush()
                mock_coro.assert_called_once()

        asyncio.run(_run())

    def test_list(self):
        async def _run():
            data = [{"id": "account:acme", "attributes": {}}]
            mock_coro = AsyncMock(return_value=_ok_json_resp({"data": data}))
            with patch("smplkit.platform.clients._gen_list_contexts.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                result = await client.list("account")
                assert isinstance(result[0], AsyncContext)
                assert result[0].type == "account"

        asyncio.run(_run())

    def test_get_composite(self):
        async def _run():
            parsed = _parsed_ctx_resp("user:u-1")
            resp = _ok_resp()
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_get_context.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                entity = await client.get("user:u-1")
                assert isinstance(entity, AsyncContext)
                assert entity.type == "user"

        asyncio.run(_run())

    def test_get_two_args(self):
        async def _run():
            parsed = _parsed_ctx_resp("user:u-1")
            resp = _ok_resp()
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_get_context.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                entity = await client.get("user", "u-1")
                assert entity.key == "u-1"

        asyncio.run(_run())

    def test_get_not_found(self):
        async def _run():
            resp = _ok_resp()
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_get_context.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                with pytest.raises(NotFoundError):
                    await client.get("user:nope")

        asyncio.run(_run())

    def test_delete_composite(self):
        async def _run():
            mock_coro = AsyncMock(return_value=_ok_resp(204, b""))
            with patch("smplkit.platform.clients._gen_delete_context.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                await client.delete("user:u-1")
                mock_coro.assert_called_once_with("user:u-1", client=client._app_http)

        asyncio.run(_run())

    def test_delete_two_args(self):
        async def _run():
            mock_coro = AsyncMock(return_value=_ok_resp(204, b""))
            with patch("smplkit.platform.clients._gen_delete_context.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                await client.delete("account", "acme")
                mock_coro.assert_called_once_with("account:acme", client=client._app_http)

        asyncio.run(_run())

    def test_save_context(self):
        async def _run():
            parsed = _parsed_ctx_resp("user:u-1", name="Alice")
            resp = _ok_resp()
            resp.parsed = parsed
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_update_context.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                ctx = AsyncContext("user", "u-1", {"plan": "pro"}, name="Alice")
                ctx._client = client
                await ctx.save()
                mock_coro.assert_called_once()

        asyncio.run(_run())

    def test_save_without_client_raises(self):
        async def _run():
            ctx = AsyncContext("user", "u-1")
            with pytest.raises(RuntimeError, match="cannot save"):
                await ctx.save()

        asyncio.run(_run())

    def test_save_validation_error_when_parsed_is_none(self):
        async def _run():
            resp = _ok_resp()
            resp.parsed = None
            mock_coro = AsyncMock(return_value=resp)
            with patch("smplkit.platform.clients._gen_update_context.asyncio_detailed", mock_coro):
                client = _make_async_contexts_client()
                ctx = AsyncContext("user", "u-1")
                ctx._client = client
                with pytest.raises(ValidationError):
                    await ctx.save()

        asyncio.run(_run())

    def test_delete_via_active_record(self):
        async def _run():
            client = MagicMock()
            client.delete = AsyncMock()
            ctx = AsyncContext("user", "u-1")
            ctx._client = client
            await ctx.delete()
            client.delete.assert_called_once_with("user:u-1")

        asyncio.run(_run())

    def test_delete_without_client_raises(self):
        async def _run():
            ctx = AsyncContext("user", "u-1")
            with pytest.raises(RuntimeError, match="cannot delete"):
                await ctx.delete()

        asyncio.run(_run())


class TestMgmtConfigRegisterAndFlush:
    """``ConfigClient`` discovery-buffer methods: register/flush/threshold."""

    @patch("smplkit.config.clients.bulk_register_configs.sync_detailed")
    def test_register_config_then_flush(self, mock_bulk):
        from smplkit.config.clients import ConfigClient as _MgmtConfigClient

        mock_bulk.return_value = _ok_resp()
        client = _MgmtConfigClient(transport=MagicMock())
        client.register_config("billing", service="svc", environment="prod")
        assert client.pending_count == 1
        client.flush()
        mock_bulk.assert_called_once()
        assert client.pending_count == 0

    @patch("smplkit.config.clients.bulk_register_configs.sync_detailed")
    def test_register_config_item_attaches(self, mock_bulk):
        from smplkit.config.clients import ConfigClient as _MgmtConfigClient

        mock_bulk.return_value = _ok_resp()
        client = _MgmtConfigClient(transport=MagicMock())
        client.register_config("billing", service="svc", environment="prod")
        client.register_config_item("billing", "max_seats", "NUMBER", 5, "Max.")
        client.flush()
        # The bulk request was built with one config carrying one item.
        body = mock_bulk.call_args.kwargs["body"]
        assert len(body.configs) == 1
        item = body.configs[0]
        assert "max_seats" in item.items.additional_properties

    @patch("smplkit.config.clients.bulk_register_configs.sync_detailed")
    def test_register_config_item_without_declare_is_dropped(self, mock_bulk):
        from smplkit.config.clients import ConfigClient as _MgmtConfigClient

        mock_bulk.return_value = _ok_resp()
        client = _MgmtConfigClient(transport=MagicMock())
        # No prior register_config; register_config_item is a no-op.
        client.register_config_item("unknown", "k", "NUMBER", 1)
        assert client.pending_count == 0
        client.flush()
        mock_bulk.assert_not_called()

    @patch("smplkit.config.clients.bulk_register_configs.sync_detailed")
    def test_flush_with_empty_buffer_is_noop(self, mock_bulk):
        from smplkit.config.clients import ConfigClient as _MgmtConfigClient

        client = _MgmtConfigClient(transport=MagicMock())
        client.flush()
        mock_bulk.assert_not_called()

    @patch("smplkit.config.clients.bulk_register_configs.sync_detailed")
    def test_threshold_triggers_background_flush(self, mock_bulk):
        from smplkit.config.clients import ConfigClient as _MgmtConfigClient

        mock_bulk.return_value = _ok_resp()
        client = _MgmtConfigClient(transport=MagicMock())
        captured: list = []

        def fake_thread(target=None, daemon=None):
            captured.append(target)
            t = MagicMock()
            t.start = lambda: None
            return t

        with patch("smplkit.config.clients._CONFIG_BATCH_FLUSH_SIZE", 1):
            with patch("smplkit.config.clients.threading.Thread", side_effect=fake_thread):
                # Hit the threshold via register_config.
                client.register_config("billing", service="svc", environment="prod")
        assert captured  # Thread was started.

    @patch("smplkit.config.clients.bulk_register_configs.sync_detailed")
    def test_threshold_via_register_config_item(self, mock_bulk):
        from smplkit.config.clients import ConfigClient as _MgmtConfigClient

        mock_bulk.return_value = _ok_resp()
        client = _MgmtConfigClient(transport=MagicMock())
        captured: list = []

        def fake_thread(target=None, daemon=None):
            captured.append(target)
            t = MagicMock()
            t.start = lambda: target()
            return t

        client.register_config("billing", service="svc", environment="prod")
        with patch("smplkit.config.clients._CONFIG_BATCH_FLUSH_SIZE", 1):
            with patch("smplkit.config.clients.threading.Thread", side_effect=fake_thread):
                client.register_config_item("billing", "max", "NUMBER", 5)
        assert captured

    @patch("smplkit.config.clients.bulk_register_configs.sync_detailed")
    def test_threshold_flush_swallows_errors(self, mock_bulk, caplog):
        import logging as _logging

        from smplkit.config.clients import ConfigClient as _MgmtConfigClient

        mock_bulk.side_effect = RuntimeError("boom")
        client = _MgmtConfigClient(transport=MagicMock())
        client.register_config("billing", service="svc", environment="prod")
        with caplog.at_level(_logging.WARNING, logger="smplkit"):
            client._threshold_flush()
        assert any("Config registration flush failed" in r.message for r in caplog.records)

    @patch("smplkit.config.clients.bulk_register_configs.sync_detailed")
    def test_flush_propagates_unexpected_errors(self, mock_bulk):
        from smplkit.config.clients import ConfigClient as _MgmtConfigClient

        mock_bulk.side_effect = RuntimeError("oops")
        client = _MgmtConfigClient(transport=MagicMock())
        client.register_config("billing", service="svc", environment="prod")
        with pytest.raises(RuntimeError):
            client.flush()

    @patch("smplkit.config.clients.bulk_register_configs.sync_detailed")
    def test_flush_reraises_network_error(self, mock_bulk):
        import httpx

        from smplkit.errors import ConnectionError as SmplConnectionError
        from smplkit.config.clients import ConfigClient as _MgmtConfigClient

        mock_bulk.side_effect = httpx.ConnectError("nope")
        http = MagicMock()
        http._base_url = "http://nope.test"
        client = _MgmtConfigClient(transport=http)
        client.register_config("billing", service="svc", environment="prod")
        with pytest.raises(SmplConnectionError):
            client.flush()


class TestAsyncMgmtConfigRegisterAndFlush:
    def test_flush_propagates_unexpected_errors(self):
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        async def _run():
            mock_coro = AsyncMock(side_effect=RuntimeError("oops"))
            with patch("smplkit.config.clients.bulk_register_configs.asyncio_detailed", mock_coro):
                client = _AsyncMgmtConfigClient(transport=MagicMock())
                client.register_config("billing", service="svc", environment="prod")
                with pytest.raises(RuntimeError):
                    await client.flush()

        asyncio.run(_run())

    def test_async_flush_empty_buffer_is_noop(self):
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        async def _run():
            with patch("smplkit.config.clients.bulk_register_configs.asyncio_detailed") as mock_bulk:
                client = _AsyncMgmtConfigClient(transport=MagicMock())
                await client.flush()
            mock_bulk.assert_not_called()

        asyncio.run(_run())

    def test_async_flush_reraises_network_error(self):
        import httpx

        from smplkit.errors import ConnectionError as SmplConnectionError
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        async def _run():
            mock_coro = AsyncMock(side_effect=httpx.ConnectError("nope"))
            with patch("smplkit.config.clients.bulk_register_configs.asyncio_detailed", mock_coro):
                http = MagicMock()
                http._base_url = "http://nope.test"
                client = _AsyncMgmtConfigClient(transport=http)
                client.register_config("billing", service="svc", environment="prod")
                with pytest.raises(SmplConnectionError):
                    await client.flush()

        asyncio.run(_run())

    def test_flush_sync_drains_buffer(self):
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        with patch("smplkit.config.clients.bulk_register_configs.sync_detailed") as mock_bulk:
            mock_bulk.return_value = _ok_resp()
            client = _AsyncMgmtConfigClient(transport=MagicMock())
            client.register_config("billing", service="svc", environment="prod")
            client.flush_sync()
            mock_bulk.assert_called_once()

    def test_flush_sync_empty_buffer_is_noop(self):
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        with patch("smplkit.config.clients.bulk_register_configs.sync_detailed") as mock_bulk:
            client = _AsyncMgmtConfigClient(transport=MagicMock())
            client.flush_sync()
        mock_bulk.assert_not_called()

    def test_flush_sync_reraises_network_error(self):
        import httpx

        from smplkit.errors import ConnectionError as SmplConnectionError
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        with patch("smplkit.config.clients.bulk_register_configs.sync_detailed") as mock_bulk:
            mock_bulk.side_effect = httpx.ConnectError("nope")
            http = MagicMock()
            http._base_url = "http://nope.test"
            client = _AsyncMgmtConfigClient(transport=http)
            client.register_config("billing", service="svc", environment="prod")
            with pytest.raises(SmplConnectionError):
                client.flush_sync()

    def test_flush_sync_propagates_unexpected_errors(self):
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        with patch("smplkit.config.clients.bulk_register_configs.sync_detailed") as mock_bulk:
            mock_bulk.side_effect = RuntimeError("oops")
            client = _AsyncMgmtConfigClient(transport=MagicMock())
            client.register_config("billing", service="svc", environment="prod")
            with pytest.raises(RuntimeError):
                client.flush_sync()

    def test_async_threshold_triggers_background_flush(self):
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        captured: list = []

        def fake_thread(target=None, daemon=None):
            captured.append(target)
            t = MagicMock()
            t.start = lambda: None
            return t

        with patch("smplkit.config.clients.bulk_register_configs.sync_detailed") as mock_bulk:
            mock_bulk.return_value = _ok_resp()
            client = _AsyncMgmtConfigClient(transport=MagicMock())
            with patch("smplkit.config.clients._CONFIG_BATCH_FLUSH_SIZE", 1):
                with patch("smplkit.config.clients.threading.Thread", side_effect=fake_thread):
                    client.register_config("billing", service="svc", environment="prod")
        assert captured

    def test_async_threshold_via_register_item(self):
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        captured: list = []

        def fake_thread(target=None, daemon=None):
            captured.append(target)
            t = MagicMock()
            t.start = lambda: None
            return t

        with patch("smplkit.config.clients.bulk_register_configs.sync_detailed") as mock_bulk:
            mock_bulk.return_value = _ok_resp()
            client = _AsyncMgmtConfigClient(transport=MagicMock())
            client.register_config("billing", service="svc", environment="prod")
            with patch("smplkit.config.clients._CONFIG_BATCH_FLUSH_SIZE", 1):
                with patch("smplkit.config.clients.threading.Thread", side_effect=fake_thread):
                    client.register_config_item("billing", "max", "NUMBER", 5)
        assert captured

    def test_async_threshold_flush_swallows_errors(self, caplog):
        import logging as _logging

        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        with patch("smplkit.config.clients.bulk_register_configs.sync_detailed") as mock_bulk:
            mock_bulk.side_effect = RuntimeError("boom")
            client = _AsyncMgmtConfigClient(transport=MagicMock())
            client.register_config("billing", service="svc", environment="prod")
            with caplog.at_level(_logging.WARNING, logger="smplkit"):
                client._threshold_flush_sync()
        assert any("Config registration flush failed" in r.message for r in caplog.records)

    def test_async_pending_count(self):
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        client = _AsyncMgmtConfigClient(transport=MagicMock())
        assert client.pending_count == 0
        client.register_config("billing", service="svc", environment="prod")
        assert client.pending_count == 1

    def test_async_flush_success_path(self):
        from smplkit.config.clients import AsyncConfigClient as _AsyncMgmtConfigClient

        async def _run():
            mock_coro = AsyncMock(return_value=_ok_resp())
            with patch(
                "smplkit.config.clients.bulk_register_configs.asyncio_detailed",
                mock_coro,
            ):
                client = _AsyncMgmtConfigClient(transport=MagicMock())
                client.register_config("billing", service="svc", environment="prod")
                await client.flush()
            mock_coro.assert_awaited_once()

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# Active-record delete() — Environment, ContextType, Context
# ---------------------------------------------------------------------------


class TestEnvironmentDelete:
    def test_calls_client_delete(self):
        from smplkit.platform.models import Environment

        client = MagicMock()
        env = Environment(client, id="staging", name="Staging")
        env.delete()
        client.delete.assert_called_once_with("staging")

    def test_without_client_raises(self):
        from smplkit.platform.models import Environment

        env = Environment(None, id="x", name="X")
        with pytest.raises(RuntimeError, match="cannot delete"):
            env.delete()


class TestAsyncEnvironmentDelete:
    def test_calls_client_delete(self):
        from smplkit.platform.models import AsyncEnvironment

        client = MagicMock()
        client.delete = AsyncMock()
        env = AsyncEnvironment(client, id="staging", name="Staging")
        asyncio.run(env.delete())
        client.delete.assert_called_once_with("staging")

    def test_without_client_raises(self):
        from smplkit.platform.models import AsyncEnvironment

        env = AsyncEnvironment(None, id="x", name="X")

        async def _run():
            with pytest.raises(RuntimeError, match="cannot delete"):
                await env.delete()

        asyncio.run(_run())


class TestContextTypeDelete:
    def test_calls_client_delete(self):
        from smplkit.platform.models import ContextType

        client = MagicMock()
        ct = ContextType(client, id="user", name="User")
        ct.delete()
        client.delete.assert_called_once_with("user")

    def test_without_client_raises(self):
        from smplkit.platform.models import ContextType

        ct = ContextType(None, id="x", name="X")
        with pytest.raises(RuntimeError, match="cannot delete"):
            ct.delete()


class TestAsyncContextTypeDelete:
    def test_calls_client_delete(self):
        from smplkit.platform.models import AsyncContextType

        client = MagicMock()
        client.delete = AsyncMock()
        ct = AsyncContextType(client, id="user", name="User")
        asyncio.run(ct.delete())
        client.delete.assert_called_once_with("user")

    def test_without_client_raises(self):
        from smplkit.platform.models import AsyncContextType

        ct = AsyncContextType(None, id="x", name="X")

        async def _run():
            with pytest.raises(RuntimeError, match="cannot delete"):
                await ct.delete()

        asyncio.run(_run())


class TestServiceDelete:
    def test_calls_client_delete(self):
        client = MagicMock()
        svc = Service(client, id="user_service", name="User Service")
        svc.delete()
        client.delete.assert_called_once_with("user_service")

    def test_without_client_raises(self):
        svc = Service(None, id="x", name="X")
        with pytest.raises(RuntimeError, match="cannot delete"):
            svc.delete()


class TestAsyncServiceDelete:
    def test_calls_client_delete(self):
        client = MagicMock()
        client.delete = AsyncMock()
        svc = AsyncService(client, id="user_service", name="User Service")
        asyncio.run(svc.delete())
        client.delete.assert_called_once_with("user_service")

    def test_without_client_raises(self):
        svc = AsyncService(None, id="x", name="X")

        async def _run():
            with pytest.raises(RuntimeError, match="cannot delete"):
                await svc.delete()

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# Threshold-flush behavior on the management sub-clients.
#
# Each ``register()`` checks ``_buffer.pending_count`` and spawns a daemon
# thread that runs ``_threshold_flush()`` once the buffer crosses its size
# threshold.  The threshold flush itself is a thin wrapper that calls
# ``flush()`` (or ``flush_sync()`` on async clients) and swallows
# exceptions so the thread doesn't propagate them.
# ---------------------------------------------------------------------------


class TestThresholdFlushTriggers:
    def test_contexts_register_spawns_thread_at_threshold(self):
        from smplkit._buffer import _CONTEXT_BATCH_FLUSH_SIZE

        client = _make_contexts_client()
        for i in range(_CONTEXT_BATCH_FLUSH_SIZE - 1):
            client.register([Context("user", f"u-{i}")])
        with patch("smplkit.platform.clients.threading.Thread") as mock_thread:
            client.register([Context("user", "trigger")])
            mock_thread.assert_called_once()
            mock_thread.return_value.start.assert_called_once()

    def test_async_contexts_register_spawns_thread_at_threshold(self):
        from smplkit._buffer import _CONTEXT_BATCH_FLUSH_SIZE

        client = _make_async_contexts_client()
        for i in range(_CONTEXT_BATCH_FLUSH_SIZE - 1):
            client.register([Context("user", f"u-{i}")])
        with patch("smplkit.platform.clients.threading.Thread") as mock_thread:
            client.register([Context("user", "trigger")])
            mock_thread.assert_called_once()

    def test_loggers_register_spawns_thread_at_threshold(self):
        from smplkit import LogLevel
        from smplkit.logging.clients import LoggersClient
        from smplkit.logging.sources import LoggerSource
        from smplkit._buffer import _LOGGER_BATCH_FLUSH_SIZE, _LoggerRegistrationBuffer

        client = LoggersClient(MagicMock(), base_url="http://logging:8003", buffer=_LoggerRegistrationBuffer())
        for i in range(_LOGGER_BATCH_FLUSH_SIZE - 1):
            client.register(LoggerSource(name=f"l-{i}", resolved_level=LogLevel.INFO))
        with patch("smplkit.logging.clients.threading.Thread") as mock_thread:
            client.register(LoggerSource(name="trigger", resolved_level=LogLevel.INFO))
            mock_thread.assert_called_once()

    def test_async_loggers_register_spawns_thread_at_threshold(self):
        from smplkit import LogLevel
        from smplkit.logging.clients import AsyncLoggersClient
        from smplkit.logging.sources import LoggerSource
        from smplkit._buffer import _LOGGER_BATCH_FLUSH_SIZE, _LoggerRegistrationBuffer

        client = AsyncLoggersClient(MagicMock(), base_url="http://logging:8003", buffer=_LoggerRegistrationBuffer())
        for i in range(_LOGGER_BATCH_FLUSH_SIZE - 1):
            client.register(LoggerSource(name=f"l-{i}", resolved_level=LogLevel.INFO))
        with patch("smplkit.logging.clients.threading.Thread") as mock_thread:
            client.register(LoggerSource(name="trigger", resolved_level=LogLevel.INFO))
            mock_thread.assert_called_once()


class TestThresholdFlushHandlesErrors:
    """``_threshold_flush`` swallows exceptions so the daemon thread doesn't crash."""

    @patch("smplkit.platform.clients._gen_bulk_register_contexts.sync_detailed")
    def test_contexts_threshold_flush_logs_warning(self, mock_bulk, caplog):
        import logging as stdlib_logging

        mock_bulk.side_effect = RuntimeError("network down")
        client = _make_contexts_client()
        client._buffer.observe([Context("user", "u-1")])
        with caplog.at_level(stdlib_logging.WARNING, logger="smplkit"):
            client._threshold_flush()
        assert any("Context registration flush failed" in r.message for r in caplog.records)

    def test_async_contexts_threshold_flush_logs_warning(self, caplog):
        import logging as stdlib_logging

        with patch("smplkit.platform.clients._gen_bulk_register_contexts.sync_detailed") as mock_bulk:
            mock_bulk.side_effect = RuntimeError("network down")
            client = _make_async_contexts_client()
            client._buffer.observe([Context("user", "u-1")])
            with caplog.at_level(stdlib_logging.WARNING, logger="smplkit"):
                client._threshold_flush()
            assert any("Context registration flush failed" in r.message for r in caplog.records)

    @patch("smplkit.logging.clients.bulk_register_loggers.sync_detailed")
    def test_loggers_threshold_flush_logs_warning(self, mock_bulk, caplog):
        import logging as stdlib_logging

        from smplkit import LogLevel
        from smplkit.logging.clients import LoggersClient
        from smplkit.logging.sources import LoggerSource
        from smplkit._buffer import _LoggerRegistrationBuffer

        mock_bulk.side_effect = RuntimeError("network down")
        client = LoggersClient(MagicMock(), base_url="http://logging:8003", buffer=_LoggerRegistrationBuffer())
        client.register(LoggerSource(name="l", resolved_level=LogLevel.INFO))
        with caplog.at_level(stdlib_logging.WARNING, logger="smplkit"):
            client._threshold_flush()
        assert any("Logger registration flush failed" in r.message for r in caplog.records)

    def test_async_loggers_threshold_flush_logs_warning(self, caplog):
        import logging as stdlib_logging

        from smplkit import LogLevel
        from smplkit.logging.clients import AsyncLoggersClient
        from smplkit.logging.sources import LoggerSource
        from smplkit._buffer import _LoggerRegistrationBuffer

        with patch("smplkit.logging.clients.bulk_register_loggers.sync_detailed") as mock_bulk:
            mock_bulk.side_effect = RuntimeError("network down")
            client = AsyncLoggersClient(MagicMock(), base_url="http://logging:8003", buffer=_LoggerRegistrationBuffer())
            client.register(LoggerSource(name="l", resolved_level=LogLevel.INFO))
            with caplog.at_level(stdlib_logging.WARNING, logger="smplkit"):
                client._threshold_flush()
            assert any("Logger registration flush failed" in r.message for r in caplog.records)


class TestPendingCountProperty:
    """Each sub-client exposes ``pending_count`` as a thin pass-through to the buffer."""

    def test_contexts_pending_count(self):
        client = _make_contexts_client()
        assert client.pending_count == 0
        client.register(Context("user", "u-1"))
        assert client.pending_count == 1

    def test_async_contexts_pending_count(self):
        client = _make_async_contexts_client()
        assert client.pending_count == 0
        client.register(Context("user", "u-1"))
        assert client.pending_count == 1

    def test_loggers_pending_count(self):
        from smplkit import LogLevel
        from smplkit.logging.clients import LoggersClient
        from smplkit.logging.sources import LoggerSource
        from smplkit._buffer import _LoggerRegistrationBuffer

        client = LoggersClient(MagicMock(), base_url="http://logging:8003", buffer=_LoggerRegistrationBuffer())
        assert client.pending_count == 0
        client.register(LoggerSource(name="l", resolved_level=LogLevel.INFO))
        assert client.pending_count == 1

    def test_async_loggers_pending_count(self):
        from smplkit import LogLevel
        from smplkit.logging.clients import AsyncLoggersClient
        from smplkit.logging.sources import LoggerSource
        from smplkit._buffer import _LoggerRegistrationBuffer

        client = AsyncLoggersClient(MagicMock(), base_url="http://logging:8003", buffer=_LoggerRegistrationBuffer())
        assert client.pending_count == 0
        client.register(LoggerSource(name="l", resolved_level=LogLevel.INFO))
        assert client.pending_count == 1


class TestAsyncContextsFlushSync:
    """``flush_sync`` lets the periodic-flush thread drain the async client's buffer."""

    @patch("smplkit.platform.clients._gen_bulk_register_contexts.sync_detailed")
    def test_flush_sync_drains_buffer(self, mock_bulk):
        mock_bulk.return_value = _ok_resp()
        client = _make_async_contexts_client()
        client._buffer.observe([Context("user", "u-1")])
        client.flush_sync()
        mock_bulk.assert_called_once()

    @patch("smplkit.platform.clients._gen_bulk_register_contexts.sync_detailed")
    def test_flush_sync_empty(self, mock_bulk):
        client = _make_async_contexts_client()
        client.flush_sync()
        mock_bulk.assert_not_called()
