"""Module providing task_utils functionality."""

import os
import shutil
import urllib.request
import zipfile
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
    
    # Download codebase ZIP file
    urllib.request.urlretrieve(model_codebase_url, codebase_zip_path)
    
    # Extract ZIP file with overwrite
    with zipfile.ZipFile(codebase_zip_path, 'r') as zip_ref:
        zip_ref.extractall(workspace_dir)
    
    # Move files from subdirectories to workspace root (equivalent to rsync -av)
    for root, dirs, files in os.walk(workspace_dir):
        # Skip the workspace_dir itself to avoid moving files to themselves
        if root == workspace_dir:
            continue
        
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(workspace_dir, file)
            
            # If destination file exists, overwrite it (equivalent to rsync -av behavior)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            
            shutil.move(src_file, dst_file)
        
        # Remove empty directories after moving files
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if os.path.exists(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)
    
    # Clean up any remaining empty subdirectories
    for root, dirs, files in os.walk(workspace_dir, topdown=False):
        if root == workspace_dir:
            continue
        if not files and not dirs:
            try:
                os.rmdir(root)
            except OSError:
                pass  # Directory might not be empty or might not exist
    
    # Download requirements.txt if URL is provided
    if model_codebase_requirements_url:
        urllib.request.urlretrieve(model_codebase_requirements_url, requirements_txt_path)
