"""The browser steps of `plato vault totp enroll`, through ego-browser on this Mac.

Code checks the signed-in account first: a browser that holds another person's session would turn
2FA on for THAT account, and the seed would go to the wrong vault item.
The agent (the :mod:`app_portal` sandbox) stops at the QR code or the "Show secret key" button, and
never types a password or a code. Code does every step that touches a secret (:class:`TotpPage`).
A script failure reports its exit code only, never the script's output.
The code goes into the script as a JSON literal on stdin, never in argv.
"""

from __future__ import annotations

import os
import secrets
import shutil
import tempfile
import time
from collections.abc import Callable
from pathlib import Path
from typing import Protocol, TypeVar

from pydantic import BaseModel, SecretStr, ValidationError

from plato.cli.vault.app_models import ConsentBrowser, VaultLine
from plato.cli.vault.app_portal import LINE_TAG, NO_FILES_RULE, PI_SCREEN_RULE, EgoDriver, PortalError, _js
from plato.cli.vault.prompts import render_prompt
from plato.cli.vault.totp_code import BadSeed, normalize_seed, parse_otpauth, seed_bytes
from plato.cli.vault.totp_models import (
    AccountMatch,
    BackupCodesFile,
    CodeResult,
    KeyCandidates,
    KeySource,
    SignedInCheck,
    TotpKey,
    TotpParams,
    TotpRecipe,
)

# How long code waits for the key after the reveal click, and for the page to
# react to the confirm click.
KEY_WAIT_MS = 20_000
CONFIRM_WAIT_MS = 20_000
# The first look after the confirm click comes this late, so the old window state is gone.
CONFIRM_SETTLE_MS = 1_500
BACKUP_WAIT_MS = 10_000
# How long code waits for an account email on a page (a single-page app renders late),
# and the second look after the first email, so a second account email that renders a
# moment later is not missed.
IDENTITY_WAIT_MS = 15_000
IDENTITY_SETTLE_MS = 1_000
STEP_TIMEOUT_S = 90.0

M = TypeVar("M", bound=BaseModel)


def agent_goal(recipe: TotpRecipe, space_id: int, browser: ConsentBrowser = ConsentBrowser.ego) -> str:
    template = recipe.pi_agent_template if browser == ConsentBrowser.pi else recipe.agent_template
    return render_prompt(
        template,
        space_id=space_id,
        settings_url=recipe.settings_url,
        no_files=NO_FILES_RULE,
        screen_rule=PI_SCREEN_RULE,
    )


def space_name(recipe: TotpRecipe, login_key: str, account: str) -> str:
    return f"vault-totp-{recipe.vendor}-{login_key}-{account}-{time.strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(4)}"


def pick_key(candidates: KeyCandidates, recipe: TotpRecipe) -> TotpKey:
    """The one seed the page shows. An otpauth URI wins (it carries the parameters);
    a text key must agree with it. Two different seeds are refused: code does not
    guess which one the vendor checks. Errors give counts and lengths only."""
    default = TotpParams(digits=recipe.digits, period_s=recipe.period_s, algorithm=recipe.algorithm)
    from_uris: dict[str, TotpParams] = {}
    for uri in candidates.uris:
        try:
            seed, params = parse_otpauth(uri.get_secret_value(), default)
        except BadSeed:
            continue
        from_uris[seed] = params
    texts = {normalize_seed(k.get_secret_value()) for k in candidates.keys}
    texts.discard("")
    if len(from_uris) > 1:
        raise PortalError(f"the page shows {len(from_uris)} different otpauth URIs; nothing was typed")
    if from_uris:
        seed, params = next(iter(from_uris.items()))
        if texts and texts != {seed}:
            raise PortalError("the page's text key and its otpauth URI do not agree; nothing was typed")
        source = KeySource.otpauth
    elif len(texts) == 1:
        seed, params, source = next(iter(texts)), default, KeySource.text
    else:
        raise PortalError(
            f"expected one setup key on the page, found {len(texts)} text key(s) and no otpauth URI; nothing was typed"
        )
    seed_bytes(seed)  # BadSeed (no seed text) when it is not base32 or too short
    return TotpKey(seed=SecretStr(seed), params=params, source=source)


def _email_domain_is(email: str, domains: list[str]) -> bool:
    host = email.rsplit("@", 1)[-1]
    return any(host == d or host.endswith("." + d) for d in (d.casefold() for d in domains))


