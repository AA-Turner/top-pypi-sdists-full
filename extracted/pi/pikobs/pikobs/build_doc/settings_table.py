#!/usr/bin/env python
"""The Configuration tables of a module page, read from its wrappers.

A wrapper's USER SETTINGS block already holds everything a reader needs:
the groups (``# ---- Output ----``), every variable with its default, and
a comment above it that says what it is for. Reading them here keeps the
page in step with the wrapper: a new variable or a changed default shows up
at the next build, with nobody having to remember.

    from settings_table import settings_tables
    rst = settings_tables(["pikobs/script/run_zone_exp.sh",
                           "pikobs/script/run_zone_cont_exp.sh"])

Rules:
  * a group per ``# ---- Name ----`` line; the block ends at
    "Resolve the period" (internal code) or at the next numbered part;
  * one row per ``NAME=value``; "" and () show as empty;
  * the description is the first sentence of the comment above the
    variable, or its end-of-line comment when there is none above;
    variables sharing one comment share one row (DATESTART / DATEEND);
  * with two wrappers, one table: what only the comparison wrapper has
    starts with "Comparison only.", and a default that differs shows both.

    python settings_table.py pikobs/script/run_scatter_exp.sh pikobs/script/run_scatter_cont_exp.sh
"""
import re
import sys

GROUP = re.compile(r"^#\s*-{3,}\s*(?P<name>[^-].*?)\s*-{3,}\s*$")
ASSIGN = re.compile(r"^(?P<name>[A-Z][A-Z0-9_]*)=(?P<value>.*)$")
STOP = re.compile(r"^#\s*-{3,}\s*Resolve the period|^#\s*\d+\.\s+\S")


# The variables every wrapper shares get the same sentence on every page.
# A wrapper's own comment is used for everything else; a list written as the
# end-of-line comment of one of these (FAMILY, PROJECTION) is kept after it.
COMMON = {
    "PATH_CONTROL_FILES": "The control's directory of 6-h files YYYYMMDDHH_<family>.",
    "CONTROL_NAME": "The control's name in the titles and the viewer.",
    "PATH_EXPERIENCE_FILES": "One directory of 6-h files per experience.",
    "EXPERIENCE_NAME": "One name per experience directory, in the same order.",
    "PATH_FILES": "The directory of 6-h files.",
    "NAME": "Its name in the titles and the viewer.",
    "PATHWORK": "Where the figures, the databases and the viewer go; wiped family "
                "by family at every run. To open the viewer in a browser, link it "
                "once under ~/public_html (the wrapper prints the command).",
    "DATESTART": "YYYYMMDDHH UTC, both ends included; empty counts back from today. "
                 "The run stops first if a single 6-h file is missing.",
    "DATEEND": "The last cycle, YYYYMMDDHH UTC, included; empty counts back from today.",
    "DAYS_BACK_END": "Only with empty dates: how many days back the last cycle is.",
    "WINDOW_DAYS": "Only with empty dates: how many days the window covers.",
    "REGION": "Regions, one selector entry each; "
              "python pikobs/configobs/import_regions.py --list shows them all.",
    "FAMILY": "Observation families",
    "FLAGS_CRITERIA": "Quality-control criteria, one series of figures each.",
    "VARNOS": "A varno list; empty takes the family's.",
    "PROJECTION": "Map projection",
    "PRESSURE_LAYERS": "Layer edges in hPa for the pressure families (ua, ai, sw, ch); "
                       "empty keeps the whole column only.",
    "HEIGHT_LAYERS": "Layer edges in km for the height families (ro, radar).",
    "ID_STN": "Station tokens, one series of figures each; see Stations and channels.",
    "CHANNEL": "Channels or levels: join, all or explicit values; an explicit list "
               "is also the fastest.",
    "MATCH": "With a control: on compares the observations both runs hold, pair "
             "by pair; off keeps every observation and uses the independent tests.",
    "SVG": "on also writes every figure as SVG, to edit before a presentation.",
    "N_CPUS": "Dask workers; ask PBS for as many CPUs.",
}
LIST_AFTER = {"FAMILY", "PROJECTION"}


def _describe(name, comment, eol):
    if name in COMMON:
        d = COMMON[name]
        if name in LIST_AFTER and eol:
            d = f"{d}: {eol}"
        return d if d.endswith(".") else d + "."
    return _first_sentence(comment) if comment else eol


def _escape(text):
    return text.replace("\\", "\\\\").replace("*", "\\*").replace("`", "\\`").replace("|", "\\|")


