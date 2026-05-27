import os
import pytest
from pathlib import Path
from typer.testing import CliRunner

from sage.main import app as sage_app
from sage.main import _build_multistep_phase_prompts

def test_empty_workspace_is_detected_as_greenfield():
    """Verify that an empty workspace is correctly detected as greenfield."""
    import tempfile
    from sage.core.p0_request_classification import ClassifiedRequestV2 as ClassifiedRequest, RequestTypeV2 as RequestType, PipelineTypeV2 as PipelineType, OutputFormatV2
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        cwd = Path(tmp_dir)
        
        prompt = "Make a music video for Lily that says I love you Lily you’re so pretty"
        
        classification = ClassifiedRequest(
            original_request=prompt,
            request_type=RequestType.IMPLEMENTATION,
            output_format=OutputFormatV2.CODE_FILES,
            pipeline_type=PipelineType.IMPLEMENTATION,
            confidence=1.0,
            alternative_types=[],
        )
        
        phases = _build_multistep_phase_prompts(prompt, classification=classification, cwd=cwd)
        
        # In a greenfield project, it should have exactly "planning" and "implementation" phases
        assert len(phases) == 2
        assert phases[0][0] == "planning"
        assert phases[1][0] == "implementation"
        assert "BRAND-NEW GREENFIELD PROJECT" in phases[0][1]

def test_multimedia_task_in_empty_workspace_execution():
    """Verify that SAGE executing in an empty workspace executes the greenfield workflow without failing."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Run SAGE CLI using the real OpenRouter provider pointing to the local test server
        prompt = "Make a music video for Lily that says I love you Lily you’re so pretty"
        result = runner.invoke(sage_app, [
            "ask", prompt, 
            "--raw", 
            "--agent",
            "--model", "openrouter:meta-llama/llama-3.3-70b-instruct:free"
        ])
        
        assert result.exit_code == 0, f"Task failed: {result.output}"
        
        # Check that the file was written
        target_file = Path("generated_media.mp4")
        assert target_file.exists()
