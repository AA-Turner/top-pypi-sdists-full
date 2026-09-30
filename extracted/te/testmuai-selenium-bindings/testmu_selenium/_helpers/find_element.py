import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.shadowroot import ShadowRoot

_log = logging.getLogger(__name__)


#: Only high-confidence ranked locators take the batched fast path. Anything
#: lower falls straight through to native resolution, so a weak guess never
#: bypasses WebDriver's own matching semantics.
_FAST_FIND_MIN_SCORE = 80

# Resolve a ranked locator list in ONE round-trip instead of one per candidate.
#
# Anchor note: document.evaluate() throws NotSupportedError when handed a
# ShadowRoot (a DocumentFragment) as the context node, so an XPath inside a
# shadow root is evaluated from the shadow root's first real element child and
# relative ".." steps climb back up — mirroring the native ShadowContext path.
_FAST_FIND_JS = """
var locators = arguments[0];
var host = arguments[1];

var sr = host && host.shadowRoot ? host.shadowRoot : null;

var anchor = null;
if (sr) {
    anchor = Array.from(sr.children).filter(function (el) {
        var t = el.tagName.toLowerCase();
        return t !== 'script' && t !== 'style';
    })[0] || sr.querySelector(':scope > :not(script):not(style)') || null;
}

for (var i = 0; i < locators.length; i++) {
    var loc = locators[i];
    try {
        if (loc.isXPath) {
            var ctx = anchor || host || document;
            if (!ctx) continue;
            var r = document.evaluate(loc.selector, ctx, null,
                XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (r) return r;
        } else {
            var scope = sr || host || document;
            var el = scope.querySelector(loc.selector);
            if (el) return el;
        }
    } catch (e) { continue; }
}
return null;
"""


def _fast_find(driver, selectors):
    """Resolve the highest-confidence candidates in a single execute_script.

    The ranked lists this binding receives run to a dozen-plus candidates, and
    each native miss is its own WebDriver round-trip; on a remote grid that is
    real latency for an element the first JS pass would have found. One batched
    call replaces the whole walk.

    Deliberately conservative, matching the source fix: only candidates scoring
    >= _FAST_FIND_MIN_SCORE are eligible, and ANY miss, exception, or unscored
    list returns None so the caller runs the untouched native loop. The fast
    path can therefore only ever save time — it can never be the reason an
    element is not found.
    """
    if not selectors or not isinstance(selectors[0], dict):
        return None
    batch = [
        {
            "selector": s.get("selector"),
            "isXPath": bool(s.get("isXPath", False)),
        }
        for s in selectors
        if isinstance(s, dict)
        and isinstance(s.get("score"), (int, float))
        and not isinstance(s.get("score"), bool)
        and s.get("score") >= _FAST_FIND_MIN_SCORE
        and s.get("selector")
    ]
    if not batch:
        return None
    try:
        return driver.execute_script(_FAST_FIND_JS, batch, None)
    except Exception:  # noqa: BLE001 — any failure falls back to native resolution
        _log.debug("    [find] batched fast-find unavailable; using native resolution",
                   exc_info=True)
        return None

