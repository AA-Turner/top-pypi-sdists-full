"""Unit tests for runtime worker-runtime detection.

No real Spark: a fake session/client models the three engine-side signals
(connection metadata, server conf, probe outcome) so every layer and every
fallback is covered deterministically.
"""

import gc
import importlib.util
import sys
import weakref

import pytest

from sagemaker_studio.utils.udf import runtime as rt

CLIENT_PY = "%d.%d" % sys.version_info[:2]

# The probe builds a real UDF, so it needs Spark Connect, and Connect needs
# grpcio, which Brazil does not build for every interpreter this package is
# tested against. Without it the probe is unavailable and resolution correctly
# falls through to `client-fallback`, so only the probe tests are skipped.
requires_connect = pytest.mark.skipif(
    importlib.util.find_spec("grpc") is None, reason="the probe needs pyspark Spark Connect"
)


class _FakeConf:
    def __init__(self, values):
        self._values = values

    def get(self, key, default=None):
        return self._values.get(key, default)


class _FakeClient:
    def __init__(self, session_id="s-1"):
        self._session_id = session_id


class _FakeSession:
    """Models only what the resolver touches."""

    def __init__(self, *, spark_version="4.1.1", conf=None, probe=None):
        self.version = spark_version
        self.conf = _FakeConf(conf or {})
        self._client = _FakeClient()
        self._probe = probe
        self.probe_calls = 0

    def range(self, n):
        self.probe_calls += 1
        if isinstance(self._probe, Exception):
            raise self._probe
        return _FakeDataFrame()


class _FakeDataFrame:
    def select(self, *cols):
        return self

    def collect(self):
        return [(1,)]


class _FakeGlueManager:
    def __init__(self, glue_version=None, python_version=None):
        self._glue_version = glue_version
        self._python_version = python_version

    def get_glue_version(self):
        return self._glue_version

    def get_connection_python_version(self):
        return self._python_version


class _UnweakreffableClient:
    """A client type CPython cannot hold a weakref to (no ``__weakref__`` slot)."""

    __slots__ = ()


class _UnweakreffableSession:
    def __init__(self):
        self._client = _UnweakreffableClient()


def _registered_session(client):
    """The session registered for ``client``, or ``None``.

    Test-only surface, so it lives in the tests: the resolver itself has no
    production caller for it.
    """
    context = rt._context_get(client)
    return None if context is None else context.session


@pytest.fixture(autouse=True)
def _clean():
    rt.clear_cache()
    yield
    rt.clear_cache()


# -- pure parsers ------------------------------------------------------- #


@pytest.mark.parametrize(
    "message,expected",
    [
        (
            "[PYTHON_VERSION_MISMATCH] Python in worker has different version: 3.13 "
            "than that in driver: 3.11, PySpark cannot run with different minor versions.",
            "3.13",
        ),
        (
            "[PYTHON_VERSION_MISMATCH] Python in worker has different version: (3, 13) "
            "than that in driver: (3, 11), PySpark cannot run...",
            "3.13",
        ),
        (
            "Python in worker has different version (3, 12) than that in driver 3.11",
            "3.12",
        ),
        ("some unrelated Spark failure", None),
    ],
)
def test_parse_worker_version_handles_both_spark_formats(message, expected):
    assert rt.parse_worker_version(message) == expected


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/usr/bin/python3.13", "3.13"),
        ("/opt/amazon/bin/python3.11", "3.11"),
        ("/usr/local/bin/python3", None),
        ("python", None),
        ("", None),
    ],
)
def test_python_version_from_path(path, expected):
    assert rt.python_version_from_path(path) == expected


# -- layered resolution -------------------------------------------------- #


def test_override_wins_and_costs_nothing():
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(session)
    rt.set_override(session, "3.9")
    result = rt.resolve_for_session(session)
    assert (result.python_version, result.source) == ("3.9", "override")
    assert session.probe_calls == 0


def test_connection_metadata_is_preferred_over_conf_and_probe():
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.11"})
    rt.register_session(session, session_manager=_FakeGlueManager(python_version="3.13"))
    result = rt.resolve_for_session(session)
    assert result.python_version == "3.13"
    assert result.source == "connection-metadata"
    assert session.probe_calls == 0


