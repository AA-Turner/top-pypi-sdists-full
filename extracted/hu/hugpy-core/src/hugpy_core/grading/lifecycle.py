"""Temporary static residency around grading, using existing worker controls.

No fit estimates or victim selection live here. The worker's normal copier,
placement admission and reaper remain authoritative.
"""
from __future__ import annotations

import logging
import time
import urllib.parse
from contextlib import contextmanager
from psycopg.types.json import Jsonb

log = logging.getLogger(__name__)


class UnsettledCopy(RuntimeError):
    pass


def target(worker):
    from hugpy_core.registry.transport import target as registered_target
    return registered_target(worker)


def request(worker, path, body=None):
    from hugpy_core.registry.transport import request as _request
    return _request(worker,path,body)


def settings(worker, key):
    result = request(worker,'/v1/settings/pair?'+urllib.parse.urlencode({'model_key':key}))
    if not isinstance(result.get('settings'),dict):
        raise ValueError('Worker did not report its own settings')
    return result['settings']


def residency(worker,key,value,owner):
    result=request(worker,'/v1/settings/pair',{'model_key':key,'settings':{'residency':value},
                                            'requested_by':owner})
    if result.get('settings',{}).get('residency') != value:
        raise ValueError('Worker did not confirm residency change')


def journal(identity,worker,key,previous):
    from hugpy_core.models import modeldb
    with modeldb._conn() as conn:
        conn.execute('INSERT INTO grading_residency(id,worker,model_key,previous,state) VALUES (%s,%s,%s,%s,%s)',
                     (identity,worker['name'],key,Jsonb({'residency':previous}),'active'))


def restore(identity,worker,key,previous):
    # A later explicit on-demand edit stands. Never touch any other knob.
    if settings(worker,key).get('residency')=='static':
        residency(worker,key,previous,identity+' cleanup')
    from hugpy_core.models import modeldb
    with modeldb._conn() as conn:
        conn.execute("UPDATE grading_residency SET state='restored',updated_at=now() WHERE id=%s",(identity,))


def recover():
    """Recover only temporary residency edits after an interrupted Core process."""
    from hugpy_core.models import modeldb
    with modeldb._conn() as conn:
        if not conn.execute("SELECT to_regclass('grading_residency') AS name").fetchone()['name']:
            return
        rows=conn.execute("SELECT * FROM grading_residency WHERE state='active'").fetchall()
    for row in rows:
        try:
            worker=target({'name':row['worker']})
            restore(row['id'],worker,row['model_key'],row['previous'].get('residency'))
        except Exception:
            log.exception('Temporary grading residency still needs cleanup: %s',row['id'])


def capacity_error(error):
    from hugpy_core.testfire.testfire import classify_error
    low=str(error).lower()
    return classify_error(low) in ('fit_failure','worker_busy','model_busy','capacity','LoadRefusal') or any(
        term in low for term in ('of room on','insufficient room','no room','cpu admission','resource refusal'))


def copy(worker,key,owner,stopped):
    from .supervisor import current
    lane=current()
    deadline=time.monotonic()+6*3600
    while not stopped.is_set():
        generation=lane.owner.generation(lane) if lane else 0
        if lane:lane.phase='staging'
        try:
            receipt=request(worker,'/v1/operator/actions',{'action':'copy-model','model_key':key,
                                                        'requested_by':owner,'params':{}})
        except Exception as exc:
            raise UnsettledCopy('Copy submission was not confirmed; inspect worker actions before releasing protection') from exc
        aid=receipt.get('id')
        if not isinstance(aid,int):raise UnsettledCopy('Worker returned no copy action ID')
        # The active transfer must settle before static protection is released.
        while time.monotonic()<deadline:
            try:row=request(worker,f'/v1/operator/actions/{aid}')
            except Exception as exc:
                raise UnsettledCopy('Copy action '+str(aid)+' is unresolved; protection retained') from exc
            if row.get('state') not in ('requested','running'):break
            time.sleep(.5)
        else:raise UnsettledCopy('Copy action remains unresolved; inspect worker action '+str(aid))
        if row.get('state')=='done':return
        error=(row.get('result') or {}).get('error') or 'Worker copy failed'
        if lane and capacity_error(error) and lane.owner.wait_capacity(lane,stopped,generation):continue
        raise ValueError(error)
    raise InterruptedError('Grading stopped before copy')


@contextmanager
def lane(run_id,model,worker,stopped,report):
    from hugpy_core.relay.pick import pick
    key=model['model_key']
    owner='benchmark:'+run_id+':'+str(worker.get('id') or worker.get('name'))+':'+key
    # Existing routing enforces operator exclusions and preserves pinned pairs.
    selected=pick(key,pin=worker.get('id') or worker['name'],source='grading')
    endpoint=target(selected)
    previous=settings(endpoint,key).get('residency')
    changed=previous!='static'
    if changed:journal(owner,endpoint,key,previous)
    unresolved=False
    try:
        if changed:residency(endpoint,key,'static',owner)
        report('lane',{'model':key,'worker':worker.get('name'),'phase':'staging'})
        if not stopped.is_set():copy(endpoint,key,owner,stopped)
        yield endpoint
    except UnsettledCopy:
        unresolved=True
        from hugpy_core.models import modeldb
        with modeldb._conn() as conn:
            conn.execute("UPDATE grading_residency SET state='copy-unresolved',updated_at=now() WHERE id=%s",(owner,))
        raise
    finally:
        if changed and not unresolved:
            try:
                restore(owner,endpoint,key,previous)
                report('lane',{'model':key,'worker':worker.get('name'),'phase':'released'})
            except Exception as exc:
                report('cleanup-error',{'model':key,'worker':worker.get('name'),'error':str(exc)})
                raise
