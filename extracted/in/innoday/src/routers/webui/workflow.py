"""The workflow launcher at ``/ui/{org}/workflow`` -- markup, CSS and script.

A **sibling of** ``render.py`` rather than more of it. That module is 4,195
lines and owns the sign-in card, the dashboard, the profile, project and team
pages; this page shares none of their structure and all of their chrome, so it
takes the chrome by importing (``_page``, ``_user_menu``, ``_wordmark``,
``esc``, ``_copyable``, ``_summary_prose``) and keeps its own
layout here. Same convention in every other respect: everything is a Python
string, there is no template engine, no build step and no external asset --
this app has no static mount, so every byte of CSS and script is inlined.

**What the page is.** Not a dashboard. Pick a project for context, pick a
workflow, walk one to three steps, finish. Data appears only at the step that
needs it to make a decision, which is why the whole org's worth of it is read
once, up front, and handed to ``workflow_page`` as four already-batched dicts
rather than fetched per card -- the rule ``_render_dashboard`` states as "two
queries for every card's summaries, not two per card".

**Steps are data, not markup.** ``_workflow_specs`` emits a JSON document that
the script at the bottom renders; there is no hand-written markup per step.
That is the one structural decision worth defending, because this surface is
temporary by design: when ``pixelfuel-ui`` replaces the server-rendered pages,
this page lifts as a single file -- a spec array and a small dependency-free
engine -- instead of being rewritten from nine bespoke fragments.

**Two kinds of string cross into the script**, and confusing them is the bug
this page would have:

* ``bodies`` values are **HTML this module built and already escaped**. The
  engine assigns them with ``innerHTML``.
* everything else (a ticket ref, a summary, an owner) is **raw text**, escaped
  by the script's own ``esc`` at the moment it is interpolated.

The JSON itself is written with ``<``, ``>`` and ``&`` escaped as ``\\uXXXX``,
so no value can close the ``<script>`` element that carries it. That matters
more here than on the other pages: this app sends no ``Content-Security-Policy``
header at all, and ``Ticket.url`` and ``SummaryItem.pr_url`` are reachable by
anyone who can write to a board.

**Eight of the ten workflows record nothing, and every one of them says so.**
Only ``run-scrum`` and ``give-scrum-update`` write a row today. The other eight are the map of what this
page will do -- dropping them would leave a launcher that silently offers less
than the product has -- but a walkthrough that collapses each step to a green
tick and finishes with "done" is a receipt for work nobody did. So the state is
carried as data on the workflow (``saves``/``warn``/``done`` -- see
``_unwired``), the engine reads it, and every unwired step carries the warning
while its receipt reads "not saved" and its completion panel names the command
or page that does the real thing. Wiring one up later flips one flag.

**The scrum walk writes as it walks.** It is the one workflow here that records
anything, and it does so through ``POST /ui/{org}/scrums`` and its two children
(see ``webui/routes.py``) -- same-origin ``fetch``, session cookie, never
``/api/v1``, which a browser cannot authenticate against. The row is opened when
the walk step appears and one ``ScrumTicketVisit`` is posted as each stop ends,
so an interrupted run still leaves the record of itself. Every failure is
painted into ``#wferr`` -- and beside the offending input when the server names
one; the page never reports a save it did not get, and never reports a failure
it did not get either.

**Dark only.** The app has no light theme and no toggle, so this page commits
to the same single world rather than inventing one production does not have.

**One accent.** An earlier pass gave each pillar its own colour; it was
decoration standing in for structure, since the pillar label already says which
pillar it is. Everything highlighted here is ``--orange``.
"""

import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence

from src.domain.organization import Organization
from src.domain.ticket import TicketStatus
from src.domain.user import User
from src.page_paths import (
    UI_PREFIX,
    dashboard_path,
    new_project_path,
    project_path,
)
from src.routers._brand_pages import (
    BRAND_FONTS,
    BRAND_TOKENS,
    strip_authoring_comments,
)
from src.routers.webui.data import ProjectCard, ProjectTicketRow, ScrumActivity
from src.routers.webui.render import (
    EM_DASH,
    _app_nav,
    _bubbles,
    _copyable,
    _page,
    _shell,
    _status_pill,
    _summary_prose,
    _user_menu,
    _wordmark,
    esc,
)
from src.services import scrum_service

#: The pillars, in the order they are read. Not alphabetical and not a
#: preference: it is the order work actually moves through -- you vibe something
#: into existence, plan it, build it, release it -- so a reader scanning left to
#: right is scanning forward in time.
PILLARS = ("vibing", "planning", "building", "releasing")

#: How long a ticket sits in flight before the walk calls it out. Seven days
#: because a stand-up runs daily and a working week is the first interval where
#: "still here" stops being normal.
LINGER_DAYS = 7

#: How far back the personal update looks for finished work worth bringing back.
#: **Taken from the service that enforces it, not chosen here.** It began as an
#: alias of `LINGER_DAYS` -- a different question ("how long has this sat in
#: flight?") that happened to have the same answer -- and that was fine while the
#: number only decided what to *show*. It now also decides what
#: `scrum_service._pick_is_eligible` will *apply*, and a page offering a wider
#: window than the applier accepts refuses a pick it just rendered, for the people
#: at the edge of the window only. One owner, so they cannot disagree.
REOPEN_WINDOW_DAYS = scrum_service.REOPEN_WINDOW_DAYS

#: How many unowned tickets the update offers to take on. Bigger than `PICK_CAP`
#: because this list is the whole point of the step -- surfacing work nobody has
#: -- and a person scanning for something to pick up is doing a different job from
#: a person confirming a decision the page already made for them.
TAKE_CAP = 25

#: The walk is a meeting, not a report. Past twenty tickets it is not a
#: stand-up any more, and a cap that truncates loudly beats a queue nobody
#: finishes.
WALK_CAP = 20

#: How many rows a picker step shows before it stops being a decision.
PICK_CAP = 8

#: The two statuses the scrum walk moves through, in the order it moves through
#: them. **IN_REVIEW is labelled "In test" in the UI and nowhere else.** There
#: is no ``IN_TEST`` status and there deliberately never has been -- the enum is
#: draft, backlog, todo, in progress, in review, done, cancelled. ``data.py``
#: records the decision in as many words at the comment on ``ProjectCard``:
#: inventing one "would misreport rather than reveal". The label is a word on a
#: chip; the status underneath it is the board's own.
WALK_STATUSES = (TicketStatus.IN_REVIEW, TicketStatus.IN_PROGRESS)

_STATUS_LABELS = {
    TicketStatus.IN_REVIEW.value: "In test",
    TicketStatus.IN_PROGRESS.value: "In progress",
}


# --------------------------------------------------------------------------- #
# Style
# --------------------------------------------------------------------------- #

