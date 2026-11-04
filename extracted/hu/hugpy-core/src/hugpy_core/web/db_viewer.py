"""Read-only console browser for Hugpy's configured PostgreSQL and SQLite stores.

EXPOSURE: these routes read every hugpy store (call_log prompts/responses,
settings, comms). Core has no auth of its own yet, so nginx limits
/api/llm/db/ to LAN + WireGuard (hugpy.ai.dev.conf, like /dbviewer/ and
/api/settings/). Never expose them without that gate."""
from contextlib import contextmanager
import hashlib
import os
from pathlib import Path
import re
import urllib.parse
import sqlite3
import time

from flask import jsonify
import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo


def _json(payload, status=200):
    """Wrap JSON-able data in a Response so register_route passes the custom
    status through (a returned (body, status) tuple would be re-wrapped)."""
    r = jsonify(payload)
    r.status_code = status
    return r


def sources():
    """Discover package stores without opening/migrating SQLite store classes."""
    out = {}
    base = os.environ.get('HUGPY_CORE_DB') or 'dbname=hugpy_core'
    configs = [('hugpy-core', base), ('hugpy-wrapper / hugpy-worker',
               __import__('hugpy_core.calllog.calllog_db', fromlist=['dsn']).dsn())]
    for key, value in os.environ.items():
        if key.startswith(('HUGPY_', 'FITEVICT_')) and key.endswith(('_DB', '_DSN')) and (
                'dbname=' in value or value.startswith(('postgres://', 'postgresql://'))):
            configs.append((key, value))
    try:
        with psycopg.connect(base, connect_timeout=3, autocommit=True) as conn:
            names = conn.execute("SELECT datname FROM pg_database WHERE datallowconn AND NOT datistemplate "
                                 "AND datname LIKE 'hugpy%%' ORDER BY datname").fetchall()
        for (name,) in names:
            configs.append((name.replace('_', '-'), make_conninfo(base, dbname=name)))
    except psycopg.Error:
        pass  # Configured sources still appear and expose their connection status on selection.
    for package, dsn in configs:
        info = conninfo_to_dict(dsn)
        name = info.get('dbname', 'postgres')
        identity = '|'.join(info.get(k, '') for k in ('host', 'port', 'dbname', 'user'))
        key = 'pg-' + hashlib.sha256(identity.encode()).hexdigest()[:16]
        if key not in out:
            out[key] = {'id': key, 'name': name, 'package': package, 'engine': 'postgresql', 'dsn': dsn}
    # Each registered worker owns its own SQLite store. Its existing admin
    # telemetry browser serves pages from that exact file over the worker key.
    from hugpy_core.registry import registrations
    for worker in registrations.all():
        name = worker.get('name')
        if name:
            key = 'worker-' + name
            out[key] = {'id': key, 'name': f'{name} · wrapper', 'package': 'hugpy-wrapper',
                        'engine': 'sqlite', 'worker': name}
    home = Path(os.environ.get('HUGPY_HOME') or Path.home() / '.hugpy').expanduser()
    data = Path(os.environ.get('HUGPY_DATA_DIR') or Path.home() / '.local/share/hugpy').expanduser()
    roots = [(home, 'hugpy-storage'), (data, 'hugpy-storage'),
             (Path.home() / '.hugpy_agent', 'hugpy-agent'),
             (Path.home() / '.local/state/hugpy_core', 'hugpy-core')]
    if os.environ.get('PROJECTS_HOME'):
        roots.append((Path(os.environ['PROJECTS_HOME']).expanduser(), 'hugpy-storage'))
    paths = []
    for root, package in roots:
        for pattern in ('*.db', '*.sqlite', '*.sqlite3', '*/*.db', '*/*.sqlite', '*/*.sqlite3'):
            paths.extend((p, package) for p in root.glob(pattern))
    runtime = Path(os.environ.get('XDG_RUNTIME_DIR') or '/tmp')
    paths.append((runtime / f'hugpy-comms-{os.getuid()}.db', 'hugpy-storage'))
    for key, value in os.environ.items():
        if key.startswith(('HUGPY_', 'FITEVICT_')) and key.endswith(('_DB', '_DB_PATH')) and value and (
                'dbname=' not in value and not value.startswith(('postgres://', 'postgresql://'))):
            paths.append((Path(value).expanduser(), key))
    for path, package in paths:
        if not path.is_file():
            continue
        path = path.resolve()
        if path.name == 'fitevict.sqlite3':
            # Wrapper stores come from their workers' authenticated read API.
            continue
        key = 'sqlite-' + hashlib.sha256(str(path).encode()).hexdigest()[:16]
        out.setdefault(key, {'id': key, 'name': path.name, 'package': package,
                             'engine': 'sqlite', 'path': str(path)})
    return out


