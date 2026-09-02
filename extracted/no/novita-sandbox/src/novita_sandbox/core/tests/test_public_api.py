from packaging.version import Version

import novita_sandbox
import novita_sandbox.core.client as core_client
from novita_sandbox import (
    AsyncCodeInterpreterSandbox,
    AsyncSandbox,
    AsyncSecret,
    AsyncTemplate,
    AsyncVolume,
    CodeInterpreterSandbox,
    Context,
    DesktopSandbox,
    Execution,
    ExecutionError,
    Logs,
    MIMEType,
    Novita,
    OutputMessage,
    Result,
    Sandbox,
    SandboxQuery,
    SandboxState,
    Secret,
    Template,
    Volume,
)
from novita_sandbox.code_interpreter import AsyncSandbox as SubpackageAsyncCodeSandbox
from novita_sandbox.code_interpreter import Context as SubpackageContext
from novita_sandbox.code_interpreter import Execution as SubpackageExecution
from novita_sandbox.code_interpreter import (
    ExecutionError as SubpackageExecutionError,
)
from novita_sandbox.code_interpreter import Logs as SubpackageLogs
from novita_sandbox.code_interpreter import MIMEType as SubpackageMIMEType
from novita_sandbox.code_interpreter import OutputMessage as SubpackageOutputMessage
from novita_sandbox.code_interpreter import Result as SubpackageResult
from novita_sandbox.code_interpreter import Sandbox as SubpackageCodeSandbox
from novita_sandbox.core.connection_config import ConnectionConfig
from novita_sandbox.core.sandbox.sandbox_api import (
    SandboxEventsResult,
    SandboxInfo,
    SandboxMetrics,
    SandboxQuota,
    SnapshotInfo,
)
from novita_sandbox.core.template.main import TemplateBase
from novita_sandbox.core.template.types import BuildInfo, TemplateList
from novita_sandbox.core.volume.types import VolumeAndToken, VolumeInfo
from novita_sandbox.desktop import Sandbox as SubpackageDesktopSandbox


def test_top_level_exports_core_public_api():
    assert novita_sandbox.Sandbox is Sandbox
    assert novita_sandbox.AsyncSandbox is AsyncSandbox
    assert novita_sandbox.Template is Template
    assert novita_sandbox.AsyncTemplate is AsyncTemplate
    assert novita_sandbox.Volume is Volume
    assert novita_sandbox.AsyncVolume is AsyncVolume
    assert novita_sandbox.Secret is Secret
    assert novita_sandbox.AsyncSecret is AsyncSecret
    assert novita_sandbox.Novita is Novita
    assert novita_sandbox.SandboxQuery is SandboxQuery
    assert novita_sandbox.SandboxState is SandboxState


def test_top_level_exports_runtime_specific_public_api():
    assert novita_sandbox.CodeInterpreterSandbox is CodeInterpreterSandbox
    assert CodeInterpreterSandbox is SubpackageCodeSandbox
    assert novita_sandbox.AsyncCodeInterpreterSandbox is AsyncCodeInterpreterSandbox
    assert AsyncCodeInterpreterSandbox is SubpackageAsyncCodeSandbox
    assert novita_sandbox.DesktopSandbox is DesktopSandbox
    assert DesktopSandbox is SubpackageDesktopSandbox

    assert Context is SubpackageContext
    assert Execution is SubpackageExecution
    assert ExecutionError is SubpackageExecutionError
    assert Logs is SubpackageLogs
    assert MIMEType is SubpackageMIMEType
    assert OutputMessage is SubpackageOutputMessage
    assert Result is SubpackageResult


def test_core_sandbox_instance_contract():
    sandbox = Sandbox(
        sandbox_id="sandbox-id",
        envd_version=Version("0.5.7"),
        envd_access_token=None,
        sandbox_domain=None,
        connection_config=ConnectionConfig(api_key="test-key"),
    )

    assert sandbox.commands is not None
    assert sandbox.files is not None
    assert sandbox.pty is not None
    assert sandbox.git is not None
    assert sandbox.sandbox_id == "sandbox-id"
    assert sandbox.sandbox_domain is not None
    assert callable(sandbox.hotplug_memory)
    assert callable(sandbox.resize)


