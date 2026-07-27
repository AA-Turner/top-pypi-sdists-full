import pytest
import subprocess
import os

@pytest.fixture
def run_cli():
    def _run(args, stdin=""):
        env = os.environ.copy()
        # Run it as a python module from the ai-platform root
        # Assuming pytest is run from ai-platform/
        result = subprocess.run(
            ["python", "-m", "sage.main"] + args,
            input=stdin,
            capture_output=True,
            text=True,
            env=env
        )
        return result
    return _run

def test_cli_slash_models(run_cli):
    """
    Test the /models slash command.
    """
    # Assuming interactive mode reads stdin
    res = run_cli(["run"], stdin="/models\n/exit\n")
    # Verify some output exists
    assert res.returncode == 0
    assert "models" in res.stdout.lower() or "qwen" in res.stdout.lower() or "gemma" in res.stdout.lower()

def test_cli_slash_undo(run_cli):
    """
    Test the /undo slash command.
    """
    res = run_cli(["run"], stdin="/undo\n/exit\n")
    assert res.returncode == 0
    assert "undo" in res.stdout.lower() or "nothing to undo" in res.stdout.lower()

def test_cli_slash_think(run_cli):
    """
    Test the /think slash command.
    """
    res = run_cli(["run"], stdin="/think on\n/exit\n")
    assert res.returncode == 0
    assert "think" in res.stdout.lower()
