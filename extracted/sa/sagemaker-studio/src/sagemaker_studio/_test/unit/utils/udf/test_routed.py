"""Unit tests for per-DataFrame routed UDF construction.

Real pyspark protos, a fake sidecar builder, and two fake clients standing in
for two connections -- enough to prove routing happens per plan build.
"""

import base64
import json
import logging

import pytest

pyspark = pytest.importorskip("pyspark", reason="routed UDFs build real pyspark protos")
# Connect specifically: its protos need grpcio, which Brazil does not build for
# every interpreter this package is tested against.
pytest.importorskip("pyspark.sql.connect.proto")

import pyspark.sql.connect.proto as proto  # noqa: E402
from pyspark.rdd import PythonEvalType  # noqa: E402
from pyspark.sql.connect.udf import UDFRegistration  # noqa: E402
from pyspark.sql.types import ArrayType, LongType, StringType, StructField, StructType  # noqa: E402

from sagemaker_studio.utils.udf import registry, routed  # noqa: E402
from sagemaker_studio.utils.udf import runtime as rt  # noqa: E402
from sagemaker_studio.utils.udf.errors import (  # noqa: E402
    UDFRegistrationError,
    UDFSidecarError,
    UDFUnsupportedError,
)

CLIENT_PY = registry.client_python_version()


_DDL_TYPES = {"long": LongType(), "string": StringType()}


class _Analyzed:
    def __init__(self, parsed):
        self.parsed = parsed


class _FakeClient:
    """Stands in for SparkConnectClient.

    ``_analyze`` models the server's ``ddl_parse`` round trip -- a string
    ``returnType``, which is what ``udf`` and ``spark.udf.register`` take by
    default, reaches the server as DDL -- so the fake resolves the handful of DDL
    strings these tests use rather than asserting the branch is unreachable.

    ``_execute_plan_request_with_metadata`` / ``_execute`` / ``register_udf``
    model the registration plumbing, so a routed ``spark.udf.register`` can be
    inspected as a real proto instead of mocked away.
    """

    def __init__(self, name):
        self.name = name
        self.analyze_calls = []
        self.executed = []
        self.register_udf_calls = []

    def _analyze(self, method, **kwargs):
        self.analyze_calls.append((method, kwargs))
        assert method == "ddl_parse"
        return _Analyzed(_DDL_TYPES[kwargs["ddl_string"]])

    def _execute_plan_request_with_metadata(self):
        return proto.ExecutePlanRequest()

    def _execute(self, request):
        self.executed.append(request)

    def register_udf(self, function, return_type, name=None, eval_type=None, deterministic=True):
        """Upstream's local-build path. Reached only on a MATCHED engine."""
        self.register_udf_calls.append((function, return_type, name, eval_type, deterministic))
        return name


class SparkSession:  # noqa: N801 - the name and module together are what
    # `validate_freevar`'s live-type check matches on (see
    # `capture._LIVE_TYPE_NAMES` / `_LIVE_OWNER_MODULES`). The name alone is not
    # enough by design: matching it unqualified also refused a pandas DataFrame.
    # `__module__` is set below so this stand-in trips the rule the way a real
    # session does, which is what
    # test_a_closure_over_a_live_session_is_refused_at_definition_time exercises.
    def __init__(self, client, spark_version):
        self._client = client
        self.version = spark_version
        self.conf = _Conf()

    class _Range:
        def select(self, *a):
            return self

        def collect(self):
            return []

    def range(self, n):
        return self._Range()


class _Conf:
    def get(self, key, default=None):
        return default


class _FakeBuilder:
    def __init__(self, python_ver, spark_version):
        self.python_ver = python_ver
        self.spark_version = spark_version
        self.requests = []
        self.commands = []  # the exact command bytes handed back, for byte comparison
        self.fail = False

    def build(self, request):
        self.requests.append(request)
        if self.fail:
            return {"ok": False, "error": "ValueError: nope", "traceback": "tb"}
        from pyspark.serializers import CloudPickleSerializer

        # Mirrors the real sidecar's decode deliberately (see
        # udf_sidecar/sidecar_server.py::_decode_return_type): DataType has no
        # public fromJson, so wrap in a one-field StructType and use the public
        # StructType.fromJson, which works on both pyspark 3.5.x and 4.1.1. Do
        # NOT "simplify" this back to the private _parse_datatype_json_string.
        return_type = (
            StructType.fromJson(
                {
                    "type": "struct",
                    "fields": [
                        {
                            "name": "v",
                            "type": json.loads(request["return_type_json"]),
                            "nullable": True,
                            "metadata": {},
                        }
                    ],
                }
            )
            .fields[0]
            .dataType
        )
        namespace = {}
        for statement in request["imports"]:
            exec(statement, namespace)
        import pickle as _pickle

        namespace.update(_pickle.loads(base64.b64decode(request["freevars_pickle_b64"])))
        exec(request["source"], namespace)
        command = CloudPickleSerializer().dumps((namespace[request["name"]], return_type))
        self.commands.append(command)
        return {
            "ok": True,
            "command_b64": base64.b64encode(command).decode("ascii"),
            "python_ver": self.python_ver,
            "spark_version": self.spark_version,
        }


@pytest.fixture(autouse=True)
def _clean():
    registry.clear_registry()
    rt.clear_cache()
    routed.uninstall_udf_register_routing()
    yield
    routed.uninstall_udf_register_routing()
    registry.clear_registry()
    rt.clear_cache()


def _register(python_ver="3.13", spark_version="4.1.1"):
    builders = {}

    def factory(sv):
        builders[sv] = _FakeBuilder(python_ver, sv)
        return builders[sv]

    registry.register_sidecar(python_ver, factory)
    return builders


# Faithful in the one dimension the live-value rule reads: a real session's class
# lives under `pyspark`, and the rule is module-qualified.
SparkSession.__module__ = "pyspark.sql.connect.session"


