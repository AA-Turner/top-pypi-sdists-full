"""hugpy-core: the coordinator of the wrappers of many hosts.

    hugpy-core                      how Core stands: its door, and every wrapper it has
    hugpy-core serve                Core itself: its door and the collector (the service runs this)
    hugpy-core connect URL|local    connect a wrapper (--key KEY when it is on another host); local: this host's own
    hugpy-core wrappers             the saved connections and how each stands
    hugpy-core disconnect NAME      stop reading a wrapper (its address and key stay saved); reconnect NAME; forget NAME
    hugpy-core fleet                every wrapper now: cards, memory, what is loaded, drives
    hugpy-core compute              the console's worker, model and resource view, and its controls
    hugpy-core calls                the calls of every wrapper, newest first (--wrapper, --model, --state, -n)
    hugpy-core call REQUEST_ID      one call whole, with its stages
    hugpy-core models               the models of the fleet and the wrappers that serve each (--wrapper, --search, --task)
    hugpy-core grading              every model's grade as it stands: graded, passed, what it is asked next (--wrapper, --model)
    hugpy-core queries              the grading table: what a model of each task is asked, in tiers (--suite)
    hugpy-core schedule MODEL       one model's queries in the order they are asked, each with its verdict
    hugpy-core test-fire WRAPPER    a round of grading calls: every model's next query that was not performed
                                    (--complete: every such query; --hot-only, --cold-only; --model M: only these)
    hugpy-core rounds               the rounds on record; round ID: one as it stands; stop ID: stop it
    hugpy-core settings | set KEY VALUE
    hugpy-core system install | status | uninstall | key      Core as a service of the host

Everything but serve, settings and system asks the Core that runs on this host, through its door, with the key
of this host's own programs (a file every account of the host can read).
"""
from ..imports import (
    PACKAGE,
    SERVICE_UNIT,
    SETTING_KEYS,
    argparse,
    compute_arguments,
    compute_model_rows,
    fmt_bytes,
    health_record,
    http_json,
    json,
    os,
    quote,
    read_secret,
    run_compute,
    sys,
    time,
    urlencode,
)
from .. import settings
from ..serve import serve, version
from ..wrappers import Refused, local_wrapper


def stamp(at) -> str:
    """A time a wrapper or Core recorded, as this host's clock reads it."""
    return time.strftime('%m-%d %H:%M:%S', time.localtime(at)) if at else '-'


def running(url: str) -> None:
    """Core answers at ``url``, or the command ends saying what does (or that nothing does)."""
    found = health_record(url, timeout=5)
    if found and found.get('package') == PACKAGE:
        return
    if found is None:
        raise SystemExit(f'hugpy-core: nothing answers at {url}. Start it: `hugpy-core serve`, or as the service of this '
                         f'host: sudo hugpy-core system install (then: systemctl status {SERVICE_UNIT})')
    raise SystemExit(f"hugpy-core: {url} is answered by {found.get('package') or found.get('service') or 'another program'}, "
                     f"not by hugpy-core. Another address for this one: hugpy-core set port N")


def key():
    """The key this account asks Core with: the key of this host's own programs, else Core's API key where this
    account may read it (root, the service account)."""
    return read_secret(settings.local_key_file()) or read_secret(settings.api_key_file())


def asked(path: str, body=None, method: str = None, timeout: float = 60):
    """One exchange with the Core of this host -> the document it answered. An answer that is a refusal ends the
    command with what Core said."""
    url = settings.url()
    try:
        status, document = http_json(url + path, body, method=method, bearer=key(), timeout=timeout)
    except OSError:
        running(url)
        raise
    if status == 401 and key() is None:
        running(url)
        raise SystemExit(f'hugpy-core: the key of this host\'s programs is not there to read ({settings.local_key_file()}): '
                         f'it is made when Core starts (hugpy-core serve) or is installed (sudo hugpy-core system install)')
    if not 200 <= status < 300 or not isinstance(document, (list, dict)):
        if not (isinstance(document, dict) and document.get('error')):
            running(url)
        reason = document.get('error') if isinstance(document, dict) else None
        raise SystemExit(f"hugpy-core: {reason or f'HTTP {status} from {url}{path}'}")
    return document


