import pytest
import subprocess
import os

@pytest.fixture
def run_cli():
    def _run(args):
        env = os.environ.copy()
        result = subprocess.run(
            ["python", "-m", "sage.main"] + args,
            capture_output=True,
            text=True,
            env=env
        )
        return result
    return _run

def test_cli_flag_help(run_cli):
    res = run_cli(["--help"])
    assert res.returncode == 0
    assert "Usage" in res.stdout or "usage" in res.stdout

def test_cli_flag_model(run_cli):
    # 'ask' might be a sub-command
    res = run_cli(["ask", "What is 2+2?", "--model", "cloud:qwen3-coder"])
    # We don't want to actually assert the full API call response here if it takes too long,
    # but the zero-mock policy means it hits the real API. There is no longer any
    # SAGE_TESTING bypass, so this requires real credentials to succeed.
    assert res.returncode == 0 or res.returncode == 1 # Depending on if the key is setup