def _mismatched_session(spark_version="4.1.1", worker="3.13"):
    session = SparkSession(_FakeClient("glue6"), spark_version)
    rt.register_session(session)
    rt.set_override(session, worker)
    return session


def _matched_session(spark_version="3.5.6"):
    session = SparkSession(_FakeClient("glue5"), spark_version)
    rt.register_session(session)
    rt.set_override(session, CLIENT_PY)
    return session


def test_matched_connection_builds_locally_with_the_client_stamp():
    session = _matched_session()
    my_udf = routed.udf(lambda x: x, returnType=StringType())
    plan = my_udf("c")._expr.to_plan_udf(session._client)
    assert plan.python_udf.python_ver == CLIENT_PY
    assert plan.python_udf.command  # cloudpickled locally


def test_mismatched_connection_uses_the_sidecar_stamp_and_command():
    _register()
    session = _mismatched_session()

    def add_one(x):
        return x + 1

    my_udf = routed.udf(add_one, returnType=LongType())
    plan = my_udf("c")._expr.to_plan_udf(session._client)
    assert plan.python_udf.python_ver == "3.13"
    assert plan.python_udf.eval_type == PythonEvalType.SQL_BATCHED_UDF
    assert plan.function_name == "add_one"


def test_the_same_udf_routes_differently_per_target_dataframe():
    # THE per-DataFrame property: one UDF object, two connections, two stamps.
    _register()
    matched = _matched_session()
    mismatched = _mismatched_session()

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=StringType())
    local_plan = my_udf("c")._expr.to_plan_udf(matched._client)
    remote_plan = my_udf("c")._expr.to_plan_udf(mismatched._client)
    assert local_plan.python_udf.python_ver == CLIENT_PY
    assert remote_plan.python_udf.python_ver == "3.13"


def test_route_decision_is_recorded_once_per_engine_not_once_per_udf_object(monkeypatch):
    """A UDF object reused across engines must report EACH engine, not just the first.

    ``_decisions_recorded`` is keyed by (worker_python, spark_version) rather than
    a single bool precisely because ``_command_cache`` anticipates one UDF object
    being applied to more than one connection. A bool would make the first engine
    the only one ever reported, silently hiding a DetectionSource regression on
    every engine after it.
    """
    _register()
    matched = _matched_session()
    mismatched = _mismatched_session()

    calls = []
    monkeypatch.setattr(
        "sagemaker_studio.utils.udf.metrics.record_route_decision",
        lambda **kwargs: calls.append(kwargs),
    )

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=StringType())
    my_udf("c")._expr.to_plan_udf(matched._client)
    my_udf("c")._expr.to_plan_udf(mismatched._client)

    assert len(calls) == 2
    assert calls[0]["routed"] is False
    assert calls[0]["worker_python"] == CLIENT_PY
    assert calls[1]["routed"] is True
    assert calls[1]["worker_python"] == "3.13"

    # Re-applying against an ALREADY-SEEN engine must not emit a third metric.
    my_udf("c")._expr.to_plan_udf(mismatched._client)
    assert len(calls) == 2


def test_defining_a_udf_never_calls_the_sidecar():
    builders = _register()
    _mismatched_session()

    def f(x):
        return x

    routed.udf(f, returnType=StringType())
    assert builders == {}  # the factory was not even invoked


def test_the_sidecar_command_is_built_once_per_engine_and_reused():
    builders = _register()
    session = _mismatched_session()

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=StringType())
    my_udf("a")._expr.to_plan_udf(session._client)
    my_udf("b")._expr.to_plan_udf(session._client)
    assert len(builders["4.1.1"].requests) == 1


def test_complex_return_types_survive_the_round_trip():
    _register()
    session = _mismatched_session()
    return_type = StructType(
        [StructField("xs", ArrayType(LongType()), True), StructField("s", StringType(), True)]
    )

    def f(x):
        return x

    plan = routed.udf(f, returnType=return_type)("c")._expr.to_plan_udf(session._client)
    from pyspark.sql.connect.types import proto_schema_to_pyspark_data_type

    assert proto_schema_to_pyspark_data_type(plan.python_udf.output_type) == return_type


def test_arrow_eval_type_from_upstream_is_preserved():
    _register()
    session = _mismatched_session()

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=StringType(), useArrow=True)
    plan = my_udf("c")._expr.to_plan_udf(session._client)
    assert plan.python_udf.eval_type == PythonEvalType.SQL_ARROW_BATCHED_UDF


def test_pandas_udf_routes_with_the_scalar_pandas_eval_type():
    _register()
    session = _mismatched_session()

    def double(s):
        return s * 2

    my_udf = routed.pandas_udf(double, returnType=LongType())
    plan = my_udf("c")._expr.to_plan_udf(session._client)
    assert plan.python_udf.eval_type == PythonEvalType.SQL_SCALAR_PANDAS_UDF
    assert plan.python_udf.python_ver == "3.13"


def test_decorator_form_is_supported():
    _register()
    session = _mismatched_session()

    @routed.udf(returnType=LongType())
    def triple(x):
        return x * 3

    plan = triple("c")._expr.to_plan_udf(session._client)
    assert plan.function_name == "triple"
    assert plan.python_udf.python_ver == "3.13"


def test_as_nondeterministic_is_inherited_from_upstream():
    _register()
    session = _mismatched_session()

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=StringType()).asNondeterministic()
    plan = my_udf("c")._expr.to_plan_udf(session._client)
    assert plan.deterministic is False


def test_missing_sidecar_registration_is_an_actionable_registration_error():
    session = _mismatched_session()

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=StringType())
    with pytest.raises(UDFRegistrationError) as excinfo:
        my_udf("c")._expr.to_plan_udf(session._client)
    message = str(excinfo.value)
    assert "3.13" in message and CLIENT_PY in message
    assert "register_sidecar" in message


