"""Task Tests: Media Generation (Image, Audio, Video, Animation)

Tests the generation of asset files using AI (either directly or via script)
across clients and verifies valid formats.
"""

from __future__ import annotations

import pytest
from sage.tests.functional.harnesses import run_test_with_verification
from sage.tests.functional.validators import validate_media

MODEL = "cloud:qwen3-coder"

class TestTaskMedia:
    
    def test_cli_image_svg(self):
        req = {
            "cli_request": "sage ask 'Generate an SVG image of a sunrise over mountains and save it as sunrise.svg and stop' --agent",
            "description": "CLI SVG Image",
        }
        res, verify = run_test_with_verification("cli", req, MODEL)
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path and res.artifact_path.is_file():
            validate_media(res.artifact_path, {"extension": ".svg"})

    def test_sms_audio_wav(self):
        req = {
            "sms_request": "@run Create a python script that generates a 1-second 440Hz sine wave WAV file called beep.wav and runs the script to generate the file.",
            "description": "SMS Audio WAV",
        }
        res, verify = run_test_with_verification("sms", req, MODEL, language="python")
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path and res.artifact_path.is_dir():
            wavs = list(res.artifact_path.glob("*.wav"))
            if wavs:
                validate_media(wavs[0], {"extension": ".wav"})
                
    def test_web_video_mp4(self):
        # We test generation of a video generating script because direct LLM video generation is rare
        req = {
            "web_request": {"task": "Write a python script using cv2 (opencv-python) to create a 1-second mp4 video with a red background. Include requirements.txt."},
            "description": "Web Video Script",
        }
        res, verify = run_test_with_verification("web", req, MODEL, language="python")
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        assert verify.tests_ok, f"Tests failed: {verify.details.get('tests')}"
        
        if res.artifact_path and res.artifact_path.is_dir():
            assert (res.artifact_path / "requirements.txt").exists()
            assert list(res.artifact_path.glob("*.py"))
