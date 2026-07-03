"""Exhaustive utility test for sms, command /clear."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_sms_cmd_clear_kdeconnect(tmp_path):
    verify_utility_command("sms", "/clear", tmp_path, delivery="kdeconnect")
