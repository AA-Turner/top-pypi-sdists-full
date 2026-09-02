"""Synchronous Secret resource API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from novita_sandbox.core.api import handle_api_exception
from novita_sandbox.core.api.client_sync import get_api_client
from novita_sandbox.core.connection_config import ConnectionConfig
from novita_sandbox.core.exceptions import InvalidArgumentException
from novita_sandbox.core.secret.validation import (
    normalize_secret_hosts,
    validate_secret_name,
)


@dataclass
class SecretBinding:
    """Non-secret metadata for a configured brokered secret."""

    name: str
    hosts: List[str]
    placeholder: str
    description: Optional[str]
    has_secret: bool
    status: str
    updated_at: Optional[str] = None


class Secret:
    """Resource methods for write-only sandbox secrets."""

    _base = "/secrets"

    @classmethod
    def create(
        cls,
        *,
        name: str,
        value: str,
        hosts: List[str],
        description: Optional[str] = None,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        domain: Optional[str] = None,
        request_timeout: Optional[float] = None,
    ) -> SecretBinding:
        """Create one brokered secret."""
        validate_secret_name(name)
        if not value:
            raise InvalidArgumentException("value is required")
        normalized_hosts = normalize_secret_hosts(hosts)
        payload = {"name": name, "value": value, "hosts": normalized_hosts}
        if description is not None:
            payload["description"] = description

        client = get_api_client(
            _connection_config(api_key, api_url, domain, request_timeout)
        )
        res = client.get_httpx_client().post(cls._base, json=payload)
        if res.status_code >= 300:
            raise handle_api_exception(res)
        return _binding_from_json(res.json())

    @classmethod
    def list(
        cls,
        *,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        domain: Optional[str] = None,
        request_timeout: Optional[float] = None,
    ) -> List[SecretBinding]:
        """List secret metadata. Never returns values."""
        client = get_api_client(
            _connection_config(api_key, api_url, domain, request_timeout)
        )
        res = client.get_httpx_client().get(cls._base)
        if res.status_code >= 300:
            raise handle_api_exception(res)
        return [_binding_from_json(item) for item in res.json().get("secrets", [])]

    @classmethod
    def get(
        cls,
        name: str,
        *,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        domain: Optional[str] = None,
        request_timeout: Optional[float] = None,
    ) -> SecretBinding:
        """Get one secret metadata entry by name. Never returns the value."""
        validate_secret_name(name)
        client = get_api_client(
            _connection_config(api_key, api_url, domain, request_timeout)
        )
        res = client.get_httpx_client().get(f"{cls._base}/{name}")
        if res.status_code >= 300:
            raise handle_api_exception(res)
        return _binding_from_json(res.json())

    @classmethod
    def update(
        cls,
        *,
        name: str,
        value: str,
        hosts: List[str],
        description: Optional[str] = None,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        domain: Optional[str] = None,
        request_timeout: Optional[float] = None,
    ) -> SecretBinding:
        """Replace one brokered secret."""
        validate_secret_name(name)
        if not value:
            raise InvalidArgumentException("value is required")
        normalized_hosts = normalize_secret_hosts(hosts)
        payload = {"value": value, "hosts": normalized_hosts}
        if description is not None:
            payload["description"] = description

        client = get_api_client(
            _connection_config(api_key, api_url, domain, request_timeout)
        )
        res = client.get_httpx_client().put(f"{cls._base}/{name}", json=payload)
        if res.status_code >= 300:
            raise handle_api_exception(res)
        return _binding_from_json(res.json())

    @classmethod
    def delete(
        cls,
        name: str,
        *,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        domain: Optional[str] = None,
        request_timeout: Optional[float] = None,
    ) -> str:
        """Delete one secret by name. Returns the deleted name."""
        validate_secret_name(name)
        client = get_api_client(
            _connection_config(api_key, api_url, domain, request_timeout)
        )
        res = client.get_httpx_client().delete(f"{cls._base}/{name}")
        if res.status_code >= 300:
            raise handle_api_exception(res)
        return str(res.json().get("deleted", ""))


def _connection_config(
    api_key: Optional[str],
    api_url: Optional[str],
    domain: Optional[str],
    request_timeout: Optional[float],
) -> ConnectionConfig:
    return ConnectionConfig(
        api_key=api_key,
        api_url=api_url,
        domain=domain,
        request_timeout=request_timeout,
    )


def _binding_from_json(data: dict) -> SecretBinding:
    return SecretBinding(
        name=data["name"],
        hosts=list(data.get("hosts", [])),
        placeholder=data["placeholder"],
        description=data.get("description"),
        has_secret=bool(data["hasSecret"]),
        status=data["status"],
        updated_at=data.get("updatedAt"),
    )
