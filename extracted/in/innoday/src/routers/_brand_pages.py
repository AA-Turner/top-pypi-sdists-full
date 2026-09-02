"""Shared Pixelfuel-branded HTML shell for the hosted auth pages (PF-350).

The device-approval page (``src/routers/device.py``) and the invite-accept page
(``src/routers/invites.py``) are both small, self-contained, dark Pixelfuel-brand
pages with identical chrome (background, card, brand wordmark, button, message
styles). ``brand_page`` owns that shared shell so each route supplies only its
own inner body + script.

``BRAND_TOKENS`` and ``BRAND_FONTS`` are exported because the signed-in web
surface (``src/routers/webui/``) is a *wide* page with a top bar rather than a
centred card, so it cannot reuse this shell -- but it must not re-declare the
palette. Both import the same tokens; only the chrome differs.

These pages are intentionally dependency-free (no external CSS, JS or fonts).
That is a weight-and-portability choice, not a CSP requirement: this app sets no
``Content-Security-Policy`` header at all. (An earlier version of this docstring
asserted "the strict CSP the API serves them under" -- there has never been one.
Keep the pages self-contained anyway, so adding one later breaks nothing.)
"""

import re
from urllib.parse import quote

# Values read from pixelfuel-website: tailwind.config.js, app/globals.css and
# components/ui/PixelFuelLogo.tsx. Keep them in sync with that repo, not with taste.
BRAND_TOKENS = (
    "--bg:#0a0a0a; --bg2:#1a1a2e; --orange:#F15B35; --amber:#fbbf24; --muted:#9aa0aa;"
)

# The brand's own declared fallback chains (tailwind.config.js `fontFamily`).
# Inter and Special Elite are named first and degrade to system equivalents -- no
# webfont is fetched. Self-hosting both as woff2 under /ui/static is a follow-up.
BRAND_FONTS = (
    '--font-ui:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;'
    ' --font-type:"Special Elite","Courier New",ui-monospace,monospace;'
)

# --------------------------------------------------------------------------- #
# The tab icon
# --------------------------------------------------------------------------- #

#: InnoDay's rocket, drawn for a 16px browser tab. Every page shell below and in
#: `webui/render.py` carries it; before this there was no `<link rel="icon">` on
#: any page at all, so every InnoDay tab showed the browser's blank default.
#:
#: **Not `icons.ROCKET_SVG` scaled down**, and the difference is the whole point.
#: That mark is pixel blocks -- yellow nose, orange body, three blocks abreast for
#: the fins -- which is right at 15px *tall beside the wordmark*, where the word
#: supplies the context. Alone in a square at 16px it renders as an **orange plus
#: sign**: the fins sit level with the body, and a yellow nose above a yellow
#: plume is vertically symmetric, so nothing says which way is up. Rasterised and
#: checked at 16px, four block-based attempts all read as a cross.
#:
#: So the tab icon is drawn from the silhouette instead: a triangular nose, a
#: body, fins swept *back* past the body's base, and a flame below. The asymmetry
#: is what makes it a rocket at 8x8 effective pixels. Three things it keeps from
#: the block version: the two brand colours in the same roles (amber nose and
#: flame, orange body), the dark plate -- `--bg`, because a transparent icon sits
#: on browser chrome that may be white, where amber on white nearly vanishes --
#: and the rounded corner radius of the app's own cards.
#:
#: A window in the body was tried and dropped: at 16px it fills with the plate
#: colour and reads as a hole punched through the rocket.
FAVICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    '<rect width="32" height="32" rx="7" fill="#0a0a0a"/>'
    '<polygon points="16,1.5 21.5,11 10.5,11" fill="#fbbf24"/>'
    '<rect x="10.5" y="11" width="11" height="9.5" fill="#F15B35"/>'
    '<polygon points="10.5,20.5 10.5,28 5.5,24.5" fill="#F15B35"/>'
    '<polygon points="21.5,20.5 21.5,28 26.5,24.5" fill="#F15B35"/>'
    '<polygon points="12.8,20.5 19.2,20.5 16,30.5" fill="#fbbf24" opacity=".95"/>'
    "</svg>"
)


def favicon_link() -> str:
    """The tab icon as a `<link>`, ready for a page `<head>`.

    A `data:` URI rather than a served file, for the reason the glyphs above are
    inline: there is no static mount to put one in, and adding
    `StaticFiles` to serve 400 bytes would be the largest change on the page.

    Percent-encoded rather than base64, so the mark stays legible in the markup.
    **The `safe` set is load-bearing and deliberately small.** A double quote left
    unencoded ends the `href` attribute at the SVG's own first `xmlns="`, and a
    `#` ends the URI at the first colour -- in both cases the browser gets a
    truncated document, renders nothing, and reports no error. An earlier version
    of this listed `"` and `<` as safe and shipped exactly that: the attribute
    read `href="data:image/svg+xml,<svg xmlns="`. Nothing about the page looked
    wrong, and a test comparing the emitted link against this same function
    could not see it -- `tests/test_summary_ui.py` now decodes the attribute out
    of the rendered page and compares it to `FAVICON_SVG`, which is a check that
    can fail.
    """
    body = quote(FAVICON_SVG, safe="/:=,.")
    return f'<link rel="icon" href="data:image/svg+xml,{body}"/>'


