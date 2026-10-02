"""Build the families.py and type_varno.py docstrings from the code itself.

    python build_config.py pikobs/configobs
"""
import os as _os_dw, sys as _sys_dw  # noqa: E401
_sys_dw.path.insert(0, _os_dw.path.dirname(_os_dw.path.abspath(__file__)))
from docwrite import write_docstring  # noqa: E402
import os
import re
import sys

import os
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
CONFIG = sys.argv[1]
sys.path.insert(0, os.path.abspath(os.path.join(CONFIG, '..', '..')))

def grid(headers, rows):
    cols = list(zip(*([headers] + rows)))
    widths = [max(len(c) for c in col) for col in cols]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def line(r):
        return "|" + "|".join(f" {c:<{w}} " for c, w in zip(r, widths)) + "|"

    out = [sep, line(headers), sep.replace("-", "=")]
    for r in rows:
        out += [line(r), sep]
    return "\n".join(out)


def image(name, alt):
    return (f".. image:: _static/{name}\n   :alt: {alt}\n"
            f"   :align: center\n   :width: 100%")



import re




from pikobs.configobs.families import (FAMILIES, VCOTYP_CHANNEL,
                                       VCOTYP_HEIGHT, VCOTYP_LATITUDE,
                                       VCOTYP_PRESSURE, VCOTYP_SURFACE,
                                       families_of_varno, family,
                                       level_summary)
from pikobs.configobs.type_varno import VARNOS

_KIND = {VCOTYP_CHANNEL: "channel", VCOTYP_PRESSURE: "pressure",
         VCOTYP_HEIGHT: "height", VCOTYP_LATITUDE: "latitude",
         VCOTYP_SURFACE: "surface"}


def family_table():
    """One row per instrument: its stage variants and its RARS broadcast
    together, when they share the vertical axis and the varnos."""
    rows, order = {}, []
    for names, cfg in FAMILIES.items():
        key = (_family_root(names[0]), cfg['VCOTYP'], cfg['ELEM'])
        if key not in rows:
            rows[key] = [[], cfg['FAM'], _KIND.get(cfg['VCOTYP'], cfg['VCOTYP']),
                         ", ".join(cfg['ELEM'].split(','))]
            order.append(key)
        rows[key][0] += [n for n in names if n not in rows[key][0]]
    out = [[f"``{rows[k][0][0]}``"] + rows[k][1:] for k in order]
    return grid(["Family", "Label", "Vertical", "Varnos"],
                out), len(out)


def _family_root(name):
    """The instrument a family name belongs to, without its stage ending:
    ua_qc -> ua, mwhs2_rars -> mwhs2, to_amsua_allsky -> to_amsua."""
    parts = name.lower().split("_")
    return "_".join(parts[:2]) if parts[0] == "to" and len(parts) > 1 else parts[0]


def level_table():
    """Every family, one row per instrument and vertical expression, with
    all its stage variants together."""
    rows, order = {}, []
    for names, cfg in FAMILIES.items():
        vcoord = " ".join(str(cfg['VCOORD']).split())
        key = (_family_root(names[0]), vcoord, cfg['VCOTYP'])
        if key not in rows:
            rows[key] = []
            order.append(key)
        for n in names:
            if n not in rows[key]:
                rows[key].append(n)
    out = []
    for key in order:
        names = rows[key]
        vcoord = key[1]
        if vcoord == "10":
            what = ("no vertical coordinate in the files: every observation "
                    "at 10 m, one level")
        elif vcoord == "9999":
            what = ("no vertical coordinate in the files: every observation "
                    "at the surface, one level")
        else:
            what = level_summary(names[0]).split(': ', 1)[1]
        out.append([f"``{names[0]}``", f"``{vcoord}``", what])
    return grid(["Family", "VCOORD", "What that gives"], out)


