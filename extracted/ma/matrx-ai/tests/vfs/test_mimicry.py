from __future__ import annotations

import errno
from datetime import UTC, datetime

import pytest

from matrx_ai.tools.vfs.mimicry import (
    Frame,
    GrepOpts,
    InodeView,
    LsOpts,
    cat_is_dir,
    cat_no_file,
    cat_perm,
    cd_no_dir,
    cd_not_dir,
    chmod_no_access,
    cmd_not_found,
    cp_no_src,
    cp_omit_dir,
    create_file_exists,
    create_success,
    edit_multiple_matches,
    edit_n_matches,
    edit_no_match,
    edit_not_found,
    edit_perm_denied,
    edit_string_not_found,
    edit_success,
    file_not_found,
    find_no_file,
    format_cat_minus_a,
    format_cat_n,
    format_cat_n_with_offset,
    format_date_ls,
    format_grep_binary_warning,
    format_grep_count,
    format_grep_filenames_only,
    format_grep_match,
    format_ls_l,
    format_ls_lh,
    format_ls_simple,
    format_size_human,
    format_stat_default,
    format_stat_format_string,
    format_traceback,
    from_oserror,
    grep_is_dir,
    grep_no_file,
    head_no_file,
    is_a_directory,
    ln_exists,
    ls_no_access,
    ls_perm_denied_dir,
    mkdir_exists,
    mkdir_no_parent,
    mv_no_src,
    not_a_directory,
    path_is_directory,
    path_not_absolute,
    permission_denied,
    rm_is_dir,
    rm_no_file,
    rmdir_not_empty,
    sed_no_file,
    tail_no_file,
    view_empty_warning,
    view_response,
)

# ---------------------------------------------------------------------------
# format_size_human
# ---------------------------------------------------------------------------


def test_size_human_zero():
    assert format_size_human(0) == "0"


def test_size_human_one():
    assert format_size_human(1) == "1"


def test_size_human_just_under_kilo():
    assert format_size_human(999) == "999"


def test_size_human_exactly_kilo():
    assert format_size_human(1024) == "1.0K"


def test_size_human_1_5k():
    # 1500 / 1024 = 1.4648... -> rounds to 1.5K
    assert format_size_human(1500) == "1.5K"


def test_size_human_12k():
    # 12*1024 = 12288 -> exactly 12.0 -> drops decimal at >= 10
    assert format_size_human(12 * 1024) == "12K"


def test_size_human_one_meg():
    assert format_size_human(1024 * 1024) == "1.0M"


def test_size_human_1_5_meg():
    assert format_size_human(int(1.5 * 1024 * 1024)) == "1.5M"


# ---------------------------------------------------------------------------
# format_date_ls
# ---------------------------------------------------------------------------


def test_date_ls_recent_padded_day():
    # May 7 17:54 UTC, viewed an hour later -> recent form
    mtime = datetime(2026, 5, 7, 17, 54, tzinfo=UTC).timestamp()
    now = mtime + 3600
    s = format_date_ls(mtime, now)
    assert s == "May  7 17:54"
    assert len(s) == 12


def test_date_ls_seven_months_ago():
    # 7 months back -> uses year form
    now = datetime(2026, 5, 7, 12, 0, tzinfo=UTC).timestamp()
    mtime = datetime(2025, 10, 1, 12, 0, tzinfo=UTC).timestamp()
    s = format_date_ls(mtime, now)
    assert s == "Oct  1  2025"
    assert len(s) == 12


def test_date_ls_two_years_ago():
    now = datetime(2026, 5, 7, 12, 0, tzinfo=UTC).timestamp()
    mtime = datetime(2024, 1, 15, 9, 0, tzinfo=UTC).timestamp()
    s = format_date_ls(mtime, now)
    assert s == "Jan 15  2024"
    assert len(s) == 12


# ---------------------------------------------------------------------------
# format_ls_l
# ---------------------------------------------------------------------------


def _ino(
    name: str,
    itype: str,
    mode: int,
    size: int,
    nlink: int,
    mtime: float,
    symlink_target: str | None = None,
) -> InodeView:
    return InodeView(
        name=name,
        type=itype,  # type: ignore[typeddict-item]
        mode=mode,
        uid=1000,
        gid=1000,
        user="user",
        group="user",
        size=size,
        nlink=nlink,
        mtime=mtime,
        ctime=mtime,
        atime=mtime,
        symlink_target=symlink_target,
    )


