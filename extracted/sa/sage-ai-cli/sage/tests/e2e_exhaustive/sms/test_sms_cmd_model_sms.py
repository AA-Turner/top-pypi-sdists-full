"""Exhaustive utility test for sms, command /model."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_sms_cmd_model_sms(tmp_path):
    verify_utility_command("sms", "/model", tmp_path, delivery="sms")