def codtyp_families_table():
    """The instrument types each family holds, from FAMILY_CODES."""
    from pikobs.configobs.special_family import DICT_CODTYP, FAMILY_CODES
    lines = [".. list-table::", "   :header-rows: 1", "   :widths: 12 88", "",
             "   * - Family", "     - Instrument types (codtyp)"]
    for fam in ("ai", "sf", "ua", "gp", "csr"):
        codes = FAMILY_CODES.get(fam, [])
        cells = ", ".join(f"{DICT_CODTYP.get(str(c), str(c))} ({c})" for c in codes)
        lines += [f"   * - ``{fam}``", f"     - {cells or '--'}"]
    return "\n".join(lines)


def _postalt_varnos():
    """{varno: families assimilating it}, {varno: families only carrying
    it}, from configobs/postalt_varnos.csv (make_varno_csv.py)."""
    import csv
    import os as _os
    path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                         "..", "configobs", "postalt_varnos.csv")
    assim, carried = {}, {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            target = assim if int(r["assimilated"]) > 0 else carried
            target.setdefault(int(r["varno"]), set()).add(r["family"])
    return assim, carried


def _cmc_names():
    """{code: (name, units)} from the CMC table B, when it can be read."""
    import os as _os
    for d in (_os.environ.get("PIKOBS_TABLE_B"),
              "/home/smco502/datafiles/constants"):
        p = _os.path.join(d or "", "table_b_bufr_e")
        if d and _os.path.isfile(p):
            out = {}
            for line in open(p, encoding="latin-1"):
                if line[:6].isdigit():
                    out[int(line[:6])] = (line[8:52].strip(), line[52:65].strip())
            return out
    return {}


def _cutoff_varnos():
    """{varno: families whose cutoff files hold it}, from
    configobs/cutoff_varnos.csv (make_cutoff_varnos.py); {} without it."""
    import csv
    import os as _os
    path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                         "..", "configobs", "cutoff_varnos.csv")
    out = {}
    if _os.path.isfile(path):
        with open(path, newline="") as fh:
            for r in csv.DictReader(fh):
                out.setdefault(int(r["varno"]), set()).add(r["family"])
    return out


def varno_table():
    """The observed BUFR codes: what postalt holds, what stays in cutoff."""
    assim, carried = _postalt_varnos()
    cutoff = _cutoff_varnos()
    cmc = _cmc_names()

    def fams(x):
        return ", ".join(f"``{f}``" for f in sorted(x)) or "--"

    def observed(code):
        # assimilated somewhere, or of a class of observed quantities (wind,
        # temperature, humidity, radiation, constituents, phenomena, radar,
        # ocean, satellite data); position, time, identification,
        # significance and quality describe an observation, they are not one
        return code in assim or code // 1000 in {11, 12, 13, 14, 15, 20, 21, 22, 40}

    def describe(code):
        key = str(code)                   # VARNOS is keyed by the code as text
        if key in VARNOS:
            label, units, axis = VARNOS[key]
            return (label.split(': ', 1)[1].title().replace('(Eccc)', '(ECCC)'),
                    units, axis)
        name, unit = cmc.get(code, ("", ""))
        return (name.title() if name else "not in the CMC table",
                f"[{unit.lower()}]" if unit else "--", "--")

    post, cut = [], []
    for code in sorted(c for c in set(assim) | set(carried) if observed(c)):
        name, units, axis = describe(code)
        post.append([f"``{code}``", name, units, axis, fams(assim.get(code, ())),
                     fams(carried.get(code, set()) - assim.get(code, set()))])
    for code in sorted(c for c in cutoff if observed(c)):
        lost = cutoff[code] - assim.get(code, set()) - carried.get(code, set())
        if lost:
            name, units, _ = describe(code)
            cut.append([f"``{code}``", name, units, fams(lost)])
    text = ("In postalt\n----------\n\n"
            + grid(["BUFR code", "Name", "Units", "Axis", "Assimilated in",
                    "In postalt, not assimilated"], post)
            + "\n\nIn cutoff, not in postalt\n-------------------------\n\n"
            + (grid(["BUFR code", "Name", "Units", "Arrives in the cutoff files of"], cut)
               if cut else "none."))
    return text, len(post) + len(cut)


