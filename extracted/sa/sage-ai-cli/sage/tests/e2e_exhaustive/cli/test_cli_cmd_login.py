"""Exhaustive utility test for cli, command login."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_login(tmp_path):
    verify_utility_command("cli", "login", tmp_path)
