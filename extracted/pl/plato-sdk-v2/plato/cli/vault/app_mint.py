"""`plato vault mint token`: an OAuth grant for any vendor's vault account, with no vendor steps
written down, kept in the Chronos login vault.

When the account's grant is there and its token read answers, nothing else runs. Else a
computer-use agent drives Chromium on the office Pi (:mod:`pi_browser`) and has web search: it
finds the vendor's developer docs, opens the vendor's pages, makes (or reuses) an OAuth app and
runs the consent. Code does every step that touches a secret, through the agent's ``vault`` MCP tools:

* ``fill_sign_in``: code types the vault item's username, password or authenticator code, or the
  code the vendor just emailed (read from the login email's inbox, :mod:`mail_code`), into the input
  that has focus, on a vendor page over https only.
* ``read_value``: the agent points at a value (the mouse pointer); code reads it from the page over
  CDP into this process.
* ``register_client``: for a server that registers clients itself (a hosted MCP server, most
  often), code discovers its OAuth metadata and registers a client (:mod:`mint_dcr`) instead of
  the agent making an app.
* ``oauth_start`` / ``oauth_finish``: code builds the authorize URL (PKCE, state), takes the
  redirect on 127.0.0.1 and exchanges the code.
* ``check``: code calls the "who am I" endpoint the agent picked, with the access token; for an
  MCP server, initialize, tools/list and one read-only tools/call.

The tools answer with names, lengths and HTTP statuses only, and a mask script hides the page
values that match its secret patterns before a frame goes out (:class:`pi_desktop_adapter.MaskGate`);
a secret in a shape the patterns miss can still show on screen. Then code moves the grant into the login vault (:mod:`mint_store`), reads its
token back through Chronos and runs the check again with it.
"""

from __future__ import annotations

import asyncio
import json
import os
import threading
from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from functools import partial
from typing import Any, TypeVar
from urllib.parse import urlencode, urlparse

import httpx
from pydantic import BaseModel, SecretStr, ValidationError

from plato.chronos.login_vault import SESSION_ID_ENV_VAR, GrantKind, LoginVault, normalize_key
from plato.cli.chronos.settings import get_settings
from plato.cli.vault import (
    app_oauth,
    app_portal,
    mail_code,
    mint_dcr,
    mint_docs,
    pi_browser,
    pi_desktop_adapter,
    totp_code,
)
from plato.cli.vault.app_models import ClientAuth, PkcePair, TokenGrant, VaultLine
from plato.cli.vault.app_portal import PortalError
from plato.cli.vault.backends import chronos_errors
from plato.cli.vault.client import NotFound, VaultConsoleError
from plato.cli.vault.mint_models import (
    CheckIdentity,
    CheckInput,
    CheckResult,
    DocsPlan,
    FillInput,
    FocusedInput,
    McpTool,
    McpToolList,
    McpToolResult,
    MintOutcome,
    MintReport,
    OAuthFinishInput,
    OAuthSpec,
    OAuthStartInput,
    OAuthTokens,
    ReadInput,
    RegisteredServer,
    RegisterInput,
    RpcReply,
    SignInField,
    ToolReply,
    VaultItem,
)
from plato.cli.vault.mint_store import GrantStore, StoreRefused, TokenReadFailed
from plato.cli.vault.prompts import GoalTemplate, render_prompt
from plato.cli.vault.totp_models import TotpParams
from plato.tools import ToolDefinition
from plato.tools.server import ToolServer
from plato.vault.mail_route import login_email_of

# The redirect URI the agent registers on an OAuth app; the Pi browser's request for it is
# routed to the listener on this machine (PiDriver.route_callback).
MINT_REDIRECT_URI = "http://127.0.0.1:8765/callback"
# The name the agent gives the OAuth app it makes, so a second run finds and reuses it.
MINT_LABEL = "plato-vault-mint"
MINT_TIMEOUT_S = 1800.0
PAGE_JOB_TIMEOUT_S = 120.0
FILL_TIMEOUT_MS = 5_000
CHECK_TIMEOUT_S = 30.0
# Per key of an emailed code: a code split over one box per character moves focus on each input
# event, and a key that lands while it moves is dropped (login world get_otp, Booking.com).
CODE_KEY_DELAY_MS = 150
CODE_MIN_LEFT_S = 5
SERVER_NAME = "vault"
# Token read answers that mean the grant cannot give a token: no grant (404), not active and
# expired or a refresh that never ended (409), the vendor refused the refresh (502).
GRANT_DEAD_STATUSES = (404, 409, 502)
# A vendor check answer that means the token is refused (403 can be a scope or role, so it stops).
TOKEN_REFUSED_STATUSES = (401,)
MINT_TOOLS = ("fill_sign_in", "read_value", "register_client", "oauth_start", "oauth_finish", "check")
MCP_PROTOCOL_VERSION = "2025-06-18"
API_TARGET = "the vendor's REST API"
MCP_TARGET = "the vendor's hosted MCP server (the remote MCP URL an MCP client connects to)"
MCP_DOCS = "Find the hosted MCP server's URL in the vendor's own docs (WebSearch, WebFetch)."
BUILTIN_TOOLS = ("WebSearch", "WebFetch")
# Authorize URL parameters code sets (or must never send): extra_params may not hold them.
RESERVED_AUTHORIZE_PARAMS = frozenset(
    {
        "response_type",
        "client_id",
        "client_secret",
        "redirect_uri",
        "state",
        "code_verifier",
        "code_challenge",
        "code_challenge_method",
    }
)
# read_value names the token exchange uses: a new value voids an exchange made with the old one.
CLIENT_VALUES = ("client_id", "client_secret")

# The secret-like test, shared by the mask and the pointer read: a run of 20+ token characters,
# not a URL or a path of words, with a letter and a digit.
_LOOKS_JS = r"""
const RUN = /[A-Za-z0-9_\-+\/=.~]{12,}/g;
// A short random word: upper and lower case and a digit (12+), or both cases and no digit (24+).
const randomWord = (s) => !/[-_\/.]/.test(s) && /[a-z]/.test(s) && /[A-Z]/.test(s)
  && ((s.length >= 12 && /[0-9]/.test(s)) || s.length >= 24);
const looks = (s) => {
  if (randomWord(s)) return true;
  if (s.length < 20 || s.includes("//") || s.startsWith("/")) return false;
  if (!/[0-9]/.test(s) || !/[A-Za-z]/.test(s)) return false;
  const parts = s.split(/[-_\/.]+/).filter(Boolean);
  if (parts.every((p) => p.length <= 12) && parts.filter((p) => /^[a-z]{3,}$/.test(p)).length * 2 >= parts.length) return false;
  return true;
};
const secretIn = (text) => (text.match(RUN) || []).filter(looks);
// A one-word value of 8+ characters next to a label that names a secret (the pattern above can
// miss a short or letters-only secret): the value itself, or its box up to 2 levels, says so.
const HINT = /secret|token|api[ _-]?key|password|credential|private key/i;
const nearHint = (el, value) => {
  if (!value || value.length < 8 || /\s/.test(value) || value.length > 4096) return false;
  if (value.includes("://") || value.startsWith("/")) return false;
  for (let n = el.parentElement, depth = 0; n && depth < 2; n = n.parentElement, depth += 1) {
    const text = (n.textContent || "").replace(value, "");
    if (text.length < 300 && HINT.test(text)) return true;
  }
  return false;
};
"""

