"""CENSUS: every URL this package writes to a log line or an exception message
passes through ``utils.proxy.redact_url_secrets``.

The class this guards: a caller-supplied (or DB-row, or proxy-config) URL is
formatted into ``logger.*`` / ``vcprint`` / ``raise X(...)`` verbatim, so its
``user:password@`` or ``?api_key=`` lands in the logs. It shipped once in
``guard_proxy`` (f4238ccc1) and in 80 sibling sites after it.

The rule, derived from the source (fails on any NEW member):
  * a SINK is ``<logger-ish>.debug|info|warning|warn|error|exception|critical(...)``,
    ``vcprint(...)``, or the constructor call in ``raise X(...)``;
  * a URL REFERENCE is a variable or attribute named ``url`` / ``uri`` /
    ``proxy`` / ``href`` or ending ``_url`` / ``_uri`` / ``_proxy`` / ``_href``
    used as a value inside a sink's arguments (f-string parts included);
  * every URL reference must sit inside ``redact_url_secrets(...)`` — or inside
    ``len()`` / ``type()`` / ``.hostname``, which carry no userinfo or query;
  * on a sink that carries a URL, the bound exception of the enclosing
    ``except ... as exc`` must be redacted too: validators and HTTP clients
    echo the URL they failed on into their message.

Deliberately OUT of the census (say so, never pretend coverage):
  * ``print`` — only ``gsc_bootstrap``'s interactive CLI uses it, and it must
    show the operator the full OAuth URL they are about to open;
  * a URL held under another name (``target``, ``link``), or reaching a log
    only through an exception on a line that names no URL, or inside an
    ``exc_info=True`` traceback — no static rule sees those without flagging
    every unrelated log line, which would make this a noise generator.

Redaction is OUTPUT-only. URL identity (``web_crawl/url_identity.py``,
``utils/url.normalize_url``), dedupe and cache keys must never route through it.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "matrx_scraper"

REDACT = "redact_url_secrets"
_URL_NAME = re.compile(r"^(?:.*_)?(?:url|uri|proxy|href)$", re.IGNORECASE)
_LOG_METHODS = {"debug", "info", "warning", "warn", "error", "exception", "critical"}
_SAFE_CALLS = {REDACT, "len", "type"}
_SAFE_ATTRS = {"hostname", "__name__"}


def _sink_args(node: ast.AST) -> list[ast.expr] | None:
    call: ast.Call | None = None
    if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
        call = node.exc
    elif isinstance(node, ast.Call):
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr in _LOG_METHODS:
            base = func.value
            base_name = base.id if isinstance(base, ast.Name) else getattr(base, "attr", "")
            if "log" in base_name.lower():
                call = node
        elif isinstance(func, ast.Name) and func.id == "vcprint":
            call = node
    if call is None:
        return None
    return [*call.args, *(kw.value for kw in call.keywords)]


def _callee_name(call: ast.Call) -> str:
    return call.func.id if isinstance(call.func, ast.Name) else getattr(call.func, "attr", "")


def _unredacted_refs(
    expr: ast.expr, exc_names: frozenset[str], *, ignore_safe: bool = False
) -> list[tuple[str, str]]:
    """URL / exception references in ``expr`` not inside a safe wrapper.

    ``ignore_safe=True`` reports every URL reference, wrapped or not — used to
    decide whether a sink carries a URL at all.
    """
    found: list[tuple[str, str]] = []

    def walk(node: ast.AST, safe: bool) -> None:
        if not ignore_safe and isinstance(node, ast.Call) and _callee_name(node) in _SAFE_CALLS:
            safe = True
        if not ignore_safe and isinstance(node, ast.Attribute) and node.attr in _SAFE_ATTRS:
            safe = True
        leaf = node.id if isinstance(node, ast.Name) else getattr(node, "attr", None)
        if not safe and isinstance(node, (ast.Name, ast.Attribute)) and leaf:
            if _URL_NAME.match(leaf):
                found.append(("url", ast.unparse(node)))
                return
            if isinstance(node, ast.Name) and node.id in exc_names:
                found.append(("exc", node.id))
                return
        for child in ast.iter_child_nodes(node):
            if isinstance(node, ast.Call) and child is node.func:
                # A callee's own name (`normalize_url(...)`) is code, not data.
                if isinstance(child, ast.Attribute):
                    walk(child.value, safe)
                continue
            walk(child, safe)

    walk(expr, False)
    return found


def find_violations(source: str, filename: str = "<source>") -> list[str]:
    """Every sink carrying an unredacted URL, as ``file:line: <refs>``."""
    violations: list[str] = []

    def visit(node: ast.AST, exc_names: frozenset[str]) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            exc_names = frozenset()
        if isinstance(node, ast.ExceptHandler) and node.name:
            exc_names = exc_names | {node.name}
        args = _sink_args(node)
        if args is not None:
            refs = [ref for arg in args for ref in _unredacted_refs(arg, exc_names)]
            # A line "carries a URL" whether or not that URL is already redacted —
            # its exception still echoes the raw URL it failed on.
            carries_url = any(kind == "url" for arg in args for kind, _ in _unredacted_refs(arg, frozenset(), ignore_safe=True))
            if refs and carries_url:
                named = ", ".join(text for _, text in refs)
                violations.append(f"{filename}:{node.lineno}: unredacted {named}")
        for child in ast.iter_child_nodes(node):
            visit(child, exc_names)

    visit(ast.parse(source, filename=filename), frozenset())
    return violations


def test_every_logged_or_raised_url_in_the_package_is_redacted() -> None:
    files = sorted(PACKAGE_ROOT.rglob("*.py"))
    assert len(files) > 100, f"census found only {len(files)} files under {PACKAGE_ROOT}"
    violations = [
        violation
        for path in files
        for violation in find_violations(path.read_text(), str(path.relative_to(PACKAGE_ROOT)))
    ]
    assert not violations, (
        "URLs reach logs/exception text without redaction — wrap each reference "
        "(and the same line's exception) in "
        "matrx_scraper.utils.proxy.redact_url_secrets(...):\n" + "\n".join(violations)
    )


_PLANTED = '''
import logging
logger = logging.getLogger(__name__)

async def planted(url, request, item, proxy):
    logger.info("rejected %r", request.url)                     # 6: attribute
    vcprint(f"SCRAPE SKIPPED: {url}")                           # 7: f-string part
    try:
        pass
    except Exception as exc:
        logger.warning("blocked %s: %s", redact_url_secrets(url), exc)   # 11: exc on a URL line
    raise RuntimeError(f"too many redirects for {item.final_url}")      # 12: raise message
    self.log.error("proxy %s down", proxy)                      # 13: logger-ish attribute

async def clean(url, request, exc_holder):
    logger.info("rejected %r", redact_url_secrets(request.url))
    vcprint(f"host {urlparse(url).hostname} len {len(url)}")
    try:
        pass
    except Exception as exc:
        logger.warning("blocked %s: %s", redact_url_secrets(url), redact_url_secrets(exc))
        logger.warning("db write failed: %s", exc)
    logger.info("normalized %s", redact_url_secrets(normalize_url(url)))
    print(f"open {url}")
'''


def test_census_self_test_flags_each_planted_leak_and_nothing_clean() -> None:
    """The census must be able to FAIL: each planted leak form is reported at
    its own line, and the redacted/hostname/len/no-URL forms are not."""
    violations = find_violations(_PLANTED, "planted.py")
    assert [v.split(": unredacted ")[0] for v in violations] == [
        "planted.py:6",
        "planted.py:7",
        "planted.py:11",
        "planted.py:12",
        "planted.py:13",
    ], violations
    assert violations[2].endswith("unredacted exc"), violations[2]
