"""HTML for the ``/ui`` pages: the sign-in card and the dashboard.

A wide app shell with a top bar, rather than the centred 440px card
``src/routers/_brand_pages.py`` serves the auth pages in -- so the chrome is
separate, but the palette and font stacks are imported from there rather than
re-declared. One source of brand truth; two shells.

Everything is a string. There is no template engine and no build step, because
this whole surface is temporary and will be replaced by a real UI application --
a dependency added here is a dependency to remove later. Every interpolated
value goes through ``esc``; the only exception is markup this module authored
itself (the glyphs in ``icons``).

Almost no JavaScript. The org switcher and the layer picker are ``<details>``
elements, so they work with a click or the keyboard and need no script.

The single exception is the copy-to-clipboard button, which has no HTML
equivalent -- ``navigator.clipboard`` is the only way. It is written as
progressive enhancement: the command is plain selectable text, the button is
added on top, and with scripting off the page loses a convenience rather than a
capability.
"""

from datetime import datetime, timezone
from html import escape
from typing import Dict, List, Optional
from urllib.parse import quote

from src.domain.organization import Organization
from src.domain.ticket import TicketStatus
from src.domain.user import User
from src.page_paths import (
    JOIN_PATH,
    LOGIN_PATH,
    LOGOUT_PATH,
    UI_PREFIX,
    dashboard_path,
    new_project_path,
    profile_path,
    project_path,
    team_path,
    workflow_path,
)
from src.routers._brand_pages import (
    BRAND_FONTS,
    BRAND_TOKENS,
    favicon_link,
    strip_authoring_comments,
)
from src.routers.webui import data, icons
from src.routers.webui.data import ProjectCard
from src.services import summary_line
from src.utils.time_windows import format_note_date, format_target_date
from src.utils.urls import safe_url

EM_DASH = "—"
CHEVRON = "»"


def esc(value: Optional[object]) -> str:
    """HTML-escape any value, including quotes, so it is safe in an attribute."""
    return escape(str(value if value is not None else ""), quote=True)


#: ``safe_url`` is imported above rather than defined here, and every caller in
#: this package still reads it from this module. It moved to
#: ``src/utils/urls.py`` because the identical rule has to run on **write** as
#: well as on render -- see that module -- and a service reaching into this
#: 4,000-line page renderer for it would have pointed the layers the wrong way.


def relative_time(value: Optional[datetime], *, now: Optional[datetime] = None) -> str:
    """A short human gap: ``4 min ago``, ``2 hr ago``, ``31 days ago``.

    Coarse on purpose -- the question is "is this stale?", not "exactly when?".
    The precise UTC timestamp goes in the element's ``title`` alongside it.
    """
    if value is None:
        return "never synced"
    now = now or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    seconds = (now - value).total_seconds()
    if seconds < 0:
        return "just now"
    if seconds < 90:
        return "just now"
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)} min ago"
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)} hr ago"
    days = int(hours / 24)
    return "1 day ago" if days == 1 else f"{days} days ago"


def _freshness(value: Optional[datetime], *, now: Optional[datetime] = None) -> str:
    """``fresh`` / ``warm`` / ``cold``, driving the dot colour beside a sync time.

    Encoding staleness in form as well as in words means a stale project is
    visible while scanning, without reading every row.
    """
    if value is None:
        return "cold"
    now = now or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    hours = (now - value).total_seconds() / 3600
    if hours < 1:
        return "fresh"
    if hours < 24:
        return "warm"
    return "cold"


def _iso(value: Optional[datetime]) -> str:
    if value is None:
        return "never synced"
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.strftime("%Y-%m-%d %H:%M UTC")