def test_a_closure_over_a_live_session_is_refused_at_definition_time():
    """Fail-fast at registration: this must raise from `udf(...)`, not at plan build.

    Source capture is lazy, but freevar validation is hoisted to definition time
    precisely so this case cannot fail late.
    """
    session = _mismatched_session()

    def leaky(x):
        return str(session)

    with pytest.raises(UDFRegistrationError) as excinfo:
        routed.udf(leaky, returnType=StringType())
    assert "'session'" in str(excinfo.value)


def test_a_definable_udf_is_not_validated_into_failure(monkeypatch):
    """Eager validation must not reject a callable whose closure cannot be inspected."""
    _register()
    _mismatched_session()

    class _Callable:
        def __call__(self, x):
            return x

    # `inspect.getclosurevars` raises TypeError on a non-function; defining the
    # UDF must still succeed (any real problem surfaces from capture(), later).
    routed.udf(_Callable(), returnType=StringType())


def test_sidecar_failure_surfaces_the_remote_traceback():
    builders = _register()
    session = _mismatched_session()

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=StringType())
    # Trip the failure on first use.
    entry = registry.get_sidecar("3.13")
    entry.builder("4.1.1").fail = True
    with pytest.raises(UDFSidecarError) as excinfo:
        my_udf("c")._expr.to_plan_udf(session._client)
    assert "ValueError: nope" in str(excinfo.value)
    assert builders  # the builder was reached


def test_install_udf_interceptor_puts_both_factories_in_the_namespace():
    session = _matched_session()
    namespace = {}
    installed = routed.install_udf_interceptor(namespace, session)
    assert set(installed) == {"udf", "pandas_udf"}
    assert namespace["udf"] is installed["udf"]
    assert namespace["pandas_udf"].__name__ == "pandas_udf"


def test_install_udf_interceptor_does_not_mutate_pyspark_globals():
    import pyspark.sql.functions as F  # noqa: N812 - mirrors pyspark's own name

    original = F.udf
    routed.install_udf_interceptor({}, _matched_session())
    assert F.udf is original


# -- spark.udf.register ---------------------------------------------------- #
#
# Connect's `UDFRegistration.register` does NOT reuse the UDF's expression: it
# calls `client.register_udf(f.func, f.returnType, name, f.evalType,
# f.deterministic)`, which builds a fresh UPSTREAM `PythonUDF` stamped with the
# local `sys.version_info`. `SidecarPythonUDF.to_plan` is never invoked, so
# `spark.sql("select myfn(...)")` dies deep in the job. These tests pin the
# wrapper that fixes it -- and that it registers a TRUTHFUL command, built by the
# sidecar, rather than a locally-pickled one wearing a borrowed version string.


def _registered_udf_proto(client):
    assert len(client.executed) == 1, client.executed
    return client.executed[0].plan.command.register_function


def test_upstream_register_stamps_the_local_python_version_without_routing():
    """The bug, pinned: with routing NOT installed, registration is mis-stamped."""
    _register()
    session = _mismatched_session()

    def add_one(x):
        return x + 1

    UDFRegistration(session).register("myfn", routed.udf(add_one, returnType=LongType()))
    # Upstream took the local-build path: our sidecar was never consulted...
    assert registry.get_sidecar("3.13")._builders == {}
    # ...and the command it will send carries THIS kernel's Python version.
    assert session._client.register_udf_calls
    assert session._client.executed == []


def test_register_routes_the_command_and_the_stamp_through_the_sidecar():
    builders = _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()

    def add_one(x):
        return x + 1

    result = UDFRegistration(session).register("myfn", routed.udf(add_one, returnType=LongType()))

    # Upstream's local-rebuild path must NOT have been taken.
    assert session._client.register_udf_calls == []

    registered = _registered_udf_proto(session._client)
    assert registered.function_name == "myfn"
    assert registered.python_udf.python_ver == "3.13"  # the WORKER's version, truthfully
    assert registered.python_udf.eval_type == PythonEvalType.SQL_BATCHED_UDF
    # The command bytes are the SIDECAR's, byte for byte -- not a local pickle
    # wearing a borrowed version string.
    builder = builders["4.1.1"]
    assert len(builder.commands) == 1
    assert registered.python_udf.command == builder.commands[0]
    assert result.evalType == PythonEvalType.SQL_BATCHED_UDF


def test_register_accepts_a_plain_function_and_a_ddl_return_type():
    _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()

    def add_one(x):
        return x + 1

    UDFRegistration(session).register("myfn", add_one, "long")

    registered = _registered_udf_proto(session._client)
    assert registered.python_udf.python_ver == "3.13"
    # The DDL string was resolved against the server, then shipped as a real type.
    assert ("ddl_parse", {"ddl_string": "long"}) in session._client.analyze_calls
    from pyspark.sql.connect.types import proto_schema_to_pyspark_data_type

    assert proto_schema_to_pyspark_data_type(registered.python_udf.output_type) == LongType()


def test_register_defaults_to_string_when_no_return_type_is_given():
    _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()

    UDFRegistration(session).register("myfn", lambda x: x)

    registered = _registered_udf_proto(session._client)
    from pyspark.sql.connect.types import proto_schema_to_pyspark_data_type

    assert proto_schema_to_pyspark_data_type(registered.python_udf.output_type) == StringType()


def test_register_reuses_the_routed_udfs_own_expression_and_command_cache():
    """Registering a UDF already applied to a DataFrame must not rebuild it.

    The wrapper reaches the `SidecarUserDefinedFunction` through `_unwrapped`, so
    the sidecar command cache is shared with the DataFrame-API applications.
    """
    builders = _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()

    def add_one(x):
        return x + 1

    my_udf = routed.udf(add_one, returnType=LongType())
    my_udf("c")._expr.to_plan_udf(session._client)  # first build
    UDFRegistration(session).register("myfn", my_udf)

    assert len(builders["4.1.1"].requests) == 1  # built once, reused


