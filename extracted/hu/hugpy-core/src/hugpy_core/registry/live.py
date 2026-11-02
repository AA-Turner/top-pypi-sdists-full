"""LIVE window: what is loaded / loading / failed / free on each box, pushed the
instant it changes. hugpy_wrapper triggers notify 'live' (residents,
call_log) and 'gpu_state' (the card); one LISTEN thread re-reads and wakes every
open page. No polling anywhere."""
from __future__ import annotations

import json
import threading
import time

from flask import Blueprint, Response, stream_with_context

from hugpy_core.registry import registry

from hugpy_core.calllog.calllog_db import dsn as _calllog_dsn
IE_DSN = _calllog_dsn()
_cond = threading.Condition()
_state = {"version": 0, "data": {}, "console_v": 0}
_started = [False]
_lock = threading.Lock()


def _read(c) -> dict:
    res = [dict(zip(("worker", "key", "state", "pid", "ctx", "ngl", "total_layers", "vram", "ram", "error",
                     "engine", "since", "last_used", "calls", "busy", "loading"), r))
           for r in c.execute("SELECT worker, key, state, pid, ctx, n_gpu_layers, total_layers, vram_bytes, ram_bytes, "
                              "load_error, engine, extract(epoch from resident_since), extract(epoch from last_used), "
                              "calls, busy, loading FROM residents ORDER BY worker, key").fetchall()]
    gpu = [dict(zip(("worker", "device", "name", "total", "usable", "used", "free", "reason", "at",
                     "processes", "hugpy_pids", "probe_pids"), r))
           for r in c.execute("SELECT worker, device, name, total, usable, used, free, reason, extract(epoch from at), "
                              "processes, hugpy_pids, probe_pids FROM gpu_state ORDER BY worker, device").fetchall()]
    host = [dict(zip(("worker", "mem_total", "mem_available", "swap_total", "swap_free", "mem_free"), r))
            for r in c.execute("SELECT worker, mem_total, mem_available, swap_total, swap_free, mem_free FROM host_state").fetchall()]
    calls = [dict(zip(("t", "worker", "model", "task", "status", "secs", "ctx", "error", "mode"), r))
             for r in c.execute("SELECT extract(epoch from received_at), worker, model_name, task, http_status, "
                                "extract(epoch from (coalesce(responded_at, now()) - received_at)), context_length, "
                                "left(error, 160), response_meta->'decision'->>'mode' "
                                "FROM call_log WHERE http_status IS NOT NULL OR dispatched_at IS NOT NULL "
                                "ORDER BY received_at DESC LIMIT 25").fetchall()]   # front-door rows (central-only stubs excluded)
    return {"residents": res, "gpu": gpu, "host": host, "calls": calls, "at": time.time()}


def _loop():
    import psycopg
    from hugpy_core.imports.functions import listen_channel
    while True:
        try:
            with psycopg.connect(IE_DSN, autocommit=True) as conn, psycopg.connect(IE_DSN, autocommit=True) as rc:
                live_chan = listen_channel(conn, "live")
                listen_channel(conn, "gpu_state")
                wake_console = True
                first = True
                while True:
                    d = _read(rc)
                    if first:
                        from hugpy_core.brain import gpu_live
                        for name in {row["worker"] for row in d["gpu"] + d["host"]}:
                            gpu_live.schedule(name)
                        first = False
                    with _cond:
                        _state["data"] = d
                        _state["version"] += 1
                        _cond.notify_all()
                    with registry._CHANGED:
                        if wake_console:                # residents / call_log moved: the heavy feeds re-diff
                            _state["console_v"] += 1
                        registry._CHANGED.notify_all()  # every change: /llm/events re-diffs gpu_state
                    got = list(conn.notifies(stop_after=1))
                    got += list(conn.notifies(timeout=0))   # coalesce a burst into one re-read
                    affected = set()
                    for notification in got:
                        try:
                            affected.add(json.loads(notification.payload).get("worker"))
                        except (TypeError, ValueError):
                            pass
                    if not affected or None in affected:
                        affected = {row["worker"] for row in d["gpu"] + d["host"]}
                    for name in affected:
                        gpu_live.schedule(name)
                    # gpu_state fires on every NVML byte move (several a second under load) and
                    # rides its own small feed; only 'live' (residents / call_log) rebuilds the rest
                    wake_console = any(n.channel == live_chan for n in got)
        except Exception as exc:  # noqa: BLE001
            print(f"[live] reconnect: {exc}")
            time.sleep(2)


