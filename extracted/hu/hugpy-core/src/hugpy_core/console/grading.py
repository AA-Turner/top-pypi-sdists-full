"""What the console asks about grading and test fire, answered from the grading table and the call log.

The console knows a test fire as a job of one worker and a grading as a benchmark run; both are a round
(grading/rounds.py), and everything said of one here is read at the moment it is asked: what was asked for from the
round's own row, what came of it from the wrappers' call logs by the grading marker.

    the Compute tab's test fire    fire, job, stop_job, current, history, history_run, resume, analysis
    the Metrics and Grader tabs    suites, metrics, model_calls, run_status, runs, run, start_run, cancel_run,
                                   failed_loads

A call counts as served when its wrapper answered it, and as failed when its wrapper could not (or turned it away
at its door). A call that was cancelled (the round was stopped) is neither: nothing was asked of the model.
"""
from ..imports import (
    CALL_ANSWERED,
    CALL_OPEN,
    ROUND_CALLS_AT_ONCE,
    json,
    statistics,
    time,
)
from .. import sql
from ..grading import read, rounds

ANALYSIS = dict(healthy_rate=0.95, failing_streak=3, regress_tok_s=0.70, regress_latency=1.50, min_baseline=3)
RESULTS_MAX = 200


def rate(tokens, milliseconds):
    """Tokens a second over a generating time, or None when there is no time to divide by."""
    return round(tokens / (milliseconds / 1000.0), 1) if tokens and milliseconds and milliseconds > 0 else None


def result(call: dict) -> dict:
    """One call of a round as the console's result row."""
    state = call['state'] or CALL_OPEN[0]          # a call whose wrapper has not said how it stands is waiting
    answered = state == CALL_ANSWERED
    took = round(call['responded_at'] - call['received_at'], 2) if call.get('responded_at') and call.get('received_at') else None
    return dict(
        model_key=call['model'], task=call.get('task'), endpoint=call.get('endpoint'), request_id=call.get('request_id'),
        prompt=call.get('asks'), started=call.get('received_at'), latency_s=took, ok=answered,
        status='ok' if answered else state if state in ('cancelled', *CALL_OPEN) else 'fail',
        tokens=call.get('completion_tokens'), tok_s=rate(call.get('completion_tokens'), call.get('predicted_ms')),
        worker=call['wrapper'], content80=(call.get('shown') or '')[:80], round=1,
        error=None if answered else call.get('error'), error_kind=None if answered else state,
        grade=dict(passed=call.get('passed'), category=call.get('category'), tier=call.get('tier_name'),
                   why=call.get('why'), expected=call.get('answer')) if call.get('category') else None)


def refusal(one: dict) -> dict:
    """A call a wrapper's door turned away, as the console's result row."""
    return dict(model_key=one['model'], task=None, endpoint=None, request_id=None, prompt=None, started=one.get('at'),
                latency_s=None, ok=False, status='fail', tokens=None, tok_s=None, worker=one['wrapper'], content80='',
                round=1, error=one.get('error'), error_kind='refused', grade=None)


def summary(results: list) -> dict:
    """{ok, failed, total, per_model} of a round's results (oldest first)."""
    per, ok, failed = {}, 0, 0
    for row in results:
        if row['status'] in ('cancelled', *CALL_OPEN):
            continue
        one = per.setdefault(row['model_key'], dict(ok=0, failed=0, grade_passed=0, grade_failed=0))
        one['ok' if row['ok'] else 'failed'] += 1
        ok, failed = ok + row['ok'], failed + (not row['ok'])
        grade = row.get('grade') or {}
        one['grade_passed'] += grade.get('passed') is True
        one['grade_failed'] += grade.get('passed') is False
        one.update(last_status=row['status'], last_error=row['error'], last_error_kind=row['error_kind'],
                   last_latency_s=row['latency_s'], last_tok_s=row['tok_s'], last_at=row['started'],
                   task=row['task'] or one.get('task'), endpoint=row['endpoint'] or one.get('endpoint'))
    return dict(ok=ok, failed=failed, total=ok + failed, per_model=per)


