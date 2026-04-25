import asyncio
import copy
import importlib
import re
import sys
import textwrap
import threading
import types
from concurrent import futures
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any, Iterator, List, Optional, cast

import grpc
import pytest
from isolate.backends.settings import IsolateSettings
from isolate.connections.grpc.configuration import get_default_options
from isolate.logs import Log, LogLevel, LogSource
from isolate.server import definitions, health
from isolate.server.health_server import HealthServicer
from isolate.server.interface import from_grpc, to_serialized_object
from isolate.server.server import (
    BridgeManager,
    ControllerAuthInterceptor,
    IsolateServicer,
    ServerBoundInterceptor,
    SingleTaskInterceptor,
)

REPO_DIR = Path(__file__).parent.parent
assert (
    REPO_DIR.exists() and REPO_DIR.name == "isolate"
), "This test should have access to isolate as an installable package."


def inherit_from_local(monkeypatch: Any, value: bool = True) -> None:
    """Enables the inherit from local mode for the isolate server."""
    monkeypatch.setattr("isolate.server.server.INHERIT_FROM_LOCAL", value)


# gRPC C core on macOS emits log lines to stderr after fork(),
# polluting captured user logs. Examples:
#   I0404 01:07:18.985849 331910 ev_poll_posix.cc:593] FD from fork ...
#   I0404 01:13:01.344279 380102 chttp2_transport.cc:1369] Got goaway ...
_GRPC_CORE_RE = re.compile(
    r"^[IWED]\d{4} "  # gRPC log level + MMDD
    r"\d{2}:\d{2}:\d{2}\.\d+\s+"  # timestamp
    r"\d+\s+"  # PID
    r"\S+\.cc:\d+\]"  # source.cc:line]
)


def _filter_grpc_noise(logs: List[Log]) -> List[Log]:
    return [log for log in logs if log.message and not _GRPC_CORE_RE.match(log.message)]


@dataclass
class Stubs:
    isolate_stub: definitions.IsolateStub
    health_stub: health.HealthStub


@pytest.fixture
def interceptors():
    return []


@contextmanager
def make_server(
    tmp_path: Path, interceptors: Optional[List[ServerBoundInterceptor]] = None
) -> Iterator[Stubs]:
    interceptors = interceptors or []
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=1),
        options=get_default_options(),
        interceptors=interceptors,  # type: ignore
    )

    for interceptor in interceptors:
        interceptor.register_server(server)

    test_settings = IsolateSettings(cache_dir=tmp_path / "cache")
    with BridgeManager() as bridge:
        servicer = IsolateServicer(bridge, test_settings)

        for interceptor in interceptors:
            interceptor.register_servicer(servicer)

        definitions.register_isolate(servicer, server)
        health.register_health(HealthServicer(), server)
        host, port = "localhost", server.add_insecure_port("[::]:0")
        server.start()

        try:
            isolate_stub = definitions.IsolateStub(
                grpc.insecure_channel(
                    f"{host}:{port}",
                    options=get_default_options(),
                )
            )

            health_stub = health.HealthStub(
                grpc.insecure_channel(
                    f"{host}:{port}",
                    options=get_default_options(),
                )
            )

            yield Stubs(isolate_stub=isolate_stub, health_stub=health_stub)
        finally:
            server.stop(None)
            servicer.cancel_tasks()


@pytest.fixture
def stub(tmp_path, interceptors):
    with make_server(tmp_path, interceptors) as stubs:
        yield stubs.isolate_stub


@pytest.fixture
def health_stub(tmp_path, interceptors):
    with make_server(tmp_path, interceptors) as stubs:
        yield stubs.health_stub


def define_environment(kind: str, **kwargs: Any) -> definitions.EnvironmentDefinition:
    struct = definitions.Struct()
    struct.update(kwargs)

    return definitions.EnvironmentDefinition(
        kind=kind,
        configuration=struct,
    )


_NOT_SET = object()


class LegacyCallableProto:
    """Simulate the pre-oneof / pre-optional-bool generated protobuf API."""

    def __init__(
        self,
        *,
        function: bool = False,
        entrypoint: bool = False,
        run_on_main_thread: bool = False,
        supports_entrypoint: bool = True,
    ) -> None:
        self.run_on_main_thread = run_on_main_thread
        self._has_field = {
            "function": function,
            "entrypoint": entrypoint,
        }
        self._supports_entrypoint = supports_entrypoint

    def WhichOneof(self, name: str) -> Optional[str]:
        raise ValueError(f'Protocol message FunctionCall has no "{name}" field.')

    def HasField(self, name: str) -> bool:
        if name == "run_on_main_thread":
            raise ValueError(
                "Field FunctionCall.run_on_main_thread does not have presence."
            )
        if name == "entrypoint" and not self._supports_entrypoint:
            raise ValueError('Protocol message FunctionCall has no "entrypoint" field.')
        try:
            return self._has_field[name]
        except KeyError as exc:
            raise ValueError(
                f'Protocol message FunctionCall has no "{name}" field.'
            ) from exc


