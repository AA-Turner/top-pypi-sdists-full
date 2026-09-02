"""Cross-language protocol and fallback coverage for the native hook shim."""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass
from functools import partial
from pathlib import Path

import anyio
import pytest

from runlayer_cli import regex_safe as re
from runlayer_cli.daemon import server
from runlayer_cli.hook import daemon_client, daemon_protocol, hook_io
from tests.daemon_frame_helpers import read_frame, write_frame

pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason="Unix-socket cross-language tests; Windows cross-build runs in Go CI",
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SHIM_ROOT = _REPO_ROOT / "aiwatch-hook-shim"
_CLIENT_ARGS = ("--client", "claude_code")


@dataclass(frozen=True)
class BuiltShims:
    current: Path
    skewed: Path


@pytest.fixture(scope="session")
def built_hook_shims(tmp_path_factory: pytest.TempPathFactory) -> BuiltShims:
    go = shutil.which("go")
    if go is None:
        pytest.skip("Go toolchain is unavailable")
    version_output = subprocess.run(
        [go, "version"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout
    match = re.search(r"\bgo(\d+)\.(\d+)\.(\d+)\b", version_output)
    if match is None or tuple(map(int, match.groups())) < (1, 26, 6):
        pytest.skip("Go 1.26.6+ is required to build the hook shim")

    output_root = tmp_path_factory.mktemp("hook-shim")
    current = output_root / "current" / "aiwatch-hook"
    skewed = output_root / "skewed" / "aiwatch-hook"
    for output, version in (
        (current, daemon_protocol.protocol_version()),
        (skewed, "cross-language-version-skew"),
    ):
        output.parent.mkdir()
        subprocess.run(
            [
                go,
                "build",
                "-trimpath",
                "-ldflags",
                f"-X main.version={version}",
                "-o",
                str(output),
                "./cmd/aiwatch-hook",
            ],
            cwd=_SHIM_ROOT,
            env={**os.environ, "GOTOOLCHAIN": "local"},
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        fallback = output.parent / "aiwatch"
        fallback.write_text(
            "#!/bin/sh\n"
            '[ "$SHIM_FALLBACK_SENTINEL" = "present" ] || exit 9\n'
            'printf "fallback-argv=%s\\n" "$*" >&2\n'
            "cat\n"
            "exit 2\n"
        )
        fallback.chmod(0o755)
    return BuiltShims(current=current, skewed=skewed)


@pytest.fixture
def endpoint() -> Iterator[Path]:
    # Darwin limits AF_UNIX paths to 103 bytes; pytest's tmp path can exceed it.
    with tempfile.TemporaryDirectory(prefix="rl-shim-", dir="/tmp") as directory:
        yield Path(directory) / "daemon.sock"


def _process_environment(endpoint: Path) -> tuple[dict[str, str], dict[str, str]]:
    expected = {
        name: f"shim-value-{index}"
        for index, name in enumerate(sorted(daemon_protocol.HOOK_ENV_ALLOWLIST))
    }
    environment = os.environ.copy()
    for name in daemon_protocol.HOOK_ENV_ALLOWLIST:
        environment.pop(name, None)
    environment.update(expected)
    environment[daemon_protocol.DAEMON_ENDPOINT_ENV] = str(endpoint)
    environment["RUNLAYER_API_KEY"] = "must-not-cross-ipc"
    environment["SHIM_FALLBACK_SENTINEL"] = "present"
    return environment, expected


def _python_request(
    shim: Path,
    *,
    stdin: str,
    cwd: Path,
    environment: dict[str, str],
) -> daemon_protocol.HookRequest:
    return {
        "version": daemon_protocol.protocol_version(),
        "argv": [str(shim.with_name("aiwatch")), *_CLIENT_ARGS],
        "cwd": str(cwd),
        "env": environment,
        "stdin": stdin,
    }


async def _run_shim(
    binary: Path,
    *,
    stdin: str,
    cwd: Path,
    environment: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    return await anyio.to_thread.run_sync(
        partial(
            subprocess.run,
            [str(binary), "hook", *_CLIENT_ARGS],
            input=stdin,
            text=True,
            capture_output=True,
            cwd=cwd,
            env=environment,
            check=False,
            timeout=10,
        )
    )


@pytest.mark.parametrize(
    ("case", "expected_stdout", "expected_stderr", "expected_exit"),
    [
        ("allow", '{"permission":"allow"}', "", 0),
        (
            "deny",
            '{"hookSpecificOutput":{"permissionDecision":"deny"}}',
            "",
            0,
        ),
        ("fail_closed", "", "AI Watch denied the request.\n", 2),
    ],
)
@pytest.mark.asyncio
async def test_shim_matches_python_client_against_live_daemon(
    built_hook_shims: BuiltShims,
    endpoint: Path,
    tmp_path: Path,
    case: str,
    expected_stdout: str,
    expected_stderr: str,
    expected_exit: int,
) -> None:
    ready = anyio.Event()
    process_environment, request_environment = _process_environment(endpoint)
    stdin = json.dumps({"case": case}, separators=(",", ":"))

    def run_hook() -> None:
        current_case = json.loads(hook_io.read_stdin())["case"]
        if current_case == "allow":
            hook_io.write_stdout('{"permission":"allow"}')
        elif current_case == "deny":
            hook_io.write_stdout('{"hookSpecificOutput":{"permissionDecision":"deny"}}')
        else:
            hook_io.write_stderr("AI Watch denied the request.\n")
            raise SystemExit(2)

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=run_hook,
            )
        )
        await ready.wait()
        try:
            python_response = await anyio.to_thread.run_sync(
                daemon_client._send_unix_request,  # noqa: SLF001
                str(endpoint),
                _python_request(
                    built_hook_shims.current,
                    stdin=stdin,
                    cwd=tmp_path,
                    environment=request_environment,
                ),
            )
            shim_response = await _run_shim(
                built_hook_shims.current,
                stdin=stdin,
                cwd=tmp_path,
                environment=process_environment,
            )
        finally:
            tasks.cancel_scope.cancel()

    parsed = daemon_protocol.parse_hook_response(python_response)
    assert "status" not in parsed
    assert shim_response.stdout == parsed["stdout"] == expected_stdout
    assert shim_response.stderr == parsed["stderr"] == expected_stderr
    assert shim_response.returncode == parsed["exit_code"] == expected_exit


@pytest.mark.asyncio
async def test_shim_environment_matches_python_allowlist(
    built_hook_shims: BuiltShims,
    endpoint: Path,
    tmp_path: Path,
) -> None:
    ready = anyio.Event()
    process_environment, expected_environment = _process_environment(endpoint)

    def report_environment() -> None:
        context = hook_io._hook_io.get()  # noqa: SLF001
        assert context is not None
        hook_io.write_stdout(json.dumps(dict(context.env), sort_keys=True))

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=report_environment,
            )
        )
        await ready.wait()
        try:
            response = await _run_shim(
                built_hook_shims.current,
                stdin="{}",
                cwd=tmp_path,
                environment=process_environment,
            )
        finally:
            tasks.cancel_scope.cancel()

    assert response.returncode == 0
    assert response.stderr == ""
    assert json.loads(response.stdout) == expected_environment
    assert "RUNLAYER_API_KEY" not in response.stdout


