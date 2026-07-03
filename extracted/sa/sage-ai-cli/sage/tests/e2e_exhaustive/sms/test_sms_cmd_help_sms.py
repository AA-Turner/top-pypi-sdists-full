"""Exhaustive utility test for sms, command /help."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_sms_cmd_help_sms(tmp_path):
    verify_utility_command("sms", "/help", tmp_path, delivery="sms")
