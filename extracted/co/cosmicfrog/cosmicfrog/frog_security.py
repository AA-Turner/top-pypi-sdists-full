"""
    Functions for service authentication
"""

from typing import Dict
import os
import httpx
import jwt
import time
from .sync_wrapper import sync_wrapper
from .frog_log import get_logger


# Environment
SECURITY_TIMEOUT = os.getenv("SECURITY_TIMEOUT") or 20.0
ADMIN_APP_KEY = os.getenv("ADMIN_APP_KEY")  # Note: Deliberate, no defaults for urls
ATLAS_SERVICE_URL = os.getenv("ATLAS_SERVICE_URL", "https://service.optilogic.app/appkey/authenticate")
ATLAS_API_BASE_URL = os.getenv("ATLAS_API_BASE_URL", "https://api.optilogic.app/v0/")
# the optilogic library has a setting for overriding the base
# url used for API calls. If this setting needs to be set, use
# this instead of the current ATLAS_API_BASE_URL
optilogic_api_url = os.getenv("OPTILOGIC_API_URL") or "https://api.optilogic.app"
if optilogic_api_url:
    ATLAS_API_BASE_URL = f"{optilogic_api_url}/v0/"


def validate_jwt(jwt_token):
    """
    Offline validation for api token
    This will throw DecodeError if token cannot be decoded
    """
    jwt.decode(jwt_token, options={"verify_signature": False})


def validate_bearer_token(bearer_token):
    """
    Fast offline validation of bearer token
    Will throw if invalid, else can be checked online
    """
    assert bearer_token is not None, "Bearer token is missing"
    assert bearer_token.startswith("Bearer "), "Bearer token is missing prefix"
    assert bearer_token.strip() != "Bearer", "Bearer token is missing jwt"
    jwt_token = bearer_token[7:]
    validate_jwt(jwt_token)


def extract_credentials(*args):
    """
    Utility to support calling security related functions with a header or individual keys
    """
    if len(args) == 1 and hasattr(args[0], "get"):
        headers = args[0]
        app_key = headers.get("X-App-KEY", None)
        api_key = headers.get("X-API-KEY", None)
        bearer_token = headers.get("Authorization", None)
    else:
        app_key, api_key, bearer_token = args

    return app_key, api_key, bearer_token


def _make_header(app_key: str, api_key: str, bearer_token: str) -> Dict[str, str]:
    """
    Create header for platform api calls
    """

    if not (app_key or api_key or bearer_token):
        assert False, "No authentication was provided (all keys empty)"

    # Basic bearer key validation
    if not (app_key or api_key):
        validate_bearer_token(bearer_token)

    assert ATLAS_API_BASE_URL

    # set up header with app key or api key depending on value set
    if app_key:
        header_key = "X-APP-KEY"
    else:
        header_key = "X-API-KEY"

    return {header_key: app_key or api_key or bearer_token.replace("Bearer ", "")}


async def _get_app_key_async(*args):
    """
    Given an api key or bearer token, fetch an app key

    Warning: Ensure keys are authenticated before calling, will use sub claim
    """
    logger = get_logger()
    assert ADMIN_APP_KEY, "ADMIN_APP_KEY is not configured"
    assert ATLAS_SERVICE_URL, "ATLAS_SERVICE_URL is not configured"

    app_key, api_key, bearer_token = extract_credentials(*args)

    if app_key:
        return app_key

    if not api_key:
        validate_bearer_token(bearer_token)
        api_key = bearer_token.replace("Bearer ", "")
    else:
        validate_jwt(api_key)

    # Get client ID from the token
    decoded_data = jwt.decode(api_key, options={"verify_signature": False})

    data = {"userId": decoded_data["sub"], "accountId": decoded_data["target_account_id"], "name": "Issuing Cosmic Frog key"}

    headers = {"x-app-key": ADMIN_APP_KEY}
    rv = ""
    async with httpx.AsyncClient() as client:
        status_code = 0
        retry_count = 0
        s_max_retries = os.getenv("AUTH_MAX_RETRIES") or "3"
        max_retries = int(s_max_retries)

        while retry_count < max_retries and status_code != 200:
            retry_count += 1
            response = await client.post(
                f"{ATLAS_SERVICE_URL}",
                headers=headers,
                json=data,
                timeout=SECURITY_TIMEOUT,
            )
            status_code = response.status_code

            if response.status_code == 409 and retry_count <= max_retries:
                logger.warning(f"retry {retry_count} to {ATLAS_SERVICE_URL} to get user token")
                time.sleep(5)
            elif response.status_code != 200:
                logger.error(
                    f"Status code {response.status_code} for {ATLAS_SERVICE_URL}. Tried {retry_count} time(s)"
                )
                raise ValueError(
                    f"Status code {response.status_code} for {ATLAS_SERVICE_URL}. Tried {retry_count} time(s). Failed to get a token: {response.content}"
                )
            else:
                rv = response.json().get("appkey")

    return rv


_get_app_key = sync_wrapper(_get_app_key_async)


async def _get_account_async(*args):
    """
    Fetch account details from platform

    Pass (app_key, api_key, bearer_token) or (request.headers)

    """

    assert ATLAS_API_BASE_URL, "ATLAS_API_BASE_URL is not configured"

    app_key, api_key, bearer_token = extract_credentials(*args)

    new_headers = _make_header(app_key, api_key, bearer_token)

    url = f'{ATLAS_API_BASE_URL.strip("/")}/account'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=new_headers, timeout=SECURITY_TIMEOUT)
        response.raise_for_status()
        return response.json()


_get_account = sync_wrapper(_get_account_async)


async def socket_secured_async(app_key: str, api_key: str, bearer_token: str):
    """
    Used for socket.io
    """
    acc = await _get_account_async(app_key, api_key, bearer_token)

    assert acc

    return acc


socket_secured = sync_wrapper(socket_secured_async)
