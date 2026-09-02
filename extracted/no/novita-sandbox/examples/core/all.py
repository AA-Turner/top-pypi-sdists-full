import asyncio
import os
from time import time

from dotenv import load_dotenv

from novita_sandbox.core import AsyncSandbox, AsyncTemplate, AsyncVolume, Sandbox, Template, Volume
from novita_sandbox.core.sandbox.filesystem.filesystem import WriteEntry

load_dotenv()


RUN_ASYNC = os.getenv("NOVITA_RUN_ASYNC", "true").lower() != "false"
TEMPLATE_NAME = os.getenv("NOVITA_TEMPLATE_NAME", f"core-all-{int(time())}")
TEMPLATE_TAG = "example"


def show_template_list(label, templates):
    print(
        f"    {label}: total={templates.total}, page={templates.page}, "
        f"limit={templates.limit}, total_pages={templates.total_pages}"
    )
    for template in templates.items[:3]:
        print(
            f"      template_id={template.template_id}, "
            f"build_id={template.build_id}, type={template.template_type}"
        )


def build_template():
    print("\n=== Template setup ===")
    template = (
        Template()
        .from_python_image("3.12")
        .run_cmd("python --version")
        .set_envs({"PYTHONUNBUFFERED": "1"})
        .set_patch_cmd("touch ~/patch-ok.txt")
        .set_ready_cmd("true")
    )

    build_info = Template.build(
        template,
        TEMPLATE_NAME,
        tags=[TEMPLATE_TAG],
        cpu_count=2,
        memory_mb=1024,
        on_build_logs=lambda log: print(f"    [{log.level}] {log.message}"),
    )
    print(f"    template_id={build_info.template_id}, build_id={build_info.build_id}")
    return build_info


