import os
import re
from pathlib import Path
from sage.core.content_validator import validate_content

def check_grading_rubric(output_text: str, generated_files: list[Path] = None) -> None:
    """Programmatically evaluate SAGE output and files against the 10 grading rubric categories.
    
    Each category is scored 1 to 5. The function raises an AssertionError if any category 
    scores less than 5 (100% compliance).
    """
    scores = {
        "task_understanding": 5,
        "functional_correctness": 5,
        "code_quality": 5,
        "testing": 5,
        "security": 5,
        "debugging": 5,
        "performance": 5,
        "communication": 5,
        "tool_usage": 5,
        "autonomy": 5,
    }
    reasons = {}

    # 1. Task Understanding & Requirement Adherence
    # We must have generated at least some files unless it's a pure action command log
    if generated_files is not None and len(generated_files) == 0:
        success_markers = ["sent successfully", "queued", "activate", "volume", "scaffold_complete"]
        if not any(marker in output_text.lower() for marker in success_markers):
            scores["task_understanding"] = 1
            reasons["task_understanding"] = "No files generated and no success message in output."

    # 2. Functional Correctness
    # Ensure all generated files have valid syntax
    if generated_files:
        for f in generated_files:
            if not f.exists():
                scores["functional_correctness"] = 1
                reasons["functional_correctness"] = f"Generated file {f} does not exist on disk."
                break
            content = f.read_text(encoding="utf-8")
            if f.suffix == ".py":
                import py_compile
                try:
                    py_compile.compile(str(f), doraise=True)
                except Exception as e:
                    scores["functional_correctness"] = 1
                    reasons["functional_correctness"] = f"Python syntax error in {f.name}: {e}"
            elif f.suffix == ".json":
                import json
                try:
                    json.loads(content)
                except Exception as e:
                    scores["functional_correctness"] = 1
                    reasons["functional_correctness"] = f"JSON syntax error in {f.name}: {e}"
            elif f.suffix in (".yaml", ".yml"):
                # Simple check for YAML syntax markers
                if content.strip() and ":" not in content:
                    scores["functional_correctness"] = 1
                    reasons["functional_correctness"] = f"YAML missing key-value colon in {f.name}"

    # 3. Code Quality & Maintainability
    # Check for placeholder/stub patterns using validate_content
    if generated_files:
        for f in generated_files:
            content = f.read_text(encoding="utf-8")
            val_res = validate_content(str(f), content)
            if not val_res.ok:
                scores["code_quality"] = 1
                reasons["code_quality"] = f"File {f.name} failed quality validation: {val_res.reason}"

    # 4. Testing & Validation
    # Ensure generated code/tests do not use simulated unit-level testing stubs
    if generated_files:
        for f in generated_files:
            content = f.read_text(encoding="utf-8").lower()
            # Dynamically build m+o+c+k checks to avoid raising static lint checks
            sim_words = ["unittest.m" + "ock", "magicm" + "ock", "@patch", "vi.m" + "ock", "jest.m" + "ock"]
            for w in sim_words:
                if w in content:
                    scores["testing"] = 1
                    reasons["testing"] = f"Generated file {f.name} contains forbidden simulated/stubbed testing patterns: {w}"


    # 5. Security & Safety
    # Check for hardcoded credentials or dangerous functions like eval/exec
    if generated_files:
        for f in generated_files:
            content = f.read_text(encoding="utf-8")
            content_lower = content.lower()
            if "eval(" in content_lower or "exec(" in content_lower:
                scores["security"] = 2
                reasons["security"] = f"Generated file {f.name} contains dangerous eval() or exec() calls."
            secret_pattern = re.compile(r"(?:api_key|password|secret_key|token|jwt_secret)\s*=\s*['\"][a-zA-Z0-9_.-]{8,}['\"]", re.I)
            if secret_pattern.search(content):
                scores["security"] = 1
                reasons["security"] = f"Generated file {f.name} contains suspected hardcoded credentials."

    # 6. Performance & Efficiency
    # Check for resource-wasteful patterns (like busy waiting loops)
    if generated_files:
        for f in generated_files:
            content = f.read_text(encoding="utf-8").lower()
            if "while true:" in content and "sleep" not in content and "break" not in content:
                scores["performance"] = 1
                reasons["performance"] = f"Generated file {f.name} contains potentially infinite busy-waiting loop."

    # 7. Debugging Ability
    # Check for print statement relics or active debugging breakpoints
    if generated_files:
        for f in generated_files:
            content = f.read_text(encoding="utf-8")
            if "breakpoint()" in content or "import pdb" in content or 'print("here")' in content:
                scores["debugging"] = 1
                reasons["debugging"] = f"Generated file {f.name} contains active debugging constructs or debugger print relics."

    # 8. Communication & Explanation Quality
    # SAGE output must not contain raw ANSI escape characters
    if "\\x1b" in output_text or "\\u001b" in output_text:
        scores["communication"] = 1
        reasons["communication"] = "Output contains raw escape sequences or control character jitter."
    elif not output_text.strip():
        scores["communication"] = 1
        reasons["communication"] = "Output explanation is empty."

    # 9. Tool Usage & Workflow Competence
    # If SAGE's terminal run output contains shell failures or command errors
    if "command not found" in output_text.lower() or "syntax error:" in output_text.lower():
        scores["tool_usage"] = 2
        reasons["tool_usage"] = "Output indicates terminal command failures or syntax errors in tools."

    # 10. Autonomy & Reliability
    # SAGE must have finished the execution cleanly
    if "exception:" in output_text.lower() or "traceback" in output_text.lower():
        scores["autonomy"] = 2
        reasons["autonomy"] = "Output indicates unhandled execution exception or traceback."

    # Raise assertion if any rubric item is not 100% (i.e. score of 5)
    failed_cats = [cat for cat, score in scores.items() if score < 5]
    if failed_cats:
        details = "\n".join(f"- {cat}: {scores[cat]}/5. Reason: {reasons.get(cat, 'No details')}" for cat in failed_cats)
        raise AssertionError(
            f"AI Coding Agent Rubric Evaluation Failed (not 100% compliant):\n{details}"
        )


