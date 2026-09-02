from __future__ import annotations

from .harness import FidelityHarness, assert_outcomes_equal


async def _run_pair(
    h: FidelityHarness,
    argv: list[str],
    *,
    sort_lines: bool = True,
) -> None:
    real = await h.run_real(argv)
    virt = await h.run_virtual(argv)
    if sort_lines:
        real_out = sorted(h.normalize_real(real.stdout).splitlines())
        virt_out = sorted(virt.stdout.splitlines())
        assert real_out == virt_out, f"sorted stdout differs.\nreal={real_out!r}\nvirt={virt_out!r}"
        real_err = h.normalize_real(real.stderr)
        assert real_err == virt.stderr, f"stderr differs.\nreal={real_err!r}\nvirt={virt.stderr!r}"
        assert real.exit_code == virt.exit_code, (
            f"exit code differs: real={real.exit_code} virt={virt.exit_code}"
        )
    else:
        assert_outcomes_equal(h, real, virt, argv)


async def test_find_name_glob_py(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["find", "/", "-name", "*.py"])


async def test_find_name_glob_txt(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["find", "/", "-name", "*.txt"])


async def test_find_type_f(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["find", "/", "-type", "f"])


async def test_find_type_d(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["find", "/", "-type", "d"])


async def test_find_missing_path(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["find", "/missing"], sort_lines=False)


async def test_find_or(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["find", "/", "-name", "*.txt", "-o", "-name", "*.md"])


async def test_find_subdir_only(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["find", "/sub", "-name", "*.py"])


async def test_find_no_predicate(basic_harness: FidelityHarness) -> None:
    # `find /` with no predicate prints every entry; both impls should agree
    # once we sort.
    await _run_pair(basic_harness, ["find", "/"])


async def test_find_maxdepth(basic_harness: FidelityHarness) -> None:
    await _run_pair(basic_harness, ["find", "/", "-maxdepth", "1"])


async def test_find_name_only_filename(basic_harness: FidelityHarness) -> None:
    # `-name` matches against the basename only — no slash.
    await _run_pair(basic_harness, ["find", "/", "-name", "deep.py"])