def results_of(state: dict) -> list:
    """Every call of a round, and every call a door turned away, as result rows, oldest first."""
    return sorted([result(call) for call in state['calls']] + [refusal(one) for one in state['refused']],
                  key=lambda row: row['started'] or 0)


def ended(state: dict) -> str:
    """How a round stands, in a word: running, complete, stopped or interrupted."""
    if state['running']:
        return 'running'
    return (state.get('ended_why') or 'interrupted').split(':')[0]


def job(state: dict, limit: int = RESULTS_MAX) -> dict:
    """A round of one wrapper as the console's test-fire job."""
    wrapper, asked, found = state['wrappers'][0], state['asked'], results_of(state)
    models = list(dict.fromkeys(call['model'] for call in state['plan']))
    grading = {}
    if asked.get('complete'):
        wanted = set(models)
        for one in read.standing(wrapper):
            if one['model'] in wanted:
                left = one['of'] - one['graded']
                grading[one['model']] = dict(status='complete' if not left else 'grading' if one['asking'] else 'pending',
                                             suite=one['suite'], remaining=left, error=None)
    return dict(
        ok=True, job_id=state['id'], worker_id=wrapper, worker=wrapper, running=state['running'], round=1, rounds=1,
        submitted=state['sent'], max_tokens=asked.get('max_tokens'), seed=None, grade=bool(asked.get('complete')),
        hot=bool(asked.get('hot')), cold=bool(asked.get('cold')), grading=grading, models=models,
        skipped=[dict(model_key=one['model'], reason=one['reason']) for one in state['skipped']],
        resumed_from=asked.get('resumed_from'), total_planned=len(state['plan']),
        done_calls=sum(1 for row in found if row['status'] not in CALL_OPEN),
        in_flight=[dict(request_id=call['request_id'], model_key=call['model']) for call in state['calls'] if call['state'] == 'running'],
        stop_requested=state['stopping'], stop_reason=None if state['running'] else ended(state),
        created=state['started_at'], started=state['started_at'], finished=state['ended_at'],
        concurrency=ROUND_CALLS_AT_ONCE, chaos=False, results=found[-max(1, min(int(limit or RESULTS_MAX), RESULTS_MAX)):],
        summary=summary(found))


def fire(wrapper: str, body: dict, by: str = None) -> tuple:
    """Start a test fire of a wrapper: {grade, hot, cold} (the console's checkboxes; ``grade``: every query that
    was not performed, not only each model's next). -> (status, document)."""
    try:
        state = rounds.start('test-fire', [wrapper], hot=body.get('hot', True) is not False, cold=body.get('cold', True) is not False,
                             complete=body.get('grade', True) is not False, models=body.get('models') or None,
                             asked={key: body[key] for key in ('rounds', 'max_tokens', 'resumed_from') if body.get(key) is not None},
                             by=by)
    except rounds.Busy as exc:
        return 409, dict(ok=False, error=str(exc), job_id=exc.round_id)
    except ValueError as exc:
        return 400, dict(ok=False, error=str(exc))
    return 202, job(state)


def find(wrapper: str, round_id: str) -> dict:
    """The state of a round of this wrapper; LookupError when it is not one."""
    state = rounds.state(round_id)
    if wrapper not in state['wrappers']:
        raise LookupError(f'{round_id} is not a round of {wrapper}')
    return state


def current(wrapper: str) -> dict:
    """The test fire the console shows for a wrapper when it opens: the one being sent, else its newest; {} when
    it never had one."""
    found = rounds.running(wrapper) or next((row['id'] for row in rounds.rounds('test-fire', wrapper, 1)), None)
    return job(rounds.state(found), 0) if found else {}


def stop_job(wrapper: str, round_id: str) -> dict:
    find(wrapper, round_id)
    said = rounds.stop(round_id)
    return dict(ok=True, job_id=round_id, was_running=said['was_running'], in_flight=said['cancelled'], cancelled=[])


