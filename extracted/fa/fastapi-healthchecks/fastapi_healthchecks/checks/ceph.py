from asyncio import wait_for
from contextlib import AbstractAsyncContextManager as AsyncContextManager
from secrets import token_hex
from typing import TYPE_CHECKING

from pydantic import AnyHttpUrl

from ._base import Check, CheckResult

try:
    from aioboto3 import Session
    from botocore.exceptions import ClientError
except ImportError as exc:
    raise ImportError("Using this module requires the aioboto3 library.") from exc

if TYPE_CHECKING:
    from types_aiobotocore_s3.client import S3Client


class CephCheck(Check):
    _host: str
    _access_key: str
    _secret_key: str
    _bucket: str | None
    _secure: bool
    _verify_ssl: bool
    _timeout: int
    _name: str

    def __init__(
        self,
        host: str,
        access_key: str,
        secret_key: str,
        bucket: str | None = None,
        secure: bool = True,
        verify_ssl: bool = True,
        timeout: int = 60,
        name: str = "Ceph",
    ):
        self._host = host
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket = bucket
        self._secure = secure
        self._verify_ssl = verify_ssl
        self._timeout = timeout
        self._name = name

    async def __call__(self) -> CheckResult:
        try:
            endpoint_url = AnyHttpUrl.build(scheme="https" if self._secure else "http", host=self._host)
            client_context_manager: AsyncContextManager[S3Client] = Session().client(
                "s3",
                endpoint_url=str(endpoint_url),
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_key,
                verify=self._verify_ssl,
            )
            async with client_context_manager as client:
                bucket: str = token_hex(16) if self._bucket is None else self._bucket
                await wait_for(client.head_bucket(Bucket=bucket), self._timeout)
        except Exception as exception:
            if not isinstance(exception, ClientError) or exception.response["Error"]["Code"] != "404":
                return CheckResult(name=self._name, passed=False, details=str(exception))

        return CheckResult(name=self._name, passed=True)
