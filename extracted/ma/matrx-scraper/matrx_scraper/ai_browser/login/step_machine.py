"""The multi-screen sign-in STEP MACHINE (email -> Next -> password -> optional TOTP).

Identifier-first sign-ins (Google, Microsoft, Okta, ...) never show a password field
on the first screen, so the one-form probe cannot work on them. This module walks the
flow screen by screen instead. It is PURE: every effect (look at the page, type a
vault value, press Next, type the authenticator code) is a method on an injected
:class:`FlowDriver`, so the whole machine is testable against synthetic screens.

Invariants (each has a test):

* **Verify before acting.** Every action is chosen from a freshly observed screen
  (:func:`classify_screen`), never from the previous screen's prediction.
* **Verify after acting.** After a submit the machine waits until the screen
  CHANGED (kind or url). A screen that did not advance is a named refusal -- it never
  types the same secret twice (a repeated password screen means the site refused it).
* **Named refusals.** A screen the machine does not know (a selfie check, a device
  prompt, a CAPTCHA, an unfamiliar form) stops the flow with a stable ``reason`` and
  the exact sentence to give a person. Nothing is clicked or typed on it.
* **Resumable by construction.** The machine keeps no state between calls: after a
  person clears a gate, calling it again observes the CURRENT screen and continues.
* **No values.** Only screen kinds, urls and step names pass through here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Literal, Protocol
from urllib.parse import urlparse


class ScreenKind(StrEnum):
    IDENTIFIER = "identifier"
    PASSWORD = "password"
    TOTP = "totp"
    BACKUP_CODE = "backup_code"
    CAPTCHA = "captcha"
    HUMAN_GATE = "human_gate"
    NO_FORM = "no_form"
    UNKNOWN = "unknown"


# Selector families the driver counts (visible matches only). The machine itself never
# touches a selector except to hand the chosen one back to the driver.
PASSWORD_SELECTOR = "input[type='password']:visible"
OTP_SELECTORS = (
    "input[name='totpPin']:visible",
    "input[name='Pin']:visible",  # Google backup-code screen
    "#backupCodePin:visible",
    "input[autocomplete='one-time-code']:visible",
    "#mfacode:visible",
    "input[name='otc']:visible",
    "input[name='otp' i]:visible",
    "input[name='otp_code' i]:visible",
    "input[name='verification_code' i]:visible",
    "input[name='mfa_code' i]:visible",
)
IDENTIFIER_SELECTORS = (
    "input[name='identifier']:visible",  # Google
    "input[name='loginfmt']:visible",  # Microsoft
    "input[autocomplete='username']:visible",
    "input[type='email']:visible",
    "input[name='username' i]:visible",
    "input[name='email' i]:visible",
    "input[name='login' i]:visible",
)
NEXT_SELECTORS = (
    "#identifierNext button:visible",
    "#identifierNext:visible",
    "#passwordNext button:visible",
    "#passwordNext:visible",
    "#totpNext button:visible",
    "#totpNext:visible",
    "#idSIButton9:visible",  # Microsoft Next / Sign in / Verify
    "button[type='submit']:visible",
    "input[type='submit']:visible",
)
CAPTCHA_SELECTOR = (
    "div.g-recaptcha:visible:not([data-size='invisible']), "
    "div.h-captcha:visible:not([data-size='invisible']), "
    "iframe[src*='recaptcha']:visible:not([src*='size=invisible']), "
    "iframe[src*='hcaptcha']:visible:not([src*='size=invisible']), "
    "iframe[src*='turnstile']:visible, #cf-challenge-running:visible"
)
ANY_INPUT_SELECTOR = "input:not([type='hidden']):not([type='checkbox']):not([type='radio']):visible"

# URL path segments that are a person's job, by name. Order matters not; first hit wins.
HUMAN_GATE_URL_SEGMENTS: tuple[tuple[str, str, str], ...] = (
    (
        "recaptcha",
        "captcha",
        "The site is showing a CAPTCHA. Solve it in the browser (Take control), then hand the browser back.",
    ),
    (
        "selfie",
        "selfie_check",
        "The site is asking for a selfie or face check. Complete it on the phone or in the browser "
        "(Take control), then hand the browser back.",
    ),
    (
        "ipp",
        "phone_verification",
        "The site wants a text or call to the account's phone. A person must complete it (Take "
        "control), then hand the browser back.",
    ),
    (
        "dp",
        "device_prompt",
        "The site sent a prompt to a signed-in device. Approve it on that device, then hand the "
        "browser back.",
    ),
    (
        "speedbump",
        "account_review_prompt",
        "The site is showing an account-review prompt. A person must read and answer it (Take "
        "control), then hand the browser back.",
    ),
    (
        "rejected",
        "sign_in_blocked",
        "The site refused this sign-in as unsafe. A person must sign in from a trusted device first.",
    ),
    (
        "disabled",
        "account_disabled",
        "The site says the account is disabled. A person must resolve it with the provider.",
    ),
    (
        "selection",
        "verification_method_choice",
        "The site is asking which verification method to use. A person must choose one (Take control), "
        "then hand the browser back.",
    ),
)

RESUME_HINT = (
    "When the person has cleared it, call credential_login action='auto' again with the same "
    "session; the step machine re-reads the current screen and continues."
)


#: Every ``reason`` the machine can return -- a CLOSED vocabulary of screen kinds and step names,
#: never a value -- so a transport that redacts free text can still pass these through.
_STEP_NAMES = ("identifier", "password", "totp", "backup_code")
HAND_OFF_REASONS: frozenset[str] = frozenset(
    {f"human_gate:{name}" for _n, name, _s in HUMAN_GATE_URL_SEGMENTS}
    | {
        "human_gate:captcha",
        "human_gate:unrecognized_screen",
        "human_gate:ambiguous_password_fields",
        "human_gate:totp_unavailable",
        "human_gate:backup_codes_unavailable",
        "password_not_accepted",
        "identifier_not_accepted",
        "totp_not_accepted",
        "backup_code_not_accepted",
        "too_many_screens",
    }
    | {f"{n}_step_did_not_advance" for n in _STEP_NAMES}
)


@dataclass(frozen=True)
class ScreenProbe:
    """Raw, value-free facts about the visible page: url + visible-match counts."""

    url: str
    password_count: int = 0
    otp_count: int = 0
    captcha_count: int = 0
    any_input_count: int = 0
    # first selector (from the family lists) with exactly one visible match, if any
    identifier_selector: str | None = None
    otp_selector: str | None = None
    next_selector: str | None = None


@dataclass(frozen=True)
class Screen:
    kind: ScreenKind
    url: str
    gate: str | None = None  # stable name of a human gate / unknown screen
    instruction: str | None = None  # the exact sentence for a person
    identifier_selector: str | None = None
    otp_selector: str | None = None
    next_selector: str | None = None

    def signature(self) -> tuple[str, str]:
        return (self.kind.value, _path(self.url))


def _path(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.netloc}{parsed.path}"


def classify_screen(probe: ScreenProbe) -> Screen:
    """Pure: one probe -> one named screen. Order encodes precedence: a CAPTCHA or a
    named human-gate URL beats any form, because typing past a gate is never right."""
    common = {
        "url": probe.url,
        "identifier_selector": probe.identifier_selector,
        "otp_selector": probe.otp_selector,
        "next_selector": probe.next_selector,
    }
    if probe.captcha_count > 0:
        return Screen(
            ScreenKind.CAPTCHA,
            gate="captcha",
            instruction=HUMAN_GATE_URL_SEGMENTS[0][2],
            **common,
        )
    segments = [s for s in urlparse(probe.url).path.lower().split("/") if s]
    for needle, name, sentence in HUMAN_GATE_URL_SEGMENTS:
        if needle in segments:
            return Screen(ScreenKind.HUMAN_GATE, gate=name, instruction=sentence, **common)
    if probe.password_count == 1:
        return Screen(ScreenKind.PASSWORD, **common)
    if probe.password_count > 1:
        return Screen(
            ScreenKind.UNKNOWN,
            gate="ambiguous_password_fields",
            instruction="The page shows several password fields; a person must pick the right form.",
            **common,
        )
    if probe.otp_count >= 1 and probe.otp_selector:
        if "bc" in segments:
            return Screen(ScreenKind.BACKUP_CODE, **common)
        if probe.otp_count == 1:
            return Screen(ScreenKind.TOTP, **common)
    if probe.identifier_selector and probe.any_input_count == 1:
        return Screen(ScreenKind.IDENTIFIER, **common)
    if probe.any_input_count == 0:
        return Screen(ScreenKind.NO_FORM, **common)
    return Screen(
        ScreenKind.UNKNOWN,
        gate="unrecognized_screen",
        instruction=(
            "The sign-in is showing a screen this tool does not know (an unfamiliar form or "
            "verification step). A person must look at it and complete it (Take control), then "
            "hand the browser back."
        ),
        **common,
    )


class FlowDriver(Protocol):
    """Effects, all behind one seam. Implementations never return a value."""

    async def observe(self) -> Screen: ...

    async def fill_identifier(self, screen: Screen) -> None:
        """Type the vault username into ``screen.identifier_selector`` and advance."""

    async def fill_password(self, screen: Screen) -> None: ...

    async def fill_totp(self, screen: Screen) -> bool:
        """Type one authenticator code from the vault item. False = the item has none."""

    # OPTIONAL backup-code capability. A driver without these methods simply has no
    # backup codes; the machine probes for them with getattr and never requires them.
    #   async def has_backup_codes(self) -> bool
    #   async def choose_backup_codes(self, screen) -> bool   (click through "Try another
    #       way" -> the backup-code option; False = the option is not on the page)
    #   async def fill_backup_code(self, screen) -> bool      (one unused code; False = none left)

    async def settle(self) -> None:
        """Give the page a moment to react (real driver sleeps; fakes no-op)."""


FlowStatus = Literal["ready_to_verify", "needs_person", "refused"]


@dataclass
class FlowOutcome:
    status: FlowStatus
    reason: str
    instruction: str | None = None
    resume: str | None = None
    final_url: str | None = None
    trail: list[str] = field(default_factory=list)  # step names only, e.g. identifier>password


MAX_SCREENS = 8
ADVANCE_POLLS = 6


# Screens where a person would normally pick a different verification method; with backup
# codes saved the machine clicks through to the backup-code option instead.
BACKUP_ROUTE_GATES = frozenset({"device_prompt", "verification_method_choice"})


async def _has_backup_codes(driver: FlowDriver) -> bool:
    fn = getattr(driver, "has_backup_codes", None)
    return bool(fn and await fn())


async def _can_totp(driver: FlowDriver) -> bool:
    """False only when the driver says its item has no authenticator."""
    fn = getattr(driver, "has_totp", None)
    return True if fn is None else bool(await fn())


async def _advanced(driver: FlowDriver, before: Screen) -> Screen | None:
    """Poll until the screen differs from ``before``; None if it never did."""
    for _ in range(ADVANCE_POLLS):
        await driver.settle()
        now = await driver.observe()
        if now.signature() != before.signature():
            return now
    return None


async def run_step_machine(driver: FlowDriver, *, max_screens: int = MAX_SCREENS) -> FlowOutcome:
    trail: list[str] = []
    done: set[ScreenKind] = set()
    routed = False
    screen = await driver.observe()
    for _ in range(max_screens):
        kind = screen.kind
        if (
            not routed
            and (
                (kind is ScreenKind.HUMAN_GATE and screen.gate in BACKUP_ROUTE_GATES)
                or (kind is ScreenKind.TOTP and not await _can_totp(driver))
            )
            and await _has_backup_codes(driver)
        ):
            routed = True
            if await driver.choose_backup_codes(screen):  # type: ignore[attr-defined]
                trail.append("backup_route")
                await driver.settle()
                screen = await driver.observe()
                continue
        if (
            kind is ScreenKind.UNKNOWN
            and screen.gate == "unrecognized_screen"
            and trail
            and not screen.identifier_selector
            and not screen.otp_selector
        ):
            # After at least one step, a page with no sign-in field at all (a signed-in account
            # page with a search box) is not a hand-off: give it to the ONE verifier to judge.
            return FlowOutcome("ready_to_verify", "no_sign_in_field_left", final_url=screen.url, trail=trail)
        if kind in (ScreenKind.CAPTCHA, ScreenKind.HUMAN_GATE, ScreenKind.UNKNOWN):
            return FlowOutcome(
                "needs_person",
                f"human_gate:{screen.gate}",
                instruction=screen.instruction,
                resume=RESUME_HINT,
                final_url=screen.url,
                trail=trail,
            )
        if kind is ScreenKind.NO_FORM:
            return FlowOutcome("ready_to_verify", "no_form_left", final_url=screen.url, trail=trail)

        if kind is ScreenKind.BACKUP_CODE:
            if ScreenKind.BACKUP_CODE in done:
                return FlowOutcome(
                    "refused",
                    "backup_code_not_accepted",
                    instruction="The backup code was not accepted. Do not retry; a person should "
                    "check the saved backup codes and the account.",
                    final_url=screen.url,
                    trail=trail,
                )
            if not await _has_backup_codes(driver) or not await driver.fill_backup_code(screen):  # type: ignore[attr-defined]
                return FlowOutcome(
                    "needs_person",
                    "human_gate:backup_codes_unavailable",
                    instruction="The site asks for a backup code and this saved login has no "
                    "unused backup code. A person must type one (Take control) or add codes to "
                    "the Vault item.",
                    resume=RESUME_HINT,
                    final_url=screen.url,
                    trail=trail,
                )
            done.add(ScreenKind.BACKUP_CODE)
            trail.append("backup_code")
        elif kind is ScreenKind.TOTP:
            if ScreenKind.TOTP in done:
                return FlowOutcome(
                    "refused",
                    "totp_not_accepted",
                    instruction="The authenticator code was not accepted. Do not retry; a person "
                    "should check the saved authenticator and the account.",
                    final_url=screen.url,
                    trail=trail,
                )
            if not await driver.fill_totp(screen):
                return FlowOutcome(
                    "needs_person",
                    "human_gate:totp_unavailable",
                    instruction="The site wants a verification code and this saved login has no "
                    "authenticator. A person must type the code (Take control) or add the "
                    "authenticator to the Vault item.",
                    resume=RESUME_HINT,
                    final_url=screen.url,
                    trail=trail,
                )
            done.add(ScreenKind.TOTP)
            trail.append("totp")
        elif kind is ScreenKind.PASSWORD:
            if ScreenKind.PASSWORD in done:
                return FlowOutcome(
                    "refused",
                    "password_not_accepted",
                    instruction="The password screen came back after the password was entered. "
                    "Do not retry the same saved login; a person should check it.",
                    final_url=screen.url,
                    trail=trail,
                )
            await driver.fill_password(screen)
            done.add(ScreenKind.PASSWORD)
            trail.append("password")
        elif kind is ScreenKind.IDENTIFIER:
            if ScreenKind.IDENTIFIER in done:
                return FlowOutcome(
                    "refused",
                    "identifier_not_accepted",
                    instruction="The account screen came back after the username was entered. "
                    "The site did not accept it; a person should check the saved login.",
                    final_url=screen.url,
                    trail=trail,
                )
            await driver.fill_identifier(screen)
            done.add(ScreenKind.IDENTIFIER)
            trail.append("identifier")

        nxt = await _advanced(driver, screen)
        if nxt is None:
            if trail[-1] == "password":
                # Same password screen after a submit = the site refused it. Never retype.
                return FlowOutcome(
                    "refused",
                    "password_not_accepted",
                    instruction="The password screen stayed after the password was entered. "
                    "Do not retry the same saved login; a person should check it.",
                    final_url=screen.url,
                    trail=trail,
                )
            return FlowOutcome(
                "refused",
                f"{trail[-1]}_step_did_not_advance",
                instruction="The page did not move on after that step. Take a screenshot and "
                "check it before trying again.",
                final_url=screen.url,
                trail=trail,
            )
        screen = nxt
    return FlowOutcome(
        "refused",
        "too_many_screens",
        instruction="The sign-in kept presenting new screens; a person should take over.",
        final_url=screen.url,
        trail=trail,
    )


__all__ = [
    "HAND_OFF_REASONS",
    "ANY_INPUT_SELECTOR",
    "CAPTCHA_SELECTOR",
    "FlowDriver",
    "FlowOutcome",
    "IDENTIFIER_SELECTORS",
    "NEXT_SELECTORS",
    "OTP_SELECTORS",
    "PASSWORD_SELECTOR",
    "Screen",
    "ScreenKind",
    "ScreenProbe",
    "classify_screen",
    "run_step_machine",
]