def test_register_routes_a_pandas_udf_with_its_own_eval_type():
    _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()

    def double(s):
        return s * 2

    UDFRegistration(session).register("myfn", routed.pandas_udf(double, returnType=LongType()))

    registered = _registered_udf_proto(session._client)
    assert registered.python_udf.eval_type == PythonEvalType.SQL_SCALAR_PANDAS_UDF
    assert registered.python_udf.python_ver == "3.13"


def test_register_routes_an_upstream_built_udf_too():
    """Someone who imported `pyspark.sql.functions.udf` directly still gets routed."""
    _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()
    from pyspark.sql.connect.functions import udf as upstream_udf

    def add_one(x):
        return x + 1

    UDFRegistration(session).register("myfn", upstream_udf(add_one, returnType=LongType()))

    registered = _registered_udf_proto(session._client)
    assert registered.python_udf.python_ver == "3.13"
    assert session._client.register_udf_calls == []


def test_register_on_a_matched_engine_is_left_to_upstream():
    session = _matched_session()
    routed.install_udf_register_routing()

    def add_one(x):
        return x + 1

    UDFRegistration(session).register("myfn", add_one, "long")

    # Upstream's own local-build path, untouched.
    assert len(session._client.register_udf_calls) == 1
    assert session._client.executed == []


def test_register_leaves_upstreams_own_validation_errors_to_upstream():
    from pyspark.errors import PySparkTypeError

    _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()
    registration = UDFRegistration(session)

    # A return type alongside a UDF object -> CANNOT_SPECIFY_RETURN_TYPE_FOR_UDF.
    with pytest.raises(PySparkTypeError):
        registration.register("myfn", routed.udf(lambda x: x, returnType=LongType()), "long")

    # An eval type `register` does not accept -> INVALID_UDF_EVAL_TYPE.
    class _GroupedMapLike:
        func = staticmethod(lambda x: x)
        returnType = LongType()  # noqa: N815 - mirrors pyspark's own name
        evalType = (
            PythonEvalType.SQL_GROUPED_MAP_PANDAS_UDF
        )  # noqa: N815 - mirrors pyspark's own name
        deterministic = True

        def asNondeterministic(self):  # noqa: N802 - mirrors pyspark's own name
            return self

    with pytest.raises(PySparkTypeError):
        registration.register("myfn", _GroupedMapLike())

    assert session._client.executed == []


@pytest.mark.parametrize(
    "missing",
    [
        "_execute_plan_request_with_metadata",
        "_execute",
        "register_function",
        "to_plan_udf",
    ],
)
def test_register_refuses_loudly_when_the_request_plumbing_is_missing(missing, monkeypatch):
    """No silent mis-registration: if the private plumbing moved, say so, early.

    Routing `register` leans on FOUR private pyspark surfaces, and every one of
    them must fail the same way -- with `UDFUnsupportedError` naming the supported
    path -- rather than with a raw `AttributeError` from inside `register`. So each
    is removed in turn and checked identically.
    """
    _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()

    if missing == "register_function":
        # A protobuf field cannot be deleted, so stand `proto.Command` up as
        # something that simply does not carry the field.
        monkeypatch.setattr(routed.proto, "Command", lambda: object())
    elif missing == "to_plan_udf":
        monkeypatch.delattr(routed.CommonInlineUserDefinedFunction, missing)
    else:
        monkeypatch.delattr(_FakeClient, missing)

    with pytest.raises(UDFUnsupportedError) as excinfo:
        UDFRegistration(session).register("myfn", lambda x: x, "long")
    message = str(excinfo.value)
    assert "spark.udf.register" in message
    assert "DataFrame API" in message
    # Refused BEFORE anything was sent, so nothing mis-stamped was registered.
    assert session._client.executed == []


def test_register_returns_the_callers_own_udf_object_like_upstream():
    """`spark.udf.register(name, u) is u`, on a mismatched engine as on a matched one.

    Upstream's UDF-object branch returns the caller's `f` itself; only its
    plain-callable branch builds a fresh `_wrapped()`. Returning our own wrapper
    for the first case would silently flip a caller's `is` check the moment the
    engine mismatched.
    """
    _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()

    def add_one(x):
        return x + 1

    my_udf = routed.udf(add_one, returnType=LongType())
    assert UDFRegistration(session).register("myfn", my_udf) is my_udf

    # Same identity contract as upstream on a matched engine, for comparison.
    matched = _matched_session()
    assert UDFRegistration(matched).register("myfn", my_udf) is my_udf

    # The plain-callable branch still returns a fresh wrapped UDF, as upstream does.
    plain = UDFRegistration(session).register("otherfn", add_one, "long")
    assert plain is not add_one
    assert plain.evalType == PythonEvalType.SQL_BATCHED_UDF


def test_register_on_an_unregistered_client_is_left_to_upstream():
    """A session the SDK knows nothing about must behave exactly as before."""
    routed.install_udf_register_routing()
    session = SparkSession(_FakeClient("stranger"), "3.5.6")  # never register_session'd

    UDFRegistration(session).register("myfn", lambda x: x, "long")
    assert len(session._client.register_udf_calls) == 1


def test_install_register_routing_is_idempotent_and_restorable():
    original = UDFRegistration.register
    assert routed.install_udf_register_routing() is True
    wrapped = UDFRegistration.register
    assert wrapped is not original
    assert routed.install_udf_register_routing() is False  # no double wrap
    assert UDFRegistration.register is wrapped
    routed.uninstall_udf_register_routing()
    assert UDFRegistration.register is original


def test_install_udf_interceptor_also_installs_register_routing():
    original = UDFRegistration.register
    routed.install_udf_interceptor({}, _matched_session())
    assert UDFRegistration.register is not original
    assert getattr(UDFRegistration.register, "_smus_register_routing", False)


