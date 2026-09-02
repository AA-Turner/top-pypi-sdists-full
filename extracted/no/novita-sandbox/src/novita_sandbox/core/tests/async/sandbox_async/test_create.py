import pytest
import time

from novita_sandbox.core import AsyncSandbox, SandboxQuery, SandboxState


@pytest.mark.skip_debug()
async def test_start(template):
    sbx = await AsyncSandbox.create(template, timeout=30)
    try:
        assert await sbx.is_running()
        assert sbx._envd_version is not None
    finally:
        await sbx.kill()

@pytest.mark.skip_debug()
async def test_start_with_node_id(template, node_id):
    sbx = await AsyncSandbox.create(template, timeout=30, node_id=node_id)
    try:
        assert await sbx.is_running()
        assert sbx.sandbox_id is not None
    finally:
        await sbx.kill()


@pytest.mark.skip_debug()
async def test_start_with_auto_pause(template):
    sbx = await AsyncSandbox.create(template, timeout=3, auto_pause=True, metadata={"test-auto-pause": "1"})
    sandbox_id = sbx.sandbox_id.split("-")[0]
    # wait for the sandbox to auto pause
    time.sleep(5)
    try:
        paginator = AsyncSandbox.list(
            query=SandboxQuery(state=[SandboxState.PAUSED], metadata={"test-auto-pause": "1"})
        )
        sandboxes = await paginator.next_items()
        exists = any(s.sandbox_id.startswith(sandbox_id) for s in sandboxes)
        assert exists
    finally:
        await sbx.kill()


@pytest.mark.skip_debug()
async def test_metadata(template):
    sbx = await AsyncSandbox.create(
        template, timeout=30, metadata={"test-key": "test-value"}
    )

    try:
        paginator = AsyncSandbox.list(
            query=SandboxQuery(metadata={"test-key": "test-value"})
        )
        sandboxes = await paginator.next_items()

        for sbx_info in sandboxes:
            if sbx.sandbox_id == sbx_info.sandbox_id:
                assert sbx_info.metadata is not None
                assert sbx_info.metadata["test-key"] == "test-value"
                break
        else:
            assert False, "Sandbox not found"
    finally:
        await sbx.kill()
