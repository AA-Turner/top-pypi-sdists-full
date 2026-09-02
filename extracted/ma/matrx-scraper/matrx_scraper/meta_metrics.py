"""
Deterministic SERP metadata metrics — the CANONICAL Python implementation.

Measures approximate rendered pixel width of meta titles/descriptions from a
per-character width table and evaluates them against Google SERP limits.

EXACT mirror of the TypeScript implementation in matrx-frontend
`features/marketing/seo/serp/char-widths.ts` + `metrics.ts` — the width table, the
limits, AND the issue strings are byte-identical, so a metric computed by the
scraper at crawl time, by the browser on an intent save, or by an agent tool
is always the same number and the same wording. Change ANY value here → make
the same change there in the same unit of work and regenerate the parity
fixtures (`features/marketing/seo/serp/metrics.parity.test.ts`).

Based on Google's font rendering:
- Title: 20px Roboto/Google Sans (weight 400), pixel limit 600px
- Description: 13px Roboto/Google Sans (weight 400), pixel limit 920px

ONE limit per field, not a desktop/mobile pair. Google truncates on rendered
PIXEL WIDTH and publishes no separate desktop/mobile metadata rule (customer
report c2fad99f, 2026-07-28). The two limits had always held the same value,
so a single overflow emitted TWO issues saying the same thing in an audit
report. `desktop_ok` / `mobile_ok` remain on the wire as aliases of the one
`*_PIXEL_LIMIT` check so persisted rows and existing consumers keep working.

Consumers:
- the scraper crawl pipeline (`seo_audit.audit_html` → `web.snapshot.seo_metrics`)
- the `seo` agent tool (matrx-ai `tools/implementations/seo.py`)
- aidream registered functions (`seo/utils/registered_functions.py`)
"""

from datetime import UTC, datetime

TITLE_FONT_PX = 20
DESCRIPTION_FONT_PX = 13

TITLE_PIXEL_LIMIT = 600
# Back-compat aliases — one rule, two historical names. Never diverge them.
TITLE_DESKTOP_PIXEL_LIMIT = TITLE_PIXEL_LIMIT
TITLE_MOBILE_PIXEL_LIMIT = TITLE_PIXEL_LIMIT
TITLE_SEO_MAX_CHARS = 60
TITLE_SEO_MIN_CHARS = 15

DESCRIPTION_PIXEL_LIMIT = 920
DESCRIPTION_DESKTOP_PIXEL_LIMIT = DESCRIPTION_PIXEL_LIMIT
DESCRIPTION_MOBILE_PIXEL_LIMIT = DESCRIPTION_PIXEL_LIMIT
DESCRIPTION_SEO_MAX_CHARS = 160
DESCRIPTION_SEO_MIN_CHARS = 70

# Average character widths for Roboto/Arial at 1px font size.
# MUST stay identical to CHAR_WIDTHS in matrx-frontend
# features/marketing/seo/serp/char-widths.ts.
CHAR_WIDTHS: dict[str, float] = {
    # Narrow characters
    "i": 0.25,
    "j": 0.25,
    "l": 0.25,
    "t": 0.28,
    "f": 0.28,
    "r": 0.33,
    "I": 0.25,
    "J": 0.42,
    "!": 0.25,
    ".": 0.25,
    ",": 0.25,
    ":": 0.25,
    ";": 0.25,
    "|": 0.25,
    "'": 0.17,
    '"': 0.32,
    "`": 0.25,
    # Medium characters
    "a": 0.56,
    "c": 0.5,
    "e": 0.56,
    "g": 0.56,
    "h": 0.56,
    "k": 0.5,
    "n": 0.56,
    "o": 0.56,
    "p": 0.56,
    "q": 0.56,
    "s": 0.5,
    "u": 0.56,
    "v": 0.5,
    "x": 0.5,
    "y": 0.5,
    "z": 0.5,
    "b": 0.56,
    "d": 0.56,
    "A": 0.67,
    "B": 0.67,
    "C": 0.72,
    "D": 0.72,
    "E": 0.61,
    "F": 0.56,
    "G": 0.78,
    "H": 0.72,
    "K": 0.67,
    "L": 0.56,
    "N": 0.72,
    "O": 0.78,
    "P": 0.67,
    "Q": 0.78,
    "R": 0.72,
    "S": 0.67,
    "T": 0.61,
    "U": 0.72,
    "V": 0.67,
    "X": 0.67,
    "Y": 0.67,
    "Z": 0.61,
    # Wide characters
    "m": 0.83,
    "w": 0.72,
    "M": 0.83,
    "W": 0.94,
    # Numbers
    "0": 0.56,
    "1": 0.56,
    "2": 0.56,
    "3": 0.56,
    "4": 0.56,
    "5": 0.56,
    "6": 0.56,
    "7": 0.56,
    "8": 0.56,
    "9": 0.56,
    # Special characters
    " ": 0.28,
    "-": 0.33,
    "_": 0.56,
    "=": 0.58,
    "+": 0.58,
    "(": 0.33,
    ")": 0.33,
    "[": 0.28,
    "]": 0.28,
    "{": 0.33,
    "}": 0.33,
    "<": 0.58,
    ">": 0.58,
    "?": 0.56,
    "/": 0.28,
    "\\": 0.28,
    "&": 0.67,
    "%": 0.89,
    "$": 0.56,
    "#": 0.56,
    "@": 1.0,
}