# -- string DDL return types ---------------------------------------------- #


def test_a_string_ddl_return_type_is_resolved_against_the_server():
    """`_resolved_output_type`'s DDL branch: `udf(f, "long")` ships UnparsedDataType.

    A string return type is the shape `udf` takes by default from most callers, so
    this branch is on the common path and needs real coverage.
    """
    _register()
    session = _mismatched_session()

    def f(x):
        return x

    from pyspark.sql.connect.types import proto_schema_to_pyspark_data_type

    plan = routed.udf(f, returnType="long")("c")._expr.to_plan_udf(session._client)
    assert session._client.analyze_calls == [("ddl_parse", {"ddl_string": "long"})]
    assert proto_schema_to_pyspark_data_type(plan.python_udf.output_type) == LongType()
    # The sidecar was given the RESOLVED type, not the DDL string.
    assert json.loads(
        registry.get_sidecar("3.13").builder("4.1.1").requests[0]["return_type_json"]
    ) == json.loads(LongType().json())


# -- a SEEN-but-unparsable mismatch --------------------------------------- #


def _mismatched_unknown_session():
    """A connection whose engine reported a mismatch we could not parse.

    No override: the probe runs and trips the engine's own
    PYTHON_VERSION_MISMATCH in wording the SDK's regex does not recognise, and no
    Glue manager is available to name the worker.
    """
    session = SparkSession(_FakeClient("mystery"), "4.1.1")

    def _boom(_n):
        raise RuntimeError("[PYTHON_VERSION_MISMATCH] unrecognised wording")

    session.range = _boom
    rt.register_session(session)
    return session


def test_a_seen_but_unparsable_mismatch_raises_at_build_time():
    """Never the local build: we know it is mismatched, we just do not know into what."""
    _register()
    session = _mismatched_unknown_session()
    runtime = rt.resolve_for_client(session._client)
    assert runtime.is_mismatched_unknown and runtime.matches_client() is False

    def f(x):
        return x

    with pytest.raises(UDFRegistrationError) as excinfo:
        routed.udf(f, returnType=StringType())("c")._expr.to_plan_udf(session._client)
    message = str(excinfo.value)
    assert "could not be determined" in message
    assert "set_override" in message  # names a way out
    # No sidecar was picked, because none could be picked truthfully.
    assert registry.get_sidecar("3.13")._builders == {}


# -- installing routing must not realise a lazy session ------------------- #


def test_installing_routing_over_a_lazy_session_does_not_create_the_spark_session():
    """Kernel start must stay cheap: installing routing may not build a Glue session.

    `register_session` reaches for the session's `_client`.
    `LazySparkSession.__getattr__` creates the underlying session on ANY attribute
    access, so a plain `getattr(spark, "_client", None)` there made merely
    installing the routing at kernel start create a Glue session -- expensive, and
    with the failure swallowed at debug level so nobody saw it. It is also
    redundant: `_get_spark()` registers the real session itself
    (`lazy_spark_session.py`), once it exists.
    """
    from unittest.mock import MagicMock

    from sagemaker_studio.utils.spark.session.lazy_spark_session import LazySparkSession
    from sagemaker_studio.utils.udf import inline_guard

    calls = []

    class _Tripwire(LazySparkSession):
        def _get_spark(self):
            calls.append("_get_spark")
            raise AssertionError("installing routing must not create the Spark session")

    lazy = _Tripwire(session_manager=MagicMock())

    routed.install_udf_interceptor({}, lazy)
    inline_guard.install_inline_guard(lazy)
    try:
        assert calls == []
        # Nothing was registered either, because there is no client to key on yet.
        assert len(rt._CONTEXTS) == 0
    finally:
        inline_guard.uninstall_inline_guard()


# -- declared capabilities are enforced ------------------------------------ #


def test_a_sidecar_that_does_not_advertise_pandas_udf_refuses_pandas_udfs():
    """`capabilities` was logged and never consulted -- a check-shaped no-op.

    A sidecar advertising only ["udf"] still received pandas_udf requests and
    failed somewhere inside its own build. Now it fails here, naming the
    capability.
    """
    builders = {}
    registry.register_sidecar(
        "3.13",
        lambda sv: builders.setdefault(sv, _FakeBuilder("3.13", sv)),
        capabilities=["udf"],
    )
    session = _mismatched_session()

    def double(s):
        return s * 2

    with pytest.raises(UDFUnsupportedError) as excinfo:
        routed.pandas_udf(double, returnType=LongType())("c")._expr.to_plan_udf(session._client)
    message = str(excinfo.value)
    assert "pandas_udf" in message
    assert "['udf']" in message

    # A plain scalar udf, which it DOES advertise, still works on the same sidecar.
    plan = routed.udf(lambda x: x, returnType=LongType())("c")._expr.to_plan_udf(session._client)
    assert plan.python_udf.python_ver == "3.13"


def test_the_default_capabilities_cover_both_factories():
    builders = {}
    registry.register_sidecar("3.13", lambda sv: builders.setdefault(sv, _FakeBuilder("3.13", sv)))
    session = _mismatched_session()

    assert registry.get_sidecar("3.13").capabilities == list(registry.DEFAULT_CAPABILITIES)
    routed.udf(lambda x: x, returnType=LongType())("c")._expr.to_plan_udf(session._client)
    routed.pandas_udf(lambda s: s, returnType=LongType())("c")._expr.to_plan_udf(session._client)


# -- callables that can never yield source text ---------------------------- #


def test_a_functools_partial_is_refused_at_definition_time():
    """It used to pass eager validation and fail at `.show()`."""
    import functools

    _register()
    _mismatched_session()

    def add(a, b):
        return a + b

    with pytest.raises(UDFRegistrationError) as excinfo:
        routed.udf(functools.partial(add, 1), returnType=LongType())
    assert "functools.partial" in str(excinfo.value)