def run_row(row: dict, wrapper: str) -> dict:
    """A round of rounds.rounds() as a row of the console's test-fire history."""
    state = 'running' if row['running'] else (row.get('ended_why') or 'interrupted').split(':')[0]
    return dict(job_id=row['id'], worker_id=wrapper, worker_name=wrapper, source='call_log', created=row['started_at'],
                started=row['started_at'], finished=row['ended_at'], ok=row['answered'],
                failed=row['failed'] + row['refused'], state=state, stop_reason=state, live=row['running'],
                grade=bool(row['asked'].get('complete')), rounds=1, max_tokens=row['asked'].get('max_tokens'),
                planned=row['planned'], skipped=row['skipped'], resumed_from=row['asked'].get('resumed_from'))


def history(wrapper: str, limit: int = 50) -> dict:
    return dict(worker_id=wrapper, stored=True, live_job_id=rounds.running(wrapper),
                runs=[run_row(row, wrapper) for row in rounds.rounds('test-fire', wrapper, limit)])


def history_run(wrapper: str, round_id: str) -> dict:
    """One past test fire with every call of it."""
    state = find(wrapper, round_id)
    found = job(state)
    waiting = [call['model'] for call in state['plan'] if call['model'] not in found['summary']['per_model']]
    return dict(found, results=results_of(state), ok=found['summary']['ok'], failed=found['summary']['failed'],
                state=ended(state), live=state['running'], current_model=waiting[0] if waiting and not state['running'] else None)


def resume(wrapper: str, round_id: str, by: str = None) -> tuple:
    """A new test fire asking what a past one asked: since a round asks what was not performed, it goes on from
    where that one stopped. -> (status, document)."""
    asked = find(wrapper, round_id)['asked']
    status, said = fire(wrapper, dict(grade=asked.get('complete'), hot=asked.get('hot'), cold=asked.get('cold'),
                                      models=asked.get('models'), max_tokens=asked.get('max_tokens'), resumed_from=round_id), by)
    return status, dict(said, resumed_from=round_id) if status == 202 else said


def middle(values: list):
    """The median of the numbers that are there, rounded; None when there are none."""
    found = [value for value in values if value is not None]
    return round(statistics.median(found), 2) if found else None


def analysis(wrapper: str, runs: int = 20) -> dict:
    """What a wrapper's last test fires say of each model: how often it answered, and whether its newest round
    is slower than the ones before it. A model's baseline is the medians of its answered calls before the newest
    round; its verdict is failing (its last calls all failed), regressed (slower than its baseline), flaky (it
    does not always answer), healthy, or untested."""
    found = rounds.rounds('test-fire', wrapper, max(1, min(int(runs or 20), 200)))
    latest, models, verdicts = (found[0]['id'] if found else None), {}, {}
    for row in reversed(found):                                 # oldest round first: calls in the order they were made
        for one in results_of(rounds.state(row['id'])):
            if one['status'] in ('cancelled', *CALL_OPEN):
                continue
            models.setdefault(one['model_key'], []).append(dict(one, job=row['id']))
    out = {}
    for model, calls in sorted(models.items()):
        answered = [call for call in calls if call['ok']]
        before, newest = [c for c in answered if c['job'] != latest], [c for c in answered if c['job'] == latest]
        kinds = {}
        for call in calls:
            if not call['ok']:
                kinds[call['error_kind'] or 'failed'] = kinds.get(call['error_kind'] or 'failed', 0) + 1
        baseline = (dict(latency_s=middle([c['latency_s'] for c in before]), tok_s=middle([c['tok_s'] for c in before]),
                         samples=len(before)) if len(before) >= ANALYSIS['min_baseline'] else None)
        last = dict(latency_s=middle([c['latency_s'] for c in newest]), tok_s=middle([c['tok_s'] for c in newest]),
                    samples=len(newest)) if newest else None
        share = len(answered) / len(calls)
        streak = calls[-ANALYSIS['failing_streak']:]
        if not answered or (len(streak) == ANALYSIS['failing_streak'] and not any(call['ok'] for call in streak)):
            verdict, why = 'failing', f"its last {len(streak)} call{'' if len(streak) == 1 else 's'} failed: {streak[-1]['error'] or 'no reason recorded'}"
        elif baseline and last and baseline['tok_s'] and last['tok_s'] and last['tok_s'] < ANALYSIS['regress_tok_s'] * baseline['tok_s']:
            verdict, why = 'regressed', f"{last['tok_s']} tok/s in the newest round, {baseline['tok_s']} before it"
        elif baseline and last and baseline['latency_s'] and last['latency_s'] and last['latency_s'] > ANALYSIS['regress_latency'] * baseline['latency_s']:
            verdict, why = 'regressed', f"{last['latency_s']} s a call in the newest round, {baseline['latency_s']} s before it"
        elif share < ANALYSIS['healthy_rate']:
            verdict, why = 'flaky', f'{len(answered)} of {len(calls)} calls answered'
        else:
            verdict, why = 'healthy', f'{len(answered)} of {len(calls)} calls answered'
        verdicts[verdict] = verdicts.get(verdict, 0) + 1
        out[model] = dict(calls=len(calls), ok=len(answered), failed=len(calls) - len(answered), success_rate=round(share, 3),
                          error_kinds=kinds, baseline=baseline, latest=last,
                          last_ok_at=answered[-1]['started'] if answered else None, why=why, verdict=verdict)
    return dict(worker_id=wrapper, runs=len(found), latest_job=latest, models=out, verdicts=verdicts, thresholds=ANALYSIS)


