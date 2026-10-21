"""Step machine for identifier-first sign-ins: synthetic screens, no browser, no vault.

Proves: two-screen flow completes; TOTP is typed only on a TOTP screen; unknown/selfie/CAPTCHA
screens stop with a named reason + exact instruction and nothing typed; a repeated screen is
never re-filled; the machine resumes from whatever screen is current; no value ever appears.
"""

from __future__ import annotations

import pytest

from matrx_scraper.ai_browser.login.step_machine import (
    Screen,
    ScreenKind,
    ScreenProbe,
    classify_screen,
    run_step_machine,
)

G = "https://accounts.google.com"


def probe(url: str, **kw) -> ScreenProbe:
    return ScreenProbe(url=url, **kw)


IDENT = probe(f"{G}/v3/signin/identifier", any_input_count=1, identifier_selector="input[name='identifier']:visible", next_selector="#identifierNext button:visible")
PASSW = probe(f"{G}/v3/signin/challenge/pwd", password_count=1, any_input_count=1, next_selector="#passwordNext button:visible")
TOTP = probe(f"{G}/v3/signin/challenge/totp", otp_count=1, any_input_count=1, otp_selector="input[name='totpPin']:visible")
HOME = probe("https://myaccount.google.com/", any_input_count=0)
SELFIE = probe(f"{G}/v3/signin/challenge/selfie", any_input_count=0)
ODD = probe(f"{G}/v3/signin/weird", any_input_count=2)
CAPTCHA = probe(f"{G}/v3/signin/identifier", captcha_count=1, any_input_count=1, identifier_selector="input[name='identifier']:visible")


class FakeDriver:
    """Plays a script of screens; each fill advances to the next one."""

    def __init__(self, screens: list[ScreenProbe], *, totp: bool = True, stuck: bool = False):
        self.screens = screens
        self.i = 0
        self.totp = totp
        self.stuck = stuck
        self.log: list[str] = []

    async def observe(self) -> Screen:
        return classify_screen(self.screens[self.i])

    def _advance(self) -> None:
        if not self.stuck and self.i < len(self.screens) - 1:
            self.i += 1

    async def fill_identifier(self, screen):
        self.log.append("identifier")
        self._advance()

    async def fill_password(self, screen):
        self.log.append("password")
        self._advance()

    async def fill_totp(self, screen):
        if not self.totp:
            return False
        self.log.append("totp")
        self._advance()
        return True

    async def settle(self):
        pass


def test_classify_each_screen():
    assert classify_screen(IDENT).kind is ScreenKind.IDENTIFIER
    assert classify_screen(PASSW).kind is ScreenKind.PASSWORD
    assert classify_screen(TOTP).kind is ScreenKind.TOTP
    assert classify_screen(HOME).kind is ScreenKind.NO_FORM
    s = classify_screen(SELFIE)
    assert (s.kind, s.gate) == (ScreenKind.HUMAN_GATE, "selfie_check")
    assert classify_screen(ODD).gate == "unrecognized_screen"
    assert classify_screen(CAPTCHA).kind is ScreenKind.CAPTCHA  # beats the identifier form


@pytest.mark.asyncio
async def test_two_screen_flow_completes():
    d = FakeDriver([IDENT, PASSW, HOME])
    out = await run_step_machine(d)
    assert out.status == "ready_to_verify"
    assert d.log == ["identifier", "password"]
    assert out.trail == ["identifier", "password"]


@pytest.mark.asyncio
async def test_three_screen_flow_with_totp():
    d = FakeDriver([IDENT, PASSW, TOTP, HOME])
    out = await run_step_machine(d)
    assert out.status == "ready_to_verify" and d.log == ["identifier", "password", "totp"]


@pytest.mark.asyncio
async def test_totp_without_authenticator_hands_off_by_name():
    d = FakeDriver([IDENT, PASSW, TOTP, HOME], totp=False)
    out = await run_step_machine(d)
    assert out.status == "needs_person" and out.reason == "human_gate:totp_unavailable"
    assert out.instruction and out.resume


@pytest.mark.asyncio
async def test_selfie_gate_stops_before_typing_and_resumes():
    d = FakeDriver([IDENT, PASSW, SELFIE, HOME])
    out = await run_step_machine(d)
    assert out.status == "needs_person" and out.reason == "human_gate:selfie_check"
    assert "selfie" in out.instruction and d.log == ["identifier", "password"]
    # a person clears the gate; calling again re-reads the CURRENT screen and finishes
    d.i = 3
    again = await run_step_machine(d)
    assert again.status == "ready_to_verify" and d.log == ["identifier", "password"]


@pytest.mark.asyncio
async def test_captcha_on_first_screen_types_nothing():
    d = FakeDriver([CAPTCHA, PASSW])
    out = await run_step_machine(d)
    assert out.status == "needs_person" and out.reason == "human_gate:captcha" and d.log == []


@pytest.mark.asyncio
async def test_unknown_screen_is_named_refusal_nothing_typed():
    d = FakeDriver([ODD])
    out = await run_step_machine(d)
    assert out.reason == "human_gate:unrecognized_screen" and d.log == []


