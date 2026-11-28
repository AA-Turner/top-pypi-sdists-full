"""How what was collated is read: the calls, the models and the hosts of every wrapper.

Each function is one read of the views in sql/create.py. The database does the selecting, the grouping and the
counting; Python here only shapes the answer. A list of calls never carries what was asked and answered (a call
read by its id does).
"""
from ..imports import (
    json,
)
from .. import sql

CALL_COLUMNS = ('wrapper', 'id', 'request_id', 'model', 'endpoint', 'task', 'state', 'http_status', 'received_at',
                'started_at', 'responded_at', 'load_s', 'prompt_tokens', 'completion_tokens', 'grading_query')
LIMIT_MAX = 1000


def calls(wrapper: str = None, model: str = None, state: str = None, limit: int = 50, before: float = None,
          graded: bool = False) -> list:
    """The calls of every wrapper, newest first: one row a call, without what was asked and answered.
    ``model`` matches any part of the model's name; ``before`` is a received_at to page back from; ``graded``
    keeps only the calls made with a grading marker."""
    where, params = (['grading_query IS NOT NULL'] if graded else []), []
    for column, value in (('wrapper', wrapper), ('state', state)):
        if value:
            where.append(f'{column} = ?')
            params.append(value)
    if model:
        where.append("model LIKE '%' || ? || '%'")
        params.append(model)
    if before is not None:
        where.append('received_at < ?')
        params.append(float(before))
    return sql.rows(f"SELECT {', '.join(CALL_COLUMNS)} FROM calls" + (' WHERE ' + ' AND '.join(where) if where else '')
                    + ' ORDER BY received_at DESC LIMIT ?', (*params, max(1, min(int(limit), LIMIT_MAX))))


def call(request_id: str):
    """One call by its request id, whole as its wrapper published it, with its stages; None when Core has no such
    call. A wrapper numbers its own calls, so an id is looked for across them, newest first."""
    found = sql.rows("SELECT wrapper, store_id, row FROM calls WHERE request_id = ? ORDER BY received_at DESC LIMIT 1",
                     (request_id,))
    if not found:
        return None
    one = found[0]
    stages = sql.rows("SELECT stage, started_at, finished_at, predicted_s, note FROM call_stages "
                      "WHERE wrapper = ? AND store_id = ? AND request_id = ? ORDER BY id",
                      (one['wrapper'], one['store_id'], request_id))
    return dict(wrapper=one['wrapper'], store_id=one['store_id'], call=json.loads(one['row']), stages=stages)


LISTS = ('required_inputs', 'optional_inputs', 'requires')     # what a wrapper says of a model as a list
REASONS = ('offer_reason', 'possible_reason', 'env_reason')     # why a wrapper does not offer it, cannot place it, cannot run it


