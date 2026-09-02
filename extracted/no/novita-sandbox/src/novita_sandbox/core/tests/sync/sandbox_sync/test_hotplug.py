import pytest
from packaging.version import Version

from novita_sandbox.core import Sandbox
from novita_sandbox.core.connection_config import ConnectionConfig
from novita_sandbox.core.exceptions import NotFoundException


@pytest.mark.skip_debug()
def test_hotplug_memory_basic(template):
    sbx = Sandbox.create(template, timeout=300)
    try:
        sbx.hotplug_memory(256)
        info = sbx.get_info()
        assert info.sandbox_id == sbx.sandbox_id
    finally:
        sbx.kill()


@pytest.mark.skip_debug()
def test_hotplug_memory_unplug_all(template):
    sbx = Sandbox.create(template, timeout=300)
    try:
        sbx.hotplug_memory(512)
        sbx.hotplug_memory(0)
        info = sbx.get_info()
        assert info.sandbox_id == sbx.sandbox_id
    finally:
        sbx.kill()


@pytest.mark.skip_debug()
def test_hotplug_memory_not_found():
    sbx = Sandbox(
        sandbox_id="nonexistent-id",
        envd_version=Version("0.1.0"),
        envd_access_token=None,
        sandbox_domain=None,
        connection_config=ConnectionConfig(),
    )

    with pytest.raises(NotFoundException):
        sbx.hotplug_memory(256)
