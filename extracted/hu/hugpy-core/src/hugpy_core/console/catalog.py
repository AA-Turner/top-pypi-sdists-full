"""The console's models, its raw call log and its landing page's "Your instance", from what Core holds of the
wrappers.

    models()        the models the wrappers can serve, as the console's model rows
    folders()       the Models tab: every model folder a wrapper's Discovery has recorded, with its variations
    folder(key)     one of them whole: its variations, its files, and the tables that hold rows of it
    records(...)    a page of one of those tables, read from the wrapper that has the model
"""
from ..imports import (
    KNOB_SCHEMA,
    PACKAGE,
    PLACEMENT_RENAMES,
    PLACEMENT_TERMS,
    PLACEMENTS,
    json,
    quant_token,
    time,
    tool_version,
)
from .. import collate, sql
from ..wrappers import registry
from . import modelsdb

NOT_MEDIA = ('text-generation', 'feature-extraction', 'summarization', 'keyword-extraction')


def models() -> list:
    """The models of the fleet as the console's model rows: each once, with the workers that can serve it and
    which of them has it loaded. A model is "installed" where a wrapper can call it."""
    out = []
    routes = {(row['wrapper'], row['model']): row for row in registry.model_routes()}
    for m in collate.models():
        serving = [w for w in m['wrappers'] if w.get('selectable')]
        out.append(dict(
            name=m['id'], model_key=m['id'], key=m['id'], hub_id=m.get('model_key'), folder=m.get('model_key'),
            framework=m.get('engine'), engine=m.get('engine'), primary_task=m.get('task'), task=m.get('task'),
            tasks=[m['task']] if m.get('task') else [], pipeline_tag=m.get('task'),
            size_bytes=m.get('weight_bytes'), total_bytes=m.get('weight_bytes'),
            status='installed' if serving else 'unavailable', source='wrapper', on_central=False,
            workers=[w['wrapper'] for w in serving],
            worker_assignments=[dict(worker_id=w['wrapper'], assigned=(w['wrapper'], m['id']) in routes,
                                     pinned=bool(routes.get((w['wrapper'], m['id']), {}).get('pinned')),
                                     loaded=bool(w.get('resident')),
                                     on_worker_drive=bool(w.get('accommodated'))) for w in serving],
            weights=[], media=bool(m.get('task')) and m['task'] not in NOT_MEDIA, _note=None, _pinned=False))
    return out


def calls_raw(limit: int = 100, before: int = None, load: str = None, worker: str = None, model: str = None) -> dict:
    """The call log as the wrappers recorded it, newest first: every row whole, with ``worker`` (whose it is),
    ``id`` (Core's own number for the row, to page by) and ``box_id`` (the row's number on its wrapper)."""
    limit = max(1, min(500, int(limit or 100)))
    where, params = ["log = 'call_log'"], []
    if before is not None:
        where.append('rowid < ?')
        params.append(int(before))
    if worker:
        where.append('wrapper = ?')
        params.append(worker)
    if model:
        where.append("json_extract(row, '$.model_name') = ?")
        params.append(model)
    if load == 'initial':
        where.append("json_extract(row, '$.load_s') IS NOT NULL")
    elif load == 'reused':
        where.append("json_extract(row, '$.request_params.reused_resident') = 1")
    found = sql.rows(f"SELECT rowid AS number, wrapper, row FROM wrapper_log WHERE {' AND '.join(where)} "
                     f"ORDER BY rowid DESC LIMIT ?", (*params, limit + 1))
    more, found = len(found) > limit, found[:limit]
    calls, columns = [], ['id', 'worker', 'box_id']
    for one in found:
        row = json.loads(one['row'])
        calls.append(dict(row, id=one['number'], box_id=row.get('id'), worker=one['wrapper']))
        columns += [name for name in row if name not in columns]
    return dict(calls=calls, columns=columns, count=len(calls), next_before=found[-1]['number'] if more else None,
                path='core.wrapper_log')


# the tables that hold rows of a model, by the tool whose record they are: {the name shown: the wrapper's table}
RECORDS = dict(
    wrapper={'units': 'units_mat', 'feasibility': 'feasibility', 'selections': 'selections'},
    discovery={'units': 'discovery.api_units_v1', 'files': 'discovery.api_unit_files_v1', 'presence': 'discovery.api_unit_presence_v1',
               'placements': 'discovery.api_placements_v1', 'representations': 'discovery.api_unit_representations_v1'})
RECORDS_PAGE = 100


