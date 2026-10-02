"""What the viewer says under a figure, and where the documentation is.

The viewer shows, under the figure, a short note for each value chosen
that has one -- what a metric shows, what a matched comparison means --
with a link to the documentation for the rest. The notes that mean the
same in every module go in COMMON_NOTES; each module passes its own to
generate_web (value_notes=...). Both are empty for now: they are written
module by module.

The documentation will move. Its address is DOC_URL, read from
$PIKOBS_DOC_URL when it is set, so a new address needs no change of the
code; the default below is the address of today.
"""
import os

#: where the documentation lives today; $PIKOBS_DOC_URL moves it, and Pikobs
#: Web takes it from here too
DEFAULT_DOC_URL = "https://goc-dx-u3.science.gc.ca/~dlo001/Pikobs/docs/build/html"
DOC_URL = os.environ.get("PIKOBS_DOC_URL", DEFAULT_DOC_URL).rstrip("/")

#: key -> value -> HTML note, the same in every module
COMMON_NOTES = {}


def doc_link(page=None, anchor=None):
    """The address of a page of the documentation, or None without one."""
    if not DOC_URL or not page:
        return None
    return f"{DOC_URL.rstrip('/')}/{page}.html" + (f"#{anchor}" if anchor else "")


def notes_for(module_notes=None):
    """The notes of a viewer: the common ones, and the module's over them."""
    out = {k: dict(v) for k, v in COMMON_NOTES.items()}
    for k, v in (module_notes or {}).items():
        out.setdefault(k, {}).update(v)
    return out