# Installs the mask in a document (an init script, so every new page and frame has it before its
# own scripts run). Each masked element gets data-plato-mask; the style hides its text and value.
# __platoMask.scan() masks what is new and answers {doc, seq}: seq counts the masks of this document.
MASK_INIT_JS = (
    r"""(() => {
  if (window.__platoMask) return;
  const ATTR = "data-plato-mask";
  const CSS = `[${ATTR}], [${ATTR}] * { color: transparent !important; -webkit-text-fill-color: transparent !important;
    text-shadow: none !important; caret-color: transparent !important; -webkit-text-security: disc !important;
    background: #555 !important; border-color: #555 !important; }`;
"""
    + _LOOKS_JS
    + r"""
  const state = { doc: Math.random().toString(36).slice(2), seq: 0 };
  const mark = (el) => { if (el && !el.hasAttribute(ATTR)) { el.setAttribute(ATTR, ""); state.seq += 1; } };
  // Each root's mask stylesheet. A page that removes or edits it gets it back on the next scan, and the
  // restore counts as a change (seq), so no frame goes out until the restored mask has taken effect.
  const styles = new WeakMap();
  const style = (root) => {
    const had = styles.get(root);
    if (had && had.isConnected && had.textContent === CSS && !had.disabled) return;
    const holder = root === document ? (document.head || document.documentElement) : root;
    if (!holder) return;
    const st = document.createElement("style");
    st.textContent = CSS;
    holder.appendChild(st);
    styles.set(root, st);
    if (had) state.seq += 1;
  };
  const scanRoot = (root) => {
    style(root);
    const top = root === document ? document.documentElement : root;
    if (!top) return;
    const walker = document.createTreeWalker(top, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const p = n.parentElement;
      if (!p || p.closest(`[${ATTR}]`) || ["SCRIPT", "STYLE", "NOSCRIPT"].includes(p.tagName)) continue;
      const t = (n.nodeValue || "").trim();
      if (secretIn(t).length || nearHint(p, t)) mark(p);
    }
    for (const el of root.querySelectorAll("input, textarea")) {
      const v = (el.value || "").trim();
      if (!v) continue;
      const named = [el.name, el.id, el.placeholder, el.getAttribute("aria-label"), el.getAttribute("autocomplete")].join(" ");
      const label = (el.labels && el.labels[0] && el.labels[0].textContent) || "";
      if (el.type === "password" || secretIn(v).length || HINT.test(named) || HINT.test(label) || nearHint(el, v)) mark(el);
    }
    for (const el of root.querySelectorAll("[title]")) {
      if (secretIn(el.getAttribute("title") || "").length) el.removeAttribute("title");
    }
    for (const el of root.querySelectorAll("*")) if (el.shadowRoot) scanRoot(el.shadowRoot);
  };
  const scan = () => { if (document.documentElement) scanRoot(document); return { doc: state.doc, seq: state.seq }; };
  let pending = false;
  const soon = () => { if (!pending) { pending = true; requestAnimationFrame(() => { pending = false; scan(); }); } };
  const pointer = { x: -1, y: -1, at: 0 };
  const track = (e) => { pointer.x = e.clientX; pointer.y = e.clientY; pointer.at = performance.timeOrigin + performance.now(); };
  document.addEventListener("mousemove", track, true);
  document.addEventListener("pointermove", track, true);
  window.__platoMask = { scan, pointer, mark };
  new MutationObserver(soon).observe(document, {
    subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ["type", "value", "title"],
  });
  document.addEventListener("input", soon, true);
  setInterval(scan, 100);
  scan();
})()"""
)
MASK_SCAN_JS = "() => (window.__platoMask ? window.__platoMask.scan() : null)"
# A query parameter that carries a code or a token: the address bar is no page element, so no
# frame goes out while the URL holds one.
URL_SECRET_JS = (
    r"""() => /[?&#](code|token|access_token|refresh_token|id_token|client_secret|secret)=/i.test(location.href)"""
)

# The value at the mouse pointer (the last mouse move this document saw, from the mask script):
# the element there, or one masked value in the small box (up to 4 levels) around it. secret false: also an
# unmasked input value or one word of text. ``at`` (epoch ms) picks the frame the pointer is in.
POINTER_READ_JS = (
    r"""(secret) => {
  const ATTR = "data-plato-mask";
"""
    + _LOOKS_JS
    + r"""
  const pt = window.__platoMask && window.__platoMask.pointer;
  if (!pt || pt.at === 0) return { found: false, at: 0, why: "the mouse has not moved over this page" };
  const el = document.elementFromPoint(pt.x, pt.y);
  if (!el) return { found: false, at: pt.at, why: "nothing is under the mouse pointer" };
  if (el.tagName === "IFRAME" || el.tagName === "FRAME") return { found: false, at: 0, frame: true };
  // A masked element's value: an input's value, the element's text when it is one word (the
  // mask may have hidden a short or letters-only secret by its label), else its one secret run.
  const valueOf = (node) => {
    if (node.tagName === "INPUT" || node.tagName === "TEXTAREA") return (node.value || "").trim();
    const text = (node.textContent || "").trim();
    if (text && !/\s/.test(text) && text.length <= 4096) return text;
    const runs = secretIn(text);
    return runs.length === 1 ? runs[0] : "";
  };
  const markOne = (node) => (window.__platoMask ? window.__platoMask.mark(node) : node.setAttribute(ATTR, ""));
  if ((el.tagName === "INPUT" || el.tagName === "TEXTAREA") && (el.value || "").trim().length >= (secret ? 8 : 1)) {
    if (secret && !el.hasAttribute(ATTR)) markOne(el);
    return { found: true, at: pt.at, value: el.value.trim() };
  }
  for (let n = el, depth = 0; n && depth < 4; n = n.parentElement, depth += 1) {
    const box = n.getBoundingClientRect();
    if (n === document.body || n === document.documentElement || (depth > 0 && box.width * box.height > 250000)) break;
    const masked = n.hasAttribute(ATTR) ? [n] : [...n.querySelectorAll(`[${ATTR}]`)].filter((m) => !m.querySelector(`[${ATTR}]`));
    if (masked.length > 1) return { found: false, at: pt.at, why: "several masked values are near the pointer: point at the value itself" };
    if (masked.length === 1) {
      const v = valueOf(masked[0]);
      if (v) return { found: true, at: pt.at, value: v };
    }
    if (!secret && depth === 0) {
      const t = (n.textContent || "").trim();
      if (t && !/\s/.test(t) && t.length <= 512) return { found: true, at: pt.at, value: t };
    }
  }
  return { found: false, at: pt.at, why: "no value is under the mouse pointer" };
}"""
)

