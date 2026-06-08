import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_11(tmp_path):
    prompt = "Create a simple Makefile for a C program with main.c."
    verify_cli_with_rubric(prompt, tmp_path)