def run_request(
    stub: definitions.IsolateStub,
    request: definitions.BoundFunction,
    *,
    stream_logs: bool = True,
    build_logs: Optional[List[Log]] = None,
    bridge_logs: Optional[List[Log]] = None,
    user_logs: Optional[List[Log]] = None,
) -> definitions.SerializedObject:
    log_store = {
        LogSource.BUILDER: build_logs if build_logs is not None else [],
        LogSource.BRIDGE: bridge_logs if bridge_logs is not None else [],
        LogSource.USER: user_logs if user_logs is not None else [],
    }

    request.stream_logs = stream_logs

    return_value = _NOT_SET
    for result in stub.Run(request):
        for _log in result.logs:
            log = from_grpc(_log)
            log_store[log.source].append(log)

        if result.is_complete:
            if return_value is _NOT_SET:
                return_value = result.result
            else:
                raise ValueError("Sent the result twice")

    if return_value is _NOT_SET:
        raise ValueError("Never sent the result")
    else:
        return cast(definitions.SerializedObject, return_value)


def prepare_request(
    function: Any,
    *args: Any,
    run_on_main_thread: Optional[bool] = None,
    **kwargs: Any,
) -> definitions.BoundFunction:
    import dill

    import __main__

    dill.settings["recurse"] = True

    # Make it seem like it originated from __main__
    setattr(__main__, function.__name__, function)
    function.__module__ = "__main__"
    function.__qualname__ = f"__main__.{function.__name__}"

    basic_function = partial(function, *args, **kwargs)
    if getattr(function, "_run_on_main_thread", False):
        setattr(basic_function, "_run_on_main_thread", True)
    environment = define_environment("virtualenv", requirements=[])
    request = definitions.BoundFunction(
        function=to_serialized_object(basic_function, method="dill"),
        environments=[environment],
    )
    if run_on_main_thread is not None:
        request.run_on_main_thread = run_on_main_thread
    return request


def run_function(stub, function, *args, log_handler=None, **kwargs):
    request = prepare_request(function, *args, **kwargs)

    user_logs: List[Log] = [] if log_handler is None else log_handler
    result = run_request(stub, request, user_logs=user_logs)

    filtered = _filter_grpc_noise(user_logs)
    raw_user_logs = [log.message for log in filtered if log.message]
    return from_grpc(result), raw_user_logs


@pytest.mark.parametrize("inherit_local", [True, False])
def test_server_basic_communication(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
    inherit_local: bool,
) -> None:
    inherit_from_local(monkeypatch, inherit_local)
    requirements = ["pyjokes==0.6.0"]
    if not inherit_local:
        # The agent process needs dill (and isolate) to actually
        # deserialize the given function, so they need to be installed
        # when we are not inheriting the local environment.
        requirements.append("dill==0.3.5.1")
        requirements.append(f"{REPO_DIR}")

    env_definition = define_environment("virtualenv", requirements=requirements)
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(
                eval,
                "__import__('pyjokes').__version__",
            ),
            method="dill",
        ),
        environments=[env_definition],
    )

    raw_result = run_request(stub, request)
    assert from_grpc(raw_result) == "0.6.0"


def test_server_entrypoint(stub: definitions.IsolateStub, monkeypatch: Any) -> None:
    """Running a BoundFunction with entrypoint resolves via importlib
    in the agent, skipping pickling entirely."""
    import os

    inherit_from_local(monkeypatch)

    env_definition = define_environment("virtualenv", requirements=[])
    request = definitions.BoundFunction(
        entrypoint="os:getpid",
        environments=[env_definition],
    )

    raw_result = run_request(stub, request)
    result = from_grpc(raw_result)

    # os.getpid runs in the agent subprocess, so the pid is a valid int
    # different from the test process's pid.
    assert isinstance(result, int)
    assert result > 0
    assert result != os.getpid()


