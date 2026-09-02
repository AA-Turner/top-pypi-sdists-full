from __future__ import annotations

import base64
import builtins
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timedelta, timezone
import json
from typing import (
    Any,
    AsyncIterator,
    BinaryIO,
    Iterable,
    Optional,
    TypedDict,
    Union,
    cast,
)
from typing_extensions import Literal, NotRequired, TypeAlias
import httpx

from .stream import Streamable, complete_stream, start_stream
from .utils import convert_to_snake_case
from .env import AsyncSandboxEnv, SandboxEnv
from .fs import AsyncSandboxFs, SandboxFs
from .process import (
    AbortSignal,
    AsyncChildProcess,
    AsyncDenoProcess,
    AsyncDenoRepl,
    ChildProcess,
    DenoProcess,
    DenoRepl,
    ProcessSpawnResult,
    RemoteProcessOptions,
)
from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    ExposeSSHResult,
    PaginatedList,
)
from .rpc import AsyncFetchResponse, AsyncRpcClient, FetchResponse
from .transport import (
    WebSocketTransport,
)
from .options import get_sandbox_ws_url
from .revisions import Revision


Mode: TypeAlias = Literal["connect", "create"]
StdIo: TypeAlias = Literal["piped", "null"]


class SandboxMeta(TypedDict):
    id: str
    """The unique identifier for the sandbox."""

    created_at: str
    """The ISO 8601 timestamp when the sandbox was created."""

    region: str
    """The region the sandbox is located in."""

    status: Literal["running", "stopped"]
    """The status of the sandbox."""

    stopped_at: NotRequired[str | None]
    """The ISO 8601 timestamp when the sandbox was stopped."""


class SecretConfig(TypedDict):
    """List of hostnames where this secret can be used. Must have at least one host."""

    hosts: builtins.list[str]
    value: str


class VolumeInfo(TypedDict):
    volume: str
    path: str


class AppConfigVolume(TypedDict):
    volume: str


class AppConfig(TypedDict):
    stop_at_ms: NotRequired[int | None]
    labels: NotRequired[dict[str, str] | None]
    memory_mb: NotRequired[int | None]
    volumes: NotRequired[builtins.list[VolumeInfo] | None]
    allow_net: NotRequired[builtins.list[str] | None]
    root: NotRequired[AppConfigVolume | None]
    secrets: NotRequired[dict[str, SecretConfig] | None]


class ExposeHTTPResult(TypedDict):
    domain: str


class BuildLog(TypedDict):
    """A build log entry from app deployment."""

    timestamp: str
    """The timestamp of the build log."""

    level: Literal["info", "error"]
    """The level of the build log."""

    message: str
    """The message of the build log."""


