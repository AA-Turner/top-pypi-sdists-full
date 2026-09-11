"""Unit tests for the inline-family guard.

The inline transforms build their UDF internally on the DataFrame object, so our
factories never see them. On a version-mismatched engine they would fail late
with PYTHON_VERSION_MISMATCH at .show(); the guard turns that into a clear
message at call time.
"""

import pytest

# Connect specifically: its protos need grpcio, which Brazil does not build for
# every interpreter this package is tested against.
pytest.importorskip("pyspark.sql.connect.dataframe")

from pyspark.sql.connect.dataframe import DataFrame as ConnectDataFrame  # noqa: E402
from pyspark.sql.connect.group import GroupedData as ConnectGroupedData  # noqa: E402

from sagemaker_studio.utils.udf import inline_guard  # noqa: E402
from sagemaker_studio.utils.udf import runtime as rt  # noqa: E402
from sagemaker_studio.utils.udf.errors import UDFUnsupportedError  # noqa: E402


class _FakeClient:
    pass


class _FakeSession:
    def __init__(self):
        self._client = _FakeClient()
        self.version = "4.1.1"
        self.conf = type("C", (), {"get": staticmethod(lambda k, d=None: d)})()

    def range(self, n):
        raise RuntimeError("no probe expected")


def _dataframe(session):
    df = ConnectDataFrame.__new__(ConnectDataFrame)
    df._session = session
    return df


def _grouped_data(session):
    """A real Connect ``GroupedData``, built the way pyspark builds one.

    Deliberately NOT given a ``_session``: the real class does not have one (see
    ``pyspark/sql/connect/group.py``, which reaches the session through
    ``self._df._session`` in every place it needs it). A stand-in that carried a
    ``_session`` would hide exactly the bug these tests exist to pin down.
    """
    grouped = ConnectGroupedData.__new__(ConnectGroupedData)
    grouped._df = _dataframe(session)
    return grouped


def _present(owner, method_names):
    """The subset of ``method_names`` this pyspark actually defines on ``owner``.

    ``INLINE_ONLY_METHODS`` names the whole deferred-build family across the
    Spark versions this SDK talks to (3.5.x for Glue 5, 4.1.x for Glue 6);
    ``applyInArrow``, ``foreach`` and ``foreachPartition`` do not exist on the
    Connect classes in 3.5.6. The guard skips what is absent, so the tests
    parametrize over what is present rather than asserting a version-specific
    list.
    """
    return [name for name in method_names if hasattr(owner, name)]


_DATAFRAME_METHODS = _present(ConnectDataFrame, inline_guard.INLINE_ONLY_METHODS["DataFrame"])
_GROUPED_METHODS = _present(ConnectGroupedData, inline_guard.INLINE_ONLY_METHODS["GroupedData"])


@pytest.fixture(autouse=True)
def _clean():
    rt.clear_cache()
    inline_guard.uninstall_inline_guard()
    yield
    inline_guard.uninstall_inline_guard()
    rt.clear_cache()


def test_guard_covers_the_documented_inline_family():
    # Assert the INTENDED family, not the module constant against itself: these
    # are the deferred-build entry points the design commits to guarding.
    assert inline_guard.INLINE_ONLY_METHODS["DataFrame"] == (
        "mapInPandas",
        "mapInArrow",
        "foreach",
        "foreachPartition",
    )
    assert inline_guard.INLINE_ONLY_METHODS["GroupedData"] == (
        "applyInPandas",
        "applyInArrow",
        "applyInPandasWithState",
    )


def test_install_wraps_every_family_method_present_on_this_pyspark():
    session = _FakeSession()
    rt.register_session(session)
    inline_guard.install_inline_guard(session)

    for owner, names in (
        (ConnectDataFrame, _DATAFRAME_METHODS),
        (ConnectGroupedData, _GROUPED_METHODS),
    ):
        for name in names:
            assert getattr(
                getattr(owner, name), "_smus_inline_guard", False
            ), f"{owner.__name__}.{name} was not wrapped"
    # Both sides must contribute something, or a silently-empty side would let
    # this pass while covering nothing.
    assert _DATAFRAME_METHODS and _GROUPED_METHODS


def test_a_real_connect_grouped_data_has_no_session_attribute():
    """Pins the reason the guard must not read ``self._session`` alone.

    Connect's ``GroupedData`` holds ``_df``, not ``_session``. Reading
    ``self._session`` raised ``AttributeError``, which a bare
    ``except Exception`` swallowed, so every grouped entry point delegated to
    upstream and failed late on the worker with a raw PYTHON_VERSION_MISMATCH.
    """
    grouped = _grouped_data(_FakeSession())
    with pytest.raises(AttributeError):
        grouped._session
    assert inline_guard._client_for(grouped) is grouped._df._session._client


@pytest.mark.parametrize("method_name", _GROUPED_METHODS)
def test_mismatched_engine_raises_for_every_grouped_entry_point(method_name):
    session = _FakeSession()
    rt.register_session(session)
    rt.set_override(session, "3.13")
    inline_guard.install_inline_guard(session)

    grouped = _grouped_data(session)
    with pytest.raises(UDFUnsupportedError) as excinfo:
        getattr(grouped, method_name)(lambda *a: a, "id long")
    message = str(excinfo.value)
    assert method_name in message
    assert "3.13" in message
    assert "udf" in message  # points at the supported alternative


