"""The code sign-in step of `plato vault app consent` and `plato vault totp enroll`.

Code, not the agent, types each value: the agent must never see a secret, and its log is kept on disk.
Code names the step from the fields on the page, never from model text (:func:`classify`).
A value goes into the page through ``page.evaluate`` or a JSON literal on stdin, never in argv, a log or an error.
A code sent by email cannot be read yet: by default a person types it.
The caller keeps its own checks after this step (the email gate of `totp enroll`, the user check of `app consent`).
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Callable, Sequence
from typing import Annotated, Any, Protocol

import typer
from pydantic import SecretStr

from plato.chronos.login_vault import SESSION_ID_ENV_VAR, LoginVault, normalize_key
from plato.cli.vault import app_portal, pi_browser, totp_code
from plato.cli.vault.app_models import VaultLine
from plato.cli.vault.app_portal import LINE_TAG, NeedPerson, PortalError, _js
from plato.cli.vault.backends import chronos_errors
from plato.cli.vault.client import NotFound, VaultConsoleError
from plato.cli.vault.sign_in_models import (
    OnEmailCode,
    SignInFill,
    SignInProbe,
    SignInRecipe,
    SignInReport,
    SignInSecrets,
    SignInStep,
)
from plato.cli.vault.totp_models import TotpParams
from plato.cli.vault.totp_portal import SIGNED_IN_EMAILS_JS, tracking_host

# The most sign-in steps one call does (email, password, code, and one entry click).
MAX_STEPS = 6
# After a fill, how long the fill script waits for an enabled submit button, for a page
# that enables it only when it renders again after the input event.
SUBMIT_WAIT_MS = 3_000
# After a submit click, how long code waits for the page to leave the step.
STEP_WAIT_MS = 15_000
STEP_POLL_MS = 500
# A code is typed only when it has at least this many seconds left.
CODE_MIN_LEFT_S = 8
# The person's turn at an email code: one look every PERSON_POLL_S, PERSON_POLLS looks (10 min).
PERSON_POLL_S = 5.0
PERSON_POLLS = 120
SCRIPT_TIMEOUT_S = 60.0
# need_person reasons of the agents after which code looks for a sign-in prompt.
SIGN_IN_REASONS = frozenset({"password", "email_code", "login", "totp"})

OnEmailCodeArg = Annotated[
    OnEmailCode,
    typer.Option(
        "--on-email-code",
        help="A sign-in code that the vendor sends by email (code cannot read the inbox yet): person (wait while "
        "a person types it) or stop",
    ),
]

# Tests patch these.
_clock = time.time
_sleep = time.sleep


class EmailCodeNeeded(PortalError):
    """The vendor sent a code by email, and ``--on-email-code stop`` was given. Exit 6."""


class SignInFailed(PortalError):
    """Code filled a field, but the page did not take it (or code could not fill it). Exit 6."""


# In-page functions take one argument each, as page.evaluate passes one.
# The ego scripts and the Pi page run the same text.

# The input selectors of an email (or username) field.
_EMAIL_INPUTS = (
    "input[type=email], input[autocomplete~=username], input[autocomplete~=email], "
    "input[name=email], input[name=username]"
)
# The current password only: a "new password" field (a set-password form) never gets the
# vault password typed into it.
_PASSWORD_INPUTS = "input[type=password]:not([autocomplete~=new-password])"
# location.hostname over https, else "" (in-page; both scripts use it).
_HOST_JS = 'location.protocol === "https:" ? location.hostname.toLowerCase() : ""'

DETECT_SIGN_IN_JS = (
    r"""(cfg) => {
  const shown = (el) => el.getClientRects().length > 0 && !el.disabled && !el.readOnly
    && getComputedStyle(el).visibility !== "hidden";
  const all = (sel) => [...document.querySelectorAll(sel)].filter(shown);
  const emails = all("""
    + json.dumps(_EMAIL_INPUTS)
    + r""").filter((i) => i.type !== "password" && i.type !== "hidden");
  const boxes = all("input[maxlength='1']");
  const textOf = (root) => {
    const text = [];
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) {
      const p = w.currentNode.parentElement;
      if (p && !["SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE"].includes(p.tagName) && p.getClientRects().length > 0)
        text.push(w.currentNode.nodeValue || "");
    }
    return text.join(" ").toLowerCase();
  };
  const body = textOf(document.body || document.documentElement);
  // The outermost open dialog around el, or null.
  const dialogs = "[role=dialog], [role=alertdialog], [aria-modal=true], dialog[open]";
  const outer = (el) => {
    let d = null;
    for (let p = el.closest(dialogs); p; p = p.parentElement ? p.parentElement.closest(dialogs) : null) d = p;
    return d;
  };
  // A re-sign-in dialog over the settings page: the page under it always shows "Delete your
  // account", so when every value field sits in one open dialog, only that dialog's text counts.
  const fields = [
    ...all("""
    + json.dumps(_PASSWORD_INPUTS)
    + r"""),
    ...all("input[autocomplete=one-time-code]"),
    ...(boxes.length === cfg.digits ? boxes : []),
  ];
  const holders = new Set(fields.map(outer));
  const dialog = holders.size === 1 && !holders.has(null) ? [...holders][0] : null;
  const dangerText = dialog ? textOf(dialog) : body;
  const accountEmails = ("""
    + SIGNED_IN_EMAILS_JS
    + r""")({ ignore: cfg.ignore });
  const has = (list) => list.some((t) => body.includes(t.toLowerCase()));
  const names = cfg.entry.map((n) => n.toLowerCase());
  const entry = [...document.querySelectorAll("button, a, [role=button], [role=link]")]
    .filter((b) => names.includes((b.getAttribute("aria-label") || b.textContent || "").trim().toLowerCase())
      && b.getClientRects().length > 0 && !b.disabled).length;
  return {
    path: location.pathname,
    host: """
    + _HOST_JS
    + r""",
    emails: accountEmails,
    email: emails.length,
    email_empty: emails.filter((i) => !i.value).length,
    password: all("""
    + json.dumps(_PASSWORD_INPUTS)
    + r""").length,
    otp: all("input[autocomplete=one-time-code]").length,
    otp_boxes: boxes.length === cfg.digits ? boxes.length : 0,
    entry,
    authenticator_text: has(cfg.authenticator),
    email_code_text: has(cfg.emailCode),
    danger_text: cfg.danger.some((t) => dangerText.includes(t.toLowerCase())),
  };
}"""
)

# Fill one field (cfg.kind: email, password or otp) with cfg.value, then click the one
# submit button (in the field's form first, else the only one on the page). The value
# is set with the input's native setter plus input and change events, so React sees
# it. A page can enable its button only when it renders again, so the script waits up
# to cfg.waitMs for one. The page took the value by itself (submitted, no click) when
# the field leaves the page, or when a submit button of the field's form turns busy
# (aria-disabled or aria-busy) after the fill: Canva's 2FA page submits the code at the
# 6th digit and shows "ContinueLoading" with aria-disabled="true" meanwhile. A busy
# button is never clicked. Returns counts and flags only, never the value. The script checks the page
# again before it types: the page can change between the probe and the fill, so a
# page off the vendor's hosts (error "origin") or an email input that holds another
# account's email (error "other_account") gets nothing. That check runs for every
# username: with no username (or one that is no email), any filled email input is
# another account's as far as code can tell.
FILL_SIGN_IN_JS = (
    r"""async (cfg) => {
  const host = """
    + _HOST_JS
    + r""";
  if (!host || !cfg.hosts.some((d) => host === d || host.endsWith("." + d)))
    return { filled: false, submitted: false, inputs: 0, error: "origin" };
  const shown = (el) => el.getClientRects().length > 0 && !el.disabled && !el.readOnly;
  const set = (el, v) => {
    Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set.call(el, v);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  };
  const all = (sel) => [...document.querySelectorAll(sel)].filter(shown);
  const emails = () => all("""
    + json.dumps(_EMAIL_INPUTS)
    + r""").filter((i) => i.type !== "password" && i.type !== "hidden");
  const want = (cfg.username || "").trim().toLowerCase();
  if (emails().some((i) => i.value && i.value.trim().toLowerCase() !== want))
    return { filled: false, submitted: false, inputs: 0, error: "other_account" };
  let fields = [];
  if (cfg.kind === "password") {
    fields = all("""
    + json.dumps(_PASSWORD_INPUTS)
    + r""");
  } else if (cfg.kind === "email") {
    fields = emails();
  } else {
    const boxes = all("input[maxlength='1']");
    fields = boxes.length === cfg.digits ? boxes : all("input[autocomplete=one-time-code]");
  }
  const boxes = cfg.kind === "otp" && fields.length === cfg.digits && cfg.digits > 1;
  if (!boxes && fields.length !== 1) return { filled: false, submitted: false, inputs: fields.length, error: "inputs" };
  const busy = (b) => b.getAttribute("aria-disabled") === "true" || b.getAttribute("aria-busy") === "true";
  const form = fields[0].closest("form");
  const submits = () => (form ? [...form.querySelectorAll("button")].filter((b) => b.type === "submit") : []);
  const busyBefore = new Set(submits().filter(busy));
  if (cfg.kind === "password" && cfg.username) {
    // A form with both fields: the empty email field takes the username too.
    const e = emails().filter((i) => !i.value);
    if (e.length === 1) { e[0].focus(); set(e[0], cfg.username); }
  }
  if (boxes) fields.forEach((b, i) => { b.focus(); set(b, cfg.value[i]); });
  else { fields[0].focus(); set(fields[0], cfg.value); }
  const filled = boxes ? fields.map((b) => b.value).join("") === cfg.value : fields[0].value === cfg.value;
  if (!filled) return { filled: false, submitted: false, inputs: fields.length, error: "value" };
  const names = cfg.submit.map((n) => n.toLowerCase());
  const match = (root) => [...root.querySelectorAll("button, [role=button], input[type=submit]")]
    .filter((b) => names.includes((b.getAttribute("aria-label") || b.textContent || b.value || "").trim().toLowerCase())
      && b.getClientRects().length > 0 && !b.disabled && !busy(b));
  const end = Date.now() + cfg.waitMs;
  for (;;) {
    if (!fields[0].isConnected || submits().some((b) => busy(b) && !busyBefore.has(b)))
      return { filled: true, submitted: true, inputs: fields.length };
    const inForm = form ? match(form) : [];
    const onPage = inForm.length ? inForm : match(document);
    if (inForm.length || onPage.length === 1) {
      onPage[0].click();
      return { filled: true, submitted: true, inputs: fields.length };
    }
    if (onPage.length > 1 || Date.now() >= end)
      return { filled: true, submitted: false, inputs: fields.length, error: onPage.length ? "submit_buttons" : "submit_button" };
    await new Promise((r) => setTimeout(r, 100));
  }
}"""
)

# After a failed step: empty the visible password and code inputs, so no later frame or
# snapshot holds a value code typed.
CLEAR_SIGN_IN_JS = r"""() => {
  const set = (el) => {
    Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set.call(el, "");
    el.dispatchEvent(new Event("input", { bubbles: true }));
  };
  let n = 0;
  for (const el of document.querySelectorAll("input[type=password], input[autocomplete=one-time-code], input[maxlength='1']")) {
    if (el.value) { set(el); n += 1; }
  }
  return n;
}"""

# Click the one entry button (an exact accessible name) that opens the email form.
CLICK_ENTRY_JS = r"""(names) => {
  const want = names.map((n) => n.toLowerCase());
  const found = [...document.querySelectorAll("button, a, [role=button], [role=link]")]
    .filter((b) => want.includes((b.getAttribute("aria-label") || b.textContent || "").trim().toLowerCase())
      && b.getClientRects().length > 0 && !b.disabled);
  if (found.length >= 1) found[0].click();
  return found.length;
}"""


def _detect_cfg(recipe: SignInRecipe) -> dict[str, Any]:
    return {
        "ignore": recipe.vendor_email_domains,
        "entry": recipe.entry_buttons,
        "authenticator": recipe.authenticator_texts,
        "emailCode": recipe.email_code_texts,
        "danger": recipe.danger_texts,
        "digits": recipe.digits,
    }


def vendor_host(host: str, recipe: SignInRecipe) -> bool:
    """``host`` (a probe's: "" off https) is one of the recipe's hosts or a subdomain of one."""
    host = host.casefold()
    return bool(host) and any(host == d or host.endswith("." + d) for d in (d.casefold() for d in recipe.hosts))


def _on_path(path: str, part: str) -> bool:
    """``part`` ("/login", "/oauth") is a whole run of segments of ``path``: a substring
    test would count "/settings/login-and-security" as a "/login" page."""
    want = [p for p in part.lower().split("/") if p]
    have = [p for p in path.lower().split("/") if p]
    return bool(want) and any(have[i : i + len(want)] == want for i in range(len(have) - len(want) + 1))


def on_reauth_page(path: str, recipe: SignInRecipe, reauth_paths: Sequence[str]) -> bool:
    """``path`` is one of the caller's re-sign-in paths and no sign-in path: there the
    recipe's ``reauth_submit_buttons`` count as submit buttons too."""
    return not any(_on_path(path, part) for part in recipe.sign_in_paths) and any(
        _on_path(path, part) for part in reauth_paths
    )


def _submit_recipe(recipe: SignInRecipe, path: str, reauth_paths: Sequence[str]) -> SignInRecipe:
    """The recipe the fill uses on ``path``: on a re-sign-in page, with its extra submit buttons."""
    if not recipe.reauth_submit_buttons or not on_reauth_page(path, recipe, reauth_paths):
        return recipe
    return recipe.model_copy(update={"submit_buttons": [*recipe.submit_buttons, *recipe.reauth_submit_buttons]})


def classify(probe: SignInProbe, recipe: SignInRecipe, reauth_paths: Sequence[str] = ()) -> SignInStep:
    """The step the page asks for, from its fields. A code input is the authenticator
    app's only when the page names the app and does not say that a code was sent; any
    other code input counts as an email code (code then types nothing). A page off the
    vendor's hosts, off the sign-in paths, or with destructive-dialog text asks for
    nothing: code never fills it. ``reauth_paths``: paths where the caller expects a
    re-sign-in prompt (the 2FA setup page); there only a password or a code counts."""
    if not vendor_host(probe.host, recipe) or probe.danger_text:
        return SignInStep.none
    on_sign_in_page = any(_on_path(probe.path, part) for part in recipe.sign_in_paths)
    # The settings page holds dialogs that ask for the password or a code to delete the
    # account or to turn 2FA off: a page off the sign-in paths gets no value at all.
    if not on_sign_in_page and not any(_on_path(probe.path, part) for part in reauth_paths):
        return SignInStep.none
    if probe.otp == 1 or probe.otp_boxes == recipe.digits:
        if probe.authenticator_text and not probe.email_code_text:
            return SignInStep.totp
        return SignInStep.email_code
    if probe.password == 1:
        return SignInStep.password
    # A settings page can show the account email in an input: only a sign-in page's counts.
    if probe.email == 1 and probe.email_empty == 1 and on_sign_in_page:
        return SignInStep.email
    if probe.entry >= 1 and on_sign_in_page:
        return SignInStep.entry
    return SignInStep.none


class SignInPage(Protocol):
    def probe(self, recipe: SignInRecipe) -> SignInProbe: ...

    def fill(self, recipe: SignInRecipe, kind: str, value: SecretStr, username: str | None) -> SignInFill: ...

    def clear(self) -> None: ...

    def click_entry(self, recipe: SignInRecipe) -> bool: ...

    def wait_ms(self, ms: int) -> None: ...


class PiSignInPage:
    """The sign-in page in the Pi's Chromium: ``page.evaluate`` over CDP, every value in
    this process, the agent's screen locked while a value is in flight."""

    def __init__(self, driver: pi_browser.PiDriver) -> None:
        self.driver = driver

    def probe(self, recipe: SignInRecipe) -> SignInProbe:
        got = self.driver.evaluate(DETECT_SIGN_IN_JS, _detect_cfg(recipe), None)
        return SignInProbe.model_validate(got) if isinstance(got, dict) else SignInProbe()

    def fill(self, recipe: SignInRecipe, kind: str, value: SecretStr, username: str | None) -> SignInFill:
        cfg = {
            "kind": kind,
            "value": value.get_secret_value(),
            "username": username,
            "submit": recipe.submit_buttons,
            "waitMs": SUBMIT_WAIT_MS,
            "digits": recipe.digits,
            "hosts": [h.casefold() for h in recipe.hosts],
        }
        try:
            with self.driver.secret_lock():
                # Never a second run: a navigation during the fill is the page's own submit
                # (Canva goes to its home page), and a second run would find no field there.
                got = self.driver.evaluate(FILL_SIGN_IN_JS, cfg, None, retry_on_navigation=False)
        except pi_browser.PiPageNavigated:
            return SignInFill(filled=True, submitted=True)  # _wait_for_change reads the new page
        finally:
            cfg.clear()
        return SignInFill.model_validate(got) if isinstance(got, dict) else SignInFill(error="no_result")

    def clear(self) -> None:
        with self.driver.secret_lock():
            self.driver.evaluate(CLEAR_SIGN_IN_JS, None, 0)

    def click_entry(self, recipe: SignInRecipe) -> bool:
        return int(self.driver.evaluate(CLICK_ENTRY_JS, recipe.entry_buttons, 0) or 0) >= 1

    def wait_ms(self, ms: int) -> None:
        self.driver.wait_ms(ms)  # Playwright handles events meanwhile (the callback route)


# What an ego script reports when a navigation destroyed the page's context during an evaluate.
_NAVIGATED = "navigated"


class EgoSignInPage:
    """The sign-in page in the ego-browser TaskSpace: one ``ego-browser nodejs`` script
    per step. A value goes into the script as a JSON literal on stdin, and the script
    runs with ``quiet_errors``, so a failure reports its exit code only."""

    def __init__(self, driver: app_portal.EgoDriver) -> None:
        self.driver = driver

    def _eval(self, fn: str, arg: object, quiet: bool = False) -> VaultLine | None:
        script = (
            f"const task = await taskSpace({_js(self.driver.space_id)});\n"
            'const page = task.page("p1");\n'
            f"let got = null;\ntry {{ got = await page.evaluate({fn}, {_js(arg)}); }} catch (e) {{\n"
            "  const m = String((e && e.message) || e).toLowerCase();\n"
            f"  got = {_js(list(pi_browser._PAGE_NAVIGATED_MARKERS))}.some((t) => m.includes(t)) ? {_js(_NAVIGATED)} : null;\n"
            "}\n"
            f"console.log({_js(LINE_TAG)} + JSON.stringify({{ sign_in: got }}));\n"
        )
        lines = self.driver.run(script, quiet_errors=quiet, timeout_s=SCRIPT_TIMEOUT_S)
        del script
        return next((ln for ln in lines if ln.sign_in is not None), None)

    def probe(self, recipe: SignInRecipe) -> SignInProbe:
        line = self._eval(DETECT_SIGN_IN_JS, _detect_cfg(recipe))
        got = line.sign_in if line is not None else None
        return SignInProbe.model_validate(got) if isinstance(got, dict) else SignInProbe()

    def fill(self, recipe: SignInRecipe, kind: str, value: SecretStr, username: str | None) -> SignInFill:
        cfg = {
            "kind": kind,
            "value": value.get_secret_value(),
            "username": username,
            "submit": recipe.submit_buttons,
            "waitMs": SUBMIT_WAIT_MS,
            "digits": recipe.digits,
            "hosts": [h.casefold() for h in recipe.hosts],
        }
        try:
            line = self._eval(FILL_SIGN_IN_JS, cfg, quiet=True)
        finally:
            cfg.clear()
        got = line.sign_in if line is not None else None
        if got == _NAVIGATED:
            return SignInFill(filled=True, submitted=True)  # the page left during the fill: its own submit
        return SignInFill.model_validate(got) if isinstance(got, dict) else SignInFill(error="no_result")

    def clear(self) -> None:
        self._eval(CLEAR_SIGN_IN_JS, None, quiet=True)

    def click_entry(self, recipe: SignInRecipe) -> bool:
        line = self._eval(CLICK_ENTRY_JS, recipe.entry_buttons)
        got = line.sign_in if line is not None else None
        return isinstance(got, int) and got >= 1

    def wait_ms(self, ms: int) -> None:
        _sleep(ms / 1000)


def page_for(driver: Any) -> SignInPage:
    """The sign-in page for the driver's browser."""
    if isinstance(driver, pi_browser.PiDriver):
        return PiSignInPage(driver)
    return EgoSignInPage(driver)


def vault_secrets(
    login_key: str, account: str, chronos_url: str | None, api_key: str | None
) -> Callable[[], SignInSecrets]:
    """A reader of the vault item's sign-in values: one Chronos read, only when a prompt
    shows, then kept in memory for the command."""
    box: list[SignInSecrets] = []

    def read() -> SignInSecrets:
        if box:
            return box[0]
        key = api_key or os.environ.get("PLATO_API_KEY") or None
        if not key:
            raise VaultConsoleError(
                "the vendor asks to sign in, and code needs the vault item's values for it: set PLATO_API_KEY "
                "or pass --api-key"
            )
        from plato.cli.chronos.settings import get_settings

        url = (chronos_url or get_settings().chronos_url).rstrip("/")
        session_id = os.environ.get(SESSION_ID_ENV_VAR, "").strip() or None
        vault = LoginVault(api_key=key, base_url=url, session_id=session_id)
        try:
            with chronos_errors(url):
                found = vault.get_account(login_key, account)
        finally:
            vault.close()
        if found is None:
            raise NotFound(f"no vault item for {normalize_key(login_key)}/{normalize_key(account)}")
        box.append(
            SignInSecrets(
                username=found.username,
                password=SecretStr(found.password) if found.password else None,
                totp_seed=SecretStr(found.totp_seed) if found.totp_seed else None,
            )
        )
        del found
        return box[0]

    return read


# The vault field each step fills, for the messages (names, never values).
_FIELD = {SignInStep.email: "username", SignInStep.password: "password", SignInStep.totp: "totp_seed"}


def _wait_for_change(
    page: SignInPage, recipe: SignInRecipe, step: SignInStep, reauth_paths: Sequence[str] = ()
) -> SignInStep:
    """Wait until the page leaves ``step``; the step it shows then (``step`` again on a timeout)."""
    waited = 0
    while waited < STEP_WAIT_MS:
        page.wait_ms(STEP_POLL_MS)
        waited += STEP_POLL_MS
        now = classify(page.probe(recipe), recipe, reauth_paths)
        if now != step:
            return now
    return step


def _person_step(
    driver: Any,
    page: SignInPage,
    recipe: SignInRecipe,
    step: SignInStep,
    why: str,
    note: Callable[[str], None],
    reauth_paths: Sequence[str] = (),
) -> None:
    """Hand the window to a person for one step and wait until the page leaves it. Then
    code takes the window back (a Pi browser), so the command goes on."""
    try:
        driver.hand_off()
    except VaultConsoleError:
        driver.handed_off = True
    note(
        f"{why}: type it in {app_portal.person_hint(driver)}. "
        f"This command waits up to {PERSON_POLLS * PERSON_POLL_S / 60:.0f} min."
    )
    for _ in range(PERSON_POLLS):
        _sleep(PERSON_POLL_S)
        try:
            now = classify(page.probe(recipe), recipe, reauth_paths)
        except VaultConsoleError:
            raise NeedPerson(f"{why}. The window is out of reach after the hand-off", reason=step.value) from None
        if now != step:
            reclaim = getattr(driver, "reclaim", None)
            if reclaim is not None:
                reclaim()
            return
    raise NeedPerson(
        f"{why}, and the page still asks for it after {PERSON_POLLS * PERSON_POLL_S / 60:.0f} min. Nothing was saved",
        reason=step.value,
    )


def sign_in(
    driver: Any,
    page: SignInPage,
    recipe: SignInRecipe,
    secrets: Callable[[], SignInSecrets],
    *,
    where: str,
    on_email_code: OnEmailCode = OnEmailCode.person,
    note: Callable[[str], None],
    done: Callable[[], bool] | None = None,
    reauth_paths: Sequence[str] = (),
) -> SignInReport:
    """Fill every sign-in prompt that the open page shows, from the vault item, until the
    page shows none (or ``done()`` is true). ``where`` names the vault item in messages.
    Returns what was done; a page with no prompt returns an empty report and changes nothing.
    ``reauth_paths``: see :func:`classify`.

    Raises :class:`SignInFailed` when the page still asks for a value after code filled
    it (the vault value is wrong, or the page did not react), :class:`EmailCodeNeeded`
    for an email code under ``stop``, and :class:`NeedPerson` when a person's turn ran out."""
    report = SignInReport()
    last_filled: SignInStep | None = None
    step = SignInStep.none
    for _ in range(MAX_STEPS):
        if done is not None and done():
            return report
        probe = page.probe(recipe)
        report.path = probe.path
        step = classify(probe, recipe, reauth_paths)
        if step == SignInStep.none:
            return report
        if step == SignInStep.entry:
            if report.entry_clicks or not page.click_entry(recipe):
                return report  # one click only: a second look at the same page is no progress
            report.entry_clicks += 1
            note("code opened the email sign-in form")
            _wait_for_change(page, recipe, step, reauth_paths)
            continue
        if step == last_filled:
            # _wait_for_change timed out on the step that code filled: the page did not take it.
            page.clear()
            raise SignInFailed(
                f"the vendor still asks for the {step.value} after code filled it from the vault item {where} "
                f"(field {_FIELD.get(step, step.value)}). Check that value in the vault. {_typed(report)}"
            )
        if step == SignInStep.email_code:
            inbox = _inbox(secrets)
            why = f"the vendor sent a sign-in code to {inbox}, and code cannot read that inbox yet"
            if on_email_code == OnEmailCode.stop:
                raise EmailCodeNeeded(
                    f"{why}. --on-email-code stop: {_typed(report)}. Run again with --on-email-code person, and "
                    f"type the code from {inbox} in {app_portal.person_hint(driver)}"
                )
            _person_step(driver, page, recipe, step, f"{why}. Read it in {inbox}", note, reauth_paths)
            report.person.append(step)
            continue
        values = secrets()
        if step in (SignInStep.password, SignInStep.totp):
            _check_account(probe, values, step, where, report)
        value = _value_for(step, values, recipe)
        if value is None:
            # Only an email code goes to a person: a value that the vault lacks is a vault fix.
            raise SignInFailed(
                f"the vendor asks for the {step.value}, and the vault item {where} has no {_FIELD[step]}. Add it "
                f"(plato vault edit), then run the command again. {_typed(report)}"
            )
        kind = "otp" if step == SignInStep.totp else step.value
        try:
            got = page.fill(_submit_recipe(recipe, probe.path, reauth_paths), kind, value, values.username)
        finally:
            del value
        if got.error in ("origin", "other_account"):
            # The page changed between the probe and the fill: the script typed nothing.
            what = "a page off the vendor's hosts" if got.error == "origin" else "another account's email in a field"
            raise SignInFailed(f"the page showed {what} at the {step.value} step. {_typed(report)}")
        if not got.filled or not got.submitted:
            if got.filled:
                page.clear()
            raise SignInFailed(
                f"code could not {'submit' if got.filled else 'fill'} the {step.value} field "
                f"({got.inputs} input(s), {got.error or 'no reason'}). The {step.value} was not submitted. "
                f"{_typed(report)}"
            )
        report.filled.append(step)
        note(f"code filled the {step.value} from the vault item {where}")
        last_filled = step
        nxt = _wait_for_change(page, recipe, step, reauth_paths)
        if nxt != step:
            last_filled = None
    raise SignInFailed(f"the sign-in did not end after {MAX_STEPS} steps (the last one: {step.value})")


def _inbox(secrets: Callable[[], SignInSecrets]) -> str:
    """The inbox the email code went to: the vault item's username (an email for Canva)."""
    try:
        username = secrets().username
    except VaultConsoleError:
        username = None
    return username if username and "@" in username else "the account's email inbox"


def _typed(report: SignInReport) -> str:
    """What code typed so far, for an error: after a fill, an error must never say that
    nothing was typed (the vendor may have taken an earlier value)."""
    if not report.filled:
        return "Code typed nothing"
    return f"Code typed the {', '.join(_FIELD.get(s, s.value) for s in report.filled)} before this, and nothing else"


def _check_account(
    probe: SignInProbe, values: SignInSecrets, step: SignInStep, where: str, report: SignInReport
) -> None:
    """A password or a code goes only to the vault item's own account: when the page shows
    account emails (a "Welcome back, <email>" sign-in, a re-sign-in dialog), the vault
    username must be one of them. A page with no email passes. A vault username that is
    no email can match no shown email, so any shown email stops the step: the prompt may
    be another account's."""
    want = (values.username or "").strip().casefold()
    shown = sorted({e.strip().casefold() for e in probe.emails if "@" in e and not tracking_host(e)})
    if not shown or ("@" in want and want in shown):
        return
    if "@" not in want:
        raise SignInFailed(
            f"the {step.value} prompt shows {', '.join(shown)}, and the vault item {where} has no email as its "
            f"username ({want or 'none'}), so code cannot tell whose prompt it is. {_typed(report)}"
        )
    raise SignInFailed(
        f"the {step.value} prompt is for {', '.join(shown)}, not for the vault item {where} ({want}). {_typed(report)}"
    )


def _value_for(step: SignInStep, values: SignInSecrets, recipe: SignInRecipe) -> SecretStr | None:
    """The value code types for ``step``: the username, the password, or a TOTP code from the seed."""
    if step == SignInStep.email:
        return SecretStr(values.username) if values.username else None
    if step == SignInStep.password:
        return values.password if values.password is not None and values.password.get_secret_value() else None
    if step == SignInStep.totp:
        if values.totp_seed is None or not values.totp_seed.get_secret_value():
            return None
        params = TotpParams(digits=recipe.digits)
        code, _ = totp_code.fresh_code(values.totp_seed, params, min_left_s=CODE_MIN_LEFT_S, clock=_clock, sleep=_sleep)
        return SecretStr(code)
    return None