# The input that has focus, as the sign-in fill needs it. No value.
FOCUSED_EL_JS = "() => document.activeElement"
FOCUSED_JS = r"""(el) => {
  if (!el || !el.isConnected || !document.hasFocus() || el !== document.activeElement) return null;
  if (el === document.body) return null;
  if (el.tagName === "IFRAME" || el.tagName === "FRAME") return { frame: true };
  return {
    tag: el.tagName,
    type: (el.getAttribute("type") || "text").toLowerCase(),
    autocomplete: (el.getAttribute("autocomplete") || "").toLowerCase(),
    usable: !el.disabled && !el.readOnly && !!(el.offsetWidth || el.offsetHeight),
    protocol: location.protocol,
    host: location.hostname,
  };
}"""
# Through the mask's own counter, so the screenshot gate sees the new mask.
MARK_FOCUSED_JS = (
    """(el) => (window.__platoMask ? window.__platoMask.mark(el) : el.setAttribute("data-plato-mask", ""))"""
)
# An emailed code split over one box per character: mask every such box of the input's form too.
MARK_CODE_BOXES_JS = r"""(el) => {
  const mark = (e) => (window.__platoMask ? window.__platoMask.mark(e) : e.setAttribute("data-plato-mask", ""));
  const texty = (i) => ["text", "tel", "number", ""].includes((i.getAttribute("type") || "").toLowerCase());
  mark(el);
  // The nearest box (up to 4 levels, or the form) that holds more than this input: every text input
  // in it, whatever its maxlength, since the code can go on into any of them.
  let box = null;
  for (let p = el.parentElement, n = 0; p && n < 4; p = p.parentElement, n++) {
    if (p.querySelectorAll("input").length > 1) { box = p; break; }
  }
  box = box || el.form;
  if (box) for (const i of box.querySelectorAll("input")) if (texty(i)) mark(i);
}"""


class MintError(PortalError):
    """The agent ended without a checked grant. Exit 6."""


class VendorHosts:
    """The vendor's hosts: the vault login URL's host and each ``--vendor-domain``, as given, and
    their subdomains, over https. Code types a vault value, and sends a client secret or a token,
    only to these: a "Continue with Google" page, a link off the vendor or another tenant of a
    shared domain (tenant-b.atlassian.net for a login on tenant-a.atlassian.net) gets nothing."""

    def __init__(self, login_url: str | None, extra_domains: list[str]) -> None:
        hosts = [urlparse(login_url).hostname or ""] if login_url else []
        hosts += [d.strip() for d in extra_domains]
        self.domains = {domain for domain in (h.casefold().strip(".") for h in hosts) if "." in domain}
        if not self.domains:
            raise VaultConsoleError(
                "the vault item has no login_url, so code cannot tell the vendor's pages: pass --vendor-domain"
            )

    def allows_host(self, host: str) -> bool:
        host = host.casefold().strip(".")
        return any(host == d or host.endswith("." + d) for d in self.domains)

    def allows_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.scheme == "https" and self.allows_host(parsed.hostname or "")

    def __str__(self) -> str:
        return ", ".join(sorted(self.domains))


def read_vault_item(
    login_key: str, account: str, chronos_url: str | None, api_key: str | None
) -> Callable[[], VaultItem]:
    """One Chronos read of the vault item, on first use, then kept in memory for the command."""
    box: list[VaultItem] = []
    lock = threading.Lock()

    def read() -> VaultItem:
        with lock:
            if box:
                return box[0]
            key = api_key or os.environ.get("PLATO_API_KEY") or None
            if not key:
                raise VaultConsoleError("mint reads the vault item: set PLATO_API_KEY or pass --api-key")
            url = chronos_url_of(chronos_url)
            vault = LoginVault(api_key=key, base_url=url, session_id=os.environ.get(SESSION_ID_ENV_VAR) or None)
            try:
                with chronos_errors(url):
                    found = vault.get_account(login_key, account)
            finally:
                vault.close()
            if found is None:
                raise NotFound(f"no vault item for {normalize_key(login_key)}/{normalize_key(account)}")
            box.append(
                VaultItem(
                    username=found.username,
                    password=SecretStr(found.password) if found.password else None,
                    totp_seed=SecretStr(found.totp_seed) if found.totp_seed else None,
                    login_url=found.login_url,
                    login_email=getattr(found, "login_email", None),
                )
            )
            del found
            return box[0]

    return read


def chronos_url_of(chronos_url: str | None) -> str:
    return (chronos_url or get_settings().chronos_url).rstrip("/")


class MaskWatch:
    """The mask in every page and frame of the Pi browser, run on the page thread.
    :meth:`masked_new` is the :class:`pi_desktop_adapter.MaskGate` check."""

    def __init__(self, driver: pi_browser.PiDriver) -> None:
        self._driver = driver
        self._seen: dict[str, int] = {}
        # A change a scan outside the gate saw (a read or a fill): the gate's next check reports it.
        self._unreported = False

    def install(self) -> None:
        context = self._driver._page().context
        pi_browser.limited(
            context, pi_browser.PAGE_CALL_TIMEOUT_S, "the mask script", lambda: context.add_init_script(MASK_INIT_JS)
        )
        self.masked_new()

    def _frames(self) -> list[Any]:
        context = self._driver._page().context
        return [frame for page in context.pages for frame in page.frames]

    def masked_new(self) -> bool:
        """The gate's check: :meth:`scan`, plus a change a scan outside the gate saw since."""
        unreported, self._unreported = self._unreported, False
        return self.scan() or unreported

    def scan_for_step(self) -> None:
        """A scan after a step masked a value (a read or a fill): the gate's next check refuses
        the frame and waits for the repaint, even though this scan took the new count."""
        if self.scan():
            self._unreported = True

    def scan(self) -> bool:
        """Mask what is new in every frame. True when this frame of the screen may show a value
        unmasked: a new mask since the last scan, a secret in a URL, or a frame code cannot read."""
        refuse = False
        for frame in self._frames():
            try:
                got = pi_browser.limited(
                    frame, pi_browser.PAGE_CALL_TIMEOUT_S, "the mask scan", lambda f=frame: f.evaluate(MASK_SCAN_JS)
                )
                if got is None:
                    pi_browser.limited(
                        frame,
                        pi_browser.PAGE_CALL_TIMEOUT_S,
                        "the mask script",
                        lambda f=frame: f.evaluate(MASK_INIT_JS),
                    )
                    got = frame.evaluate(MASK_SCAN_JS)
                if frame.parent_frame is None and frame.evaluate(URL_SECRET_JS):
                    refuse = True
            except Exception:
                return True
            if not isinstance(got, dict):
                return True
            doc, seq = str(got.get("doc")), int(got.get("seq") or 0)
            if self._seen.get(doc, 0) != seq:
                self._seen[doc] = seq
                refuse = True
        return refuse


