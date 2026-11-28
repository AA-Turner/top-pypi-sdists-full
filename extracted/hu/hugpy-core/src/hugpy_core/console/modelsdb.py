"""The fleet models database, as the console's Databases tab reads it.

Every model a wrapper's Discovery has recorded is a row here, on every wrapper that has it: what it is (its
Discovery's facts), whether its wrapper can serve it and how it would place it (the wrapper's own verdicts), and
what the call log says of it. Nothing is kept for this: the list is a read of what Core collated (the views units,
models and model_calls), and a model's tables are read where they are, when its page is opened:

    in the wrapper       its own tables and its Discovery's export, through the table reader it has for Core
                         (GET /v1/telemetry/rows): the model's files, its copy on each drive, its variations,
                         its parts, what it needs to load, its saved choices, its tensors
    in Core              the calls, the loads and the grades of the model (the call log)

The console names tables as its first models database did (model_files, model_calls ...); TABLES says where the
rows of each are. A table of that list no wrapper has rows for answers empty.
"""
from ..imports import (
    json,
    time,
    urlencode,
)
from .. import sql
from ..grading import read as grading_read
from ..wrappers import ask, registry

SUMMARY_COLUMNS = ('model_uid', 'status', 'display_name', 'hub_id', 'catalog_key', 'engine', 'runner', 'primary_task',
                   'architecture', 'size_label', 'n_params', 'context_length', 'elected_quant', 'served_bytes', 'is_moe',
                   'has_vision', 'has_chat_template', 'license', 'feasibility_status', 'auto_mode', 'auto_ctx',
                   'calls_total', 'last_called_at', 'median_decode_tok_s', 'served_store_role', 'copies')
STATUS_ORDER = ('servable', 'discovered', 'external', 'remote', 'retired')
SECTION_LABELS = dict(overview='Overview', identity='Identity', variants='Variants', files='Files', feasibility='Feasibility',
                      runtime='Runtime', structure='Structure', content='Content', provider='Provider', history='History',
                      grading='Grading')
WRAPPER, CORE = 'wrapper', 'core'
# the console's table: (its section, where its rows are, the table or view there, whether it holds every
# variation of the model's folder and not only this one, what it is)
TABLES = {
    'model_copies': ('identity', WRAPPER, 'discovery.api_unit_presence_v1', False,
                     'The model on each declared drive: whether it is whole there, and how much of it is.'),
    'model_variants': ('variants', WRAPPER, 'units_mat', True,
                       "Every variation of the model's folder as its wrapper serves it: its weights, its engine, where it is loaded from."),
    'model_units': ('variants', WRAPPER, 'discovery.api_units_v1', True,
                    "Every variation of the model's folder as its Discovery recorded it, with the route it is loaded by."),
    'model_components': ('variants', WRAPPER, 'discovery.api_unit_representations_v1', False,
                         'The parts of the model and the bytes of each as stored, as 16-bit and as 4-bit.'),
    'model_dependencies': ('variants', WRAPPER, 'discovery.api_unit_dependencies_v1', False,
                           'The other models this one needs beside it.'),
    'model_files': ('files', WRAPPER, 'discovery.api_unit_files_v1', False,
                    "The files that make the model: each one's bytes, its role, where it is on the central and the worker drive."),
    'model_feasibility': ('feasibility', WRAPPER, 'feasibility', False,
                          'What the model needs to load here, and the least and most of it each of card, memory, swap and disk can hold.'),
    'model_allocations': ('feasibility', WRAPPER, 'allocations', False,
                          "Every column of the model's scale on its wrapper: how many of its GPU layers are on the card, "
                          "in host memory or read from its file, ranked by speed (rank 1 the fastest), whether every routed "
                          "expert is off the card (moe), and the most ticks of context the card and host memory hold beside it."),
    'model_allocation_layers': ('feasibility', WRAPPER, 'allocation_layers', False,
                                "Every allocation column written out layer by layer: each GPU layer, in fill order, on the "
                                "resource that column puts it on (gpu; ram or disk below the card; offload)."),
    'model_gpu_layers': ('feasibility', WRAPPER, 'gpu_layers', False,
                         "The model's GPU layers in the order a placement fills them (what every step reads first, the "
                         "routed experts after, what a call reads once last), each with its bytes on the card and in host memory."),
    'model_kv_ticks': ('feasibility', WRAPPER, 'kv_ticks', False,
                       "The model's context in ticks: tick k is k hundredths of the context it was trained for, with "
                       "the bytes its memory takes there."),
    'model_load_estimates': ('feasibility', WRAPPER, 'discovery.api_placements_v1', False,
                             'Having the model on each drive: whether it fits, what must be copied, and how long that takes.'),
    'model_measured_loads': ('feasibility', CORE, 'loads', False,
                             'Every load of the model its wrapper recorded: where it was placed, how long it took, how it ended.'),
    'model_calls': ('runtime', CORE, 'calls', False,
                    'Every call of the model in the call log, newest first.'),
    'model_settings': ('runtime', WRAPPER, 'selections', False,
                       "What was chosen for the model on its wrapper: its placement limits, its context, its quant."),
    'model_residency': ('runtime', CORE, 'residents', False,
                        'The model as it is loaded now: its process, its bytes on the card and in memory.'),
    'model_grades': ('grading', CORE, 'grading_schedule', False,
                     "The model's grading schedule: every query it is asked, in order, with the verdict of its answer."),
}
LAZY_TABLES = {'model_tensors': ('discovery.api_unit_tensors_v1', "Every tensor of the model's files: its bytes, its layer, its role.")}
COLUMN_TEXT = dict(
    model_uid="The model as its wrapper names it: its folder and its variation.",
    status='servable: its wrapper can call it. discovered: recorded on a drive, and no engine there serves it.',
    display_name="The name of the model's folder.", hub_id='Where the model came from on the hub.',
    catalog_key='The name a call gives to have this model.', engine='The engine that serves it on this wrapper.',
    primary_task='What it does.', architecture='Its architecture, as its files say.',
    context_length='The context it was trained with, in tokens.', elected_quant='Its variation: the file of the folder that is loaded.',
    served_bytes="The bytes of its weights.", is_moe='Whether it is a mixture of experts.',
    has_vision='Whether it takes images.', feasibility_status='Whether it can be loaded on this host at all.',
    auto_mode='How its wrapper would place it now.', auto_ctx='The context its wrapper would give it now.',
    calls_total='The calls of it in the call log.', last_called_at='When it was last called.',
    median_decode_tok_s='Its tokens a second: tokens over generating time, over every call that has both.',
    served_store_role='The drive it is loaded from: worker, immutable or central.',
    copies='On how many declared drives it is whole.')
