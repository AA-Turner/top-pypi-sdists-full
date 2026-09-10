from pathlib import Path

import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_cleans_up_temp_file_when_atomic_replace_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "dispatch.json"
    temp_paths: list[Path] = []
    original_replace = dispatch_state_module.os.replace

    def raising_replace(src: str | Path, dst: str | Path) -> None:
        temp_paths.append(Path(src))
        raise OSError("boom")

    monkeypatch.setattr(dispatch_state_module.os, "replace", raising_replace)

    with pytest.raises(OSError):
        dispatch_state_module._write_store(path, {})

    assert temp_paths
    assert all(not temp_path.exists() for temp_path in temp_paths)
    monkeypatch.setattr(dispatch_state_module.os, "replace", original_replace)


def test_ignores_temp_cleanup_failures(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "dispatch.json"
    monkeypatch.setattr(dispatch_state_module.os, "replace", lambda _src, _dst: (_ for _ in ()).throw(OSError("boom")))
    monkeypatch.setattr(dispatch_state_module.os, "unlink", lambda _path: (_ for _ in ()).throw(OSError("missing")))

    with pytest.raises(OSError):
        dispatch_state_module._write_store(path, {})
