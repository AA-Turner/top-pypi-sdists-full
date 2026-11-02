"""Tests for _parse_deferral_payload."""

from agentic_devtools.cli.ci.pipeline.deferral import _DEFERRAL_SENTINEL, _parse_deferral_payload


def test_returns_none_for_malformed_terminal_label() -> None:
    body = f'{_DEFERRAL_SENTINEL}{{"review_id":1}} -->\n🤖 AI PR Loop ·'

    assert _parse_deferral_payload(body) is None