def test_format_ls_l_byte_exact():
    mt = datetime(2026, 5, 7, 17, 53, tzinfo=UTC).timestamp()
    now = mt + 60
    entries: list[InodeView] = [
        _ino("a.txt", "file", 0o644, 12, 1, mt),
        _ino("b.txt", "file", 0o644, 100, 1, mt),
        _ino("c.sh", "file", 0o755, 50, 1, mt),
        _ino("subdir", "dir", 0o755, 4096, 2, mt),
        _ino("link", "link", 0o777, 5, 1, mt, symlink_target="a.txt"),
    ]
    opts = LsOpts(now=now)
    out = format_ls_l(entries, opts)
    # total = 5 entries each rounded up to one 4 KiB block -> 5 * 4 = 20 KiB blocks.
    expected = (
        "total 20\n"
        "-rw-r--r-- 1 user user   12 May  7 17:53 a.txt\n"
        "-rw-r--r-- 1 user user  100 May  7 17:53 b.txt\n"
        "-rwxr-xr-x 1 user user   50 May  7 17:53 c.sh\n"
        "lrwxrwxrwx 1 user user    5 May  7 17:53 link -> a.txt\n"
        "drwxr-xr-x 2 user user 4096 May  7 17:53 subdir\n"
    )
    assert out == expected


def test_format_ls_simple():
    mt = datetime(2026, 5, 7, 17, 53, tzinfo=UTC).timestamp()
    entries = [
        _ino("b.txt", "file", 0o644, 5, 1, mt),
        _ino("a.txt", "file", 0o644, 5, 1, mt),
    ]
    out = format_ls_simple(entries, LsOpts())
    assert out == "a.txt\nb.txt\n"


def test_format_ls_lh_uses_human_sizes():
    mt = datetime(2026, 5, 7, 17, 53, tzinfo=UTC).timestamp()
    now = mt + 60
    entries = [_ino("big.bin", "file", 0o644, 1500, 1, mt)]
    out = format_ls_lh(entries, LsOpts(now=now))
    assert "1.5K" in out


def test_format_ls_l_hides_dotfiles_by_default():
    mt = datetime(2026, 5, 7, 17, 53, tzinfo=UTC).timestamp()
    now = mt + 60
    entries = [
        _ino(".hidden", "file", 0o644, 1, 1, mt),
        _ino("visible", "file", 0o644, 1, 1, mt),
    ]
    out = format_ls_l(entries, LsOpts(now=now))
    assert ".hidden" not in out
    assert "visible" in out


def test_format_ls_l_shows_dotfiles_with_all():
    mt = datetime(2026, 5, 7, 17, 53, tzinfo=UTC).timestamp()
    now = mt + 60
    entries = [
        _ino(".hidden", "file", 0o644, 1, 1, mt),
        _ino("visible", "file", 0o644, 1, 1, mt),
    ]
    out = format_ls_l(entries, LsOpts(now=now, all=True, show_hidden=True))
    assert ".hidden" in out


# ---------------------------------------------------------------------------
# format_cat_n
# ---------------------------------------------------------------------------


def test_cat_n_empty():
    assert format_cat_n("") == ""


def test_cat_n_single_line():
    assert format_cat_n("hello") == "     1\thello\n"


def test_cat_n_multi_line():
    out = format_cat_n("a\nb\nc")
    assert out == "     1\ta\n     2\tb\n     3\tc\n"


def test_cat_n_trailing_newline():
    out = format_cat_n("a\nb\n")
    assert out == "     1\ta\n     2\tb\n"


def test_cat_n_with_tabs_in_content():
    out = format_cat_n("\thello")
    assert out == "     1\t\thello\n"


def test_cat_n_offset():
    out = format_cat_n_with_offset("x\ny\nz", 10)
    assert out == "    10\tx\n    11\ty\n    12\tz\n"


def test_cat_minus_a_basic():
    assert format_cat_minus_a("a\tb\n") == "a^Ib$\n"
    assert format_cat_minus_a("hi\n") == "hi$\n"


# ---------------------------------------------------------------------------
# format_stat_default
# ---------------------------------------------------------------------------


def test_stat_default_regular_file():
    mt = datetime(2026, 5, 7, 17, 54, 23, tzinfo=UTC).timestamp()
    inode = _ino("file.txt", "file", 0o644, 12, 1, mt)
    out = format_stat_default(inode, "/path/file.txt")
    assert "File: /path/file.txt" in out
    assert "regular file" in out
    assert "(0644/-rw-r--r--)" in out
    assert "2026-05-07 17:54:23.000000000 +0000" in out
    assert "Modify: 2026-05-07 17:54:23" in out
    assert "Birth:" in out
    assert "Links: 1" in out


def test_stat_default_directory():
    mt = datetime(2026, 5, 7, 17, 54, 23, tzinfo=UTC).timestamp()
    inode = _ino("d", "dir", 0o755, 4096, 2, mt)
    out = format_stat_default(inode, "/path/d")
    assert "directory" in out
    assert "(0755/drwxr-xr-x)" in out