def test_an_exec_defined_function_with_no_source_on_record_is_refused_eagerly():
    _register()
    _mismatched_session()

    namespace = {}
    exec(compile("def f(x):\n    return x\n", "<string>", "exec"), namespace)

    with pytest.raises(UDFRegistrationError) as excinfo:
        routed.udf(namespace["f"], returnType=LongType())
    assert "cannot be read" in str(excinfo.value)


def test_a_function_whose_source_is_only_in_linecache_is_still_accepted():
    """A notebook cell lives in `linecache`, so the check must not reject it.

    This is the exact shape IPython produces; rejecting it would break every
    notebook UDF.
    """
    import linecache

    _register()
    session = _mismatched_session()

    source = "def cell_udf(x):\n    return x + 1\n"
    filename = "<ipython-input-1-abcdef>"
    linecache.cache[filename] = (len(source), None, source.splitlines(True), filename)
    namespace = {}
    exec(compile(source, filename, "exec"), namespace)

    plan = routed.udf(namespace["cell_udf"], returnType=LongType())("c")._expr.to_plan_udf(
        session._client
    )
    assert plan.python_udf.python_ver == "3.13"


# -- `routed` / `python_ver` on the UDF object ------------------------------ #
#
# The POC exposed these because it built the sidecar command EAGERLY, at UDF
# construction. Production builds lazily and per DataFrame, so these tests pin
# both halves of the replacement: a prediction that costs nothing, and a refresh
# from the sidecar's own answer once a real decision has been made.


def test_a_mismatched_engine_predicts_routing_without_building_anything():
    builders = _register()
    # Bound: a context whose session has been collected can no longer describe an
    # engine, and `resolve_current()` deliberately skips it.
    session = _mismatched_session()  # noqa: F841

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=LongType())

    assert my_udf.routed is True
    assert my_udf.python_ver == "3.13"
    # Reading them built nothing: the sidecar FACTORY was never even invoked, so
    # there is no builder that could have been asked for a command.
    assert builders == {}
    assert registry.get_sidecar("3.13")._builders == {}


def test_a_matched_engine_reports_not_routed_and_the_clients_own_version():
    _register()
    session = _matched_session()  # noqa: F841

    my_udf = routed.udf(lambda x: x, returnType=LongType())

    assert my_udf.routed is False
    assert my_udf.python_ver == CLIENT_PY


def test_a_mismatched_engine_with_no_sidecar_registered_does_not_claim_routing():
    """`routed` promises a sidecar build. With none registered there is none."""
    session = _mismatched_session()  # noqa: F841

    my_udf = routed.udf(lambda x: x, returnType=LongType())

    assert my_udf.routed is False
    assert my_udf.python_ver == CLIENT_PY


@pytest.mark.parametrize("factory_name", ["udf", "pandas_udf"])
def test_the_call_form_and_the_decorator_form_both_carry_the_attributes(factory_name):
    _register()
    session = _mismatched_session()  # noqa: F841
    factory = getattr(routed, factory_name)

    called = factory(lambda x: x, returnType=LongType())

    @factory(returnType=LongType())
    def decorated(x):
        return x

    for udf_object in (called, decorated):
        assert udf_object.routed is True, factory_name
        assert udf_object.python_ver == "3.13", factory_name


def test_as_nondeterministic_keeps_the_attributes():
    """`asNondeterministic()` builds a FRESH wrapper; it must describe the route too."""
    _register()
    session = _mismatched_session()  # noqa: F841

    my_udf = routed.udf(lambda x: x, returnType=LongType()).asNondeterministic()

    assert my_udf.routed is True
    assert my_udf.python_ver == "3.13"


def test_the_object_register_returns_carries_the_attributes():
    _register()
    session = _mismatched_session()
    routed.install_udf_register_routing()

    def add_one(x):
        return x + 1

    # Plain callable: upstream's contract is a fresh wrapped UDF.
    plain = UDFRegistration(session).register("myfn", add_one, "long")
    assert plain.routed is True
    assert plain.python_ver == "3.13"

    # A UDF object: the caller's OWN object comes back, and describes the route.
    mine = routed.udf(add_one, returnType=LongType())
    assert UDFRegistration(session).register("minefn", mine) is mine
    assert mine.routed is True
    assert mine.python_ver == "3.13"

    # Including one built by upstream's own factory.
    from pyspark.sql.connect.functions import udf as upstream_udf

    theirs = upstream_udf(add_one, returnType=LongType())
    UDFRegistration(session).register("theirfn", theirs)
    assert theirs.routed is True
    assert theirs.python_ver == "3.13"


def test_register_on_a_matched_engine_reports_the_local_build():
    session = _matched_session()
    routed.install_udf_register_routing()

    registered = UDFRegistration(session).register("myfn", lambda x: x, "long")

    assert registered.routed is False
    assert registered.python_ver == CLIENT_PY


def test_a_real_route_replaces_the_prediction_with_what_actually_happened():
    """Per-DataFrame routing: the attributes report the MOST RECENT decision.

    The matched engine is registered last, so the prediction is made against it;
    applying the UDF to the mismatched engine and back again must move the
    attributes each time, which no static snapshot taken at definition time could
    do.
    """
    _register()
    mismatched = _mismatched_session()
    matched = _matched_session()

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=LongType())
    assert my_udf.routed is False  # predicted against the matched engine

    my_udf("c")._expr.to_plan_udf(mismatched._client)
    assert my_udf.routed is True
    assert my_udf.python_ver == "3.13"

    my_udf("c")._expr.to_plan_udf(matched._client)
    assert my_udf.routed is False
    assert my_udf.python_ver == CLIENT_PY