_APP_CSS_SOURCE = (
    "\n  :root { "
    + BRAND_TOKENS
    + " "
    + BRAND_FONTS
    + " }"
    + """
  * { box-sizing:border-box; }
  /* **Form controls do not inherit `font-family`** -- browsers give them a
     platform default, so every `<button>` on this app rendered in Arial or
     Helvetica beside Inter text. It showed up worst on the two create-project
     controls: the dashboard's `+ New project` is an `<a>` and inherited
     correctly, while the form's `Create project` is a `<button>` and did not, so
     the same button in the same style read in two different faces one click
     apart. Set here rather than on each class, because the next control added
     would have the same bug and no reason to suspect it. */
  button, input, select, textarea, optgroup { font-family:inherit; }
  body { margin:0; min-height:100vh; color:#fff; font-family:var(--font-ui);
         -webkit-font-smoothing:antialiased;
         background:radial-gradient(900px 420px at 15% -12%, rgba(241,91,53,.13), transparent 60%),
                    linear-gradient(160deg, var(--bg) 0%, var(--bg2) 52%, var(--bg) 100%);
         background-attachment:fixed; }
  a { color:inherit; text-decoration:none; }
  :focus-visible { outline:2px solid var(--orange); outline-offset:2px; border-radius:6px; }

  /* Status colours, named once. Every place a status is shown -- a ticket chip,
     a release pill, a count on a project card -- reads them from here, because a
     colour that means "moving" on one panel and "waiting" on another is worse
     than no colour at all.

     Green is *in progress*, not done: the page is about work in flight, and the
     state a reader scans for is the one being worked on right now. Done and
     released are deliberately the quietest of the four -- they need no attention,
     and they are also the largest numbers on most projects, so a loud colour
     would put all the visual weight on the finished half of the board. These two
     were both green before, which made "shipped" and "under way" the same colour
     on the same card. Amber is what is waiting on somebody. */
  :root { --s-plan:#fbbf24; --s-live:#4ade80; --s-rev:#a78bfa; --s-done:#8b9cb3; }

  .topbar { display:flex; align-items:center; justify-content:space-between; gap:16px;
            padding:16px 24px; border-bottom:1px solid rgba(255,255,255,.10);
            background:rgba(10,10,10,.62); position:relative; flex-wrap:wrap; }
  .topbar::after { content:""; position:absolute; left:0; right:0; bottom:-1px; height:1px;
                   background:linear-gradient(90deg,var(--orange),var(--amber) 32%,transparent 72%); }
  .mark { display:flex; align-items:center; gap:11px; }
  .mark .div { width:1px; height:18px; background:rgba(255,255,255,.14); }
  .mark .rocket { display:flex; align-items:center; gap:7px; }
  .mark .name { font-size:15px; font-weight:800; letter-spacing:-.02em;
                background:linear-gradient(93deg,var(--orange),var(--amber));
                -webkit-background-clip:text; background-clip:text; color:transparent; }

  details.usermenu { position:relative; }
  details.usermenu > summary { list-style:none; cursor:pointer; display:flex; align-items:center; gap:11px;
            border:1px solid rgba(255,255,255,.10); border-radius:10px; padding:7px 12px;
            background:rgba(255,255,255,.04); }
  details.usermenu > summary::-webkit-details-marker { display:none; }
  .avatar { width:30px; height:30px; border-radius:7px; flex:none; display:grid; place-items:center;
            font-size:12px; font-weight:800; color:#1a1a2e;
            background:linear-gradient(135deg,var(--orange),var(--amber)); }
  .who { display:flex; flex-direction:column; line-height:1.28; text-align:left; }
  .who b { font-size:12.5px; font-weight:600; }
  .who em { font-style:normal; font-size:11px; color:var(--muted); }
  .chev { color:var(--orange); font-weight:800; }
  .dropdown { position:absolute; right:0; top:calc(100% + 9px); width:262px; z-index:5;
              background:#12121c; border:1px solid rgba(255,255,255,.10); border-radius:12px;
              box-shadow:0 20px 48px rgba(0,0,0,.6); overflow:hidden; padding-bottom:6px; }
  .dd-label { font-size:10px; letter-spacing:.13em; text-transform:uppercase; font-weight:700;
              color:#6b7280; padding:11px 14px 6px; }
  .dd-row { display:flex; align-items:center; gap:4px; padding:0 8px 0 0; font-size:13px; }
  .dd-row:hover { background:rgba(255,255,255,.05); }
  .dd-orglink { display:flex; align-items:center; gap:10px; padding:9px 14px; flex:1 1 auto; }
  .dd-hint { font-weight:400; letter-spacing:0; text-transform:none; color:#4b5563; }
  .starform { display:flex; flex:none; }
  .star { background:none; border:0; cursor:pointer; font-size:14px; line-height:1;
          padding:5px 6px; border-radius:6px; color:#4b5563; }
  .star:hover { color:var(--amber); background:rgba(255,255,255,.07); }
  .star.is-default { color:var(--amber); }
  .dd-row.on { background:rgba(241,91,53,.11); }
  .dd-row .tick { width:12px; font-size:11px; color:transparent; flex:none; }
  .dd-row.on .tick { color:var(--orange); }
  .dd-sep { height:1px; background:rgba(255,255,255,.10); margin:6px 0; }
  .signout { display:block; width:100%; text-align:left; background:none; border:0; cursor:pointer;
             color:var(--muted); font:inherit; font-size:12.5px; padding:9px 14px; }
  .signout:hover { color:#fff; }
  .dd-cli { display:block; padding:9px 14px; font-size:12.5px; color:var(--muted); }
  .dd-cli:hover { background:rgba(255,255,255,.05); color:#fff; }
  .dd-cli b { color:var(--amber); font-weight:600; font-family:var(--font-type); }
  .dd-cli-sub { display:block; font-size:11px; color:#4b5563; margin-top:2px; }

  main { max-width:1140px; margin:0 auto; padding:28px 24px 64px;
         display:flex; flex-direction:column; gap:26px; }
  /* The section label and the one action that belongs to it, on one line. */
  .lblrow { display:flex; align-items:center; gap:12px; }
  .newproj { flex:none; font-size:12px; font-weight:600; color:#14121a;
             border-radius:8px; padding:6px 12px;
             background:linear-gradient(135deg,var(--orange),#ff8a5c); }
  .newproj:hover { filter:brightness(1.08); }
  .seclabel { font-size:10.5px; letter-spacing:.15em; text-transform:uppercase;
              color:#6b7280; font-weight:700; }

  /* No overflow:hidden -- it clipped the layer dropdown, so the last repo's menu
     opened into the card edge and could not be reached. The radius is preserved
     by the children that touch the corners setting their own, below. */
  .proj { border:1px solid rgba(255,255,255,.10); border-radius:18px; position:relative;
          background:linear-gradient(150deg, rgba(15,23,42,.88), rgba(30,41,59,.62)); }
  .proj-head { border-radius:18px 18px 0 0; }
  .proj-body { border-radius:0 0 18px 18px; }
  .proj .pixel { position:absolute; width:6px; height:6px; background:rgba(255,255,255,.09);
                 top:18px; right:16px; }
  .proj .pixel.b { top:30px; right:28px; width:4px; height:4px; }
  .proj-head { display:flex; align-items:center; gap:13px; flex-wrap:wrap;
               padding:17px 20px; border-bottom:1px solid rgba(255,255,255,.10); }
  .alias { font-family:var(--font-type); font-size:12.5px; font-weight:700; letter-spacing:.07em;
           padding:4px 9px; border-radius:6px; color:#14121a; flex:none;
           background:linear-gradient(135deg,var(--orange),#ff8a5c); }
  .proj-name { font-size:15.5px; font-weight:650; letter-spacing:-.01em; }
  /* The alias and name together are one target. Padding is negative-margined
     back out so adding the link does not shift the header's layout by a pixel. */
  .projlink { display:flex; align-items:center; gap:13px; border-radius:9px;
              padding:2px 4px; margin:-2px -4px; }
  .projlink:hover { background:rgba(255,255,255,.05); }
  .projlink:hover .proj-name { color:var(--amber); }
  .grow { flex:1 1 auto; }
  /* The project bar: the same alias chip and name as the card, sitting above the
     whole shell so it survives a tab change. */
  .projbar { display:flex; align-items:center; gap:13px; flex-wrap:wrap;
             margin:0 0 13px; }
  /* The sync pill *is* the sync control: one target, and the freshness it reports
     is the reason you would press it. A separate dot restated the colour the pill
     already carries. */
  .sync { display:inline-flex; align-items:center; gap:7px; flex:none; cursor:pointer;
          font:inherit; font-size:11.5px; font-variant-numeric:tabular-nums;
          border:1px solid rgba(255,255,255,.10); border-radius:999px; padding:4px 11px;
          background:rgba(255,255,255,.03); color:var(--muted); }
  .sync:hover { background:rgba(255,255,255,.08); color:#fff; }
  .sync svg { flex:none; transition:transform .3s ease; }
  .sync:active svg { transform:rotate(180deg); }
  .sync.fresh { color:#4ade80; border-color:rgba(74,222,128,.28); }
  .sync.warm { color:var(--amber); border-color:rgba(251,191,36,.28); }
  .sync.cold { color:#6b7280; }

  /* What this project is wired to, immediately left of the sync pill. Same two
     colours the pill already uses -- #4ade80 for connected and #6b7280 for not
     -- so the header reads as one system rather than two vocabularies of green.
     The detail lives in `title`; the icon stays a dot, because three labelled
     chips in a card header is a second row of text nobody asked for. */
  /* Who is on this project, as overlapping initials. Overlapped rather than
     spaced so five people cost the width of about three -- the card header is
     already carrying an alias, a name, a command and four other controls. */
  .bubbles { display:inline-flex; align-items:center; flex:none; padding-left:6px; }
  .bubbles .bub { width:24px; height:24px; border-radius:50%; flex:none;
                  display:grid; place-items:center; font-size:9.5px; font-weight:800;
                  color:#14121a; margin-left:-6px;
                  border:1.5px solid #12121c;
                  background:linear-gradient(135deg,var(--orange),var(--amber)); }
  .bubbles .bub:first-child { margin-left:0; }
  .bubbles .bub.more { background:rgba(255,255,255,.10); color:var(--muted);
                       font-weight:600; }
  .bubbles:hover .bub { border-color:rgba(255,255,255,.28); }
  .bubbles.none { font-size:11px; color:#6b7280; padding:3px 9px; border-radius:999px;
                  border:1px dashed rgba(255,255,255,.14); }
  .bubbles.none:hover { color:#fff; border-color:rgba(255,255,255,.28); }
  .intgs { display:flex; align-items:center; gap:6px; flex:none; }
  .intg { width:26px; height:26px; border-radius:7px; flex:none; display:grid;
          place-items:center; color:#5b6472;
          border:1px solid rgba(255,255,255,.09); background:rgba(255,255,255,.03); }
  .intg svg { display:block; }
  .intg.on { color:#4ade80; border-color:rgba(74,222,128,.30);
             background:rgba(74,222,128,.10); }
  /* Configured, and broken. Louder than green on purpose -- an integration that
     stopped working is the one thing on this row worth interrupting for. */
  .intg.err { color:#f87171; border-color:rgba(248,113,113,.34);
              background:rgba(248,113,113,.11); }

  /* An even split, not 1.72:1. The right-hand column carries the next launch
     *and* the scrum summary now -- ticket titles, owners and PR links -- and at
     the old ratio those wrapped to two and three lines each while the repo list
     ran out of rows and left whitespace. Both halves are lists of the same kind
     of thing; neither has a claim on more room. `minmax(0,...)` on both keeps a
     long unbroken string (a branch name) from forcing the grid wider than the
     card, which is what makes the whole page scroll sideways. */
  /* **One third / two thirds, not half and half.** The right column carries the
     version, the scrum summary and the ticket counts -- prose and titles, which
     need width -- while the left is a list of repository names, which is the
     shortest text on the card. An even split gave the most room to the column
     that needed it least. Collapses to one column under 780px, where a third of
     a phone is not a column at all. */
  .proj-body { display:grid;
               grid-template-columns:minmax(0,1fr) minmax(0,2fr); }
  .repos { padding:16px 20px 18px; display:flex; flex-direction:column; gap:3px; }
  .launch { padding:16px 20px 18px; border-left:1px solid rgba(255,255,255,.10); }
  .repo { display:flex; align-items:center; gap:11px; padding:7px 8px; border-radius:9px; margin:0 -8px; }
  .repo:hover { background:rgba(255,255,255,.035); }
  .tile { width:28px; height:28px; border-radius:7px; flex:none; display:grid; place-items:center;
          background:color-mix(in srgb, var(--h) 15%, transparent);
          border:1px solid color-mix(in srgb, var(--h) 26%, transparent); color:var(--h); }
  .repo-name { font-size:13.2px; font-weight:500; min-width:0; overflow:hidden;
               text-overflow:ellipsis; white-space:nowrap; }
  .layer { font-family:var(--font-type); font-size:10px; letter-spacing:.09em; text-transform:uppercase;
           padding:2px 7px; border-radius:4px; flex:none; color:var(--h);
           background:color-mix(in srgb, var(--h) 13%, transparent); }

  /* The layer chip doubles as its own picker: a <details> holding one submit
     button per layer. No JS, and no separate save step. */
  details.laypick { position:relative; flex:none; }
  details.laypick > summary { list-style:none; cursor:pointer; }
  details.laypick > summary::-webkit-details-marker { display:none; }
  details.laypick > summary:hover { background:color-mix(in srgb, var(--h) 26%, transparent); }
  .lay-menu { position:absolute; right:0; top:calc(100% + 6px); z-index:6; min-width:172px;
              display:flex; flex-direction:column; padding:5px;
              background:#12121c; border:1px solid rgba(255,255,255,.12); border-radius:11px;
              box-shadow:0 18px 40px rgba(0,0,0,.62); }
  /* The last row opens upward: there is no card left below it to grow into, and
     a menu that renders off the bottom is one you cannot pick from. */
  .repo:last-child .lay-menu { top:auto; bottom:calc(100% + 6px); }
  .lay-opt { display:flex; align-items:center; gap:9px; width:100%; text-align:left; cursor:pointer;
             background:none; border:0; border-radius:7px; padding:7px 10px;
             font:inherit; font-size:12.5px; color:var(--muted); }
  .lay-opt:hover { background:rgba(255,255,255,.06); color:#fff; }
  .lay-opt.on { color:#fff; background:color-mix(in srgb, var(--h) 15%, transparent); }
  .lay-dot { width:8px; height:8px; border-radius:2px; flex:none; background:var(--h); }

  .prs { font-size:11px; flex:none; font-variant-numeric:tabular-nums;
         padding:2px 8px; border-radius:999px; min-width:52px; text-align:center; }
  .prs.open { color:var(--amber); background:rgba(251,191,36,.13); }
  .prs.zero { color:#6b7280; }
  .prs.none { background:none; }
  /* A count that has stopped being current still reads, but stops asserting: the
     dotted underline is the same "unverified" convention as an abbreviation, and
     it survives the two colours above rather than replacing either -- an amber
     `3 PRs` going grey would read as "none open", which is the confusion this
     mark exists to remove (#650). */
  .prs.stale { text-decoration:underline dotted rgba(255,255,255,.34);
               text-underline-offset:3px; }
  /* ---------- one project: menu + pane ---------- */
  /* `auto` on the first track is what makes the menu collapsible without a
     second width to maintain: a shut <details> is as wide as its toggle, and
     the grid follows. No JS, and nothing to keep in step. */
  /* `stretch`, not `start`: the menu is a full-length rail down the side of the
     pane, so it needs the row's height to stretch into. */
  .shell { display:grid; grid-template-columns:auto minmax(0,1fr); gap:18px;
           align-items:stretch; }
  /* A rail, not a bubble. It runs the full length of the pane and is bounded by
     one edge rather than four, so it reads as the side of the page rather than a
     card that happens to contain links.
     **That one edge is the whole rail.** The menu carried a vertical gradient
     fill as well, which made it a panel beside the pane rather than an edge of
     it -- so the only structure left here is the border, and the pane's own
     background runs behind the links. */
  .navwrap { align-self:stretch; display:flex; flex-direction:column; gap:0;
             border-right:1px solid rgba(255,255,255,.10);
             overflow:hidden; }
  .navwrap > summary { list-style:none; cursor:pointer; height:38px; flex:none;
            display:flex; align-items:center; gap:9px; padding:0 12px;
            color:#6b7280; font-size:10.5px; font-weight:700; letter-spacing:.14em;
            text-transform:uppercase; }
  .navwrap > summary::-webkit-details-marker { display:none; }
  /* Hover brightens the type. No fill: the menu has no background of its own to
     lighten, and a lit rectangle over the pane reads as a separate surface. */
  .navwrap > summary:hover { color:#fff; }
  .navwrap > summary svg { flex:none; }
  /* Open, the toggle is a labelled header; shut, it is just the icon -- so the
     collapsed rail is 38px wide instead of a header with nothing under it. */
  .navwrap[open] > summary { border-bottom:1px solid rgba(255,255,255,.08); }
  .navwrap[open] > summary svg:first-of-type { display:none; }
  .navwrap:not([open]) > summary svg:last-of-type { display:none; }
  /* Open, the close glyph sits at the rail's right edge; shut, the hamburger is
     centred in the 38px rail. */
  .navwrap[open] > summary { justify-content:flex-end; }
  .navwrap:not([open]) > summary { justify-content:center; padding:0; width:38px; }

  .nav { display:flex; flex-direction:column; padding:6px; width:186px; }
  /* Rows, not pills: they sit inside a panel now, so a border on each one would
     be a box in a box. The active row is marked with a rail on its leading edge
     -- the same device the topbar's gradient underline uses. */
  .nav a { display:flex; align-items:center; gap:11px; padding:9px 11px;
           border-radius:8px; font-size:13.2px; color:var(--muted);
           border-left:2px solid transparent; }
  .nav a:hover { color:#fff; }
  /* The active row is the leading rail, the white type and the weight -- and
     `aria-current="page"` in the markup. It used to carry a tinted fill too,
     which was the menu's background reappearing one row at a time. Three cues
     survive it, only one of which is colour, so the row is still identifiable
     without one. */
  .nav a.on { color:#fff; border-left-color:var(--orange); font-weight:600; }
  .nav .ic { width:15px; height:15px; flex:none; opacity:.7; }
  .nav a.on .ic, .nav a:hover .ic { opacity:1; }
  .nav .ct { margin-left:auto; font-size:10.5px; font-variant-numeric:tabular-nums;
             color:#6b7280; background:rgba(255,255,255,.06); padding:1px 6px;
             border-radius:999px; }
  .nav a.on .ct { color:var(--amber); background:rgba(251,191,36,.14); }
  .navsep { height:1px; background:rgba(255,255,255,.08); margin:6px 10px; }
  /* The org's name, and the project's alias one level in. Same type as the
     topbar's section labels, because that is what they are: a heading over the
     rows beneath, not a row you can click. Truncated rather than wrapped -- the
     rail is a fixed 186px open, and a three-line org name would push the first
     link below the fold on a short window. */
  .nav .navhead { padding:9px 11px 3px; font-size:10.5px; letter-spacing:.14em;
                  text-transform:uppercase; color:#6b7280; font-weight:700;
                  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  /* The project block, indented under its own heading so the rail reads as two
     levels rather than as seven links in a row. Indent only -- no second border,
     which would sit a pixel from the active row's orange rail and read as one
     smeared line. */
  .nav .navsub { display:flex; flex-direction:column; padding-left:9px; }

  .pane { display:flex; flex-direction:column; gap:14px; min-width:0; }
  .card { border:1px solid rgba(255,255,255,.10); border-radius:16px;
          background:linear-gradient(150deg, rgba(15,23,42,.80), rgba(30,41,59,.55)); }
  .card > header { display:flex; align-items:center; gap:12px; padding:13px 18px;
                   border-bottom:1px solid rgba(255,255,255,.10); }
  .card > header h4 { margin:0; font-size:10.5px; letter-spacing:.15em;
                      text-transform:uppercase; color:#6b7280; font-weight:700; }
  .card .body { padding:15px 18px 17px; display:flex; flex-direction:column; gap:2px; }
  .card .more { font-size:11.5px; color:var(--amber); flex:none; }
  .card .more:hover { text-decoration:underline; }
  .card .src { font-size:11.5px; color:#6b7280; flex:none; }
  /* The scrum panel brings its own heading and padding from the dashboard. */
  .pane-scrum { padding:15px 18px 17px; }

  .duo { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:14px; }
  /* The planning board: two halves. The pool on the left, and the two slots
     stacked on the right in the order work moves through them -- current above
     next. Two columns rather than three because the slots are a *sequence*, not
     three peers: stacking them says "this one, then that one", and it gives both
     the full half-width their ticket titles need.
     `align-items:start` so a long list on one side does not stretch the other
     into matching whitespace. */
  /* `.planboard`, not `.board` -- a `.kindchip.board` already exists below, and
     a bare `.board { display:grid }` would turn those chips into grids. */
  .planboard { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr);
               gap:14px; align-items:start; }
  .planboard .stack { display:flex; flex-direction:column; gap:14px; min-width:0; }
  .slothint { margin:0 0 10px; font-size:11.5px; color:#6b7280; line-height:1.45; }
  /* Work pointing at a version the project does not have. A rule rather than a
     heading -- it is still unplanned work, so it stays in the same card. */
  .staleband { margin-top:10px; padding-top:8px;
               border-top:1px dashed rgba(248,113,113,.34); }
  .orphan { flex:none; font-family:var(--font-type); font-size:10.5px; color:#f87171;
            background:rgba(248,113,113,.11); padding:2px 7px; border-radius:4px; }
  /* One column when there is no room for two. The pool leads, because it is
     where you look first. */
  @media (max-width:900px) {
    .planboard { grid-template-columns:minmax(0,1fr); }
  }

  /* Ticket-list controls. Release chips first (two questions worth one click),
     status boxes under them. */
  .rchips { display:flex; align-items:center; gap:7px; flex-wrap:wrap; margin:0 0 9px; }
  .rchip { font-size:11.5px; padding:3px 10px; border-radius:999px; color:#94a3b8;
           border:1px solid rgba(255,255,255,.10); background:rgba(255,255,255,.03); }
  .rchip b { font-family:var(--font-type); font-weight:600; }
  a.rchip:hover { color:#fff; border-color:rgba(255,255,255,.24); }
  .rchip.on { color:var(--amber); background:rgba(251,191,36,.12);
              border-color:rgba(251,191,36,.34); }
  .filters { display:flex; align-items:center; gap:6px; flex-wrap:wrap;
             margin:0 0 4px; padding-bottom:10px;
             border-bottom:1px solid rgba(255,255,255,.055); }
  .fbox { display:inline-flex; align-items:center; gap:5px; cursor:pointer;
          font-size:11px; letter-spacing:.02em; color:#6b7280; padding:3px 9px 3px 6px;
          border:1px solid rgba(255,255,255,.09); border-radius:999px;
          background:rgba(255,255,255,.02); text-transform:lowercase; }
  .fbox input { position:absolute; opacity:0; width:0; height:0; }
  .fbox .box { width:13px; height:13px; border-radius:3px; flex:none;
               border:1px solid rgba(255,255,255,.18); font-size:9px; color:transparent;
               display:flex; align-items:center; justify-content:center; }
  .fbox.on { color:#d5d8de; border-color:rgba(255,255,255,.20); }
  .fbox.on .box { background:var(--amber); border-color:var(--amber); color:#111; }
  /* Keyboard reachability: the real input is offscreen, so the ring has to be
     drawn on the label instead or focus is invisible. */
  .fbox:focus-within { outline:2px solid rgba(251,191,36,.55); outline-offset:1px; }
  .fapply { font-size:11px; padding:4px 12px; border-radius:999px; cursor:pointer;
            color:#111; background:var(--amber); border:0; font-weight:650;
            margin-left:3px; }
  /* A rule between status groups. The chips already name them, so a heading per
     group would say the same thing twice. */
  .statusgap { height:1px; margin:7px 0; background:rgba(255,255,255,.10); }
  /* A release's tail, disclosed. The chevron turns; the summary counts what is
     hidden, so a shut list never reads as the whole list. */
  .slotrest > summary { list-style:none; cursor:pointer; display:flex; align-items:center;
                        gap:7px; padding:7px 0 2px; font-size:11.5px; color:#6b7280; }
  .slotrest > summary::-webkit-details-marker { display:none; }
  .slotrest > summary:hover { color:var(--amber); }
  .slotrest .chev { display:flex; transition:transform .12s ease; }
  .slotrest[open] > summary .chev { transform:rotate(90deg); }
  .slotmore { display:inline-block; margin-top:8px; font-size:11.5px; }
  /* The unassigned pool is a plain list, not a card: it is the source you drag
     from, and a panel around it made it look like a third destination. */
  .pool { min-width:0; }
  .pool > header { display:flex; align-items:baseline; gap:10px; padding:0 0 8px;
                   border-bottom:1px solid rgba(255,255,255,.07); margin-bottom:4px; }
  /* `flex:none` and `nowrap`: uppercase with .15em tracking is wide, and in the
     narrow left half of the planning board "Unassigned" wrapped onto a second
     line -- a two-line heading over a one-line list. The count beside it is what
     should give way, not the word. */
  .pool > header h4 { margin:0; font-size:10.5px; letter-spacing:.15em;
                      text-transform:uppercase; color:#6b7280; font-weight:700;
                      flex:none; white-space:nowrap; }
  /* Finished work with no release. Separated by a rule and labelled, because a
     DONE row in a planning pool reads as a fault until you know why it is there.
     The heading is an `h5` -- the card's `h4` still covers the whole pool. */
  .doneband { margin-top:14px; padding-top:4px;
              border-top:1px solid rgba(255,255,255,.10); }
  .bandhead { display:flex; align-items:baseline; gap:10px; padding:6px 0 2px; }
  .bandhead h5 { margin:0; font-size:10.5px; letter-spacing:.13em;
                 text-transform:uppercase; color:#6b7280; font-weight:700;
                 flex:none; white-space:nowrap; }

  .undoq { display:inline; margin-left:10px; }
  .undoq button { cursor:pointer; font-size:11.5px; padding:2px 10px; border-radius:999px;
                  color:inherit; background:rgba(255,255,255,.10);
                  border:1px solid rgba(255,255,255,.22); font-weight:600; }
  .undoq button:hover { background:rgba(255,255,255,.18); }
  .relpill { flex:none; font-family:var(--font-type); font-size:10.5px; color:#7c8493;
             background:rgba(255,255,255,.055); padding:2px 7px; border-radius:4px; }
  /* The plan control appears on hover -- and on focus, or it would be
     unreachable without a mouse.
     **Both row classes.** This keyed on `.trow` alone, and the rows the control
     actually lives on are `.brow` (the unassigned pool), so the buttons rendered
     at zero width and were invisible on the one surface they exist for. */
  .planq { flex:none; display:flex; overflow:hidden; max-width:0; opacity:0;
           transition:max-width .16s ease, opacity .14s ease; }
  .brow:hover .planq, .trow:hover .planq, .planq:focus-within {
      max-width:120px; opacity:1; }
  /* The row lifts slightly under the cursor, so it reads as a thing you can act
     on rather than a line of text that happens to have a button. */
  .brow { border-radius:6px; transition:background .14s ease; }
  .brow:hover { background:rgba(255,255,255,.035); }
  .planq button { display:flex; align-items:center; cursor:pointer; padding:2px 5px;
                  border-radius:5px; color:#94a3b8; background:rgba(255,255,255,.05);
                  border:1px solid rgba(255,255,255,.10); }
  .planq button:hover { color:var(--amber); border-color:rgba(251,191,36,.40);
                        background:rgba(251,191,36,.12); }
  .planq button { gap:4px; }
  .ptag { font-size:9.5px; letter-spacing:.06em; text-transform:uppercase;
          font-weight:700; }

  .trow { display:flex; align-items:center; gap:11px; font-size:12.7px; padding:9px 0;
          border-top:1px solid rgba(255,255,255,.055); }
  .trow:first-child { border-top:0; }
  .stxt { color:#d5d8de; min-width:0; overflow:hidden; text-overflow:ellipsis;
          white-space:nowrap; }
  .age { flex:none; font-size:11px; color:#6b7280; font-variant-numeric:tabular-nums; }
  .rname { flex:none; font-family:var(--font-type); font-size:10.5px; color:#7c8493;
           background:rgba(255,255,255,.045); padding:2px 7px; border-radius:4px; }
  .pnum { flex:none; font-family:var(--font-type); font-size:11px; color:#60a5fa;
          display:inline-flex; align-items:center; gap:4px; }
  .pnum .ext { flex:none; opacity:.5; }
  .pnum:hover .ext { opacity:1; }
  .st { flex:none; font-size:9.5px; letter-spacing:.08em; text-transform:uppercase;
        font-weight:700; padding:2px 7px; border-radius:4px; }
  .st.prog { color:var(--s-live); background:rgba(74,222,128,.13); }
  .st.rev  { color:var(--s-rev); background:rgba(167,139,250,.14); }
  .st.todo { color:var(--s-plan); background:rgba(251,191,36,.12); }
  .st.done { color:var(--s-done); background:rgba(139,156,179,.14); }

  /* Releases tab. `.brow` is `.trow` without the status chip's breathing room --
     these lists are titles, so they sit tighter. */
  .brow { display:flex; align-items:center; gap:11px; font-size:12.7px; padding:6px 0;
          border-top:1px solid rgba(255,255,255,.055); }
  .brow:first-child { border-top:0; }
  /* Dragging. The row fades while it is in flight and the slot under the cursor
     lights up, so the gesture has somewhere obvious to land. */
  .brow[draggable="true"] { cursor:grab; }
  .brow.dragging { opacity:.4; cursor:grabbing; }
  .slot.dropok { border-color:rgba(251,191,36,.65);
                 box-shadow:0 0 0 2px rgba(251,191,36,.22) inset; }

  /* Slots are drop targets, so they answer the cursor: a target that does not
     respond does not read as one. Border and lift only -- moving the card would
     shift the rows underneath mid-reach. */
  .slot { transition:border-color .16s ease, box-shadow .16s ease,
                     background .16s ease; }
  .slot:hover { border-color:rgba(251,191,36,.30);
                box-shadow:0 0 0 1px rgba(251,191,36,.10),
                           0 8px 22px -18px rgba(0,0,0,.7); }
  @media (prefers-reduced-motion: reduce) {
    .slot, .brow, .planq { transition:none; }
  }
  .relnext { display:flex; align-items:baseline; gap:11px; margin-bottom:4px;
             flex-wrap:wrap; }
  .relnext .ver { margin-bottom:0; font-size:21px; }

  /* The version's own face and size, one weight down: a target date is a peer of
     the version, not a note about it. `.ver` is 21px on the slot cards, so this
     tracks it rather than declaring a size of its own. */
  .tdate { flex:none; font-family:var(--font-type); font-size:inherit;
           color:#cbd2dc; letter-spacing:.02em; font-weight:500; }
  .launch .tdate { display:block; margin-top:7px; }

  /* The picker. One row, wrapping on a narrow slot -- the label and the field
     must not separate, since the field alone is an unexplained date box. */
  .dateq { display:flex; align-items:center; gap:9px; flex-wrap:wrap;
           margin:11px 0 0; }
  .dateq label { display:inline-flex; align-items:center; gap:8px; font-size:11px;
                 letter-spacing:.09em; text-transform:uppercase; color:#8b95a5; }
  /* Safari renders the native indicator dark-on-dark; the filter is the only way
     to reach it, and it is a no-op where the control is already legible. */
  .dateq input[type=date]::-webkit-calendar-picker-indicator { filter:invert(.75); }
  .rel { border-top:1px solid rgba(255,255,255,.055); }
  .rel:first-child { border-top:0; }
  .rel > summary, .rel > .relhead { display:flex; align-items:baseline; gap:11px;
                                    padding:8px 0; font-size:12.7px; }
  .rel > summary { cursor:pointer; list-style:none; }
  /* The disclosure triangle is replaced by the row itself being the control.
     Both rules are needed: WebKit uses the pseudo-element, everyone else `list-style`. */
  .rel > summary::-webkit-details-marker { display:none; }
  .rel > summary:hover .rver { color:var(--amber); }
  .rel .rver { font-family:var(--font-type); font-size:12.5px; color:#e6e8ec; flex:none; }
  .rel .rmeta { flex:none; font-size:11px; color:#6b7280; font-variant-numeric:tabular-nums; }
  .rsum { margin:2px 0 12px; font-size:12.3px; color:var(--muted); line-height:1.6;
          white-space:pre-wrap; }

  /* Moving the pipeline onto another version line. The parts are a toggle, so
     the current one is a flat marker rather than a disabled-looking control. */
  .bumps { display:flex; align-items:center; gap:7px; margin:2px 0 10px; flex-wrap:wrap; }
  .bumplbl { font-size:10.5px; letter-spacing:.12em; text-transform:uppercase;
             color:#6b7280; font-weight:700; margin-right:2px; }
  .bump { font-size:11px; padding:2px 9px; border-radius:999px; color:#94a3b8;
          border:1px solid rgba(255,255,255,.10); background:rgba(255,255,255,.03); }
  a.bump:hover { color:var(--amber); border-color:rgba(251,191,36,.34); }
  .bump.on { color:var(--amber); background:rgba(251,191,36,.13);
             border-color:rgba(251,191,36,.34); font-weight:600; }
  .bumpc { margin:2px 0 12px; padding:12px 14px; border-radius:10px;
           border:1px solid rgba(251,191,36,.30); background:rgba(251,191,36,.07);
           display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
  .bumpq { margin:0; flex:1 1 260px; font-size:12.5px; color:#d5d8de; line-height:1.55; }
  .pv { font-family:var(--font-type); color:#e6e8ec; }

  .tl { display:flex; align-items:baseline; gap:12px; font-size:12.5px; padding:6px 0;
        border-top:1px solid rgba(255,255,255,.055); }
  .tl:first-child { border-top:0; }
  .tl .ago { font-size:10.5px; color:#6b7280; flex:none; width:52px; text-align:right;
             font-variant-numeric:tabular-nums; }
  /* The dot is the event kind. Colour only -- the title says what happened, so
     this is a scanning aid, never the sole carrier of the meaning. */
  .tl .dot { width:7px; height:7px; border-radius:2px; flex:none; background:#6b7280; }
  .tl .dot.release, .tl .dot.release_created, .tl .dot.release_updated { background:#4ade80; }
  .tl .dot.ticket_sync, .tl .dot.board_attached { background:var(--amber); }
  .tl .dot.repo_added, .tl .dot.repo_removed { background:#60a5fa; }
  .tl .ev { color:#d5d8de; min-width:0; }

  /* ---------- team ---------- */
  .mrow { display:flex; align-items:center; gap:11px; padding:9px 0;
          border-top:1px solid rgba(255,255,255,.055); }
  .mrow:first-child { border-top:0; }
  .mrow .bub { width:28px; height:28px; border-radius:50%; flex:none; display:grid;
               place-items:center; font-size:10.5px; font-weight:800; color:#14121a;
               background:linear-gradient(135deg,var(--orange),var(--amber)); }
  .mname { display:flex; flex-direction:column; line-height:1.3; min-width:0;
           font-size:13px; }
  .mname small { font-size:11px; color:#6b7280; }
  .youtag { font-size:9.5px; letter-spacing:.08em; text-transform:uppercase;
            color:var(--amber); background:rgba(251,191,36,.14); border-radius:4px;
            padding:1px 5px; margin-left:7px; font-weight:700; }
  .handles { display:flex; gap:5px; flex-wrap:wrap; }
  .hchip { font-family:var(--font-type); font-size:10.5px; color:var(--amber);
           background:rgba(251,191,36,.12); border-radius:5px; padding:2px 7px; }
  .hchip.gh { color:#d5d8de; background:rgba(255,255,255,.07); }
  .kindchip { font-size:9.5px; letter-spacing:.08em; text-transform:uppercase;
              font-weight:700; border-radius:4px; padding:2px 7px; flex:none; }
  .kindchip.board { color:#a78bfa; background:rgba(167,139,250,.14); }
  .kindchip.commit { color:#60a5fa; background:rgba(96,165,250,.14); }
  .rolechip { font-size:10px; letter-spacing:.08em; text-transform:uppercase;
              font-weight:700; border-radius:999px; padding:3px 9px; flex:none;
              color:#6b7280; background:rgba(255,255,255,.06); }
  .rolechip.admin { color:var(--orange); background:rgba(241,91,53,.14); }
  .rolechip.developer { color:#4ade80; background:rgba(74,222,128,.13); }
  .rolechip.locked { opacity:.75; cursor:not-allowed; }
  details.rolepick > summary { cursor:pointer; }
  .rolepick .lay-menu { min-width:280px; }
  .rm { background:none; border:0; cursor:pointer; color:#6b7280; font-size:16px;
        line-height:1; padding:2px 6px; border-radius:6px; flex:none; }
  .rm:hover { color:#f87171; background:rgba(248,113,113,.12); }
  .inlineform, .mapform { display:flex; align-items:center; gap:7px; flex:none; }
  .inviterow { display:flex; align-items:center; gap:9px; padding:13px 18px;
               border-top:1px solid rgba(255,255,255,.10); }
  .inp.mini { flex:0 0 auto; font-size:12px; padding:6px 9px; }
  .fine.quiet { font-size:11.5px; color:#6b7280; margin:0; }
  /* ---------- new project form ---------- */
  .frow { display:grid; grid-template-columns:150px minmax(0,1fr); gap:16px;
          align-items:start; padding:14px 20px;
          border-top:1px solid rgba(255,255,255,.06); }
  .frow:first-child { border-top:0; }
  .frow > label { font-size:12.5px; color:var(--muted); padding-top:8px; }
  .frow > label b { display:block; color:#fff; font-weight:600; font-size:12.8px; }
  .frow > label span { font-size:11.5px; color:#6b7280; line-height:1.45;
                       display:block; margin-top:3px; }
  .fld { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
  .fld.col { flex-direction:column; align-items:stretch; gap:8px; }
  .inp { flex:1 1 auto; min-width:0; font:inherit; font-size:13px; color:#fff;
         border:1px solid rgba(255,255,255,.10); border-radius:9px; padding:8px 12px;
         background:rgba(0,0,0,.34); }
  .inp.mono { font-family:var(--font-type); letter-spacing:.06em; }
  .inp.short { flex:0 0 110px; }
  .inp.area { min-height:62px; line-height:1.55; resize:vertical; }
  .inp::placeholder { color:#5b6472; }
  .hint { margin:0; font-size:11.5px; color:#6b7280; line-height:1.5; }
  .ok { display:inline-flex; align-items:center; gap:5px; flex:none; font-size:11.5px;
        color:#4ade80; background:rgba(74,222,128,.12);
        border:1px solid rgba(74,222,128,.28); border-radius:999px; padding:3px 10px; }
  .warn { flex:none; font-size:11.5px; color:var(--amber);
          background:rgba(251,191,36,.12); border:1px solid rgba(251,191,36,.28);
          border-radius:999px; padding:3px 10px; }

  .topics { display:flex; flex-direction:column; gap:5px; }
  /* A <label> wrapping its own checkbox: the whole row is the target, and the
     tick is drawn by CSS off :checked, so this needs no script. */
  .topic { display:flex; align-items:center; gap:11px; padding:8px 11px;
           border-radius:9px; border:1px solid rgba(255,255,255,.10);
           background:rgba(255,255,255,.025); font-size:12.8px; cursor:pointer; }
  .topic:hover { background:rgba(255,255,255,.05); }
  .topic input { position:absolute; opacity:0; width:0; height:0; }
  .topic .box { width:15px; height:15px; border-radius:4px; flex:none; display:grid;
                place-items:center; font-size:9px; color:transparent;
                border:1.5px solid rgba(255,255,255,.24); }
  .topic input:checked ~ .box { background:var(--orange); border-color:var(--orange);
                                color:#14121a; }
  .topic:has(input:checked) { border-color:rgba(241,91,53,.38);
                              background:rgba(241,91,53,.10); }
  .topic.locked { border-style:dashed; cursor:default; }
  .topic.locked .box { background:rgba(241,91,53,.5); border-color:var(--orange);
                       border-style:dashed; color:#14121a; }
  .topic.off { opacity:.5; }
  .topic .tname { font-family:var(--font-type); font-size:11.5px; letter-spacing:.05em;
                  color:var(--amber); }
  .topic .why { font-size:11px; color:#6b7280; }
  .topic .n { margin-left:auto; flex:none; font-size:11px; color:var(--muted);
              font-variant-numeric:tabular-nums; }

  .preview { border:1px solid rgba(74,222,128,.24); background:rgba(74,222,128,.055);
             border-radius:11px; padding:12px 14px; display:flex;
             flex-direction:column; gap:8px; }
  .preview.none { border-color:rgba(255,255,255,.10); background:rgba(255,255,255,.025); }
  .preview .ph { font-size:11.5px; color:#4ade80; font-weight:600; }
  .preview.none .ph { color:var(--muted); }
  .chips { display:flex; flex-wrap:wrap; gap:6px; }
  .rchip { display:inline-flex; align-items:center; gap:6px; font-size:11.5px;
           color:#d5d8de; border:1px solid rgba(255,255,255,.10); border-radius:7px;
           padding:3px 9px; background:rgba(0,0,0,.28); }
  .rchip.gone { opacity:.45; text-decoration:line-through; }
  .actions { display:flex; align-items:center; gap:10px; padding:15px 20px;
             border-top:1px solid rgba(255,255,255,.10); }
  /* `font:inherit` here was the local workaround for the missing family, and as
     the shorthand it also blew away the `font-size`/`font-weight` those classes
     declare -- so the form's buttons were a different *size* from the dashboard's
     as well as a different face. The reset above covers the family; these keep
     their own type. */
  .actions .newproj, .actions .ghost { cursor:pointer; }
  .actions .ghost { font-size:12px; color:var(--muted); border-radius:8px;
                    padding:6px 12px; border:1px solid rgba(255,255,255,.10);
                    background:rgba(255,255,255,.03); }
  .actions .ghost:hover { color:#fff; background:rgba(255,255,255,.08); }
  .actions .newproj { border:0; }
  .setrow { display:flex; align-items:baseline; gap:14px; font-size:12.8px;
            padding:7px 0; border-top:1px solid rgba(255,255,255,.055); }
  .setrow:first-child { border-top:0; }
  .setlbl { flex:0 0 130px; color:#6b7280; font-size:11.5px; }
  .setval { color:#d5d8de; min-width:0; }
  .body.repos { gap:3px; }
  .you { border:1px solid rgba(255,255,255,.10); border-radius:16px;
         background:linear-gradient(150deg, rgba(30,20,16,.70), rgba(20,18,26,.58)); }
  .empty-you { display:flex; align-items:center; gap:14px; padding:18px 20px;
               flex-wrap:wrap; font-size:13px; color:var(--muted); }
  .handle { display:flex; align-items:center; gap:12px; padding:13px 18px; flex-wrap:wrap;
            border:1px solid rgba(255,255,255,.10); border-radius:16px;
            background:linear-gradient(150deg, rgba(30,20,16,.70), rgba(20,18,26,.58)); }
  .handle .lbl { font-size:10.5px; letter-spacing:.15em; text-transform:uppercase;
                 color:#6b7280; font-weight:700; flex:none; }
  .handle .chip { font-family:var(--font-type); font-size:11.5px; padding:3px 9px;
                  border-radius:6px; color:var(--amber);
                  background:rgba(251,191,36,.12); flex:none; }
  .handle .src { font-size:11.5px; color:#6b7280; }
  .btn { flex:none; font-size:11.5px; color:var(--muted); border-radius:7px;
         padding:4px 11px; border:1px solid rgba(255,255,255,.10);
         background:rgba(255,255,255,.03); }
  .btn:hover { color:#fff; background:rgba(255,255,255,.08); }

  @media (max-width:900px) {
    .duo { grid-template-columns:minmax(0,1fr); }
    .shell { grid-template-columns:minmax(0,1fr); }
    .navwrap { position:static; }
  }

  .reqrow { display:flex; align-items:center; gap:12px; padding:14px 18px;
            border-top:1px solid rgba(255,255,255,.07); }
  .reqrow:first-child { border-top:0; }
  .reqwho { flex:1; display:flex; flex-direction:column; gap:2px; min-width:0; }
  .reqwho .quiet { font-size:13px; }
  .reqnote { margin:4px 0 0; font-size:13px; color:#9aa1ad; }
  .cta.small, .ghost.small { width:auto; padding:7px 14px; font-size:13px; margin:0; }
  .ghost { background:transparent; border:1px solid rgba(255,255,255,.18);
           color:#cfd4dc; border-radius:999px; cursor:pointer; font-weight:600; }
  .ghost:hover { background:rgba(255,255,255,.08); }
  a.prs:hover { color:#fff; background:rgba(255,255,255,.12); }
  .flight { margin-top:12px !important; font-size:12px; color:var(--muted); }
  .flight b { color:#fff; font-weight:600; font-variant-numeric:tabular-nums; }
  /* The number carries the colour, not the whole phrase: four coloured labels in
     one line competes with the version above it, and the digit is what is being
     compared between cards. */
  .flight b.c-plan { color:var(--s-plan); }
  .flight b.c-live { color:var(--s-live); }
  .flight b.c-rev  { color:var(--s-rev); }
  .flight b.c-done { color:var(--s-done); }

  /* The release's counts, under their own heading rather than trailing the version.
     The heading is `.launch h4` like its neighbours, so it needs no rules of its
     own -- only the spacing between it and the line beneath, which the `.flight`
     rule above would otherwise double via its own top margin. */
  .tickets { margin-top:16px; padding-top:14px;
             border-top:1px solid rgba(255,255,255,.10); }
  .tickets .flight { margin-top:0 !important; }
  /* A second line in the block -- the project-wide total under the release's own
     counts -- needs a gap back. The rule above removes the top margin only so it
     does not double the heading's spacing, which is not a reason to weld two
     sibling lines together. */
  .tickets .flight + .flight { margin-top:6px !important; }

  /* The init command for a project, copyable. */
  .initcmd { display:inline-flex; align-items:center; gap:6px; flex:none;
             border:1px solid rgba(255,255,255,.10); border-radius:999px;
             padding:3px 4px 3px 11px; background:rgba(0,0,0,.32); }
  .initcmd code { font-family:var(--font-type); font-size:11px; color:var(--amber);
                  white-space:nowrap; }
  .copybtn, .iconbtn { display:grid; place-items:center; cursor:pointer; flex:none;
             width:24px; height:24px; padding:0; border-radius:50%;
             background:none; border:0; color:var(--muted); }
  .copybtn:hover, .iconbtn:hover { color:#fff; background:rgba(255,255,255,.09); }
  .copybtn.done { color:#4ade80; }
  .syncform { display:flex; flex:none; }
  .iconbtn { width:28px; height:28px; }
  .iconbtn:active { transform:rotate(180deg); transition:transform .3s ease; }
  .syncnote { font-size:12px; padding:10px 20px; border-top:1px solid rgba(255,255,255,.10); }
  .syncnote.ok { color:#4ade80; } .syncnote.err { color:#f87171; }

  .repo-sync { font-size:11px; color:#6b7280; flex:none; font-variant-numeric:tabular-nums; }
  .launch h4 { margin:0 0 12px; font-size:10.5px; letter-spacing:.15em; text-transform:uppercase;
               color:#6b7280; font-weight:700; }
  .ver { font-family:var(--font-type); font-size:25px; letter-spacing:-.01em; display:block;
         margin-bottom:9px; }
  .ver.none { color:#6b7280; }
  .pill { display:inline-flex; align-items:center; font-size:11px; padding:3px 10px; border-radius:999px;
          font-weight:600; letter-spacing:.04em; text-transform:uppercase; }
  .pill.in_progress { color:var(--s-live); background:rgba(74,222,128,.13); border:1px solid rgba(74,222,128,.28); }
  .pill.planned { color:var(--s-plan); background:rgba(251,191,36,.13); border:1px solid rgba(251,191,36,.28); }
  .pill.released { color:var(--s-done); background:rgba(139,156,179,.13); border:1px solid rgba(139,156,179,.26);
                   text-transform:none; letter-spacing:0; }

  .launch p { margin:12px 0 0; font-size:12px; color:var(--muted); line-height:1.5; }
  .quiet { color:#6b7280; font-size:12.5px; }

  .panel { border:1px solid rgba(255,255,255,.10); border-radius:18px; overflow:hidden;
           background:rgba(255,255,255,.022); }
  .panel-head { display:flex; align-items:baseline; gap:12px; flex-wrap:wrap;
                padding:16px 20px; border-bottom:1px solid rgba(255,255,255,.10); }
  .panel-head h3 { margin:0; font-size:14.5px; font-weight:650; }
  .panel-head small { font-size:12px; color:var(--muted); }
  .tblwrap { overflow-x:auto; }
  table { width:100%; border-collapse:collapse; font-size:12.5px; }
  th { text-align:left; font-size:10px; letter-spacing:.13em; text-transform:uppercase;
       color:#6b7280; font-weight:700; padding:11px 20px 7px; white-space:nowrap; }
  td { padding:9px 20px; border-top:1px solid rgba(255,255,255,.055); color:var(--muted);
       white-space:nowrap; }
  td.nm { color:#fff; font-weight:500; }
  td.num { font-variant-numeric:tabular-nums; }
  .revoke { background:none; border:0; cursor:pointer; color:#f87171; font:inherit; font-size:11.5px; }
  .mintrow { display:flex; gap:10px; align-items:center; flex-wrap:wrap;
             padding:15px 20px; border-top:1px solid rgba(255,255,255,.10); }
  .fld { background:rgba(0,0,0,.4); border:1px solid rgba(255,255,255,.10); border-radius:9px;
         padding:9px 13px; font-size:13px; color:#fff; font-family:var(--font-ui); }
  .fld.n { flex:1 1 180px; min-width:0; }
  .fld.d { width:150px; }
  .cta { border:0; border-radius:999px; padding:10px 22px; font-size:13px; font-weight:800;
         color:#fff; cursor:pointer; flex:none;
         background:linear-gradient(93deg,var(--orange),#ff7a4a);
         box-shadow:0 8px 22px rgba(241,91,53,.34); }
  .cta.sm { padding:7px 16px; font-size:12px; box-shadow:0 6px 16px rgba(241,91,53,.3); }

  .authwrap { display:grid; place-items:center; padding:9vh 24px; }
  /* A second way in, given equal weight to the email form rather than buried
     under it -- for anyone who has one, it is the faster path. */
  .oauth { display:flex; align-items:center; justify-content:center; gap:10px;
           width:100%; padding:11px 14px; margin:4px 0 0; border-radius:10px;
           font-size:13.5px; font-weight:600; color:#1f2328; background:#fff;
           border:1px solid rgba(255,255,255,.16); }
  .oauth:hover { background:#f1f3f5; }
  .oauth svg { width:17px; height:17px; flex:none; }
  .orsep { display:flex; align-items:center; gap:12px; margin:16px 0 4px;
           color:#6b7280; font-size:11px; letter-spacing:.1em;
           text-transform:uppercase; }
  .orsep::before, .orsep::after { content:""; flex:1 1 auto; height:1px;
           background:rgba(255,255,255,.12); }
  .authcard { width:min(420px,100%); background:rgba(255,255,255,.03);
              border:1px solid rgba(255,255,255,.10); border-radius:20px; padding:34px 30px;
              box-shadow:0 24px 60px rgba(0,0,0,.5); }
  .authcard h1 { margin:22px 0 7px; font-size:20px; font-weight:650; letter-spacing:-.015em;
                 text-wrap:balance; }
  .authcard p { margin:0 0 22px; font-size:13.5px; color:var(--muted); line-height:1.55; }
  .lbl { display:block; font-size:10.5px; letter-spacing:.13em; text-transform:uppercase;
         color:#6b7280; font-weight:700; margin-bottom:8px; }
  .authcard .fld { width:100%; }
  .authcard .cta { width:100%; margin-top:14px; }
  .fine { font-size:11.5px; color:#6b7280; margin:15px 0 0; text-align:center; }
  .err { font-size:13px; color:#f87171; margin:0 0 18px; }
  .sent { text-align:center; }
  .sent b { color:#fff; }
  /* The wordmark is a flex row; centre it on the waiting screen without
     restyling the header copy of the same component. */
  .markrow { display:flex; justify-content:center; margin-bottom:20px; }

  /* --- scrum summary panel, inside .launch ------------------------------- */
  /* `padding-bottom` because the panel is the last thing in the card: its final
     row sat against the card's edge, so the block read as clipped rather than as
     finished. */
  .scrum { margin-top:20px; padding-top:16px; padding-bottom:18px;
           border-top:1px solid rgba(255,255,255,.10); }
  .scrum-head { display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; margin-bottom:11px; }
  .scrum-head h4 { margin:0; }
  .scope { display:inline-flex; gap:2px; padding:2px; border-radius:999px; margin-left:auto;
           border:1px solid rgba(255,255,255,.10); background:rgba(0,0,0,.28); }
  .scope a { font-size:11px; padding:3px 10px; border-radius:999px; color:var(--muted); }
  .scope a:hover { color:#fff; }
  .scope a.on { color:#14121a; font-weight:700;
                background:linear-gradient(135deg,var(--orange),var(--amber)); }
  /* A little more air between rows. Each of these is a ticket reference, a title,
     a line of prose and a row of icons -- four things stacked -- so 8px above and
     below left consecutive tickets reading as one block of text rather than as
     separate items. The rule between them does the dividing; the padding is what
     makes the rule land in a gap instead of against the type.
     Asymmetric, though: 12px under the icon row *plus* the next row's 12px above
     its reference put 24px between a ticket's prose and the next ticket, which
     is more air than the four stacked lines inside one row get. The gap back to
     the divider is the one to spend less on. */
  .sitem { padding:12px 0 7px; border-top:1px solid rgba(255,255,255,.055);
           min-width:0; }
  .sitem:first-of-type { border-top:0; }
  /* **No wrap.** With `flex-wrap`, a long ticket title took the full width and
     pushed the owner bubble onto a line of its own -- a 22px circle alone on row
     two, reading as a separate item rather than as that row's owner. Unwrapped,
     the title shrinks and wraps *inside its own box* (`.stitle` already has
     `min-width:0` and `overflow-wrap:anywhere`) while the bubble stays on the
     first line beside it. */
  .sitem-top { display:flex; align-items:baseline; gap:8px; min-width:0; }
  /* `inline-flex` so the external-link arrow sits on the reference's baseline
     row rather than wrapping under it. The arrow is what says "this leaves
     InnoDay" -- the reference alone read as an internal anchor. */
  .sref { font-family:var(--font-type); font-size:11px; color:var(--amber); flex:none;
          display:inline-flex; align-items:center; gap:4px; }
  .sref .ext { flex:none; opacity:.5; }
  .sref:hover .ext { opacity:1; }
  /* A notch larger than it was (12.6px). These three -- title, prose and thin
     row -- are the panel's reading matter, and they were set smaller than the
     card copy above them for no reason other than that they are dense. The
     labels, references and chips around them keep their sizes, so the hierarchy
     is unchanged; only the text you actually read got bigger. */
  .stitle { font-size:13.4px; color:#fff; min-width:0; overflow-wrap:anywhere; }
  /* A person as initials, not as an address. Same size and gradient as the
     contributor bubbles on the card header, so one device means one thing. */
  /* `align-self:flex-start` so a title that wraps to three lines still has its
     owner beside the first one. Baseline alignment would drop the bubble to the
     last line, which reads as belonging to whatever ended up there. */
  /* `inline-grid`, not `grid`: the trailing blocks put a bubble at the end of a
     `.sthin` line of running text, and a block-level box there would drop it onto
     a row of its own. Inside `.sitem-top` this is identical -- a flex item's
     display is blockified, and `vertical-align` is ignored -- so the active rows
     are unaffected. */
  .obub { flex:none; align-self:flex-start; width:22px; height:22px;
          border-radius:50%; display:inline-grid; vertical-align:middle;
          place-items:center; font-size:9.5px; font-weight:800; color:#14121a;
          background:linear-gradient(135deg,var(--orange),var(--amber)); }
  /* Unmapped is a ring, not a word: it is a state of the mapping, not part of
     anyone's name -- but it has to stay visible or the profile page goes
     unadvertised. */
  .obub.unmapped { color:var(--amber); background:rgba(251,191,36,.14);
                   box-shadow:inset 0 0 0 1.5px rgba(251,191,36,.55); }

  /* What a line is wired to. Its own row, code on the left of the divider and the
     board on the right. Grey is "not connected"; green is. */
  .cxrow { display:flex; align-items:center; gap:8px; margin-top:6px; }
  .cxrow .cx { display:inline-flex; color:#4b5563; }
  .cxrow .cx.on { color:var(--s-live); }
  /* A draft is open but not asking for review, so it reads as pending rather than
     as done. */
  .cxrow .cx.on.draft { color:var(--s-plan); }
  .cxrow a.cx:hover { color:#fff; }
  .cxsep { color:#374151; font-size:12px; line-height:1; }
  .sbody { margin:3px 0 0; font-size:12.6px; color:var(--muted); line-height:1.5;
           overflow-wrap:anywhere; }
  /* The verdict a release line was judged with, read from the stored row. Colour
     carries the same three-way reading the words do, so a wall of lines can be
     skimmed for the ones that need attention. */
  .sverdict { font-family:var(--font-type); font-size:10px; letter-spacing:.08em;
              text-transform:uppercase; padding:1px 6px; border-radius:3px;
              flex:none; white-space:nowrap; border:1px solid currentColor; }
  .sverdict.shipped { color:var(--s-live); }
  .sverdict.partial { color:var(--s-plan); }
  .sverdict.missing { color:#f87171; }
  .sverdict.idle    { color:var(--s-done); }
  .speople { font-size:11.5px; color:#6b7280; margin-top:2px; }
  .speople b { color:var(--muted); font-weight:500; }
  .smeta { margin-top:3px; font-size:11px; color:#6b7280; display:flex; gap:8px;
           flex-wrap:wrap; align-items:baseline; }
  .smeta a { color:var(--amber); }
  .smeta a:hover { text-decoration:underline; }
  .sblock { margin-top:12px; font-size:10px; letter-spacing:.13em; text-transform:uppercase;
            color:#6b7280; font-weight:700; }
  .sthin { font-size:12.8px; color:var(--muted); padding:6px 0 2px;
           overflow-wrap:anywhere; }
  .sfoot { margin-top:12px; font-size:11px; color:#6b7280; font-variant-numeric:tabular-nums; }
  .sfoot a { color:var(--amber); }
  .sfoot a:hover { text-decoration:underline; }
  .sempty { font-size:12.5px; color:var(--muted); line-height:1.55; }
  .sempty b { color:#fff; font-weight:600; display:block; margin-bottom:4px; }
  .sempty a { color:var(--amber); }
  .sempty a:hover { text-decoration:underline; }
  .sempty .initcmd { margin-top:9px; }

  /* --- profile page ------------------------------------------------------ */
  .backlink { font-size:12px; color:var(--muted); }
  .backlink:hover { color:#fff; }
  .prow { display:flex; align-items:flex-start; gap:13px; flex-wrap:wrap;
          padding:14px 20px; border-top:1px solid rgba(255,255,255,.055); }
  .prow-id { min-width:190px; flex:0 1 auto; }
  .prow-id b { display:block; font-size:13px; font-weight:600; }
  .prow-id em { font-style:normal; font-size:11.5px; color:#6b7280; }
  .plat { font-family:var(--font-type); font-size:10px; letter-spacing:.09em;
          text-transform:uppercase; padding:2px 7px; border-radius:4px; flex:none;
          color:#93c5fd; background:rgba(147,197,253,.13); }
  .handle { font-family:var(--font-type); font-size:12.5px; color:#fff; }
  .badge { font-size:10px; letter-spacing:.04em; padding:2px 8px; border-radius:999px; flex:none;
           color:#4ade80; background:rgba(74,222,128,.12); border:1px solid rgba(74,222,128,.26); }
  .badge.grey { color:#94a3b8; background:rgba(148,163,184,.12);
                border-color:rgba(148,163,184,.24); }
  .pform { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-left:auto; }
  .pform .fld { padding:7px 11px; font-size:12.5px; }
  .pick { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px; width:100%; }
  .pick-lbl { width:100%; font-size:10.5px; letter-spacing:.13em; text-transform:uppercase;
              color:#6b7280; font-weight:700; }
  .pick button { cursor:pointer; font:inherit; font-size:12px; padding:5px 11px;
                 border-radius:999px; color:var(--muted);
                 border:1px solid rgba(255,255,255,.12); background:rgba(255,255,255,.03); }
  .pick button:hover { color:#14121a; border-color:transparent;
                       background:linear-gradient(135deg,var(--orange),var(--amber)); }
  .pick .n { font-variant-numeric:tabular-nums; opacity:.62; }

  @media (max-width:780px) {
    .proj-body { grid-template-columns:1fr; }
    .launch { border-left:0; border-top:1px solid rgba(255,255,255,.10); }
    .pform { margin-left:0; width:100%; }
  }
  @media (prefers-reduced-motion:reduce) { * { animation:none !important; transition:none !important; } }
"""
)


