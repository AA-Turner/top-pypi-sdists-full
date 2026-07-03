"""Exhaustive utility test for sms, command /autoorg."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_sms_cmd_autoorg_kdeconnect(tmp_path):
    verify_utility_command("sms", "/autoorg", tmp_path, delivery="kdeconnect")
