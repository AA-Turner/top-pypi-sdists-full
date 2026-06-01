"""Smpl management-plane sub-clients and top-level :class:`SmplManagementClient`.

This module owns every CRUD/management surface in the SDK.  The top-level
:class:`SmplManagementClient` (and :class:`AsyncSmplManagementClient`)
expose them as flat namespaces:

- ``mgmt.contexts.*``         (was ``client.management.contexts.*``)
- ``mgmt.context_types.*``    (was ``client.management.context_types.*``)
- ``mgmt.environments.*``     (was ``client.management.environments.*``)
- ``mgmt.account_settings.*`` (was ``client.management.account_settings.*``)
- ``mgmt.config.*``           (was ``client.config.management.*``)
- ``mgmt.flags.*``            (was ``client.flags.management.*``)
- ``mgmt.loggers.*``          (was ``client.logging.management.*`` — logger surface)
- ``mgmt.log_groups.*``       (was ``client.logging.management.*`` — group surface)

The runtime :class:`smplkit.SmplClient` no longer exposes a ``.management``
attribute anywhere; runtime and management are strictly separated.
"""

from __future__ import annotations

import json
import logging
import threading
from typing import TYPE_CHECKING, Any, overload

import httpx

from smplkit._config import ResolvedManagementConfig, _service_url, resolve_management_config
from smplkit._debug import enable_debug
from smplkit._errors import (
    ConflictError,
    ConnectionError,
    NotFoundError,
    TimeoutError,
    ValidationError,
    _raise_for_status,
)
from smplkit._helpers import key_to_display_name
from smplkit._generated.app.api.context_types import (
    create_context_type as _gen_create_context_type,
    delete_context_type as _gen_delete_context_type,
    get_context_type as _gen_get_context_type,
    list_context_types as _gen_list_context_types,
    update_context_type as _gen_update_context_type,
)
from smplkit._generated.app.api.contexts import (
    bulk_register_contexts as _gen_bulk_register_contexts,
    delete_context as _gen_delete_context,
    get_context as _gen_get_context,
    list_contexts as _gen_list_contexts,
    update_context as _gen_update_context,
)
from smplkit._generated.app.api.environments import (
    create_environment as _gen_create_environment,
    delete_environment as _gen_delete_environment,
    get_environment as _gen_get_environment,
    list_environments as _gen_list_environments,
    update_environment as _gen_update_environment,
)
from smplkit._generated.app.api.services import (
    create_service as _gen_create_service,
    delete_service as _gen_delete_service,
    get_service as _gen_get_service,
    list_services as _gen_list_services,
    update_service as _gen_update_service,
)
from smplkit._generated.app.client import AuthenticatedClient as _AppAuthClient
from smplkit._generated.audit.client import AuthenticatedClient as _AuditAuthClient
from smplkit._generated.app.models import (
    Context as _GenContext,
    ContextAttributes as _GenContextAttributes,
    ContextBulkItem as _GenContextBulkItem,
    ContextBulkItemAttributes as _GenContextBulkItemAttributes,
    ContextBulkRegister as _GenContextBulkRegister,
    ContextResource as _GenContextResource,
    ContextResponse as _GenContextResponse,
    ContextType as _GenContextType,
    ContextTypeAttributes as _GenContextTypeAttributes,
    ContextTypeRequest as _GenContextTypeRequest,
    ContextTypeResource as _GenContextTypeResource,
    Environment as _GenEnvironment,
    EnvironmentRequest as _GenEnvironmentRequest,
    EnvironmentResource as _GenEnvironmentResource,
    Service as _GenService,
    ServiceRequest as _GenServiceRequest,
    ServiceResource as _GenServiceResource,
)
from smplkit._generated.config.api.configs import (
    bulk_register_configs as _gen_bulk_register_configs,
    create_config as _gen_create_config,
    delete_config as _gen_delete_config,
    get_config as _gen_get_config,
    list_configs as _gen_list_configs,
    update_config as _gen_update_config,
)
from smplkit._generated.config.client import AuthenticatedClient as _ConfigAuthClient
from smplkit._generated.config.models.config_bulk_item import (
    ConfigBulkItem as _GenConfigBulkItem,
)
from smplkit._generated.config.models.config_bulk_item_items_type_0 import (
    ConfigBulkItemItemsType0 as _GenConfigBulkItemItems,
)
from smplkit._generated.config.models.config_bulk_request import (
    ConfigBulkRequest as _GenConfigBulkRequest,
)
from smplkit._generated.config.models.config_item_definition import (
    ConfigItemDefinition as _GenConfigItemDefinition,
)
from smplkit._generated.config.types import UNSET as _CONFIG_UNSET
from smplkit._generated.flags.api.flags import (
    bulk_register_flags as _gen_bulk_register_flags,
    create_flag as _gen_create_flag,
    delete_flag as _gen_delete_flag,
    get_flag as _gen_get_flag,
    list_flags as _gen_list_flags,
    update_flag as _gen_update_flag,
)
from smplkit._generated.flags.models.flag_bulk_item import FlagBulkItem as _GenFlagBulkItem
from smplkit._generated.flags.models.flag_bulk_request import FlagBulkRequest as _GenFlagBulkRequest
from smplkit._generated.flags.client import AuthenticatedClient as _FlagsAuthClient
from smplkit._generated.logging.api.log_groups import (
    create_log_group as _gen_create_log_group,
    delete_log_group as _gen_delete_log_group,
    get_log_group as _gen_get_log_group,
    list_log_groups as _gen_list_log_groups,
    update_log_group as _gen_update_log_group,
)
from smplkit._generated.logging.api.loggers import (
    bulk_register_loggers as _gen_bulk_register_loggers,
    delete_logger as _gen_delete_logger,
    get_logger as _gen_get_logger,
    list_loggers as _gen_list_loggers,
    update_logger as _gen_update_logger,
)
from smplkit._generated.logging.client import AuthenticatedClient as _LoggingAuthClient
from smplkit.config.helpers import (
    _build_config_request_body,
    _resource_to_config,
    _resource_to_async_config,
)
from smplkit.config.models import AsyncConfig, Config
from smplkit.flags.helpers import (
    _build_flag_request_body,
    _flag_dict_from_json,
)
from smplkit.flags.models import (
    AsyncBooleanFlag,
    AsyncFlag,
    AsyncJsonFlag,
    AsyncNumberFlag,
    AsyncStringFlag,
    BooleanFlag,
    Flag,
    FlagValue,
    JsonFlag,
    NumberFlag,
    StringFlag,
)
from smplkit.logging._normalize import normalize_logger_name
from smplkit.logging._sources import LoggerSource
from smplkit.logging.helpers import (
    _build_log_group_body,
    _build_logger_body,
    _logger_resource_to_async_model,
    _logger_resource_to_model,
    _loglevel_value,
    _log_group_resource_to_async_model,
    _log_group_resource_to_model,
)
from smplkit.logging.models import (
    AsyncSmplLogGroup,
    AsyncSmplLogger,
    SmplLogGroup,
    SmplLogger,
    _environments_to_wire as _logger_environments_to_wire,
)
from smplkit.flags.types import AsyncContext, Context
from smplkit.management.models import (
    AccountSettings,
    AsyncAccountSettings,
    AsyncContextType,
    AsyncEnvironment,
    AsyncService,
    ContextType,
    Environment,
    Service,
)
from smplkit.management._buffer import (  # noqa: F401  (some imports below)
    _CONFIG_BATCH_FLUSH_SIZE,
    _ConfigRegistrationBuffer,
    _CONTEXT_BATCH_FLUSH_SIZE,
    _FLAG_BATCH_FLUSH_SIZE,
    _LOGGER_BATCH_FLUSH_SIZE,
)
from smplkit.management.types import Color, EnvironmentClassification

if TYPE_CHECKING:  # pragma: no cover
    from smplkit.flags.types import FlagDeclaration
    from smplkit.management._buffer import _ContextRegistrationBuffer
    from smplkit.management.audit import (
        AsyncAuditClient as _MgmtAsyncAuditClient,
        AuditClient as _MgmtAuditClient,
    )

logger = logging.getLogger("smplkit")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _split_context_id(id_or_type: str, key: str | None) -> tuple[str, str]:
    """Resolve the two-arg or composite-id form to ``(type, key)``."""
    if key is None:
        if ":" not in id_or_type:
            raise ValueError(
                f"context id must be 'type:key' (got {id_or_type!r}); alternatively pass type and key as separate args"
            )
        ctx_type, _, ctx_key = id_or_type.partition(":")
        return ctx_type, ctx_key
    return id_or_type, key


def _env_to_resource(env: Environment | AsyncEnvironment) -> _GenEnvironmentRequest:
    attrs = _GenEnvironment(
        name=env.name,
        color=env.color.hex if env.color is not None else None,
        classification=env.classification.value,
    )
    resource = _GenEnvironmentResource(
        type_="environment",
        attributes=attrs,
        id=env.id,
    )
    return _GenEnvironmentRequest(data=resource)