class AsyncSandboxApi:
    def __init__(
        self,
        client: AsyncConsoleClient,
    ):
        self._client = client

    @asynccontextmanager
    async def create(
        self,
        *,
        region: Optional[str] = None,
        env: Optional[dict[str, str]] = None,
        timeout: Optional[str] = None,
        memory_mb: Optional[int] = None,
        debug: Optional[bool] = None,
        labels: Optional[dict[str, str]] = None,
        root: Optional[str] = None,
        volumes: Optional[dict[str, str]] = None,
        allow_net: Optional[builtins.list[str]] = None,
        secrets: Optional[dict[str, SecretConfig]] = None,
        ssh: Optional[bool] = None,
        port: Optional[int] = None,
    ) -> AsyncIterator[AsyncSandbox]:
        """Creates a new sandbox instance.

        Args:
            region: The region where the sandbox should be created.
            env: Environment variables to start the sandbox with.
            timeout: The timeout of the sandbox. Defaults to "session". Other values like "30s" or "2m" are supported.
            memory_mb: The memory size in MiB of the sandbox. Defaults to 1280.
            debug: Enable debug logging for the sandbox connection.
            labels: Labels to set on the sandbox. Up to 5 labels can be specified.
            root: A volume or snapshot to use as the root filesystem of the sandbox.
            volumes: Volumes to mount on the sandbox. The key is the mount path, the value is the volume ID or slug.
            allow_net: List of hostnames/IP addresses the sandbox can make outbound requests to.
            secrets: Secret environment variables injected on the wire for HTTPS requests.
            ssh: Whether to expose SSH access to the sandbox.
            port: The port number to expose for HTTP access.
        """
        config_dict: dict[str, Any] = {
            "memory_mb": memory_mb if memory_mb is not None else 1280,
            "debug": debug if debug is not None else False,
        }

        if region is not None:
            config_dict["region"] = region
        if env is not None:
            config_dict["env"] = env
        if timeout is not None:
            config_dict["timeout"] = timeout
        if labels is not None:
            config_dict["labels"] = labels
        if root is not None:
            config_dict["root"] = {"volume": root}
        if volumes is not None:
            config_dict["volumes"] = volumes
        if allow_net is not None:
            config_dict["allow_net"] = allow_net
        if secrets is not None:
            config_dict["secrets"] = secrets
        if ssh is not None:
            config_dict["ssh"] = ssh
        if port is not None:
            config_dict["port"] = port

        app_config = cast(AppConfig, config_dict)

        json_config = json.dumps(app_config, separators=(",", ":")).encode("utf-8")

        ws_base = get_sandbox_ws_url(self._client._options, region)
        url = ws_base.join("/api/v3/sandboxes/create")
        token = self._client._options["token"]

        transport = WebSocketTransport(debug=debug if debug is not None else False)
        ws = await transport.connect(
            url=url,
            headers={
                "Authorization": f"Bearer {token}",
                "x-deno-sandbox-config": base64.b64encode(json_config).decode("utf-8"),
            },
        )

        response = ws.response
        if response is None:
            raise Exception("No response received")

        if response.headers is None:
            raise Exception("No response headers received")

        sandbox_id = response.headers.get("x-deno-sandbox-id")
        if sandbox_id is None:
            raise Exception("Sandbox ID not found in response headers")

        if debug:
            print(f"Trace ID: {response.headers.get('x-deno-trace-id', 'n/a')}")

        sandbox = None
        try:
            rpc = AsyncRpcClient(transport)
            sandbox = AsyncSandbox(
                self._client,
                rpc,
                sandbox_id,
                trace_id=response.headers.get("x-deno-trace-id"),
            )
            yield sandbox
        finally:
            if sandbox is not None:
                await sandbox.close()

    @asynccontextmanager
    async def connect(
        self,
        sandbox_id: str,
        *,
        debug: Optional[bool] = None,
    ) -> AsyncIterator[AsyncSandbox]:
        """Connects to an existing sandbox instance.

        Args:
            sandbox_id: The unique id of the sandbox to connect to.
            debug: Enable debug logging for the sandbox connection.
        """
        url = self._client._options["sandbox_ws_url"].join(
            f"/api/v3/sandbox/{sandbox_id}/connect"
        )
        token = self._client._options["token"]
        transport = WebSocketTransport(debug=debug if debug is not None else False)
        await transport.connect(
            url=url,
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        sandbox = None
        try:
            rpc = AsyncRpcClient(transport)
            sandbox = AsyncSandbox(self._client, rpc, sandbox_id)
            yield sandbox
        finally:
            if sandbox is not None:
                await sandbox.close()

    async def list(
        self,
        *,
        labels: Optional[dict[str, str]] = None,
    ) -> AsyncPaginatedList[SandboxMeta]:
        """List sandboxes.

        Args:
            labels: Filter sandboxes by labels.
        """
        options: dict[str, Any] = {}
        if labels is not None:
            options["labels"] = labels
        return await self._client.get_paginated(
            path="/api/v3/sandboxes", cursor=None, params=options if options else None
        )


class SandboxApi:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._bridge = bridge
        self._client = client
        self._async = AsyncSandboxApi(client)

    @contextmanager
    def create(
        self,
        *,
        region: Optional[str] = None,
        env: Optional[dict[str, str]] = None,
        timeout: Optional[str] = None,
        memory_mb: Optional[int] = None,
        debug: Optional[bool] = None,
        labels: Optional[dict[str, str]] = None,
        root: Optional[str] = None,
        volumes: Optional[dict[str, str]] = None,
        allow_net: Optional[builtins.list[str]] = None,
        secrets: Optional[dict[str, SecretConfig]] = None,
        ssh: Optional[bool] = None,
        port: Optional[int] = None,
    ):
        """Creates a new sandbox instance.

        Args:
            region: The region where the sandbox should be created.
            env: Environment variables to start the sandbox with.
            timeout: The timeout of the sandbox. Defaults to "session". Other values like "30s" or "2m" are supported.
            memory_mb: The memory size in MiB of the sandbox. Defaults to 1280.
            debug: Enable debug logging for the sandbox connection.
            labels: Labels to set on the sandbox. Up to 5 labels can be specified.
            root: A volume or snapshot to use as the root filesystem of the sandbox.
            volumes: Volumes to mount on the sandbox. The key is the mount path, the value is the volume ID or slug.
            allow_net: List of hostnames/IP addresses the sandbox can make outbound requests to.
            secrets: Secret environment variables injected on the wire for HTTPS requests.
            ssh: Whether to expose SSH access to the sandbox.
            port: The port number to expose for HTTP access.
        """
        async_cm = self._async.create(
            region=region,
            env=env,
            timeout=timeout,
            memory_mb=memory_mb,
            debug=debug,
            labels=labels,
            root=root,
            volumes=volumes,
            allow_net=allow_net,
            secrets=secrets,
            ssh=ssh,
            port=port,
        )
        async_handle = self._bridge.run(async_cm.__aenter__())

        try:
            yield Sandbox(self._client, self._bridge, async_handle._rpc, async_handle)
        except Exception:
            import sys

            self._bridge.run(async_cm.__aexit__(*sys.exc_info()))
            raise
        finally:
            self._bridge.run(async_cm.__aexit__(None, None, None))

    @contextmanager
    def connect(
        self,
        sandbox_id: str,
        *,
        debug: Optional[bool] = None,
    ):
        """Connects to an existing sandbox instance.

        Args:
            sandbox_id: The unique id of the sandbox to connect to.
            debug: Enable debug logging for the sandbox connection.
        """
        async_cm = self._async.connect(sandbox_id, debug=debug)
        async_handle = self._bridge.run(async_cm.__aenter__())

        try:
            yield Sandbox(self._client, self._bridge, async_handle._rpc, async_handle)
        except Exception:
            import sys

            self._bridge.run(async_cm.__aexit__(*sys.exc_info()))
            raise
        finally:
            self._bridge.run(async_cm.__aexit__(None, None, None))

    def list(
        self,
        *,
        labels: Optional[dict[str, str]] = None,
    ) -> PaginatedList[SandboxMeta]:
        """List sandboxes.

        Args:
            labels: Filter sandboxes by labels.
        """
        paginated = self._bridge.run(self._async.list(labels=labels))
        return PaginatedList(self._bridge, paginated)


async def _parse_sse_stream(stream: AsyncIterator[bytes]) -> AsyncIterator[str]:
    """Parse Server-Sent Events from a byte stream."""
    buffer = b""
    async for chunk in stream:
        buffer += chunk
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            line = line.rstrip(b"\r")
            if line.startswith(b"data: "):
                data = line[6:].decode("utf-8")
                yield data


class AsyncBuild:
    """The result of a deno.deploy() operation."""

    def __init__(
        self,
        revision_id: str,
        app: str,
        client: AsyncConsoleClient,
    ):
        self.id = revision_id
        """The ID of the build."""
        self._app = app
        self._client = client

    async def wait(self) -> Revision:
        """A coroutine that resolves when the build is complete, returning the revision."""

        url = self._client._options["console_url"].join(
            f"/api/v2/revisions/{self.id}/progress"
        )
        headers = {
            "Authorization": f"Bearer {self._client._options['token']}",
        }

        # Stream NDJSON progress updates until the stream closes.
        # Use a long read timeout since builds can take a while.
        timeout = httpx.Timeout(10.0, read=120.0)
        async with httpx.AsyncClient(timeout=timeout) as http_client:
            async with http_client.stream("GET", str(url), headers=headers) as response:
                response.raise_for_status()
                async for _line in response.aiter_lines():
                    pass  # consume progress updates until stream ends

            # Fetch the final revision state
            revision_url = self._client._options["console_url"].join(
                f"/api/v2/revisions/{self.id}"
            )
            revision_response = await http_client.get(
                str(revision_url), headers=headers
            )
            revision_response.raise_for_status()
            revision_data = revision_response.json()

            return cast(Revision, convert_to_snake_case(revision_data))

    async def logs(self) -> AsyncIterator[BuildLog]:
        """An async iterator of build logs."""
        url = self._client._options["console_url"].join(
            f"/api/v2/revisions/{self.id}/build_logs"
        )
        headers = {
            "Authorization": f"Bearer {self._client._options['token']}",
        }

        timeout = httpx.Timeout(10.0, read=120.0)
        async with httpx.AsyncClient(timeout=timeout) as http_client:
            async with http_client.stream("GET", str(url), headers=headers) as response:
                response.raise_for_status()
                async for data in _parse_sse_stream(response.aiter_bytes()):
                    try:
                        yield cast(BuildLog, json.loads(data))
                    except json.JSONDecodeError:
                        # Skip malformed log entries
                        continue


class Build:
    """The result of a deno.deploy() operation (sync version)."""

    def __init__(
        self,
        revision_id: str,
        app: str,
        client: AsyncConsoleClient,
        bridge: AsyncBridge,
    ):
        self.id = revision_id
        """The ID of the build."""
        self._async_build = AsyncBuild(revision_id, app, client)
        self._bridge = bridge

    def wait(self) -> Revision:
        """Returns the revision when the build is complete."""
        return self._bridge.run(self._async_build.wait())

    def logs(self) -> builtins.list[BuildLog]:
        """Returns a list of build logs."""

        async def _collect_logs():
            logs = []
            async for log in self._async_build.logs():
                logs.append(log)
            return logs

        return self._bridge.run(_collect_logs())


class AsyncSandboxDeno:
    def __init__(
        self,
        rpc: AsyncRpcClient,
        processes: builtins.list[AsyncChildProcess],
        client: AsyncConsoleClient,
        sandbox_id: str,
    ):
        self._rpc = rpc
        self._processes = processes
        self._client = client
        self._sandbox_id = sandbox_id

    async def run(
        self,
        *,
        args: Optional[builtins.list[str]] = None,
        cwd: Optional[str] = None,
        clear_env: Optional[bool] = None,
        env: Optional[dict[str, str]] = None,
        signal: Optional[AbortSignal] = None,
        stdin: Optional[Literal["piped", "null"]] = None,
        stdout: Optional[Literal["piped", "null", "inherit"]] = None,
        stderr: Optional[Literal["piped", "null", "inherit"]] = None,
        script_args: Optional[list[str]] = None,
        entrypoint: Optional[str] = None,
        code: Optional[str] = None,
        extension: Optional[
            Literal["js", "cjs", "mjs", "ts", "cts", "mts", "jsx", "tsx"]
        ] = None,
        stdin_data: Optional[Streamable] = None,
    ) -> AsyncDenoProcess:
        """Create a new Deno process from the specified entrypoint file or code.

        Args:
            args: Arguments to pass to the process.
            cwd: The working directory of the process.
            clear_env: Clear environment variables from parent process.
            env: Environment variables to pass to the subprocess.
            signal: An abort signal to cancel the process.
            stdin: How stdin of the spawned process should be handled.
            stdout: How stdout of the spawned process should be handled.
            stderr: How stderr of the spawned process should be handled.
            script_args: Arguments to pass to the Deno runtime, available as Deno.args.
            entrypoint: A module to read from disk and execute as the entrypoint.
            code: Deno code to execute as the entrypoint.
            extension: File extension to use when executing code. Default is 'ts'.
            stdin_data: Data to write to stdin of the process.
        """
        params: dict[str, Any] = {
            "stdout": stdout if stdout is not None else "inherit",
            "stderr": stderr if stderr is not None else "inherit",
        }

        if args is not None:
            params["args"] = args
        if cwd is not None:
            params["cwd"] = cwd
        if clear_env is not None:
            params["clear_env"] = clear_env
        if env is not None:
            params["env"] = env
        if signal is not None:
            params["signal"] = signal
        if stdin is not None:
            params["stdin"] = stdin
        if script_args is not None:
            params["script_args"] = script_args
        if entrypoint is not None:
            params["entrypoint"] = entrypoint
        if code is not None:
            params["code"] = code
        if extension is not None:
            params["extension"] = extension

        if "code" in params and "extension" not in params:
            params["extension"] = "ts"

        # If stdin data is provided, start stream first (but don't send data yet)
        stdin_writer = None
        if stdin_data is not None:
            params["stdin"] = "piped"
            stdin_stream_id, stdin_writer = await start_stream(self._rpc)
            params["stdinStreamId"] = stdin_stream_id

        opts = RemoteProcessOptions(
            stdout_inherit=params["stdout"] == "inherit",
            stderr_inherit=params["stderr"] == "inherit",
        )

        if params["stdout"] == "inherit":
            params["stdout"] = "piped"
        if params["stderr"] == "inherit":
            params["stderr"] = "piped"

        result = await self._rpc.call("spawnDeno", params)

        # Now that process is spawned, complete the stdin stream
        if stdin_writer is not None and stdin_data is not None:
            await complete_stream(stdin_writer, stdin_data)

        process = await AsyncDenoProcess.create(
            result, self._rpc, opts, self._processes
        )
        self._processes.append(process)
        return process

    async def eval(self, code: str) -> Any:
        repl = await self.repl()
        result = await repl.eval(code)
        await repl.close()
        return result

    async def repl(
        self,
        *,
        args: Optional[builtins.list[str]] = None,
        cwd: Optional[str] = None,
        clear_env: Optional[bool] = None,
        env: Optional[dict[str, str]] = None,
        signal: Optional[AbortSignal] = None,
        stdin: Optional[Literal["piped", "null"]] = None,
        stdout: Optional[Literal["piped", "null", "inherit"]] = None,
        stderr: Optional[Literal["piped", "null", "inherit"]] = None,
        script_args: Optional[builtins.list[str]] = None,
    ) -> AsyncDenoRepl:
        """Create a new Deno REPL process.

        Args:
            args: Arguments to pass to the process.
            cwd: The working directory of the process.
            clear_env: Clear environment variables from parent process.
            env: Environment variables to pass to the subprocess.
            signal: An abort signal to cancel the process.
            stdin: How stdin of the spawned process should be handled.
            stdout: How stdout of the spawned process should be handled.
            stderr: How stderr of the spawned process should be handled.
            script_args: Arguments to pass to the Deno runtime, available as Deno.args.
        """
        params: dict[str, Any] = {"stdout": "piped", "stderr": "piped"}

        opts = RemoteProcessOptions(stdout_inherit=True, stderr_inherit=True)

        if args is not None:
            params["args"] = args
        if cwd is not None:
            params["cwd"] = cwd
        if clear_env is not None:
            params["clearEnv"] = clear_env
        if env is not None:
            params["env"] = env
        if signal is not None:
            params["signal"] = signal
        if stdin is not None:
            params["stdin"] = stdin
        if stdout is not None:
            params["stdout"] = stdout
            if stdout != "inherit":
                opts["stdout_inherit"] = False
        if stderr is not None:
            params["stderr"] = stderr
            if stderr != "inherit":
                opts["stderr_inherit"] = False
        if script_args is not None:
            params["scriptArgs"] = script_args

        result: ProcessSpawnResult = await self._rpc.call("spawnDenoRepl", params)

        process = await AsyncDenoRepl.create(result, self._rpc, opts, self._processes)
        self._processes.append(process)
        return process

    async def deploy(
        self,
        app: str,
        *,
        entrypoint: Optional[str] = None,
        args: Optional[builtins.list[str]] = None,
        path: Optional[str] = None,
        production: Optional[bool] = None,
        preview: Optional[bool] = None,
    ) -> AsyncBuild:
        """Deploy the contents of the sandbox to the specified app in Deno Deploy platform.

        Args:
            app: The app ID or slug to deploy to.
            entrypoint: The entrypoint file path relative to the path option. Defaults to 'main.ts'.
            args: Arguments to pass to the entrypoint script.
            path: The path to the directory to deploy. If relative, it is relative to /home/app. Defaults to '/home/app'.
            production: Whether to deploy in production mode. Defaults to True.
            preview: Whether to deploy a preview deployment. Defaults to False.

        Returns:
            An AsyncBuild object with the revision ID and methods to check status and logs.

        Example:
            ```python
            from deno_sandbox import AsyncDenoDeploy

            async with AsyncDenoDeploy() as client:
                async with client.sandbox.create() as sandbox:
                    await sandbox.fs.write_text_file(
                        "main.ts",
                        'Deno.serve(() => new Response("Hi from sandbox.deploy()"))',
                    )
                    build = await sandbox.deno.deploy("my-deno-app", entrypoint="main.ts")
                    print(f"Deployed revision ID: {build.id}")
                    revision = await build.done
                    print(f"Revision status: {revision['status']}")
            ```
        """
        url = self._client._options["console_url"].join(
            f"/api/v2/sandboxes/{self._sandbox_id}/deploy"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._client._options['token']}",
        }

        # Build request body
        body: dict[str, Any] = {
            "app": app,
            "entrypoint": entrypoint if entrypoint is not None else "main.ts",
            "path": path if path is not None else "/home/app",
            "mode": "none",
            "frameworkPreset": "",
        }

        if args is not None:
            body["args"] = args
        if production is not None:
            body["production"] = production
        if preview is not None:
            body["preview"] = preview

        # Make the deploy request
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                str(url), headers=headers, json=body, timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            revision_id = result["revision_id"]

        return AsyncBuild(revision_id, app, self._client)


