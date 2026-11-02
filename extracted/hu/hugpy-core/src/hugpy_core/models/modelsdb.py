"""Fleet models database: read handlers over Core's mdb_* projection (models-db-v1).

Each Wrapper builds its own models database; intake/models_db.py mirrors it into
mdb_builds / mdb_rows / mdb_digests (schema/sql/051_models_db.sql). These handlers
only READ that projection (plus one live, read-only proxy to the Wrapper for the
lazy per-tensor tables). They never write, route or allocate.

Plain kwargs functions in the ROUTES-CONVENTION style (query + body + path params
in, JSON-able out, ``(payload, status)`` for errors). MODELSDB_CATEGORIES states the
URL tree; the section's routes.py registers it (bare and under /api), giving
hugpy_terminal.models_db.CORE_BASE = /api/modelsdb:

  GET /modelsdb/models?q=&status=&worker=&engine=&task=&sort=&desc=&limit=&offset=&include_removed=
  GET /modelsdb/models/<worker>/<path:uid>[?include_removed=1]
  GET /modelsdb/models/<worker>/<path:uid>/tables/<table>?limit=&offset=
  GET /modelsdb/models/<worker>/<path:uid>/tensors?after=&limit=&table=&build_id=&generation=
  GET /modelsdb/workers/<worker>/tables/<table>?limit=&offset=    (global tables)
  GET /modelsdb/workers/<worker>/tables/<table>?unattributed=1    (a per-model table's '' partition)
  GET /modelsdb/builds[?include_removed=1]
  GET /modelsdb/dictionary[?worker=]

Workers: fleet(), model() and builds() show only workers that are currently
registered (core_worker_registrations); ?include_removed=1 also shows mirrored
data of removed workers. Every entry says whether its worker is registered and
connected.

Unattributed rows: rows of a per-model table that the builder could not attribute
to a model are mirrored as that table's '' partition. They never appear on a model
page; builds() lists their counts per worker (``unattributed: {table: rows}``) and
/workers/<worker>/tables/<table>?unattributed=1 pages them.

Errors carry {error: {code, message}}; codes the console treats as neutral notices:
terminal-too-old (503: Core's hugpy-terminal predates models-db-v1 generation
pinning), not-offered (the Wrapper has no models DB), worker-not-connected (409,
lazy tensor reads only). rebuilt (409): the Wrapper replaced its database during a
paged tensor read; restart from after=0 without build_id/generation.
"""
from __future__ import annotations

import functools
import re

from abstract_flask import spec

from hugpy_core.imports.functions import core_dsn

SECTION_LIMIT = 100
SECTION_LIMIT_MAX = 1000
FLEET_LIMIT = 500
FLEET_LIMIT_MAX = 5000
TENSOR_LIMIT = 500
# models columns fleet_identity reads besides SUMMARY_COLUMNS (all exposed by mdb_models).
IDENTITY_COLUMNS = ('hub_id_source', 'repo_id', 'subpath', 'location_scope')
# Columns the mdb_models view (schema/sql/051_models_db.sql) exposes, typed.
VIEW_COLUMNS = frozenset((
    'model_uid', 'status', 'display_name', 'hub_id', 'catalog_key', 'engine', 'runner', 'primary_task',
    'architecture', 'size_label', 'n_params', 'context_length', 'elected_quant', 'served_bytes', 'is_moe',
    'has_vision', 'has_chat_template', 'license', 'feasibility_status', 'auto_mode', 'auto_ctx',
    'calls_total', 'last_called_at', 'median_decode_tok_s', 'served_store_role', 'copies',
    *IDENTITY_COLUMNS))


def _contract():
    from hugpy_core.intake.models_db import contract
    return contract()


def _surrogates():
    from hugpy_core.intake.models_db import SURROGATE_COLUMNS
    return SURROGATE_COLUMNS


def _conn():
    import psycopg
    from psycopg.rows import dict_row
    return psycopg.connect(core_dsn(), row_factory=dict_row, connect_timeout=5)


