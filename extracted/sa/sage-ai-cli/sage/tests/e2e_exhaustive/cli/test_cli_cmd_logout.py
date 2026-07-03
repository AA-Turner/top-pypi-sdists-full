"""Exhaustive utility test for cli, command logout."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_logout(tmp_path):
    verify_utility_command("cli", "logout", tmp_path)