def show_wrappers(found: list) -> None:
    if not found:
        print('no wrapper is connected. Connect one:  hugpy-core connect URL [--key KEY]   (this host\'s own: hugpy-core connect local)')
        return
    print(f"{'wrapper':<16} {'state':<13} {'version':<10} {'address':<34} last read")
    for row in found:
        state = ('disconnected' if not row['connected'] else 'unreachable' if not row['reachable']
                 else row.get('status') or 'reachable')
        print(f"{row['name']:<16} {state:<13} {row.get('version') or '-':<10} "
              f"{('link (it connects out)' if row['link'] else row['url']):<34} {stamp(row.get('read_at'))}")
        for reason in row.get('reasons') or []:
            print(f'{"":<16} it says: {reason}')
        if row.get('error') and row['connected']:
            print(f'{"":<16} not read since {stamp(row.get("error_at"))}: {row["error"]}')


def show_fleet(found: list) -> None:
    for row in found:
        state = 'disconnected' if not row['connected'] else 'unreachable' if not row['reachable'] else row.get('status') or 'reachable'
        print(f"{row['name']}  ({state}; hugpy-wrapper {row.get('version') or '?'}; {row['models']} models, "
              f"{row['selectable'] or 0} callable; {row['calls']} calls, last {stamp(row.get('last_call_at'))})")
        for card in row['cards']:
            print(f"  card {card['device']}  {card['name']}: {fmt_bytes(card['free'])} free of {fmt_bytes(card['total'])}")
        if row['host']:
            host = row['host']
            print(f"  memory  {fmt_bytes(host['mem_available'])} available of {fmt_bytes(host['mem_total'])}; "
                  f"swap {fmt_bytes(host['swap_free'])} free of {fmt_bytes(host['swap_total'])}")
        for resident in row['residents']:
            where = ' + '.join(part for part in (
                f"{fmt_bytes(resident['vram_bytes'])} card" if resident.get('vram_bytes') else '',
                f"{fmt_bytes(resident['ram_bytes'])} memory" if resident.get('ram_bytes') else '') if part) or 'no memory read yet'
            doing = 'loading' if resident.get('loading') else 'busy' if resident.get('busy') else 'idle'
            print(f"  loaded  {resident['model']}  ({resident.get('engine')}; {where}; {doing}; last used {stamp(resident.get('last_used'))})")
        if not row['residents'] and row['reachable']:
            print('  loaded  nothing')
        for drive in row['drives']:
            print(f"  drive   {drive['role']:<10} {drive['path']}: {fmt_bytes(drive['free'])} free of {fmt_bytes(drive['total'])}, "
                  f"{drive['models']} models")
    if not found:
        show_wrappers(found)


def show_compute(document: dict, query: str) -> None:
    """Show the worker tabs and their model state with the same identities as the web console."""
    if 'worker' in document:
        tabs = [(document['worker'], document['models'])]
    else:
        tabs = [(worker, compute_model_rows(document['models'], worker, query)) for worker in document['workers']]
        disconnected = [row['name'] for row in document['saved_workers'] if row['connected'] is False]
        if disconnected:
            print('Saved, disconnected: ' + ', '.join(disconnected))
    if not tabs:
        print('No connected workers. Use hugpy-core connect URL to add one.')
    for worker, models in tabs:
        print(f"{worker['name']}  {worker['status']}  ·  wildcard {'on' if worker.get('wildcard') else 'off'}")
        print(f"  VRAM {fmt_bytes(worker.get('vram_used'))} / {fmt_bytes(worker.get('vram_total'))}"
              f"  ·  RAM available {fmt_bytes(worker.get('free_ram'))} / {fmt_bytes(worker.get('ram_total'))}"
              f"  ·  swap free {fmt_bytes(worker.get('swap_free'))} / {fmt_bytes(worker.get('swap_total'))}")
        for card in worker.get('gpus') or []:
            print(f"  GPU {card.get('index', '—')}  {card.get('name') or '—'}  "
                  f"{fmt_bytes(card.get('memory_free'))} free / {fmt_bytes(card.get('memory_total'))}")
        cpu, storage = worker.get('cpu') or {}, worker.get('storage') or {}
        queue = (worker.get('resources') or {}).get('queue') or {}
        print(f"  CPU {cpu.get('physical_cores', '—')} physical cores  ·  disk {fmt_bytes(storage.get('disk_free'))} free"
              f"  ·  queue {queue.get('waiting', '—')} waiting, {queue.get('turn', '—')} running")
        for row in models:
            flags = [label for field, label in (('offered', 'offered'), ('local', 'on drive'), ('assigned', 'allocated'),
                     ('pinned', 'pinned'), ('resident', 'loaded'), ('loading', 'loading'), ('blocked', 'blocked'),
                     ('static', 'static'), ('static_pending', 'static change pending')) if row[field]]
            print(f"  {row['model_key']}  {fmt_bytes(row['bytes'])}  {' · '.join(flags)}")
        if not models:
            print('  No matching models.')


