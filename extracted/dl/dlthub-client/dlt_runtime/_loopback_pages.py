"""HTML served by the loopback login callback server."""

_DLTHUB_LOGO_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 82 25'"
    " role='img' aria-label='dltHub'>"
    "<path fill='#C6D300' d='M30.7337 21.0714H27.2898V24.5H30.7337V21.0714Z'/>"
    "<path fill='#59C1D5' d='M27.2898 3.92856V0.5H23.8459V3.92856V7.35716V10.7857V14.2143V17.6429V21.0714H27.2898V17.6429V14.2143V10.7857H30.7337V7.35716H27.2898V3.92856Z'/>"
    "<path fill='#59C1D5' d='M17.0887 3.92856V7.35716V10.7857V14.2143V17.6429V21.0714V24.5H20.5326V21.0714V17.6429V14.2143V10.7857V7.35716V3.92856V0.5H17.0887V3.92856Z'/>"
    "<path fill='#59C1D5' d='M10.3316 3.92856V7.35716H6.88772H3.44385V10.7857H6.88772H10.3316V14.2143V17.6429V21.0714H6.88772H3.44385V24.5H6.88772H10.3316H13.7755V21.0714V17.6429V14.2143V10.7857V7.35716V3.92856V0.5H10.3316V3.92856Z'/>"
    "<path fill='#59C1D5' d='M3.44388 14.2143V10.7857H0V14.2143V17.6429V21.0714H3.44388V17.6429V14.2143Z'/>"
    "<path fill='#C6D300' d='M44.3786 10.7857H37.4908V0.5H34.0469V24.5H37.4908V14.2143H44.3786V24.5H47.8224V0.5H44.3786V10.7857Z'/>"
    "<path fill='#C6D300' d='M54.5796 7.35718H51.1357V21.0715H54.5796V7.35718Z'/>"
    "<path fill='#C6D300' d='M61.4673 21.0715H54.5796V24.5H64.9112V7.35718H61.4673V21.0715Z'/>"
    "<path fill='#C6D300' d='M71.6684 10.7857H78.5561V7.35716H71.6684V0.5H68.2245V24.5H78.5561V21.0714H71.6684V10.7857Z'/>"
    "<path fill='#C6D300' d='M82 10.7857H78.5562V21.0714H82V10.7857Z'/>"
    "</svg>"
)


def _loopback_html(heading: str, subheading: str, *, error: bool = False) -> bytes:
    text_light = "#d23a3a" if error else "#191937"
    text_dark = "#ff6b6b" if error else "#fff"
    return (
        "<!DOCTYPE html>"
        "<html lang='en'><head><meta charset='utf-8'/>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'/>"
        "<title>dltHub CLI</title><style>"
        ":root{color-scheme:light dark}"
        "html,body{height:100%}"
        "body{margin:0;display:flex;align-items:center;justify-content:center;"
        f"min-height:100dvh;background:#fff;color:{text_light};"
        "font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;"
        "-webkit-font-smoothing:antialiased}"
        "main{text-align:center;padding:2rem;max-width:30rem}"
        "svg{width:160px;height:auto;display:block;margin:0 auto 2rem}"
        "h1{margin:0 0 .5rem;font-size:1.5rem;font-weight:600}"
        "p{margin:0;font-size:1rem;line-height:1.5}"
        f"@media(prefers-color-scheme:dark){{body{{background:#191937;color:{text_dark}}}}}"
        "</style></head><body><main>"
        f"{_DLTHUB_LOGO_SVG}<h1>{heading}</h1><p>{subheading}</p>"
        "</main></body></html>"
    ).encode("utf-8")


_LOOPBACK_SUCCESS_HTML = _loopback_html(
    "You're logged in.",
    "You can close this tab and return to the terminal.",
)
_LOOPBACK_ERROR_HTML = _loopback_html(
    "Login failed.",
    "Return to the terminal for details.",
    error=True,
)
