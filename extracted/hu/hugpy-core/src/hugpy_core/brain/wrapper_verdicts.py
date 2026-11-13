"""Mirror wrapper-owned verdicts. No model sizing, fit solving or file reads."""
from __future__ import annotations

from collections import defaultdict
import os
import psycopg
from psycopg.types.json import Jsonb

from hugpy_core.imports import functions as F


def fetch(worker):
    from hugpy_core.registry.transport import request as _request, target
    configured = target(worker)
    # An empty preview resolves saved pair/box defaults at the owning Wrapper.
    # Core's observed settings can lag a local terminal edit.
    return _request(configured, '/v1/verdicts/plan', {'settings': {}})


def cells(verdict):
    for name, cell in (verdict.get('memory') or {}).items():
        if name == 'bnb_4bit':
            for mode, inner in (cell or {}).items():
                if isinstance(inner, dict) and inner.get('supported') is not False:
                    yield mode + ':bnb4', inner
        elif isinstance(cell, dict) and cell.get('supported') is not False:
            yield name, cell


def fit_value(values):
    """Aggregate reported tri-state verdicts without evaluating requirements."""
    values = list(values)
    if any(v is True for v in values):
        return True
    return False if values and all(v is False for v in values) else None


def selected(rows, settings):
    row = next((r for r in rows if r['file'] == settings.get('gguf_file')), None)
    row = row or next((r for r in rows if r.get('elected')), rows[0])
    auto = row.get('auto') or {}
    mode = settings.get('alloc_mode')
    moe = settings.get('moe') is True
    branch = ('bnb_moe_explicit' if moe else 'bnb_4bit') if settings.get('bnb_4bit') else 'moe_explicit' if moe else 'standard'
    if not mode or mode in ('auto','automatic'):
        mode = (auto.get(branch) or auto.get('standard') or {}).get('mode')
    memory = row.get('memory') or {}
    if settings.get('bnb_4bit'):
        memory = memory.get('bnb_4bit') or {}
    from hugpy_core.intake.schema import cell
    return row, mode, cell(memory, mode) or {}


def _parent_model_key(key, file):
    from hugpy_core.models.identity import parent_key
    return parent_key(key, file)


