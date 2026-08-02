"""nx_browse — the /browse web agent (Phase 2: a REAL, read-only, visible/headless browse).

Drives the operator's own system Chrome via Playwright (channel="chrome") to SEARCH + READ the open web for a task,
then hands the findings back for a cited answer.
  • watch  = headed  — you see the browser navigate (on the go)
  • flight = headless — no window; it goes and returns results

READ-ONLY BY CONSTRUCTION: navigate + read + extract only. It writes nothing and transacts nothing. Every browser
action is classified through the SAME RiskTier wall the money path uses (classify_browse_action) — a transactional
action (buy / submit / credential) is REFUSED here and deferred to the gated Phase 3, never fired autonomously.

Playwright is a LAZY / OPTIONAL import: `nx` runs without it, and /browse guides the one-time install on first drive.
"""
import urllib.parse


def playwright_available() -> bool:
    try:
        import playwright  # noqa: F401
        return True
    except Exception:
        return False


def install_hint() -> str:
    return "pipx inject nxplora playwright   (drives your installed Chrome directly — no extra download)"


# ── the safety gate: a browse action → the RiskTier wall (posture, not a denylist) ────────────────────────
# SAFE = reversible, no outward effect (navigate, read, TYPE into a field, click a nav/link). The transaction is the
# SUBMIT/BUY, not the typing — so typing is allowed and the irreversible outward step is what gets gated.
_SAFE_KINDS = {"navigate", "goto", "read", "extract", "get_text", "screenshot", "scroll", "search", "back",
               "forward", "click", "fill", "type", "press", "select"}
_TRANSACT_KINDS = {"click_buy", "submit_form", "submit", "checkout", "place_order", "subscribe", "post", "publish", "send"}
_PROHIBITED_KINDS = {"enter_credential", "enter_password", "enter_payment", "solve_captcha", "create_account"}
# a plain click/press whose TARGET reads transactional → GATED even if the caller under-labelled it (defense).
_TRANSACT_WORDS = ("buy", "checkout", "pay ", "pay now", "place order", "order now", "purchase", "add to cart",
                   "confirm order", "complete purchase", "place your order", "subscribe", "checkout now")


def classify_browse_action(kind: str, target: str = "") -> str:
    """SAFE (autonomous) | GATED (stage for the operator's confirmation) | PROHIBITED (never autonomous).

    fail-CLOSED: anything not recognized as a reversible read/type is NOT auto-fired (enumeration loses; the posture
    holds). Credentials / payment / CAPTCHA are untouchable — NX hands the wheel back. A plain click whose TARGET
    reads transactional is treated as GATED, so a mislabelled 'Buy now' still can't auto-fire."""
    k = (kind or "").strip().lower()
    if k in _PROHIBITED_KINDS:
        return "PROHIBITED"
    if k in _TRANSACT_KINDS:
        return "GATED"
    t = (target or "").strip().lower()
    if k in ("click", "press", "tap") and any(w in t for w in _TRANSACT_WORDS):
        return "GATED"  # target-based defense against an under-labelled transactional click
    return "SAFE" if k in _SAFE_KINDS else "GATED"  # default-closed


def _noop(*_a, **_k):
    return None


def _looks_blocked(body_text: str) -> bool:
    """Search engines bot-challenge automated browsers. Detect it honestly instead of returning empty 'results'."""
    b = (body_text or "").lower()
    return any(s in b for s in ("bots use", "solve the challenge", "confirm this search", "one last step", "are you a robot", "unusual traffic"))


# ── Phase 3: GATED action execution — the enforcement core ────────────────────────────────────────────────
_SENSITIVE_INPUT_TYPES = {"password"}  # <input type> NX must NEVER fill, whatever the action is labelled


def _find_clickable(page, target: str):
    """Find a link/button by its visible text (or a CSS selector). Best-effort, exact-ish then contains."""
    t = (target or "").strip()
    if not t:
        return None
    if t.startswith((".", "#", "[")) or t.split()[0] in ("a", "button", "input"):
        el = page.query_selector(t)
        if el:
            return el
    for sel in ("button", "a", "[role=button]", "input[type=submit]"):
        for el in page.query_selector_all(sel):
            try:
                txt = (el.inner_text() or el.get_attribute("value") or "").strip().lower()
            except Exception:
                txt = ""
            if txt and (txt == t.lower() or t.lower() in txt):
                return el
    return None


def _is_sensitive_field(el) -> bool:
    try:
        typ = (el.get_attribute("type") or "").lower()
        name = ((el.get_attribute("name") or "") + " " + (el.get_attribute("autocomplete") or "")).lower()
    except Exception:
        return False
    if typ in _SENSITIVE_INPUT_TYPES:
        return True
    return any(s in name for s in ("password", "cc-number", "card", "cvc", "cvv", "ssn"))