def _error(message, status, code=None):
    error = {"message": message}
    if code:
        error["code"] = code
    payload = {"error": error}
    if code:
        payload["reason"] = code
    return payload, status


def _guarded(view):
    """503 {reason: 'terminal-too-old'} instead of a traceback when hugpy_terminal.models_db
    is missing or too old (intake does not mirror anything then either)."""
    @functools.wraps(view)
    def run(*args, **kwargs):
        from hugpy_core.intake.models_db import TerminalTooOld, TERMINAL_TOO_OLD, contract
        try:
            contract()   # before any database or Wrapper access
            return view(*args, **kwargs)
        except TerminalTooOld as exc:
            return _error(str(exc), 503, TERMINAL_TOO_OLD)
    return run


def _registered():
    """{worker: connected} for every currently registered worker."""
    from hugpy_core.registry import registrations
    out = {}
    for config in registrations.all():
        name = (config or {}).get('name')
        if name:
            out[str(name)] = registrations.is_connected(config)
    return out


def _one(value):
    if isinstance(value, (list, tuple)):
        value = value[0] if value else None
    return None if value is None else str(value).strip()


def _uid(value):
    """A model uid from the path. uids contain '/', which the console sends as %2F; servers normally
    decode it before routing, but a proxy may pass it through encoded. Only %2F is decoded, so a
    literal '%' in a directory name survives."""
    value = _one(value)
    return None if value is None else value.replace('%2F', '/').replace('%2f', '/')


def _choices(value):
    """'a,b' or ['a', 'b'] -> {'a', 'b'}; empty -> None (no filter)."""
    items = value if isinstance(value, (list, tuple)) else [value]
    found = {part.strip() for item in items if item is not None for part in str(item).split(',')}
    found.discard('')
    return found or None


def _int(value, default, low=0, high=None):
    try:
        number = int(_one(value) or default)
    except (TypeError, ValueError):
        number = default
    number = max(low, number)
    return min(number, high) if high is not None else number


def _flag(value):
    return (_one(value) or '').lower() in ('1', 'true', 'yes', 'on', 'desc')


def _iso(value):
    if value is None or isinstance(value, str):
        return value
    from datetime import timezone
    return value.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _build_view(row, registered=None):
    """mdb_builds row -> JSON (status is reduced to the Wrapper's own build health).

    sync_state not_offered / disabled is neutral (no error); 'unavailable' keeps the
    last good build fields; run is the last sync attempt's summary."""
    status = row.get('status') or {}
    status = status if isinstance(status, dict) else {}
    run = row.get('run') or {}
    run = run if isinstance(run, dict) else {}
    wrapper = {key: status.get(key) for key in (
        'available', 'enabled', 'reason', 'building', 'bytes', 'last_error', 'last_started_at',
        'last_finished_at') if key in status}
    # the latest Wrapper reply of an unavailable/disabled attempt is fresher than the last good one
    wrapper.update({key: value for key, value in (run.get('wrapper') or {}).items()
                    if key in ('available', 'enabled', 'reason', 'building', 'last_error')})
    view = {
        'worker': row['worker'], 'store_id': row.get('store_id'), 'build_id': row.get('build_id'),
        'generation': row.get('generation'),
        'built_at': _iso(row.get('built_at')), 'builder_version': row.get('builder_version'),
        'source_user_version': row.get('source_user_version'), 'models': row.get('models'),
        'synced_at': _iso(row.get('synced_at')), 'sync_state': row.get('sync_state'),
        'neutral': row.get('sync_state') in ('not_offered', 'disabled'),
        'error': row.get('error'), 'error_at': _iso(row.get('error_at')),
        'failed_sections': status.get('failed_sections'),
        'wrapper': wrapper, 'run': run or None,
    }
    if registered is not None:
        view['registered'] = row['worker'] in registered
        view['connected'] = bool(registered.get(row['worker']))
    return view


