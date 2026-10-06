"""What several modules select the same way: stations and their codtyp,
regions crossed with flags and surfaces, the special column of a family,
GPS-RO's reference profile, and a few SQL helpers to go with them.

It was in zone, and histogram and verifprofile took it from there with
private names: a change inside zone could break them. Here it has public
names and one home; zone, histogram and verifprofile import it alike.
"""
import os
import sys
from typing import Dict, List, Optional, Tuple

import pikobs
from pikobs.configobs import regionsobs
from pikobs.obsdb import open_result

# Which real stations a group stood for: a prefix such as C% is only a
# label in the sums, and the title of a figure should say what it held.
DDL_MEMBERS = """
    CREATE TABLE IF NOT EXISTS members (
        label TEXT, member TEXT, PRIMARY KEY (label, member)
    );
"""

class Selection:
    """A station selection of zone: a label, a SQL filter and a tag."""

    def __init__(self, label, sql, tag, display):
        self.label = label            # None: one group per station
        self._sql = sql
        self.tag = tag
        self.display = display

    def sql(self) -> str:
        return self._sql

def codtyp_case(column: str) -> str:
    """SQL that turns a codtyp into its label, e.g. 'AMDAR (42)'."""
    try:
        from pikobs.configobs.special_family import DICT_CODTYP
    except Exception:
        DICT_CODTYP = {}
    whens = " ".join(
        f"WHEN {int(code)} THEN '{str(name).replace(chr(39), '')} ({int(code)})'"
        for code, name in sorted(DICT_CODTYP.items(),
                                 key=lambda kv: int(kv[0])))
    return (f"(CASE CAST({column} AS INTEGER) {whens} "
            f"ELSE CAST({column} AS TEXT) END)")

def is_composite(family: str) -> bool:
    try:
        from pikobs.configobs.special_family import has_codtyp_groups
        return bool(has_codtyp_groups(family))
    except Exception:
        return False

def num(col: str) -> str:
    """The column when it holds a number, NULL otherwise.

    SQLite reads an empty string as 0 in any arithmetic, and it is not
    NULL, so a departure stored as '' would pass IS NOT NULL and be summed
    as a perfect zero. typeof() tells a real number from anything else.
    """
    return f"(CASE WHEN typeof({col}) IN ('real', 'integer') THEN {col} END)"

def is_num(col: str) -> str:
    return f"typeof({col}) IN ('real', 'integer')"

def distinct(path: str, table: str, sql: str) -> List[tuple]:
    if not os.path.isfile(path):
        return []
    try:
        with open_result(path) as conn:
            return conn.execute(sql).fetchall()
    except Exception as exc:
        print(f"[zone] query failed on {os.path.basename(path)}: {exc}",
              file=sys.stderr, flush=True)
        return []

def combinations(regions, flags, channels, land_oceans, vcoord_expr,
                  prefix: str = "") -> List[Dict[str, str]]:
    """Every selection of one pass, as a set of SQL conditions."""
    p = f"{prefix}." if prefix else ""
    combos = []
    for region in regions:
        latlon = regionsobs.criteria(region)
        if prefix:
            latlon = latlon.replace("lat", f"{p}lat").replace("lon", f"{p}lon")
        for flag in flags:
            flag_sql = pikobs.flag_criteria(flag)
            if prefix:
                flag_sql = flag_sql.replace("flag", f"{p}flag")
            for chan in channels:
                if chan in ('all', 'join'):
                    chan_sql = ""
                else:
                    chan_sql = f" AND {vcoord_expr} = {float(chan)}"
                for lo in land_oceans:
                    if lo == 'all':
                        lo_sql = ""
                    elif lo == 'land':
                        lo_sql = f" AND is_land_sql({p}lat, {p}lon) = 1"
                    else:
                        lo_sql = f" AND is_land_sql({p}lat, {p}lon) = 0"
                    combos.append({
                        'region': region, 'flag': flag, 'channel': chan,
                        'land_ocean': lo,
                        'cond': f"(1=1 {latlon} {flag_sql}{chan_sql}{lo_sql})",
                    })
    return combos

def selections(tokens, family: str = "") -> List[Selection]:
    """Turn the --id_stn tokens into selections.

    On a composite family a name such as ``pilot`` or ``AMDAR (42)``
    means an instrument type, resolved by the same code as scatter;
    anywhere else a token is a station id, a prefix or a pattern.
    """
    from pikobs.stations.stations import codtyp_token_to_selector as _codtyp_token_to_selector, token_to_selector as _token_to_selector
    composite = is_composite(family)
    try:
        from pikobs.configobs.special_family import DICT_CODTYP
        present = sorted(int(c) for c in DICT_CODTYP)
    except Exception:
        present = []
    out, seen = [], set()
    for tok in tokens:
        if tok in seen:
            continue
        seen.add(tok)
        if tok == 'all':
            out.append(Selection(None, "", "all", "all"))
            continue
        sel = None
        if composite and tok != 'join':
            try:
                sel = _codtyp_token_to_selector(tok, family, present)
            except Exception:
                sel = None
        if sel is None:
            sel = _token_to_selector(tok)
        out.append(Selection(sel.display, sel.sql(), sel.tag, sel.display))
    return out or [Selection("join", "", "join", "join")]

def station_select(label: Optional[str], family: str = "",
                    codtyp_col: str = "codtyp") -> Tuple[str, str]:
    """(SELECT expression, GROUP BY term) of the station column.

    ``None`` means one group per member (the token ``all``). For a
    composite family -- ai, sf, ua, gp, csr -- a member is an instrument
    type, found through codtyp: AMDAR and AIREP, PILOT and TEMP. Its
    ``id_stn`` is an aircraft or a single station, and one figure per
    aircraft would tell nothing. Any other label puts every matching row
    into a single group under that name, which is what ``join`` or a
    prefix ask for.
    """
    if label is None:
        if is_composite(family):
            return codtyp_case(codtyp_col), codtyp_col
        return "id_stn", "id_stn"
    safe = str(label).replace("'", "''")
    return f"'{safe}'", ""

def special(family: str, head_cols, enabled: bool,
             prefix: str = "") -> Tuple[str, str]:
    """(SELECT expression, GROUP BY term) of the family's special column.

    For ``sw`` that is WIND_COMP_METHOD, which separates the infrared from
    the water-vapour winds: two populations with different errors, whose
    sum would hide both. When it is off, or the column is not in the
    file, every row goes to the single value 'all'.
    """
    # the one definition, for every module
    from pikobs.configobs.special_family import special_select
    return special_select(family, head_cols, enabled, prefix)

def special_label(family: str, value) -> str:
    """IR / WV for sw, the raw value otherwise, 'all' when not split."""
    from pikobs.configobs.special_family import special_label
    return special_label(family, value)

def ro_ref(height):
    import math
    try:
        return 300.0 * math.exp(-float(height) / 6500.0)
    except (TypeError, ValueError, OverflowError):
        return None

def save_members(new_db: str, label: Optional[str], rows) -> None:
    """Record the stations behind a group label; duplicates are ignored."""
    if not label or label == 'join' or not rows:
        return
    try:
        with open_result(new_db) as out:
            out.execute(DDL_MEMBERS)
            out.executemany("INSERT OR IGNORE INTO members VALUES (?, ?)",
                            [(label, str(r[0])) for r in rows if r[0]])
    except Exception as exc:
        print(f"[zone] could not record the members of {label}: {exc}",
              file=sys.stderr, flush=True)
