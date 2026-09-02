from __future__ import annotations

from .harness import FidelityHarness, assert_outcomes_equal


async def _run_pair(h: FidelityHarness, argv: list[str]) -> None:
    real = await h.run_real(argv)
    virt = await h.run_virtual(argv)
    assert_outcomes_equal(h, real, virt, argv)


# ---------------------------------------------------------------------------
# cat
# ---------------------------------------------------------------------------


async def test_err_cat_no_such(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["cat", "/no/such"])


async def test_err_cat_directory(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["cat", "/sub"])


async def test_err_cat_dot_in_path(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["cat", "/missing/file"])


# ---------------------------------------------------------------------------
# ls
# ---------------------------------------------------------------------------


async def test_err_ls_no_such(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["ls", "/no/such/path"])


# ---------------------------------------------------------------------------
# mkdir
# ---------------------------------------------------------------------------


async def test_err_mkdir_existing(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["mkdir", "/existing"])


async def test_err_mkdir_no_parent(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["mkdir", "/no/such/path"])


# ---------------------------------------------------------------------------
# rm
# ---------------------------------------------------------------------------


async def test_err_rm_missing(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["rm", "/missing"])


async def test_err_rm_directory_no_recursive(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["rm", "/sub"])


# ---------------------------------------------------------------------------
# rmdir
# ---------------------------------------------------------------------------


async def test_err_rmdir_non_empty(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["rmdir", "/non-empty"])


async def test_err_rmdir_missing(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["rmdir", "/missing"])


async def test_err_rmdir_file(error_harness: FidelityHarness) -> None:
    # GNU rmdir reports 'Not a directory' when target is a file; the VFS
    # matches this exactly.
    await _run_pair(error_harness, ["rmdir", "/a.txt"])


# ---------------------------------------------------------------------------
# mv / cp
# ---------------------------------------------------------------------------


async def test_err_mv_missing(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["mv", "/missing", "/dest"])


async def test_err_cp_missing(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["cp", "/missing", "/dest"])


async def test_err_cp_dir_no_recursive(error_harness: FidelityHarness) -> None:
    # cp without -r on a directory: both emit "cp: -r not specified; omitting
    # directory '<path>'" with matching exit code.
    await _run_pair(error_harness, ["cp", "/sub", "/dest"])


# ---------------------------------------------------------------------------
# chmod / chown
# ---------------------------------------------------------------------------


async def test_err_chmod_missing(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["chmod", "644", "/missing"])


async def test_err_chown_missing(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["chown", "root", "/missing"])


# ---------------------------------------------------------------------------
# head / tail
# ---------------------------------------------------------------------------


async def test_err_head_missing(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["head", "/missing"])


async def test_err_tail_missing(error_harness: FidelityHarness) -> None:
    await _run_pair(error_harness, ["tail", "/missing"])