def execute_action(page, action: dict, on_gate=None, on_step=None) -> dict:
    """Execute ONE structured browser action UNDER THE GATE. action = {kind, target?, value?}.

      SAFE       → execute (navigate / read / scroll / a benign click).
      GATED      → on_gate(action) must return True (operator confirmed) BEFORE it fires; else it is skipped.
      PROHIBITED → REFUSED, never executed — NX never types a credential/payment or completes a purchase.

    Defense-in-depth: even a GATED-and-approved fill into a password/card field is REFUSED (the field itself is
    sensitive, whatever the caller labelled the action). Returns {ok, kind, verdict, executed, refused?, staged?, detail?}."""
    on_step = on_step or _noop
    a = action or {}
    kind = (a.get("kind") or "").lower()
    target = a.get("target") or ""
    value = a.get("value") or ""
    verdict = classify_browse_action(kind, target)
    res = {"ok": True, "kind": kind, "verdict": verdict, "executed": False}

    if verdict == "PROHIBITED":
        on_step("REFUSED (%s) — that's yours to do; I never enter credentials/payment or complete a purchase" % (kind or "?"))
        res["refused"] = True
        return res

    if verdict == "GATED":
        on_step("needs your OK: %s %s" % (kind, target[:50]))
        res["staged"] = True
        if not (on_gate and bool(on_gate(a))):
            on_step("not approved — skipped")
            return res
        on_step("approved — doing it")

    try:
        if kind in ("navigate", "goto"):
            page.goto(target if "://" in target else "https://" + target, timeout=30000, wait_until="domcontentloaded")
        elif kind in ("read", "get_text", "extract"):
            res["detail"] = (page.inner_text("body") or "")[:2000]
        elif kind in ("fill", "type"):
            el = page.query_selector(target) if target else None
            if el is None:
                res["ok"] = False; res["detail"] = "field not found: " + target[:50]
            elif _is_sensitive_field(el):
                on_step("REFUSED — that field is a password/payment/credential; you fill it, not me")
                res["refused"] = True; return res
            else:
                el.fill(value, timeout=8000)
                res["executed"] = True
        else:  # click / click_buy / any transactional click (already gate-approved above if needed)
            el = _find_clickable(page, target)
            if el is None:
                res["ok"] = False; res["detail"] = "element not found: " + target[:50]
            else:
                el.click(timeout=8000)
                res["executed"] = True
        if kind in ("navigate", "goto", "read", "get_text", "extract") and res["ok"]:
            res["executed"] = True
    except Exception as e:
        res["ok"] = False; res["detail"] = "%s: %s" % (type(e).__name__, str(e)[:120])
    return res


# ── Phase 3: the LLM planner — turns (task + page) into the next browser action ────────────────────────────
_PLAN_SYS = (
    "You are NX driving a real web browser to accomplish a task, ONE action at a time. You are given the task, the "
    "current page, and your past actions. Reply with EXACTLY ONE json object and nothing else:\n"
    '  {"kind":"<action>","target":"<link/button text OR css selector OR url>","value":"<text to type>","why":"<one line>"}\n'
    "kinds: navigate (target=a url) · click (target=link/button text) · fill (target=css selector, value=text) · read · done.\n"
    "For a purchase / checkout / submit-order use kind \"click_buy\" or \"submit_form\" — it will be STAGED for the operator "
    "to confirm before it fires. NEVER attempt to enter a password or payment (those are refused). Use \"done\" when the "
    "task is achieved OR you are blocked (login wall, CAPTCHA). Prefer the FEWEST steps; return done rather than guessing."
)


def plan_next_action(task: str, obs: dict, history: list, model_fn) -> dict:
    """Ask the LLM for the next browser action (structured). `model_fn(prompt)->str` runs one model completion.
    Returns {kind, target?, value?, why?}; FAIL-SAFE — a model error / unparseable reply → {"kind":"done"} (stop,
    never act blindly). The gate still governs whatever kind comes back, so a hallucinated 'click_buy' is staged, not fired."""
    hist = "\n".join(
        "- %s %s -> %s" % (h.get("kind"), (h.get("target") or "")[:40], "ok" if h.get("executed") else "skip/no")
        for h in (history or [])[-6:]
    ) or "(none yet)"
    prompt = (
        "%s\n\nTASK: %s\n\nCURRENT PAGE:\n  url: %s\n  title: %s\n  visible text (truncated):\n%s\n\nPAST ACTIONS:\n%s\n\n"
        "Next action (one json object only):"
        % (_PLAN_SYS, task, obs.get("url", ""), obs.get("title", ""), (obs.get("text", "") or "")[:1800], hist)
    )
    try:
        raw = model_fn(prompt) or ""
    except Exception:
        return {"kind": "done", "why": "planner error"}
    import json
    import re
    m = re.search(r"\{.*\}", str(raw), re.S)
    if not m:
        return {"kind": "done", "why": "no action parsed"}
    try:
        a = json.loads(m.group(0))
    except Exception:
        return {"kind": "done", "why": "unparseable action"}
    if not isinstance(a, dict):
        return {"kind": "done", "why": "not an object"}
    return {
        "kind": str(a.get("kind") or "done").strip().lower(),
        "target": str(a.get("target") or ""),
        "value": str(a.get("value") or ""),
        "why": str(a.get("why") or "")[:120],
    }


