"""Snapshot-first grading coordinator; wrapper owns physical copy/reap/restore."""
from __future__ import annotations

import json
import time

from psycopg.types.json import Jsonb
from hugpy_core.models import modeldb
from hugpy_core.registry import registry


class StorageCycle:
    def __init__(self, job):
        self.job = job
        self.lease_id = None
        self.source = 'test-fire:' + job.job_id
        self.state = {'phase':'snapshotting','events':[],'errors':[]}
        self.job.storage = self.state

    def request(self, method, path, body=None):
        worker = registry.lookup_worker(self.job.worker_id)
        if not worker:
            raise ValueError('Grading worker disappeared')
        from hugpy_core.registry.transport import request, target
        return request(target(worker), path, body, method=method)

    def action(self, action, key=None, **params):
        receipt = self.request('POST','/v1/operator/actions',{'action':action,'model_key':key,
            'requested_by':self.source,'params':{'job_id':self.job.job_id,'lease_id':self.lease_id,**params}})
        if not isinstance(receipt.get('id'),int):
            raise ValueError('Worker returned no grading action ID')
        # Copies and restores may be large. The durable worker queue is authoritative;
        # never dispatch another grading call while a transfer is still in flight.
        deadline = time.monotonic()+6*3600
        while time.monotonic()<deadline:
            row = self.request('GET',f"/v1/operator/actions/{receipt['id']}")
            if row.get('state') not in ('requested','running'):
                result = row.get('result') or {}
                public = result.get('storage') or (result if 'phase' in result else None)
                if public:
                    self.lease_id = public.get('lease_id') or self.lease_id
                    self.state.update(public)
                if row.get('state') != 'done':
                    raise ValueError(str(result.get('error') or f'{action}: {row.get("state")}'))
                return result
            time.sleep(.5)
        raise TimeoutError('Worker grading action is still unresolved; snapshot retained for recovery')

    def begin(self, progress):
        # Snapshot all logical allocations once, including initially unassigned pairs.
        with modeldb._conn() as conn:
            rows = [dict(r) for r in conn.execute('SELECT model_key,assigned,pinned,source FROM model_workers WHERE worker_id=%s',
                                                (self.job.worker_id,))]
            conn.execute('INSERT INTO grading_storage_runs(job_id,worker_id,allocations,state) VALUES (%s,%s,%s,%s)',
                         (self.job.job_id,self.job.worker_id,Jsonb(rows),'active'))
        graded = [key for key,row in progress.items() if row['status']=='complete']
        # Include completed local copies outside the selected subset as reclaim candidates.
        from hugpy_core.grading import grader
        from hugpy_core.testfire.testfire import _catalog, model_tasks
        for key,row in _catalog().items():
            suites = grader.suites_for_tasks(model_tasks(row))
            if suites and key not in progress and all(not grader.pending_items(key,suite) for suite in suites):
                graded.append(key)
        self.action('station-grading-begin',models=self.job.models,graded=graded)
        self.job.station_lease = self.lease_id
        self.state['phase'] = 'grading'

    def fill(self, pending):
        result = self.action('station-grading-fill',pending=pending)
        self.state['phase'] = 'grading'
        return result

    def complete(self, key):
        self.action('station-grading-complete',key=key)
        self.state['phase'] = 'grading'

    def restore(self):
        self.state['phase'] = 'restoring'
        failures = []
        try:
            if self.lease_id:
                result = self.action('station-grading-restore')
                if result.get('phase') != 'restored':
                    failures.extend(result.get('errors') or ['Worker snapshot was not restored'])
        except Exception as exc:
            failures.append(str(exc))
        try:
            restore_allocations(self.job.job_id)
        except Exception as exc:
            failures.append('Allocation restore: '+str(exc))
        self.job.station_lease = None
        self.state.update(phase='restore-failed' if failures else 'restored',errors=failures)
        return not failures


def restore_allocations(job_id):
    """Undo this run's own temporary routes; preserve newer operator changes."""
    with modeldb._conn() as conn:
        saved = conn.execute('SELECT * FROM grading_storage_runs WHERE job_id=%s FOR UPDATE',(job_id,)).fetchone()
        if not saved:
            return
        before = {r['model_key']:r for r in saved['allocations']}
        rows = conn.execute('SELECT model_key,pinned FROM model_workers WHERE worker_id=%s AND source=%s FOR UPDATE',
                            (saved['worker_id'],'test-fire:'+job_id)).fetchall()
        for row in rows:
            old = before.get(row['model_key']) or {'assigned':False,'pinned':False,'source':None}
            if row['pinned'] != old['pinned']:
                continue
            conn.execute('UPDATE model_workers SET assigned=%s,source=%s,updated_at=now() WHERE model_key=%s AND worker_id=%s AND source=%s',
                         (old['assigned'],old['source'],row['model_key'],saved['worker_id'],'test-fire:'+job_id))
        conn.execute("UPDATE grading_storage_runs SET state='allocations-restored',updated_at=now() WHERE job_id=%s",(job_id,))


def recover_allocations():
    """Called on Core startup; physical recovery belongs to the wrapper ledger."""
    with modeldb._conn() as conn:
        if not conn.execute("SELECT to_regclass('grading_storage_runs') AS name").fetchone()["name"]:
            return
        rows = conn.execute("SELECT job_id FROM grading_storage_runs WHERE state='active'").fetchall()
    for row in rows:
        restore_allocations(row['job_id'])
