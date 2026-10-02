"""Which storage outlives the job: the per-file call output capture makes.

The mount table is injected; nothing here reads the real machine's mounts.
"""

from __future__ import annotations


import pytest

from probe.sdk import ephemeral


@pytest.fixture(autouse=True)
def _clean_machine(monkeypatch):
    for name in (*ephemeral.MACHINE_MARKERS, "CI", ephemeral.ENV):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(ephemeral, "_CONTAINER_FILES", ())
    monkeypatch.setattr(ephemeral, "_realpath", lambda p: str(p))


def _mounts(monkeypatch, *pairs):
    ordered = tuple(sorted(pairs, key=lambda m: len(m[0]), reverse=True))
    monkeypatch.setattr(ephemeral, "_mounts", lambda: ordered)


def test_a_laptop_disk_lasts(monkeypatch):
    _mounts(monkeypatch, ("/", "ext4"))
    assert ephemeral.storage_is_durable("/home/me/run/ckpt.pt")


@pytest.mark.parametrize("fstype", ["overlay", "tmpfs", "ramfs"])
def test_the_containers_own_layer_and_ram_are_throwaway(monkeypatch, fstype):
    _mounts(monkeypatch, ("/", fstype))
    assert not ephemeral.storage_is_durable("/app/outputs/model.pt")


def test_an_anthrogen_pod_writing_to_the_shared_drive_keeps_pointers(monkeypatch):
    """A Kubernetes pod is a disposable machine, but its NFS-mounted
    /workspace is the storage that lasts."""
    monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "10.0.0.1")
    _mounts(monkeypatch, ("/", "overlay"), ("/workspace", "nfs4"))
    assert ephemeral.storage_is_durable("/workspace/Library/ckpt-2000.pt")
    assert not ephemeral.storage_is_durable("/tmp/scratch.pt")


def test_a_modal_volume_lasts_and_the_container_does_not(monkeypatch):
    monkeypatch.setenv("MODAL_TASK_ID", "ta-1")
    _mounts(
        monkeypatch,
        ("/", "overlay"),
        ("/__modal/volumes", "9p"),
        ("/__modal/mounts", "9p"),
    )
    assert ephemeral.storage_is_durable("/__modal/volumes/vo-abc/ckpt.pt")
    assert not ephemeral.storage_is_durable("/__modal/mounts/code/x.py")
    assert not ephemeral.storage_is_durable("/root/outputs/ckpt.pt")


def test_links_are_followed_to_the_real_storage(monkeypatch):
    monkeypatch.setenv("MODAL_TASK_ID", "ta-1")
    monkeypatch.setattr(
        ephemeral, "_realpath", lambda p: str(p).replace("/vol", "/__modal/volumes/vo-abc", 1)
    )
    _mounts(monkeypatch, ("/", "overlay"), ("/__modal/volumes", "9p"))
    assert ephemeral.storage_is_durable("/vol/ckpt.pt")


@pytest.mark.parametrize("fstype", ["nfs", "lustre", "gpfs", "cephfs", "fuse.sshfs", "fuse.juicefs", "fuse.s3fs"])
def test_network_and_remote_mounts_last(monkeypatch, fstype):
    monkeypatch.setenv("SLURM_JOB_ID", "123")
    _mounts(monkeypatch, ("/", "ext4"), ("/scratch", fstype))
    assert ephemeral.storage_is_durable("/scratch/me/run/ckpt.pt")


def test_a_local_fuse_filesystem_is_not_mistaken_for_remote(monkeypatch):
    monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "10.0.0.1")
    _mounts(monkeypatch, ("/", "ext4"), ("/proc/cpuinfo", "fuse.lxcfs"))
    assert not ephemeral.storage_is_durable("/proc/cpuinfo")


@pytest.mark.parametrize("marker", ["MODAL_TASK_ID", "KUBERNETES_SERVICE_HOST", "SLURM_JOB_ID", "GITHUB_ACTIONS", "RUNPOD_POD_ID"])
def test_a_local_disk_on_a_disposable_machine_is_throwaway(monkeypatch, marker):
    monkeypatch.setenv(marker, "1")
    _mounts(monkeypatch, ("/", "ext4"))
    assert not ephemeral.storage_is_durable("/tmp/job/out.bin")