def test_stat_default_empty_file():
    mt = datetime(2026, 5, 7, 17, 54, 23, tzinfo=UTC).timestamp()
    inode = _ino("e", "file", 0o644, 0, 1, mt)
    out = format_stat_default(inode, "/e")
    assert "regular empty file" in out


def test_stat_format_string():
    mt = datetime(2026, 5, 7, 17, 54, 23, tzinfo=UTC).timestamp()
    inode = _ino("file.txt", "file", 0o644, 12, 1, mt)
    out = format_stat_format_string(inode, "%n %s %a %A %U %G")
    assert out == "file.txt 12 644 -rw-r--r-- user user"


# ---------------------------------------------------------------------------
# grep formatters
# ---------------------------------------------------------------------------


def test_grep_match_no_filename_no_lineno():
    assert format_grep_match("f.txt", 3, "hello", GrepOpts()) == "hello"


def test_grep_match_filename_only():
    out = format_grep_match("f.txt", 3, "hello", GrepOpts(show_filename=True))
    assert out == "f.txt:hello"


def test_grep_match_lineno_only():
    out = format_grep_match("f.txt", 3, "hello", GrepOpts(show_lineno=True))
    assert out == "3:hello"


def test_grep_match_both():
    out = format_grep_match("f.txt", 3, "hello", GrepOpts(show_filename=True, show_lineno=True))
    assert out == "f.txt:3:hello"


def test_grep_count_with_filename():
    assert format_grep_count("f.txt", 5, GrepOpts(show_filename=True)) == "f.txt:5"


def test_grep_count_no_filename():
    assert format_grep_count("f.txt", 5, GrepOpts()) == "5"


def test_grep_filenames_only():
    out = format_grep_filenames_only(["a.txt", "b.txt"])
    assert out == "a.txt\nb.txt\n"


def test_grep_binary_warning():
    assert format_grep_binary_warning("/x") == "Binary file /x matches"


# ---------------------------------------------------------------------------
# coreutils errors
# ---------------------------------------------------------------------------


def test_coreutils_errors_exact_strings():
    assert ls_no_access("/x") == "ls: cannot access '/x': No such file or directory\n"
    assert ls_perm_denied_dir("/x") == "ls: cannot open directory '/x': Permission denied\n"
    assert cat_no_file("/x") == "cat: /x: No such file or directory\n"
    assert cat_is_dir("/x") == "cat: /x: Is a directory\n"
    assert cat_perm("/x") == "cat: /x: Permission denied\n"
    assert mkdir_exists("/x") == "mkdir: cannot create directory '/x': File exists\n"
    assert (
        mkdir_no_parent("/x") == "mkdir: cannot create directory '/x': No such file or directory\n"
    )
    assert mv_no_src("/x") == "mv: cannot stat '/x': No such file or directory\n"
    assert cp_no_src("/x") == "cp: cannot stat '/x': No such file or directory\n"
    assert cp_omit_dir("/x") == "cp: -r not specified; omitting directory '/x'\n"
    assert rm_no_file("/x") == "rm: cannot remove '/x': No such file or directory\n"
    assert rm_is_dir("/x") == "rm: cannot remove '/x': Is a directory\n"
    assert rmdir_not_empty("/x") == "rmdir: failed to remove '/x': Directory not empty\n"
    assert grep_no_file("/x") == "grep: /x: No such file or directory\n"
    assert grep_is_dir("/x") == "grep: /x: Is a directory\n"
    assert find_no_file("/x") == "find: '/x': No such file or directory\n"
    assert chmod_no_access("/x") == "chmod: cannot access '/x': No such file or directory\n"
    assert head_no_file("/x") == "head: cannot open '/x' for reading: No such file or directory\n"
    assert tail_no_file("/x") == "tail: cannot open '/x' for reading: No such file or directory\n"
    assert sed_no_file("/x") == "sed: can't read /x: No such file or directory\n"
    assert cmd_not_found("foo") == "bash: foo: command not found\n"
    assert cd_no_dir("/x") == "bash: cd: /x: No such file or directory\n"
    assert cd_not_dir("/x") == "bash: cd: /x: Not a directory\n"
    assert ln_exists("/x") == "ln: failed to create symbolic link '/x': File exists\n"


def test_from_oserror_dispatches_correctly():
    err_enoent = OSError(errno.ENOENT, "No such file or directory")
    assert from_oserror("ls", "/x", err_enoent) == ls_no_access("/x")
    assert from_oserror("cat", "/x", err_enoent) == cat_no_file("/x")
    err_isdir = OSError(errno.EISDIR, "Is a directory")
    assert from_oserror("cat", "/x", err_isdir) == cat_is_dir("/x")


