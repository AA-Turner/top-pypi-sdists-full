import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_11(tmp_path):
    prompt = "Create a simple Makefile for a C program with main.c."
    verify_sms_with_rubric(prompt, tmp_path)