def varno_carried():
    """The varnos the postalt files carry but no family assimilates: the
    variable when pikobs knows it, and the families it travels in."""
    assim, carried = _postalt_varnos()
    rows = []
    for code in sorted(c for c in carried if c not in assim):
        key = str(code)
        name = (VARNOS[key][0].split(': ', 1)[1].title() if key in VARNOS
                else "not in pikobs' list")
        rows.append([f"``{code}``", name,
                     ", ".join(f"``{f}``" for f in sorted(carried[code]))])
    if not rows:
        return "none."
    return grid(["Varno", "Variable", "In the files of"], rows)


def dbase_table():
    """The folders of dbase and the cutoff file each one becomes, one table
    per group, read from configobs/dbase_to_cutoff.csv."""
    import csv
    import os as _os
    path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                         "..", "configobs", "dbase_to_cutoff.csv")
    status_text = {"ok": "", "renamed": "renamed",
                   "merged": "several networks in one file",
                   "missing": "no cutoff file"}
    groups, order = {}, []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["group"] not in groups:
                groups[r["group"]] = []
                order.append(r["group"])
            what = "; ".join(t for t in (status_text.get(r["status"], r["status"]),
                                         r["note"].strip()) if t)
            groups[r["group"]].append((r["dbase"], r["cutoff"], what))
    out = []
    for g in order:
        out += [f"**{g}**", "", ".. list-table::", "   :header-rows: 1",
                "   :widths: 34 26 40", "",
                "   * - dbase", "     - cutoff", "     - Note"]
        for d, c, w in groups[g]:
            out += [f"   * - ``{d}``", f"     - ``{c}``" if c else "     - --",
                    f"     - {w or ' '}"]
        out.append("")
    return "\n".join(out).rstrip()


def chain_table():
    """The names of every family at each stage, cutoff to postalt, read
    from configobs/cutoff_to_postalt.csv (written by make_chain_csv.py)."""
    import csv
    import os as _os
    path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                         "..", "configobs", "cutoff_to_postalt.csv")
    stages = ("cutoff", "derialt", "evalalt", "bgckalt", "postalt")
    out = [".. list-table::", "   :header-rows: 1",
           "   :widths: 10 30 16 16 14 14", "",
           "   * - Family"] + [f"     - {s}" for s in stages]
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            out.append(f"   * - **{r['family']}**")
            for s in stages:
                names = r[s].split()
                out.append("     - " + (", ".join(f"``{n}``" for n in names) if names else "--"))
    return "\n".join(out)