_WORKFLOW_CSS_SOURCE = (
    """
  /* The brand values arrive twice on this page and that is deliberate: `_page`
     ships them in `_APP_CSS`, and they are re-emitted here from the *same
     constants* so this block is self-sufficient. The point of the page is that
     it lifts into `pixelfuel-ui` as one file; a stylesheet that silently
     depends on a 195KB sibling does not lift. Re-emitting an imported constant
     is not redeclaring a colour -- there is still exactly one place either
     value is written down. */
  /* Declared on the page root rather than on `:root`, so lifting this file
     cannot restyle whatever it is lifted into. Custom properties inherit, so
     every descendant reads them exactly as it would from `:root`.

     The structural neutrals below -- surfaces, hairlines and body text for a
     page built out of stacked cards -- are the ones the brand tokens do not
     name. The three status hues are read from `_APP_CSS`'s own `--s-*` tokens
     rather than restated, with the literal only as the lifted-file fallback:
     "in progress" must not be one green on the dashboard and another here. */
  .wfpage { """
    + BRAND_TOKENS
    + " "
    + BRAND_FONTS
    + """
    --wf-surface:#131320; --wf-surface2:#1b1b2b;
    --wf-line:#2a2a3d; --wf-line2:#383850; --wf-text:#e8e8ef;
    --wf-green:var(--s-live, #4ade80);
    --wf-violet:var(--s-rev, #a78bfa);
    --wf-slate:var(--s-done, #8b9cb3);
    display:block; max-width:1080px; color:var(--wf-text);
  }

  /* ---- project rail ---- */
  .wfpage .railhead { display:flex; align-items:baseline; justify-content:space-between;
                      gap:16px; margin-bottom:12px; flex-wrap:wrap; }
  .wfpage .railhead .lbl { font-family:var(--font-type); font-size:10.5px;
                           letter-spacing:.2em; text-transform:uppercase; color:var(--muted); }
  .wfpage .railhead .hint { font-size:12px; color:var(--muted); }

  .wfpage .rail { display:flex; flex-wrap:wrap; gap:10px; }
  /* A `div` with `role="button"`, not a `<button>`. The star is a form and the
     arrow is a link, and neither may be nested inside a button element -- the
     markup would be invalid and browsers recover from it by hoisting the form
     out of the block, which breaks the layout in a way that only shows up on
     some engines. The keyboard affordance is restored explicitly below. */
  .wfpage .block { display:flex; flex-direction:column; gap:7px; min-width:118px;
                   padding:12px 13px 10px; border:1px solid var(--wf-line);
                   border-radius:10px; background:var(--wf-surface); cursor:pointer;
                   text-align:left;
                   transition:opacity .22s ease, border-color .22s ease,
                              background .22s ease, transform .22s ease; }
  .wfpage .block:hover { border-color:var(--wf-line2); transform:translateY(-1px); }
  /* `.alias` and `.star` are `_APP_CSS`'s, on purpose: the chip a project wears
     here is the chip it wears on its card and in its page header, and a second
     definition is how those three drift apart. Only the two properties the rail
     needs and the card does not are set. */
  .wfpage .block .alias { align-self:flex-start; background:var(--wf-line2);
                          transition:background .22s ease; }
  .wfpage .block.is-active { border-color:rgba(241,91,53,.55); background:var(--wf-surface2); }
  .wfpage .block.is-active .alias { background:linear-gradient(135deg,var(--orange),#ff8a5c); }
  .wfpage .block .foot { display:flex; align-items:center; justify-content:space-between; gap:8px; }
  .wfpage .block .starform { display:flex; flex:none; }
  .wfpage .out { font-size:12px; color:var(--muted); line-height:1;
                 padding:2px 4px; border-radius:4px;
                 transition:color .18s ease, background .18s ease; }
  .wfpage .out:hover { color:var(--orange); background:rgba(241,91,53,.1); }

  /* Context, not navigation: the rail dims to say "this is the project the
     steps below are about" without ever leaving the page. */
  .wfpage .viewport.focused .block:not(.is-active) { opacity:.22; pointer-events:none; }
  .wfpage .viewport.focused .block.is-active { border-color:rgba(241,91,53,.7); }
  /* The rule above covers the *inactive* blocks only, and the active block's
     star is a form and its arrow a link -- both still live. Ten tickets into a
     scrum, one click on either navigated away: `ended_at` stayed NULL, which is
     how this schema spells "abandoned", and the typed comments went with it.
     The script disables them too (a pointer rule does not stop the keyboard). */
  .wfpage .viewport.focused .block .starform,
  .wfpage .viewport.focused .block .out { opacity:.3; pointer-events:none; }

  /* ---- pillar grid ---- */
  .wfpage .chooser { margin-top:22px; max-height:520px; opacity:1;
                     transition:max-height .34s ease, opacity .2s ease, transform .28s ease; }
  .wfpage .chooser.is-out { max-height:0; opacity:0; transform:translateY(-18px);
                            overflow:hidden; pointer-events:none; }
  .wfpage .grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }
  .wfpage .pillar { display:flex; flex-direction:column; gap:8px; }
  .wfpage .pillar > .wname { font-family:var(--font-type); font-size:11px;
                             letter-spacing:.18em; text-transform:uppercase; color:var(--muted);
                             padding-bottom:8px; border-bottom:1px solid var(--wf-line); }
  .wfpage .wf { padding:11px 12px; border:1px solid var(--wf-line); border-radius:9px;
                background:rgba(27,27,43,.5); cursor:pointer; text-align:left;
                font:inherit; font-size:13.5px; font-weight:600; color:inherit; line-height:1.3;
                transition:border-color .18s ease, background .18s ease, transform .18s ease; }
  .wfpage .wf:hover { border-color:rgba(241,91,53,.5); background:var(--wf-surface2);
                      transform:translateY(-2px); }
  /* The daily tick. `display:flex` on the button rather than on the tick, so the
     mark sits at the end of the line without the label losing its own wrapping.
     `--wf-green` is the app's own "live" token, read the same way every other
     status colour on this page is -- a second green here is how the dashboard and
     this page come to disagree about what "done today" looks like. */
  .wfpage .wf { display:flex; align-items:baseline; gap:8px; }
  .wfpage .wf .wtick { margin-left:auto; flex:none; font-style:normal;
                       font-size:12.5px; color:var(--wf-green); }
  .wfpage .wf .wtick[hidden] { display:none; }

  /* ---- the runner ---- */
  .wfpage .runner { display:none; margin-top:20px; flex-direction:column; }
  .wfpage .runner.is-live { display:flex; }
  .wfpage .runhead { display:flex; align-items:center; justify-content:space-between;
                     gap:14px; flex-wrap:wrap;
                     padding-bottom:12px; border-bottom:1px solid var(--wf-line); }
  .wfpage .runhead .who { display:flex; align-items:baseline; gap:10px; }
  .wfpage .runhead .pill { font-family:var(--font-type); font-size:10px;
                           letter-spacing:.16em; text-transform:uppercase; color:var(--muted); }
  .wfpage .runhead .title { font-size:15px; font-weight:600; }
  .wfpage .runctl { display:flex; align-items:center; gap:14px; }
  /* Position, not progress: the row says which step of how many, which is the
     one thing the collapsed receipts above stop being able to say. */
  .wfpage .dots { display:flex; gap:6px; align-items:center; }
  .wfpage .dots i { width:7px; height:7px; border-radius:50%; background:var(--wf-line2);
                    display:block; transition:background .24s ease, transform .24s ease; }
  .wfpage .dots i.on { background:var(--orange); transform:scale(1.18); }
  .wfpage .dots i.past { background:rgba(241,91,53,.4); }
  .wfpage .quit { border:1px solid var(--wf-line); background:none; color:var(--muted);
                  font:inherit; font-size:12px; padding:4px 11px; border-radius:999px;
                  cursor:pointer; transition:color .18s ease, border-color .18s ease; }
  .wfpage .quit:hover { color:var(--wf-text); border-color:var(--wf-line2); }

  /* **Bottom-anchored.** The stack grows downward from a floor, so a step
     rising into it pushes the finished ones up on its own -- no scroll maths,
     and the thing you are meant to be reading is always in the same place. */
  .wfpage .wstack { display:flex; flex-direction:column; justify-content:flex-end;
                    gap:9px; min-height:380px; padding-top:14px; }
  .wfpage .step { border:1px solid var(--wf-line); border-radius:11px;
                  background:var(--wf-surface); padding:15px 16px;
                  transition:opacity .24s ease, transform .24s ease,
                             padding .24s ease, background .24s ease, border-color .24s ease; }
  .wfpage .step.enter { opacity:0; transform:translateY(26px); }
  .wfpage .step .shead { display:flex; align-items:baseline; gap:10px; margin-bottom:4px; }
  .wfpage .step .idx { font-family:var(--font-type); font-size:10.5px;
                       letter-spacing:.12em; color:var(--orange); }
  .wfpage .step .wstitle { font-size:14.5px; font-weight:600; }
  .wfpage .step .guide { color:var(--muted); font-size:13px; margin:0 0 13px; }
  /* A finished step collapses to a one-line receipt. It has to stay on the page
     -- it is what you just decided -- and it must stop competing with the step
     that is asking you something now. */
  .wfpage .step.wdone { padding:9px 14px; background:rgba(19,19,32,.5);
                        border-color:rgba(42,42,61,.7); }
  .wfpage .step.wdone .guide,
  .wfpage .step.wdone .wbody,
  .wfpage .step.wdone .act { display:none; }
  .wfpage .step.wdone .shead { margin-bottom:0; }
  .wfpage .step.wdone .wstitle { font-size:13px; font-weight:500; color:var(--muted); }
  .wfpage .step.wdone .idx { color:var(--wf-green); }
  .wfpage .step.wdone .idx::after { content:" \\2713"; }
  /* A step that wrote nothing must not leave the same receipt as one that did.
     Eight of the nine workflows record nothing yet, and the collapsed receipt is
     exactly where that stops being visible -- the body carrying the warning is
     hidden by the rule above -- so the receipt states it itself. */
  .wfpage .step.wdone.unwired .idx { color:var(--amber); }
  .wfpage .step.wdone.unwired .idx::after { content:" \\2014 not saved"; }

  /* ---- controls inside a step ---- */
  .wfpage .wbody { display:flex; flex-direction:column; gap:10px; }
  .wfpage .field { display:flex; flex-direction:column; gap:5px; }
  .wfpage .field label { font-family:var(--font-type); font-size:10px;
                         letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }
  .wfpage .field input, .wfpage .field textarea {
      background:rgba(10,10,10,.6); border:1px solid var(--wf-line);
      border-radius:7px; padding:9px 11px; color:var(--wf-text);
      font:inherit; font-size:13.5px; width:100%; }
  .wfpage .field textarea { min-height:70px; resize:vertical; line-height:1.5; }
  .wfpage .field input:focus, .wfpage .field textarea:focus {
      outline:2px solid var(--orange); outline-offset:1px; }

  .wfpage .wrow { display:flex; align-items:center; gap:10px;
                  padding:8px 11px; border:1px solid var(--wf-line); border-radius:7px;
                  background:rgba(10,10,10,.4); font-size:13px; }
  .wfpage .wrow .wgrow { flex:1; min-width:0; overflow:hidden;
                         text-overflow:ellipsis; white-space:nowrap; }
  .wfpage .wrow .meta { color:var(--muted); font-size:12px; flex:none; }
  .wfpage .wrow .ref { font-family:var(--font-type); font-size:11.5px; color:var(--muted); }
  .wfpage .wrow input[type=checkbox] { accent-color:var(--orange);
                                       width:15px; height:15px; flex:none; }

  /* The comment box under a pick. Indented to the width of the checkbox and its
     gap so it reads as belonging to the row above it rather than as a control of
     its own -- the two are one answer about one ticket. */
  .wfpage .pcom { margin:-2px 0 8px 26px; }
  .wfpage .pcom textarea { width:100%; box-sizing:border-box; min-height:44px;
                           resize:vertical; line-height:1.5;
                           padding:7px 10px; font:inherit; font-size:12.5px;
                           color:var(--fg); background:rgba(10,10,10,.4);
                           border:1px solid var(--wf-line); border-radius:7px; }
  .wfpage .pcom textarea:focus { outline:2px solid var(--orange); outline-offset:1px; }

  .wfpage .wchip { font-family:var(--font-type); font-size:10.5px; letter-spacing:.07em;
                   padding:3px 8px; border-radius:5px; flex:none;
                   background:rgba(241,91,53,.14); color:var(--orange); }
  .wfpage .wchip.g { background:rgba(74,222,128,.13); color:var(--wf-green); }
  .wfpage .wchip.v { background:rgba(167,139,250,.14); color:var(--wf-violet); }
  .wfpage .wchip.a { background:rgba(251,191,36,.13); color:var(--amber); }
  .wfpage .wchip.n { background:rgba(139,156,179,.13); color:var(--wf-slate); }

  /* `_copyable` on its own line. The command chip is `_APP_CSS`'s `.initcmd`,
     unchanged -- a command reads the same everywhere in this app or it stops
     being recognisable as one. */
  .wfpage .cmdrow { display:flex; }

  .wfpage .note { font-size:12.5px; color:var(--muted);
                  border-left:2px solid var(--wf-line2); padding:2px 0 2px 11px; }
  .wfpage .note b { color:var(--amber); font-weight:600; }
  .wfpage .note a { color:var(--orange); text-decoration:underline; }
  .wfpage .note.warn { border-left-color:var(--orange); }

  /* What the scrum walk says when a write did not land. It sits above the
     stack rather than inside a step, because the failure it reports outlives
     the step that was on screen when it happened -- a stop that never reached
     the server is still missing three steps later, and a message that scrolled
     away with its step would be a page quietly dropping the bad news. */
  .wfpage .wferr { font-size:12.5px; color:var(--orange); margin:0 0 12px;
                   white-space:pre-line;
                   border:1px solid var(--orange); border-radius:7px;
                   padding:9px 11px; background:rgba(10,10,10,.45); }
  .wfpage .wferr[hidden] { display:none; }

  /* A refusal that names one field belongs next to that field, not only in the
     banner above. The transcript input's only hint is its placeholder, so a
     message shown anywhere else leaves the box that caused it looking fine. */
  .wfpage .field .ferr { font-family:var(--font-type); font-size:10.5px;
                         font-style:normal; letter-spacing:.04em;
                         color:var(--orange); }
  .wfpage .field input.bad, .wfpage .field textarea.bad {
                         border-color:var(--orange); }

  .wfpage .wprose { font-size:13px; line-height:1.65; color:var(--wf-text);
                    background:rgba(10,10,10,.45); border:1px solid var(--wf-line);
                    border-radius:7px; padding:12px 13px; }
  .wfpage .wprose .sbody { color:var(--wf-text); }
  .wfpage .wprose .sbody:first-child { margin-top:0; }

  .wfpage .act { display:flex; align-items:center; gap:10px; margin-top:13px; }
  .wfpage .go { border:0; border-radius:8px; cursor:pointer;
                font:inherit; font-size:13px; font-weight:700; padding:9px 18px;
                color:#14121a; background:linear-gradient(135deg,var(--orange),#ff8a5c);
                transition:filter .18s ease, transform .18s ease; }
  .wfpage .go:hover { filter:brightness(1.08); transform:translateY(-1px); }
  .wfpage .go.danger { background:linear-gradient(135deg,#ff8a5c,var(--amber)); }

  /* Completion flashes and then **waits**. Restoring the grid on a timer would
     take the conclusion away before it had been read. */
  .wfpage .fin { border:1px solid rgba(74,222,128,.35); background:rgba(74,222,128,.07);
                 border-radius:11px; padding:15px 16px;
                 transition:opacity .24s ease, transform .24s ease; }
  .wfpage .fin.enter { opacity:0; transform:translateY(26px); }
  .wfpage .fin .t { font-size:14.5px; font-weight:600; color:var(--wf-green); }
  .wfpage .fin .s { font-size:13px; color:var(--muted); margin:3px 0 12px; }
  /* Green is the colour this page uses for "written". A walkthrough that saved
     nothing gets the warning colour instead, so the panel cannot be mistaken
     for the scrum's at a glance. */
  .wfpage .fin.unwired { border-color:rgba(251,191,36,.35); background:rgba(251,191,36,.06); }
  .wfpage .fin.unwired .t { color:var(--amber); }

  /* ---- the scrum walk ---- */
  .wfpage .walk { display:flex; flex-direction:column; gap:11px; }
  .wfpage .walkbar { display:flex; align-items:center; justify-content:space-between;
                     gap:12px; flex-wrap:wrap;
                     font-family:var(--font-type); font-size:11px; color:var(--muted);
                     letter-spacing:.08em; }
  .wfpage .walkbar .clocks { display:flex; gap:16px; font-variant-numeric:tabular-nums; }
  .wfpage .walkbar b { color:var(--amber); font-weight:400; }

  .wfpage .tk { border:1px solid rgba(241,91,53,.45); border-radius:10px;
                background:var(--wf-surface2); padding:14px 15px;
                display:flex; flex-direction:column; gap:9px; }
  .wfpage .tk .top { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
  .wfpage .tk .ref { font-family:var(--font-type); font-size:12px;
                     color:var(--orange); letter-spacing:.06em; }
  .wfpage .tk .sum { font-size:14px; font-weight:600; flex:1; min-width:160px; }
  .wfpage .tk .det { display:flex; flex-direction:column; gap:6px;
                     font-size:12.5px; color:var(--muted); }
  .wfpage .tk .det div { display:flex; gap:9px; }
  .wfpage .tk .det .k { font-family:var(--font-type); font-size:10px; letter-spacing:.12em;
                        text-transform:uppercase; color:var(--wf-line2);
                        flex:none; width:62px; padding-top:2px; }

  .wfpage .queue { display:flex; flex-direction:column; gap:5px; }
  .wfpage .qrow { display:flex; align-items:center; gap:9px;
                  padding:6px 10px; border-radius:6px; font-size:12.5px;
                  color:var(--muted); border:1px solid transparent; }
  .wfpage .qrow.now { color:var(--wf-text); border-color:var(--wf-line);
                      background:rgba(241,91,53,.07); }
  .wfpage .qrow.past { opacity:.45; }
  .wfpage .qrow .r { font-family:var(--font-type); font-size:11px; flex:none; width:74px; }
  .wfpage .qrow .t { flex:1; min-width:0; overflow:hidden;
                     text-overflow:ellipsis; white-space:nowrap; }
  .wfpage .qrow .s { font-variant-numeric:tabular-nums; font-family:var(--font-type);
                     font-size:11px; flex:none; }
  .wfpage .qhead { font-family:var(--font-type); font-size:10px; letter-spacing:.16em;
                   text-transform:uppercase; color:var(--wf-line2); margin-top:4px; }

  .wfpage .empty { border:1px dashed var(--wf-line2); border-radius:11px;
                   padding:20px; color:var(--muted); font-size:13.5px; }
  .wfpage noscript .note { margin-top:18px; display:block; }

  @media (max-width:860px) { .wfpage .grid { grid-template-columns:repeat(2,1fr); } }
  @media (max-width:520px) {
    .wfpage .grid { grid-template-columns:1fr; }
    .wfpage .block { min-width:0; flex:1; }
  }
  /* `_APP_CSS` already carries a global `* { transition:none !important }` under
     the same query, so on the served page this block is belt and braces. It is
     here because the file has to be able to stand alone when it is lifted, and
     motion that only respects the preference by accident of a sibling
     stylesheet is motion that stops respecting it the moment it moves. */
  @media (prefers-reduced-motion: reduce) {
    .wfpage *, .wfpage *::before, .wfpage *::after {
      animation:none !important; transition:none !important;
    }
  }
"""
)


# --------------------------------------------------------------------------- #
# The engine
#
# Small and dependency-free on purpose. It knows four things: how to paint the
# rail's selection, how to push a step, how to collapse one, and how to run the
# scrum clock. Everything else is in the JSON the page hands it.
# --------------------------------------------------------------------------- #

