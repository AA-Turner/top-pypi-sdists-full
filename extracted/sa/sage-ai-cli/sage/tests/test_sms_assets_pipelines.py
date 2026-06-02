import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

ASSETS_PIPELINE_TASKS = [
    ("IMG-01", "Generate geometric shapes sprite sheet using Python Pillow atlas for IMG-01"),
    ("IMG-02", "Write Node.js script to create vector SVG logo with gradient for IMG-02"),
    ("AUD-01", "Generate procedural wav drum loop using Python pydub/numpy for AUD-01"),
    ("AUD-02", "Synthesize narration voiceover mp3 using TTS API for AUD-02"),
    ("VID-01", "Create Python moviepy animated intro mp4 for VID-01"),
    ("MODEL-01", "Use Blender Python API to rig humanoid 3D character fbx for MODEL-01"),
    ("MODEL-02", "Write Three.js scene glb exporter for MODEL-02"),
    ("DOC-01", "Generate markdown README with table of contents and shields badge for DOC-01"),
    ("DOC-02", "Use LaTeX to produce technical architecture spec pdf with PlantUML for DOC-02"),
    ("DATA-01", "Write JSON schema config validation check for DATA-01"),
    ("DATA-02", "Generate synthetic CSV dataset with 10M rows using Faker for DATA-02")
]
@pytest.mark.parametrize("task_id, prompt", ASSETS_PIPELINE_TASKS)
def test_assets_pipelines_sms(task_id, prompt, tmp_path):
    """Verify complex asset pipeline tasks via SMS."""
    verify_sms_with_rubric(prompt, tmp_path)
