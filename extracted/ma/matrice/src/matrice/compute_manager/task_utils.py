"""Module providing task_utils functionality."""

import os
import shlex
import subprocess
from matrice.utils import log_errors


@log_errors(raise_exception=True, log_error=True)
def setup_workspace_and_run_task(
    work_fs,
    action_id,
    model_codebase_url,
    model_codebase_requirements_url,
):
    """Set up workspace and run task with provided parameters.

    Args:
        work_fs: Working filesystem path
        action_id: Unique identifier for the action
        model_codebase_url: URL to download model codebase from
        model_codebase_requirements_url: URL to download requirements from

    Returns:
        None
    """
    workspace_dir = f"{work_fs}/{action_id}"
    codebase_zip_path = f"{workspace_dir}/file.zip"
    requirements_txt_path = f"{workspace_dir}/requirements.txt"
    if os.path.exists(workspace_dir):
        return
    os.makedirs(workspace_dir, exist_ok=True)
    download_codebase_cmd = (
        f"curl -L -o {shlex.quote(codebase_zip_path)} {shlex.quote(model_codebase_url)}"
    )
    subprocess.run(
        download_codebase_cmd,
        shell=True,
        check=True,
    )
    unzip_codebase_cmd = (
        f"unzip -o {shlex.quote(codebase_zip_path)} -d {shlex.quote(workspace_dir)}"
    )
    subprocess.run(unzip_codebase_cmd, shell=True, check=True)
    move_files_cmd = f"rsync -av {shlex.quote(workspace_dir)}/*/ {shlex.quote(workspace_dir)}/ "
    subprocess.run(move_files_cmd, shell=True, check=True)
    if model_codebase_requirements_url:
        download_requirements_cmd = f"curl -L -o {shlex.quote(requirements_txt_path)} {shlex.quote(model_codebase_requirements_url)}"
        subprocess.run(
            download_requirements_cmd,
            shell=True,
            check=True,
        )