# ── the Metrics and Grader tabs ──────────────────────────────────────────────────────────────────────────

def suites() -> dict:
    """The suites of the grading table as the console's registry: a suite's columns are its categories."""
    return dict(generated_at=time.time(), suites=[dict(
        name=suite['name'], task=suite['task'], serves_tasks=[suite['task']], tasks=suite['categories'],
        tiers=suite['tiers'], max=suite['queries'], legacy=False, available=True,
        items={category: [dict(tier=query['tier_name'], prompt=query['asks'], expected=query['rule'],
                               expected_answer=query['answer']) for query in found]
               for category, found in suite['items'].items()}) for suite in read.suites()])


def placed(row: str) -> tuple:
    """(the file of a model's id, how its wrapper says it would be placed) from the wrapper's row of the model."""
    said = json.loads(row) if row else {}
    variation = str(said.get('id') or '').partition('::')[2]
    return ('' if variation in ('', '*') else variation), ((said.get('options') or {}).get('placed') or {}).get('reads_as') or ''


def throughput(calls: dict, wrapper: str) -> dict:
    """A row of the model_calls view as the console's throughput block: tokens over generating time, with n."""
    if not calls:
        return dict(n_calls=0, n_rated=0, n_failed=0, mean_tok_s=None, worker=wrapper, reason='no calls recorded')
    mean = round(calls['tokens'] / calls['seconds'], 2) if calls['tokens'] and calls['seconds'] else None
    return dict(n_calls=calls['calls'], n_ok=calls['answered'], n_rated=calls['rated'], n_failed=calls['failed'],
                mean_tok_s=mean, tokens=calls['tokens'] or 0, seconds=round(calls['seconds'] or 0, 3),
                mean_s_per_call=round(calls['mean_s_per_call'], 3) if calls['mean_s_per_call'] is not None else None,
                first_at=calls['first_call_at'], last_at=calls['last_call_at'], worker=wrapper,
                reason=None if mean is not None else f"{calls['calls']} call(s), none with tokens and a generating time")


def detail(rows: list) -> dict:
    """A model's schedule as the console's grade detail: under each category, a verdict a tier."""
    out = dict(suite=rows[0]['suite'])
    for row in rows:
        cell = out.setdefault(row['category'], dict(tier=0, max=0, history=[]))
        cell['max'] += 1
        cell['tier'] += row['passed'] is True
        cell['history'].append(dict(tier=row['tier_name'], prompt=row.get('asks'), expected=row.get('rule'),
                                    expected_answer=row.get('answer'), actual=row['shown'], why=row['why'],
                                    check_pass=row['passed'], **({'pass': row['passed']})))
    return out


