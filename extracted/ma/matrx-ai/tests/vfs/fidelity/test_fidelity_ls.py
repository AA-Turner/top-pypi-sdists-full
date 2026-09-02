from __future__ import annotations

from .harness import FidelityHarness, assert_outcomes_equal


async def _run_pair(
    h: FidelityHarness,
    argv: list[str],
    *,
    strip_timestamps: bool = False,
    normalize_paths: bool = True,
) -> None:
    real = await h.run_real(argv)
    virt = await h.run_virtual(argv)
    assert_outcomes_equal(
        h,
        real,
        virt,
        argv,
        normalize_paths=normalize_paths,
        strip_timestamps=strip_timestamps,
    )


async def test_ls_root(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "/"])


async def test_ls_subdir(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "/sub"])


async def test_ls_one_per_line(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "-1", "/"])


async def test_ls_all(basic_harness: FidelityHarness) -> None:
    # `-a` includes "." and "..", which the VFS may or may not emit; if it
    # diverges this test will surface it.
    await _run_pair(basic_harness, ["ls", "-a", "/"])


async def test_ls_capital_a(basic_harness: FidelityHarness) -> None:
    # `-A` shows dotfiles but not "." / "..".  This is the most reliable
    # subset of -a behavior.
    await _run_pair(basic_harness, ["ls", "-A", "/"])


async def test_ls_missing_path(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "/missing"])


async def test_ls_file_arg(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "/a.txt"])


async def test_ls_mixed_partial_fail(basic_harness: FidelityHarness) -> None:
    # real ls prints OK files then errors; the VFS replicates this.
    await _run_pair(basic_harness, ["ls", "/a.txt", "/missing"])


async def test_ls_classify(basic_harness: FidelityHarness) -> None:
    # `-F` appends a type suffix.  Both implementations should agree.
    await _run_pair(basic_harness, ["ls", "-F", "/"])


async def test_ls_recursive(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "-R", "/"])


async def test_ls_long(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "-l", "/"], strip_timestamps=True)


async def test_ls_long_all(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "-la", "/"], strip_timestamps=True)


async def test_ls_empty_dir(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "/empty"])


async def test_ls_nested_subdir(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "/sub/inner"])


async def test_ls_two_dirs(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "/sub", "/empty"])


async def test_ls_dotfile_explicit(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["ls", "/.dotfile"])