def _env_from_parsed(
    parsed: Any, sync_client: EnvironmentsClient | None, async_client: AsyncEnvironmentsClient | None
) -> Any:
    """Build an Environment / AsyncEnvironment from a parsed EnvironmentResponse."""
    data = parsed.data
    attrs = data.attributes
    classification_value = getattr(attrs, "classification", None) or "STANDARD"
    if classification_value == "AD_HOC":
        classification = EnvironmentClassification.AD_HOC
    else:
        classification = EnvironmentClassification.STANDARD
    color_val = getattr(attrs, "color", None)
    if _is_unset(color_val):
        color_val = None
    if async_client is not None:
        return AsyncEnvironment(
            async_client,
            id=data.id,
            name=attrs.name,
            color=color_val,
            classification=classification,
            created_at=getattr(attrs, "created_at", None) or None,
            updated_at=getattr(attrs, "updated_at", None) or None,
        )
    return Environment(
        sync_client,
        id=data.id,
        name=attrs.name,
        color=color_val,
        classification=classification,
        created_at=getattr(attrs, "created_at", None) or None,
        updated_at=getattr(attrs, "updated_at", None) or None,
    )


def _ct_to_resource(ct: ContextType | AsyncContextType) -> _GenContextTypeRequest:
    attr_meta = _GenContextTypeAttributes()
    attr_meta.additional_properties = dict(ct.attributes)
    attrs = _GenContextType(name=ct.name, attributes=attr_meta)
    resource = _GenContextTypeResource(
        type_="context_type",
        attributes=attrs,
        id=ct.id,
    )
    return _GenContextTypeRequest(data=resource)


def _ct_from_parsed(
    parsed: Any, sync_client: ContextTypesClient | None, async_client: AsyncContextTypesClient | None
) -> Any:
    data = parsed.data
    attrs = data.attributes
    raw_attr_meta = getattr(attrs, "attributes", None)
    if raw_attr_meta is None or _is_unset(raw_attr_meta):
        attributes: dict[str, dict[str, Any]] = {}
    else:
        # Generated ContextTypeAttributes wraps a dict on additional_properties.
        attributes = dict(getattr(raw_attr_meta, "additional_properties", {}))
    if async_client is not None:
        return AsyncContextType(
            async_client,
            id=data.id,
            name=attrs.name,
            attributes=attributes,
            created_at=getattr(attrs, "created_at", None) or None,
            updated_at=getattr(attrs, "updated_at", None) or None,
        )
    return ContextType(
        sync_client,
        id=data.id,
        name=attrs.name,
        attributes=attributes,
        created_at=getattr(attrs, "created_at", None) or None,
        updated_at=getattr(attrs, "updated_at", None) or None,
    )


def _ctx_entity_from_parsed(parsed: Any, sync: bool, client: Any = None) -> Context | AsyncContext:
    """Build a :class:`Context` or :class:`AsyncContext` from a parsed ContextResponse.

    The on-the-wire id is the composite ``"type:key"``. We split it
    back into the two fields the model exposes (mirrored back as a
    composite via the ``id`` property).
    """
    data = parsed.data
    composite_id = data.id or ""
    if ":" in composite_id:
        ctx_type, _, ctx_key = composite_id.partition(":")
    else:
        ctx_type, ctx_key = composite_id, ""

    attrs = data.attributes
    attr_obj = getattr(attrs, "attributes", None)
    if attr_obj is None or _is_unset(attr_obj):
        attr_dict: dict[str, Any] = {}
    elif isinstance(attr_obj, dict):
        attr_dict = dict(attr_obj)
    else:
        attr_dict = dict(getattr(attr_obj, "additional_properties", {}))

    cls = Context if sync else AsyncContext
    ctx = cls(
        ctx_type,
        ctx_key,
        attr_dict,
        name=getattr(attrs, "name", None) or None,
        created_at=getattr(attrs, "created_at", None) or None,
        updated_at=getattr(attrs, "updated_at", None) or None,
    )
    ctx._client = client
    return ctx


def _ctx_to_resource(ctx: Context | AsyncContext) -> _GenContextResponse:
    """Build a wire ContextResponse body from a Context."""
    gen_attrs = _GenContextAttributes()
    gen_attrs.additional_properties = dict(ctx.attributes)
    attrs = _GenContext(
        context_type=ctx.type,
        name=ctx.name,
        attributes=gen_attrs,
    )
    resource = _GenContextResource(type_="context", attributes=attrs, id=ctx.id)
    return _GenContextResponse(data=resource)


def _is_unset(value: Any) -> bool:
    return type(value).__name__ == "Unset"


def _pagination_kwargs(page_number: int | None, page_size: int | None) -> dict[str, int]:
    """Build the ``pagenumber``/``pagesize`` kwargs for a generated list call.

    Each value is included only when the caller supplied a non-None override —
    omitting both yields ``{}``, letting the generated client send the
    server-default page (1) and size (1000).
    """
    kwargs: dict[str, int] = {}
    if page_number is not None:
        kwargs["pagenumber"] = page_number
    if page_size is not None:
        kwargs["pagesize"] = page_size
    return kwargs


def _check_status(status_code: int, content: bytes) -> None:
    _raise_for_status(int(status_code), content)


def _exc_url(exc: Exception) -> str | None:
    try:
        return str(exc.request.url)  # type: ignore[attr-defined]
    except Exception:
        return None


def _maybe_reraise_network_error(exc: Exception, base_url: str | None = None) -> None:
    """Re-raise httpx exceptions as SDK exceptions when applicable."""
    if isinstance(exc, httpx.TimeoutException):
        url = _exc_url(exc) or base_url
        msg = f"Request timed out connecting to {url}" if url else f"Request timed out: {exc}"
        raise TimeoutError(msg) from exc
    if isinstance(exc, httpx.HTTPError):
        url = _exc_url(exc) or base_url
        msg = f"Cannot connect to {url}: {exc}" if url else f"Connection error: {exc}"
        raise ConnectionError(msg) from exc
    if isinstance(exc, (NotFoundError, ConflictError, ValidationError)):
        raise exc


# ---------------------------------------------------------------------------
# Environments
# ---------------------------------------------------------------------------