def _select(name):
    """A typed mdb_models column, or the raw jsonb value for a summary column newer than 051."""
    if name in VIEW_COLUMNS:
        return name
    if not re.fullmatch(r'[a-z_][a-z0-9_]*', name):
        raise ValueError('invalid models column ' + repr(name))
    return f'"row" -> \'{name}\' AS {name}'


def _summary_rows(conn, workers=None):
    """({worker: [models summary rows]}, {worker: built_at}); ``workers`` limits both."""
    m = _contract()
    names = list(dict.fromkeys(('model_uid', *m.SUMMARY_COLUMNS, *IDENTITY_COLUMNS)))
    rows = conn.execute('SELECT worker, ' + ', '.join(map(_select, names)) + ' FROM mdb_models').fetchall()
    built = {r['worker']: _iso(r['built_at']) for r in conn.execute(
        'SELECT worker, built_at FROM mdb_builds') if workers is None or r['worker'] in workers}
    by_worker = {}
    for row in rows:
        worker = row.pop('worker')
        if workers is None or worker in workers:
            by_worker.setdefault(worker, []).append(row)
    return by_worker, built


def _scope(include_removed):
    """(registered {worker: connected}, worker filter or None when removed ones are included)."""
    registered = _registered()
    return registered, (None if _flag(include_removed) else set(registered))


# --------------------------------------------------------------------------- fleet

def _entry_match(record, key, wanted):
    return any(entry.get(key) in wanted for entry in record['workers'])


def _search_text(record):
    parts = [record.get('fleet_id'), record.get('display_name'), record.get('hub_id')]
    for entry in record['workers']:
        parts.extend((entry.get('model_uid'), entry.get('catalog_key'), entry.get('display_name')))
    return ' '.join(str(p) for p in parts if p).casefold()


def _facets(records):
    out = {'status': {}, 'engine': {}, 'task': {}, 'worker': {}}
    for record in records:
        seen = {name: set() for name in out}
        for entry in record['workers']:
            seen['status'].add(entry.get('status'))
            seen['engine'].add(entry.get('engine') or entry.get('runner'))
            seen['task'].add(entry.get('primary_task'))
            seen['worker'].add(entry.get('worker'))
        for name, values in seen.items():
            for value in values:
                if value:
                    out[name][value] = out[name].get(value, 0) + 1
    return {name: dict(sorted(counts.items())) for name, counts in out.items()}


def _sort_key(column):
    def key(record):
        value = record['display_name'] if column == 'display_name' else record['summary'].get(column)
        if value is None:
            return (1, 0, '')
        if isinstance(value, (int, float)):
            return (0, value, '')
        return (0, 0, str(value).casefold())
    return key


def fleet_records(rows_by_worker, built_at=None, q=None, status=None, worker=None, engine=None,
                  task=None, sort=None, desc=None, limit=None, offset=None):
    """merge_fleet + filters + sort + page; pure (the handler feeds it from mdb_models)."""
    m = _contract()
    records = m.merge_fleet(rows_by_worker, built_at)
    facets = _facets(records)
    wanted = {name: _choices(value) for name, value in
              (('status', status), ('worker', worker), ('engine', engine), ('task', task))}
    text = (_one(q) or '').casefold()
    found = []
    for record in records:
        if text and text not in _search_text(record):
            continue
        if wanted['status'] and not _entry_match(record, 'status', wanted['status']):
            continue
        if wanted['worker'] and not _entry_match(record, 'worker', wanted['worker']):
            continue
        if wanted['engine'] and not (_entry_match(record, 'engine', wanted['engine'])
                                     or _entry_match(record, 'runner', wanted['engine'])):
            continue
        if wanted['task'] and not _entry_match(record, 'primary_task', wanted['task']):
            continue
        found.append(record)
    column = _one(sort)
    if column and (column == 'display_name' or column in m.SUMMARY_COLUMNS):
        found.sort(key=_sort_key(column), reverse=_flag(desc))
        if _flag(desc):   # keep unknown values last in both directions
            found.sort(key=lambda r: (r['display_name'] if column == 'display_name'
                                      else r['summary'].get(column)) is None)
    limit = _int(limit, FLEET_LIMIT, 1, FLEET_LIMIT_MAX)
    offset = _int(offset, 0)
    return {'total': len(found), 'fleet_total': len(records), 'limit': limit, 'offset': offset,
            'columns': list(m.SUMMARY_COLUMNS), 'facets': facets,
            'rows': found[offset:offset + limit]}