def test_server_entrypoint_honors_legacy_main_thread_flag(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    inherit_from_local(monkeypatch)

    package_dir = tmp_path / "entrypoint_main_thread_test_pkg"
    package_dir.mkdir()

    (package_dir / "setup.py").write_text(
        textwrap.dedent(
            """
            from setuptools import setup


            setup(py_modules=["entrypoint_main_thread_test"])
            """
        )
    )
    (package_dir / "entrypoint_main_thread_test.py").write_text(
        textwrap.dedent(
            """
            import threading


            def should_fail_on_main_thread():
                if threading.current_thread() == threading.main_thread():
                    raise RuntimeError("should fail on main thread")
                return "should succeed on non-main thread"


            should_fail_on_main_thread._run_on_main_thread = True
            """
        )
    )

    env_definition = define_environment(
        "virtualenv",
        requirements=[str(package_dir)],
    )
    request = definitions.BoundFunction(
        entrypoint="entrypoint_main_thread_test:should_fail_on_main_thread",
        environments=[env_definition],
    )

    raw_result = run_request(stub, request)
    with pytest.raises(RuntimeError, match="should fail on main thread"):
        from_grpc(raw_result)


def test_server_entrypoint_explicit_false_overrides_legacy_main_thread_flag(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    inherit_from_local(monkeypatch)

    package_dir = tmp_path / "entrypoint_main_thread_override_test_pkg"
    package_dir.mkdir()

    (package_dir / "setup.py").write_text(
        textwrap.dedent(
            """
            from setuptools import setup


            setup(py_modules=["entrypoint_main_thread_override_test"])
            """
        )
    )
    (package_dir / "entrypoint_main_thread_override_test.py").write_text(
        textwrap.dedent(
            """
            import threading


            def should_fail_on_main_thread():
                if threading.current_thread() == threading.main_thread():
                    raise RuntimeError("should fail on main thread")
                return "should succeed on non-main thread"


            should_fail_on_main_thread._run_on_main_thread = True
            """
        )
    )

    env_definition = define_environment(
        "virtualenv",
        requirements=[str(package_dir)],
    )
    request = definitions.BoundFunction(
        entrypoint="entrypoint_main_thread_override_test:should_fail_on_main_thread",
        environments=[env_definition],
        run_on_main_thread=False,
    )

    raw_result = run_request(stub, request)
    assert from_grpc(raw_result) == "should succeed on non-main thread"


def test_agent_import_falls_back_when_settings_constant_missing(
    monkeypatch: Any,
) -> None:
    """Newer agent code may run against an older installed isolate build
    where ``DEFAULT_SERIALIZATION_METHOD`` is not exported yet."""
    import isolate.connections.grpc.agent as agent_module
    from isolate.backends import settings as real_settings
    from isolate.backends.settings import DEFAULT_SETTINGS, IsolateSettings

    fake_settings = types.ModuleType("isolate.backends.settings")
    setattr(fake_settings, "IsolateSettings", IsolateSettings)
    setattr(fake_settings, "DEFAULT_SETTINGS", DEFAULT_SETTINGS)

    try:
        monkeypatch.setitem(sys.modules, "isolate.backends.settings", fake_settings)
        reloaded = importlib.reload(agent_module)
        assert reloaded.DEFAULT_SERIALIZATION_METHOD == "pickle"
    finally:
        monkeypatch.setitem(sys.modules, "isolate.backends.settings", real_settings)
        importlib.reload(agent_module)


def test_agent_import_falls_back_when_common_validator_missing(
    monkeypatch: Any,
) -> None:
    """Newer agent code may run against an older installed isolate build
    where ``validate_entrypoint`` is not exported yet."""
    import isolate.connections.grpc.agent as agent_module
    from isolate.connections import common as real_common
    from isolate.connections.common import SerializationError, serialize_object

    fake_common = types.ModuleType("isolate.connections.common")
    setattr(fake_common, "SerializationError", SerializationError)
    setattr(fake_common, "serialize_object", serialize_object)

    try:
        monkeypatch.setitem(sys.modules, "isolate.connections.common", fake_common)
        reloaded = importlib.reload(agent_module)
        reloaded.validate_entrypoint("os:getpid")
        with pytest.raises(ValueError, match="Invalid entrypoint"):
            reloaded.validate_entrypoint("not_an_entrypoint")
    finally:
        monkeypatch.setitem(sys.modules, "isolate.connections.common", real_common)
        importlib.reload(agent_module)


@pytest.mark.parametrize(
    "module_name",
    [
        "isolate.connections.grpc.agent",
        "isolate.server.server",
    ],
)
def test_callable_kind_falls_back_when_proto_has_no_oneof(module_name: str) -> None:
    module = importlib.import_module(module_name)

    assert module._get_callable_kind(LegacyCallableProto(function=True)) == "function"
    assert (
        module._get_callable_kind(
            LegacyCallableProto(function=True, supports_entrypoint=False)
        )
        == "function"
    )
    assert (
        module._get_callable_kind(LegacyCallableProto(entrypoint=True)) == "entrypoint"
    )
    assert module._get_callable_kind(LegacyCallableProto()) is None


@pytest.mark.parametrize(
    "module_name",
    [
        "isolate.connections.grpc.agent",
        "isolate.server.server",
    ],
)
def test_optional_bool_field_falls_back_when_proto_has_no_presence(
    module_name: str,
) -> None:
    module = importlib.import_module(module_name)

    assert (
        module._get_optional_bool_field(
            LegacyCallableProto(run_on_main_thread=False),
            "run_on_main_thread",
        )
        is None
    )
    assert module._get_optional_bool_field(
        LegacyCallableProto(run_on_main_thread=True),
        "run_on_main_thread",
    )


def test_server_entrypoint_module_not_found(
    stub: definitions.IsolateStub, monkeypatch: Any
) -> None:
    """An unimportable entrypoint surfaces as a raised exception on the
    client side (not an abort), matching the pickle error path."""
    inherit_from_local(monkeypatch)

    env_definition = define_environment("virtualenv", requirements=[])
    request = definitions.BoundFunction(
        entrypoint="isolate_entrypoint_test_missing_xyz:some_attr",
        environments=[env_definition],
    )

    raw_result = run_request(stub, request)
    with pytest.raises(ModuleNotFoundError):
        from_grpc(raw_result)


def test_server_rejects_setup_func_with_entrypoint(
    stub: definitions.IsolateStub, monkeypatch: Any
) -> None:
    """setup_func is only meaningful for the pickled-callable path and the
    combination must be hard-rejected at the server boundary."""
    inherit_from_local(monkeypatch)

    env_definition = define_environment("virtualenv", requirements=[])
    request = definitions.BoundFunction(
        entrypoint="os:getpid",
        setup_func=to_serialized_object(lambda: None, method="cloudpickle"),
        environments=[env_definition],
    )

    with pytest.raises(grpc.RpcError) as exc:
        run_request(stub, request)
    assert exc.match("'setup_func' is not supported together with 'entrypoint'")


def test_server_rejects_neither_function_nor_entrypoint(
    stub: definitions.IsolateStub, monkeypatch: Any
) -> None:
    inherit_from_local(monkeypatch)

    env_definition = define_environment("virtualenv", requirements=[])
    request = definitions.BoundFunction(environments=[env_definition])

    with pytest.raises(grpc.RpcError) as exc:
        run_request(stub, request)
    assert exc.match("One of 'function' or 'entrypoint'")


def test_server_builder_error(stub: definitions.IsolateStub, monkeypatch: Any) -> None:
    inherit_from_local(monkeypatch)

    # $$$$ as a package can't exist on PyPI since PEP 508 explicitly defines
    # what is considered to be a legit package name.
    #
    # https://peps.python.org/pep-0508/#names

    env_definition = define_environment("virtualenv", requirements=["$$$$"])
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(
                eval,
                "__import__('pyjokes').__version__",
            ),
            method="dill",
        ),
        environments=[env_definition],
    )

    build_logs: List[Log] = []
    with pytest.raises(grpc.RpcError) as exc:
        run_request(stub, request, build_logs=build_logs)

    assert "Failure during 'pip install': Command" in exc.value.details()

    raw_logs = [log.message for log in build_logs]
    assert any("ERROR: Invalid requirement: '$$$$'" in raw_log for raw_log in raw_logs)