_WORKFLOW_JS_SOURCE = """
(function () {
  "use strict";

  var DATA = window.INNODAY_WORKFLOWS;
  var vp = document.getElementById("wfvp");
  if (!DATA || !vp) { return; }

  var rail    = document.getElementById("wfrail"),
      chooser = document.getElementById("wfchooser"),
      grid    = document.getElementById("wfgrid"),
      runner  = document.getElementById("wfrunner"),
      stack   = document.getElementById("wfstack"),
      rPillar = document.getElementById("wfpillar"),
      rTitle  = document.getElementById("wftitle"),
      rDots   = document.getElementById("wfdots"),
      wferr   = document.getElementById("wferr"),
      hint    = document.getElementById("wfhint");

  // Raw text from the JSON is escaped *here*, at the point of interpolation.
  // Anything under `bodies` was escaped on the server and is assigned as HTML.
  function esc(s) {
    return String(s === null || s === undefined ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function mmss(s) {
    var m = Math.floor(s / 60), r = s % 60;
    return m + ":" + (r < 10 ? "0" : "") + r;
  }
  function rise(el) {
    // Two frames: one to let the browser record the offset start, one to
    // release it. A single frame lands both in the same style recalculation
    // and the element appears without moving.
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () { el.classList.remove("enter"); });
    });
  }

  var project = DATA.selected, run = null, teardown = null;

  function currentProject() { return DATA.projects[project] || null; }

  // Selection is context, never navigation. Changing project mid-run would
  // leave the steps on screen describing a project they were not built from,
  // so the rail is inert while a workflow is open -- the CSS says so too.
  function select(id) {
    if (run || !DATA.projects[id]) { return; }
    project = id;
    Array.prototype.forEach.call(rail.querySelectorAll(".block"), function (b) {
      b.classList.toggle("is-active", b.dataset.project === id);
      b.setAttribute("aria-pressed", b.dataset.project === id ? "true" : "false");
    });
    paintTicks();
  }

  // The two daily workflows carry a tick when today's answer is already in. It is
  // painted from the *selected project's* payload rather than rendered into the
  // button, because the rail switches project here with no round trip -- a
  // server-rendered tick would keep reporting whichever project the page loaded
  // with, which is worse than no tick: it would say a stand-up had run that had
  // not.
  //
  // The two titles are different sentences on purpose (see `_ticks`): one means
  // "you did this", the other "somebody did".
  function paintTicks() {
    var proj = currentProject();
    var ticks = (proj && proj.ticks) || {};
    Array.prototype.forEach.call(grid.querySelectorAll(".wf"), function (b) {
      var mark = b.querySelector("[data-tick]");
      if (!mark) { return; }
      var state = ticks[b.dataset.w];
      if (!state) { mark.hidden = true; b.removeAttribute("title"); return; }
      mark.hidden = !state.on;
      b.setAttribute("title", state.title || "");
    });
  }

  // The whole rail is inert while a workflow is open, the star and the arrow
  // included. They are a form and a link, so the CSS `pointer-events` rule
  // above cannot be the only guard: a focused link still follows on Enter, and
  // a submit button still submits. Leaving the page mid-walk abandons the scrum
  // -- `ended_at` never gets written -- and takes every typed comment with it.
  function railLocked(locked) {
    Array.prototype.forEach.call(rail.querySelectorAll(".star"), function (b) {
      b.disabled = locked;
    });
    Array.prototype.forEach.call(rail.querySelectorAll(".out"), function (a) {
      if (locked) {
        a.setAttribute("tabindex", "-1");
        a.setAttribute("aria-disabled", "true");
      } else {
        a.removeAttribute("tabindex");
        a.removeAttribute("aria-disabled");
      }
    });
  }

  rail.addEventListener("click", function (e) {
    if (run) { e.preventDefault(); return; }
    if (e.target.closest(".star") || e.target.closest(".out")) { return; }
    var b = e.target.closest(".block");
    if (b) { select(b.dataset.project); }
  });
  rail.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") { return; }
    if (run) { e.preventDefault(); return; }
    var b = e.target.closest(".block");
    if (!b || e.target.closest(".star") || e.target.closest(".out")) { return; }
    e.preventDefault();
    select(b.dataset.project);
  });

  // The star's own optimism. `_COPY_JS` has this behaviour already but bails
  // when the star is not inside a `.dropdown`, which is the org switcher's
  // shape and not the rail's. The form still submits and the server still
  // decides; this only moves the highlight before the round trip, because a
  // control that waits on a reload to acknowledge a click reads as broken.
  rail.addEventListener("click", function (e) {
    if (run) { return; }
    var star = e.target.closest(".star");
    if (!star) { return; }
    Array.prototype.forEach.call(rail.querySelectorAll(".star.is-default"), function (other) {
      other.classList.remove("is-default");
      other.innerHTML = "\\u2606";
    });
    star.classList.add("is-default");
    star.innerHTML = "\\u2605";
    var block = star.closest(".block");
    if (block && hint) {
      hint.textContent = (block.dataset.alias || "This project") + " now opens by default";
    }
  });

  grid.addEventListener("click", function (e) {
    var b = e.target.closest(".wf");
    if (b) { begin(b.dataset.w); }
  });

  function steps(id) {
    var wf = DATA.workflows.filter(function (w) { return w.id === id; })[0];
    return wf ? wf.steps : [];
  }

  function bodyFor(id, i, step) {
    var proj = currentProject();
    var key = id + "." + i;
    if (proj && proj.bodies && proj.bodies[key] !== undefined) { return proj.bodies[key]; }
    return step.body || "";
  }

  function ctaFor(id, i, step) {
    var proj = currentProject();
    var key = id + "." + i;
    if (proj && proj.ctas && proj.ctas[key] !== undefined) { return proj.ctas[key]; }
    return step.cta;
  }

  /* =================================================================
     Recording the scrum.

     The walk is a meeting being minuted, so the writes happen *while it
     happens*: the row is opened as the walk step appears, one visit is
     posted as each stop ends, and the wrap-up closes it. Nothing is
     collected and sent at the finish -- a run that is interrupted half
     way through is the ordinary case, and batching would mean exactly
     those runs left no trace.

     These are `/ui` routes, reached by a same-origin `fetch` carrying
     the session cookie. They are not `/api/v1`: a browser cannot send
     `X-Team-Secret`, and putting the shared secret in this script would
     leak it to every viewer.

     Nothing here ever reports success it did not get, and nothing
     reports a failure it did not get: a failed write paints `#wferr`
     and holds the wrap-up where it is, while a 409 ("already closed")
     is the outcome the wrap-up was asking for and completes the walk.

     A failure that is temporary is treated as temporary. The open is
     retried by the next write rather than latched, so a blip mid-walk
     costs the stops it actually covered and not the meeting. Only a
     browser that cannot write at all is permanent -- and that case
     still finishes the walk, saying plainly that nothing was saved.
     ================================================================= */

  var rec = null;

  //: Which control on the wrap-up step each refusable field belongs to. The
  //: server names the field it refused; this is what turns that name into the
  //: box the message has to appear beside.
  var FIELD_HOOKS = {
    transcript_url: "[data-scrum-transcript]",
    notes_markdown: "[data-scrum-notes]"
  };

  function fail(message) {
    if (!wferr) { return; }
    // One string or several. Several, because a submit can fail in more than
    // one way at once -- a move the board refused *and* a comment it would not
    // take -- and showing only the first meant the second was never told to
    // anybody. `textContent` still, so board-supplied text can never become
    // markup on a page that sends no CSP; the newlines are made to render by
    // `white-space: pre-line` on `.wferr` rather than by building elements.
    var lines = Array.isArray(message) ? message.filter(Boolean) : [message];
    if (!lines.length) { return; }
    wferr.textContent = lines.join("\\n");
    wferr.hidden = false;
  }
  function clearFail() {
    if (!wferr) { return; }
    wferr.textContent = "";
    wferr.hidden = true;
  }

  // A refusal that names a field is shown *at* that field. Returns whether it
  // found one, so the caller can fall back to the banner rather than silently
  // showing nothing.
  function fieldError(field, message) {
    var sel = FIELD_HOOKS[field];
    if (!sel || !message) { return false; }
    var el = stack.querySelector(sel);
    if (!el || !el.parentNode) { return false; }
    var slot = el.parentNode.querySelector(".ferr");
    if (!slot) {
      slot = document.createElement("em");
      slot.className = "ferr";
      el.parentNode.appendChild(slot);
    }
    slot.textContent = message;
    el.classList.add("bad");
    el.focus();
    return true;
  }

  function clearFieldErrors() {
    Array.prototype.forEach.call(stack.querySelectorAll(".ferr"), function (slot) {
      slot.parentNode.removeChild(slot);
    });
    Array.prototype.forEach.call(stack.querySelectorAll(".bad"), function (el) {
      el.classList.remove("bad");
    });
  }

  function post(url, body) {
    return window.fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body || {})
    }).then(function (r) {
      // A 4xx is a refusal, not a payload. Treating `!r.ok` as an error is
      // what keeps "saved" from being printed over a 403.
      if (r.ok) { return r.json(); }
      // The refusal's own words are carried, not discarded. A 422 says which
      // value it rejected and why; replacing that with "HTTP 422" leaves the
      // user a generic "try again" about a field only they can fix, and the
      // meeting's record never gets written.
      return r.json().then(function (b) { return b; }, function () { return {}; })
        .then(function (b) {
          var e = new Error((b && b.error) ? b.error : ("HTTP " + r.status));
          e.status = r.status;
          e.field = (b && b.field) || "";
          throw e;
        });
    });
  }

  // `kind` comes from the workflow spec (`_saves(records=…)`), never from the
  // engine recognising a workflow by name: it is what decides which row the writes
  // land on, so a record cannot turn out to be the wrong one, and a third
  // recording workflow needs no change here.
  // What the *record* is, in the words of whichever workflow is open. "This walk"
  // was hard-coded, which is right for a stand-up and wrong for a daily form --
  // and a message that describes the wrong thing reads as a message about
  // somebody else's problem.
  function recordNoun() {
    return run && run.wf.records === "update" ? "Your update" : "This walk";
  }

  function openRecord(kind) {
    rec = { url: DATA.scrumsUrl || "", kind: kind, id: null, lost: 0,
            chain: null, opening: null,
            supported: !!(DATA.scrumsUrl && window.fetch && window.Promise) };
    if (!rec.supported) {
      // Nothing can be written from this browser, and nothing will change that
      // while the workflow is open -- unlike a failed open, which is temporary.
      fail(recordNoun() + " is not being recorded \\u2014 nothing from it will "
           + "be saved.");
      return;
    }
    ensureOpen();
  }

  // The open is retried, never latched. A five-second blip while the walk step
  // renders used to mark the record permanently broken: every later stop was
  // skipped without even attempting a request and the wrap-up refused outright,
  // so connectivity that returned immediately still cost the whole meeting and
  // the only way out was a reload that discarded every typed comment. Each
  // write asks for the record it needs, and the ask re-attempts the open.
  function ensureOpen() {
    if (!rec || !rec.supported) {
      return window.Promise.reject(new Error("not recorded"));
    }
    if (rec.id) { return window.Promise.resolve(rec.id); }
    if (!rec.opening) {
      rec.opening = post(rec.url, { project_id: project, kind: rec.kind })
        .then(function (r) {
        rec.id = r.scrum_id;
        // Only if nothing has actually been lost -- a recovered open must not
        // erase "3 tickets were not saved", which is still true.
        if (!rec.lost) { clearFail(); }
        return rec.id;
      }, function (e) {
        // Cleared, so the next write attempts a fresh open rather than
        // chaining onto the rejection this one already settled with.
        rec.opening = null;
        // Marked so the write wrapper can tell whose 409 this was. **No refusal
        // on the open maps to 409 today** -- `open_scrum` answers 404, 422 or 403
        // -- so this is a guard, not a fix, and it is worth the one line because
        // of what it guards against and how quietly that would fail.
        //
        // `ensureOpen` is chained *inside* `closeRecord` and `submitPicks`, so an
        // open's rejection arrives at the same handler a close's does. That
        // handler treats 409 as "the thing this button asked for has already
        // happened" and completes the step. Any future rule that refuses an open
        // with 409 -- a per-day cap, a locked project, a record somebody else
        // finalised -- would therefore be reported to the user as a **successful
        // save** of a record that was never written, with nothing on screen to
        // notice. The trap is in the shape of the chain rather than in this
        // change, which is why the flag stays regardless of what the open
        // currently returns.
        e.fromOpen = true;
        throw e;
      });
    }
    return rec.opening;
  }

  // One request per stop, queued behind the one that opened the record --
  // a visit needs the scrum's id, and the id arrives asynchronously. A stop
  // that fails is counted and named, and the walk carries on: losing one
  // ticket is the failure this shape was chosen to have.
  function recordStop(t, position, seconds, comment) {
    if (!rec || !rec.supported || !t) { return; }
    rec.chain = (rec.chain || window.Promise.resolve()).then(function () {
      return ensureOpen();
    }).then(function () {
      return post(rec.url + "/" + encodeURIComponent(rec.id) + "/visits", {
        ticket_id: t.id,
        position: position,
        seconds: seconds,
        status_at_visit: t.st,
        comment: comment || null
      });
    }).then(null, function () {
      rec.lost++;
      fail(rec.lost + (rec.lost === 1 ? " ticket was" : " tickets were")
           + " not saved to the scrum record. The rest of the walk still is.");
      // Swallowed deliberately: the chain has to survive so the next stop --
      // and the wrap-up -- still try.
    });
  }

  // Null means "this browser cannot write at all", which is a different answer
  // from a rejected promise: the caller finishes the walk rather than trapping
  // the user on a step they can never leave.
  function closeRecord(seconds) {
    if (!window.Promise || !rec || !rec.supported) { return null; }
    var notes = stack.querySelector("[data-scrum-notes]"),
        link  = stack.querySelector("[data-scrum-transcript]"),
        proj  = currentProject();
    var body = {
      ended_at: new Date().toISOString(),
      notes_markdown: (notes && notes.value) ? notes.value : null
    };
    // A walk has a clock and a board it went round; a daily form has neither, so
    // the three columns that measure a meeting are **not sent** and stay NULL
    // rather than being sent as zero. Zero is a measurement -- "the meeting took
    // no time and nothing was lingering" -- and `domain.scrum` records that
    // anything aggregating them must filter on `kind`, which only works if the
    // rows that never had one hold NULL.
    if (rec.kind !== "update") {
      body.total_seconds = seconds === null ? null : seconds;
      body.transcript_url = link ? link.value : "";
      body.lingering_count = proj ? (proj.lingering || 0) : 0;
    }
    return (rec.chain || window.Promise.resolve()).then(function () {
      return ensureOpen();
    }).then(function () {
      return post(rec.url + "/" + encodeURIComponent(rec.id) + "/finish", body);
    }).then(function (r) {
      // **A saved record that did not fully land is still a saved record.** The
      // close succeeded -- the row is written and the moves are applied -- so
      // this is not a rejection and the step advances. What it is is something
      // the page was told and must not drop: a move the board refused, or an
      // assignment the board could not attribute. Parked here and painted by
      // `saved()`, which is the one place that decides what the banner says
      // after a successful write.
      // Everything the server said went wrong, from both halves of the write.
      // `comment_errors` used to be returned and never read at all: a comment
      // the board refused was recorded server-side and produced no banner, so
      // the page said the update was done and the person believed their message
      // had reached the ticket.
      rec.warn = [].concat(
        (r && r.errors) || [],
        (r && r.comment_errors) || [],
        (r && r.notices) || [],
        (r && r.comment_notices) || []
      ).filter(Boolean);
      return r;
    });
  }

  /* -----------------------------------------------------------------
     A picker step: send the **whole selection**, so the record ends up
     holding exactly what is ticked.

     **Not one request per pick.** A per-ticket write can say "add this"
     and cannot say "and nothing else", so it cannot express somebody
     un-ticking a box -- the withdrawn pick simply stayed in the record
     while step 2 said the record was theirs to correct. One request
     carrying the complete set is what makes removal expressible at all,
     and it makes the write idempotent: a retry after a partial failure
     converges instead of doubling what already landed.

     **Read from `stack`, not from this step.** A collapsed step stays in
     the DOM, so by the second picker this finds both steps' boxes -- which
     is what "the whole selection" has to mean when the selection is spread
     over two steps.

     **But it is a superset of the last post only within one run.** On a
     *resumed* record the picks already exist server-side while step 1 has
     not been rendered yet, so the post made on leaving step 0 is a strict
     subset. That is what `offered` below is for: the post says which boxes
     it could see as well as which are ticked, and the server leaves the
     rest alone instead of reading the gap as a withdrawal.

     **Nothing moves until the last step.** The visit records the ask;
     *submitting* applies it and pushes it to the board. Both halves are in
     the step copy, because a picker that claimed either one alone would be
     wrong -- one invites somebody to tick boxes believing they can think
     about it afterwards, the other says the tickets have already moved.

     Zero selections is a legal answer and the common one -- "nothing to
     bring back" is most days. It is still **posted**, because on a resumed
     record an empty selection is a real change: it means "remove what I
     recorded earlier", and posting nothing would silently keep it.
     ----------------------------------------------------------------- */
  function submitPicks() {
    if (!window.Promise || !rec || !rec.supported) { return null; }
    var proj = currentProject();
    var meta = (proj && proj.update) || {};
    var rows = meta.rows || {};
    // What was typed beside each ticket, read from the whole `stack` for the same
    // reason the boxes are: a collapsed step stays in the DOM, so by the second
    // picker this has to see both steps' notes.
    var notes = {};
    Array.prototype.forEach.call(
      stack.querySelectorAll("[data-pick-note]"),
      function (box) { notes[box.getAttribute("data-pick-note")] = box.value || ""; }
    );
    // A note beside a ticket nobody ticked has nowhere to go -- there is no visit
    // to hold it -- so it is dropped. **Said at submit time, not only in the
    // static copy under the list.** A paragraph somebody typed and then watched
    // vanish with no acknowledgement is the page telling them nothing happened
    // when something did, which is the same rule this surface holds everywhere
    // else, just quieter.
    var dropped = 0;
    Array.prototype.forEach.call(
      stack.querySelectorAll("[data-pick-note]"),
      function (box) {
        var id = box.getAttribute("data-pick-note");
        var tick = stack.querySelector('[data-pick="' + id + '"]');
        if ((box.value || "").replace(/^\\s+|\\s+$/g, "") && tick && !tick.checked) {
          dropped++;
        }
      }
    );
    var picks = Array.prototype.map.call(
      stack.querySelectorAll("[data-pick]:checked"),
      function (box) {
        var id = box.getAttribute("data-pick");
        return {
          ticket_id: parseInt(id, 10),
          // The status the ticket is at *now*, which the server stores as a
          // historical observation. Absent from the payload it is refused with a
          // 422 naming the field rather than stored as a guess.
          status_at_visit: rows[id] || "",
          moved_to: meta.moveTo || "",
          // **Always present, even empty.** The server keys the write on the
          // key being *sent*, not on it being truthy, because an emptied box is
          // a deletion -- somebody removing what they wrote. Omitting it when
          // blank would make "I deleted that" indistinguishable from "I never
          // mentioned comments", and the stored sentence would survive a
          // deliberate removal while the page showed it gone.
          comment: notes[id] || ""
        };
      }
    );
    // Every box on screen, ticked or not -- the *scope* this post speaks for.
    // Steps render one at a time and stay in the DOM, so on a resumed record the
    // post made when step 0 is left can only see step 0's boxes. Sending just
    // the ticked ones let the server read "and nothing else" over the whole
    // record and delete the take-picks it had; restored a moment later when step
    // 1 was left, but not if the tab was abandoned in between. Saying what was
    // visible keeps un-ticking expressible (a withdrawn box is here and not in
    // `picks`) while leaving alone what was never asked about.
    var offered = Array.prototype.map.call(
      stack.querySelectorAll("[data-pick]"),
      function (box) { return parseInt(box.getAttribute("data-pick"), 10); }
    );
    var chain = ensureOpen().then(function () {
      return post(rec.url + "/" + encodeURIComponent(rec.id) + "/picks",
                  { picks: picks, offered: offered });
    }).then(function (r) {
      // Painted from what the server says it stored, not from what was sent.
      publishPicked(r && typeof r.recorded === "number" ? r.recorded : picks.length);
      // Assigned every time, not only when something dropped -- and as an
      // array, like everything else that reaches the banner. Set-only, it went
      // stale: a warning raised on the first picker was still parked on the
      // record when the second picker painted, so the page reported notes
      // dropped by a step the reader had already left.
      rec.warn = dropped
        ? [dropped + (dropped === 1 ? " note was" : " notes were")
           + " not kept \u2014 a comment only goes with a ticket you have"
           + " ticked."]
        : [];
      return r;
    });
    // Parked on the record so the closing write waits for this, exactly as it
    // waits for the walk's stops.
    rec.chain = chain;
    return chain;
  }

  function begin(id) {
    var wf = DATA.workflows.filter(function (w) { return w.id === id; })[0];
    if (!wf || !currentProject()) { return; }
    rec = null;
    clearFail();
    run = { wf: wf, at: 0 };
    vp.classList.add("focused");
    chooser.classList.add("is-out");
    runner.classList.add("is-live");
    rPillar.textContent = wf.pillar;
    rTitle.textContent = wf.title + " \\u00b7 " + (currentProject().alias || "");
    stack.innerHTML = "";
    railLocked(true);
    paintDots();
    pushStep(0);
  }

  function paintDots() {
    if (!run) { rDots.innerHTML = ""; return; }
    rDots.innerHTML = run.wf.steps.map(function (_, i) {
      return "<i class='" + (i < run.at ? "past" : (i === run.at ? "on" : "")) + "'></i>";
    }).join("");
    rDots.setAttribute(
      "aria-label",
      "Step " + Math.min(run.at + 1, run.wf.steps.length) + " of " + run.wf.steps.length
    );
  }

  /* =================================================================
     A step that writes.

     Two shapes today: a picker posts the choices it collected, and the
     last step of a recording workflow closes the record. Both need the
     *same* handling -- disable the button, post, paint the failure and
     stay where you are, collapse only on the answer you asked for -- and
     that handling was already written once, hard-gated on
     `run.wf.id === "run-scrum"`.

     Generalised rather than copied. Two copies of "is a 409 a failure?"
     is precisely how the two paths come to disagree about it, and this
     page's one hard rule is that it never reports a save it did not get
     and never reports a failure it did not get either.

     Named on the step's own shape (`custom`) and on the workflow's
     `saves`/`records` data -- never on a workflow's id. The moment the
     engine knows one by name, the next one has to be added to it too.
     ================================================================= */

  // What this workflow calls the thing it is saving, for the failure messages.
  // `run-scrum`'s wording is its own on purpose: "the scrum was not saved" is
  // what somebody reads when a stand-up they just walked fails to record, and
  // generalising it to "the record" to serve two callers made the specific case
  // vaguer for no gain.
  function nounFor() {
    return run.wf.records === "update" ? "Your update" : "The scrum";
  }

  function writerFor(step, i, el) {
    var last = i === run.wf.steps.length - 1;
    var picker = step.custom === "picks";
    var closes = !!run.wf.saves && last;
    if (!picker && !closes) { return null; }

    // **Both, when a picker *is* the last step**, and in that order. Nothing
    // reaches that combination today -- `give-scrum-update` ends on a plain step
    // and `run-scrum` has no picker -- but the whole point of keying on the
    // step's shape instead of on `run.wf.id` is that the next recording workflow
    // needs no change here, and a picker-as-last-step is exactly the shape this
    // would otherwise mis-handle: it would post the picks and never close the
    // record, leaving `ended_at` NULL (which `domain.scrum` spells "somebody
    // walked out of this") and the daily tick permanently off.
    return {
      noun: closes ? nounFor() : "Your picks",
      // The tick beside this workflow in the picker, turned on from a save we
      // actually got rather than from the payload -- which was rendered before
      // any of this happened and would otherwise keep saying "not yet" until a
      // reload.
      marks: closes ? run.wf.id : "",
      run: function () {
        if (!picker) { return closeRecord(totalSeconds); }
        var picking = submitPicks(el);
        if (!closes) { return picking; }
        // `submitPicks` returns null only when this browser cannot write at all,
        // in which case `closeRecord` returns null too and the caller says so.
        if (!picking) { return null; }
        return picking.then(function () { return closeRecord(totalSeconds); });
      }
    };
  }

  function wireWrite(el, i, btn, writer) {
    btn.addEventListener("click", function () {
      if (btn.disabled) { return; }
      var label = btn.textContent;
      clearFieldErrors();
      btn.disabled = true;
      btn.textContent = "Saving\\u2026";

      function saved() {
        clearFail();
        var told = [];
        if (rec && rec.lost) {
          told.push(rec.lost + (rec.lost === 1 ? " ticket" : " tickets")
                    + " could not be saved, but " + writer.noun.toLowerCase()
                    + " itself was recorded.");
        }
        if (rec && rec.warn && rec.warn.length) {
          // Added to, never instead of. A lost stop still leads -- part of the
          // record is missing, which outranks a write the board refused -- but
          // it no longer *replaces* the rest. The banner used to hold one line,
          // so whichever of these came first was the only one anybody saw.
          told = told.concat(rec.warn);
        }
        if (told.length) { fail(told); }
        var proj = currentProject();
        if (writer.marks && proj && proj.ticks && proj.ticks[writer.marks]) {
          proj.ticks[writer.marks].on = true;
        }
        advance(el, i);
      }

      var writing = writer.run();
      if (!writing) {
        // This browser cannot write at all -- no `fetch`, no `Promise`, or no
        // write URL. The workflow still has to *finish*: refusing to advance
        // turns a page that saves nothing into a page that cannot be completed,
        // which is worse. Say plainly that nothing was recorded and move on.
        fail(recordNoun() + " was not recorded \\u2014 nothing from it has "
             + "been saved.");
        advance(el, i);
        return;
      }

      writing.then(saved, function (err) {
        // 409 is "the thing this button was asking for has already happened":
        // the record is closed. It arrives when the response to a write that
        // *did* commit was dropped in transit, and painting a failure over it is
        // the same lie as reporting a save that never happened, in the other
        // direction.
        //
        // **Scoped to the write, not to the whole chain.** `ensureOpen` runs
        // inside that chain, so an open's rejection lands here too -- and a 409
        // from an open means nothing this click asked for happened. Nothing
        // returns one today; see `ensureOpen` for why the guard is still here.
        if (err && err.status === 409 && !err.fromOpen) { saved(); return; }
        btn.disabled = false;
        btn.textContent = label;
        var message = (err && err.message) ? err.message : "";
        if (err && err.field && fieldError(err.field, message)) {
          fail(writer.noun + " has not been saved yet \\u2014 fix the value "
               + "marked below and press the button again.");
          return;
        }
        fail(message
          ? writer.noun + " was not saved: " + message
          : writer.noun + " was not saved. Nothing has been recorded for this "
            + "step \\u2014 try again.");
      });
    });
  }

  function pushStep(i) {
    var s = run.wf.steps[i];
    var el = document.createElement("div");
    // `unwired` when the workflow writes nothing, which is eight of the ten.
    // It is what turns the collapsed receipt from a green tick into "not saved".
    el.className = "step enter" + (run.wf.saves ? "" : " unwired");
    el.innerHTML =
        '<div class="shead"><span class="idx">Step ' + (i + 1) + "</span>"
      +   '<span class="wstitle">' + esc(s.title) + "</span></div>"
      + '<p class="guide">' + esc(s.guide) + "</p>"
      + '<div class="wbody">' + (s.custom === "walk" ? walkMarkup() : bodyFor(run.wf.id, i, s))
      // Raw text from the JSON, so it is escaped here like every other value --
      // it is not a `bodies` entry and must not become one. It sits inside
      // `.wbody`, directly above the button, so the sentence that says nothing
      // is saved is the last thing read before the button that saves nothing.
      +   (run.wf.warn ? '<div class="note warn">' + esc(run.wf.warn) + "</div>" : "")
      + "</div>"
      + '<div class="act"><button class="go' + (s.danger ? " danger" : "") + '" type="button">'
      +   esc(ctaFor(run.wf.id, i, s)) + "</button></div>";

    stack.appendChild(el);
    rise(el);

    // The record opens as the **first step that writes** appears -- the walk for
    // a scrum, the first picker for an update -- and not at the wrap-up. A run
    // interrupted half way through is the ordinary case and the record of *that*
    // run is the one worth having. Keyed on the step's own shape, so no workflow
    // is named here.
    if (!rec && run.wf.records && (s.custom === "walk" || s.custom === "picks")) {
      openRecord(run.wf.records);
    }

    if (s.custom === "walk") {
      teardown = wireWalk(el);
      var go = el.querySelector(".go");
      go.textContent = "Next ticket \\u23ce";
      go.addEventListener("click", function () {
        var state = el.__walkState();
        if (!state.pulling) { el.__walkNext(); return; }
        if (teardown) { teardown(); teardown = null; }
        publishTotal(state.total);
        advance(el, i);
      });
      return;
    }

    var btn = el.querySelector(".go");
    var writer = writerFor(s, i, el);
    if (writer) { wireWrite(el, i, btn, writer); }
    else { btn.addEventListener("click", function () { advance(el, i); }); }

    var focusable = el.querySelector("input, textarea");
    if (focusable) { focusable.focus(); }
  }

  // The wrap-up step is server-rendered like any other; the one number it
  // cannot know is how long the meeting took, so the walk posts it into the
  // slot the server left for it.
  var totalSeconds = null;
  function publishTotal(seconds) {
    totalSeconds = seconds;
    paintTotals();
  }
  function paintTotals() {
    if (totalSeconds === null) { return; }
    Array.prototype.forEach.call(stack.querySelectorAll("[data-wf-total]"), function (slot) {
      slot.textContent = mmss(totalSeconds);
    });
  }

  // The same mechanism for the update's "Recorded so far", and for the same
  // reason the clock has one: the number changes *during* the run, so the server
  // cannot render it. It was rendered anyway, from what the record held when the
  // page was served -- so a fresh run read "0 tickets" immediately after
  // recording five, and a resumed one kept reading its old count no matter what
  // was ticked next. Understating is less dangerous than overstating, but
  // "Recorded so far" is a claim about state and the page is in a position to get
  // it right.
  //
  // `null` means nothing has been recorded *this run*, in which case the
  // server-rendered value is the best answer available and is left alone.
  var pickedCount = null;
  function publishPicked(count) {
    pickedCount = count;
    paintPicked();
  }
  function paintPicked() {
    if (pickedCount === null) { return; }
    var label = pickedCount + (pickedCount === 1 ? " ticket" : " tickets");
    Array.prototype.forEach.call(stack.querySelectorAll("[data-wf-picked]"), function (slot) {
      slot.textContent = label;
    });
  }

  function advance(el, i) {
    el.classList.add("wdone");
    run.at = i + 1;
    paintDots();
    // 130ms, so the collapse has visibly started before the next step begins
    // rising into the space it just gave up.
    if (run.at < run.wf.steps.length) {
      // Both repaints run *after* the next step exists, because the slot they
      // fill is in markup that has only just been appended.
      window.setTimeout(function () {
        pushStep(run.at);
        paintTotals();
        paintPicked();
      }, 130);
    } else {
      window.setTimeout(finish, 130);
    }
  }

  // The completion panel says what actually happened, and the sentence comes
  // from the workflow rather than from here: a walk that wrote nothing may not
  // print the receipt of one that did. Only the two words of the heading are
  // structural -- "done" is a claim, so an unwired run does not get to make it.
  function finish() {
    var el = document.createElement("div");
    var saved = !!run.wf.saves;
    el.className = "fin enter" + (saved ? "" : " unwired");
    el.innerHTML = '<div class="t">' + esc(run.wf.title)
                 +   (saved ? " \\u2014 done" : " \\u2014 walkthrough complete") + "</div>"
                 + '<div class="s">' + esc(run.wf.done) + "</div>"
                 + '<button class="go" type="button">Finish</button>';
    stack.appendChild(el);
    rise(el);
    el.querySelector(".go").addEventListener("click", reset);
    el.querySelector(".go").focus();
  }

  function reset() {
    if (teardown) { teardown(); teardown = null; }
    run = null;
    rec = null;
    clearFail();
    totalSeconds = null;
    pickedCount = null;
    runner.classList.remove("is-live");
    chooser.classList.remove("is-out");
    vp.classList.remove("focused");
    stack.innerHTML = "";
    railLocked(false);
    paintDots();
    // A run that recorded something turned its own tick on; repaint so the
    // picker shows it without a reload.
    paintTicks();
  }

  document.getElementById("wfquit").addEventListener("click", reset);
  // The first paint. `select` handles every later one.
  paintTicks();

  /* =================================================================
     The scrum walk -- the one step that is a loop rather than a form.
     ================================================================= */

  function walkMarkup() {
    return '<div class="walk" data-walk>'
         +   '<div class="walkbar">'
         +     '<span data-phase></span>'
         +     '<span class="clocks"><span>ticket <b data-tclock>0:00</b></span>'
         +       "<span>scrum <b data-sclock>0:00</b></span></span>"
         +   "</div>"
         +   "<div data-card></div>"
         +   '<div class="field" data-commentwrap><label>Comment</label>'
         +     '<input data-comment placeholder="Optional \\u2014 Enter moves to the next ticket" /></div>'
         +   '<div class="queue" data-queue></div>'
         + "</div>";
  }

  function cardMarkup(t) {
    return '<div class="tk">'
         +   '<div class="top"><span class="ref">' + esc(t.ref) + "</span>"
         +     '<span class="sum">' + esc(t.sum) + "</span>"
         +     '<span class="wchip ' + (t.st === "in review" ? "v" : "") + '">' + esc(t.lbl) + "</span>"
         +     (t.days >= DATA.lingerDays ? '<span class="wchip a">' + esc(t.days) + "d</span>" : "")
         +   "</div>"
         +   '<div class="det">'
         +     (t.note ? '<div><span class="k">Summary</span><span>' + esc(t.note) + "</span></div>" : "")
         +     (t.owner ? '<div><span class="k">Owner</span><span>' + esc(t.owner) + "</span></div>" : "")
         +   "</div>"
         + "</div>";
  }

  // Timers and Enter-to-advance for one freshly-rendered walk. Returns its own
  // teardown: the interval outlives the element otherwise, and a cancelled
  // scrum that goes on counting is a clock lying about a meeting that ended.
  function wireWalk(root) {
    var proj    = currentProject();
    var walk    = (proj && proj.walk) || [];
    var el      = root.querySelector("[data-walk]");
    var phaseEl = el.querySelector("[data-phase]");
    var tEl     = el.querySelector("[data-tclock]");
    var sEl     = el.querySelector("[data-sclock]");
    var cardEl  = el.querySelector("[data-card]");
    var queueEl = el.querySelector("[data-queue]");
    var input   = el.querySelector("[data-comment]");

    var i = 0, tSec = 0, sSec = 0, spent = [], pulling = walk.length === 0;

    function paintQueue() {
      if (pulling) { queueEl.innerHTML = (proj && proj.pull) || ""; return; }
      queueEl.innerHTML = walk.map(function (t, n) {
        var cls = n === i ? "now" : (n < i ? "past" : "");
        return '<div class="qrow ' + cls + '">'
             +   '<span class="r">' + esc(t.ref) + "</span>"
             +   '<span class="t">' + esc(t.sum) + "</span>"
             +   '<span class="s">'
             +     (n < i ? mmss(spent[n] || 0) : (n === i ? mmss(tSec) : "\\u2014"))
             +   "</span>"
             + "</div>";
      }).join("");
    }

    function paintCard() {
      if (pulling) {
        cardEl.innerHTML = '<div class="note">'
          + (walk.length
              ? "Walk complete \\u2014 <b>" + mmss(sSec) + "</b> across " + walk.length
                + " ticket" + (walk.length === 1 ? "" : "s") + ". "
              : "Nothing is in test or in progress on this board. ")
          + "Pull anything else in before wrapping up.</div>";
        phaseEl.textContent = "Adjusting the board";
        el.querySelector("[data-commentwrap]").style.display = "none";
      } else {
        var t = walk[i];
        cardEl.innerHTML = cardMarkup(t);
        var group = walk.filter(function (x) { return x.st === t.st; });
        var idx = group.indexOf(t) + 1;
        phaseEl.textContent = t.lbl + " \\u00b7 " + idx + " of " + group.length;
      }
      paintQueue();
    }

    var tick = window.setInterval(function () {
      if (pulling) { sSec++; sEl.textContent = mmss(sSec); return; }
      tSec++; sSec++;
      tEl.textContent = mmss(tSec);
      sEl.textContent = mmss(sSec);
      paintQueue();
    }, 1000);

    function next() {
      if (pulling) { return; }
      spent[i] = tSec;
      // Written as the stop ends, with the comment that was typed for it --
      // not queued for the finish.
      recordStop(walk[i], i, tSec, input.value);
      tSec = 0;
      tEl.textContent = "0:00";
      input.value = "";
      i++;
      if (i >= walk.length) { pulling = true; }
      paintCard();
    }

    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); next(); }
    });

    root.__walkNext = next;
    root.__walkState = function () {
      return { total: sSec, spent: spent, pulling: pulling, at: i };
    };
    paintCard();

    return function () { window.clearInterval(tick); };
  }
})();
"""


