"""Task Tests: Website Generation

Tests the generation of full responsive websites (HTML/CSS/JS) across
different clients (CLI, Web, SMS) and verifies them using the 4-gate system
(install, build, run, tests).
"""

from __future__ import annotations

import pytest
from sage.tests.functional.harnesses import run_test_with_verification
from sage.tests.functional.validators import validate_website

MODEL = "cloud:qwen3-coder"

# We test a subset of permutations to keep test time reasonable,
# but cover all channels and core website types.

class TestTaskWebsite:
    
    @pytest.mark.parametrize("theme", ["dark", "minimal"])
    def test_cli_portfolio(self, theme):
        req = {
            "cli_request": f"sage ask 'Build a {theme} portfolio website using React. Include an index.js and package.json with a build script.' --agent",
            "description": f"CLI Portfolio ({theme})",
        }
        res, verify = run_test_with_verification("cli", req, MODEL)
        
        assert res.exit_code == 0
        assert verify.install_ok, f"Install failed: {verify.details.get('install')}"
        assert verify.build_ok, f"Build failed: {verify.details.get('build')}"
        assert verify.run_ok, f"Run failed: {verify.details.get('run')}"
        
        # Additional manual validation
        if res.artifact_path and res.artifact_path.is_dir():
            if (res.artifact_path / "package.json").exists():
                assert (res.artifact_path / "src").exists() or (res.artifact_path / "public").exists() or (res.artifact_path / "index.js").exists()

    def test_sms_landing_page(self):
        req = {
            "sms_request": f"@run Build a landing page for a coffee shop in vanilla HTML/CSS. Put it in index.html.",
            "description": "SMS Landing Page",
        }
        res, verify = run_test_with_verification("sms", req, MODEL)
        
        assert res.exit_code == 0
        assert verify.install_ok  # Auto-pass for vanilla HTML
        assert verify.build_ok    # Auto-pass for vanilla HTML
        assert verify.run_ok      # Should find index.html
        
        if res.artifact_path and res.artifact_path.is_dir():
            index = res.artifact_path / "index.html"
            validate_website(index, {"valid_html": True})

    def test_web_dashboard(self):
        req = {
            "web_request": {"task": "Build a simple admin dashboard using React. Save files in the workspace."},
            "description": "Web Dashboard",
        }
        res, verify = run_test_with_verification("web", req, MODEL)
        
        assert res.exit_code == 0
        assert verify.install_ok
        assert verify.build_ok
        assert verify.run_ok