def metrics(model: str = None) -> dict:
    """One row a model and wrapper: what the call log says of its calls, and its grade as it stands now."""
    asked = {query['id']: query for query in read.queries()}
    schedules = {}
    for row in read.schedule(model=model):
        query = asked.get(row['query']) or {}
        schedules.setdefault((row['wrapper'], row['model']), []).append(dict(row, asks=query.get('asks'), rule=query.get('rule'),
                                                                            answer=query.get('answer')))
    called = {(row['wrapper'], row['model']): row for row in sql.rows(
        "SELECT * FROM model_calls" + (' WHERE model = ?' if model else ''), (model,) if model else ())}
    known = {(row['wrapper'], row['id']): row for row in sql.rows(
        "SELECT wrapper, id, task, row FROM models" + (' WHERE id = ?' if model else ''), (model,) if model else ())}
    rows = []
    for wrapper, name in sorted(set(called) | set(schedules)):
        calls, schedule, about = called.get((wrapper, name)), schedules.get((wrapper, name)), known.get((wrapper, name)) or {}
        quant, mode = placed(about.get('row'))
        graded = [row for row in schedule or [] if row['standing'] == 'graded']
        block = throughput(calls, wrapper)
        rows.append(dict(
            model_name=name, model=name, worker=wrapper, worker_id=wrapper, quant=quant, alloc_mode=mode,
            task=about.get('task') or (calls or {}).get('task'), n_samples=block['n_calls'], n_calls=block['n_calls'],
            updated_at=(calls or {}).get('last_call_at'),
            grade=sum(1 for row in graded if row['passed'] is True) if graded else None,
            grade_suite=schedule[0]['suite'] if schedule else None, grade_task=schedule[0]['task'] if schedule else None,
            grade_detail=detail(schedule) if graded else None,
            graded_at=max((row['graded_at'] for row in graded), default=None),
            cold_load_s=round(calls['mean_load_s'], 2) if calls and calls['mean_load_s'] is not None else None, hot_load_s=None,
            tok_per_s=block['mean_tok_s'], throughput=block))
    return dict(rows=rows, count=len(rows), generated_at=time.time())


def graded_call(call: dict, quant: str = '', mode: str = '') -> dict:
    """A call of the call log as the console's graded-call row (a call with no marker carries no grade; one its
    wrapper has not finished carries neither a grade nor an error)."""
    state = call['state'] or CALL_OPEN[0]
    answered, waiting = state == CALL_ANSWERED, state in CALL_OPEN
    passed = call.get('passed')
    return dict(
        model=call['model'], worker=call['wrapper'], worker_id=call['wrapper'], quant=quant, alloc_mode=mode, config=mode,
        request_id=call['request_id'], timestamp=call['received_at'], finished=call.get('responded_at'), state=state,
        task=f"{call['category']} ({call['tier_name']})" if call.get('category') else call.get('endpoint'),
        grade_suite=call.get('suite'), benchmark=bool(call.get('query')), prompt=call.get('asks'), expected=call.get('rule'),
        expected_answer=call.get('answer'), output=call.get('shown'), actual=call.get('shown'), passed=passed, check_pass=passed,
        grade=None if waiting or not call.get('query') else 'PASS' if passed is True else 'FAIL' if passed is False else 'ERROR',
        why=call.get('why') if passed is False else None, error=None if answered or waiting else (call.get('error') or state),
        tok_s=rate(call.get('completion_tokens'), call.get('predicted_ms')), prompt_tokens=call.get('prompt_tokens'),
        completion_tokens=call.get('completion_tokens'), ctx_in=call.get('prompt_tokens'), ctx_out=call.get('completion_tokens'),
        elapsed_s=round(call['responded_at'] - call['received_at'], 2) if call.get('responded_at') and call.get('received_at') else None,
        caller='grading' if call.get('query') else None, round=call.get('round'))


def with_rules(calls: list) -> list:
    """Graded calls with what each one's query requires, in words."""
    asked = {query['id']: query['rule'] for query in read.queries()}
    return [dict(call, rule=asked.get(call.get('query'))) for call in calls]


