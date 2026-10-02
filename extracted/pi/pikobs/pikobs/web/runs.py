#!/usr/bin/python3
"""Where the data of a viewer came from.

A viewer names its runs -- control, experience, A120 -- and those names
are whatever the wrapper said. Three suites of the same experiment often
get the same three names, and a month later nobody remembers which
directory each one was read from. So every page ends with the list.

    from pikobs.web.runs import runs_block

    generate_web(..., subtitle=my_text + runs_block(runs, control))

The block is plain HTML because that is what the viewer's ``subtitle``
takes; it has no colour of its own, the viewer styles it in its About
box, at the end, under the explanation.
"""

from typing import Optional, Sequence, Tuple

__all__ = ["runs_block", "runs_text"]


def _pairs(runs: Sequence[Tuple[str, str]],
           control: Optional[Tuple[str, str]] = None):
    """(role, name, path) for every run, the control first."""
    out = []
    seen = set()
    if control:
        out.append(("control", str(control[0]), str(control[1])))
        seen.add(str(control[0]))
    for entry in runs or ():
        try:
            name, path = entry[0], entry[1]
        except (TypeError, IndexError):                # pragma: no cover
            continue
        if str(name) in seen:
            continue
        seen.add(str(name))
        out.append(("experience" if control else "run",
                    str(name), str(path)))
    return out


def runs_text(runs: Sequence[Tuple[str, str]],
              control: Optional[Tuple[str, str]] = None) -> str:
    """The same list as plain text, for a log or a figure caption."""
    return "\n".join(f"{role}: {name} = {path}"
                     for role, name, path in _pairs(runs, control))


def runs_block(runs: Sequence[Tuple[str, str]],
               control: Optional[Tuple[str, str]] = None,
               period: Optional[Tuple[str, str]] = None) -> str:
    """The HTML block for the About box of a viewer, or '' when there is
    nothing to say: a row per run -- its role, its name, its path -- and the
    period. No colour of its own: the viewer styles it."""
    from html import escape
    rows = _pairs(runs, control)
    if not rows:
        return ""
    body = "".join(
        f'<tr><td class="role">{escape(role)}</td><td class="name">{escape(name)}</td>'
        f'<td class="path"><code>{escape(path)}</code></td></tr>'
        for role, name, path in rows)
    when = (f'<p class="period">Period <b>{escape(str(period[0]))}</b> &rarr; '
            f'<b>{escape(str(period[1]))}</b>, every 6 h</p>' if period else "")
    return ('<div class="runs"><p class="runs-title">Data read from</p>'
            f'<table>{body}</table>{when}</div>')
