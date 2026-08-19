# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for worker-side re-vending of expiring storage credentials.

The driver vends temporary (STS) credentials once at plan time and ships them
into every ScanTask / checkpoint store. Long-running backfills outlive the
token, so workers must re-vend before ``expires_at_millis`` rather than sign S3
requests with an expired token (400/403 mid-job).
"""

from __future__ import annotations

from types import SimpleNamespace

from geneva.credentials import (
    CREDENTIAL_REFRESH_SAFETY_MS,
    VENDED_EXPIRY_KEY,
    refresh_storage_options,
    storage_options_need_refresh,
)

_NOW_MS = 1_000_000_000_000


def _opts(expires_ms: int | None, **extra: str) -> dict[str, str]:
    opts = {"aws_access_key_id": "AKIA", "aws_secret_access_key": "s", **extra}
    if expires_ms is not None:
        opts[VENDED_EXPIRY_KEY] = str(expires_ms)
    return opts


class _FakeNamespace:
    """Minimal namespace client returning a fixed vended storage_options."""

    def __init__(self, vended: dict[str, str] | None, *, raises: bool = False) -> None:
        self._vended = vended
        self._raises = raises
        self.calls: list[list[str]] = []

    def describe_table(self, request) -> SimpleNamespace:  # noqa: ANN001
        self.calls.append(list(request.id))
        if self._raises:
            raise RuntimeError("namespace unavailable")
        return SimpleNamespace(storage_options=self._vended)


def test_need_refresh_static_and_missing_expiry() -> None:
    assert storage_options_need_refresh(None) is False
    assert storage_options_need_refresh({}) is False
    # Static credentials never carry an expiry -> never refreshed.
    assert storage_options_need_refresh(_opts(None)) is False
    # Unparseable expiry is treated as "no expiry" (fail safe, not fail hard).
    assert storage_options_need_refresh({VENDED_EXPIRY_KEY: "not-an-int"}) is False


def test_need_refresh_expiry_window() -> None:
    far = _opts(_NOW_MS + 3600_000)  # ~1h out
    assert storage_options_need_refresh(far, now_ms=_NOW_MS) is False

    within = _opts(_NOW_MS + CREDENTIAL_REFRESH_SAFETY_MS - 1)
    assert storage_options_need_refresh(within, now_ms=_NOW_MS) is True

    expired = _opts(_NOW_MS - 1)
    assert storage_options_need_refresh(expired, now_ms=_NOW_MS) is True


def test_refresh_noop_for_static_options() -> None:
    static = _opts(None)
    ns = _FakeNamespace(_opts(_NOW_MS + 3600_000))
    out = refresh_storage_options(static, table_id=["t"], namespace_client=ns)
    # Same object returned, and the namespace was never consulted.
    assert out is static
    assert ns.calls == []


def test_refresh_revends_when_expiring() -> None:
    expiring = _opts(_NOW_MS - 1)
    fresh = _opts(_NOW_MS + 3600_000, aws_session_token="new-token")
    ns = _FakeNamespace(fresh)
    out = refresh_storage_options(expiring, table_id=["db", "tbl"], namespace_client=ns)
    assert out is fresh
    assert ns.calls == [["db", "tbl"]]


def test_refresh_falls_back_when_vend_fails() -> None:
    expiring = _opts(_NOW_MS - 1)
    ns = _FakeNamespace(None, raises=True)
    out = refresh_storage_options(expiring, table_id=["t"], namespace_client=ns)
    # A namespace hiccup must not abort the read; keep the existing options.
    assert out is expiring


def test_refresh_falls_back_without_namespace() -> None:
    expiring = _opts(_NOW_MS - 1)
    out = refresh_storage_options(expiring, table_id=None)
    assert out is expiring


def test_multibase_rebuilds_base_stores_on_expiry() -> None:
    """Base stores can't self-refresh (no namespace context), so the wrapper
    re-vends via the default store and rebuilds them with fresh credentials."""
    from geneva.checkpoint import FlatLanceCheckpointStore, MultiBaseCheckpointStore

    fresh = _opts(_NOW_MS + 3_600_000, aws_session_token="new-token")
    ns = _FakeNamespace(fresh)
    default_store = FlatLanceCheckpointStore(
        "memory://default",
        namespace_client=ns,
        table_id=["db", "tbl"],
        storage_options=_opts(_NOW_MS + 3_600_000),
    )
    store = MultiBaseCheckpointStore(
        default_store,
        base_checkpoint_uris={0: "s3://base-0/_ckp"},
        frag_to_base={5: 0},
        base_storage_options=_opts(_NOW_MS - 1),  # already expired
    )
    before = store.base_stores[0]

    # Any routed access triggers the refresh + rebuild.
    store.store_for_frag(5)

    after = store.base_stores[0]
    assert store.base_storage_options is fresh
    assert after is not before
    assert after.storage_options is fresh
    assert ns.calls == [["db", "tbl"]]


def test_env_override_safety_window(monkeypatch) -> None:  # noqa: ANN001
    from geneva.credentials import (
        CREDENTIAL_REFRESH_SAFETY_MS,
        CREDENTIAL_REFRESH_SAFETY_MS_ENV,
    )
    from geneva.credentials import (
        credential_refresh_safety_ms as _credential_refresh_safety_ms,
    )

    monkeypatch.delenv(CREDENTIAL_REFRESH_SAFETY_MS_ENV, raising=False)
    assert _credential_refresh_safety_ms() == CREDENTIAL_REFRESH_SAFETY_MS

    # A window wider than the token TTL makes even far-future creds look
    # "expiring", so every open re-vends — how the integ test forces re-vending
    # without waiting out a real ~15 min AWS STS lifetime.
    monkeypatch.setenv(CREDENTIAL_REFRESH_SAFETY_MS_ENV, str(365 * 24 * 3600 * 1000))
    far = _opts(_NOW_MS + 3_600_000)  # 1h out
    assert storage_options_need_refresh(far, now_ms=_NOW_MS) is True

    # Garbage falls back to the default rather than crashing the read path.
    monkeypatch.setenv(CREDENTIAL_REFRESH_SAFETY_MS_ENV, "not-a-number")
    assert _credential_refresh_safety_ms() == CREDENTIAL_REFRESH_SAFETY_MS


def test_is_credential_expiry_error() -> None:
    from geneva.credentials import (
        is_credential_expiry_error as _is_credential_expiry_error,
    )

    def err(m: str) -> RuntimeError:
        return RuntimeError(m)

    assert _is_credential_expiry_error(
        err("lance error: Generic S3 error: HEAD ... 400 Bad Request")
    )
    assert _is_credential_expiry_error(err("Generic S3 error: 403 Forbidden"))
    assert _is_credential_expiry_error(err("S3 error: The provided token has expired"))
    # An S3 error without an auth signature is not credential expiry.
    assert not _is_credential_expiry_error(err("Generic S3 error: 500 Internal Error"))
    # Non-S3 errors are never treated as credential expiry.
    assert not _is_credential_expiry_error(err("some unrelated RuntimeError"))


def test_retry_lance_revends_on_credential_error(monkeypatch) -> None:  # noqa: ANN001
    import geneva.utils as gu

    # No backoff so the test is fast.
    monkeypatch.setattr(gu, "RETRY_LANCE_INITIAL_SECS", 0.0)
    monkeypatch.setattr(gu, "RETRY_LANCE_MAX_SECS", 0.0)

    class _Flaky:
        def __init__(self) -> None:
            self.attempts = 0
            self.refreshed = 0

        def _refresh_credentials_on_error(self) -> None:
            self.refreshed += 1

        @gu.retry_lance
        def op(self) -> str:
            self.attempts += 1
            # Fail with an expired-credential S3 error until creds are refreshed.
            if self.refreshed == 0:
                raise RuntimeError(
                    "lance error: LanceError(IO): Generic S3 error: "
                    "Error performing HEAD ... 400 Bad Request"
                )
            return "ok"

    obj = _Flaky()
    assert obj.op() == "ok"
    assert obj.refreshed >= 1  # the retry re-vended before succeeding
    assert obj.attempts >= 2


def test_list_keys_retries_and_revends_on_credential_error(monkeypatch) -> None:  # noqa: ANN001
    """A @retry_lance-decorated *generator* runs its LIST I/O lazily on the
    caller's first ``next()`` -- outside retry_lance's try/except -- so retries
    and the credential-refresh hook never fire. The helper refactor moves the
    I/O into a retried, non-generator ``_list_keys`` so both actually happen."""
    import geneva.checkpoint as ckpt
    import geneva.utils as gu

    monkeypatch.setattr(gu, "RETRY_LANCE_INITIAL_SECS", 0.0)
    monkeypatch.setattr(gu, "RETRY_LANCE_MAX_SECS", 0.0)
    # Stub the session so no real LanceFileSession is built (and so the
    # post-refresh session reset doesn't try to reconnect).
    monkeypatch.setattr(
        ckpt.FlatLanceCheckpointStore,
        "session",
        property(lambda self: "fake-session"),
    )

    fresh = _opts(_NOW_MS + 3_600_000, aws_session_token="new-token")
    ns = _FakeNamespace(fresh)
    store = ckpt.FlatLanceCheckpointStore(
        "memory://x",
        namespace_client=ns,
        table_id=["db", "tbl"],
        storage_options=_opts(_NOW_MS - 1),
    )

    calls = {"n": 0}

    def fake_timed_list(session, prefix, **kwargs) -> list[str]:  # noqa: ANN001, ANN003
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError(
                "lance error: LanceError(IO): Generic S3 error: "
                "Error performing HEAD ... 403 Forbidden"
            )
        return ["k1.lance", "k2.lance", "other.txt"]

    monkeypatch.setattr(ckpt, "timed_list", fake_timed_list)

    keys = list(store.list_keys())

    assert keys == ["k1", "k2"]
    assert calls["n"] >= 2  # the credential error triggered a retry
    assert ns.calls == [["db", "tbl"]]  # re-vended before the retry
    assert store.storage_options is fresh


def test_multibase_base_store_reactive_refresh_revends_via_delegate() -> None:
    """A multi-base child store carries no namespace context of its own, so its
    reactive ``_refresh_credentials_on_error`` must re-vend through the default
    store (the delegate) instead of being a silent no-op."""
    from geneva.checkpoint import FlatLanceCheckpointStore, MultiBaseCheckpointStore

    fresh = _opts(_NOW_MS + 3_600_000, aws_session_token="new-token")
    ns = _FakeNamespace(fresh)
    default_store = FlatLanceCheckpointStore(
        "memory://default",
        namespace_client=ns,
        table_id=["db", "tbl"],
        storage_options=_opts(_NOW_MS + 3_600_000),
    )
    store = MultiBaseCheckpointStore(
        default_store,
        base_checkpoint_uris={0: "s3://base-0/_ckp"},
        frag_to_base={5: 0},
        base_storage_options=_opts(_NOW_MS + 3_600_000),  # not proactively expiring
    )
    base = store.base_stores[0]

    # The base store has no namespace/table context of its own...
    assert base._resolve_namespace_client() is None
    assert base.table_id is None
    # ...but its reactive refresh re-vends through the default store.
    base._refresh_credentials_on_error()

    assert base.storage_options is fresh
    assert ns.calls == [["db", "tbl"]]


def test_multibase_static_creds_are_noop() -> None:
    from geneva.checkpoint import FlatLanceCheckpointStore, MultiBaseCheckpointStore

    ns = _FakeNamespace(_opts(_NOW_MS + 3_600_000))
    default_store = FlatLanceCheckpointStore(
        "memory://default", namespace_client=ns, table_id=["db", "tbl"]
    )
    store = MultiBaseCheckpointStore(
        default_store,
        base_checkpoint_uris={0: "s3://base-0/_ckp"},
        frag_to_base={5: 0},
        base_storage_options=_opts(None),  # static, no expiry
    )
    before = store.base_stores[0]
    store.store_for_frag(5)
    # No re-vend, base stores left untouched.
    assert store.base_stores[0] is before
    assert ns.calls == []