def test_novita_exposes_core_namespaces():
    novita = Novita(api_key="test-key")

    assert callable(novita.sandbox.create)
    assert callable(novita.sandbox.beta_create)
    assert callable(novita.sandbox.connect)
    assert callable(novita.sandbox.get)
    assert callable(novita.sandbox.list)
    assert callable(novita.sandbox.kill)
    assert callable(novita.sandbox.set_timeout)
    assert callable(novita.sandbox.get_info)
    assert callable(novita.sandbox.get_metrics)
    assert callable(novita.sandbox.pause)
    assert callable(novita.sandbox.beta_pause)
    assert callable(novita.sandbox.clone)
    assert callable(novita.sandbox.reset)
    assert callable(novita.sandbox.commit)
    assert callable(novita.sandbox.set_network)
    assert callable(novita.sandbox.create_snapshot)
    assert callable(novita.sandbox.list_snapshots)
    assert callable(novita.sandbox.delete_snapshot)
    assert callable(novita.sandbox.get_quota)
    assert callable(novita.sandbox.get_events)
    assert callable(novita.sandbox.resize)

    assert callable(novita.template.new)
    assert callable(novita.template.create)
    assert callable(novita.template.from_image)
    assert callable(novita.template.from_python_image)
    assert callable(novita.template.from_template)
    assert callable(novita.template.from_dockerfile)
    assert callable(novita.template.to_json)
    assert callable(novita.template.to_dockerfile)
    assert callable(novita.template.wait_for_port)
    assert callable(novita.template.build)
    assert callable(novita.template.build_in_background)
    assert callable(novita.template.get_build_status)
    assert callable(novita.template.list)
    assert callable(novita.template.delete)

    assert callable(novita.volume.create)
    assert callable(novita.volume.connect)
    assert callable(novita.volume.get_info)
    assert callable(novita.volume.list)
    assert callable(novita.volume.update_quota)
    assert callable(novita.volume.destroy)

    assert callable(novita.secret.create)
    assert callable(novita.secret.list)
    assert callable(novita.secret.get)
    assert callable(novita.secret.update)
    assert callable(novita.secret.delete)


def test_novita_exposes_runtime_sandbox_namespaces():
    novita = Novita(api_key="test-key")

    for namespace in (novita.code_interpreter, novita.desktop):
        assert callable(namespace.create)
        assert callable(namespace.beta_create)
        assert callable(namespace.connect)
        assert callable(namespace.get)
        assert callable(namespace.list)
        assert callable(namespace.kill)
        assert callable(namespace.set_timeout)
        assert callable(namespace.get_info)
        assert callable(namespace.get_metrics)
        assert callable(namespace.pause)
        assert callable(namespace.beta_pause)
        assert callable(namespace.clone)
        assert callable(namespace.reset)
        assert callable(namespace.commit)
        assert callable(namespace.set_network)
        assert callable(namespace.create_snapshot)
        assert callable(namespace.list_snapshots)
        assert callable(namespace.delete_snapshot)
        assert callable(namespace.get_quota)
        assert callable(namespace.get_events)
        assert callable(namespace.resize)

    assert novita.code_interpreter.Sandbox is CodeInterpreterSandbox
    assert novita.code_interpreter.AsyncSandbox is AsyncCodeInterpreterSandbox
    assert novita.code_interpreter.Context is Context
    assert novita.code_interpreter.Execution is Execution
    assert novita.code_interpreter.ExecutionError is ExecutionError
    assert novita.code_interpreter.Logs is Logs
    assert novita.code_interpreter.MIMEType is MIMEType
    assert novita.code_interpreter.OutputMessage is OutputMessage
    assert novita.code_interpreter.Result is Result
    assert novita.code_interpreter.SandboxQuery is SandboxQuery
    assert novita.code_interpreter.SandboxState is SandboxState

    assert novita.desktop.Sandbox is DesktopSandbox
    assert novita.desktop.SandboxQuery is SandboxQuery
    assert novita.desktop.SandboxState is SandboxState


def test_novita_core_namespaces_expose_related_public_types():
    novita = Novita(api_key="test-key")

    assert novita.sandbox.Sandbox is Sandbox
    assert novita.sandbox.AsyncSandbox is AsyncSandbox
    assert novita.sandbox.SandboxQuery is SandboxQuery
    assert novita.sandbox.SandboxState is SandboxState
    assert novita.sandbox.SandboxInfo is SandboxInfo
    assert novita.sandbox.SandboxMetrics is SandboxMetrics
    assert novita.sandbox.SnapshotInfo is SnapshotInfo
    assert novita.sandbox.SandboxQuota is SandboxQuota
    assert novita.sandbox.SandboxEventsResult is SandboxEventsResult

    assert novita.template.Template is Template
    assert novita.template.AsyncTemplate is AsyncTemplate
    assert novita.template.TemplateBase is TemplateBase
    assert novita.template.BuildInfo is BuildInfo
    assert novita.template.TemplateList is TemplateList

    assert novita.volume.Volume is Volume
    assert novita.volume.AsyncVolume is AsyncVolume
    assert novita.volume.VolumeInfo is VolumeInfo
    assert novita.volume.VolumeAndToken is VolumeAndToken

    assert novita.secret.Secret is Secret
    assert novita.secret.AsyncSecret is AsyncSecret


