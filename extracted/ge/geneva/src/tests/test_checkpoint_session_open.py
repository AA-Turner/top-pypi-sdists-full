# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Session-open resilience for the Lance checkpoint store: the direct
physical-URI fallback and the bounded not-found retry on
``FlatLanceCheckpointStore``."""

import logging
import pickle
import threading
import time

import pytest
from lance_namespace.errors import TableNotFoundError

import geneva.checkpoint as checkpoint_mod
from geneva.checkpoint import FlatLanceCheckpointStore, HierarchicalLanceCheckpointStore
from geneva.utils.object_store_retry import is_retryable_object_store_error

_ATTEMPTS = FlatLanceCheckpointStore._SESSION_OPEN_ATTEMPTS


def _dir_store(**overrides) -> FlatLanceCheckpointStore:
    kwargs = {
        "root": "az://bucket/mytable.lance/_ckp",
        "namespace_client_impl": "dir",
        "namespace_client_properties": {
            "root": "az://bucket",
            "manifest_enabled": "true",
        },
        "table_id": ["mytable"],
        "storage_options": {"account": "acct"},
    }
    kwargs.update(overrides)
    return FlatLanceCheckpointStore(**kwargs)


class _FakeDataset:
    """Stand-in dataset whose file session is an identifiable sentinel."""

    def __init__(self, tag: str) -> None:
        self.tag = tag

    def new_file_session(self) -> str:
        return f"session:{self.tag}"


# --- _direct_session_uri eligibility -----------------------------------------


def test_direct_uri_dir_plain() -> None:
    assert _dir_store()._direct_session_uri() == "az://bucket/mytable.lance"


def test_direct_uri_rest_returns_none() -> None:
    store = _dir_store(
        namespace_client_impl="rest",
        namespace_client_properties={"uri": "http://ns:8080"},
    )
    assert store._direct_session_uri() is None


@pytest.mark.parametrize(
    "props",
    [
        {"root": "az://bucket", "vend_input_storage_options": "true"},
        {"root": "az://bucket", "credential_vendor.impl": "phalanx"},
    ],
)
def test_direct_uri_vendor_returns_none(props: dict) -> None:
    assert _dir_store(namespace_client_properties=props)._direct_session_uri() is None


def test_direct_uri_missing_root_returns_none() -> None:
    store = _dir_store(namespace_client_properties={"manifest_enabled": "true"})
    assert store._direct_session_uri() is None


def test_direct_uri_nested_table_id_returns_none() -> None:
    # Nested tables live at a manifest-hashed path, not <root>/<leaf>.lance.
    store = _dir_store(table_id=["sub", "mytable"])
    assert store._direct_session_uri() is None


def test_nested_table_id_no_direct_fallback(monkeypatch) -> None:  # noqa: ANN001
    """Multi-element table_id -> the physical-URI fallback is skipped entirely;
    a wrong/colliding direct open would silently cross checkpoints."""
    store = _dir_store(table_id=["sub", "mytable"])

    def fake_open(**kwargs) -> None:
        raise TableNotFoundError("Table not found: table id 'sub.mytable'")

    def fail_direct(uri, **kwargs) -> None:  # noqa: ANN001
        raise AssertionError("direct fallback must not run for nested table_id")

    monkeypatch.setattr("geneva.db.open_lance_dataset", fake_open)
    monkeypatch.setattr(checkpoint_mod.lance, "dataset", fail_direct)
    monkeypatch.setattr(checkpoint_mod.time, "sleep", lambda s: None)

    with pytest.raises(TableNotFoundError):
        store._open_session_dataset(ns_client=object())


# --- _open_session_dataset (fallback + bounded retry) ------------------------


def test_falls_back_to_direct_uri(monkeypatch, caplog) -> None:  # noqa: ANN001
    """(a) namespace not-found but the physical-URI open succeeds -> recovered,
    warning logged."""
    store = _dir_store()
    ns_calls = {"n": 0}
    direct_calls = []

    def fake_open(**kwargs) -> _FakeDataset:
        ns_calls["n"] += 1
        raise TableNotFoundError("Table not found: table id 'mytable'")

    def fake_dataset(uri, **kwargs) -> _FakeDataset:  # noqa: ANN001
        direct_calls.append(uri)
        return _FakeDataset("direct")

    monkeypatch.setattr("geneva.db.open_lance_dataset", fake_open)
    monkeypatch.setattr(checkpoint_mod.lance, "dataset", fake_dataset)
    caplog.set_level(logging.WARNING)

    ds = store._open_session_dataset(ns_client=object())

    assert isinstance(ds, _FakeDataset)
    assert ds.tag == "direct"
    assert ns_calls["n"] == 1
    assert direct_calls == ["az://bucket/mytable.lance"]
    assert any("direct physical URI" in r.getMessage() for r in caplog.records)


def test_both_fail_retries_then_raises_original(monkeypatch) -> None:  # noqa: ANN001
    """(b) namespace and direct both fail -> the original not-found propagates
    after the bounded number of attempts, with the direct-open failure chained
    as its cause so retry classifiers see the throttle evidence."""
    store = _dir_store()
    ns_calls = {"n": 0}
    sleep_calls = []

    def fake_open(**kwargs) -> None:
        ns_calls["n"] += 1
        raise TableNotFoundError("Table not found: table id 'mytable'")

    def fake_dataset(uri, **kwargs) -> None:  # noqa: ANN001
        raise ValueError("LanceError(IO): ... 503 Service Unavailable ServerBusy")

    monkeypatch.setattr("geneva.db.open_lance_dataset", fake_open)
    monkeypatch.setattr(checkpoint_mod.lance, "dataset", fake_dataset)
    monkeypatch.setattr(checkpoint_mod.time, "sleep", lambda s: sleep_calls.append(s))

    with pytest.raises(TableNotFoundError) as excinfo:
        store._open_session_dataset(ns_client=object())

    assert ns_calls["n"] == _ATTEMPTS
    assert len(sleep_calls) == _ATTEMPTS - 1
    cause = excinfo.value.__cause__
    assert isinstance(cause, ValueError)
    assert "503" in str(cause)
    # The chained evidence is what flips the applier predicate to retryable.
    assert is_retryable_object_store_error(excinfo.value) is True


def test_both_fail_genuine_miss_stays_non_retryable(monkeypatch) -> None:  # noqa: ANN001
    """Direct open failing with a genuine not-found chains no throttle
    evidence -> the propagated error stays non-retryable."""
    store = _dir_store()

    def fake_open(**kwargs) -> None:
        raise TableNotFoundError("Table not found: table id 'mytable'")

    def fake_dataset(uri, **kwargs) -> None:  # noqa: ANN001
        raise ValueError("Dataset at path mytable.lance was not found")

    monkeypatch.setattr("geneva.db.open_lance_dataset", fake_open)
    monkeypatch.setattr(checkpoint_mod.lance, "dataset", fake_dataset)
    monkeypatch.setattr(checkpoint_mod.time, "sleep", lambda s: None)

    with pytest.raises(TableNotFoundError) as excinfo:
        store._open_session_dataset(ns_client=object())

    assert isinstance(excinfo.value.__cause__, ValueError)
    assert is_retryable_object_store_error(excinfo.value) is False


def test_rest_impl_no_direct_fallback(monkeypatch) -> None:  # noqa: ANN001
    """(c) REST/non-dir impl -> the physical-URI fallback is never attempted,
    but the bounded not-found retry still applies."""
    store = _dir_store(
        namespace_client_impl="rest",
        namespace_client_properties={"uri": "http://ns:8080"},
    )
    ns_calls = {"n": 0}

    def fake_open(**kwargs) -> None:
        ns_calls["n"] += 1
        raise TableNotFoundError("Table not found: table id 'mytable'")

    def fail_direct(uri, **kwargs) -> None:  # noqa: ANN001
        raise AssertionError("direct fallback must not run for REST namespaces")

    monkeypatch.setattr("geneva.db.open_lance_dataset", fake_open)
    monkeypatch.setattr(checkpoint_mod.lance, "dataset", fail_direct)
    monkeypatch.setattr(checkpoint_mod.time, "sleep", lambda s: None)

    with pytest.raises(TableNotFoundError) as excinfo:
        store._open_session_dataset(ns_client=object())

    assert ns_calls["n"] == _ATTEMPTS
    # No direct attempt -> nothing chained.
    assert excinfo.value.__cause__ is None


def test_vendor_config_no_direct_fallback(monkeypatch) -> None:  # noqa: ANN001
    """(d) credential-vendor config -> no direct fallback (it would bypass the
    vended, table-scoped credentials)."""
    store = _dir_store(
        namespace_client_properties={
            "root": "az://bucket",
            "vend_input_storage_options": "true",
        }
    )

    def fake_open(**kwargs) -> None:
        raise TableNotFoundError("Table not found: table id 'mytable'")

    def fail_direct(uri, **kwargs) -> None:  # noqa: ANN001
        raise AssertionError("direct fallback must not run when vending creds")

    monkeypatch.setattr("geneva.db.open_lance_dataset", fake_open)
    monkeypatch.setattr(checkpoint_mod.lance, "dataset", fail_direct)
    monkeypatch.setattr(checkpoint_mod.time, "sleep", lambda s: None)

    with pytest.raises(TableNotFoundError):
        store._open_session_dataset(ns_client=object())


def test_non_not_found_error_propagates_without_retry(monkeypatch) -> None:  # noqa: ANN001
    """A non-not-found failure with no direct fallback propagates immediately;
    the bounded retry is scoped to not-found only."""
    store = _dir_store(
        namespace_client_impl="rest",
        namespace_client_properties={"uri": "http://ns:8080"},
    )
    ns_calls = {"n": 0}
    sleep_calls = []

    def fake_open(**kwargs) -> None:
        ns_calls["n"] += 1
        raise PermissionError("credentials rejected")

    monkeypatch.setattr("geneva.db.open_lance_dataset", fake_open)
    monkeypatch.setattr(checkpoint_mod.time, "sleep", lambda s: sleep_calls.append(s))

    with pytest.raises(PermissionError):
        store._open_session_dataset(ns_client=object())

    assert ns_calls["n"] == 1
    assert sleep_calls == []


# --- session property wiring -------------------------------------------------


def test_session_property_namespace_success(monkeypatch) -> None:  # noqa: ANN001
    store = _dir_store()
    monkeypatch.setattr(store, "_maybe_refresh_storage_options", lambda: None)
    monkeypatch.setattr(store, "_resolve_namespace_client", lambda: object())
    monkeypatch.setattr("geneva.db.open_lance_dataset", lambda **kw: _FakeDataset("ns"))

    assert store.session == "session:ns"


def test_session_property_direct_fallback(monkeypatch) -> None:  # noqa: ANN001
    store = _dir_store()
    monkeypatch.setattr(store, "_maybe_refresh_storage_options", lambda: None)
    monkeypatch.setattr(store, "_resolve_namespace_client", lambda: object())

    def fake_open(**kwargs) -> None:
        raise TableNotFoundError("Table not found: table id 'mytable'")

    monkeypatch.setattr("geneva.db.open_lance_dataset", fake_open)
    monkeypatch.setattr(
        checkpoint_mod.lance, "dataset", lambda uri, **kw: _FakeDataset("direct")
    )

    assert store.session == "session:direct"


# --- concurrency + pickle ----------------------------------------------------


def test_concurrent_first_access_opens_once(monkeypatch) -> None:  # noqa: ANN001
    """Concurrent cold-session access coalesces to exactly one open.

    The stubbed open sleeps to release the GIL, so all racers clear the
    None-check before the first finishes; without the double-checked lock each
    would open independently. (This assertion fails on the pre-lock code.)
    """
    store = _dir_store()
    monkeypatch.setattr(store, "_maybe_refresh_storage_options", lambda: None)
    monkeypatch.setattr(store, "_resolve_namespace_client", lambda: object())

    open_calls = {"n": 0}
    count_lock = threading.Lock()
    n_threads = 16
    entry = threading.Barrier(n_threads)

    def fake_open(**kwargs) -> _FakeDataset:
        with count_lock:  # += is non-atomic once the open genuinely races
            open_calls["n"] += 1
        time.sleep(0.02)  # release the GIL to widen the check-then-set window
        return _FakeDataset("ns")

    monkeypatch.setattr("geneva.db.open_lance_dataset", fake_open)

    results: list = []

    def worker() -> None:
        entry.wait()  # release all threads into .session at once
        results.append(store.session)

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert open_calls["n"] == 1
    assert results == ["session:ns"] * n_threads


@pytest.mark.parametrize(
    "store_cls", [FlatLanceCheckpointStore, HierarchicalLanceCheckpointStore]
)
def test_session_lock_recreated_after_unpickle(store_cls) -> None:  # noqa: ANN001
    # The lock is excluded from the __getstate__ whitelist and recreated in
    # __setstate__, so an unpickled store has a fresh, usable lock. Both layouts
    # go through the base __setstate__ (Hierarchical delegates via super()).
    store = store_cls(
        root="az://bucket/mytable.lance/_ckp",
        namespace_client_impl="dir",
        namespace_client_properties={"root": "az://bucket", "manifest_enabled": "true"},
        table_id=["mytable"],
        storage_options={"account": "acct"},
    )
    restored = pickle.loads(pickle.dumps(store))
    assert restored._session_lock is not None
    with restored._session_lock:
        pass
