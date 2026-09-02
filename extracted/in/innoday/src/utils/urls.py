"""URL validation shared by the pages that render links and the routes that store them.

``safe_url`` began life in ``src/routers/webui/render.py`` as a *rendering*
guard: refuse to put a ``javascript:`` URL in an ``href``. It lives here now
because the same rule has to run one step earlier as well -- on **write**. A
``javascript:`` value that is only caught at render time is still stored, still
returned by the API, and still reaches every other client of that row; the page
declining to make it clickable is one consumer defending itself, not the value
being rejected.

Keeping a single implementation is the point of the move. Two copies of an
allowlist drift, and the direction they drift in is always "the one you forgot
about accepts more".
"""

from typing import Optional
from urllib.parse import urlsplit

#: The only schemes a link may carry. Everything reaching an ``href`` -- or a
#: stored URL column -- is either a path this app built or a URL somebody else's
#: data supplied; the second kind gets this allowlist.
LINK_SCHEMES = frozenset({"http", "https"})


def safe_url(value: Optional[object]) -> Optional[str]:
    """A URL if it is safe to put in an ``href``, otherwise None.

    ``esc`` escapes, it does not *validate* -- and an escaped
    ``javascript:alert(1)`` is still a working link, because nothing in an
    attribute value needs escaping to run. The URLs on the dashboard come from
    a board sync (``Ticket.url``), a request body (``SummaryItem.pr_url``, which
    no model validates) or the repository table, so all three are attacker-
    reachable by any org member, and the page they land on is one every other
    member loads. This app sends no ``Content-Security-Policy`` header
    (``src/routers/_brand_pages.py``), so there is no second line of defence.

    Anything not ``http``/``https`` returns None. A renderer then draws the row
    as plain text rather than as a link -- the row still says what it says, it
    just stops being clickable -- while a *write* path refuses the value
    outright. Scheme-relative ``//host`` is refused with the rest: it has no
    scheme to check and points off-site regardless.

    ``urlsplit`` is what does the deciding, deliberately, because it strips the
    ASCII tabs and newlines browsers also strip -- so ``java&#9;script:`` is
    recognised as the ``javascript`` scheme it will become, not waved through as
    schemeless. A value it cannot parse at all yields no scheme and is refused;
    failing closed is the only safe direction here.
    """
    if value is None:
        return None
    candidate = str(value).strip()
    if not candidate or candidate.startswith("//"):
        return None
    try:
        scheme = urlsplit(candidate).scheme.lower()
    except ValueError:
        return None
    return candidate if scheme in LINK_SCHEMES else None


def normalised_link(value: Optional[object]) -> Optional[str]:
    """`safe_url`, after supplying the scheme a person typing a link leaves off.

    Used on **hand-entered** URLs only -- the scrum's transcript link is the one
    today. ``meet.google.com/abc-defg`` is what a hand produces when the field's
    only hint is a placeholder, and refusing it is correct but useless: the same
    value is retyped, refused identically, and the record it belongs to is never
    written at all. Completing the scheme turns a dead end into a saved meeting.

    **Only a value with no scheme whatsoever is completed**, and the result still
    goes through `safe_url`. ``javascript:`` and ``mailto:`` already *have* a
    scheme, so they are left alone and refused there -- prefixing them would
    launder precisely the value that check exists to stop. Scheme-relative
    ``//host`` is left alone for the same reason.

    Not folded into `safe_url` because that one also guards *rendering*, where a
    stored value must be shown as it is rather than quietly improved.
    """
    if value is None:
        return None
    candidate = str(value).strip()
    if not candidate:
        return None
    if not candidate.startswith("//"):
        try:
            has_scheme = bool(urlsplit(candidate).scheme)
        except ValueError:
            return None
        if not has_scheme:
            candidate = f"https://{candidate}"
    return safe_url(candidate)