def variation_of(unit: dict, served: dict, wrapper: str) -> dict:
    """One variation of a model folder as the console's quant: what loads, its bytes, and what its wrapper says of
    loading it."""
    said, about = json.loads(unit['row']), json.loads(served['row']) if served else {}
    whole = unit['variation'] in ('', '*')
    placed = (about.get('options') or {}).get('placed') or {}
    fits = None if not about else 'fits' if about.get('possible') else 'exceeds'
    home = next((place for place in said.get('locations') or [] if place.get('source')), None)
    return dict(
        file='dir' if whole else unit['variation'], label='full folder' if whole else None,
        quant=None if whole else (quant_token(unit['variation']) or None), selected=bool(about.get('resident')),
        bytes=about.get('weight_bytes') or unit['bytes'], shards=None, feasibility=fits,
        feasibility_why=about.get('possible_reason') or about.get('offer_reason'),
        facts=dict(arch=unit['arch'], block_count=said.get('layers'), moe_is_moe=bool(said.get('expert_count')),
                   moe_experts=said.get('expert_count'), moe_experts_per_token=said.get('expert_used_count'), ctx_train=unit['ctx_train']),
        origin_worker=wrapper, sources=['discovery', *(['wrapper'] if about else [])],
        path=f"{home['root'].rstrip('/')}/{unit['model_key']}" + ('' if whole else f"/{unit['variation']}") if home else None,
        allocations=[dict(variant='native', allocation=placed['reads_as'], status='fits', reason=None, context_tokens=placed.get('ctx'),
                          gpu_bytes=round((placed.get('gib') or {}).get('gpu', 0) * 2 ** 30) or None,
                          ram_bytes=round((placed.get('gib') or {}).get('ram', 0) * 2 ** 30) or None)] if placed.get('reads_as') else [])


def folders(whole: bool = True, key: str = None) -> list:
    """Every model folder a wrapper's Discovery has recorded, once, with its variations (``whole``: each as the
    console's quant; else only their names, for the list's first paint)."""
    served = {(row['wrapper'], row['id']): row for row in sql.rows("SELECT wrapper, id, row FROM models")}
    out = {}
    for unit in sql.rows("SELECT wrapper, model_key, variation, bytes, engine, task, source_role, arch, ctx_train, row FROM units"
                         + (' WHERE model_key = ?' if key else '') + " ORDER BY model_key, variation, wrapper", (key,) if key else ()):
        mine = served.get((unit['wrapper'], f"{unit['model_key']}::{unit['variation']}"))
        about = json.loads(mine['row']) if mine else {}
        said = json.loads(unit['row'])
        home = next((place for place in said.get('locations') or [] if place.get('source')), None)
        one = out.setdefault(unit['model_key'], dict(
            key=unit['model_key'], name=unit['model_key'].rsplit('/', 1)[-1], hub_id=about.get('hub_id') or unit['model_key'],
            engine=about.get('owned_by') or unit['engine'], primary_task=about.get('primary_task') or unit['task'],
            architecture=unit['arch'], context_length=unit['ctx_train'], location='local', origin_worker=unit['wrapper'],
            source='wrapper' if mine else 'discovery', runner=None, license=None, has_tools=None, has_reasoning=None,
            has_vision=(about.get('primary_task') or unit['task']) == 'image-text-to-text',
            discovery_dir=f"{home['root'].rstrip('/')}/{unit['model_key']}" if home else None, model_dir=None,
            discovery_state='recorded', selected_quant=None, feasibility_best='none', quants=[], _bytes=[], _seen=set()))
        if unit['variation'] in one['_seen']:           # the same variation on another wrapper: it is there too
            continue
        one['_seen'].add(unit['variation'])
        quant = variation_of(unit, mine, unit['wrapper'])
        one['quants'].append(quant if whole else dict(file=quant['file'], quant=quant['quant']))
        one['_bytes'].append(quant['bytes'] or 0)
        if mine and one['source'] == 'discovery':
            one['source'] = 'wrapper'
        if quant['feasibility'] == 'fits' or (quant['feasibility'] == 'exceeds' and one['feasibility_best'] == 'none'):
            one['feasibility_best'] = quant['feasibility']
        if quant['selected']:
            one['selected_quant'] = quant['quant'] or quant['file']
    for one in out.values():
        sizes = one.pop('_bytes')
        one.pop('_seen')
        one.update(quant_count=len(one['quants']), size_range=[min(sizes), max(sizes)] if sizes else None)
    return list(out.values())


