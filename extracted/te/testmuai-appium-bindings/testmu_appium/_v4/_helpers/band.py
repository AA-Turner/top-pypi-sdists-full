"""The 15% viewport band.

One definition of the margin, imported by both the runner's pre-action gate and
the ``scroll_until`` stop test so the two cannot drift apart. The comparison is
integer arithmetic over the element centre and the window span, cross-multiplied
by the margin denominator so it never divides — a centre that lands exactly on
the boundary resolves the same under every rounding.
"""

#: The margin as an exact fraction of the window's height, held as
#: numerator/denominator so the comparison stays integer arithmetic. 3/20 = 15%:
#: a centre must clear 15% of each vertical edge to count as in-band.
BAND_MARGIN_NUMERATOR = 3
BAND_MARGIN_DENOMINATOR = 20

#: Slack on each band edge, in device pixels. Below the sub-slop dead zone a
#: gesture moves no content, so a centre within this distance of the band counts
#: as placed rather than nudged toward precision the hardware cannot deliver.
BAND_TOLERANCE_PX = 8

#: A nudge aims this fraction into the band from the near edge — not the edge
#: (barely in) nor the centre (overshoot). Viewport-relative, so the reach is the
#: same proportion on any screen.
BAND_NUDGE_LANDING = 1 / 3

#: A nudge is a bounded reposition of an on-screen element, never a search, so it
#: is capped at this many gestures.
BAND_NUDGE_MAX_GESTURES = 3


def in_band(centre, top, bottom, *, tolerance=BAND_TOLERANCE_PX):
    """Whether ``centre`` lies inside the band of the vertical span ``[top, bottom]``.

    True when the centre is at least the margin from each edge, ``tolerance``
    pixels of slack allowed. Cross-multiplied by the denominator, so it holds to
    exact integers with no division.
    """
    span = bottom - top
    margin = BAND_MARGIN_NUMERATOR * span
    slack = BAND_MARGIN_DENOMINATOR * tolerance
    return (
        BAND_MARGIN_DENOMINATOR * (centre - top) >= margin - slack
        and BAND_MARGIN_DENOMINATOR * (bottom - centre) >= margin - slack
    )


def band_edges(top, bottom, *, tolerance=BAND_TOLERANCE_PX):
    """The centre range ``[lo, hi]`` that ``in_band`` accepts, tolerance applied.

    A nudge reads these to size its drag — how far a centre must travel to enter
    the band. The crisp verdict stays ``in_band``; these edges only aim the
    gesture, so a float value is fine here.
    """
    margin = (BAND_MARGIN_NUMERATOR * (bottom - top)
              - BAND_MARGIN_DENOMINATOR * tolerance) / BAND_MARGIN_DENOMINATOR
    return (top + margin, bottom - margin)


def nudge_toward_band(centre, top, bottom, *, landing=BAND_NUDGE_LANDING):
    """``(direction, distance)`` to bring ``centre`` into the band of ``[top, bottom]``.

    ``(None, 0.0)`` when the centre already lies in band. Otherwise the gesture aims
    ``landing`` of the way into the band from the near edge, and ``distance`` is how far
    the centre must travel to get there. ``direction`` is ``"down"`` for a centre below
    the band — scrolling down reveals lower content, so on-screen rows move up — and
    ``"up"`` for a centre above it. One definition of the landing, read by both the
    adapter's authoring nudge and the binding's ``scroll_until`` so the two place an
    element identically.
    """
    if in_band(centre, top, bottom):
        return None, 0.0
    lo, hi = band_edges(top, bottom)
    mid = (top + bottom) / 2
    if centre > mid:
        target = hi - landing * (hi - mid)
        return "down", centre - target
    target = lo + landing * (mid - lo)
    return "up", target - centre