# One delegated listener rather than an inline handler per button: the buttons are
# generated per project, and inline `onclick` would be the thing a future CSP has
# to allow. Feature-detected, so an insecure context (plain http) degrades to the
# text being selectable rather than to a broken-looking button.
_COPY_JS_SOURCE = """
document.addEventListener('click', function (event) {
  var copy = event.target.closest('.copybtn');
  if (copy && navigator.clipboard) {
    navigator.clipboard.writeText(copy.dataset.copy).then(function () {
      copy.classList.add('done');
      window.setTimeout(function () { copy.classList.remove('done'); }, 1200);
    });
    return;
  }

  // The default org star. The form still submits and the server still decides --
  // this only moves the highlight before the round trip, because a control that
  // waits on a page reload to acknowledge a click reads as broken. If the POST
  // fails, the reload shows the truth and this optimism is discarded.
  var star = event.target.closest('.star');
  if (star) {
    var menu = star.closest('.dropdown');
    if (!menu) { return; }
    menu.querySelectorAll('.star.is-default').forEach(function (other) {
      other.classList.remove('is-default');
      other.innerHTML = '\u2606';
    });
    star.classList.add('is-default');
    star.innerHTML = '\u2605';
    return;
  }

  // Layer picker, same bargain as the star: repaint the chip and the tile now,
  // let the POST and its reload confirm it. Picking a classification and then
  // watching the page sit still is the interaction reading as broken, not the
  // round trip being genuinely slow.
  var option = event.target.closest('.lay-opt');
  if (!option) { return; }
  var picker = option.closest('.laypick');
  var row = option.closest('.repo');
  if (!picker || !row) { return; }
  var hue = option.style.getPropertyValue('--h');
  var summary = picker.querySelector('summary');
  if (summary) { summary.textContent = option.textContent.trim(); }
  if (hue) { row.style.setProperty('--h', hue); }
  picker.removeAttribute('open');
});


// The project menu remembers whether it is open. `<details>` state does not
// survive a page load, so without this every tab change silently re-opened a
// menu the reader had just collapsed -- which reads as the app forgetting.
//
// localStorage rather than a cookie: it is a viewing preference, never sent to
// the server, and nothing here needs it. `try` because Safari's private mode
// throws on access rather than returning null, and a broken menu is a worse
// outcome than an unremembered one.
(function () {
  // Drag a ticket onto a release. **Progressive enhancement over the buttons**:
  // it finds the hidden form the hover arrow already renders for that release and
  // submits it, so there is no second write path, no new endpoint, and no
  // divergence to keep in step. With script disabled the arrows still work.
  var rows = document.querySelectorAll('.brow[draggable="true"]');
  var slots = document.querySelectorAll('.slot[data-release]');
  if (rows.length && slots.length) {
    var held = null;
    rows.forEach(function (row) {
      row.addEventListener('dragstart', function (e) {
        held = row;
        row.classList.add('dragging');
        // `setData` is required or Firefox refuses to start the drag at all.
        try { e.dataTransfer.setData('text/plain', row.dataset.ticket || ''); } catch (err) {}
        if (e.dataTransfer) { e.dataTransfer.effectAllowed = 'move'; }
      });
      row.addEventListener('dragend', function () {
        row.classList.remove('dragging');
        held = null;
      });
    });
    slots.forEach(function (slot) {
      slot.addEventListener('dragover', function (e) {
        if (!held) { return; }
        // Without preventDefault the browser never fires `drop`.
        e.preventDefault();
        if (e.dataTransfer) { e.dataTransfer.dropEffect = 'move'; }
        slot.classList.add('dropok');
      });
      slot.addEventListener('dragleave', function () { slot.classList.remove('dropok'); });
      slot.addEventListener('drop', function (e) {
        slot.classList.remove('dropok');
        if (!held) { return; }
        e.preventDefault();
        var want = slot.dataset.release;
        var form = null;
        held.querySelectorAll('form.planq').forEach(function (f) {
          var input = f.querySelector('input[name="release"]');
          if (input && input.value === want) { form = f; }
        });
        // No form for this slot means the ticket is already in it. Nothing to do,
        // and inventing a request would be a write the page never offered.
        if (!form) { return; }
        if (form.requestSubmit) { form.requestSubmit(); } else { form.submit(); }
      });
    });
  }

  var nav = document.querySelector('.navwrap');
  if (!nav) { return; }
  // Versioned key. The previous one stored '1' whenever the rail was open, and
  // open used to be the default -- so every browser that had simply *used* the
  // page carried a value that reopened it against the new default. A new key is
  // the only way to distinguish "chose open" from "was open before the change".
  var KEY = 'innoday.nav.open.v2';
  try {
    // Shut is the default, so only an explicit '1' reopens it. Reading the
    // absence of a value as "open" is what made a first visit start expanded.
    if (window.localStorage.getItem(KEY) === '1') { nav.setAttribute('open', ''); }
  } catch (err) { /* no storage: the rail simply starts shut every time */ }
  nav.addEventListener('toggle', function () {
    try { window.localStorage.setItem(KEY, nav.open ? '1' : '0'); } catch (err) {}
  });
})();
"""


#: What is actually served. The sources above keep their comments; the browser
#: gets neither them nor the chance to satisfy a test that meant to check
#: behaviour -- see `strip_authoring_comments`.
_APP_CSS = strip_authoring_comments(_APP_CSS_SOURCE)
_COPY_JS = strip_authoring_comments(_COPY_JS_SOURCE)


def _page(title: str, body: str) -> str:
    """Wrap a page body in the shared app shell."""
    return (
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8"/>\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
        f"<title>{esc(title)}</title>\n"
        f"{favicon_link()}\n"
        f"<style>{_APP_CSS}</style></head>\n"
        f"<body>{body}\n<script>{_COPY_JS}</script></body></html>"
    )


def _wordmark() -> str:
    return (
        '<span class="mark">'
        f"{icons.WORDMARK_SVG}"
        '<span class="div"></span>'
        f'<span class="rocket">{icons.ROCKET_SVG}<span class="name">innoday</span></span>'
        "</span>"
    )


# --------------------------------------------------------------------------- #
# Sign-in
# --------------------------------------------------------------------------- #


