import subprocess
from pathlib import Path

import pyright
import pytest

MYPY_DIR = Path(__file__).parent / "data" / "mypy"

pytestmark = pytest.mark.typechecking


@pytest.mark.parametrize("test_file", MYPY_DIR.glob("*.py"))
def test_pyright(test_file: Path):
    """The mypy examples should pass static type checking with pyright too"""
    res = pyright.run(
        "--outputjson", str(test_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert res.returncode == 0, f"stderr:\n{res.stderr}\n\nstdout:\n{res.stdout}"
