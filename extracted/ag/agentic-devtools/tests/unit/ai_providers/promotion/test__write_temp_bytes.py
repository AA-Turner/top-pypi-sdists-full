import re
from pathlib import Path

import pytest

from agentic_devtools.ai_providers import promotion


def test_write_temp_bytes_uses_uuid_suffix(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    created_paths: list[Path] = []
    original_write = Path.write_bytes

    def tracking_write(self: Path, data: bytes) -> int:
        created_paths.append(self)
        return original_write(self, data)

    monkeypatch.setattr(Path, "write_bytes", tracking_write)

    target = tmp_path / "target.json"
    promotion._write_temp_bytes(target, b'{"foo": "bar"}')

    uuid_hex_pattern = re.compile(r"^[0-9a-f]{32}$")
    temp_paths = [p for p in created_paths if p.suffix == ".tmp"]
    assert temp_paths, "Expected at least one .tmp file to be created"
    for p in temp_paths:
        parts = p.name.split(".")
        assert uuid_hex_pattern.fullmatch(parts[-2]), f"Expected UUID hex suffix in temp filename, got: {p.name}"


def test_write_temp_bytes_cleans_up_partial_temp_file_on_write_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def failing_write(self: Path, data: bytes) -> int:
        self.parent.mkdir(parents=True, exist_ok=True)
        with self.open("wb") as handle:
            handle.write(data[:3])
        raise OSError("disk full")

    monkeypatch.setattr(Path, "write_bytes", failing_write)

    with pytest.raises(OSError, match="disk full"):
        promotion._write_temp_bytes(tmp_path / "target.json", b"abcdef")

    assert list(tmp_path.iterdir()) == []