@contextmanager
def connection(source):
    if source['engine'] == 'postgresql':
        with psycopg.connect(source['dsn'], connect_timeout=3) as conn:
            conn.execute('SET TRANSACTION READ ONLY')
            conn.execute("SET LOCAL statement_timeout = '5s'")
            yield conn
    else:
        conn = sqlite3.connect(Path(source['path']).as_uri() + '?mode=ro', uri=True, timeout=3)
        try:
            # Wrapper views use the same scalar functions its writer registers.
            # Read-only browser connections must register them too.
            conn.create_function('greatest', -1, lambda *values: max((v for v in values if v is not None), default=None))
            conn.create_function('least', -1, lambda *values: min((v for v in values if v is not None), default=None))
            conn.create_function('regexp_replace', 4, lambda value, pattern, replacement, flags:
                                 re.sub(pattern, replacement or '', value or '', count=0 if flags and 'g' in flags else 1))
            conn.create_function('regexp_replace', 3, lambda value, pattern, replacement:
                                 re.sub(pattern, replacement or '', value or '', count=1))
            conn.execute('PRAGMA query_only=ON')
            deadline = time.monotonic() + 5
            conn.set_progress_handler(lambda: int(time.monotonic() > deadline), 1000)
            yield conn
        finally:
            conn.close()


def tables(conn, engine):
    if engine == 'postgresql':
        rows = conn.execute("SELECT n.nspname,c.relname,c.relkind,c.reltuples::bigint "
                            "FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace "
                            "WHERE c.relkind IN ('r','p','v','m','f') AND n.nspname NOT LIKE 'pg_%' "
                            "AND n.nspname <> 'information_schema' ORDER BY 1,2").fetchall()
        kinds = {'r': 'table', 'p': 'partitioned table', 'v': 'view', 'm': 'materialized view', 'f': 'foreign table'}
        return [{'schema': s, 'name': n, 'kind': kinds[k], 'estimated_rows': max(count, 0)} for s,n,k,count in rows]
    return [{'schema': 'main', 'name': n, 'kind': k, 'estimated_rows': None}
            for n,k in conn.execute("SELECT name,type FROM sqlite_master WHERE type IN ('table','view') "
                                    "AND name NOT LIKE 'sqlite_%' ORDER BY name")]


def quote(name):
    return '"' + name.replace('"', '""') + '"'


def columns(conn, engine, schema, table):
    if engine == 'postgresql':
        rows = conn.execute("SELECT a.attname,format_type(a.atttypid,a.atttypmod),NOT a.attnotnull, "
                            "EXISTS(SELECT 1 FROM pg_index i WHERE i.indrelid=c.oid AND i.indisprimary "
                            "AND a.attnum=ANY(i.indkey)) FROM pg_attribute a JOIN pg_class c ON c.oid=a.attrelid "
                            "JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname=%s AND c.relname=%s "
                            "AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attnum", (schema, table)).fetchall()
        return [{'name': n, 'type': t, 'nullable': null, 'primary_key': pk} for n,t,null,pk in rows]
    return [{'name': r[1], 'type': r[2], 'nullable': not bool(r[3]), 'primary_key': bool(r[5])}
            for r in conn.execute('PRAGMA table_xinfo(' + quote(table) + ')') if len(r) < 7 or r[6] != 1]