DEFAULT_CHAR_WIDTH = 0.56


def calculate_text_width(text: str, font_size: int = 16) -> float:
    """Approximate rendered pixel width of ``text`` at ``font_size``. Deterministic."""
    if not text:
        return 0.0
    total_width = 0.0
    for char in text:
        total_width += CHAR_WIDTHS.get(char, DEFAULT_CHAR_WIDTH) * font_size
    return total_width


def calculate_meta_title_metrics(title: str) -> dict:
    """
    Pixel width, character count, and SEO quality signals for a meta title.

    Returns: pixel_width, character_count, desktop_ok, mobile_ok,
    seo_length_ok, too_short, issues, title_ok
    """
    if not title or not title.strip():
        return {
            "pixel_width": 0,
            "character_count": len(title) if title else 0,
            "desktop_ok": False,
            "mobile_ok": False,
            "seo_length_ok": False,
            "too_short": True,
            "issues": ["Title is empty"],
            "title_ok": False,
        }

    pixel_width = calculate_text_width(title, font_size=TITLE_FONT_PX)
    character_count = len(title)

    width_ok = pixel_width <= TITLE_PIXEL_LIMIT
    desktop_ok = mobile_ok = width_ok
    too_short = character_count < TITLE_SEO_MIN_CHARS
    too_long = character_count > TITLE_SEO_MAX_CHARS
    seo_length_ok = not too_short and not too_long

    issues: list[str] = []
    if too_short:
        issues.append(
            f"Title is too short ({character_count} chars; minimum is {TITLE_SEO_MIN_CHARS})"
        )
    if too_long:
        issues.append(
            f"Title is too long ({character_count} chars; maximum is {TITLE_SEO_MAX_CHARS})"
        )
    if not width_ok:
        issues.append(
            f"Title exceeds the width limit ({round(pixel_width)}px > {TITLE_PIXEL_LIMIT}px) and may be truncated"
        )

    return {
        "pixel_width": round(pixel_width),
        "character_count": character_count,
        "desktop_ok": desktop_ok,
        "mobile_ok": mobile_ok,
        "seo_length_ok": seo_length_ok,
        "too_short": too_short,
        "issues": issues,
        "title_ok": width_ok and seo_length_ok,
    }