def browse_task(start_url, task, planner, confirm=None, watch: bool = True, max_steps: int = 8, on_step=None) -> dict:
    """Phase-3 agentic loop: open a browser, then observe → plan → act UNDER THE GATE until done.

    `planner(task, observation, history) -> {kind, target?, value?}` (or {kind:'done'}) — the LLM decides the next
    step; EVERY step runs through execute_action, so SAFE auto-fires, GATED needs `confirm(action)->bool`, and
    PROHIBITED is refused (NX never types a credential or completes a purchase). Pluggable planner keeps the loop
    testable. Returns {ok, steps:[...], trail:[...]}."""
    on_step = on_step or _noop
    out = {"ok": False, "steps": [], "trail": []}
    if not playwright_available():
        out["error"] = "playwright_missing"
        return out
    from playwright.sync_api import sync_playwright

    def step(s):
        out["trail"].append(s)
        on_step(s)

    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(channel="chrome", headless=not watch)
            except Exception:
                browser = p.chromium.launch(headless=not watch)
            page = browser.new_page()
            if start_url:
                u = start_url if "://" in start_url else "https://" + start_url
                page.goto(u, timeout=30000, wait_until="domcontentloaded")
            history = []
            for _ in range(max_steps):
                obs = {"url": page.url, "title": page.title(), "text": (page.inner_text("body") or "")[:2500]}
                action = planner(task, obs, history)
                if not action or (action.get("kind") or "").lower() == "done":
                    step("done")
                    break
                r = execute_action(page, action, on_gate=confirm, on_step=step)
                out["steps"].append({"action": action, "result": {k: r.get(k) for k in ("kind", "verdict", "executed", "refused", "staged")}})
                history.append({"kind": action.get("kind"), "target": action.get("target", ""), "executed": bool(r.get("executed"))})
                if r.get("refused"):
                    step("stopped — that step is yours to do")
            # the page NX ended on — its content is what a cited answer is grounded in
            try:
                out["final"] = {"url": page.url, "title": page.title(), "text": (page.inner_text("body") or "")[:5000]}
            except Exception:
                out["final"] = {}
            browser.close()
            out["ok"] = True
    except Exception as e:
        out["error"] = "%s: %s" % (type(e).__name__, str(e)[:150])
    return out


def _goto_with_retry(page, url, tool="browse_url", **kwargs):
    """Navigate with a bounded retry on a TRANSIENT failure (timeout / connection reset / 5xx / 429). A
    DETERMINISTIC failure (bad url, 404) raises immediately — re-running would just fail again. Parity with the
    Nexplora code agent's transient retry; reuses nx_harness.is_retryable + RETRY_BACKOFFS. Read tools only."""
    import time
    try:
        import nx_harness as _nxh
    except Exception:
        _nxh = None
    delays = (0.0,) + (tuple(_nxh.RETRY_BACKOFFS) if _nxh else ())
    last_exc = None
    for delay in delays:
        if delay:
            time.sleep(delay)
        try:
            return page.goto(url, **kwargs)
        except Exception as e:
            last_exc = e
            if not (_nxh and _nxh.is_retryable(tool, str(e))):
                raise
    if last_exc:
        raise last_exc
    return None


