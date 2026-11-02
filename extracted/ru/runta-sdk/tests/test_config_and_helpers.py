from __future__ import annotations

import asyncio
import importlib
import inspect
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from runta import (
    AsyncCheckpointManager,
    AsyncEgressManager,
    AsyncFileManager,
    AsyncRunta,
    AsyncRuntime,
    AsyncRuntimeCheckpointManager,
    AsyncRuntimeManager,
    ApiError,
    AsyncSecretManager,
    CheckpointInfo,
    CheckpointManager,
    CheckpointState,
    ConfigError,
    CreateRuntimeResources,
    EgressManager,
    EgressMode,
    EgressPolicy,
    FileManager,
    Runta,
    Runtime,
    RuntimeCheckpointManager,
    RuntimeInfo,
    RuntimeManager,
    RuntimeResourceLimits,
    RuntimeResourceRequests,
    RuntimeResources,
    RuntimeStatus,
    SecretManager,
)
from runta._internal.config import DEFAULT_ENDPOINT, resolve_config
from runta._internal.helpers import (
    _command_parts,
    _host_from_url,
    _status_filter,
    _status_query,
)


class ConfigTests(unittest.TestCase):
    def test_hosted_endpoint_is_default(self) -> None:
        self.assertEqual(DEFAULT_ENDPOINT, "https://api.runta.com")
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "missing-config.toml"
            with patch.dict(os.environ, {"RUNTA_TOKEN": "rt_env"}, clear=True):
                endpoint, token = resolve_config(
                    endpoint=None, token=None, config_path=config_path
                )
        self.assertEqual(endpoint, DEFAULT_ENDPOINT)
        self.assertEqual(token, "rt_env")

    def test_explicit_values_win(self) -> None:
        endpoint, token = resolve_config(
            endpoint="http://control:50072",
            token="rt_explicit",
            config_path=None,
        )
        self.assertEqual(endpoint, "http://control:50072")
        self.assertEqual(token, "rt_explicit")

    def test_env_values_are_used(self) -> None:
        with patch.dict(
            os.environ,
            {
                "RUNTA_ENDPOINT": "http://env:50072",
                "RUNTA_TOKEN": "rt_env",
                "RUNTA_CONFIG": "/tmp/missing-runta-config.toml",
            },
            clear=False,
        ):
            endpoint, token = resolve_config(
                endpoint=None, token=None, config_path=None
            )
        self.assertEqual(endpoint, "http://env:50072")
        self.assertEqual(token, "rt_env")

    def test_env_token_file_is_not_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            token_file = Path(tmp) / "token"
            token_file.write_text("rt_file_token\n")
            with patch.dict(
                os.environ,
                {
                    "RUNTA_TOKEN_FILE": str(token_file),
                },
                clear=True,
            ):
                with self.assertRaises(ConfigError):
                    resolve_config(
                        endpoint=None,
                        token=None,
                        config_path=Path(tmp) / "missing-config.toml",
                    )

    def test_file_values_are_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.toml"
            path.write_text('endpoint = "http://file:50072"\ntoken = "rt_file"\n')
            with patch.dict(os.environ, {}, clear=True):
                endpoint, token = resolve_config(
                    endpoint=None, token=None, config_path=path
                )
        self.assertEqual(endpoint, "http://file:50072")
        self.assertEqual(token, "rt_file")