def test_server_conf_path_is_used_when_metadata_is_absent():
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="6.0"))
    result = rt.resolve_for_session(session)
    assert result.python_version == "3.13"
    assert result.source == "server-conf"
    assert session.probe_calls == 0


@requires_connect
def test_probe_reports_the_worker_version_from_the_mismatch_error():
    boom = RuntimeError(
        "[PYTHON_VERSION_MISMATCH] Python in worker has different version: 3.13 "
        "than that in driver: 3.11, PySpark cannot run with different minor versions."
    )
    session = _FakeSession(probe=boom)
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="6.0"))
    result = rt.resolve_for_session(session)
    assert result.python_version == "3.13"
    assert result.source == "probe"
    assert session.probe_calls == 1


@requires_connect
def test_probe_success_means_the_worker_matches_the_client():
    session = _FakeSession()
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="5.1"))
    result = rt.resolve_for_session(session)
    assert result.python_version == CLIENT_PY
    assert result.source == "probe"
    assert result.matches_client()


def test_a_probe_failure_unrelated_to_versions_assumes_a_match():
    """No evidence of a mismatch means assume there is none.

    A Glue-version table used to answer here. It was deleted because with no
    evidence either way it could invent a mismatch: an engine whose workers match
    this kernel would be routed to a sidecar its workers then reject. Assuming a
    match takes the untouched upstream path, which is the safe direction to be
    wrong in -- if the worker really does differ, the probe would have said so.
    """
    session = _FakeSession(probe=RuntimeError("AccessDeniedException: no permission"))
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="6.0"))
    result = rt.resolve_for_session(session)
    assert result.python_version == CLIENT_PY
    assert result.source == "client-fallback"
    assert result.matches_client() is True


def test_probe_can_be_disabled_by_env(monkeypatch):
    monkeypatch.setenv("SMUS_UDF_WORKER_PROBE", "0")
    session = _FakeSession(probe=RuntimeError("must not be raised"))
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="6.0"))
    result = rt.resolve_for_session(session)
    assert session.probe_calls == 0
    assert result.source == "client-fallback"
    assert result.python_version == CLIENT_PY


def test_completely_unknown_engine_degrades_to_the_client_version():
    session = _FakeSession(probe=RuntimeError("unrelated"))
    rt.register_session(session, session_manager=None)
    result = rt.resolve_for_session(session)
    assert result.python_version == CLIENT_PY
    assert result.source == "client-fallback"


@requires_connect
def test_resolution_is_cached_so_the_probe_runs_at_most_once():
    boom = RuntimeError("Python in worker has different version: 3.13 than that in driver: 3.11")
    session = _FakeSession(probe=boom)
    rt.register_session(session)
    first = rt.resolve_for_session(session)
    second = rt.resolve_for_session(session)
    assert first == second
    assert session.probe_calls == 1
    assert rt.resolve_for_session(session).source == "probe"


def test_spark_version_is_read_from_the_engine():
    session = _FakeSession(
        spark_version="3.5.6", conf={"spark.pyspark.python": "/usr/bin/python3.11"}
    )
    rt.register_session(session)
    assert rt.resolve_for_session(session).spark_version == "3.5.6"


def test_resolve_for_client_finds_the_registered_session():
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(session)
    result = rt.resolve_for_client(session._client)
    assert result.python_version == "3.13"


def test_resolve_for_an_unknown_client_degrades_to_the_client_version():
    result = rt.resolve_for_client(_FakeClient("unregistered"))
    assert result.python_version == CLIENT_PY
    assert result.source == "client-fallback"


def test_unregister_drops_the_cache_entry():
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(session)
    rt.resolve_for_session(session)
    rt.unregister_session(session)
    assert _registered_session(session._client) is None


def test_the_server_conf_keys_name_worker_interpreters_only():
    # `spark.pyspark.driver.python` names the DRIVER's interpreter and defaults
    # to `spark.pyspark.python`, so it is evidence about the driver, not the
    # workers -- and it must not sit above the authoritative worker probe.
    assert rt.SERVER_CONF_PYTHON_KEYS == (
        "spark.pyspark.python",
        "spark.executorEnv.PYSPARK_PYTHON",
        "spark.yarn.appMasterEnv.PYSPARK_PYTHON",
    )