@_guarded
def fleet(q=None, status=None, worker=None, engine=None, task=None, sort=None, desc=None,
          limit=None, offset=None, include_removed=None, **_):
    """One row per fleet model (hugpy_terminal.models_db.merge_fleet) with worker entries.

    Only currently registered workers unless include_removed=1."""
    registered, scope = _scope(include_removed)
    with _conn() as conn:
        rows_by_worker, built = _summary_rows(conn, scope)
        builds = [_build_view(r, registered) for r in conn.execute('SELECT * FROM mdb_builds ORDER BY worker')
                  if scope is None or r['worker'] in scope]
    result = fleet_records(rows_by_worker, built, q=q, status=status, worker=worker, engine=engine,
                           task=task, sort=sort, desc=desc, limit=limit, offset=offset)
    result['builds'] = builds
    result['include_removed'] = scope is None
    return result


# --------------------------------------------------------------------------- one model

def section_index(counts):
    """[{section, label, tables:[{table, rows}]}] in contract order; counts = {table: rows}."""
    m = _contract()
    return [{'section': section, 'label': m.SECTION_LABELS.get(section, section.title()),
             'tables': [{'table': table, 'rows': int(counts.get(table) or 0)} for table in tables]}
            for section, tables in m.SECTIONS.items()]


@_guarded
def model(worker=None, uid=None, include_removed=None, **_):
    """One worker's model: its models row, build, per-section row counts, and the
    same fleet model on other (registered, unless include_removed=1) workers."""
    m = _contract()
    worker, uid = _one(worker), _uid(uid)
    if not worker or not uid:
        return _error('worker and model uid are required', 400)
    registered, scope = _scope(include_removed)
    if scope is not None and worker not in scope:
        return _error(f'Worker {worker} is not registered (include_removed=1 shows its last mirrored data)',
                      404, 'worker-removed')
    with _conn() as conn:
        found = conn.execute(
            'SELECT "row" FROM mdb_rows WHERE worker=%s AND table_name=%s AND model_uid=%s '
            'ORDER BY ord LIMIT 1', (worker, 'models', uid)).fetchone()
        if found is None:
            return _error('Unknown model on this worker', 404)
        counts = {r['table_name']: r['rows'] for r in conn.execute(
            'SELECT table_name, "rows" FROM mdb_digests WHERE worker=%s AND model_uid=%s', (worker, uid))}
        build = conn.execute('SELECT * FROM mdb_builds WHERE worker=%s', (worker,)).fetchone()
        rows_by_worker, _built = _summary_rows(conn, scope)
    row = found['row']
    # Same grouping as fleet(): per-row identities folded through canonical_fleet_ids, so a repo seen
    # verified on one worker and unverified on another is one fleet model here too.
    every = [m.fleet_identity(other) for others in rows_by_worker.values() for other in others]
    canon = m.canonical_fleet_ids(every + [m.fleet_identity(row)]) if hasattr(m, 'canonical_fleet_ids') else {}
    ident = lambda r: canon.get(m.fleet_identity(r), m.fleet_identity(r))
    fleet_id = ident(row)
    siblings = [{'worker': name, 'model_uid': other.get('model_uid'), 'status': other.get('status'),
                 'catalog_key': other.get('catalog_key')}
                for name, others in sorted(rows_by_worker.items()) for other in others
                if ident(other) == fleet_id
                and not (name == worker and other.get('model_uid') == uid)]
    return {'worker': worker, 'model_uid': uid, 'fleet_id': fleet_id,
            'display_name': row.get('display_name') or row.get('catalog_key') or uid.rsplit('/', 1)[-1],
            'model': row, 'build': _build_view(build, registered) if build else None,
            'sections': section_index(counts), 'siblings': siblings,
            'lazy_tables': sorted(m.LAZY_TABLES)}