def test_from_oserror_fallback_quoting():
    # Unmapped errno + single-quote command falls back to single-quoted form.
    err = OSError(errno.EIO, "I/O error")
    out = from_oserror("ls", "/y", err)
    assert "'/y'" in out
    out2 = from_oserror("cat", "/y", err)
    # cat is bare-path
    assert "'/y'" not in out2
    assert "/y" in out2


# ---------------------------------------------------------------------------
# traceback
# ---------------------------------------------------------------------------


def test_traceback_file_not_found_exact():
    out = file_not_found("/missing")
    expected = (
        "Traceback (most recent call last):\n"
        '  File "<stdin>", line 1, in <module>\n'
        "    open('...')\n"
        "FileNotFoundError: [Errno 2] No such file or directory: '/missing'\n"
    )
    assert out == expected


def test_traceback_other_helpers():
    assert "[Errno 21] Is a directory: '/d'" in is_a_directory("/d")
    assert "[Errno 20] Not a directory: '/f'" in not_a_directory("/f")
    assert "[Errno 13] Permission denied: '/p'" in permission_denied("/p")
    from matrx_ai.tools.vfs.mimicry import file_exists as fexists

    assert "[Errno 17] File exists: '/e'" in fexists("/e")


def test_format_traceback_multi_frame():
    frames: list[Frame] = [
        Frame(file="a.py", lineno=10, funcname="main", source_line="foo()"),
        Frame(file="b.py", lineno=20, funcname="foo", source_line="raise X"),
    ]
    out = format_traceback("ValueError", "boom", frames)
    expected = (
        "Traceback (most recent call last):\n"
        '  File "a.py", line 10, in main\n'
        "    foo()\n"
        '  File "b.py", line 20, in foo\n'
        "    raise X\n"
        "ValueError: boom\n"
    )
    assert out == expected


# ---------------------------------------------------------------------------
# claude_tool emitters
# ---------------------------------------------------------------------------


def test_view_response():
    out = view_response("/p", "     1\thi\n")
    assert out == "Here's the result of running `cat -n` on /p:\n     1\thi\n"


def test_view_empty_warning():
    assert (
        view_empty_warning()
        == "<system-reminder>Warning: the file exists but the contents are empty.</system-reminder>"
    )


def test_create_success():
    assert create_success("/p") == "File created successfully at: /p"


def test_edit_success():
    out = edit_success("/p", "     1\tnew\n")
    expected = (
        "The file /p has been edited. Here's the result of running `cat -n` on /p:\n"
        "     1\tnew\n\n"
        "Review the changes and make sure they are as expected. Edit the file again "
        "if necessary."
    )
    assert out == expected


def test_edit_no_match():
    out = edit_no_match("foo", "/p")
    assert out == "No replacement was performed, old_str `foo` did not appear verbatim in /p."


def test_edit_multiple_matches():
    out = edit_multiple_matches("foo", [3, 7, 12])
    assert out == (
        "No replacement was performed. Multiple occurrences of old_str `foo` in lines "
        "[3, 7, 12]. Please ensure it is unique"
    )


def test_edit_not_found():
    assert edit_not_found() == "Error: File not found"


def test_edit_perm_denied():
    assert edit_perm_denied() == "Error: Permission denied. Cannot write to file."


def test_path_not_absolute():
    out = path_not_absolute("rel/p", "/abs/rel/p")
    assert out == (
        "The path rel/p is not an absolute path, it should start with `/`. Maybe you "
        "meant /abs/rel/p?"
    )


def test_path_is_directory():
    out = path_is_directory("/d")
    assert out == (
        "The path /d is a directory and only the `view` command can be used on directories"
    )


def test_create_file_exists():
    out = create_file_exists("/p")
    assert out == "File already exists at: /p. Cannot overwrite files using command `create`."


def test_edit_string_not_found():
    assert edit_string_not_found() == "String to replace not found in file."


def test_edit_n_matches():
    out = edit_n_matches(3)
    assert out == (
        "Found 3 matches of the string to replace, but replace_all is false. To "
        "replace all occurrences, set replace_all to true. To replace only one "
        "occurrence, please provide more context to uniquely identify the instance."
    )


# ---------------------------------------------------------------------------
# misc sanity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (0, "0"),
        (1023, "1023"),
        (1024, "1.0K"),
        (1025, "1.0K"),
        (10 * 1024, "10K"),
        # 1048575 / 1024 = 1023.999... rounds up to 1024, which GNU promotes to 1.0M.
        (1024 * 1024 - 1, "1.0M"),
        (1024 * 1024, "1.0M"),
        (1024 * 1024 * 1024, "1.0G"),
    ],
)
def test_size_human_table(size: int, expected: str):
    assert format_size_human(size) == expected