def test_matched_engine_delegates_for_grouped_data_too(monkeypatch):
    session = _FakeSession()
    rt.register_session(session)
    rt.set_override(session, rt.client_python_version())
    calls = []
    monkeypatch.setattr(
        ConnectGroupedData,
        "applyInPandas",
        lambda self, *a, **k: calls.append(a) or "delegated",
    )
    inline_guard.install_inline_guard(session)

    grouped = _grouped_data(session)
    assert grouped.applyInPandas(lambda *a: a, "id long") == "delegated"
    assert calls

    # Uninstall HERE, not via the autouse fixture -- see the DataFrame case below
    # for why ordering against monkeypatch's undo matters.
    inline_guard.uninstall_inline_guard()


@pytest.mark.parametrize("method_name", _DATAFRAME_METHODS)
def test_mismatched_engine_raises_for_every_dataframe_entry_point(method_name):
    session = _FakeSession()
    rt.register_session(session)
    rt.set_override(session, "3.13")
    inline_guard.install_inline_guard(session)

    df = _dataframe(session)
    with pytest.raises(UDFUnsupportedError) as excinfo:
        getattr(df, method_name)(lambda it: it, "id long")
    message = str(excinfo.value)
    assert method_name in message
    assert "3.13" in message
    assert "udf" in message  # points at the supported alternative


def test_an_object_with_no_resolvable_session_delegates_instead_of_raising(monkeypatch):
    """A guarded method called on something with neither ``_session`` nor ``_df``
    must delegate, not blow up in the guard's own plumbing."""
    session = _FakeSession()
    rt.register_session(session)
    rt.set_override(session, "3.13")
    calls = []
    monkeypatch.setattr(
        ConnectDataFrame, "mapInPandas", lambda self, *a, **k: calls.append(a) or "delegated"
    )
    inline_guard.install_inline_guard(session)

    bare = ConnectDataFrame.__new__(ConnectDataFrame)  # no _session, no _df
    assert bare.mapInPandas(lambda it: it, "id long") == "delegated"
    assert calls

    inline_guard.uninstall_inline_guard()


def test_matched_engine_delegates_to_upstream(monkeypatch):
    session = _FakeSession()
    rt.register_session(session)
    rt.set_override(session, rt.client_python_version())
    calls = []
    monkeypatch.setattr(
        ConnectDataFrame, "mapInPandas", lambda self, *a, **k: calls.append(a) or "delegated"
    )
    inline_guard.install_inline_guard(session)

    df = _dataframe(session)
    assert df.mapInPandas(lambda it: it, "id long") == "delegated"
    assert calls

    # Uninstall HERE, not via the autouse fixture. The fixture was set up before
    # `monkeypatch`, so its teardown runs AFTER monkeypatch's undo -- which would
    # restore the monkeypatched stub over the real method and leak it into every
    # later test in the session.
    inline_guard.uninstall_inline_guard()


def test_uninstall_restores_the_original_methods():
    original = ConnectDataFrame.mapInPandas
    session = _FakeSession()
    rt.register_session(session)
    inline_guard.install_inline_guard(session)
    assert ConnectDataFrame.mapInPandas is not original
    inline_guard.uninstall_inline_guard()
    assert ConnectDataFrame.mapInPandas is original


def test_install_is_idempotent():
    session = _FakeSession()
    rt.register_session(session)
    inline_guard.install_inline_guard(session)
    wrapped = ConnectDataFrame.mapInPandas
    inline_guard.install_inline_guard(session)
    assert ConnectDataFrame.mapInPandas is wrapped


def test_a_seen_but_unparsable_mismatch_still_blocks_the_inline_family():
    """A known-unknown is still a mismatch: the guard must fire, and say so."""
    session = _FakeSession()

    def _boom(_n):
        raise RuntimeError("[PYTHON_VERSION_MISMATCH] unrecognised wording")

    session.range = _boom
    rt.register_session(session)
    inline_guard.install_inline_guard(session)

    runtime = rt.resolve_for_client(session._client)
    assert runtime.is_mismatched_unknown

    with pytest.raises(UDFUnsupportedError) as excinfo:
        _dataframe(session).mapInPandas(lambda it: it, "id long")
    assert "could not determine" in str(excinfo.value)


def test_installing_the_guard_survives_a_session_that_cannot_be_registered():
    """The guard is class-level, so registration is a bonus, not a prerequisite.

    A session whose `_client` read blows up must not cost the notebook its inline
    guard -- the guard resolves per call and will simply see no client until a
    working session registers.
    """

    class _HostileSession:
        @property
        def _client(self):
            raise RuntimeError("session is half-built")

    inline_guard.install_inline_guard(_HostileSession())  # must not raise

    # the guard is in place regardless of the failed registration
    assert getattr(ConnectDataFrame.mapInPandas, "_smus_inline_guard", False)