@pytest.mark.asyncio
async def test_shim_start_stamp_reaches_daemon_hook_context(
    built_hook_shims: BuiltShims,
    endpoint: Path,
    tmp_path: Path,
) -> None:
    ready = anyio.Event()
    process_environment, _ = _process_environment(endpoint)
    before = int(time.time() * 1000)

    def report_stamp() -> None:
        hook_io.write_stdout(json.dumps({"client_start_ms": hook_io.client_start_ms()}))

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=report_stamp,
            )
        )
        await ready.wait()
        try:
            response = await _run_shim(
                built_hook_shims.current,
                stdin="{}",
                cwd=tmp_path,
                environment=process_environment,
            )
        finally:
            tasks.cancel_scope.cancel()

    assert response.returncode == 0
    stamp = json.loads(response.stdout)["client_start_ms"]
    assert before <= stamp <= int(time.time() * 1000)


@pytest.mark.asyncio
async def test_dead_socket_fallback_child_receives_start_stamp(
    built_hook_shims: BuiltShims,
    endpoint: Path,
    tmp_path: Path,
) -> None:
    # Own shim directory: the shared fixture's fallback script asserts exact
    # stderr, so this test pairs a copied shim with a stamp-echoing fallback.
    shim_directory = tmp_path / "stamp-shim"
    shim_directory.mkdir()
    shim = shim_directory / "aiwatch-hook"
    shutil.copy2(built_hook_shims.current, shim)
    fallback = shim_directory / "aiwatch"
    fallback.write_text('#!/bin/sh\nprintf "%s" "$RUNLAYER_HOOK_CLIENT_START_MS"\n')
    fallback.chmod(0o755)
    process_environment, _ = _process_environment(endpoint)
    before = int(time.time() * 1000)

    response = await _run_shim(
        shim,
        stdin='{"case":"dead-socket"}',
        cwd=tmp_path,
        environment=process_environment,
    )

    assert response.returncode == 0
    assert before <= int(response.stdout) <= int(time.time() * 1000)


