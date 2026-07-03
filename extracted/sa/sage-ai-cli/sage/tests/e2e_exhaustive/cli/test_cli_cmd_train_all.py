"""Exhaustive utility test for cli, command train-all."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_cli_cmd_train_all(tmp_path):
    verify_utility_command("cli", "train-all", tmp_path)
