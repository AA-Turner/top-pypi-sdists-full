import subprocess
import os
import shutil
import tempfile
from pathlib import Path
from . import TestResult

def execute(request: dict, model: str) -> TestResult:
    prompt = request.get("cli_request", request.get("description", "Perform task"))
    
    workspace = Path(tempfile.mkdtemp(prefix="sage-cli-functional-"))
    test_home = Path(tempfile.mkdtemp(prefix="sage-home-"))
    (test_home / ".sage").mkdir(parents=True, exist_ok=True)
    
    import shlex
    cmd = shlex.split(prompt)
    if "ask" in cmd and "--model" not in cmd:
        cmd.extend(["--model", model, "--agent"])
        
    import sys
    real_home = Path.home().resolve()
    env = os.environ.copy()
    env["SAGE_TESTING"] = "1"
    env["HOME"] = str(test_home)
    playwright_browsers_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if not playwright_browsers_path:
        if sys.platform == "darwin":
            playwright_browsers_path = str(real_home / "Library/Caches/ms-playwright")
        elif sys.platform == "win32":
            playwright_browsers_path = str(real_home / "AppData" / "Local" / "ms-playwright")
        else:
            playwright_browsers_path = str(real_home / ".cache" / "ms-playwright")
    env["PLAYWRIGHT_BROWSERS_PATH"] = playwright_browsers_path
    env["SAGE_API_BASE"] = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
    env["SAGE_DISABLE_RAG"] = "1"
    
    try:
        result = subprocess.run(
            cmd, cwd=workspace, capture_output=True, text=True, env=env, timeout=600
        )
        
        target_ext = request.get("success_criteria", {}).get("extension", "")
        primary_artifact = None
        
        def is_noise(p):
            if p.name in ["prompt_history.json", "message_log.jsonl", "config.json", "CACHEDIR.TAG", "output_history.json", "file_manifest.json", "conversation_memory.json", "session_state.json"]:
                return True
            if ".pytest_cache" in str(p) or "__pycache__" in str(p) or ".git" in str(p) or ".sage" in str(p):
                return True
            if target_ext and target_ext != ".json" and p.suffix == ".json":
                return True
            return False
            
        candidate_files = [f for f in workspace.glob("**/*") if f.is_file() and not is_noise(f)]
        
        if target_ext:
            ext_matches = [f for f in candidate_files if f.suffix == target_ext]
            if ext_matches:
                ext_matches.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                primary_artifact = ext_matches[0]
                
        if not primary_artifact and candidate_files:
            candidate_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            primary_artifact = candidate_files[0]
            
        if not primary_artifact:
            primary_artifact = workspace / "cli_output.log"
            primary_artifact.write_text(result.stdout or result.stderr)

        return TestResult(
            request=request, raw_response=result.stdout,
            artifact_path=primary_artifact, logs=result.stderr, exit_code=result.returncode
        )
    except subprocess.TimeoutExpired:
        return TestResult(request=request, raw_response="", artifact_path=workspace, logs="Timeout expired", exit_code=1)
