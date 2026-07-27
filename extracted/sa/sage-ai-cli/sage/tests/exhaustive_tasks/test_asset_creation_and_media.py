import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

@pytest.mark.parametrize("asset_type", [
    "svg", "png", "jpg", "gif", "mp3", "wav", "midi", "mp4", "webm", "pdf",
    "csv", "json", "yaml", "toml", "md"
])
def test_asset_generation(asset_type):
    """Verify that asset creation tasks write complete content with appropriate file extensions and pass the rubric."""
    prompt = f"Create a complete asset file for {asset_type} extension."
    verify_cli_with_rubric(prompt)


@pytest.mark.parametrize("asset_type", [
    "svg", "png", "jpg", "gif", "mp3", "wav", "midi", "mp4", "webm", "pdf",
    "csv", "json", "yaml", "toml", "md"
])
def test_asset_generation_sms(asset_type, tmp_path):
    """Verify asset creation via SMS bridge."""
    prompt = f"Create a complete asset file for {asset_type} extension."
    verify_sms_with_rubric(prompt, tmp_path)


@pytest.mark.parametrize("asset_type", [
    "svg", "png", "jpg", "gif", "mp3", "wav", "midi", "mp4", "webm", "pdf",
    "csv", "json", "yaml", "toml", "md"
])
def test_asset_generation_website(asset_type):
    """Verify asset creation via website backend."""
    prompt = f"Create a complete asset file for {asset_type} extension."
    verify_website_with_rubric(prompt)