def test_user_logs_immediate(stub: definitions.IsolateStub, monkeypatch: Any) -> None:
    inherit_from_local(monkeypatch)

    env_definition = define_environment("virtualenv", requirements=["pyjokes==0.6.0"])
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(
                exec,
                textwrap.dedent(
                    """
                import sys, pyjokes
                print(pyjokes.__version__)
                print("error error!", file=sys.stderr)
                print("[debug] error!", file=sys.stderr)
                """
                ),
            ),
            method="dill",
        ),
        environments=[env_definition],
    )

    user_logs: List[Log] = []
    run_request(stub, request, user_logs=user_logs)
    user_logs = _filter_grpc_noise(user_logs)

    assert len(user_logs) == 3

    by_stream = {log.level: log.message for log in user_logs}
    assert by_stream[LogLevel.INFO] == "0.6.0"
    assert by_stream[LogLevel.ERROR] == "error error!"
    assert by_stream[LogLevel.DEBUG] == "[debug] error!"


def test_no_stream_logs(stub: definitions.IsolateStub, monkeypatch: Any) -> None:
    inherit_from_local(monkeypatch)

    env_definition = define_environment("virtualenv", requirements=["pyjokes==0.6.0"])
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(
                exec,
                textwrap.dedent(
                    """
                import sys, pyjokes
                print(pyjokes.__version__)
                print("error error!", file=sys.stderr)
                """
                ),
            ),
            method="dill",
        ),
        environments=[env_definition],
    )

    user_logs: List[Log] = []
    build_logs: List[Log] = []
    bridge_logs: List[Log] = []
    run_request(
        stub,
        request,
        user_logs=user_logs,
        build_logs=build_logs,
        bridge_logs=bridge_logs,
        stream_logs=False,
    )

    assert len(user_logs) == 0
    assert len(build_logs) == 0
    assert len(bridge_logs) == 0


