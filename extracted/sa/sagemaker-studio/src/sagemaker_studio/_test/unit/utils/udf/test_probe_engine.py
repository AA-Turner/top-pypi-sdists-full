"""Unit tests for the operator engine-signal dump.

`probe_engine` is a hand-run diagnostic, not library code, so nothing imports it
in production. That is exactly why it needs tests: it reads four `runtime` APIs
(`SERVER_CONF_PYTHON_KEYS`, `python_version_from_path`, `parse_worker_version`,
`resolve_for_session`), and if one is renamed the tool breaks silently -- with
nobody finding out until an operator reaches for it mid-investigation.

Every signal it reports is also a signal that can FAIL on a real engine, so the
error branches matter as much as the happy path: the whole point of the dump is
to still print the other signals when one of them blows up.
"""

import importlib.util

import pytest

from sagemaker_studio.utils.udf import probe_engine
from sagemaker_studio.utils.udf import runtime as rt

# The probe section builds a real upstream UDF, so it needs Spark Connect, and
# Connect needs grpcio, which Brazil does not build for every interpreter this
# package is tested against. Only the two probe-outcome tests need it; the rest
# of the dump is engine conf and runs anywhere.
requires_connect = pytest.mark.skipif(
    importlib.util.find_spec("grpc") is None, reason="the probe needs pyspark Spark Connect"
)


class _Conf:
    def __init__(self, values=None, raises_for=()):
        self._values = values or {}
        self._raises_for = set(raises_for)

    def get(self, key, default=None):
        if key in self._raises_for:
            raise RuntimeError("conf unavailable")
        return self._values.get(key, default)


class _DataFrame:
    def select(self, *cols):
        return self

    def collect(self):
        return [(1,)]


class _Session:
    """Models only the four things `report` touches on a live connection."""

    def __init__(self, *, version="4.1.1", conf=None, range_raises=None):
        self._version = version
        self.conf = conf if conf is not None else _Conf()
        self._range_raises = range_raises
        self._client = object()

    @property
    def version(self):
        if isinstance(self._version, Exception):
            raise self._version
        return self._version

    def range(self, n):
        if self._range_raises is not None:
            raise self._range_raises
        return _DataFrame()


@pytest.fixture(autouse=True)
def _clean():
    rt.clear_cache()
    yield
    rt.clear_cache()


def test_reports_every_section_and_the_resolver_verdict():
    session = _Session(conf=_Conf({"spark.pyspark.python": "/usr/bin/python3.13"}))

    out = probe_engine.report(session)

    for heading in ("== engine ==", "== candidate runtime conf keys ==", "== worker probe =="):
        assert heading in out
    assert "== resolver verdict ==" in out
    assert "session.version (server Spark) = 4.1.1" in out
    # the conf key that answered is echoed WITH its parsed version, which is the
    # question an operator runs this to settle
    assert "spark.pyspark.python = '/usr/bin/python3.13'   -> python 3.13" in out
    assert "source=server-conf" in out


def test_every_candidate_key_is_listed_even_when_unset():
    """The absent keys are the finding: they prove the list can shrink."""
    out = probe_engine.report(_Session())

    for key in list(rt.SERVER_CONF_PYTHON_KEYS) + probe_engine.EXTRA_CONF_KEYS:
        assert f"{key} = " in out


def test_a_failing_session_version_does_not_abort_the_dump():
    session = _Session(version=RuntimeError("no server"), conf=_Conf({"x": "y"}))

    out = probe_engine.report(session)

    assert "session.version FAILED: RuntimeError: no server" in out
    # the later sections still ran
    assert "== worker probe ==" in out
    assert "== resolver verdict ==" in out


def test_a_conf_key_that_raises_is_reported_inline_and_the_rest_still_read():
    bad = "spark.pyspark.python"
    session = _Session(conf=_Conf({"spark.executorEnv.PYTHONPATH": "/x"}, raises_for=[bad]))

    out = probe_engine.report(session)

    assert f'{bad} = "<error: RuntimeError: conf unavailable>"' in out or (
        f"{bad} = '<error: RuntimeError: conf unavailable>'" in out
    )
    assert "spark.executorEnv.PYTHONPATH = '/x'" in out


@requires_connect
def test_a_probe_mismatch_reports_the_parsed_worker_version_and_raw_text():
    boom = RuntimeError(
        "[PYTHON_VERSION_MISMATCH] Python in worker has different version: 3.13 "
        "than that in driver: 3.11, PySpark cannot run with different minor versions."
    )
    out = probe_engine.report(_Session(range_raises=boom))

    assert "probe RAISED RuntimeError" in out
    assert "worker version parsed: 3.13" in out
    # the raw message is what goes into a bug report, so it must survive verbatim
    assert "PYTHON_VERSION_MISMATCH" in out


@requires_connect
def test_a_successful_probe_says_the_worker_matches():
    out = probe_engine.report(_Session(conf=_Conf()))

    assert "probe SUCCEEDED -> the worker Python matches this client" in out