def tracking_host(email: str) -> bool:
    """An address at an error-tracking or ingest host (a Sentry DSN's user part), never an
    account. The same rule as :data:`TRACKING_HOST_JS`, so a reader that missed it here
    still does not count it."""
    host = email.rsplit("@", 1)[-1].casefold()
    return host == "sentry.io" or host.endswith(".sentry.io") or host.startswith("ingest.") or ".ingest." in host


class EmailReadFailed(PortalError):
    """The account check could not read the page. Not "no email": the caller stops."""


class _VendorDomains(Protocol):
    """What :func:`check_signed_in` reads from a recipe: a TotpRecipe and a SignInRecipe both have it."""

    @property
    def vendor_email_domains(self) -> list[str]: ...


def check_signed_in(found: list[str], username: str | None, recipe: _VendorDomains, page: str | None) -> SignedInCheck:
    """Code, not a model, decides whether the browser is signed in as the vault account.
    Only one result lets the setup start: the page shows the vault item's username
    (case-folded) and no other account email. Anything else (another email, two
    emails, no email, a username that is no email) stops the command."""
    want = (username or "").strip().casefold()
    emails = sorted(
        {e.strip().casefold() for e in found if "@" in e} - {""},
    )
    emails = [e for e in emails if not _email_domain_is(e, recipe.vendor_email_domains) and not tracking_host(e)]
    if "@" not in want:
        result = AccountMatch.no_vault_email
    elif not emails:
        result = AccountMatch.unknown
    elif emails == [want]:
        result = AccountMatch.match
    elif want in emails:
        result = AccountMatch.ambiguous
    else:
        result = AccountMatch.mismatch
    return SignedInCheck(result=result, expected=want or None, found=emails, page=page if emails else None)


class TotpPage:
    """The code-only steps on page p1 of the driver's TaskSpace."""

    def __init__(self, driver: EgoDriver, recipe: TotpRecipe) -> None:
        self.driver = driver
        self.recipe = recipe

    def _run(self, script: str) -> list[VaultLine]:
        return self.driver.run(script, quiet_errors=True, timeout_s=STEP_TIMEOUT_S)

    def _read_file(self, script_for: Callable[[str], str], model: type[M]) -> tuple[M, VaultLine]:
        """Run a script that writes one JSON file into a private 700 temp directory;
        the parsed file and the script's result line. The directory is always removed."""
        workdir = tempfile.mkdtemp(prefix="vault-totp-")
        path = os.path.join(workdir, "out.json")
        try:
            lines = self._run(script_for(path))
            line = next((ln for ln in lines if ln.written is not None or ln.error), None)
            if line is None or not line.written:
                raise PortalError(f"the read step wrote nothing ({line.error if line else 'no result line'})")
            try:
                return model.model_validate_json(Path(path).read_text()), line
            except (OSError, ValueError, ValidationError):
                raise PortalError("the read step's file is missing or unreadable") from None
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    def signed_in_emails(self) -> list[str]:
        """The account emails that the open page shows (vendor addresses left out), after
        a wait for the page to render one. ``[]``: the page was read and showed none.
        A failed last read or no result line raises :class:`EmailReadFailed`, so a failed
        check never looks like a page with no email."""
        lines = self._run(_emails_script(self.driver.space_id, self.recipe))
        line = next((ln for ln in lines if ln.emails is not None or ln.error), None)
        if line is None:
            raise EmailReadFailed("the account check printed no result line")
        if line.error:
            raise EmailReadFailed(f"the account check could not read the page ({line.error})")
        return [str(e) for e in line.emails or []]

    def reveal_key(self) -> tuple[TotpKey, VaultLine]:
        candidates, line = self._read_file(
            lambda path: _reveal_script(self.driver.space_id, path, self.recipe), KeyCandidates
        )
        return pick_key(candidates, self.recipe), line

    def type_code(self, code: str) -> VaultLine:
        lines = self._run(_code_script(self.driver.space_id, code, self.recipe))
        line = next((ln for ln in lines if ln.result is not None or ln.error), None)
        if line is None:
            return VaultLine(result=CodeResult.unknown.value, error="no result line")
        return line

    def key_ready(self) -> bool:
        """True when the setup window shows the QR code step (a reveal button or an
        ``otpauth`` URI). Reads no key: it prints one boolean."""
        lines = self._run(_key_ready_script(self.driver.space_id, self.recipe))
        return any(ln.ready_for_key for ln in lines)

    def read_backup_codes(self) -> list[SecretStr]:
        """The backup codes, or ``[]`` when the page shows none that match the recipe."""
        try:
            found, _ = self._read_file(
                lambda path: _backup_script(self.driver.space_id, path, self.recipe), BackupCodesFile
            )
        except PortalError:
            return []
        codes = [c for c in found.codes if c.get_secret_value()]
        if not self.recipe.backup_codes_min <= len(codes) <= self.recipe.backup_codes_max:
            return []
        return codes

    def finish_setup(self) -> bool:
        lines = self._run(_finish_script(self.driver.space_id, self.recipe))
        return any(ln.finished for ln in lines)


