import uuid

import pytest
import pytest_asyncio

from novita_sandbox.core import AsyncSandbox, AsyncVolume, NotFoundException

pytestmark = pytest.mark.skip("Volume lifecycle tests require enabled volume creation")


def volume_name():
    return f"vol-{uuid.uuid4().hex[:8]}"


@pytest_asyncio.fixture
async def async_volume():
    """Create an async volume for the test and destroy it afterwards."""
    vol = await AsyncVolume.create(volume_name())
    try:
        yield vol
    finally:
        await AsyncVolume.destroy(vol.volume_id)


@pytest_asyncio.fixture
async def mounted_async_volume(volume_template):
    """Create an async volume mounted into a sandbox and clean both up."""
    vol = await AsyncVolume.create(volume_name())
    sbx = await AsyncSandbox.create(
        volume_template, timeout=60, volume_mounts={"/mnt/vol": vol}
    )
    try:
        yield vol, sbx
    finally:
        try:
            await sbx.kill()
        finally:
            await AsyncVolume.destroy(vol.volume_id)


# ── Volume lifecycle ──────────────────────────────────────────────


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_create():
    name = volume_name()
    vol = await AsyncVolume.create(name)

    assert vol.volume_id is not None
    assert vol.name == name
    assert vol.token is not None

    await AsyncVolume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_create_with_quotas():
    name = volume_name()
    vol = await AsyncVolume.create(name, quota_size_gib=10, quota_inodes=1000)

    info = await AsyncVolume.get_info(vol.volume_id)
    assert info.quota_size_gib == 10
    assert info.quota_inodes == 1000

    await AsyncVolume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_connect(async_volume):
    connected = await AsyncVolume.connect(async_volume.volume_id)
    assert connected.volume_id == async_volume.volume_id
    assert connected.name == async_volume.name
    assert connected.token is not None


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_get_info(async_volume):
    info = await AsyncVolume.get_info(async_volume.volume_id)
    assert info.volume_id == async_volume.volume_id
    assert info.name == async_volume.name
    assert info.token is not None
    assert isinstance(info.quota_size_gib, int)


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_get_info_nonexistent():
    with pytest.raises(NotFoundException):
        await AsyncVolume.get_info(str(uuid.uuid4()))


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_list_includes_created(async_volume):
    volumes = await AsyncVolume.list()
    found = [v for v in volumes if v.volume_id == async_volume.volume_id]
    assert len(found) == 1
    assert found[0].name == async_volume.name


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_update_quota_size_gib():
    name = volume_name()
    vol = await AsyncVolume.create(name, quota_size_gib=5)

    updated = await AsyncVolume.update_quota(vol.volume_id, quota_size_gib=20)
    assert updated.quota_size_gib == 20

    await AsyncVolume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_update_quota_inodes():
    name = volume_name()
    vol = await AsyncVolume.create(name, quota_inodes=500)

    updated = await AsyncVolume.update_quota(vol.volume_id, quota_inodes=2000)
    assert updated.quota_inodes == 2000

    await AsyncVolume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_destroy_returns_true():
    name = volume_name()
    vol = await AsyncVolume.create(name)

    result = await AsyncVolume.destroy(vol.volume_id)
    assert result is True


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_destroy_already_destroyed_returns_false():
    name = volume_name()
    vol = await AsyncVolume.create(name)
    await AsyncVolume.destroy(vol.volume_id)

    result = await AsyncVolume.destroy(vol.volume_id)
    assert result is False


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_destroy_mounted_volume_raises_error(volume_template):
    name = volume_name()
    vol = await AsyncVolume.create(name)
    sbx = await AsyncSandbox.create(
        volume_template, timeout=60, volume_mounts={"/mnt/vol": vol}
    )

    try:
        with pytest.raises(Exception):
            await AsyncVolume.destroy(vol.volume_id)
    finally:
        try:
            await sbx.kill()
        finally:
            await AsyncVolume.destroy(vol.volume_id)


# ── Mounted volume content ───────────────────────────────────────


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_create_directory_in_mounted_volume(mounted_async_volume):
    _, sbx = mounted_async_volume
    await sbx.commands.run("mkdir -p /mnt/vol/test-dir")
    result = await sbx.commands.run("test -d /mnt/vol/test-dir && echo ok")
    assert "ok" in result.stdout


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_create_nested_directory_in_mounted_volume(mounted_async_volume):
    _, sbx = mounted_async_volume
    await sbx.commands.run("mkdir -p /mnt/vol/a/b/c")
    result = await sbx.commands.run("test -d /mnt/vol/a/b/c && echo ok")
    assert "ok" in result.stdout


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_write_read_text_in_mounted_volume(mounted_async_volume):
    _, sbx = mounted_async_volume
    await sbx.commands.run('echo "hello volume world" > /mnt/vol/hello.txt')
    result = await sbx.commands.run("cat /mnt/vol/hello.txt")
    assert "hello volume world" in result.stdout


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_write_read_binary_in_mounted_volume(mounted_async_volume):
    _, sbx = mounted_async_volume
    await sbx.commands.run('printf "\\x00\\x01\\x02\\xff" > /mnt/vol/binary.bin')
    result = await sbx.commands.run("wc -c < /mnt/vol/binary.bin")
    assert result.stdout.strip() == "4"


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_list_directory_contents_in_mounted_volume(mounted_async_volume):
    _, sbx = mounted_async_volume
    await sbx.commands.run("mkdir -p /mnt/vol/list-test/a /mnt/vol/list-test/b")
    result = await sbx.commands.run("ls /mnt/vol/list-test | sort")
    assert result.stdout.strip().split("\n") == ["a", "b"]


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_remove_file_in_mounted_volume(mounted_async_volume):
    _, sbx = mounted_async_volume
    await sbx.commands.run("echo bye > /mnt/vol/to-remove.txt")
    await sbx.commands.run("rm /mnt/vol/to-remove.txt")
    result = await sbx.commands.run("test ! -e /mnt/vol/to-remove.txt && echo ok")
    assert "ok" in result.stdout


# ── Volume + Sandbox integration ─────────────────────────────────


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_sandbox_with_premounted_volume(volume_template):
    name = volume_name()
    vol = await AsyncVolume.create(name)
    try:
        sbx = await AsyncSandbox.create(
            volume_template, timeout=60, volume_mounts={"/mnt/vol": vol}
        )
        try:
            assert await sbx.is_running()
        finally:
            await sbx.kill()
    finally:
        await AsyncVolume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_premounted_volume_content_accessible(volume_template):
    name = volume_name()
    vol = await AsyncVolume.create(name)
    try:
        sbx = await AsyncSandbox.create(
            volume_template, timeout=60, volume_mounts={"/mnt/vol": vol}
        )
        try:
            await sbx.commands.run("mkdir -p /mnt/vol/data")
            await sbx.commands.run('echo "hello from volume" > /mnt/vol/data/hello.txt')
            result = await sbx.commands.run("cat /mnt/vol/data/hello.txt")
            assert "hello from volume" in result.stdout
        finally:
            await sbx.kill()
    finally:
        await AsyncVolume.destroy(vol.volume_id)
