"""Console simulation and reusable experiment templates; no live action path."""
from __future__ import annotations

import hashlib
import json
import time
import uuid

from psycopg.types.json import Jsonb

from hugpy_core.brain.distribution_sim import number, simulate, validate
from hugpy_core.models import modeldb
from hugpy_core.registry import registry


def catalog():
    from hugpy_core.web.native_fleet import models
    with modeldb._conn() as conn:
        budgets = {r['worker_id']:dict(r) for r in conn.execute('SELECT * FROM worker_budgets')}
    workers = []
    for worker in registry.all_workers():
        wid = worker['id']
        b = budgets.get(wid) or {}
        available = b.get('reported_available') or {}
        budget = {'gpu':number(b.get('gpu_budget')), 'ram':number(b.get('ram_budget')),
                  'swap':number(b.get('swap_free')),
                  'cpu':number((worker.get('cpu') or {}).get('physical_cores')) or number(available.get('cores'))}
        workers.append({'id':wid,'name':worker.get('name') or wid,'online':registry.is_online(worker),
                        'picker_worker':{k:worker[k] for k in ('id','name','storage','models_local','models_central','models_discovered') if k in worker},
                        'budget':budget,'available':{'gpu':number(available.get('gpu')),
                        'ram':number(available.get('ram')),'swap':number(available.get('swap')),
                        'cpu':number(available.get('cores'))},'observed_at':b.get('observed_at')})
    rows = models(picker_facts=True)
    return {'workers':workers,'models':rows,'simulation_only':True}


def snapshot(configuration):
    listing = catalog()
    workers = {w['id']:w for w in listing['workers']}
    keys = configuration['models']
    if any(w['id'] not in workers or not workers[w['id']]['online'] for w in configuration['workers']):
        raise ValueError('Selected workers must still be available; refresh the simulation catalog')
    models = {r['model_key']:r for r in modeldb.fetch_rows(keys=keys,include_evidence=False)}
    if set(models) != set(keys):
        raise ValueError('Some selected model identities changed; refresh the simulation catalog')
    for item in listing['models']:
        if item['id'] in models:
            models[item['id']]['tasks'] = item['tasks']
    workers = {w['id']:workers[w['id']] for w in configuration['workers']}
    data = {'workers':workers,'models':models}
    digest = hashlib.sha256(json.dumps(data,sort_keys=True,default=str).encode()).hexdigest()
    return {**data,'meta':{'id':digest,'captured_at':time.time(),
            'source':'Core mirror of wrapper budgets and per-model resource verdicts',
            'worker_observed_at':{wid:w['observed_at'] for wid,w in workers.items()}}}


def run(scenario=None):
    try:
        configuration = validate(scenario)
        return {'ok':True,'report':simulate(snapshot(configuration),configuration)}
    except (ValueError, KeyError) as exc:
        return {'ok':False,'error':str(exc)},400


def templates():
    with modeldb._conn() as conn:
        rows = [dict(row) for row in conn.execute('SELECT * FROM simulation_templates ORDER BY updated_at DESC')]
    return {'templates':rows}


def save_template(name='', description='', scenario=None, id=None, revision=None):
    try:
        if not isinstance(name,str) or not name.strip() or len(name) > 120:
            raise ValueError('Use a template name of 1–120 characters')
        if not isinstance(description,str) or len(description) > 2000:
            raise ValueError('Template description is too long')
        configuration = validate(scenario)
        if id is not None and (not isinstance(id,str) or not id):
            raise ValueError('Invalid template ID')
        with modeldb._conn() as conn:
            if id:
                if not isinstance(revision,int) or isinstance(revision,bool):
                    raise ValueError('Reload the template before saving')
                row = conn.execute('UPDATE simulation_templates SET name=%s,description=%s,scenario=%s,'
                    'revision=revision+1,updated_at=now() WHERE id=%s AND revision=%s RETURNING *',
                    (name.strip(),description,Jsonb(configuration),id,revision)).fetchone()
                if row is None:
                    return {'ok':False,'error':'Template changed in another tab; reload it before saving'},409
            else:
                row = conn.execute('INSERT INTO simulation_templates(id,name,description,scenario) '
                    'VALUES (%s,%s,%s,%s) RETURNING *',
                    (uuid.uuid4().hex,name.strip(),description,Jsonb(configuration))).fetchone()
        return {'ok':True,'template':dict(row)}
    except ValueError as exc:
        return {'ok':False,'error':str(exc)},400


def delete_template(id=None, revision=None):
    if not isinstance(id,str) or not id or not isinstance(revision,int) or isinstance(revision,bool):
        return {'ok':False,'error':'Template ID and revision are required'},400
    with modeldb._conn() as conn:
        removed = conn.execute('DELETE FROM simulation_templates WHERE id=%s AND revision=%s RETURNING id',
                               (id,revision)).fetchone()
    if removed is None:
        return {'ok':False,'error':'Template changed or was already deleted; reload the list'},409
    return {'ok':True}
