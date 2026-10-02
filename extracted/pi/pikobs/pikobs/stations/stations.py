"""Station selection shared by the Pikobs modules.

``--id_stn`` takes several tokens, and each one is a separate series of
figures. The tokens have the same meaning everywhere:

* ``join``          every station merged into one figure
* ``all``           one figure per station, or per instrument type for the
                    codtyp families (ai, sf, ua, gp only)
* ``CAS`` / ``CAS*`` every station whose id starts with CAS
* ``C%``            SQL LIKE pattern, used as given
* ``=NENE``         exactly that station
* ``AMDAR (42)``    every station of that codtyp; for the codtyp families
                    a name also works (``pilot``, ``=TEMP``, ``temp_ship``)

A module turns the tokens into selectors once, then uses ``selector.sql()``
to filter its own table and ``selector.tag`` / ``selector.display`` to name
the files and the viewer entries::

    from pikobs.stations import parse_station_tokens, expand_station_selectors

    tokens = parse_station_tokens(args.id_stn)
    for sel in expand_station_selectors(db_paths, tokens, family,
                                        table='moyenne'):
        rows = conn.execute(f"SELECT ... WHERE varno = ?{sel.sql()}", (varno,))
"""

import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from pikobs.obsdb import open_result
from pikobs.configobs.special_family import (codtyp_label, DICT_CODTYP,
                                             has_codtyp_groups)


def _safe_filename(text: Any) -> str:
    return (str(text)
            .replace(' ', '_')
            .replace(':', '')
            .replace('/', '_')
            .replace('\\', '_')
            .replace('%', 'pct')
            .replace('*', '')
            .replace('=', '')
            .replace('"', '')
            .replace("'", ''))