# -- never-raises regressions --------------------------------------------- #


def test_server_conf_skips_a_non_string_value_without_raising():
    """A conf implementation returning a non-string truthy value must not
    crash the whole server-conf layer -- it should skip that key and keep
    checking the rest of SERVER_CONF_PYTHON_KEYS."""
    session = _FakeSession(
        conf={
            "spark.pyspark.python": 12345,
            "spark.executorEnv.PYSPARK_PYTHON": "/usr/bin/python3.13",
        }
    )
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="6.0"))
    result = rt.resolve_for_session(session)
    assert result.python_version == "3.13"
    assert result.source == "server-conf"
    assert session.probe_calls == 0


@requires_connect
def test_probe_udf_construction_failure_falls_through_without_raising(monkeypatch):
    """If building the probe UDF itself raises (not just running it), the probe
    layer must still degrade instead of propagating the exception."""
    import pyspark.sql.connect.functions as connect_functions

    def _boom(*_args, **_kwargs):
        raise RuntimeError("cannot construct udf")

    monkeypatch.setattr(connect_functions, "udf", _boom)
    session = _FakeSession(probe=RuntimeError("must not be reached"))
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="6.0"))
    result = rt.resolve_for_session(session)
    assert result.source == "client-fallback"
    assert result.python_version == CLIENT_PY
    assert session.probe_calls == 0


# -- context eviction ------------------------------------------------------ #


def test_register_session_evicts_when_the_client_is_collected():
    """A collected client's context goes with it, with no bookkeeping of ours.

    ``_CONTEXTS`` is keyed on the client OBJECT, so the mapping drops the entry
    itself. Nothing of ours runs during collection -- which is what makes the
    whole class of finalizer hazards inapplicable rather than handled.

    Nothing leaks either: the context holds only a weakref to the session.

    Note the client is deliberately never bound to a local name that outlives the
    collection -- the mapping keys on that object, so a test holding it would keep
    the entry alive and prove nothing.
    """
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(session)
    assert rt._context_get(session._client) is not None
    client_ref = weakref.ref(session._client)

    del session
    gc.collect()

    # The client is gone, and its entry went with it -- no drain step, no queue.
    assert client_ref() is None
    assert len(rt._CONTEXTS) == 0


def test_collections_during_resolution_neither_hang_nor_corrupt():
    """Regression test for a real hang: 34 minutes, then killed.

    Eviction used to run inside a ``weakref.finalize`` callback that took a module
    lock. Such a callback fires at an arbitrary point on whichever thread triggers
    collection -- including during garbage collection provoked by an allocation
    inside a section already holding that lock -- so it deadlocked the thread
    against itself. The observed stack was ``Garbage-collecting -> _evict ->
    weakref.__call__ -> resolve_current``.

    Keying on the client object removes both the callback and the deferred-eviction
    queue that replaced it. The window the queue guarded was narrow but real: a
    collection provoked by the allocation *inside* ``list(_CONTEXTS.values())``
    mutating the mapping mid-walk, which raises "dictionary changed size during
    iteration". ``WeakKeyDictionary`` defers its own removals while being iterated
    (``weakref._IterationGuard``), so this drives that interleaving hard to prove
    the stdlib guard holds where our queue used to.
    """
    live = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(live)

    for _ in range(50):
        doomed = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
        rt.register_session(doomed)
        del doomed
        gc.collect()  # collects mid-resolution, at an arbitrary point
        assert rt.resolve_current() is not None

    assert len(rt._CONTEXTS) == 1


def test_resolve_current_prefers_the_most_recent_registration():
    """Ordering is by explicit registration sequence, not mapping iteration order.

    ``WeakKeyDictionary`` documents no iteration order, and ordering ACROSS the
    weak mapping and the non-weak-referenceable fallback has none at all -- so
    ``_SessionContext.seq`` is what makes "most recent" mean anything.
    """
    first = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.11"})
    second = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(first)
    rt.register_session(second)

    assert rt.resolve_current().python_version == "3.13"

    # A non-weak-referenceable client registered last still wins, even though it
    # lives in the other mapping.
    third = _UnweakreffableSession()
    third.conf = {"spark.pyspark.python": "/usr/bin/python3.12"}
    rt.register_session(third)

    assert rt.resolve_current().python_version == "3.12"