def show_calls(found: list) -> None:
    if not found:
        print('no call is on record for that')
        return
    print(f"{'received':<15} {'wrapper':<12} {'state':<10} {'tokens in/out':<14} {'seconds':>8}  model")
    for row in found:
        took = f"{row['responded_at'] - row['received_at']:.1f}" if row.get('responded_at') and row.get('received_at') else '-'
        tokens = f"{row.get('prompt_tokens') if row.get('prompt_tokens') is not None else '-'}/{row.get('completion_tokens') if row.get('completion_tokens') is not None else '-'}"
        print(f"{stamp(row.get('received_at')):<15} {row['wrapper']:<12} {str(row.get('state') or '-'):<10} {tokens:<14} {took:>8}  "
              f"{row.get('model') or '-'}   [{row.get('request_id')}]"
              + (f"  graded: {row['grading_query']}" if row.get('grading_query') else ''))


def show_models(found: list) -> None:
    if not found:
        print('no model matches (only wrappers that can be asked now are counted: hugpy-core wrappers)')
        return
    print(f"{'size':>9}  {'task':<28} {'served by':<22} model")
    for row in found:
        served = ', '.join(w['wrapper'] + ('*' if w.get('resident') else '') + ('' if w.get('selectable') else ' (not callable)')
                           for w in row['wrappers'])
        print(f"{fmt_bytes(row.get('weight_bytes') or 0):>9}  {str(row.get('task') or '-'):<28} {served:<22} {row['id']}")
    print(f"{len(found)} model{'' if len(found) == 1 else 's'} (* loaded now)")


def show_standing(found: list) -> None:
    if not found:
        print('no model has a schedule: the grading table has no query for the tasks of the models served (hugpy-core queries)')
        return
    print(f"{'graded':>8} {'passed':>7}  {'asked next':<28} {'wrapper':<10} model")
    for row in found:
        doing = row['next'] or (f"{row['asking']} being asked" if row['asking'] else 'nothing: all graded')
        print(f"{row['graded']:>4}/{row['of']:<3} {row['passed']:>7}  {doing:<28} {row['wrapper']:<10} {row['model']}")
    print(f"{len(found)} model{'' if len(found) == 1 else 's'}; {sum(1 for row in found if row['graded'] == row['of'])} graded whole, "
          f"{sum(1 for row in found if not row['graded'])} not graded at all")


def show_queries(found: list) -> None:
    suite = None
    for row in found:
        if row['suite'] != suite:
            suite = row['suite']
            print(f"{suite}  (asked of the models that serve {row['task']}" + (f" on {row['engine']}" if row['engine'] else '') + ')')
        print(f"  {row['id']:<30} {row['asks'][:74]}")
        print(f"  {'':<30} right when: {row['rule']}" + ('   [changed here]' if row['changed_at'] else ''))
    print(f"{len(found)} quer{'y' if len(found) == 1 else 'ies'}")