def page(conn, engine, schema, table, args):
    limit, offset = int(args.get('limit', 50)), int(args.get('offset', 0))
    if not 1 <= limit <= 200 or offset < 0:
        raise ValueError('Page size must be 1–200 and offset must be nonnegative.')
    cols = columns(conn, engine, schema, table)
    names = [c['name'] for c in cols]
    sort = args.get('sort') or next((c['name'] for c in cols if c['primary_key']), names[0] if names else '')
    field = args.get('column') or ''
    if sort not in names or (field and field not in names):
        raise ValueError('Unknown column.')
    direction = args.get('direction', 'asc').lower()
    if direction not in ('asc', 'desc'):
        raise ValueError('Direction must be asc or desc.')
    q = args.get('q', '')
    needle = '%' + q.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'
    keys = [sort] + [c['name'] for c in cols if c['primary_key'] and c['name'] != sort]
    if engine == 'postgresql':
        order = sql.SQL(', ').join(sql.SQL('CAST({} AS text) {}').format(sql.Identifier(k), sql.SQL(direction))
                                  if next(c['type'] for c in cols if c['name']==k) in ('json', 'xml') else
                                  sql.SQL('{} {}').format(sql.Identifier(k), sql.SQL(direction)) for k in keys)
        where = sql.SQL('')
        params = []
        if q:
            expression = sql.SQL('CAST({} AS text)').format(sql.Identifier(field)) if field else sql.SQL('to_jsonb(t)::text')
            where = sql.SQL(" WHERE {} ILIKE %s ESCAPE '\\'").format(expression)
            params.append(needle)
        query = sql.SQL('SELECT to_jsonb(t)::text FROM {}.{} t{} ORDER BY {} LIMIT %s OFFSET %s').format(
            sql.Identifier(schema), sql.Identifier(table), where, order)
        import json
        rows = [json.loads(r[0]) for r in conn.execute(query, (*params, limit+1, offset)).fetchall()]
    else:
        where, params = '', []
        if q:
            searchable = [field] if field else names
            where = ' WHERE ' + ' OR '.join('CAST(' + quote(c) + " AS TEXT) LIKE ? ESCAPE '\\'" for c in searchable)
            params = [needle] * len(searchable)
        order = ', '.join(quote(k) + ' ' + direction for k in keys)
        cursor = conn.execute('SELECT * FROM ' + quote(table) + where + ' ORDER BY ' + order + ' LIMIT ? OFFSET ?',
                              (*params, limit+1, offset))
        rows = [dict(zip([c[0] for c in cursor.description], r)) for r in cursor.fetchall()]
        for row in rows:
            for key, val in row.items():
                if isinstance(val, bytes):
                    row[key] = {'encoding': 'hex', 'bytes': len(val), 'value': val.hex()}
    return {'columns': cols, 'rows': rows[:limit], 'offset': offset, 'limit': limit,
            'has_more': len(rows)>limit, 'sort': sort, 'direction': direction}


def search_all(conn, engine, q, cursor=''):
    """Search row values in every relation, returning a resumable page."""
    if not q or len(q) > 200:
        raise ValueError('Search text must be 1–200 characters.')
    catalog = tables(conn, engine)
    index, offset = (int(x) for x in cursor.split(':')) if cursor else (0, 0)
    if index < 0 or index > len(catalog) or offset < 0:
        raise ValueError('Invalid search cursor.')
    matches = []
    while index < len(catalog) and len(matches) < 50:
        table = catalog[index]
        cols = columns(conn, engine, table['schema'], table['name'])
        if not cols:
            index, offset = index + 1, 0
            continue
        result = page(conn, engine, table['schema'], table['name'],
                      {'q': q, 'limit': 50 - len(matches), 'offset': offset})
        matches.extend({'schema': table['schema'], 'table': table['name'], 'row': row}
                       for row in result['rows'])
        if result['has_more']:
            offset += len(result['rows'])
            break
        index, offset = index + 1, 0
    return {'matches': matches, 'next_cursor': f'{index}:{offset}' if index < len(catalog) else None,
            'table_count': len(catalog)}


# Views are pure functions (register_categories convention): their input (the
# former request.args — source/schema/table/limit/offset/sort/…) arrives as
# kwargs via get_request_datas, passed straight to read()/page() as a mapping.

def list_sources(**kwargs):
    return jsonify({'sources': [{k:v for k,v in s.items() if k not in ('dsn', 'path')}
                                for s in sources().values()]})


def _proxied(proxied):
    """(payload, status) from a _proxy_worker reply: a Flask Response carrying the
    worker's own JSON, or the bare ({'error': {'message': …}}, status) tuple
    _error() returns when the worker is unknown or unreachable. The console reads
    `error` as a string, so the nested message is flattened (2026-10-27: the
    worker path raised "'dict' object has no attribute 'get_json'" instead)."""
    response, status = proxied
    payload = response.get_json() if hasattr(response, 'get_json') else response
    if isinstance(payload, dict) and isinstance(payload.get('error'), dict):
        payload = {**payload, 'error': payload['error'].get('message') or str(payload['error'])}
    return payload, status


