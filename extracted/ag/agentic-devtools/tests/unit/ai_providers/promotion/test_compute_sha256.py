import hashlib
from pathlib import Path

from agentic_devtools.ai_providers.promotion import compute_sha256


def test_compute_sha256_returns_file_digest(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("hello", encoding="utf-8")

    digest = compute_sha256(path)

    assert digest == hashlib.sha256(b"hello").hexdigest()