def login_page(
    *,
    error: Optional[str] = None,
    email: str = "",
    google_url: Optional[str] = None,
) -> str:
    """The sign-in card. ``error`` is shown above the form when present.

    ``google_url`` is None when the provider is not configured, and then no
    button is drawn at all. A "Continue with Google" that leads to a 400 is worse
    than its absence -- it reads as InnoDay being broken rather than as a door
    that was never opened, which is the same reasoning the email form already
    applies when Supabase is missing.
    """
    error_html = f'<p class="err">{esc(error)}</p>' if error else ""
    google_html = ""
    if google_url:
        google_html = f"""
  <a class="oauth" href="{esc(google_url)}">{icons.GOOGLE_SVG}
    <span>Continue with Google</span></a>
  <div class="orsep"><span>or</span></div>"""
    body = f"""
<div class="authwrap"><div class="authcard">
  {_wordmark()}
  <h1>Sign in</h1>
  <p>We&rsquo;ll email you a link that signs you in. No password to remember.</p>
  {error_html}{google_html}
  <form method="post" action="{esc(LOGIN_PATH)}">
    <label class="lbl" for="email">Email</label>
    <input class="fld" id="email" name="email" type="email" required
           autocomplete="email" autofocus value="{esc(email)}"/>
    <button class="cta" type="submit">Send my link</button>
  </form>
  <p class="fine">Links expire after one use. Either way, you need an invite
    &mdash; signing in with Google does not create an account.</p>
</div></div>"""
    return _page("Sign in to innoday", body)


def login_sent_page(email: str) -> str:
    """Shown after a link is requested -- identically, whether or not the address
    has an account. A page that says "no such user" hands over a list of who is.

    Carries the same wordmark as the sign-in card rather than a bare rocket: this
    is the screen someone stares at while waiting for an email, and an unbranded
    one reads like the flow handed them off somewhere else.
    """
    body = f"""
<div class="authwrap"><div class="authcard sent">
  <div class="markrow">{_wordmark()}</div>
  <h1>Check your email</h1>
  <p>A sign-in link is on its way to <b>{esc(email)}</b>. Open it on this device
  and you&rsquo;ll land straight on your dashboard.</p>
  <form method="post" action="{esc(LOGIN_PATH)}" class="resend">
    <input type="hidden" name="email" value="{esc(email)}">
    <button class="ghost wide" type="submit">Didn&rsquo;t arrive? Send another</button>
  </form>
  <p class="fine">Links expire and an old one cannot be reused, so ask again for
  a fresh one. Repeat requests are rate-limited, so give it a minute.<br>
  <a href="{esc(LOGIN_PATH)}">Use a different address</a></p>
</div></div>"""
    return _page("Check your email", body)


def join_page(*, error: Optional[str] = None, email: str = "") -> str:
    """Request access, holding the team secret.

    The secret field is `type="password"` and `autocomplete="off"`: it is a
    shared credential, and a browser helpfully remembering it on whatever machine
    someone happened to use is exactly how a shared secret stops being one.
    """
    error_html = f'<p class="err">{esc(error)}</p>' if error else ""
    body = f"""
<div class="authwrap"><div class="authcard">
  {_wordmark()}
  <h1>Request access</h1>
  <p>Already have an account but can&rsquo;t sign in? This sends you a fresh
  link. New here? Your request goes to an administrator.</p>
  {error_html}
  <form method="post" action="{esc(JOIN_PATH)}">
    <label class="lbl" for="email">Email</label>
    <input class="fld" id="email" name="email" type="email" required
           autocomplete="email" autofocus value="{esc(email)}"/>

    <label class="lbl" for="full_name">Your name</label>
    <input class="fld" id="full_name" name="full_name" type="text"
           autocomplete="name" placeholder="Optional"/>

    <label class="lbl" for="team_secret">Team secret</label>
    <input class="fld" id="team_secret" name="team_secret" type="password"
           required autocomplete="off"/>

    <label class="lbl" for="note">Anything we should know?</label>
    <input class="fld" id="note" name="note" type="text"
           placeholder="Optional &mdash; e.g. which project you&rsquo;re joining"/>

    <button class="cta" type="submit">Request access</button>
  </form>
  <p class="fine"><a href="{esc(LOGIN_PATH)}">Back to sign in</a></p>
</div></div>"""
    return _page("Request access to innoday", body)


def join_submitted_page(email: str, *, queued: bool) -> str:
    """Two different truths, told plainly.

    An existing account gets an email now; a new one waits for a person. Showing
    one message for both would leave half of them refreshing an inbox for
    something that is never coming.
    """
    if queued:
        headline = "Request received"
        detail = (
            f"We&rsquo;ve passed <b>{esc(email)}</b> to an administrator. "
            "You&rsquo;ll get an email as soon as someone approves it."
        )
    else:
        headline = "Check your email"
        detail = (
            f"You already have an account, so a fresh link is on its way to "
            f"<b>{esc(email)}</b>. Open it on this device."
        )
    body = f"""
<div class="authwrap"><div class="authcard sent">
  <div class="markrow">{_wordmark()}</div>
  <h1>{headline}</h1>
  <p>{detail}</p>
  <p class="fine"><a href="{esc(LOGIN_PATH)}">Back to sign in</a></p>
</div></div>"""
    return _page(headline, body)


def join_unavailable_page() -> str:
    """No team secret configured means this page has no gate, so it does not open.

    "Not configured" must never read as "gate passed" -- that is the failure
    where a permissive local default silently ships to production.
    """
    body = f"""
<div class="authwrap"><div class="authcard">
  {_wordmark()}
  <h1>Not available</h1>
  <p>This deployment has no team secret set, so requests for access can&rsquo;t
  be verified. Ask an administrator to invite you directly.</p>
  <p class="fine"><a href="{esc(LOGIN_PATH)}">Back to sign in</a></p>
</div></div>"""
    return _page("Not available", body)


def unconfigured_page() -> str:
    """Browser sign-in needs Supabase; say so rather than showing a dead form."""
    body = f"""
<div class="authwrap"><div class="authcard">
  {_wordmark()}
  <h1>Browser sign-in isn&rsquo;t set up here</h1>
  <p>This deployment has no email identity provider configured, so it cannot send
  sign-in links. Set <code>SUPABASE_URL</code> and <code>SUPABASE_KEY</code>, or use
  the CLI: <code>innoday login</code>.</p>
</div></div>"""
    return _page("Sign-in unavailable", body)


def no_orgs_page(user: User) -> str:
    """A real, verified user who belongs to nothing. Dead-ends politely."""
    body = f"""
<header class="topbar">{_wordmark()}
  <form method="post" action="{esc(LOGOUT_PATH)}">
    <button class="signout" type="submit">Sign out</button>
  </form>
</header>
<main>
  <div class="panel"><div class="panel-head">
    <h3>No organizations yet</h3>
    <small>{esc(user.email)} isn&rsquo;t a member of any organization.</small>
  </div>
  <div class="mintrow"><p class="quiet" style="margin:0">Ask an admin to invite you,
  then reload this page.</p></div></div>
</main>"""
    return _page("innoday", body)


# --------------------------------------------------------------------------- #
# Dashboard
# --------------------------------------------------------------------------- #


def _initials(full_name: str, email: str) -> str:
    parts = [p for p in (full_name or "").split() if p]
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    if parts:
        return parts[0][:2].upper()
    return (email or "?")[:2].upper()


def _user_menu(user: User, current: Organization, orgs: List[Organization]) -> str:
    """The user menu, with an org switcher only when there is a choice to make.

    One org means no chevron and no dropdown of alternatives -- an affordance that
    leads nowhere is worse than no affordance.
    """
    multi = len(orgs) > 1
    chevron = f' <span class="chev">{CHEVRON}</span>' if multi else ""

    default_action = f"{UI_PREFIX}/{(current.alias or current.id).lower()}/default-org"

    org_rows = ""
    if multi:
        rows = []
        for org in orgs:
            on = " on" if org.id == current.id else ""
            is_default = org.id == user.default_organization_id
            # A star per row, filled for the default. It is a submit button rather
            # than a link because it changes state, and it sits inside the row so
            # "go there" and "always go there" are one gesture apart.
            star = (
                f'<form method="post" action="{esc(default_action)}" class="starform">'
                f'<input type="hidden" name="organization_id" value="{esc(org.id)}"/>'
                f'<button class="star{" is-default" if is_default else ""}" type="submit" '
                f'title="{"Your default organization" if is_default else "Make this your default"}" '
                f'aria-label="{"Default organization" if is_default else "Make " + esc(org.name) + " default"}">'
                f"{'&#9733;' if is_default else '&#9734;'}</button></form>"
            )
            rows.append(
                f'<div class="dd-row{on}">'
                f'<a class="dd-orglink" href="{esc(dashboard_path(org.alias or org.id))}">'
                f'<span class="tick">&#10003;</span>{esc(org.name)}</a>{star}</div>'
            )
        org_rows = (
            '<div class="dd-sep"></div>'
            '<div class="dd-label">Organization <span class="dd-hint">&#9733; = opens by default</span></div>'
            + "".join(rows)
        )

    return f"""
<details class="usermenu">
  <summary>
    <span class="avatar">{esc(_initials(user.full_name, user.email))}</span>
    <span class="who"><b>{esc(user.full_name or user.email)}</b>
      <em>{esc(current.name)}{chevron}</em></span>
  </summary>
  <div class="dropdown">
    <div class="dd-label">Signed in as</div>
    <div class="dd-row quiet">{esc(user.email)}</div>
    {org_rows}
    <div class="dd-sep"></div>
    <form method="post" action="{esc(LOGOUT_PATH)}">
      <button class="signout" type="submit">Sign out</button>
    </form>
    <div class="dd-sep"></div>
    <a class="dd-cli" href="https://pypi.org/project/innoday/" target="_blank" rel="noopener">
      Install the innoday CLI
      <span class="dd-cli-sub">pypi.org/project/innoday</span>
    </a>
  </div>
</details>"""


# --------------------------------------------------------------------------- #
# The left nav -- one of them, on every signed-in page
#
# It used to render at a single call site, the project page, so the dashboard,
# the workflow launcher, profile, team and the new-project form each had no way
# out at all: the launcher is where signing in lands, and it could not reach the
# projects list (#636).
#
# **One function, imported rather than copied.** `workflow.py` builds its page
# from this module's `_page`, `_user_menu` and `_wordmark` already and takes the
# nav the same way. A second implementation there is precisely the duplication
# that drifted `/ui` and `/api/v1` validation apart in #627.
# --------------------------------------------------------------------------- #


def _nav_link(
    href: str, label: str, glyph: str, *, on: bool, trailing: str = ""
) -> str:
    """One row. ``on`` marks it both visibly (`.on`) and to a screen reader."""
    cls = ' class="on"' if on else ""
    current = ' aria-current="page"' if on else ""
    return (
        f'<a{cls}{current} href="{esc(href)}">{glyph}'
        f"<span>{esc(label)}</span>{trailing}</a>"
    )


def _app_nav(
    org: Organization,
    *,
    active: str = "",
    project_alias: Optional[str] = None,
    open_tickets: int = 0,
) -> str:
    """The left menu, collapsible without a line of JavaScript.

    A ``<details>``, which is the idiom the user menu and the layer picker
    already use here. The shell grid's first track is ``auto``, so a closed
    ``<details>`` shrinks the column by itself -- there is no collapsed width
    constant to keep in step with an expanded one.

    **Shut by default.** The pane beside it is the thing you came for, and a rail
    that must be dismissed on every visit costs more than it gives. `_COPY_JS`
    reopens it if this browser last left it open, so the choice persists per
    person without a server-side preference.

    Two levels, and the second one is conditional. The org's own pair --
    Workflows and Projects -- is on every page. The project block is drawn only
    when ``project_alias`` names a project that is actually in scope, nested
    under its alias so the rail reads as a hierarchy rather than as seven flat
    links. ``active`` is one of ``"workflow"``, ``"projects"`` or a project tab;
    a page that is none of those (profile, team, the new-project form) passes
    ``""`` and no row claims to be the current one, which is the honest answer.

    The project block leads with "Project", not "You". It leads with the
    project's own state -- the card, its repos, its next launch -- and only then
    the viewer's part in it, so naming the whole tab after the smaller half
    misdescribed it.
    """
    org_ref = org.alias or org.id
    rows = [
        # Headings, not links. A heading that navigates is the confusion the
        # removed "Project" label caused, and both destinations are one row down.
        f'<span class="navhead" title="{esc(org.name)}">{esc(org.name)}</span>',
        _nav_link(
            workflow_path(org_ref),
            "Workflows",
            icons.NAV_WORKFLOWS_SVG,
            on=active == "workflow",
        ),
        # **Projects points at the dashboard, and no `/ui/{org}/projects` route
        # was added.** The dashboard *is* the projects list -- it renders one
        # card per project and nothing else above them -- so a second path would
        # be either a redirect or a second rendering of the same page, and the
        # only thing it would buy is a URL whose noun matches the label. The
        # "projects" entry in `RESERVED_UI_SEGMENTS` is not thereby wasted: it is
        # what stops an org aliased "projects" producing
        # `/ui/projects/projects/pf`, which is its own reason and still holds.
        _nav_link(
            dashboard_path(org_ref),
            "Projects",
            icons.NAV_PROJECTS_SVG,
            on=active == "projects",
        ),
    ]

    if project_alias:
        base = project_path(org_ref, project_alias)
        items = (
            ("you", "Project", icons.NAV_ROCKET_SVG, ""),
            (
                "tickets",
                "Tickets",
                icons.NAV_TICKETS_SVG,
                f'<span class="ct">{open_tickets}</span>' if open_tickets else "",
            ),
            ("releases", "Releases", icons.NAV_RELEASES_SVG, ""),
            ("timeline", "Timeline", icons.NAV_TIMELINE_SVG, ""),
        )
        sub = [
            f'<span class="navhead" title="{esc(project_alias)}">'
            f"{esc(project_alias)}</span>"
        ]
        for key, label, glyph, count in items:
            href = base if key == "you" else f"{base}/{key}"
            sub.append(_nav_link(href, label, glyph, on=key == active, trailing=count))

        # Settings sits under a rule: it configures the project rather than
        # reporting on it, and grouping it with the three views would imply it is
        # a fourth one.
        sub.append('<span class="navsep"></span>')
        sub.append(
            _nav_link(
                f"{base}/settings",
                "Settings",
                icons.NAV_SETTINGS_SVG,
                on=active == "settings",
            )
        )
        rows.append(f'<div class="navsub">{"".join(sub)}</div>')

    # **No label beside the toggle.** It read "Project" in the same position as
    # the nav rows and was not a link -- so the one word on the menu that looked
    # most like its heading was the one thing that did nothing when clicked. The
    # org and project names are headings *inside* the rail instead, where they
    # disappear with the rest of it when it is shut and cannot widen the 38px
    # closed column.
    #
    # The glyphs stay in this order in the markup -- hamburger, then close -- and
    # only one is ever displayed. Open, the close glyph is pushed to the rail's
    # right edge by CSS rather than by markup, so the toggle is where the eye
    # already is when the menu is wide, and the hamburger stays centred in the
    # 38px rail when it is shut.
    return (
        '<details class="navwrap">'
        '<summary title="Show or hide the menu" aria-label="Show or hide the menu">'
        f"{icons.MENU_SVG}{icons.MENU_CLOSE_SVG}"
        "</summary>"
        f'<nav class="nav">{"".join(rows)}</nav>'
        "</details>"
    )


def _shell(nav: str, pane: str) -> str:
    """The two-track grid every signed-in page is laid out on: rail, then pane.

    One helper rather than the same three lines in six page functions, so a page
    cannot be added with a `.pane` and no nav beside it.
    """
    return f'<div class="shell">{nav}<div class="pane">{pane}</div></div>'


def _count_row(planned: int, in_progress: int, in_review: int, done: int) -> str:
    """The four counts as one line, or ``""`` when there is nothing to count.

    Colour-coded by the same three semantic classes the release pills use, and
    ordered the way work moves: queued, moving, being checked, shipped. ``done``
    is what makes the line readable as progress -- without it the card showed only
    what was unfinished, so a project that had delivered a hundred tickets and a
    project that had delivered none looked identical.

    "in review", not "in test": the board's statuses are BACKLOG / TODO /
    IN_PROGRESS / IN_REVIEW / DONE. There is no test state, and labelling
    IN_REVIEW as "in test" would report something the data does not say.
    """
    parts = []
    if planned:
        parts.append(f'<b class="c-plan">{planned}</b> planned')
    if in_progress:
        parts.append(f'<b class="c-live">{in_progress}</b> in progress')
    if in_review:
        parts.append(f'<b class="c-rev">{in_review}</b> in review')
    if done:
        parts.append(f'<b class="c-done">{done}</b> done')
    return " &middot; ".join(parts)


def _work_in_flight(card: ProjectCard) -> str:
    """The open release's tickets, beside the version they belong to.

    Its own block with its own heading, rather than a bare line under the
    version. Unlabelled, the counts read as whatever sat above them. The heading
    is the same ``h4`` as "Next launch" and "Scrum summary", so it joins a rhythm
    the panel already has instead of introducing one.

    Rendered **even when every count is zero**. Returning "" for a quiet project
    left neighbouring cards at different heights for no reason a reader could
    infer, and a version with nothing attached to it is a fact worth stating
    rather than an absence to be inferred from a gap -- so the zero case says
    what it means and gives the board's own total beside it.
    """
    total = card.planned + card.in_progress + card.in_review + card.done
    upcoming = card.next_release

    if upcoming is None:
        # No open version, so there is no release to scope to and nothing to
        # name. The project's own totals under a heading that says "project" is
        # the honest thing left; a "Release tickets" heading with no version
        # would be the ambiguity this block exists to remove.
        row = _count_row(card.planned, card.in_progress, card.in_review, card.done)
        body = (
            f'<p class="flight">{row}</p>'
            if row
            else '<p class="flight quiet">No tickets on this project yet.</p>'
        )
        return f'<div class="tickets"><h4>Project tickets</h4>{body}</div>'

    version = esc(upcoming.version)
    row = _count_row(
        card.release_planned,
        card.release_in_progress,
        card.release_in_review,
        card.release_done,
    )
    board = f"{total} ticket{'' if total == 1 else 's'} on the project board"
    if row:
        # The project total rides along as a single qualified figure, plainly
        # labelled as the board's and not the release's, because "how is this
        # project doing" is still worth knowing on a dashboard.
        body = (
            f'<p class="flight">{row}</p><p class="flight quiet">{board} in total.</p>'
        )
    elif total:
        body = (
            '<p class="flight quiet">Nothing assigned to this version yet '
            f"&mdash; {board}, none of them attached to {version}.</p>"
        )
    else:
        body = '<p class="flight quiet">No tickets on this project yet.</p>'
    # **Release-scoped, and the heading names the version.** The owner asked for
    # this block to describe the release rather than the board (HS-574): "56
    # planned · 117 done" under `v1.10.0` was a specific and false claim about
    # that version, and a heading reading "Release tickets" without saying *which*
    # release just moves the same ambiguity one step along.
    #
    # This reverses an earlier deliberate decision to keep the counts project-wide
    # and merely label them "Project tickets" -- so it has now been weighed twice,
    # and here is what changed. The earlier reasoning was that release scope shows
    # `0 · 0 · 0 · 0`, since on real data almost no ticket carries a version at
    # all (BPAI: 180 tickets, 0 with a release; AT: 340 / 0; PF: 357 / 4). That is
    # true and those zeros are real -- but they are *information*: they mean
    # "nothing has been attached to this version yet", not "no work". So the zero
    # case says exactly that in words and prints the board's total beside it,
    # which keeps the project-wide figure available without ever letting a number
    # stand under a version it is not about.
    return (
        f'<div class="tickets"><h4>Release tickets &middot; {version}</h4>{body}</div>'
    )


def _release_panel(card: ProjectCard, org_ref: str, panel=None) -> str:
    """What this project is heading toward -- or, failing that, where it got to.

    An em-dash for a project that has plainly shipped things is worse than the
    stale row it replaced: it reads as "no releases" when the truth is "nothing
    planned yet". So with nothing upcoming, the panel shows the newest shipped
    version and says so.

    There is no "plan the next one" button: sync opens the next version as PLANNED
    when nothing is ahead of the high-water mark, so by the time anyone looks there
    is something to show. Blastoff still cuts the tag and creates the GitHub
    release; this is only the record of where the project is heading.

    The scrum summary rides in the same column, below the launch. It belongs
    here rather than in a panel of its own because both answer "where is this
    project right now?" -- and a full-width band under every card would push
    the next project off the screen.
    """
    scrum = _scrum_panel(panel, org_ref)
    release = card.next_release
    if release is not None:
        status = getattr(release.status, "value", release.status)
        name = f"<p>{esc(release.name)}</p>" if release.name else ""
        return (
            '<div class="launch"><h4>Next launch</h4>'
            f'<span class="ver">{esc(release.version)}</span>'
            f'<span class="pill {esc(status)}">'
            f"{esc(str(status).replace('_', ' '))}</span>"
            f"{_target_date_chip(release)}"
            f"{name}{_work_in_flight(card)}{scrum}</div>"
        )

    if card.latest_released is not None:
        shipped = card.latest_released
        when = (
            f" &middot; {esc(_iso(shipped.released_at))}" if shipped.released_at else ""
        )
        return (
            '<div class="launch"><h4>Latest release</h4>'
            f'<span class="ver">{esc(shipped.version)}</span>'
            f'<span class="pill released">released{when}</span>'
            f"{_work_in_flight(card)}{scrum}</div>"
        )

    return (
        '<div class="launch"><h4>Next launch</h4>'
        f'<span class="ver none">{EM_DASH}</span>'
        '<p class="quiet">Nothing on the pad yet.</p>'
        f"{_work_in_flight(card)}{scrum}</div>"
    )


def _copyable(command: str) -> str:
    """A shell command as selectable text, with a copy button on top.

    Same bargain as ``_init_command``: the text is the feature and the button is
    an enhancement, so a page with scripting off loses a convenience rather than
    the instruction itself.
    """
    return (
        '<span class="initcmd">'
        f"<code>{esc(command)}</code>"
        f'<button class="copybtn" type="button" data-copy="{esc(command)}" '
        f'title="Copy" aria-label="Copy {esc(command)}">{icons.COPY_SVG}</button>'
        "</span>"
    )


def _summary_prose(text: Optional[str], *, heading: Optional[str] = None) -> str:
    """Escaped paragraphs for a block of summary prose, or "" for nothing.

    Rendered as escaped paragraphs, not as markdown: parsing it would mean
    either a dependency or a hand-rolled parser, and either one turns prose
    somebody typed into a way to inject markup into a shared page. Shared by the
    generated summary and the human note so there is exactly one escaping path
    for the two -- they sit next to each other, and only one of them being
    sanitised would be a vulnerability rather than an inconsistency.
    """
    if not text or not text.strip():
        return ""
    head = f'<div class="sblock">{esc(heading)}</div>' if heading else ""
    return head + "".join(
        f'<p class="sbody">{esc(line)}</p>'
        for line in text.strip().splitlines()
        if line.strip()
    )


def _owner_bubble(label: Optional[str]) -> str:
    """A person as initials in a bubble, not as a full handle.

    Board handles are addresses (`george@havilandsoftware.com`) or logins
    (`dgillen27`), and a column of those beside ticket titles is most of the row's
    width spent on something the reader already knows. The full handle stays in
    the `title`, so nothing is lost -- it just stops being the loudest thing on
    the line.

    The unmapped marker survives as a ring on the bubble rather than the "(unmapped)"
    suffix: it is a state of the mapping, not part of the person's name, and it has
    to remain visible or the profile page's whole purpose goes unadvertised.
    """
    if not label:
        return ""
    display = label.lstrip("@")
    unmapped = "(unmapped)" in display
    display = display.replace(" (unmapped)", "").strip()
    # An address has no surname to take an initial from, so the local part stands
    # in -- `_initials` already does exactly this when handed no name.
    name = display if " " in display else ""
    initials = _initials(name, display)
    hint = f"{display} — not mapped to an InnoDay user" if unmapped else display
    return (
        f'<span class="obub{" unmapped" if unmapped else ""}" '
        f'title="{esc(hint)}">{esc(initials)}</span>'
    )


