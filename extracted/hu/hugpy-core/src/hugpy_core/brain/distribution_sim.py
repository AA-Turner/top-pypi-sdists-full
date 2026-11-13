"""Pure fleet experiments over frozen wrapper prices; never dispatch or evict."""
from __future__ import annotations

import copy
import math
from collections import Counter

from hugpy_core.lifted.sizing import rank_candidates, host_fit

MODES = ('gpu-only', 'explicit', 'max-gpu', 'max-ram', 'ram-only')
from hugpy_core.intake import schema as _schema  # noqa: E402 — either verdict vocabulary
GOALS = ('quality', 'fast')
TOLERANCES = ('', 'fast', 'slow', 'slowest', 'low-quality')
PLACEMENTS = ('gpu-only', 'moe', 'ram-only', 'max-ram', 'max-gpu', '4bit', 'alternate-quants', 'disk-mmap')


def number(value):
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0 else None


def validate(scenario):
    if not isinstance(scenario, dict):
        raise ValueError('A simulation configuration is required')
    scenario = copy.deepcopy(scenario)
    if set(scenario) - {'workers','models','groups','baseline','order','compare_starts','paging'}:
        raise ValueError('Unsupported simulation configuration field')
    workers, models = scenario.get('workers'), scenario.get('models')
    if not isinstance(workers, list) or not 1 <= len(workers) <= 32:
        raise ValueError('Select 1–32 workers')
    if not isinstance(models, list) or not 1 <= len(models) <= 512 or any(not isinstance(k, str) or not k for k in models):
        raise ValueError('Select 1–512 models')
    if len(set(models)) != len(models):
        raise ValueError('Each model must appear once')
    ids = []
    for worker in workers:
        if not isinstance(worker, dict) or not isinstance(worker.get('id'), str) or not worker['id']:
            raise ValueError('Worker IDs must be explicit')
        if set(worker) - {'id','auto_goal','tolerance','allowed_placements'}:
            raise ValueError('Worker resource snapshots cannot be supplied by a simulation request')
        if worker.get('auto_goal', 'quality') not in GOALS or worker.get('tolerance', '') not in TOLERANCES:
            raise ValueError('Invalid worker Auto goal or tolerance')
        allowed = worker.get('allowed_placements')
        if allowed is not None and (not isinstance(allowed, list) or any(not isinstance(p, str) or p not in PLACEMENTS for p in allowed) or len(set(allowed)) != len(allowed)):
            raise ValueError('Explicit tolerance choices must be a unique list of supported placements')
        ids.append(worker['id'])
    if len(set(ids)) != len(ids):
        raise ValueError('Each worker must appear once')
    if scenario.get('baseline', 'budget') not in ('budget', 'available'):
        raise ValueError('Invalid resource baseline')
    if scenario.get('order', 'largest') not in ('largest', 'smallest', 'selected'):
        raise ValueError('Invalid load order')
    for flag in ('compare_starts', 'paging'):
        if flag in scenario and not isinstance(scenario[flag], bool):
            raise ValueError('Simulation switches must be boolean')
    groups, grouped = scenario.get('groups', []), set()
    if not isinstance(groups, list) or len(groups) > 64:
        raise ValueError('Use at most 64 model groups')
    names = set()
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get('name'), str) or not group['name'].strip():
            raise ValueError('Each group needs a name')
        if set(group) - {'name','models','knobs'}:
            raise ValueError('Unsupported model group field')
        if len(group['name']) > 120 or group['name'].strip() in names:
            raise ValueError('Group names must be unique and at most 120 characters')
        names.add(group['name'].strip())
        members = group.get('models', [])
        if not isinstance(members, list) or any(not isinstance(k, str) or k not in models for k in members):
            raise ValueError('Group members must be selected models')
        if len(set(members)) != len(members) or grouped.intersection(members):
            raise ValueError('A model may belong to only one simulation group')
        grouped.update(members)
        knobs = group.get('knobs') or {}
        if not isinstance(knobs, dict) or set(knobs) - {'alloc_mode', 'ctx_pct', 'bnb_4bit','cpu_floor_cores'}:
            raise ValueError('Unsupported simulation group knob')
        if knobs.get('alloc_mode', 'auto') not in ('auto', *MODES):
            raise ValueError('Invalid group placement')
        if knobs.get('ctx_pct') is not None and (number(knobs['ctx_pct']) is None or not 1 <= knobs['ctx_pct'] <= 100):
            raise ValueError('Context target must be 1–100 percent')
        if knobs.get('bnb_4bit') is not None and not isinstance(knobs['bnb_4bit'], bool):
            raise ValueError('4-bit choice must be boolean')
        cores = knobs.get('cpu_floor_cores')
        if cores is not None and (number(cores) is None or not 1 <= cores <= 1024 or int(cores) != cores):
            raise ValueError('CPU reservation must be a whole number of physical cores')
    if scenario.get('compare_starts') and len(models) ** 2 * len(workers) > 5_000_000:
        raise ValueError('This comparison exceeds 5 million placement steps; select fewer models or workers')
    return scenario


