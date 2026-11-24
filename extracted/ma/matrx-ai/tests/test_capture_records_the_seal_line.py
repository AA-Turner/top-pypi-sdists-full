"""The Model view draws the static seal line where the real send puts it: a capture keeps the
send's own seal stamp (prompt blocks P0.5)."""

from __future__ import annotations

import pytest

from matrx_ai.providers import final_outbound_snapshot as fos
from matrx_ai.providers.request_capture import (
    ProviderRequestCaptured,
    capture_wire_request,
    capturing_provider_request,
)


@pytest.fixture(autouse=True)
def _seal_check_switched_on(monkeypatch):
    """These tests prove the check itself; production starts it off (knob seal_check_on = 0)."""
    from matrx_ai.providers import final_outbound_snapshot as _fos

    monkeypatch.setattr(_fos, "seal_check_on", lambda: True)



def test_a_capture_keeps_the_seal_stamp_of_its_send() -> None:
    fos.reset_for_tests()
    stamp = fos.SealStamp(fos.SHAPE_ANTHROPIC, 3, 1, position=2)
    with capturing_provider_request() as slot:
        fos.stamp_seal(stamp)
        try:
            capture_wire_request(method="post", url="https://api.anthropic.com/v1/messages", headers={}, body=b"{}")
        except ProviderRequestCaptured:
            pass
    assert slot.seal == stamp
    fos.reset_for_tests()


def test_a_capture_with_no_line_says_none() -> None:
    fos.reset_for_tests()
    with capturing_provider_request() as slot:
        try:
            capture_wire_request(method="post", url="https://api.anthropic.com/v1/messages", headers={}, body=b"{}")
        except ProviderRequestCaptured:
            pass
    assert slot.seal is None