CALL_COLUMNS = ('request_id', 'endpoint', 'task', 'state', 'http_status', 'received_at', 'started_at', 'responded_at', 'load_s',
                'prompt_tokens', 'completion_tokens', 'predicted_ms', 'grading_query', 'grading_round', 'error')
LOAD_COLUMNS = ('load_id', 'engine', 'placement', 'staged_at', 'ready_at', 'ended_at', 'outcome', 'end_reason', 'vram_bytes')
GRADE_COLUMNS = ('query', 'suite', 'category', 'tier_name', 'standing', 'passed', 'shown', 'why', 'graded_at', 'request_id')
COUNT_PAGE = 200                # rows asked of a wrapper to count a model's rows of one table


class Unanswered(Exception):
    """The console's models database could not answer: a code it knows, and what to say (``status`` is HTTP's)."""

    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status, self.code = status, code


def iso(at):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(at)) if at else None


def unit_id(key: str, variation: str) -> str:
    return f'{key}::{variation}'


def summary(unit: dict, model: dict, calls: dict) -> dict:
    """One recorded model on one wrapper as the console's summary: its Discovery's facts, its wrapper's verdicts,
    and its calls."""
    said, served = json.loads(unit['row']), json.loads(model['row']) if model else {}
    placed = (served.get('options') or {}).get('placed') or {}
    uid = unit_id(unit['model_key'], unit['variation'])
    tokens, seconds = (calls or {}).get('tokens'), (calls or {}).get('seconds')
    return dict(
        model_uid=uid, status='servable' if served.get('selectable') else 'discovered',
        display_name=unit['model_key'].rsplit('/', 1)[-1], hub_id=served.get('hub_id') or unit['model_key'], catalog_key=uid,
        engine=served.get('owned_by') or unit['engine'], runner=None, primary_task=served.get('primary_task') or unit['task'],
        architecture=unit['arch'], size_label=None, n_params=None, context_length=unit['ctx_train'],
        elected_quant=None if unit['variation'] in ('', '*') else unit['variation'],
        served_bytes=served.get('weight_bytes') or unit['bytes'], is_moe=bool(said.get('expert_count')),
        has_vision=(served.get('primary_task') or unit['task']) == 'image-text-to-text', has_chat_template=None, license=None,
        feasibility_status=None if not served else 'possible' if served.get('possible') else 'impossible',
        auto_mode=placed.get('reads_as'), auto_ctx=placed.get('ctx'), calls_total=(calls or {}).get('calls', 0),
        last_called_at=iso((calls or {}).get('last_call_at')),
        median_decode_tok_s=round(tokens / seconds, 2) if tokens and seconds else None,
        served_store_role=unit['source_role'],
        copies=sum(1 for place in said.get('locations') or [] if place.get('present')))


