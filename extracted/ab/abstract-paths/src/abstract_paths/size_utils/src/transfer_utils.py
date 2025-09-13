from .cmd_utils import *
from .dir_utils import *
from .size_utils import *
def transfer_missing(src_directory, dst_directory, local=True, host=None):
    """
    Compare local vs backup and transfer missing/different files to backup.
    Try normal rsync first, fall back to sudo rsync if permission denied.
    """
    diffs = get_sizes(src_directory, dst_directory, local=local, host=host)
    if not diffs or not diffs.get("needs"):
        print("✅ Backup is already up to date.")
        return

    skipped = {}

    for directory, diff in diffs["needs"].items():
        src_path = os.path.join(src_directory if isinstance(src_directory, str) else src_directory["directory"], directory)
        dst_path = os.path.join(dst_directory if isinstance(dst_directory, str) else dst_directory["directory"], directory)

        # Ensure remote directory exists
        run_remote_cmd(
            user_at_host=host,
            cmd=f"mkdir -p {dst_path}",
            workdir=os.path.dirname(dst_path),
            shell=True,
            text=True,
            capture_output=True,
        )

        # Base rsync command
        cmd = f'rsync -avz --ignore-existing "{src_path}/" "{host}:{dst_path}/"'
        print(f"🔄 Syncing {src_path} → {host}:{dst_path}")

        result = run_local_cmd(cmd=cmd, workdir=os.path.dirname(src_path), shell=True, text=True, capture_output=True)

        if "Permission denied" in str(result):
            print(f"⚠️ Permission denied, retrying with sudo: {src_path}")
            cmd_sudo = f'sudo rsync -avz --ignore-existing "{src_path}/" "{host}:{dst_path}/"'
            result = run_local_cmd(cmd=cmd_sudo, workdir=os.path.dirname(src_path), shell=True, text=True, capture_output=True)

            if "Permission denied" in str(result):
                print(f"❌ Still could not copy {src_path}")
                skipped[src_path] = result

    print("✅ Transfer complete. Backup updated.")
    if skipped:
        print("⚠️ The following paths still could not be copied:")
        for k in skipped:
            print(f"   - {k}")
