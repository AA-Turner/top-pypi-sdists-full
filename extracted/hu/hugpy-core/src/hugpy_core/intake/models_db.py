"""Mirror each Wrapper's own models database (models-db-v1) into Core's mdb_* projection.

The Wrapper is the custodian: it builds hugpy_models.sqlite3 from its own store and
serves it read-only under /v1/telemetry/models-db (status, digests, keyset rows).
Core only projects it. This module runs off the telemetry loop, like
fact_exchange: ``schedule(worker, advert)`` is called after a committed collection
pass with the ``data_service.models_db`` advert of that pass; it starts at most one
sync thread per worker, and only when the advertised build/generation differs from
the one already handled (or REVERIFY_S has passed since, so a projection whose rows
were dropped is rebuilt without waiting for a new build).

A sync reads the Wrapper's status. Its ``generation`` names the built FILE (a
rebuild with identical content keeps build_id but gets a new generation); when the
build_id or generation differ from mdb_builds, or this worker has no mirrored
partitions, the sync diffs the Wrapper's per-(table, model_uid) digests against
mdb_digests (unchanged partitions are skipped, so a same-content rebuild only
refreshes mdb_builds), reads every changed partition (one whole-table read when many
partitions of a table changed), spools the rows to a private temporary file, and
only then opens ONE write transaction: changed and vanished partitions are deleted,
the new rows copied in, digests and mdb_builds (status, built_at, failed sections,
generation, this run's summary) updated, and mdb_changed notified after commit.
Every page is pinned to build_id + generation; a rebuild mid-sync aborts it (the
next advert retries). Nothing here writes any table outside mdb_builds / mdb_rows /
mdb_digests.

Defensive filters before anything is stored:
  * per-build surrogate ids (SURROGATE_COLUMNS) are dropped from mirrored rows;
  * download-staging copies (STAGING_RE on model_uid, catalog_key, rel_dir,
    served_dir) never become mdb rows that look like separate models; skips are
    counted in mdb_builds.run.staging_skipped.

Requires hugpy_terminal.models_db with generation support (contract_problem()).
Without it schedule() does nothing and the API answers 503 terminal-too-old.
"""
from __future__ import annotations

import inspect
import json
import logging
import math
import re
import tempfile
import threading
import time
from datetime import datetime, timezone

from hugpy_core.imports.functions import notify_channel

log = logging.getLogger(__name__)

COOLDOWN_S = 60                       # min seconds between two sync attempts of one worker
BACKOFF_S = (60, 120, 300, 600, 900)  # after consecutive failures
REVERIFY_S = 900                      # a handled advert is re-checked (one status call) after this
WHOLE_TABLE_MIN = 32                  # changed partitions of one table that justify a whole-table read
WHOLE_TABLE_SHARE = 0.25              # ... or this share of the table's partitions
HTTP_TIMEOUT_S = 60
STATES = ('synced', 'not_offered', 'disabled', 'unavailable', 'error')
NEUTRAL_STATES = ('not_offered', 'disabled')   # not errors: the Wrapper does not (want to) offer it
TERMINAL_TOO_OLD = 'terminal-too-old'

# Ids the builder renumbers on every build (its digests leave them out too): stale
# the moment the partition is mirrored, so they are never stored.
SURROGATE_COLUMNS = {'model_facts': ('fact_id',), 'model_tensor_files': ('file_id',)}
# A download-staging key or directory (<final>.tmp-<pid>/...): the builder folds it
# into the final model; Core skips anything that still carries one.
STAGING_RE = re.compile(r'\.tmp-\d+(/|$)')
STAGING_MODEL_COLUMNS = ('catalog_key', 'rel_dir', 'served_dir')

# What Core needs from hugpy_terminal.models_db (generation pinning came with 0.1.23+).
REQUIRED = ('CAPABILITY', 'PROTOCOL', 'VERSION', 'SECTIONS', 'SECTION_OF', 'SECTION_LABELS',
            'GLOBAL_TABLES', 'GLOBAL_UID', 'LAZY_TABLES', 'SUMMARY_COLUMNS', 'STATUS_ORDER', 'ROWS_LIMIT',
            'ROWS_LIMIT_MAX', 'WrapperModelsDb', 'ModelsDbError', 'ModelsDbChanged', 'ModelsDbUnavailable',
            'merge_fleet', 'fleet_identity', 'section_of')