def recorded(wrapper: str = None) -> list:
    """Every model every wrapper's Discovery has recorded, each with its summary: [{worker, summary}]."""
    where, params = (' WHERE u.wrapper = ?', (wrapper,)) if wrapper else ('', ())
    served = {(row['wrapper'], row['id']): row for row in sql.rows("SELECT wrapper, id, row FROM models")}
    called = {(row['wrapper'], row['model']): row for row in sql.rows("SELECT * FROM model_calls")}
    out = []
    for unit in sql.rows("SELECT u.wrapper, u.model_key, u.variation, u.bytes, u.engine, u.task, u.source_role, u.arch, "
                         "u.ctx_train, u.row FROM units u" + where + " ORDER BY u.model_key, u.variation", params):
        uid = unit_id(unit['model_key'], unit['variation'])
        out.append(dict(worker=unit['wrapper'], summary=summary(unit, served.get((unit['wrapper'], uid)), called.get((unit['wrapper'], uid)))))
    return out


def builds() -> list:
    """Each wrapper's record of models as Core holds it: the generation of its Discovery's record, when it was
    built, when Core last read it, and how many models it has."""
    counted = {row['wrapper']: row for row in sql.rows(
        "SELECT u.wrapper, count(*) AS models, max(u.read_at) AS read_at FROM units u GROUP BY u.wrapper")}
    health = {row['wrapper']: json.loads(row['document']) for row in sql.rows(
        "SELECT wrapper, document FROM wrapper_documents WHERE name = 'health'")}
    out = []
    for row in registry.status():
        name = row['name']
        catalog = ((health.get(name) or {}).get('discovery') or {}).get('catalog') or {}
        mine = counted.get(name)
        out.append(dict(
            worker=name, store_id=row.get('store_id'), build_id=catalog.get('generation'), generation=catalog.get('generation'),
            built_at=iso(catalog.get('built_at')), synced_at=iso(mine['read_at']) if mine else None,
            models=mine['models'] if mine else 0, partitions=mine['models'] if mine else 0, rows=mine['models'] if mine else 0,
            sync_state='synced' if mine and row['reachable'] else 'unavailable' if not mine else 'error' if row.get('error') else 'synced',
            neutral=False, error=row.get('error') if row['connected'] else None, error_at=iso(row.get('error_at')),
            failed_sections=[], unattributed={}, run=None, registered=True, connected=bool(row['connected']),
            wrapper=dict(building=catalog.get('state') not in (None, 'current'), enabled=True, last_error=catalog.get('reason'))))
    return out


def fleet(q: str = None, status: str = None, worker: str = None, engine: str = None, task: str = None, sort: str = None,
          desc: bool = False, limit: int = 200, offset: int = 0) -> dict:
    """The fleet's models, one row a model with the wrappers that have it: searched (``q``: any part of its name),
    narrowed (status, worker, engine, task), ordered (``sort``: a summary column), a page at a time."""
    found = recorded()
    grouped = {}
    for one in found:
        grouped.setdefault(one['summary']['model_uid'], []).append(one)
    needle = (q or '').strip().lower()
    rows, facets = [], dict(status={}, engine={}, task={}, worker={})
    for uid, places in grouped.items():
        if needle and needle not in uid.lower() and needle not in str(places[0]['summary']['hub_id']).lower():
            continue
        kept = [one for one in places if (not worker or one['worker'] == worker) and (not status or one['summary']['status'] == status)
                and (not engine or one['summary']['engine'] == engine) and (not task or one['summary']['primary_task'] == task)]
        # what each choice would show is counted over what the search found, whatever is chosen now
        for one in places:
            for name, value in (('status', one['summary']['status']), ('engine', one['summary']['engine']),
                                ('task', one['summary']['primary_task']), ('worker', one['worker'])):
                if value:
                    facets[name][value] = facets[name].get(value, 0) + 1
        if kept:
            first = kept[0]['summary']
            rows.append(dict(fleet_id=uid, display_name=first['display_name'], hub_id=first['hub_id'], summary=first,
                             workers=[dict(worker=one['worker'], model_uid=uid, status=one['summary']['status']) for one in kept],
                             observed_by=[]))
    column = sort if sort in SUMMARY_COLUMNS else 'display_name'
    rows.sort(key=lambda row: (row['summary'].get(column) is None, row['summary'].get(column) if not isinstance(
        row['summary'].get(column), str) else row['summary'][column].lower(), row['fleet_id']), reverse=bool(desc))
    limit, offset = max(1, min(int(limit or 200), 5000)), max(0, int(offset or 0))
    return dict(total=len(rows), fleet_total=len(grouped), limit=limit, offset=offset, columns=list(SUMMARY_COLUMNS),
                facets=facets, rows=rows[offset:offset + limit], builds=builds(), include_removed=False)


