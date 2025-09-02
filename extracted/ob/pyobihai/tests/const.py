"""PyObihai Test Constants."""

import os

from . import MockResponse

MOCK_LOGIN = ["192.168.1.100", "admin", "admin"]
_RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")
FAILED_REQUEST = MockResponse("", 404)
GENERIC_SUCCESS = MockResponse("", 200)

with open(os.path.join(_RESOURCES_DIR, "line_state.xml"), "r", encoding="utf8") as fd:
    LINE_STATE_XML = MockResponse(fd.read(), 200)

with open(os.path.join(_RESOURCES_DIR, "status.xml"), "r", encoding="utf8") as fd:
    STATUS_XML = MockResponse(fd.read(), 200)

with open(
    os.path.join(_RESOURCES_DIR, "no_active_calls.html"), "r", encoding="utf8"
) as fd:
    NO_ACTIVE_CALLS_HTML = MockResponse(fd.read(), 200)

with open(
    os.path.join(_RESOURCES_DIR, "outbound_call.html"), "r", encoding="utf8"
) as fd:
    OUTBOUND_CALL_HTML = MockResponse(fd.read(), 200)

with open(
    os.path.join(_RESOURCES_DIR, "inbound_call.html"), "r", encoding="utf8"
) as fd:
    INBOUND_CALL_HTML = MockResponse(fd.read(), 200)