def test_a_manager_arriving_later_invalidates_a_resolution_made_without_it():
    """A cached answer must not outlive the arrival of better evidence.

    The kernel registers the session before a manager exists, so a UDF defined in
    between resolves without connection metadata. That answer is cached, and the
    cache is never invalidated -- so adopting the manager afterwards left the
    connection pinned for its whole life. Both stuck states are bad: a
    `mismatched-unknown` keeps raising on every UDF, and a `client-fallback`
    keeps claiming "matched" and hands the user the raw PYTHON_VERSION_MISMATCH.
    """
    session = _FakeSession(probe=RuntimeError("unrelated failure"))
    rt.register_session(session)  # no manager yet
    first = rt.resolve_for_session(session)
    assert first.source == "client-fallback"

    # The manager shows up afterwards and can answer a higher layer.
    rt.register_session(session, session_manager=_FakeGlueManager(python_version="3.13"))

    second = rt.resolve_for_session(session)
    assert (second.python_version, second.source) == ("3.13", "connection-metadata")


def test_a_second_registration_without_a_manager_keeps_the_cached_resolution():
    """Only NEW evidence invalidates. A repeat registration is not new evidence."""
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(session)
    first = rt.resolve_for_session(session)

    rt.register_session(session)  # same, no manager
    assert rt.resolve_for_session(session) is first


def test_register_session_on_a_non_weak_referenceable_client_still_registers():
    session = _UnweakreffableSession()
    rt.register_session(session)
    assert _registered_session(session._client) is session


# -- idempotent re-registration -------------------------------------------- #


def test_reregistering_preserves_an_override_set_between_the_two_calls():
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(session)
    rt.set_override(session, "3.9")

    # A second, independent caller (e.g. install_udf_interceptor) registers
    # the same session again -- this must not discard the override.
    rt.register_session(session)

    result = rt.resolve_for_session(session)
    assert (result.python_version, result.source) == ("3.9", "override")
    assert session.probe_calls == 0


@requires_connect
def test_reregistering_preserves_a_cached_resolution_so_the_probe_does_not_rerun():
    boom = RuntimeError("Python in worker has different version: 3.13 than that in driver: 3.11")
    session = _FakeSession(probe=boom)
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="6.0"))
    first = rt.resolve_for_session(session)
    assert session.probe_calls == 1

    # Re-registering after resolution must not wipe the cached WorkerRuntime --
    # if it did, the next resolve_for_session would re-run the probe.
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="6.0"))
    second = rt.resolve_for_session(session)

    assert second == first
    assert session.probe_calls == 1


def test_reregistering_fills_in_a_manager_the_first_call_lacked():
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(session)  # no manager the first time
    rt.register_session(session, session_manager=_FakeGlueManager(python_version="3.11"))

    result = rt.resolve_for_session(session)
    assert result.python_version == "3.11"
    assert result.source == "connection-metadata"


# -- a SEEN mismatch we cannot parse ---------------------------------------- #


_UNPARSABLE_MISMATCH = RuntimeError(
    "[PYTHON_VERSION_MISMATCH] the worker's interpreter disagrees with the driver's "
    "(new wording this SDK's regex does not know)"
)


@requires_connect
def test_an_unparsable_mismatch_does_not_resolve_to_matched():
    """A known-unknown must not collapse into "fine".

    The probe SAW the engine's own PYTHON_VERSION_MISMATCH; only the version was
    unreadable. Resolving to the client's version -- `matches_client() is True` --
    would take the local-build path against direct evidence to the contrary, and
    the user would get the raw mismatch at `.show()` after all.
    """
    session = _FakeSession(probe=_UNPARSABLE_MISMATCH)
    rt.register_session(session, session_manager=None)  # no Glue manager available
    result = rt.resolve_for_session(session)

    assert result.python_version == rt.UNKNOWN_PYTHON_VERSION
    assert result.source == rt.MISMATCHED_UNKNOWN_SOURCE
    assert result.is_mismatched_unknown is True
    assert result.matches_client() is False