def test_a_sidecar_reporting_a_different_python_ver_wins_but_warns(caplog):
    """A disagreement here is a genuine fidelity bug, so it may not pass silently.

    The proto has to carry the version of the interpreter that actually pickled
    the command -- it is what the worker's own `check_python_version` compares
    against -- so the sidecar's answer is authoritative. But a sidecar registered
    for 3.13 answering "3.12" means the registration is lying about which
    interpreter it runs, and overwriting the prediction without a trace would hide
    exactly that.
    """
    builders = {}

    def factory(spark_version):
        builders[spark_version] = _FakeBuilder("3.12", spark_version)
        return builders[spark_version]

    registry.register_sidecar("3.13", factory)
    session = _mismatched_session()

    def f(x):
        return x

    my_udf = routed.udf(f, returnType=LongType())
    assert my_udf.python_ver == "3.13"  # predicted from the engine's resolution

    with caplog.at_level(logging.WARNING, logger="SparkConnect"):
        plan = my_udf("c")._expr.to_plan_udf(session._client)

    assert plan.python_udf.python_ver == "3.12"  # the sidecar's own answer ships
    assert my_udf.routed is True
    assert my_udf.python_ver == "3.12"  # ...and is what a later read reports
    warnings = [r.getMessage() for r in caplog.records if r.levelno >= logging.WARNING]
    assert any("3.12" in message and "3.13" in message for message in warnings), warnings


def test_reading_the_attributes_over_a_lazy_session_does_not_create_it():
    """The laziness contract again, for the attribute path specifically.

    `resolve_current()` only sees sessions REGISTERED with the resolver, and a
    still-lazy `LazySparkSession` cannot be registered (it has no `_client` to key
    on), so nothing here may reach `_get_spark`.
    """
    from unittest.mock import MagicMock

    from sagemaker_studio.utils.spark.session.lazy_spark_session import LazySparkSession

    _register()
    calls = []

    class _Tripwire(LazySparkSession):
        def _get_spark(self):
            calls.append("_get_spark")
            raise AssertionError("reading route attributes must not create the Spark session")

    lazy = _Tripwire(session_manager=MagicMock())
    namespace = {}
    routed.install_udf_interceptor(namespace, lazy)

    my_udf = namespace["udf"](lambda x: x, returnType=LongType())
    assert my_udf.routed is False  # nothing is resolvable, so nothing is claimed
    assert my_udf.python_ver == CLIENT_PY
    assert calls == []
    assert len(rt._CONTEXTS) == 0


# -- the user's own notebook cells, end to end ----------------------------- #


class _CellRow:
    """A ``Row``-alike, so the cells' ``r.y`` reads as it does in the notebook."""

    def __init__(self, name, value):
        setattr(self, name, value)


class _CellResult:
    def __init__(self, name, values):
        self._name = name
        self._values = values

    def collect(self):
        return [_CellRow(self._name, value) for value in self._values]

    def show(self):
        print(self._name)
        for value in self._values:
            print(value)


class _CellDataFrame:
    """Just enough DataFrame to run the notebook cells against the fake sidecar.

    ``select`` builds the REAL plan through :meth:`SidecarPythonUDF.to_plan` -- so
    the routing decision, the sidecar request and the command bytes are the
    production ones -- and then EVALUATES the command the plan carries. That is
    what makes the cells' ``assert [r.y for r in df.collect()] == [1, 2, 3]`` a
    statement about the routed command: the function being called is the one the
    sidecar rebuilt from source and cloudpickled, unpickled straight out of the
    proto.
    """

    def __init__(self, client, values):
        self._client = client
        self._values = values

    def select(self, column):
        from pyspark.serializers import CloudPickleSerializer

        name, expr = _unalias(column)
        plan = expr.to_plan_udf(self._client)
        func, _return_type = CloudPickleSerializer().loads(plan.python_udf.command)
        if plan.python_udf.eval_type in routed._PANDAS_EVAL_TYPES:
            import pandas as pd

            results = list(func(pd.Series(self._values)))
        else:
            results = [func(value) for value in self._values]
        return _CellResult(name, results)


def _unalias(column):
    """``plus_one("id").alias("y")`` -> ``("y", <the UDF expression>)``."""
    expr = column._expr
    parent = getattr(expr, "_parent", None)
    if parent is None:
        return "value", expr
    return expr._alias[0], parent


class _CellSession(SparkSession):
    """The notebook's session (the cells call it ``sparktest``)."""

    def range(self, start, end=None):
        values = list(range(start)) if end is None else list(range(start, end))
        return _CellDataFrame(self._client, values)


def test_the_two_notebook_cells_the_user_runs(capsys, monkeypatch):
    """The end-to-end cells, verbatim -- including the ``print``.

    These attributes exist FOR that print: the POC had them, the production
    rewrite dropped them, and this is the shape the user validated. Kept as one
    test rather than split so the cells stay copy-pasteable in both directions.

    ``SPARK_CONNECT_MODE_ENABLED`` is what a Connect notebook runs with, and it
    matters here: `pandas_udf` lives in `pyspark.sql.pandas.functions`, which
    branches on `is_remote()` and only then builds a CONNECT UDF whose DDL return
    type stays unparsed. Without it, upstream tries to parse `"long"` through a
    JVM this process does not have -- so the cell's own `@pandas_udf("long")`
    would fail in upstream code, before any routing.
    """
    monkeypatch.setenv("SPARK_CONNECT_MODE_ENABLED", "1")
    _register()
    session = _CellSession(_FakeClient("glue6"), "4.1.1")
    rt.register_session(session)
    namespace = {}
    routed.install_udf_interceptor(namespace, session)
    udf = namespace["udf"]
    pandas_udf = namespace["pandas_udf"]
    sparktest = session

    # `spark.set_engine_python_version_override("3.13")`: LazySparkSession
    # forwards to exactly this, one layer down (lazy_spark_session.py).
    rt.set_override(session, "3.13")

    # -- cell 1 ------------------------------------------------------------- #
    @udf("long")
    def plus_one(x):
        return (x or 0) + 1

    print("routed via sidecar:", plus_one.routed, "| proto python_ver:", plus_one.python_ver)
    df = sparktest.range(3).select(plus_one("id").alias("y"))
    df.show()
    assert [r.y for r in df.collect()] == [1, 2, 3]
    assert plus_one.routed and plus_one.python_ver == "3.13"

    # -- cell 2 ------------------------------------------------------------- #
    @pandas_udf("long")
    def times_ten(s):
        return s * 10

    print("routed via sidecar:", times_ten.routed, "| proto python_ver:", times_ten.python_ver)
    rows = [r.y for r in sparktest.range(1, 4).select(times_ten("id").alias("y")).collect()]
    assert rows == [10, 20, 30]

    # Both prints reported the route BEFORE anything was applied to a DataFrame.
    printed = capsys.readouterr().out
    assert printed.count("routed via sidecar: True | proto python_ver: 3.13") == 2


