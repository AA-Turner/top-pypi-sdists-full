"""Exhaustive utility test for cli, command train."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_train(tmp_path):
    verify_utility_command("cli", "train", tmp_path)
