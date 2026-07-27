import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


@pytest.mark.parametrize("asset_type", [
    "svg", "png", "jpg", "gif", "mp3", "wav", "midi", "mp4", "webm", "pdf",
    "csv", "json", "yaml", "toml", "md"
])
def test_asset_generation_sms(asset_type, tmp_path):
    """Verify simple asset creation tasks via SMS bridge."""
    prompt = f"Create a complete asset file for {asset_type} extension."
    verify_sms_with_rubric(prompt, tmp_path)