def browse_url(url: str, watch: bool = True, on_step=None) -> dict:
    """Open a REAL browser and READ one page — the working Phase-2 primitive (verified). READ-ONLY: navigate + extract
    title/text/links, nothing else. watch = headed (you see it); flight = headless. If a login wall / CAPTCHA blocks
    the page, that's T3 — in watch mode the browser is open for YOU to pass it; NX never types a credential.
    Returns {ok, url, title, text, links:[{text,url}], trail:[str], blocked?, error?}."""
    on_step = on_step or _noop
    out = {"ok": False, "url": url, "title": "", "text": "", "links": [], "trail": []}
    u = (url or "").strip()
    if not u:
        out["error"] = "empty_url"
        return out
    if not (u.startswith("http://") or u.startswith("https://")):
        u = "https://" + u
    if not playwright_available():
        out["error"] = "playwright_missing"
        return out
    from playwright.sync_api import sync_playwright

    def step(s):
        out["trail"].append(s)
        on_step(s)

    try:
        with sync_playwright() as p:
            step("opening " + ("Chrome — watch it go" if watch else "a headless browser"))
            try:
                browser = p.chromium.launch(channel="chrome", headless=not watch)
            except Exception:
                browser = p.chromium.launch(headless=not watch)
            page = browser.new_page()
            step("navigating: " + u)                                   # SAFE
            _goto_with_retry(page, u, tool="browse_url", timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(700)
            out["title"] = (page.title() or "").strip()
            body = page.inner_text("body") or ""                       # SAFE (read)
            out["text"] = body[:6000]
            if _looks_blocked(body):
                out["blocked"] = True
                step("blocked by a bot-check / login wall — that one's yours to pass (never a credential I type)")
            for a in page.query_selector_all("a[href]")[:40]:
                t = (a.inner_text() or "").strip()
                h = a.get_attribute("href") or ""
                if t and h.startswith("http"):
                    out["links"].append({"text": t[:60], "url": h})
            browser.close()
            out["ok"] = True
            step("done")
    except Exception as e:
        out["error"] = "%s: %s" % (type(e).__name__, str(e)[:180])
    return out


def browse_research(query: str, watch: bool = True, max_results: int = 5, read_top: int = 1, on_step=None) -> dict:
    """Open a browser, SEARCH the web for `query`, READ the top result(s), return findings. READ-ONLY.

    Returns {ok, results:[{title,url,snippet}], readings:[{url,title,text}], trail:[str], error?}. Never clicks a
    transactional control; never enters data. `on_step(str)` streams progress so watch mode reads live."""
    on_step = on_step or _noop
    out = {"ok": False, "results": [], "readings": [], "trail": []}

    q = (query or "").strip()
    if not q:
        out["error"] = "empty_query"
        return out
    if not playwright_available():
        out["error"] = "playwright_missing"
        return out
    from playwright.sync_api import sync_playwright

    def step(s):
        out["trail"].append(s)
        on_step(s)

    try:
        with sync_playwright() as p:
            step("opening " + ("Chrome — watch it go" if watch else "a headless browser"))
            try:
                browser = p.chromium.launch(channel="chrome", headless=not watch)
            except Exception:
                browser = p.chromium.launch(headless=not watch)  # fall back to Playwright's own chromium
            page = browser.new_page()

            # SAFE — navigate to a scrape-friendly search surface
            step("searching: " + q)
            _goto_with_retry(page, "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q),
                             tool="browse_research", timeout=25000, wait_until="domcontentloaded")
            page.wait_for_timeout(700)
            if _looks_blocked(page.inner_text("body") or ""):
                # search engines bot-challenge automation — honest, not empty. Reliable web search is the research
                # tools (Tavily/Exa); browser search is for watch mode where the operator can pass the challenge.
                out["blocked"] = True
                step("search engine bot-challenged the browser — use research tools, or /browse in watch mode")
                browser.close()
                out["ok"] = True
                return out

            for a in page.query_selector_all("a.result__a")[:max_results]:
                title = (a.inner_text() or "").strip()
                href = a.get_attribute("href") or ""
                if "uddg=" in href:  # DDG wraps the real target in a redirect param
                    try:
                        href = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
                    except Exception:
                        pass
                if title and href:
                    out["results"].append({"title": title, "url": href, "snippet": ""})
            # pair snippets by position (best-effort)
            snips = [s.inner_text().strip() for s in page.query_selector_all(".result__snippet")]
            for i, r in enumerate(out["results"]):
                if i < len(snips):
                    r["snippet"] = snips[i][:280]
            step("found %d result%s" % (len(out["results"]), "" if len(out["results"]) == 1 else "s"))

            # SAFE — open + read the top result(s)
            for r in out["results"][:read_top]:
                try:
                    step("reading: " + (r["title"] or r["url"])[:60])
                    page.goto(r["url"], timeout=25000, wait_until="domcontentloaded")
                    page.wait_for_timeout(600)
                    out["readings"].append({"url": r["url"], "title": r["title"], "text": (page.inner_text("body") or "")[:4000]})
                except Exception:
                    continue

            browser.close()
            out["ok"] = True
            step("done")
    except Exception as e:
        out["error"] = "%s: %s" % (type(e).__name__, str(e)[:180])
    return out
