"""High-level scroll_into_view action — find element, scroll it into view, heal on failure.

V2 reference (scroll_to branch).

Heal tier selection is shadow-context-aware (V2 parity):

* Non-shadow (search_root is None):  ('DESKTOP_LOCATE_FULL_PAGE', 'VISION_QUERY').
  DESKTOP_LOCATE_FULL_PAGE captures a full-page screenshot so the below-fold
  target is visible to the locate API (V2-parity gap fix, spec §9).
  LIST_XPATHS is suppressed to avoid false-positive relocates on flat DOM
  (the non-vision DOM-rerank tier returns plausible-but-wrong xpaths even
  when the real target is absent — see _DEFAULT_HEAL_TIERS comment).

* Shadow DOM (search_root is not None): ('LIST_XPATHS', 'VISION_QUERY').
  VISION_QUERY calls /v1/heal/vision which returns a top-document xpath;
  that xpath cannot cross a shadow boundary and will never re-resolve a
  shadow-hosted scroll target.  LIST_XPATHS runs healer.list_xpaths() with
  op_type='scroll_until_element', which gates _heal.py's full-page tagify
  (tagifyWebpage(true,true,true)) and returns shadow-relative xpaths plus
  frameInformation — exactly V2's scroll_until heal path.

An explicit ``tiers=`` argument always overrides both defaults.

coord_runner (_scroll_coord_runner): idempotent fine-adjustment for the
DESKTOP_LOCATE_FULL_PAGE coordinate-fallback path. The tier already centered
the target in the viewport before xpath resolution; this runner re-runs
elementFromPoint + scrollIntoView as a safe no-op if the element is still in view.
"""
import time

from testmu_selenium._action_engine import _ActionSpec, _run_action


# Non-shadow default: DESKTOP_LOCATE_FULL_PAGE first (full-page capture for below-fold targets),
# then VISION_QUERY as fallback. LIST_XPATHS suppressed (false-positive relocate risk on flat DOM).
_HEAL_TIERS = ('DESKTOP_LOCATE_FULL_PAGE', 'VISION_QUERY')
# Shadow default: LIST_XPATHS first so full-page tagify returns shadow-relative xpaths.
_SHADOW_HEAL_TIERS = ('LIST_XPATHS', 'VISION_QUERY')


def _scroll_into_view_runner(element, ctx):
    ctx['driver'].execute_script("arguments[0].scrollIntoView({block:'center'})", element)
    time.sleep(1)  # V2-parity settle
    return None


def _scroll_coord_runner(driver, x: int, y: int, ctx) -> bool:
    """Coordinate fallback for DESKTOP_LOCATE_FULL_PAGE — spec §9.3.

    The tier already centered the target in the viewport before xpath resolution.
    This runner is an idempotent fine-adjustment: locate the element at (x, y)
    via elementFromPoint and call scrollIntoView, or no-op safely if the point
    is off-screen / element is null.
    """
    driver.execute_script(
        "var el = document.elementFromPoint(arguments[0], arguments[1]);"
        " if (el) { el.scrollIntoView({block: 'center'}); }",
        x, y,
    )
    return True


# op_type='scroll_until_element' ensures _heal.py gates full-page tagify when
# LIST_XPATHS runs (healer.list_xpaths() reads operation_type at _heal.py).
# coord_runner handles the DESKTOP_LOCATE_FULL_PAGE coordinate-fallback path.
_SCROLL_INTO_VIEW_SPEC = _ActionSpec(
    runner=_scroll_into_view_runner,
    op_type="scroll_until_element",
    coord_runner=_scroll_coord_runner,
)


def scroll_into_view(driver, selector, *, description='', tiers=None, autoheal=True,
                     max_attempts=4, retry_delay=0.5, search_root=None):
    """Find element and scroll it into view, retrying with heal cascade on recoverable errors.

    When ``tiers`` is None, tier selection is shadow-context-aware:
    - Non-shadow (search_root is None): ('VISION_QUERY',) only.
    - Shadow DOM (search_root is not None): ('LIST_XPATHS', 'VISION_QUERY').
    An explicit ``tiers`` always wins.
    """
    if tiers is None:
        tiers = _SHADOW_HEAL_TIERS if search_root is not None else _HEAL_TIERS
    return _run_action(
        driver, _SCROLL_INTO_VIEW_SPEC, selector,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
    )