def _pr_icon(
    url: Optional[str],
    repo: Optional[str],
    *,
    state: Optional[str] = None,
    draft: bool = False,
    number: Optional[int] = None,
) -> str:
    """One repository's pull request, as a linked icon.

    A rejected URL still renders the icon rather than dropping the row's only
    trace of the pull request -- the same choice the old `repo · branch` line made,
    for the same reason: "there is a PR and we will not link to it" is different
    from "there is no PR".
    """
    where = repo or "a repository"
    label = f"#{number}" if number is not None else "pull request"
    detail = " (draft)" if draft else (f" ({state})" if state else "")
    href = safe_url(url)
    title = f"{where} — {label}{detail}"
    if href:
        return (
            f'<a class="cx on{" draft" if draft else ""}" href="{esc(href)}" '
            f'target="_blank" rel="noopener" title="{esc(title)}">'
            f"{icons.GITHUB_SVG}</a>"
        )
    return (
        f'<span class="cx on" title="{esc(title)} — link withheld">'
        f"{icons.GITHUB_SVG}</span>"
    )


def _connection_icons(row) -> str:
    """What this line is wired to: the board, and the code.

    Green when connected, grey when not -- the same convention the project card's
    integration icons already use, so one glyph means one thing across the page.
    The `|` separates the board from the repositories, because they answer
    different questions ("is this tracked?" and "did code ship for it?").

    **One icon per repository with a pull request**, which is what a ticket
    actually looks like: its code can land in three repos at once. That needed a
    ticket-to-PR join, which needed `RepositoryPullRequest.head_ref` -- the branch
    is the only thing on a pull request that names a ticket, and it was not stored
    (#579). `row.pull_requests` is that join.

    **Three sources, in order, because the join cannot see a merged release.** It
    is open pull requests only, so a shipped ticket matches nothing in it --
    `row.prs` is then what the summary actually recorded, and `row.pr_url` the
    single link an older stored line has. A row never loses the links it had.
    """
    board = safe_url(row.url)
    board_icon = (
        f'<a class="cx on" href="{esc(board)}" target="_blank" rel="noopener" '
        f'title="Open {esc(row.ticket_ref or "this ticket")} on the board">'
        f"{icons.LINEAR_SVG}</a>"
        if board
        else f'<span class="cx" title="Not linked to a board issue">{icons.LINEAR_SVG}</span>'
    )

    joined = list(getattr(row, "pull_requests", None) or [])
    stored = list(getattr(row, "prs", None) or [])
    if joined:
        code = "".join(
            _pr_icon(pr.url, pr.repo, draft=pr.is_draft, number=pr.number)
            for pr in joined
        )
    elif stored:
        # **The join is open pull requests only.** So a shipped release ticket --
        # every one of whose pull requests has merged by definition -- matched
        # nothing above and rendered as having no code at all, while the row it
        # came from held both links. The stored list is what the summary recorded
        # and does not drift as later pull requests land.
        code = "".join(
            _pr_icon(pr.get("url"), pr.get("repo"), number=pr.get("number"))
            for pr in stored
            if pr.get("url") or pr.get("repo")
        )
    elif row.pr_url:
        # The stored item's single PR: a summary written before `head_ref` existed
        # still has this, and dropping it would lose the row's only link.
        code = _pr_icon(row.pr_url, row.repo, state=row.pr_state)
    else:
        code = (
            f'<span class="cx" title="No pull request on this ticket">'
            f"{icons.GITHUB_SVG}</span>"
        )
    return f'<div class="cxrow">{code}<span class="cxsep">|</span>{board_icon}</div>'


def _summary_item(row) -> str:
    """One ticket's line: what it is, who owns it, and where the code went.

    Both URLs on this row are somebody else's data -- the ticket link came from
    a board sync, the PR link from a request body -- so both go through
    ``safe_url``, and a rejected one renders the same text without an anchor.
    """
    ticket_href = safe_url(row.url)
    ref = ""
    if row.ticket_ref:
        ref = (
            f'<a class="sref" href="{esc(ticket_href)}" target="_blank" '
            f'rel="noopener" title="Open {esc(row.ticket_ref)} on the board">'
            f"{esc(row.ticket_ref)}{icons.EXTERNAL_SVG}</a>"
            if ticket_href
            else f'<span class="sref">{esc(row.ticket_ref)}</span>'
        )

    owner = _owner_bubble(row.owner_label)

    # **No "Untitled".** The title lives on the ticket, so a line with no
    # `ticket_id` has none -- and that is every line of a narrated summary whose
    # author dropped the ids (see `SummaryService.resolve_narrated_items`, which
    # now recovers them). "Untitled" named nothing a reader could act on and read
    # as a rendering fault; the narrator's own sentence is directly below, and it
    # is what a person would call the line. So the slot is simply left empty.
    title = f'<span class="stitle">{esc(row.title)}</span>' if row.title else ""
    body = f'<p class="sbody">{esc(row.body_markdown)}</p>' if row.body_markdown else ""

    # A release line is four things: the ticket, a sentence a person can read,
    # who did it, and how it was judged. The first two were already here; these
    # are the other two, and they render only when the stored row has them --
    # every row written before the columns existed has neither.
    # Same five fields, same order, same words as the terminal and the release
    # note -- `src/services/summary_line.py` is the shape; this renders it in
    # HTML. Only the medium differs, never the layout.
    verdict = _verdict_pill(getattr(row, "verdict", None))
    people = _people_line(getattr(row, "people", None), row.owner_label)

    # `bps-api · refactor/BPAI-367-v1-types` used to sit here. The icons carry it
    # in less room and link to the same places: the branch name was the longest
    # string on the row and the least readable thing on it.
    meta_html = _connection_icons(row)

    return (
        f'<div class="sitem"><div class="sitem-top">{ref}{title}'
        f'<span class="grow"></span>{verdict}{owner}</div>'
        f"{body}{people}{meta_html}</div>"
    )


#: Verdict -> the class that colours it. Grouped by what a reader has to *do*
#: about it, not one colour per word: `shipped` needs nothing, `partly_merged`
#: needs chasing, a ticket with unmerged or no code needs a decision before the
#: release can claim it.
_VERDICT_CLASS = {
    "shipped": "shipped",
    "shipped_untagged": "shipped",
    "partly_merged": "partial",
    "not_merged": "missing",
    "no_code": "missing",
    "started_untagged": "partial",
    "not_started": "idle",
}


def _verdict_words(verdict: str) -> str:
    """`not_merged` -> `not merged`. Deferred to the shared formatter so the page
    and the terminal cannot spell one verdict two ways."""
    return summary_line.provenance(verdict=verdict)


def _verdict_pill(verdict: Optional[str]) -> str:
    """The stored verdict, or nothing at all.

    **Never derived here.** A row with no verdict predates the column, and
    guessing one from today's pull requests is precisely the recomputation that
    made a cut release read as though nothing had shipped. An unknown word still
    renders -- the vocabulary can grow server-side without this dropping a value
    on the floor -- it just gets the neutral colour.
    """
    if not verdict:
        return ""
    cls = _VERDICT_CLASS.get(verdict, "idle")
    label = _verdict_words(verdict)
    return f'<span class="sverdict {cls}">{esc(label)}</span>'


def _people_line(people: Optional[List[str]], owner_label: Optional[str]) -> str:
    """Everyone credited, when that is more than the one name already shown.

    A single name is already in the owner bubble, so repeating it under the line
    is noise -- this draws only when a ticket took more than one person, which is
    the case the bubble cannot represent at all.
    """
    names = [n for n in (people or []) if n]
    if len(names) < 2:
        return ""
    shown = ", ".join(esc(n) for n in names)
    return f'<p class="speople"><b>{shown}</b></p>'


def _summary_thin_block(label: str, rows: List[object]) -> str:
    """A trailing block: one compact line per row, under a small heading.

    A row with no ticket reference, no title and no owner has nothing to render,
    and an unassigned item with no ticket link is exactly that -- it used to emit
    an empty ``<div>``, which on a shared dashboard reads as a rendering fault
    rather than as the absence it is. Such rows are skipped, and a block left
    with none of them is not drawn at all rather than left as a bare heading.

    **The owner is a bubble here too, not a handle.** These rows used to print
    `row.owner_label` verbatim -- so the same person appeared as initials in the
    active rows and as `george@havilandsoftware.com` two blocks below, and the
    class it was printed under (``sowner``) had no stylesheet rule at all. One
    device for one thing: ``_owner_bubble`` is the device, and it keeps the full
    handle in the `title` exactly as it does above.

    **The prose counts as content here, exactly as it does above.** This block
    used to render only ref, title and owner -- so a line whose ticket was never
    identified showed as a bare name under a heading, and the narrator's sentence
    about it, the only thing on the row that said anything, was dropped. Nothing
    justified the asymmetry: these rows are shorter than the active ones because
    they matter less, not because they say less.
    """
    lines = []
    for row in rows:
        ref = (
            f'<span class="sref">{esc(row.ticket_ref)}</span> '
            if row.ticket_ref
            else ""
        )
        owner = f" {_owner_bubble(row.owner_label)}" if row.owner_label else ""
        # The ticket's title when there is one, else what the narrator wrote --
        # the same precedence `_summary_item` applies one block up.
        title = row.title or getattr(row, "body_markdown", None) or ""
        if not (ref or owner or title.strip()):
            continue
        lines.append(f'<div class="sthin">{ref}{esc(title)}{owner}</div>')
    if not lines:
        return ""
    return f'<div class="sblock">{esc(label)}</div>' + "".join(lines)


def _summary_empty(panel, org_ref: str) -> str:
    """Why the panel is empty, and the one thing that would fill it.

    Two different reasons, and the fix differs, so they are two different
    messages. The identity one wins when both apply: generating a summary you
    cannot be attributed in produces another empty box, so "map yourself" is
    the step that actually unblocks anything.

    **"Map your board handle" is only offered to someone who has none.** It used
    to appear whenever nothing on *this* project resolved to the viewer -- and
    identities are usually registered per project, so anyone with handles on two
    projects was told to map them on every other project in the org, by a link to
    a page that already listed them. There is nothing for that person to do:
    their handle simply is not on this board, which is a fact about the board.
    """
    if not panel.identity_mapped:
        if panel.handles_mapped:
            return (
                '<div class="sempty"><b>None of your handles are on this board</b>'
                "Your board handles are mapped, but none of them appears on this "
                "project&rsquo;s board &mdash; so nothing here can be shown as "
                "yours yet.</div>"
            )
        return (
            '<div class="sempty"><b>We can&rsquo;t attribute your work yet</b>'
            "No board handle on this project maps to you, so nothing here can be "
            "shown as yours. "
            f'<a href="{esc(profile_path(org_ref))}">Map your board handle</a>.'
            "</div>"
        )
    return (
        '<div class="sempty"><b>We haven&rsquo;t generated your summary yet</b>'
        "Summaries are written locally &mdash; run this from the project, and it "
        "will appear here for the whole team."
        f"{_copyable('innoday summary --scrum')}</div>"
    )


def _scope_toggle(panel, org_ref: str, base: Optional[str] = None) -> str:
    """Team / Yours, and only when there is a "Yours" to switch to.

    A link pair, not a control: the whole panel is server-rendered and the
    switch is a different URL for the same page. ``?you=<project>`` is scoped to
    one card, so switching one project's panel leaves the others alone.

    ``base`` is *which* page, and it has to be passed rather than computed: the
    panel renders on the dashboard and on the project page now, and a hardcoded
    ``dashboard_path`` sent anyone who clicked "Yours" on a project page back to
    the index -- the same page they had deliberately navigated away from.
    """
    if not panel.has_personal:
        return ""
    base = base or dashboard_path(org_ref)
    tabs = [
        ("Team", base, panel.scope == "team"),
        ("Yours", f"{base}?you={panel.project_id}", panel.scope == "yours"),
    ]
    links = "".join(
        f'<a{' class="on"' if on else ""} href="{esc(href)}"'
        f"{' aria-current="page"' if on else ''}>{label}</a>"
        for label, href, on in tabs
    )
    return f'<span class="scope">{links}</span>'


def _scrum_panel(panel, org_ref: str, base: Optional[str] = None) -> str:
    """The read-only scrum summary, under the launch panel.

    **No generate button.** Writing a summary means reading the project's
    boards and repositories and then narrating them, and the narration happens
    in the caller's Claude session -- there is no server-side LLM call to fire
    (see `src/routers/summaries.py`). A button that could only ever say "run
    this in your terminal" is a worse version of printing the command, which is
    what the empty state does.
    """
    if panel is None:
        return ""

    # The window is whatever the summary on show actually covers, not the one
    # the panel prefers. A team that summarises weekly used to be told "last 3
    # days" over a `week` summary, or shown nothing at all -- see
    # `data.PANEL_WINDOW_SPEC`.
    head = (
        '<div class="scrum-head"><h4>Scrum summary</h4>'
        f'<small class="quiet">{esc(panel.window_label)}</small>'
        f"{_scope_toggle(panel, org_ref, base)}</div>"
    )

    if panel.summary is None:
        return f'<div class="scrum">{head}{_summary_empty(panel, org_ref)}</div>'

    # The narrative first. It is the part a person wrote, it covers the whole
    # window rather than one row, and the items below are its evidence -- the
    # CLI prints it in the same position for the same reason. Rendered as
    # escaped paragraphs, not as markdown: parsing it would mean either a
    # dependency or a hand-rolled parser, and either one turns prose somebody
    # typed into a way to inject markup into a shared page.
    prose = _summary_prose(panel.summary.body_markdown)

    # A person's note, under its own heading. Labelled rather than merged into
    # the prose above for the same reason it is a separate column: the two have
    # different authors, and a reader who cannot tell them apart is being
    # misled about who said what. Escaped by the same helper as the prose -- one
    # escaping path, so a note can never be sanitised differently from the
    # summary it sits beside.
    note_heading = "Note"
    if panel.summary.notes_updated_at:
        # Dated for the same reason the CLI dates it: the note is inherited by
        # every regeneration, so without a date there is nothing to tell a
        # reader whether it still applies.
        note_heading = f"Note · {format_note_date(panel.summary.notes_updated_at)}"
    prose += _summary_prose(panel.summary.notes_markdown, heading=note_heading)

    body = "".join(_summary_item(row) for row in panel.active)
    # The rows were the only unlabelled run on the panel: the narrative above them
    # and both trailing blocks below say what they are, so a reader met the
    # tickets with nothing telling them these are the ones that moved. Same
    # `.sblock` device as those trailing blocks rather than a second heading
    # style -- they are peer sections of one panel, and only one of them was
    # named. Drawn only when there are rows under it, for the reason
    # `_summary_thin_block` gives: a heading over nothing is worse than none.
    if body:
        body = '<div class="sblock">Active Tickets</div>' + body
    elif not prose:
        body = '<p class="quiet" style="margin:0">Nothing active in this window.</p>'

    # The trailing blocks never consume an active slot: they answer a different
    # question ("what is *not* moving?") and letting them compete for the five
    # would hide the work that is.
    #
    # "No work detected" was the assembler's own column name and read, on a page,
    # as a claim that the project was idle -- when what it records is that one
    # ticket saw no *code* activity in the window. The heading now says that.
    # The window named, not referred to. "No activity in this window" assumed the
    # reader had connected it to the small caption in the panel heading; spelled
    # out, the block says what it means wherever it is read from.
    body += _summary_thin_block(
        f"No activity in the {panel.window_label}", panel.no_work
    )
    body += _summary_thin_block("Unassigned — work happening", panel.unassigned_active)

    # **No idle count and no "N of N shown".** Both were true and neither was
    # usable: the idle figure is the size of the unassigned backlog (221 tickets
    # on this repo's own project), which is a board-hygiene number that changes on
    # a different clock from a stand-up and told a reader nothing about the
    # window they were reading. "2 of 2 active shown" described the renderer's own
    # cap, which only ever matters when the two numbers differ -- and said it in
    # the one position on the panel a person looks for a conclusion.
    foot = []
    if panel.unmapped_count:
        plural = "s" if panel.unmapped_count != 1 else ""
        foot.append(
            f"{panel.unmapped_count} assignee{plural} unmapped &mdash; "
            f'<a href="{esc(profile_path(org_ref))}">map them</a>'
        )
    # Only when there is actually nothing to map. Someone whose handles *are*
    # registered, just not on this project's board, was being sent to a page
    # where their own handles were already listed -- see `_summary_empty`.
    if not panel.identity_mapped and not panel.handles_mapped:
        foot.append(
            f'<a href="{esc(profile_path(org_ref))}">we can&rsquo;t attribute '
            "your work yet</a>"
        )

    # The footer is drawn only when it has something to say. It used to always
    # carry a count, so the element was always there to hang the rest off.
    foot_html = f'<div class="sfoot">{" &middot; ".join(foot)}</div>' if foot else ""
    return f'<div class="scrum">{head}{prose}{body}{foot_html}</div>'


def _init_command(org_ref: str, project_alias: str) -> str:
    """The exact `innoday init` line for this project, with a copy button.

    The alias is lowercased on both halves. `WorkspaceOnboardService` resolves
    with `func.lower()` on both sides, so `hs/pf` and `hs/PF` are the same project
    -- and a command you can type without reaching for shift is the better default.

    The command is plain selectable text first; the button is an enhancement on
    top. That ordering matters because the clipboard API is the one thing on this
    page that needs JavaScript -- without it the command is still readable and
    selectable, which is how it worked before the button existed.
    """
    command = f"innoday init {org_ref.lower()}/{project_alias.lower()}"
    return (
        '<span class="initcmd">'
        f"<code>{esc(command)}</code>"
        f'<button class="copybtn" type="button" data-copy="{esc(command)}" '
        f'title="Copy" aria-label="Copy {esc(command)}">{icons.COPY_SVG}</button>'
        "</span>"
    )


def _pr_badge(repo, *, now: Optional[datetime] = None) -> str:
    """Open pull requests for a repo, linking to them on GitHub.

    Replaces a per-repo "last synced" that read `never synced` on every row --
    accurate, since repo sync had never run, and therefore telling nobody
    anything. Open PRs is the number people actually scan a repo list for, and
    the next thing anyone wants after reading it is to look at them.

    Links even at zero: "are there really none?" is a fair question, and the
    answer is one click away rather than a dead badge. It does not link when the
    count is None -- never counted -- because the number would be a claim the
    page cannot make. That distinction is the whole reason this replaced a column
    that flattened one.

    **The count carries its own age, because it is not continuously true (#650).**
    Nothing schedules a repository sync -- it runs when a human presses the sync
    pill or runs the CLI -- so the number here is only as current as the last
    press. A five-day-old `0 PRs` rendered exactly like a freshly-read one, and a
    teammate read it as "my pull requests have disappeared" when the truth was
    that nobody had looked since Tuesday. #641 gave the *project's* GitHub icon a
    red/grey/green state for the same blind spot but did not reach the counts, so
    the icon could go red beside a confident zero.

    **The age is `open_pr_counted_at`, and nothing else may stand in for it.** That
    column is written by `_refresh_open_pr_counts` alone, in the same place and on
    the same occasion as the count itself. An earlier draft of this badge read
    `last_synced_at` instead, which looks equivalent and is not: other code paths
    stamp that field without reading a single pull request, and the org-wide
    registration sync deleted by #658 stamped it on every
    repository in the org while leaving `open_pr_count` untouched. A five-day-old
    zero would then have rendered with a tooltip claiming it was "read 3 min ago" --
    a false provenance claim where previously there had only been a bare number,
    which is worse than the bug. So a count with no stamp of its own is treated as
    genuinely unknown-age, not dated from a neighbouring field.

    Two things make the number old, and they are said differently because the
    reader does different things about them:

    * **Nobody has counted lately** -- the age is appended
      ("0 PRs &middot; 5 days ago") and the badge takes the `stale` class.
    * **The last sync could not read *this* repo's pull requests** --
      `RepoRow.errored` is written by exactly one caller,
      `_refresh_open_pr_counts`, on precisely that failure, so the flag means "the
      count you are reading was not refreshed by the last attempt". The **age is
      still shown**, and it is the age of the count rather than of the failed
      attempt: without it, a repository whose GitHub grant lapsed in July reads
      identically to one that failed this morning -- staleness blindness in the one
      state where the count is guaranteed stale. The wording is
      "not refreshed", not "unread": `unread` is GitHub's own word for
      notifications nobody has looked at, and "2 PRs &middot; unread" reads as
      "two pull requests I have not reviewed".

    Staleness is `_freshness(...) == "cold"`, i.e. **over 24 hours** -- the same
    boundary the sync pill on this card already uses, reused rather than
    re-picked so one card cannot call itself cold beside an unqualified count.
    24h and not tighter for a specific reason: with no scheduler, a count read
    earlier today is the freshest anyone can have, and flagging *that* would flag
    every badge on the page and teach people to ignore the mark -- the failure
    mode #499 records for a flag that is only ever set. Beyond a day the number
    has stopped being current and become historical, which is the case that
    caused the report.

    A `None` count still renders the pre-existing "not counted yet" pill: that
    branch already refuses to claim a number, so there is no age to qualify.
    """
    if repo.open_pr_count is None:
        return '<span class="prs none" title="Not counted yet - run a sync"></span>'

    zero = repo.open_pr_count == 0
    count_label = (
        "0 PRs"
        if zero
        else ("1 PR" if repo.open_pr_count == 1 else f"{repo.open_pr_count} PRs")
    )
    count_title = (
        "No open pull requests" if zero else f"{repo.open_pr_count} open pull requests"
    )

    unread = bool(getattr(repo, "errored", False))
    counted_at = getattr(repo, "open_pr_counted_at", None)
    # `relative_time(None)` says "never synced", which is the one thing this badge
    # must not say: it is the phrase from the column this replaced, and beside a
    # non-`None` count it is a contradiction -- something counted these. So the
    # unknown case is named rather than dated.
    age = (
        relative_time(counted_at, now=now) if counted_at is not None else "age unknown"
    )
    cold = counted_at is None or _freshness(counted_at, now=now) == "cold"

    if unread:
        label = f"{count_label} · {age}, not refreshed"
        title = (
            f"{count_title} when the count was last read ({age}"
            f"{'' if counted_at is None else ', ' + _iso(counted_at)}). The last "
            f"sync could not read this repository's pull requests, so the number "
            f"was left as it was. Sync again to refresh it."
        )
    elif counted_at is None:
        label = f"{count_label} · age unknown"
        title = (
            f"{count_title} when something last counted them, but nothing "
            f"records when that was — so how current this is cannot be said. "
            f"Sync to establish it."
        )
    elif cold:
        label = f"{count_label} · {age}"
        title = (
            f"{count_title} when they were last counted, {age} "
            f"({_iso(counted_at)}). Nothing syncs on a schedule, so this "
            f"is how old the number is, not how many are open now."
        )
    else:
        label = count_label
        title = f"{count_title}, counted {age}"

    classes = "prs zero" if zero else "prs open"
    if unread or cold:
        classes += " stale"

    base = safe_url(repo.url)
    if not base:
        return f'<span class="{classes}" title="{esc(title)}">{esc(label)}</span>'

    # `.../pulls` is the repo's own PR list; GitHub filters to open by default.
    href = base.rstrip("/") + "/pulls"
    return (
        f'<a class="{classes}" href="{esc(href)}" target="_blank" rel="noopener" '
        f'title="{esc(title)} &mdash; open on GitHub">{esc(label)}</a>'
    )


def _layer_picker(org_ref: str, repo, return_to: str) -> str:
    """The layer chip, which is also how you change it.

    A ``<details>`` dropdown of one submit button per layer -- no JavaScript, and
    no separate "save" step. Each option posts the value, so changing a
    classification is one click on the thing you are looking at rather than a
    form somewhere else that names the repo again.
    """
    action = f"{UI_PREFIX}/{org_ref.lower()}/repos/{repo.id}/layer"
    options = []
    for layer in icons.selectable_layers():
        current = " on" if layer == repo.layer else ""
        options.append(
            f'<button class="lay-opt{current}" name="layer" value="{esc(layer)}" '
            f'type="submit" style="--h:{esc(icons.layer_hue(layer))}">'
            f'<span class="lay-dot"></span>{esc(icons.layer_label(layer))}</button>'
        )
    return (
        '<details class="laypick">'
        f'<summary class="layer" title="Change classification">'
        f"{esc(icons.layer_label(repo.layer))}</summary>"
        f'<form class="lay-menu" method="post" action="{esc(action)}">'
        f'<input type="hidden" name="return_to" value="{esc(return_to)}">'
        + "".join(options)
        + "</form></details>"
    )


