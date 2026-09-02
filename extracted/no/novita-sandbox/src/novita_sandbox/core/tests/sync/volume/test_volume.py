import uuid

import pytest

from novita_sandbox.core import NotFoundException, Sandbox, Volume

pytestmark = pytest.mark.skip("Volume lifecycle tests require enabled volume creation")


def volume_name():
    return f"vol-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def volume():
    """Create a volume for the test and destroy it afterwards."""
    vol = Volume.create(volume_name())
    try:
        yield vol
    finally:
        Volume.destroy(vol.volume_id)


@pytest.fixture
def mounted_volume(volume_template):
    """Create a volume mounted into a sandbox and clean both up."""
    vol = Volume.create(volume_name())
    sbx = Sandbox.create(volume_template, timeout=60, volume_mounts={"/mnt/vol": vol})
    try:
        yield vol, sbx
    finally:
        try:
            sbx.kill()
        finally:
            Volume.destroy(vol.volume_id)


# ── Volume lifecycle ──────────────────────────────────────────────


@pytest.mark.skip_debug()
def test_create():
    name = volume_name()
    vol = Volume.create(name)

    assert vol.volume_id is not None
    assert vol.name == name
    assert vol.token is not None

    Volume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
def test_create_with_quotas():
    name = volume_name()
    vol = Volume.create(name, quota_size_gib=10, quota_inodes=1000)

    info = Volume.get_info(vol.volume_id)
    assert info.quota_size_gib == 10
    assert info.quota_inodes == 1000

    Volume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
def test_connect(volume):
    connected = Volume.connect(volume.volume_id)
    assert connected.volume_id == volume.volume_id
    assert connected.name == volume.name
    assert connected.token is not None


@pytest.mark.skip_debug()
def test_get_info(volume):
    info = Volume.get_info(volume.volume_id)
    assert info.volume_id == volume.volume_id
    assert info.name == volume.name
    assert info.token is not None
    assert isinstance(info.quota_size_gib, int)


@pytest.mark.skip_debug()
def test_get_info_nonexistent():
    with pytest.raises(NotFoundException):
        Volume.get_info(str(uuid.uuid4()))


@pytest.mark.skip_debug()
def test_list_includes_created(volume):
    volumes = Volume.list()
    found = [v for v in volumes if v.volume_id == volume.volume_id]
    assert len(found) == 1
    assert found[0].name == volume.name


@pytest.mark.skip_debug()
def test_update_quota_size_gib():
    name = volume_name()
    vol = Volume.create(name, quota_size_gib=5)

    updated = Volume.update_quota(vol.volume_id, quota_size_gib=20)
    assert updated.quota_size_gib == 20

    Volume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
def test_update_quota_inodes():
    name = volume_name()
    vol = Volume.create(name, quota_inodes=500)

    updated = Volume.update_quota(vol.volume_id, quota_inodes=2000)
    assert updated.quota_inodes == 2000

    Volume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
def test_destroy_returns_true():
    name = volume_name()
    vol = Volume.create(name)

    result = Volume.destroy(vol.volume_id)
    assert result is True


@pytest.mark.skip_debug()
def test_destroy_already_destroyed_returns_false():
    name = volume_name()
    vol = Volume.create(name)
    Volume.destroy(vol.volume_id)

    result = Volume.destroy(vol.volume_id)
    assert result is False


@pytest.mark.skip_debug()
def test_destroy_mounted_volume_raises_error(volume_template):
    name = volume_name()
    vol = Volume.create(name)
    sbx = Sandbox.create(volume_template, timeout=60, volume_mounts={"/mnt/vol": vol})

    try:
        with pytest.raises(Exception):
            Volume.destroy(vol.volume_id)
    finally:
        try:
            sbx.kill()
        finally:
            Volume.destroy(vol.volume_id)


# ── Mounted volume content ───────────────────────────────────────


@pytest.mark.skip_debug()
def test_create_directory_in_mounted_volume(mounted_volume):
    _, sbx = mounted_volume
    sbx.commands.run("mkdir -p /mnt/vol/test-dir")
    result = sbx.commands.run("test -d /mnt/vol/test-dir && echo ok")
    assert "ok" in result.stdout


@pytest.mark.skip_debug()
def test_create_nested_directory_in_mounted_volume(mounted_volume):
    _, sbx = mounted_volume
    sbx.commands.run("mkdir -p /mnt/vol/a/b/c")
    result = sbx.commands.run("test -d /mnt/vol/a/b/c && echo ok")
    assert "ok" in result.stdout


@pytest.mark.skip_debug()
def test_write_read_text_in_mounted_volume(mounted_volume):
    _, sbx = mounted_volume
    sbx.commands.run('echo "hello volume world" > /mnt/vol/hello.txt')
    result = sbx.commands.run("cat /mnt/vol/hello.txt")
    assert "hello volume world" in result.stdout


@pytest.mark.skip_debug()
def test_write_read_binary_in_mounted_volume(mounted_volume):
    _, sbx = mounted_volume
    sbx.commands.run('printf "\\x00\\x01\\x02\\xff" > /mnt/vol/binary.bin')
    result = sbx.commands.run("wc -c < /mnt/vol/binary.bin")
    assert result.stdout.strip() == "4"


@pytest.mark.skip_debug()
def test_list_directory_contents_in_mounted_volume(mounted_volume):
    _, sbx = mounted_volume
    sbx.commands.run("mkdir -p /mnt/vol/list-test/a /mnt/vol/list-test/b")
    result = sbx.commands.run("ls /mnt/vol/list-test | sort")
    assert result.stdout.strip().split("\n") == ["a", "b"]


@pytest.mark.skip_debug()
def test_remove_file_in_mounted_volume(mounted_volume):
    _, sbx = mounted_volume
    sbx.commands.run("echo bye > /mnt/vol/to-remove.txt")
    sbx.commands.run("rm /mnt/vol/to-remove.txt")
    result = sbx.commands.run("test ! -e /mnt/vol/to-remove.txt && echo ok")
    assert "ok" in result.stdout


# ── Volume + Sandbox integration ─────────────────────────────────


@pytest.mark.skip_debug()
def test_sandbox_with_premounted_volume(volume_template):
    name = volume_name()
    vol = Volume.create(name)
    try:
        sbx = Sandbox.create(volume_template, timeout=60, volume_mounts={"/mnt/vol": vol})
        try:
            assert sbx.is_running()
        finally:
            sbx.kill()
    finally:
        Volume.destroy(vol.volume_id)


@pytest.mark.skip_debug()
def test_premounted_volume_content_accessible(volume_template):
    name = volume_name()
    vol = Volume.create(name)
    try:
        sbx = Sandbox.create(volume_template, timeout=60, volume_mounts={"/mnt/vol": vol})
        try:
            sbx.commands.run("mkdir -p /mnt/vol/data")
            sbx.commands.run('echo "hello from volume" > /mnt/vol/data/hello.txt')
            result = sbx.commands.run("cat /mnt/vol/data/hello.txt")
            assert "hello from volume" in result.stdout
        finally:
            sbx.kill()
    finally:
        Volume.destroy(vol.volume_id)