@pytest.mark.asyncio
async def test_restarting_live_daemon_execs_python_fallback(
    built_hook_shims: BuiltShims,
    endpoint: Path,
    tmp_path: Path,
) -> None:
    ready = anyio.Event()
    process_environment, _ = _process_environment(endpoint)
    payload = '{"case":"restarting"}'

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=lambda: pytest.fail("version-skew hook dispatched"),
            )
        )
        await ready.wait()
        response = await _run_shim(
            built_hook_shims.skewed,
            stdin=payload,
            cwd=tmp_path,
            environment=process_environment,
        )

    assert response.returncode == 2
    assert response.stdout == payload
    assert response.stderr == "fallback-argv=hook --client claude_code\n"


@pytest.mark.asyncio
async def test_dead_socket_execs_python_fallback(
    built_hook_shims: BuiltShims,
    endpoint: Path,
    tmp_path: Path,
) -> None:
    process_environment, _ = _process_environment(endpoint)
    payload = '{"case":"dead-socket"}'

    response = await _run_shim(
        built_hook_shims.current,
        stdin=payload,
        cwd=tmp_path,
        environment=process_environment,
    )

    assert response.returncode == 2
    assert response.stdout == payload
    assert response.stderr == "fallback-argv=hook --client claude_code\n"


def _start_accept_then_close_server(endpoint: Path) -> threading.Thread:
    ready = threading.Event()

    def serve() -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
            listener.settimeout(10)
            listener.bind(str(endpoint))
            listener.listen()
            ready.set()
            connection, _ = listener.accept()
            with connection, connection.makefile("rwb", buffering=0) as stream:
                read_frame(stream)
                write_frame(stream, {"status": "accepted"})
                assert stream.read(1) == daemon_protocol.REQUEST_ACCEPTED_ACK

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    assert ready.wait(timeout=5)
    return thread


@pytest.mark.asyncio
async def test_post_ack_disconnect_fails_closed_without_replay(
    built_hook_shims: BuiltShims,
    endpoint: Path,
    tmp_path: Path,
) -> None:
    process_environment, _ = _process_environment(endpoint)
    thread = _start_accept_then_close_server(endpoint)

    response = await _run_shim(
        built_hook_shims.current,
        stdin='{"case":"post-ack"}',
        cwd=tmp_path,
        environment=process_environment,
    )
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert response.returncode == 2
    assert response.stdout == ""
    assert (
        response.stderr == "AI Watch daemon stopped before returning a hook result.\n"
    )