def _bubbles(people, org_ref: str, *, cap: int = 5) -> str:
    """Who is working on this project, as overlapping initials.

    A link to the team page rather than a decoration: the bubbles are how you
    notice someone is missing, and the page is where you do something about it.

    Zero renders "No one mapped yet" pointing at the same place. An absent row
    and an empty team must not look alike -- one means nobody has been mapped,
    the other would mean the card forgot to draw it.
    """
    href = esc(team_path(org_ref))
    if not people:
        return (
            f'<a class="bubbles none" href="{href}" '
            'title="Nobody is mapped to this project yet">No one mapped yet</a>'
        )
    shown = people[:cap]
    extra = len(people) - len(shown)
    dots = "".join(
        f'<span class="bub" title="{esc(p.name)}">{esc(_initials(p.name, p.email))}</span>'
        for p in shown
    )
    more = f'<span class="bub more">+{extra}</span>' if extra > 0 else ""
    names = ", ".join(p.name for p in people)
    return f'<a class="bubbles" href="{href}" title="{esc(names)}">{dots}{more}</a>'


def _integration_icons(card: ProjectCard, *, now: Optional[datetime] = None) -> str:
    """What this project is wired to: GitHub, its board, and its own context.

    Three states ship. Grey means "not configured", green "configured and
    working", red "configured and broken" -- and **red beats green**, because an
    icon reading "connected" over a dead token is worse than no icon at all.

    Red is read from three columns, one per way a sync can fail: a per-repo
    `Repository.errored_at` (part of what you see could not be read),
    `BoardRegistration.errored_at`, and `Project.github_errored_at` (the sync
    itself died, which is the only thing left to read when discovery failed
    before any repo row existed -- #640). Each is set on failure and cleared on
    success, so NULL means the last attempt worked.

    An unconfigured integration renders a *greyed* icon rather than no icon.
    Omitting it would make "no board" and "board fine" differ only by an absence
    nobody counts -- and being able to see what is **not** set up is the whole
    reason the row exists.

    The detail goes in `title`, not on screen: three labelled chips in a card
    header is a second row of text, and the row has to survive beside the alias,
    the name, the init command and the sync pill.
    """
    parts: List[str] = []

    repos = len(card.repos)
    parts.append(
        _integration_icon(
            icons.GITHUB_SVG,
            on=card.github_connected,
            errored=card.github_errored,
            title=(
                f"GitHub · last sync failed — {card.github_error}"
                if card.github_errored and card.github_error
                # The generic branch stays: the per-repo path marks the
                # repository rather than the project, and `RepoRow` carries only
                # `errored: bool`, so there is no message to quote there.
                else "GitHub · last sync failed — check the organization's token"
                if card.github_errored
                else f"GitHub · {repos} repositor{'y' if repos == 1 else 'ies'}"
                if card.github_connected
                else "GitHub · no repositories linked"
            ),
        )
    )

    platform = card.board_platform
    parts.append(
        _integration_icon(
            icons.board_glyph(platform),
            on=platform is not None,
            errored=card.board_errored,
            title=(
                f"{str(platform).title()} · last sync failed — check the "
                "board's credential"
                if card.board_errored
                else f"{str(platform).title()} · synced "
                f"{relative_time(card.last_synced_at, now=now)}"
                if platform is not None
                else "Board · not connected"
            ),
        )
    )

    parts.append(
        _integration_icon(
            icons.DOC_SVG,
            on=card.has_context,
            title=(
                "Project context · generated"
                if card.has_context
                else "Project context · not generated yet"
            ),
        )
    )

    return f'<span class="intgs">{"".join(parts)}</span>'


def _integration_icon(
    glyph: str, *, on: bool, title: str, errored: bool = False
) -> str:
    """One status icon. The glyph never encodes the state -- the tile does.

    Keeping colour on the wrapper is what let red arrive (#499) as one extra
    class rather than a second set of SVGs to keep in step with the first.

    Red beats green: a configured-but-broken integration is *more* urgent than a
    working one, and an icon that showed "connected" while the token was dead
    would be worse than no icon at all.
    """
    state = " err" if errored else (" on" if on else "")
    return (
        f'<span class="intg{state}" title="{esc(title)}" '
        f'role="img" aria-label="{esc(title)}">{glyph}</span>'
    )


def _project_card(
    card: ProjectCard,
    org_ref: str,
    *,
    now: Optional[datetime] = None,
    panel=None,
    link: bool = True,
    return_to: Optional[str] = None,
    contributors=None,
    identity: bool = True,
) -> str:
    if card.repos:
        repo_rows = []
        for repo in card.repos:
            hue = icons.layer_hue(repo.layer)
            repo_href = safe_url(repo.url)
            name = (
                f'<a class="repo-name grow" href="{esc(repo_href)}" '
                f'target="_blank" rel="noopener">{esc(repo.name)}</a>'
                if repo_href
                else f'<span class="repo-name grow">{esc(repo.name)}</span>'
            )
            repo_rows.append(
                f'<div class="repo" style="--h:{esc(hue)}">'
                f'<span class="tile">{icons.layer_glyph(repo.layer)}</span>'
                f"{name}"
                f"{_layer_picker(org_ref, repo, return_to)}"
                f"{_pr_badge(repo, now=now)}"
                "</div>"
            )
        repos_html = "".join(repo_rows)
    elif card.archived_only:
        # **Not "no repositories linked yet".** There are repositories; every one
        # of them is archived. The old wording was the only thing this card said
        # about the case, and it said something false -- and it is the same
        # sentence a genuinely new project shows, which is precisely the
        # distinction `archived_only` exists to draw.
        repos_html = (
            '<p class="quiet" style="margin:0">Every repository on this project '
            "is archived.</p>"
        )
    else:
        repos_html = '<p class="quiet" style="margin:0">No repositories linked yet.</p>'

    fresh = _freshness(card.last_synced_at, now=now)
    when = relative_time(card.last_synced_at, now=now)
    # "synced never synced" reads badly; say it once.
    synced_label = when if card.last_synced_at is None else f"synced {when}"
    sync_action = f"{UI_PREFIX}/{org_ref.lower()}/projects/{card.id}/sync"
    # Where the card's two POSTs send the browser back to. The card is rendered
    # on more than one page now, and neither handler can work this out for
    # itself: `Referer` is optional and routinely stripped, so a handler that
    # trusted it would land people on the dashboard some of the time.
    return_to = return_to or dashboard_path(org_ref)

    # The alias and the name are the link; the sync pill and the init command are
    # not. Making the whole header one target would have swallowed both controls
    # that already live in it. `link=False` on the project page, where following
    # it would reload the page you are already on.
    # `identity=False` on the project page, where `_project_bar` above the shell
    # already carries the alias and name -- two copies a few pixels apart read as
    # a fault rather than as emphasis. The rest of the header (the init command,
    # the people, the integration icons, the sync control) is unaffected: those
    # are per-card controls, not identity.
    #
    # **A project is not selectable when every repository it has is archived.**
    # `card.archived_only` and not a scan of `card.repos`: that list has archived
    # rows filtered out before it gets here, so scanning it would answer "none are
    # archived" for the very project this is about. A card with no repos *at all*
    # stays a link -- nothing has been archived, it is simply new, and making the
    # empty case unreachable would strand a project at the moment it is created.
    if card.archived_only:
        link = False
    head = ""
    if identity:
        head = (
            f'<span class="alias">{esc(card.alias)}</span>'
            f'<span class="proj-name">{esc(card.name)}</span>'
        )
        if link:
            head = (
                f'<a class="projlink" href="{esc(project_path(org_ref, card.alias))}">'
                f"{head}</a>"
            )
        elif card.archived_only:
            # Say why it is not a link. An alias that silently stops responding to
            # a click is indistinguishable from a broken page.
            head += (
                '<span class="src" title="Every repository on this project is '
                'archived">archived</span>'
            )

    return f"""
<section class="proj">
  <span class="pixel"></span><span class="pixel b"></span>
  <div class="proj-head">
    {head}
    <span class="grow"></span>
    {_init_command(org_ref, card.alias)}
    {_bubbles(contributors or [], org_ref)}
    {_integration_icons(card, now=now)}
    <form method="post" action="{esc(sync_action)}" class="syncform">
      <input type="hidden" name="return_to" value="{esc(return_to)}">
      <button class="sync {fresh}" type="submit" title="{esc(_iso(card.last_synced_at))} &mdash; click to sync now"
              aria-label="Sync now"><span>{esc(synced_label)}</span>{icons.SYNC_SVG}</button>
    </form>
  </div>
  <div class="proj-body">
    <div class="repos">{repos_html}</div>
    {_release_panel(card, org_ref, panel)}
  </div>
</section>"""


def _token_panel(
    org: Organization,
    tokens: List[object],
    new_token: Optional[str],
    *,
    now: Optional[datetime] = None,
) -> str:
    """The CLI token panel: at most one token, created from the header.

    There is deliberately no name or expiry field. Both were free-text inputs on a
    form whose only real question is "do you want a token" -- and a name nobody
    chooses carefully is worse than one derived from the date, which at least sorts
    and dates itself. Creating replaces the previous token rather than stacking a
    new one beside it, so "which of these is my laptop using?" is never a question.
    """
    action = f"{UI_PREFIX}/{(org.alias or org.id).lower()}/tokens"
    create = (
        f'<form method="post" action="{esc(action)}" style="margin-left:auto">'
        f'<button class="cta sm" type="submit">'
        f"{'Replace token' if tokens else 'Create token'}</button></form>"
    )

    if tokens:
        token = tokens[0]
        expires = (
            _iso(token.expires_at) if token.expires_at else "Never"  # type: ignore[attr-defined]
        )
        body = (
            '<div class="tblwrap"><table><thead><tr><th>Name</th><th>Created</th>'
            "<th>Last used</th><th>Expires</th></tr></thead><tbody>"
            f'<tr><td class="nm">{esc(token.name)}</td>'  # type: ignore[attr-defined]
            f'<td class="num">{esc(_iso(token.created_at))}</td>'  # type: ignore[attr-defined]
            f'<td class="num">{esc(relative_time(token.last_used_at, now=now))}</td>'  # type: ignore[attr-defined]
            f'<td class="num">{esc(expires)}</td></tr>'
            "</tbody></table></div>"
        )
    else:
        body = (
            '<div class="mintrow" style="border-top:0"><p class="quiet" style="margin:0">'
            "No token yet. Create one to use the CLI or the MCP server.</p></div>"
        )

    reveal = ""
    if new_token:
        reveal = f"""
  <div class="reveal">
    <div class="rl">New token &mdash; copy it now</div>
    <div class="val">{esc(new_token)}</div>
    <div class="warn">This is the only time it will be shown, and it replaced any
    previous one. Store it in your password manager, then
    <code>export INNODAY_TOKEN=&hellip;</code></div>
  </div>"""

    return f"""
<section class="panel">
  <div class="panel-head">
    <h3>CLI tokens</h3>
    <small>Used by the innoday CLI and the MCP server to authenticate as you.</small>
    {create}
  </div>
  {body}{reveal}
</section>"""


def _signup_queue(org: Organization, requests: List[object]) -> str:
    """Pending access requests. Rendered only for platform members.

    Absent entirely when the queue is empty rather than showing an empty panel:
    for most people, most of the time, there is nothing here, and a permanent
    "0 pending" box is a box you stop reading.
    """
    if not requests:
        return ""

    base = f"{UI_PREFIX}/{(org.alias or org.id).lower()}/signup-requests"
    rows = []
    for r in requests:
        note = (
            f'<p class="reqnote">{esc(r.note)}</p>' if getattr(r, "note", None) else ""
        )
        rows.append(
            f'<div class="reqrow">'
            f'<div class="reqwho"><b>{esc(r.full_name)}</b>'
            f'<span class="quiet">{esc(r.email)}</span>{note}</div>'
            f'<form method="post" action="{esc(base)}/{esc(r.id)}/approve">'
            f'<button class="cta small" type="submit">Approve</button></form>'
            f'<form method="post" action="{esc(base)}/{esc(r.id)}/deny">'
            f'<button class="ghost small" type="submit">Deny</button></form>'
            f"</div>"
        )
    plural = "" if len(requests) == 1 else "s"
    return (
        f'<div class="seclabel">Access request{plural}</div>'
        f'<div class="panel">{"".join(rows)}</div>'
    )


def dashboard_page(
    user: User,
    org: Organization,
    orgs: List[Organization],
    cards: List[ProjectCard],
    tokens: List[object],
    *,
    new_token: Optional[str] = None,
    notice: Optional[tuple] = None,
    signup_requests: Optional[List[object]] = None,
    now: Optional[datetime] = None,
    panels: Optional[Dict[str, object]] = None,
    contributors: Optional[Dict[str, list]] = None,
) -> str:
    """The whole signed-in surface: projects, their repos, launches and tokens.

    ``panels`` maps project id -> ``data.SummaryPanel``. Optional, and absent
    means "render no scrum panels" rather than "render empty ones": the panel
    is a read of two more tables, and a caller that has not done that read has
    nothing to say, which is different from having read and found nothing.
    """
    notice_html = ""
    if notice:
        message, ok = notice
        notice_html = (
            f'<div class="syncnote {"ok" if ok else "err"}">{esc(message)}</div>'
        )
    if cards:
        panels = panels or {}
        projects_html = "".join(
            _project_card(
                c,
                org.alias or org.id,
                now=now,
                panel=panels.get(c.id),
                contributors=(contributors or {}).get(c.id),
            )
            for c in cards
        )
    else:
        projects_html = (
            '<div class="panel"><div class="mintrow" style="border-top:0">'
            '<p class="quiet" style="margin:0">No projects in this organization yet.'
            "</p></div></div>"
        )

    pane = f"""
  <div class="lblrow">
    <span class="seclabel">Projects</span>
    <span class="grow"></span>
    <a class="newproj" href="{esc(new_project_path(org.alias or org.id))}">+ New project</a>
  </div>
  {projects_html}
  {_token_panel(org, tokens, new_token, now=now)}"""

    body = f"""
<header class="topbar">{_wordmark()}{_user_menu(user, org, orgs)}</header>
<main>
  {notice_html}
  {_signup_queue(org, signup_requests or [])}
  {_shell(_app_nav(org, active="projects"), pane)}
</main>"""
    return _page(f"{org.name} · innoday", body)


# --------------------------------------------------------------------------- #
# Profile
# --------------------------------------------------------------------------- #


def _github_panel(user: User, org_ref: str) -> str:
    """The GitHub login, which is one field and one place.

    Writes ``users.github_username`` -- the *same* column
    ``PUT /api/v1/users/{id}/integrations`` writes, through the same
    ``User.update_integration_status`` method. Adding a second GitHub handle
    field here would have created two columns claiming the same fact, and
    nothing to say which one the summary engine reads.
    """
    action = f"{UI_PREFIX}/{org_ref.lower()}/profile/github"
    return f"""
<section class="panel">
  <div class="panel-head">
    <h3>GitHub</h3>
    <small>Your GitHub login, so commits and pull requests are attributed to you
    across every project.</small>
  </div>
  <div class="prow" style="border-top:0">
    <div class="prow-id"><b>GitHub login</b><em>github.com/&hellip;</em></div>
    <form class="pform" method="post" action="{esc(action)}">
      <input class="fld" name="github_username" type="text" autocomplete="off"
             spellcheck="false" placeholder="octocat"
             value="{esc(user.github_username or "")}" aria-label="GitHub login"/>
      <button class="cta sm" type="submit">Save</button>
    </form>
  </div>
</section>"""


def _identity_row(row, org_ref: str) -> str:
    """One project: how the board names you, and how to change it."""
    action = f"{UI_PREFIX}/{org_ref.lower()}/profile/identities"

    if row.platform is None:
        return (
            f'<div class="prow"><div class="prow-id"><b>{esc(row.project_alias)}</b>'
            f"<em>{esc(row.project_name)}</em></div>"
            '<span class="quiet">No board connected, so there is nothing to map '
            "yet.</span></div>"
        )

    state: List[str] = [f'<span class="plat">{esc(row.platform)}</span>']
    if row.handle:
        state.append(f'<span class="handle">{esc(row.handle)}</span>')
        if row.matched_by_email:
            # Named, not hidden: it is the one mapping nobody chose, so a person
            # who does not recognise the name needs to know where it came from
            # before they decide whether to replace it.
            state.append('<span class="badge">matched by email</span>')
        elif row.is_global:
            state.append(
                '<span class="badge grey" title="Your handle everywhere, not just '
                'this project">global</span>'
            )
    else:
        state.append('<span class="quiet">Not mapped</span>')

    # The picklist first, and the text field second. Auto-matching needs the
    # board to supply an email: Linear does, Jira usually does not, Trello never
    # does -- so picking your own name off the board's own list is the primary
    # path on most projects, not a fallback.
    picker = ""
    if row.candidates:
        buttons = "".join(
            f'<button name="handle" value="{esc(c["assignee"])}" type="submit">'
            f'{esc(c["assignee"])} <span class="n">{esc(c["ticket_count"])}</span>'
            "</button>"
            for c in row.candidates
        )
        picker = (
            f'<form class="pick" method="post" action="{esc(action)}">'
            f'<input type="hidden" name="project_id" value="{esc(row.project_id)}"/>'
            f'<input type="hidden" name="platform" value="{esc(row.platform)}"/>'
            '<span class="pick-lbl">Unmapped on this board &mdash; pick yours</span>'
            f"{buttons}</form>"
        )

    return f"""
<div class="prow">
  <div class="prow-id"><b>{esc(row.project_alias)}</b><em>{esc(row.project_name)}</em></div>
  {"".join(state)}
  <form class="pform" method="post" action="{esc(action)}">
    <input type="hidden" name="project_id" value="{esc(row.project_id)}"/>
    <input type="hidden" name="platform" value="{esc(row.platform)}"/>
    <input class="fld" name="handle" type="text" autocomplete="off" spellcheck="false"
           placeholder="Name on the board"
           aria-label="Board handle on {esc(row.project_alias)}"/>
    <button class="cta sm" type="submit">{"Change" if row.handle else "Map"}</button>
  </form>
  {picker}
</div>"""


def profile_page(
    user: User,
    org: Organization,
    orgs: List[Organization],
    rows: List[object],
    *,
    notice: Optional[tuple] = None,
) -> str:
    """Where a person tells InnoDay which board handles are theirs.

    Every mapping on this page exists to make one column truthful:
    ``ticket.assigned_to``. Until a handle resolves, a person's board work is a
    display string the summary engine can render but cannot attribute, which is
    what "@Name (unmapped)" means everywhere else in the UI.
    """
    notice_html = ""
    if notice:
        message, ok = notice
        notice_html = (
            f'<div class="syncnote {"ok" if ok else "err"}">{esc(message)}</div>'
        )

    if rows:
        identity_rows = "".join(_identity_row(row, org.alias or org.id) for row in rows)
    else:
        identity_rows = (
            '<div class="prow" style="border-top:0"><p class="quiet" style="margin:0">'
            "No projects in this organization yet.</p></div>"
        )

    pane = f"""
  <div class="seclabel">
    <a class="backlink" href="{esc(dashboard_path(org.alias or org.id))}">
    &larr; {esc(org.name)}</a>
  </div>
  {_github_panel(user, org.alias or org.id)}
  <section class="panel">
    <div class="panel-head">
      <h3>Board handles</h3>
      <small>Boards name people however they like. Tell us which name is you and
      your tickets, commits and summaries line up.</small>
    </div>
    {identity_rows}
  </section>"""

    # No nav row is marked current: the profile is reached from the org switcher
    # in the topbar, and neither Workflows nor Projects is the page you are on.
    body = f"""
<header class="topbar">{_wordmark()}{_user_menu(user, org, orgs)}</header>
<main>
  {notice_html}
  {_shell(_app_nav(org), pane)}
</main>"""
    return _page(f"Profile · {org.name} · innoday", body)


# --------------------------------------------------------------------------- #
# One project
#
# Five tabs in the shared left nav (`_app_nav`). The project's own state sits
# above them,
# unchanged from the card on the dashboard -- `_project_card(link=False)`, the
# same function, because two renderings of a project that could drift is a bug
# waiting rather than a design.
# --------------------------------------------------------------------------- #

PROJECT_TABS = ("you", "tickets", "releases", "timeline", "settings")


def _project_bar(card: ProjectCard) -> str:
    """The project's identity, above the whole shell, on every tab.

    **The point is that it does not move.** The alias and name used to live only
    inside the project card, which only the Project tab renders -- so clicking
    Tickets or Releases left a page with a menu, a list, and nothing saying which
    project any of it belonged to. On a surface where six projects look alike,
    that is the one thing a reader needs to stay oriented.

    Same `.alias` chip and `.proj-name` as the card, deliberately: continuity is
    the requirement, so this has to read as the same object the dashboard card
    showed, not as a second styling of the same fact. The card suppresses its own
    copy when this is on screen (`identity=False`), since two of them a few
    pixels apart reads as a rendering fault.

    Not a link. The Project tab is where it would go, that tab is one row away in
    the menu beside it, and a heading that navigates is exactly the confusion the
    removed "Project" label caused.
    """
    return (
        '<div class="projbar">'
        f'<span class="alias">{esc(card.alias)}</span>'
        f'<span class="proj-name">{esc(card.name)}</span>'
        "</div>"
    )


def _status_pill(status: str) -> str:
    """A ticket status as a chip. Unknown values render rather than disappear."""
    key = str(status).lower().replace("_", " ")
    css = {
        "in progress": "prog",
        "in review": "rev",
        "todo": "todo",
        "done": "done",
    }.get(key, "todo")
    return f'<span class="st {css}">{esc(key)}</span>'


def _my_tickets(rows, *, now: Optional[datetime] = None) -> str:
    """The viewer's active tickets. Full width, and all of them."""
    if not rows:
        return (
            '<section class="card"><header><h4>Your active tickets</h4></header>'
            '<div class="body"><p class="quiet" style="margin:0">'
            "Nothing on this project is assigned to you right now.</p></div></section>"
        )

    lines = []
    for row in rows:
        href = safe_url(row.url)
        ref = ""
        if row.ref:
            ref = (
                f'<a class="sref" href="{esc(href)}" target="_blank" rel="noopener" '
                f'title="Open {esc(row.ref)} on the board">'
                f"{esc(row.ref)}{icons.EXTERNAL_SVG}</a>"
                if href
                else f'<span class="sref">{esc(row.ref)}</span>'
            )
        lines.append(
            '<div class="trow">'
            f"{ref}"
            f'<span class="stxt grow">{esc(row.summary)}</span>'
            f'<span class="age">{esc(relative_time(row.updated_at, now=now))}</span>'
            f"{_status_pill(row.status)}"
            "</div>"
        )

    count = len(rows)
    return (
        '<section class="card"><header><h4>Your active tickets</h4>'
        '<span class="grow"></span>'
        f'<span class="src">{count} assigned to you</span></header>'
        f'<div class="body">{"".join(lines)}</div></section>'
    )