def test_unknown_environment(stub: definitions.IsolateStub, monkeypatch: Any) -> None:
    inherit_from_local(monkeypatch)

    env_definition = define_environment("unknown")
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(
                eval,
                "__import__('pyjokes').__version__",
            ),
            method="dill",
        ),
        environments=[env_definition],
    )

    with pytest.raises(grpc.RpcError) as exc:
        run_request(stub, request)

    assert exc.match("Unknown environment kind")


def test_invalid_param(stub: definitions.IsolateStub, monkeypatch: Any) -> None:
    inherit_from_local(monkeypatch)

    env_definition = define_environment("virtualenv", packages=["pyjokes==1.0"])
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(
                eval,
                "__import__('pyjokes').__version__",
            ),
            method="dill",
        ),
        environments=[env_definition],
    )

    with pytest.raises(grpc.RpcError) as exc:
        run_request(stub, request)

    assert exc.match("unexpected keyword argument 'packages'")


@pytest.mark.parametrize("inherit_local", [True, False])
def test_server_multiple_envs(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
    inherit_local: bool,
) -> None:
    inherit_from_local(monkeypatch, inherit_local)
    xtra_requirements = ["python-dateutil==2.8.2"]
    requirements = ["pyjokes==0.6.0"]
    if not inherit_local:
        # The agent process needs dill (and isolate) to actually
        # deserialize the given function, so they need to be installed
        # when we are not inheriting the local environment.
        requirements.append("dill==0.3.5.1")

        # TODO: apparently [server] doesn't work but [grpc] does work (not sure why
        # needs further investigation, probably poetry related).
        requirements.append(f"{REPO_DIR}[grpc]")

    env_definition = define_environment("virtualenv", requirements=requirements)
    xtra_env_definition = define_environment(
        "virtualenv", requirements=xtra_requirements
    )
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(
                eval,
                (
                    "__import__('pyjokes').__version__ + "
                    "' ' + "
                    "__import__('dateutil').__version__"
                ),
            ),
            method="dill",
        ),
        environments=[env_definition, xtra_env_definition],
    )

    raw_result = run_request(stub, request)

    assert from_grpc(raw_result) == "0.6.0 2.8.2"


@pytest.mark.parametrize("python_version", ["3.8"])
def test_agent_requirements_custom_version(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
    python_version: str,
) -> None:
    requirements = ["pyjokes==0.6.0"]
    agent_requirements = ["dill==0.3.5.1", f"{REPO_DIR}[grpc]"]
    monkeypatch.setattr("isolate.server.server.AGENT_REQUIREMENTS", agent_requirements)

    env_definition = define_environment(
        "virtualenv",
        requirements=requirements,
        python_version=python_version,
    )
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(
                eval,
                (
                    "__import__('sysconfig').get_python_version(), "
                    "__import__('pyjokes').__version__"
                ),
            ),
            method="dill",
        ),
        environments=[env_definition],
    )

    raw_result = run_request(stub, request)
    assert from_grpc(raw_result) == ("3.8", "0.6.0")


def test_agent_show_logs_from_agent_requirements(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
) -> None:
    requirements = ["pyjokes==0.6.0"]
    agent_requirements = ["$$$$", f"{REPO_DIR}[grpc]"]
    monkeypatch.setattr("isolate.server.server.AGENT_REQUIREMENTS", agent_requirements)

    env_definition = define_environment(
        "virtualenv",
        requirements=requirements,
    )
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(
                eval,
                (
                    "__import__('sysconfig').get_python_version(), "
                    "__import__('pyjokes').__version__"
                ),
            ),
            method="dill",
        ),
        environments=[env_definition],
    )

    build_logs: List[Log] = []
    with pytest.raises(grpc.RpcError) as exc:
        run_request(stub, request, build_logs=build_logs)

    assert "Failure during 'pip install': Command" in exc.value.details()

    raw_logs = [log.message for log in build_logs]
    assert any("ERROR: Invalid requirement: '$$$$'" in raw_log for raw_log in raw_logs)