def tolerance_allows(mode, bnb, variant, disk, tolerance, allowed=None):
    # Explicit choices replace the preset floor, while artifact approvals still apply.
    if allowed is not None:
        placement = 'moe' if mode == 'explicit' else mode
        return (placement in allowed and (not bnb or '4bit' in allowed)
                and (not variant or 'alternate-quants' in allowed)
                and (not disk or 'disk-mmap' in allowed))
    # Mirror front_door._floor_allows; only eligibility, never goal ranking.
    if not tolerance:
        return True
    if disk and tolerance not in ('slowest', 'low-quality'):
        return False
    if bnb or variant:
        return tolerance == 'low-quality'
    if mode == 'gpu-only':
        return True
    if mode == 'explicit':
        return tolerance != 'fast'
    return tolerance in ('slowest', 'low-quality')


def candidates(model, worker, knobs):
    pair = next((p for p in model.get('workers', []) if p['worker_id'] == worker['id']), {})
    verdicts = pair.get('verdicts') or []
    settings = {**(pair.get('user_settings') or {}), **{k:v for k,v in knobs.items() if v is not None}}
    if settings.get('blocked'):
        return [], ['ineligible: blocked for this model and worker']
    default = settings.get('gguf_file') or (pair.get('plan') or {}).get('default_variant')
    default = default or next((v['file'] for v in verdicts if (v.get('inputs') or {}).get('elected')), None)
    default = default or (verdicts[0]['file'] if verdicts else None)
    choices, unknown = [], [] if verdicts else ['Resource requirements are unpriced for this worker']
    for verdict in verdicts:
        inputs = verdict.get('inputs') or {}
        admission = inputs.get('feasibility') or {}
        if admission.get('admissible') is False:
            unknown.append('ineligible: ' + (admission.get('why') or 'Model is not admitted'))
            continue
        variant = verdict['file'] != default
        # Another quant is eligible only if the published Auto ladder approves it.
        ladder = next(((v.get('auto') or {}).get('ladder') for v in verdicts if v['file'] == default), None) or []
        if variant and not any(r.get('variant') == verdict['file'] for r in ladder):
            continue
        memory = verdict.get('memory') or {}
        if not memory:
            unknown.append('Memory requirements are unpriced')
        for bnb, cells in ((False, memory), (True, memory.get('bnb_4bit') or {})):
            if 'bnb_4bit' in knobs and knobs['bnb_4bit'] is not None and bnb != knobs['bnb_4bit']:
                continue
            if bnb and settings.get('bnb_4bit') is False:
                continue
            if bnb and settings.get('bnb_4bit') is not True and not any(r.get('mode') == 'bnb_4bit' or r.get('bnb4') for r in ladder):
                continue
            if settings.get('bnb_4bit') is True and not bnb:
                continue
            for mode in MODES:
                cell = _schema.cell(cells, mode)
                if not isinstance(cell, dict) or cell.get('supported') is False or cell.get('applicable') is False:
                    continue
                pinned = _schema.canonical(settings.get('alloc_mode'))
                if pinned not in (None, 'auto', 'automatic', _schema.canonical(mode)):
                    continue
                if mode == 'explicit' and (not verdict.get('moe_offered') or settings.get('moe') is False):
                    continue
                disk = bool(cell.get('disk_mmap'))
                if not tolerance_allows(mode, bnb, variant, disk, worker.get('tolerance', ''), worker.get('allowed_placements')):
                    continue
                gpu, ram = number(cell.get('gpu_bytes')), number(cell.get('ram_bytes'))
                if gpu is None or ram is None:
                    unknown.append(f"{verdict['file']} / {mode}: exact GPU/RAM split is unpriced")
                    continue
                # A new context target uses the wrapper's stored KV ticks, not a new model-size estimate.
                ctx = cell.get('ctx')
                if knobs.get('ctx_pct') is not None and cell.get('kv_bytes'):
                    kv = inputs.get('kv_cost') or {}
                    tick = (kv.get('ticks') or {}).get(str(round(knobs['ctx_pct']))) or {}
                    new = number(tick.get(settings.get('kv_cache_type') or 'f16'))
                    old = number(cell.get('kv_bytes'))
                    if new is None or not old:
                        unknown.append(f"{verdict['file']} / {mode}: requested context has no stored KV price")
                        continue
                    share = number(cell.get('kv_gpu_bytes'))
                    if share is None:
                        share = old if cell.get('kv_device') == 'gpu' else 0 if cell.get('kv_device') == 'ram' else None
                    if share is None:
                        unknown.append('KV placement is unknown')
                        continue
                    gpu = max(0, gpu + (new - old) * share / old)
                    ram = max(0, ram + (new - old) * (1 - share / old))
                    ctx = tick.get('ctx')
                rung = next((r for r in ladder if r.get('mode') == mode and not r.get('variant')), {})
                mapped = min(ram, number(cell.get('ram_file_bytes')) or 0)
                anon = number(cell.get('ram_anon_bytes'))
                if knobs.get('ctx_pct') is not None or anon is None:
                    anon = ram - mapped
                cpu = number(rung.get('cores_required'))
                if cpu is None and mode != 'gpu-only':
                    cpu = number(settings.get('cpu_floor_cores'))
                if mode != 'gpu-only' and cpu is None:
                    unknown.append(f"{verdict['file']} / {mode}: CPU admission requirement is unpriced")
                    continue
                choices.append({'file':verdict['file'], 'mode':mode, 'bnb_4bit':bnb,
                    'gpu':int(gpu), 'ram':int(ram), 'anon':int(anon), 'mapped':int(mapped),
                    'cpu':int(cpu or 0), 'ctx':ctx, 'disk_mmap':disk,
                    'ram_file_reservation':cell.get('ram_file_reservation'),
                    'q':int(variant) + int(bnb), 'T':number(rung.get('T')), 'R':number(rung.get('R')),
                    'ladder_index':len(choices), 'source':cell.get('source') or 'wrapper memory verdict'})
    return rank_candidates(choices, worker.get('auto_goal', 'quality')), list(dict.fromkeys(unknown))