def calculate_meta_description_metrics(description: str) -> dict:
    """
    Pixel width, character count, and SEO quality signals for a meta description.

    Returns: pixel_width, character_count, desktop_ok, mobile_ok,
    seo_length_ok, too_short, issues, description_ok
    """
    if not description or not description.strip():
        return {
            "pixel_width": 0,
            "character_count": len(description) if description else 0,
            "desktop_ok": False,
            "mobile_ok": False,
            "seo_length_ok": False,
            "too_short": True,
            "issues": ["Description is empty"],
            "description_ok": False,
        }

    pixel_width = calculate_text_width(description, font_size=DESCRIPTION_FONT_PX)
    character_count = len(description)

    width_ok = pixel_width <= DESCRIPTION_PIXEL_LIMIT
    desktop_ok = mobile_ok = width_ok
    too_short = character_count < DESCRIPTION_SEO_MIN_CHARS
    too_long = character_count > DESCRIPTION_SEO_MAX_CHARS
    seo_length_ok = not too_short and not too_long

    issues: list[str] = []
    if too_short:
        issues.append(
            f"Description is too short ({character_count} chars; minimum is {DESCRIPTION_SEO_MIN_CHARS})"
        )
    if too_long:
        issues.append(
            f"Description is too long ({character_count} chars; maximum is {DESCRIPTION_SEO_MAX_CHARS})"
        )
    if not width_ok:
        issues.append(
            f"Description exceeds the width limit ({round(pixel_width)}px > {DESCRIPTION_PIXEL_LIMIT}px) and may be truncated"
        )

    return {
        "pixel_width": round(pixel_width),
        "character_count": character_count,
        "desktop_ok": desktop_ok,
        "mobile_ok": mobile_ok,
        "seo_length_ok": seo_length_ok,
        "too_short": too_short,
        "issues": issues,
        "description_ok": width_ok and seo_length_ok,
    }


def analyze_meta_tags(title: str = "", description: str = "") -> dict:
    """Analyze both meta title and description together."""
    title_metrics = calculate_meta_title_metrics(title)
    description_metrics = calculate_meta_description_metrics(description)

    return {
        "title": title_metrics,
        "description": description_metrics,
        "overall_seo_ok": title_metrics["seo_length_ok"] and description_metrics["seo_length_ok"],
        "overall_display_ok": (
            title_metrics["desktop_ok"]
            and title_metrics["mobile_ok"]
            and description_metrics["desktop_ok"]
            and description_metrics["mobile_ok"]
        ),
    }


def analyze_meta_tags_batch(meta_data: list[dict]) -> list[dict]:
    """Analyze a list of ``{"title": ..., "description": ...}`` objects."""
    results = []
    for item in meta_data:
        title = item.get("title", "")
        description = item.get("description", "")
        analysis = analyze_meta_tags(title, description)
        title_metrics = analysis["title"]
        description_metrics = analysis["description"]
        results.append(
            {
                "title": title,
                "description": description,
                "title_pixels": title_metrics["pixel_width"],
                "title_chars": title_metrics["character_count"],
                "title_ok": title_metrics["title_ok"],
                "title_issues": title_metrics["issues"],
                "description_pixels": description_metrics["pixel_width"],
                "description_chars": description_metrics["character_count"],
                "description_ok": description_metrics["description_ok"],
                "description_issues": description_metrics["issues"],
                "overall_ok": analysis["overall_seo_ok"] and analysis["overall_display_ok"],
            }
        )
    return results


def _stored_field(metrics: dict, ok_key: str) -> dict:
    return {
        "pixel_width": metrics["pixel_width"],
        "character_count": metrics["character_count"],
        "desktop_ok": metrics["desktop_ok"],
        "mobile_ok": metrics["mobile_ok"],
        "seo_length_ok": metrics["seo_length_ok"],
        "too_short": metrics["too_short"],
        "ok": metrics[ok_key],
        "issues": metrics["issues"],
    }


def build_stored_seo_metrics(title: str, description: str, source: str = "scraper") -> dict:
    """
    The canonical PERSISTED payload (contract v1) written to
    ``web.snapshot.seo_metrics`` (scraper, observed) and
    ``web.page.seo_metrics_desired`` (client, desired). Identical shape to the
    TypeScript ``buildStoredSeoMetrics`` in features/seo/serp/metrics.ts.
    """
    title_metrics = calculate_meta_title_metrics(title or "")
    description_metrics = calculate_meta_description_metrics(description or "")
    return {
        "v": 1,
        "source": source,
        "computed_at": datetime.now(UTC).isoformat(),
        "title": _stored_field(title_metrics, "title_ok"),
        "description": _stored_field(description_metrics, "description_ok"),
        "overall_ok": title_metrics["title_ok"] and description_metrics["description_ok"],
    }
