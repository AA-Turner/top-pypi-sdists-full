"""Benchmark history is a view of call_log, never a second execution archive.

The orchestration call owns its plan and outcome. Its grading entries retain
only call pointers, criterion IDs and verdicts. Answers/timing/token counts are
read from the referenced calls when a history view is requested.
"""
from __future__ import annotations

import copy
import datetime
import os
import re

ENDPOINT = '/llm/benchmark/run'


def _ie(sql, params=()):
    # the wrapper call log is read only through calllog.py (the one reader)
    from hugpy_core.calllog.calllog import query
    return query(sql, params)


def compact(public):
    result = copy.deepcopy(public)
    result['calls'] = [{k: c[k] for k in ('request_id', 'core_request_id', 'task',
                                        'grade', 'passed', 'why') if k in c}
                       for c in public.get('calls', [])]
    # Lane identity/decisions are the planner's own response. All measured or
    # graded values are projections over its call pointers, including aggregates.
    for lane in result.get('results', []):
        for key in ('detail', 'grade', 'score', 'max', 'tok_s', 'tok_s_avg',
                    'task_best', 'task_worst', 'hot_load_s', 'cold_s', 'cold_measured',
                    'metrics_complete', 'disk_bytes'):
            lane.pop(key, None)
    for lane in result.get('plan', {}).get('rows', []):
        for key in ('disk_bytes', 'grade', 'tok_s'):
            lane.pop(key, None)
    return result


