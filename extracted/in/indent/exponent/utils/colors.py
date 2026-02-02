from colour import Color


def relative_luminance(c: Color) -> float:
    """Compute sRGB-based luminance, per the standard (WCAG-like) formula."""

    r, g, b = c.rgb

    def to_linear(channel: float) -> float:
        return (
            channel / 12.92
            if channel <= 0.03928
            else ((channel + 0.055) / 1.055) ** 2.4
        )

    R, G, B = map(to_linear, (r, g, b))

    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast_ratio(c1: Color, c2: Color) -> float:
    """Compute ratio = (Llighter + 0.05) / (Ldarker + 0.05)."""

    L1 = relative_luminance(c1)
    L2 = relative_luminance(c2)
    L_high, L_low = max(L1, L2), min(L1, L2)

    return (L_high + 0.05) / (L_low + 0.05)


def adjust_color_for_contrast(
    base: Color, target: Color, min_contrast: float = 4.5, step: float = 0.005
) -> Color:
    """
    Increments either upward or downward in HSL 'l'
    (depending on whether target is lighter or darker than base)
    until the desired contrast ratio is reached or we hit the boundary (0 or 1).
    """

    # Work on a copy so we don't mutate the original
    new_color = Color(target.hex)

    L_base = relative_luminance(base)
    L_target = relative_luminance(new_color)

    # Check which color is darker:
    # if the target is darker, we'll push it darker; if it's lighter, we push it lighter.
    h, s, l = new_color.hsl  # noqa: E741

    if L_target < L_base:
        # target color is darker => keep making it darker
        while l >= 0.0:
            if contrast_ratio(base, new_color) >= min_contrast:
                return new_color
            l -= step  # noqa: E741
            new_color.hsl = (h, s, max(l, 0.0))
    else:
        # target color is lighter => keep making it lighter
        while l <= 1.0:
            if contrast_ratio(base, new_color) >= min_contrast:
                return new_color
            l += step  # noqa: E741
            new_color.hsl = (h, s, min(l, 1.0))

    # If we exhaust the channel range, just return whatever we ended with
    return new_color