@requires_connect
def test_an_unparsable_mismatch_stays_unknown_and_never_claims_a_match():
    """A mismatch we SAW but could not read must not resolve to anything else.

    A Glue-version table used to supply a guess here. Deleting it makes this the
    only outcome, which is the honest one: reaching this point essentially
    requires upstream to have changed its mismatch wording, and a wording change
    ships with a new Spark release -- exactly when a hardcoded table is most
    likely to be stale. A wrong guess costs a multi-minute venv build and then
    surfaces the raw PYTHON_VERSION_MISMATCH anyway; this fails fast and says
    what it knows.
    """
    session = _FakeSession(probe=_UNPARSABLE_MISMATCH)
    rt.register_session(session, session_manager=_FakeGlueManager(glue_version="6.0"))
    result = rt.resolve_for_session(session)

    assert result.python_version == rt.UNKNOWN_PYTHON_VERSION
    assert result.source == rt.MISMATCHED_UNKNOWN_SOURCE
    assert result.is_mismatched_unknown is True
    assert result.matches_client() is False


@requires_connect
def test_a_parsable_mismatch_is_unaffected():
    session = _FakeSession(
        probe=RuntimeError(
            "[PYTHON_VERSION_MISMATCH] Python in worker has different version: 3.13 "
            "than that in driver: 3.11"
        )
    )
    rt.register_session(session)
    result = rt.resolve_for_session(session)
    assert (result.python_version, result.source) == ("3.13", "probe")
    assert result.is_mismatched_unknown is False


def test_no_signal_at_all_still_degrades_to_the_client_version():
    """Deliberately different from a SEEN mismatch: no evidence means local build."""
    session = _FakeSession(probe=RuntimeError("AccessDeniedException: no permission"))
    rt.register_session(session, session_manager=None)
    result = rt.resolve_for_session(session)
    assert result.python_version == CLIENT_PY
    assert result.source == "client-fallback"
    assert result.is_mismatched_unknown is False
    assert result.matches_client() is True


# -- a transient session.version failure must not be memoized --------------- #