_lock = threading.Lock()
_inflight = set()
_last = {}       # worker -> monotonic start of the last attempt
_done = {}       # worker -> (advert key already handled, monotonic time handled)
_failures = {}   # worker -> consecutive failures
_logged = {}     # worker -> last error text logged (one warning per distinct error)
_problem = None  # cached contract_problem(): None = not checked, '' = fine
_problem_logged = False


class TerminalTooOld(RuntimeError):
    """hugpy_terminal.models_db is missing or predates what Core needs."""
    reason = TERMINAL_TOO_OLD


def contract_problem():
    """None when hugpy_terminal.models_db is usable, else why not (checked once per process)."""
    global _problem
    if _problem is None:
        try:
            from hugpy_terminal import models_db as module
        except Exception as exc:  # noqa: BLE001 — ImportError or a broken install
            _problem = f'hugpy_terminal.models_db is not importable ({type(exc).__name__}: {exc})'
        else:
            missing = [name for name in REQUIRED if not hasattr(module, name)]
            if not missing:
                try:
                    params = inspect.signature(module.WrapperModelsDb.rows).parameters
                except (TypeError, ValueError):
                    params = {}
                if 'generation' not in params:
                    missing.append('WrapperModelsDb.rows(generation=)')
            _problem = ('hugpy-terminal is too old for models-db-v1 (missing ' + ', '.join(missing) + ')'
                        if missing else '')
    return _problem or None


def contract():
    """hugpy_terminal.models_db, or TerminalTooOld."""
    problem = contract_problem()
    if problem:
        raise TerminalTooOld(problem)
    from hugpy_terminal import models_db
    return models_db


_contract = contract


# --------------------------------------------------------------------------- scheduling

def _generation(value):
    return '' if value is None or value == '' else str(value)


def _disabled(reply):
    """The Wrapper's models DB is switched off (W0: enabled false / reason 'disabled')."""
    return isinstance(reply, dict) and (reply.get('enabled') is False or reply.get('reason') == 'disabled')


def advert_key(advert):
    """What an advert says about the Wrapper's models DB, as a comparable key.

    None/non-dict: not advertised (an older Wrapper). ``available`` false: no
    build yet, or switched off. Otherwise (build_id, generation): the same pair
    means the same file; a missing generation (older Wrapper) compares as ''."""
    if not isinstance(advert, dict):
        return ('absent',)
    if not advert.get('available') or not advert.get('build_id'):
        if _disabled(advert):
            return ('disabled',)
        return ('unavailable', str(advert.get('build_id') or ''))
    return ('build', str(advert['build_id']), _generation(advert.get('generation')))


def handled_by(key, result):
    """Whether a sync result settles the advert ``key`` (no HTTP until it changes)."""
    state = (result or {}).get('state')
    if state in NEUTRAL_STATES:
        return True
    if state != 'synced' or key[0] != 'build':
        return False
    return result.get('build_id') == key[1] and (not key[2] or result.get('generation') == key[2])


