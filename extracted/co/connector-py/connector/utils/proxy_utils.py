import json
import logging
import tempfile
from asyncio import get_running_loop
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import Lock

import httpx
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.session import get_session
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger("integration-connectors.sdk")

API_ENDPOINT = "https://0q6vf2tzd1.execute-api.us-west-2.amazonaws.com/prod"
MACAROON_TTL = 60 * 5  # 5 minutes
TEMPFILE_NAME = "lumos-proxy-auth.json"
CACHE_LOCK = Lock()


class ProxyToken(BaseModel):
    token: str
    expire_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(seconds=MACAROON_TTL)
    )


def _call_prod_macaroon_dispenser_sync() -> str:
    session = get_session()
    credentials = session.get_credentials().get_frozen_credentials()
    region = "us-west-2"
    service = "execute-api"
    headers = {"Content-Type": "application/json"}

    request = AWSRequest(method="POST", url=API_ENDPOINT, headers=headers)
    signer = SigV4Auth(credentials, service, region)

    signer.add_auth(request)

    logger.info("Requesting a new proxy macaroon token")
    with httpx.Client() as client:
        response = client.post(
            API_ENDPOINT,
            headers=dict(request.headers.items()),
            content=request.body,
        )

    data = response.json()
    if isinstance(data, str):
        # it sometimes returns a JSON string for some reason
        data = json.loads(data)

    if "macaroon" not in data:
        raise ValueError(f"Proxy macaroon not found in response: {data}")

    logger.info("Received a new proxy macaroon token")
    return data["macaroon"]


def get_proxy_token_sync() -> ProxyToken:
    with CACHE_LOCK:
        path = Path(tempfile.gettempdir()) / TEMPFILE_NAME
        try:
            if not path.exists():
                raise FileNotFoundError("File not found")
            data = path.read_text(encoding="utf-8")
            cache = ProxyToken.model_validate_json(data)
            if cache.expire_at < datetime.now(timezone.utc):
                raise TimeoutError("Token expired")

        except (ValidationError, TimeoutError, FileNotFoundError, TypeError) as exc:
            logger.info(f"Proxy token cache invalid or expired: {exc}")
            cache = ProxyToken(token=_call_prod_macaroon_dispenser_sync())
            path.write_text(cache.model_dump_json(), encoding="utf-8")

    return cache


async def get_proxy_token_async() -> ProxyToken:
    return await get_running_loop().run_in_executor(None, get_proxy_token_sync)


def get_proxy_url() -> str:
    return "https://secure-integration-proxy.lumos.com/forward"