def apply(conn, worker, document):
    """One atomic snapshot; retain operator settings and prune only absent verdicts."""
    from hugpy_core.intake.mirror import without_nul
    document = without_nul(document)
    name, wid = worker.get('name') or worker['id'], worker['id']
    if document.get('worker') != name or not isinstance(document.get('verdicts'), list):
        raise ValueError('invalid wrapper verdict snapshot or worker identity')
    reported_keys = [(r.get('model_key'), r.get('file')) for r in document['verdicts']]
    if len(set(reported_keys)) != len(reported_keys):
        raise ValueError('duplicate wrapper verdict key')
    observed = set()
    for (ids,) in conn.execute("SELECT payload->'models' FROM worker_presence"):
        if isinstance(ids, list):
            observed.update(key for key in ids if isinstance(key, str))
    # Keep the quant file and its measurements, but collapse the old
    # owner~repo~GGUF-stem identity before it creates model-worker routes.
    aliases = dict(conn.execute("SELECT alias_key,model_key FROM model_key_aliases"))
    # Prefer discovery's explicit handle mapping over historical suffix repair.
    from hugpy_core.models.identity import resolve_handle
    discovery = []
    for copy_key, details in conn.execute(
            "SELECT model_key,details FROM model_copies WHERE location_kind='worker' AND location_id=%s AND present", (name,)):
        discovery.append({'model_key':copy_key, 'identity':(details or {}).get('identity') or {}})
    normalized = {}
    for source in document['verdicts']:
        key = resolve_handle(source.get('model_key'), discovery)
        if key == source.get('model_key') and key not in observed:
            key = _parent_model_key(key, source.get('file'))
        if key != source.get('model_key') and key not in observed:
            # A unique ownerless key may already be the fleet's chosen ID.
            short = key.rsplit('~', 1)[-1]
            if short in observed:
                key = short
        key = aliases.get(key, key)
        row = {**source, 'model_key': key}
        pair = (key, row.get('file'))
        if pair not in normalized or key == source.get('model_key'):
            normalized[pair] = row
    rows = list(normalized.values())
    from hugpy_core.intake import schema
    for r in rows:   # the schema in the middle: canonical placements when enabled
        if isinstance(r.get('memory'), dict):
            r['memory'] = schema.memory(r['memory'])
        r['auto'] = schema.auto(r.get('auto'))
    if any(not r.get('model_key') or not r.get('file') or not isinstance(r.get('memory'), dict) for r in rows):
        raise ValueError('incomplete wrapper verdict row')
    keys = [(r['model_key'],r['file']) for r in rows]
    if len(set(keys)) != len(keys):
        raise ValueError('duplicate wrapper verdict key')
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['model_key']].append(row)
    budget, room = document.get('budgets') or {}, document.get('available') or {}
    conn.execute("INSERT INTO worker_budgets(worker_id,name,gpu_budget,ram_budget,swap_free,last_change,reported_available) "
                 "VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(worker_id) DO UPDATE SET "
                 "gpu_budget=EXCLUDED.gpu_budget,ram_budget=EXCLUDED.ram_budget,swap_free=EXCLUDED.swap_free,"
                 "last_change=EXCLUDED.last_change,reported_available=EXCLUDED.reported_available,observed_at=now()",
                 (wid,name,budget.get('gpu_budget'),budget.get('ram_budget'),budget.get('swap'),
                  Jsonb({'source':'wrapper','at':document.get('at')}),Jsonb(room)))
    for key, variants in grouped.items():
        conn.execute("INSERT INTO model_workers(model_key,worker_id,source) VALUES (%s,%s,'wrapper') "
                     "ON CONFLICT DO NOTHING", (key,wid))
        settings = conn.execute("SELECT user_settings FROM model_workers WHERE model_key=%s AND worker_id=%s",
                                (key,wid)).fetchone()[0] or {}
        chosen, mode, cell = selected(variants,settings)
        fits = fit_value(c.get('fits') for v in variants for _, c in cells(v))
        # Plan contains selection only. Requirement values live once in the quant mirror.
        plan = {'source':'wrapper','default_variant':chosen['file'],'quants':[v['file'] for v in variants]}
        conn.execute("UPDATE model_workers SET plan=%s,fits=%s,updated_at=now() WHERE model_key=%s AND worker_id=%s "
                     "AND (plan,fits) IS DISTINCT FROM (%s,%s)",
                     (Jsonb(plan),fits,key,wid,Jsonb(plan),fits))
        for v in variants:
            modes = [m for m,c in cells(v) if c.get('fits') is True]
            # Retain the remaining wrapper fields as source metadata, once.
            extra = {k:value for k,value in v.items() if k not in ('memory','auto','moe_offered')}
            extra['authority'] = 'wrapper'
            payload = (fit_value(c.get('fits') for _,c in cells(v)),Jsonb(modes),Jsonb(v['memory']),
                       Jsonb(v.get('auto') or {}),bool(v.get('moe_offered')),Jsonb(extra))
            conn.execute("INSERT INTO model_worker_quants(model_key,worker_id,file,fits,modes,memory,auto,moe_offered,inputs) "
                         "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(model_key,worker_id,file) DO UPDATE SET "
                         "fits=EXCLUDED.fits,modes=EXCLUDED.modes,memory=EXCLUDED.memory,auto=EXCLUDED.auto,"
                         "moe_offered=EXCLUDED.moe_offered,inputs=EXCLUDED.inputs,computed_at=now() "
                         "WHERE (model_worker_quants.fits,model_worker_quants.modes,model_worker_quants.memory,"
                         "model_worker_quants.auto,model_worker_quants.moe_offered,model_worker_quants.inputs) IS DISTINCT FROM "
                         "(EXCLUDED.fits,EXCLUDED.modes,EXCLUDED.memory,EXCLUDED.auto,EXCLUDED.moe_offered,EXCLUDED.inputs)",
                         (key,wid,v['file'],*payload))
    # A complete empty snapshot clears stale calculated results, not assignments.
    conn.execute("DELETE FROM model_worker_quants WHERE worker_id=%s AND NOT EXISTS ("
                 "SELECT 1 FROM jsonb_to_recordset(%s) AS x(model_key text,file text) "
                 "WHERE x.model_key=model_worker_quants.model_key AND x.file=model_worker_quants.file)",
                 (wid,Jsonb([{'model_key':k,'file':f} for k,f in keys])))
    conn.execute("UPDATE model_workers SET plan=NULL,fits=NULL WHERE worker_id=%s AND NOT(model_key=ANY(%s)) "
                 "AND (plan IS NOT NULL OR fits IS NOT NULL)", (wid,list(grouped)))
    # Discovery-derived pairs are current availability, not durable assignments.
    # Retain explicit operator choices when a model disappears from a full report.
    conn.execute("DELETE FROM model_workers WHERE worker_id=%s AND source='wrapper' "
                 "AND NOT(model_key=ANY(%s)) AND NOT assigned AND NOT pinned "
                 "AND user_settings='{}'::jsonb AND env_profile IS NULL",
                 (wid,list(grouped)))
    return {'worker':name,'pairs':len(grouped),'files':len(rows),'source':'wrapper'}


def refresh(worker, *, force=False):
    # A wrapper that said it serves no verdict plans is never asked for one,
    # whichever path triggers the refresh (planner, knob save, console).
    capabilities = (worker.get('data_service') or {}).get('capabilities') or {}
    if capabilities.get('verdicts') is False:
        return {'worker': worker.get('name') or worker['id'], 'source': 'wrapper',
                'skipped': 'wrapper serves no verdict plans'}
    # A core HTTP process and its independent collector share this gate.
    # The lock prevents duplicate requests across processes, not just threads.
    name = worker.get('name') or worker['id']
    with psycopg.connect(F.core_dsn(), autocommit=True) as conn:
        if force:
            conn.execute("SELECT pg_advisory_lock(hashtextextended(%s, 936))", (name,))
            locked = True
        else:
            locked = conn.execute("SELECT pg_try_advisory_lock(hashtextextended(%s, 936))", (name,)).fetchone()[0]
        if not locked:
            return {'worker':name,'source':'wrapper','skipped':'refresh in progress'}
        try:
            fresh = conn.execute("SELECT observed_at > now()-interval '5 seconds' AND last_change->>'source'='wrapper' "
                                 "FROM worker_budgets WHERE worker_id=%s", (worker['id'],)).fetchone()
            if not force and fresh and fresh[0]:
                return {'worker':name,'source':'wrapper','skipped':'recent observation'}
            document = fetch(worker)
            with conn.transaction():
                return apply(conn,worker,document)
        finally:
            conn.execute("SELECT pg_advisory_unlock(hashtextextended(%s, 936))", (name,))
