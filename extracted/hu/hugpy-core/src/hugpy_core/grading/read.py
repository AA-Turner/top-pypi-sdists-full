"""How grading is read: the table, every model's schedule, and what the call log says came of each query.

Nothing here is kept. A grade is a call of the call log that carries a query's marker and was answered (the views
graded_calls, grades and grading_schedule of sql/create.py), with the query's checks applied to its answer when it
is asked for (hugpy_resources check_reply). So a grade can be read at any time, of any call ever made with a marker,
and a query whose checks were changed regrades every answer it ever had.

    queries()       the grading table, each query with what it asks and what its checks require, in words
    suites()        the suites of the table: the task each grades, its categories, its tiers
    verdict(row)    whether one graded call's answer passes its query's checks, and why not
    graded(...)     the calls made with a marker (of a wrapper, a model, a round ...), each with its verdict
    schedule(...)   every model's queries in the order they are asked, each graded, being asked, or not performed
    standing(...)   one row a model: how much of its schedule is graded, how much passed, what is asked next
    unperformed(wrapper)  {model: its queries not performed yet, in order}: what a round sets out to ask
"""
from ..imports import (
    CALL_ANSWERED,
    TIER_NAMES,
    check_reply,
    check_rule,
    json,
    reply_shown,
)
from .. import sql

VERDICTS_KEPT = 50000           # verdicts remembered while Core runs: a call that was answered does not change
_VERDICTS = {}                  # (wrapper, store_id, call id, checks) -> (passed, why, shown)
GRADED_COLUMNS = ('wrapper, store_id, id, request_id, model, endpoint, state, http_status, received_at, started_at, '
                  'responded_at, load_s, prompt_tokens, completion_tokens, predicted_ms, error, query, round, suite, '
                  'task, category, tier, position, checks, answer, body, reply, nth')


def tier_name(tier) -> str:
    """A tier as it is said: 1 is easy."""
    return TIER_NAMES[tier - 1] if isinstance(tier, int) and 1 <= tier <= len(TIER_NAMES) else str(tier)


def asked(body) -> str:
    """What a query asks, in a line: the words of its question, the text it embeds or speaks, its prompt."""
    body = json.loads(body) if isinstance(body, str) else body or {}
    for message in reversed(body.get('messages') or []):
        content = message.get('content') if isinstance(message, dict) else None
        if isinstance(content, list):
            content = ' '.join(part.get('text') or '' for part in content if isinstance(part, dict) and part.get('type') == 'text')
        if isinstance(content, str) and content.strip():
            return content.replace('/no_think', '').strip()
    given = body.get('input', body.get('prompt'))
    if isinstance(given, list):
        return ' | '.join(str(part) for part in given)
    if isinstance(given, str):
        return given
    return ', '.join(sorted(name.rsplit('_', 1)[0] for name in body if name.endswith('_b64'))) or '(nothing in words)'


def queries(suite: str = None) -> list:
    """The grading table in the order a model is asked it, each query with what it asks (``asks``) and what its
    checks require (``rule``), in words. Its body and checks are given as they are."""
    found = sql.rows("SELECT * FROM grading_queries" + (" WHERE suite = ?" if suite else "")
                     + " ORDER BY suite, tier, position", (suite,) if suite else ())
    for row in found:
        row['checks'] = json.loads(row['checks'])
        row.update(tier_name=tier_name(row['tier']), asks=asked(row['body']), rule=check_rule(row['checks']))
    return found


def suites() -> list:
    """The suites of the grading table: the task each grades, its categories in the table's order, its tiers and
    how many queries it has, with every query under its category."""
    out = {}
    for query in queries():
        suite = out.setdefault(query['suite'], dict(name=query['suite'], task=query['task'], categories=[], tiers=0,
                                                    queries=0, items={}))
        if query['category'] not in suite['categories']:
            suite['categories'].append(query['category'])
        suite['tiers'] = max(suite['tiers'], query['tier'])
        suite['queries'] += 1
        suite['items'].setdefault(query['category'], []).append(query)
    return list(out.values())


def verdict(row: dict) -> tuple:
    """(passed, why, shown) of one graded call: whether its answer meets its query's checks, why not, and what the
    answer showed. passed is None for a call that was not answered, or whose query the table does not have: there
    is nothing to check."""
    if row.get('state') != CALL_ANSWERED or not row.get('checks'):
        return None, row.get('error'), ''
    key = (row['wrapper'], row['store_id'], row['id'], row['checks'])
    if key not in _VERDICTS:
        if len(_VERDICTS) >= VERDICTS_KEPT:
            _VERDICTS.clear()
        reply = json.loads(row['reply']) if row.get('reply') else None
        try:
            passed, why = check_reply(json.loads(row['checks']), reply)
        except ValueError as exc:               # the query's checks cannot be read: said, never passed
            passed, why = None, str(exc)
        _VERDICTS[key] = (passed, why, reply_shown(reply))
    return _VERDICTS[key]