def test_novita_secret_namespace_forwards_create_arguments(monkeypatch):
    captured = {}

    def fake_create(*, name, value, hosts, description=None, **opts):
        captured["create"] = (name, value, hosts, description, opts)
        return "secret"

    monkeypatch.setattr(Secret, "create", staticmethod(fake_create))

    novita = Novita(api_key="client-key")
    result = novita.secret.create(
        name="openai-prod",
        value="sk-real",
        hosts=["api.example.com"],
        description="Example",
    )

    assert result == "secret"
    name, value, hosts, description, opts = captured["create"]
    assert (name, value, hosts, description) == (
        "openai-prod",
        "sk-real",
        ["api.example.com"],
        "Example",
    )
    assert opts["api_key"] == "client-key"
    assert "domain" in opts
    assert "api_url" in opts
    assert "request_timeout" in opts


def test_novita_secret_namespace_forwards_update_arguments(monkeypatch):
    captured = {}

    def fake_update(*, name, value, hosts, description=None, **opts):
        captured["update"] = (name, value, hosts, description, opts)
        return "secret"

    monkeypatch.setattr(Secret, "update", staticmethod(fake_update))

    novita = Novita(api_key="client-key")
    result = novita.secret.update(
        name="openai-prod",
        value="sk-new",
        hosts=["api.example.com"],
        headers={"X-Trace": "1"},
    )

    assert result == "secret"
    name, value, hosts, description, opts = captured["update"]
    assert (name, value, hosts, description) == (
        "openai-prod",
        "sk-new",
        ["api.example.com"],
        None,
    )
    assert opts["api_key"] == "client-key"
    assert "domain" in opts
    assert "api_url" in opts
    assert "request_timeout" in opts


def test_novita_sandbox_namespace_merges_client_options(monkeypatch):
    captured = {}

    def fake_create(*args, **opts):
        captured["args"] = args
        captured["opts"] = opts
        return "sandbox"

    monkeypatch.setattr(Sandbox, "create", staticmethod(fake_create))

    novita = Novita(api_key="client-key", headers={"X-Base": "1"})
    result = novita.sandbox.create("base", headers={"X-Next": "2"})

    assert result == "sandbox"
    assert captured["args"] == ("base",)
    assert captured["opts"]["api_key"] == "client-key"
    assert captured["opts"]["headers"]["X-Base"] == "1"
    assert captured["opts"]["headers"]["X-Next"] == "2"


def test_novita_sandbox_namespace_preserves_positional_arguments(monkeypatch):
    captured = {}

    def fake_reset(*args, **opts):
        captured["reset"] = (args, opts)
        return True

    def fake_connect(*args, **opts):
        captured["connect"] = (args, opts)
        return "sandbox"

    monkeypatch.setattr(Sandbox, "reset", staticmethod(fake_reset))
    monkeypatch.setattr(Sandbox, "connect", staticmethod(fake_connect))

    novita = Novita(api_key="client-key")

    assert novita.sandbox.reset("sandbox-id", True, 30, request_timeout=5) is True
    assert novita.sandbox.connect("sandbox-id", 60) == "sandbox"

    reset_args, reset_opts = captured["reset"]
    connect_args, connect_opts = captured["connect"]

    assert reset_args == ("sandbox-id", True, 30)
    assert reset_opts["api_key"] == "client-key"
    assert reset_opts["request_timeout"] == 5
    assert connect_args == ("sandbox-id", 60)
    assert connect_opts["api_key"] == "client-key"