class _FlakyVersionSession(_FakeSession):
    """A session whose `session.version` fails once, then recovers.

    `session.version` on a Connect session is a live server round trip, so a
    single blip is expected. It must not pin the connection for its whole life.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._version_reads = 0

    @property
    def version(self):
        self._version_reads += 1
        if self._version_reads == 1:
            raise RuntimeError("transient: AnalyzePlan(spark_version) failed")
        return "4.1.1"

    @version.setter
    def version(self, value):
        pass  # the base class assigns in __init__; the property above is the source


def test_a_transient_spark_version_failure_is_not_cached_for_the_connections_life():
    session = _FlakyVersionSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})
    rt.register_session(session)

    first = rt.resolve_for_session(session)
    assert first.spark_version == "unknown"
    assert first.python_version == "3.13"

    # `session.version` answers now, so the very next resolution must see it --
    # otherwise every later UDF on this connection asks for
    # `entry.builder("unknown")`, a sidecar built against the wrong pyspark.
    second = rt.resolve_for_session(session)
    assert second.spark_version == "4.1.1"
    assert second.python_version == "3.13"

    # ...and THAT one is cached.
    assert rt.resolve_for_session(session) is second


@requires_connect
def test_re_resolving_after_an_unknown_spark_version_does_not_re_run_the_probe():
    """The probe is one-shot per CONNECTION, not per resolution.

    Not caching an unknown-Spark runtime means re-resolving; the probe is a real
    job on the engine, so it must not be re-run each time.
    """
    session = _FlakyVersionSession(
        probe=RuntimeError("Python in worker has different version: 3.13 than that in driver: 3.11")
    )
    rt.register_session(session)

    first = rt.resolve_for_session(session)
    assert (first.python_version, first.spark_version) == ("3.13", "unknown")
    assert session.probe_calls == 1

    second = rt.resolve_for_session(session)
    assert (second.python_version, second.spark_version) == ("3.13", "4.1.1")
    assert session.probe_calls == 1


# -- degrading instead of raising ---------------------------------------- #
#
# Every engine-side signal can fail on a real connection, and none of them may
# take the notebook down with it. These drive the helpers directly rather than
# through the ladder, so a failure is attributed to the layer that caused it and
# the test needs no Spark Connect.


def test_an_empty_mismatch_message_yields_no_worker_version():
    assert rt.parse_worker_version("") is None


def test_connection_metadata_that_raises_is_no_signal_rather_than_an_error():
    class _Boom:
        def get_connection_python_version(self):
            raise RuntimeError("DescribeConnection throttled")

    assert rt._from_connection_metadata(_Boom()) is None


def test_connection_metadata_that_cannot_be_parsed_is_no_signal():
    """A garbage value must not become a version, nor raise out of the ladder."""
    assert rt._from_connection_metadata(_FakeGlueManager(python_version="python-next")) is None


def test_a_manager_without_the_getter_is_no_signal():
    assert rt._from_connection_metadata(object()) is None


def test_a_manager_returning_nothing_is_no_signal():
    assert rt._from_connection_metadata(_FakeGlueManager(python_version="")) is None


def test_server_conf_is_no_signal_when_the_session_exposes_no_conf():
    assert rt._from_server_conf(object()) is None


def test_a_conf_key_that_raises_is_skipped_and_a_later_key_still_answers():
    """One unreadable key must not hide the key that would have answered."""
    first, second = rt.SERVER_CONF_PYTHON_KEYS[0], rt.SERVER_CONF_PYTHON_KEYS[1]

    class _RaisingConf:
        def get(self, key, default=None):
            if key == first:
                raise RuntimeError("conf unavailable")
            return "/usr/bin/python3.13" if key == second else default

    class _Session:
        conf = _RaisingConf()

    answered = rt._from_server_conf(_Session())
    assert answered is not None
    version, key, _value = answered
    assert (version, key) == ("3.13", second)


def test_an_engine_spark_version_that_raises_degrades_to_unknown():
    class _Session:
        @property
        def version(self):
            raise RuntimeError("no server")

    assert rt._engine_spark_version(_Session()) == rt.UNKNOWN_SPARK_VERSION


def test_a_collected_session_resolves_to_the_client_without_touching_an_engine():
    """The context outlives its session by design: the registry holds a weakref.

    Resolution must still answer -- attribute reads on a routed UDF go through
    here -- and the only honest answer is the client's own version.
    """
    context = rt._SessionContext(_FakeSession(), None)
    context.session_ref = lambda: None  # model the session having been collected

    runtime = rt._resolve(context)

    assert runtime.python_version == CLIENT_PY
    assert runtime.source == "client-fallback"
    assert "collected" in runtime.detail


def test_resolving_an_unregistered_session_works_without_registering_it_first():
    """`resolve_for_session` is reachable before any explicit registration."""
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.13"})

    runtime = rt.resolve_for_session(session)

    assert (runtime.python_version, runtime.source) == ("3.13", "server-conf")


def test_an_override_on_a_never_registered_session_still_takes_effect():
    session = _FakeSession(conf={"spark.pyspark.python": "/usr/bin/python3.11"})
    rt.set_override(session, "3.13")

    assert rt.resolve_for_session(session).python_version == "3.13"


def test_setting_an_override_on_a_clientless_session_is_a_no_op():
    """A still-lazy session has no `_client` to key on, so there is nothing to do."""

    class _NoClient:
        pass

    rt.set_override(_NoClient(), "3.13")  # must not raise
    assert rt.resolve_current() is None


def test_unregistering_a_clientless_session_is_a_no_op():
    class _NoClient:
        pass

    rt.unregister_session(_NoClient())  # must not raise


def test_current_runtime_skips_a_context_whose_session_was_collected():
    """A dead context must not be reported as the engine resolvable right now."""
    dead = rt._SessionContext(_FakeSession(), None)
    dead.session_ref = lambda: None
    rt._UNWEAKREFFABLE[id(dead)] = dead

    assert rt.resolve_current() is None
