import pytest

from agentic_devtools.cli.ci.windows_specific import _parse_collection_output


@pytest.mark.parametrize(
    ("output", "expected"),
    [
        ("tests/unit/a.py::test_one\n1 test collected", ("tests/unit/a.py::test_one",)),
        (
            " tests/unit/a.py::test_one \ntests/unit/a.py::test_two\n2 tests collected in 0.12s",
            ("tests/unit/a.py::test_one", "tests/unit/a.py::test_two"),
        ),
        ("tests/unit/a.py::test_one\n1 item collected", ("tests/unit/a.py::test_one",)),
        (
            "tests/unit/a.py::test_one\ntests/unit/a.py::test_two\n2 items collected",
            ("tests/unit/a.py::test_one", "tests/unit/a.py::test_two"),
        ),
        ("tests/unit/a.py::test_one[a value!]\n1 test collected", ("tests/unit/a.py::test_one[a value!]",)),
    ],
)
def test_parse_valid_collection_output(output, expected):
    assert _parse_collection_output(output) == expected


@pytest.mark.parametrize(
    "output",
    [
        "",
        "0 tests collected",
        "tests/unit/a.py::test_one\n0 tests collected",
        "tests/unit/a.py::test_one\n2 tests collected",
        "tests/unit/a.py::test_one\n1 tests collected",
        "tests/unit/a.py::test_one\n2 test collected",
        "tests/unit/a.py::test_one\n1 test collected, 1 deselected",
        "tests/unit/a.py::test_one\n1 test collected with 1 error",
        "tests/unit/a.py::test_one\nwarning: plugin warning\n1 test collected",
        "tests/unit/a.py::test_one\ntests/unit/a.py::test_one\n2 tests collected",
        "tests/unit/a.py::test_one\n1 passed",
        "not a node ID\n1 test collected",
        "tests/unit/a.py::test_one\n",
    ],
)
def test_parse_invalid_collection_output(output):
    with pytest.raises(ValueError):
        _parse_collection_output(output)


def test_parse_rejects_non_text_output():
    with pytest.raises(ValueError):
        _parse_collection_output(None)
