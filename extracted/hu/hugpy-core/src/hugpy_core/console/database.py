"""The console's Database panel: every connected wrapper's database, browsed read-only where it is.

A wrapper browses its own database for whoever asks (GET /v1/telemetry/tables and /v1/telemetry/rows): its own
tables (schema main: the queue, its loads, every model's GPU layers, context ticks and allocation columns ...), its
resource log (kernel) and the Discovery export it reads (discovery). Each connected wrapper is one source here;
Core keeps nothing of what is shown and decides nothing about it.

    sources   GET /api/llm/db/sources                       {sources: [{id, name, engine, package, worker}]}
    tables    GET /api/llm/db/tables?source=                {tables: [{schema, name, kind}]}
    rows      GET /api/llm/db/rows?source=&schema=&table=   one page of a table, as the wrapper gives it: {columns,
              &limit=&offset=&q=&column=&sort=&direction=   rows, has_more, sort, direction}
    search    GET /api/llm/db/search?source=&q=&cursor=     every table searched for q, a page of matches at a time:
                                                            {matches: [{schema, table, row}], next_cursor}
"""
from ..imports import (
    urlencode,
)
from ..wrappers import ask, registry
from .modelsdb import Unanswered

SOURCE = 'worker-'           # a source is a connected wrapper: worker-<its name>
SEARCH_PAGE = 25             # the rows one table gives a search at a time
SEARCH_MATCHES = 50          # the matches one search answer carries


def sources() -> dict:
    """Every connected wrapper's database."""
    return dict(sources=[dict(id=SOURCE + w['name'], name=f"{w['name']} · wrapper.sqlite3", engine='sqlite',
                              package='hugpy-wrapper', worker=w['name']) for w in registry.connected()])


def wrapper_of(source: str) -> dict:
    """The connected wrapper a source names."""
    name = source[len(SOURCE):] if (source or '').startswith(SOURCE) else None
    found = registry.get(name) if name else None
    if not found or not found['connected']:
        raise Unanswered(404, 'source-unknown', f'source-unknown: {source!r} is not a connected wrapper\'s database')
    return found


def asked(wrapper: dict, path: str, params: dict) -> dict:
    """A wrapper's answer to one browse, or Unanswered with why."""
    try:
        status, page = ask(wrapper, path + ('?' + urlencode(params) if params else ''), timeout=30)
    except (OSError, LookupError, TimeoutError) as exc:
        raise Unanswered(409, 'worker-not-connected', f"worker-not-connected: {wrapper['name']} did not answer ({exc})") from None
    if status != 200 or not isinstance(page, dict):
        said = page.get('error') if isinstance(page, dict) else None
        raise Unanswered(status if status and status >= 400 else 502, 'not-offered',
                         f"not-offered: {wrapper['name']} did not give {path} (HTTP {status}" + (f': {said}' if said else '') + ')')
    return page


def tables(source: str) -> dict:
    """The tables and views of a wrapper's database, each in its schema (main, kernel, discovery)."""
    page = asked(wrapper_of(source), '/v1/telemetry/tables', {})
    out = []
    for t in page.get('tables') or []:
        schema, name = t.get('schema') or 'main', t.get('name') or ''
        if schema != 'main' and name.startswith(schema + '.'):
            name = name[len(schema) + 1:]              # the wrapper names a table of another schema schema.name
        out.append(dict(schema=schema, name=name, kind=t.get('kind')))
    return dict(source=source, tables=out)


def rows(source: str, schema: str, table: str, limit=50, offset=0, q: str = '', column: str = '', sort: str = '',
         direction: str = 'asc') -> dict:
    """One page of a table, as its wrapper gives it."""
    if not table:
        raise Unanswered(400, 'no-table', 'no-table: name a table')
    params = dict(table=table if schema in (None, '', 'main') else f'{schema}.{table}', limit=int(limit or 50),
                  offset=int(offset or 0), direction=direction or 'asc')
    params.update({k: v for k, v in dict(q=q, column=column, sort=sort).items() if v})
    page = asked(wrapper_of(source), '/v1/telemetry/rows', params)
    return dict(page, source=source, schema=schema or 'main', table=table)


def search(source: str, q: str, cursor: str = '') -> dict:
    """Every table of a source searched for `q`, a page of matches at a time. The cursor is where the last answer
    stopped: the table's place in the list and the rows of it already read."""
    q = (q or '').strip()
    if not q:
        raise Unanswered(400, 'no-query', 'no-query: say what to search for')
    listed = tables(source)['tables']
    at, _, skip = (cursor or '0:0').partition(':')
    at, skip = int(at or 0), int(skip or 0)
    matches = []
    while at < len(listed) and len(matches) < SEARCH_MATCHES:
        t = listed[at]
        try:
            page = rows(source, t['schema'], t['name'], limit=SEARCH_PAGE, offset=skip, q=q)
        except Unanswered:
            page = dict(rows=[], has_more=False)       # a table that cannot be read is passed over
        matches += [dict(schema=t['schema'], table=t['name'], row=r) for r in page.get('rows') or []]
        if page.get('has_more'):
            skip += SEARCH_PAGE
        else:
            at, skip = at + 1, 0
    return dict(source=source, q=q, matches=matches, next_cursor=f'{at}:{skip}' if at < len(listed) else None)