def show_schedule(found: list) -> None:
    if not found:
        print('no such model has a schedule (hugpy-core grading lists the ones that do)')
        return
    for row in found:
        mark = {True: 'passed', False: 'FAILED', None: 'unchecked'}[row['passed']] if row['standing'] == 'graded' else row['standing']
        print(f"{row['query']:<30} {mark:<10} " + (repr(row['shown'])[:60] if row['standing'] == 'graded' else '')
              + (f"\n{'':<42}{row['why'][:150]}" if row['passed'] is False and row['why'] else ''))


def show_rounds(found: list) -> None:
    if not found:
        print('no round is on record. Ask one:  hugpy-core test-fire WRAPPER')
        return
    print(f"{'started':<15} {'round':<16} {'kind':<10} {'state':<12} {'calls':>11}  wrappers")
    for row in found:
        state = 'running' if row['running'] else (row['ended_why'] or 'interrupted').split(':')[0]
        print(f"{stamp(row['started_at']):<15} {row['id']:<16} {row['kind']:<10} {state:<12} "
              f"{row['answered']:>4}/{row['planned']:<6} {', '.join(row['wrappers'])}"
              + (f"   ({row['skipped']} models left out)" if row['skipped'] else '') + (f"   ({row['refused']} turned away)" if row['refused'] else ''))


