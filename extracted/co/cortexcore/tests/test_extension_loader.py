from __future__ import annotations

import os
import time
from contextlib import nullcontext
from pathlib import Path

from cortex.kernels.cuda import extension_loader


def test_safe_load_extension_retries_missing_lock(monkeypatch) -> None:
    attempts = {"count": 0}

    def fake_maybe_clear_stale_lock(name: str) -> None:
        assert name == "demo_ext"

    def fake_load(**kwargs):
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise FileNotFoundError(2, "No such file or directory", str(Path("/tmp") / "lock"))
        return {"name": kwargs["name"]}

    monkeypatch.setattr(extension_loader, "_host_build_lock", lambda _name: nullcontext())
    monkeypatch.setattr(extension_loader, "_maybe_clear_stale_lock", fake_maybe_clear_stale_lock)
    monkeypatch.setattr(extension_loader, "load", fake_load)

    loaded = extension_loader.safe_load_extension(name="demo_ext", sources=["demo.cpp"])

    assert loaded == {"name": "demo_ext"}
    assert attempts["count"] == 2


def test_safe_load_extension_does_not_retry_unrelated_file_not_found(monkeypatch) -> None:
    def fake_load(**_kwargs):
        raise FileNotFoundError(2, "No such file or directory", str(Path("/tmp") / "demo.cpp"))

    monkeypatch.setattr(extension_loader, "_host_build_lock", lambda _name: nullcontext())
    monkeypatch.setattr(extension_loader, "_maybe_clear_stale_lock", lambda _name: None)
    monkeypatch.setattr(extension_loader, "load", fake_load)

    try:
        extension_loader.safe_load_extension(name="demo_ext", sources=["demo.cpp"])
    except FileNotFoundError as exc:
        assert Path(exc.filename or "").name == "demo.cpp"
    else:
        raise AssertionError("Expected FileNotFoundError to be raised for non-lock paths")


def test_safe_load_extension_retries_partial_import(monkeypatch, tmp_path: Path) -> None:
    attempts = {"count": 0}

    def fake_load(**kwargs):
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise ImportError(f"{tmp_path / 'demo_ext.so'}: file too short")
        return {"name": kwargs["name"]}

    monkeypatch.setattr(extension_loader, "_host_build_lock", lambda _name: nullcontext())
    monkeypatch.setattr(extension_loader, "_maybe_clear_stale_lock", lambda _name: None)
    monkeypatch.setattr(extension_loader, "_extension_path", lambda _name: tmp_path / "demo_ext.so")
    monkeypatch.setattr(extension_loader, "load", fake_load)

    loaded = extension_loader.safe_load_extension(name="demo_ext", sources=["demo.cpp"])

    assert loaded == {"name": "demo_ext"}
    assert attempts["count"] == 2


def test_extension_loader_clears_recent_lock_when_extension_exists(monkeypatch, tmp_path: Path) -> None:
    build_dir = tmp_path / "agalite_discounted_sum"
    build_dir.mkdir()
    lock_path = build_dir / "lock"
    lock_path.write_text("")
    (build_dir / "agalite_discounted_sum.so").write_text("")

    monkeypatch.setattr(extension_loader, "_get_build_directory", lambda name, verbose=False: str(build_dir))

    extension_loader._maybe_clear_stale_lock("agalite_discounted_sum")

    assert not lock_path.exists()


def test_extension_loader_clears_old_lock_when_extension_exists(monkeypatch, tmp_path: Path) -> None:
    build_dir = tmp_path / "agalite_discounted_sum"
    build_dir.mkdir()
    lock_path = build_dir / "lock"
    lock_path.write_text("")
    (build_dir / "agalite_discounted_sum.so").write_text("")
    old_time = time.time() - extension_loader._STALE_LOCK_MAX_AGE_SEC - 1
    os.utime(lock_path, (old_time, old_time))

    monkeypatch.setattr(extension_loader, "_get_build_directory", lambda name, verbose=False: str(build_dir))

    extension_loader._maybe_clear_stale_lock("agalite_discounted_sum")

    assert not lock_path.exists()