def graded(wrapper: str = None, model: str = None, round_id: str = None, query: str = None, newest: bool = False,
           limit: int = None) -> list:
    """The calls made with a grading marker, newest first, each with its verdict (passed, why, shown) and without
    its body and its reply. ``newest`` keeps, of every model and query, only the call its grade is read from."""
    where, params = (['state = ?', 'nth = 1', 'suite IS NOT NULL'], [CALL_ANSWERED]) if newest else ([], [])
    for column, value in (('wrapper', wrapper), ('model', model), ('round', round_id), ('query', query)):
        if value:
            where.append(f'{column} = ?')
            params.append(value)
    found = sql.rows(f"SELECT {GRADED_COLUMNS} FROM graded_calls" + (' WHERE ' + ' AND '.join(where) if where else '')
                     + ' ORDER BY received_at DESC, id DESC' + (' LIMIT ?' if limit else ''),
                     (*params, int(limit)) if limit else params)
    for row in found:
        row['passed'], row['why'], row['shown'] = verdict(row)
        body = row.pop('body')
        row.update(asks=asked(body) if body else None, tier_name=tier_name(row['tier']))
        del row['reply'], row['checks']
    return found


def schedule(wrapper: str = None, model: str = None) -> list:
    """Every model's schedule, in the order it is asked: each query with ``standing`` (graded, asking: its wrapper
    holds a call for it now, or open: not performed) and, when graded, whether it passed."""
    where, params = [], []
    for column, value in (('wrapper', wrapper), ('model', model)):
        if value:
            where.append(f'{column} = ?')
            params.append(value)
    found = sql.rows("SELECT * FROM grading_schedule" + (' WHERE ' + ' AND '.join(where) if where else '')
                     + ' ORDER BY wrapper, model, tier, position', params)
    verdicts = {(row['wrapper'], row['model'], row['query']): row for row in graded(wrapper, model, newest=True)}
    for row in found:
        call = verdicts.get((row['wrapper'], row['model'], row['query'])) if row['request_id'] else None
        row.update(tier_name=tier_name(row['tier']), passed=call['passed'] if call else None,
                   why=call['why'] if call else None, shown=call['shown'] if call else None,
                   standing='graded' if row['request_id'] else 'asking' if row['asking'] else 'open')
    return found


def standing(wrapper: str = None, model: str = None) -> list:
    """One row a model that has a schedule: its suite, how many queries it has (of), how many are graded, how
    many passed, how many its wrapper is being asked now, and the query it is asked next (None: none is left)."""
    out = {}
    for row in schedule(wrapper, model):
        one = out.setdefault((row['wrapper'], row['model']), dict(
            wrapper=row['wrapper'], model=row['model'], task=row['task'], engine=row['engine'], suite=row['suite'],
            of=0, graded=0, passed=0, asking=0, next=None, graded_at=None))
        one['of'] += 1
        one['graded'] += row['standing'] == 'graded'
        one['passed'] += row['passed'] is True
        one['asking'] += row['standing'] == 'asking'
        if row['standing'] == 'open' and one['next'] is None:
            one['next'] = row['query']
        if row['graded_at'] and (one['graded_at'] is None or row['graded_at'] > one['graded_at']):
            one['graded_at'] = row['graded_at']
    return list(out.values())


def unperformed(wrapper: str) -> dict:
    """{model: the queries of its schedule not performed yet, in the order they are asked} for one wrapper. A
    model whose every query is graded or being asked has an empty list; one with no schedule is not here."""
    out = {}
    for row in sql.rows("SELECT model, query, request_id, asking FROM grading_schedule WHERE wrapper = ? "
                        "ORDER BY model, tier, position", (wrapper,)):
        found = out.setdefault(row['model'], [])
        if not row['request_id'] and not row['asking']:
            found.append(row['query'])
    return out


def first_query(wrapper: str) -> dict:
    """{model: the first query of its schedule} for one wrapper: what a model with nothing left to grade is asked
    again when it is fired all the same."""
    out = {}
    for row in sql.rows("SELECT model, query FROM grading_schedule WHERE wrapper = ? ORDER BY model, tier, position",
                        (wrapper,)):
        out.setdefault(row['model'], row['query'])
    return out


__all__ = ['asked', 'first_query', 'graded', 'queries', 'schedule', 'standing', 'suites', 'tier_name', 'unperformed', 'verdict']