def console_version() -> int:
    return _state["console_v"]


def gpu_feed() -> dict:
    """The console's ``gpu_state`` feed: every card + host RAM and swap, exact bytes, as
    last read by the LISTEN loop (no query of its own)."""
    d = _state["data"] or {}
    residents = {(r["worker"], int(r["pid"])): r.get("key") for r in d.get("residents", []) if r.get("pid") is not None}
    activity = {}
    for card in d.get("gpu", []):
        worker = card["worker"]
        rows = activity.setdefault(worker, [])
        processes = card.get("processes") or {}
        if isinstance(processes, str):
            try:
                processes = json.loads(processes)
            except ValueError:
                processes = {}
        ours, probes = card.get("hugpy_pids") or [], card.get("probe_pids") or []
        if isinstance(ours, str):
            try: ours = json.loads(ours)
            except ValueError: ours = []
        if isinstance(probes, str):
            try: probes = json.loads(probes)
            except ValueError: probes = []
        for pid_s, nbytes in sorted(processes.items()):
            pid = int(pid_s)
            key = residents.get((worker, pid))
            kind = "hugpy" if key or pid in ours else ("probe" if pid in probes else "observed")
            rows.append({"kind": kind, "model_key": key, "service": "fitevict" if kind == "hugpy" else
                         ("llama.cpp dry run" if kind == "probe" else "gpu process"),
                         "pids": [pid], "gpu_indices": [card["device"]], "vram_bytes": int(nbytes),
                         "vram_mib": int(nbytes) // 1048576, "state": "running",
                         "evictable": kind == "hugpy", "immutable": kind == "observed",
                         "api_available": bool(key), "activity": {},
                         "note": ("Hugpy managed (fitevict)" if kind == "hugpy" else
                                  "transient sizing probe" if kind == "probe" else
                                  "GPU process observed; not managed by hugpy")})
    return {"cards": d.get("gpu", []), "activity": activity,
            "hosts": {h["worker"]: {"mem_total": h["mem_total"], "mem_available": h["mem_available"], "mem_free": h.get("mem_free"),
                                    "swap_total": h["swap_total"], "swap_free": h["swap_free"]}
                      for h in d.get("host", [])}}


def _ensure():
    with _lock:
        if not _started[0]:
            _started[0] = True
            threading.Thread(target=_loop, name="live-listen", daemon=True).start()


