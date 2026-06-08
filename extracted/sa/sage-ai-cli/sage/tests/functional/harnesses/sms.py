import subprocess
import os
import time
import uuid
import httpx
import tempfile
import json
from pathlib import Path
from . import TestResult

def execute(request: dict, model: str) -> TestResult:
    prompt = request.get("sms_request", request.get("description", "Perform task"))
    
    workspace = Path(tempfile.mkdtemp(prefix="sage-sms-functional-"))
    test_home = Path(tempfile.mkdtemp(prefix="sage-home-"))
    sage_dir = test_home / ".sage"
    sage_dir.mkdir(parents=True, exist_ok=True)
    
    computer_name = f"test-bot-{uuid.uuid4().hex[:8]}"
    
    sms_config = {
        "computer_name": computer_name,
        "working_dir": str(workspace),
        "model": model,
        "temperature": 0.7,
        "task_timeout": 0,
        "output_mode": "verbose"
    }
    (sage_dir / "sms_config.json").write_text(json.dumps(sms_config, indent=2))
    
    # We assume the local backend is running on 8091 for tests
    backend_url = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
    
    env = os.environ.copy()
    env["SAGE_TESTING"] = "1"
    env["HOME"] = str(test_home)
    env["SAGE_API_BASE"] = backend_url
    env["SAGE_DISABLE_RAG"] = "1"
    
    bridge_proc = subprocess.Popen(
        ["sage", "sms", "start", "--name", computer_name, "--foreground"],
        cwd=workspace, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    
    try:
        time.sleep(15) # Wait for bridge WebSocket to connect
        
        headers = {"Authorization": "Bearer test-token"}
        payload = {
            "text": f"@{computer_name}: {prompt}",
            "from": "tester@example.com",
            "device_type": "apple"
        }
        
        response = httpx.post(f"{backend_url}/sms/webhook", json=payload, headers=headers, timeout=600)
        
        if response.status_code != 200:
            return TestResult(request=request, raw_response=response.text, artifact_path=workspace, logs=f"Webhook failed: {response.status_code}", exit_code=1)
            
        webhook_data = response.json()
        
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
            primary_artifact = workspace / "sms_output.txt"
            primary_artifact.write_text(webhook_data.get("output", ""))

        return TestResult(
            request=request, raw_response=webhook_data.get("output", ""),
            artifact_path=primary_artifact, logs="SMS task completed", exit_code=0
        )
    except Exception as exc:
        return TestResult(request=request, raw_response="", artifact_path=workspace, logs=str(exc), exit_code=1)
    finally:
        bridge_proc.terminate()
        try:
            bridge_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            bridge_proc.kill()
