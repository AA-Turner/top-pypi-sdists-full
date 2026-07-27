"""Exhaustive utility test for sms, command /status."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_sms_cmd_status_sms(tmp_path):
    verify_utility_command("sms", "/status", tmp_path, delivery="sms")
