import pytest

from agentic_devtools.cli.ci.windows_specific import evaluate_gate


def _selection(groups=(), contract=False, windows=None, bootstrap=False):
    return {
        "ok": True,
        "product_groups": list(groups),
        "contract_required": contract,
        "windows_required": bool(groups) if windows is None else windows,
        "bootstrap_allowed": bootstrap,
    }


@pytest.mark.parametrize(
    ("selection", "linux", "windows", "expected"),
    [
        (_selection(), None, None, {"ok": True, "classification": "not-applicable"}),
        (_selection(), "skipped", "skipped", {"ok": True, "classification": "not-applicable"}),
        (_selection(contract=True), "success", None, {"ok": True, "classification": "not-applicable"}),
        (_selection(contract=True), "success", "skipped", {"ok": True, "classification": "not-applicable"}),
        (
            _selection(("setup-check",)),
            "success",
            "success",
            {"ok": True, "classification": "native-evidence"},
        ),
        (
            _selection(("benchmark",)),
            None,
            "success",
            {"ok": True, "classification": "native-evidence"},
        ),
        (
            _selection(("portability",)),
            "skipped",
            "success",
            {"ok": True, "classification": "native-evidence"},
        ),
        (_selection(contract=True), None, None, {"ok": False, "error_code": "required_evidence_missing"}),
        (_selection(contract=True), "skipped", None, {"ok": False, "error_code": "required_evidence_missing"}),
        (
            _selection(("setup-check",)),
            "success",
            None,
            {"ok": False, "error_code": "required_evidence_missing"},
        ),
        (
            _selection(("setup-check",), contract=True),
            None,
            "success",
            {"ok": False, "error_code": "required_evidence_missing"},
        ),
        (_selection(), "failure", "success", {"ok": False, "error_code": "required_evidence_missing"}),
        (_selection(), "success", "cancelled", {"ok": False, "error_code": "required_evidence_missing"}),
        (_selection(), "success", "failure", {"ok": False, "error_code": "required_evidence_missing"}),
        (_selection(), "cancelled", None, {"ok": False, "error_code": "required_evidence_missing"}),
    ],
)
def test_gate_truth_table(selection, linux, windows, expected):
    result = evaluate_gate(selection, linux, windows)
    assert result == expected
    assert set(result) == ({"ok", "classification"} if expected["ok"] else {"ok", "error_code"})
    assert type(result["ok"]) is bool
    if expected["ok"]:
        assert type(result["classification"]) is str
    else:
        assert type(result["error_code"]) is str


def test_gate_preserves_selection_error_code():
    selection = {"ok": False, "error_code": "no_product_groups"}
    assert evaluate_gate(selection, None, None) == {"ok": False, "error_code": "no_product_groups"}


@pytest.mark.parametrize(
    "selection",
    [
        None,
        {},
        {"ok": False},
        {"ok": False, "error_code": ""},
        {"ok": False, "error_code": "bad", "extra": True},
        {
            "ok": 1,
            "product_groups": [],
            "contract_required": False,
            "windows_required": False,
            "bootstrap_allowed": False,
        },
        {**_selection(), "extra": True},
        {key: value for key, value in _selection().items() if key != "windows_required"},
        {**_selection(), "product_groups": "setup-check"},
        {**_selection(), "product_groups": ["unknown"]},
        {**_selection(), "product_groups": ["setup-check", "setup-check"], "windows_required": True},
        {**_selection(), "contract_required": 1},
        {**_selection(), "windows_required": 1},
        {**_selection(), "bootstrap_allowed": 1},
        {**_selection(("setup-check",)), "windows_required": False},
        {**_selection(), "windows_required": True},
        _selection(("setup-check",), bootstrap=True),
    ],
)
def test_gate_rejects_malformed_selections(selection):
    assert evaluate_gate(selection, "success", "success") == {"ok": False, "error_code": "selection_failed"}


@pytest.mark.parametrize("result", ["unknown", 1, False, []])
def test_gate_rejects_unknown_job_results(result):
    assert evaluate_gate(_selection(), result, None) == {"ok": False, "error_code": "selection_failed"}