def find(worker: str, uid: str) -> tuple:
    """(the wrapper's saved connection, the model's folder, its variation, its summary). Unanswered when the
    wrapper is not one Core has, or has no such model."""
    wrapper = registry.get(worker)
    if wrapper is None:
        raise Unanswered(404, 'worker-removed', f'worker-removed: {worker} is not a wrapper this Core has connected')
    key, _, variation = uid.partition('::')
    mine = next((one['summary'] for one in recorded(worker) if one['summary']['model_uid'] == uid), None)
    if mine is None:
        raise Unanswered(404, 'not-found', f"{worker}'s record has no model {uid}")
    return wrapper, key, variation, mine


# a wrapper table read in its own order: an allocation column by rank, a layer by its place, a tick by its number
SORTED_BY = dict(allocations='rank', gpu_layers='pos', kv_ticks='tick', allocation_layers='seq')


def wrapper_rows(wrapper: dict, table: str, key: str, variation, limit: int, offset: int) -> tuple:
    """A page of one of a wrapper's tables, kept to one model -> (columns, rows, whether there is more). The
    wrapper finds rows whose folder name holds the model's; only the rows of exactly this model are kept."""
    # exactly this model's rows (eq.key, eq.variation: a wrapper since 0.2.0.12), and the folder name as well, which a
    # wrapper before it filters by alone
    exact = {'eq.key': key, **({'eq.variation': variation} if variation is not None else {})}
    try:
        status, page = ask(wrapper, '/v1/telemetry/rows?' + urlencode(dict(table=table, column='key', q=key, limit=limit,
                                                                            offset=offset, **exact,
                                                                            **({'sort': SORTED_BY[table]} if table in SORTED_BY else {}))),
                           timeout=20)
    except (OSError, LookupError, TimeoutError) as exc:
        raise Unanswered(409, 'worker-not-connected', f"worker-not-connected: {wrapper['name']} did not answer ({exc})") from None
    if status != 200 or not isinstance(page, dict):
        said = (page or {}).get('error') if isinstance(page, dict) else None
        raise Unanswered(404, 'not-offered', f"not-offered: {wrapper['name']} did not give its table {table} (HTTP {status}"
                                             + (f': {said}' if said else '') + ')')
    columns = [column['name'] if isinstance(column, dict) else column for column in page.get('columns') or []]
    rows = [row for row in page.get('rows') or []
            if row.get('key') == key and (variation is None or 'variation' not in row or row['variation'] == variation)]
    return columns, rows, bool(page.get('has_more'))


def core_rows(worker: str, uid: str, view: str, limit: int, offset: int) -> tuple:
    """A page of what Core itself holds of one model -> (columns, rows, total)."""
    if view == 'grading_schedule':
        rows = [dict({name: row.get(name) for name in GRADE_COLUMNS}) for row in grading_read.schedule(worker, uid)]
        return list(GRADE_COLUMNS), rows[offset:offset + limit], len(rows)
    if view == 'residents':
        rows = sql.rows("SELECT * FROM residents WHERE wrapper = ? AND model = ?", (worker, uid))
        return ([name for name in rows[0] if name != 'wrapper'] if rows else []), [
            {name: value for name, value in row.items() if name != 'wrapper'} for row in rows], len(rows)
    columns, order = (CALL_COLUMNS, 'received_at') if view == 'calls' else (LOAD_COLUMNS, 'staged_at')
    total = sql.rows(f"SELECT count(*) AS n FROM {view} WHERE wrapper = ? AND model = ?", (worker, uid))[0]['n']
    rows = sql.rows(f"SELECT {', '.join(columns)} FROM {view} WHERE wrapper = ? AND model = ? ORDER BY {order} DESC LIMIT ? OFFSET ?",
                    (worker, uid, limit, offset))
    return list(columns), rows, total