def _my_pull_requests(rows) -> str:
    """The viewer's open pull requests on this project.

    ``rows`` is None for "we cannot answer this yet", which is different from an
    empty list meaning "you have none open". Nothing in the schema records pull
    requests: `RepositoryIssue` is issues-only with no author field, and
    `_refresh_open_pr_counts` fetches every open PR object per repo and keeps
    only `len()`. Issue #500 persists them; until it does, the honest thing is a
    card that says so rather than an empty list that reads as "no open PRs" --
    which is a claim about your work that would be wrong for most people.
    """
    if rows is None:
        # No GitHub username on file, so "you have none open" cannot be claimed.
        # Absence of a handle is not absence of work.
        return (
            '<section class="card"><header><h4>Your open pull requests</h4>'
            '<span class="grow"></span>'
            '<span class="src">handle not set</span></header>'
            '<div class="body"><p class="quiet" style="margin:0">'
            "Add your GitHub username on your profile and your open pull "
            "requests will appear here.</p></div></section>"
        )
    if not rows:
        return (
            '<section class="card"><header><h4>Your open pull requests</h4></header>'
            '<div class="body"><p class="quiet" style="margin:0">'
            "Nothing open on this project&rsquo;s repositories.</p></div></section>"
        )
    lines = []
    for row in rows:
        href = safe_url(row.url)
        num = f"#{esc(row.number)}"
        number = (
            f'<a class="pnum" href="{esc(href)}" target="_blank" rel="noopener" '
            f'title="Open {num} on GitHub">{num}{icons.EXTERNAL_SVG}</a>'
            if href
            else f'<span class="pnum">{num}</span>'
        )
        draft = '<span class="st todo">draft</span>' if row.is_draft else ""
        lines.append(
            '<div class="trow">'
            f'<span class="rname">{esc(row.repo)}</span>'
            f"{number}"
            f'<span class="stxt grow">{esc(row.title)}</span>'
            f"{draft}"
            "</div>"
        )
    lines = "".join(lines)
    return (
        '<section class="card"><header><h4>Your open pull requests</h4>'
        f'<span class="grow"></span><span class="src">{len(rows)} open</span>'
        f'</header><div class="body">{lines}</div></section>'
    )


def _my_summary(panel, org_ref: str, alias: str) -> str:
    """The viewer's own scrum summary, beside their timeline.

    Reuses the dashboard's panel wholesale rather than re-rendering its rows: the
    empty states, the window label and the Team/Yours switch are all decisions
    already made there, and a second copy of them would be a second place for
    them to be made differently.
    """
    inner = _scrum_panel(panel, org_ref, base=project_path(org_ref, alias))
    if not inner:
        inner = '<p class="quiet" style="margin:0">No summary for this project yet.</p>'
    return f'<section class="card pane-scrum">{inner}</section>'


def _handle_row(identity, org_ref: str) -> str:
    """How the board knows the viewer, and one way to change it."""
    if identity is None or identity.platform is None:
        return ""
    if identity.handle:
        source = ("matched by email" if identity.matched_by_email else "claimed") + (
            " · global" if identity.is_global else ""
        )
        value = (
            f'<span class="chip">{esc(identity.platform)} &middot; '
            f'{esc(identity.handle)}</span><span class="src">{esc(source)}</span>'
        )
        action = "Change"
    else:
        value = (
            f'<span class="chip">{esc(identity.platform)}</span>'
            '<span class="src">no handle mapped yet</span>'
        )
        action = "Map"
    return (
        '<div class="handle"><span class="lbl">Board handle</span>'
        f'{value}<span class="grow"></span>'
        f'<a class="btn" href="{esc(profile_path(org_ref))}">{action} &rsaquo;</a></div>'
    )


def _you_pane(
    card: ProjectCard,
    org_ref: str,
    *,
    panel,
    identity,
    tickets,
    pull_requests,
    has_identity: bool,
    handles_mapped: bool = False,
    now: Optional[datetime] = None,
) -> str:
    """ "You": the project's state, then the viewer's own part in it.

    **One honest sentence beats four empty cards.** When nothing on this project
    can be attributed to the viewer, the whole band collapses to a single row
    pointing at the profile page. Rendering "Your summary" and "Your tickets" both
    empty would be two separate ways of saying the same thing, and neither would
    say what to do about it. This is the same
    reasoning ``_summary_empty`` already applies one level down.
    """
    project_block = _project_card(
        card, org_ref, now=now, link=False, panel=None, identity=False
    )

    if not has_identity:
        # The call to action only where there is one. Someone who has mapped their
        # handles and simply does not appear on *this* board is not being asked to
        # do anything -- see `_summary_empty` for the same distinction one level
        # down.
        action = (
            ""
            if handles_mapped
            else '<span class="grow"></span>'
            f'<a class="btn" href="{esc(profile_path(org_ref))}">'
            "Map your handle &rsaquo;</a>"
        )
        reason = (
            "Your board handles are mapped, but none of them appears on this "
            "project&rsquo;s board, so nothing here can be shown as yours."
            if handles_mapped
            else "You&rsquo;re not mapped to this project&rsquo;s board yet, so "
            "nothing here can be shown as yours."
        )
        return project_block + (
            '<div class="seclabel">You on this project</div>'
            '<section class="you"><div class="empty-you">'
            f"<span>{reason}</span>{action}"
            "</div></section>"
        )

    # No `.duo` wrapper any more: the summary was paired with a personal timeline,
    # and with that gone a two-column grid holding one card would leave the
    # right-hand half blank. Full width is the honest layout for one thing.
    return project_block + (
        '<div class="seclabel">You on this project</div>'
        f"{_handle_row(identity, org_ref)}"
        f"{_my_summary(panel, org_ref, card.alias)}"
        f"{_my_tickets(tickets, now=now)}"
        f"{_my_pull_requests(pull_requests)}"
    )


def _tab_placeholder(title: str, message: str) -> str:
    """An empty pane that says why it is empty.

    It began life as the stand-in for tabs that were routed but not yet built.
    **Every tab is built now**, and its remaining callers are genuine empty states
    -- a project with no releases, a board with no tickets. The old name and
    docstring outlived that, and read as though parts of the page were still
    scaffolding.
    """
    return (
        f'<section class="card"><header><h4>{esc(title)}</h4></header>'
        f'<div class="body"><p class="quiet" style="margin:0">{esc(message)}</p>'
        "</div></section>"
    )


#: Statuses worth a chip on a *planning* list. In progress and in test are the
#: ones that change how you plan -- work already moving is not work you assign
#: freely. Todo and backlog would be a chip on nearly every row, saying nothing.
LIVE_STATUSES = (TicketStatus.IN_PROGRESS.value, TicketStatus.IN_REVIEW.value)


def _live_status_pill(status) -> str:
    """A status chip, only for work already under way."""
    value = str(getattr(status, "value", status))
    return _status_pill(value) if value in LIVE_STATUSES else ""


def _release_pill(version: Optional[str]) -> str:
    """Which release a ticket is planned into, or nothing at all.

    Absent rather than "unassigned": on a list where most rows carry a version,
    the ones that do not are the exception, and a chip saying so on every other
    row would be the loudest thing on screen.
    """
    if not version:
        return ""
    return f'<span class="relpill">{esc(version)}</span>'


def _plan_button(
    row, target: Optional[str], base: str, return_to: str, label: str = ""
) -> str:
    """One click to plan a ticket into a release. Appears on hover.

    A form, not a link: it writes. Hidden until the row is hovered (and shown
    permanently on keyboard focus, or it would be unreachable without a mouse),
    because a button on every row of a two-hundred-row list is noise until you
    want it.

    Nothing renders when the ticket is already there, or when the project has no
    release to plan into -- an affordance that would fail is worse than none.
    """
    if not target or row.release == target:
        return ""
    return (
        f'<form class="planq" method="post" action="{esc(base)}/tickets/plan">'
        f'<input type="hidden" name="ticket_id" value="{esc(str(row.id))}">'
        f'<input type="hidden" name="release" value="{esc(target)}">'
        f'<input type="hidden" name="previous" value="{esc(row.release or "")}">'
        f'<input type="hidden" name="return_to" value="{esc(return_to)}">'
        f'<button type="submit" title="Plan into {esc(label or target)}'
        f' ({esc(target)})" aria-label="Plan into {esc(target)}">'
        f"{icons.PLAN_ARROW_SVG}"
        + (f'<span class="ptag">{esc(label)}</span>' if label else "")
        + "</button>"
        "</form>"
    )


def _status_filters(selected, base: str, release: Optional[str]) -> str:
    """A checkbox per status, submitting itself into the URL.

    GET, so the result is a link someone can send: the filter *is* the address.
    Ticked is the default for every status -- boxes that start cleared hide work
    without saying they have.

    No JavaScript. The submit button is the honest cost of that; the alternative
    is an onchange handler, and this page has managed without one so far.
    """
    boxes = []
    for status in data.STATUS_ORDER:
        value = status.value
        on = value in selected
        boxes.append(
            f'<label class="fbox{" on" if on else ""}">'
            f'<input type="checkbox" name="status" value="{esc(value)}"'
            f"{' checked' if on else ''}>"
            f'<span class="box">&check;</span>{esc(value)}</label>'
        )
    keep = (
        f'<input type="hidden" name="release" value="{esc(release)}">'
        if release
        else ""
    )
    return (
        f'<form class="filters" method="get" action="{esc(base)}/tickets">'
        f"{keep}{''.join(boxes)}"
        '<button class="fapply" type="submit">Apply</button>'
        "</form>"
    )


def _release_filters(board, base: str, active: Optional[str]) -> str:
    """Current and next release, as one-click filters at the top.

    Only the two slots. A dropdown of every version a project has ever shipped
    would be a list of history, and this is a planning surface -- the two
    questions worth one click are "what is going out" and "what is next".
    """
    if board is None:
        return ""
    chips = []
    for label, slot in (("Current", board.current), ("Next", board.planned)):
        if slot is None:
            continue
        version = slot.release.version
        on = active == version
        href = f"{base}/tickets" if on else f"{base}/tickets?release={quote(version)}"
        chips.append(
            f'<a class="rchip{" on" if on else ""}" href="{esc(href)}" '
            f'title="{"Clear this filter" if on else f"Only {version}"}">'
            f"{label} &middot; <b>{esc(version)}</b></a>"
        )
    if not chips:
        return ""
    allc = ' class="rchip on"' if not active else ' class="rchip"'
    chips.insert(0, f'<a{allc} href="{esc(base)}/tickets">All</a>')
    return f'<div class="rchips">{"".join(chips)}</div>'


def _tickets_pane(
    rows,
    limit: int,
    *,
    board=None,
    base: str = "",
    selected=(),
    release: Optional[str] = None,
    plan_target: Optional[str] = None,
    return_to: str = "",
) -> str:
    """Every live ticket on the project, grouped by status.

    Order is the pipeline reversed -- in test, in progress, todo, backlog, then
    done at the bottom -- and newest movement first inside each group. That answers
    "what is nearly out" before "what has not started", and keeps finished work as
    reference rather than as the top of a queue.
    """
    controls = _release_filters(board, base, release) + _status_filters(
        selected, base, release
    )

    if not rows:
        empty = (
            "No tickets match these filters."
            if (selected and len(selected) < len(data.STATUS_ORDER)) or release
            else "No tickets on this project yet. They arrive from the board on sync."
        )
        return (
            '<section class="card"><header><h4>Tickets</h4></header>'
            f'<div class="body">{controls}'
            f'<p class="quiet" style="margin:10px 0 0">{esc(empty)}</p>'
            "</div></section>"
        )

    lines = []
    last_rank = None
    for row in rows:
        rank = data.status_rank(row.status)
        if last_rank is not None and rank != last_rank:
            # A rule between groups. The status chips already name them, so a
            # heading per group would say everything twice.
            lines.append('<div class="statusgap"></div>')
        last_rank = rank

        owner = (
            f'<span class="sown">{esc(row.owner)}</span>'
            if row.owner
            else '<span class="sown quiet">unassigned</span>'
        )
        lines.append(
            '<div class="trow">'
            f"{_ticket_ref(row)}"
            f'<span class="stxt grow">{esc(row.summary)}</span>'
            f"{_release_pill(row.release)}"
            f"{_plan_button(row, plan_target, base, return_to)}"
            f"{owner}"
            f"{_status_pill(row.status)}"
            "</div>"
        )

    note = (
        f'<span class="src">showing the {limit} most recently updated</span>'
        if len(rows) >= limit
        else f'<span class="src">{len(rows)} tickets</span>'
    )
    return (
        '<section class="card"><header><h4>Tickets</h4>'
        f'<span class="grow"></span>{note}</header>'
        f'<div class="body">{controls}{"".join(lines)}</div></section>'
    )


def _ticket_ref(row) -> str:
    """A ticket's board reference, linked out where the board gave us a URL.

    A row with no usable URL renders as plain text rather than a dead anchor --
    the same fallback ``_tickets_pane`` and ``_my_tickets`` already apply, lifted
    here because the Releases tab needs it in two more places.
    """
    if not row.ref:
        return ""
    href = safe_url(row.url)
    if not href:
        return f'<span class="sref">{esc(row.ref)}</span>'
    return (
        f'<a class="sref" href="{esc(href)}" target="_blank" rel="noopener" '
        f'title="Open {esc(row.ref)} on the board">'
        f"{esc(row.ref)}{icons.EXTERNAL_SVG}</a>"
    )


def _backlog_card(
    rows,
    limit: int,
    orphaned=(),
    *,
    targets=(),
    base: str = "",
    return_to: str = "",
    done_unreleased=(),
    done_unreleased_total: int = 0,
) -> str:
    """Live work carrying no version: what a planner would draw from.

    Titles and references only. Status is deliberately absent here and present
    on the release side -- this list answers "what could go in", where a status
    chip is noise, while the release list answers "how far along is what is in",
    where it is the point.
    """
    if not rows:
        # Silent when there are orphans to show below: "every live ticket is
        # already assigned to a version" sitting directly above tickets assigned
        # to a version that does not exist would contradict itself.
        body = (
            ""
            if orphaned
            else '<p class="quiet" style="margin:0">Every live ticket is already '
            "assigned to a version.</p>"
        )
        note = ""
    else:
        body = "".join(
            _brow(
                row,
                _live_status_pill(row.status)
                # One arrow per slot: "into what is shipping" and "into what is
                # next" are different decisions, and one control could only mean
                # one of them.
                + "".join(
                    _plan_button(row, version, base, return_to, label=label)
                    for label, version in targets
                ),
                draggable=True,
            )
            for row in rows
        )
        # Just the count. "first 100" answered a question nobody had: the number
        # is what a reader wants, and naming the cap only invites "first 100 of
        # how many?" -- which this list cannot answer, since it stopped counting
        # at the cap.
        note = f'<span class="src">{len(rows)}</span>'
    # Work pointing at a version this project does not have. It belongs to no
    # slot and no release will ship it, so it would otherwise be absent from the
    # board entirely -- the one place someone would look for it. Kept in the same
    # card rather than given a third section: it is unplanned work, which is what
    # this card is, and it only differs in *why*.
    stale = ""
    if orphaned:
        stale = (
            '<div class="staleband">'
            + "".join(
                _brow(
                    row,
                    f'<span class="orphan" title="This project has no release '
                    f'{esc(row.release or "")}">{esc(row.release or "")}</span>',
                )
                for row in orphaned
            )
            + "</div>"
        )

    # Finished work nobody recorded against a release. A **labelled** band, unlike
    # the orphans above it: an orphan row carries the version it points at, which
    # explains itself, whereas a DONE ticket sitting in a planning pool looks like
    # a mistake until you are told why it is there. Same plan controls as the pool,
    # because the whole point is to attach it after the fact.
    done = ""
    if done_unreleased:
        shown = len(done_unreleased)
        count = (
            f"{shown} of {done_unreleased_total}"
            if done_unreleased_total > shown
            else str(shown)
        )
        done = (
            '<div class="doneband">'
            '<div class="bandhead"><h5>Done, never in a release</h5>'
            '<span class="grow"></span>'
            f'<span class="src" title="Completed before it was attached to any '
            f'version. Attach one to record where it shipped.">{esc(count)}</span>'
            "</div>"
            + "".join(
                _brow(
                    row,
                    "".join(
                        _plan_button(row, version, base, return_to, label=label)
                        for label, version in targets
                    ),
                )
                for row in done_unreleased
            )
            + "</div>"
        )

    return (
        '<section class="pool"><header><h4>Unassigned</h4>'
        f'<span class="grow"></span>{note}</header>'
        f"<div>{body}{stale}{done}</div></section>"
    )


def _bump_control(board, base: str, proposed: Optional[str]) -> str:
    """Move the pipeline onto a different version line.

    Two steps and no JavaScript: the parts are links that re-render the tab with
    a *proposal*, and only the confirm button writes. A one-click control here
    would rename the version every repo is about to be tagged with, and rewrite
    every ticket planned into it, on a misclick.

    There is no separate revert. Every option is recomputed from the last shipped
    version rather than from where the pipeline currently sits, so the parts are
    a toggle -- major then minor lands exactly back where it started, and the
    option the project is already on is simply the one marked current.
    """
    if not board.options or board.current is None:
        return ""

    if proposed is not None:
        option = next((o for o in board.options if o.part == proposed), None)
        if option is not None and not option.current:
            planned = (
                f' and <span class="pv">{esc(board.planned.release.version)}</span>'
                f' becomes <span class="pv">{esc(option.planned)}</span>'
                if board.planned is not None
                else ""
            )
            return (
                '<form class="bumpc" method="post" action="'
                f'{esc(base)}/releases/version">'
                f'<input type="hidden" name="bump" value="{esc(option.part)}">'
                '<p class="bumpq">Move this project onto the '
                f"<strong>{esc(option.part)}</strong> line? "
                f'<span class="pv">{esc(board.current.release.version)}</span> becomes '
                f'<span class="pv">{esc(option.version)}</span>{planned}. '
                "Tickets planned into them move too.</p>"
                '<button class="btn" type="submit">Confirm</button>'
                f'<a class="more" href="{esc(base)}/releases">Cancel</a>'
                "</form>"
            )

    links = []
    for option in board.options:
        if option.current:
            links.append(
                f'<span class="bump on" title="Where this project is now">'
                f"{esc(option.part)}</span>"
            )
        else:
            links.append(
                f'<a class="bump" href="{esc(base)}/releases?bump={esc(option.part)}"'
                f' title="Move to {esc(option.version)}">{esc(option.part)}</a>'
            )
    return f'<div class="bumps"><span class="bumplbl">Version line</span>{"".join(links)}</div>'


#: How many of a release's tickets show before the disclosure, and how many after.
#: Five is what fits without the slot becoming the page; twenty is enough to plan
#: against. Beyond that the Tickets tab is the right surface -- it has filters,
#: grouping and the whole list, and duplicating those here would be building a
#: second one badly.
SLOT_PREVIEW = 5
SLOT_EXPANDED = 20


def _brow(row, trailing: str = "", *, draggable: bool = False) -> str:
    """One planning-list row: reference, summary, then whatever the caller adds.

    The three lists on the Releases tab -- a release's tickets, the unassigned
    pool, and the orphans below it -- were three copies of the same two spans
    differing only in what trailed them. ``trailing`` is that difference; nothing
    else about a row varies.
    """
    drag = f' draggable="true" data-ticket="{esc(str(row.id))}"' if draggable else ""
    return (
        f'<div class="brow"{drag}>'
        f"{_ticket_ref(row)}"
        f'<span class="stxt grow">{esc(row.summary)}</span>'
        f"{trailing}</div>"
    )


def _slot_row(row) -> str:
    return _brow(row, _status_pill(row.status))


def _slot_tickets(slot, base: str) -> str:
    """A release's tickets: five, then twenty, then the Tickets tab.

    Newest movement first, which is why planning a ticket in puts it at the top
    without anything here arranging that -- the write touches ``updated_at`` and
    the ordering does the rest.

    The disclosure is a ``<details>``, so it opens and closes with no JavaScript
    and the closed state is the honest default rather than a collapsed list
    pretending to be complete. Its summary says how many more there are.
    """
    rows = list(slot.tickets)
    version = slot.release.version
    more_href = f"{base}/tickets?release={quote(version)}"

    head = "".join(_slot_row(row) for row in rows[:SLOT_PREVIEW])
    if len(rows) <= SLOT_PREVIEW:
        return head

    rest = rows[SLOT_PREVIEW:SLOT_EXPANDED]
    hidden = len(rows) - SLOT_PREVIEW
    beyond = len(rows) - SLOT_EXPANDED
    tail = "".join(_slot_row(row) for row in rest)
    if beyond > 0:
        tail += (
            f'<a class="more slotmore" href="{esc(more_href)}">'
            f"All {len(rows)} in Tickets &rsaquo;</a>"
        )
    else:
        tail += f'<a class="more slotmore" href="{esc(more_href)}">Open in Tickets &rsaquo;</a>'
    return (
        head + '<details class="slotrest"><summary>'
        f'<span class="chev">{icons.CHEVRON_SVG}</span>'
        f"{hidden} more</summary>{tail}</details>"
    )


def _target_date_chip(release) -> str:
    """The day a release is aimed at, beside the version it belongs to.

    **Nothing at all when unset.** This used to render "no date set", on the
    reasoning that a missing chip and a dateless release would otherwise look
    identical. True, and not worth the line: it appeared on every release of every
    project, which is a permanent label reporting the absence of something almost
    nobody sets. The picker sits directly below for anyone who wants to set one,
    so the absence is discoverable without being announced.

    Set, it reads in the version's own face rather than the chip style it used to
    have -- a date and a version are the same kind of fact about a release, and
    two typefaces for them made the date look like metadata about the version
    instead of a peer of it.
    """
    day = getattr(release, "target_date", None)
    if day is None:
        return ""
    return (
        f'<span class="tdate"><time datetime="{esc(day.isoformat())}">'
        f"{esc(format_target_date(day))}</time></span>"
    )


def _target_date_control(release, base: str, *, can_edit_release: bool) -> str:
    """A date picker for the release's target day -- admins only.

    A native `<input type="date">`, so the calendar, the locale and the keyboard
    handling are the browser's. This page ships one small script and no build
    step; a hand-rolled picker would be the largest thing on it.

    Non-admins get nothing rather than a disabled control: the chip above already
    says what the date is, and a greyed-out field only advertises a thing you
    cannot do. Shipped releases get nothing either -- the date they were aimed at
    is now history, and `released_at` is the fact that matters.
    """
    status = str(getattr(release.status, "value", release.status))
    if not can_edit_release or status == "released":
        return ""
    day = getattr(release, "target_date", None)
    return (
        f'<form class="dateq" method="post" action="{esc(base)}/releases/date">'
        f'<input type="hidden" name="version" value="{esc(release.version)}">'
        "<label>Target date"
        f'<input class="inp mini" type="date" name="target_date" '
        f'value="{esc(day.isoformat() if day else "")}">'
        "</label>"
        '<button class="ghost" type="submit">Save</button>'
        "</form>"
    )


def _slot_card(
    title: str,
    hint: str,
    slot,
    *,
    control: str = "",
    empty: str,
    base: str = "",
    can_edit_release: bool = False,
) -> str:
    """One of the pipeline's two forward slots, and the work in it.

    Both slots render through this. They are genuinely the same shape -- a
    version, a status, and the tickets carrying that version -- and the thing
    that distinguishes them is what the reader is being told to do with each,
    which is what ``title`` and ``hint`` carry.
    """
    if slot is None:
        return (
            f'<section class="card slot"><header><h4>{esc(title)}</h4></header>'
            f'<div class="body"><p class="quiet" style="margin:0">{esc(empty)}</p>'
            "</div></section>"
        )

    release = slot.release
    status = str(getattr(release.status, "value", release.status))
    name = f'<span class="src">{esc(release.name)}</span>' if release.name else ""
    # `notes` is the release engine's narrative and `description` the human one.
    # Whichever exists is shown; notes wins because a generated narrative only
    # exists once the release is genuinely being cut.
    prose = release.notes or release.description
    prose_html = f'<p class="rsum">{esc(prose)}</p>' if prose else ""

    if slot.tickets:
        tickets = _slot_tickets(slot, base)
    else:
        tickets = (
            '<p class="quiet" style="margin:0">Nothing is labelled '
            f"{esc(release.version)} yet.</p>"
        )

    return (
        f'<section class="card slot" data-release="{esc(release.version)}">'
        f"<header><h4>{esc(title)}</h4>"
        f'<span class="grow"></span>{name}</header>'
        '<div class="body">'
        '<div class="relnext">'
        f'<span class="ver">{esc(release.version)}</span>'
        f'<span class="pill {esc(status)}">'
        f"{esc(status.replace('_', ' '))}</span>"
        f"{_target_date_chip(release)}</div>"
        f'<p class="slothint">{esc(hint)}</p>'
        f"{_target_date_control(release, base, can_edit_release=can_edit_release)}"
        f"{control}{prose_html}{tickets}"
        "</div></section>"
    )