def model_calls(model: str, limit: int = 2000) -> dict:
    """Every call of one model in the call log, newest first, the graded ones with their verdicts; and what each
    wrapper's calls of it come to."""
    limit = max(1, min(int(limit or 2000), 5000))
    graded = {(call['wrapper'], call['request_id']): call for call in with_rules(read.graded(model=model, limit=limit))}
    places = {row['wrapper']: placed(row['row']) for row in sql.rows("SELECT wrapper, row FROM models WHERE id = ?", (model,))}
    calls = []
    for row in sql.rows("SELECT wrapper, request_id, model, endpoint, state, received_at, responded_at, prompt_tokens, "
                        "completion_tokens, predicted_ms, error FROM calls WHERE model = ? AND endpoint != '/v1/load' "
                        "ORDER BY received_at DESC LIMIT ?", (model, limit)):
        calls.append(graded_call(graded.get((row['wrapper'], row['request_id'])) or row, *places.get(row['wrapper'], ('', ''))))
    averages = [throughput(row, row['wrapper']) for row in sql.rows("SELECT * FROM model_calls WHERE model = ?", (model,))]
    return dict(calls=calls, worker_averages=averages, count=len(calls))


def run(state: dict) -> dict:
    """A round as the console's benchmark run: its plan, a result a model and wrapper, and every call of it."""
    places = {(row['wrapper'], row['id']): placed(row['row']) for row in sql.rows("SELECT wrapper, id, row FROM models")}
    calls = [graded_call(call, *places.get((call['wrapper'], call['model']), ('', ''))) for call in with_rules(state['calls'])]
    for one in state['refused']:
        quant, mode = places.get((one['wrapper'], one['model']), ('', ''))
        calls.append(dict(model=one['model'], worker=one['wrapper'], worker_id=one['wrapper'], quant=quant, alloc_mode=mode,
                          config=mode, task=one.get('query'), grade='ERROR', passed=None, error=one.get('error'),
                          timestamp=one.get('at'), benchmark=True, state='refused'))
    pairs = list(dict.fromkeys((call['wrapper'], call['model']) for call in state['plan']))
    measured = {(row['worker'], row['model']): row for row in metrics()['rows']} if pairs else {}
    planned, results, done = [], [], 0
    for wrapper, model in pairs:
        quant, mode = places.get((wrapper, model), ('', ''))
        mine = [call for call in calls if call['worker'] == wrapper and call['model'] == model]
        asked = sum(1 for call in state['plan'] if call['wrapper'] == wrapper and call['model'] == model)
        finished = [call for call in mine if call['state'] not in CALL_OPEN]
        row = measured.get((wrapper, model)) or {}
        over = len(finished) >= asked or not state['running']
        done += len(finished)
        failed = [call for call in finished if call.get('grade') == 'ERROR']
        status = ('running' if not over else 'error' if finished and len(failed) == len(finished) else 'passed' if finished else 'not run')
        planned.append(dict(model=model, worker=wrapper, worker_id=wrapper, quant=quant, config=mode, alloc_mode=mode,
                            runnable=True, status=status, constraint_reason=None))
        if finished:
            results.append(dict(
                model=model, worker=wrapper, worker_id=wrapper, quant=quant, config=mode, alloc_mode=mode, status=status,
                ok=status == 'passed', error=failed[-1]['error'] if status == 'error' else None, constraint_reason=None,
                grade=row.get('grade'), grade_suite=row.get('grade_suite'), grade_task=row.get('grade_task'),
                score=row.get('grade'), detail=row.get('grade_detail'), tok_s=row.get('tok_per_s'), cold_s=row.get('cold_load_s'),
                cold_measured=row.get('cold_load_s') is not None, hot_load_s=None, throughput=row.get('throughput'),
                finished=max((call.get('finished') or call.get('timestamp') or 0 for call in finished), default=None),
                metric_source='call_log'))
    total = len(state['plan'])
    status = 'running' if state['running'] else 'idle'
    return dict(
        run_id=state['id'], request_id=None, status=status, executor='hugpy-core', started=state['started_at'],
        finished=state['ended_at'], updated=time.time(), error=None, models=list(dict.fromkeys(model for _, model in pairs)),
        workers=state['wrappers'], params=dict(state['asked'], measure_cold_load=False), kind=state['kind'],
        ended=None if state['running'] else ended(state),
        progress=dict(completed=done, total=total, percent=round(100 * done / total) if total else 0,
                      active_lanes=[dict(worker=call['worker'], model=call['model'], phase='answering')
                                    for call in calls if call['state'] == 'running']),
        plan=dict(runnable=len(planned), total=len(planned), rows=planned), results=results, calls=calls, events=[],
        summary={}, skipped=state['skipped'])


