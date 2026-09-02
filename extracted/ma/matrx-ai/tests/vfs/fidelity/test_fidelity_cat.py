from __future__ import annotations

from .harness import FidelityHarness, assert_outcomes_equal


async def _run_pair(h: FidelityHarness, argv: list[str]) -> None:
    real = await h.run_real(argv)
    virt = await h.run_virtual(argv)
    assert_outcomes_equal(h, real, virt, argv)


async def test_cat_single_file(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "/a.txt"])


async def test_cat_concat(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "/a.txt", "/b.py"])


async def test_cat_three_files(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "/a.txt", "/b.py", "/c.md"])


async def test_cat_missing(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "/missing"])


async def test_cat_directory(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "/sub"])


async def test_cat_partial_fail(basic_harness: FidelityHarness) -> None:
    # Real cat outputs the readable file then errors on the missing one.
    await _run_pair(basic_harness, ["cat", "/a.txt", "/missing"])


async def test_cat_number_lines(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "-n", "/a.txt"])


async def test_cat_show_ends(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "-E", "/a.txt"])


async def test_cat_dotfile(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "/.dotfile"])


async def test_cat_nested(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "/sub/x.txt"])


async def test_cat_show_all(basic_harness: FidelityHarness) -> None:
    # `-A` combines `-E -T -v`; both implementations produce identical output
    # on plain ASCII text.
    await _run_pair(basic_harness, ["cat", "-A", "/a.txt"])


async def test_cat_squeeze_blank(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["cat", "-s", "/a.txt"])
