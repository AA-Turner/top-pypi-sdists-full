"""Exhaustive utility test for cli, command use."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_use(tmp_path):
    verify_utility_command("cli", "use", tmp_path)