def run_sync_core(build_info):
    sbx = None
    connected = None
    clone_result = None
    vol = None
    snapshot_id = None
    volume_name = f"example-vol-sync-{int(time())}"

    print("\n=== Sync core APIs ===")
    try:
        print("[sync:1] Template list/status/tag helpers")
        show_template_list(
            "template_build",
            Template.list(template_type="template_build", page=1, limit=3),
        )
        show_template_list(
            "snapshot_template",
            Template.list(template_type="snapshot_template", page=1, limit=3),
        )
        status = Template.get_build_status(build_info)
        print(f"    build_status={status.status}, logs={len(status.logs)}")
        print(f"    exists={Template.exists(TEMPLATE_NAME)}")
        print(f"    alias_exists={Template.alias_exists(TEMPLATE_NAME)}")
        tag_info = Template.assign_tags(f"{TEMPLATE_NAME}:{TEMPLATE_TAG}", "sync")
        print(f"    assigned_tags={tag_info.tags}")
        print(f"    tags={len(Template.get_tags(build_info.template_id))}")
        Template.remove_tags(TEMPLATE_NAME, "sync")

        print("[sync:2] Volume.create/connect/get_info/list/update_quota")
        vol = Volume.create(volume_name, quota_size_gib=1, quota_inodes=1000)
        connected_vol = Volume.connect(vol.volume_id)
        volume_info = Volume.get_info(vol.volume_id)
        volumes = Volume.list()
        updated_volume = Volume.update_quota(vol.volume_id, quota_size_gib=2)
        print(
            f"    volume_id={vol.volume_id}, connected={connected_vol.name}, "
            f"quota={updated_volume.quota_size_gib}GiB, listed={len(volumes)}, "
            f"token={'yes' if volume_info.token else 'no'}"
        )

        print("[sync:3] Sandbox.create with created volume pre-mounted")
        sbx = Sandbox.create(
            build_info.template_id,
            timeout=300,
            metadata={"example": "core-all-sync"},
            envs={"EXAMPLE_MODE": "sync"},
            lifecycle={"on_timeout": "kill"},
            volume_mounts={"/mnt/pre": vol},
        )
        print(f"    sandbox_id={sbx.sandbox_id}, running={sbx.is_running()}")

        print("[sync:4] Sandbox info/connect/list/set_timeout/metrics")
        info = sbx.get_info()
        connected = Sandbox.connect(sbx.sandbox_id, timeout=300)
        paginator = Sandbox.list(limit=5)
        listed = paginator.next_items()
        sbx.set_timeout(300)
        try:
            metrics = sbx.get_metrics()
        except Exception as exc:
            metrics = []
            print(f"    metrics skipped: {exc}")
        print(
            f"    info_id={info.sandbox_id}, connected_id={connected.sandbox_id}, "
            f"listed={len(listed)}, metrics={len(metrics)}"
        )

        print("[sync:5] Filesystem methods")
        sbx.files.write("/tmp/core-all.txt", "hello sync")
        sbx.files.write_files([
            WriteEntry(path="/tmp/core-all-a.txt", data="a"),
            WriteEntry(path="/tmp/core-all-b.txt", data="b"),
        ])
        print(f"    read={sbx.files.read('/tmp/core-all.txt')}")
        print(f"    exists={sbx.files.exists('/tmp/core-all.txt')}")
        print(f"    entries={len(sbx.files.list('/tmp'))}")
        print(f"    file_info={sbx.files.get_info('/tmp/core-all.txt').name}")
        sbx.files.rename("/tmp/core-all-a.txt", "/tmp/core-all-renamed.txt")
        sbx.files.make_dir("/tmp/core-all-dir")
        sbx.files.remove("/tmp/core-all-b.txt")

        print("[sync:6] Command methods")
        result = sbx.commands.run("printf sync-command")
        handle = sbx.commands.run("sleep 1 && printf sync-start", background=True)
        print(f"    run={result.stdout.strip()}, wait={handle.wait().stdout.strip()}")
        print(f"    processes={len(sbx.commands.list())}")

        print("[sync:7] Git methods")
        sbx.commands.run("mkdir -p /tmp/core-all-git && cd /tmp/core-all-git && git init")
        sbx.git.set_config("user.email", "example@example.com", scope="local", path="/tmp/core-all-git")
        sbx.git.set_config("user.name", "Example", scope="local", path="/tmp/core-all-git")
        print(f"    git_user={sbx.git.get_config('user.name', scope='local', path='/tmp/core-all-git')}")
        git_status = sbx.git.status(path="/tmp/core-all-git")
        branches = sbx.git.branches(path="/tmp/core-all-git")
        print(f"    git_clean={git_status.is_clean}, branches={len(branches.branches)}")

        print("[sync:8] Mount/unmount volume")
        sbx.mount_volume(vol.name, "/mnt/manual")
        sbx.commands.run('echo "mounted" > /mnt/manual/manual.txt')
        sbx.unmount_volume("/mnt/manual", force=True)

        print("[sync:9] Snapshot/template methods")
        snapshot = sbx.create_snapshot()
        snapshot_id = snapshot.snapshot_id
        snapshots = sbx.list_snapshots(limit=5).next_items()
        print(f"    snapshot_id={snapshot_id}, listed_snapshots={len(snapshots)}")

        print("[sync:10] Clone/reset/pause/connect")
        clone_result = Sandbox.clone(sbx.sandbox_id, count=1)
        print(f"    clones={clone_result.count}")
        print(f"    reset={sbx.reset(resume=True, timeout=300)}")
        sbx.pause()
        sbx.connect(timeout=300)

    finally:
        print("[sync:cleanup]")
        if clone_result:
            for clone in clone_result:
                try:
                    clone.kill()
                except Exception as exc:
                    print(f"    clone cleanup skipped: {exc}")
        if connected and connected is not sbx:
            try:
                connected.kill()
            except Exception:
                pass
        if sbx:
            try:
                sbx.kill()
            except Exception as exc:
                print(f"    sandbox cleanup skipped: {exc}")
        if snapshot_id:
            try:
                print(f"    delete_snapshot={Sandbox.delete_snapshot(snapshot_id)}")
            except Exception as exc:
                print(f"    snapshot cleanup skipped: {exc}")
        if vol:
            try:
                print(f"    volume_destroy={Volume.destroy(vol.volume_id)}")
            except Exception as exc:
                print(f"    volume cleanup skipped: {exc}")