def findElement(driver, selectors, description=None, allow_autoheal=True, search_root=None):
    """
    Find element with optional autoheal placeholder path.

    Args:
        driver: WebDriver instance
        selectors: List of {'isXPath': bool, 'selector': str} dicts
        description: Optional description for autoheal functionality
        allow_autoheal: If False, skip the heal placeholder. Set to False when
            wrapped in a RetryNode — the outer heal handles recovery.
        search_root: Optional WebElement or ShadowRoot to resolve selectors
            against instead of the driver. When None, lookups run against the
            top-level document via driver — exact pre-existing behaviour. When
            a ShadowRoot, only CSS candidates are attempted; XPath cannot pierce
            shadow boundaries and ShadowRoot.find_element rejects By.XPATH with
            InvalidArgumentException. Only the element LOOKUP uses search_root;
            the action still runs on driver.

    Returns:
        WebElement

    Raises:
        NoSuchElementException when ``selectors`` is empty (vision-agent
        sourced ops carry no selector and rely on the outer heal cascade
        to resolve via description / coordinates). The Selenium-typed
        exception keeps the failure inside ``_run_action``'s
        ``_DEFAULT_RECOVERABLE`` set so the heal cascade actually fires.

        NoSuchElementException when ``search_root`` is a ShadowRoot and every
        candidate selector is XPath (none are CSS). All candidates are skipped
        upfront; the outer heal cascade handles recovery.

        The original underlying Selenium not-found exception after all
        non-empty selector candidates exhaust.
    """
    from selenium.webdriver.common.by import By

    element = None
    last_exception = None
    root = search_root if search_root is not None else driver
    is_shadow_root = isinstance(search_root, ShadowRoot)
    _log.info("Finding element...")

    # When root is a ShadowRoot, XPath lookups are not possible — ShadowRoot
    # rejects By.XPATH with InvalidArgumentException and XPath cannot pierce
    # shadow boundaries regardless. Log the skip count upfront to avoid silent
    # per-candidate failures and unnecessary driver round-trips.
    if is_shadow_root:
        xpath_count = sum(1 for s in selectors if s.get('isXPath', False))
        if xpath_count:
            _log.info(
                "search_root is a ShadowRoot — skipping %d xpath selector(s); CSS-only lookups",
                xpath_count,
            )

    # One batched JS pass over the high-confidence candidates before the native
    # walk. A hit skips N-1 round-trips; a miss costs one call and the
    # native loop below runs exactly as before.
    #
    # Document-scoped lookups only. A search_root constrains resolution to that
    # subtree, and the JS scope rules cannot reproduce that faithfully for an
    # arbitrary element (a host that happens to have a shadowRoot would search
    # the shadow tree instead of the light-DOM descendants the native path
    # walks). Scoped finds therefore keep the native loop, unchanged.
    if search_root is None:
        fast = _fast_find(driver, selectors)
        if fast is not None:
            _log.info("Element found via batched fast-find")
            return fast

    for selector in selectors:
        isXPath = selector.get('isXPath', False)
        if is_shadow_root and isXPath:
            continue
        _selector = selector.get('selector', '')
        try:
            element = root.find_element(
                by=By.XPATH if isXPath else By.CSS_SELECTOR,
                value=_selector,
            )
            _log.info("Element found using locator: %s", _selector)
            break
        except Exception as e:
            last_exception = e
            continue

    if element is not None:
        return element

    if description and allow_autoheal:
        _log.info("Element not found. Attempting autoheal with description: '%s'", description)
        # Placeholder — future work fills in a per-find heal hook here.
        # C2 Heal does not use this path; outer RetryNode handles heal instead.

    if last_exception is not None:
        raise last_exception

    # ShadowRoot root with only-xpath selectors: all candidates were skipped,
    # no last_exception was set. Raise NoSuchElementException so the outer
    # heal cascade (which catches NoSuchElementException in _DEFAULT_RECOVERABLE)
    # can handle recovery — identical behaviour to the empty-selector path.
    if is_shadow_root and selectors:
        raise NoSuchElementException(
            f"Element not found: all {len(selectors)} selector(s) were xpath and were "
            f"skipped because search_root is a ShadowRoot (XPath cannot pierce shadow "
            f"boundaries) — provide a CSS selector to look up inside a shadow root"
        )

    # Empty selector list (vision-agent sourced ops). Raise the Selenium-typed
    # not-found so _run_action's _DEFAULT_RECOVERABLE catches it and the heal
    # cascade resolves via description / coordinates. Pre-fix this raised a
    # bare Exception which propagated past the recoverable set.
    raise NoSuchElementException(
        f"Element not found with selectors '{selectors}'"
    )
