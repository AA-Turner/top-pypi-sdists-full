from pathlib import Path
from unittest.mock import patch

from agentic_devtools.ai_providers.copilot_discovery import get_cache_path


def test_cache_path_is_under_the_user_config_dir(tmp_path: Path) -> None:
    with patch("agentic_devtools.ai_providers.copilot_discovery.user_config_dir", return_value=tmp_path):
        assert get_cache_path() == tmp_path / "agdt" / "caches" / "copilot-models.json"