async def run_async_core(build_info):
    sbx = None
    connected = None
    clone_result = None
    vol = None
    snapshot_id = None
    volume_name = f"example-vol-async-{int(time())}"

    print("\n=== Async core APIs ===")
    try:
        print("[async:1] AsyncTemplate list/status/tag helpers")
        show_template_list(
            "template_build",
            await AsyncTemplate.list(template_type="template_build", page=1, limit=3),
        )
        show_template_list(
            "snapshot_template",
            await AsyncTemplate.list(template_type="snapshot_template", page=1, limit=3),
        )
        status = await AsyncTemplate.get_build_status(build_info)
        print(f"    build_status={status.status}, logs={len(status.logs)}")
        print(f"    exists={await AsyncTemplate.exists(TEMPLATE_NAME)}")
        print(f"    alias_exists={await AsyncTemplate.alias_exists(TEMPLATE_NAME)}")
        tag_info = await AsyncTemplate.assign_tags(f"{TEMPLATE_NAME}:{TEMPLATE_TAG}", "async")
        print(f"    assigned_tags={tag_info.tags}")
        print(f"    tags={len(await AsyncTemplate.get_tags(build_info.template_id))}")
        await AsyncTemplate.remove_tags(TEMPLATE_NAME, "async")

        print("[async:2] AsyncVolume.create/connect/get_info/list/update_quota")
        vol = await AsyncVolume.create(volume_name, quota_size_gib=1, quota_inodes=1000)
        connected_vol = await AsyncVolume.connect(vol.volume_id)
        volume_info = await AsyncVolume.get_info(vol.volume_id)
        volumes = await AsyncVolume.list()
        updated_volume = await AsyncVolume.update_quota(vol.volume_id, quota_size_gib=2)
        print(
            f"    volume_id={vol.volume_id}, connected={connected_vol.name}, "
            f"quota={updated_volume.quota_size_gib}GiB, listed={len(volumes)}, "
            f"token={'yes' if volume_info.token else 'no'}"
        )

        print("[async:3] AsyncSandbox.create with created volume pre-mounted")
        sbx = await AsyncSandbox.create(
            build_info.template_id,
            timeout=300,
            metadata={"example": "core-all-async"},
            envs={"EXAMPLE_MODE": "async"},
            lifecycle={"on_timeout": "kill"},
            volume_mounts={"/mnt/pre": vol},
        )
        print(f"    sandbox_id={sbx.sandbox_id}, running={await sbx.is_running()}")

        print("[async:4] Sandbox info/connect/list/set_timeout/metrics")
        info = await sbx.get_info()
        connected = await AsyncSandbox.connect(sbx.sandbox_id, timeout=300)
        paginator = AsyncSandbox.list(limit=5)
        listed = await paginator.next_items()
        await sbx.set_timeout(300)
        try:
            metrics = await sbx.get_metrics()
        except Exception as exc:
            metrics = []
            print(f"    metrics skipped: {exc}")
        print(
            f"    info_id={info.sandbox_id}, connected_id={connected.sandbox_id}, "
            f"listed={len(listed)}, metrics={len(metrics)}"
        )

        print("[async:5] Filesystem methods")
        await sbx.files.write("/tmp/core-all.txt", "hello async")
        await sbx.files.write_files([
            WriteEntry(path="/tmp/core-all-a.txt", data="a"),
            WriteEntry(path="/tmp/core-all-b.txt", data="b"),
        ])
        print(f"    read={await sbx.files.read('/tmp/core-all.txt')}")
        print(f"    exists={await sbx.files.exists('/tmp/core-all.txt')}")
        print(f"    entries={len(await sbx.files.list('/tmp'))}")
        file_info = await sbx.files.get_info("/tmp/core-all.txt")
        print(f"    file_info={file_info.name}")
        await sbx.files.rename("/tmp/core-all-a.txt", "/tmp/core-all-renamed.txt")
        await sbx.files.make_dir("/tmp/core-all-dir")
        await sbx.files.remove("/tmp/core-all-b.txt")

        print("[async:6] Command methods")
        result = await sbx.commands.run("printf async-command")
        handle = await sbx.commands.run("sleep 1 && printf async-start", background=True)
        waited = await handle.wait()
        print(f"    run={result.stdout.strip()}, wait={waited.stdout.strip()}")
        print(f"    processes={len(await sbx.commands.list())}")

        print("[async:7] Git methods")
        await sbx.commands.run("mkdir -p /tmp/core-all-git && cd /tmp/core-all-git && git init")
        await sbx.git.set_config("user.email", "example@example.com", scope="local", path="/tmp/core-all-git")
        await sbx.git.set_config("user.name", "Example", scope="local", path="/tmp/core-all-git")
        print(f"    git_user={await sbx.git.get_config('user.name', scope='local', path='/tmp/core-all-git')}")
        git_status = await sbx.git.status(path="/tmp/core-all-git")
        branches = await sbx.git.branches(path="/tmp/core-all-git")
        print(f"    git_clean={git_status.is_clean}, branches={len(branches.branches)}")

        print("[async:8] Mount/unmount volume")
        await sbx.mount_volume(vol.name, "/mnt/manual")
        await sbx.commands.run('echo "mounted" > /mnt/manual/manual.txt')
        await sbx.unmount_volume("/mnt/manual", force=True)

        print("[async:9] Snapshot/template methods")
        snapshot = await sbx.create_snapshot()
        snapshot_id = snapshot.snapshot_id
        snapshots = await sbx.list_snapshots(limit=5).next_items()
        print(f"    snapshot_id={snapshot_id}, listed_snapshots={len(snapshots)}")

        print("[async:10] Clone/reset/pause/connect")
        clone_result = await AsyncSandbox.clone(sbx.sandbox_id, count=1)
        print(f"    clones={clone_result.count}")
        print(f"    reset={await sbx.reset(resume=True, timeout=300)}")
        await sbx.pause()
        await sbx.connect(timeout=300)

    finally:
        print("[async:cleanup]")
        if clone_result:
            for clone in clone_result:
                try:
                    await clone.kill()
                except Exception as exc:
                    print(f"    clone cleanup skipped: {exc}")
        if connected and connected is not sbx:
            try:
                await connected.kill()
            except Exception:
                pass
        if sbx:
            try:
                await sbx.kill()
            except Exception as exc:
                print(f"    sandbox cleanup skipped: {exc}")
        if snapshot_id:
            try:
                print(f"    delete_snapshot={await AsyncSandbox.delete_snapshot(snapshot_id)}")
            except Exception as exc:
                print(f"    snapshot cleanup skipped: {exc}")
        if vol:
            try:
                print(f"    volume_destroy={await AsyncVolume.destroy(vol.volume_id)}")
            except Exception as exc:
                print(f"    volume cleanup skipped: {exc}")


def main():
    build_info = None
    try:
        build_info = build_template()
        run_sync_core(build_info)
        if RUN_ASYNC:
            asyncio.run(run_async_core(build_info))
    finally:
        if build_info:
            try:
                print(f"\n=== Template cleanup ===\n    template_delete={Template.delete(build_info.template_id)}")
            except Exception as exc:
                print(f"\n=== Template cleanup ===\n    template cleanup skipped: {exc}")


if __name__ == "__main__":
    main()
