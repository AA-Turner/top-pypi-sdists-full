"""Environment variable factory."""

from os import getenv
from typing import Optional, Tuple, Union
from urllib.parse import urlparse

from ..constants.auth import DEFAULT_SCOPE
from ..constants.env_var_names import (
    CLIENT_ID_ENV_NAME,
    CLIENT_SECRET_ENV_NAME,
    SITE_URL_ENV_NAME,
    CONNECTOR_TIMEOUT_SECONDS_ENV_NAME,
    QUERY_PAGE_SIZE_ENV_NAME,
    QUERY_CELL_PAGINATION_LIMIT_ENV_NAME,
    QUERY_DELETE_PAGE_SIZE_ENV_NAME,
    CONCURRENCY_LIMIT_READ_ENV_NAME,
    CONCURRENCY_LIMIT_DELETE_ENV_NAME,
    CONCURRENCY_LIMIT_CREATE_ENV_NAME,
    RETRY_TOO_MANY_REQUESTS_ENV_NAME,
    RETRY_INTERNAL_SERVER_ERROR_ENV_NAME,
    RETRY_SERVICE_UNAVAILABLE_ENV_NAME,
    RETRY_BAD_GATEWAY_ENV_NAME,
    RETRY_GATEWAY_TIMEOUT_ENV_NAME,
    RETRY_BACKOFF_FACTOR_ENV_NAME,
    RETRY_MAX_BACKOFF_SECONDS_ENV_NAME,
)
from ..models.factory_models import DealCloudConfig, DealCloudFactoryArgs, QuerySettings, ConcurrencyLimits, ResponseRetrySettings


def read_env_config(env_name: str) -> str:
    """Read environment variable, raising KeyError if not set."""
    env_value = getenv(env_name)
    if not env_value:
        raise KeyError(f"The environment variable {env_name} could not be found!")
    return env_value


def read_env_int(env_name: str, default: Optional[int] = None) -> Optional[int]:
    """Read integer environment variable, returning default if not set."""
    env_value = getenv(env_name)
    if not env_value:
        return default
    try:
        return int(env_value)
    except ValueError:
        raise ValueError(f"Environment variable {env_name} must be an integer, got: {env_value}")


def read_env_float(env_name: str, default: Optional[float] = None) -> Optional[float]:
    """Read float environment variable, returning default if not set."""
    env_value = getenv(env_name)
    if not env_value:
        return default
    try:
        return float(env_value)
    except ValueError:
        raise ValueError(f"Environment variable {env_name} must be a float, got: {env_value}")


def normalize_site_url(site_url: str) -> str:
    """
    Return only the host part of a site URL (e.g. site.intapp.com).
    If the value contains a scheme (https:// or http://) or path, strip to host only.
    """
    if not site_url or not isinstance(site_url, str):
        return site_url
    s = site_url.strip()
    parsed = urlparse(s) if "://" in s else urlparse("//" + s)
    return parsed.netloc if parsed.netloc else s