class MintSession:
    """What code holds during one mint: the read values, the OAuth state and tokens, the
    passed check. The page steps run on the page thread (through :class:`pi_browser.PageJobs`);
    ``oauth_finish`` and ``check`` run on the tool server's thread. Replies carry no secret."""

    def __init__(
        self,
        driver: pi_browser.PiDriver,
        item: Callable[[], VaultItem],
        hosts: VendorHosts,
        http: httpx.Client,
        email_code: mail_code.EmailCodeReader | None = None,
    ) -> None:
        self.driver = driver
        self.item = item
        self.hosts = hosts
        self.http = http
        self.email_code = email_code
        self.watch = MaskWatch(driver)
        self.values: dict[str, SecretStr] = {}
        self.oauth: OAuthSpec | None = None
        self.tokens: OAuthTokens | None = None
        self.passed: CheckInput | None = None
        self.agent_check: CheckResult | None = None
        self._pkce: PkcePair | None = None
        self._listener: app_oauth.CallbackListener | None = None
        # The consent in progress: bumped by oauth_start and by a client credential change, so an
        # exchange that finishes after either stores nothing.
        self._exchange = 0
        self._client: tuple[SecretStr, SecretStr | None] | None = None
        # The client register_client made, with the server it found.
        self._registered: tuple[mint_dcr.Discovered, mint_dcr.RegisteredClient] | None = None
        self._lock = threading.Lock()

    # -- page thread -------------------------------------------------------------------------

    @staticmethod
    def _input_info(element: Any) -> FocusedInput | None:
        got = pi_browser.limited(
            element, pi_browser.PAGE_CALL_TIMEOUT_S, "the focus read", lambda: element.evaluate(FOCUSED_JS)
        )
        return FocusedInput.model_validate(got) if isinstance(got, dict) else None

    def _focused(self) -> tuple[Any, FocusedInput] | None:
        """The focused input as a handle bound to its document, and what it is. A handle whose
        document navigated away fails every later call, so a fill through it cannot land on the
        next page."""
        for frame in self.driver._page().frames:
            handle = pi_browser.limited(
                frame,
                pi_browser.PAGE_CALL_TIMEOUT_S,
                "the focus read",
                lambda f=frame: f.evaluate_handle(FOCUSED_EL_JS),
            )
            element = handle.as_element()
            got = self._input_info(element) if element is not None else None
            if got is not None and not got.frame:
                return element, got
            handle.dispose()
        return None

    def fill(self, field: SignInField) -> ToolReply:
        found = self._focused()
        if found is None:
            return _fail("no input has focus: click into the field first, then call fill_sign_in")
        element, info = found
        try:
            return self._fill(field, element, info)
        finally:
            with suppress(Exception):
                element.dispose()

    def _fill(self, field: SignInField, element: Any, info: FocusedInput) -> ToolReply:
        if info.protocol != "https:" or not self.hosts.allows_host(info.host):
            return _fail(f"code types vault values only on the vendor's https pages ({self.hosts}), not on this page")
        if info.tag != "INPUT" or not info.usable:
            return _fail("the focused element is not an input that takes text")
        kind, auto = info.type, info.autocomplete
        item = self.item()
        value: SecretStr | None
        if field == SignInField.username:
            if kind == "password":
                return _fail("that is a password input: call fill_sign_in with field password")
            value = SecretStr(item.username) if item.username else None
        elif field == SignInField.password:
            if kind != "password" or auto == "new-password":
                return _fail("the focused input is not a sign-in password input")
            value = item.password
        elif field == SignInField.email_code:
            if kind not in ("text", "tel", "number") or auto in ("current-password", "new-password", "username"):
                return _fail("the focused input is not a one-time-code input")
            if self.email_code is None:
                return _fail("code reads no inbox in this run: end with need_person")
            try:
                value = self.email_code.wait()
            except mail_code.MailCodeError as e:
                return _fail(f"{e}: end with need_person")
            if value is None:
                return _fail(
                    f"no code came by email within {mail_code.WAIT_S:.0f} s: have the page send it "
                    "(or send it again), then call fill_sign_in with email_code again"
                )
        else:
            if kind not in ("text", "tel", "number") or auto in ("current-password", "new-password", "username"):
                return _fail("the focused input is not a one-time-code input")
            if item.totp_seed is None:
                return _fail("the vault item has no authenticator seed: end with need_person")
            code, _ = totp_code.fresh_code(item.totp_seed, TotpParams(), min_left_s=CODE_MIN_LEFT_S)
            value = SecretStr(code)
        if value is None:
            return _fail(f"the vault item has no {field.value}: end with need_person")
        with self.driver.secret_lock():
            try:
                # The code wait above can outlast a redirect: the checked input must still hold
                # focus in the checked document.
                if self._input_info(element) != info:
                    return _fail("the page or its focus changed: click into the field again, then call fill_sign_in")
                if field == SignInField.email_code:
                    # Mask the boxes before the first key: the code shows in each as it is typed.
                    element.evaluate(MARK_CODE_BOXES_JS)
                    # Key by key from the focused box: one box per character moves focus itself.
                    text = value.get_secret_value()
                    pi_browser.limited(
                        element,
                        len(text) * CODE_KEY_DELAY_MS / 1000 + FILL_TIMEOUT_MS / 1000 + pi_browser.PAGE_CALL_MARGIN_S,
                        "the fill",
                        lambda: element.type(text, delay=CODE_KEY_DELAY_MS, timeout=FILL_TIMEOUT_MS),
                    )
                else:
                    pi_browser.limited(
                        element,
                        FILL_TIMEOUT_MS / 1000 + pi_browser.PAGE_CALL_MARGIN_S,
                        "the fill",
                        lambda: element.fill(value.get_secret_value(), timeout=FILL_TIMEOUT_MS),
                    )
            except PortalError:
                raise
            except Exception:
                return _fail("code could not type into the focused input")
            if field == SignInField.email_code and self.email_code is not None:
                self.email_code.typed()
                element.evaluate(MARK_CODE_BOXES_JS)
                self.watch.scan_for_step()
            elif field != SignInField.username:
                element.evaluate(MARK_FOCUSED_JS)
                self.watch.scan_for_step()
        return ToolReply(ok=True, filled=field, next="click the page's continue or sign-in button")

    def read(self, name: str, secret: bool) -> ToolReply:
        got: dict[str, Any] | None = None
        with self.driver.secret_lock():
            for frame in self.driver._page().frames:
                one = pi_browser.limited(
                    frame,
                    pi_browser.PAGE_CALL_TIMEOUT_S,
                    "the pointer read",
                    lambda f=frame: f.evaluate(POINTER_READ_JS, secret),
                )
                # The frame whose document saw the last mouse move holds the pointer.
                if isinstance(one, dict) and float(one.get("at") or 0) > float((got or {}).get("at") or 0):
                    got = one
            self.watch.scan_for_step()
        if not got or not got.get("found"):
            return _fail(str((got or {}).get("why") or "no value is under the mouse pointer"))
        value = SecretStr(str(got.get("value") or ""))
        del got
        warning = None
        with self._lock:
            old = self.values.get(name)
            self.values[name] = value
            if name in CLIENT_VALUES and old is not None and old.get_secret_value() != value.get_secret_value():
                if self.tokens is not None or self._client is not None:
                    warning = f"{name} changed: the earlier consent is void, run oauth_start again"
                self._exchange += 1
                self._client = None
                self.tokens = None
                self.passed = None
                self.agent_check = None
                self._close_listener()
        return ToolReply(
            ok=True,
            name=name,
            length=len(value.get_secret_value()),
            starts_with=None if secret else value.get_secret_value()[:4],
            warning=warning,
        )

    def _current_registration(self) -> tuple[mint_dcr.Discovered, mint_dcr.RegisteredClient] | None:
        """register_client's client while it is still the client_id in use."""
        registered, client_id = self._registered, self.values.get("client_id")
        if registered is None or client_id is None:
            return None
        if registered[1].client_id.get_secret_value() != client_id.get_secret_value():
            return None
        return registered

    def oauth_start(self, spec: OAuthStartInput) -> ToolReply:
        for what, url in (("authorize_url", spec.authorize_url), ("token_url", spec.token_url)):
            if not self.hosts.allows_url(url):
                return _fail(f"{what} must be an https URL of the vendor ({self.hosts})")
        public = spec.client_auth == ClientAuth.none
        needed = ("client_id",) if public else ("client_id", "client_secret")
        missing = [n for n in needed if n not in self.values]
        if missing:
            return _fail(f"read these first with read_value: {', '.join(missing)}")
        if public and not spec.pkce:
            return _fail("a public client (client_auth none) needs PKCE: pkce true")
        with self._lock:
            registered = self._current_registration()
        resource = registered[0].resource if registered else None
        if registered is not None:
            found, client_reg = registered
            if spec.token_url != found.metadata.token_endpoint or spec.client_auth != client_reg.client_auth:
                return _fail(
                    "the registered client works only with the token_url and client_auth register_client "
                    f"answered ({found.metadata.token_endpoint}, {client_reg.client_auth.value})"
                )
        reserved_params = RESERVED_AUTHORIZE_PARAMS | ({"scope"} if spec.scopes else set())
        if resource:
            reserved_params |= {"resource"}
        reserved = sorted(set(spec.extra_params) & reserved_params)
        if reserved:
            return _fail(f"code sets these itself, drop them from extra_params: {', '.join(reserved)}")
        self._close_listener()
        with self._lock:
            client = (self.values["client_id"], None if public else self.values["client_secret"])
            self._exchange += 1
            self._client = client
            # A new consent: a check of an earlier token approves nothing.
            self.tokens = None
            self.passed = None
            self.agent_check = None
        state = app_oauth.new_state()
        params = {
            "response_type": "code",
            "client_id": client[0].get_secret_value(),
            "redirect_uri": MINT_REDIRECT_URI,
            "state": state,
            **spec.extra_params,
        }
        if spec.scopes:
            params["scope"] = spec.scope_separator.join(spec.scopes)
        if resource:
            params["resource"] = resource
        self._pkce = app_oauth.make_pkce() if spec.pkce else None
        if self._pkce is not None:
            params.update(code_challenge=self._pkce.challenge, code_challenge_method=self._pkce.method)
        listener = app_oauth.CallbackListener(MINT_REDIRECT_URI, state)
        listener.__enter__()
        self._listener = listener
        self.oauth = OAuthSpec(
            authorize_url=spec.authorize_url,
            token_url=spec.token_url,
            scopes=spec.scopes,
            client_auth=spec.client_auth,
            resource=resource,
        )
        self.driver.route_callback(MINT_REDIRECT_URI)
        sep = "&" if "?" in spec.authorize_url else "?"
        self.driver.goto(f"{spec.authorize_url}{sep}{urlencode(params)}")
        return ToolReply(
            ok=True,
            next="handle the consent page (pick the site or workspace if asked, then allow), then call oauth_finish",
        )

    # -- tool server thread ------------------------------------------------------------------

    def register_client(self, server_url: str) -> ToolReply:
        """Discover the server's OAuth metadata and register a client: its id (and secret) take
        the place of read values, as if read from a developer console."""
        if not self.hosts.allows_url(server_url):
            return _fail(f"server_url must be an https URL of the vendor ({self.hosts})")
        try:
            found = mint_dcr.discover(self.http, server_url)
            meta = found.metadata
            for what, url in (
                ("authorization_endpoint", meta.authorization_endpoint),
                ("token_endpoint", meta.token_endpoint),
                ("registration_endpoint", meta.registration_endpoint),
            ):
                if url is not None and not self.hosts.allows_url(url):
                    return _fail(f"the server's {what} is not on the vendor's hosts ({self.hosts}): nothing registered")
            client = mint_dcr.register(self.http, found, MINT_REDIRECT_URI, MINT_LABEL)
        except mint_dcr.DcrError as e:
            return _fail(str(e))
        with self._lock:
            self.values["client_id"] = client.client_id
            if client.client_secret is not None:
                self.values["client_secret"] = client.client_secret
            else:
                self.values.pop("client_secret", None)
            self._registered = (found, client)
            self._exchange += 1
            self._client = None
            self.tokens = None
            self.passed = None
            self.agent_check = None
            self._close_listener()
        expires = client.client_secret_expires_at
        return ToolReply(
            ok=True,
            name="client_id",
            length=len(client.client_id.get_secret_value()),
            server=RegisteredServer(
                authorize_url=meta.authorization_endpoint,
                token_url=meta.token_endpoint,
                client_auth=client.client_auth,
                scopes_supported=found.scopes,
            ),
            next="call oauth_start with this authorize_url, token_url and client_auth and pkce true (scopes: the "
            "ones the server or its docs name for full access, with what it needs for a refresh token; none if "
            "it names none), then handle the consent page",
            warning="the client secret expires, and the grant stops refreshing then" if expires else None,
        )

    def oauth_finish(self, timeout_s: int) -> ToolReply:
        with self._lock:
            listener, spec, client, exchange = self._listener, self.oauth, self._client, self._exchange
        if listener is None or spec is None or client is None:
            return _fail("call oauth_start first")
        try:
            code = listener.wait(float(timeout_s))
        except app_oauth.OAuthError as e:
            return _fail(str(e))
        finally:
            self._close_listener(listener)
        data = {"grant_type": "authorization_code", "code": code, "redirect_uri": MINT_REDIRECT_URI}
        if self._pkce is not None:
            data["code_verifier"] = self._pkce.verifier.get_secret_value()
        if spec.resource:
            data["resource"] = spec.resource
        client_id, secret = client[0].get_secret_value(), client[1].get_secret_value() if client[1] else ""
        extra: dict[str, Any] = {}
        if spec.client_auth == ClientAuth.none:
            data["client_id"] = client_id
        elif spec.client_auth == ClientAuth.basic:
            extra["auth"] = httpx.BasicAuth(client_id, secret)
        else:
            data.update(client_id=client_id, client_secret=secret)
        try:
            response = self.http.post(spec.token_url, data=data, headers={"Accept": "application/json"}, **extra)
        except httpx.HTTPError as e:
            return _fail(f"the token call got no answer ({type(e).__name__}); run oauth_start again")
        if response.status_code != 200:
            return _fail(f"the token call failed: HTTP {response.status_code} {app_oauth._error_code(response)}")
        try:
            body = response.json()
        except ValueError:
            return _fail("the token reply is not JSON")
        if isinstance(body, dict) and body.get("ok") is False:
            # Slack answers an error as HTTP 200 with ok: false.
            return _fail(f"the token call failed: {app_portal.redact(str(body.get('error') or 'ok: false'))}")
        try:
            grant = TokenGrant.model_validate(user_grant(body))
        except ValidationError:
            return _fail("the token reply is not a token grant")
        expires = datetime.now(UTC) + timedelta(seconds=grant.expires_in) if grant.expires_in else None
        with self._lock:
            if self._exchange != exchange:
                return _fail(
                    "the consent was voided (new client credentials or a new oauth_start): run oauth_start again"
                )
            self.passed = None
            self.agent_check = None
            self.tokens = OAuthTokens(
                access_token=grant.access_token,
                refresh_token=grant.refresh_token,
                expires_at=expires,
                scope=grant.scope,
                client_id=client[0],
                client_secret=client[1],
            )
        return ToolReply(
            ok=True,
            has_refresh_token=grant.refresh_token is not None,
            expires_in=grant.expires_in,
            scopes=len((grant.scope or "").split()),
            next="call check with a 'who am I' endpoint",
            warning=None
            if grant.refresh_token is not None
            else "no refresh token: the login vault keeps only grants with one. Ask for offline access "
            "(e.g. an offline_access scope or access_type=offline) and run oauth_start again",
        )

    def check(self, args: CheckInput) -> ToolReply:
        if self.tokens is None:
            return _fail("run oauth_start and oauth_finish first")
        result = self.run_check(args, self.tokens.access_token)
        why = self.check_refusal(result)
        if result.ok and why is None:
            self.passed = args
            self.agent_check = result
        else:
            self.passed = None
            self.agent_check = None
        if self.identity_match(result) is False:
            # The browser is signed in as someone else: its cookies must not be saved as this account's.
            self.driver.discard_login()
        if result.ok and why is not None:
            return ToolReply(ok=False, status=result.status, identity=result.identity, tools=result.tools, error=why)
        return ToolReply(
            ok=result.ok, status=result.status, identity=result.identity, tools=result.tools, error=result.error
        )

    def check_refusal(self, result: CheckResult) -> str | None:
        """Why a successful check reply does not prove whose account the grant reaches, or None."""
        if self.identity_match(result) is False:
            return "the reply names another account than the vault item's: this grant is not stored"
        if not result.identity.names_account():
            return (
                "the reply names no account (no email, user id or login): call check with a 'who am I' "
                "endpoint that returns the signed-in user"
            )
        return None

    def run_check(self, check: CheckInput, token: SecretStr) -> CheckResult:
        if check.mcp_tool:
            return mcp_check(self.http, self.hosts, check.url, check.mcp_tool, token)
        return vendor_check(self.http, self.hosts, check.url, token)

    def identity_match(self, result: CheckResult) -> bool | None:
        """False when the reply shows an email and none is the vault username; None when it shows none."""
        emails = result.identity.emails()
        if not emails:
            return None
        username = (self.item().username or "").casefold()
        return username in emails

    def _close_listener(self, listener: app_oauth.CallbackListener | None = None) -> None:
        """Close the current callback listener. With ``listener``: only if it is still the
        current one (a newer oauth_start already closed it and owns the new one)."""
        current = self._listener
        if current is None or (listener is not None and current is not listener):
            return
        self._listener = None
        current.__exit__(None, None, None)

    def close(self) -> None:
        self._close_listener()