def _history_card(rows, *, limit: int) -> str:
    """What has shipped, newest first, each summary a click away.

    A ``<details>`` per release rather than ten summaries on the page: these are
    multi-paragraph narratives written for a client audience, and stacking them
    would bury the list they are attached to. Same no-JS idiom as the menu.
    """
    if not rows:
        return (
            '<section class="card"><header><h4>Released</h4></header>'
            '<div class="body"><p class="quiet" style="margin:0">'
            "Nothing shipped yet. Releases appear here once "
            "<code>innoday release</code> has cut one.</p></div></section>"
        )

    blocks = []
    for row in rows:
        meta = []
        if row.released_at:
            meta.append(esc(_iso(row.released_at)))
        if row.repo_count:
            plural = "" if row.repo_count == 1 else "s"
            meta.append(f"{row.repo_count} repo{plural}")
        if row.pr_count:
            plural = "" if row.pr_count == 1 else "s"
            meta.append(f"{row.pr_count} PR{plural}")
        head = (
            f'<span class="rver">{esc(row.version)}</span>'
            f'<span class="stxt grow">{esc(row.name or "")}</span>'
            f'<span class="rmeta">{" &middot; ".join(meta)}</span>'
        )
        if row.summary:
            blocks.append(
                f'<details class="rel"><summary>{head}</summary>'
                f'<p class="rsum">{esc(row.summary)}</p></details>'
            )
        else:
            blocks.append(f'<div class="rel"><div class="relhead">{head}</div></div>')

    note = (
        f'<span class="src">last {limit}</span>'
        if len(rows) >= limit
        else f'<span class="src">{len(rows)}</span>'
    )
    return (
        '<section class="card"><header><h4>Released</h4>'
        f'<span class="grow"></span>{note}</header>'
        f'<div class="body">{"".join(blocks)}</div></section>'
    )


def _slot_targets(board):
    """``(label, version)`` for each slot a ticket can be planned into."""
    out = []
    if board.current is not None:
        out.append(("current", board.current.release.version))
    if board.planned is not None:
        out.append(("next", board.planned.release.version))
    return out


def _releases_pane(
    board,
    *,
    history_limit: int = 10,
    base: str = "",
    proposed: Optional[str] = None,
    return_to: str = "",
    can_edit_release: bool = False,
) -> str:
    """Planning above, history below.

    Read-only, and the layout is the point: this is where drag and drop lands
    (issue #523 phase 2), so it is built now in the arrangement it will keep.
    **Two halves** -- the pool on the left, the two slots stacked on the right in
    the order work moves through them.

    Two halves rather than three columns, which is what this was first built as.
    The slots are a sequence, not three peers: stacking them says "this one, then
    that one", and the drag gesture becomes one direction (left to right) instead
    of a choice between two equally-placed targets. Each slot also gets the full
    half-width, which ticket titles need more than the pool does.

    They still have to be two separate targets. Dragging onto the current release
    adds work to what is being cut right now; dragging onto the next one defers
    it. An earlier version of this page showed only slot 1 and mislabelled it
    "Next release", which said the opposite of what it meant.
    """
    if board is None:
        return _tab_placeholder("Releases", "Nothing to show for this project yet.")
    return (
        '<div class="seclabel">Planning</div>'
        '<div class="planboard">'
        f"{_backlog_card(board.backlog, board.backlog_limit, board.orphaned, targets=_slot_targets(board) if can_edit_release else [], base=base, return_to=return_to, done_unreleased=board.done_unreleased, done_unreleased_total=board.done_unreleased_total)}"
        '<div class="stack">'
        f"{_slot_card('Current release', 'The version that ships next.', board.current, control=_bump_control(board, base, proposed) if can_edit_release else '', empty='Nothing in progress. A version opens on the next sync.', base=base, can_edit_release=can_edit_release)}"
        f"{_slot_card('Next release', 'New work goes here.', board.planned, empty='Nothing planned above the current release yet.', base=base, can_edit_release=can_edit_release)}"
        "</div>"
        "</div>"
        '<div class="seclabel">History</div>'
        f"{_history_card(board.history, limit=history_limit)}"
    )


def _timeline_pane(rows, *, now: Optional[datetime] = None) -> str:
    """The project's record, with the viewer's own entries marked."""
    if not rows:
        return _tab_placeholder(
            "Timeline",
            "Nothing recorded yet. Releases, board syncs and repository changes "
            "appear here as they happen.",
        )
    lines = "".join(
        '<div class="tl">'
        f'<span class="ago">{esc(relative_time(row.occurred_at, now=now))}</span>'
        f'<span class="dot {esc(row.event_type)}"></span>'
        f'<span class="ev grow">{esc(row.title)}</span>'
        + ('<span class="sown">you</span>' if row.is_yours else "")
        + "</div>"
        for row in rows
    )
    return (
        '<section class="card"><header><h4>Project timeline</h4>'
        f'<span class="grow"></span><span class="src">{len(rows)} entries</span>'
        f'</header><div class="body">{lines}</div></section>'
    )


def _settings_pane(card: ProjectCard, org_ref: str, project) -> str:
    """What this project is configured with, and the one thing editable here.

    Read-only apart from the repository layers, and that is the honest state of
    the app rather than a design choice: there is no endpoint to rename a
    project, change its topics or move its board from a page. Rendering inputs
    that post nowhere would be worse than showing the values and saying where
    they are actually changed.
    """
    rows = []
    for label, value in (
        ("Alias", card.alias),
        ("Name", card.name),
        ("Description", getattr(project, "description", "") or "—"),
        (
            "Board",
            f"{str(card.board_platform).title()} · connected"
            if card.board_platform
            else "Not connected",
        ),
        (
            "Repositories",
            f"{len(card.repos)} linked"
            if card.repos
            else "None linked — check the project's GitHub topic",
        ),
        (
            "Project context",
            "Generated" if card.has_context else "Not generated yet",
        ),
    ):
        rows.append(
            '<div class="setrow">'
            f'<span class="setlbl">{esc(label)}</span>'
            f'<span class="setval">{esc(value)}</span></div>'
        )

    layers = ""
    if card.repos:
        picker_rows = "".join(
            f'<div class="repo" style="--h:{esc(icons.layer_hue(repo.layer))}">'
            f'<span class="tile">{icons.layer_glyph(repo.layer)}</span>'
            f'<span class="repo-name grow">{esc(repo.name)}</span>'
            f"{_layer_picker(org_ref, repo, project_path(org_ref, card.alias) + '/settings')}"
            "</div>"
            for repo in card.repos
        )
        layers = (
            '<section class="card"><header><h4>Repository layers</h4>'
            '<span class="grow"></span>'
            '<span class="src">changes apply to this project only</span></header>'
            f'<div class="body repos">{picker_rows}</div></section>'
        )

    return (
        '<section class="card"><header><h4>Configuration</h4>'
        '<span class="grow"></span>'
        '<span class="src">read-only — change these from the CLI</span></header>'
        f'<div class="body">{"".join(rows)}</div></section>'
        f"{layers}"
    )


def project_page(
    user: User,
    org: Organization,
    orgs: List[Organization],
    card: ProjectCard,
    *,
    tab: str = "you",
    panel=None,
    identity=None,
    tickets=(),
    pull_requests=None,
    has_identity: bool = False,
    handles_mapped: bool = False,
    open_tickets: int = 0,
    all_tickets=(),
    ticket_limit: int = 200,
    release_board=None,
    release_history_limit: int = 10,
    selected_statuses=(),
    release_filter: Optional[str] = None,
    plan_target: Optional[str] = None,
    return_to: Optional[str] = None,
    proposed_bump: Optional[str] = None,
    can_edit_release: bool = False,
    full_timeline=(),
    project=None,
    notice: Optional[tuple] = None,
    undo: Optional[tuple] = None,
    now: Optional[datetime] = None,
) -> str:
    """One project, with its menu. ``tab`` selects the pane."""
    org_ref = org.alias or org.id

    if tab == "you":
        pane = _you_pane(
            card,
            org_ref,
            panel=panel,
            identity=identity,
            tickets=tickets,
            pull_requests=pull_requests,
            has_identity=has_identity,
            handles_mapped=handles_mapped,
            now=now,
        )
    elif tab == "tickets":
        pane = _tickets_pane(
            all_tickets,
            ticket_limit,
            board=release_board,
            base=project_path(org_ref, card.alias),
            selected=selected_statuses,
            release=release_filter,
            plan_target=plan_target if can_edit_release else None,
            return_to=return_to or "",
        )
    elif tab == "releases":
        pane = _releases_pane(
            release_board,
            history_limit=release_history_limit,
            base=project_path(org_ref, card.alias),
            proposed=proposed_bump,
            return_to=return_to or "",
            can_edit_release=can_edit_release,
        )
    elif tab == "timeline":
        pane = _timeline_pane(full_timeline, now=now)
    else:
        pane = _settings_pane(card, org_ref, project)

    notice_html = ""
    if notice:
        message, ok = notice
        # The undo rides in the notice rather than staying on the row: by the time
        # the page has re-rendered, the row has moved to wherever its new release
        # put it, so a control attached to it would be somewhere else on screen
        # from where the click happened.
        undo_html = ""
        if undo and ok:
            ticket_id, version = undo
            undo_html = (
                '<form class="undoq" method="post" action="'
                f'{esc(project_path(org_ref, card.alias))}/tickets/plan">'
                f'<input type="hidden" name="ticket_id" value="{esc(str(ticket_id))}">'
                f'<input type="hidden" name="release" value="{esc(version)}">'
                '<button type="submit">Undo</button></form>'
            )
        notice_html = (
            f'<div class="syncnote {"ok" if ok else "err"}">{esc(message)}'
            f"{undo_html}</div>"
        )

    body = f"""
<header class="topbar">{_wordmark()}{_user_menu(user, org, orgs)}</header>
<main>
  {notice_html}
  <a class="backlink" href="{esc(dashboard_path(org_ref))}">&lsaquo; Projects</a>
  {_project_bar(card)}
  {
        _shell(
            _app_nav(
                org,
                active=tab,
                project_alias=card.alias,
                open_tickets=open_tickets,
            ),
            pane,
        )
    }
</main>"""
    return _page(f"{card.alias} · {org.name} · innoday", body)


# --------------------------------------------------------------------------- #
# Creating a project
# --------------------------------------------------------------------------- #


def _topic_picker(preview, chosen, max_extra: int) -> str:
    """The topic list, with the alias locked and the rest selectable."""
    picked = {t.lower() for t in chosen}
    rows = []
    for option in preview.options:
        count = len(option.repos)
        label = f"{count} repositor{'y' if count == 1 else 'ies'}"
        if option.locked:
            rows.append(
                '<label class="topic locked">'
                '<span class="box">&check;</span>'
                f'<span class="tname">{esc(option.name)}</span>'
                '<span class="why">always included &mdash; it is the alias</span>'
                f'<span class="n">{esc(label)}</span></label>'
            )
            continue
        on = option.name in picked
        rows.append(
            f'<label class="topic{" picked" if on else ""}'
            f'{"" if count else " off"}">'
            f'<input type="checkbox" name="topic" value="{esc(option.name)}"'
            f"{' checked' if on else ''}>"
            f'<span class="box">&check;</span>'
            f'<span class="tname">{esc(option.name)}</span>'
            f'<span class="n">{esc(label)}</span></label>'
        )
    if not rows:
        return (
            '<p class="hint">No topics found on this organization&rsquo;s '
            "repositories. Tag a repo on GitHub and it will appear here.</p>"
        )
    return (
        f'<div class="topics">{"".join(rows)}</div>'
        f'<p class="hint">Up to {max_extra} extra, on top of the alias.</p>'
    )


def _repo_preview(preview) -> str:
    """Names, not a count -- a count cannot show you picked the wrong topic."""
    if not preview.included and not preview.archived:
        return (
            '<div class="preview none"><span class="ph">No repositories match yet'
            '</span><span class="hint">Pick a topic above, or tag repositories '
            "with the alias on GitHub.</span></div>"
        )
    chips = "".join(
        f'<span class="rchip">{esc(name)}</span>' for name in preview.included
    )
    archived = "".join(
        f'<span class="rchip gone">{esc(name)}</span>' for name in preview.archived
    )
    count = len(preview.included)
    note = (
        '<span class="hint">Struck through: archived on GitHub, so sync will not '
        "link them.</span>"
        if preview.archived
        else ""
    )
    return (
        f'<div class="preview"><span class="ph">{count} '
        f"repositor{'y' if count == 1 else 'ies'} would be included</span>"
        f'<div class="chips">{chips}{archived}</div>{note}</div>'
    )


def new_project_page(
    user: User,
    org: Organization,
    orgs: List[Organization],
    *,
    preview,
    values: Dict[str, str],
    chosen: List[str],
    max_extra: int,
    github_org: Optional[str],
    github_ok: bool,
    error: Optional[str] = None,
) -> str:
    """The create-a-project form.

    One form, two submit buttons. "Update preview" re-renders it with the repo
    list recomputed; "Create project" commits. Both are POSTs to the same route,
    which is what lets the preview round-trip without JavaScript and without
    losing anything already typed -- a GET-based preview would have had to carry
    every field in the query string, and a JS-based one would have made the whole
    form depend on scripting to be usable.
    """
    error_html = f'<div class="syncnote err">{esc(error)}</div>' if error else ""
    verified = (
        '<span class="ok">&check; Verified</span>'
        if github_ok
        else '<span class="warn">No GitHub credential for this organization</span>'
    )

    pane = f"""
  <a class="backlink" href="{esc(dashboard_path(org.alias or org.id))}">&lsaquo; Projects</a>
  <div class="seclabel">New project in {esc(org.name)}</div>
  <form class="card" method="post" action="{esc(new_project_path(org.alias or org.id))}">
    <div class="frow">
      <label for="np-name"><b>Name</b><span>What people call it.</span></label>
      <div class="fld"><input class="inp" id="np-name" name="name" required
             maxlength="255" value="{esc(values.get("name", ""))}"
             placeholder="Innoday"></div>
    </div>
    <div class="frow">
      <label for="np-alias"><b>Alias</b>
        <span>Ticket prefix, and the GitHub topic. Unique in this organization.</span></label>
      <div class="fld">
        <input class="inp mono short" id="np-alias" name="alias" required
               maxlength="10" value="{esc(values.get("alias", ""))}" placeholder="PF">
        <span class="hint">Tickets read <code>PF-412</code>; repositories tagged
          <code>pf</code> are picked up automatically.</span>
      </div>
    </div>
    <div class="frow">
      <label for="np-desc"><b>Description</b><span>One paragraph.</span></label>
      <div class="fld"><textarea class="inp area" id="np-desc" name="description"
             maxlength="2000"
             placeholder="What this project is for">{esc(values.get("description", ""))}</textarea></div>
    </div>
    <div class="frow">
      <label><b>GitHub</b><span>Where the repositories live.</span></label>
      <div class="fld">
        <span class="chip">{esc(github_org or "not configured")}</span>{verified}
      </div>
    </div>
    <div class="frow">
      <label><b>Topics</b><span>A repository carrying <em>any</em> of them belongs.</span></label>
      <div class="fld col">{_topic_picker(preview, chosen, max_extra)}</div>
    </div>
    <div class="frow">
      <label><b>Included</b><span>Recomputed when you update the preview.</span></label>
      <div class="fld col">{_repo_preview(preview)}</div>
    </div>
    <div class="actions">
      <button class="ghost" type="submit" name="intent" value="preview">Update preview</button>
      <span class="grow"></span>
      <a class="btn" href="{esc(dashboard_path(org.alias or org.id))}">Cancel</a>
      <button class="newproj" type="submit" name="intent" value="create">Create project</button>
    </div>
  </form>"""

    # The form is not a nav destination -- it is reached from the dashboard's
    # "+ New project" -- so no row is marked current.
    body = f"""
<header class="topbar">{_wordmark()}{_user_menu(user, org, orgs)}</header>
<main>
  {error_html}
  {_shell(_app_nav(org), pane)}
</main>"""
    return _page(f"New project · {org.name} · innoday", body)


# --------------------------------------------------------------------------- #
# The team
# --------------------------------------------------------------------------- #

_ROLE_BLURB = {
    "ADMIN": "manages members, settings and projects",
    "DEVELOPER": "syncs boards and manages tickets",
    "MEMBER": "reads tickets and summaries",
}


def _role_control(member, org_ref: str, *, can_admin: bool, last_admin: bool) -> str:
    """A member's role: a picker for an admin, a chip for everyone else.

    The last admin's picker is disabled **and** the server refuses the change.
    Only the second is a guarantee -- the first is a courtesy so nobody discovers
    the rule by being told no.
    """
    role = member.role.upper()
    if not can_admin:
        return f'<span class="rolechip {esc(role.lower())}">{esc(role.lower())}</span>'

    locked = last_admin and role == "ADMIN"
    if locked:
        return (
            f'<span class="rolechip {esc(role.lower())} locked" '
            'title="The last admin cannot be demoted — the org would have nobody '
            'who can add one">'
            f"{esc(role.lower())} &middot; locked</span>"
        )

    options = "".join(
        f'<button class="lay-opt{" on" if r == role else ""}" type="submit" '
        f'name="role" value="{esc(r)}">'
        f'<span class="lay-dot"></span>{esc(r.lower())}'
        f'<small class="quiet"> &mdash; {esc(_ROLE_BLURB[r])}</small></button>'
        for r in ("MEMBER", "DEVELOPER", "ADMIN")
    )
    action = f"{team_path(org_ref)}/members/{member.user_id}/role"
    return (
        '<details class="laypick rolepick"><summary>'
        f'<span class="rolechip {esc(role.lower())}">{esc(role.lower())} &#9662;</span>'
        "</summary>"
        f'<form class="lay-menu" method="post" action="{esc(action)}">{options}</form>'
        "</details>"
    )


def _member_row(member, org_ref: str, *, can_admin: bool, last_admin: bool) -> str:
    handles = "".join(
        f'<span class="hchip">{esc(h)}</span>' for h in member.board_handles
    )
    if member.github_username:
        handles += f'<span class="hchip gh">{esc(member.github_username)}</span>'
    if not handles:
        handles = '<span class="quiet" style="font-size:11px">no handles mapped</span>'

    remove = ""
    if (
        can_admin
        and not member.is_you
        and not (last_admin and member.role.upper() == "ADMIN")
    ):
        action = f"{team_path(org_ref)}/members/{member.user_id}/remove"
        remove = (
            f'<form method="post" action="{esc(action)}" class="inlineform">'
            '<button class="rm" type="submit" '
            'title="Remove from this organization">&times;</button></form>'
        )

    you = '<span class="youtag">you</span>' if member.is_you else ""
    return (
        '<div class="mrow">'
        f'<span class="bub">{esc(_initials(member.name, member.email))}</span>'
        f'<span class="mname">{esc(member.name)}{you}'
        f"<small>{esc(member.email)}</small></span>"
        f'<span class="handles">{handles}</span>'
        f'<span class="grow"></span>'
        f"{_role_control(member, org_ref, can_admin=can_admin, last_admin=last_admin)}"
        f"{remove}"
        "</div>"
    )


def _unmapped_panel(rows, members, org_ref: str, *, can_admin: bool) -> str:
    """Handles nobody owns, and a way to say who they are.

    **The point of this page.** A board or commit handle that maps to nobody is
    work that silently belongs to no one in every summary that follows -- and
    the person it belongs to usually cannot fix it themselves, because they
    cannot see a name they have never been shown.

    Mapping is reversible from here for the same reason: a wrong mapping
    reattributes somebody else's work indefinitely, so undoing it has to be as
    easy as doing it.
    """
    if not rows:
        return (
            '<section class="card"><header><h4>Unmapped handles</h4></header>'
            '<div class="body"><p class="quiet" style="margin:0">'
            "Every board and commit handle on this organization&rsquo;s work "
            "resolves to somebody. Nothing to do.</p></div></section>"
        )

    options = "".join(
        f'<option value="{esc(m.user_id)}">{esc(m.name)}</option>' for m in members
    )
    lines = []
    for row in rows:
        control = (
            f'<form method="post" action="{esc(team_path(org_ref))}/map" '
            'class="mapform">'
            f'<input type="hidden" name="kind" value="{esc(row.kind)}">'
            f'<input type="hidden" name="handle" value="{esc(row.handle)}">'
            f'<select name="user_id" class="inp mini">'
            f'<option value="">Who is this?</option>{options}</select>'
            '<button class="ghost" type="submit">Map</button></form>'
            if can_admin
            else '<span class="quiet" style="font-size:11px">an admin can map this</span>'
        )
        lines.append(
            '<div class="mrow">'
            f'<span class="kindchip {esc(row.kind)}">{esc(row.kind)}</span>'
            f'<span class="hchip">{esc(row.handle)}</span>'
            f'<span class="quiet" style="font-size:11px">{esc(row.detail)}</span>'
            '<span class="grow"></span>'
            f"{control}</div>"
        )
    return (
        '<section class="card"><header><h4>Unmapped handles</h4>'
        f'<span class="grow"></span><span class="src">{len(rows)} to resolve</span>'
        f'</header><div class="body">{"".join(lines)}</div></section>'
    )


def team_page(
    user: User,
    org: Organization,
    orgs: List[Organization],
    *,
    members,
    unmapped,
    can_admin: bool,
    last_admin: bool,
    notice: Optional[tuple] = None,
) -> str:
    """Who is in this organization, what they may do, and who is unmapped.

    **Org-scoped, and it says so.** `OrganizationMembership` has no project
    column, so this roster is the same whichever project you arrived from -- the
    bubbles on a card are a different thing (who is *working on* that project,
    derived from tickets and identities) and conflating the two would make one of
    them a lie.
    """
    notice_html = ""
    if notice:
        message, ok = notice
        notice_html = (
            f'<div class="syncnote {"ok" if ok else "err"}">{esc(message)}</div>'
        )

    invite = ""
    if can_admin:
        invite = f"""
    <form class="inviterow" method="post" action="{esc(team_path(org.alias or org.id))}/invite">
      <input class="inp" name="email" type="email" required placeholder="name@company.com"
             aria-label="Email to invite">
      <select class="inp mini" name="role" aria-label="Role">
        <option value="MEMBER">member</option>
        <option value="DEVELOPER">developer</option>
        <option value="ADMIN">admin</option>
      </select>
      <button class="newproj" type="submit">Send invite</button>
    </form>"""

    rows = "".join(
        _member_row(m, org.alias or org.id, can_admin=can_admin, last_admin=last_admin)
        for m in members
    )
    pane = f"""
  <a class="backlink" href="{esc(dashboard_path(org.alias or org.id))}">&lsaquo; Projects</a>
  <div class="seclabel">Team &mdash; {esc(org.name)}</div>
  <section class="card">
    <header><h4>Members</h4><span class="grow"></span>
      <span class="src">{len(members)} in this organization</span></header>
    <div class="body">{rows}</div>
    {invite}
  </section>
  {_unmapped_panel(unmapped, members, org.alias or org.id, can_admin=can_admin)}
  <p class="fine quiet">Roles and membership are organization-wide. The people
    shown on a project card are whoever is working on <em>that</em> project.</p>"""

    # Org-scoped, like the profile page, and reached from the same topbar menu --
    # so again no nav row is the current page.
    body = f"""
<header class="topbar">{_wordmark()}{_user_menu(user, org, orgs)}</header>
<main>
  {notice_html}
  {_shell(_app_nav(org), pane)}
</main>"""
    return _page(f"Team · {org.name} · innoday", body)
