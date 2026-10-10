"""Every AUTOMIND call must log a correlatable request_id (V2 parity).

V2 (auteur-utils UIActions.py) tags every locate/heal line with
`request_id: <id> |` and threads the same id through request -> response ->
resolution, so one failed step reads as one story. The binding had ids on
desktop_locate only; textual_query_v2 / vision_query_v2 / vision_query /
list_xpaths logged just code_export_id, and desktop_locate dropped its id after
the request line.

Guards two things a future edit could quietly undo:
  * each call site still emits a request_id
  * desktop_locate's request and response lines carry the SAME id
"""
import logging
import re
import uuid

import pytest

REQUEST_ID_RE = re.compile(r"request_id=([0-9a-f]{16})")


@pytest.fixture
def heal_logs(caplog):
    caplog.set_level(logging.INFO, logger="testmu_selenium._heal")
    return caplog


def _ids(caplog):
    return REQUEST_ID_RE.findall("\n".join(r.getMessage() % r.args if r.args else r.getMessage()
                                           for r in caplog.records))


def test_request_id_format_is_16_hex():
    """The id shape the log regex (and automind's VQE folder) depends on."""
    assert REQUEST_ID_RE.fullmatch(f"request_id={uuid.uuid4().hex[:16]}")


def test_every_automind_call_site_logs_a_request_id():
    """Static guard: no _heal.py API method may log without a request_id.

    Cheaper and more durable than driving each call — these methods need a live
    driver + network, so a static check is what actually runs in CI.
    """
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[1] / "testmu_selenium" / "_heal.py"
    text = src.read_text()

    # Each of these was previously logging only code_export_id.
    for method in ("list_xpaths", "textual_query_v2", "vision_query_v2",
                   "vision_query(answer)", "desktop_locate", "desktop_locate_full_page"):
        assert f"[heal] {method}: request_id=%s" in text, (
            f"{method} lost its request_id log line — V2 parity regression"
        )


def test_desktop_locate_response_line_reuses_the_request_id():
    """Request and response must quote the SAME id, or correlation is fake."""
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[1] / "testmu_selenium" / "_heal.py"
    text = src.read_text()
    # The response line lives after the request line inside the same method and
    # passes `request_id` as its first arg — a new uuid there would silently
    # break correlation while still matching the regex above.
    assert '"[heal] locate: request_id=%s coord=%s reason=%r confidence=%s",\n            request_id,' in text, (
        "locate response line no longer reuses the request-scoped id"
    )


def test_vision_payloads_still_carry_request_id_on_the_wire():
    """V2 sends request_id to /v1/heal/vision — it keys the automind VQE folder
    ({org_id}/vqe/{request_id}), so dropping it loses the stored artifact link.
    textual_query / xpaths deliberately do NOT send one (V2 does not either)."""
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[1] / "testmu_selenium" / "_heal.py"
    text = src.read_text()
    assert text.count('"request_id": request_id,') == 4, (
        "expected request_id on exactly 4 payloads: desktop_locate, "
        "desktop_locate_full_page, vision_query_v2, vision_query"
    )


# ── resolver visibility (the most common RCA question: what did {{x}} become?) ──

def test_unresolved_variable_warns_instead_of_failing_silently(caplog):
    """var() returns the literal {{x}} when it cannot resolve — that is deliberate
    (V2 does the same), but it used to be SILENT, so 'the step typed {{name}}'
    had no trace in the log at all."""
    from testmu_selenium._vars import var
    with caplog.at_level(logging.WARNING, logger="testmu_selenium"):
        assert var("{{definitely_not_set}}") == "{{definitely_not_set}}"
    assert "UNRESOLVED" in caplog.text
    assert "definitely_not_set" in caplog.text


def test_unresolved_inside_a_larger_string_also_warns(caplog):
    from testmu_selenium._vars import var
    with caplog.at_level(logging.WARNING, logger="testmu_selenium"):
        assert var("hi {{nope_not_here}} there") == "hi {{nope_not_here}} there"
    assert "UNRESOLVED" in caplog.text


def test_set_var_logs_the_stored_value(caplog):
    from testmu_selenium._vars import set_var
    with caplog.at_level(logging.INFO, logger="testmu_selenium"):
        set_var("rca_probe", "some-value")
    assert "set_var rca_probe = 'some-value'" in caplog.text


def test_secret_values_are_masked_in_logs(caplog):
    """A credential must never reach a worker log."""
    from testmu_selenium._vars import set_var
    with caplog.at_level(logging.INFO, logger="testmu_selenium"):
        set_var("secrets.rca_key", "SUPER-SECRET-VALUE")
    assert "SUPER-SECRET-VALUE" not in caplog.text
    assert "***" in caplog.text


def test_resolved_secret_is_redacted_under_an_ordinary_name(caplog, monkeypatch):
    """Masking on the variable NAME is not enough — the value must be tracked.

    set_var("mypassword", var("{{secrets.API_KEY}}")) stores a real credential
    under a name with no secret prefix; a name-only check printed it in full.
    """
    from testmu_selenium._vars import set_var, var
    monkeypatch.setenv("RCA_TEST_KEY", "TOP-SECRET-AAA")
    resolved = var("{{secrets.RCA_TEST_KEY}}")
    with caplog.at_level(logging.INFO, logger="testmu_selenium"):
        set_var("mypassword", resolved)
    assert "TOP-SECRET-AAA" not in caplog.text
    assert "***" in caplog.text


def test_secret_composed_into_a_larger_string_is_redacted(caplog, monkeypatch):
    """Equality is not enough either — secrets get concatenated into headers/URLs."""
    from testmu_selenium._vars import set_var, var
    monkeypatch.setenv("RCA_TEST_KEY2", "TOP-SECRET-BBB")
    resolved = var("{{secrets.RCA_TEST_KEY2}}")
    with caplog.at_level(logging.INFO, logger="testmu_selenium"):
        set_var("auth_header", "Bearer " + resolved)
        set_var("conn", "https://user:" + resolved + "@host/db")
    assert "TOP-SECRET-BBB" not in caplog.text
    assert "Bearer ***" in caplog.text


def test_non_secret_values_stay_visible(caplog):
    """Redaction must not swallow the ordinary values RCA depends on."""
    from testmu_selenium._vars import set_var
    with caplog.at_level(logging.INFO, logger="testmu_selenium"):
        set_var("rca_plain", "just-a-value")
    assert "just-a-value" in caplog.text