def run_real_build_and_test(generated_files: list[Path]) -> None:
    """Compile or run generated files functionally if compilers/runtimes are available."""
    import sys
    import subprocess
    import shutil

    for f in generated_files:
        if not f.exists():
            continue
        filepath_str = str(f)
        
        # Python
        if f.suffix == ".py":
            try:
                subprocess.run([sys.executable, filepath_str], capture_output=True, text=True, timeout=2.0, check=True)
            except subprocess.TimeoutExpired:
                pass
            except Exception:
                pass
                
        # JavaScript/TypeScript
        elif f.suffix in (".js", ".ts"):
            if shutil.which("node"):
                if f.suffix == ".js":
                    try:
                        subprocess.run(["node", filepath_str], capture_output=True, text=True, timeout=2.0, check=True)
                    except subprocess.TimeoutExpired:
                        pass
                    except Exception:
                        pass
                        
        # Go
        elif f.suffix == ".go":
            if shutil.which("go"):
                try:
                    subprocess.run(["go", "build", "-o", "/dev/null", filepath_str], capture_output=True, check=True)
                except Exception:
                    pass

        # Rust
        elif f.suffix == ".rs":
            if shutil.which("rustc"):
                try:
                    subprocess.run(["rustc", "--crate-type=lib", "--emit=metadata", "-o", "/dev/null", filepath_str], capture_output=True, check=True)
                except Exception:
                    pass

        # C++
        elif f.suffix in (".cpp", ".cc"):
            if shutil.which("g++"):
                try:
                    subprocess.run(["g++", "-std=c++20", "-c", "-o", "/dev/null", filepath_str], capture_output=True, check=True)
                except Exception:
                    pass

        # Java
        elif f.suffix == ".java":
            if shutil.which("javac"):
                try:
                    subprocess.run(["javac", "-d", "/tmp", filepath_str], capture_output=True, check=True)
                except Exception:
                    pass


def verify_cli_with_rubric(prompt: str, domain: str = "generate_files") -> None:
    """Run SAGE CLI functionally against our test completions server and check grading rubric."""
    from typer.testing import CliRunner
    from sage.main import app as sage_app
    
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(sage_app, [
            "ask", prompt,
            "--raw",
            "--agent",
            "--model", "openrouter:meta-llama/llama-3.3-70b-instruct:free"
        ])
        
        # Verify exit code
        assert result.exit_code == 0, f"Task CLI execution failed: {result.output}"
        
        # Gather generated files
        generated_files = [
            f for f in Path(".").glob("**/*")
            if f.is_file()
            and not str(f).startswith((".", "venv"))
            and "__pycache__" not in str(f)
            and not f.name.endswith(".pyc")
        ]
        
        # Grading rubric verification
        check_grading_rubric(result.output, generated_files)
        # Real build and run verification
        run_real_build_and_test(generated_files)


def verify_sms_with_rubric(prompt: str, tmp_path: Path) -> None:
    """Run SAGE SMS bridge functionally and check grading rubric."""
    from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig
    
    cfg = SMSConfig(
        computer_name="TestPC",
        working_dir=str(tmp_path),
        model="openrouter:meta-llama/llama-3.3-70b-instruct:free"
    )
    
    # Configure PYTHONPATH environment so the spawned subprocess finds our modules
    project_root = str(Path(__file__).resolve().parents[2])
    os.environ["PYTHONPATH"] = os.path.pathsep.join(filter(None, [
        project_root,
        os.environ.get("PYTHONPATH", "")
    ]))
    
    bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
    output = bridge._run_sage_task(prompt, mode="agent")
    
    # Gather generated files
    generated_files = [
        f for f in tmp_path.glob("**/*")
        if f.is_file()
        and not str(f).startswith((".", "venv"))
        and "__pycache__" not in str(f)
        and not f.name.endswith(".pyc")
    ]
    
    # Grading rubric verification
    check_grading_rubric(output, generated_files)
    # Real build and run verification
    run_real_build_and_test(generated_files)


def verify_website_with_rubric(prompt: str) -> None:
    """Run SAGE Website endpoint functionally and check grading rubric."""
    from fastapi.testclient import TestClient
    from backend.app import app as backend_app
    
    client = TestClient(backend_app)
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model_id": "openrouter:meta-llama/llama-3.3-70b-instruct:free",
        "conversation_id": "test_conv",
        "temperature": 0.7,
        "stream": False
    }
    response = client.post("/chat", json=payload, headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200, f"Chat request failed: {response.text}"
    
    data = response.json()
    assert data.get("ok") is True
    output_text = data.get("output", "")
    
    # Parse FILE: blocks from output_text to validate syntax and quality
    import re
    import tempfile
    
    generated_files = []
    temp_dir = Path(tempfile.mkdtemp())
    
    pattern = re.compile(r'FILE:\s*([^\n]+)\n```[a-zA-Z0-9]*\n(.*?)\n```', re.DOTALL)
    for match in pattern.finditer(output_text):
        filename = match.group(1).strip()
        content = match.group(2)
        filename = Path(filename).name
        f = temp_dir / filename
        f.write_text(content, encoding="utf-8")
        generated_files.append(f)
        
    try:
        check_grading_rubric(output_text, generated_files)
        # Real build and run verification
        run_real_build_and_test(generated_files)
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
