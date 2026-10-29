"""The vendor portal step of `plato vault app`, through ego-browser on this Mac.

The agent (``claude -p``) has the Bash tool with ``ego-browser`` commands only, no MCP server, an empty
cwd and no ``PLATO_API_KEY``. Limit: ``ego-browser nodejs`` can still import ``node:fs``, so the store is
safe from the agent only because its goal forbids that (:data:`NO_FILES_RULE`). Never put page text in a goal.
Code does every step that touches a secret, and no model sees one. A script gets no environment, so every
input is a JSON literal in the script. Only the last script of a TaskSpace calls ``finish()``.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, SecretStr, ValidationError

from plato.cli.vault.app_models import ConsentBrowser, CredentialKind, PortalSecretFile, VaultLine, VendorRecipe
from plato.cli.vault.client import VaultConsoleError
from plato.cli.vault.prompts import GoalTemplate, load_prompt, render_prompt

LINE_TAG = "@@VAULT "
NOTICE_TAG = "[ego-browser:notice]"
SCRIPT_TIMEOUT_S = 120.0
AGENT_TIMEOUT_S = 900.0
# claude-seat is the seat-pool wrapper; in zsh `claude` is a shell function around
# it, which a subprocess cannot see, so look for the binaries themselves.
AGENT_CANDIDATES = (str(Path.home() / ".local" / "bin" / "claude-seat"), "claude")
AGENT_ALLOWED_TOOLS = "Bash(ego-browser:*)"
# The only environment the agent gets: enough for claude-seat to pick a seat and
# for claude and ego-browser to run, and claude's own credential where no seat pool is set up.
# No PLATO_API_KEY, no vendor token.
AGENT_ENV_NAMES = (
    "HOME",
    "PATH",
    "USER",
    "LOGNAME",
    "SHELL",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TERM",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "ANTHROPIC_API_KEY",
)
AGENT_ENV_PREFIXES = ("CLAUDE_POOL_", "CLAUDE_SEAT_", "EGO_")
# The consent click (click_consent): how long code waits for the grant button,
# for the redirect after one click, and how many clicks it tries.
CONSENT_BUTTON_WAIT_MS = 60_000
CONSENT_REDIRECT_WAIT_MS = 20_000
CONSENT_CLICKS = 2
CONSENT_SCRIPT_TIMEOUT_S = 180.0
# EgoDriver.pump: ego-browser has no events to handle, so the consent listener only waits.
PUMP_S = 0.25
# Agent logs: ~/.cache/plato-vault-app/agent-<space>-<ts>.log, dir 700, file 600.
AGENT_LOG_DIR = Path(".cache") / "plato-vault-app"
# Token-like strings that the log redaction replaces. The agent never sees a
# secret, but a page snapshot can show a code or a token in a URL.
_REDACT_PATTERNS = (
    # an OAuth value in a query string or a form: keep the name, drop the value
    re.compile(
        r"(?i)\b(code|state|code_verifier|code_challenge|access_token|refresh_token|client_secret|id_token)"
        r"=([^&\s\"'<>]+)"
    ),
    re.compile(r"(?i)otpauth://[^\s\"'<>]+"),  # a TOTP key URI (the seed is in its query)
    re.compile(r"eyJ[A-Za-z0-9_\-.]{10,}"),  # a JWT (Canva access and refresh tokens)
    # A TOTP seed in groups of 4, and a TOTP seed (base32). Any case: the vendor can
    # show the key in lower case. The cost: four 4-letter words in a row are redacted too.
    re.compile(r"(?i)\b[A-Z2-7]{4}(?:[ -][A-Z2-7]{4}){3,}[A-Z2-7]{0,3}\b"),
    re.compile(r"(?i)\b[A-Z2-7]{16,}=*"),
    re.compile(r"cnv[A-Za-z0-9_\-]{8,}"),  # a Canva client secret
    re.compile(r"[A-Za-z0-9_\-]{32,}"),  # a long base64url run
    re.compile(r"[A-Za-z0-9+/]{32,}={0,2}"),  # a long base64 run
)
NO_FILES_RULE = load_prompt(GoalTemplate.no_files)
# The `--browser pi` agent has no file tool and no shell; this rule keeps it in the one
# tab (a new tab or chrome:// page is out of the code steps' sight) and off the CDP port.
PI_SCREEN_RULE = load_prompt(GoalTemplate.pi_screen)


class PortalUnavailable(VaultConsoleError):
    """ego-browser (or the agent) is not installed here. Exit code 2."""

    exit_code = 2


class PortalError(VaultConsoleError):
    """A portal script or agent did not reach its goal. Exit code 6."""

    exit_code = 6


class NeedPerson(PortalError):
    """The browser stopped at a page a person must handle (sign-in, MFA). The TaskSpace
    was handed off, so it stays open. ``reason`` is the agent's ``need_person`` value."""

    def __init__(self, message: str, reason: str | None = None) -> None:
        super().__init__(message)
        self.reason = reason