FAMILIES_DOC = r"""
===========================================================
pikobs.configobs.families -- What to read, family by family
===========================================================

Every module starts the same way::

    FAM, VCOORD, VCOCRIT, STATB, ELEM, VCOTYP = pikobs.family('sw')

Those six values are the whole contract between a family and the rest of
pikobs: the label of the figures, the SQL expression of the vertical
coordinate, the extra criteria of the family, the column holding the bias
estimate, the varnos to read, and what kind of vertical axis it is.

The families
============

__FAMILY_TABLE__

One row per family, by the name ``FAMILY`` takes in a wrapper. The files it
has at each stage of the chain are in *From cutoff to postalt*, below.

A name is matched without regard to case, so ``sw_polaireDB`` and
``sw_polairedb`` are the same family. An unknown name raises an error
that lists the ones that exist, rather than failing later in someone
else's tuple unpacking.

RARS families -- the regional retransmission of an instrument -- share
the configuration of what they retransmit, so the table lists them with
it; in the figures they keep a label of their own (AMSU-A RARS), so a
figure never leaves in doubt which broadcast it shows.

From dbase to cutoff
====================

The files a module reads are the end of a chain. What arrives lands in
``dbase``, sorted by source -- ``remote/iasi``, ``surface/synop_b``,
``swob/ca`` -- and ``cutoff`` gathers it into the files the analysis
starts from, one per network: ``YYYYMMDDHH_sf_synop_b``. A ``_b`` marks
the BUFR broadcast of a network, no ``_b`` its text (TAC) broadcast; the
radiances all arrive in BUFR without saying it. From ``derialt`` on, the
networks of a family are joined -- ``ai_acars``, ``ai_amdar`` and the
others become ``ai``; the ``_qc`` files of ``evalalt`` carry the quality
control, and ``bgckalt`` and ``postalt`` hold the families the modules
read. A RARS broadcast keeps files of its own to the end -- ``mwhs2_rars``
next to ``mwhs2`` in postalt -- so it can be looked at apart from the
global data of its instrument.

__DBASE_TABLE__

The table lives in ``configobs/dbase_to_cutoff.csv``: a network that moves
is one line there.

From cutoff to postalt
======================

From ``cutoff`` on, every stage writes one file per name and cycle, and the
names of a family keep its start -- ``sf_synop_b`` in cutoff, ``sf`` in
postalt -- which is what puts them on one row below. The table is one cycle
of G2: ``cutoff`` and ``derialt`` from the banco of the suite, ``evalalt``,
``bgckalt`` and ``postalt`` from ``monitoring/banco``, the SQLite files the
modules read. It is written by ``pikobs/build_doc/make_chain_csv.py`` into
``configobs/cutoff_to_postalt.csv``; run it again when the chain changes.

__CHAIN_TABLE__

The vertical coordinate
=======================

``VCOORD`` is an expression, not a column. This is what makes a family
have twenty levels rather than three hundred thousand, and it is why a
module must always read the coordinate through it. The rounding is
chosen so that each family gets a number of levels that reads well in
the modules that group by the vertical -- profile, zone, verifprofile,
the layers of scatter: about twenty pressure levels, one per kilometre
of height, one per channel. Families whose files carry no vertical
coordinate get a constant: 10 for observations at 10 m, 9999 for the
surface.

__LEVEL_TABLE__

Rounding the pressure to 2000 Pa suits the troposphere, where most
conventional observations are: it gives about twenty levels between the
ground and 200 hPa. Above that the levels grow coarse in relative terms,
so a run that cares about the stratosphere is better served by a family
that keeps its coordinate -- ``ch`` does, and so does ``radar``.

Each module prints what it groups by when it starts:

.. code-block:: text

   [zone] ua: pressure, grouped by ROUND(VCOORD / 2000.) * 2000
   [profile] radar: height, grouped by VCOORD

``VCOTYP`` says what the coordinate means, and the modules read it rather
than guessing from the family: ``PRESSION`` is drawn with the ground at
the bottom, ``CANAL`` is a list of channels, ``SURFACE`` and ``LATITUDE``
have no vertical axis at all. Two helpers save repeating that test:
:func:`has_vertical_axis` and :func:`axis_is_inverted`.

Stations of ai, sf, ua, gp and csr
==================================

For these families the station id is not what you want to group by. The
tokens are read as instrument types (``CODTYP`` column, names from
``DICT_CODTYP``), without regard to case:

__CODTYP_FAMILIES__

A name matches every codtyp that *starts* with it: ``temp`` takes TEMP,
TEMP SHIP, TEMP DROP, TEMP MOBIL and the combined TEMP + PILOT types.
Use ``=TEMP`` or ``35`` for land radiosondes only. Spaces in names are
written ``_`` because bash splits on spaces. Only codtyps present in the
data are considered, and the log shows how each token was read:

.. code-block:: text

   [scatter] ua: id_stn 'pilot' -> PILOT (32), PILOT SHIP (33), PILOT MOBIL (34)
   [scatter] ua: id_stn 'CYUL' -> no codtyp name matches, used as station id prefix
   [scatter] WARNING ua: id_stn 'xyz*' matches no data for the selected channel(s), no map produced

Reading a family from code
==========================

.. code-block:: python

   from pikobs.configobs import families

   families.family('iasi')            # the six values
   families.family_varnos('ua')       # [11004, 11003, 12001, 12192]
   families.families_of_varno(12163)  # every family that reads it
   families.level_summary('ua')       # the line the modules print
   families.families()                # every name recognised
"""