# Shared helpers: buttons by exact name (aria-label or text, any case, visible and
# enabled), and the setup window (the last visible [role=dialog], else the body).
# In-page functions (one argument each, as page.evaluate passes one). The ego
# scripts below and the Pi driver (pi_browser.PiTotpPage) run the same text.
BY_NAME_JS = """({ names, click }) => {
  const want = names.map((n) => n.toLowerCase());
  const found = [...document.querySelectorAll("button, a, [role=button], [role=link]")]
    .filter((b) => want.includes((b.getAttribute("aria-label") || b.textContent || "").trim().toLowerCase())
      && b.getClientRects().length > 0 && !b.disabled);
  if (click && found.length >= 1) found[0].click();
  return found.length;
}"""

_HELPERS = (
    """
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const byName = """
    + BY_NAME_JS
    + """;
const count = async (names) => { try { return await page.evaluate(byName, { names, click: false }); } catch (e) { return 0; } };
const clickName = async (name) => {
  try {
    await page.click("loc=role:button[name=" + JSON.stringify(name) + "]", { label: "totp setup: " + name });
    return true;
  } catch (e) {
    try { return (await page.evaluate(byName, { names: [name], click: true })) >= 1; } catch (e2) { return false; }
  }
};
"""
)

FIND_KEY_JS = r"""(cfg) => {
  const uriRe = /otpauth:\/\/totp\/[^\s"'<>]+/gi;
  const keyRe = new RegExp(cfg.keyPattern);
  const uris = new Set();
  const keys = new Set();
  for (const el of document.querySelectorAll("*")) {
    for (const attr of ["href", "src", "alt", "title", "aria-label", "data-value", "value"]) {
      let v = attr === "value" ? el.value : el.getAttribute(attr);
      if (typeof v !== "string") continue;
      // A QR image URL can carry the URI URL-encoded (otpauth%3A%2F%2F...).
      if (/otpauth%3a/i.test(v)) { try { v = v + " " + decodeURIComponent(v); } catch (e) {} }
      for (const m of v.matchAll(uriRe)) uris.add(m[0]);
    }
    if ((el.tagName === "INPUT" || el.tagName === "TEXTAREA") && typeof el.value === "string"
        && keyRe.test(el.value.trim())) keys.add(el.value.trim());
  }
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = (walker.currentNode.nodeValue || "").trim();
    for (const m of t.matchAll(uriRe)) uris.add(m[0]);
    if (keyRe.test(t)) keys.add(t);
  }
  // A key split over several spans (one group of 4 each): the parent's text.
  for (const el of document.querySelectorAll("div, span, p, code, pre, strong, b")) {
    if (el.children.length < 2 || el.children.length > 12) continue;
    const t = (el.innerText || el.textContent || "").replace(/\s+/g, " ").trim();
    if (keyRe.test(t)) keys.add(t);
  }
  return { uris: [...uris], keys: [...keys] };
}"""

TYPE_CODE_JS = r"""(cfg) => {
  const shown = (el) => el.getClientRects().length > 0 && !el.disabled && !el.readOnly;
  const set = (el, v) => {
    const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, "value").set.call(el, v);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  };
  const root = [...document.querySelectorAll("[role=dialog]")].filter((d) => d.getClientRects().length > 0).pop()
    || document.body;
  const boxes = [...root.querySelectorAll("input[maxlength='1']")].filter(shown);
  if (boxes.length === cfg.digits) {
    boxes.forEach((b, i) => { b.focus(); set(b, cfg.code[i]); });
    return { typed: true, inputs: boxes.length };
  }
  for (const sel of cfg.selectors) {
    const found = [...root.querySelectorAll(sel)].filter(shown);
    if (found.length === 1) {
      found[0].focus();
      set(found[0], cfg.code);
      return { typed: found[0].value === cfg.code, inputs: 1 };
    }
    if (found.length > 1) return { typed: false, inputs: found.length };
  }
  return { typed: false, inputs: 0 };
}"""

