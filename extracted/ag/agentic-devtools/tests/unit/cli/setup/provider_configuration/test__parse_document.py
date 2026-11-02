"""Unit tests for _parse_document."""

from pathlib import Path
from unittest.mock import patch

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def test__parse_document_maps_file_read_failures(tmp_path: Path) -> None:
    path = tmp_path / "bad-provider-config.yml"
    path.write_bytes(b"\xff")
    assert provider_configuration._parse_document(path)[1] == "invalid_yaml"

    path.write_text("- item", encoding="utf-8")
    assert provider_configuration._parse_document(path)[1] == "invalid_root"

    with patch.object(Path, "read_text", side_effect=OSError):
        assert provider_configuration._parse_document(path)[1] == "invalid_yaml"
