from __future__ import annotations

from .harness import FidelityHarness, assert_outcomes_equal


async def _run_pair(
    h: FidelityHarness,
    argv: list[str],
    *,
    sort_lines: bool = False,
) -> None:
    real = await h.run_real(argv)
    virt = await h.run_virtual(argv)
    if sort_lines:
        real_lines = sorted(h.normalize_real(real.stdout).splitlines())
        virt_lines = sorted(virt.stdout.splitlines())
        assert real_lines == virt_lines, (
            f"sorted stdout differs.\nreal={real_lines!r}\nvirt={virt_lines!r}"
        )
        assert real.exit_code == virt.exit_code
        # Stderr / paths still need normalization for any error lines.
        real_err = h.normalize_real(real.stderr)
        assert real_err == virt.stderr
        return
    assert_outcomes_equal(h, real, virt, argv)


async def test_grep_no_match(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "TODO", "/a.txt"])


async def test_grep_match(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "alpha", "/a.txt"])


async def test_grep_multiple_matches(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "alpha", "/sub/c.py"])


async def test_grep_recursive(grep_harness: FidelityHarness) -> None:
    # Real grep -r and the VFS may walk in different order; sort line-by-line.
    await _run_pair(grep_harness, ["grep", "-rn", "alpha", "/"], sort_lines=True)


async def test_grep_recursive_no_lineno(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "-r", "alpha", "/"], sort_lines=True)


async def test_grep_missing_file(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "PAT", "/missing"])


async def test_grep_directory_no_recurse(grep_harness: FidelityHarness) -> None:
    # grep on a dir without -r is an error.  Both sides should match.
    await _run_pair(grep_harness, ["grep", "PAT", "/sub"])


async def test_grep_invert(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "-v", "alpha", "/a.txt"])


async def test_grep_count(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "-c", "alpha", "/a.txt"])


async def test_grep_ignore_case(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "-i", "GAMMA", "/a.txt"])


async def test_grep_line_number(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "-n", "alpha", "/a.txt"])


async def test_grep_files_with_matches(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "-rl", "alpha", "/"], sort_lines=True)


async def test_grep_word_match(grep_harness: FidelityHarness) -> None:
    await _run_pair(grep_harness, ["grep", "-w", "alpha", "/a.txt"])
