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


def test_healing_loop_functional_no_mocks():
    """Verify that SAGE's self-healing loop successfully repairs a compilation error in a Python project using the real LLM end-to-end without mocks."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # 1. Write a pyproject.toml and requirements.txt to define a Python project
        Path("pyproject.toml").write_text("[build-system]\nrequires = ['setuptools']\nbuild-backend = 'setuptools.build_meta'\n\n[project]\nname = 'broken-app'\nversion = '0.1.0'\n\n[tool.setuptools]\npackages = ['app']\n", encoding="utf-8")
        Path("requirements.txt").write_text("# requirements", encoding="utf-8")
        
        # 2. Write a Python file with a deliberate syntax error (missing colon)
        main_py = Path("app/main.py")
        main_py.parent.mkdir(parents=True, exist_ok=True)
        main_py.write_text("def run_app()\n    print('broken')\n", encoding="utf-8")
        
        # 3. Invoke SAGE CLI to fix the syntax error using the real OpenRouter free model.
        # We use a build prompt so that looks_like_build_request classifies it as a build and routes it to the builder pipeline.
        # We omit --raw so that it outputs build progress containing install_ok, build_ok, runs_ok, tests_ok.
        prompt = "Build a FastAPI backend app and fix the compilation error in app/main.py."
        result = runner.invoke(sage_app, [
            "run",
            "--prompt", prompt,
            "--no-color",
            "--model", "openrouter:meta-llama/llama-3.3-70b-instruct:free"
        ])
        
        # SAGE should run compile, hit compile error, call LLM to get the fix, validate, write, and exit 0
        print("\n=== SAGE OUTPUT ===")
        print(result.output)
        print("===================\n")
        assert result.exit_code == 0, f"Healing loop task failed: {result.output}"
        
        # 4. Verify that the output shows that verification checks succeeded
        assert "install_ok=True" in result.output
        assert "build_ok=True" in result.output
        assert "runs_ok=True" in result.output
        assert "tests_ok=True" in result.output
        
        # 5. Verify that app/main.py has been successfully fixed and is syntactically valid
        content = main_py.read_text(encoding="utf-8")
        assert "def run_app():" in content or "def run_app(" in content
        
        # Compile it to ensure it is valid Python syntax
        import py_compile
        py_compile.compile(str(main_py), doraise=True)