#: What is actually served. The sources above keep their comments; the browser
#: gets neither them nor the chance to satisfy a substring assertion that meant
#: to check behaviour -- see `strip_authoring_comments`.
_WORKFLOW_CSS = strip_authoring_comments(_WORKFLOW_CSS_SOURCE)
_WORKFLOW_JS = strip_authoring_comments(_WORKFLOW_JS_SOURCE)


# --------------------------------------------------------------------------- #
# Small markup helpers
# --------------------------------------------------------------------------- #


def _chip(text: str, kind: str = "") -> str:
    """One status chip. ``kind`` is "", g, v, a or n -- see the CSS."""
    suffix = f" {kind}" if kind else ""
    return f'<span class="wchip{suffix}">{esc(text)}</span>'


def _row(
    left: str,
    right: str = "",
    *,
    check: Optional[bool] = None,
    ticket_id: Optional[int] = None,
) -> str:
    """One line in a step: something on the left, a chip or count on the right.

    ``check`` adds a checkbox. It is ``None`` for a row that only reports, and
    a bool for a row that is a choice -- an unticked box beside a fact reads as
    an action the page will not in fact take.

    ``ticket_id`` makes the box **readable from the script**: it emits
    ``data-pick="<int>"``, which is what the update workflow's collect-and-post
    handler selects on. Until it existed the checkbox had no ``name``, no
    ``value`` and no hook, so nothing client-side could tell which rows had been
    ticked -- the boxes were decoration.

    **Optional, and the other eight callers' markup is byte-identical without
    it.** A helper that grows an attribute for one caller and emits it for all of
    them changes markup nine steps rely on, and nothing on the page would say so
    (`test_the_other_eight_pickers_keep_their_markup_byte_identical`).

    The ``hook`` convention on `_text_input`/`_textarea` is "a bare ``data-``
    attribute name, never interpolated content". Here and in `_pick_comment` a
    *value* joins one, so it is not escaped -- it is coerced. ``int()`` either
    produces an integer or raises, and an integer formatted into an attribute
    cannot carry a quote, an angle bracket or anything else that matters.
    Escaping a value that is already provably safe would read as though a string
    could arrive here.
    """
    box = ""
    if check is not None:
        pick = f' data-pick="{int(ticket_id)}"' if ticket_id is not None else ""
        box = f'<input type="checkbox"{" checked" if check else ""}{pick} />'
    return f'<div class="wrow">{box}<span class="wgrow">{left}</span>{right}</div>'