IDLE = dict(status='idle', run_id=None, results=[], calls=[], events=[], models=[], workers=[],
            plan=dict(runnable=0, total=0, rows=[]), progress={}, summary={}, error=None, executor='hugpy-core')


def run_status() -> dict:
    """The round being sent now, else the newest one, as the console's live benchmark; idle when there never
    was one."""
    found = rounds.running() or next((row['id'] for row in rounds.rounds(limit=1)), None)
    return run(rounds.state(found)) if found else dict(IDLE)


def runs() -> dict:
    return dict(source='call_log', errors=[], runs=[dict(
        run_id=row['id'], request_id=None, kind=row['kind'], started=row['started_at'], finished=row['ended_at'],
        updated=row['ended_at'] or time.time(), workers=row['wrappers'], models=row['asked'].get('models') or [],
        status='running' if row['running'] else 'completed' if row.get('ended_why') == 'complete' else (row.get('ended_why') or 'interrupted').split(':')[0],
        results=row['planned'], calls=row['calls'], error=None) for row in rounds.rounds(limit=200)])


def start_run(body: dict, by: str = None) -> tuple:
    """Grade chosen models on chosen wrappers: every query of their schedules that was not performed.
    {models: [...] (none: every model), workers: [...]} -> (status, document)."""
    workers = [name for name in body.get('workers') or [] if isinstance(name, str)]
    if not workers:
        return 400, dict(error='name the workers to grade on: {"workers": [...]}')
    try:
        state = rounds.start('grading', workers, models=[m for m in body.get('models') or [] if isinstance(m, str)] or None,
                             complete=True, asked={key: body[key] for key in ('tokens', 'executor') if body.get(key) is not None},
                             by=by)
    except rounds.Busy as exc:
        return 409, dict(run(rounds.state(exc.round_id)), message=str(exc))
    except ValueError as exc:
        return 400, dict(error=str(exc))
    return 202, run(state)


def cancel_run() -> tuple:
    found = rounds.running()
    if not found:
        return 409, dict(status='not_running')
    rounds.stop(found)
    return 200, run(rounds.state(found))


def failed_loads(model: str = None, limit: int = 1) -> dict:
    """The loads a wrapper could not finish, newest first, each with what its wrapper said of the call that
    waited on it (the failed call of the same model nearest in time)."""
    found = sql.rows("SELECT wrapper, model, load_id, coalesce(ended_at, staged_at) AS at, engine, placement, end_reason "
                     "FROM loads WHERE outcome = 'failed'" + (' AND model = ?' if model else '') + " ORDER BY at DESC LIMIT ?",
                     (*((model,) if model else ()), max(1, min(int(limit or 1), 500))))
    actions = []
    for row in found:
        said = sql.rows("SELECT error FROM calls WHERE wrapper = ? AND model = ? AND state = 'failed' "
                        "ORDER BY abs(coalesce(responded_at, received_at) - ?) LIMIT 1", (row['wrapper'], row['model'], row['at'] or 0))
        actions.append(dict(
            id=row['load_id'], action='load', outcome='fail', model=row['model'], model_name=row['model'], worker=row['wrapper'],
            ts=row['at'], at=row['at'], source='load_runs', reason=row['end_reason'],
            detail={'message': (said[0]['error'] if said else None) or row['end_reason'] or 'the load failed; its wrapper recorded no reason',
                    'class': 'load failed'}))
    return dict(count=len(actions), actions=actions)


__all__ = ['analysis', 'cancel_run', 'current', 'failed_loads', 'fire', 'history', 'history_run', 'job', 'metrics',
           'model_calls', 'resume', 'run', 'run_status', 'runs', 'start_run', 'stop_job', 'suites']