def models(wrapper: str = None, search: str = None, task: str = None, engine: str = None, endpoint: str = None) -> list:
    """The models of the fleet: each model once, with the wrappers that can serve it and what each says of it
    (loaded now, on its worker drive, whether it can be called there, and why not when it cannot), the paths it is
    called on, what a call of it must carry and what it may, and the models its engine loads beside it. Only
    wrappers that can be asked now count. A model is offered, possible or selectable when it is on any of them.
    ``task`` and ``engine`` may each name several, with commas; ``endpoint`` keeps the models called on that path."""
    where, params = ['s.reachable = 1'], []
    if wrapper:
        where.append('m.wrapper = ?')
        params.append(wrapper)
    for column, value in (('m.task', task), ('m.engine', engine)):
        names = [name for name in (value or '').split(',') if name]
        if names:
            where.append(f"{column} IN ({', '.join('?' * len(names))})")
            params += names
    if endpoint:
        where.append("EXISTS (SELECT 1 FROM json_each(m.endpoints) e WHERE e.value = ?)")
        params.append(endpoint)
    if search:
        where.append("m.id LIKE '%' || ? || '%'")
        params.append(search)
    found = sql.rows(
        "SELECT m.id, max(m.model_key) AS model_key, max(m.engine) AS engine, max(m.task) AS task, "
        "max(m.weight_bytes) AS weight_bytes, max(m.resident) AS resident, max(m.accommodated) AS accommodated, "
        "max(m.selectable) AS selectable, max(m.offered) AS offered, max(m.task) AS primary_task, "
        "max(m.possible) AS possible, max(json_extract(m.row, '$.hub_id')) AS hub_id, "
        + ''.join(f"max(json_extract(m.row, '$.{name}')) AS {name}, " for name in LISTS) +
        "json_group_array(json_object('wrapper', m.wrapper, 'resident', m.resident, 'accommodated', m.accommodated, "
        "'selectable', m.selectable, 'possible', m.possible, 'env_status', m.env_status, "
        "'endpoints', json(m.endpoints), "
        + ''.join(f"'{name}', json_extract(m.row, '$.{name}'), " for name in REASONS) +
        # how the wrapper says a load of it would lie there now, and how it is loaded there (its own names)
        "'placed', json_extract(m.row, '$.options.placed.reads_as'), "
        "'loaded_as', json_extract(m.row, '$.options.loaded_as'))) AS wrappers "
        "FROM models m JOIN wrapper_status s ON s.name = m.wrapper WHERE " + ' AND '.join(where)
        + " GROUP BY m.id ORDER BY m.id", params)
    for row in found:
        row['wrappers'] = json.loads(row['wrappers'])
        row['endpoints'] = sorted({path for worker in row['wrappers'] for path in worker['endpoints']})
        for name in LISTS:
            row[name] = json.loads(row[name]) if row[name] else []
        for name in ('resident', 'accommodated', 'selectable', 'offered', 'possible'):
            row[name] = bool(row[name])
        for name in REASONS:                  # said for the model only where no wrapper can: the first one's own words
            said = [w[name] for w in row['wrappers'] if w.get(name)]
            if said and not row[{'offer_reason': 'offered', 'possible_reason': 'possible', 'env_reason': 'selectable'}[name]]:
                row[name] = said[0]
            for w in row['wrappers']:
                if not w.get(name):
                    w.pop(name, None)
    return found


def fleet() -> list:
    """Every saved wrapper as it stands now: its connection, its cards, its memory, what is loaded and its drives."""
    parts = {name: {} for name in ('cards', 'hosts', 'residents', 'drives')}
    for name, by_wrapper in parts.items():
        columns = '*' if name != 'drives' else 'wrapper, path, role, total, free, room, models, read_bytes_per_s, write_bytes_per_s'
        for row in sql.rows(f'SELECT {columns} FROM {name}'):
            by_wrapper.setdefault(row.pop('wrapper'), []).append(row)
    counted = {row['wrapper']: row for row in sql.rows(
        "SELECT wrapper, count(*) AS models, sum(selectable) AS selectable FROM models GROUP BY wrapper")}
    called = {row['wrapper']: row for row in sql.rows(
        "SELECT wrapper, count(*) AS calls, max(received_at) AS last_call_at FROM calls GROUP BY wrapper")}
    out = []
    for row in sql.rows('SELECT * FROM wrapper_status ORDER BY name'):
        name = row['name']
        row['reasons'] = json.loads(row['reasons']) if row.get('reasons') else []
        out.append(dict(row, cards=parts['cards'].get(name, []), host=(parts['hosts'].get(name) or [None])[0],
                        residents=parts['residents'].get(name, []), drives=parts['drives'].get(name, []),
                        models=(counted.get(name) or {}).get('models', 0),
                        selectable=(counted.get(name) or {}).get('selectable', 0),
                        calls=(called.get(name) or {}).get('calls', 0),
                        last_call_at=(called.get(name) or {}).get('last_call_at')))
    return out


__all__ = ['call', 'calls', 'fleet', 'models']