class SandboxDeno:
    def __init__(
        self,
        rpc: AsyncRpcClient,
        bridge: AsyncBridge,
        processes: builtins.list[AsyncChildProcess],
        client: AsyncConsoleClient,
        sandbox_id: str,
    ):
        self._rpc = rpc
        self._bridge = bridge
        self._client = client

        self._async = AsyncSandboxDeno(rpc, processes, client, sandbox_id)

    def run(
        self,
        *,
        args: Optional[builtins.list[str]] = None,
        cwd: Optional[str] = None,
        clear_env: Optional[bool] = None,
        env: Optional[dict[str, str]] = None,
        signal: Optional[AbortSignal] = None,
        stdin: Optional[Literal["piped", "null"]] = None,
        stdout: Optional[Literal["piped", "null", "inherit"]] = None,
        stderr: Optional[Literal["piped", "null", "inherit"]] = None,
        script_args: Optional[builtins.list[str]] = None,
        entrypoint: Optional[str] = None,
        code: Optional[str] = None,
        extension: Optional[
            Literal["js", "cjs", "mjs", "ts", "cts", "mts", "jsx", "tsx"]
        ] = None,
        stdin_data: Optional[Union[Iterable[bytes], BinaryIO]] = None,
    ) -> DenoProcess:
        """Create a new Deno process from the specified entrypoint file or code.

        Args:
            args: Arguments to pass to the process.
            cwd: The working directory of the process.
            clear_env: Clear environment variables from parent process.
            env: Environment variables to pass to the subprocess.
            signal: An abort signal to cancel the process.
            stdin: How stdin of the spawned process should be handled.
            stdout: How stdout of the spawned process should be handled.
            stderr: How stderr of the spawned process should be handled.
            script_args: Arguments to pass to the Deno runtime, available as Deno.args.
            entrypoint: A module to read from disk and execute as the entrypoint.
            code: Deno code to execute as the entrypoint.
            extension: File extension to use when executing code. Default is 'ts'.
            stdin_data: Data to write to stdin of the process.
        """
        async_deno = self._bridge.run(
            self._async.run(
                args=args,
                cwd=cwd,
                clear_env=clear_env,
                env=env,
                signal=signal,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                script_args=script_args,
                entrypoint=entrypoint,
                code=code,
                extension=extension,
                stdin_data=stdin_data,
            )
        )
        return DenoProcess(self._rpc, self._bridge, async_deno)

    def eval(self, code: str) -> Any:
        return self._bridge.run(self._async.eval(code))

    def repl(
        self,
        *,
        args: Optional[builtins.list[str]] = None,
        cwd: Optional[str] = None,
        clear_env: Optional[bool] = None,
        env: Optional[dict[str, str]] = None,
        signal: Optional[AbortSignal] = None,
        stdin: Optional[Literal["piped", "null"]] = None,
        stdout: Optional[Literal["piped", "null", "inherit"]] = None,
        stderr: Optional[Literal["piped", "null", "inherit"]] = None,
        script_args: Optional[builtins.list[str]] = None,
    ) -> DenoRepl:
        """Create a new Deno REPL process.

        Args:
            args: Arguments to pass to the process.
            cwd: The working directory of the process.
            clear_env: Clear environment variables from parent process.
            env: Environment variables to pass to the subprocess.
            signal: An abort signal to cancel the process.
            stdin: How stdin of the spawned process should be handled.
            stdout: How stdout of the spawned process should be handled.
            stderr: How stderr of the spawned process should be handled.
            script_args: Arguments to pass to the Deno runtime, available as Deno.args.
        """
        async_repl = self._bridge.run(
            self._async.repl(
                args=args,
                cwd=cwd,
                clear_env=clear_env,
                env=env,
                signal=signal,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                script_args=script_args,
            )
        )
        return DenoRepl(self._rpc, self._bridge, async_repl)

    def deploy(
        self,
        app: str,
        *,
        entrypoint: Optional[str] = None,
        args: Optional[builtins.list[str]] = None,
        path: Optional[str] = None,
        production: Optional[bool] = None,
        preview: Optional[bool] = None,
    ) -> Build:
        """Deploy the contents of the sandbox to the specified app in Deno Deploy platform.

        Args:
            app: The app ID or slug to deploy to.
            entrypoint: The entrypoint file path relative to the path option. Defaults to 'main.ts'.
            args: Arguments to pass to the entrypoint script.
            path: The path to the directory to deploy. If relative, it is relative to /home/app. Defaults to '/home/app'.
            production: Whether to deploy in production mode. Defaults to True.
            preview: Whether to deploy a preview deployment. Defaults to False.

        Returns:
            A Build object with the revision ID and methods to check status and logs.

        Example:
            ```python
            from deno_sandbox import DenoDeploy

            client = DenoDeploy()
            with client.sandbox.create() as sandbox:
                sandbox.fs.write_text_file(
                    "main.ts",
                    'Deno.serve(() => new Response("Hi from sandbox.deploy()"))',
                )
                build = sandbox.deno.deploy("my-deno-app", entrypoint="main.ts")
                print(f"Deployed revision ID: {build.id}")
                revision = build.done
                print(f"Revision status: {revision['status']}")
            ```
        """
        async_build = self._bridge.run(
            self._async.deploy(
                app,
                entrypoint=entrypoint,
                args=args,
                path=path,
                production=production,
                preview=preview,
            )
        )
        return Build(async_build.id, app, self._client, self._bridge)