def vendor_check(http: httpx.Client, hosts: VendorHosts, url: str, token: SecretStr) -> CheckResult:
    """GET ``url`` with the bearer token: the status and the reply's identity fields."""
    if not hosts.allows_url(url):
        return CheckResult(error=f"the check URL must be an https URL of the vendor ({hosts})")
    headers = {
        "Accept": "application/json",
        "User-Agent": "plato-vault-mint",
        "Authorization": f"Bearer {token.get_secret_value()}",
    }
    try:
        response = http.get(url, headers=headers, timeout=CHECK_TIMEOUT_S)
    except httpx.HTTPError as e:
        return CheckResult(error=f"no answer ({type(e).__name__})")
    finally:
        del headers
    return CheckResult(status=response.status_code, identity=_identity(response))


class McpSession:
    """JSON-RPC over an MCP server's streamable HTTP endpoint, with a bearer token. A reply comes
    as JSON or as an event stream whose ``data:`` lines carry it."""

    def __init__(self, http: httpx.Client, url: str, token: SecretStr) -> None:
        self._http = http
        self._url = url
        self._token = token
        self._session_id: str | None = None
        self._next_id = 0

    def call(self, method: str, params: dict[str, Any]) -> tuple[int, RpcReply | None]:
        """The HTTP status and the JSON-RPC reply to this request (None when there is none)."""
        self._next_id += 1
        response = self._post({"jsonrpc": "2.0", "id": self._next_id, "method": method, "params": params})
        if self._session_id is None:
            self._session_id = response.headers.get("mcp-session-id")
        return response.status_code, _rpc_reply(response, self._next_id)

    def notify(self, method: str) -> None:
        self._post({"jsonrpc": "2.0", "method": method})

    def _post(self, body: dict[str, Any]) -> httpx.Response:
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "User-Agent": "plato-vault-mint",
            "Authorization": f"Bearer {self._token.get_secret_value()}",
            "MCP-Protocol-Version": MCP_PROTOCOL_VERSION,
        }
        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id
        try:
            return self._http.post(self._url, json=body, headers=headers, timeout=CHECK_TIMEOUT_S)
        finally:
            del headers


