"""How every InnoDay CLI command opens, and the five colours it may use.

Three things live here because they only make sense together, and kept apart
they drifted: the palette, the command header, and the section rules.

**The shape is not new.** ``blastoff/report.py`` -- the release report -- already
states its subject once in a header, separates sections with ``── Title ──────``
rules, and spends exactly three colours. ``innoday sync`` already steps through
numbered stages. This module is those two conventions made available to every
command, so that a person who has read one InnoDay command's output can read all
of them. The rule itself is imported from blastoff rather than re-drawn, so the
widths cannot drift apart.

**One rocket per run.** The header owns it. A command that prints a second one
(five spinner captions in a row, a panel title above an emoji tagline) is
spending the mark that says "this is InnoDay speaking" on decoration.

**The header goes to stderr.** stdout belongs to the machine -- the same reason
``advisory_console`` exists. A header printed to stdout lands immediately before
``--format json`` output and makes the stream unparseable.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

# The release report's own rule. Imported, not reimplemented: `innoday-blastoff`
# is a hard dependency, `section()` returns plain text with no colour of its
# own, and a second copy of the width constant is how two rule styles start
# appearing in the same output.
from blastoff.report import RULE_WIDTH, section
from rich.console import Console
from rich.markup import escape
from rich.theme import Theme

from src.cli.utils.project_context import load_project_context
from src.version import get_display_version

#: The whole palette. Anything not in here is dim or unstyled.
#:
#: Five tokens, chosen by role rather than by hue, because the CLI had grown
#: two cyans, a blue, a magenta and three greens with no rule saying which
#: meant what. `header` marks InnoDay speaking; `muted` is everything
#: secondary; the last three are the only semantic colours -- good, warning,
#: bad -- and nothing else may claim them.
THEME = Theme(
    {
        "header": "bold cyan",
        "muted": "dim",
        "good": "green",
        "warn": "yellow",
        "bad": "red",
        # An explicit "no emphasis", so a ramp can have a middle value that is
        # a deliberate choice rather than a lookup that fell through.
        "plain": "default",
        # Data ramps, built from the same five so a table cannot introduce a
        # sixth colour by the back door.
        "status.draft": "dim",
        "status.backlog": "dim",
        "status.todo": "dim",
        "status.in_progress": "yellow",
        "status.in_review": "bold cyan",
        "status.done": "green",
        "status.cancelled": "red",
    }
)

#: The CLI's payload stream. Command modules import this instead of building
#: their own bare ``Console()`` -- 23 of them did, which is why ``--no-color``
#: reached almost nothing.
console = Console(theme=THEME)

#: Advisories, spinners and the command header: anything a person needs and a
#: script must not receive. Re-exported by ``formatters`` as
#: ``advisory_console``, which is the name the rest of the CLI knows it by.
advisory = Console(stderr=True, theme=THEME)

#: Every console the CLI writes through, so ``--no-color`` has one place to
#: reach. Command modules keep their own console object -- tests patch them
#: individually -- but they build it here, with the palette attached.
_CONSOLES: List[Console] = [console, advisory]


def make_console(**kwargs: Any) -> Console:
    """A console with the palette, registered for ``--no-color``.

    Command modules call this instead of ``Console()``. Twenty-three of them
    built a bare one, which is both why ``--no-color`` did almost nothing and
    why a palette token printed from one of them would have been an error
    rather than a colour.
    """
    made = Console(theme=THEME, **kwargs)
    _CONSOLES.append(made)
    return made


#: Environment that suppresses the header, and the CI variables that mean
#: nobody is watching the terminal.
_NO_BANNER_ENV = "INNODAY_NO_BANNER"
_CI_ENV = ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL", "TRAVIS")

#: The action lines, in one place so the voice can be read as a set rather than
#: found one command at a time. Present participle, plain, naming the real
#: thing. ``{project}`` and ``{org}`` are filled from the resolved context; a
#: command whose line needs more than that passes ``action=`` itself.
ACTIONS: Dict[str, str] = {
    "init": "Onboarding {project}",
    "join": "Joining {org}, then onboarding {project}",
    "refresh": "Re-onboarding {project}",
    "status": "Checking your connection, identity and assigned work",
    "sync": "Syncing {project}",
    "sync --status": "Checking whether a sync is running",
    "sync ticket": "Fetching one ticket from the board",
    "summary": "Assembling your last {window}",
    "summary --scrum": "Assembling the team's last {window}",
    "timeline": "Reading this project's event history",
    "releases list": "Listing the releases InnoDay has recorded",
    "releases summarize": "Reading what shipped",
    "scope show": "Reading the scope document",
    "scope generate": "Generating tickets from the scope document",
    "upgrade": "Reinstalling the InnoDay CLI from PyPI",
    "scheduler start": "Watching {org}'s board",
    "config init": "Setting up your InnoDay profile",
    "platform init": "Setting up the platform",
}


def set_color_enabled(enabled: bool) -> None:
    """Honour ``--no-color`` on both streams.

    Before this, the flag reached only ``OutputFormatter``: every command
    module's own console kept its colours, so the flag silently did about a
    tenth of what it says.
    """
    for existing in _CONSOLES:
        existing.no_color = not enabled


# --------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------


def rule(title: str, *, style: str = "muted") -> str:
    """``── Title ──────…`` as Rich markup, with the title lifted out of the dim.

    The plain text comes from ``blastoff.report.section`` so a stage rule here
    and a section rule in the release report are the same object at the same
    width (:data:`blastoff.report.RULE_WIDTH`).
    """
    raw = section(title)
    prefix, _, suffix = raw.partition(title)
    return f"[muted]{prefix}[/muted][{style}]{escape(title)}[/{style}][muted]{suffix}[/muted]"


def step_rule(number: int, title: str) -> str:
    """A numbered stage rule: ``── 2. Repositories ──────…``.

    Numbering is not decoration here -- these commands genuinely run stages in
    order, and which stage failed is the question being asked.
    """
    return rule(f"{number}. {title}", style="header")


def print_rule(
    title: str, *, style: str = "muted", stream: Optional[Console] = None
) -> None:
    (stream or console).print(rule(title, style=style))


def print_step(number: int, title: str, *, stream: Optional[Console] = None) -> None:
    (stream or console).print(step_rule(number, title))


def print_done(facts: Sequence[str], *, stream: Optional[Console] = None) -> None:
    """The closing rule: what the run actually did, in counts."""
    out = stream or console
    out.print()
    out.print(rule("Done"))
    if facts:
        out.print(f"[muted]   {escape(' · '.join(str(f) for f in facts))}[/muted]")


# --------------------------------------------------------------------------
# The header
# --------------------------------------------------------------------------


def header_enabled(args: Any) -> bool:
    """Whether this run should print a header.

    Suppressed for the machine (``--format json/csv``, a command's own
    ``--json``), for the person who asked for silence (``--quiet``,
    ``INNODAY_NO_BANNER``), and for CI, where nobody is reading it.
    """
    if os.getenv(_NO_BANNER_ENV, "").lower() in ("1", "true", "yes"):
        return False
    if any(os.getenv(var) for var in _CI_ENV):
        return False
    if getattr(args, "quiet", False):
        return False
    if getattr(args, "json", False):
        return False
    if (getattr(args, "format", None) or "") in ("json", "csv"):
        return False
    return True


def resolve_context(args: Any) -> Dict[str, Optional[str]]:
    """Org, project and workspace for the header's context line.

    Reads the same ``.innoday/project.yml`` every command resolves from, and
    honours ``--dir`` -- a header that ignored it would name the directory the
    process happens to be in rather than the one being acted on.
    """
    context_dir = getattr(args, "dir", None)
    try:
        found = load_project_context(Path(context_dir) if context_dir else None) or {}
    except Exception:
        # A legacy or unreadable project.yml is reported by the entrypoint with
        # far better guidance than a header could give. Say less, not wrong.
        found = {}

    workspace = None
    source = found.get("source_path")
    if source:
        # <workspace>/.innoday/project.yml -> <workspace>
        workspace = str(Path(source).parent.parent)
        home = str(Path.home())
        if workspace.startswith(home):
            workspace = "~" + workspace[len(home) :]

    return {
        "org_alias": found.get("org_alias"),
        "org_name": found.get("org_name"),
        "project_label": found.get("project_alias") or found.get("project_name"),
        "workspace": workspace,
    }


def _api_host(config: Any) -> Optional[str]:
    """The API's host for the context line, or nothing.

    Deliberately total: a header must never be the reason a command fails, and
    ``config`` here is whatever the caller had -- including a test double that
    answers every attribute.
    """
    try:
        url = config.get_api_url()
    except Exception:
        return None
    if not isinstance(url, str) or not url:
        return None
    return url.split("://", 1)[-1].rstrip("/")


def build_command_header(
    command: str,
    action: str,
    *,
    facts: Iterable[str] = (),
    context: Iterable[str] = (),
) -> List[str]:
    """The three lines, as Rich markup. Pure -- no console, no config.

    Every interpolated value is escaped: a workspace path containing ``[`` is a
    real directory name, and Rich would otherwise read it as a style tag.
    """
    lines = [
        f"[header]🚀 InnoDay[/header] [muted]{escape(get_display_version())}"
        f" · {escape(command)}[/muted]",
        rule(action, style="bold"),
    ]
    fact_parts = [str(f) for f in facts if f]
    if fact_parts:
        lines.append(f"[muted]   {escape(' · '.join(fact_parts))}[/muted]")
    ctx_parts = [str(c) for c in context if c]
    if ctx_parts:
        lines.append(f"[muted]   {escape(' · '.join(ctx_parts))}[/muted]")
    return lines


def print_command_header(
    args: Any,
    config: Any = None,
    command: Optional[str] = None,
    *,
    action: Optional[str] = None,
    facts: Iterable[str] = (),
    context: Optional[Sequence[str]] = None,
    show_workspace: bool = False,
    **action_fields: Any,
) -> None:
    """Open a command: identity, what is happening, what it is happening to.

    ``command`` doubles as the key into :data:`ACTIONS`, so the ordinary call
    site is one line and the wording stays reviewable in one place. Pass
    ``action=`` for a line that has to be assembled at runtime.
    """
    if not header_enabled(args):
        return

    ctx = resolve_context(args)
    if action is None:
        # "sync --scope repos" falls back to "sync": a flag narrows what a
        # command does, it does not make it a different command, and writing
        # out every flag combination is how the table stops being readable.
        key = command or ""
        template = ACTIONS.get(key) or ACTIONS.get(key.split(" --")[0], "")
        fields = {
            "project": ctx["project_label"] or "this project",
            "org": ctx["org_name"] or "your organization",
        }
        fields.update({k: v for k, v in action_fields.items() if v is not None})
        try:
            action = template.format(**fields)
        except KeyError:
            action = template
    if not action:
        return

    context_parts = list(context) if context is not None else []
    if context is not None:
        pass
    elif ctx["org_alias"] and ctx["project_label"]:
        context_parts.append(f"{ctx['org_alias']}/{ctx['project_label']}")
    elif ctx["org_alias"]:
        context_parts.append(str(ctx["org_alias"]))
    if context is None:
        host = _api_host(config) if config is not None else None
        if host:
            context_parts.append(host)
        if show_workspace and ctx["workspace"]:
            context_parts.append(ctx["workspace"])

    for line in build_command_header(
        command or "", action, facts=facts, context=context_parts
    ):
        advisory.print(line)


def print_identity() -> None:
    """``--version`` and ``version``: the header's first line, alone.

    The ASCII box this replaces had a hardcoded 39-column interior and appeared
    nowhere else in the product, so it taught a reader nothing about what the
    rest of the CLI looks like.
    """
    console.print(
        f"[header]🚀 InnoDay[/header] [muted]{escape(get_display_version())}[/muted]"
    )


__all__ = [
    "ACTIONS",
    "RULE_WIDTH",
    "THEME",
    "advisory",
    "build_command_header",
    "console",
    "make_console",
    "header_enabled",
    "print_command_header",
    "print_done",
    "print_identity",
    "print_rule",
    "print_step",
    "resolve_context",
    "rule",
    "set_color_enabled",
    "step_rule",
]