def show_round(doc: dict) -> None:
    state = 'running' if doc['running'] else (doc['ended_why'] or 'interrupted')
    answered = [call for call in doc['calls'] if call['state'] == 'done']
    print(f"{doc['id']}  ({doc['kind']} of {', '.join(doc['wrappers'])}; {state}; started {stamp(doc['started_at'])})")
    print(f"  {len(doc['plan'])} calls planned, {doc['sent']} sent, {doc['flying']} held by a wrapper now, {len(answered)} answered: "
          f"{sum(1 for call in answered if call['passed'] is True)} passed, {sum(1 for call in answered if call['passed'] is False)} failed their check")
    for call in reversed(doc['calls']):
        mark = {True: 'passed', False: 'FAILED', None: 'unchecked'}[call['passed']] if call['state'] == 'done' else call['state'] or 'waiting'
        print(f"  {stamp(call['received_at']):<15} {mark:<10} {str(call['query']):<30} {call['model']}"
              + (f"\n{'':<28}{call['why'][:150]}" if call['why'] and call['passed'] is not True else ''))
    for one in doc['refused']:
        print(f"  {stamp(one.get('at')):<15} {'turned away':<10} {one['query']:<30} {one['model']}\n{'':<28}{str(one.get('error'))[:150]}")
    reasons = {}
    for one in doc['skipped']:
        reasons.setdefault(one['reason'], []).append(one['model'])
    for reason, models in reasons.items():
        print(f"  left out, {len(models)}: {reason}")


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv[:1] == ['system']:
        from ..system import main as system_main
        return system_main(argv[1:], given=os.environ.get('HUGPY_DATA_DIR'))
    parser = argparse.ArgumentParser(prog='hugpy-core', description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command')
    p = sub.add_parser('serve', help='Core itself: its door and the collector (the service runs this)')
    p.add_argument('--host')
    p.add_argument('--port', type=int)
    p = sub.add_parser('connect', help='connect a wrapper by its address (local: this host\'s own wrapper)')
    p.add_argument('url', metavar='URL|local')
    p.add_argument('--key', default='', help="the wrapper's API key, when it is on another host (there: sudo hugpy-wrapper system key)")
    sub.add_parser('wrappers', help='the saved connections and how each stands')
    for name, text in (('disconnect', 'stop reading a wrapper; its address and key stay saved'),
                       ('reconnect', 'read a disconnected wrapper again'), ('forget', 'drop a saved connection (its calls and loads stay)')):
        sub.add_parser(name, help=text).add_argument('name')
    sub.add_parser('fleet', help='every wrapper now: cards, memory, what is loaded, drives')
    p = sub.add_parser('compute', help='the Compute console: workers, serving variations, settings and controls')
    compute_arguments(p)
    p.add_argument('--json', action='store_true', default=argparse.SUPPRESS, help='print the Compute response as JSON')
    p = sub.add_parser('calls', help='the calls of every wrapper, newest first')
    p.add_argument('--wrapper')
    p.add_argument('--model', help='any part of the model\'s name')
    p.add_argument('--state', help='pending, running, done, failed or cancelled')
    p.add_argument('--graded', action='store_true', help='only the calls made with a grading marker')
    p.add_argument('-n', '--limit', type=int, default=20)
    sub.add_parser('call', help='one call whole, with its stages').add_argument('request_id')
    p = sub.add_parser('models', help='the models of the fleet and the wrappers that serve each')
    p.add_argument('--wrapper')
    p.add_argument('--search', help='any part of the model\'s name')
    p.add_argument('--task')
    p = sub.add_parser('grading', help="every model's grade as it stands: graded, passed, what it is asked next")
    p.add_argument('--wrapper')
    p.add_argument('--model', help="the model's whole name")
    sub.add_parser('queries', help='the grading table: what a model of each task is asked, and how it is checked').add_argument('--suite')
    p = sub.add_parser('schedule', help="one model's queries in the order they are asked, each with its verdict")
    p.add_argument('model')
    p.add_argument('--wrapper')
    p = sub.add_parser('test-fire', help="a round of grading calls of one wrapper: every model's next query that was not performed")
    p.add_argument('wrapper')
    p.add_argument('--complete', action='store_true', help='every query that was not performed, not only the next of each model')
    p.add_argument('--hot-only', action='store_true', help="only models already on the worker's own drives")
    p.add_argument('--cold-only', action='store_true', help='only models that must first be copied there')
    p.add_argument('--model', action='append', help='only this model (may be given again)')
    sub.add_parser('rounds', help='the rounds of grading calls on record, newest first')
    sub.add_parser('round', help='one round as it stands, with every call of it').add_argument('round')
    sub.add_parser('stop', help='stop a round: no more of it is sent, what its wrappers hold of it is cancelled').add_argument('round')
    sub.add_parser('settings', help='every setting, its value and where it comes from')
    p = sub.add_parser('set', help='save one setting in the database (an empty VALUE: its default again)')
    p.add_argument('key')
    p.add_argument('value')
    sub.add_parser('system', help='install | status | uninstall | key: the service (hugpy-core system --help)')
    sub.add_parser('version')
    parser.add_argument('--json', action='store_true', help='the answer as Core gave it')
    args = parser.parse_args(argv)
    command = args.command

    if command == 'version':
        print(version())
        return 0
    if command == 'serve':
        if settings.is_client():
            raise SystemExit(f'hugpy-core: on this host Core is the service {SERVICE_UNIT}, and its folder ({settings.home()}) '
                             f'is the service account\'s own: sudo hugpy-core system status')
        serve(args.host, args.port)
        return 0
    if command == 'settings':
        print(f'database: {settings.database()}   .env: {os.path.join("~", ".hugpy", ".env")}' if not settings.is_client() else
              f'Core is the service {SERVICE_UNIT} on this host; its saved settings are in its own folder. From this '
              f'account: its address, then the environment, then the defaults')
        for key, row in settings.resolve().items():
            print(f"  {key:<8} {row['value'] if row['value'] is not None else '(none)'}   [{row['source']}]")
        return 0
    if command == 'set':
        if settings.is_client():
            raise SystemExit(f'hugpy-core: the settings of this host\'s Core are the service\'s: sudo hugpy-core system set {args.key} VALUE')
        if args.key not in SETTING_KEYS:
            raise SystemExit(f"hugpy-core: {args.key} is not one of: {', '.join(SETTING_KEYS)}")
        changed = settings.save({args.key: settings.typed(args.value)})
        print(f"{args.key}: " + ('unchanged' if not changed else 'its default again' if settings.typed(args.value) is None else f'saved as {settings.typed(args.value)!r}')
              + f'  ({settings.database()}; a running Core takes it at its next start)')
        return 0

    def out(document, show):
        print(json.dumps(document, indent=1)) if args.json else show(document)
        return 0

    if command == 'compute':
        try:
            document = run_compute(asked, args)
        except ValueError as exc:
            parser.error(str(exc))
        if args.operation == 'view':
            return out(document, lambda doc: show_compute(doc, args.query))
        print(json.dumps(document, indent=2, ensure_ascii=False))
        return 0

    if command in (None, 'wrappers'):
        found = asked('/v1/wrappers')
        if command is None and not args.json:
            health = health_record(settings.url()) or {}
            print(f"hugpy-core {health.get('version')} at {settings.url()}: {health.get('status')}"
                  + ''.join(f'; {reason}' for reason in health.get('reasons') or []))
        return out(found, lambda doc: show_wrappers(doc['wrappers']))
    if command == 'connect':
        try:
            url = local_wrapper() if args.url == 'local' else args.url
        except Refused as exc:
            raise SystemExit(f'hugpy-core: {exc}') from None
        return out(asked('/api/fleet/workers/connect', dict(url=url, key=args.key)),
                   lambda doc: print(f"{doc['name']}: {doc['message']}  ({doc['url']})"))
    if command in ('disconnect', 'reconnect'):
        return out(asked(f'/v1/wrappers/{quote(args.name, safe="")}/{command}', {}),
                   lambda doc: print(f"{doc['name']}: {doc['message']}"))
    if command == 'forget':
        return out(asked(f'/v1/wrappers/{quote(args.name, safe="")}', method='DELETE'),
                   lambda doc: print(f"{doc['name']}: {doc['message']}"))
    if command == 'fleet':
        return out(asked('/v1/fleet'), lambda doc: show_fleet(doc['wrappers']))
    if command == 'calls':
        query = {key: value for key, value in (('wrapper', args.wrapper), ('model', args.model), ('state', args.state),
                                               ('graded', '1' if args.graded else ''), ('limit', args.limit)) if value}
        return out(asked('/v1/calls?' + urlencode(query)), lambda doc: show_calls(doc['calls']))
    if command == 'call':
        return out(asked(f'/v1/calls/{quote(args.request_id, safe="")}'), lambda doc: print(json.dumps(doc, indent=1)))
    if command == 'models':
        query = {key: value for key, value in (('wrapper', args.wrapper), ('search', args.search), ('task', args.task)) if value}
        return out(asked('/v1/models' + ('?' + urlencode(query) if query else '')), lambda doc: show_models(doc['data']))
    if command == 'grading':
        query = {key: value for key, value in (('wrapper', args.wrapper), ('model', args.model)) if value}
        return out(asked('/v1/grading' + ('?' + urlencode(query) if query else '')), lambda doc: show_standing(doc['models']))
    if command == 'queries':
        return out(asked('/v1/grading/queries' + ('?' + urlencode(dict(suite=args.suite)) if args.suite else '')),
                   lambda doc: show_queries(doc['queries']))
    if command == 'schedule':
        query = {key: value for key, value in (('model', args.model), ('wrapper', args.wrapper)) if value}
        return out(asked('/v1/grading/schedule?' + urlencode(query)), lambda doc: show_schedule(doc['schedule']))
    if command == 'test-fire':
        if args.hot_only and args.cold_only:
            raise SystemExit('hugpy-core: --hot-only and --cold-only leave nothing to ask')
        started = asked('/v1/rounds', dict(kind='test-fire', wrappers=[args.wrapper], models=args.model, complete=args.complete,
                                           hot=not args.cold_only, cold=not args.hot_only))
        return out(started, lambda doc: (show_round(doc), print(f"follow it:  hugpy-core round {doc['id']}     stop it:  hugpy-core stop {doc['id']}")))
    if command == 'rounds':
        return out(asked('/v1/rounds'), lambda doc: show_rounds(doc['rounds']))
    if command == 'round':
        return out(asked(f'/v1/rounds/{quote(args.round, safe="")}'), show_round)
    if command == 'stop':
        return out(asked(f'/v1/rounds/{quote(args.round, safe="")}/stop', {}),
                   lambda doc: print(f"{doc['id']}: " + (f"stopped; its wrappers were holding {doc['cancelled']} of its calls, which are being cancelled"
                                                        if doc['was_running'] else 'it was not running')))
    parser.print_help()
    return 2
