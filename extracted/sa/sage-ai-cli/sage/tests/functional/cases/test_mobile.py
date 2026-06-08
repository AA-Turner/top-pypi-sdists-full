import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from sage.tests.functional.harnesses import run_test

def test_mobile(test_case):
    result = run_test(
        channel=test_case["channel"],
        request=test_case["request"],
        model=test_case["model"]
    )
