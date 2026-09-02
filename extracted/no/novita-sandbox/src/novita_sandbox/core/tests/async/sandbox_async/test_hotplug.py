import pytest

from novita_sandbox.core import AsyncSandbox
from novita_sandbox.core.exceptions import NotFoundException


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_hotplug_memory_basic(template):
    sbx = await AsyncSandbox.create(template, timeout=300)
    try:
        await sbx.hotplug_memory(256)
        info = await sbx.get_info()
        assert info.sandbox_id == sbx.sandbox_id
    finally:
        await sbx.kill()


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_hotplug_memory_unplug_all(template):
    sbx = await AsyncSandbox.create(template, timeout=300)
    try:
        await sbx.hotplug_memory(512)
        await sbx.hotplug_memory(0)
        info = await sbx.get_info()
        assert info.sandbox_id == sbx.sandbox_id
    finally:
        await sbx.kill()