def test_bridge_connection_reuse(
    stub: definitions.IsolateStub, monkeypatch: Any
) -> None:
    inherit_from_local(monkeypatch)

    first_env = define_environment(
        "virtualenv",
        requirements=["pyjokes==0.6.0"],
    )
    request = definitions.BoundFunction(
        setup_func=to_serialized_object(
            lambda: __import__("os").getpid(), method="cloudpickle"
        ),
        function=to_serialized_object(
            lambda process_pid: process_pid, method="cloudpickle"
        ),
        environments=[first_env],
    )

    initial_process_pid = from_grpc(run_request(stub, request))
    secondary_process_pid = from_grpc(run_request(stub, request))

    # Both of the functions should run in the same agent process
    assert initial_process_pid == secondary_process_pid

    # But if we run a third function that has a different environment
    # then its process should be different
    second_env = define_environment(
        "virtualenv",
        requirements=["pyjokes==0.5.0"],
    )
    request_2 = copy.deepcopy(request)
    request_2.environments.remove(first_env)
    request_2.environments.append(second_env)

    third_process_pid = from_grpc(run_request(stub, request_2))
    assert third_process_pid != initial_process_pid

    # As long as the environments are same, they are cached
    fourth_process_pid = from_grpc(run_request(stub, request_2))
    assert fourth_process_pid == third_process_pid


@pytest.mark.flaky(max_runs=3)
def test_bridge_connection_reuse_logs(
    stub: definitions.IsolateStub, monkeypatch: Any
) -> None:
    inherit_from_local(monkeypatch)

    first_env = define_environment(
        "virtualenv",
        requirements=["pyjokes==0.6.0"],
    )
    request = definitions.BoundFunction(
        setup_func=to_serialized_object(
            lambda: print("setup"),
            method="cloudpickle",
        ),
        function=to_serialized_object(
            lambda _: print("run"),
            method="cloudpickle",
        ),
        environments=[first_env],
    )

    logs: List[Log] = []
    run_request(stub, request, user_logs=logs)
    run_request(stub, request, user_logs=logs)
    run_request(stub, request, user_logs=logs)

    str_logs = [log.message for log in logs if log.message in ("setup", "run")]
    assert str_logs == [
        "setup",
        "run",
        "run",
        "run",
    ]


def print_logs_no_delay(num_lines, should_flush):
    for i in range(num_lines):
        print(i, flush=should_flush)

    return num_lines


@pytest.mark.parametrize("num_lines", [0, 1, 10, 100, 1000])
@pytest.mark.parametrize("should_flush", [True, False])
@pytest.mark.flaky(max_runs=5)
def test_receive_complete_logs(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
    num_lines: int,
    should_flush: bool,
) -> None:
    inherit_from_local(monkeypatch)
    result, logs = run_function(stub, print_logs_no_delay, num_lines, should_flush)
    assert result == num_lines
    assert logs == [str(i) for i in range(num_lines)]


def take_buffer(buffer):
    return buffer


def test_grpc_option_configuration(tmp_path, monkeypatch):
    inherit_from_local(monkeypatch)
    with monkeypatch.context() as ctx:
        ctx.setenv("ISOLATE_GRPC_CALL_MAX_SEND_MESSAGE_LENGTH", "100")
        ctx.setenv("ISOLATE_GRPC_CALL_MAX_RECEIVE_MESSAGE_LENGTH", "100")

        with pytest.raises(grpc.RpcError, match="Sent message larger than max"):
            with make_server(tmp_path) as stubs:
                run_function(stubs.isolate_stub, take_buffer, b"0" * 200)

    with monkeypatch.context() as ctx:
        ctx.setenv("ISOLATE_GRPC_CALL_MAX_SEND_MESSAGE_LENGTH", "5000")
        ctx.setenv("ISOLATE_GRPC_CALL_MAX_RECEIVE_MESSAGE_LENGTH", "5000")

        with make_server(tmp_path) as stubs:
            result, _ = run_function(stubs.isolate_stub, take_buffer, b"0" * 200)
            assert result == b"0" * 200


def test_health_check(health_stub: health.HealthStub) -> None:
    resp: health.HealthCheckResponse = health_stub.Check(
        health.HealthCheckRequest(service="")
    )
    assert resp.status == health.HealthCheckResponse.SERVING


@pytest.mark.parametrize(
    "interceptors",
    [[ControllerAuthInterceptor(controller_auth_key="test-secret")]],
)
def test_controller_auth_rejects_without_token(
    stub: definitions.IsolateStub,
) -> None:
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.List(definitions.ListRequest())
    assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED

    with pytest.raises(grpc.RpcError) as exc_info:
        stub.SetMetadata(
            definitions.SetMetadataRequest(
                task_id="task-id",
                metadata=definitions.TaskMetadata(logger_labels={"test": "test"}),
            )
        )
    # there is no task, so it should return NOT_FOUND
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND


@pytest.mark.parametrize(
    "interceptors",
    [[ControllerAuthInterceptor(controller_auth_key="test-secret")]],
)
def test_controller_auth_rejects_wrong_token(
    stub: definitions.IsolateStub,
) -> None:
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.List(
            definitions.ListRequest(),
            metadata=[("controller-token", "wrong")],
        )
    assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED


