r"""
=================================================
pikobs.match -- Which observations are compared
=================================================

A comparison between two runs is only as honest as the sample behind it.
If the control kept a wind that the experience rejected, and the
experience kept another that the control never had, the two sigmas no
longer describe the same thing, and no statistical test can repair that
afterwards. So before anything is summed, every comparing module in
Pikobs pairs the two runs observation by observation and keeps only the
observations that both of them hold. The control departure :math:`x_i`
and the experience departure :math:`y_i` of the same observation then
travel together, and every statistic of the comparison is computed on the
same set of pairs :math:`\{(x_i, y_i)\}_{i=1}^{N}`.

Two records are taken to be the same observation when they agree on seven
fields: the station, the date, the time, the latitude and the longitude
rounded to 1e-4 degree (about ten metres, because two runs can write the
same position with a different last digit), the variable and the vertical
coordinate. The choice was not made by argument but by counting. Over the
global suites and all twenty families, among the observations that carry
a departure, that key never occurs twice. Remove the station and it stops
being unique in one family only: in the satellite winds about twenty
vectors per cycle share position, time and level, two platforms or two
producers seeing the same cloud. The station is what tells them apart, so
it stays in the key.

A key of one's own can repeat, and then the obvious join is wrong in one
of two ways. Dropping the repeated observations loses data silently;
joining them all with all multiplies them, two winds on each side giving
four pairs, each counted twice in every sum. Pikobs does neither. Inside a
repeated key the observations of each run are ranked by their observed
value, and the rank becomes part of the key. The same observation carries
the same value in both runs, so the first is paired with the first and
the second with the second, whatever order the files wrote them in; a
key that does not repeat gets rank one everywhere and nothing changes.
When that happens, the log says so once per family -- on one day of
satellite winds paired without the station, for instance, 21 repeated
keys in the control and 15 in the experience -- so that a key which is
not enough never passes unnoticed.

In a wrapper the choice is a single line. ``MATCH="on"`` pairs on the key
above and is what a comparison should almost always use. ``MATCH="off"``
does not pair at all: each run is summarised with all of its own
observations, and the change is tested as between two independent
samples. That is the only option when the two runs cannot share their
observations, a different thinning for instance, and it is far less
sensitive, for reasons the page on the significance of a change sets out
with numbers. A list of field names, such as ``MATCH="lat lon date time
varno vcoord"``, pairs on those fields and nothing else.

What the pairs buy is the whole point. Two runs of the same suite agree
on nearly every observation: the observed value is the same, the
background almost the same, and their departures correlate at 0.9999.
Paired, a test measures what differs against everything the runs share,
and a small, steady change becomes visible. Unpaired, the same change is
lost in the sigma that both runs carry. How large that difference is, on
a real experiment, is in :doc:`stats`.
"""

from typing import Dict, Iterable, List, NamedTuple, Optional, Sequence, Tuple, Union

DEFAULT_KEY: Tuple[str, ...] = ('id_stn', 'date', 'time', 'lat', 'lon',
                                'varno', 'vcoord')

# field -> SQL expression, {h} the header alias, {d} the data alias.
# lat and lon are rounded as every module did: the same position can be
# written with a different last digit by two runs.
FIELDS: Dict[str, str] = {
    'id_stn': "{h}.id_stn",
    'date':   "{h}.date",
    'time':   "{h}.time",
    'lat':    "ROUND({h}.lat, 4)",
    'lon':    "ROUND({h}.lon, 4)",
    'codtyp': "{h}.codtyp",
    'varno':  "{d}.varno",
    'vcoord': "{d}.vcoord",
}

RANK = 'k_rank'


class MatchSpec(NamedTuple):
    enabled: bool
    fields: Tuple[str, ...]

    @property
    def label(self) -> str:
        if not self.enabled:
            return 'off'
        return 'on' if self.fields == DEFAULT_KEY else ' '.join(self.fields)


def parse_match(value: Union[None, str, Sequence[str]]) -> MatchSpec:
    """MATCH as written in a wrapper or on the command line -> MatchSpec.

    Accepts a string ("on", "off", "lat lon date ...", commas allowed) or
    the list argparse gives with nargs='+'.
    """
    if value is None:
        tokens: List[str] = []
    elif isinstance(value, str):
        tokens = value.replace(',', ' ').split()
    else:
        tokens = [t for v in value for t in str(v).replace(',', ' ').split()]
    tokens = [t.strip().lower() for t in tokens if t.strip()]

    if not tokens or tokens == ['on']:
        return MatchSpec(True, DEFAULT_KEY)
    if tokens == ['off']:
        return MatchSpec(False, ())
    if 'on' in tokens or 'off' in tokens:
        raise ValueError(f"MATCH: 'on' and 'off' stand alone, got {tokens}")
    unknown = [t for t in tokens if t not in FIELDS]
    if unknown:
        raise ValueError(f"MATCH: unknown field(s) {unknown}; "
                         f"allowed: {', '.join(FIELDS)}, or on / off")
    seen: List[str] = []
    for t in tokens:
        if t not in seen:
            seen.append(t)
    return MatchSpec(True, tuple(seen))


