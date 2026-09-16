"""A FAILED TURN NEVER PRINTS A DICT INTO THE THREAD.

The defect (independent review, production, 2026-09-15): a failed turn's
visible message body read

    {'error_type': 'message_sanitization_error', 'message': 'This request ends
    with an assistant response and has no new user or tool turn to send...'}

with the honest red notice and its Retry control rendering directly beneath it.
Python's ``str(dict)``, straight into ``cx_message.content`` — duplicate
leakage of what the notice already said, in the ugliest possible form.

Root cause: ``CompletedRequest._structured_error()`` deliberately promotes a
bare error string + error_type into a dict for the STRUCTURED column, and the
reserved-message closer in ``persistence.py`` wrote ``str(...)`` of that same
value into the message CONTENT. The structured branch three lines below it
already special-cased the dict; the text branch never did.

Proven failing before passing: restore ``_err_text = _err_raw or "…"`` and
``str(_err_text)`` in the content block → the sanitization test below prints
the dict repr and goes RED.
"""

from matrx_ai.db.persistence import _build_cx_request_error, human_error_sentence

SANITIZATION_ERROR = {
    "error_type": "message_sanitization_error",
    "message": (
        "This request ends with an assistant response and has no new user or "
        "tool turn to send. Add the next user instruction and try again."
    ),
}


def test_the_exact_live_leak_becomes_a_sentence():
    text = human_error_sentence(SANITIZATION_ERROR, fallback="fallback")
    assert text == SANITIZATION_ERROR["message"]
    assert "error_type" not in text
    assert "{" not in text and "'" not in text


def test_a_plain_string_is_left_alone():
    assert human_error_sentence("Error code: 400 boom", fallback="f") == (
        "Error code: 400 boom"
    )


def test_user_message_wins_over_message():
    payload = {"message": "technical", "user_message": "what a person reads"}
    assert human_error_sentence(payload, fallback="f") == "what a person reads"


def test_a_structure_with_no_human_field_falls_back_rather_than_repr():
    for value in ({"code": 500, "retryable": True}, ["a", "b"], object()):
        text = human_error_sentence(value, fallback="This response failed.")
        assert text == "This response failed."
        assert "{" not in text and "[" not in text


def test_nothing_at_all_still_says_something():
    assert human_error_sentence(None, fallback="This response failed.") == (
        "This response failed."
    )
    assert human_error_sentence("", fallback="This response failed.") == (
        "This response failed."
    )


def test_the_request_error_payload_carries_the_sentence_and_still_finds_codes():
    # The human half is a sentence…
    payload = _build_cx_request_error({"error": SANITIZATION_ERROR})
    assert payload["message"] == SANITIZATION_ERROR["message"]
    assert "error_type" not in payload["message"]

    # …and the provider status code is still parsed out of the raw error,
    # including when the raw error is a dict (it used to be parsed from the
    # stringified message only).
    coded = _build_cx_request_error(
        {"error": {"message": "Error code: 400 - bad request"}}
    )
    assert coded["status_code"] == 400
    coded_str = _build_cx_request_error({"error": "Error code: 429 - slow down"})
    assert coded_str["status_code"] == 429