def _split_value(raw):
    """(value, end-of-line comment) of the right-hand side of an assignment."""
    depth, quote = 0, None
    for i, c in enumerate(raw):
        if quote:
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "#" and depth == 0 and (i == 0 or raw[i - 1].isspace()):
            return raw[:i].strip(), raw[i + 1:].strip()
    return raw.strip(), ""


def _first_sentence(lines):
    """The first sentence of a comment block, stopping at its first list."""
    text = []
    for l in lines:
        if l.startswith("  ") and text:        # an indented list: stop
            break
        text.append(l.strip())
    s = " ".join(t for t in text if t)
    m = re.search(r"^(.+?[.:])(\s|$)", s)
    s = m.group(1) if m else s
    return s.rstrip(":").strip()


def read_settings(path):
    """[(group, [(names, default, description)])] of a wrapper."""
    lines = open(path).read().splitlines()
    # the numbered title of the block; a mention of it in the header above
    # ("only the USER SETTINGS block is meant to be edited") is not it
    starts = [i for i, l in enumerate(lines)
              if re.match(r"^#\s*\d+\.\s+USER SETTINGS", l)]
    if not starts:
        starts = [i for i, l in enumerate(lines) if "USER SETTINGS" in l]
    if not starts:
        return []
    start = starts[0]
    groups, group, comment, last = [], None, [], None
    for l in lines[start + 1:]:
        if STOP.match(l):
            break
        g = GROUP.match(l)
        if g:
            group = (g["name"], [])
            groups.append(group)
            comment, last = [], None
            continue
        if l.startswith("#"):
            body = l[1:]
            if body.startswith(" "):
                body = body[1:]
            if set(body.strip()) <= set("=-"):
                continue
            comment.append(body)
            last = None
            continue
        if not l.strip():
            if last is None:
                comment = []
            continue
        a = ASSIGN.match(l)
        if not a or group is None:
            continue
        value, eol = _split_value(a["value"])
        value = value.strip('"').strip("'")
        if value in ("", "()"):
            value = ""
        if last is not None and not comment and not eol and value == last[1]:
            last[0].append(a["name"])           # same comment, same default
            continue
        desc = _describe(a["name"], comment, eol)
        row = ([a["name"]], value, desc)
        group[1].append(row)
        last, comment = row, []
    return [g for g in groups if g[1]]


def _merge(single, compare):
    """One list of groups for a pair of wrappers."""
    if not compare:
        return [(g, [(n, v, None, d) for n, v, d in rows]) for g, rows in single]
    if not single:
        return [(g, [(n, v, None, d) for n, v, d in rows]) for g, rows in compare]
    s_rows = {tuple(n): (v, d) for _, rows in single for n, v, d in rows}
    out = []
    for g, rows in compare:
        merged = []
        for n, v, d in rows:
            key = tuple(n)
            if key in s_rows:
                sv, sd = s_rows[key]
                merged.append((n, sv, v if v != sv else None, sd or d))
            else:
                merged.append((n, v, None, f"Comparison only. {d}".strip()))
        out.append((g, merged))
    return out


SUITE = re.compile(r"/home/\w+/\.suites/\w+/(?P<suite>\w+)/.*?/banco/(?P<stage>\w+)/?$")


def _show(value):
    """A default as it reads best in a table cell."""
    v = value
    if v.startswith("(") and v.endswith(")") and " " not in v[1:-1]:
        v = v[1:-1]                              # a one-element array
    m = SUITE.match(v)
    if m:
        return f"{m['suite'].upper()} ``{m['stage']}``"
    v = re.sub(r"^/home/\$\{?USER\}?/", "~/", v)
    return f"``{v}``"


def settings_tables(wrappers):
    """RST for the Configuration section, from one or two wrapper paths
    (the single-run one first, then the comparison one)."""
    single = compare = []
    for p in wrappers:
        if "_cont_exp" in p:
            compare = read_settings(p)
        else:
            single = read_settings(p)
    out = []
    for group, rows in _merge(single, compare):
        out.append(f"**{group}**\n")
        out.append(".. list-table::\n   :header-rows: 1\n   :widths: 26 24 50\n")
        out.append("   * - Variable\n     - Default\n     - What it sets")
        for names, v, v_cmp, desc in rows:
            var = " / ".join(f"``{n}``" for n in names)
            default = _show(v) if v else "empty"
            if v_cmp is not None:
                default += f" ({_show(v_cmp)} to compare)" if v_cmp else " (empty to compare)"
            out.append(f"   * - {var}\n     - {default}\n     - {_escape(desc) or ' '}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


if __name__ == "__main__":
    print(settings_tables(sys.argv[1:]))
