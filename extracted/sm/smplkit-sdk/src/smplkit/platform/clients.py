"""The Smpl Platform client — cross-cutting CRUD on ``client.platform``.

``PlatformClient`` / ``AsyncPlatformClient`` group the account-wide
configuration resources that aren't owned by a single product, mirroring the
product UI's Platform area:

- ``platform.environments`` — environment CRUD
- ``platform.services`` — service CRUD
- ``platform.contexts`` — evaluation-context registration + read/delete
- ``platform.context_types`` — context-type CRUD

All four are pure CRUD — no ``install()`` gate. Every sub-client speaks to the
app service, so the client needs exactly one app transport (plus the
context-registration buffer that ``contexts`` drains).

The client supports two construction shapes:

* **Wired** into :class:`smplkit.SmplClient` — borrows the parent's app
  transport and an externally-supplied context buffer. This is the common
  path; ``client.flags`` borrows ``client.platform.contexts`` as its
  evaluation-context registration seam.
* **Standalone** — ``PlatformClient(api_key=..., base_url=..., ...)`` builds
  and owns its own app transport and buffer. ``close()`` / ``aclose()`` tears
  down only the owned transport.
"""

from __future__ import annotations

import json
import logging
import threading
from typing import Any, overload

from smplkit._config import _service_url, resolve_client_config
from smplkit.errors import (
    NotFoundError,
    ValidationError,
    _raise_for_status,
)
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
from smplkit.flags.types import AsyncContext, Context
from smplkit._buffer import _CONTEXT_BATCH_FLUSH_SIZE, _ContextRegistrationBuffer
from smplkit.platform.models import (
    AsyncContextType,
    AsyncEnvironment,
    AsyncService,
    ContextType,
    Environment,
    Service,
)
from smplkit.platform.types import Color, EnvironmentClassification

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


def _platform_transport(
    *,
    api_key: str | None,
    base_url: str | None,
    profile: str | None,
    base_domain: str | None,
    scheme: str | None,
    debug: bool | None,
    extra_headers: dict[str, str] | None,
) -> _AppAuthClient:
    """Build a standalone app transport from resolved config.

    ``base_url``/``api_key`` are used directly when both are supplied (the
    path the top-level client takes after it has already resolved them);
    otherwise the config resolver fills in whatever is missing
    (``~/.smplkit`` / env vars / defaults).
    """
    cfg = resolve_client_config(
        profile=profile,
        api_key=api_key,
        base_domain=base_domain,
        scheme=scheme,
        debug=debug,
    )
    resolved_key = api_key if api_key is not None else cfg.api_key
    app_url = base_url if base_url is not None else _service_url(cfg.scheme, "app", cfg.base_domain)
    headers: dict[str, str] = {}
    headers.update(cfg.extra_headers or {})
    headers.update(extra_headers or {})
    return _AppAuthClient(base_url=app_url.rstrip("/"), token=resolved_key, headers=headers)


# ---------------------------------------------------------------------------
# Environments
# ---------------------------------------------------------------------------