def _sql_str(value: Any) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def _dedupe(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _query_distinct(db_paths: Sequence[str], sql: str,
                    params: Sequence[Any] = ()) -> List[tuple]:
    """Run sql on every database and return the ordered union of the rows."""
    seen: Dict[tuple, None] = {}
    for path in db_paths:
        if not os.path.isfile(path):
            continue
        try:
            with open_result(path) as conn:
                rows = conn.execute(sql, params).fetchall()
        except Exception as exc:
            print(f"[stations] query failed on {os.path.basename(path)}: "
                  f"{exc}", file=sys.stderr, flush=True)
            continue
        for r in rows:
            seen.setdefault(tuple(r), None)
    return list(seen)


_CODTYP_RE      = re.compile(r'\((\d+)\)\s*$')
_CODTYP_ONLY_RE = re.compile(r'^\(\d+\)$')


@dataclass(frozen=True)
class StationSelector:
    """One id_stn selection, i.e. one series of maps.

    kind:
        join    all stations merged
        station one station, produced by the ``all`` expansion
        prefix  ids starting with ``value``
        exact   exact id given as ``=VALUE``
        like    SQL LIKE pattern (token contains ``%``)
        codtyp  every station whose CODTYP is in ``codes``
    """
    kind:  str
    value: str
    codes: Tuple[int, ...] = ()
    label: str = ''

    @property
    def display(self) -> str:
        if self.label:
            return self.label
        if self.kind == 'prefix':
            return f'{self.value}*'
        if self.kind == 'exact':
            return f'={self.value}'
        if self.kind == 'station':
            return codtyp_label(self.value)
        return self.value

    @property
    def tag(self) -> str:
        if self.kind == 'prefix':
            return f'{_safe_filename(self.value)}_grp'
        if self.kind == 'exact':
            return f'{_safe_filename(self.value)}_eq'
        if self.kind == 'codtyp':
            return 'codtyp_' + '-'.join(str(c) for c in self.codes)
        return _safe_filename(self.value)

    @property
    def is_group(self) -> bool:
        return self.kind in ('join', 'prefix', 'like', 'codtyp')

    def sql(self) -> str:
        """SQL condition starting with ' AND ' (empty string for join).

        Valid on both the ``moyenne`` and ``stations`` tables.
        """
        if self.kind == 'join':
            return ''
        if self.kind in ('station', 'exact'):
            return f" AND id_stn = {_sql_str(self.value)}"
        if self.kind == 'prefix':
            return (f" AND substr(id_stn, 1, {len(self.value)}) = "
                    f"{_sql_str(self.value)}")
        if self.kind == 'like':
            return f" AND id_stn LIKE {_sql_str(self.value)}"
        if self.kind == 'codtyp':
            if len(self.codes) == 1:
                return f" AND CODTYP = {int(self.codes[0])}"
            return (" AND CODTYP IN ("
                    + ", ".join(str(int(c)) for c in self.codes) + ")")
        raise ValueError(f"Unknown selector kind: {self.kind}")


def _split_tokens(raw: Any) -> List[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        raw = [raw]
    toks: List[str] = []
    for item in raw:
        toks.extend(str(item).split())
    return toks


def parse_station_tokens(raw: Any) -> List[str]:
    """Normalise --id_stn into a token list.

    Whitespace-separated; a bare ``(42)`` is glued to the previous word so
    ``AMDAR (42)`` survives an unquoted shell expansion.
    """
    merged: List[str] = []
    for tok in _split_tokens(raw):
        if _CODTYP_ONLY_RE.match(tok) and merged and merged[-1] not in ('all', 'join'):
            merged[-1] = f"{merged[-1]} {tok}"
        else:
            merged.append('all' if tok == 'one_per_plot' else tok)
    return _dedupe(merged) or ['join']


def parse_channel_tokens(raw: Any) -> List[str]:
    toks = ['join' if t == 'one_per_plot' else t for t in _split_tokens(raw)]
    return _dedupe(toks) or ['join']


def _codtyp_name(code: int) -> str:
    """Instrument name of a codtyp (DICT_CODTYP may key by int or str)."""
    for key in (code, str(code)):
        name = DICT_CODTYP.get(key)
        if name:
            return str(name).strip()
    return str(code)


def _norm_name(text: str) -> str:
    """Case-insensitive name key; '_' stands for a space (PILOT_SHIP)."""
    return " ".join(str(text).replace('_', ' ').upper().split())


def _codtyp_single(code: int) -> StationSelector:
    return StationSelector('codtyp', str(code), (int(code),),
                           f"{_codtyp_name(code)} ({code})")


def _codtyp_group(token: str, codes: Sequence[int]) -> StationSelector:
    codes = tuple(sorted(int(c) for c in codes))
    if len(codes) == 1:
        return _codtyp_single(codes[0])
    return StationSelector('codtyp', token, codes,
                           f"{_norm_name(token)}* ({','.join(map(str, codes))})")


def _token_to_selector(tok: str) -> StationSelector:
    """Generic families: tokens refer to station ids."""
    if tok == 'join':
        return StationSelector('join', 'join')
    m = _CODTYP_RE.search(tok)
    if m:
        return StationSelector('codtyp', tok, (int(m.group(1)),), tok)
    if tok.startswith('=') and len(tok) > 1:
        return StationSelector('exact', tok[1:])
    if '%' in tok:
        return StationSelector('like', tok)
    if tok.endswith('*') and len(tok) > 1 and '*' not in tok[:-1]:
        return StationSelector('prefix', tok[:-1])
    return StationSelector('prefix', tok)


_RESOLUTION_LOGGED: set = set()


def _log_resolution(family: str, tok: str, text: str) -> None:
    key = (family, tok)
    if key not in _RESOLUTION_LOGGED:
        _RESOLUTION_LOGGED.add(key)
        print(f"[scatter] {family}: id_stn '{tok}' -> {text}")


def _codtyp_token_to_selector(tok: str, family: str,
                              present: Sequence[int]) -> StationSelector:
    """Codtyp families (ai, sf, ua, ...): tokens refer to instrument types.

    Resolution order:
      NAME (42) / (42)   codtyp 42
      42                 codtyp 42 if present, else station prefix
      =PILOT             codtyp named exactly PILOT, else station =PILOT
      C%                 SQL LIKE on id_stn
      pilot / PILOT*     every present codtyp whose name starts with PILOT,
                         else station prefix
    """
    m = _CODTYP_RE.search(tok)
    if m:
        sel = _codtyp_single(int(m.group(1)))
        _log_resolution(family, tok, sel.display)
        return sel

    if tok.isdigit() and int(tok) in present:
        sel = _codtyp_single(int(tok))
        _log_resolution(family, tok, sel.display)
        return sel

    if '%' in tok:
        return StationSelector('like', tok)

    if tok.startswith('=') and len(tok) > 1:
        name  = _norm_name(tok[1:])
        codes = [c for c in present if _norm_name(_codtyp_name(c)) == name]
        if codes:
            sel = _codtyp_group(tok[1:], codes)
            _log_resolution(family, tok, sel.display)
            return sel
        _log_resolution(family, tok, f"no codtyp named {tok[1:]}, "
                                     f"exact station id")
        return StationSelector('exact', tok[1:])

    stem  = tok[:-1] if tok.endswith('*') and len(tok) > 1 else tok
    codes = [c for c in present
             if _norm_name(_codtyp_name(c)).startswith(_norm_name(stem))]
    if codes:
        sel = _codtyp_group(stem, codes)
        _log_resolution(family, tok, ", ".join(
            f"{_codtyp_name(c)} ({c})" for c in sel.codes))
        return sel

    _log_resolution(family, tok, "no codtyp name matches, "
                                 "used as station id prefix")
    return StationSelector('prefix', stem)




# The families whose stations are aircraft, ships or ground stations by the
# thousand: for them ``all`` and the name tokens go by instrument type
# (codtyp). Every other family -- the radiances (csr included), ro, sw,
# sc -- has a station per satellite or platform, and ``all`` gives one
# figure per station. The same rule as obschain.
CODTYP_FAMILIES = ("ai", "sf", "ua", "gp")


def is_codtyp_family(family: str) -> bool:
    """ai, sf, ua, gp -- and their file names (ua_radiosonde, sf_synop)."""
    f = str(family or "").lower()
    return any(f == base or f.startswith(base + "_") for base in CODTYP_FAMILIES)


def _present_codtyps(db_paths: Sequence[str],
                     tables: Sequence[str] = ('stations', 'moyenne')
                     ) -> List[int]:
    rows = []
    for table in tables:
        rows = _query_distinct(
            db_paths,
            f"SELECT DISTINCT CODTYP FROM {table} WHERE CODTYP IS NOT NULL;")
        if rows:
            break
    return sorted({int(r[0]) for r in rows})


def expand_station_selectors(db_paths: Sequence[str],
                             stn_tokens: Sequence[str],
                             family: str,
                             table: str = 'moyenne'
                             ) -> List[StationSelector]:
    """Turn the --id_stn tokens into concrete selectors (``all`` expanded).

    For codtyp families (``is_codtyp_family``: ai, sf, ua, gp) ``all``
    gives one map per instrument type present in the data, and name
    tokens such as ``pilot`` select instrument types. ``table`` is the
    table holding id_stn / CODTYP, so other modules can reuse this.
    """
    codtyp_family = is_codtyp_family(family)
    tables = ('stations', table) if table == 'moyenne' else (table,)
    present = _present_codtyps(db_paths, tables) if codtyp_family else []

    out: List[StationSelector] = []
    for tok in stn_tokens:
        if tok == 'join':
            out.append(StationSelector('join', 'join'))
            continue

        if tok == 'all':
            if codtyp_family and present:
                out += [_codtyp_single(c) for c in present]
                continue
            rows = _query_distinct(
                db_paths,
                f"SELECT DISTINCT id_stn FROM {table} "
                f"WHERE id_stn != 'join';")
            out += [StationSelector('station', s)
                    for s in sorted({r[0] for r in rows if r[0] is not None})]
            continue

        if codtyp_family:
            out.append(_codtyp_token_to_selector(tok, family, present))
        else:
            out.append(_token_to_selector(tok))
    return _dedupe(out)
