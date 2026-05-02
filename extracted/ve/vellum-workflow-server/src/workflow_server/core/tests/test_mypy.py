import pytest
import pathlib

from workflow_server.core.type_checker import get_checker


def test_build_cache__mypy(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    # GIVEN
    checker = get_checker("mypy")
    is_configured, _ = checker.is_configured()
    assert is_configured

    cache_dir = tmp_path / ".mypy_cache"
    monkeypatch.setenv("VELLUM_MYPY_CACHE_DIR", str(cache_dir))

    # WHEN
    result = checker.build_cache()

    # THEN we should populate the cache directory
    assert result is None

    assert cache_dir.exists()
    assert any(cache_dir.iterdir()), "Cache directory should contain files after building cache"
