"""Exhaustive utility test for cli, command sync."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_sync(tmp_path):
    verify_utility_command("cli", "sync", tmp_path)
