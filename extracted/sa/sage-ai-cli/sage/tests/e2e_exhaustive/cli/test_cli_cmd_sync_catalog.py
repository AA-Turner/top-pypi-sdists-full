"""Exhaustive utility test for cli, command sync-catalog."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_sync_catalog(tmp_path):
    verify_utility_command("cli", "sync-catalog", tmp_path)