CODE_STATE_JS = r"""(cfg) => {
  const root = [...document.querySelectorAll("[role=dialog]")].filter((d) => d.getClientRects().length > 0).pop();
  const text = ((root || document.body).innerText || (root || document.body).textContent || "").toLowerCase();
  const names = (list) => list.map((n) => n.toLowerCase());
  const buttons = [...document.querySelectorAll("button, a, [role=button]")]
    .filter((b) => b.getClientRects().length > 0)
    .map((b) => (b.getAttribute("aria-label") || b.textContent || "").trim().toLowerCase());
  const accepted = buttons.some((b) => names(cfg.accepted).includes(b));
  const error = root ? names(cfg.errors).some((e) => text.includes(e)) : false;
  const confirmOpen = buttons.includes(cfg.confirm.toLowerCase());
  return { accepted, error, confirmOpen, dialog: !!root };
}"""

# The account emails on the page: only what a person can see. Text nodes whose element
# is visible (no script, style, noscript or template, no hidden element) and the values
# of visible inputs; never an attribute or a URL. Canva pages hold
# a Sentry DSN (``<key>@o1.ingest.sentry.io``) next to the real email, so the gate saw
# "two emails": an address in a word with ``//`` before it is part of a URL, and an address
# at a tracking or ingest host (TRACKING_HOST_JS), or at cfg.ignore domains (the
# vendor's own), is left out. Lower case.
TRACKING_HOST_JS = r"""(h) => h === "sentry.io" || h.endsWith(".sentry.io")
  || h.startsWith("ingest.") || h.includes(".ingest.")"""
SIGNED_IN_EMAILS_JS = (
    r"""(cfg) => {
  const re = /[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}/g;
  const ignore = (cfg.ignore || []).map((d) => d.toLowerCase());
  const tracking = """
    + TRACKING_HOST_JS
    + r""";
  const skip = (e) => {
    const h = e.split("@").pop();
    return tracking(h) || ignore.some((d) => h === d || h.endsWith("." + d));
  };
  // Visible = a person can see it. Judge the text's own element, not each ancestor on its own: a
  // display:contents wrapper has no box (no client rects, checkVisibility false) while its children
  // show. Canva's /settings/your-account puts the account email under one (live probe 2026-10-19).
  // checkVisibility already looks at the ancestors (display, content-visibility, opacity, visibility).
  const visible = (el) => {
    if (el.closest("script, style, noscript, template, head, title, [hidden]")) return false;
    if (typeof el.checkVisibility === "function") {
      return el.checkVisibility({ opacityProperty: true, visibilityProperty: true }) && el.getClientRects().length > 0;
    }
    // no checkVisibility (an old browser, jsdom): the computed style of the element and its ancestors
    for (let e = el; e; e = e.parentElement) {
      const st = getComputedStyle(e);
      if (st.display === "none" || st.visibility === "hidden" || st.visibility === "collapse" || st.opacity === "0") return false;
    }
    return true;
  };
  const found = new Set();
  const add = (v) => {
    if (typeof v !== "string") return;
    for (const m of v.matchAll(re)) {
      // A URL's user part (a DSN "https://<key>@host", or "user:pw@host"), not an email: the
      // word that holds the match has "//" before it. "Email:jim@x.so" stays an email.
      const word = /\S*$/.exec(v.slice(0, m.index))[0];
      if (word.includes("//")) continue;
      const e = m[0].toLowerCase();
      if (!skip(e)) found.add(e);
    }
  };
  const root = document.body || document.documentElement;
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const p = w.currentNode.parentElement;
    if (p && visible(p)) add(w.currentNode.nodeValue || "");
  }
  for (const el of document.querySelectorAll("input, textarea")) {
    if (el.type === "hidden" || el.type === "password") continue;
    if (visible(el)) add(el.value);
  }
  return [...found];
}"""
)

OTPAUTH_IN_PAGE_JS = "() => /otpauth(:|%3a)/i.test(document.documentElement.innerHTML)"

