"""Opt-in real-runtime validation for the SDK API and bundled Harbor adapter."""

import asyncio
import os
import uuid

import pytest

from runta import AsyncRunta, CommandError, Runta

pytestmark = pytest.mark.skipif(
    os.getenv("RUNTA_PYTEST_LIVE") != "1"
    or not os.getenv("RUNTA_TOKEN")
    or not os.getenv("RUNTA_ENDPOINT"),
    reason="pass --live with RUNTA_ENDPOINT and RUNTA_TOKEN",
)


async def delete_and_wait(client, runtime):
    await runtime.delete()
    deadline = asyncio.get_running_loop().time() + 60
    while runtime.id in {info.id for info in await client.runtimes.list()}:
        if asyncio.get_running_loop().time() >= deadline:
            pytest.fail(f"runtime deletion did not converge: {runtime.id}")
        await asyncio.sleep(0.5)


@pytest.mark.asyncio
async def test_directory_contents_real_runtime(tmp_path):
    async with AsyncRunta(timeout=60, retry_max_attempts=2) as client:
        runtime = await client.runtimes.create(
            f"sdk-dir-contents-{uuid.uuid4().hex[:12]}",
            vcpus=1,
            memory_mib=1024,
        )
        try:
            setup = await runtime.exec(
                [
                    "sh",
                    "-c",
                    "mkdir -p /tmp/source/nested /tmp/empty; "
                    "printf payload >/tmp/source/nested/data; "
                    "printf new >/tmp/source/replace; "
                    "ln -s nested/data /tmp/source/sym; "
                    "ln /tmp/source/nested/data /tmp/source/hard; "
                    "ln -s /tmp/source /tmp/source-link; "
                    "chmod 755 /tmp/source/replace",
                ]
            )
            assert setup.exit_code == 0, setup.stderr_text

            def prepare(name):
                target = tmp_path / name
                target.mkdir()
                (target / "keep").write_text("keep")
                if name == "sync":
                    os.link(target / "keep", target / "replace")
                else:
                    (target / "replace").symlink_to("keep")
                return target

            def verify(target):
                assert (target / "keep").read_text() == "keep"
                assert (target / "replace").read_text() == "new"
                assert (target / "nested/data").read_text() == "payload"
                assert (target / "sym").read_text() == "payload"
                assert (target / "hard").read_text() == "payload"
                assert not (target / "source").exists()
                assert not (target / "replace").is_symlink()
                assert not os.path.samefile(target / "keep", target / "replace")

            target = prepare("async")
            await runtime.files.download_dir_contents("/tmp/source-link", str(target))
            verify(target)
            await runtime.files.download_dir_contents("/tmp/empty", str(target))
            verify(target)
            with pytest.raises(CommandError):
                await runtime.files.download_dir_contents(
                    "/tmp/source/replace", str(target)
                )
            verify(target)

            target = prepare("sync")

            def sync_download():
                with Runta(timeout=60, retry_max_attempts=2) as sync_client:
                    sync_runtime = sync_client.runtimes.get(runtime.id)
                    sync_runtime.files.download_dir_contents(
                        "/tmp/source-link", str(target)
                    )

            await asyncio.to_thread(sync_download)
            verify(target)
        finally:
            await delete_and_wait(client, runtime)


@pytest.mark.asyncio
async def test_harbor_directory_contents_real_runtime(tmp_path):
    pytest.importorskip("harbor")
    from runta_harbor.environment import RuntaEnvironment

    async with AsyncRunta(timeout=60, retry_max_attempts=2) as client:
        runtime = await client.runtimes.create(
            f"sdk-harbor-contents-{uuid.uuid4().hex[:12]}",
            vcpus=1,
            memory_mib=1024,
        )
        try:
            result = await runtime.exec(
                [
                    "sh",
                    "-c",
                    "mkdir -p /tmp/source; printf new >/tmp/source/data; mkfifo /tmp/source/fifo",
                ]
            )
            assert result.exit_code == 0, result.stderr_text
            env = object.__new__(RuntaEnvironment)
            env._runtime = runtime
            (tmp_path / "keep").write_text("keep")
            await env._runtime_download_dir("/tmp/source", tmp_path)
            assert (tmp_path / "data").read_text() == "new"
            assert (tmp_path / "keep").read_text() == "keep"
            assert not (tmp_path / "fifo").exists()
        finally:
            await delete_and_wait(client, runtime)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.asyncio
async def test_selected_directory_contents_real_runtime(tmp_path, asynchronous):
    async with AsyncRunta(timeout=60, retry_max_attempts=2) as client:
        runtime = await client.runtimes.create(
            f"sdk-selected-contents-{uuid.uuid4().hex[:12]}",
            vcpus=1,
            memory_mib=1024,
        )
        try:
            setup = await runtime.exec(
                [
                    "sh",
                    "-c",
                    "mkdir -p /tmp/selected/nested; "
                    "printf log >/tmp/selected/agent.log; "
                    "printf result >/tmp/selected/nested/result.json; "
                    "printf excluded >/tmp/selected/nested/excluded; "
                    "ln /tmp/selected/agent.log /tmp/selected/hard; "
                    "ln -s nested/result.json /tmp/selected/sym; "
                    "ln -s /tmp/selected /tmp/selected-source-link",
                ]
            )
            assert setup.exit_code == 0, setup.stderr_text
            target = tmp_path / "target"
            target.mkdir()
            (target / "keep").write_text("keep")
            (target / "agent.log").write_text("old")
            paths = ["nested", "nested/result.json", "agent.log", "hard", "sym"]
            if asynchronous:
                await runtime.files.download_dir_contents(
                    "/tmp/selected-source-link", str(target), paths=paths
                )
                with pytest.raises(CommandError):
                    await runtime.files.download_dir_contents(
                        "/tmp/selected", str(target), paths=["absent"]
                    )
                await runtime.files.download_dir_contents(
                    "/absent", str(tmp_path / "empty-target"), paths=[]
                )
            else:

                def download():
                    with Runta(timeout=60, retry_max_attempts=2) as sync_client:
                        files = sync_client.runtimes.get(runtime.id).files
                        files.download_dir_contents(
                            "/tmp/selected-source-link", str(target), paths=paths
                        )
                        with pytest.raises(CommandError):
                            files.download_dir_contents(
                                "/tmp/selected", str(target), paths=["absent"]
                            )
                        files.download_dir_contents(
                            "/absent", str(tmp_path / "empty-target"), paths=[]
                        )

                await asyncio.to_thread(download)
            assert (target / "agent.log").read_text() == "log"
            assert (target / "hard").read_text() == "log"
            assert (target / "nested/result.json").read_text() == "result"
            assert (target / "keep").read_text() == "keep"
            assert not (target / "nested/excluded").exists()
            assert not (target / "sym").exists()
            assert not (tmp_path / "empty-target").exists()
        finally:
            await delete_and_wait(client, runtime)