class AsyncSandbox:
    def __init__(
        self,
        client: AsyncConsoleClient,
        rpc: AsyncRpcClient,
        sandbox_id: str,
        trace_id: str | None = None,
    ):
        self._client = client
        self._rpc = rpc
        self._processes: builtins.list[AsyncChildProcess] = []

        self.url: str | None = None
        self.ssh: None = None
        self.id = sandbox_id
        self.trace_id: str | None = trace_id
        self.fs = AsyncSandboxFs(rpc)
        self.deno = AsyncSandboxDeno(rpc, self._processes, client, sandbox_id)
        self.env = AsyncSandboxEnv(rpc)

    @property
    def closed(self) -> bool:
        return self._rpc._transport.closed

    async def spawn(
        self,
        command: str,
        *,
        args: Optional[list[str]] = None,
        cwd: Optional[str] = None,
        clear_env: Optional[bool] = None,
        env: Optional[dict[str, str]] = None,
        signal: Optional[AbortSignal] = None,
        stdin: Optional[Literal["piped", "null"]] = None,
        stdout: Optional[Literal["piped", "null", "inherit"]] = None,
        stderr: Optional[Literal["piped", "null", "inherit"]] = None,
        stdin_data: Optional[Streamable] = None,
    ) -> AsyncChildProcess:
        """Spawn a new child process.

        Args:
            command: The command to execute.
            args: Arguments to pass to the process.
            cwd: The working directory of the process.
            clear_env: Clear environment variables from parent process.
            env: Environment variables to pass to the subprocess.
            signal: An abort signal to cancel the process.
            stdin: How stdin of the spawned process should be handled.
            stdout: How stdout of the spawned process should be handled.
            stderr: How stderr of the spawned process should be handled.
            stdin_data: Data to write to stdin of the process.
        """
        params: dict[str, Any] = {
            "command": command,
            "stdout": stdout if stdout is not None else "inherit",
            "stderr": stderr if stderr is not None else "inherit",
        }

        if args is not None:
            params["args"] = args
        if cwd is not None:
            params["cwd"] = cwd
        if clear_env is not None:
            params["clear_env"] = clear_env
        if env is not None:
            params["env"] = env
        if signal is not None:
            params["signal"] = signal
        if stdin is not None:
            params["stdin"] = stdin

        # If stdin data is provided, start stream first (but don't send data yet)
        stdin_writer = None
        if stdin_data is not None:
            params["stdin"] = "piped"
            stdin_stream_id, stdin_writer = await start_stream(self._rpc)
            params["stdinStreamId"] = stdin_stream_id

        opts = RemoteProcessOptions(
            stdout_inherit=params["stdout"] == "inherit",
            stderr_inherit=params["stderr"] == "inherit",
        )

        if params["stdout"] == "inherit":
            params["stdout"] = "piped"
        if params["stderr"] == "inherit":
            params["stderr"] = "piped"

        result: ProcessSpawnResult = await self._rpc.call("spawn", params)

        # Now that process is spawned, complete the stdin stream
        if stdin_writer is not None and stdin_data is not None:
            await complete_stream(stdin_writer, stdin_data)

        process = await AsyncChildProcess.create(
            result, self._rpc, opts, self._processes
        )
        self._processes.append(process)
        return process

    async def fetch(
        self,
        url: str,
        *,
        method: Optional[str] = "GET",
        headers: Optional[dict[str, str]] = None,
        redirect: Optional[Literal["follow", "manual"]] = None,
    ) -> AsyncFetchResponse:
        return await self._rpc.fetch(url, method, headers, redirect)

    async def close(self) -> None:
        # Kill all tracked processes
        for process in self._processes:
            await process.kill()
        self._processes.clear()
        await self._rpc.close()

    async def kill(self) -> None:
        await self._client.delete(f"/api/v3/sandboxes/{self.id}")

    async def extend_timeout(self, additional_s: int) -> datetime:
        """Request to extend the timeout of the sandbox by the specified duration.
        You can at max extend timeout of a sandbox by 30 minutes at once.

        Please note the extension is not guranteed to be the same as requested time.
        You should rely on the returned Date value to know the exact extension time.
        """

        now = datetime.now(timezone.utc)
        future_time = now + timedelta(seconds=additional_s)
        stop_at_ms = int(future_time.timestamp() * 1000)

        url = self._client._options["sandbox_url"].join(f"/api/v3/sandbox/{self.id}")
        result = await self._client._request("PATCH", url, {"stop_at_ms": stop_at_ms})
        data = result.json()

        return datetime.fromtimestamp(data["stop_at_ms"] / 1000, tz=timezone.utc)

    async def expose_http(
        self, *, port: Optional[int] = None, pid: Optional[int] = None
    ) -> str:
        """Publicly expose a HTTP service via a publicly routeable URL.

        NOTE: when you call this API, the target HTTP service will be PUBLICLY
        EXPOSED WITHOUT AUTHENTICATION. Anyone with knowledge of the public domain
        will be able to send arbitrary requests to the exposed service.

        An exposed service can either be a service listening on an arbitrary HTTP
        port, or a JavaScript runtime that can handle HTTP requests.
        """

        if port is not None and pid is not None:
            raise ValueError("Only one of port or pid can be specified")

        params: dict[str, Any] = {}
        if port is not None:
            params["port"] = port
        if pid is not None:
            params["pid"] = pid

        url = self._client._options["sandbox_url"].join(
            f"/api/v3/sandbox/{self.id}/expose/http"
        )
        result = await self._client._request("POST", url, params)
        data = cast(ExposeHTTPResult, result.json())
        domain = data["domain"]

        params["domain"] = domain
        await self._rpc.call("exposeHttp", params)

        return f"https://{domain}"

    async def expose_ssh(self) -> ExposeSSHResult:
        """Expose an isolate over SSH, allowing access to the isolate's shell.

        NOTE: The SSH connection is authenticated through the 'username' field. This field is populated
        with a randomly generated, unique identifier. Anyone with knowledge of the 'username' can
        connect to the isolate's shell without further authentication.
        """

        url = self._client._options["sandbox_url"].join(
            f"/api/v3/sandbox/{self.id}/expose/ssh"
        )
        response = await self._client._request("POST", url, {})

        return cast(ExposeSSHResult, response.json())

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class Sandbox:
    def __init__(
        self,
        client: AsyncConsoleClient,
        bridge: AsyncBridge,
        rpc: AsyncRpcClient,
        async_sandbox: AsyncSandbox,
    ):
        self._client = client
        self._bridge = bridge
        self._rpc = rpc
        self._async = async_sandbox

        self.url: str | None = None
        self.ssh: None = None
        self.id = async_sandbox.id
        self.trace_id: str | None = async_sandbox.trace_id
        self.fs = SandboxFs(rpc, bridge)
        self.deno = SandboxDeno(
            rpc, bridge, self._async._processes, client, async_sandbox.id
        )
        self.env = SandboxEnv(rpc, bridge)

    @property
    def closed(self) -> bool:
        return self._rpc._transport.closed

    def spawn(
        self,
        command: str,
        *,
        args: Optional[builtins.list[str]] = None,
        cwd: Optional[str] = None,
        clear_env: Optional[bool] = None,
        env: Optional[dict[str, str]] = None,
        signal: Optional[AbortSignal] = None,
        stdin: Optional[Literal["piped", "null"]] = None,
        stdout: Optional[Literal["piped", "null", "inherit"]] = None,
        stderr: Optional[Literal["piped", "null", "inherit"]] = None,
        stdin_data: Optional[Union[Iterable[bytes], BinaryIO]] = None,
    ) -> ChildProcess:
        """Spawn a new child process.

        Args:
            command: The command to execute.
            args: Arguments to pass to the process.
            cwd: The working directory of the process.
            clear_env: Clear environment variables from parent process.
            env: Environment variables to pass to the subprocess.
            signal: An abort signal to cancel the process.
            stdin: How stdin of the spawned process should be handled.
            stdout: How stdout of the spawned process should be handled.
            stderr: How stderr of the spawned process should be handled.
            stdin_data: Data to write to stdin of the process.
        """
        async_child = self._bridge.run(
            self._async.spawn(
                command,
                args=args,
                cwd=cwd,
                clear_env=clear_env,
                env=env,
                signal=signal,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                stdin_data=stdin_data,
            )
        )
        return ChildProcess(self._rpc, self._bridge, async_child)

    def fetch(
        self,
        url: str,
        *,
        method: Optional[str] = "GET",
        headers: Optional[dict[str, str]] = None,
        redirect: Optional[Literal["follow", "manual"]] = None,
    ) -> FetchResponse:
        async_response = self._bridge.run(
            self._rpc.fetch(url, method, headers, redirect, None)
        )
        return FetchResponse(async_response)

    def close(self) -> None:
        self._bridge.run(self._async.close())

    def kill(self) -> None:
        self._bridge.run(self._async.kill())

    def extend_timeout(self, additional_s: int) -> datetime:
        """Request to extend the timeout of the sandbox by the specified duration.
        You can at max extend timeout of a sandbox by 30 minutes at once.

        Please note the extension is not guranteed to be the same as requested time.
        You should rely on the returned Date value to know the exact extension time.
        """
        return self._bridge.run(self._async.extend_timeout(additional_s))

    def expose_http(
        self, *, port: Optional[int] = None, pid: Optional[int] = None
    ) -> str:
        """Publicly expose a HTTP service via a publicly routeable URL.

        NOTE: when you call this API, the target HTTP service will be PUBLICLY
        EXPOSED WITHOUT AUTHENTICATION. Anyone with knowledge of the public domain
        will be able to send arbitrary requests to the exposed service.

        An exposed service can either be a service listening on an arbitrary HTTP
        port, or a JavaScript runtime that can handle HTTP requests.
        """
        return self._bridge.run(self._async.expose_http(port=port, pid=pid))

    def expose_ssh(self) -> ExposeSSHResult:
        """Expose an isolate over SSH, allowing access to the isolate's shell.

        NOTE: The SSH connection is authenticated through the 'username' field. This field is populated
        with a randomly generated, unique identifier. Anyone with knowledge of the 'username' can
        connect to the isolate's shell without further authentication.
        """
        return self._bridge.run(self._async.expose_ssh())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._bridge.run(self._async.__aexit__(exc_type, exc_val, exc_tb))