def _rpc_reply(response: httpx.Response, request_id: int) -> RpcReply | None:
    if "text/event-stream" in response.headers.get("content-type", ""):
        bodies = [line[5:] for line in response.text.splitlines() if line.startswith("data:")]
    else:
        bodies = [response.text]
    for body in bodies:
        try:
            reply = RpcReply.model_validate_json(body)
        except ValidationError:
            continue
        if reply.id == request_id:
            return reply
    return None


M = TypeVar("M", bound=BaseModel)


def _rpc_result(model: type[M], reply: RpcReply | None) -> M | None:
    """The reply's result as ``model``; None for an error reply, no reply or an unreadable result."""
    if reply is None or reply.result is None:
        return None
    try:
        return model.model_validate(reply.result)
    except ValidationError:
        return None


def mcp_check(http: httpx.Client, hosts: VendorHosts, url: str, tool: str, token: SecretStr) -> CheckResult:
    """An MCP server check: initialize, tools/list (every page) and a tools/call of ``tool``,
    which the server must mark read-only and which must take no required input. The status is
    the last HTTP status; a JSON-RPC or tool error fails it with that status."""
    if not hosts.allows_url(url):
        return CheckResult(error=f"the MCP server URL must be an https URL of the vendor ({hosts})")
    mcp = McpSession(http, url, token)
    tools: list[McpTool] = []
    try:
        status, reply = mcp.call(
            "initialize",
            {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "plato-vault-mint", "version": "1"},
            },
        )
        if status != 200 or reply is None or reply.result is None:
            return CheckResult(status=status, error=None if status != 200 else "initialize answered no result")
        mcp.notify("notifications/initialized")
        cursor: str | None = None
        seen: set[str] = set()
        while True:
            status, reply = mcp.call("tools/list", {"cursor": cursor} if cursor else {})
            page = _rpc_result(McpToolList, reply)
            if status != 200 or page is None:
                return CheckResult(status=status, error=None if status != 200 else "tools/list answered no tool list")
            tools += page.tools
            cursor = page.nextCursor
            if not cursor or cursor in seen:
                break
            seen.add(cursor)
        found = next((t for t in tools if t.name == tool), None)
        if found is None:
            return CheckResult(status=status, tools=len(tools), error=f"the server lists no tool {tool}")
        if found.annotations is None or found.annotations.readOnlyHint is not True:
            return CheckResult(status=status, tools=len(tools), error=f"the server does not mark {tool} read-only")
        if found.inputSchema.required:
            return CheckResult(status=status, tools=len(tools), error=f"{tool} needs input: pick one that takes none")
        status, reply = mcp.call("tools/call", {"name": tool, "arguments": {}})
    except httpx.HTTPError as e:
        return CheckResult(error=f"no answer ({type(e).__name__})")
    result = _rpc_result(McpToolResult, reply)
    if status != 200 or result is None:
        return CheckResult(
            status=status, tools=len(tools), error=None if status != 200 else f"{tool} answered no tool result"
        )
    if result.isError:
        return CheckResult(status=status, tools=len(tools), error=f"{tool} answered an error")
    return CheckResult(status=status, tools=len(tools), identity=_tool_identity(result))