def _columns(build_columns, table, rows):
    drop = _surrogates().get(table, ())
    known = [c for c in (build_columns or {}).get(table) or () if c not in drop]
    extra = [key for row in rows for key in row if key not in known and key not in drop]
    return known + list(dict.fromkeys(extra))


def _page(worker, uid, table, limit, offset):
    drop = _surrogates().get(table, ())
    with _conn() as conn:
        # surrogate ids mirrored before they were dropped at intake are hidden here too
        rows = [{k: v for k, v in r['row'].items() if k not in drop} if drop and isinstance(r['row'], dict)
                else r['row'] for r in conn.execute(
            'SELECT "row" FROM mdb_rows WHERE worker=%s AND table_name=%s AND model_uid=%s '
            'ORDER BY ord LIMIT %s OFFSET %s', (worker, table, uid, limit, offset))]
        total = conn.execute('SELECT count(*) AS n FROM mdb_rows WHERE worker=%s AND table_name=%s '
                             'AND model_uid=%s', (worker, table, uid)).fetchone()['n']
        build = conn.execute('SELECT columns FROM mdb_builds WHERE worker=%s', (worker,)).fetchone()
    return rows, total, (build or {}).get('columns')


@_guarded
def section(worker=None, uid=None, table=None, limit=None, offset=None, **_):
    """One per-model table of one worker's model, paged in the Wrapper's row order."""
    m = _contract()
    worker, uid, table = _one(worker), _uid(uid), _one(table)
    if not worker or not uid or not table:
        return _error('worker, model uid and table are required', 400)
    if table in m.LAZY_TABLES:
        return _error(f'{table} is not mirrored; read it through .../tensors', 400)
    if table not in m.SECTION_OF:
        return _error(f'Unknown models-db table: {table}', 400)
    limit = _int(limit, SECTION_LIMIT, 1, SECTION_LIMIT_MAX)
    offset = _int(offset, 0)
    rows, total, columns = _page(worker, uid, table, limit, offset)
    section_name = m.SECTION_OF[table]
    return {'worker': worker, 'model_uid': uid, 'table': table, 'section': section_name,
            'label': m.SECTION_LABELS.get(section_name, section_name.title()),
            'columns': _columns(columns, table, rows), 'rows': rows,
            'total': total, 'limit': limit, 'offset': offset}


@_guarded
def worker_table(worker=None, table=None, limit=None, offset=None, unattributed=None, **_):
    """One worker's '' partition of a table: a global table (stores, engines,
    build_info, ...), or with unattributed=1 the rows of a per-model table that the
    builder could not attribute to any model."""
    m = _contract()
    worker, table = _one(worker), _one(table)
    if not worker or not table:
        return _error('worker and table are required', 400)
    if table in m.GLOBAL_TABLES:
        section_name = 'global'
    elif table in m.SECTION_OF:
        if not _flag(unattributed):
            return _error(f'{table} is per model: read it under /models/<worker>/<uid>/tables/{table}, '
                          'or pass unattributed=1 for its unattributed rows', 400)
        section_name = m.SECTION_OF[table]
    else:
        return _error(f'Unknown models-db table: {table}', 400)
    limit = _int(limit, SECTION_LIMIT, 1, SECTION_LIMIT_MAX)
    offset = _int(offset, 0)
    rows, total, columns = _page(worker, m.GLOBAL_UID, table, limit, offset)
    return {'worker': worker, 'table': table, 'section': section_name,
            'unattributed': section_name != 'global',
            'columns': _columns(columns, table, rows), 'rows': rows,
            'total': total, 'limit': limit, 'offset': offset}


# --------------------------------------------------------------------------- fleet-wide

