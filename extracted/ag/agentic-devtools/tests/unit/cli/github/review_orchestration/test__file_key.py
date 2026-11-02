import pytest

from agentic_devtools.cli.github.review_orchestration import _file_key


def test_normalizes_windows_and_case_aliases():
    assert _file_key(r"SRC\Example.py") == "file:src/example.py"


@pytest.mark.parametrize("path", ["", "/tmp/x", r"C:\src\x", "../x", "src/../x", "./x", "x//y", "x/", " x", "x\x00"])
def test_rejects_ambiguous_reservations(path):
    with pytest.raises(ValueError, match="repository-relative file"):
        _file_key(path)