@pytest.mark.parametrize(
    "interceptors",
    [[ControllerAuthInterceptor(controller_auth_key="test-secret")]],
)
def test_controller_auth_accepts_correct_token(
    stub: definitions.IsolateStub,
) -> None:
    stub.List(
        definitions.ListRequest(),
        metadata=[("controller-token", "test-secret")],
    )


def check_machine():
    import os

    return os.getpid()


def kill_machine():
    import os

    os._exit(1)


def get_pid_as_exc():
    import os

    raise ValueError(os.getpid())


@pytest.mark.flaky(max_runs=3)
def test_bridge_caching_when_undeerlying_channel_fails(
    stub: definitions.IsolateStub, monkeypatch: Any
) -> None:
    import os
    import time

    inherit_from_local(monkeypatch)
    pid_1, _ = run_function(stub, check_machine)
    pid_2, _ = run_function(stub, check_machine)
    assert pid_1 == pid_2  # Same bridge

    # Now send some faulty code that breaks the
    # running agent and thus invalidatathing the
    # bridge
    with pytest.raises(grpc.RpcError):
        run_function(stub, kill_machine)

    # Now we should get a new bridge
    pid_3, _ = run_function(stub, check_machine)
    assert pid_1 != pid_3

    # Even if there is a normal exception, the bridge
    # should be reused (since we can capture it and it
    # does not affect it badly).
    with pytest.raises(ValueError) as exc_info:
        run_function(stub, get_pid_as_exc)

    [pid_4] = exc_info.value.args
    assert pid_3 == pid_4

    # Ensure that outside factors are also accounted for
    # and the bridge is not reused
    os.kill(pid_4, 9)

    # And channels are kept fresh for a while (according
    # to gRPC spec they might fall into idle when there is
    # no exchange between client and server for a while but
    # that doesn't seem to happen to us? If it did, we would
    # add keepalive pings to the channel but not sure if we need
    # it now).
    pid_5 = run_function(stub, check_machine)
    assert pid_4 != pid_5

    time.sleep(10)  # I've tried up to 90, and it seems to work fine?
    # using 10 as it is the default keepalive time
    # which would mean the channel would normally be
    # fallen into the idle status?

    pid_6 = run_function(stub, check_machine)
    assert pid_5 == pid_6


def test_server_minimum_viable_proto_version(stub: definitions.IsolateStub) -> None:
    # The agent process needs dill (and isolate) to actually
    # deserialize the given function, so they need to be installed
    # when we are not inheriting the local environment.

    # protobuf<3 (the 2.x series) seems to use Python 2 only?
    requirements = ["protobuf>3,<4"]
    requirements.append("dill==0.3.5.1")
    requirements.append(f"{REPO_DIR}")

    env_definition = define_environment("virtualenv", requirements=requirements)
    request = definitions.BoundFunction(
        function=to_serialized_object(
            partial(eval, "1+2"),
            method="dill",
        ),
        environments=[env_definition],
    )

    raw_result = run_request(stub, request)
    assert from_grpc(raw_result) == 3


def send_unserializable_object():
    import sys

    return sys._getframe()


def raise_unserializable_object():
    import sys

    raise Exception("relevant information", sys._getframe())


def test_server_proper_error_delegation(
    stub: definitions.IsolateStub, monkeypatch: Any
) -> None:
    inherit_from_local(monkeypatch)

    user_logs: List[Any] = []
    with pytest.raises(grpc.RpcError) as exc_info:
        run_function(stub, send_unserializable_object, log_handler=user_logs)

    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert (
        "Error while serializing the execution result (object of type <class 'frame'>)."
    ) in exc_info.value.details()
    assert not _filter_grpc_noise(user_logs)

    user_logs = []
    with pytest.raises(grpc.RpcError) as exc_info:
        run_function(stub, raise_unserializable_object, log_handler=user_logs)

    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert (
        "Error while serializing the execution result "
        "(object of type <class 'Exception'>)."
    ) in exc_info.value.details()
    filtered = _filter_grpc_noise(user_logs)
    assert "relevant information" in "\n".join(log.message for log in filtered)


def myfunc(path):
    import time

    with open(path, "w") as fobj:
        for _ in range(10):
            time.sleep(0.1)
            fobj.write("still alive")

        fobj.write("completed")


