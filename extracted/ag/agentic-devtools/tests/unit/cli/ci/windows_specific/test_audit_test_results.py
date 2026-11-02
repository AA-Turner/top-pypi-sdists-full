import subprocess

import pytest

from agentic_devtools.cli.ci.windows_specific import audit_test_results

NODE_ID = "tests/unit/sample/test_example.py::TestExample::test_parameter[space & punctuation!]"
CLASSNAME = "tests.unit.sample.test_example.TestExample"
NAME = "test_parameter[space & punctuation!]"
COLLECTION = f"{NODE_ID}\n1 test collected"
JUNIT = (
    "<testsuite><testcase classname='tests.unit.sample.test_example.TestExample' "
    "name='test_parameter[space &amp; punctuation!]'/></testsuite>"
)


def _audit(
    *,
    collection=COLLECTION,
    execution="1 passed",
    report=JUNIT,
    expected=(NODE_ID,),
    collection_returncode=0,
    execution_returncode=0,
):
    return audit_test_results(
        collection,
        execution,
        report,
        expected,
        collection_returncode=collection_returncode,
        execution_returncode=execution_returncode,
    )


def test_audit_returns_exact_deterministic_result_shape():
    result = _audit()
    assert set(result) == {"ok", "collected_ids", "executed_ids", "skipped"}
    assert result == {
        "ok": True,
        "collected_ids": [NODE_ID],
        "executed_ids": [NODE_ID],
        "skipped": 0,
    }
    assert type(result["ok"]) is bool
    assert type(result["collected_ids"]) is list
    assert type(result["executed_ids"]) is list
    assert type(result["skipped"]) is int
    assert CLASSNAME in JUNIT and "test_parameter[" in JUNIT


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"collection_returncode": 2}, "collect-only"),
        ({"execution_returncode": 3}, "pytest"),
    ],
)
def test_audit_preserves_nonzero_process_details(kwargs, message):
    with pytest.raises(subprocess.CalledProcessError) as error:
        _audit(**kwargs)
    assert error.value.returncode == kwargs.get("collection_returncode", kwargs.get("execution_returncode"))
    assert message in " ".join(error.value.cmd)
    assert error.value.output == (COLLECTION if "collection_returncode" in kwargs else "1 passed")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"collection": "tests/unit/sample/test_example.py::test_other\n1 test collected"},
        {"collection": f"{NODE_ID}\n1 test collected\n", "execution": "1 deselected"},
        {"execution": "1 passed, 1 deselected"},
        {"expected": (NODE_ID, NODE_ID)},
        {"expected": ()},
        {"expected": ("not a node ID",)},
        {"report": "<not xml"},
        {"report": "<testsuite/>"},
        {"report": "<unknown><testcase classname='x' name='y'/></unknown>"},
        {"report": "<testsuites/>"},
        {"report": "<testsuite><testcase name='test'/></testsuite>"},
        {"report": "<testsuite><testcase classname='x'/></testsuite>"},
        {
            "report": "<testsuite><testcase classname='x' name='test'/></testsuite>",
        },
        {
            "report": (
                "<testsuite><testcase classname='tests.unit.sample.test_example.TestExample' "
                "name='test_parameter[space &amp; punctuation!]'/><testcase "
                "classname='tests.unit.sample.test_example.TestExample' "
                "name='test_parameter[space &amp; punctuation!]'/></testsuite>"
            )
        },
        {
            "report": (
                "<testsuite><testcase classname='tests.unit.sample.test_example.TestExample' "
                "name='test_parameter[space &amp; punctuation!]'><skipped/></testcase></testsuite>"
            )
        },
        {
            "report": (
                "<testsuite><testcase classname='tests.unit.sample.test_example.TestExample' "
                "name='test_parameter[space &amp; punctuation!]'><failure/></testcase></testsuite>"
            )
        },
        {
            "report": (
                "<testsuite><testcase classname='tests.unit.sample.test_example.TestExample' "
                "name='test_parameter[space &amp; punctuation!]'><error/></testcase></testsuite>"
            )
        },
    ],
)
def test_audit_rejects_invalid_or_incomplete_evidence(kwargs):
    with pytest.raises(ValueError):
        _audit(**kwargs)


@pytest.mark.parametrize("marker", ["skipped", "failure", "error"])
@pytest.mark.parametrize("container", ["suite", "properties"])
def test_audit_rejects_junit_outcome_markers_outside_testcases(marker, container):
    marker_xml = f"<{marker}/>"
    outside_testcase = marker_xml if container == "suite" else f"<properties>{marker_xml}</properties>"
    report = JUNIT.replace("<testsuite>", f"<testsuite>{outside_testcase}", 1)
    with pytest.raises(ValueError, match="outcome"):
        _audit(report=report)


def test_audit_rejects_testcase_nested_in_properties():
    testcase = JUNIT[len("<testsuite>") : -len("</testsuite>")]
    report = f"<testsuite><properties>{testcase}</properties></testsuite>"
    with pytest.raises(ValueError, match="allowed position"):
        _audit(report=report)


def test_audit_rejects_nested_testcase_alongside_direct_testcase():
    testcase = JUNIT[len("<testsuite>") : -len("</testsuite>")]
    report = f"<testsuite>{testcase}<system-out>{testcase}</system-out></testsuite>"
    with pytest.raises(ValueError, match="allowed position"):
        _audit(report=report)


def test_audit_accepts_testsuites_root_and_bytes_xml():
    report = (
        b"<testsuites><testsuite><properties/><testcase "
        b"classname='tests.unit.sample.test_example.TestExample' "
        b"name='test_parameter[space &amp; punctuation!]'/></testsuite></testsuites>"
    )
    assert _audit(report=report)["executed_ids"] == [NODE_ID]


def test_audit_rejects_missing_junit_identity():
    second = "tests/unit/sample/test_example.py::test_second"
    collection = f"{NODE_ID}\n{second}\n2 tests collected"
    with pytest.raises(ValueError, match="execution IDs"):
        _audit(
            collection=collection,
            expected=(NODE_ID, second),
            report=JUNIT,
        )


def test_audit_rejects_ambiguous_expected_junit_pairs():
    first = "tests/unit/sample.py::TestExample::test_case"
    second = "tests/unit/sample/TestExample.py::test_case"
    collection = f"{first}\n{second}\n2 tests collected"
    with pytest.raises(ValueError, match="ambiguous"):
        _audit(collection=collection, expected=(first, second))


def test_audit_rejects_invalid_input_types():
    with pytest.raises(ValueError, match="Execution output"):
        audit_test_results(COLLECTION, None, JUNIT, (NODE_ID,), collection_returncode=0, execution_returncode=0)
    with pytest.raises(ValueError, match="Expected IDs"):
        audit_test_results(
            COLLECTION, "passed", JUNIT, "not a collection", collection_returncode=0, execution_returncode=0
        )
    with pytest.raises(ValueError, match="JUnit XML"):
        audit_test_results(COLLECTION, "passed", None, (NODE_ID,), collection_returncode=0, execution_returncode=0)