def paging(limit, offset) -> tuple:
    return max(1, min(int(limit or 50), 200)), max(0, int(offset or 0))


def table(worker: str, uid: str, name: str, limit: int = 50, offset: int = 0) -> dict:
    """A page of one table of a model's page. A table the console names that has no rows anywhere answers empty."""
    wrapper, key, variation, _ = find(worker, uid)
    limit, offset = paging(limit, offset)
    out = dict(worker=worker, model_uid=uid, table=name, limit=limit, offset=offset)
    if name not in TABLES:
        return dict(out, columns=[], rows=[], total=0)
    section, where, source, whole, _ = TABLES[name]
    out.update(section=section, label=SECTION_LABELS[section])
    if where == CORE:
        columns, rows, total = core_rows(worker, uid, source, limit, offset)
        return dict(out, columns=columns, rows=rows, total=total)
    columns, rows, more = wrapper_rows(wrapper, source, key, None if whole else variation, limit, offset)
    return dict(out, columns=columns, rows=rows, has_more=more, **({} if more or offset else {'total': len(rows)}))


def tensors(worker: str, uid: str, name: str, after: int = 0, limit: int = 50) -> dict:
    """A page of a model's tensors, read live from its wrapper; ``after`` is where the page before it ended."""
    wrapper, key, variation, _ = find(worker, uid)
    limit, after = paging(limit, after)
    out = dict(worker=worker, model_uid=uid, table=name, after=after, limit=limit, build_id='', generation='')
    if name not in LAZY_TABLES:
        return dict(out, columns=[], rows=[], next_after=None, more=False)
    columns, rows, more = wrapper_rows(wrapper, LAZY_TABLES[name][0], key, variation, limit, after)
    return dict(out, columns=columns, rows=rows, next_after=after + limit, more=more)


def model(worker: str, uid: str) -> dict:
    """One model's page: what is known of it (its summary and every fact its Discovery published), the sections of
    its tables with how many rows each has for it, and the other wrappers that have the same model."""
    wrapper, key, variation, mine = find(worker, uid)
    unit = sql.rows("SELECT row FROM units WHERE wrapper = ? AND model_key = ? AND variation = ?", (worker, key, variation))
    served = sql.rows("SELECT row FROM models WHERE wrapper = ? AND id = ?", (worker, uid))
    facts = dict(mine)
    for name, value in (json.loads(unit[0]['row']) if unit else {}).items():
        facts.setdefault(name, value)
    for name, value in (json.loads(served[0]['row']) if served else {}).items():
        if name not in ('id', 'object'):
            facts.setdefault(name, value)
    sections = {}
    for name, (section, where, source, whole, _) in TABLES.items():
        try:
            if where == CORE:
                count = core_rows(worker, uid, source, 1, 0)[2]
            else:
                _, rows, more = wrapper_rows(wrapper, source, key, None if whole else variation, COUNT_PAGE, 0)
                count = None if more else len(rows)
        except Unanswered:
            count = None                    # its wrapper does not answer now: the count is not known
        sections.setdefault(section, []).append(dict(table=name, rows=count))
    return dict(worker=worker, model_uid=uid, fleet_id=uid, display_name=mine['display_name'], model=facts,
                build=next((build for build in builds() if build['worker'] == worker), None),
                sections=[dict(section=section, label=SECTION_LABELS[section], tables=tables) for section, tables in sections.items()],
                siblings=[dict(worker=one['worker'], model_uid=uid, status=one['summary']['status'])
                          for one in recorded() if one['summary']['model_uid'] == uid and one['worker'] != worker],
                lazy_tables=list(LAZY_TABLES))


def dictionary() -> dict:
    """What the tables and the summary columns are, in words."""
    tables = {name: dict(description=about, columns={}, section=section) for name, (section, _, _, _, about) in TABLES.items()}
    tables.update({name: dict(description=about, columns={}, section='structure') for name, (_, about) in LAZY_TABLES.items()})
    tables['models'] = dict(description="One row a model a wrapper's Discovery has recorded.", columns=dict(COLUMN_TEXT), section='overview')
    return dict(tables=tables, sections=[dict(section=name, label=label) for name, label in SECTION_LABELS.items()],
                global_tables=[], lazy_tables=list(LAZY_TABLES), summary_columns=list(SUMMARY_COLUMNS),
                status_order=list(STATUS_ORDER), workers=[row['name'] for row in registry.saved()])


__all__ = ['Unanswered', 'builds', 'dictionary', 'fleet', 'model', 'table', 'tensors']
