import pytest
from unittest.mock import MagicMock, patch
from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig

# Import mocks from other exhaustive tests to keep it DRY
from sage.tests.exhaustive_tasks.test_frontend_web_frameworks import FRONTEND_MOCKS
from sage.tests.exhaustive_tasks.test_backend_web_frameworks import BACKEND_MOCKS
from sage.tests.exhaustive_tasks.test_mobile_app_frameworks import MOBILE_MOCKS
from sage.tests.exhaustive_tasks.test_video_game_platforms import GAME_MOCKS
from sage.tests.exhaustive_tasks.test_programming_languages_core import CORE_MOCKS
from sage.tests.exhaustive_tasks.test_asset_creation_and_media import ASSET_MOCKS

# Construct the tasks list programmatically
ALL_TASKS = []

for key, val in FRONTEND_MOCKS.items():
    ALL_TASKS.append((
        "frontend",
        key,
        f"Implement a complete {key} application with state management and layouts.",
        val
    ))

for key, val in BACKEND_MOCKS.items():
    ALL_TASKS.append((
        "backend",
        key,
        f"Implement a complete {key} backend service with routing and DB persistence.",
        val
    ))

for key, val in MOBILE_MOCKS.items():
    ALL_TASKS.append((
        "mobile",
        key,
        f"Implement a complete {key} mobile component with lists and navigation.",
        val
    ))

for key, val in GAME_MOCKS.items():
    ALL_TASKS.append((
        "game",
        key,
        f"Implement a complete {key} video game player movement script.",
        val
    ))

for key, val in CORE_MOCKS.items():
    ALL_TASKS.append((
        "core_lang",
        key,
        f"Implement a complete, production-ready {key} module for concurrency or data management.",
        val
    ))

for key, val in ASSET_MOCKS.items():
    ALL_TASKS.append((
        "asset",
        key,
        f"Create a complete asset file for {key} extension.",
        val
    ))

@pytest.mark.parametrize("category,key,prompt,mock_output", ALL_TASKS)
def test_sms_exhaustive_task(category, key, prompt, mock_output, tmp_path):
    """Verify that the SMS Bridge successfully triggers the task and returns correct results."""
    cfg = SMSConfig(computer_name="TestPC", working_dir=str(tmp_path))
    
    with patch("sage.core.sms_bridge.SAGEBackend"), \
         patch("time.sleep"), \
         patch("subprocess.run") as mock_run:
         
        mock_run_inst = MagicMock()
        mock_run_inst.returncode = 0
        mock_run_inst.stdout = mock_output
        mock_run_inst.stderr = ""
        mock_run.return_value = mock_run_inst
        
        bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
        output = bridge._run_sage_task(prompt, mode="agent")
        
        assert "error" not in output.lower()
        
        expected_prefix = mock_output.strip().splitlines()[0]
        assert expected_prefix in output
        
        # Verify bridge called subprocess with correct parameters
        called_args = mock_run.call_args[0][0]
        assert any(x in called_args for x in ("run", "ask"))
        assert "--prompt" in called_args