BACKUP_FIND_JS = r"""(cfg) => {
  const re = new RegExp(cfg.pattern);
  const root = [...document.querySelectorAll("[role=dialog]")].filter((d) => d.getClientRects().length > 0).pop();
  if (!root) return [];
  const codes = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = (walker.currentNode.nodeValue || "").trim();
    if (re.test(t) && !codes.includes(t)) codes.push(t);
  }
  return codes;
}"""


def _head(space_id: int | None) -> str:
    return (
        f"const task = await taskSpace({_js(space_id)});\n"
        'const page = task.page("p1");\n'
        f"const out = (o) => console.log({_js(LINE_TAG)} + JSON.stringify(o));\n"
    )


def _reveal_script(space_id: int | None, path: str, recipe: TotpRecipe) -> str:
    """Click a reveal button if no key is in the DOM yet, wait for one, and write every
    candidate to ``path`` (mode 600, ``wx``). Prints counts only."""
    return (
        _head(space_id)
        + _HELPERS
        + f"""
const fs = await import("node:fs/promises");
const cfg = {{ keyPattern: {_js(recipe.key_pattern)} }};
const find = {FIND_KEY_JS};
const look = async () => {{ try {{ return await page.evaluate(find, cfg); }} catch (e) {{ return {{ uris: [], keys: [] }}; }} }};
let got = await look();
if (got.uris.length === 0 && got.keys.length === 0) {{
  for (const name of {_js(recipe.reveal_texts)}) {{
    if ((await count([name])) >= 1) {{ await clickName(name); break; }}
  }}
  const end = Date.now() + {KEY_WAIT_MS};
  while (Date.now() < end) {{
    got = await look();
    if (got.uris.length || got.keys.length) break;
    await sleep(500);
  }}
}}
if (got.uris.length === 0 && got.keys.length === 0) {{
  out({{ written: false, error: "no_key", uri_count: 0, key_count: 0 }});
}} else {{
  const fh = await fs.open({_js(path)}, "wx", 0o600);
  try {{
    await fh.writeFile(JSON.stringify({{ uris: got.uris, keys: got.keys }}));
  }} finally {{
    await fh.close();
  }}
  out({{ written: true, uri_count: got.uris.length, key_count: got.keys.length }});
}}
"""
    )


def _code_script(space_id: int | None, code: str, recipe: TotpRecipe) -> str:
    """Type ``code`` into the one code input (or into ``digits`` one-character boxes),
    click the confirm button, then wait. An accepted button means accepted, also when
    the page took the code by itself (auto-submit) before the click.

    Rejected needs an error that is NEW after the click, while the code step is still
    open. The script reads the error state before the click: an error text that was
    there already (the last attempt's, or help text) counts only after it went away
    and came back. Anything else is unknown, and the caller then saves the seed,
    because a lost seed with 2FA on is worse than an unused seed. ``not_typed`` means
    that no code went into an input; a typing call with no reply is unknown.

    The value is set with the input's native setter plus input and change events, so
    React sees it. Prints the result and counts only, never the code."""
    return (
        _head(space_id)
        + _HELPERS
        + f"""
const cfg = {{ code: {_js(code)}, selectors: {_js(recipe.code_input_selectors)}, digits: {recipe.digits} }};
const type = {TYPE_CODE_JS};
const state = {CODE_STATE_JS};
const scfg = {{ accepted: {_js(recipe.accepted_buttons)}, errors: {_js(recipe.error_texts)}, confirm: {_js(recipe.confirm_button)} }};
const look = async () => {{ try {{ return await page.evaluate(state, scfg); }} catch (e) {{ return null; }} }};
let typed = {{ typed: false, inputs: 0 }};
let failed = false;
try {{ typed = await page.evaluate(type, cfg); }} catch (e) {{ failed = true; }}
if (failed) {{
  // The script may have typed before its reply was lost (a last digit that submits navigates).
  out({{ result: "unknown", typed: true, inputs: -1 }});
}} else if (!typed.typed) {{
  out({{ result: "not_typed", typed: false, inputs: typed.inputs }});
}} else {{
  await sleep(500);
  // The state before the click: an error shown now is an old one.
  const before = await look();
  let result = "unknown";
  let clicked = false;
  if (before && before.accepted) {{
    result = "accepted";  // the page took the code by itself
  }} else {{
    if ((await count([{_js(recipe.confirm_button)}])) === 1) clicked = await clickName({_js(recipe.confirm_button)});
    // No clickable button: still wait, because the page can move on by itself.
    await sleep({CONFIRM_SETTLE_MS});
    let cleared = !(before && before.error);
    const end = Date.now() + {CONFIRM_WAIT_MS};
    while (Date.now() < end) {{
      const s = await look();
      if (s && s.accepted) {{ result = "accepted"; break; }}
      if (s && !s.error) cleared = true;
      if (s && s.error && cleared && s.confirmOpen && clicked) {{
        // A new error while the code step is open: look once more before the verdict.
        await sleep({CONFIRM_SETTLE_MS});
        const again = await look();
        if (again && again.accepted) result = "accepted";
        else if (again && again.error && again.confirmOpen) result = "rejected";
        break;
      }}
      await sleep(500);
    }}
  }}
  const line = {{ result, typed: true, clicked, inputs: typed.inputs }};
  if (!clicked && result !== "accepted") line.error = "confirm_button";
  out(line);
}}
"""
    )


