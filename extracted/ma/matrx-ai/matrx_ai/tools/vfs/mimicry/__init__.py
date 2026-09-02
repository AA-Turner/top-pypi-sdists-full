from __future__ import annotations

from typing import Literal, TypedDict

from matrx_ai.tools.vfs.mimicry.cat import (
    format_cat,
    format_cat_minus_a,
    format_cat_n,
    format_cat_n_with_offset,
)
from matrx_ai.tools.vfs.mimicry.claude_tool import (
    create_file_exists,
    create_success,
    edit_multiple_matches,
    edit_n_matches,
    edit_no_match,
    edit_not_found,
    edit_perm_denied,
    edit_string_not_found,
    edit_success,
    path_is_directory,
    path_not_absolute,
    view_empty_warning,
    view_response,
)
from matrx_ai.tools.vfs.mimicry.coreutils_errors import (
    cat_is_dir,
    cat_no_file,
    cat_perm,
    cd_no_dir,
    cd_not_dir,
    chmod_no_access,
    cmd_not_found,
    cp_no_src,
    cp_omit_dir,
    find_no_file,
    from_oserror,
    grep_is_dir,
    grep_no_file,
    head_no_file,
    ln_exists,
    ls_no_access,
    ls_perm_denied_dir,
    mkdir_exists,
    mkdir_no_parent,
    mv_no_src,
    rm_is_dir,
    rm_no_file,
    rmdir_not_empty,
    sed_no_file,
    tail_no_file,
)
from matrx_ai.tools.vfs.mimicry.dates import format_date_ls, format_iso_nanos, format_stat_y
from matrx_ai.tools.vfs.mimicry.grep import (
    GrepOpts,
    format_grep_binary_warning,
    format_grep_count,
    format_grep_filenames_only,
    format_grep_match,
    format_grep_with_context,
)
from matrx_ai.tools.vfs.mimicry.ls import (
    LsOpts,
    format_ls_l,
    format_ls_lh,
    format_ls_simple,
)
from matrx_ai.tools.vfs.mimicry.sizes import format_size_human
from matrx_ai.tools.vfs.mimicry.stat import format_stat_default, format_stat_format_string
from matrx_ai.tools.vfs.mimicry.traceback import (
    Frame,
    file_exists,
    file_not_found,
    format_traceback,
    is_a_directory,
    not_a_directory,
    permission_denied,
)


class InodeView(TypedDict):
    name: str
    type: Literal["file", "dir", "link"]
    mode: int
    uid: int
    gid: int
    user: str
    group: str
    size: int
    nlink: int
    mtime: float
    ctime: float
    atime: float
    symlink_target: str | None


__all__ = [
    "Frame",
    "GrepOpts",
    "InodeView",
    "LsOpts",
    "cat_is_dir",
    "cat_no_file",
    "cat_perm",
    "cd_no_dir",
    "cd_not_dir",
    "chmod_no_access",
    "cmd_not_found",
    "cp_no_src",
    "cp_omit_dir",
    "create_file_exists",
    "create_success",
    "edit_multiple_matches",
    "edit_n_matches",
    "edit_no_match",
    "edit_not_found",
    "edit_perm_denied",
    "edit_string_not_found",
    "edit_success",
    "file_exists",
    "file_not_found",
    "find_no_file",
    "format_cat",
    "format_cat_minus_a",
    "format_cat_n",
    "format_cat_n_with_offset",
    "format_date_ls",
    "format_grep_binary_warning",
    "format_grep_count",
    "format_grep_filenames_only",
    "format_grep_match",
    "format_grep_with_context",
    "format_iso_nanos",
    "format_ls_l",
    "format_ls_lh",
    "format_ls_simple",
    "format_size_human",
    "format_stat_default",
    "format_stat_format_string",
    "format_stat_y",
    "format_traceback",
    "from_oserror",
    "grep_is_dir",
    "grep_no_file",
    "head_no_file",
    "is_a_directory",
    "ln_exists",
    "ls_no_access",
    "ls_perm_denied_dir",
    "mkdir_exists",
    "mkdir_no_parent",
    "mv_no_src",
    "not_a_directory",
    "path_is_directory",
    "path_not_absolute",
    "permission_denied",
    "rm_is_dir",
    "rm_no_file",
    "rmdir_not_empty",
    "sed_no_file",
    "tail_no_file",
    "view_empty_warning",
    "view_response",
]