@_guarded
def builds(include_removed=None, **_):
    """Every (registered, unless include_removed=1) worker's mirrored build and sync
    state, with partition/row totals and the unattributed row counts per table."""
    m = _contract()
    registered, scope = _scope(include_removed)
    with _conn() as conn:
        rows = [r for r in conn.execute('SELECT * FROM mdb_builds ORDER BY worker').fetchall()
                if scope is None or r['worker'] in scope]
        totals = {r['worker']: r for r in conn.execute(
            'SELECT worker, count(*) AS partitions, coalesce(sum("rows"), 0) AS rows '
            'FROM mdb_digests GROUP BY worker')}
        unattributed = {}
        for r in conn.execute('SELECT worker, table_name, "rows" FROM mdb_digests '
                              'WHERE model_uid = %s AND "rows" > 0 ORDER BY worker, table_name', (m.GLOBAL_UID,)):
            if r['table_name'] in m.SECTION_OF:
                unattributed.setdefault(r['worker'], {})[r['table_name']] = int(r['rows'])
    out = []
    for row in rows:
        view = _build_view(row, registered)
        total = totals.get(row['worker']) or {}
        view['partitions'] = int(total.get('partitions') or 0)
        view['rows'] = int(total.get('rows') or 0)
        view['unattributed'] = unattributed.get(row['worker'], {})
        out.append(view)
    return {'protocol': m.PROTOCOL, 'version': m.VERSION, 'capability': m.CAPABILITY,
            'include_removed': scope is None, 'builds': out}


def dictionary_from(rows_by_worker, built_at=None):
    """Merge data_dictionary rows of several workers (newest build wins per entry); pure."""
    m = _contract()
    order = sorted(rows_by_worker, key=lambda w: (built_at or {}).get(w) or '')
    tables = {}
    for name in order:   # oldest first, so newer builds overwrite
        for row in rows_by_worker[name]:
            table = row.get('table_name')
            if not table:
                continue
            entry = tables.setdefault(table, {'description': None, 'columns': {},
                                              'section': m.section_of(table)})
            column = row.get('column_name') or ''
            if column:
                entry['columns'][column] = row.get('description')
            else:
                entry['description'] = row.get('description')
    sections = [{'section': s, 'label': m.SECTION_LABELS.get(s, s.title()), 'tables': list(t)}
                for s, t in m.SECTIONS.items()]
    return {'tables': dict(sorted(tables.items())), 'sections': sections,
            'global_tables': list(m.GLOBAL_TABLES), 'lazy_tables': sorted(m.LAZY_TABLES),
            'summary_columns': list(m.SUMMARY_COLUMNS), 'status_order': list(m.STATUS_ORDER),
            'workers': order}


@_guarded
def dictionary(worker=None, **_):
    """Table and column descriptions from the mirrored data_dictionary (all workers merged)."""
    worker = _one(worker)
    with _conn() as conn:
        params = ['data_dictionary']
        sql = 'SELECT worker, "row" FROM mdb_rows WHERE table_name=%s'
        if worker:
            sql += ' AND worker=%s'
            params.append(worker)
        rows_by_worker = {}
        for r in conn.execute(sql + ' ORDER BY worker, ord', params):
            rows_by_worker.setdefault(r['worker'], []).append(r['row'])
        built = {r['worker']: _iso(r['built_at']) for r in conn.execute(
            'SELECT worker, built_at FROM mdb_builds')}
    return dictionary_from(rows_by_worker, built)


# --------------------------------------------------------------------------- lazy, live

def _wrapper(worker):
    """(client, None) for a registered, connected worker; else (None, error reply)."""
    from hugpy_core.registry import registrations
    from hugpy_core.intake.models_db import client_for
    config = registrations.get(worker)
    if config is None:
        return None, _error('Unknown worker', 404, 'worker-removed')
    if not registrations.is_connected(config):
        return None, _error(f'Worker {worker} is not connected; per-tensor rows are read live from it',
                            409, 'worker-not-connected')
    return client_for(config, timeout=20), None