class HelperTests(unittest.TestCase):
    def _assert_no_instance_dict(self, *objects: object) -> None:
        for obj in objects:
            with self.subTest(slotted=type(obj).__name__):
                self.assertFalse(hasattr(obj, "__dict__"))
                with self.assertRaises(AttributeError):
                    setattr(obj, "unexpected_attribute", object())

    def test_runta_exports_sync_and_async_clients(self) -> None:
        import runta

        self.assertEqual(Runta.__name__, "Runta")
        self.assertEqual(AsyncRunta.__name__, "AsyncRunta")
        self.assertEqual(EgressMode.DENYLIST.value, "denylist")
        self.assertFalse(hasattr(runta, "AuditManager"))
        self.assertFalse(hasattr(runta, "AuditInfo"))
        self.assertFalse(hasattr(runta, "Session"))
        self.assertFalse(hasattr(runta, "SessionManager"))
        self.assertEqual(
            CreateRuntimeResources().__class__.__name__, "CreateRuntimeResources"
        )
        self.assertFalse(hasattr(AsyncRunta, "aclose"))
        self.assertFalse(hasattr(runta, "CpuArch"))
        self.assertIs(runta.RuntimeManager, RuntimeManager)
        self.assertIs(runta.SecretManager, SecretManager)
        self.assertIs(runta.EgressManager, EgressManager)
        self.assertIs(runta.FileManager, FileManager)
        self.assertIs(runta.CheckpointManager, CheckpointManager)
        self.assertFalse(hasattr(runta, "SecretStubConfig"))
        self.assertFalse(hasattr(runta, "SecretStubInfo"))
        self.assertFalse(hasattr(runta, "DefaultSecretStubInfo"))
        self.assertNotIn(
            "runtime_agent", inspect.signature(RuntimeManager.create).parameters
        )
        self.assertNotIn(
            "runtime_agent", inspect.signature(AsyncRuntimeManager.create).parameters
        )
        self.assertFalse(hasattr(SecretManager, "list_secret_stubs"))
        self.assertFalse(hasattr(AsyncSecretManager, "list_secret_stubs"))
        self.assertIs(runta.AsyncRuntimeManager, AsyncRuntimeManager)
        self.assertIs(runta.AsyncSecretManager, AsyncSecretManager)
        self.assertIs(runta.AsyncEgressManager, AsyncEgressManager)
        self.assertIs(runta.AsyncFileManager, AsyncFileManager)
        self.assertIs(runta.AsyncCheckpointManager, AsyncCheckpointManager)
        for name in runta.__all__:
            obj = getattr(runta, name)
            if isinstance(obj, type):
                self.assertEqual(obj.__module__, "runta", name)

        sync_client = Runta(endpoint="http://mock-runta-api", token="rt_mock")
        try:
            self.assertIsInstance(sync_client.runtimes, RuntimeManager)
            self.assertIsInstance(sync_client.secrets, SecretManager)
        finally:
            sync_client.close()

        async_client = AsyncRunta(endpoint="http://mock-runta-api", token="rt_mock")
        try:
            self.assertIsInstance(async_client.runtimes, AsyncRuntimeManager)
            self.assertIsInstance(async_client.secrets, AsyncSecretManager)
        finally:
            asyncio.run(async_client.close())

    def test_removed_public_packages_are_not_importable(self) -> None:
        with self.assertRaises(ModuleNotFoundError):
            importlib.import_module("asyncrunta")
        with self.assertRaises(ModuleNotFoundError):
            importlib.import_module("_common")

    def test_runtime_constructors_are_private(self) -> None:
        with self.assertRaisesRegex(TypeError, "Runta.runtimes.create"):
            Runtime()
        with self.assertRaisesRegex(TypeError, "AsyncRunta.runtimes.create"):
            AsyncRuntime()

    def test_manager_constructors_are_private(self) -> None:
        managers = [
            RuntimeManager,
            AsyncRuntimeManager,
            SecretManager,
            AsyncSecretManager,
            CheckpointManager,
            AsyncCheckpointManager,
            EgressManager,
            AsyncEgressManager,
            FileManager,
            AsyncFileManager,
            RuntimeCheckpointManager,
            AsyncRuntimeCheckpointManager,
        ]
        for manager in managers:
            with self.subTest(manager=manager.__name__):
                with self.assertRaisesRegex(TypeError, "do not call"):
                    manager(object())

    def test_client_manager_properties_are_read_only_and_cached(self) -> None:
        sync_client = Runta(endpoint="http://mock-runta-api", token="rt_mock")
        try:
            self.assertIs(sync_client.runtimes, sync_client.runtimes)
            self.assertIs(sync_client.secrets, sync_client.secrets)
            self.assertIs(sync_client.checkpoints, sync_client.checkpoints)
            self._assert_no_instance_dict(
                sync_client,
                sync_client.runtimes,
                sync_client.secrets,
                sync_client.checkpoints,
            )

            for name in ("runtimes", "secrets", "checkpoints"):
                with self.subTest(client="sync", name=name):
                    with self.assertRaises(AttributeError):
                        setattr(sync_client, name, object())
        finally:
            sync_client.close()

        async def check_async() -> None:
            async_client = AsyncRunta(endpoint="http://mock-runta-api", token="rt_mock")
            try:
                self.assertIs(async_client.runtimes, async_client.runtimes)
                self.assertIs(async_client.secrets, async_client.secrets)
                self.assertIs(async_client.checkpoints, async_client.checkpoints)
                self._assert_no_instance_dict(
                    async_client,
                    async_client.runtimes,
                    async_client.secrets,
                    async_client.checkpoints,
                )

                for name in ("runtimes", "secrets", "checkpoints"):
                    with self.subTest(client="async", name=name):
                        with self.assertRaises(AttributeError):
                            setattr(async_client, name, object())
            finally:
                await async_client.close()

        asyncio.run(check_async())

    def test_runtime_manager_properties_are_read_only_and_cached(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        self.assertIs(runtime.cached_info, fake_http.info)
        self.assertIs(runtime.egress, runtime.egress)
        self.assertFalse(hasattr(runtime, "secrets"))
        self.assertIs(runtime.files, runtime.files)
        self.assertIs(runtime.checkpoints, runtime.checkpoints)
        self.assertFalse(hasattr(runtime, "sessions"))
        self._assert_no_instance_dict(
            runtime,
            runtime.egress,
            runtime.files,
            runtime.checkpoints,
        )

        with self.assertRaises(AttributeError):
            runtime.cached_info = fake_http.info
        with self.assertRaises(AttributeError):
            runtime.info = fake_http.info
        with self.assertRaises(AttributeError):
            runtime.refresh
        with self.assertRaises(AttributeError):
            getattr(runtime, "wait_until_" + "running")
        for name in (
            "egress",
            "files",
            "checkpoints",
        ):
            with self.subTest(name=name):
                with self.assertRaises(AttributeError):
                    setattr(runtime, name, object())

    def test_async_runtime_manager_properties_are_read_only_and_cached(self) -> None:
        async def check() -> None:
            fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
            runtime = AsyncRuntime._from_info(
                SimpleNamespace(_http=fake_http),
                fake_http.info,
            )

            self.assertIs(runtime.cached_info, fake_http.info)
            self.assertIs(runtime.egress, runtime.egress)
            self.assertFalse(hasattr(runtime, "secrets"))
            self.assertIs(runtime.files, runtime.files)
            self.assertIs(runtime.checkpoints, runtime.checkpoints)
            self.assertFalse(hasattr(runtime, "sessions"))
            self._assert_no_instance_dict(
                runtime,
                runtime.egress,
                runtime.files,
                runtime.checkpoints,
            )

            with self.assertRaises(AttributeError):
                runtime.cached_info = fake_http.info
            with self.assertRaises(AttributeError):
                runtime.info = fake_http.info
            with self.assertRaises(AttributeError):
                runtime.refresh
            for name in (
                "egress",
                "files",
                "checkpoints",
            ):
                with self.subTest(name=name):
                    with self.assertRaises(AttributeError):
                        setattr(runtime, name, object())

        asyncio.run(check())

    def test_status_filter_accepts_canonical_statuses(self) -> None:
        self.assertEqual(
            _status_filter(["running", "shutdown"]),
            {RuntimeStatus.RUNNING, RuntimeStatus.SHUTDOWN},
        )
        with self.assertRaisesRegex(ValueError, "unknown runtime status: stopped"):
            _status_filter("stopped")

    def test_host_from_url_normalizes_hosts(self) -> None:
        self.assertEqual(
            _host_from_url("https://API.GitHub.com/repos/x/y"), "api.github.com"
        )
        self.assertEqual(_host_from_url("gitlab.com"), "gitlab.com")

    def test_command_parts_wraps_cwd(self) -> None:
        command, args = _command_parts("pwd", cwd="/tmp/work dir")
        self.assertEqual(command, "sh")
        self.assertIn("cd '/tmp/work dir' && pwd", args[-1])

    def test_status_query_uses_canonical_runtime_statuses(self) -> None:
        self.assertEqual(_status_query(["running", "shutdown"]), "running,shutdown")

    def test_sync_boot_waits_until_running(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.CREATING, RuntimeStatus.RUNNING])
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        with patch("runta.time.sleep", return_value=None):
            returned = runtime.boot(poll_interval=0)

        self.assertIsNone(returned)
        self.assertIs(runtime.cached_info, fake_http.info)
        self.assertEqual(runtime.cached_info.status, RuntimeStatus.RUNNING)
        self.assertEqual(fake_http.boot_calls, 1)
        self.assertEqual(fake_http.status_calls, 2)

    def test_sync_boot_can_skip_wait_and_has_no_legacy_aliases(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.CREATING])
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        returned = runtime.boot(wait=False)

        self.assertIsNone(returned)
        self.assertEqual(fake_http.status_updates, ["boot"])
        self.assertEqual(fake_http.status_calls, 0)
        self.assertFalse(hasattr(runtime, "start"))
        self.assertFalse(hasattr(runtime, "stop"))

    def test_sync_shutdown_requests_shutdown_without_ready_polling(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        returned = runtime.shutdown()

        self.assertIsNone(returned)
        self.assertEqual(fake_http.status_updates, ["shutdown"])
        self.assertEqual(fake_http.status_calls, 0)

    def test_sync_boot_fails_fast_on_terminal_state(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.ERROR])
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        with self.assertRaisesRegex(RuntimeError, "entered error state"):
            runtime.boot(poll_interval=0)

        self.assertEqual(fake_http.status_updates, ["boot"])
        self.assertEqual(fake_http.status_calls, 1)

    def test_sync_create_waits_until_ready(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.CREATING, RuntimeStatus.RUNNING])
        manager = RuntimeManager._from_owner(SimpleNamespace(_http=fake_http))

        with patch("runta.time.sleep", return_value=None):
            runtime = manager.create("ready-runtime", poll_interval=0)

        self.assertEqual(runtime.cached_info.status, RuntimeStatus.RUNNING)
        self.assertEqual(fake_http.create_calls, 1)
        self.assertEqual(fake_http.status_calls, 2)

    def test_sync_create_can_skip_ready_wait(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.CREATING])
        manager = RuntimeManager._from_owner(SimpleNamespace(_http=fake_http))

        runtime = manager.create(
            "creating-runtime", memory_mib=1024, memory_max_mib=4096, wait=False
        )

        self.assertEqual(runtime.cached_info.status, RuntimeStatus.CREATING)
        self.assertEqual(fake_http.create_calls, 1)
        self.assertEqual(fake_http.status_calls, 0)
        self.assertEqual(fake_http.create_kwargs["memory_mib"], 1024)
        self.assertEqual(fake_http.create_kwargs["memory_max_mib"], 4096)

    def test_sync_checkpoint_create_waits_until_ready(self) -> None:
        fake_http = _FakeSyncHttp(
            [RuntimeStatus.RUNNING],
            checkpoint_states=[CheckpointState.CREATING, CheckpointState.READY],
        )
        owner = SimpleNamespace(_http=fake_http)
        owner.checkpoints = CheckpointManager._from_owner(owner)
        runtime = Runtime._from_info(owner, fake_http.info)

        with patch("runta.time.sleep", return_value=None):
            checkpoint = runtime.checkpoints.create(
                name="ready-checkpoint", poll_interval=0
            )

        self.assertEqual(checkpoint.state, CheckpointState.READY)
        self.assertEqual(fake_http.checkpoint_create_calls, 1)
        self.assertEqual(fake_http.checkpoint_get_calls, 2)

    def test_sync_checkpoint_create_can_skip_ready_wait(self) -> None:
        fake_http = _FakeSyncHttp(
            [RuntimeStatus.RUNNING],
            checkpoint_states=[CheckpointState.CREATING],
        )
        owner = SimpleNamespace(_http=fake_http)
        owner.checkpoints = CheckpointManager._from_owner(owner)
        runtime = Runtime._from_info(owner, fake_http.info)

        checkpoint = runtime.checkpoints.create(name="creating-checkpoint", wait=False)

        self.assertEqual(checkpoint.state, CheckpointState.CREATING)
        self.assertEqual(fake_http.checkpoint_create_calls, 1)
        self.assertEqual(fake_http.checkpoint_get_calls, 0)

    def test_sync_resume_waits_until_ready(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.PAUSED, RuntimeStatus.RUNNING])
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        with patch("runta.time.sleep", return_value=None):
            returned = runtime.resume(poll_interval=0)

        self.assertIsNone(returned)
        self.assertEqual(fake_http.status_updates, ["resume"])
        self.assertEqual(fake_http.status_calls, 2)

    def test_sync_refresh_info_updates_cached_info(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)
        original_info = runtime.cached_info
        fake_http.info = RuntimeInfo(
            id="runtime-id",
            display_name="runtime-name",
            status=RuntimeStatus.PAUSED,
            ingress_specs=[],
            egress_policy=EgressPolicy(mode=EgressMode.DENYLIST),
            resources=RuntimeResources(
                requests=RuntimeResourceRequests(vcpus=1, memory_mib=1024),
                limits=RuntimeResourceLimits(memory_mib=1024),
            ),
        )

        refreshed = runtime.refresh_info()

        self.assertIs(refreshed, fake_http.info)
        self.assertIs(runtime.cached_info, fake_http.info)
        self.assertIsNot(runtime.cached_info, original_info)
        self.assertEqual(runtime.id, "runtime-id")
        runtime.cached_info.id = "mutated-runtime-id"
        self.assertEqual(runtime.id, "runtime-id")

    def test_async_refresh_info_updates_cached_info(self) -> None:
        async def check() -> None:
            sync_fake = _FakeSyncHttp([RuntimeStatus.RUNNING])
            fake_http = _FakeAsyncRefreshHttp(sync_fake.info)
            runtime = AsyncRuntime._from_info(
                SimpleNamespace(_http=fake_http),
                fake_http.info,
            )
            original_info = runtime.cached_info
            fake_http.info = RuntimeInfo(
                id="runtime-id",
                display_name="runtime-name",
                status=RuntimeStatus.PAUSED,
                ingress_specs=[],
                egress_policy=EgressPolicy(mode=EgressMode.DENYLIST),
                resources=RuntimeResources(
                    requests=RuntimeResourceRequests(vcpus=1, memory_mib=1024),
                    limits=RuntimeResourceLimits(memory_mib=1024),
                ),
            )

            refreshed = await runtime.refresh_info()

            self.assertIs(refreshed, fake_http.info)
            self.assertIs(runtime.cached_info, fake_http.info)
            self.assertIsNot(runtime.cached_info, original_info)
            self.assertEqual(runtime.id, "runtime-id")
            runtime.cached_info.id = "mutated-runtime-id"
            self.assertEqual(runtime.id, "runtime-id")

        asyncio.run(check())

    def test_sync_resize_memory_uses_resource_patch(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        runtime.resize_memory(new_memory_mib=2048)

        resources = fake_http.resource_patch_calls[0]
        self.assertEqual(resources.requests.memory_mib, 2048)
        self.assertEqual(resources.limits.memory_mib, 2048)

    def test_failed_download_does_not_create_destination_directory(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
        fake_http.download_path = Mock(side_effect=ConnectionResetError("lost"))
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "new" / "nested"
            with self.assertRaises(ConnectionResetError):
                runtime.files.download("/remote/file", str(destination) + "/")
            self.assertFalse(destination.exists())

    def test_async_failed_download_does_not_create_destination_directory(self) -> None:
        async def check() -> None:
            fake_http = _FakeAsyncHttp([RuntimeStatus.RUNNING])
            fake_http.download_path = AsyncMock(
                side_effect=ConnectionResetError("lost")
            )
            runtime = AsyncRuntime._from_info(
                SimpleNamespace(_http=fake_http), fake_http.info
            )
            with tempfile.TemporaryDirectory() as temp:
                destination = Path(temp) / "new" / "nested"
                with self.assertRaises(ConnectionResetError):
                    await runtime.files.download("/remote/file", str(destination) + "/")
                self.assertFalse(destination.exists())

        asyncio.run(check())

    def test_sync_set_policy_normalizes_and_deduplicates_hosts(self) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        runtime.egress.set_policy(
            EgressPolicy(
                mode=EgressMode.ALLOWLIST,
                allowed_hosts=[" API.GitHub.com. ", "api.github.com"],
                denied_hosts=[],
            )
        )

        self.assertEqual(
            runtime.cached_info.egress_policy.allowed_hosts, ["api.github.com"]
        )


class _FakeSyncHttp:
    def __init__(
        self,
        statuses: list[RuntimeStatus],
        *,
        checkpoint_states: list[CheckpointState] | None = None,
    ) -> None:
        self._statuses = statuses
        self._checkpoint_states = checkpoint_states or [CheckpointState.READY]
        self.create_calls = 0
        self.create_kwargs = {}
        self.boot_calls = 0
        self.status_calls = 0
        self.status_updates = []
        self.resource_patch_calls = []
        self.checkpoint_create_calls = 0
        self.checkpoint_get_calls = 0
        self.info = RuntimeInfo(
            id="runtime-id",
            display_name="runtime-name",
            resources=RuntimeResources(
                requests=RuntimeResourceRequests(memory_mib=1024, vcpus=1),
                limits=RuntimeResourceLimits(memory_mib=1024),
            ),
            ingress_specs=[],
            status=statuses[0],
            egress_policy=EgressPolicy(),
        )
        self.checkpoint_info = CheckpointInfo(
            id="checkpoint-id",
            display_name="checkpoint-name",
            resources=self.info.resources,
            state=self._checkpoint_states[0],
        )

    def create_runtime(self, name: str | None = None, **kwargs) -> RuntimeInfo:
        self.create_calls += 1
        self.create_kwargs = kwargs
        if name is not None:
            self.info.display_name = name
        return self.info

    def update_runtime_status(self, runtime_id: str, action: str) -> RuntimeInfo:
        if runtime_id != self.info.id:
            raise AssertionError(runtime_id)
        if action not in {"boot", "pause", "resume", "shutdown"}:
            raise AssertionError(action)
        self.status_updates.append(action)
        if action == "boot":
            self.boot_calls += 1
        return self.info

    def get_runtime(self, runtime_id: str) -> RuntimeInfo:
        if runtime_id != self.info.id:
            raise AssertionError(runtime_id)
        index = min(self.status_calls, len(self._statuses) - 1)
        self.info.status = self._statuses[index]
        self.status_calls += 1
        return self.info

    def patch_runtime(self, runtime_id: str, **kwargs) -> RuntimeInfo:
        if runtime_id != self.info.id:
            raise AssertionError(runtime_id)
        if kwargs.get("egress_policy") is not None:
            self.info.egress_policy = kwargs["egress_policy"]
        if kwargs.get("resources") is not None:
            self.resource_patch_calls.append(kwargs["resources"])
        return self.info

    def create_checkpoint(
        self, runtime_id: str, name: str | None = None, kind: str = "full"
    ) -> CheckpointInfo:
        if runtime_id != self.info.id:
            raise AssertionError(runtime_id)
        if kind != "full":
            raise AssertionError(kind)
        self.checkpoint_create_calls += 1
        if name is not None:
            self.checkpoint_info.display_name = name
        return self.checkpoint_info

    def get_checkpoint(self, checkpoint_id: str) -> CheckpointInfo:
        if checkpoint_id != self.checkpoint_info.id:
            raise AssertionError(checkpoint_id)
        index = min(self.checkpoint_get_calls, len(self._checkpoint_states) - 1)
        self.checkpoint_info.state = self._checkpoint_states[index]
        self.checkpoint_get_calls += 1
        return self.checkpoint_info


class _FakeAsyncRefreshHttp:
    def __init__(self, info: RuntimeInfo) -> None:
        self.info = info

    async def get_runtime(self, runtime_id: str) -> RuntimeInfo:
        if runtime_id != self.info.id:
            raise AssertionError(runtime_id)
        return self.info


class RuntimeDeleteTests(unittest.TestCase):
    @patch("runta.time.sleep")
    def test_delete_treats_not_found_as_success(self, sleep: Mock) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
        fake_http.delete_runtime = Mock(
            side_effect=ApiError("not found", status_code=404)
        )
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        runtime.delete()

        fake_http.delete_runtime.assert_called_once_with(fake_http.info.id)
        sleep.assert_not_called()

    @patch("runta.time.sleep")
    def test_delete_does_not_retry_non_transient_error(self, sleep: Mock) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
        error = ApiError("forbidden", status_code=403)
        fake_http.delete_runtime = Mock(side_effect=error)
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        with self.assertRaises(ApiError) as raised:
            runtime.delete()

        self.assertIs(raised.exception, error)
        fake_http.delete_runtime.assert_called_once_with(fake_http.info.id)
        sleep.assert_not_called()

    @patch("runta.time.sleep")
    def test_delete_does_not_add_outer_retries(self, sleep: Mock) -> None:
        fake_http = _FakeSyncHttp([RuntimeStatus.RUNNING])
        error = ApiError("internal", status_code=500)
        fake_http.delete_runtime = Mock(side_effect=error)
        runtime = Runtime._from_info(SimpleNamespace(_http=fake_http), fake_http.info)

        with self.assertRaises(ApiError) as raised:
            runtime.delete()

        self.assertIs(raised.exception, error)
        self.assertEqual(fake_http.delete_runtime.call_count, 1)
        sleep.assert_not_called()


class AsyncRuntimeReadyTests(unittest.IsolatedAsyncioTestCase):
    @patch("runta.asyncio.sleep", new_callable=AsyncMock)
    async def test_async_delete_treats_not_found_as_success(
        self, sleep: AsyncMock
    ) -> None:
        fake_http = _FakeAsyncHttp([RuntimeStatus.RUNNING])
        fake_http.delete_runtime = AsyncMock(
            side_effect=ApiError("not found", status_code=404)
        )
        runtime = AsyncRuntime._from_info(
            SimpleNamespace(_http=fake_http), fake_http.info
        )

        await runtime.delete()

        fake_http.delete_runtime.assert_awaited_once_with(fake_http.info.id)
        sleep.assert_not_awaited()

    @patch("runta.asyncio.sleep", new_callable=AsyncMock)
    async def test_async_delete_does_not_retry_non_transient_error(
        self, sleep: AsyncMock
    ) -> None:
        fake_http = _FakeAsyncHttp([RuntimeStatus.RUNNING])
        error = ApiError("forbidden", status_code=403)
        fake_http.delete_runtime = AsyncMock(side_effect=error)
        runtime = AsyncRuntime._from_info(
            SimpleNamespace(_http=fake_http), fake_http.info
        )

        with self.assertRaises(ApiError) as raised:
            await runtime.delete()

        self.assertIs(raised.exception, error)
        fake_http.delete_runtime.assert_awaited_once_with(fake_http.info.id)
        sleep.assert_not_awaited()

    @patch("runta.asyncio.sleep", new_callable=AsyncMock)
    async def test_async_delete_does_not_add_outer_retries(
        self, sleep: AsyncMock
    ) -> None:
        fake_http = _FakeAsyncHttp([RuntimeStatus.RUNNING])
        error = ApiError("internal", status_code=500)
        fake_http.delete_runtime = AsyncMock(side_effect=error)
        runtime = AsyncRuntime._from_info(
            SimpleNamespace(_http=fake_http), fake_http.info
        )

        with self.assertRaises(ApiError) as raised:
            await runtime.delete()

        self.assertIs(raised.exception, error)
        self.assertEqual(fake_http.delete_runtime.await_count, 1)
        sleep.assert_not_awaited()

    async def test_async_create_waits_until_ready(self) -> None:
        fake_http = _FakeAsyncHttp([RuntimeStatus.CREATING, RuntimeStatus.RUNNING])
        manager = AsyncRuntimeManager._from_owner(SimpleNamespace(_http=fake_http))

        runtime = await manager.create("async-ready-runtime", poll_interval=0)

        self.assertEqual(runtime.cached_info.status, RuntimeStatus.RUNNING)
        self.assertEqual(fake_http.create_calls, 1)
        self.assertEqual(fake_http.status_calls, 2)

    async def test_async_create_can_skip_ready_wait(self) -> None:
        fake_http = _FakeAsyncHttp([RuntimeStatus.CREATING])
        manager = AsyncRuntimeManager._from_owner(SimpleNamespace(_http=fake_http))

        runtime = await manager.create("async-creating-runtime", wait=False)

        self.assertEqual(runtime.cached_info.status, RuntimeStatus.CREATING)
        self.assertEqual(fake_http.create_calls, 1)
        self.assertEqual(fake_http.status_calls, 0)

    async def test_async_checkpoint_create_waits_until_ready(self) -> None:
        fake_http = _FakeAsyncHttp(
            [RuntimeStatus.RUNNING],
            checkpoint_states=[CheckpointState.CREATING, CheckpointState.READY],
        )
        owner = SimpleNamespace(_http=fake_http)
        owner.checkpoints = AsyncCheckpointManager._from_owner(owner)
        runtime = AsyncRuntime._from_info(owner, fake_http.info)

        checkpoint = await runtime.checkpoints.create(
            name="async-ready-checkpoint", poll_interval=0
        )

        self.assertEqual(checkpoint.state, CheckpointState.READY)
        self.assertEqual(fake_http.checkpoint_create_calls, 1)
        self.assertEqual(fake_http.checkpoint_get_calls, 2)

    async def test_async_checkpoint_create_can_skip_ready_wait(self) -> None:
        fake_http = _FakeAsyncHttp(
            [RuntimeStatus.RUNNING],
            checkpoint_states=[CheckpointState.CREATING],
        )
        owner = SimpleNamespace(_http=fake_http)
        owner.checkpoints = AsyncCheckpointManager._from_owner(owner)
        runtime = AsyncRuntime._from_info(owner, fake_http.info)

        checkpoint = await runtime.checkpoints.create(
            name="async-creating-checkpoint", wait=False
        )

        self.assertEqual(checkpoint.state, CheckpointState.CREATING)
        self.assertEqual(fake_http.checkpoint_create_calls, 1)
        self.assertEqual(fake_http.checkpoint_get_calls, 0)

    async def test_async_runtime_boot_waits_until_ready(self) -> None:
        fake_http = _FakeAsyncHttp([RuntimeStatus.CREATING, RuntimeStatus.RUNNING])
        runtime = AsyncRuntime._from_info(
            SimpleNamespace(_http=fake_http), fake_http.info
        )

        returned = await runtime.boot(poll_interval=0)

        self.assertIsNone(returned)
        self.assertEqual(fake_http.status_updates, ["boot"])
        self.assertEqual(fake_http.status_calls, 2)

    async def test_async_boot_can_skip_wait_and_shutdown_does_not_poll(self) -> None:
        fake_http = _FakeAsyncHttp([RuntimeStatus.CREATING])
        runtime = AsyncRuntime._from_info(
            SimpleNamespace(_http=fake_http), fake_http.info
        )

        self.assertIsNone(await runtime.boot(wait=False))
        self.assertIsNone(await runtime.shutdown())

        self.assertEqual(fake_http.status_updates, ["boot", "shutdown"])
        self.assertEqual(fake_http.status_calls, 0)
        self.assertFalse(hasattr(runtime, "start"))
        self.assertFalse(hasattr(runtime, "stop"))

    async def test_async_resume_waits_until_ready(self) -> None:
        fake_http = _FakeAsyncHttp([RuntimeStatus.PAUSED, RuntimeStatus.RUNNING])
        runtime = AsyncRuntime._from_info(
            SimpleNamespace(_http=fake_http), fake_http.info
        )

        returned = await runtime.resume(poll_interval=0)

        self.assertIsNone(returned)
        self.assertEqual(fake_http.status_updates, ["resume"])
        self.assertEqual(fake_http.status_calls, 2)


class _FakeAsyncHttp:
    def __init__(
        self,
        statuses: list[RuntimeStatus],
        *,
        checkpoint_states: list[CheckpointState] | None = None,
    ) -> None:
        self._statuses = statuses
        self._checkpoint_states = checkpoint_states or [CheckpointState.READY]
        self.create_calls = 0
        self.status_calls = 0
        self.status_updates = []
        self.checkpoint_create_calls = 0
        self.checkpoint_get_calls = 0
        self.info = RuntimeInfo(
            id="async-runtime-id",
            display_name="async-runtime-name",
            resources=RuntimeResources(
                requests=RuntimeResourceRequests(memory_mib=1024, vcpus=1),
                limits=RuntimeResourceLimits(memory_mib=1024),
            ),
            ingress_specs=[],
            status=statuses[0],
            egress_policy=EgressPolicy(),
        )
        self.checkpoint_info = CheckpointInfo(
            id="async-checkpoint-id",
            display_name="async-checkpoint-name",
            resources=self.info.resources,
            state=self._checkpoint_states[0],
        )

    async def create_runtime(self, name: str | None = None, **_kwargs) -> RuntimeInfo:
        self.create_calls += 1
        if name is not None:
            self.info.display_name = name
        return self.info

    async def update_runtime_status(self, runtime_id: str, action: str) -> RuntimeInfo:
        if runtime_id != self.info.id:
            raise AssertionError(runtime_id)
        if action not in {"boot", "pause", "resume", "shutdown"}:
            raise AssertionError(action)
        self.status_updates.append(action)
        return self.info

    async def get_runtime(self, runtime_id: str) -> RuntimeInfo:
        if runtime_id != self.info.id:
            raise AssertionError(runtime_id)
        index = min(self.status_calls, len(self._statuses) - 1)
        self.info.status = self._statuses[index]
        self.status_calls += 1
        return self.info

    async def create_checkpoint(
        self, runtime_id: str, name: str | None = None, kind: str = "full"
    ) -> CheckpointInfo:
        if runtime_id != self.info.id:
            raise AssertionError(runtime_id)
        if kind != "full":
            raise AssertionError(kind)
        self.checkpoint_create_calls += 1
        if name is not None:
            self.checkpoint_info.display_name = name
        return self.checkpoint_info

    async def get_checkpoint(self, checkpoint_id: str) -> CheckpointInfo:
        if checkpoint_id != self.checkpoint_info.id:
            raise AssertionError(checkpoint_id)
        index = min(self.checkpoint_get_calls, len(self._checkpoint_states) - 1)
        self.checkpoint_info.state = self._checkpoint_states[index]
        self.checkpoint_get_calls += 1
        return self.checkpoint_info


if __name__ == "__main__":
    unittest.main()