def _key_ready_script(space_id: int | None, recipe: TotpRecipe) -> str:
    """One look: does the setup window show the QR code step (a reveal button, or an
    ``otpauth`` URI anywhere in the DOM)? Prints one boolean, never the key."""
    return (
        _head(space_id)
        + _HELPERS
        + f"""
let ready = (await count({_js(recipe.reveal_texts)})) >= 1;
if (!ready) {{
  try {{
    ready = await page.evaluate({OTPAUTH_IN_PAGE_JS});
  }} catch (e) {{
    ready = false;
  }}
}}
out({{ ready_for_key: ready }});
"""
    )


def _emails_script(space_id: int | None, recipe: TotpRecipe) -> str:
    """Wait for the page to show an account email, look once more after a short settle,
    and print every account email seen. Emails only: the page holds no secret yet.
    A read can throw while the page navigates, so the wait reads again. ``error`` prints
    only when the last read failed and no read found an email (the caller then raises,
    never sees ``[]``): emails that an earlier read found stay a result."""
    return (
        _head(space_id)
        + f"""
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const cfg = {{ ignore: {_js(recipe.vendor_email_domains)} }};
const find = {SIGNED_IN_EMAILS_JS};
let failed = false;
const look = async () => {{
  try {{ const got = await page.evaluate(find, cfg); failed = false; return got; }} catch (e) {{ failed = true; return []; }}
}};
let emails = await look();
const end = Date.now() + {IDENTITY_WAIT_MS};
while (emails.length === 0 && Date.now() < end) {{
  await sleep(500);
  emails = await look();
}}
if (emails.length) {{
  await sleep({IDENTITY_SETTLE_MS});
  emails = [...new Set([...emails, ...(await look())])];
}}
out(failed && emails.length === 0 ? {{ emails, error: "read_failed" }} : {{ emails }});
"""
    )


def _backup_script(space_id: int | None, path: str, recipe: TotpRecipe) -> str:
    """Read the leaf texts of the setup window that match the backup-code pattern and
    write them to ``path`` (mode 600, ``wx``). Prints the count only."""
    return (
        _head(space_id)
        + _HELPERS
        + f"""
const fs = await import("node:fs/promises");
const cfg = {{ pattern: {_js(recipe.backup_code_pattern)} }};
const find = {BACKUP_FIND_JS};
let codes = [];
const end = Date.now() + {BACKUP_WAIT_MS};
while (Date.now() < end) {{
  try {{ codes = await page.evaluate(find, cfg); }} catch (e) {{ codes = []; }}
  if (codes.length) break;
  await sleep(500);
}}
const fh = await fs.open({_js(path)}, "wx", 0o600);
try {{
  await fh.writeFile(JSON.stringify({{ codes }}));
}} finally {{
  await fh.close();
}}
out({{ written: true, codes: codes.length }});
"""
    )


def _finish_script(space_id: int | None, recipe: TotpRecipe) -> str:
    """Click the finish button (when there is one), then send the page to about:blank."""
    return (
        _head(space_id)
        + _HELPERS
        + f"""
let finished = false;
try {{
  if ((await count([{_js(recipe.finish_button)}])) >= 1) {{
    finished = await clickName({_js(recipe.finish_button)});
    await sleep(1500);
  }}
}} finally {{
  try {{ await page.goto("about:blank"); }} catch (e) {{}}
}}
out({{ finished }});
"""
    )