def test_novita_runtime_namespaces_merge_client_options(monkeypatch):
    captured = {}

    def fake_code_create(*args, **opts):
        captured["code"] = (args, opts)
        return "code-sandbox"

    def fake_desktop_create(*args, **opts):
        captured["desktop"] = (args, opts)
        return "desktop-sandbox"

    monkeypatch.setattr(
        CodeInterpreterSandbox, "create", staticmethod(fake_code_create)
    )
    monkeypatch.setattr(DesktopSandbox, "create", staticmethod(fake_desktop_create))

    novita = Novita(api_key="client-key", headers={"X-Base": "1"})

    assert (
        novita.code_interpreter.create(
            metadata={"name": "code"}, headers={"X-Next": "2"}
        )
        == "code-sandbox"
    )
    assert (
        novita.desktop.create(resolution=(1280, 720), request_timeout=5)
        == "desktop-sandbox"
    )

    code_args, code_opts = captured["code"]
    desktop_args, desktop_opts = captured["desktop"]

    assert code_args == ()
    assert code_opts["api_key"] == "client-key"
    assert code_opts["metadata"] == {"name": "code"}
    assert code_opts["headers"]["X-Base"] == "1"
    assert code_opts["headers"]["X-Next"] == "2"

    assert desktop_args == ()
    assert desktop_opts["api_key"] == "client-key"
    assert desktop_opts["resolution"] == (1280, 720)
    assert desktop_opts["request_timeout"] == 5


def test_novita_template_namespace_can_start_builder_without_template_import():
    novita = Novita(api_key="test-key")

    template = novita.template.from_image("python:3.12")

    assert template._template._base_image == "python:3.12"


def test_novita_template_namespace_preserves_positional_list_arguments(monkeypatch):
    captured = {}

    def fake_list(*args, **opts):
        captured["args"] = args
        captured["opts"] = opts
        return "templates"

    monkeypatch.setattr(Template, "list", staticmethod(fake_list))

    novita = Novita(api_key="client-key")
    result = novita.template.list("snapshot_template", 2, 10, request_timeout=5)

    assert result == "templates"
    assert captured["args"] == ("snapshot_template", 2, 10)
    assert captured["opts"]["api_key"] == "client-key"
    assert captured["opts"]["request_timeout"] == 5


def test_resize_delegates_to_hotplug_memory(monkeypatch):
    captured = {}

    def fake_hotplug(self, requested_size_mib, **opts):
        captured["sandbox_id"] = self.sandbox_id
        captured["requested_size_mib"] = requested_size_mib
        captured["opts"] = opts

    monkeypatch.setattr(Sandbox, "hotplug_memory", fake_hotplug)

    sandbox = Sandbox(
        sandbox_id="sandbox-id",
        envd_version=Version("0.5.7"),
        envd_access_token=None,
        sandbox_domain=None,
        connection_config=ConnectionConfig(api_key="test-key"),
    )

    sandbox.resize(memory_mib=512, request_timeout=5)

    assert captured == {
        "sandbox_id": "sandbox-id",
        "requested_size_mib": 512,
        "opts": {"request_timeout": 5},
    }


def test_novita_resize_namespaces_delegate_to_hotplug_memory(monkeypatch):
    captured = []

    def fake_hotplug(cls, sandbox_id, requested_size_mib=0, **opts):
        captured.append(
            {
                "sandbox_id": sandbox_id,
                "requested_size_mib": requested_size_mib,
                "opts": opts,
            }
        )

    monkeypatch.setattr(
        core_client.SandboxApi,
        "_cls_hotplug_memory",
        classmethod(fake_hotplug),
    )

    novita = Novita(api_key="client-key", headers={"X-Base": "1"})

    novita.sandbox.resize(
        "sandbox-id",
        memory_mib=512,
        request_timeout=5,
        headers={"X-Next": "2"},
    )
    novita.code_interpreter.resize("code-id", memory_mib=256)
    novita.desktop.resize("desktop-id", memory_mib=128)

    assert len(captured) == 3
    assert [call["sandbox_id"] for call in captured] == [
        "sandbox-id",
        "code-id",
        "desktop-id",
    ]
    assert [call["requested_size_mib"] for call in captured] == [512, 256, 128]

    assert captured[0]["opts"]["api_key"] == "client-key"
    assert captured[0]["opts"]["request_timeout"] == 5
    assert captured[0]["opts"]["headers"]["X-Base"] == "1"
    assert captured[0]["opts"]["headers"]["X-Next"] == "2"

    assert captured[1]["opts"]["api_key"] == "client-key"
    assert captured[1]["opts"]["headers"]["X-Base"] == "1"

    assert captured[2]["opts"]["api_key"] == "client-key"
    assert captured[2]["opts"]["headers"]["X-Base"] == "1"
