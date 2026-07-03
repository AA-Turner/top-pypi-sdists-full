"""Exhaustive utility test for cli, command whoami."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_whoami(tmp_path):
    verify_utility_command("cli", "whoami", tmp_path)