#: Comment syntaxes that exist for whoever reads the source, not for the browser.
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_WHOLE_LINE_COMMENT = re.compile(r"^[ \t]*//.*$", re.M)
_BLANK_RUN = re.compile(r"\n\s*\n\s*\n+")


def strip_authoring_comments(source: str) -> str:
    """Remove source comments from CSS or JS before it is inlined into a page.

    **These pages have no static mount**, so every stylesheet and script is
    embedded in every response. This repo comments its CSS heavily -- and rightly,
    the rationale belongs next to the rule -- but that made 19% of `_APP_CSS`
    (10.8 KB) prose shipped to every browser on every page load, and created a
    subtler problem:

    **A substring assertion against a rendered page was searching the source.**
    Page tests check `"some phrase" in page`, and `page` contains the whole
    stylesheet. Two tests passed for the wrong reason because of it:
    `assert "no date set" in page` went on succeeding after that label was
    removed, satisfied by a CSS comment describing the class that used to render
    it; and an unrelated `assert "closed" not in page` failed against a comment
    that merely used the word. Stripping here means a comment can no longer stand
    in for behaviour, for every test that exists now or later, rather than each
    one having to remember the hazard.

    Two syntaxes, and the second is deliberately narrow:

    * ``/* ... */`` everywhere. Verified safe by inspection -- no quoted literal
      in either stylesheet or the script contains a delimiter.
    * ``//`` **only when it is the whole line.** An inline rule would eat the
      ``//`` in every URL. All 30 line comments in `_COPY_JS` are whole-line and
      none of its lines carries an inline one, so the narrow rule loses nothing
      and cannot corrupt a link.

    Applied once at import, so it costs nothing per request. The comments stay
    exactly where they are in the source, which is the only place they were ever
    for.
    """
    out = _BLOCK_COMMENT.sub("", source)
    out = _WHOLE_LINE_COMMENT.sub("", out)
    return _BLANK_RUN.sub("\n\n", out)


# Concatenated (NOT an f-string) so the CSS braces below need no escaping.
_BRAND_CSS_SOURCE = (
    "\n  :root { "
    + BRAND_TOKENS
    + " }"
    + """
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         background:radial-gradient(1200px 600px at 50% -10%, var(--bg2), var(--bg));
         color:#fff; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif; }
  .card { width:min(440px,92vw); background:rgba(255,255,255,0.03);
          border:1px solid rgba(255,255,255,0.08); border-radius:18px; padding:40px 32px;
          box-shadow:0 24px 60px rgba(0,0,0,0.5); }
  .brand { font-weight:800; letter-spacing:-0.02em; font-size:20px;
           background:linear-gradient(90deg,var(--orange),var(--amber));
           -webkit-background-clip:text; background-clip:text; color:transparent; }
  h1 { font-size:22px; margin:18px 0 6px; }
  p { color:var(--muted); font-size:14px; line-height:1.5; margin:0 0 20px; }
  label { display:block; font-size:12px; text-transform:uppercase; letter-spacing:0.08em;
          color:var(--muted); margin-bottom:8px; }
  input { width:100%; padding:14px 16px; font-size:18px; letter-spacing:0.15em; text-align:center;
          background:#000; border:1px solid rgba(255,255,255,0.14); border-radius:12px; color:#fff;
          font-family:ui-monospace,SFMono-Regular,Menlo,monospace; text-transform:uppercase; }
  input:focus { outline:none; border-color:var(--orange); }
  button { width:100%; margin-top:18px; padding:14px; font-weight:800; font-size:15px; cursor:pointer;
           border:none; border-radius:999px; color:#fff;
           background:linear-gradient(90deg,var(--orange),#ff7a4a);
           box-shadow:0 8px 24px rgba(241,91,53,0.35); transition:transform .06s ease; }
  button:active { transform:translateY(1px); }
  .msg { margin-top:16px; font-size:14px; text-align:center; min-height:20px; }
  .ok { color:var(--amber); } .err { color:#ff6b6b; }
"""
)


#: What is actually served -- see `strip_authoring_comments`.
_BRAND_CSS = strip_authoring_comments(_BRAND_CSS_SOURCE)


def brand_page(title: str, card_html: str, script_js: str) -> str:
    """Wrap ``card_html`` (the inner .card contents) + ``script_js`` in the
    shared Pixelfuel page shell. ``title`` sets the browser tab title.

    ``card_html``/``script_js`` are already-rendered HTML/JS strings (each route
    builds its own via an f-string, so any interpolation/escaping is the caller's
    concern) — they are inserted verbatim.
    """
    return (
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8"/>\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
        f"<title>{title}</title>\n"
        f"{favicon_link()}\n"
        f"<style>{_BRAND_CSS}</style></head>\n"
        f'<body><div class="card">\n{card_html}\n</div>\n'
        f"<script>\n{script_js}\n</script>\n"
        "</body></html>"
    )
