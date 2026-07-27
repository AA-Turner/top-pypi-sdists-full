import subprocess
import os
import shutil
import tempfile
from pathlib import Path
from . import TestResult

def execute(request: dict, model: str) -> TestResult:
    prompt = request.get("cli_request", request.get("description", "Perform task"))

    workspace = Path(tempfile.mkdtemp(prefix="sage-cli-functional-"))
    print(f"WORKSPACE: {workspace}", flush=True)
    test_home = Path(tempfile.mkdtemp(prefix="sage-home-"))
    sage_dir = test_home / ".sage"
    sage_dir.mkdir(parents=True, exist_ok=True)

    # The CLI has an auth gate in sage/commands_models.py: every subcommand that
    # is not in _AUTH_EXEMPT ({login, logout, whoami, update}) calls load_auth()
    # and, when it returns None, prints "Login required." and exits 1.
    #
    # This harness deliberately isolates HOME (env["HOME"] below) so a run cannot
    # touch the developer's real ~/.sage. That isolation is correct, but the
    # isolated .sage directory created above started out EMPTY -- so load_auth()
    # returned None and *every* functional CLI test died at the gate, exit code 1,
    # without exercising a single line of the behaviour it claimed to test. The
    # sibling harnesses/sms.py already seeds auth.json into its isolated HOME for
    # exactly this reason (see its "mock auth token" block); cli.py just never did.
    #
    # The credential is COPIED from the developer's real ~/.sage/auth.json rather
    # than synthesised. A fake token is not good enough here and not allowed here:
    #   * not good enough -- clearing the CLI's local gate only moves the failure
    #     one hop. The backend verifies id_token as a Firebase JWT, so a
    #     placeholder yields "401 Invalid or expired auth token: Wrong number of
    #     segments in token" and the test still never reaches real behaviour.
    #   * not allowed -- functional/conftest.py installs enforce_zero_mock_policy
    #     and this suite's whole contract is "real cloud APIs, zero mocks". A
    #     stubbed identity would violate the contract the directory exists to
    #     enforce.
    # When no credential exists the test SKIPS loudly and names the prerequisite,
    # instead of reporting a red failure that looks like a product defect.
    real_auth = Path.home().resolve() / ".sage" / "auth.json"
    if not real_auth.is_file():
        import pytest
        pytest.skip(
            "MISSING PREREQUISITE: sage/tests/functional drives the real `sage` "
            "CLI against the real cloud backend, which requires a logged-in "
            f"account. No credential found at {real_auth}.\n"
            "  To enable this suite run:  sage login\n"
            "  (Sign up first at https://sageworksai.com if you have no account.)"
        )
    shutil.copyfile(real_auth, sage_dir / "auth.json")
    (sage_dir / "auth.json").chmod(0o600)

    # The sage package must be installed in the environment running the tests
    if "ask" not in prompt:
        # Wrap the whole prompt in quotes so it's a single argument for the PROMPT parameter
        full_cmd = ["sage", "ask", prompt, "--model", model]
    else:
        import shlex
        cmd = shlex.split(prompt)
        if "ask" in cmd and "--model" not in cmd:
            cmd.extend(["--model", model, "--agent"])
        if cmd[0] == "sage":
            full_cmd = cmd
        else:
            full_cmd = ["sage", *cmd]

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
    env["SAGE_API_BASE"] = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
    env["SAGE_DISABLE_RAG"] = "1"

    try:
        out_f = open(workspace / "stdout.log", "w")
        err_f = open(workspace / "stderr.log", "w")
        result = subprocess.run(
            full_cmd, cwd=workspace, stdout=out_f, stderr=err_f, text=True, env=env, timeout=1800
        )
        out_f.close()
        err_f.close()
        result.stdout = (workspace / "stdout.log").read_text()
        result.stderr = (workspace / "stderr.log").read_text()

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
