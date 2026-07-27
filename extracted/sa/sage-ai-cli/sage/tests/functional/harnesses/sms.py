import subprocess
import os
import time
import uuid
import httpx
import tempfile
import json
import sqlite3
import sys
from pathlib import Path
from . import TestResult
from sage.core.sms_bridge import SMS_PID_FILE

def get_latest_imessage(computer_name: str) -> str:
    """Poll chat.db for the latest OUTBOUND message containing our computer name."""
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    if not os.path.exists(db_path):
        return ""

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()

        # Look for messages containing our specific test bot name
        # Outbound messages from the Mac will be is_from_me = 1
        query = """
            SELECT text, attributedBody
            FROM message
            WHERE is_from_me = 1
            ORDER BY date DESC
            LIMIT 10
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            text, attr_body = row[0], row[1]
            if not text and attr_body:
                # Basic extraction for tests
                try:
                    s = "".join([chr(b) for b in attr_body if 32 <= b <= 126 or b in (10, 13)])
                    import re
                    match = re.search(r'^[^a-zA-Z0-9@/]*(.*?)(?:iI|i_|NSDictionary)', s)
                    if match:
                        text = match.group(1).strip()
                    else:
                        text = s.strip()
                except Exception:
                    continue

            if text and computer_name in text:
                return text
    except Exception:
        pass

    return ""

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

    # Write a mock auth token so the bridge authenticates as test-uid, matching the webhook
    mock_auth = {
        "uid": "test-uid",
        "email": "test@example.com",
        "id_token": "test-token",
        "refresh_token": "test-refresh",
        "expires_at": time.time() + 3600,
        "tier": "pro"
    }
    (sage_dir / "auth.json").write_text(json.dumps(mock_auth))

    backend_url = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")

    import sys
    real_home = Path.home().resolve()
    env = os.environ.copy()
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
    env["SAGE_API_BASE"] = backend_url
    env["SAGE_DISABLE_RAG"] = "1"

    # Ensure subprocess can import the 'sage' package
    ai_platform_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
    env["PYTHONPATH"] = str(ai_platform_dir)

    # Open a file to capture bridge output
    bridge_log = workspace / "bridge.log"
    bridge_log_fd = open(bridge_log, "w")
    bridge_proc = subprocess.Popen(
        ["sage", "sms", "start", "--name", computer_name, "--foreground", "--no-announce"],
        cwd=workspace, env=env, stdout=bridge_log_fd, stderr=subprocess.STDOUT, text=True
    )

    test_email = "laynefaler@gmail.com"

    try:
        # Wait for bridge to fully connect and start polling
        time.sleep(15)

        # Trigger the task via the webhook to simulate an inbound message from laynefaler@gmail.com
        headers = {"Authorization": "Bearer test-token"}
        payload = {
            "text": f"@{computer_name}: {prompt}",
            "from": test_email,
            "device_type": "apple"
        }

        # The webhook should dispatch it to the CLI.
        response = httpx.post(f"{backend_url}/sms/webhook", json=payload, headers=headers, timeout=600)

        if response.status_code != 200:
            return TestResult(request=request, raw_response=response.text, artifact_path=workspace, logs=f"Webhook failed: {response.status_code}", exit_code=1)

        data = response.json()
        output = data.get("output", "")

        target_ext = request.get("success_criteria", {}).get("extension", "")
        primary_artifact = None

        def is_noise(p):
            if p.name in ["prompt_history.json", "message_log.jsonl", "config.json", "CACHEDIR.TAG", "output_history.json", "file_manifest.json", "conversation_memory.json", "session_state.json", "bridge.log"]:
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
            primary_artifact.write_text(str(output))

        output_str = str(output).lower()
        has_error_flag = "❌ error:" in output_str or "sage backend error" in output_str or "failed to execute" in output_str
        exit_code = 1 if has_error_flag else 0

        return TestResult(
            request=request, raw_response=str(output),
            artifact_path=primary_artifact, logs="SMS task completed", exit_code=exit_code
        )
    except Exception as exc:
        return TestResult(request=request, raw_response="", artifact_path=workspace, logs=str(exc), exit_code=1)
    finally:
        bridge_proc.terminate()
        try:
            bridge_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            bridge_proc.kill()