def _epoch(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        value = datetime.datetime.fromisoformat(value)
    return value.timestamp()


def project(row, facts):
    from hugpy_core.grading import grader
    public = copy.deepcopy(row.get('response_body') or {})
    public.update(request_id=row['request_id'], source='call_log')
    calls = []
    plan = public.get('plan', {}).get('rows', [])
    for pointer in public.get('calls', []):
        execution = facts.get(pointer.get('request_id'), {})
        core = facts.get(pointer.get('core_request_id'), {})
        req = core.get('request_body') or execution.get('request_body') or {}
        resp = execution.get('response_body') or {}
        choices = resp.get('choices') or []
        text = (choices[0].get('message', {}).get('content') if choices else None)
        if text is None:
            text = (core.get('response_body') or {}).get('text')
        model = execution.get('model_name') or core.get('model_name')
        worker = execution.get('worker') or core.get('worker')
        base = next((p for p in plan if p.get('model') == model and p.get('worker') == worker), {})
        messages = req.get('messages') or []
        prompt = messages[-1].get('content') if messages else req.get('prompt')
        err = execution.get('error') or core.get('error')
        if not execution:
            err = err or 'referenced execution call is unavailable'
        call = {**base, **pointer, 'model': model, 'worker': worker,
                'timestamp': _epoch(execution.get('received_at') or core.get('received_at')),
                'cold_load_s': execution.get('cold_load_s'), 'hot_load_s': execution.get('hot_load_s'),
                'elapsed_s': execution.get('total_s'), 'tok_s': execution.get('tok_per_s') or 'N/A',
                'tok_s_avg': execution.get('tok_per_s') or 'N/A',
                'ctx_in': execution.get('prompt_tokens'), 'ctx_out': execution.get('completion_tokens'),
                'caller': 'orchestrator', 'output': text, 'prompt': prompt, 'error': err or 'N/A',
                'check_pass': pointer.get('passed', False)}
        criterion = re.fullmatch(r'(.+) \((\d+)\)', pointer.get('task') or '')
        if criterion:
            cat, tier = criterion[1], int(criterion[2])
            item = {'suite': base.get('grade_suite') or grader.SUITE, 'category': cat, 'tier': tier}
            check = next((x[2] for x in grader.TASKS_TIERED.get(cat, []) if x[0] == tier), None)
            call.update(expected=getattr(check, 'rule', None), expected_answer=getattr(check, 'answer', None))
            if text is not None and not err and check is not None:
                _, call['actual'], _ = grader.check(item, text)
        calls.append(call)
    public['calls'] = calls
    for lane in public.get('results', []):
        selected = [c for c in calls if (c.get('model'), c.get('worker')) ==
                    (lane.get('model'), lane.get('worker'))]
        lane.update(detail={}, grade='N/A', tok_s='N/A')
        if lane.get('status') != 'complete':
            continue
        detail = {}
        for c in selected:
            match = re.fullmatch(r'(.+) \((\d+)\)', c.get('task') or '')
            if not match:
                continue
            cat, tier = match[1], int(match[2])
            d = detail.setdefault(cat, {'tier': 0, 'max': len(grader.TASKS_TIERED.get(cat, [])),
                                         'format': 0, 'revised': 0, 'history': []})
            passed = bool(c.get('passed'))
            d['tier'] += int(passed)
            d['format'] += int(passed)
            d['history'].append({k: c.get(k) for k in
                                 ('prompt', 'expected', 'expected_answer', 'actual', 'why')} |
                                {'tier': tier, 'pass': passed, 'check_pass': passed,
                                 'format': passed if c.get('grade') != 'ERROR' else None, 'revised': False})
        score = sum(d['tier'] for d in detail.values())
        maximum = sum(d['max'] for d in detail.values())
        speeds = [c['tok_s'] for c in selected if isinstance(c.get('tok_s'), (float, int))]
        speed = round(sum(speeds) / len(speeds), 2) if speeds else None
        measured = sorted(selected, key=lambda c: (c.get('timestamp') or 0, c.get('request_id') or ''), reverse=True)
        cold = next((c for c in measured if (c.get('cold_load_s') or 0) > 0), {})
        hot = next((c for c in measured if (c.get('hot_load_s') or 0) > 0), {})
        lane.update(detail=detail, score=score, max=maximum, grade=f'{score}/{maximum}',
                    tok_s=speed or 'N/A', tok_s_avg=speed or 'N/A', metrics_complete=speed is not None,
                    cold_s=cold.get('cold_load_s'), cold_measured=bool(cold),
                    hot_load_s=hot.get('hot_load_s'), cold_request_id=cold.get('request_id'),
                    hot_request_id=hot.get('request_id'))
        if detail:
            lane.update(task_best=max(detail, key=lambda k: detail[k]['tier']),
                        task_worst=min(detail, key=lambda k: detail[k]['tier']))
    return public


def runs(run_id=None, limit=None):
    where = "endpoint = %s AND request_body->'metadata'->'benchmark'->>'run_id' IS NOT NULL"
    params = [ENDPOINT]
    if run_id:
        where += " AND request_body->'metadata'->'benchmark'->>'run_id' = %s"
        params.append(run_id)
    suffix = ''
    if limit is not None:
        suffix = ' LIMIT %s'
        params.append(limit)
    rows = [r[0] for r in _ie('SELECT to_jsonb(c) FROM call_log c WHERE ' + where +
                              ' ORDER BY id DESC' + suffix, tuple(params))]
    # Persisted pending calls from an earlier core process cannot still be running.
    from hugpy_core.grading.review import _PROCESS_STARTED
    from hugpy_core.calllog.call_record import finish
    for row in rows:
        if row.get('call_state') == 'pending' and _epoch(row['received_at']) < _PROCESS_STARTED:
            body = row.setdefault('response_body', {})
            body.update(status='interrupted', error='core restarted before benchmark finished')
            import time
            body['finished'] = time.time()
            finish(row, 500, body['error'], body)
    ids = {c[k] for row in rows for c in (row.get('response_body') or {}).get('calls', [])
           for k in ('request_id', 'core_request_id') if c.get(k)}
    # the referenced calls' facts, chain-resolved, through the one reader
    from hugpy_core.calllog.calllog import by_request_ids
    facts = by_request_ids(ids)
    return [project(row, facts) for row in rows]