def key_aliases(spec: MatchSpec, with_rank: bool = True,
                prefix: str = 'k_') -> List[str]:
    """Column names of the key in a side table: k_<field> (+ k_rank).

    prefix changes the k_ for a module whose own k_ columns are payload
    it keeps using (scatter reads k_stn and k_varno after the join).
    """
    names = [f"{prefix}{f}" for f in spec.fields]
    return names + [f"{prefix}rank"] if with_rank else names


def key_select(spec: MatchSpec, h: str = 'h', d: str = 'd',
               order: str = "{d}.obsvalue", prefix: str = 'k_') -> str:
    """The SELECT items that build the key, rank included.

    Goes straight into the SELECT that fills a side table, e.g.

        CREATE TEMP TABLE c AS
        SELECT {key_select(spec)}, d.omp AS omp, ...
        FROM ctl.header h JOIN ctl.data d USING (id_obs) WHERE ...
    """
    exprs = [FIELDS[f].format(h=h, d=d) for f in spec.fields]
    items = [f"{e} AS {prefix}{f}" for e, f in zip(exprs, spec.fields)]
    items.append(f"ROW_NUMBER() OVER (PARTITION BY {', '.join(exprs)} "
                 f"ORDER BY {order.format(h=h, d=d)}) AS {prefix}rank")
    return ", ".join(items)


def rank_select(exprs: Sequence[str], order: str = "d.obsvalue") -> str:
    """The rank item alone, over any key expressions.

    For a module that keeps a key of its own (profile knows that radar
    pairs on range, not vcoord) but wants the same one-to-one rule.
    """
    return (f"ROW_NUMBER() OVER (PARTITION BY {', '.join(exprs)} "
            f"ORDER BY {order}) AS {RANK}")


def key_join(spec: MatchSpec, left: str = 'c', right: str = 'e',
             prefix: str = 'k_') -> str:
    """The ON clause pairing two side tables."""
    return " AND ".join(f"{left}.{k} = {right}.{k}"
                        for k in key_aliases(spec, prefix=prefix))


def count_repeats(conn, table: str,
                  spec: Union[MatchSpec, Sequence[str]],
                  where: Optional[str] = None) -> Tuple[int, int]:
    """(keys that repeat, rows inside them) in a side table.

    spec is a MatchSpec, or the key column names themselves (rank left
    out) for a module with a key of its own. where restricts the count
    to the rows that matter -- e.g. "omp IS NOT NULL OR oma IS NOT NULL"
    for a table that also keeps rows no sum ever uses.
    """
    names = (key_aliases(spec, with_rank=False)
             if isinstance(spec, MatchSpec) else list(spec))
    keys = ", ".join(names)
    cond = f"WHERE {where} " if where else ""
    row = conn.execute(
        f"SELECT COUNT(*), COALESCE(SUM(n), 0) FROM "
        f"(SELECT COUNT(*) AS n FROM {table} {cond}GROUP BY {keys} "
        f"HAVING COUNT(*) > 1);").fetchone()
    return int(row[0]), int(row[1])


def add_counts(total: Dict[str, List[int]],
               part: Optional[Dict[str, Tuple[int, int]]]) -> None:
    """Sum the per-task counts {side: (keys, rows)} into total."""
    for side, (k, r) in (part or {}).items():
        t = total.setdefault(side, [0, 0])
        t[0] += k
        t[1] += r


def repeat_warning(module: str, family: str, spec: MatchSpec,
                   counts: Dict[str, Sequence[int]]) -> Optional[str]:
    """One line for the log when the key repeated somewhere, else None."""
    bad = {s: c for s, c in counts.items() if c[0]}
    if not bad:
        return None
    sides = ", ".join(f"{s}: {c[0]} keys, {c[1]} rows" for s, c in bad.items())
    return (f"[{module}] WARNING: match key not unique in {family} "
            f"({sides}); key = {spec.label}. Those observations are paired "
            f"one to one by value -- add a field to MATCH if they should "
            f"not be.")