def _note(text: str, *, warn: bool = False) -> str:
    """An aside under a step's controls. ``text`` is markup this module built."""
    return f'<div class="note{" warn" if warn else ""}">{text}</div>'


def _field(label: str, control: str) -> str:
    return f'<div class="field"><label>{esc(label)}</label>{control}</div>'


#: ``hook`` on the two helpers below is a bare ``data-`` attribute name, never
#: interpolated content -- the script finds a control by it (``[data-scrum-notes]``)
#: after the step that owns it has already collapsed. It is written verbatim
#: rather than through ``esc`` because only this module supplies it; a value from
#: anywhere else belongs in ``value``/``placeholder``, which are escaped.
def _text_input(
    *, placeholder: str = "", value: str = "", style: str = "", hook: str = ""
) -> str:
    attrs = f' placeholder="{esc(placeholder)}"' if placeholder else ""
    attrs += f' value="{esc(value)}"' if value else ""
    attrs += f' style="{esc(style)}"' if style else ""
    attrs += f" {hook}" if hook else ""
    return f"<input{attrs} />"


def _textarea(placeholder: str = "", *, hook: str = "", value: str = "") -> str:
    """A multi-line box, with ``value`` as its **text node** rather than an attribute.

    That distinction is the reason this takes a value at all. `_text_input` puts
    its value in ``value="…"``, where a newline is not representable -- a resumed
    note typed on three lines would arrive back as one, or worse, be truncated at
    the first quote by whatever it was escaped with. A ``textarea``'s content is
    character data, so `esc` is the correct and sufficient treatment.
    """
    attrs = f' placeholder="{esc(placeholder)}"'
    attrs += f" {hook}" if hook else ""
    return f"<textarea{attrs}>{esc(value)}</textarea>"


def _command(command: str) -> str:
    """A shell command on its own line, using the app's own copy affordance."""
    return f'<div class="cmdrow">{_copyable(command)}</div>'


def _link(href: str, label: str) -> str:
    return f'<a href="{esc(href)}">{esc(label)}</a>'


def _ticket_left(row: ProjectTicketRow) -> str:
    """A ticket as one line: its ref in the typewriter face, then its summary."""
    ref = f'<span class="ref">{esc(row.ref)}</span> &nbsp;' if row.ref else ""
    return f"{ref}{esc(row.summary)}"