class PortalTools(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ego: str | None
    agent: str | None


class EgoRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lines: list[VaultLine]
    notice: bool


class PortalResult(BaseModel):
    """What the portal step produced. ``client_secret`` is None when the stored secret was kept."""

    model_config = ConfigDict(extra="forbid")

    app_id: str | None
    client_id: str | None
    client_secret: SecretStr | None
    notice: bool


def find_tools() -> PortalTools:
    agent = next((p for p in (shutil.which(c) for c in AGENT_CANDIDATES) if p), None)
    return PortalTools(ego=shutil.which("ego-browser"), agent=agent)


def agent_env(environ: dict[str, str] | None = None) -> dict[str, str]:
    """The agent's environment: :data:`AGENT_ENV_NAMES` and the :data:`AGENT_ENV_PREFIXES` names only."""
    src = os.environ if environ is None else environ
    return {k: v for k, v in src.items() if k in AGENT_ENV_NAMES or k.startswith(AGENT_ENV_PREFIXES)}


def agent_command(agent: str, goal: str) -> list[str]:
    """``claude -p`` with the Bash tool only, only ``ego-browser`` commands allowed
    (``dontAsk`` refuses the rest, whatever the user's ``defaultMode`` says), and no
    MCP server. ``--allowedTools`` alone adds no limit: it only skips prompts."""
    return [
        agent,
        "-p",
        goal,
        "--tools",
        "Bash",
        "--allowedTools",
        AGENT_ALLOWED_TOOLS,
        "--permission-mode",
        "dontAsk",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
    ]


def redact(text: str) -> str:
    """``text`` with token-like strings replaced by ``<redacted:N>`` (N = the length)."""
    out = _REDACT_PATTERNS[0].sub(lambda m: f"{m.group(1)}=<redacted:{len(m.group(2))}>", text)
    for pattern in _REDACT_PATTERNS[1:]:
        out = pattern.sub(lambda m: f"<redacted:{len(m.group(0))}>", out)
    return out


def agent_log_dir() -> Path:
    return Path.home() / AGENT_LOG_DIR


def write_agent_log(space_id: int | None, header: str, stdout: str, stderr: str) -> Path | None:
    """Keep one agent run's output, redacted, in a new 600 file in a 700 directory.
    None when the file cannot be written: a lost log never fails the command."""
    try:
        root = agent_log_dir()
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        os.chmod(root, 0o700)
        stem = f"agent-{space_id if space_id is not None else 'none'}-{time.strftime('%Y%m%d-%H%M%S')}"
        body = redact(f"{header}\n\n## stdout\n{stdout}\n\n## stderr\n{stderr}\n").encode()
        for n in range(100):
            path = root / (f"{stem}.log" if n == 0 else f"{stem}-{n}.log")
            try:
                fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            except FileExistsError:
                continue
            with os.fdopen(fd, "wb") as fh:
                fh.write(body)
            return path
    except OSError:
        return None
    return None


def _text(value: str | bytes | None) -> str:
    """A captured stream as text (``TimeoutExpired`` can hold bytes)."""
    if value is None:
        return ""
    return value.decode(errors="replace") if isinstance(value, bytes) else value


def log_hint(path: Path | None) -> str:
    return f" (agent log: {path})" if path is not None else " (the agent log could not be written)"


def _js(value: object) -> str:
    """A Python value as a JavaScript literal (JSON is valid JavaScript)."""
    return json.dumps(value)


class BrowserDriver(Protocol):
    """What `plato vault app` calls on a browser driver: :class:`EgoDriver` and
    :class:`pi_browser.PiDriver`. On ego-browser, reclaim, discard_login and route_callback
    do nothing, and pump only waits :data:`PUMP_S` (a pump that does nothing makes the
    consent listener spin a CPU core)."""

    tools: PortalTools
    space_id: int | None
    handed_off: bool
    last_agent_log: Path | None

    def open_space(self, name: str) -> int: ...

    def goto(self, url: str) -> None: ...

    def hand_off(self) -> None: ...

    def finish(self) -> None: ...

    def agent(self, goal: str, timeout_s: float = AGENT_TIMEOUT_S, *, hand_off_on_need: bool = True) -> VaultLine: ...

    def click_consent(self, recipe: VendorRecipe) -> VaultLine: ...

    def route_callback(self, redirect_uri: str) -> None: ...

    def pump(self) -> None: ...

    def reclaim(self) -> bool: ...

    def discard_login(self) -> None: ...


class EgoDriver:
    """Runs scripts and agents against ONE ego-browser TaskSpace."""

    def __init__(self, tools: PortalTools, space_id: int | None = None) -> None:
        if tools.ego is None:
            raise PortalUnavailable(
                "ego-browser is not installed here, so the portal step cannot run on its own: "
                "pass --manual and do the portal steps by hand"
            )
        self.tools = tools
        self.space_id = space_id
        self.notice = False
        self.handed_off = False
        self.last_agent_log: Path | None = None

    def run(self, script: str, *, quiet_errors: bool = False, timeout_s: float = SCRIPT_TIMEOUT_S) -> list[VaultLine]:
        """Run one script; its ``@@VAULT`` lines. ``quiet_errors`` (the secret script)
        reports a failure by exit code only, never with the script's output."""
        assert self.tools.ego is not None
        try:
            proc = subprocess.run(
                [self.tools.ego, "nodejs"], input=script, text=True, capture_output=True, timeout=timeout_s
            )
        except subprocess.TimeoutExpired:
            raise PortalError(f"an ego-browser script ran over {timeout_s:.0f} s") from None
        out = proc.stdout or ""
        if NOTICE_TAG in out or NOTICE_TAG in (proc.stderr or ""):
            self.notice = True
        if proc.returncode != 0:
            detail = "" if quiet_errors else f": {redact((proc.stderr or out).strip()[-300:])}"
            raise PortalError(f"an ego-browser script failed (exit {proc.returncode}){detail}")
        # ego-browser 0.6 prints the script's console.log on stderr, not stdout so read both
        return parse_lines(out + "\n" + (proc.stderr or ""))

    def open_space(self, name: str) -> int:
        lines = self.run(
            f"const task = await taskSpace({_js(name)});\n"
            f"console.log({_js(LINE_TAG)} + JSON.stringify({{ space_id: task.spaceId }}));\n"
        )
        space = next((line.space_id for line in lines if line.space_id is not None), None)
        if space is None:
            raise PortalError("ego-browser did not report a TaskSpace id")
        self.space_id = space
        return space

    def goto(self, url: str) -> None:
        self.run(
            f"const task = await taskSpace({_js(self.space_id)});\n"
            f'await task.page("p1").goto({_js(url)});\n'
            f"console.log({_js(LINE_TAG)} + JSON.stringify({{ space_id: task.spaceId }}));\n"
        )

    def hand_off(self) -> None:
        self.run(f"const task = await taskSpace({_js(self.space_id)});\nawait task.handOff();\n")
        self.handed_off = True

    def reclaim(self) -> bool:
        """ego-browser has no take-back: the window stays with the person (False)."""
        return False

    def discard_login(self) -> None:
        """ego-browser keeps its own profile: there is no saved login to leave out."""

    def route_callback(self, redirect_uri: str) -> None:
        """The redirect reaches the listener on this machine directly: no route."""

    def pump(self) -> None:
        """No Playwright events to handle: one short wait for the consent listener."""
        time.sleep(PUMP_S)

    def finish(self) -> None:
        """Close the TaskSpace. Not after a hand-off: the person owns it then."""
        if self.space_id is None or self.handed_off:
            return
        self.run(f"const task = await taskSpace({_js(self.space_id)});\nawait task.finish({{ keep: [] }});\n")
        self.space_id = None

    def agent(self, goal: str, timeout_s: float = AGENT_TIMEOUT_S, *, hand_off_on_need: bool = True) -> VaultLine:
        """Run the click agent; its last ``@@VAULT`` line. Its output is not printed (it
        holds page snapshots of the portal); it goes to :func:`write_agent_log`, and
        :attr:`last_agent_log` names the file.

        A ``need_person`` line raises :class:`NeedPerson`. ``hand_off_on_need`` False: the
        window stays with code, because the caller first lets code sign in (:mod:`sign_in`)
        and hands off itself only when code cannot."""
        if self.tools.agent is None:
            raise PortalUnavailable("no `claude` binary here for the portal agent: pass --manual")
        workdir = tempfile.mkdtemp(prefix="vault-agent-")  # empty: no project files to read
        header = f"# portal agent, TaskSpace {self.space_id}\n## goal\n{goal}"
        try:
            proc = subprocess.run(
                agent_command(self.tools.agent, goal),
                text=True,
                capture_output=True,
                timeout=timeout_s,
                stdin=subprocess.DEVNULL,
                cwd=workdir,
                env=agent_env(),
            )
        except subprocess.TimeoutExpired as e:
            self.last_agent_log = write_agent_log(
                self.space_id, f"{header}\n## exit: timeout after {timeout_s:.0f} s", _text(e.stdout), _text(e.stderr)
            )
            raise PortalError(f"the portal agent ran over {timeout_s:.0f} s{log_hint(self.last_agent_log)}") from None
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
        stdout = proc.stdout or ""
        self.last_agent_log = write_agent_log(
            self.space_id, f"{header}\n## exit: {proc.returncode}", stdout, proc.stderr or ""
        )
        lines = parse_lines(stdout)
        if NOTICE_TAG in stdout:
            self.notice = True
        if not lines:
            raise PortalError(
                f"the portal agent ended (exit {proc.returncode}) without a result line{log_hint(self.last_agent_log)}"
            )
        last = lines[-1]
        if last.need_person:
            self.handed_off = hand_off_on_need or self.handed_off
            raise NeedPerson(
                f"the browser needs a person ({last.need_person}): finish it in the ego-browser window "
                f"(TaskSpace {self.space_id}), then run the command again{log_hint(self.last_agent_log)}",
                reason=last.need_person,
            )
        return last

    def click_consent(self, recipe: VendorRecipe) -> VaultLine:
        """Code clicks the consent page's grant button, with no model in the path.

        The button has a fixed accessible name (``recipe.consent_button``),
        so a script can wait for it, check that there is exactly one, click it, and
        check the redirect itself. The agent stays as the fallback for a page that
        does not match (:func:`_consent_script` reports ``allowed`` false)."""
        base = recipe.redirect_uri.split("/callback")[0]
        lines = self.run(
            _consent_script(self.space_id, recipe.consent_button, base), timeout_s=CONSENT_SCRIPT_TIMEOUT_S
        )
        return next((ln for ln in lines if ln.allowed is not None), VaultLine(allowed=False, error="no result line"))

    def count_generate_buttons(self) -> int:
        lines = self.run(
            f"const task = await taskSpace({_js(self.space_id)});\n"
            'const page = task.page("p1");\n'
            "const n = await page.evaluate(() => [...document.querySelectorAll('button')]"
            ".filter((b) => (b.textContent || '').trim().toLowerCase() === 'generate secret').length);\n"
            f"console.log({_js(LINE_TAG)} + JSON.stringify({{ generate_buttons: n }}));\n"
        )
        return next((line.generate_buttons for line in lines if line.generate_buttons is not None), 0)

    def read_secret(self, recipe: VendorRecipe) -> tuple[PortalSecretFile, VaultLine]:
        """Click "Generate secret" and read the values from the DOM, with no model in
        the path. Canva shows a new secret ONE time: if this fails after the click, a
        person must generate another one."""
        workdir = tempfile.mkdtemp(prefix="vault-app-")
        path = os.path.join(workdir, "secret.json")
        try:
            lines = self.run(_secret_script(self.space_id, path, recipe.client_id_prefix), quiet_errors=True)
            line = next((ln for ln in lines if ln.written or ln.error), None)
            if line is None or not line.written:
                why = line.error if line else "no result line"
                raise PortalError(f"the secret step did not write the secret ({why})")
            try:
                values = PortalSecretFile.model_validate_json(Path(path).read_text())
            except (OSError, ValueError, ValidationError):
                raise PortalError("the secret file is missing or unreadable") from None
            if not values.client_id.startswith(recipe.client_id_prefix) or not values.client_secret.get_secret_value():
                raise PortalError(
                    f"the page gave no client id starting {recipe.client_id_prefix} or no secret "
                    f"(client id prefix {line.client_id_prefix!r}, secret length {line.secret_len})"
                )
            return values, line
        finally:
            shutil.rmtree(workdir, ignore_errors=True)


def parse_lines(output: str) -> list[VaultLine]:
    out: list[VaultLine] = []
    for raw in output.splitlines():
        idx = raw.find(LINE_TAG)
        if idx < 0:
            continue
        try:
            out.append(VaultLine.model_validate_json(raw[idx + len(LINE_TAG) :]))
        except ValidationError:
            continue
    return out


# In-page functions (page.evaluate passes one argument). The ego scripts below and
# the Pi driver (pi_browser.PiDriver) run the same text.
GENERATE_COUNT_JS = """() => [...document.querySelectorAll("button")]
  .filter((b) => (b.textContent || "").trim().toLowerCase() === "generate secret").length"""
SECRET_READY_JS = (
    """() => [...document.querySelectorAll("input[type=password]")].some((i) => (i.value || "").length >= 20)"""
)
SECRET_VALUES_JS = """(prefix) => {
      const secret = [...document.querySelectorAll("input[type=password]")]
        .map((i) => i.value || "").find((x) => x.length >= 20) || "";
      const clientId = [...document.querySelectorAll("input")]
        .map((i) => i.value || "").find((x) => x.startsWith(prefix)) || "";
      return { secret, clientId };
    }"""
# The buttons whose accessible name is exactly `want` (any case), visible and enabled.
# `click` true: click the one button with a DOM click.
CONSENT_MATCH_JS = """({ want, click }) => {
  const found = [...document.querySelectorAll("button, [role=button]")]
    .filter((b) => ((b.getAttribute("aria-label") || b.textContent || "").trim().toLowerCase() === want)
      && b.getClientRects().length > 0 && !b.disabled);
  if (click && found.length === 1) found[0].click();
  return found.length;
}"""


def _secret_script(space_id: int | None, path: str, client_id_prefix: str) -> str:
    """The code-only secret step. On any error after the click it still blanks the page."""
    return f"""
const fs = await import("node:fs/promises");
const task = await taskSpace({_js(space_id)});
const page = task.page("p1");
const out = (o) => console.log({_js(LINE_TAG)} + JSON.stringify(o));
const count = await page.evaluate({GENERATE_COUNT_JS});
if (count !== 1) {{
  out({{ error: "generate_buttons", generate_buttons: count }});
}} else {{
  const url = String(await page.url());
  const m = url.match(/\\/apps\\/([A-Za-z0-9_-]{{6,}})/);
  let clicked = false;
  try {{
    await page.click('loc=role:button[name="Generate secret"]', {{ label: "generate the client secret" }});
    clicked = true;
    await page.waitForFunction(
      {SECRET_READY_JS},
      undefined,
      {{ timeout: 30000 }},
    );
    const v = await page.evaluate({SECRET_VALUES_JS}, {_js(client_id_prefix)});
    const fh = await fs.open({_js(path)}, "wx", 0o600);
    try {{
      await fh.writeFile(JSON.stringify({{ client_id: v.clientId, client_secret: v.secret }}));
    }} finally {{
      await fh.close();
    }}
    out({{ written: true, client_id_prefix: v.clientId.slice(0, 5), secret_len: v.secret.length,
           app_id: m ? m[1] : null }});
  }} catch (e) {{
    out({{ error: clicked ? "after_click" : "click_failed" }});
  }} finally {{
    await page.goto("about:blank");
  }}
}}
"""


def _consent_script(space_id: int | None, button: str, redirect_base: str) -> str:
    """Wait for exactly one grant button, click it, and wait for the redirect to the
    listener; a second click if the first did not navigate (a click before the page's
    script is ready does nothing). Reports ``allowed`` true only when the page URL
    starts with ``redirect_base``. Uses page.url() and page.evaluate() in poll loops,
    so a navigation in the middle of a check is not an error."""
    return f"""
const task = await taskSpace({_js(space_id)});
const page = task.page("p1");
const out = (o) => console.log({_js(LINE_TAG)} + JSON.stringify(o));
const base = {_js(redirect_base)};
const name = {_js(button)};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const atBase = async () => {{ try {{ return String(await page.url()).startsWith(base); }} catch (e) {{ return false; }} }};
// The buttons whose accessible name is exactly `name` (any case), visible and enabled.
// One argument (evaluate passes one). `click` true: click the button with a DOM click, used when the loc= click throws.
const match = {CONSENT_MATCH_JS};
const count = async () => {{ try {{ return await page.evaluate(match, {{ want: name.toLowerCase(), click: false }}); }} catch (e) {{ return 0; }} }};
const waitFor = async (ms, test) => {{
  const end = Date.now() + ms;
  while (Date.now() < end) {{ if (await test()) return true; await sleep(500); }}
  return await test();
}};
let n = 0;
let clicks = 0;
if (await atBase()) {{
  out({{ allowed: true, allow_buttons: 0, clicks: 0 }});
}} else {{
  await waitFor({CONSENT_BUTTON_WAIT_MS}, async () => (await atBase()) || (n = await count()) >= 1);
  if (await atBase()) {{
    out({{ allowed: true, allow_buttons: 0, clicks: 0 }});
  }} else if (n !== 1) {{
    out({{ allowed: false, error: "allow_buttons", allow_buttons: n, clicks: 0 }});
  }} else {{
    await sleep(1000);  // let the page's script attach its click handler
    let done = false;
    while (!done && clicks < {CONSENT_CLICKS}) {{
      if ((await count()) !== 1) break;
      try {{
        await page.click("loc=role:button[name=" + JSON.stringify(name) + "]", {{ label: "allow access on the consent page" }});
      }} catch (e) {{
        // The loc= name match can be wider than this script's exact match (a
        // "Don't allow" button): click the one exact button in the DOM instead.
        let n2 = 0;
        try {{ n2 = await page.evaluate(match, {{ want: name.toLowerCase(), click: true }}); }} catch (e2) {{ n2 = 0; }}
        if (n2 !== 1) {{
          out({{ allowed: false, error: "click_failed", allow_buttons: n2, clicks }});
          done = null;
          break;
        }}
      }}
      clicks += 1;
      done = await waitFor({CONSENT_REDIRECT_WAIT_MS}, atBase);
    }}
    if (done) out({{ allowed: true, allow_buttons: 1, clicks }});
    else if (done === false) out({{ allowed: false, error: "no_redirect", allow_buttons: await count(), clicks }});
  }}
}}
"""


def portal_goal(
    recipe: VendorRecipe,
    space_id: int,
    kinds: list[CredentialKind],
    app_name: str | None,
    app_id: str | None,
    browser: ConsentBrowser = ConsentBrowser.ego,
) -> str:
    if app_id:
        app_step = f"open the existing app with id {app_id} (from the app list at {recipe.portal_url})."
    else:
        app_step = f"create a new app named '{app_name}'."
    template = recipe.pi_portal_template if browser == ConsentBrowser.pi else recipe.portal_template
    return render_prompt(
        template,
        space_id=space_id,
        portal_url=recipe.portal_url,
        app_step=app_step,
        switches=", ".join(f"'{recipe.switches[k]}'" for k in kinds),
        scopes=" ".join(recipe.scopes_for(kinds)),
        redirect_uri=recipe.redirect_uri,
        no_files=NO_FILES_RULE,
        screen_rule=PI_SCREEN_RULE,
    )


def consent_goal(recipe: VendorRecipe, space_id: int, app: str, browser: ConsentBrowser = ConsentBrowser.ego) -> str:
    base = recipe.redirect_uri.split("/callback")[0]
    template = recipe.pi_consent_template if browser == ConsentBrowser.pi else recipe.consent_template
    return render_prompt(
        template,
        space_id=space_id,
        app=app,
        button=recipe.consent_button,
        redirect_base=base,
        no_files=NO_FILES_RULE,
        screen_rule=PI_SCREEN_RULE,
    )


def driver_browser(driver: object) -> ConsentBrowser:
    """The browser a driver runs (EgoDriver and test fakes have no ``browser``: ego)."""
    return getattr(driver, "browser", ConsentBrowser.ego)


def person_hint(driver: object) -> str:
    """Where a person finishes a step: the driver's own hint, else the ego-browser window."""
    hint = getattr(driver, "person_hint", None)
    if isinstance(hint, str):
        return hint
    return f"the ego-browser window (TaskSpace {getattr(driver, 'space_id', None)})"


def space_name(recipe: VendorRecipe, login_key: str, account: str) -> str:
    return f"vault-{recipe.vendor}-{login_key}-{account}-{time.strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(4)}"


def run_portal(
    driver: Any,
    recipe: VendorRecipe,
    kinds: list[CredentialKind],
    *,
    app_name: str | None,
    app_id: str | None,
    generate_secret: bool,
) -> PortalResult:
    """The agent configures the app, then (``generate_secret``) code reads a new secret.
    ``driver`` must already have an open TaskSpace on the portal."""
    assert driver.space_id is not None
    end = driver.agent(portal_goal(recipe, driver.space_id, kinds, app_name, app_id, driver_browser(driver)))
    if not end.ready_for_secret:
        raise PortalError(
            f"the portal agent did not finish the app setup: {end.reason or 'no reason given'}"
            f"{log_hint(driver.last_agent_log)}"
        )
    if not generate_secret:
        return PortalResult(app_id=app_id, client_id=None, client_secret=None, notice=driver.notice)
    buttons = driver.count_generate_buttons()
    if buttons != 1:
        raise PortalError(f"expected one 'Generate secret' button on the page, found {buttons}; nothing was clicked")
    values, line = driver.read_secret(recipe)
    return PortalResult(
        app_id=line.app_id or app_id,
        client_id=values.client_id,
        client_secret=values.client_secret,
        notice=driver.notice,
    )