PAGE = r"""<!doctype html><html><head><meta charset="utf-8"><title>hugpy live</title>
<style>
body{font:13px/1.4 ui-monospace,Menlo,monospace;background:#0f1115;color:#d6d9e0;margin:16px}
h2{font-size:14px;margin:18px 0 6px;color:#9aa4b2}
table{border-collapse:collapse;width:100%}td,th{padding:3px 8px;border-bottom:1px solid #222733;text-align:left;white-space:nowrap}
th{color:#7d8696;font-weight:normal}.n{text-align:right}
.loading{color:#f5b942}.serving{color:#5aa9ff}.idle{color:#4cc38a}.error,.dead{color:#ff6b6b}.fail{color:#ff6b6b}.ok{color:#4cc38a}
.bar{height:16px;background:#222733;position:relative;margin:4px 0}.bar i{position:absolute;top:0;bottom:0;left:0;background:#5aa9ff}
#st{color:#7d8696}
</style></head><body>
<div id=st>connecting…</div>
<h2>GPU</h2><div id=gpu></div>
<h2>Models on the boxes (fitevict front door)</h2><table id=res></table>
<h2>Recent calls</h2><table id=calls></table>
<script>
const B=n=>n==null?'—':Number(n).toLocaleString('en-US')+' B';
const T=e=>e?new Date(e*1000).toLocaleTimeString():'—';
function draw(d){
  document.getElementById('st').textContent='live · updated '+T(d.at);
  document.getElementById('gpu').innerHTML=d.gpu.map(g=>{
    const h=(d.host||[]).find(x=>x.worker===g.worker)||{};
    const pct=g.usable?Math.min(100,100*g.used/g.usable):0;
    return `<div>${g.worker} · ${g.name} · used ${B(g.used)} · free ${B(g.free)} of usable ${B(g.usable)} · RAM available ${B(h.mem_available)} · swap free ${B(h.swap_free)} / ${B(h.swap_total)} · last change: ${g.reason} ${T(g.at)}</div><div class=bar><i style="width:${pct}%"></i></div>`}).join('');
  document.getElementById('res').innerHTML='<tr><th>box</th><th>model</th><th>state</th><th>engine</th><th class=n>ctx</th><th class=n>gpu layers</th><th class=n>VRAM</th><th class=n>RAM</th><th>since</th><th class=n>calls</th><th>error</th></tr>'+
    (d.residents.length?d.residents.map(r=>{const st=r.busy?'serving':(r.loading?'loading':r.state);
      return `<tr><td>${r.worker}</td><td>${r.key}</td><td class="${st}">● ${st}</td><td>${r.engine||''}</td><td class=n>${r.ctx??'—'}</td><td class=n>${r.ngl==null?'—':(r.ngl<0?'all':r.ngl)}${r.total_layers?'/'+r.total_layers:''}</td><td class=n>${B(r.vram)}</td><td class=n>${B(r.ram)}</td><td>${T(r.since)}</td><td class=n>${r.calls??0}</td><td class=error>${r.error||''}</td></tr>`}).join(''):'<tr><td colspan=11>nothing loaded</td></tr>');
  document.getElementById('calls').innerHTML='<tr><th>time</th><th>model</th><th>task</th><th>status</th><th class=n>secs</th><th class=n>ctx</th><th>mode</th><th>error</th></tr>'+
    d.calls.map(c=>{const ok=c.status==200, run=c.status==null;
      return `<tr><td>${T(c.t)}</td><td>${c.model}</td><td>${c.task||''}</td><td class="${run?'loading':(ok?'ok':'fail')}">${run?'running':c.status}</td><td class=n>${c.secs==null?'':Number(c.secs).toFixed(1)}</td><td class=n>${c.ctx??''}</td><td>${c.mode||''}</td><td class=fail>${c.error||''}</td></tr>`}).join('');
}
function go(){const es=new EventSource('live/stream');es.onmessage=e=>draw(JSON.parse(e.data));
  es.onerror=()=>{document.getElementById('st').textContent='reconnecting…'}}
go();
</script></body></html>"""


# The LIVE window handlers, as plain views for the registry category tree. The
# page's EventSource is pinned to the absolute ``/live/stream`` so it works under
# either mount (bare and /api).
_PAGE = PAGE.replace("new EventSource('live/stream')", "new EventSource('/live/stream')")


def live_page(**_):
    _ensure()
    return Response(_PAGE, mimetype="text/html")


def live_stream(**_):
    _ensure()

    def gen():
        seen = -1
        started = time.time()
        while time.time() - started < 3600:
            with _cond:
                if _state["version"] == seen:
                    _cond.wait(timeout=15)
                v, d = _state["version"], _state["data"]
            if v == seen:
                yield ": keepalive\n\n"
                continue
            seen = v
            yield "data: " + json.dumps(d, default=str) + "\n\n"
    return Response(stream_with_context(gen()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