def fit(candidate, room, paging=False):
    for resource in ('gpu', 'ram', 'cpu'):
        if room.get(resource) is None and candidate[resource] > 0:
            return None
    if candidate['gpu'] > (room.get('gpu') or 0) or candidate['cpu'] > (room.get('cpu') or 0):
        return False
    if not paging:
        return candidate['ram'] <= (room.get('ram') or 0)
    if candidate['disk_mmap'] and number(candidate.get('ram_file_reservation')) is None:
        return None
    result, _ = host_fit({'ram':candidate['ram'], 'ram_anon':candidate['anon'],
                         'ram_file':candidate['mapped'], 'disk_mmap':candidate['disk_mmap'],
                         'ram_file_reservation':candidate.get('ram_file_reservation') or 0},
                        room.get('ram'), room.get('swap'))
    return result


def reserve(candidate, room, paging):
    room = dict(room)
    ram = candidate['ram']
    streamed = swapped = 0
    if paging:
        swapped = max(0, candidate['anon'] - (room.get('ram') or 0))
        streamed = max(0, ram - (room.get('ram') or 0) - swapped)
        ram = min(ram, room.get('ram') or 0)
        if room.get('swap') is not None:
            room['swap'] = max(0, room['swap'] - swapped)
    for resource, amount in (('gpu',candidate['gpu']), ('ram',ram), ('cpu',candidate['cpu'])):
        if room.get(resource) is not None:
            room[resource] = max(0, room[resource] - amount)
    return room, swapped, streamed