VARNO_DOC = r"""
==================
BUFR codes (varno)
==================

A varno is the BUFR code of a physical variable in the observation
databases, and ``pikobs.configobs.type_varno`` is where pikobs reads it.
It decides the label of a figure, its units, and what its vertical axis
means::

    name, units, axis = pikobs.type_varno(11003)
    # '11003: U COMPONENT OF WIND', '[m/s]', 'Pressure [Pa]'

The codes are those of BUFR Table B of the WMO, master table 0, set out
in the `Manual on Codes, Volume I.2 (WMO-No. 306)
<https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes>`_.
The WMO also keeps `the current tables <https://wmo.int/latest-version>`_
online, in a form programs can read; where the two differ, the Manual
is the one that counts.

Look up a BUFR code
===================

Type a BUFR code (``12163``), a word in English or in French
(``brightness``, ``humidité``) or a family (``iasi``). The search gives
the name in both languages from the CMC table B, the unit, and the
families that assimilate the code or only carry it. A link can open it on
a code, as in ``varno.html?varno=12163``.

The families are read in two places of the chain. The postalt files, the
ones the modules read, say what is left at the end and what is
assimilated. The cutoff files say what arrives, and some of it is dropped
on the way: the bending angle of ``ro`` (``15037``) is in the cutoff files
and gone by derialt, where only the refractivity is kept. Such a code
shows under *Only in cutoff*. Only observed quantities count there -- wind,
temperature, humidity, radiation, constituents like the refractivity,
satellite data: the position, the time, the identification and the quality
flags of the cutoff files are not lost, they become columns of the postalt
header.

.. include:: varno_search.rst

BUFR codes in cutoff and postalt
================================

Two tables, of what is observed only: a code of position, time,
identification, significance or quality describes an observation
rather than being one, so it is left out -- it becomes a column of the
postalt header, or goes. The first table is what the postalt files hold
at the end: what is assimilated, and what is there but not assimilated.
The second is what arrives in the cutoff files and never reaches
postalt, family by family, like the bending angle of ``ro``.

The postalt part is read from the files, over the last day, each time
the documentation is built (``pikobs/build_doc/make_varno_csv.py``), so a
new code or a new family shows up by itself. The cutoff part takes
longer -- its files are BURP and are converted one by one -- so it is
read when the chain changes, with
``pikobs/build_doc/make_cutoff_varnos.py``, from one cycle; the families
of ``ch`` and ``asr`` are left out, their cutoff files do not convert. The axis is
the one pikobs draws the code against, ``--`` when pikobs has no use for
the code yet.

__VARNO_TABLE__

Reading a varno from code
=========================

An unknown code raises an error naming it and listing what is known,
which is what you want when a new instrument arrives with a variable
nobody has met yet.

.. code-block:: python

   from pikobs.configobs import type_varno as tv

   tv.type_varno(21014)          # label, units, axis
   tv.units_of(12163)            # '[K]'
   tv.axis_of(15036)             # 'Height [m]'
   tv.varnos()                   # every code known
"""

import re as _re

fam_table, n_fam = family_table()
var_table, n_var = varno_table()
fam_doc = (FAMILIES_DOC.replace("__CHAIN_TABLE__", chain_table()).replace("__DBASE_TABLE__", dbase_table()).replace("__FAMILY_TABLE__", fam_table)
                       .replace("__LEVEL_TABLE__", level_table())
                       .replace("__CODTYP_FAMILIES__", codtyp_families_table()))
var_doc = VARNO_DOC.replace("__VARNO_CARRIED__", varno_carried()).replace("__VARNO_TABLE__", var_table)
for doc in (fam_doc, var_doc):
    assert not _re.findall(r"__[A-Z_]+__", doc)
    assert '"""' not in doc


def write(path, doc):
    write_docstring(path, doc, __file__)


write(os.path.join(CONFIG, "families.py"), fam_doc)
write(os.path.join(CONFIG, "type_varno.py"), var_doc)
print(f"families.py: {n_fam} families, {fam_doc.count(chr(10))} lines")
print(f"type_varno.py: {n_var} varnos, {var_doc.count(chr(10))} lines")
