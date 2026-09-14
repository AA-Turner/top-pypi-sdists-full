"""The package-side door of THE PROVIDER-OUTAGE ALARM.

matrx-ai must stay independent of the host: with nothing configured the seam is
a silent no-op, and the executor's hot-path gate must never do host work while
no outage can be open.
"""

from __future__ import annotations

import pytest

from matrx_ai.ops import provider_outage as seam


@pytest.fixture(autouse=True)
def _reset() -> None:
    seam.reset_outage_watch()


@pytest.mark.asyncio
async def test_no_host_wiring_is_a_silent_no_op(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("matrx_ai._ext.has_ext", lambda name: False)
    await seam.note_provider_failure(provider="anthropic", error_type="billing_error")
    await seam.note_provider_success(provider="anthropic")


@pytest.mark.asyncio
async def test_the_gate_arms_on_an_open_outage_and_disarms_on_recovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    async def _failure(**_: object) -> bool:
        calls.append("failure")
        return True

    async def _success(**_: object) -> bool:
        calls.append("success")
        return False

    monkeypatch.setattr("matrx_ai._ext.has_ext", lambda name: True)
    monkeypatch.setattr(
        "matrx_ai._ext.get_ext",
        lambda name: _failure if name == "provider_outage_failure" else _success,
    )

    await seam.note_provider_failure(provider="anthropic", error_type="billing_error")
    assert seam.outage_watch_active() is True, "an open outage must arm the success check"

    await seam.note_provider_success(provider="anthropic")
    assert calls == ["failure", "success"]
    assert seam.outage_watch_active() is False, "a closed outage must disarm it again"


@pytest.mark.asyncio
async def test_a_restarted_process_rechecks_instead_of_stranding_an_open_row(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Fresh process: nothing known yet, so the very first success asks the host.
    assert seam.outage_watch_active() is True

    async def _success(**_: object) -> bool:
        return False

    monkeypatch.setattr("matrx_ai._ext.has_ext", lambda name: True)
    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: _success)
    await seam.note_provider_success(provider="anthropic")
    assert seam.outage_watch_active() is False

    # …and it re-arms itself once the answer goes stale.
    seam._last_checked -= seam.RECHECK_SECONDS + 1
    assert seam.outage_watch_active() is True


@pytest.mark.asyncio
async def test_a_throwing_host_hook_never_escapes(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _boom(**_: object) -> bool:
        raise RuntimeError("host is mid-restart")

    monkeypatch.setattr("matrx_ai._ext.has_ext", lambda name: True)
    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: _boom)

    await seam.note_provider_failure(provider="anthropic", error_type="billing_error")
    await seam.note_provider_success(provider="anthropic")