def schedule(worker, advert=None):
    """Keep the models-DB pull off the worker's telemetry loop; True when a thread started.

    ``advert`` is ``state['data_service'].get('models_db')`` of the pass that just
    committed. No advert means the Wrapper does not offer models-db-v1: the state is
    recorded (neutral) and nothing is requested from that Wrapper."""
    global _problem_logged
    problem = contract_problem()
    if problem:
        if not _problem_logged:
            _problem_logged = True
            log.warning('models-db mirror disabled: %s', problem)
        return False
    name = worker['name']
    key = advert_key(advert)
    now = time.monotonic()
    with _lock:
        done = _done.get(name)
        if name in _inflight or (done and done[0] == key and now - done[1] < REVERIFY_S):
            return False
        wait = BACKOFF_S[min(_failures.get(name, 0), len(BACKOFF_S)) - 1] if _failures.get(name) else COOLDOWN_S
        if now - _last.get(name, -wait) < wait:
            return False
        _inflight.add(name)
        _last[name] = now

    def run():
        m = contract()
        try:
            if key[0] == 'absent':
                record_state(name, 'not_offered', run={'reason': 'Wrapper does not advertise ' + m.CAPABILITY})
                handled = True
            elif key[0] == 'disabled':
                record_state(name, 'disabled', run={'reason': 'disabled', 'wrapper': _brief(advert)})
                handled = True
            elif key[0] == 'unavailable':
                record_state(name, 'unavailable', run={'wrapper': _brief(advert)})
                handled = True
            else:
                # Compared with the advert that triggered it: a Wrapper that rebuilt
                # meanwhile advertises a new generation and syncs again.
                handled = handled_by(key, sync(worker))
            with _lock:
                _failures.pop(name, None)
                _logged.pop(name, None)
                if handled:
                    _done[name] = (key, time.monotonic())
        except m.ModelsDbChanged as exc:
            # A rebuild during the read is not a failure: nothing was written, the next
            # advert (new generation) or REVERIFY_S retries without backoff.
            log.info('%s: models-db rebuilt during the read; retrying later (%s)', name, exc)
        except Exception as exc:  # noqa: BLE001 — a failed pull must never touch telemetry
            text = f'{type(exc).__name__}: {exc}'[:2000]
            with _lock:
                _failures[name] = _failures.get(name, 0) + 1
                repeated = _logged.get(name) == text
                _logged[name] = text
            if repeated:
                log.debug('%s: models-db sync failed again: %s', name, text)
            else:
                log.warning('%s: models-db sync failed: %s', name, text)
            try:
                record_state(name, 'error', error=text)
            except Exception:  # noqa: BLE001
                log.debug('%s: could not record models-db sync failure', name, exc_info=True)
        finally:
            with _lock:
                _inflight.discard(name)

    threading.Thread(target=run, name=f'models-db-{name}', daemon=True).start()
    return True


# --------------------------------------------------------------------------- pure helpers

def partition_uid(value):
    """Partition key of a row or digest: global tables and unattributed rows are ''."""
    return '' if value is None else str(value)


def mirrored(table):
    """Core mirrors the contract's section tables and global tables, never lazy ones."""
    m = contract()
    return table not in m.LAZY_TABLES and (table in m.SECTION_OF or table in m.GLOBAL_TABLES)


def is_staging(value):
    """A download-staging key or directory (``<name>.tmp-<pid>`` as a path segment)."""
    return isinstance(value, str) and bool(STAGING_RE.search(value))


def staging_model(row):
    """A models row that describes a staging copy rather than a model."""
    return any(is_staging(row.get(column)) for column in ('model_uid', *STAGING_MODEL_COLUMNS))


def strip_surrogates(table, row):
    """The row without its per-build surrogate ids (SURROGATE_COLUMNS)."""
    drop = SURROGATE_COLUMNS.get(table)
    if not drop or not any(column in row for column in drop):
        return row
    return {key: value for key, value in row.items() if key not in drop}


def stored_columns(table, columns):
    drop = SURROGATE_COLUMNS.get(table, ())
    return [column for column in columns if column not in drop]


def remote_partitions(digests, skipped=None):
    """{(table, uid): (rows, digest)} from the Wrapper's digest index, mirrored tables only.

    Partitions of a staging uid are left out (counted in ``skipped['partitions']``)."""
    out = {}
    for entry in digests or ():
        if not isinstance(entry, dict):
            continue
        table = entry.get('table') or entry.get('table_name')
        if not table or not mirrored(table) or not entry.get('digest'):
            continue
        uid = partition_uid(entry.get('model_uid'))
        if uid and is_staging(uid):
            if skipped is not None:
                skipped['partitions'] = skipped.get('partitions', 0) + 1
            continue
        rows = entry.get('rows')
        out[(str(table), uid)] = (
            int(rows) if isinstance(rows, (int, float)) and not isinstance(rows, bool) else None,
            str(entry['digest']))
    return out


def diff(remote, local):
    """Partitions to replace and to delete, per table.

    remote: {(table, uid): (rows, digest)}; local: {(table, uid): digest}.
    Returns (changed, vanished), each {table: set(uid)}."""
    changed, vanished = {}, {}
    for (table, uid), (_, digest) in remote.items():
        if local.get((table, uid)) != digest:
            changed.setdefault(table, set()).add(uid)
    for table, uid in local:
        if (table, uid) not in remote:
            vanished.setdefault(table, set()).add(uid)
    return changed, vanished


