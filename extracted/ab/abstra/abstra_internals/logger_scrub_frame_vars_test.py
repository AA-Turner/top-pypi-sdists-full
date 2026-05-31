"""before_send scrubber must redact a DB DSN password wherever Sentry put it:
the message, the exception value, stack-frame locals (vars), extra, request, and
breadcrumbs — including nested structures."""

from abstra_internals.logger import _scrub_secrets_in_event

SECRET = "sup3rs3cr3t"
DSN = f"postgresql://user:{SECRET}@host:5432/db"


def test_scrubs_dsn_in_stack_frame_vars():
    event = {
        "exception": {
            "values": [
                {
                    "value": "boom",
                    "stacktrace": {"frames": [{"vars": {"uri": DSN, "n": "3"}}]},
                }
            ]
        }
    }
    out = _scrub_secrets_in_event(event, None)
    leaked = out["exception"]["values"][0]["stacktrace"]["frames"][0]["vars"]["uri"]
    assert SECRET not in leaked
    assert "***" in leaked


def test_scrubs_nested_structures_in_vars():
    event = {
        "exception": {
            "values": [{"stacktrace": {"frames": [{"vars": {"cfg": {"db": [DSN]}}}]}}]
        }
    }
    out = _scrub_secrets_in_event(event, None)
    assert SECRET not in str(out)


def test_scrubs_extra_request_and_breadcrumbs():
    event = {
        "extra": {"conn": DSN},
        "request": {"data": {"dsn": DSN}},
        "breadcrumbs": {"values": [{"message": DSN}]},
    }
    out = _scrub_secrets_in_event(event, None)
    assert SECRET not in str(out)


def test_message_and_exception_value_still_scrubbed():
    event = {"message": DSN, "exception": {"values": [{"value": DSN}]}}
    out = _scrub_secrets_in_event(event, None)
    assert SECRET not in out["message"]
    assert SECRET not in out["exception"]["values"][0]["value"]


def test_event_without_secrets_is_untouched():
    event = {"message": "all good", "extra": {"k": "v"}}
    out = _scrub_secrets_in_event(event, None)
    assert out["message"] == "all good"
    assert out["extra"]["k"] == "v"