class EnvironmentsClient:
    """Sync environment CRUD (``client.platform.environments``)."""

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
        """Build an unsaved :class:`Environment`; call ``.save()`` to persist it.

        Args:
            id: Stable, human-readable identifier for the environment
                (for example ``"production"``).
            name: Display name shown in the Console.
            color: Accent color for the environment, as a :class:`Color` or a
                CSS hex string. Defaults to no color.
            classification: Whether the environment participates in the
                standard environment ordering. Defaults to
                ``EnvironmentClassification.STANDARD``.

        Returns:
            An unsaved :class:`Environment` bound to this client.
        """
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
        """List environments in the account.

        Args:
            page_number: 1-based page to fetch. Defaults to the first page.
            page_size: Maximum number of environments per page. Defaults to
                the server's page size.

        Returns:
            The environments on the requested page.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = _gen_list_environments.sync_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_env_resource_from_dict(item, sync_client=self) for item in body.get("data", [])]

    def get(self, id: str) -> Environment:
        """Fetch a single environment by id.

        Args:
            id: Identifier of the environment to fetch.

        Returns:
            The matching :class:`Environment`.

        Raises:
            NotFoundError: If no environment with that id exists.
        """
        resp = _gen_get_environment.sync_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"Environment with id {id!r} not found", status_code=404)
        return _env_from_parsed(resp.parsed, sync_client=self, async_client=None)

    def delete(self, id: str) -> None:
        """Delete an environment by id.

        Args:
            id: Identifier of the environment to delete.
        """
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
    """Async environment CRUD (``client.platform.environments``)."""

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
        """Build an unsaved :class:`AsyncEnvironment`; ``await .save()`` to persist it.

        Args:
            id: Stable, human-readable identifier for the environment
                (for example ``"production"``).
            name: Display name shown in the Console.
            color: Accent color for the environment, as a :class:`Color` or a
                CSS hex string. Defaults to no color.
            classification: Whether the environment participates in the
                standard environment ordering. Defaults to
                ``EnvironmentClassification.STANDARD``.

        Returns:
            An unsaved :class:`AsyncEnvironment` bound to this client.
        """
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
        """List environments in the account. Awaits the round-trip.

        Args:
            page_number: 1-based page to fetch. Defaults to the first page.
            page_size: Maximum number of environments per page. Defaults to
                the server's page size.

        Returns:
            The environments on the requested page.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = await _gen_list_environments.asyncio_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_env_resource_from_dict(item, async_client=self) for item in body.get("data", [])]

    async def get(self, id: str) -> AsyncEnvironment:
        """Fetch a single environment by id. Awaits the round-trip.

        Args:
            id: Identifier of the environment to fetch.

        Returns:
            The matching :class:`AsyncEnvironment`.

        Raises:
            NotFoundError: If no environment with that id exists.
        """
        resp = await _gen_get_environment.asyncio_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"Environment with id {id!r} not found", status_code=404)
        return _env_from_parsed(resp.parsed, sync_client=None, async_client=self)

    async def delete(self, id: str) -> None:
        """Delete an environment by id. Awaits the round-trip.

        Args:
            id: Identifier of the environment to delete.
        """
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
    """Sync service CRUD (``client.platform.services``)."""

    def __init__(self, app_http: _AppAuthClient) -> None:
        self._app_http = app_http

    def new(
        self,
        id: str,
        *,
        name: str,
    ) -> Service:
        """Build an unsaved :class:`Service`; call ``.save()`` to persist it.

        Args:
            id: Stable, human-readable identifier for the service.
            name: Display name shown in the Console.

        Returns:
            An unsaved :class:`Service` bound to this client.
        """
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
        """List services in the account.

        Args:
            page_number: 1-based page to fetch. Defaults to the first page.
            page_size: Maximum number of services per page. Defaults to the
                server's page size.

        Returns:
            The services on the requested page.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = _gen_list_services.sync_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_svc_resource_from_dict(item, sync_client=self) for item in body.get("data", [])]

    def get(self, id: str) -> Service:
        """Fetch a single service by id.

        Args:
            id: Identifier of the service to fetch.

        Returns:
            The matching :class:`Service`.

        Raises:
            NotFoundError: If no service with that id exists.
        """
        resp = _gen_get_service.sync_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"Service with id {id!r} not found", status_code=404)
        return _svc_from_parsed(resp.parsed, sync_client=self, async_client=None)

    def delete(self, id: str) -> None:
        """Delete a service by id.

        Args:
            id: Identifier of the service to delete.
        """
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
    """Async service CRUD (``client.platform.services``)."""

    def __init__(self, app_http: _AppAuthClient) -> None:
        self._app_http = app_http

    def new(
        self,
        id: str,
        *,
        name: str,
    ) -> AsyncService:
        """Build an unsaved :class:`AsyncService`; ``await .save()`` to persist it.

        Args:
            id: Stable, human-readable identifier for the service.
            name: Display name shown in the Console.

        Returns:
            An unsaved :class:`AsyncService` bound to this client.
        """
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
        """List services in the account. Awaits the round-trip.

        Args:
            page_number: 1-based page to fetch. Defaults to the first page.
            page_size: Maximum number of services per page. Defaults to the
                server's page size.

        Returns:
            The services on the requested page.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = await _gen_list_services.asyncio_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_svc_resource_from_dict(item, async_client=self) for item in body.get("data", [])]

    async def get(self, id: str) -> AsyncService:
        """Fetch a single service by id. Awaits the round-trip.

        Args:
            id: Identifier of the service to fetch.

        Returns:
            The matching :class:`AsyncService`.

        Raises:
            NotFoundError: If no service with that id exists.
        """
        resp = await _gen_get_service.asyncio_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"Service with id {id!r} not found", status_code=404)
        return _svc_from_parsed(resp.parsed, sync_client=None, async_client=self)

    async def delete(self, id: str) -> None:
        """Delete a service by id. Awaits the round-trip.

        Args:
            id: Identifier of the service to delete.
        """
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
    """Sync context-type CRUD (``client.platform.context_types``)."""

    def __init__(self, app_http: _AppAuthClient) -> None:
        self._app_http = app_http

    def new(
        self,
        id: str,
        *,
        name: str | None = None,
        attributes: dict[str, dict[str, Any]] | None = None,
    ) -> ContextType:
        """Build an unsaved :class:`ContextType`; call ``.save()`` to persist it.

        Args:
            id: Stable, human-readable identifier for the context type
                (for example ``"user"``).
            name: Display name shown in the Console. Defaults to ``id`` when
                omitted.
            attributes: Known-attribute slots, keyed by attribute name, with a
                metadata dict per slot. Defaults to no declared attributes.

        Returns:
            An unsaved :class:`ContextType` bound to this client.
        """
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
        """List context types in the account.

        Args:
            page_number: 1-based page to fetch. Defaults to the first page.
            page_size: Maximum number of context types per page. Defaults to
                the server's page size.

        Returns:
            The context types on the requested page.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = _gen_list_context_types.sync_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_ct_resource_from_dict(item, sync_client=self) for item in body.get("data", [])]

    def get(self, id: str) -> ContextType:
        """Fetch a single context type by id.

        Args:
            id: Identifier of the context type to fetch.

        Returns:
            The matching :class:`ContextType`.

        Raises:
            NotFoundError: If no context type with that id exists.
        """
        resp = _gen_get_context_type.sync_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"ContextType with id {id!r} not found", status_code=404)
        return _ct_from_parsed(resp.parsed, sync_client=self, async_client=None)

    def delete(self, id: str) -> None:
        """Delete a context type by id.

        Args:
            id: Identifier of the context type to delete.
        """
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
        """Build an unsaved :class:`AsyncContextType`; ``await .save()`` to persist it.

        Args:
            id: Stable, human-readable identifier for the context type
                (for example ``"user"``).
            name: Display name shown in the Console. Defaults to ``id`` when
                omitted.
            attributes: Known-attribute slots, keyed by attribute name, with a
                metadata dict per slot. Defaults to no declared attributes.

        Returns:
            An unsaved :class:`AsyncContextType` bound to this client.
        """
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
        """List context types in the account. Awaits the round-trip.

        Args:
            page_number: 1-based page to fetch. Defaults to the first page.
            page_size: Maximum number of context types per page. Defaults to
                the server's page size.

        Returns:
            The context types on the requested page.
        """
        kwargs = _pagination_kwargs(page_number, page_size)
        resp = await _gen_list_context_types.asyncio_detailed(client=self._app_http, **kwargs)
        _check_status(int(resp.status_code), resp.content)
        body = json.loads(resp.content)
        return [_ct_resource_from_dict(item, async_client=self) for item in body.get("data", [])]

    async def get(self, id: str) -> AsyncContextType:
        """Fetch a single context type by id. Awaits the round-trip.

        Args:
            id: Identifier of the context type to fetch.

        Returns:
            The matching :class:`AsyncContextType`.

        Raises:
            NotFoundError: If no context type with that id exists.
        """
        resp = await _gen_get_context_type.asyncio_detailed(id, client=self._app_http)
        _check_status(int(resp.status_code), resp.content)
        if resp.parsed is None:
            raise NotFoundError(f"ContextType with id {id!r} not found", status_code=404)
        return _ct_from_parsed(resp.parsed, sync_client=None, async_client=self)

    async def delete(self, id: str) -> None:
        """Delete a context type by id. Awaits the round-trip.

        Args:
            id: Identifier of the context type to delete.
        """
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
    """Sync context registration + read/delete (``client.platform.contexts``)."""

    def __init__(
        self,
        app_http: _AppAuthClient,
        buffer: _ContextRegistrationBuffer,
    ) -> None:
        self._app_http = app_http
        self._buffer = buffer

    def register(self, items: Context | list[Context], *, flush: bool = False) -> None:
        """Buffer one or more contexts for registration.

        Buffered contexts are sent in batches: a background flush kicks in once
        enough have accumulated, and any remainder is sent on the next explicit
        flush. Pass ``flush=True`` to send everything buffered right away.

        Args:
            items: A single context or a list of contexts to register.
            flush: When ``True``, send all buffered contexts immediately rather
                than waiting for the batch threshold. Defaults to ``False``.
        """
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
        """List all contexts of a given type.

        Args:
            type: Context type to list (for example ``"user"``).
            page_number: 1-based page to fetch. Defaults to the first page.
            page_size: Maximum number of contexts per page. Defaults to the
                server's page size.

        Returns:
            The contexts of the given type on the requested page.
        """
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
        """Fetch a single context, identified by composite id or by type and key.

        Args:
            id_or_type: Either the composite context id ``"type:key"`` (when
                ``key`` is omitted) or just the context type (when ``key`` is
                supplied).
            key: The context key. Provide it to use the two-argument form;
                omit it when ``id_or_type`` already carries the composite id.

        Returns:
            The matching :class:`Context`.

        Raises:
            NotFoundError: If no context with that id exists.
        """
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
        """Delete a single context, identified by composite id or by type and key.

        Args:
            id_or_type: Either the composite context id ``"type:key"`` (when
                ``key`` is omitted) or just the context type (when ``key`` is
                supplied).
            key: The context key. Provide it to use the two-argument form;
                omit it when ``id_or_type`` already carries the composite id.
        """
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
        """Buffer one or more contexts for registration.

        Buffered contexts are sent in batches: a background flush kicks in once
        enough have accumulated. Call ``await flush()`` to send any remainder
        immediately.

        Args:
            items: A single context or a list of contexts to register.
        """
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
        """List all contexts of a given type. Awaits the round-trip.

        Args:
            type: Context type to list (for example ``"user"``).
            page_number: 1-based page to fetch. Defaults to the first page.
            page_size: Maximum number of contexts per page. Defaults to the
                server's page size.

        Returns:
            The contexts of the given type on the requested page.
        """
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
        """Fetch a single context, identified by composite id or by type and key.

        Awaits the round-trip.

        Args:
            id_or_type: Either the composite context id ``"type:key"`` (when
                ``key`` is omitted) or just the context type (when ``key`` is
                supplied).
            key: The context key. Provide it to use the two-argument form;
                omit it when ``id_or_type`` already carries the composite id.

        Returns:
            The matching :class:`AsyncContext`.

        Raises:
            NotFoundError: If no context with that id exists.
        """
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
        """Delete a single context, identified by composite id or by type and key.

        Awaits the round-trip.

        Args:
            id_or_type: Either the composite context id ``"type:key"`` (when
                ``key`` is omitted) or just the context type (when ``key`` is
                supplied).
            key: The context key. Provide it to use the two-argument form;
                omit it when ``id_or_type`` already carries the composite id.
        """
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
# PlatformClient (client.platform)
# ---------------------------------------------------------------------------


class PlatformClient:
    """The Smpl Platform client (sync).

    Groups the account-wide CRUD resources that aren't owned by a single
    product, reachable as ``client.platform`` (:class:`smplkit.SmplClient`)
    or constructed directly::

        from smplkit import PlatformClient

        with PlatformClient(api_key="sk_...") as platform:
            prod = platform.environments.new("production", name="Production")
            prod.save()
            for svc in platform.services.list():
                ...

    Sub-clients: ``environments``, ``services``, ``contexts``,
    ``context_types``. Pure CRUD — no ``install()`` required.

    Args:
        api_key: API key. When omitted, resolved from ``SMPLKIT_API_KEY`` or
            ``~/.smplkit``.
        base_url: Full app-service base URL. Usually resolved from
            ``base_domain``/``scheme``; supplied directly by the top-level
            clients which have already computed it.
        profile: Named ``~/.smplkit`` profile section.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable SDK debug logging.
        extra_headers: Extra headers attached to every request.
        app_transport: Internal — a pre-built app transport supplied by a
            top-level client so the platform surface shares one connection
            pool. Not for direct use.
        context_buffer: Internal — the shared context-registration buffer.
            Not for direct use.
    """

    environments: EnvironmentsClient
    services: ServicesClient
    contexts: ContextsClient
    context_types: ContextTypesClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
        app_transport: _AppAuthClient | None = None,
        context_buffer: _ContextRegistrationBuffer | None = None,
    ) -> None:
        if app_transport is not None:
            self._app_http = app_transport
            self._owns_transport = False
        else:
            self._app_http = _platform_transport(
                api_key=api_key,
                base_url=base_url,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._owns_transport = True

        buffer = context_buffer if context_buffer is not None else _ContextRegistrationBuffer()
        self._context_buffer = buffer

        self.environments = EnvironmentsClient(self._app_http)
        self.services = ServicesClient(self._app_http)
        self.contexts = ContextsClient(self._app_http, buffer)
        self.context_types = ContextTypesClient(self._app_http)

    def close(self) -> None:
        """Close the app transport — only when this client owns it.

        A wired client borrows the parent's app transport and closes nothing.
        """
        if self._owns_transport:
            client = self._app_http._client
            if client is not None:
                client.close()
                self._app_http._client = None

    def __enter__(self) -> PlatformClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncPlatformClient:
    """The Smpl Platform client (async) — counterpart of :class:`PlatformClient`.

    Reads and CRUD perform their network round-trips with ``await``. Pure CRUD;
    no ``install()`` required.
    """

    environments: AsyncEnvironmentsClient
    services: AsyncServicesClient
    contexts: AsyncContextsClient
    context_types: AsyncContextTypesClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
        app_transport: _AppAuthClient | None = None,
        context_buffer: _ContextRegistrationBuffer | None = None,
    ) -> None:
        if app_transport is not None:
            self._app_http = app_transport
            self._owns_transport = False
        else:
            self._app_http = _platform_transport(
                api_key=api_key,
                base_url=base_url,
                profile=profile,
                base_domain=base_domain,
                scheme=scheme,
                debug=debug,
                extra_headers=extra_headers,
            )
            self._owns_transport = True

        buffer = context_buffer if context_buffer is not None else _ContextRegistrationBuffer()
        self._context_buffer = buffer

        self.environments = AsyncEnvironmentsClient(self._app_http)
        self.services = AsyncServicesClient(self._app_http)
        self.contexts = AsyncContextsClient(self._app_http, buffer)
        self.context_types = AsyncContextTypesClient(self._app_http)

    async def aclose(self) -> None:
        """Close the async app transport — only when this client owns it."""
        if self._owns_transport:
            ac = self._app_http._async_client
            if ac is not None:
                await ac.aclose()
                self._app_http._async_client = None

    async def __aenter__(self) -> AsyncPlatformClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()