@_guarded
def tensors(worker=None, uid=None, after=None, limit=None, table=None, build_id=None, generation=None, **_):
    """Per-tensor rows of one model, read live from its Wrapper (never mirrored).

    table=model_tensor_files pages the model's weight files; the default pages
    model_tensors for the model (the Wrapper maps model_uid through
    model_tensor_files). The first page (no build_id/generation) pins the read: its
    reply carries build_id + generation, and every following page must send both
    back; 409 code 'rebuilt' means the Wrapper replaced its database meanwhile
    (restart from after=0 without them). The first model_tensors page also carries
    the model's files, read under the same pin."""
    from hugpy_core.intake.models_db import iter_rows
    m = _contract()
    worker, uid = _one(worker), _uid(uid)
    table = _one(table) or 'model_tensors'
    if not worker or not uid:
        return _error('worker and model uid are required', 400)
    if table not in m.LAZY_TABLES:
        return _error(f'{table} is mirrored; read it through .../tables/{table}', 400)
    after = _int(after, 0)
    limit = _int(limit, TENSOR_LIMIT, 1, m.ROWS_LIMIT_MAX)
    build_id = _one(build_id) or None
    generation = _one(generation) or None
    if after and not build_id:
        return _error('Pass the build_id (and generation) of the first page with after > 0', 400)
    try:
        client, problem = _wrapper(worker)
    except m.ModelsDbError as exc:
        return _error(str(exc), 502)
    if problem:
        return problem
    result = {'worker': worker, 'model_uid': uid, 'table': table}
    try:
        page = client.rows(table, after=after, limit=limit, model_uid=uid, build_id=build_id,
                           generation=generation)
        got_build = page.get('build_id')
        got_gen = page.get('generation')
        got_gen = None if got_gen in (None, '') else str(got_gen)
        if (build_id and got_build not in (None, build_id)) or (generation and got_gen not in (None, generation)):
            raise m.ModelsDbChanged('Wrapper replaced its models database during the read', 409)
        build_id, generation = build_id or got_build, generation or got_gen
        if table == 'model_tensors' and not after:
            # file_id stays: within one pinned read it links tensors to their file
            result['files'] = list(iter_rows(client, 'model_tensor_files', model_uid=uid,
                                             build_id=build_id, generation=generation))
    except m.ModelsDbChanged as exc:
        return _error(f'{exc} (restart from after=0)', 409, 'rebuilt')
    except m.ModelsDbUnavailable as exc:
        return _error(f'Wrapper does not offer {m.CAPABILITY}: {exc}', 404, 'not-offered')
    except m.ModelsDbError as exc:
        return _error(str(exc), 400 if exc.status == 400 else 502)
    columns = page['columns']
    result.update({'build_id': build_id, 'generation': generation, 'columns': columns,
                   'rows': [dict(zip(columns, row)) for row in page['rows']],
                   'next_after': page.get('next_after'), 'more': bool(page.get('more')),
                   'after': after, 'limit': limit})
    return result


def _get(view):
    return spec(view, 'GET', response='native')


# Registered by the section's routes.py (coordinator), bare and under /api.
MODELSDB_CATEGORIES = {
    'modelsdb': {
        'models': {
            '': _get(fleet),                                    # /modelsdb/models
            '<worker>': {
                '<path:uid>': {
                    '': _get(model),                            # /modelsdb/models/<worker>/<path:uid>
                    'tables': {'<table>': _get(section)},       # .../tables/<table>
                    'tensors': _get(tensors),                   # .../tensors
                },
            },
        },
        'workers': {'<worker>': {'tables': {'<table>': _get(worker_table)}}},
        'builds': _get(builds),                                 # /modelsdb/builds
        'dictionary': _get(dictionary),                         # /modelsdb/dictionary
    },
}

__all__ = ['fleet', 'model', 'section', 'worker_table', 'builds', 'dictionary', 'tensors',
           'fleet_records', 'dictionary_from', 'section_index', 'MODELSDB_CATEGORIES']
