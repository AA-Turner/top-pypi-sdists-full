from __future__ import annotations

import asyncio
import threading
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from arraylake import AsyncClient, _credential_cache
from arraylake._credential_cache import (
    CLOCK_SKEW_SAFETY,
    CredentialCacheKey,
    clear,
    get_or_refresh,
    populate,
)
from arraylake.asyn import asyncio_run
from arraylake.types import BucketResponse, GSCredentials, S3Credentials, VirtualChunkCredentials


def _key(identifier: str = "repo-a", auth_key: int = 1) -> CredentialCacheKey:
    return CredentialCacheKey(
        api_url="https://api.test",
        auth_key=auth_key,
        scope="repo",
        org="org-a",
        identifier=identifier,
        platform="s3",
    )


def _creds(remaining: timedelta | None = timedelta(hours=1)) -> S3Credentials:
    return S3Credentials(
        aws_access_key_id="AKIA",
        aws_secret_access_key="secret",
        aws_session_token="token",
        expiration=datetime.now(UTC) + remaining if remaining is not None else None,
    )


def test_validity_boundary():
    """Cache freshness follows expires_at - CLOCK_SKEW_SAFETY. Each case runs
    two back-to-back lookups; count is 1 (cache hit) or 2 (refetched)."""
    cases = [
        ("hour-lifetime", timedelta(hours=1), 1),
        ("hard-expired", timedelta(seconds=-5), 2),
        ("inside-clock-skew", CLOCK_SKEW_SAFETY // 2, 2),
        ("just-past-clock-skew", CLOCK_SKEW_SAFETY + timedelta(seconds=10), 1),
        ("none-never-cached", None, 2),
    ]
    for name, remaining, expected in cases:
        clear()
        calls = 0

        async def fetch(_remaining=remaining) -> S3Credentials:
            nonlocal calls
            calls += 1
            return _creds(remaining=_remaining)

        async def body() -> None:
            await get_or_refresh(_key(), fetch)
            await get_or_refresh(_key(), fetch)

        asyncio_run(body())
        assert calls == expected, f"case {name}: expected {expected} fetches, got {calls}"


def test_keys_isolate_entries():
    """Two distinct cache keys hold independent entries."""
    cases = [
        ("different-identifier", _key("repo-a"), _key("repo-b")),
        ("different-auth-key", _key(auth_key=1), _key(auth_key=2)),
    ]
    for name, key_a, key_b in cases:
        clear()
        calls = 0

        async def fetch() -> S3Credentials:
            nonlocal calls
            calls += 1
            return _creds()

        async def body() -> None:
            await get_or_refresh(key_a, fetch)
            await get_or_refresh(key_b, fetch)

        asyncio_run(body())
        assert calls == 2, f"case {name}: expected 2 fetches, got {calls}"


def test_async_single_flight():
    started = asyncio.Event()
    release = asyncio.Event()
    calls = 0

    async def fetch() -> S3Credentials:
        nonlocal calls
        calls += 1
        started.set()
        await release.wait()
        return _creds()

    async def body() -> None:
        tasks = [asyncio.create_task(get_or_refresh(_key(), fetch)) for _ in range(50)]
        await started.wait()
        release.set()
        results = await asyncio.gather(*tasks)
        for r in results:
            assert results[0] is r

    asyncio_run(body())
    assert calls == 1


def test_cross_thread_single_flight():
    release = threading.Event()
    fetch_thread_arrived = threading.Event()
    calls = 0

    async def fetch() -> S3Credentials:
        nonlocal calls
        calls += 1
        fetch_thread_arrived.set()
        await asyncio.get_running_loop().run_in_executor(None, release.wait)
        return _creds()

    def worker() -> None:
        asyncio_run(get_or_refresh(_key(), fetch))

    threads = [threading.Thread(target=worker) for _ in range(30)]
    for t in threads:
        t.start()
    assert fetch_thread_arrived.wait(timeout=5), "fetcher never started"
    release.set()
    for t in threads:
        t.join(timeout=10)
    assert calls == 1


def test_works_from_foreign_loop():
    """Regression: previously get_or_refresh asserted that the caller was
    running on the arraylake background loop, breaking any user who awaited
    AsyncClient methods from their own asyncio loop. Calling from a fresh
    foreign loop must complete normally."""

    async def fetch() -> S3Credentials:
        return _creds()

    foreign_loop = asyncio.new_event_loop()
    try:
        creds = foreign_loop.run_until_complete(get_or_refresh(_key(), fetch))
    finally:
        foreign_loop.close()
    assert creds.aws_access_key_id == "AKIA"


def test_fetcher_exception_does_not_poison_cache():
    attempts = 0

    async def flaky() -> S3Credentials:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise RuntimeError("transient")
        return _creds()

    async def body() -> None:
        with pytest.raises(RuntimeError):
            await get_or_refresh(_key(), flaky)
        creds = await get_or_refresh(_key(), flaky)
        assert creds.aws_access_key_id == "AKIA"

    asyncio_run(body())
    assert attempts == 2


def test_populate_serves_subsequent_lookup_without_fetch():
    calls = 0

    async def fetch() -> S3Credentials:
        nonlocal calls
        calls += 1
        return _creds()

    async def body() -> None:
        populate(_key(), _creds())
        creds = await get_or_refresh(_key(), fetch)
        assert creds.aws_access_key_id == "AKIA"

    asyncio_run(body())
    assert calls == 0


def test_populate_skips_expired_creds():
    populate(_key(), _creds(remaining=timedelta(seconds=-5)))
    calls = 0

    async def fetch() -> S3Credentials:
        nonlocal calls
        calls += 1
        return _creds()

    asyncio_run(get_or_refresh(_key(), fetch))
    assert calls == 1


def test_populate_does_not_clobber_fresher_entry():
    async def fetch() -> S3Credentials:
        return _creds(remaining=timedelta(hours=2))

    asyncio_run(get_or_refresh(_key(), fetch))
    populate(_key(), _creds(remaining=timedelta(seconds=45)))
    assert _credential_cache._CACHE[_key()].expires_at > datetime.now(UTC) + timedelta(hours=1)


def test_clear_drops_entries():
    calls = 0

    async def fetch() -> S3Credentials:
        nonlocal calls
        calls += 1
        return _creds()

    async def body() -> None:
        await get_or_refresh(_key(), fetch)
        assert _credential_cache._CACHE != {}
        clear()
        assert _credential_cache._CACHE == {}
        await get_or_refresh(_key(), fetch)

    asyncio_run(body())
    assert calls == 2


VCC_PREFIX_A = "s3://provider-bucket/a/"
VCC_PREFIX_B = "s3://provider-bucket/b/"


def _vcc(access_key: str, expiry: datetime) -> VirtualChunkCredentials:
    return VirtualChunkCredentials(
        credentials=S3Credentials(
            aws_access_key_id=access_key, aws_secret_access_key="secret", aws_session_token="token", expiration=expiry
        ),
        org="org-a",
        bucket_nickname="provider-bucket",
        platform="s3",
    )


def _open_response(expiry: datetime) -> SimpleNamespace:
    """A minimal stand-in for OpenRepoResponse with repo + two VCC credentials."""
    return SimpleNamespace(
        repo_bucket=BucketResponse(
            id=uuid4(), platform="s3", nickname="repo-bucket", name="repo-bucket", is_default=False, extra_config={}
        ),
        repo_credentials=_creds().model_copy(update={"aws_access_key_id": "REPOKEY", "expiration": expiry}),
        virtual_chunk_credentials={VCC_PREFIX_A: _vcc("AKEY", expiry), VCC_PREFIX_B: _vcc("BKEY", expiry)},
    )


def test_vcc_credentials_are_process_cached():
    """Two back-to-back refreshes of the same virtual chunk container hit /open once."""
    client = AsyncClient("https://test.example", token="ema_fake_token")
    expiry = datetime.now(UTC) + timedelta(hours=1)
    mstore = MagicMock()
    mstore.open_repo = AsyncMock(return_value=_open_response(expiry))

    with patch.object(AsyncClient, "_metastore_for_org", return_value=mstore):
        client._get_icechunk_s3_vcc_credentials_refresh_function("org-a", "repo-a", VCC_PREFIX_A, "s3")
        client._get_icechunk_s3_vcc_credentials_refresh_function("org-a", "repo-a", VCC_PREFIX_A, "s3")

    assert mstore.open_repo.await_count == 1


def test_single_open_refreshes_repo_and_all_vccs():
    """One /open seeds the repo bucket and every virtual chunk container, so refreshing the
    other VCC and the repo bucket afterwards is served from cache without another /open."""
    client = AsyncClient("https://test.example", token="ema_fake_token")
    expiry = datetime.now(UTC) + timedelta(hours=1)
    mstore = MagicMock()
    mstore.open_repo = AsyncMock(return_value=_open_response(expiry))

    with patch.object(AsyncClient, "_metastore_for_org", return_value=mstore):
        # First refresh of one VCC triggers the single /open.
        a = client._get_icechunk_s3_vcc_credentials_refresh_function("org-a", "repo-a", VCC_PREFIX_A, "s3")
        # The other VCC and the repo bucket are now served from the cache it seeded.
        b = client._get_icechunk_s3_vcc_credentials_refresh_function("org-a", "repo-a", VCC_PREFIX_B, "s3")
        repo = client._get_icechunk_s3_credentials_refresh_function_for_repo("org-a", "repo-a")

    assert mstore.open_repo.await_count == 1
    assert a.access_key_id == "AKEY"
    assert b.access_key_id == "BKEY"
    assert repo.access_key_id == "REPOKEY"


def test_delegated_credentials_are_process_cached():
    """Two back-to-back calls to the same delegated-credential fetcher must
    only hit the metastore once. This is the core guarantee for the
    pickled-icechunk-session-across-dask-workers scenario."""
    expiry = datetime.now(UTC) + timedelta(hours=1)
    s3_creds = S3Credentials(
        aws_access_key_id="AKIA",
        aws_secret_access_key="secret",
        aws_session_token="token",
        expiration=expiry,
    )
    gs_creds = GSCredentials(access_token="bearer", principal="sa@x", expiration=expiry)
    aclient = AsyncClient("https://test.example", token="ema_fake_token")
    aclient_no_cache = AsyncClient("https://test.example", token="ema_fake_token", cache_credentials=False)

    cases = [
        ("s3-repo", "s3", "repo", aclient, "_get_s3_delegated_credentials_from_repo", ("org-a", "repo-a"), 1),
        ("gs-repo", "gs", "repo", aclient, "_get_gcs_delegated_credentials_from_repo", ("org-a", "repo-a"), 1),
        ("s3-bucket", "s3", "bucket", aclient, "_get_s3_delegated_credentials_from_bucket", ("org-a", "bucket-a"), 1),
        ("gs-bucket", "gs", "bucket", aclient, "_get_gcs_delegated_credentials_from_bucket", ("org-a", "bucket-a"), 1),
        ("s3-repo-nocache", "s3", "repo", aclient_no_cache, "_get_s3_delegated_credentials_from_repo", ("org-a", "repo-a"), 2),
        ("gs-bucket-nocache", "gs", "bucket", aclient_no_cache, "_get_gcs_delegated_credentials_from_bucket", ("org-a", "bucket-a"), 2),
    ]
    for name, platform, scope, client, method_name, args, expected_calls in cases:
        clear()
        creds = s3_creds if platform == "s3" else gs_creds
        mstore = MagicMock()
        mstore.get_s3_bucket_credentials_from_repo = AsyncMock(return_value=creds)
        mstore.get_gs_bucket_credentials_from_repo = AsyncMock(return_value=creds)
        mstore.get_s3_bucket_credentials_from_bucket = AsyncMock(return_value=creds)
        mstore.get_gs_bucket_credentials_from_bucket = AsyncMock(return_value=creds)

        method = getattr(client, method_name)

        async def invoke(_method=method, _args=args) -> None:
            await _method(*_args)
            await _method(*_args)

        with (
            patch.object(AsyncClient, "_metastore_for_org", return_value=mstore),
            patch.object(AsyncClient, "_bucket_id_for_nickname", new=AsyncMock(return_value="bucket-uuid")),
        ):
            asyncio_run(invoke())

        mstore_method = f"get_{'gs' if platform == 'gs' else 's3'}_bucket_credentials_from_{scope}"
        assert getattr(mstore, mstore_method).await_count == expected_calls, (
            f"case {name}: expected {expected_calls} metastore call(s), got {getattr(mstore, mstore_method).await_count}"
        )
        if expected_calls == 1:
            assert _credential_cache._CACHE != {}, f"case {name}: expected cache to be populated"
        else:
            assert _credential_cache._CACHE == {}, f"case {name}: expected cache to remain empty"
