"""Stainless-compatible client construction, cloning, and lifecycle behavior."""

from __future__ import annotations

import asyncio
from collections.abc import Mapping
from typing import Any

import httpx
import pytest
from typing_extensions import is_typeddict

import composio_client
from composio_client import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    NOT_GIVEN,
    AsyncComposio,
    Auth,
    Composio,
    DefaultAsyncHttpxClient,
    DefaultHttpxClient,
    NotGiven,
    Omit,
    ProjectAuth,
    RequestOptions,
    omit,
)
from composio_client._types import PropertyInfo


class StainlessShapedSubclass(Composio):
    """A downstream subclass whose constructor predates ``scope`` and ``identity``."""

    def __init__(
        self,
        *,
        auth: Auth,
        environment: Any = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str | None] | None = None,
        http_client: httpx.Client | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        super().__init__(
            auth=auth,
            environment=environment,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )


def test_root_exports_are_runtime_values() -> None:
    assert composio_client.__title__ == "composio_client"
    assert DEFAULT_MAX_RETRIES == 2
    assert DEFAULT_TIMEOUT.connect == 5.0
    assert DEFAULT_TIMEOUT.read == 60.0
    assert isinstance(NOT_GIVEN, NotGiven)
    assert isinstance(omit, Omit)


def test_request_options_are_constructible_mappings() -> None:
    assert is_typeddict(RequestOptions)
    options = RequestOptions(headers={"x-trace": "trace"}, max_retries=0, timeout=None)
    assert options == {"headers": {"x-trace": "trace"}, "max_retries": 0, "timeout": None}


def test_property_info_repr_uses_only_present_python_values() -> None:
    assert repr(PropertyInfo()) == "PropertyInfo()"
    assert repr(PropertyInfo(alias="customer's")) == """PropertyInfo(alias="customer's")"""
    assert repr(
        PropertyInfo(
            alias="authScheme",
            format="date-time",
            format_template="{value}",
            discriminator="kind",
        )
    ) == (
        "PropertyInfo(alias='authScheme', format='date-time', "
        "format_template='{value}', discriminator='kind')"
    )


def test_default_httpx_clients_apply_stainless_defaults() -> None:
    with DefaultHttpxClient() as sync:
        assert sync.follow_redirects is True
        assert sync.timeout.connect == 5.0
        assert sync.timeout.read == 60.0

    async_client = DefaultAsyncHttpxClient()
    try:
        assert async_client.follow_redirects is True
        assert async_client.timeout.connect == 5.0
    finally:
        asyncio.run(async_client.aclose())


def test_constructor_accepts_url_timeout_and_strict_validation() -> None:
    client = Composio(
        auth=ProjectAuth("key"),
        base_url=httpx.URL("https://client.invalid"),
        timeout=None,
        _strict_response_validation=True,
    )
    try:
        assert client.base_url == "https://client.invalid"
        assert client.timeout is None
        assert client._strict_response_validation is True
    finally:
        client.close()


def test_explicit_base_url_takes_precedence_over_environment() -> None:
    client = Composio(
        auth=ProjectAuth("key"),
        environment="staging",
        base_url="https://explicit.invalid",
    )
    try:
        assert client.base_url == "https://explicit.invalid"
    finally:
        client.close()


def test_with_options_merges_defaults_and_reuses_the_transport() -> None:
    transport = httpx.Client()
    client = Composio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=transport,
        default_headers={"x-first": "1"},
    )
    merged = client.with_options(default_headers={"x-second": "2"})
    replaced = client.with_options(set_default_headers={"x-only": "3"})

    assert merged._client is transport
    assert replaced._client is transport
    assert merged.default_headers == {"x-first": "1", "x-second": "2"}
    assert replaced.default_headers == {"x-only": "3"}
    assert merged.tool_router._client is merged
    assert replaced.tool_router._client is replaced

    # Stainless clones share the caller's transport; closing any clone closes
    # that transport for the whole family.
    merged.close()
    assert transport.is_closed


def test_with_options_supports_stainless_shaped_subclasses() -> None:
    client = StainlessShapedSubclass(auth=ProjectAuth("key"), base_url="https://client.invalid")
    clone = client.with_options(max_retries=0)
    try:
        assert isinstance(clone, StainlessShapedSubclass)
        assert clone.max_retries == 0
    finally:
        clone.close()


def test_with_options_can_select_an_environment_without_inheriting_base_url() -> None:
    client = Composio(auth=ProjectAuth("key"), base_url="https://client.invalid")
    clone = client.with_options(environment="staging")
    try:
        assert clone.base_url == "https://staging-backend.composio.dev"
    finally:
        clone.close()
        client.close()


def test_context_manager_returns_and_closes_the_client() -> None:
    client = Composio(auth=ProjectAuth("key"), base_url="https://client.invalid")
    with client as entered:
        assert entered is client
        assert client.is_closed() is False
    assert client.is_closed() is True


@pytest.mark.asyncio
async def test_async_with_options_and_close_alias_match_sync_behavior() -> None:
    transport = httpx.AsyncClient()
    client = AsyncComposio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=transport,
        default_headers={"x-first": "1"},
    )
    clone = client.with_options(default_headers={"x-second": "2"})

    assert clone._client is transport
    assert clone.default_headers == {"x-first": "1", "x-second": "2"}
    assert clone.tool_router._client is clone

    await clone.close()
    assert transport.is_closed


@pytest.mark.asyncio
async def test_async_context_manager_uses_public_close() -> None:
    client = AsyncComposio(auth=ProjectAuth("key"), base_url="https://client.invalid")
    async with client as entered:
        assert entered is client
        assert client.is_closed() is False
    assert client.is_closed() is True