def folders_list(whole: bool = True) -> dict:
    return dict(object='list', generated_at=time.time(), sources=dict(discovery="each wrapper's Discovery record"),
                data=folders(whole))


def holder(key: str) -> dict:
    """The saved connection of a wrapper that has a model folder (one that can be asked now, when there is one).
    LookupError when no wrapper's record has it."""
    have = [row['wrapper'] for row in sql.rows("SELECT DISTINCT wrapper FROM units WHERE model_key = ?", (key,))]
    if not have:
        raise LookupError(f'no wrapper has recorded a model folder {key}')
    reachable = {row['name'] for row in registry.status() if row['reachable']}
    return registry.get(next((name for name in have if name in reachable), have[0]))


def folder(key: str) -> dict:
    """One model folder whole: its variations, its files (as its Discovery recorded them, read from its wrapper
    now), and the tables of the wrapper and of its Discovery that hold rows of it, each with how many."""
    found = folders(True, key)
    if not found:
        raise LookupError(f'no wrapper has recorded a model folder {key}')
    wrapper, one = holder(key), found[0]
    files, counted = [], dict(wrapper=[], discovery=[])
    try:
        for row in modelsdb.wrapper_rows(wrapper, RECORDS['discovery']['files'], key, None, 200, 0)[1]:
            files.append(dict(file=row.get('rel_path'), role=row.get('role'), weight_class=None, bytes=row.get('bytes'),
                              quant=quant_token(row.get('rel_path') or '') or None, format=None, source='discovery'))
        for group, tables in RECORDS.items():
            for name, table in tables.items():
                _, rows, more = modelsdb.wrapper_rows(wrapper, table, key, None, 200, 0)
                if rows:
                    counted[group].append(dict(table=name, total=len(rows) if not more else 200))
    except modelsdb.Unanswered as exc:              # its wrapper does not answer now: the folder is shown without them
        one['discovery_state'] = str(exc)
    return dict(one, files=files, records=counted, projectors=[],
                sources=dict(wrapper=f"{wrapper['name']}: its own tables", discovery=f"{wrapper['name']}: its Discovery's export"))


def records(key: str, named: str, offset: int = 0) -> dict:
    """A page of one table's rows of a model folder (``named``: wrapper.units, discovery.files ...)."""
    group, _, name = named.partition('.')
    if name not in RECORDS.get(group, {}):
        raise ValueError(f'{named} is not one of the tables of a model folder')
    try:
        _, rows, more = modelsdb.wrapper_rows(holder(key), RECORDS[group][name], key, None, RECORDS_PAGE, max(0, int(offset or 0)))
    except modelsdb.Unanswered as exc:
        raise LookupError(str(exc)) from None
    start = max(0, int(offset or 0))
    return dict(table=name, offset=start, total=start + len(rows) + (1 if more else 0),
                rows=[dict(row, _rowid=start + at) for at, row in enumerate(rows)])


def schema() -> dict:
    """The placements and the knobs as the function library defines them: the console draws its placement choices
    from this, under the names the wrappers themselves say a model would be placed by."""
    return dict(canonical=True, placements=[dict(PLACEMENT_TERMS[key], key=key) for key in PLACEMENTS],
                knobs=KNOB_SCHEMA, renames=dict(PLACEMENT_RENAMES))


def saved() -> dict:
    """The saved connections, for the console's "saved wrappers": each by its name, its address and whether it is
    switched on. Never a key."""
    return dict(connections=[dict(name=row['name'], url=row['url'], connected=bool(row['connected']), link=bool(row['link']),
                                  connected_changed_at=row['changed_at']) for row in registry.saved()])


def readiness() -> dict:
    """How this install stands, for the landing page's "Your instance" panel and for a brochure looking for a
    visitor's own Core: its wrappers, how many are reachable, what they advertise and whether anything is loaded."""
    wrappers = registry.status()
    loaded = sql.rows("SELECT count(*) AS n FROM residents r JOIN wrapper_status s ON s.name = r.wrapper WHERE s.reachable = 1")[0]['n']
    advertised = sql.rows("SELECT count(DISTINCT m.id) AS n FROM models m JOIN wrapper_status s ON s.name = m.wrapper WHERE s.reachable = 1")[0]['n']
    return dict(profile='basic', central=dict(version=tool_version(PACKAGE, __file__), auth_mode='open', package=PACKAGE),
                serving=dict(workers_total=len(wrappers), workers_online=sum(1 for w in wrappers if w['reachable']),
                             any_serving=loaded > 0, loaded=loaded),
                storage=dict(model_count=advertised), connect={}, console={})