def _days_since(value: Optional[datetime], *, now: datetime) -> int:
    """Whole days since ``value``, floored at 0. 0 when nothing is recorded."""
    if value is None:
        return 0
    moment = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return max(0, int((now - moment).total_seconds() // 86400))


def _by_status(
    rows: Sequence[ProjectTicketRow], statuses: Sequence[TicketStatus]
) -> List[ProjectTicketRow]:
    """The rows in one of ``statuses``, **grouped in the order ``statuses`` names**.

    The argument decides the grouping, not `STATUS_ORDER`. It used to be a plain
    filter that kept arrival order, which happened to give the same answer
    because `project_tickets_for` had already sorted by `STATUS_ORDER` and the
    two orders agree -- so `WALK_STATUSES` documented itself as "the order the
    walk moves through them" while contributing nothing to the order at all.
    Reversing that tuple changed no output and no test.

    ``sort`` is stable, so the ``updated_at`` ordering inside each group
    survives, exactly as it does in `project_tickets_for`.
    """
    rank = {status.value: index for index, status in enumerate(statuses)}
    return sorted(
        (row for row in rows if row.status in rank), key=lambda row: rank[row.status]
    )


def _walk_rows(rows: Sequence[ProjectTicketRow]) -> List[ProjectTicketRow]:
    """Exactly the tickets the walk stops at, capped the way the walk caps them."""
    return _by_status(rows, WALK_STATUSES)[:WALK_CAP]


def _lingering_count(rows: Sequence[ProjectTicketRow], *, now: datetime) -> int:
    """How many of the walk's tickets have not moved in ``LINGER_DAYS``.

    One definition, two consumers: the wrap-up step shows it, and the walk sends
    it to the server as ``Scrum.lingering_count``. Deriving it twice is how the
    number on the screen and the number in the record start disagreeing.
    """
    return sum(
        1
        for row in _walk_rows(rows)
        if _days_since(row.updated_at, now=now) >= LINGER_DAYS
    )


# --------------------------------------------------------------------------- #
# The step specs
#
# One builder per workflow. Each returns the *shared* step list; anything that
# differs per project goes into `bodies` / `ctas` below, keyed `"<id>.<index>"`.
# --------------------------------------------------------------------------- #


def _step(
    title: str,
    guide: str,
    body: str = "",
    cta: str = "Continue",
    *,
    custom: Optional[str] = None,
    danger: bool = False,
) -> Dict[str, object]:
    step: Dict[str, object] = {"title": title, "guide": guide, "cta": cta}
    if body:
        step["body"] = body
    if custom:
        step["custom"] = custom
    if danger:
        step["danger"] = True
    return step


#: What every step of a workflow that writes nothing carries, under its controls
#: and directly above its button. One sentence rather than nine, because the fact
#: is the same one in all of them and a per-workflow wording is a per-workflow
#: chance to soften it.
UNWIRED_STEP_NOTE = (
    "Nothing on this step is saved. This workflow is a walkthrough of the work "
    "and not the work itself — nothing entered here reaches InnoDay."
)


def _unwired(handoff: str) -> Dict[str, object]:
    """The three fields a workflow that records nothing has to carry.

    **Eight of the ten workflows are this.** Only ``run-scrum`` and
    ``give-scrum-update`` write a row; the rest render their steps, collapse them
    and finish. Before these fields
    existed the finish said "<title> -- done. Nothing else is pending." over a
    walk that had created no ``Project``, linked no repo and cut no release --
    the same defect the scrum walk needed two review rounds to lose, in eight
    more places.

    They are data on the workflow rather than eight cases in the engine, so the
    day one is wired up it is this call that changes and nothing else has to be
    found. ``handoff`` names the command or page that *does* the thing, because
    "nothing was saved" on its own leaves the reader with no next move.

    Both strings are raw text -- the script escapes them at interpolation, like
    every other non-``bodies`` value on this page.
    """
    return {
        "saves": False,
        "warn": UNWIRED_STEP_NOTE,
        "done": "Nothing was saved. " + handoff,
    }


def _saves(done: str, *, records: str) -> Dict[str, object]:
    """The same three fields for a workflow that does write, plus what it writes to.

    ``done`` is the whole of the honesty here, and it has to name **what** was
    written rather than what the walk was about: `give-scrum-update` records the
    moves somebody asked for and applies none of them, so a sentence that merely
    said "saved" would let the reader supply the rest.

    ``records`` is the `ScrumKind` value the walk opens its row with. **It is data
    on the workflow rather than a branch in the engine** for the same reason
    ``saves`` is: the engine's job is to run whatever the spec describes, and the
    moment it knows a workflow *by name* the next one has to be added to it too.
    It is also what stops the two recording workflows sharing a row -- the kind
    travels with the open, so a record cannot turn out to be the wrong one.
    """
    return {"saves": True, "warn": "", "done": done, "records": records}


def _workflow_catalogue(org_ref: str) -> List[Dict[str, object]]:
    """Every workflow, in reading order, with the steps that are project-agnostic.

    The ten are fixed and ordered deliberately: **the two daily workflows lead
    Building** -- Run scrum, then Give scrum update -- because they are the ones
    that run every day, and a launcher whose daily workflow is third in its column
    is a launcher you scan past.

    Every entry declares whether walking it writes anything -- ``_saves`` for the
    two that do, ``_unwired`` for the eight that do not. See ``_unwired`` for why
    that is a field rather than eight special cases in the engine.
    """
    create_form = new_project_path(org_ref)
    return [
        # ---------------- vibing ----------------
        {
            "id": "create-project",
            "pillar": "vibing",
            "title": "Create a project",
            **_unwired(
                "Projects are created on the New project form, which is also "
                "where topic discovery reads GitHub live."
            ),
            "steps": [
                _step(
                    "Name it",
                    "The alias is the ticket prefix and the GitHub topic. "
                    "Three letters is plenty.",
                    _field("Project name", _text_input(placeholder="Atomic Pipeline"))
                    + _field(
                        "Alias",
                        _text_input(
                            placeholder="AP",
                            style="width:110px;font-family:var(--font-type);letter-spacing:.08em",
                        ),
                    )
                    + _note(
                        "Tickets will read <b>AP-1</b>, <b>AP-2</b>. Repos are found "
                        "by the matching GitHub topic."
                    ),
                ),
                _step(
                    "Find the repos",
                    "Discovered by topic. Uncheck anything that isn't part of "
                    "this project.",
                    _note(
                        "Topic discovery reads GitHub live, so it runs on the "
                        f"{_link(create_form, 'create form')} where the topic is "
                        "typed &mdash; this step is the shape of it, not a second "
                        "copy of it."
                    ),
                    cta="Continue",
                ),
                _step(
                    "Connect a board",
                    "Optional — you can sync a board later from the project page.",
                    _command(f"innoday init {org_ref.lower()}/<alias>")
                    + _note(
                        "Cloning happens on your machine, so the last move is a "
                        "command rather than a button."
                    ),
                    cta="Create project",
                ),
            ],
        },
        {
            "id": "connect-repos",
            "pillar": "vibing",
            "title": "Connect repos",
            **_unwired(
                "Repositories are discovered by GitHub topic when the project "
                "syncs, and layers are assigned on the project's Settings tab."
            ),
            "steps": [
                _step(
                    "Discover by topic",
                    "The alias is always searched. Add up to three more topics.",
                    cta="Discover",
                ),
                _step(
                    "Assign layers",
                    "Layers drive how the dashboard groups work. Unassigned is "
                    "fine to start.",
                    cta="Save layers",
                ),
            ],
        },
        # ---------------- planning ----------------
        {
            "id": "design-features",
            "pillar": "planning",
            "title": "Design features",
            **_unwired(
                "Run /pixelfuel:design-rocket in your Claude Code session to "
                "parse the description and create the drafts for real."
            ),
            "steps": [
                _step(
                    "Describe it",
                    "Plain sentences. One thought per line works best.",
                    _field(
                        "What are we building?",
                        _textarea(
                            "Workflow homepage — project rail, four pillars, "
                            "animated step runner."
                        ),
                    ),
                    cta="Parse into tickets",
                ),
                _step(
                    "Review the tickets",
                    "Parsed, not saved. Edit anything before it becomes real.",
                    cta="Looks right",
                ),
                _step(
                    "Create as draft",
                    "Drafts stay in InnoDay until you push them to the board.",
                    cta="Create the drafts",
                ),
            ],
        },
        {
            "id": "organize-release",
            "pillar": "planning",
            "title": "Organize the release",
            **_unwired(
                "The version is named and its tickets attached on the project's "
                "Releases tab, which is the one place a release is written."
            ),
            "steps": [
                _step(
                    "Set the version",
                    "Suggested from the last released tag. Override if this is a "
                    "bigger swing.",
                    cta="Set the version",
                ),
                _step(
                    "Pull in what's done",
                    "Finished tickets with no release assigned yet.",
                    cta="Add to the release",
                ),
            ],
        },
        # ---------------- building ----------------
        {
            "id": "run-scrum",
            "pillar": "building",
            "title": "Run scrum",
            **_saves(
                "The scrum is recorded — one row for the meeting, one per "
                "ticket visited, written as the walk went. Finish returns you "
                "to the project and workflow picker.",
                records="scrum",
            ),
            "steps": [
                _step(
                    "Review today's summary",
                    "Already generated for this project. Correct anything wrong "
                    "before the walk.",
                    cta="Start the walk",
                ),
                _step(
                    "Walk the board",
                    "In test first, then in progress. Enter moves on. Time lands "
                    "on whichever ticket is up.",
                    custom="walk",
                    cta="Done walking",
                ),
                _step(
                    "Wrap up",
                    "Regenerated from the walk — your comments, the moves, and "
                    "the clock.",
                    cta="Save scrum",
                ),
            ],
        },
        {
            "id": "give-scrum-update",
            "pillar": "building",
            "title": "Give scrum update",
            # `_saves`, because it does: one `Scrum` row of kind `update`, one
            # `ScrumTicketVisit` per choice, **and the moves themselves**.
            # **The wording is the load-bearing part, in both directions.** It
            # used to say the tickets had not moved, which was true then and is
            # not now -- and a panel that understates what a button did is the
            # same failure as one that overstates it, because the reader cannot
            # act on either. What it must not do is promise the *board* was
            # updated: that is reported per run, from what the push actually
            # answered, in `#wferr`.
            **_saves(
                "Your update is recorded and applied — the tickets you ticked "
                "have moved to in progress, and anything you took on is assigned "
                "to you. Where the project is connected to a board, each move was "
                "pushed there too; anything the board would not accept is named "
                "above rather than hidden. Finish returns you to the picker.",
                records="update",
            ),
            "steps": [
                _step(
                    "Bring anything back?",
                    "Work you finished in the last week that is not actually "
                    "done. Tick it to ask for it back.",
                    custom="picks",
                    cta="Record these",
                ),
                _step(
                    "Take anything on?",
                    "Queued work nobody owns yet, oldest first. Tick what you "
                    "are picking up.",
                    custom="picks",
                    cta="Record these",
                ),
                _step(
                    "Submit",
                    "Everything you ticked, plus anything you want to say about "
                    "it. Yours to correct until the day is over.",
                    cta="Submit update",
                ),
            ],
        },
        {
            "id": "pick-ticket",
            "pillar": "building",
            "title": "Pick up a ticket",
            **_unwired(
                "Run /pixelfuel:build-rockets in your Claude Code session — it "
                "takes the ticket, marks it in progress and opens the worktree."
            ),
            "steps": [
                _step(
                    "Choose what's next",
                    "Open tickets in this project, closest to ready first.",
                    cta="Take it",
                ),
                _step(
                    "Launch the agent",
                    "Run this in your Claude Code session. It creates the "
                    "worktree, branch and PR.",
                    cta="Mark in progress",
                ),
            ],
        },
        {
            "id": "review-pr",
            "pillar": "building",
            "title": "Review a PR",
            **_unwired(
                "Reviews run in your Claude Code session against the checkout, "
                "and the pull request itself is still chosen on GitHub."
            ),
            "steps": [
                _step(
                    "Pick the PR",
                    "Open pull requests across every repo in this project.",
                    cta="Continue",
                ),
                _step(
                    "Send it to review",
                    "Multi-agent review runs on the diff before a human sees it.",
                    _command("/code-review")
                    + _note(
                        "Review runs in your Claude Code session against the "
                        "checkout, not on the server."
                    ),
                    cta="Start review",
                ),
            ],
        },
        # ---------------- releasing ----------------
        {
            "id": "summarize-release",
            "pillar": "releasing",
            "title": "Summarize the release",
            **_unwired(
                "Run blastoff summarize where the repos are — it writes the "
                "narrative and stores it on the release."
            ),
            "steps": [
                _step(
                    "Assemble the material",
                    "Tickets, commits and PRs since the last release. No prose yet.",
                    cta="Assemble",
                ),
                _step(
                    "Narrate and save",
                    "Written where the repos are, then stored on the release.",
                    cta="Save summary",
                ),
            ],
        },
        {
            "id": "run-release",
            "pillar": "releasing",
            "title": "Run the release",
            **_unwired(
                "Run innoday blastoff from your machine — tagging every repo "
                "needs push credentials the server does not hold."
            ),
            "steps": [
                _step(
                    "Preflight",
                    "A dry run. Nothing is tagged or pushed.",
                    cta="Run preflight",
                ),
                _step(
                    "Confirm what ships",
                    "Each repo gets the release tag. This is the last reversible "
                    "moment.",
                    cta="Confirm",
                ),
                _step(
                    "Execute",
                    # **It does not close tickets, and saying so was a promise
                    # the platform deliberately stopped keeping.**
                    # `_bulk_close_tickets_for_release` was removed because
                    # membership in a release is free text somebody typed, not
                    # evidence that work happened -- so a ticket nobody started
                    # was being closed with a completion timestamp, identically
                    # to one that shipped. This line outlived it, and a person
                    # reading it has every reason to leave finished work open
                    # expecting the release to tidy up. See `_shipped_stamp`.
                    "Tags every repo and publishes the release. Tickets are "
                    "left alone \u2014 closing them stays your call.",
                    cta="Blast off",
                    danger=True,
                ),
            ],
        },
    ]


# --------------------------------------------------------------------------- #
# Per-project bodies
# --------------------------------------------------------------------------- #


def _pick_comment(ticket_id: int, value: str) -> str:
    """The box for what you want to say about one ticket.

    **A sibling of the row, not a field inside it.** `_row` renders one line --
    something on the left, a chip on the right -- and eight other steps depend on
    that markup being what it is (`test_the_other_eight_pickers_keep_their_markup_byte_identical`).
    A multi-line control does not belong on a line.

    **A `<textarea>` text node, never `_text_input(value=…)`.** A comment is
    prose, so it has newlines, and a newline is not representable in an HTML
    attribute -- a note typed on three lines would come back as one. `_textarea`
    puts its value in character data, where `esc` is the correct and sufficient
    treatment. This page sends no Content-Security-Policy header and the value is
    whatever a teammate typed, so that is not a detail.

    ``data-pick-note`` carries the ticket id for the same reason ``data-pick``
    does, and with the same argument for not escaping it: ``int()`` either
    produces an integer or raises, and an integer in an attribute cannot carry a
    quote or an angle bracket.
    """
    return (
        '<div class="pcom">'
        + _textarea(
            "Optional — posted as a comment on the ticket, here and on the board.",
            hook=f'data-pick-note="{int(ticket_id)}"',
            value=value,
        )
        + "</div>"
    )


def _pick_rows(
    rows: Sequence[ProjectTicketRow],
    *,
    cap: int,
    picked: Dict[int, str],
    empty: str,
    comments: Optional[Dict[int, str]] = None,
) -> str:
    """A picker's rows: one tickable line each, prior choices already ticked.

    ``picked`` is what the day's record already holds (`data.ScrumActivity`), so a
    resumed step shows what was recorded rather than an empty form inviting the
    reader to blank it. Rendered server-side because the whole list is known here
    -- the script's job is to read the boxes, not to discover them.

    ``comments`` is the same thing for what was *said* about each pick. It is
    resumed for exactly the reason the tick is: the post sends the whole answer,
    so a box rendered empty over a recorded comment would delete it the moment
    somebody pressed through -- and this page's one rule is that it never reports
    a save it did not get, in either direction.

    ``_ticket_left`` is the row formatter, not a second one written here: it is
    where `esc` is applied to a board-supplied summary and ref, and this page sends
    no CSP header, so a parallel formatter is a parallel escaping decision.
    """
    if not rows:
        return _note(empty)
    comments = comments or {}
    out = "".join(
        _row(
            _ticket_left(row),
            _status_pill(row.status),
            check=int(row.id) in picked,
            ticket_id=int(row.id),
        )
        + _pick_comment(int(row.id), comments.get(int(row.id), ""))
        for row in rows[:cap]
    )
    extra = len(rows) - cap
    if extra > 0:
        out += _note(f"{extra} more not shown.")
    return out


#: What a comment box actually does, said once and shown under both pickers.
#:
#: **It names both halves and the order they happen in.** A comment is written to
#: InnoDay first and pushed to the board second, and either can be true without
#: the other -- so a sentence promising only "it goes on the ticket" would be a
#: claim the page cannot keep. Saying so up front is what makes the failure
#: banner afterwards read as a detail rather than as a surprise.
_COMMENT_NOTE = _note(
    "What you type beside a <b>ticked</b> ticket is <b>posted as a comment on "
    "it</b> when you submit &mdash; recorded in InnoDay, and sent on to the board "
    "where there is one, signed with your name so the board knows who said it. "
    "If the board will not take it you are told, and the comment is still here. "
    "A note beside a ticket you have not ticked is not part of your update and "
    "is not kept &mdash; you are told at submit if that happens. Clearing a box "
    "you already submitted removes it from your update here; it cannot take back "
    "a comment the board has already been given. If a comment cannot be sent "
    "the first time it is sent again later, so a board may occasionally end up "
    "with it twice &mdash; that is deliberate, because a comment nobody can see "
    "is worse than one said twice."
)


#: Said on `run-scrum` when nobody has given their own update yet today.
#:
#: **Rendered here rather than by `_bubbles`.** That helper answers "who is mapped
#: to this project" and says *"No one mapped yet"* on an empty list -- which on
#: this step would be a different and wrong fact: the team is mapped, they simply
#: have not filled their form in yet. The dashboard card depends on that wording,
#: so the empty case is answered here and `_bubbles` is left alone.
_NO_SUBMITTERS_YET = "Nobody has given their update yet today."


def _submitters_group(activity: Optional[ScrumActivity], org_ref: str) -> str:
    """Today's update submitters as an avatar group, or the empty sentence.

    `_bubbles` returns **already-escaped HTML**, so whatever this returns is a
    ``bodies`` value -- the engine assigns those with ``innerHTML`` -- and never a
    raw-text field. Teammate names are self-edited, so they are attacker-writable
    in exactly the way a board summary is; `_bubbles` runs them through `esc`.

    ``activity.submitters`` is used as it comes, without a second query: it is
    populated by the *same* read that answers the daily ticks
    (`data.scrum_activity_today`), which is what stops the tick and the avatars
    disagreeing about who has submitted. An abandoned update is already excluded
    there -- `ended_at IS NULL` is how this schema spells "walked out of it".
    """
    people = list(activity.submitters) if activity is not None else []
    if not people:
        return f'<span class="meta">{esc(_NO_SUBMITTERS_YET)}</span>'
    return _bubbles(people, org_ref)


def _submitters_sentence(activity: Optional[ScrumActivity]) -> str:
    """Who has submitted, named -- the wrap-up's own sentence.

    A group of initials says *how many*; the wrap-up is where the walk is written
    down, so it names them. Built here rather than sent as a raw-text field for
    the same reason every other sentence on this page is: it lands in a ``bodies``
    value, and one escaping decision per string beats two channels that have to
    agree.
    """
    names = [person.name for person in (activity.submitters if activity else [])]
    if not names:
        return _note(
            "No one has given their own update today, so this wrap-up covers the "
            "walk alone."
        )
    listed = ", ".join(esc(name) for name in names)
    return _note(
        f"Updates in today from <b>{listed}</b> "
        f"&mdash; {len(names)} of the team, recorded before this walk."
    )


def _project_steps(
    card: ProjectCard,
    org_ref: str,
    *,
    panel: Optional[object],
    tickets: Sequence[ProjectTicketRow],
    unreleased: Sequence[ProjectTicketRow],
    unreleased_total: Optional[int] = None,
    reopen: Sequence[ProjectTicketRow] = (),
    take: Sequence[ProjectTicketRow] = (),
    activity: Optional[ScrumActivity] = None,
    now: datetime,
) -> tuple:
    """Every step body **and** button label that depends on the project in context.

    Returns ``(bodies, ctas)``, both keyed ``"<workflow id>.<step index>"``. A
    key that is absent falls back to the catalogue's shared value, so a step
    appears here only when it has something project-specific to say.

    **One function rather than two.** The bodies and the buttons were built
    separately and each derived ``suggested``, ``queued`` and ``first_ref`` from
    the same rows to reach the same answers -- and they are only ever called
    together, once per project, on the same arguments. Two derivations of one
    value is how a button comes to name a version the step below it does not
    show.

    Every read this needs was already done by the caller and handed in. Nothing
    in here touches a session: the page is one batch of queries, not one batch
    per project and certainly not one per step.

    ``unreleased_total`` is how many finished-and-unreleased tickets the project
    actually has; ``unreleased`` is the capped page of them
    (`done_unreleased_for`). They are different numbers and the difference is
    the point -- ``len(unreleased)`` was being printed as the total, so a
    project with 300 of them read "60 finished tickets with no release" and was
    told "52 more not shown" about 292. None means "not counted", and the rows
    in hand are then the only honest answer available.
    """
    alias = card.alias
    page = project_path(org_ref, alias)
    bodies: Dict[str, str] = {}
    ctas: Dict[str, str] = {}
    total_unreleased = len(unreleased) if unreleased_total is None else unreleased_total

    # ---- connect repos -------------------------------------------------- #
    repo_count = len(card.repos)
    bodies["connect-repos.0"] = _row(
        f"{repo_count} repositor{'y' if repo_count == 1 else 'ies'} linked",
        _chip(alias.lower(), "n"),
    ) + _note(
        "The alias is always searched as a GitHub topic. Adding more topics "
        f"is a {_link(page + '/settings', 'project setting')}."
    )
    if card.repos:
        rows = "".join(
            _row(esc(repo.name), _chip(repo.layer or "unassigned", "n"))
            for repo in card.repos[:PICK_CAP]
        )
    else:
        rows = _note(
            "No repositories are linked yet. They are discovered by topic when "
            "the project syncs."
        )
    bodies["connect-repos.1"] = rows + _note(
        f"The layer picker itself lives on the {_link(page + '/settings', 'settings tab')} "
        "&mdash; one write path, not two."
    )

    # ---- design features ------------------------------------------------ #
    bodies["design-features.1"] = _note(
        "Parsing happens in your Claude session, not on this page &mdash; the "
        "server has no parser to call, and a button that could only print a "
        "command is a worse version of printing it."
    ) + _command(f"/pixelfuel:design-rocket {alias.lower()}")
    bodies["design-features.2"] = _note(
        "Drafts are hidden from ticket lists unless you filter for them, so they "
        f"will not clutter the board. They land on the "
        f"{_link(page + '/tickets', 'tickets tab')}."
    )

    # ---- organize the release ------------------------------------------- #
    last = card.latest_released.version if card.latest_released else None
    suggested = (
        card.next_release.version
        if card.next_release
        else (card.next_version_suggestion or "")
    )
    bodies["organize-release.0"] = (
        _row("Last released", _chip(last or EM_DASH, "n"))
        + _field(
            "Next version",
            _text_input(
                value=suggested,
                placeholder="v1.0.0",
                style="width:150px;font-family:var(--font-type)",
            ),
        )
        + _note(
            "Naming it writes to the release board on the "
            f"{_link(page + '/releases', 'releases tab')}, which is the one place "
            "a version is set."
        )
    )
    if unreleased:
        rows = "".join(
            _row(_ticket_left(row), _status_pill(row.status), check=True)
            for row in unreleased[:PICK_CAP]
        )
        # Against the real total, not against the page of rows in hand: the
        # sentence is about what is *not* on screen, so counting only what is
        # makes it wrong by exactly the amount that matters.
        extra = total_unreleased - PICK_CAP
        if extra > 0:
            rows += _note(f"{extra} more not shown.")
        bodies["organize-release.1"] = rows
    else:
        bodies["organize-release.1"] = _note(
            "Nothing is finished and unassigned to a release right now."
        )

    # ---- run scrum ------------------------------------------------------ #
    summary = getattr(panel, "summary", None) if panel is not None else None
    if summary is not None and (summary.body_markdown or "").strip():
        opening = f'<div class="wprose">{_summary_prose(summary.body_markdown)}</div>'
    else:
        opening = _note(
            "No scrum summary has been generated for this project yet. Summaries "
            "are written where the repos are, and appear here for the whole team."
        ) + _command("innoday summary --scrum")
    bodies["run-scrum.0"] = (
        # Who has already said their piece, before the room walks the board. It
        # leads the step because it changes what the walk is for: with four
        # updates in, the meeting is reading them; with none, it is collecting
        # them.
        _row("Updates in today", _submitters_group(activity, org_ref))
        + opening
        + _field(
            "Corrections",
            _textarea(
                "What the summary got wrong — saved with the scrum record.",
                hook="data-scrum-notes",
            ),
        )
        + _note(
            "Saved to the scrum record as <b>notes_markdown</b> when you finish, "
            "and fed to the closing regeneration."
        )
    )

    lingering = _lingering_count(tickets, now=now)
    bodies["run-scrum.2"] = (
        _row(
            f"Lingering over {LINGER_DAYS} days",
            _chip(f"{lingering} ticket{'' if lingering == 1 else 's'}", "a"),
        )
        + _row("Total time", '<span class="meta" data-wf-total>&mdash;</span>')
        + _row("Updates in today", _submitters_group(activity, org_ref))
        # The group says how many; this names them, which is what a wrap-up is
        # for. Both are `bodies` values -- `_bubbles` returns escaped HTML and the
        # sentence interpolates names, so neither may travel as raw text.
        + _submitters_sentence(activity)
        + _field(
            "Transcript link",
            _text_input(
                placeholder="https://… meeting recording or transcript",
                hook="data-scrum-transcript",
            ),
        )
        + _note(
            "Stored as a <b>Scrum</b> row &mdash; both summaries, the transcript "
            "link, total time and who ran it &mdash; plus one "
            "<b>ScrumTicketVisit</b> per ticket with its seconds. The visits were "
            "written as the walk went; this button writes the wrap-up and closes "
            "the run."
        )
        + _command("innoday summary --scrum")
    )

    # ---- give scrum update ---------------------------------------------- #
    #
    # Every sentence below is written to the same rule: **it says what happens,
    # and when.** Ticking records the ask (`ScrumTicketVisit.moved_to`);
    # *submitting* writes `Ticket.status` and pushes it to the board. Both halves
    # have to be in the copy, because a step that said "records that you want it
    # back" and nothing else now understates the button -- somebody would tick
    # boxes believing they could think about it afterwards. Saying only "moves it"
    # would be wrong in the other direction: nothing moves until the last step.
    picked = dict(activity.my_picks) if activity is not None else {}
    said = dict(activity.my_pick_comments) if activity is not None else {}
    resumed = activity is not None and activity.my_update_scrum_id is not None
    bodies["give-scrum-update.0"] = (
        _pick_rows(
            reopen,
            cap=PICK_CAP,
            picked=picked,
            comments=said,
            empty=(
                "You have not finished anything in the last "
                f"{REOPEN_WINDOW_DAYS} days, so there is nothing to bring back."
            ),
        )
        + _note(
            "Ticking a ticket <b>records that you want it back</b>; <b>submitting "
            "moves it</b> to in progress, clears its completion date, and pushes the "
            "change to the board if this project has one. Until you submit it is "
            "still yours to un-tick. Only work with a recorded completion date "
            "(<b>completed_at</b>) can appear here: a finished ticket the board never "
            "stamped is not offered, because guessing the date from the last sync "
            "would offer you things you finished months ago."
        )
        + _COMMENT_NOTE
    )
    bodies["give-scrum-update.1"] = (
        _pick_rows(
            take,
            cap=TAKE_CAP,
            picked=picked,
            comments=said,
            empty="Nothing queued is unowned right now.",
        )
        + _note(
            "Unowned work only, oldest first &mdash; a ticket somebody already has is "
            "not offered, here or anywhere else. Ticking one <b>records that you are "
            "taking it</b>; <b>submitting assigns it to you</b> and moves it to in "
            "progress, on the board as well where there is one. If the board cannot "
            "tell which of its members you are, the move still happens and you are "
            "told the assignment is InnoDay-only."
        )
        + _COMMENT_NOTE
    )
    chosen = len(picked)
    bodies["give-scrum-update.2"] = (
        _row(
            "Recorded so far",
            # `data-wf-picked`, repainted by the engine from what the server said
            # it stored -- the same mechanism, and the same reason, as the walk's
            # `data-wf-total`. The value here is only the opening one: it is what
            # the record held when the page was served, which on a fresh run is
            # zero and stops being true the moment the first picker submits.
            f'<span class="wchip n" data-wf-picked>'
            f"{chosen} ticket{'' if chosen == 1 else 's'}</span>",
        )
        + _field(
            "Anything to say?",
            _textarea(
                "Optional — what you are stuck on, what you need, what changed.",
                # The same hook the scrum's wrap-up notes use, deliberately: the
                # name says which *field* this is (`Scrum.notes_markdown`), not
                # which workflow rendered it. That is what lets `closeRecord` and
                # `FIELD_HOOKS` stay one implementation instead of learning a
                # second control for the same column. Only one workflow is ever
                # on screen, so the two cannot collide.
                hook="data-scrum-notes",
                value=(activity.my_update_notes or "") if activity is not None else "",
            ),
        )
        + _note(
            "Stored as a <b>Scrum</b> row of kind <b>update</b> &mdash; yours, this "
            "project's, today's &mdash; plus one <b>ScrumTicketVisit</b> per ticket "
            "recording the status you asked for. This button is also what "
            "<b>applies</b> those moves and pushes them to the board; a move the "
            "board refuses is kept here and shown, never dropped quietly. "
            + (
                "You have already submitted today; this rewrites that record "
                "rather than adding a second one."
                if resumed
                else "Re-entering this workflow later today reopens this same "
                "record rather than starting a second one."
            )
        )
    )
    # **No count on the button.** It was `f"Submit update ({chosen} recorded)"`,
    # baked at render like the chip above -- but unlike the chip there is nothing
    # for the engine to repaint it from without inventing a second hook for a
    # number the row directly above already states. A button label that is
    # reliably wrong is worse than one that is merely plain.

    # ---- pick up a ticket ----------------------------------------------- #
    queued = _by_status(tickets, (TicketStatus.TODO, TicketStatus.BACKLOG))
    if queued:
        # `_status_pill` decides the colour, here and in `_pull_markup`. It is
        # `render.py`'s one status-to-colour mapping and this page had started a
        # second: BACKLOG was slate in this step and amber in the walk's pull
        # list, from two hand-written choices about the same status.
        bodies["pick-ticket.0"] = "".join(
            _row(
                _ticket_left(row),
                _status_pill(row.status),
                check=(index == 0),
            )
            for index, row in enumerate(queued[:PICK_CAP])
        )
    else:
        bodies["pick-ticket.0"] = _note(
            "Nothing is queued on this board. Design a feature first, or pull "
            "something out of the backlog."
        )
    first_ref = next((row.ref for row in queued if row.ref), None)
    bodies["pick-ticket.1"] = _command(
        f"/pixelfuel:build-rockets {first_ref}"
        if first_ref
        else "/pixelfuel:build-rockets"
    ) + _note(
        "The ticket is marked <b>in progress</b> and labelled with your agent "
        "identity when the run starts."
    )

    # ---- review a PR ---------------------------------------------------- #
    # Counts, not a list: open pull requests are rendered in-process per repo
    # today and there is no endpoint that returns them, so the step says what it
    # can see and stays honest about the rest rather than showing nothing.
    open_prs = [repo for repo in card.repos if (repo.open_pr_count or 0) > 0]
    if open_prs:
        rows = "".join(
            _row(
                esc(repo.name),
                _chip(
                    f"{repo.open_pr_count} open PR"
                    f"{'' if repo.open_pr_count == 1 else 's'}"
                ),
            )
            for repo in open_prs[:PICK_CAP]
        )
    else:
        rows = _note("No open pull requests were counted on this project's repos.")
    bodies["review-pr.0"] = rows + _note(
        "<b>Counts only.</b> Pull requests are rendered in-process today and are "
        "not reachable as a list, so the choice of which one is still made on "
        "GitHub.",
        warn=True,
    )

    # ---- summarize the release ------------------------------------------ #
    ready = total_unreleased
    bodies["summarize-release.0"] = _row(
        f"{ready} finished ticket{'' if ready == 1 else 's'} with no release",
        f'<span class="meta">across {repo_count} '
        f"repo{'' if repo_count == 1 else 's'}</span>",
    ) + _row("Next version", _chip(suggested or EM_DASH, "n"))
    bodies["summarize-release.1"] = _note(
        "The narrative is written where the repos are and then stored on the "
        "release, for the reason the scrum panel gives: there is no server-side "
        "narration to fire."
    ) + _command(f"blastoff summarize --alias {alias.lower()}")

    # ---- run the release ------------------------------------------------ #
    bodies["run-release.0"] = _note(
        "The dry run reads your working trees, so it runs on your machine. "
        "Nothing is tagged or pushed."
    ) + _command("innoday blastoff --dry-run")
    if card.repos:
        target = suggested or "next"
        bodies["run-release.1"] = "".join(
            _row(
                esc(repo.name),
                f'<span class="meta">{esc(last or EM_DASH)} &rarr; {esc(target)}</span>',
            )
            for repo in card.repos[:PICK_CAP]
        )
    else:
        bodies["run-release.1"] = _note(
            "No repositories are linked, so there is nothing to tag."
        )
    # The execute endpoint is deliberately out of scope: release execution
    # imports `blastoff.release.Release` and runs it in-process in the CLI, and
    # doing it server-side needs Vault push credentials, a job record with
    # polling and a shared dry-run path. The workflow stays complete and honest
    # rather than absent.
    bodies["run-release.2"] = _note(
        "<b>Releases are executed from your machine.</b> Running one here would "
        "need push credentials on the server and a job to poll, so this step "
        "hands you the command instead.",
        warn=True,
    ) + _command("innoday blastoff")

    # ---- the buttons ----------------------------------------------------- #
    # A button that names what it is about to do ("Take PF-1320") is the whole
    # difference between a wizard and a form, so the few that can name it, do.
    # Every value they need was derived above, once.
    if first_ref:
        ctas["pick-ticket.0"] = f"Take {first_ref}"
    elif not queued:
        ctas["pick-ticket.0"] = "Nothing queued"

    if unreleased:
        # The number of rows the step actually ticked, not the total: this
        # button is a promise about what is on screen.
        ctas["organize-release.1"] = (
            f"Add {min(len(unreleased), PICK_CAP)} to the release"
        )

    if repo_count:
        ctas["run-release.1"] = (
            f"Confirm {repo_count} repo{'' if repo_count == 1 else 's'}"
        )

    if suggested:
        ctas["organize-release.0"] = f"Set {suggested}"

    return bodies, ctas


def _walk_payload(
    tickets: Sequence[ProjectTicketRow],
    *,
    panel: Optional[object],
    now: datetime,
) -> List[Dict[str, object]]:
    """The scrum walk's queue: in review first, then in progress.

    **The order is the point.** Work closest to shipping is what a stand-up
    should spend its first minutes on, and IN_REVIEW is the closest state the
    board has. It is labelled "In test" on the chip and nowhere else -- see
    ``WALK_STATUSES``.

    Values here are raw text: the script escapes them at interpolation.

    ``id`` is ``ticket.id`` -- the integer primary key, not the board's ``ref``.
    It is here because each stop is written to the server as it ends, and
    `ScrumTicketVisit.ticket_id` is that integer. The ref is what a person reads;
    the id is what the row points at.

    **No pull-request entry.** An earlier revision emitted one, guarded by
    ``safe_url``, from ``ProjectTicketRow.pull_requests`` -- which
    ``project_tickets_for`` (the only feed for this page) never populates, and
    which the issue puts out of scope. Dead code carrying a security control
    reads as a live path being defended; it was neither, so it is gone. Adding
    the list back means populating that field and restoring the ``safe_url``
    call with it, in one change rather than finding half of it already here.
    """
    notes: Dict[str, str] = {}
    for row in getattr(panel, "active", None) or []:
        ref = getattr(row, "ticket_ref", None)
        body = getattr(row, "body_markdown", None)
        if ref and body and ref not in notes:
            notes[ref] = " ".join(str(body).split())

    return [
        {
            "id": row.id,
            "ref": row.ref or EM_DASH,
            "sum": row.summary,
            "st": row.status,
            "lbl": _STATUS_LABELS.get(row.status, row.status),
            "days": _days_since(row.updated_at, now=now),
            "note": notes.get(row.ref or "", ""),
            "owner": (row.owner or "").lstrip("@"),
        }
        for row in _walk_rows(tickets)
    ]


#: What the update records against each ticket it is told about. One status, named
#: once: the step copy, the payload, the visit row **and the write** all have to
#: agree, and separate literals is how they come to disagree.
#:
#: Owned by `scrum_service`, which refuses to apply anything else -- `moved_to` is
#: free text on the column, so without that refusal a hand-rolled post could name
#: any status at all. The constant lives where the enforcement is; this is the
#: page's view of it.
UPDATE_MOVES_TO = scrum_service.APPLIED_UPDATE_STATUS.value


def _with_resumed_picks(
    reopen: Sequence[ProjectTicketRow],
    take: Sequence[ProjectTicketRow],
    activity: Optional[ScrumActivity],
) -> tuple:
    """Put back any pick the day's record holds that its own list no longer offers.

    **Why this is needed at all, and why it is not cosmetic.** Submitting now
    *applies* the moves, so a ticket brought back from DONE is IN_PROGRESS
    afterwards -- out of `my_done_recently_for`'s answer -- and a ticket taken on
    is assigned, out of `unowned_todo_for`'s. Re-entering the workflow would show
    two empty pickers, and pressing through posts the complete selection it can
    see: an empty one. `replace_picks` is a whole-set write by design, so it would
    faithfully delete every visit the day's record holds -- and with them each
    visit's `push_error`, the only record that a move never reached the board.
    Opening a record to look at it would destroy it.

    So a recorded pick stays visible for as long as it is recorded. The box is
    already ticked (`_pick_rows` reads `picked`), so re-submitting re-sends it and
    converges; un-ticking still expresses a withdrawal, which now means "take this
    off my update" rather than "put the ticket back" -- nothing here reverses a
    move that has already been applied, and the step copy does not claim it does.

    **Which picker a resumed row goes under is decided by `status_at_visit`, not
    by the ticket's status now.** That column is the visit's own historical
    observation of where the ticket was when it was picked, so a row returns to
    the step the person actually used. Deciding from the current status would put
    everything under "bring anything back", since a take ends up IN_PROGRESS too.
    """
    if activity is None or not activity.my_pick_rows:
        return list(reopen), list(take)

    known = {int(row.id) for row in reopen} | {int(row.id) for row in take}
    extra_back: List[ProjectTicketRow] = []
    extra_take: List[ProjectTicketRow] = []
    for row in activity.my_pick_rows:
        ticket_id = int(row.id)
        if ticket_id in known:
            continue
        was = activity.my_pick_status_at_visit.get(ticket_id, "")
        if was == TicketStatus.DONE.value:
            extra_back.append(row)
        else:
            extra_take.append(row)

    # **Prepended, not appended.** `_pick_rows` cuts at `rows[:cap]`, so anything
    # at the tail is what falls off -- and a recorded pick is the one row in the
    # list that must not, because a pick the page cannot show is a pick the next
    # submit deletes. It also reads better: what you already chose is at the top.
    return extra_back + list(reopen), extra_take + list(take)


def _update_payload(
    reopen: Sequence[ProjectTicketRow],
    take: Sequence[ProjectTicketRow],
    activity: Optional[ScrumActivity] = None,
) -> Dict[str, object]:
    """What the update workflow's script needs that the markup cannot carry.

    The checkbox carries a ticket id (``data-pick``) and nothing else, because an
    integer in an attribute is provably safe and a status string in one is a second
    escaping decision. So the status each ticket is *at* -- required, because
    `ScrumTicketVisit.status_at_visit` is NOT NULL and records a historical
    observation -- travels here instead, keyed by id.

    Values are raw text; the script escapes at interpolation, and none of these
    reach markup anyway.

    **Two fields are deliberately absent.** An earlier revision also emitted
    ``picked`` (the ids already recorded) and ``scrumId`` (the day's record), and
    the script read neither: the pre-ticked boxes come from the server-rendered
    markup, and the record id comes from `ensureOpen`, which asks for it rather
    than trusting a value the page was rendered with. Tests pinned both, which is
    the strongest possible signal that a field is load-bearing -- and this repo has
    been bitten more than once by config that read as live because something
    referenced it. If a later change needs either, it can add it back with a
    consumer in the same commit.
    """
    rows: Dict[str, str] = {}
    for row in list(reopen[:PICK_CAP]) + list(take[:TAKE_CAP]):
        rows[str(int(row.id))] = row.status
    # **A resumed pick posts the status it was picked at, not the status it is
    # at now.** `status_at_visit` is a historical observation the column's own
    # description says must never be rewritten -- and by the time somebody
    # re-enters, the move has been applied, so `row.status` is the *result* of
    # the pick rather than its subject. Posting that overwrote the observation,
    # and since a resumed row is routed back to its picker by exactly that value,
    # a brought-back ticket appeared under "Take anything on?" on the second
    # re-entry. `replace_picks` also refuses to overwrite it, which is the
    # authoritative half; this keeps the wire honest as well.
    if activity is not None:
        for ticket_id, was in activity.my_pick_status_at_visit.items():
            rows[str(int(ticket_id))] = was
    return {"moveTo": UPDATE_MOVES_TO, "rows": rows}


def _ticks(activity: Optional[ScrumActivity]) -> Dict[str, object]:
    """Which of the two daily workflows already has today's answer, per project.

    **Painted client-side from this, not baked into the grid.** The workflow buttons
    are rendered once for the whole page while the rail switches project in the
    browser with no round trip -- so a tick rendered into the button would keep
    saying whatever the project you arrived with had done.

    **The two hover strings are deliberately different sentences**, because the two
    ticks answer different questions and a reader who assumes otherwise draws the
    wrong conclusion in both directions: an update tick means *you* did it, and a
    scrum tick means *somebody* did. Identical wording would make "already done"
    ambiguous exactly where it matters -- somebody deciding whether to go and run
    the stand-up again.
    """
    mine = activity is not None and activity.my_update_submitted
    theirs = activity is not None and activity.scrum_ran
    return {
        "give-scrum-update": {
            "on": mine,
            "title": (
                "You have given your update today"
                if mine
                else "You have not given your update today"
            ),
        },
        "run-scrum": {
            "on": theirs,
            "title": (
                "Somebody has run scrum for this project today"
                if theirs
                else "Nobody has run scrum for this project today"
            ),
        },
    }


def _pull_markup(tickets: Sequence[ProjectTicketRow]) -> str:
    """The two lists the walk ends on: pull something in, or reopen something.

    Rendered server-side because they are the same for the whole meeting -- only
    the ticket the clock is on changes, and that is the part the script paints.
    """
    todo = _by_status(tickets, (TicketStatus.TODO, TicketStatus.BACKLOG))[:PICK_CAP]
    done = _by_status(tickets, (TicketStatus.DONE,))[:PICK_CAP]
    out = ""
    if todo:
        # `_status_pill` again, for the reason `pick-ticket.0` gives: this list
        # painted BACKLOG amber while that one painted it slate.
        out += '<div class="qhead">Anything to pull in?</div>' + "".join(
            _row(_ticket_left(row), _status_pill(row.status), check=False)
            for row in todo
        )
    if done:
        out += '<div class="qhead">Anything to reopen?</div>' + "".join(
            _row(_ticket_left(row), _status_pill(row.status), check=False)
            for row in done
        )
    if not out:
        out = _note("Nothing queued and nothing finished in this window.")
    return out


# --------------------------------------------------------------------------- #
# The page
# --------------------------------------------------------------------------- #


def _json_blob(payload: object) -> str:
    """``payload`` as JavaScript, safe to sit inside a ``<script>`` element.

    ``json.dumps`` alone is not enough: a value containing ``</script>`` closes
    the element that carries it, and every string in here is either a ticket
    summary somebody typed on a board or markup this module built out of one.
    Escaping the three characters that can start a tag or an entity means the
    parser sees no markup at all, and the JS string literals still decode to
    exactly what was meant.

    U+2028 and U+2029 are escaped for the older reason: they are legal in JSON
    and are line terminators in JavaScript, so an unescaped one is a syntax
    error that only some content can trigger.
    """
    raw = json.dumps(payload, separators=(",", ":"))
    return (
        raw.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def _rail(
    cards: Sequence[ProjectCard],
    org_ref: str,
    *,
    selected_id: Optional[str],
    default_project_id: Optional[str],
    can_set_default: bool = True,
) -> str:
    """The project rail: alias, a star, and a way out to the project page.

    The alias alone. A name and a count on each block would make the rail the
    page's centre of gravity, and it is meant to be the thing you glance at
    before looking at the workflows.

    The star is a real form, so it works with scripting off and the server stays
    the thing that decides -- exactly the shape ``_user_menu``'s default-org star
    already has. The block itself is a ``div`` with ``role="button"``: a form and
    a link cannot legally live inside a ``<button>``.

    ``can_set_default`` is False for a viewer with **no membership row in this
    org** -- a platform member, who may open every org but holds a membership in
    none of them. ``default_project_id`` is a column on that row, so there is
    nothing for them to read and nothing the POST could write; it 404s. The star
    is therefore not drawn at all. Drawing it and letting the click fail is
    strictly worse than omitting it, because the script moves the highlight
    optimistically: the star visibly changed before the 404 page arrived.
    """
    action = f"{UI_PREFIX}/{org_ref.lower()}/default-project"
    blocks = []
    for card in cards:
        is_default = can_set_default and card.id == default_project_id
        active = " is-active" if card.id == selected_id else ""
        star_title = (
            "Your default project" if is_default else "Open this project by default"
        )
        star = (
            (
                f'<form method="post" action="{esc(action)}" class="starform">'
                f'<input type="hidden" name="project_id" value="{esc(card.id)}"/>'
                f'<button class="star{" is-default" if is_default else ""}" type="submit" '
                f'title="{esc(star_title)}" '
                f'aria-label="{esc(star_title)}: {esc(card.alias)}">'
                f"{'&#9733;' if is_default else '&#9734;'}</button></form>"
            )
            if can_set_default
            else ""
        )
        blocks.append(
            f'<div class="block{active}" data-project="{esc(card.id)}" '
            f'data-alias="{esc(card.alias)}" role="button" tabindex="0" '
            f'aria-pressed="{"true" if active else "false"}" '
            f'title="{esc(card.name)}">'
            f'<span class="alias">{esc(card.alias)}</span>'
            f'<span class="foot">{star}'
            f'<a class="out" href="{esc(project_path(org_ref, card.alias))}" '
            f'title="Go to the {esc(card.alias)} project page" '
            f'aria-label="Go to the {esc(card.alias)} project page">&#8599;</a>'
            "</span></div>"
        )
    return f'<div class="rail" id="wfrail">{"".join(blocks)}</div>'


def _grid(catalogue: Sequence[Dict[str, object]]) -> str:
    """The four pillars and their workflows, as buttons the runner picks up.

    Each button carries an **empty** tick slot. The daily workflows' ticks depend on
    the project in the rail, which changes in the browser with no round trip, so
    the mark and its hover text are painted by the engine from the per-project
    payload -- see `_ticks`. Rendering them here would freeze both to whichever
    project the page was loaded with.
    """
    columns = []
    for pillar in PILLARS:
        buttons = "".join(
            f'<button class="wf" type="button" data-w="{esc(entry["id"])}">'
            f"{esc(entry['title'])}"
            f'<i class="wtick" data-tick hidden aria-hidden="true">&#10003;</i>'
            f"</button>"
            for entry in catalogue
            if entry["pillar"] == pillar
        )
        columns.append(
            f'<div class="pillar"><span class="wname">{esc(pillar)}</span>{buttons}</div>'
        )
    return f'<div class="grid" id="wfgrid">{"".join(columns)}</div>'


def workflow_page(
    *,
    user: User,
    org: Organization,
    orgs: List[Organization],
    cards: Sequence[ProjectCard],
    panels: Optional[Dict[str, object]] = None,
    tickets: Optional[Dict[str, List[ProjectTicketRow]]] = None,
    unreleased: Optional[Dict[str, List[ProjectTicketRow]]] = None,
    unreleased_totals: Optional[Dict[str, int]] = None,
    reopen: Optional[Dict[str, List[ProjectTicketRow]]] = None,
    unowned: Optional[Dict[str, List[ProjectTicketRow]]] = None,
    scrum_activity: Optional[Dict[str, ScrumActivity]] = None,
    default_project_id: Optional[str] = None,
    can_set_default: bool = True,
    scrums_url: Optional[str] = None,
    selected_project_id: Optional[str] = None,
    notice: Optional[tuple] = None,
    now: Optional[datetime] = None,
) -> str:
    """The workflow launcher for one organization.

    Every ``Dict`` argument is **keyed by project id and already batched** --
    one read of each table for the whole page, never one per project and never
    one per step. That is the rule ``_render_dashboard`` states, and it matters
    more here than there: the page carries the data for every project at once,
    because switching projects in the rail must not cost a round trip.

    ``panels`` maps project id to ``data.SummaryPanel``; ``tickets`` to the
    project's live tickets in ``STATUS_ORDER``; ``unreleased`` to its finished
    tickets carrying no release. All three are optional and an absent key means
    "not read", which the steps render as a placeholder rather than as an empty
    result -- the same distinction ``dashboard_page`` draws for ``panels``.

    ``unreleased_totals`` is how many of those finished tickets each project
    actually has. It is separate because ``unreleased`` is *capped*
    (`done_unreleased_for` stops at 60 per project) and the page states a count
    in words: without the total it printed the size of the page it was handed as
    though it were the whole board.

    ``reopen`` is each project's finished work belonging to the *viewer* inside
    `REOPEN_WINDOW_DAYS` (`data.my_done_recently_for`), and ``unowned`` its queued
    work belonging to nobody (`data.unowned_todo_for`). Both feed the personal
    update's two pickers and nothing else.

    ``scrum_activity`` is what has already been recorded today, per project
    (`data.scrum_activity_today`): whether this viewer submitted, whether anybody
    ran the stand-up, and the row to resume. It is what the two daily ticks are
    painted from -- one query answering both, so the ticks cannot disagree with
    each other or with the record they describe.

    ``scrums_url`` is where the scrum walk posts what it records. Absent, the
    walk still runs and still keeps time, but nothing is written and the page
    says so -- it never claims a record it did not make.
    """
    now = now or datetime.now(timezone.utc)
    org_ref = org.alias or org.id
    panels = panels or {}
    tickets = tickets or {}
    unreleased = unreleased or {}
    unreleased_totals = unreleased_totals or {}
    reopen = reopen or {}
    unowned = unowned or {}
    scrum_activity = scrum_activity or {}

    notice_html = ""
    if notice:
        message, ok = notice
        notice_html = (
            f'<div class="syncnote {"ok" if ok else "err"}">{esc(message)}</div>'
        )

    if not cards:
        empty_pane = f"""
  <div class="railhead"><span class="lbl">Working in</span></div>
  <div class="empty">No projects in this organization yet. Workflows run against
  a project, so the first move is to
  {_link(new_project_path(org_ref), "create one")}.</div>"""
        body = f"""
<style>{_WORKFLOW_CSS}</style>
<header class="topbar">{_wordmark()}{_user_menu(user, org, orgs)}</header>
<main class="wfpage">
  {notice_html}
  {_shell(_app_nav(org, active="workflow"), empty_pane)}
</main>"""
        return _page(f"Workflows · {org.name} · innoday", body)

    known = {card.id for card in cards}
    selected = selected_project_id if selected_project_id in known else None
    if selected is None:
        selected = default_project_id if default_project_id in known else cards[0].id

    catalogue = _workflow_catalogue(org_ref)

    projects: Dict[str, object] = {}
    for card in cards:
        rows = tickets.get(card.id, [])
        loose = unreleased.get(card.id, [])
        activity = scrum_activity.get(card.id)
        back, take = _with_resumed_picks(
            reopen.get(card.id, []), unowned.get(card.id, []), activity
        )
        bodies, ctas = _project_steps(
            card,
            org_ref,
            panel=panels.get(card.id),
            tickets=rows,
            unreleased=loose,
            unreleased_total=unreleased_totals.get(card.id),
            reopen=back,
            take=take,
            activity=activity,
            now=now,
        )
        projects[card.id] = {
            "alias": card.alias,
            # Per project, not per page: the rail switches project in the browser
            # with no round trip, so both of these have to be here for every
            # project the page carries.
            "ticks": _ticks(activity),
            "update": _update_payload(back, take, activity),
            # Sent as well as rendered: the wrap-up step shows this number and
            # the finish write stores it, and deriving it twice is how the two
            # start disagreeing.
            "lingering": _lingering_count(rows, now=now),
            "bodies": bodies,
            "ctas": ctas,
            "walk": _walk_payload(rows, panel=panels.get(card.id), now=now),
            "pull": _pull_markup(rows),
        }

    blob = _json_blob(
        {
            "selected": selected,
            "lingerDays": LINGER_DAYS,
            # Where the walk posts what it records. A path this module built, so
            # it carries nothing a person typed -- but it still goes through the
            # blob's escaping like every other value, because the rule that
            # keeps this page safe is "everything", not "everything untrusted".
            "scrumsUrl": scrums_url or "",
            "workflows": catalogue,
            "projects": projects,
        }
    )

    pane = f"""
  <div class="viewport" id="wfvp">
    <div class="railhead">
      <span class="lbl">Working in</span>
      <span class="hint" id="wfhint">{
        "&#9733; opens by default &middot; &#8599; goes to the project page"
        if can_set_default
        else "&#8599; goes to the project page"
    }</span>
    </div>
    {
        _rail(
            cards,
            org_ref,
            selected_id=selected,
            default_project_id=default_project_id,
            can_set_default=can_set_default,
        )
    }
    <div class="chooser" id="wfchooser">{_grid(catalogue)}</div>
    <div class="runner" id="wfrunner">
      <div class="wferr" id="wferr" role="alert" hidden></div>
      <div class="runhead">
        <div class="who">
          <span class="pill" id="wfpillar"></span>
          <span class="title" id="wftitle"></span>
        </div>
        <div class="runctl">
          <div class="dots" id="wfdots" role="status"></div>
          <button class="quit" id="wfquit" type="button">Cancel</button>
        </div>
      </div>
      <div class="wstack" id="wfstack"></div>
    </div>
  </div>
  <noscript>
    <div class="note warn">Workflows walk their steps in the browser, so this page
    needs JavaScript. The star and the project links above still work, and every
    project has a full {_link(dashboard_path(org_ref), "dashboard")} without it.</div>
  </noscript>"""

    # Org-level only: no project block, even though a project is selected in the
    # rail. That selection changes in the browser when you click another block,
    # so a server-rendered project section beside it would name the project you
    # arrived with rather than the one you are looking at -- a nav that lies
    # after one click is worse than one that stops at the org.
    body = f"""
<style>{_WORKFLOW_CSS}</style>
<header class="topbar">{_wordmark()}{_user_menu(user, org, orgs)}</header>
<main class="wfpage">
  {notice_html}
  {_shell(_app_nav(org, active="workflow"), pane)}
</main>
<script>window.INNODAY_WORKFLOWS={blob};</script>
<script>{_WORKFLOW_JS}</script>"""
    return _page(f"Workflows · {org.name} · innoday", body)
