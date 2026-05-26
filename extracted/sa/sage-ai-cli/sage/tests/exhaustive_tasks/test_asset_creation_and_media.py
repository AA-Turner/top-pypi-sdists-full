import os
import re
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from sage.main import app as sage_app
from sage.core.content_validator import validate_content

runner = CliRunner()

ASSET_MOCKS = {
    "svg": """
Output for SVG:
FILE: icon.svg
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <rect x="10" y="10" width="80" height="80" fill="#10b981" rx="15" />
</svg>
```
""",
    "png": """
Output for PNG:
FILE: placeholder.png
```
PNG_BINARY_MOCK_DATA_STREAM
```
""",
    "jpg": """
Output for JPG:
FILE: placeholder.jpg
```
JPG_BINARY_MOCK_DATA_STREAM
```
""",
    "gif": """
Output for GIF:
FILE: placeholder.gif
```
GIF_BINARY_MOCK_DATA_STREAM
```
""",
    "mp3": """
Output for MP3:
FILE: audio.mp3
```
MP3_BINARY_MOCK_DATA_STREAM
```
""",
    "wav": """
Output for WAV:
FILE: audio.wav
```
WAV_BINARY_MOCK_DATA_STREAM
```
""",
    "midi": """
Output for MIDI:
FILE: song.midi
```
MIDI_BINARY_MOCK_DATA_STREAM
```
""",
    "mp4": """
Output for MP4:
FILE: video.mp4
```
MP4_BINARY_MOCK_DATA_STREAM
```
""",
    "webm": """
Output for WebM:
FILE: video.webm
```
WEBM_BINARY_MOCK_DATA_STREAM
```
""",
    "pdf": """
Output for PDF:
FILE: document.pdf
```
PDF_BINARY_MOCK_DATA_STREAM
```
""",
    "csv": """
Output for CSV:
FILE: data.csv
```csv
id,name,value
1,Campaign A,100
2,Campaign B,250
```
""",
    "json": """
Output for JSON:
FILE: config.json
```json
{
  "name": "ad-platform",
  "version": "1.0.0",
  "settings": {
    "enableAds": true,
    "maxCampaigns": 50
  }
}
```
""",
    "yaml": """
Output for YAML:
FILE: config.yaml
```yaml
name: ad-platform
version: 1.0.0
settings:
  enableAds: true
  maxCampaigns: 50
```
""",
    "toml": """
Output for TOML:
FILE: config.toml
```toml
name = "ad-platform"
version = "1.0.0"

[settings]
enableAds = true
maxCampaigns = 50
```
""",
    "md": """
Output for Markdown:
FILE: README.md
```markdown
# Ad Platform

This is a complete ad platform repository setup.
It contains routing, DB connection, and tests.
```
"""
}

@pytest.mark.parametrize("asset_type", [
    "svg", "png", "jpg", "gif", "mp3", "wav", "midi", "mp4", "webm", "pdf",
    "csv", "json", "yaml", "toml", "md"
])
def test_asset_generation(asset_type):
    """Verify that asset creation tasks write complete content with appropriate file extensions."""
    prompt = f"Create a complete asset file for {asset_type} extension."
    mock_output = ASSET_MOCKS[asset_type]

    with patch("sage.main._prepare_model_for_use") as mock_prep, \
         patch("sage.main._build_router") as mock_router:
         
        mock_prep.return_value = (MagicMock(), "cloud:gemini-2.0-flash")
        mock_router_inst = MagicMock()
        mock_router_inst.stream.return_value = [mock_output]
        mock_router.return_value = mock_router_inst
        
        with runner.isolated_filesystem():
            result = runner.invoke(sage_app, ["ask", prompt, "--raw", "--agent"])
            assert result.exit_code == 0, f"Task failed: {result.output}"
            
            generated_files = [
                f for f in Path(".").glob("**/*")
                if f.is_file() and not any(part.startswith(".") or part in ("venv", "__pycache__") for part in f.parts) and f.suffix != ".pyc"
            ]
            assert len(generated_files) > 0, "No files written"
            
            for f in generated_files:
                content = f.read_text(encoding="utf-8")
                val_res = validate_content(str(f), content)
                assert val_res.ok, f"File {f} contains placeholders/errors: {val_res.reason}"