def _tool_identity(result: McpToolResult) -> CheckIdentity:
    """The identity fields of a tools/call result: its structured content, else the first text
    part that is JSON."""
    if result.structuredContent is not None:
        return _identity_of(result.structuredContent)
    for part in result.content:
        if part.type == "text" and part.text:
            try:
                return _identity_of(json.loads(part.text))
            except ValueError:
                continue
    return CheckIdentity()


def _fail(why: str) -> ToolReply:
    return ToolReply(ok=False, error=why)


def _identity(response: httpx.Response) -> CheckIdentity:
    try:
        body = response.json()
    except ValueError:
        return CheckIdentity()
    return _identity_of(body)


def _identity_of(body: Any) -> CheckIdentity:
    if isinstance(body, list):
        body = body[0] if body and isinstance(body[0], dict) else {}
    if not isinstance(body, dict):
        return CheckIdentity()
    out: dict[str, str] = {}
    for scope in [body, *(v for v in body.values() if isinstance(v, dict))]:
        for key in CheckIdentity.model_fields:
            value = scope.get(key)
            if isinstance(value, str | int) and not isinstance(value, bool) and key not in out:
                out[key] = str(value)
    return CheckIdentity.model_validate(out)


class MintToolServer(ToolServer):
    """The agent's ``vault`` MCP server. A page step goes to the page thread through ``jobs``;
    an error becomes ``{"ok": false, "error": ...}`` (no message holds a value)."""

    name = SERVER_NAME

    def __init__(self, session: MintSession, jobs: pi_browser.PageJobs) -> None:
        self._session = session
        self._jobs = jobs
        super().__init__(name="Plato vault", host="127.0.0.1", port=pi_browser.free_local_port())

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}{self.mcp_path()}"

    def build_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="fill_sign_in",
                description="Code types the vault item's username, password or authenticator code, or email_code: "
                "the code the vendor just emailed (code reads the inbox, waiting up to 90 s), into the input that "
                "has focus now (click into it first; for a code split over boxes, the first box). You never type "
                "these. Then click the page's button.",
                input_model=FillInput,
                handler=self._fill,
            ),
            ToolDefinition(
                name="read_value",
                description="Code reads the value under the mouse pointer (move the mouse onto it first, no click) "
                "and keeps it under this name. Answers its length only.",
                input_model=ReadInput,
                handler=self._read,
            ),
            ToolDefinition(
                name="register_client",
                description="For a server that registers OAuth clients itself (a hosted MCP server, most often): code "
                "reads its OAuth metadata and registers a client for the redirect URI "
                f"{MINT_REDIRECT_URI}, in place of an app made in a developer console. Answers the authorize_url, "
                "token_url and client_auth to pass to oauth_start.",
                input_model=RegisterInput,
                handler=self._register,
            ),
            ToolDefinition(
                name="oauth_start",
                description="Code opens the vendor's authorize URL in the browser with the client id read before, "
                f"the redirect URI {MINT_REDIRECT_URI}, PKCE and a state. Then handle the consent page.",
                input_model=OAuthStartInput,
                handler=self._oauth_start,
            ),
            ToolDefinition(
                name="oauth_finish",
                description="Code waits for the consent redirect and exchanges the code for tokens "
                "(kept as access_token).",
                input_model=OAuthFinishInput,
                handler=self._oauth_finish,
            ),
            ToolDefinition(
                name="check",
                description="Code calls a GET endpoint of the vendor's API with the credential and answers the "
                "HTTP status and the identity fields of the reply.",
                input_model=CheckInput,
                handler=self._check,
            ),
        ]

    def _on_page(self, fn: Callable[[], ToolReply]) -> ToolReply:
        try:
            return self._jobs.call(fn, PAGE_JOB_TIMEOUT_S)
        except VaultConsoleError as e:
            return _fail(str(e))

    async def _page(self, fn: Callable[[], ToolReply]) -> dict[str, Any]:
        return _out(await asyncio.to_thread(self._on_page, fn))

    async def _fill(self, args: FillInput) -> dict[str, Any]:
        return await self._page(partial(self._session.fill, args.field))

    async def _read(self, args: ReadInput) -> dict[str, Any]:
        return await self._page(partial(self._session.read, args.name, args.secret))

    async def _register(self, args: RegisterInput) -> dict[str, Any]:
        return _out(await asyncio.to_thread(self._session.register_client, args.server_url))

    async def _oauth_start(self, args: OAuthStartInput) -> dict[str, Any]:
        return await self._page(partial(self._session.oauth_start, args))

    async def _oauth_finish(self, args: OAuthFinishInput) -> dict[str, Any]:
        return _out(await asyncio.to_thread(self._session.oauth_finish, args.timeout_s))

    async def _check(self, args: CheckInput) -> dict[str, Any]:
        return _out(await asyncio.to_thread(self._session.check, args))


def user_grant(body: Any) -> Any:
    """The account's own token in a token reply. Slack's oauth.v2.access puts the user token
    (user scopes, and its refresh token with token rotation) under ``authed_user``, next to an
    optional bot token at the top: the mint acts as the account, so the user token wins."""
    if isinstance(body, dict):
        user = body.get("authed_user")
        if isinstance(user, dict) and user.get("access_token"):
            return user
    return body


def _out(reply: ToolReply) -> dict[str, Any]:
    return reply.model_dump(mode="json", exclude_none=True)


class MintRun(BaseModel):
    """The options of one mint (no secret)."""

    login_key: str
    account: str
    kind: str
    hint: str | None = None
    vendor_domains: list[str] = []
    check_url: str | None = None
    replace: bool = False
    model: str | None = None
    timeout_s: float = MINT_TIMEOUT_S


def mint_goal(run: MintRun, item: VaultItem, plan: DocsPlan | None = None) -> str:
    return render_prompt(
        GoalTemplate.mint_pi,
        target=MCP_TARGET if run.kind == GrantKind.hosted_mcp else API_TARGET,
        docs=MCP_DOCS if run.kind == GrantKind.hosted_mcp else mint_docs.plan_text(plan),
        login_key=run.login_key,
        account=run.account,
        username=item.username or "(no username in the vault item)",
        login_url=item.login_url or "(no login URL in the vault item)",
        label=MINT_LABEL,
        redirect_uri=MINT_REDIRECT_URI,
        hint=f"Note from the person who ran this: {run.hint}" if run.hint else "",
    )