def simulate(snapshot, config):
    config = validate(config)
    workers = [{**snapshot['workers'][w['id']], **w} for w in config['workers']]
    models = {k:snapshot['models'][k] for k in config['models']}
    groups = {k:g for g in config.get('groups', []) for k in g['models']}
    priced = {(k,w['id']):candidates(m,w,(groups.get(k) or {}).get('knobs') or {}) for k,m in models.items() for w in workers}
    capacity = {w['id']:dict(w.get(config.get('baseline','budget')) or {}) for w in workers}
    order = list(models)
    sizes = {k:max((c['gpu']+c['ram'] for w in workers for c in priced[k,w['id']][0]), default=-1) for k in order}
    if config.get('order','largest') != 'selected':
        order.sort(key=lambda k: (sizes[k] if config.get('order') == 'smallest' else -sizes[k], k))
    starts = order if config.get('compare_starts') else [order[0]]
    frequencies = {k:Counter() for k in order}
    trials, best = [], None
    for first in starts:
        sequence = [first, *(k for k in order if k != first)]
        room = copy.deepcopy(capacity)
        steps = []
        counts = Counter()
        quality_cost = 0
        for k in sequence:
            options, explanations, has_unknown = [], [], False
            for w in workers:
                wid = w['id']
                choices, unknown = priced[k,wid]
                chosen = next((c for c in choices if fit(c,room[wid],config.get('paging',False)) is True), None)
                uncertain = any(fit(c,room[wid],config.get('paging',False)) is None for c in choices)
                unknown_price = any(not note.startswith('ineligible:') for note in unknown)
                has_unknown |= unknown_price or uncertain
                if chosen:
                    # Best packing among policy-approved choices preserves larger workers.
                    after, swap, stream = reserve(chosen,room[wid],config.get('paging',False))
                    waste = sum((after.get(r) or 0)/(capacity[wid].get(r) or 1) for r in ('gpu','ram'))
                    phase = {'gpu-only':0,'explicit':1,'max-gpu':1,'max-ram':1,'ram-only':2}[chosen['mode']]
                    options.append((chosen['q'],phase,waste,wid,chosen,after,swap,stream))
                explanations.append({'worker_id':wid,'state':'candidate' if chosen else 'unknown' if unknown_price or uncertain else 'no-fit',
                                     'reason':None if chosen else '; '.join(unknown[:2]) or ('Worker budget or paging reservation is unknown' if uncertain else 'No eligible priced placement' if not choices else 'Remaining resources are insufficient')})
            if options:
                _,_,_,wid,c,after,swap,stream = min(options,key=lambda row:row[:4])
                before = room[wid]
                room[wid] = after
                quality_cost += c['q']
                counts['projected'] += 1
                frequencies[k][wid] += 1
                steps.append({'model_key':k,'group':(groups.get(k) or {}).get('name'), 'state':'projected',
                              'worker_id':wid,'placement':c,'before':before,'after':after,
                              'swap_bytes':swap,'streamed_bytes':stream,'alternatives':explanations})
            else:
                state = 'unknown' if has_unknown else 'no-fit'
                counts[state] += 1
                frequencies[k][state] += 1
                steps.append({'model_key':k,'group':(groups.get(k) or {}).get('name'), 'state':state,'alternatives':explanations})
        trial = {'first_model':first, 'projected':counts['projected'], 'unknown':counts['unknown'],
                 'no_fit':counts['no-fit'],'representation_changes':quality_cost,'remaining':room}
        trials.append(trial)
        score = (-counts['projected'],quality_cost,counts['unknown'],first)
        if best is None or score < best[0]:
            best = (score,{**trial,'steps':steps})
    return {'snapshot':snapshot['meta'], 'configuration':config, 'trials':trials, 'best_trial':best[1],
            'model_statistics':[{'model_key':k,'routes':dict(frequencies[k]),'trials':len(trials)} for k in order],
            'capacities':capacity, 'workers':[{'id':w['id'],'name':w.get('name') or w['id']} for w in workers],
            'assumptions':['Sequential co-resident reservations; no eviction or actual loading.',
                           'Worker Auto goals rank their stored candidates; best packing chooses a worker.',
                           'Unpriced memory splits or CPU admission remain unknown.',
                           'Timing and context prices are used only when reported by the wrapper.',
                           'A declared CPU floor reserves cores; it does not certify decode speed or bandwidth.',
                           'The recommendation is the best observed order, not a proof of global optimality.']}
