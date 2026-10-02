"""Wiring between Arraylake's vended bucket credentials and obstore's credential providers.

Stores handed to users need credentials that outlive a single vend, so that long
operations (large listings, long uploads) don't die partway through with an expired
token. obstore supports this via a `credential_provider` callback, which it invokes
only once the credential it holds has lapsed.
"""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any, Literal

from arraylake.asyn import asyncio_run
from arraylake.credentials import _use_delegated_credentials
from arraylake.types import (
    BucketNickname,
    BucketResponse,
    GSCredentials,
    OrgName,
    Platform,
    S3Credentials,
    TempCredentials,
)

if TYPE_CHECKING:
    from arraylake.client import AsyncClient


def _as_aware(expiration: datetime | None) -> datetime | None:
    """obstore requires timezone-aware expiries; credentials may carry naive UTC datetimes."""
    if expiration is not None and expiration.tzinfo is None:
        return expiration.replace(tzinfo=UTC)
    return expiration


def _to_obstore_credential(creds: TempCredentials) -> dict[str, Any]:
    """Convert vended credentials into the dict shape obstore's S3/GCS credential providers expect."""
    if isinstance(creds, S3Credentials):
        cred: dict[str, Any] = {
            "access_key_id": creds.aws_access_key_id,
            "secret_access_key": creds.aws_secret_access_key,
            "expires_at": _as_aware(creds.expiration),
        }
        if creds.aws_session_token:
            cred["token"] = creds.aws_session_token
        return cred
    if isinstance(creds, GSCredentials):
        return {"token": creds.access_token, "expires_at": _as_aware(creds.expiration)}
    raise NotImplementedError(f"obstore credential refresh not supported for {type(creds).__name__}")


def _credentials_still_valid(creds: TempCredentials | None, buffer_seconds: int = 60) -> bool:
    expiration = _as_aware(getattr(creds, "expiration", None))
    if expiration is None:
        return False
    return expiration > datetime.now(UTC) + timedelta(seconds=buffer_seconds)


class _BucketCredentialRefresher:
    """Credential provider handed to obstore for buckets with refreshable (delegated) auth.

    obstore caches the returned credential until ``expires_at`` and only calls back to refresh
    once it lapses, so long-running operations (e.g. listing or uploading to a very large
    bucket) no longer fail partway through with an expired token. The credentials already
    vended when the store was built are returned on the first call to avoid a redundant fetch.

    obstore calls this from its own worker thread, so the async fetch is driven on the
    client's background event loop via ``asyncio_run`` — the same approach the Icechunk
    credential refresh functions use.
    """

    def __init__(
        self,
        aclient: AsyncClient,
        org: OrgName,
        nickname: BucketNickname,
        platform: Platform,
        access: Literal["read", "write"],
        initial_creds: TempCredentials | None,
    ) -> None:
        self._aclient = aclient
        self._org = org
        self._nickname = nickname
        self._platform = platform
        self._access = access
        self._initial_creds = initial_creds
        self._used_initial = False

    def __call__(self) -> dict[str, Any]:
        if not self._used_initial:
            self._used_initial = True
            if self._initial_creds is not None and _credentials_still_valid(self._initial_creds):
                return _to_obstore_credential(self._initial_creds)
        if self._platform == "s3":
            coro: Coroutine[Any, Any, TempCredentials] = self._aclient._get_s3_delegated_credentials_from_bucket(
                self._org, self._nickname, access=self._access
            )
        elif self._platform == "gs":
            coro = self._aclient._get_gcs_delegated_credentials_from_bucket(self._org, self._nickname, access=self._access)
        else:
            raise NotImplementedError(f"obstore credential refresh not supported for platform {self._platform!r}")
        return _to_obstore_credential(asyncio_run(coro, timeout=None))


def maybe_get_credential_provider(
    aclient: AsyncClient,
    bucket: BucketResponse,
    org: OrgName,
    access: Literal["read", "write"],
    initial_creds: TempCredentials | None,
) -> Callable[[], dict[str, Any]] | None:
    """Build an obstore credential provider that re-vends before the token expires.

    Returns None for buckets whose credentials are not refreshable (HMAC, anonymous,
    bucket-policy) and for Azure, where obstore has no credential provider hook. In
    those cases callers fall back to obstore's static credential config.
    """
    if not _use_delegated_credentials(bucket):
        return None
    platform = aclient._delegated_credential_platform(bucket)
    if platform not in ("s3", "gs"):
        return None
    return _BucketCredentialRefresher(
        aclient=aclient,
        org=org,
        nickname=bucket.nickname,
        platform=platform,
        access=access,
        initial_creds=initial_creds,
    )
