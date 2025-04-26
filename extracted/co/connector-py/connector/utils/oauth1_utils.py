import base64
import hashlib
import hmac
import random
import string
import time
import urllib.parse
from typing import Any

import httpx

from connector.generated import OAuth1Credential


def generate_nonce(length: int = 16) -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_timestamp() -> str:
    return str(int(time.time()))


def encode_parameter(value: str | bytes) -> str:
    if isinstance(value, str):
        value = value.encode("utf-8")
    return urllib.parse.quote(value, safe="").replace("%7E", "~")


def build_signature_base_string(http_method: str, base_url: str, params: dict[str, Any]) -> str:
    encoded_params = []
    for key, value in sorted(params.items()):
        encoded_params.append(f"{encode_parameter(key)}={encode_parameter(value)}")

    parameter_string = "&".join(encoded_params)

    signature_base = (
        encode_parameter(http_method.upper())
        + "&"
        + encode_parameter(base_url)
        + "&"
        + encode_parameter(parameter_string)
    )

    return signature_base


def build_signature(signature_base: str, consumer_secret: str, token_secret: str) -> str:
    key = encode_parameter(consumer_secret) + "&" + encode_parameter(token_secret)

    signature = hmac.new(
        key.encode("utf-8"), signature_base.encode("utf-8"), hashlib.sha256
    ).digest()

    return base64.b64encode(signature).decode("utf-8")


def generate_oauth1_header(
    consumer_key: str,
    consumer_secret: str,
    token_id: str,
    token_secret: str,
    url: str,
    realm: str | None = None,
    http_method: str = "GET",
    query_params: dict[str, Any] | None = None,
    oauth_body_hash: str | None = None,
):
    parsed_url = urllib.parse.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    url_params = {}
    if parsed_url.query:
        url_params = dict(urllib.parse.parse_qsl(parsed_url.query))

    combined_params = {}
    if query_params:
        combined_params.update(query_params)
    combined_params.update(url_params)

    oauth_params = {
        "oauth_consumer_key": consumer_key,
        "oauth_token": token_id,
        "oauth_nonce": generate_nonce(),
        "oauth_timestamp": get_timestamp(),
        "oauth_signature_method": "HMAC-SHA256",
        "oauth_version": "1.0",
    }

    if oauth_body_hash:
        oauth_params["oauth_body_hash"] = oauth_body_hash

    signature_params = {}
    signature_params.update(combined_params)
    signature_params.update(oauth_params)

    signature_base = build_signature_base_string(http_method, base_url, signature_params)
    signature = build_signature(signature_base, consumer_secret, token_secret)

    oauth_params["oauth_signature"] = signature

    auth_header = "OAuth "
    if realm:
        auth_header += f'realm="{realm}",'

    auth_header += ",".join(
        [f'{encode_parameter(k)}="{encode_parameter(v)}"' for k, v in oauth_params.items()]
    )

    return auth_header


def calculate_body_hash(body: bytes | dict[str, Any] | list[Any] | str | None):
    if body is None:
        body = ""
    elif isinstance(body, dict) or isinstance(body, list):
        import json

        body = json.dumps(body)
    elif not isinstance(body, str):
        body = str(body)

    if isinstance(body, str):
        body = body.encode("utf-8")

    hash_obj = hashlib.sha256(body)
    return base64.b64encode(hash_obj.digest()).decode("utf-8")


def use_oauth1_with_request(
    request: httpx.Request, credentials: OAuth1Credential, realm: str | None = None
) -> httpx.Request:
    consumer_key = credentials.consumer_key
    consumer_secret = credentials.consumer_secret
    token_id = credentials.token_id
    token_secret = credentials.token_secret

    http_method = str(request.method)
    url = str(request.url)

    oauth_body_hash = None
    if http_method.upper() in ["POST", "PUT", "PATCH"] and hasattr(request, "content"):
        oauth_body_hash = calculate_body_hash(request.content)

    query_params = {}
    if hasattr(request.url, "params") and request.url.params:
        query_params = dict(request.url.params)

    auth_header = generate_oauth1_header(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        token_id=token_id,
        token_secret=token_secret,
        realm=realm,
        url=url,
        http_method=http_method,
        query_params=query_params,
        oauth_body_hash=oauth_body_hash,
    )

    request.headers["Authorization"] = auth_header

    return request
