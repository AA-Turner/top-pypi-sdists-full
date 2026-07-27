"""Exhaustive utility test for sms, command /exit."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_sms_cmd_exit_imessage(tmp_path):
    verify_utility_command("sms", "/exit", tmp_path, delivery="imessage")
