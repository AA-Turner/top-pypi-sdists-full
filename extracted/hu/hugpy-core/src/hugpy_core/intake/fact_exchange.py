"""Relay changed identified facts to peers; never route or allocate a model."""
import hashlib
import json
import logging
import threading
import time

_lock=threading.Lock()
_last={}
_sent={}
_inflight=set()
_log=logging.getLogger(__name__)


def schedule(worker):
    """Keep slow fact exports off the worker's telemetry collection loop."""
    name=worker['name']
    with _lock:
        if name in _inflight or time.monotonic()-_last.get(name,-60)<60:
            return
        _inflight.add(name)

    def run():
        try:
            sync(worker)
        except Exception:
            _log.exception('%s: identified fact exchange failed', name)
        finally:
            with _lock:
                _inflight.discard(name)

    threading.Thread(target=run, name=f'fact-exchange-{name}', daemon=True).start()


def sync(worker):
    from hugpy_core.intake.service import get, registrations
    from hugpy_core.registry.registrations import is_connected
    from hugpy_core.registry.transport import request as _request
    name=worker['name']
    now=time.monotonic()
    with _lock:
        if now-_last.get(name,-60)<60:return
        _last[name]=now
    document=get(worker,'/v1/facts/export',60)
    pairs=document.get('pairs') or []
    if not pairs:return
    for target in registrations():
        if target['name']==name or not is_connected(target):continue
        changed=[]
        for pair in pairs:
            identity=(name,target['name'],pair['model_key'],pair['file'])
            signature=hashlib.sha256(json.dumps(pair,sort_keys=True,default=str).encode()).hexdigest()
            if _sent.get(identity)!=signature:changed.append((identity,signature,pair))
        try:
            for start in range(0,len(changed),40):
                batch=changed[start:start+40]
                _request(target,'/v1/facts/import',{'origin_worker':name,'pairs':[p for _,_,p in batch]})
                for identity,signature,_ in batch:_sent[identity]=signature
        except Exception:
            # A failed peer must not prevent delivery to the remaining peers.
            # Only acknowledged batches are stamped; the next round retries others.
            _log.exception('%s -> %s: identified fact delivery failed', name, target['name'])