class EnvironmentsClient:
    """Sync environment CRUD (``mgmt.environments``)."""

    def __init__(self, app_http: _AppAuthClient) -> None:
        self._app_http = app_http

    def new(
        self,
        id: str,
        *,
        name: str,
        color: Color | str | None = None,
        classification: EnvironmentClassification = EnvironmentClassification.STANDARD,
    ) -> Environment:
        """Return an unsaved :class:`Environment`. Call ``.save()`` to persist."""
        return Environment(
            self,
            id=id,
            name=name,
            color=color,
            classification=classification,
        )

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[Environment]:
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = _gen_list_environments.sync_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_env_resource_from_dict(item, sync_client=self) for item in body.get("data", [])]

    def get(self, id: str) -> Environment:
        resp = _gen_get_environment.sync_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"Environment with id {id!r} not found", status_code=404)
        return _env_from_parsed(resp.parsed, sync_client=self, async_client=None)

    def delete(self, id: str) -> None:
        resp = _gen_delete_environment.sync_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)

    def _create(self, env: Environment) -> Environment:
        body = _env_to_resource(env)
        resp = _gen_create_environment.sync_detailed(client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _env_from_parsed(resp.parsed, sync_client=self, async_client=None)

    def _update(self, env: Environment) -> Environment:
        body = _env_to_resource(env)
        if env.id is None:
            raise ValueError("cannot update an Environment with no id")
        resp = _gen_update_environment.sync_detailed(env.id, client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _env_from_parsed(resp.parsed, sync_client=self, async_client=None)


class AsyncEnvironmentsClient:
    """Async environment CRUD (``mgmt.environments``)."""

    def __init__(self, app_http: _AppAuthClient) -> None:
        self._app_http = app_http

    def new(
        self,
        id: str,
        *,
        name: str,
        color: Color | str | None = None,
        classification: EnvironmentClassification = EnvironmentClassification.STANDARD,
    ) -> AsyncEnvironment:
        return AsyncEnvironment(
            self,
            id=id,
            name=name,
            color=color,
            classification=classification,
        )

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncEnvironment]:
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = await _gen_list_environments.asyncio_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_env_resource_from_dict(item, async_client=self) for item in body.get("data", [])]

    async def get(self, id: str) -> AsyncEnvironment:
        resp = await _gen_get_environment.asyncio_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"Environment with id {id!r} not found", status_code=404)
        return _env_from_parsed(resp.parsed, sync_client=None, async_client=self)

    async def delete(self, id: str) -> None:
        resp = await _gen_delete_environment.asyncio_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)

    async def _create(self, env: AsyncEnvironment) -> AsyncEnvironment:
        body = _env_to_resource(env)
        resp = await _gen_create_environment.asyncio_detailed(client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _env_from_parsed(resp.parsed, sync_client=None, async_client=self)

    async def _update(self, env: AsyncEnvironment) -> AsyncEnvironment:
        body = _env_to_resource(env)
        if env.id is None:
            raise ValueError("cannot update an AsyncEnvironment with no id")
        resp = await _gen_update_environment.asyncio_detailed(env.id, client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _env_from_parsed(resp.parsed, sync_client=None, async_client=self)


def _env_resource_from_dict(
    item: dict[str, Any],
    *,
    sync_client: EnvironmentsClient | None = None,
    async_client: AsyncEnvironmentsClient | None = None,
) -> Any:
    """Build an Environment from a raw JSON resource dict (used by list)."""
    attrs = item.get("attributes") or {}
    classification = (
        EnvironmentClassification.AD_HOC
        if attrs.get("classification") == "AD_HOC"
        else EnvironmentClassification.STANDARD
    )
    if async_client is not None:
        return AsyncEnvironment(
            async_client,
            id=item.get("id"),
            name=attrs.get("name", ""),
            color=attrs.get("color"),
            classification=classification,
            created_at=attrs.get("created_at"),
            updated_at=attrs.get("updated_at"),
        )
    return Environment(
        sync_client,
        id=item.get("id"),
        name=attrs.get("name", ""),
        color=attrs.get("color"),
        classification=classification,
        created_at=attrs.get("created_at"),
        updated_at=attrs.get("updated_at"),
    )


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------


def _svc_to_resource(svc: Service | AsyncService) -> _GenServiceRequest:
    attrs = _GenService(name=svc.name)
    resource = _GenServiceResource(
        type_="service",
        attributes=attrs,
        id=svc.id,
    )
    return _GenServiceRequest(data=resource)


def _svc_from_parsed(parsed: Any, sync_client: ServicesClient | None, async_client: AsyncServicesClient | None) -> Any:
    """Build a Service / AsyncService from a parsed ServiceResponse."""
    data = parsed.data
    attrs = data.attributes
    if async_client is not None:
        return AsyncService(
            async_client,
            id=data.id,
            name=attrs.name,
            created_at=getattr(attrs, "created_at", None) or None,
            updated_at=getattr(attrs, "updated_at", None) or None,
        )
    return Service(
        sync_client,
        id=data.id,
        name=attrs.name,
        created_at=getattr(attrs, "created_at", None) or None,
        updated_at=getattr(attrs, "updated_at", None) or None,
    )


class ServicesClient:
    """Sync service CRUD (``mgmt.services``)."""

    def __init__(self, app_http: _AppAuthClient) -> None:
        self._app_http = app_http

    def new(
        self,
        id: str,
        *,
        name: str,
    ) -> Service:
        """Return an unsaved :class:`Service`. Call ``.save()`` to persist."""
        return Service(
            self,
            id=id,
            name=name,
        )

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[Service]:
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = _gen_list_services.sync_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_svc_resource_from_dict(item, sync_client=self) for item in body.get("data", [])]

    def get(self, id: str) -> Service:
        resp = _gen_get_service.sync_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"Service with id {id!r} not found", status_code=404)
        return _svc_from_parsed(resp.parsed, sync_client=self, async_client=None)

    def delete(self, id: str) -> None:
        resp = _gen_delete_service.sync_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)

    def _create(self, svc: Service) -> Service:
        body = _svc_to_resource(svc)
        resp = _gen_create_service.sync_detailed(client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _svc_from_parsed(resp.parsed, sync_client=self, async_client=None)

    def _update(self, svc: Service) -> Service:
        body = _svc_to_resource(svc)
        if svc.id is None:
            raise ValueError("cannot update a Service with no id")
        resp = _gen_update_service.sync_detailed(svc.id, client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _svc_from_parsed(resp.parsed, sync_client=self, async_client=None)


class AsyncServicesClient:
    """Async service CRUD (``mgmt.services``)."""

    def __init__(self, app_http: _AppAuthClient) -> None:
        self._app_http = app_http

    def new(
        self,
        id: str,
        *,
        name: str,
    ) -> AsyncService:
        return AsyncService(
            self,
            id=id,
            name=name,
        )

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncService]:
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = await _gen_list_services.asyncio_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_svc_resource_from_dict(item, async_client=self) for item in body.get("data", [])]

    async def get(self, id: str) -> AsyncService:
        resp = await _gen_get_service.asyncio_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"Service with id {id!r} not found", status_code=404)
        return _svc_from_parsed(resp.parsed, sync_client=None, async_client=self)

    async def delete(self, id: str) -> None:
        resp = await _gen_delete_service.asyncio_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)

    async def _create(self, svc: AsyncService) -> AsyncService:
        body = _svc_to_resource(svc)
        resp = await _gen_create_service.asyncio_detailed(client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _svc_from_parsed(resp.parsed, sync_client=None, async_client=self)

    async def _update(self, svc: AsyncService) -> AsyncService:
        body = _svc_to_resource(svc)
        if svc.id is None:
            raise ValueError("cannot update an AsyncService with no id")
        resp = await _gen_update_service.asyncio_detailed(svc.id, client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _svc_from_parsed(resp.parsed, sync_client=None, async_client=self)


def _svc_resource_from_dict(
    item: dict[str, Any],
    *,
    sync_client: ServicesClient | None = None,
    async_client: AsyncServicesClient | None = None,
) -> Any:
    """Build a Service from a raw JSON resource dict (used by list)."""
    attrs = item.get("attributes") or {}
    if async_client is not None:
        return AsyncService(
            async_client,
            id=item.get("id"),
            name=attrs.get("name", ""),
            created_at=attrs.get("created_at"),
            updated_at=attrs.get("updated_at"),
        )
    return Service(
        sync_client,
        id=item.get("id"),
        name=attrs.get("name", ""),
        created_at=attrs.get("created_at"),
        updated_at=attrs.get("updated_at"),
    )


# ---------------------------------------------------------------------------
# Context Types
# ---------------------------------------------------------------------------


class ContextTypesClient:
    """Sync context-type CRUD (``mgmt.context_types``)."""

    def __init__(self, app_http: _AppAuthClient) -> None:
        self._app_http = app_http

    def new(
        self,
        id: str,
        *,
        name: str | None = None,
        attributes: dict[str, dict[str, Any]] | None = None,
    ) -> ContextType:
        return ContextType(
            self,
            id=id,
            name=name or id,
            attributes=attributes or {},
        )

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[ContextType]:
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = _gen_list_context_types.sync_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_ct_resource_from_dict(item, sync_client=self) for item in body.get("data", [])]

    def get(self, id: str) -> ContextType:
        resp = _gen_get_context_type.sync_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"ContextType with id {id!r} not found", status_code=404)
        return _ct_from_parsed(resp.parsed, sync_client=self, async_client=None)

    def delete(self, id: str) -> None:
        resp = _gen_delete_context_type.sync_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)

    def _create(self, ct: ContextType) -> ContextType:
        body = _ct_to_resource(ct)
        resp = _gen_create_context_type.sync_detailed(client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _ct_from_parsed(resp.parsed, sync_client=self, async_client=None)

    def _update(self, ct: ContextType) -> ContextType:
        body = _ct_to_resource(ct)
        if ct.id is None:
            raise ValueError("cannot update a ContextType with no id")
        resp = _gen_update_context_type.sync_detailed(ct.id, client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _ct_from_parsed(resp.parsed, sync_client=self, async_client=None)


class AsyncContextTypesClient:
    def __init__(self, app_http: _AppAuthClient) -> None:
        self._app_http = app_http

    def new(
        self,
        id: str,
        *,
        name: str | None = None,
        attributes: dict[str, dict[str, Any]] | None = None,
    ) -> AsyncContextType:
        return AsyncContextType(
            self,
            id=id,
            name=name or id,
            attributes=attributes or {},
        )

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncContextType]:
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = await _gen_list_context_types.asyncio_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_ct_resource_from_dict(item, async_client=self) for item in body.get("data", [])]

    async def get(self, id: str) -> AsyncContextType:
        resp = await _gen_get_context_type.asyncio_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"ContextType with id {id!r} not found", status_code=404)
        return _ct_from_parsed(resp.parsed, sync_client=None, async_client=self)

    async def delete(self, id: str) -> None:
        resp = await _gen_delete_context_type.asyncio_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)

    async def _create(self, ct: AsyncContextType) -> AsyncContextType:
        body = _ct_to_resource(ct)
        resp = await _gen_create_context_type.asyncio_detailed(client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _ct_from_parsed(resp.parsed, sync_client=None, async_client=self)

    async def _update(self, ct: AsyncContextType) -> AsyncContextType:
        body = _ct_to_resource(ct)
        if ct.id is None:
            raise ValueError("cannot update an AsyncContextType with no id")
        resp = await _gen_update_context_type.asyncio_detailed(ct.id, client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _ct_from_parsed(resp.parsed, sync_client=None, async_client=self)


def _ct_resource_from_dict(
    item: dict[str, Any],
    *,
    sync_client: ContextTypesClient | None = None,
    async_client: AsyncContextTypesClient | None = None,
) -> Any:
    attrs = item.get("attributes") or {}
    raw_attr_meta = attrs.get("attributes")
    if isinstance(raw_attr_meta, dict):
        attribute_metadata: dict[str, dict[str, Any]] = {
            k: dict(v) if isinstance(v, dict) else {} for k, v in raw_attr_meta.items()
        }
    else:
        attribute_metadata = {}
    if async_client is not None:
        return AsyncContextType(
            async_client,
            id=item.get("id"),
            name=attrs.get("name", ""),
            attributes=attribute_metadata,
            created_at=attrs.get("created_at"),
            updated_at=attrs.get("updated_at"),
        )
    return ContextType(
        sync_client,
        id=item.get("id"),
        name=attrs.get("name", ""),
        attributes=attribute_metadata,
        created_at=attrs.get("created_at"),
        updated_at=attrs.get("updated_at"),
    )


# ---------------------------------------------------------------------------
# Contexts
# ---------------------------------------------------------------------------


def _build_logger_bulk_request(buffer: Any) -> Any:
    """Drain the logger-discovery buffer and build a JSON:API bulk request body.

    Returns ``None`` when there is nothing to flush.
    """
    from smplkit._generated.logging.models.logger_bulk_item import LoggerBulkItem
    from smplkit._generated.logging.models.logger_bulk_request import LoggerBulkRequest

    batch = buffer.drain()
    if not batch:
        return None
    items = [
        LoggerBulkItem(
            id=b["id"],
            level=b.get("level"),
            resolved_level=b["resolved_level"],
            service=b.get("service"),
            environment=b.get("environment"),
        )
        for b in batch
    ]
    return LoggerBulkRequest(loggers=items)


def _build_config_bulk_request(batch: list[dict[str, Any]]) -> _GenConfigBulkRequest | None:
    """Build a JSON:API bulk request body from a list of pending config entries.

    Returns ``None`` when *batch* is empty.  Each entry's ``items`` is a
    ``{item_key: {value, type, description?}}`` dict that the generated
    client expects as ``ConfigBulkItemItemsType0`` with the items as
    ``additional_properties``.
    """
    if not batch:
        return None
    configs: list[_GenConfigBulkItem] = []
    for entry in batch:
        items_field: Any = _CONFIG_UNSET
        if entry.get("items"):
            items_obj = _GenConfigBulkItemItems()
            for item_key, item_def in entry["items"].items():
                items_obj.additional_properties[item_key] = _GenConfigItemDefinition(
                    value=item_def["value"],
                    type_=item_def["type"],
                    description=item_def.get("description", _CONFIG_UNSET),
                )
            items_field = items_obj
        configs.append(
            _GenConfigBulkItem(
                id=entry["id"],
                name=entry.get("name", _CONFIG_UNSET),
                description=entry.get("description", _CONFIG_UNSET),
                parent=entry.get("parent", _CONFIG_UNSET),
                items=items_field,
                service=entry.get("service", _CONFIG_UNSET),
                environment=entry.get("environment", _CONFIG_UNSET),
            )
        )
    return _GenConfigBulkRequest(configs=configs)


def _build_flag_bulk_request(batch: list[dict[str, Any]]) -> _GenFlagBulkRequest | None:
    """Build a JSON:API bulk request body from a list of pending flag items.

    Returns ``None`` when *batch* is empty.  Items are not removed from any
    buffer here; callers must commit on a successful send.
    """
    if not batch:
        return None
    items = [
        _GenFlagBulkItem(
            id=b["id"],
            type_=b["type"],
            default=b["default"],
            service=b.get("service"),
            environment=b.get("environment"),
        )
        for b in batch
    ]
    return _GenFlagBulkRequest(flags=items)


def _build_bulk_register_body(items: list[dict[str, Any]]) -> _GenContextBulkRegister:
    bulk: list[_GenContextBulkItem] = []
    for item in items:
        attrs = _GenContextBulkItemAttributes()
        attrs.additional_properties = dict(item.get("attributes") or {})
        bulk.append(
            _GenContextBulkItem(
                type_=item["type"],
                key=item["key"],
                attributes=attrs,
            )
        )
    return _GenContextBulkRegister(contexts=bulk)


class ContextsClient:
    """Sync context registration + read/delete (``mgmt.contexts``)."""

    def __init__(
        self,
        app_http: _AppAuthClient,
        buffer: _ContextRegistrationBuffer,
    ) -> None:
        self._app_http = app_http
        self._buffer = buffer

    def register(self, items: Context | list[Context], *, flush: bool = False) -> None:
        """Buffer contexts for registration; optionally flush immediately."""
        batch = items if isinstance(items, list) else [items]
        self._buffer.observe(batch)
        if flush:
            self.flush()
            return
        if self._buffer.pending_count >= _CONTEXT_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush()
        except Exception as exc:
            logger.warning("Context registration flush failed: %s", exc)

    def flush(self) -> None:
        """Send any pending observations to the server."""
        batch = self._buffer.drain()
        if not batch:
            return
        body = _build_bulk_register_body(batch)
        resp = _gen_bulk_register_contexts.sync_detailed(client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)

    @property
    def pending_count(self) -> int:
        """Number of observations queued and awaiting flush."""
        return self._buffer.pending_count

    def list(
        self,
        type: str,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[Context]:
        """List all contexts of a given type."""
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = _gen_list_contexts.sync_detailed(
            client=self._app_http,
            filtercontext_type=type,
            **kwargs,
        )
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_ctx_entity_from_dict(item, client=self) for item in body.get("data", [])]

    @overload
    def get(self, id: str) -> Context: ...
    @overload
    def get(self, type: str, key: str) -> Context: ...
    def get(self, id_or_type: str, key: str | None = None) -> Context:
        ctx_type, ctx_key = _split_context_id(id_or_type, key)
        composite = f"{ctx_type}:{ctx_key}"
        resp = _gen_get_context.sync_detailed(composite, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(
                f"Context with id {composite!r} not found",
                status_code=404,
            )
        return _ctx_entity_from_parsed(resp.parsed, sync=True, client=self)

    @overload
    def delete(self, id: str) -> None: ...
    @overload
    def delete(self, type: str, key: str) -> None: ...
    def delete(self, id_or_type: str, key: str | None = None) -> None:
        ctx_type, ctx_key = _split_context_id(id_or_type, key)
        composite = f"{ctx_type}:{ctx_key}"
        resp = _gen_delete_context.sync_detailed(composite, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)

    def _save_context(self, ctx: Context) -> Context:
        body = _ctx_to_resource(ctx)
        resp = _gen_update_context.sync_detailed(ctx.id, client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _ctx_entity_from_parsed(resp.parsed, sync=True, client=self)  # type: ignore[return-value]


class AsyncContextsClient:
    def __init__(
        self,
        app_http: _AppAuthClient,
        buffer: _ContextRegistrationBuffer,
    ) -> None:
        self._app_http = app_http
        self._buffer = buffer

    def register(self, items: Context | list[Context]) -> None:
        """Buffer contexts for registration.  Call ``await flush()`` to send them."""
        batch = items if isinstance(items, list) else [items]
        self._buffer.observe(batch)
        if self._buffer.pending_count >= _CONTEXT_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush_sync()
        except Exception as exc:
            logger.warning("Context registration flush failed: %s", exc)

    async def flush(self) -> None:
        batch = self._buffer.drain()
        if not batch:
            return
        body = _build_bulk_register_body(batch)
        resp = await _gen_bulk_register_contexts.asyncio_detailed(client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)

    def flush_sync(self) -> None:
        """Synchronous flush — for use from non-event-loop threads (e.g. atexit handlers)."""
        batch = self._buffer.drain()
        if not batch:
            return
        body = _build_bulk_register_body(batch)
        resp = _gen_bulk_register_contexts.sync_detailed(client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)

    @property
    def pending_count(self) -> int:
        """Number of observations queued and awaiting flush."""
        return self._buffer.pending_count

    async def list(
        self,
        type: str,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncContext]:
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = await _gen_list_contexts.asyncio_detailed(
            client=self._app_http,
            filtercontext_type=type,
            **kwargs,
        )
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_ctx_entity_from_dict(item, async_=True, client=self) for item in body.get("data", [])]  # type: ignore[misc]

    @overload
    async def get(self, id: str) -> AsyncContext: ...
    @overload
    async def get(self, type: str, key: str) -> AsyncContext: ...
    async def get(self, id_or_type: str, key: str | None = None) -> AsyncContext:
        ctx_type, ctx_key = _split_context_id(id_or_type, key)
        composite = f"{ctx_type}:{ctx_key}"
        resp = await _gen_get_context.asyncio_detailed(composite, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(
                f"Context with id {composite!r} not found",
                status_code=404,
            )
        return _ctx_entity_from_parsed(resp.parsed, sync=False, client=self)  # type: ignore[return-value]

    @overload
    async def delete(self, id: str) -> None: ...
    @overload
    async def delete(self, type: str, key: str) -> None: ...
    async def delete(self, id_or_type: str, key: str | None = None) -> None:
        ctx_type, ctx_key = _split_context_id(id_or_type, key)
        composite = f"{ctx_type}:{ctx_key}"
        resp = await _gen_delete_context.asyncio_detailed(composite, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)

    async def _save_context(self, ctx: AsyncContext) -> AsyncContext:
        body = _ctx_to_resource(ctx)
        resp = await _gen_update_context.asyncio_detailed(ctx.id, client=self._app_http, body=body)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise ValidationError(
                f"HTTP {int(resp.status_code)}: unexpected response",
                status_code=int(resp.status_code),
            )
        return _ctx_entity_from_parsed(resp.parsed, sync=False, client=self)  # type: ignore[return-value]


def _ctx_entity_from_dict(item: dict[str, Any], *, async_: bool = False, client: Any = None) -> Context | AsyncContext:
    composite_id = item.get("id") or ""
    if ":" in composite_id:
        ctx_type, _, ctx_key = composite_id.partition(":")
    else:
        ctx_type, ctx_key = composite_id, ""
    attrs = item.get("attributes") or {}
    raw_attrs = attrs.get("attributes") or {}
    cls = AsyncContext if async_ else Context
    ctx = cls(
        ctx_type,
        ctx_key,
        dict(raw_attrs) if isinstance(raw_attrs, dict) else {},
        name=attrs.get("name") or None,
        created_at=attrs.get("created_at"),
        updated_at=attrs.get("updated_at"),
    )
    ctx._client = client
    return ctx


# ---------------------------------------------------------------------------
# Account Settings
# ---------------------------------------------------------------------------


class AccountSettingsClient:
    """Sync account-settings get/save (``mgmt.account_settings``).

    The endpoint isn't JSON:API — body is a raw JSON object — so we
    use httpx directly rather than going through a generated client.
    """

    def __init__(self, app_base_url: str, api_key: str) -> None:
        self._base_url = app_base_url
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def get(self) -> AccountSettings:
        with httpx.Client(base_url=self._base_url, headers=self._headers, timeout=30.0) as h:
            resp = h.get("/api/v1/accounts/current/settings")
        _check_status(resp.status_code, resp.content)
        return AccountSettings(self, data=resp.json() or {})

    def _save(self, data: dict[str, Any]) -> AccountSettings:
        with httpx.Client(base_url=self._base_url, headers=self._headers, timeout=30.0) as h:
            resp = h.put("/api/v1/accounts/current/settings", json=data)
        _check_status(resp.status_code, resp.content)
        return AccountSettings(self, data=resp.json() or {})


class AsyncAccountSettingsClient:
    def __init__(self, app_base_url: str, api_key: str) -> None:
        self._base_url = app_base_url
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def get(self) -> AsyncAccountSettings:
        async with httpx.AsyncClient(base_url=self._base_url, headers=self._headers, timeout=30.0) as h:
            resp = await h.get("/api/v1/accounts/current/settings")
        _check_status(resp.status_code, resp.content)
        return AsyncAccountSettings(self, data=resp.json() or {})

    async def _save(self, data: dict[str, Any]) -> AsyncAccountSettings:
        async with httpx.AsyncClient(base_url=self._base_url, headers=self._headers, timeout=30.0) as h:
            resp = await h.put("/api/v1/accounts/current/settings", json=data)
        _check_status(resp.status_code, resp.content)
        return AsyncAccountSettings(self, data=resp.json() or {})


# ---------------------------------------------------------------------------
# Configs
# ---------------------------------------------------------------------------


def _resolve_parent(parent: str | Config | AsyncConfig | None) -> str | None:
    """Normalize a ``parent`` argument to a config id string."""
    if parent is None or isinstance(parent, str):
        return parent
    if not parent.id:
        raise ValueError(
            "parent config must be saved (have an id) before being used as a parent",
        )
    return parent.id


class ConfigClient:
    """Sync config CRUD (``mgmt.config``).

    Also owns the config-discovery buffer that the runtime client
    populates when customer code calls ``client.config.bind`` to
    register a Pydantic-modeled configuration.
    """

    def __init__(self, http_client: _ConfigAuthClient) -> None:
        self._http_client = http_client
        self._buffer = _ConfigRegistrationBuffer()

    # ------------------------------------------------------------------
    # Discovery: declare + add_item + flush
    # ------------------------------------------------------------------

    def register_config(
        self,
        config_id: str,
        *,
        service: str | None,
        environment: str | None,
        parent: str | None = None,
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        """Queue a configuration declaration for bulk-discovery upload."""
        self._buffer.declare(
            config_id,
            service=service,
            environment=environment,
            parent=parent,
            name=name,
            description=description,
        )
        if self._buffer.pending_count >= _CONFIG_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def register_config_item(
        self,
        config_id: str,
        item_key: str,
        item_type: str,
        default: Any,
        description: str | None = None,
    ) -> None:
        """Queue a config item declaration. ``register_config`` must run first."""
        self._buffer.add_item(config_id, item_key, item_type, default, description)
        if self._buffer.pending_count >= _CONFIG_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush()
        except Exception as exc:
            logger.warning("Config registration flush failed: %s", exc)

    def flush(self) -> None:
        """POST pending declarations to ``/api/v1/configs/bulk``.

        Per ADR-024 §2.9, bulk registration always lands rows as
        ``managed=false`` and is plan-limit-exempt — failures here never
        propagate to customer code. Drained entries are not requeued;
        the SDK will re-observe on the next process start.
        """
        batch = self._buffer.drain()
        body = _build_config_bulk_request(batch)
        if body is None:
            return
        try:
            response = _gen_bulk_register_configs.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    @property
    def pending_count(self) -> int:
        """Number of pending config declarations awaiting flush."""
        return self._buffer.pending_count

    def new(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        parent: str | Config | None = None,
    ) -> Config:
        """Return a new unsaved :class:`Config`. Call :meth:`Config.save` to persist.

        ``parent`` accepts either a config id (string) or an existing
        :class:`Config` instance — passing the instance lets you skip naming
        the id explicitly when you already have the parent in scope.
        """
        return Config(
            self,
            id=id,
            name=name or key_to_display_name(id),
            description=description,
            parent=_resolve_parent(parent),
        )

    def get(self, id: str) -> Config:
        try:
            response = _gen_get_config.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            raise NotFoundError(f"Config with id '{id}' not found", status_code=404)
        return _resource_to_config(self, response.parsed.data)

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[Config]:
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = _gen_list_configs.sync_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_resource_to_config(self, r) for r in response.parsed.data]

    def delete(self, id: str) -> None:
        try:
            response = _gen_delete_config.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    def _create_config(self, config: Config) -> Config:
        body = _build_config_request_body(
            config_id=config.id,
            name=config.name,
            description=config.description,
            parent=config.parent,
            items=config._items_raw,
            environments=config.environments,
        )
        try:
            response = _gen_create_config.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _resource_to_config(self, response.parsed.data)

    def _update_config_from_model(self, config: Config) -> Config:
        body = _build_config_request_body(
            config_id=config.id,
            name=config.name,
            description=config.description,
            parent=config.parent,
            items=config._items_raw,
            environments=config.environments,
        )
        try:
            response = _gen_update_config.sync_detailed(config.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _resource_to_config(self, response.parsed.data)


class AsyncConfigClient:
    """Async config CRUD (``mgmt.config``).

    Also owns the config-discovery buffer that the runtime client
    populates when customer code calls ``client.config.bind`` to
    register a Pydantic-modeled configuration.
    """

    def __init__(self, http_client: _ConfigAuthClient) -> None:
        self._http_client = http_client
        self._buffer = _ConfigRegistrationBuffer()

    # ------------------------------------------------------------------
    # Discovery: declare + add_item + flush
    # ------------------------------------------------------------------

    def register_config(
        self,
        config_id: str,
        *,
        service: str | None,
        environment: str | None,
        parent: str | None = None,
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        """Queue a configuration declaration for bulk-discovery upload."""
        self._buffer.declare(
            config_id,
            service=service,
            environment=environment,
            parent=parent,
            name=name,
            description=description,
        )
        if self._buffer.pending_count >= _CONFIG_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush_sync, daemon=True).start()

    def register_config_item(
        self,
        config_id: str,
        item_key: str,
        item_type: str,
        default: Any,
        description: str | None = None,
    ) -> None:
        """Queue a config item declaration. ``register_config`` must run first."""
        self._buffer.add_item(config_id, item_key, item_type, default, description)
        if self._buffer.pending_count >= _CONFIG_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush_sync, daemon=True).start()

    def _threshold_flush_sync(self) -> None:
        try:
            self.flush_sync()
        except Exception as exc:
            logger.warning("Config registration flush failed: %s", exc)

    async def flush(self) -> None:
        """POST pending declarations to ``/api/v1/configs/bulk`` (async)."""
        batch = self._buffer.drain()
        body = _build_config_bulk_request(batch)
        if body is None:
            return
        try:
            response = await _gen_bulk_register_configs.asyncio_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    def flush_sync(self) -> None:
        """Synchronous flush from a background thread (final flush, threshold flush)."""
        batch = self._buffer.drain()
        body = _build_config_bulk_request(batch)
        if body is None:
            return
        try:
            response = _gen_bulk_register_configs.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    @property
    def pending_count(self) -> int:
        """Number of pending config declarations awaiting flush."""
        return self._buffer.pending_count

    def new(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        parent: str | AsyncConfig | None = None,
    ) -> AsyncConfig:
        """Return a new unsaved :class:`AsyncConfig`. Call ``await save()`` to persist.

        ``parent`` accepts either a config id (string) or an existing
        :class:`AsyncConfig` instance — passing the instance lets you skip
        naming the id explicitly when you already have the parent in scope.
        """
        return AsyncConfig(
            self,
            id=id,
            name=name or key_to_display_name(id),
            description=description,
            parent=_resolve_parent(parent),
        )

    async def get(self, id: str) -> AsyncConfig:
        try:
            response = await _gen_get_config.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            raise NotFoundError(f"Config with id '{id}' not found", status_code=404)
        return _resource_to_async_config(self, response.parsed.data)

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncConfig]:
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = await _gen_list_configs.asyncio_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_resource_to_async_config(self, r) for r in response.parsed.data]

    async def delete(self, id: str) -> None:
        try:
            response = await _gen_delete_config.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    async def _create_config(self, config: AsyncConfig) -> AsyncConfig:
        body = _build_config_request_body(
            config_id=config.id,
            name=config.name,
            description=config.description,
            parent=config.parent,
            items=config._items_raw,
            environments=config.environments,
        )
        try:
            response = await _gen_create_config.asyncio_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _resource_to_async_config(self, response.parsed.data)

    async def _update_config_from_model(self, config: AsyncConfig) -> AsyncConfig:
        body = _build_config_request_body(
            config_id=config.id,
            name=config.name,
            description=config.description,
            parent=config.parent,
            items=config._items_raw,
            environments=config.environments,
        )
        try:
            response = await _gen_update_config.asyncio_detailed(config.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _resource_to_async_config(self, response.parsed.data)


# ---------------------------------------------------------------------------
# Flags
# ---------------------------------------------------------------------------


class FlagsClient:
    """Sync flag CRUD (``mgmt.flags``).

    Distinct from the runtime :class:`smplkit.flags.client.FlagsClient` —
    this class exposes management operations.  It also owns the
    flag-discovery buffer that the runtime client populates when
    customer code declares typed flag handles.
    """

    def __init__(self, http_client: _FlagsAuthClient) -> None:
        self._http_client = http_client
        from smplkit.management._buffer import _FlagRegistrationBuffer

        self._buffer = _FlagRegistrationBuffer()

    def register(
        self,
        items: FlagDeclaration | list[FlagDeclaration],
        *,
        flush: bool = False,
    ) -> None:
        """Buffer flag declarations for registration; optionally flush immediately."""
        batch = items if isinstance(items, list) else [items]
        for d in batch:
            self._buffer.add(d.id, d.type, d.default, d.service, d.environment)
        if flush:
            self.flush()
            return
        if self._buffer.pending_count >= _FLAG_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush()
        except Exception as exc:
            logger.warning("Flag registration flush failed: %s", exc)

    def flush(self) -> None:
        """POST pending declarations to the bulk endpoint.

        Items remain in the buffer until the request succeeds, so a flush
        against an unhealthy ``flags`` service is automatically retried by
        the next ``flush()`` call (lazy ``start()`` retry, periodic
        background flush, or final flush on close).
        """
        batch = self._buffer.peek()
        body = _build_flag_bulk_request(batch)
        if body is None:
            return
        try:
            response = _gen_bulk_register_flags.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        self._buffer.commit([b["id"] for b in batch])

    @property
    def pending_count(self) -> int:
        """Number of declarations queued and awaiting flush."""
        return self._buffer.pending_count

    def new_boolean_flag(
        self,
        id: str,
        *,
        default: bool,
        name: str | None = None,
        description: str | None = None,
    ) -> BooleanFlag:
        return BooleanFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="BOOLEAN",
            default=default,
            values=[FlagValue(name="True", value=True), FlagValue(name="False", value=False)],
            description=description,
        )

    def new_string_flag(
        self,
        id: str,
        *,
        default: str,
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> StringFlag:
        return StringFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="STRING",
            default=default,
            values=values,
            description=description,
        )

    def new_number_flag(
        self,
        id: str,
        *,
        default: int | float,
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> NumberFlag:
        return NumberFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="NUMERIC",
            default=default,
            values=values,
            description=description,
        )

    def new_json_flag(
        self,
        id: str,
        *,
        default: dict[str, Any],
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> JsonFlag:
        return JsonFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="JSON",
            default=default,
            values=values,
            description=description,
        )

    def get(self, id: str) -> Flag:
        try:
            response = _gen_get_flag.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        body = json.loads(response.content)
        return self._model_from_json(body["data"])

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[Flag]:
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = _gen_list_flags.sync_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        body = json.loads(response.content)
        return [self._model_from_json(r) for r in body.get("data", [])]

    def delete(self, id: str) -> None:
        try:
            response = _gen_delete_flag.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    def _create_flag(self, flag: Flag) -> Flag:
        body = _build_flag_request_body(flag, flag_id=flag.id)
        try:
            response = _gen_create_flag.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        resp_body = json.loads(response.content)
        return self._model_from_json(resp_body["data"])

    def _update_flag(self, *, flag: Flag) -> Flag:
        body = _build_flag_request_body(flag, flag_id=flag.id)
        try:
            response = _gen_update_flag.sync_detailed(flag.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        resp_body = json.loads(response.content)
        return self._model_from_json(resp_body["data"])

    def _model_from_json(self, data: dict[str, Any]) -> Flag:
        d = _flag_dict_from_json(data)
        return Flag(self, **d)


class AsyncFlagsClient:
    """Async flag CRUD (``mgmt.flags``)."""

    def __init__(self, http_client: _FlagsAuthClient) -> None:
        self._http_client = http_client
        from smplkit.management._buffer import _FlagRegistrationBuffer

        self._buffer = _FlagRegistrationBuffer()

    def register(
        self,
        items: FlagDeclaration | list[FlagDeclaration],
    ) -> None:
        """Buffer flag declarations for registration.  Call ``await flush()`` to send."""
        batch = items if isinstance(items, list) else [items]
        for d in batch:
            self._buffer.add(d.id, d.type, d.default, d.service, d.environment)
        if self._buffer.pending_count >= _FLAG_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush_sync()
        except Exception as exc:
            logger.warning("Flag registration flush failed: %s", exc)

    async def flush(self) -> None:
        """POST pending declarations to the bulk endpoint.

        Items remain in the buffer until the request succeeds; failed
        flushes are retried by the next ``flush()`` call.
        """
        batch = self._buffer.peek()
        body = _build_flag_bulk_request(batch)
        if body is None:
            return
        try:
            response = await _gen_bulk_register_flags.asyncio_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        self._buffer.commit([b["id"] for b in batch])

    def flush_sync(self) -> None:
        """Synchronous flush — for use from non-event-loop threads."""
        batch = self._buffer.peek()
        body = _build_flag_bulk_request(batch)
        if body is None:
            return
        try:
            response = _gen_bulk_register_flags.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        self._buffer.commit([b["id"] for b in batch])

    @property
    def pending_count(self) -> int:
        """Number of declarations queued and awaiting flush."""
        return self._buffer.pending_count

    def new_boolean_flag(
        self,
        id: str,
        *,
        default: bool,
        name: str | None = None,
        description: str | None = None,
    ) -> AsyncBooleanFlag:
        return AsyncBooleanFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="BOOLEAN",
            default=default,
            values=[FlagValue(name="True", value=True), FlagValue(name="False", value=False)],
            description=description,
        )

    def new_string_flag(
        self,
        id: str,
        *,
        default: str,
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> AsyncStringFlag:
        return AsyncStringFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="STRING",
            default=default,
            values=values,
            description=description,
        )

    def new_number_flag(
        self,
        id: str,
        *,
        default: int | float,
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> AsyncNumberFlag:
        return AsyncNumberFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="NUMERIC",
            default=default,
            values=values,
            description=description,
        )

    def new_json_flag(
        self,
        id: str,
        *,
        default: dict[str, Any],
        name: str | None = None,
        description: str | None = None,
        values: list[FlagValue] | None = None,
    ) -> AsyncJsonFlag:
        return AsyncJsonFlag(
            self,
            id=id,
            name=name or key_to_display_name(id),
            type="JSON",
            default=default,
            values=values,
            description=description,
        )

    async def get(self, id: str) -> AsyncFlag:
        try:
            response = await _gen_get_flag.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        body = json.loads(response.content)
        return self._model_from_json(body["data"])

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncFlag]:
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = await _gen_list_flags.asyncio_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        body = json.loads(response.content)
        return [self._model_from_json(r) for r in body.get("data", [])]

    async def delete(self, id: str) -> None:
        try:
            response = await _gen_delete_flag.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    async def _create_flag(self, flag: AsyncFlag) -> AsyncFlag:
        body = _build_flag_request_body(flag, flag_id=flag.id)
        try:
            response = await _gen_create_flag.asyncio_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        resp_body = json.loads(response.content)
        return self._model_from_json(resp_body["data"])

    async def _update_flag(self, *, flag: AsyncFlag) -> AsyncFlag:
        body = _build_flag_request_body(flag, flag_id=flag.id)
        try:
            response = await _gen_update_flag.asyncio_detailed(flag.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._http_client._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        resp_body = json.loads(response.content)
        return self._model_from_json(resp_body["data"])

    def _model_from_json(self, data: dict[str, Any]) -> AsyncFlag:
        d = _flag_dict_from_json(data)
        return AsyncFlag(self, **d)


# ---------------------------------------------------------------------------
# Loggers
# ---------------------------------------------------------------------------


class LoggersClient:
    """Sync logger CRUD (``mgmt.loggers``)."""

    def __init__(self, http_client: _LoggingAuthClient, *, base_url: str) -> None:
        self._http_client = http_client
        self._base_url = base_url
        from smplkit.management._buffer import _LoggerRegistrationBuffer

        self._buffer = _LoggerRegistrationBuffer()

    def register(
        self,
        items: LoggerSource | list[LoggerSource],
        *,
        flush: bool = False,
    ) -> None:
        """Buffer logger sources for registration; optionally flush immediately."""
        batch = items if isinstance(items, list) else [items]
        for src in batch:
            self._buffer.add(
                normalize_logger_name(src.name),
                _loglevel_value(src.level, where="register[level]"),
                _loglevel_value(src.resolved_level, where="register[resolved_level]"),
                src.service,
                src.environment,
            )
        if flush:
            self.flush()
            return
        if self._buffer.pending_count >= _LOGGER_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush()
        except Exception as exc:
            logger.warning("Logger registration flush failed: %s", exc)

    def flush(self) -> None:
        """Drain the buffer and POST pending logger sources to the bulk endpoint."""
        body = _build_logger_bulk_request(self._buffer)
        if body is None:
            return
        try:
            response = _gen_bulk_register_loggers.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    @property
    def pending_count(self) -> int:
        """Number of sources queued and awaiting flush."""
        return self._buffer.pending_count

    def new(self, id: str, *, managed: bool = True) -> SmplLogger:
        return SmplLogger(
            self,
            id=id,
            name=id,
            managed=managed,
        )

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[SmplLogger]:
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = _gen_list_loggers.sync_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_logger_resource_to_model(self, r) for r in response.parsed.data]

    def get(self, id: str) -> SmplLogger:
        try:
            response = _gen_get_logger.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise NotFoundError(f"Logger with id {id!r} not found", status_code=404)
        return _logger_resource_to_model(self, response.parsed.data)

    def delete(self, id: str) -> None:
        try:
            response = _gen_delete_logger.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    def _save_logger(self, lg: SmplLogger) -> SmplLogger:
        body = _build_logger_body(
            logger_id=lg.id,
            name=lg.name,
            level=_loglevel_value(lg.level, where="SmplLogger.save"),
            managed=lg.managed,
            group=lg.group,
            environments=_logger_environments_to_wire(lg._environments) if lg._environments else None,
        )
        try:
            response = _gen_update_logger.sync_detailed(lg.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _logger_resource_to_model(self, response.parsed.data)


class AsyncLoggersClient:
    """Async logger CRUD (``mgmt.loggers``)."""

    def __init__(self, http_client: _LoggingAuthClient, *, base_url: str) -> None:
        self._http_client = http_client
        self._base_url = base_url
        from smplkit.management._buffer import _LoggerRegistrationBuffer

        self._buffer = _LoggerRegistrationBuffer()

    def register(
        self,
        items: LoggerSource | list[LoggerSource],
    ) -> None:
        """Buffer logger sources for registration.  Call ``await flush()`` to send them."""
        batch = items if isinstance(items, list) else [items]
        for src in batch:
            self._buffer.add(
                normalize_logger_name(src.name),
                _loglevel_value(src.level, where="register[level]"),
                _loglevel_value(src.resolved_level, where="register[resolved_level]"),
                src.service,
                src.environment,
            )
        if self._buffer.pending_count >= _LOGGER_BATCH_FLUSH_SIZE:
            threading.Thread(target=self._threshold_flush, daemon=True).start()

    def _threshold_flush(self) -> None:
        try:
            self.flush_sync()
        except Exception as exc:
            logger.warning("Logger registration flush failed: %s", exc)

    async def flush(self) -> None:
        """Drain the buffer and POST pending logger sources to the bulk endpoint."""
        body = _build_logger_bulk_request(self._buffer)
        if body is None:
            return
        try:
            response = await _gen_bulk_register_loggers.asyncio_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    def flush_sync(self) -> None:
        """Synchronous flush — for use from non-event-loop threads."""
        body = _build_logger_bulk_request(self._buffer)
        if body is None:
            return
        try:
            response = _gen_bulk_register_loggers.sync_detailed(client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    @property
    def pending_count(self) -> int:
        """Number of sources queued and awaiting flush."""
        return self._buffer.pending_count

    def new(self, id: str, *, managed: bool = True) -> AsyncSmplLogger:
        return AsyncSmplLogger(
            self,
            id=id,
            name=id,
            managed=managed,
        )

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncSmplLogger]:
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = await _gen_list_loggers.asyncio_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_logger_resource_to_async_model(self, r) for r in response.parsed.data]

    async def get(self, id: str) -> AsyncSmplLogger:
        try:
            response = await _gen_get_logger.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise NotFoundError(f"Logger with id {id!r} not found", status_code=404)
        return _logger_resource_to_async_model(self, response.parsed.data)

    async def delete(self, id: str) -> None:
        try:
            response = await _gen_delete_logger.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    async def _save_logger(self, lg: AsyncSmplLogger) -> AsyncSmplLogger:
        body = _build_logger_body(
            logger_id=lg.id,
            name=lg.name,
            level=_loglevel_value(lg.level, where="AsyncSmplLogger.save"),
            managed=lg.managed,
            group=lg.group,
            environments=_logger_environments_to_wire(lg._environments) if lg._environments else None,
        )
        try:
            response = await _gen_update_logger.asyncio_detailed(lg.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _logger_resource_to_async_model(self, response.parsed.data)


# ---------------------------------------------------------------------------
# Log Groups
# ---------------------------------------------------------------------------


class LogGroupsClient:
    """Sync log-group CRUD (``mgmt.log_groups``)."""

    def __init__(self, http_client: _LoggingAuthClient, *, base_url: str) -> None:
        self._http_client = http_client
        self._base_url = base_url

    def new(self, id: str, *, name: str | None = None, group: str | None = None) -> SmplLogGroup:
        return SmplLogGroup(
            self,
            id=id,
            name=name if name is not None else key_to_display_name(id),
            group=group,
        )

    def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[SmplLogGroup]:
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = _gen_list_log_groups.sync_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_log_group_resource_to_model(self, r) for r in response.parsed.data]

    def get(self, id: str) -> SmplLogGroup:
        try:
            response = _gen_get_log_group.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise NotFoundError(f"Log group with id {id!r} not found", status_code=404)
        return _log_group_resource_to_model(self, response.parsed.data)

    def delete(self, id: str) -> None:
        try:
            response = _gen_delete_log_group.sync_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    def _save_group(self, grp: SmplLogGroup) -> SmplLogGroup:
        body = _build_log_group_body(
            group_id=grp.id,
            name=grp.name,
            level=_loglevel_value(grp.level, where="SmplLogGroup.save"),
            group=grp.group,
            environments=_logger_environments_to_wire(grp._environments) if grp._environments else None,
        )
        try:
            if grp.created_at is None:
                response = _gen_create_log_group.sync_detailed(client=self._http_client, body=body)
            else:
                response = _gen_update_log_group.sync_detailed(grp.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _log_group_resource_to_model(self, response.parsed.data)


class AsyncLogGroupsClient:
    """Async log-group CRUD (``mgmt.log_groups``)."""

    def __init__(self, http_client: _LoggingAuthClient, *, base_url: str) -> None:
        self._http_client = http_client
        self._base_url = base_url

    def new(self, id: str, *, name: str | None = None, group: str | None = None) -> AsyncSmplLogGroup:
        return AsyncSmplLogGroup(
            self,
            id=id,
            name=name if name is not None else key_to_display_name(id),
            group=group,
        )

    async def list(
        self,
        *,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> list[AsyncSmplLogGroup]:
        kwargs = _pagination_kwargs(page_number, page_size)
        try:
            response = await _gen_list_log_groups.asyncio_detailed(client=self._http_client, **kwargs)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None or not hasattr(response.parsed, "data"):
            return []
        return [_log_group_resource_to_async_model(self, r) for r in response.parsed.data]

    async def get(self, id: str) -> AsyncSmplLogGroup:
        try:
            response = await _gen_get_log_group.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise NotFoundError(f"Log group with id {id!r} not found", status_code=404)
        return _log_group_resource_to_async_model(self, response.parsed.data)

    async def delete(self, id: str) -> None:
        try:
            response = await _gen_delete_log_group.asyncio_detailed(id, client=self._http_client)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)

    async def _save_group(self, grp: AsyncSmplLogGroup) -> AsyncSmplLogGroup:
        body = _build_log_group_body(
            group_id=grp.id,
            name=grp.name,
            level=_loglevel_value(grp.level, where="AsyncSmplLogGroup.save"),
            group=grp.group,
            environments=_logger_environments_to_wire(grp._environments) if grp._environments else None,
        )
        try:
            if grp.created_at is None:
                response = await _gen_create_log_group.asyncio_detailed(client=self._http_client, body=body)
            else:
                response = await _gen_update_log_group.asyncio_detailed(grp.id, client=self._http_client, body=body)
        except Exception as exc:
            _maybe_reraise_network_error(exc, self._base_url)
            raise
        _check_status(int(response.status_code), response.content)
        if response.parsed is None:
            raise ValidationError(
                f"HTTP {int(response.status_code)}: unexpected response", status_code=int(response.status_code)
            )
        return _log_group_resource_to_async_model(self, response.parsed.data)


# ---------------------------------------------------------------------------
# Top-level SmplManagementClient
# ---------------------------------------------------------------------------


class SmplManagementClient:
    """Synchronous management-only entry point for the smplkit SDK.

    Use this client for setup scripts, CI/CD jobs, admin tools, and
    anywhere else the goal is CRUD against the platform — not runtime
    instrumentation. Construction has zero side effects: no service
    registration, no metrics thread, no websocket, no logger discovery.

    Usage::

        from smplkit import SmplManagementClient

        with SmplManagementClient() as mgmt:
            for env in mgmt.environments.list():
                print(env.id)

    Args:
        api_key: API key for authenticating with the smplkit platform.
            When omitted, resolved from ``SMPLKIT_API_KEY`` or ``~/.smplkit``.
        profile: Named profile section to read from ``~/.smplkit``.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable debug logging in the SDK.
    """

    contexts: ContextsClient
    context_types: ContextTypesClient
    environments: EnvironmentsClient
    services: ServicesClient
    account_settings: AccountSettingsClient
    config: ConfigClient
    flags: FlagsClient
    loggers: LoggersClient
    log_groups: LogGroupsClient
    audit: "_MgmtAuditClient"

    def __init__(
        self,
        api_key: str | None = None,
        *,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
    ) -> None:
        cfg = resolve_management_config(
            profile=profile,
            api_key=api_key,
            base_domain=base_domain,
            scheme=scheme,
            debug=debug,
        )
        self._init_from_resolved(cfg)

    @classmethod
    def _from_resolved(cls, cfg: "ResolvedManagementConfig") -> "SmplManagementClient":
        """Construct from an already-resolved config (used by ``SmplClient``)."""
        instance = cls.__new__(cls)
        instance._init_from_resolved(cfg)
        return instance

    def _init_from_resolved(self, cfg: "ResolvedManagementConfig") -> None:
        if cfg.debug:
            enable_debug()
            logger.setLevel(logging.DEBUG)

        self._api_key = cfg.api_key
        self._base_domain = cfg.base_domain
        self._scheme = cfg.scheme

        config_url = _service_url(cfg.scheme, "config", cfg.base_domain)
        app_url = _service_url(cfg.scheme, "app", cfg.base_domain)
        flags_url = _service_url(cfg.scheme, "flags", cfg.base_domain)
        logging_url = _service_url(cfg.scheme, "logging", cfg.base_domain)
        audit_url = _service_url(cfg.scheme, "audit", cfg.base_domain)

        _extra = {**(cfg.extra_headers or {})}
        self._app_http = _AppAuthClient(base_url=app_url, token=cfg.api_key, headers=_extra)
        self._config_http = _ConfigAuthClient(base_url=config_url, token=cfg.api_key, headers=_extra)
        self._flags_http = _FlagsAuthClient(base_url=flags_url, token=cfg.api_key, headers=_extra)
        self._logging_http = _LoggingAuthClient(base_url=logging_url, token=cfg.api_key, headers=_extra)
        # Audit's wire format is JSON:API; all other services pass through
        # ``application/json`` because their generated clients send it. The
        # Accept header here mirrors the runtime audit client.
        self._audit_http = _AuditAuthClient(
            base_url=audit_url,
            token=cfg.api_key,
            headers={**_extra, "Accept": "application/vnd.api+json"},
        )

        from smplkit.management._buffer import _ContextRegistrationBuffer

        self._context_buffer = _ContextRegistrationBuffer()

        self.contexts = ContextsClient(self._app_http, self._context_buffer)
        self.context_types = ContextTypesClient(self._app_http)
        self.environments = EnvironmentsClient(self._app_http)
        self.services = ServicesClient(self._app_http)
        self.account_settings = AccountSettingsClient(app_url, cfg.api_key)
        self.config = ConfigClient(self._config_http)
        self.flags = FlagsClient(self._flags_http)
        self.loggers = LoggersClient(self._logging_http, base_url=logging_url)
        self.log_groups = LogGroupsClient(self._logging_http, base_url=logging_url)
        # Lazily imported to avoid a circular reference while management
        # types are still loading the runtime audit module for shared
        # dataclasses.
        from smplkit.management.audit import AuditClient as _MgmtAuditClient

        self.audit = _MgmtAuditClient(auth_client=self._audit_http)

    def close(self) -> None:
        """Release HTTP resources held by this client."""
        for http in (
            self._app_http,
            self._config_http,
            self._flags_http,
            self._logging_http,
            self._audit_http,
        ):
            client = http._client
            if client is not None:
                client.close()
                http._client = None

    def __enter__(self) -> SmplManagementClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncSmplManagementClient:
    """Asynchronous management-only entry point for the smplkit SDK.

    Mirrors :class:`SmplManagementClient` but exposes async sub-clients.
    Construction has the same zero-side-effect contract.
    """

    contexts: AsyncContextsClient
    context_types: AsyncContextTypesClient
    environments: AsyncEnvironmentsClient
    services: AsyncServicesClient
    account_settings: AsyncAccountSettingsClient
    config: AsyncConfigClient
    flags: AsyncFlagsClient
    loggers: AsyncLoggersClient
    log_groups: AsyncLogGroupsClient
    audit: "_MgmtAsyncAuditClient"

    def __init__(
        self,
        api_key: str | None = None,
        *,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
    ) -> None:
        cfg = resolve_management_config(
            profile=profile,
            api_key=api_key,
            base_domain=base_domain,
            scheme=scheme,
            debug=debug,
        )
        self._init_from_resolved(cfg)

    @classmethod
    def _from_resolved(cls, cfg: "ResolvedManagementConfig") -> "AsyncSmplManagementClient":
        """Construct from an already-resolved config (used by ``AsyncSmplClient``)."""
        instance = cls.__new__(cls)
        instance._init_from_resolved(cfg)
        return instance

    def _init_from_resolved(self, cfg: "ResolvedManagementConfig") -> None:
        if cfg.debug:
            enable_debug()
            logger.setLevel(logging.DEBUG)

        self._api_key = cfg.api_key
        self._base_domain = cfg.base_domain
        self._scheme = cfg.scheme

        config_url = _service_url(cfg.scheme, "config", cfg.base_domain)
        app_url = _service_url(cfg.scheme, "app", cfg.base_domain)
        flags_url = _service_url(cfg.scheme, "flags", cfg.base_domain)
        logging_url = _service_url(cfg.scheme, "logging", cfg.base_domain)
        audit_url = _service_url(cfg.scheme, "audit", cfg.base_domain)

        _extra = {**(cfg.extra_headers or {})}
        self._app_http = _AppAuthClient(base_url=app_url, token=cfg.api_key, headers=_extra)
        self._config_http = _ConfigAuthClient(base_url=config_url, token=cfg.api_key, headers=_extra)
        self._flags_http = _FlagsAuthClient(base_url=flags_url, token=cfg.api_key, headers=_extra)
        self._logging_http = _LoggingAuthClient(base_url=logging_url, token=cfg.api_key, headers=_extra)
        self._audit_http = _AuditAuthClient(
            base_url=audit_url,
            token=cfg.api_key,
            headers={**_extra, "Accept": "application/vnd.api+json"},
        )

        from smplkit.management._buffer import _ContextRegistrationBuffer

        self._context_buffer = _ContextRegistrationBuffer()

        self.contexts = AsyncContextsClient(self._app_http, self._context_buffer)
        self.context_types = AsyncContextTypesClient(self._app_http)
        self.environments = AsyncEnvironmentsClient(self._app_http)
        self.services = AsyncServicesClient(self._app_http)
        self.account_settings = AsyncAccountSettingsClient(app_url, cfg.api_key)
        self.config = AsyncConfigClient(self._config_http)
        self.flags = AsyncFlagsClient(self._flags_http)
        self.loggers = AsyncLoggersClient(self._logging_http, base_url=logging_url)
        self.log_groups = AsyncLogGroupsClient(self._logging_http, base_url=logging_url)
        from smplkit.management.audit import AsyncAuditClient as _MgmtAsyncAuditClient

        self.audit = _MgmtAsyncAuditClient(auth_client=self._audit_http)

    async def close(self) -> None:
        """Release HTTP resources held by this client."""
        for http in (
            self._app_http,
            self._config_http,
            self._flags_http,
            self._logging_http,
            self._audit_http,
        ):
            ac = http._async_client
            if ac is not None:
                await ac.aclose()
                http._async_client = None

    async def __aenter__(self) -> AsyncSmplManagementClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