def verify_grant(
    run: MintRun, store: GrantStore, report: MintReport, check: Callable[[str, SecretStr], CheckResult] | None
) -> bool:
    """True when the account's grant is in the vault, active, and its token read answers (Chronos
    refreshes it first when it is due, so a dead refresh token shows here). With ``--check-url``
    the token must also pass that vendor call. False (and ``report.why_mint``) when it must be minted."""
    grant = store.grant(run.login_key, run.account, run.kind)
    if grant is None:
        report.why_mint = f"no {run.kind} grant in the login vault"
        return False
    report.state, report.generation, report.scopes = grant.state, grant.generation, len(grant.scopes)
    if grant.state != "active":
        report.why_mint = f"the {run.kind} grant is {grant.state}"
        return False
    try:
        token = store.token(run.login_key, run.account, run.kind)
    except TokenReadFailed as e:
        if e.status not in GRANT_DEAD_STATUSES:
            raise  # Chronos could not answer: that says nothing about the grant
        report.why_mint = str(e)
        return False
    report.generation, report.refreshed, report.expires_at = token.generation, token.refreshed, token.expires_at
    if check is not None and run.check_url:
        report.check_url = run.check_url
        report.stored_check = check(run.check_url, token.access_token)
        if report.stored_check.status in TOKEN_REFUSED_STATUSES:
            report.why_mint = f"the check answered HTTP {report.stored_check.status}"
            return False
        if not report.stored_check.ok:
            raise MintError(
                f"the check {run.check_url} answered {report.stored_check.status or report.stored_check.error}, "
                "which says nothing about the grant: fix --check-url or try again"
            )
    return True


def verify_only(run: MintRun, item: Callable[[], VaultItem], store: GrantStore) -> MintReport:
    """:func:`verify_grant` alone: the report says ``verified``, or why a mint is needed."""
    report = MintReport(login_key=normalize_key(run.login_key), account=normalize_key(run.account), kind=run.kind)
    hosts = VendorHosts(item().login_url, run.vendor_domains)
    with httpx.Client(timeout=CHECK_TIMEOUT_S) as http:
        if verify_grant(run, store, report, partial(vendor_check, http, hosts)):
            report.outcome = MintOutcome.verified
    return report


def store_grant(run: MintRun, session: MintSession, store: GrantStore, report: MintReport) -> SecretStr:
    """Move the checked grant into the login vault (pausing an active grant it replaces), set it
    active and read its token back through Chronos."""
    oauth, tokens = session.oauth, session.tokens
    assert oauth is not None and tokens is not None
    existing = store.grant(run.login_key, run.account, run.kind)
    paused: int | None = None
    if existing is not None and existing.state == "active":
        # Chronos refuses an import over an active grant.
        paused = store.set_state(run.login_key, run.account, run.kind, "paused", existing.generation).generation
    user_id = session.agent_check.identity.user_id_value() if session.agent_check else None
    try:
        got = store.import_grant(
            run.login_key,
            run.account,
            run.kind,
            oauth,
            tokens.client_id.get_secret_value(),
            tokens.client_secret,
            MINT_REDIRECT_URI,
            tokens,
            user_id,
            session.item().username,
        )
    except StoreRefused:
        if paused is not None:
            # Put back the grant this run paused (the refused import changed nothing).
            store.set_state(run.login_key, run.account, run.kind, "active", paused)
        raise
    active = store.set_state(run.login_key, run.account, run.kind, "active", got.generation)
    token = store.token(run.login_key, run.account, run.kind)
    report.state, report.scopes = active.state, len(active.scopes)
    report.generation, report.refreshed, report.expires_at = token.generation, token.refreshed, token.expires_at
    return token.access_token


def run_mint(
    run: MintRun,
    item: Callable[[], VaultItem],
    store: GrantStore,
    tools: app_portal.PortalTools,
    driver_factory: Callable[[str], pi_browser.PiDriver] | None = None,
    docs_reader: Callable[[str, app_portal.PortalTools], tuple[DocsPlan | None, str | None]] = mint_docs.read_docs,
) -> MintReport:
    """Verify the account's grant; mint it when it is missing or dead (or ``replace``). Raises
    :class:`NeedPerson` when the agent stopped at a page for a person (the window stays in noVNC)."""
    report = MintReport(login_key=normalize_key(run.login_key), account=normalize_key(run.account), kind=run.kind)
    vault_item = item()
    hosts = VendorHosts(vault_item.login_url, run.vendor_domains)
    with httpx.Client(timeout=CHECK_TIMEOUT_S) as http:
        if not run.replace:
            if verify_grant(run, store, report, partial(vendor_check, http, hosts)):
                report.outcome = MintOutcome.verified
                return report
        else:
            report.why_mint = "--replace"
        # The docs step runs before the Pi is taken, on the cheap model; no plan never stops the mint.
        # Its plan is a developer-console app, which a hosted MCP server's registered client replaces.
        if run.kind == GrantKind.hosted_mcp:
            plan, report.docs_note = None, "hosted MCP: the walker finds the server and registers a client"
        else:
            plan, report.docs_note = docs_reader(
                mint_docs.docs_goal(run.login_key, vault_item, run.vendor_domains, run.hint), tools
            )
        report.docs_pages = len(plan.docs) if plan else None
        login = pi_browser.login_slug(run.login_key, run.account)
        driver = driver_factory(login) if driver_factory else pi_browser.PiDriver(tools, login=login)
        driver.open_space(pi_browser.launcher_token(f"mint-{report.login_key}-{report.account}"))
        email_code = mail_code.EmailCodeReader(
            run.account,
            lambda: login_email_of(item().login_email, item().username),
            mail_code.sender_domains(hosts.domains),
        )
        session = MintSession(driver, item, hosts, http, email_code)
        try:
            session.watch.install()
            if vault_item.login_url:
                driver.goto(vault_item.login_url)
            jobs = pi_browser.PageJobs()
            extras = pi_browser.AgentExtras(
                server=lambda: MintToolServer(session, jobs),
                server_tools=MINT_TOOLS,
                builtin_tools=BUILTIN_TOOLS,
                model=run.model,
            )
            line: VaultLine = driver.agent(
                mint_goal(run, vault_item, plan),
                timeout_s=run.timeout_s,
                gate=pi_desktop_adapter.MaskGate(session.watch.masked_new),
                jobs=jobs,
                extras=extras,
            )
            report.summary = line.summary
            report.values = {name: len(v.get_secret_value()) for name, v in session.values.items()}
            report.agent_check = session.agent_check
            report.check_url = session.passed.url if session.passed else None
            if session.passed is None or session.tokens is None:
                why = line.reason or "no check passed with a token from oauth_finish"
                raise MintError(f"the agent ended without a grant: {why}{app_portal.log_hint(driver.last_agent_log)}")
            if session.tokens.refresh_token is None:
                raise MintError(
                    "the vendor gave no refresh token, and the login vault keeps only grants with one: "
                    "the vendor needs a static-token store (not built)"
                )
            token = store_grant(run, session, store, report)
            report.stored_check = session.run_check(session.passed, token)
            if not report.stored_check.ok:
                raise StoreRefused(
                    f"the grant is stored, but the check with the token read back from Chronos answered "
                    f"HTTP {report.stored_check.status or report.stored_check.error}"
                )
            if (why := session.check_refusal(report.stored_check)) is not None:
                raise StoreRefused(f"the grant is stored, but the check with the token read back from Chronos: {why}")
            report.outcome = MintOutcome.minted
            return report
        finally:
            session.close()
            if not driver.handed_off:
                driver.finish()
