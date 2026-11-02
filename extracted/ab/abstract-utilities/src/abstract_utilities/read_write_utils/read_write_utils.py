"""
read_write_utils.py
-------------------
Read, write, create and copy files — locally, on a remote host over ssh, and as
root via sudo. The implementation is abstract_essentials.read_write_utils; this
module re-exports it.

Usage:
    from abstract_utilities.read_write_utils import <names>
"""
from .imports import (
    shlex,
    os,
    shutil,
    uuid,
    Path,
    is_file,
    is_exists,
    get_user_pass_host_key,
    run_cmd,
    get_print_sudo_cmd,
    run_local_cmd,
    run_remote_cmd,
    run_pruned_func,
    eatAll,
    eatOuter,
    string_in_keys,
    check_read_write_params,
    make_dirs,
    make_path,
    path_join,
    get_rel_path,
    make_relative_path,
    get_path,
    break_down_find_existing,
    write_to_file,
    write_to_path,
    read_from_file,
    delete_file,
    copy_dirs,
    copy_file,
    copy_files,
    create_and_read_file,
    is_file_extension,
    get_content_lines,
    collate_text_docs,
    get_content,
    get_text_or_read,
)