def read_plan(changed, remote):
    """[(table, uid_or_None, wanted_uids)]: None = one whole-table read, filtered to wanted.

    Global tables and a per-model table's '' (unattributed) partition are read with
    model_uid='' (the Wrapper selects model_uid NULL or ''); a whole-table read is
    used when many partitions of one table changed (fewer, larger requests).
    ``models`` is read first so a staging models row is known before its other rows."""
    totals = {}
    for table, _ in remote:
        totals[table] = totals.get(table, 0) + 1
    plan = []
    for table in sorted(changed, key=lambda t: (t != 'models', t)):
        uids = changed[table]
        whole = len(uids) > 1 and (len(uids) >= WHOLE_TABLE_MIN
                                   or len(uids) > totals.get(table, 0) * WHOLE_TABLE_SHARE)
        if whole:
            plan.append((table, None, frozenset(uids)))
        else:
            plan.extend((table, uid, frozenset((uid,))) for uid in sorted(uids))
    return plan


def clean(value):
    """JSON value Postgres jsonb accepts: no NUL characters, no NaN/Infinity."""
    if isinstance(value, str):
        return value.replace('\x00', '') if '\x00' in value else value
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {clean(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    return value


def iter_rows(client, table, model_uid=None, build_id=None, generation=None, limit=None):
    """Every row of a Wrapper table (or one partition) as dicts, every page pinned to
    build_id + generation (the Wrapper answers 409 -> ModelsDbChanged when either moved;
    a page reporting another build/generation raises the same)."""
    m = contract()
    after = 0
    limit = limit or m.ROWS_LIMIT
    while True:
        page = client.rows(table, after=after, limit=limit, model_uid=model_uid, build_id=build_id,
                           generation=generation or None)
        got_build, got_gen = page.get('build_id'), _generation(page.get('generation'))
        if build_id is None:
            build_id = got_build
        elif got_build not in (None, build_id):
            raise m.ModelsDbChanged('Wrapper rebuilt its models database during the read', 409)
        if not generation:
            generation = got_gen
        elif got_gen and got_gen != generation:
            raise m.ModelsDbChanged('Wrapper replaced its models database file during the read', 409)
        columns = page['columns']
        for row in page['rows']:
            yield dict(zip(columns, row))
        following = page.get('next_after')
        if not page.get('more') or not page['rows']:
            return
        if not isinstance(following, int) or following <= after:
            raise m.ModelsDbError('Wrapper rows paging did not advance for ' + str(table))
        after = following


def fetch(client, plan, build_id, remote, spool, generation=None, stats=None):
    """Read every planned partition into ``spool`` (JSON lines [table, uid, ord, row]).

    Returns {table: [columns]} for every table read (surrogates left out). Each
    partition's row count must match the digest index; ord is the row's position in
    the Wrapper's rowid order among the rows kept. ``stats`` (optional dict) gets
    rows_written, reads and staging_skipped_rows."""
    m = contract()
    stats = {} if stats is None else stats
    columns, counts, seen = {}, {}, {}
    staging_uids = set()
    for table, uid, wanted in plan:
        stats['reads'] = stats.get('reads', 0) + 1
        for row in iter_rows(client, table, model_uid=uid, build_id=build_id, generation=generation):
            if table not in columns:
                columns[table] = stored_columns(table, list(row))
            part = '' if table in m.GLOBAL_TABLES else partition_uid(row.get('model_uid'))
            if part not in wanted:
                continue
            seen[(table, part)] = seen.get((table, part), 0) + 1
            if part and (part in staging_uids or (table == 'models' and staging_model(row))):
                # a staging copy: never stored as a model of its own
                staging_uids.add(part)
                stats['staging_skipped_rows'] = stats.get('staging_skipped_rows', 0) + 1
                continue
            ord_ = counts.get((table, part), 0)
            counts[(table, part)] = ord_ + 1
            # header TAB row: json.dumps escapes tabs and newlines inside strings
            spool.write(json.dumps([table, part, ord_]).encode('utf-8') + b'\t'
                        + json.dumps(clean(strip_surrogates(table, row)), ensure_ascii=False, allow_nan=False,
                                     separators=(',', ':')).encode('utf-8') + b'\n')
            stats['rows_written'] = stats.get('rows_written', 0) + 1
        for part in wanted:
            expected = remote.get((table, part), (None, None))[0]
            got = seen.get((table, part), 0)
            if expected is not None and got != expected:
                raise ValueError(f'{table}[{part!r}]: read {got} rows, digest index says {expected}')
    if staging_uids:
        stats['staging_uids'] = sorted(staging_uids)[:20]
    return columns


def spooled(spool):
    """Rows back out of the spool: (table, uid, ord, row as JSON text)."""
    spool.seek(0)
    for line in spool:
        head, _, row = line.rstrip(b'\n').partition(b'\t')
        table, uid, ord_ = json.loads(head)
        yield table, uid, ord_, row.decode('utf-8')


def parse_time(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return datetime.fromtimestamp(value, timezone.utc)
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip())
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _now_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _jsonb(value):
    from psycopg.types.json import Jsonb as _Jsonb
    return _Jsonb(value)


def _int(value):
    try:
        return int(value) if value is not None and not isinstance(value, bool) else None
    except (TypeError, ValueError):
        return None


def _brief(reply):
    """The Wrapper fields worth keeping from a status/advert that is not a build."""
    if not isinstance(reply, dict):
        return None
    return {key: reply[key] for key in ('available', 'enabled', 'reason', 'building', 'build_id', 'generation',
                                        'built_at', 'last_error', 'last_started_at', 'last_finished_at',
                                        'failed_sections') if key in reply}


# --------------------------------------------------------------------------- sync

def client_for(worker, timeout=HTTP_TIMEOUT_S):
    """WrapperModelsDb with the URL and bearer key intake uses for this worker."""
    from hugpy_core.registry.transport import headers
    auth = headers(worker).get('Authorization', '')
    key = auth[7:] if auth.startswith('Bearer ') else None
    return contract().WrapperModelsDb(worker['url'], key=key, timeout=timeout)


def _db():
    from hugpy_core.intake.store import store
    return store()


def load_local(conn, name):
    """(mdb_builds row as dict or None, {(table, uid): digest})."""
    row = conn.execute('SELECT build_id, sync_state, columns, generation FROM mdb_builds WHERE worker=%s',
                       (name,)).fetchone()
    build = None if row is None else {'build_id': row[0], 'sync_state': row[1], 'columns': row[2] or {},
                                      'generation': row[3] or ''}
    local = {(t, u): d for t, u, d in conn.execute(
        'SELECT table_name, model_uid, digest FROM mdb_digests WHERE worker=%s', (name,))}
    return build, local


def _digests(client, build_id, generation):
    """The digest index, pinned to build_id + generation as far as the terminal supports
    (the caller compares the reply's build_id/generation either way)."""
    try:
        params = inspect.signature(client.digests).parameters
    except (TypeError, ValueError):
        params = {}
    pins = {'build_id': build_id, 'generation': generation or None}
    return client.digests(**{k: v for k, v in pins.items() if k in params and v})


def sync(worker):
    """Bring one worker's projection up to its current build and generation.

    Returns {'state': synced|not_offered|disabled|unavailable|dropped, 'build_id',
    'generation', ...}. Raises on any failure (nothing is written then, except by the
    caller's error record); ModelsDbChanged when the Wrapper rebuilt mid-read."""
    m = contract()
    name = worker['name']
    started = time.monotonic()
    client = client_for(worker)
    try:
        status = client.status()
    except m.ModelsDbUnavailable as exc:
        record_state(name, 'not_offered', run={'reason': str(exc)[:500]})
        return {'state': 'not_offered'}
    build_id = str(status.get('build_id') or '')
    generation = _generation(status.get('generation'))
    if not status.get('available') or not build_id:
        state = 'disabled' if _disabled(status) else 'unavailable'
        # 'unavailable' keeps the last good status and rows; only the bookkeeping changes.
        record_state(name, state, error=status.get('last_error') if state == 'unavailable' else None,
                     run={'reason': status.get('reason'), 'wrapper': _brief(status)})
        return {'state': state}
    db = _db()
    with db.connect() as conn:
        previous, local = load_local(conn, name)
    if (previous and local and previous['sync_state'] == 'synced' and previous['build_id'] == build_id
            and previous['generation'] == generation):
        return {'state': 'synced', 'build_id': build_id, 'generation': generation, 'unchanged': True}
    index = _digests(client, build_id, generation)
    if str(index.get('build_id') or '') != build_id:
        raise m.ModelsDbChanged('Wrapper rebuilt its models database between status and digests', 409)
    index_gen = _generation(index.get('generation'))
    if generation and index_gen and index_gen != generation:
        raise m.ModelsDbChanged('Wrapper replaced its models database file between status and digests', 409)
    skipped = {}
    remote = remote_partitions(index['digests'], skipped)
    changed, vanished = diff(remote, local)
    plan = read_plan(changed, remote)
    stats = {}
    # Finish all network reads before opening the write transaction.
    with tempfile.TemporaryFile(prefix='hugpy-mdb-') as spool:
        columns = fetch(client, plan, build_id, remote, spool, generation=generation, stats=stats)
        from hugpy_core.registry.registrations import get as saved_connection, is_connected
        if not is_connected(saved_connection(name)):
            return {'state': 'dropped'}   # disconnected while this pull was in flight: drop it
        run = {
            'at': _now_iso(), 'state': 'synced', 'build_id': build_id, 'generation': generation or None,
            'mode': 'full' if not local else ('refresh' if not changed and not vanished else 'diff'),
            'partitions': {'remote': len(remote), 'changed': sum(map(len, changed.values())),
                           'removed': sum(map(len, vanished.values()))},
            'reads': stats.get('reads', 0), 'rows_written': stats.get('rows_written', 0),
            'staging_skipped': {'partitions': skipped.get('partitions', 0),
                                'rows': stats.get('staging_skipped_rows', 0),
                                'uids': stats.get('staging_uids', [])},
            'failed_sections': status.get('failed_sections'),
            'seconds': round(time.monotonic() - started, 2),
        }
        with db.connect() as conn:
            applied = apply(conn, name, status, previous, local, remote, changed, vanished, columns, spool, run)
    if applied and (changed or vanished):
        log.info('%s: models-db %s mirrored (%d tables changed, %d partitions replaced, %d removed)',
                 name, build_id[:12], len(set(changed) | set(vanished)),
                 run['partitions']['changed'], run['partitions']['removed'])
    if skipped.get('partitions') or stats.get('staging_skipped_rows'):
        log.info('%s: models-db skipped download-staging copies (%d partitions, %d rows)',
                 name, skipped.get('partitions', 0), stats.get('staging_skipped_rows', 0))
    return {'state': 'synced', 'build_id': build_id, 'generation': generation, 'applied': applied}


def apply(conn, name, status, previous, local, remote, changed, vanished, columns, spool, run=None):
    """The ONE write transaction (the caller's connection context commits it)."""
    conn.execute("SELECT pg_advisory_xact_lock(hashtext('hugpy-mdb:' || %s::text))", (name,))
    row = conn.execute('SELECT build_id, sync_state, columns, generation FROM mdb_builds WHERE worker=%s',
                       (name,)).fetchone()
    build_id, generation = str(status['build_id']), _generation(status.get('generation'))
    now_build, now_gen = (row[0], row[3] or '') if row else (None, '')
    if row and now_build == build_id and now_gen == generation and row[1] == 'synced' and local:
        return False   # another collector applied this build meanwhile
    if (now_build, now_gen) != ((previous or {}).get('build_id'), (previous or {}).get('generation') or ''):
        raise RuntimeError('mdb_builds changed during the models-db read; retrying')
    if not local:
        # Full (re)build: nothing of this worker is tracked, so nothing stale may survive.
        for target in ('mdb_rows', 'mdb_digests'):
            conn.execute(f'DELETE FROM {target} WHERE worker=%s', (name,))
    else:
        held, offered = {}, {}
        for table, uid in local:
            held.setdefault(table, set()).add(uid)
        for table, uid in remote:
            offered.setdefault(table, set()).add(uid)
        for table in sorted(set(changed) | set(vanished)):
            drop = changed.get(table, set()) | vanished.get(table, set())
            if (held.get(table, set()) | offered.get(table, set())) <= drop:
                for target in ('mdb_rows', 'mdb_digests'):
                    conn.execute(f'DELETE FROM {target} WHERE worker=%s AND table_name=%s', (name, table))
            else:
                for target in ('mdb_rows', 'mdb_digests'):
                    conn.execute(f'DELETE FROM {target} WHERE worker=%s AND table_name=%s '
                                 'AND model_uid = ANY(%s::text[])', (name, table, sorted(drop)))
    with conn.cursor() as cur:
        with cur.copy('COPY mdb_rows (worker, table_name, model_uid, ord, "row") FROM STDIN') as copy:
            for table, uid, ord_, text in spooled(spool):
                copy.write_row((name, table, uid, ord_, text))
        with cur.copy('COPY mdb_digests (worker, table_name, model_uid, "rows", digest) FROM STDIN') as copy:
            for table in sorted(changed):
                for uid in sorted(changed[table]):
                    rows, digest = remote[(table, uid)]
                    copy.write_row((name, table, uid, rows or 0, digest))
    kept = dict((row[2] if row else None) or {})
    kept.update(columns)
    present = {table for table, _ in remote}
    kept = {table: stored_columns(table, cols) for table, cols in kept.items() if table in present}
    conn.execute(
        'INSERT INTO mdb_builds (worker, store_id, build_id, generation, built_at, builder_version,'
        ' source_user_version, models, status, columns, run, synced_at, sync_state, error) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s,NULL) '
        'ON CONFLICT (worker) DO UPDATE SET store_id=EXCLUDED.store_id, build_id=EXCLUDED.build_id,'
        ' generation=EXCLUDED.generation, built_at=EXCLUDED.built_at, builder_version=EXCLUDED.builder_version,'
        ' source_user_version=EXCLUDED.source_user_version, models=EXCLUDED.models,'
        ' status=EXCLUDED.status, columns=EXCLUDED.columns, run=EXCLUDED.run, synced_at=now(),'
        ' sync_state=EXCLUDED.sync_state, error=NULL',
        (name, status.get('store_id'), build_id, generation or None, parse_time(status.get('built_at')),
         status.get('builder_version'), _int(status.get('source_user_version')), _int(status.get('models')),
         _jsonb(clean(status)), _jsonb(kept), _jsonb(clean(run or {})), 'synced'))
    # Listeners wake only after this transaction commits (NOTIFY is transactional).
    conn.execute('SELECT pg_notify(%s, %s)', (notify_channel('mdb_changed'), name))
    return True


def record_state(name, state, error=None, run=None):
    """Upsert only the bookkeeping columns of mdb_builds; mirrored rows stay as they are.

    The Wrapper status of the last good sync is kept (an unavailable or switched-off
    Wrapper does not erase what Core last mirrored). Neutral states (not_offered,
    disabled) clear the error; 'unavailable' and 'error' record it with error_at."""
    if state not in STATES:
        raise ValueError(state)
    neutral = state in NEUTRAL_STATES
    text = None if neutral or error is None else str(error)[:2000]
    run = dict(run or {})
    run.setdefault('at', _now_iso())
    run['state'] = state
    if text:
        run.setdefault('error', text)
    with _db().connect() as conn:
        conn.execute(
            'INSERT INTO mdb_builds (worker, sync_state, error, error_at, run) VALUES (%s,%s,%s,%s,%s) '
            'ON CONFLICT (worker) DO UPDATE SET sync_state=EXCLUDED.sync_state, error=EXCLUDED.error,'
            ' error_at=COALESCE(EXCLUDED.error_at, mdb_builds.error_at), run=EXCLUDED.run',
            (name, state, text, None if text is None else datetime.now(timezone.utc), _jsonb(clean(run))))
        conn.execute('SELECT pg_notify(%s, %s)', (notify_channel('mdb_changed'), name))


__all__ = ['schedule', 'sync', 'advert_key', 'handled_by', 'diff', 'read_plan', 'remote_partitions', 'fetch',
           'iter_rows', 'apply', 'record_state', 'client_for', 'contract', 'contract_problem', 'TerminalTooOld',
           'is_staging', 'staging_model', 'strip_surrogates', 'SURROGATE_COLUMNS', 'STAGING_RE',
           'NEUTRAL_STATES', 'COOLDOWN_S', 'REVERIFY_S']