def test_ci_true_is_disposable(monkeypatch):
    monkeypatch.setenv("CI", "true")
    _mounts(monkeypatch, ("/", "ext4"))
    assert not ephemeral.storage_is_durable("/work/out.bin")


def test_a_docker_container_marker_is_disposable(monkeypatch, tmp_path):
    marker = tmp_path / ".dockerenv"
    marker.write_text("")
    monkeypatch.setattr(ephemeral, "_CONTAINER_FILES", (str(marker),))
    _mounts(monkeypatch, ("/", "ext4"))
    assert not ephemeral.storage_is_durable("/data/out.bin")


def test_no_mount_table_falls_back_to_the_machine(monkeypatch):
    _mounts(monkeypatch)  # macOS: nothing to read
    assert ephemeral.storage_is_durable("/Users/me/out.bin")
    monkeypatch.setenv("CI", "1")
    assert not ephemeral.storage_is_durable("/Users/me/out.bin")


@pytest.mark.parametrize(("value", "durable"), [("1", False), ("0", True)])
def test_the_override_wins(monkeypatch, value, durable):
    monkeypatch.setenv(ephemeral.ENV, value)
    _mounts(monkeypatch, ("/", "overlay"), ("/workspace", "nfs"))
    assert ephemeral.storage_is_durable("/workspace/x") is durable
    assert ephemeral.storage_is_durable("/tmp/x") is durable


def test_the_mount_table_parser_reads_real_mountinfo_lines(monkeypatch, tmp_path):
    ephemeral.refresh()
    text = (
        "22 1 0:21 / / rw,relatime - overlay overlay rw\n"
        "35 22 0:40 / /mnt/my\\040drive rw - nfs4 srv:/export rw\n"
        "36 22 0:41 / /workspace rw shared:1 - fuse.sshfs me@host:/w rw\n"
    )
    real_open = open

    def fake_open(path, *a, **k):
        if path == "/proc/self/mountinfo":
            from io import StringIO

            return StringIO(text)
        return real_open(path, *a, **k)

    monkeypatch.setattr("builtins.open", fake_open)
    try:
        assert ephemeral.fstype_of("/mnt/my drive/ckpt.pt") == "nfs4"
        assert ephemeral.fstype_of("/workspace/run/x") == "fuse.sshfs"
        assert ephemeral.fstype_of("/workspacefoo/x") == "overlay"  # prefix is per path segment
        assert ephemeral.fstype_of("/root/x") == "overlay"
    finally:
        ephemeral.refresh()


@pytest.mark.parametrize("fstype", ["fuse.fuse-overlayfs", "fuse.squashfuse"])
def test_a_rootless_containers_fuse_layer_is_throwaway(monkeypatch, fstype):
    """Podman rootless mounts its layers through FUSE; every other FUSE mount
    counts as remote storage, which would make big files pointers to nothing."""
    _mounts(monkeypatch, ("/", fstype))
    assert not ephemeral.storage_is_durable("/app/ckpt.pt")


def test_of_two_mounts_on_one_point_the_one_on_top_decides(monkeypatch, tmp_path):
    ephemeral.refresh()
    text = (
        "22 1 0:21 / / rw - overlay overlay rw\n"
        "40 22 0:50 / /data rw - ext4 /dev/sda1 rw\n"
        "41 40 0:51 / /data rw - nfs4 srv:/data rw\n"
    )
    real_open = open

    def fake_open(path, *a, **k):
        if path == "/proc/self/mountinfo":
            from io import StringIO

            return StringIO(text)
        return real_open(path, *a, **k)

    monkeypatch.setattr("builtins.open", fake_open)
    try:
        assert ephemeral.fstype_of("/data/ckpt.pt") == "nfs4"
    finally:
        ephemeral.refresh()


def test_pseudo_filesystems_are_named_for_the_walk_to_skip(monkeypatch):
    _mounts(monkeypatch, ("/", "overlay"), ("/proc", "proc"), ("/sys", "sysfs"), ("/workspace", "nfs4"))
    assert ephemeral.pseudo_mountpoints() == {"/proc", "/sys"}