@pytest.mark.asyncio
async def test_screen_that_does_not_advance_is_refused_not_retyped():
    d = FakeDriver([IDENT, PASSW], stuck=True)
    out = await run_step_machine(d)
    assert out.status == "refused" and out.reason == "identifier_step_did_not_advance"
    assert d.log == ["identifier"]


@pytest.mark.asyncio
async def test_password_screen_returning_is_never_retyped():
    PASSW_AGAIN = PASSW
    d = FakeDriver([PASSW, PASSW_AGAIN])
    out = await run_step_machine(d)
    assert out.status == "refused" and out.reason == "password_not_accepted"
    assert d.log == ["password"]


@pytest.mark.asyncio
async def test_no_value_in_outcome():
    d = FakeDriver([IDENT, PASSW, SELFIE])
    out = await run_step_machine(d)
    assert "hunter2" not in repr(out)


# ---- backup codes -------------------------------------------------------------------
DP = probe(f"{G}/v3/signin/challenge/dp", any_input_count=0)
SELECTION = probe(f"{G}/v3/signin/challenge/selection", any_input_count=0)
BC = probe(f"{G}/v3/signin/challenge/bc", otp_count=1, any_input_count=1, otp_selector="input[name='Pin']:visible")


class BackupDriver(FakeDriver):
    def __init__(self, screens, *, codes: int = 1, option: bool = True, totp: bool = True):
        super().__init__(screens, totp=totp)
        self.codes = codes
        self.option = option

    async def has_backup_codes(self):
        return True

    async def has_totp(self):
        return self.totp

    async def choose_backup_codes(self, screen):
        self.log.append("route")
        if not self.option:
            return False
        self._advance()
        return True

    async def fill_backup_code(self, screen):
        if self.codes <= 0:
            return False
        self.codes -= 1
        self.log.append("backup_code")
        self._advance()
        return True


def test_bc_url_with_one_input_is_a_backup_code_screen():
    assert classify_screen(BC).kind is ScreenKind.BACKUP_CODE


@pytest.mark.asyncio
async def test_device_prompt_routes_to_backup_code_and_types_exactly_one():
    d = BackupDriver([IDENT, PASSW, DP, BC, HOME])
    out = await run_step_machine(d)
    assert out.status == "ready_to_verify", out
    assert d.log == ["identifier", "password", "route", "backup_code"]
    assert out.trail == ["identifier", "password", "backup_route", "backup_code"]


@pytest.mark.asyncio
async def test_without_backup_capability_device_prompt_still_hands_off():
    d = FakeDriver([IDENT, PASSW, DP])
    out = await run_step_machine(d)
    assert out.status == "needs_person" and out.reason == "human_gate:device_prompt"


@pytest.mark.asyncio
async def test_missing_backup_option_hands_off_by_name():
    d = BackupDriver([IDENT, PASSW, SELECTION], option=False)
    out = await run_step_machine(d)
    assert out.reason == "human_gate:verification_method_choice"
    assert d.log.count("route") == 1


@pytest.mark.asyncio
async def test_exhausted_codes_stop_and_never_retype():
    d = BackupDriver([IDENT, PASSW, BC], codes=0)
    out = await run_step_machine(d)
    assert out.status == "needs_person" and out.reason == "human_gate:backup_codes_unavailable"


@pytest.mark.asyncio
async def test_rejected_backup_code_is_never_retried():
    d = BackupDriver([IDENT, PASSW, BC], codes=5)
    d.stuck = False
    d.screens = [IDENT, PASSW, BC, BC]  # bc screen returns after the code was typed
    # second BC has the same signature, so the machine sees "did not advance"
    out = await run_step_machine(d)
    assert out.status == "refused"
    assert d.log.count("backup_code") == 1


@pytest.mark.asyncio
async def test_totp_screen_without_authenticator_routes_to_backup_codes():
    d = BackupDriver([IDENT, PASSW, TOTP, BC, HOME], totp=False)
    out = await run_step_machine(d)
    assert out.status == "ready_to_verify"
    assert "totp" not in d.log and d.log[-1] == "backup_code"


ACCOUNT_PAGE = probe("https://myaccount.google.com/", any_input_count=2)


@pytest.mark.asyncio
async def test_signed_in_page_with_other_inputs_after_steps_goes_to_the_verifier():
    """Live 2026-10-20: after the backup code Google's account page (search box) was read as an
    unrecognized screen and a finished sign-in was reported as a hand-off."""
    d = BackupDriver([IDENT, PASSW, DP, BC, ACCOUNT_PAGE])
    out = await run_step_machine(d)
    assert out.status == "ready_to_verify" and out.reason == "no_sign_in_field_left"


@pytest.mark.asyncio
async def test_unrecognized_screen_with_no_steps_done_still_hands_off():
    out = await run_step_machine(FakeDriver([ODD]))
    assert out.status == "needs_person" and out.reason == "human_gate:unrecognized_screen"
