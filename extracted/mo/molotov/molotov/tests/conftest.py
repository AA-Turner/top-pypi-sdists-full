import pytest
import sys
from io import StringIO


@pytest.fixture
def catch_output():
    oldout, olderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = StringIO(), StringIO()
    try:
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout.seek(0)
        sys.stderr.seek(0)
        sys.stdout, sys.stderr = oldout, olderr