def test_server_submit(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    import time

    inherit_from_local(monkeypatch)

    file = tmp_path / "file"

    request = definitions.SubmitRequest(
        function=prepare_request(myfunc, str(file)),
    )
    stub.Submit(request)
    time.sleep(5)
    assert "completed" in file.read_text()
    assert not list(stub.List(definitions.ListRequest()).tasks)


def myserver():
    import time

    while True:
        print("running")
        time.sleep(1)


def test_server_submit_server(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
) -> None:
    inherit_from_local(monkeypatch)

    request = definitions.SubmitRequest(function=prepare_request(myserver))
    task_id = stub.Submit(request).task_id

    tasks = [task.task_id for task in stub.List(definitions.ListRequest()).tasks]
    assert task_id in tasks

    stub.Cancel(definitions.CancelRequest(task_id=task_id))

    assert not list(stub.List(definitions.ListRequest()).tasks)


@pytest.mark.parametrize(
    "interceptors",
    [
        [SingleTaskInterceptor()],
    ],
)
def test_server_single_use_submit(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
) -> None:
    import time

    inherit_from_local(monkeypatch)

    request = definitions.SubmitRequest(function=prepare_request(myserver))
    task_id = stub.Submit(request).task_id

    tasks = [task.task_id for task in stub.List(definitions.ListRequest()).tasks]
    assert task_id in tasks

    # Now try to Submit again
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.Submit(request)
    assert exc_info.value.code() == grpc.StatusCode.RESOURCE_EXHAUSTED

    # And try to Run a task
    with pytest.raises(grpc.RpcError) as exc_info:
        run_request(stub, prepare_request(myserver))
    assert exc_info.value.code() == grpc.StatusCode.RESOURCE_EXHAUSTED

    stub.Cancel(definitions.CancelRequest(task_id=task_id))
    time.sleep(1)

    with pytest.raises(grpc.RpcError) as exc_info:
        stub.List(definitions.ListRequest())

    # Server should be shutting down
    assert exc_info.value.code() == grpc.StatusCode.UNAVAILABLE


@pytest.mark.parametrize(
    "interceptors",
    [
        [SingleTaskInterceptor()],
    ],
)
def test_server_single_use_run(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
) -> None:
    import time

    inherit_from_local(monkeypatch)

    run_function(stub, check_machine)
    time.sleep(1)

    # Now try to Submit again
    with pytest.raises(grpc.RpcError) as exc_info:
        submit_request = definitions.SubmitRequest(function=prepare_request(myserver))
        stub.Submit(submit_request)

    assert exc_info.value.code() == grpc.StatusCode.UNAVAILABLE

    # And try to Run a task
    with pytest.raises(grpc.RpcError) as exc_info:
        run_function(stub, check_machine)

    assert exc_info.value.code() == grpc.StatusCode.UNAVAILABLE

    with pytest.raises(grpc.RpcError) as exc_info:
        stub.List(definitions.ListRequest())

    assert exc_info.value.code() == grpc.StatusCode.UNAVAILABLE


def test_server_run_on_main_thread(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
) -> None:
    inherit_from_local(monkeypatch)

    def func_should_fail_on_main_thread():
        if threading.current_thread() == threading.main_thread():
            raise RuntimeError("should fail on main thread")
        else:
            return "should succeed on non-main thread"

    def func_should_fail_off_main_thread():
        if threading.current_thread() != threading.main_thread():
            raise RuntimeError("should fail on non-main thread")
        else:
            return "should succeed on main thread"

    result = from_grpc(
        run_request(stub, prepare_request(func_should_fail_on_main_thread))
    )
    assert result == "should succeed on non-main thread"

    setattr(func_should_fail_on_main_thread, "_run_on_main_thread", True)
    with pytest.raises(RuntimeError):
        from_grpc(run_request(stub, prepare_request(func_should_fail_on_main_thread)))

    result = from_grpc(
        run_request(
            stub,
            prepare_request(
                func_should_fail_on_main_thread,
                run_on_main_thread=False,
            ),
        )
    )
    assert result == "should succeed on non-main thread"

    result = from_grpc(
        run_request(
            stub,
            prepare_request(
                func_should_fail_off_main_thread,
                run_on_main_thread=True,
            ),
        )
    )
    assert result == "should succeed on main thread"


def test_server_async_function(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
) -> None:
    inherit_from_local(monkeypatch)

    async def myasyncfunc():
        await asyncio.sleep(0.1)
        return "async function"

    result = from_grpc(run_request(stub, prepare_request(myasyncfunc)))
    assert result == "async function"

    setattr(myasyncfunc, "_run_on_main_thread", True)
    result = from_grpc(run_request(stub, prepare_request(myasyncfunc)))
    assert result == "async function"


def test_server_asyncio_run_function(
    stub: definitions.IsolateStub,
    monkeypatch: Any,
) -> None:
    inherit_from_local(monkeypatch)

    def asyncio_run_function():
        async def myasyncfunc():
            await asyncio.sleep(0.1)
            return "async function"

        return asyncio.run(myasyncfunc())

    result = from_grpc(run_request(stub, prepare_request(asyncio_run_function)))
    assert result == "async function"

    setattr(asyncio_run_function, "_run_on_main_thread", True)
    with pytest.raises(RuntimeError):
        from_grpc(run_request(stub, prepare_request(asyncio_run_function)))
