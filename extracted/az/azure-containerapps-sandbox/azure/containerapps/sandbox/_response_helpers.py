"""Preserve existing handwritten response-list defaults."""

from __future__ import annotations

from typing import Any, TypeVar

from azure.containerapps.sandbox import models
from azure.containerapps.sandbox._generated._utils.model_base import Model
from azure.containerapps.sandbox._helpers import _get_json_array

_T = TypeVar("_T")

_LIST_FIELDS = {
    models.Sandbox: (("ports", False), ("connections", False)),
    models.PortsListResponse: (("ports", False),),
    models.PortIpAccessControl: (("rules", False),),
    models.PortIpAccessControlRule: (("sourceCidrs", False),),
    models.PortAuthEntraId: (("emails", False),),
    models.EgressPolicy: (("hostRules", False), ("rules", True)),
    models.TdsEgressSection: (("credentials", False), ("rules", True)),
    models.PostgresEgressSection: (("credentials", False), ("rules", True)),
    models.DirListing: (("entries", False),),
    models.NetworkEgressDecisions: (("allowed", False), ("denied", False)),
}

_NESTED_FIELDS = {
    models.Sandbox: ("ports", "egress_policy"),
    models.PortsListResponse: ("ports",),
    models.SandboxPort: ("auth", "ip_access_control"),
    models.PortAuthConfig: ("entra_id",),
    models.PortIpAccessControl: ("rules",),
    models.EgressPolicy: ("tds", "postgres"),
    models.EgressDecisions: ("http",),
}


def _normalize_response_lists(value: _T) -> _T:
    """Apply only the list conversions supported by the previous facade."""
    if isinstance(value, Model):
        for wire_name, nullable in _LIST_FIELDS.get(type(value), ()):
            items = _get_json_array(value, wire_name, nullable=nullable)
            if wire_name not in value or value[wire_name] is None:
                value[wire_name] = items
        for name in _NESTED_FIELDS.get(type(value), ()):
            _normalize_response_lists(getattr(value, name))
    elif isinstance(value, list):
        for item in value:
            _normalize_response_lists(item)
    return value


def _normalize_response(_response: Any, value: _T, _headers: Any) -> _T:
    return _normalize_response_lists(value)


def _normalize_page(items: list[_T]) -> list[_T]:
    if items is None:
        raise TypeError("value must be a JSON array")
    return _normalize_response_lists(items)
