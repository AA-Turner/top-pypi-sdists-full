"""Exhaustive utility test for cli, command rm."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_rm(tmp_path):
    verify_utility_command("cli", "rm", tmp_path)