def read(rows=False, args=None):
    args = args or {}
    source = sources().get(args.get('source'))
    if not source:
        return _json({'error': 'Unknown database source.'}, 404)
    if source.get('worker'):
        from hugpy_core.web.recovered_surfaces import _proxy_worker
        path = '/v1/telemetry/rows?' + urllib.parse.urlencode({
            key: value for key, value in args.items() if key in
            ('table', 'limit', 'offset', 'sort', 'direction', 'q', 'column')}) if rows else '/v1/telemetry/tables'
        proxied = _proxy_worker(source['worker'], path)
        if isinstance(proxied, tuple):
            return _json(*_proxied(proxied))
        return proxied
    try:
        with connection(source) as conn:
            available = tables(conn, source['engine'])
            if not rows:
                return jsonify({'tables': available})
            schema, table = args.get('schema', 'public'), args.get('table', '')
            if not any(t['schema']==schema and t['name']==table for t in available):
                return _json({'error': 'Unknown table or view.'}, 404)
            return jsonify(page(conn, source['engine'], schema, table, args))
    except (ValueError, TypeError):
        return _json({'error': 'Invalid page, sort, direction, or filter column.'}, 400)
    except (psycopg.Error, sqlite3.Error, OSError) as exc:
        # Never include a DSN or credentials from a connection exception.
        return _json({'error': 'Database read failed (' + type(exc).__name__ +
                      '). Check access, availability, or narrow the search.'}, 503)


def list_tables(**kwargs):
    return read(False, kwargs)


def list_rows(**kwargs):
    return read(True, kwargs)


def search(**kwargs):
    source = sources().get(kwargs.get('source'))
    if not source:
        return _json({'error': 'Unknown database source.'}, 404)
    if source.get('worker'):
        from hugpy_core.web.recovered_surfaces import _proxy_worker
        path = '/v1/telemetry/search?' + urllib.parse.urlencode({
            key: value for key, value in kwargs.items() if key in ('q', 'cursor')})
        proxied = _proxy_worker(source['worker'], path)
        if isinstance(proxied, tuple):
            response, status = _proxied(proxied)
            if status != 404:
                return _json(response, status)
            # Workers running the previous code still expose the same read-only
            # tables/rows API. Search through that until their next restart.
            q = kwargs.get('q', '')
            cursor = kwargs.get('cursor', '')
            try:
                if not q or len(q) > 200:
                    raise ValueError('Invalid search text.')
                index, offset = (int(x) for x in cursor.split(':')) if cursor else (0, 0)
                catalog_response, catalog_status = _proxied(_proxy_worker(source['worker'], '/v1/telemetry/tables'))
                if catalog_status != 200:
                    return _json(catalog_response, catalog_status)
                catalog = catalog_response.get('tables') or []
                if index < 0 or index > len(catalog) or offset < 0:
                    raise ValueError('Invalid search cursor.')
                matches = []
                while index < len(catalog) and len(matches) < 50:
                    table = catalog[index]
                    params = urllib.parse.urlencode({'table': table['name'], 'q': q,
                                                     'limit': 50 - len(matches), 'offset': offset})
                    result, result_status = _proxied(_proxy_worker(source['worker'], '/v1/telemetry/rows?' + params))
                    if result_status != 200:
                        return _json(result, result_status)
                    matches.extend({'schema': 'main', 'table': table['name'], 'row': row}
                                   for row in result.get('rows') or [])
                    if result.get('has_more'):
                        offset += len(result['rows'])
                        break
                    index, offset = index + 1, 0
                return jsonify({'matches': matches, 'next_cursor': f'{index}:{offset}' if index < len(catalog) else None,
                                'table_count': len(catalog)})
            except (ValueError, TypeError):
                return _json({'error': 'Invalid search text or cursor.'}, 400)
        return proxied
    try:
        with connection(source) as conn:
            if source['engine'] == 'postgresql':
                conn.execute("SET LOCAL statement_timeout = '30s'")
            return jsonify(search_all(conn, source['engine'], kwargs.get('q', ''), kwargs.get('cursor', '')))
    except (ValueError, TypeError):
        return _json({'error': 'Invalid search text or cursor.'}, 400)
    except (psycopg.Error, sqlite3.Error, OSError) as exc:
        return _json({'error': 'Database search failed (' + type(exc).__name__ + ').'}, 503)


# category -> {route_name: callable}
DB_CATEGORIES = {
    "llm": {"db": {"sources": list_sources, "tables": list_tables, "rows": list_rows, "search": search}},
}
