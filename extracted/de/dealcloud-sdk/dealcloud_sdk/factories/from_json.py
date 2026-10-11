"""JSON configuration factory."""

import json
from typing import Optional, Tuple, Union

import fsspec

from .from_env import normalize_site_url
from ..constants.auth import DEFAULT_SCOPE
from ..models.factory_models import DealCloudFactoryArgs, DealCloudConfig


# Keys that indicate full configuration format
_DOTNET_FORMAT_KEYS = {
    'connectorTimeoutSeconds',
    'responseRetrySettings',
    'querySettings',
    'concurrencyLimits',
}


def _get_nested_value(data: dict, path: str) -> dict:
    """Get nested value from dict using dot notation path."""
    if not path:
        return data
    
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            raise KeyError(f"Path '{path}' not found in configuration")
    return current


def _is_dotnet_format(data: dict) -> bool:
    """Check if config data is in full configuration format."""
    return bool(_DOTNET_FORMAT_KEYS & set(data.keys()))


def dc_from_json_config(
    json_file_path: str,
    json_path_to_credentials: Optional[str] = None,
    scope: Tuple[str, ...] = DEFAULT_SCOPE,
) -> Union[DealCloudFactoryArgs, DealCloudConfig]:
    """
    Create DealCloud config from JSON file.
    
    Supports two formats with auto-detection:
    
    1. Legacy Python SDK format (simple credentials):
        {
            "site_url": "client.dealcloud.com",
            "client_id": "12345",
            "client_secret": "secret"
        }
    
    2. Full configuration format:
        {
            "siteUrl": "client.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret",
            "connectorTimeoutSeconds": 100,
            "querySettings": {
                "pageSize": 1000,
                "cellPaginationLimit": 9000,
                "deletePageSize": 10000
            },
            "concurrencyLimits": {
                "read": 2,
                "delete": 2,
                "create": 2
            },
            "responseRetrySettings": {
                "tooManyRequests": 5,
                "internalServerError": 2,
                "serviceUnavailable": 2,
                "backoffFactor": 2
            }
        }
    
    Auto-detection: If any of these keys are present, full configuration format is assumed:
    - connectorTimeoutSeconds
    - responseRetrySettings
    - querySettings
    - concurrencyLimits
    
    Args:
        json_file_path: Path to JSON config file
        json_path_to_credentials: Optional dot notation path to credentials object
            e.g., "dealcloud.credentials" to access nested config
    
    Returns:
        DealCloudConfig if full configuration format detected, else DealCloudFactoryArgs
    
    Example JSON (flat legacy):
        {
            "site_url": "client.dealcloud.com",
            "client_id": "12345",
            "client_secret": "secret"
        }
    
    Example JSON (nested legacy, path="dealcloud"):
        {
            "dealcloud": {
                "site_url": "client.dealcloud.com",
                "client_id": "12345",
                "client_secret": "secret"
            }
        }
    
    Example JSON (full configuration format):
        {
            "siteUrl": "client.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret",
            "connectorTimeoutSeconds": 100,
            "responseRetrySettings": {
                "tooManyRequests": 10,
                "backoffFactor": 3.0
            }
        }
    """
    with fsspec.open(json_file_path, 'r') as f:
        data = json.load(f)
    
    if json_path_to_credentials:
        data = _get_nested_value(data, json_path_to_credentials)
    
    # Check for full configuration format
    if _is_dotnet_format(data):
        # Normalize keys: support both snake_case and camelCase for credentials
        normalized = _normalize_to_dotnet_format(data)
        if "scope" not in normalized:
            normalized["scope"] = scope
        elif isinstance(normalized["scope"], list):
            normalized["scope"] = tuple(normalized["scope"])
        return DealCloudConfig(**normalized)

    # Legacy format - return simple args
    raw_site_url = data.get("site_url") or data.get("siteUrl")
    return DealCloudFactoryArgs(
        site_url=normalize_site_url(raw_site_url) if raw_site_url else raw_site_url,
        client_id=str(data.get("client_id") or data.get("clientId")),
        client_secret=data.get("client_secret") or data.get("clientSecret"),
        scope=scope,
    )


def _normalize_to_dotnet_format(data: dict) -> dict:
    """
    Normalize config keys to full configuration format (camelCase).
    
    Supports snake_case alternatives for the core credential fields.
    Strips scheme/path from siteUrl so only the host is stored (e.g. site.intapp.com).
    """
    result = data.copy()

    # Normalize core credential fields (support snake_case)
    if 'site_url' in result and 'siteUrl' not in result:
        result['siteUrl'] = result.pop('site_url')
    if 'client_id' in result and 'clientId' not in result:
        result['clientId'] = str(result.pop('client_id'))
    if 'client_secret' in result and 'clientSecret' not in result:
        result['clientSecret'] = result.pop('client_secret')

    # Ensure siteUrl is host-only (no https:// or path)
    if 'siteUrl' in result and result['siteUrl']:
        result['siteUrl'] = normalize_site_url(result['siteUrl'])
    # Ensure clientId is string
    if 'clientId' in result:
        result['clientId'] = str(result['clientId'])

    return result