# -- best-effort surfaces never take the notebook down -------------------- #
#
# `routed` / `python_ver` are DESCRIPTIVE: reading them must not raise and must
# not create a session. Everything below drives the failure modes of those
# best-effort paths directly.


def _bare_expr():
    """A SidecarPythonUDF with no captured source -- enough to poke the seams."""
    return routed.SidecarPythonUDF(
        StringType(), PythonEvalType.SQL_BATCHED_UDF, lambda x: x, "3.13"
    )


def _udf_obj(func=None):
    """The UDF object itself, not the wrapper `routed.udf` hands back."""
    return routed.SidecarUserDefinedFunction(
        func or (lambda x: x),
        returnType=StringType(),
        name="my_udf",
        evalType=PythonEvalType.SQL_BATCHED_UDF,
        deterministic=True,
    )


def test_predicting_the_route_reports_not_routed_when_resolution_raises(monkeypatch):
    """An attribute read must degrade to "not routed", never propagate."""

    def boom():
        raise RuntimeError("resolver exploded")

    monkeypatch.setattr(routed, "resolve_current", boom)

    assert routed._predict_route() == (False, CLIENT_PY)


def test_predicting_the_route_reports_not_routed_when_no_sidecar_is_registered():
    """A mismatch with nothing registered to serve it is not a route."""
    session = _mismatched_session()
    rt.resolve_for_session(session)

    assert routed._predict_route() == (False, CLIENT_PY)


def test_stamping_route_attributes_onto_an_unwritable_object_is_silent():
    """Some callables have no writable `__dict__`; the stamp is a nicety, not a need."""

    class _Unwritable:
        __slots__ = ()

    routed._stamp_route(_Unwritable(), True, "3.13")  # must not raise


def test_comparing_unparsable_versions_falls_back_to_a_string_compare():
    assert routed._same_minor("3.13", "3.13") is True
    # neither side normalises, so the comparison degrades rather than raising
    assert routed._same_minor("not-a-version", "not-a-version") is True
    assert routed._same_minor("not-a-version", "also-not") is False


def test_the_proto_builder_reprs_its_type_and_function():
    """It appears in plan reprs and error text, so it must not be opaque."""
    assert "SidecarPythonUDF(" in repr(_bare_expr())


def test_a_non_weakreferenceable_wrapper_still_gets_its_prediction():
    """The later refresh needs a weakref; without one the prediction still stands."""
    _register()
    # keep the session alive: the registry holds only a weakref, so a collected
    # session makes `resolve_current()` correctly report nothing to route to
    session = _mismatched_session()
    rt.resolve_for_session(session)

    class _Unreferenceable:
        __slots__ = ("routed", "python_ver")

    wrapper = _Unreferenceable()
    _udf_obj()._track_wrapper(wrapper)  # must not raise

    assert wrapper.routed is True
    assert wrapper.python_ver == "3.13"


def test_installing_the_interceptor_survives_a_session_that_cannot_be_registered():
    """Pre-registration is a convenience; the namespace install must still happen.

    Routing is decided per DataFrame, so a session that blows up on `_client`
    costs nothing but the head start.
    """

    class _HostileSession:
        @property
        def _client(self):
            raise RuntimeError("session is half-built")

    namespace = {}
    installed = routed.install_udf_interceptor(namespace, _HostileSession())

    assert namespace["udf"] is routed.udf
    assert namespace["pandas_udf"] is routed.pandas_udf
    assert set(installed) == {"udf", "pandas_udf"}


def test_a_failing_register_route_does_not_cost_us_the_udf_path(monkeypatch):
    """The udf/pandas_udf install is the main event; register routing is extra."""

    def boom():
        raise RuntimeError("pyspark moved UDFRegistration")

    monkeypatch.setattr(routed, "install_udf_register_routing", boom)

    namespace = {}
    installed = routed.install_udf_interceptor(namespace, _matched_session())

    assert set(installed) == {"udf", "pandas_udf"}
    assert namespace["udf"] is routed.udf


def test_registering_through_a_clientless_session_delegates_and_still_describes():
    """A still-lazy session has no client, so there is no engine to route to yet.

    Upstream registers it locally and the returned object must still carry the
    route attributes, or `.routed` would be missing exactly where a user looks.
    Drives `_routed_register` with a stub upstream: on this branch upstream's real
    `register` would need the very client we are asserting is absent.
    """
    upstream_calls = []

    def fake_original(self, name, f, returnType=None):  # noqa: N803 - mirrors pyspark
        upstream_calls.append((name, returnType))
        return lambda *a: None

    class _ClientlessSession:
        """No `_client` anywhere -- models a session that is still lazy."""

    class _Registration:
        sparkSession = _ClientlessSession()  # noqa: N815 - mirrors pyspark's own name

    registered = routed._routed_register(fake_original)(_Registration(), "add_one", len, "long")

    assert upstream_calls == [("add_one", "long")], "upstream must do the registering"
    assert registered.routed is False
    assert registered.python_ver == CLIENT_PY
