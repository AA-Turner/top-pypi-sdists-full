"""Read Wrapper predictions and measured timings from Core's call mirror."""

from .. import sql
from ..imports import json
from ..wrappers import Unanswered, read, registry


PREDICTIONS = """
WITH timings AS (
    SELECT wrapper AS worker, store_id, id, request_id, model, state, received_at,
           json_extract(row, '$.predicted_output_s') AS predicted_output_s,
           json_extract(row, '$.predicted_load_s') AS predicted_load_s,
           json_extract(row, '$.predicted_wait_s') AS predicted_wait_s,
           json_extract(row, '$.predicted_basis') AS basis,
           json_extract(row, '$.eta_derivation') AS derivation,
           CASE WHEN state = 'done' AND coalesce(http_status, 200) < 400 AND error IS NULL
                AND json_extract(row, '$.inference_ended_at') >= started_at
                THEN json_extract(row, '$.inference_ended_at') - started_at END AS actual_s,
           json_extract(row, '$.predicted_n') AS output_tokens,
           json_extract(row, '$.prompt_n') AS prompt_n,
           json_extract(row, '$.prompt_ms') AS prompt_ms,
           predicted_ms AS decode_ms,
           load_s AS actual_load_s,
           json_extract(row, '$.dispatched_at') - received_at AS actual_wait_s
    FROM calls WHERE endpoint <> '/v1/load'
), estimates AS (
    SELECT *, CASE WHEN predicted_output_s > 0 AND actual_s IS NOT NULL
                   THEN 100.0 * (actual_s - predicted_output_s) / predicted_output_s END AS error_pct,
           CASE WHEN json_array_length(derivation, '$.output_band_s') = 2 AND actual_s IS NOT NULL
                THEN actual_s BETWEEN json_extract(derivation, '$.output_band_s[0]')
                                  AND json_extract(derivation, '$.output_band_s[1]') END AS in_band,
           json_extract(derivation, '$.estimator') AS estimator,
           derivation IS NOT NULL AS derivation_recorded
    FROM timings
)
"""
FIELDS = """worker, id, request_id, model, state, received_at, predicted_output_s,
            actual_s, error_pct, in_band, basis, estimator, derivation_recorded"""


def recent(worker=None, model=None, limit=300):
    limit = max(1, min(int(limit), 2000))
    return sql.rows(
        PREDICTIONS + f"""SELECT {FIELDS} FROM estimates
        WHERE (predicted_output_s > 0 OR predicted_load_s > 0 OR predicted_wait_s > 0)
          AND (? IS NULL OR worker = ?) AND (? IS NULL OR model = ?)
        ORDER BY received_at DESC, worker, id DESC LIMIT ?""",
        (worker, worker, model, model, limit))


def accuracy(worker=None, model=None, limit=300):
    rows = recent(worker, model, limit)
    models = {}
    for row in reversed(rows):
        if row['error_pct'] is None:
            continue
        entry = models.setdefault(row['model'], dict(model=row['model'], series=[], bands=[], errors=[]))
        entry['series'].append(dict(received_at=row['received_at'], error_pct=row['error_pct']))
        entry['errors'].append(abs(row['error_pct']))
        if row['in_band'] is not None:
            entry['bands'].append(row['in_band'])
    result = []
    for entry in models.values():
        errors, bands = entry.pop('errors'), entry.pop('bands')
        result.append(dict(entry, n=len(errors), mean_abs_error_pct=sum(errors) / len(errors),
                           band_n=len(bands), band_coverage=sum(bands) / len(bands) if bands else None))
    return result


def detail(worker, request_id):
    found = sql.rows(PREDICTIONS + f"""SELECT {FIELDS}, store_id, derivation, predicted_wait_s,
        actual_wait_s, predicted_load_s, actual_load_s, output_tokens, prompt_n, prompt_ms, decode_ms FROM estimates
        WHERE worker = ? AND request_id = ? LIMIT 1""", (worker, request_id))
    if not found:
        raise LookupError('No recorded call matches this worker and request')
    row = found[0]
    stages = sql.rows("""SELECT stage, predicted_s, finished_at - started_at AS actual_s
        FROM call_stages WHERE wrapper = ? AND store_id = ? AND request_id = ?
        AND (predicted_s IS NOT NULL OR finished_at IS NOT NULL) ORDER BY id""",
        (worker, row.pop('store_id'), request_id))
    derivation = row.pop('derivation')
    return dict(summary=row, stages=stages, eta_derivation=json.loads(derivation) if derivation else None,
                actual=dict(prompt=dict(x=row['prompt_n'], y=row['prompt_ms']),
                            decode=dict(x=row['output_tokens'], y=row['decode_ms']),
                            out_tokens=dict(value=row['output_tokens']), load=dict(y=row['actual_load_s'])))


def current(worker, model=None):
    if not worker:
        raise ValueError('Choose a worker')
    connection = registry.get(worker)
    if not connection:
        raise LookupError('Unknown worker')
    if not connection['connected']:
        return dict(rows=[], note='This worker is disconnected.')
    try:
        plan = read(connection, '/v1/queue/plan', timeout=8)
    except (OSError, LookupError, Unanswered):
        return dict(rows=[], note='The worker’s live queue plan is unavailable.')
    rows = [row for row in plan.get('rows', []) if row.get('kind') == 'call'
            and (not model or model in (row.get('model'), row.get('unit')))]
    fields = ('queue_id', 'model', 'starts_in_s', 'load_s', 'engine_lo_s', 'engine_hi_s',
              'done_in_lo_s', 'done_in_hi_s', 'error')
    return dict(rows=[{key: row.get(key) for key in fields} for row in rows],
                note=None if rows else 'No queued calls match this worker and model.')
