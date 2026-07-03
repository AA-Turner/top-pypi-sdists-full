"""Exhaustive utility test for cli, command fix-llama-cpp."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_fix_llama_cpp(tmp_path):
    verify_utility_command("cli", "fix-llama-cpp", tmp_path)