def dc_from_environment_variables(
    site_url_env_name: str = SITE_URL_ENV_NAME,
    client_id_env_name: str = CLIENT_ID_ENV_NAME,
    client_secret_env_name: str = CLIENT_SECRET_ENV_NAME,
    scope: Tuple[str, ...] = DEFAULT_SCOPE,
    connector_timeout_env_name: str = CONNECTOR_TIMEOUT_SECONDS_ENV_NAME,
    query_page_size_env_name: str = QUERY_PAGE_SIZE_ENV_NAME,
    query_cell_pagination_limit_env_name: str = QUERY_CELL_PAGINATION_LIMIT_ENV_NAME,
    query_delete_page_size_env_name: str = QUERY_DELETE_PAGE_SIZE_ENV_NAME,
    concurrency_limit_read_env_name: str = CONCURRENCY_LIMIT_READ_ENV_NAME,
    concurrency_limit_delete_env_name: str = CONCURRENCY_LIMIT_DELETE_ENV_NAME,
    concurrency_limit_create_env_name: str = CONCURRENCY_LIMIT_CREATE_ENV_NAME,
    retry_too_many_requests_env_name: str = RETRY_TOO_MANY_REQUESTS_ENV_NAME,
    retry_internal_server_error_env_name: str = RETRY_INTERNAL_SERVER_ERROR_ENV_NAME,
    retry_service_unavailable_env_name: str = RETRY_SERVICE_UNAVAILABLE_ENV_NAME,
    retry_bad_gateway_env_name: str = RETRY_BAD_GATEWAY_ENV_NAME,
    retry_gateway_timeout_env_name: str = RETRY_GATEWAY_TIMEOUT_ENV_NAME,
    retry_backoff_factor_env_name: str = RETRY_BACKOFF_FACTOR_ENV_NAME,
    retry_max_backoff_seconds_env_name: str = RETRY_MAX_BACKOFF_SECONDS_ENV_NAME,
) -> Union[DealCloudConfig, DealCloudFactoryArgs]:
    """
    Create DealCloud config from environment variables.
    
    Returns DealCloudConfig if any optional settings are provided via environment variables,
    otherwise returns DealCloudFactoryArgs for backward compatibility.
    """
    # Required credentials
    site_url = normalize_site_url(read_env_config(site_url_env_name))
    client_id = read_env_config(client_id_env_name)
    client_secret = read_env_config(client_secret_env_name)
    
    # Optional settings
    connector_timeout = read_env_int(connector_timeout_env_name)
    query_page_size = read_env_int(query_page_size_env_name)
    query_cell_pagination_limit = read_env_int(query_cell_pagination_limit_env_name)
    query_delete_page_size = read_env_int(query_delete_page_size_env_name)
    concurrency_limit_read = read_env_int(concurrency_limit_read_env_name)
    concurrency_limit_delete = read_env_int(concurrency_limit_delete_env_name)
    concurrency_limit_create = read_env_int(concurrency_limit_create_env_name)
    retry_too_many_requests = read_env_int(retry_too_many_requests_env_name)
    retry_internal_server_error = read_env_int(retry_internal_server_error_env_name)
    retry_service_unavailable = read_env_int(retry_service_unavailable_env_name)
    retry_bad_gateway = read_env_int(retry_bad_gateway_env_name)
    retry_gateway_timeout = read_env_int(retry_gateway_timeout_env_name)
    retry_backoff_factor = read_env_float(retry_backoff_factor_env_name)
    retry_max_backoff_seconds = read_env_float(retry_max_backoff_seconds_env_name)
    
    # Check if any optional settings were provided
    has_optional_settings = any([
        connector_timeout is not None,
        query_page_size is not None,
        query_cell_pagination_limit is not None,
        query_delete_page_size is not None,
        concurrency_limit_read is not None,
        concurrency_limit_delete is not None,
        concurrency_limit_create is not None,
        retry_too_many_requests is not None,
        retry_internal_server_error is not None,
        retry_service_unavailable is not None,
        retry_bad_gateway is not None,
        retry_gateway_timeout is not None,
        retry_backoff_factor is not None,
        retry_max_backoff_seconds is not None,
    ])
    
    if has_optional_settings:
        # Build full DealCloudConfig with provided settings
        query_settings = QuerySettings()
        if query_page_size is not None:
            query_settings.pageSize = query_page_size
        if query_cell_pagination_limit is not None:
            query_settings.cellPaginationLimit = query_cell_pagination_limit
        if query_delete_page_size is not None:
            query_settings.deletePageSize = query_delete_page_size
        
        concurrency_limits = ConcurrencyLimits()
        if concurrency_limit_read is not None:
            concurrency_limits.read = concurrency_limit_read
        if concurrency_limit_delete is not None:
            concurrency_limits.delete = concurrency_limit_delete
        if concurrency_limit_create is not None:
            concurrency_limits.create = concurrency_limit_create
        
        retry_settings = ResponseRetrySettings()
        if retry_too_many_requests is not None:
            retry_settings.tooManyRequests = retry_too_many_requests
        if retry_internal_server_error is not None:
            retry_settings.internalServerError = retry_internal_server_error
        if retry_service_unavailable is not None:
            retry_settings.serviceUnavailable = retry_service_unavailable
        if retry_bad_gateway is not None:
            retry_settings.badGateway = retry_bad_gateway
        if retry_gateway_timeout is not None:
            retry_settings.gatewayTimeout = retry_gateway_timeout
        if retry_backoff_factor is not None:
            retry_settings.backoffFactor = retry_backoff_factor
        if retry_max_backoff_seconds is not None:
            retry_settings.maxBackoffSeconds = retry_max_backoff_seconds
        
        return DealCloudConfig(
            siteUrl=site_url,
            clientId=client_id,
            clientSecret=client_secret,
            scope=scope,
            connectorTimeoutSeconds=connector_timeout if connector_timeout is not None else 100,
            querySettings=query_settings,
            concurrencyLimits=concurrency_limits,
            responseRetrySettings=retry_settings,
        )
    else:
        # Backward compatibility: return DealCloudFactoryArgs if only credentials provided
        return DealCloudFactoryArgs(
            site_url=site_url,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
        )


