"""Synthetic regressions at the SDK wire boundary, independent of opt-in hooks."""
import json

import httpx
import pytest

from probe.sdk import diagnostics, redaction
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.journal import Journal
from probe.sdk.launch import scrub_argv
from probe.sdk.transport import Transport

SYNTHETIC = 'auditQ7'
VENDOR = 'ghp_' + 'A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8'
RID = '11111111-2222-4333-8444-555555555555'

@pytest.fixture
def wire(monkeypatch, tmp_path):
    requests = []
    def receive(request):
        requests.append(request)
        body = json.loads(request.content) if request.content else {}
        return httpx.Response(200, json={'id': RID, **body})
    monkeypatch.setattr('probe.sdk.transport._device_headers_for', lambda _: {})
    monkeypatch.setattr(Client, '_wrap_run', lambda self, data, **kw: data)
    monkeypatch.setattr('probe.sdk.client._touch_run_lease', lambda *a, **kw: None)
    settings = Settings(base_url='https://audit.invalid', token=VENDOR)
    transport = Transport(settings, client=httpx.Client(base_url=settings.base_url, transport=httpx.MockTransport(receive)), attribution='backfill')
    def client(redact=None):
        return Client(settings=settings, transport=transport, journal=Journal(tmp_path / 'outbox', context={'base_url': settings.base_url}), async_writes=False, auto_drain=False, redact=redact)
    yield client, transport, requests
    transport.close()

@pytest.mark.parametrize('redact', [None, False, True])
@pytest.mark.parametrize('method', ['create_run', 'create_project_run'])
def test_creation_payload_scrubbed_at_serialized_boundary(wire, redact, method):
    client, _, requests = wire
    getattr(client(redact), method)(RID, 'benign-run', heartbeat=False, config={'accessToken': SYNTHETIC}, metadata={'nested': {'message': VENDOR}})
    body = requests[-1].content.decode()
    assert SYNTHETIC not in body and VENDOR not in body
    assert 'benign-run' in body
    assert requests[-1].headers['Authorization'] == 'Bearer ' + VENDOR


def test_transport_direct_request_scrubs_dict_keys_and_repr(wire):
    _, transport, requests = wire
    class Opaque:
        def __repr__(self): return 'password=' + SYNTHETIC
    transport.post('/v1/runs/x/spans', {VENDOR: {'opaque': Opaque()}})
    assert VENDOR not in requests[-1].content.decode()
    assert SYNTHETIC not in requests[-1].content.decode()


@pytest.mark.parametrize('value', [
    {'message': json.dumps({'accessToken': SYNTHETIC})},
    {'privateKey': SYNTHETIC}, {'passwd': SYNTHETIC}, {'clientSecret': SYNTHETIC},
    {'message': 'Authorization: Bearer ' + SYNTHETIC},
    {'message': 'password="firstpart tailPartQ7"'},
    {'message': 'password="firstpart;tailPartQ7"'},
    {'message': 'password=' + 'a' * 200 + 'a1' * 50},
    {'message': 'https://user:' + SYNTHETIC + '@audit.invalid?token=' + SYNTHETIC},
    {'message': 'https://audit.invalid#access_token=' + SYNTHETIC},
])
def test_recursive_payload_scrubbing_removes_complete_values(value):
    result = json.dumps(redaction.default_scrub(value))
    for marker in (SYNTHETIC, 'tailPartQ7', 'a1' * 50):
        assert marker not in result


def test_diagnostic_extra_and_exception_are_safe_to_upload():
    result = json.dumps(diagnostics.build_report(ValueError('password="firstpart tailPartQ7"'), extra={'nested': {'message': VENDOR}}))
    assert 'tailPartQ7' not in result and VENDOR not in result


def test_transport_scrubber_failure_is_closed(wire, monkeypatch):
    _, transport, requests = wire
    def broken(*a, **kw): raise ValueError('synthetic failure')
    monkeypatch.setattr(redaction, 'default_scrub', broken)
    with pytest.raises(ValueError):
        transport.post('/v1/runs/x/metrics', {'password': SYNTHETIC})
    assert requests == []


@pytest.mark.parametrize('selector_field', ['notes_edit', 'expected_summary_markdown'])
def test_historical_secret_selectors_never_bypass_wire_scrubbing(wire, selector_field):
    from probe.sdk.errors import ConflictError

    make_client, transport, _ = wire
    legacy = 'password=Historical8!value'
    new_text = 'password=Replacement9!value'
    seen = []

    def existing_document(request):
        payload = json.loads(request.content)
        seen.append(payload)
        selector = (payload['notes_edit']['old_text'] if selector_field == 'notes_edit'
                    else payload['expected_summary_markdown'])
        assert selector != legacy
        return httpx.Response(409, json={'detail': 'Document changed; review it again'})

    transport._client._transport = httpx.MockTransport(existing_document)
    body = ({'notes_edit': {'old_text': legacy, 'new_text': new_text}}
            if selector_field == 'notes_edit' else
            {'expected_summary_markdown': legacy, 'summary_markdown': new_text})
    client = make_client(False)
    with pytest.raises(ConflictError):
        client.write('PATCH', '/v1/projects/' + RID, body, strict=True, sync=True)
    assert seen == [redaction.default_scrub(body)]
    assert 'Historical8!value' not in json.dumps(seen)
    assert 'Replacement9!value' not in json.dumps(seen)
    assert not client.journal.pending()


def test_benign_training_identifiers_remain_intact(wire):
    _, transport, requests = wire
    original = {'eos_token': '</s>', 'bos_token': '<s>', 'max_tokens': 2048,
        'run_id': RID, 'sha': 'a123456789abcdef' * 4,
        'path': '/Users/synthetic/project/train.py',
        'label': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN',
        'loss': 0.45, 'nested': ['plain prose', 5]}
    transport.post('/v1/runs/x/metrics', original)
    assert json.loads(requests[-1].content) == original


@pytest.mark.parametrize('argv', [
    ['train.py', '--accessToken', SYNTHETIC],
    ['train.py', '--clientSecret=' + SYNTHETIC],
    ['sh', '-c', 'export PASSWORD=' + SYNTHETIC + '; echo benign'],
    ['train.py', '--message', VENDOR],
])
def test_argv_sensitive_flags_and_inline_shell_values(argv):
    out, changed = scrub_argv(argv)
    assert SYNTHETIC not in json.dumps(out) and VENDOR not in json.dumps(out)
    assert changed


def test_argv_benign_flags_and_paths_preserved():
    args = ['train.py', '--max-tokens', '512', '--eos-token', '</s>', '--dataset', '/Users/synthetic/train.json']
    assert scrub_argv(args) == (args, False)


def test_plain_authentication_words_are_not_credentials():
    prose = 'Basic training uses a bearer of information, with ordinary paths and UUIDs.'
    assert redaction.default_scrub({'message': prose}) == {'message': prose}


@pytest.mark.parametrize('text', [
    'https%3A%2F%2Faudit.invalid%3Ftoken%3DauditQ7',
    'https://[bad?token=auditQ7',
    'password="auditQ7',
    'PASSWORD=firstpart\\ tailPartQ7',
    r'password\u003dauditQ7',
])
def test_encoding_and_malformed_text_never_hide_credential_context(text):
    clean = redaction.default_scrub(text)
    assert SYNTHETIC not in clean and 'tailPartQ7' not in clean


def test_benign_encoded_text_is_preserved():
    text = r'https%3A%2F%2Faudit.invalid%3Fpage%3D2 slash\u0020space'
    assert redaction.default_scrub(text) == text


def test_repeated_boundary_scrubs_preserve_url_and_benign_query():
    once = redaction.default_scrub({'url': 'https://user:auditQ7@audit.invalid?token=auditQ7&page=2'})
    assert 'page=2' in once['url']
    assert redaction.default_scrub(once) == once


def test_ingest_hmac_signs_sanitized_bytes_and_keeps_auth_header(wire):
    import hashlib
    import hmac
    _, transport, requests = wire
    transport.settings.ingest_token = 'synthetic-ingest-auth'
    transport.settings.hmac_secret = 'synthetic-hmac-auth'
    transport.post('/ingest/v1/runs', {'config': {'password': SYNTHETIC}})
    request = requests[-1]
    assert SYNTHETIC.encode() not in request.content
    assert request.headers['Authorization'] == 'Bearer synthetic-ingest-auth'
    expected = hmac.new(b'synthetic-hmac-auth', request.content, hashlib.sha256).hexdigest()
    assert request.headers['X-Signature'] == 'sha256=' + expected


def test_opaque_attachment_grant_remains_usable(wire):
    client, _, requests = wire
    client().attach_current_credential('install-synthetic', grant='opaque-synthetic-join-grant')
    assert json.loads(requests[-1].content) == {'grant': 'opaque-synthetic-join-grant'}


def test_redacted_dictionary_keys_do_not_overwrite_siblings_or_benign_keys():
    second = 'ghp_' + 'Z9y8X7w6V5u4T3s2R1q0P9o8N7m6L5k4J3i2'
    payload = {VENDOR: {'sample': 'first'}, second: {'sample': 'second'},
               '<redacted:github-token>': {'sample': 'third'}, '<redacted:github-token>:1': {'sample': 'fourth'}}
    clean = redaction.default_scrub(payload)
    assert len(clean) == 4
    assert sorted(item['sample'] for item in clean.values()) == ['first', 'fourth', 'second', 'third']
    assert clean['<redacted:github-token>'] == {'sample': 'third'}
    assert clean['<redacted:github-token>:1'] == {'sample': 'fourth'}
    assert redaction.default_scrub(clean) == clean


@pytest.mark.parametrize('text_blocks', [False, True])
def test_shared_scanner_redacts_secrets_split_across_large_adjacent_fragments(text_blocks):
    from probe.tap_core.secrets import redact_event
    parts = ['padding ' * 10000 + VENDOR[:12], VENDOR[12:25], VENDOR[25:] + ' padding' * 10000]
    payload = [{'type': 'text', 'text': part} for part in parts] if text_blocks else parts
    clean, fired = redact_event(payload)
    texts = [item['text'] for item in clean] if text_blocks else clean
    assert VENDOR not in ''.join(texts)
    assert all(part not in ''.join(texts) for part in [VENDOR[:12], VENDOR[12:25], VENDOR[25:]])
    assert fired
    assert texts[0].startswith('padding ' * 10000)
    assert texts[-1].endswith(' padding' * 10000)


@pytest.mark.parametrize('payload', [
    {'eos_token': 'AbC12345', 'bos_token': 'ZyX98765'},
    '{"eos_token": "AbC12345", "bos_token": "ZyX98765"}',
    'eos_token=AbC12345 bos_token=ZyX98765',
])
def test_shared_token_anchor_preserves_model_vocabulary(payload):
    from probe.tap_core.secrets import redact_event
    assert redact_event(payload)[0] == payload
    assert redaction.default_scrub(payload) == payload


@pytest.mark.parametrize('text', ['password=hunter2', 'password=hunter', 'password="abc"'])
def test_shared_explicit_password_catches_short_values(text):
    from probe.tap_core.secrets import redact
    clean, fired = redact(text)
    assert clean != text and fired
    assert text.split('=', 1)[1].strip('"') not in clean


@pytest.mark.parametrize('text', ['password=${AUDIT_PW}', "password=os.environ['AUDIT_PW']", 'password=/Users/synthetic/project/.env'])
def test_shared_password_references_are_not_credentials(text):
    from probe.tap_core.secrets import redact
    assert redact(text)[0] == text


def test_sdk_and_shared_scrubber_remove_entire_explicit_passphrase():
    text = 'password = correct horse battery staple; loss=0.5'
    clean = redaction.default_scrub(text)
    assert all(word not in clean for word in ('correct', 'horse', 'battery', 'staple'))
    assert 'loss=0.5' in clean


def test_shared_partial_detection_cannot_hide_long_sdk_keyed_value():
    value = 'aB3xY8mN2pQ4rT7v' * 80
    clean = redaction.default_scrub('api_key=' + value)
    assert 'aB3xY8mN2pQ4rT7v' not in clean


def test_previously_redacted_pretty_json_is_unchanged():
    text = '{\n  "password": "<redacted>",\n  "eos_token": "AbC12345"\n}'
    assert redaction.default_scrub(text) == text


# --- code capture (plan 0.5) ----------------------------------------------------
#
# The snapshot's per-file PUT (and the archive path) streamed raw bytes and never
# went through `prepare_upload`, so the content gate never saw them: an untracked
# `.env` and a scratch file holding a `probe_pat_` token were stored
# byte-identical. These drive the REAL `Run.snapshot` against the fake server and
# read every byte that crossed the wire, under both code storages.

CAPTURE_SECRETS = (
    'probe_pat_' + '0123456789abcdef' * 2,
    'hf_' + 'AbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGh',
    'AKIA' + 'Q3ZP7XK2M5N8R4T6',
    'ghp_' + 'A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8',
)


def _wire_bytes(app):
    """Everything the client sent, with gzip bodies (the archive) opened up."""
    import gzip
    import io
    import tarfile

    out = []
    for request in app.requests:
        body = request.content or b''
        out.append(body)
        if body[:2] == b'\x1f\x8b':
            with gzip.open(io.BytesIO(body)) as gz, tarfile.open(fileobj=gz) as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        out.append(tar.extractfile(member).read())
    return out


def _stored_files(app, run_id):
    """name -> stored bytes, whichever storage the snapshot used."""
    import gzip
    import io
    import tarfile

    rows = app.artifacts.get(run_id, [])
    files = {r['name']: app.blobs[r['id']] for r in rows if r.get('kind') == 'code' and r['id'] in app.blobs}
    for row in rows:
        if row.get('kind') == 'code_bytes' and row['id'] in app.blobs:
            with gzip.open(io.BytesIO(app.blobs[row['id']])) as gz, tarfile.open(fileobj=gz) as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        files[member.name] = tar.extractfile(member).read()
    return files


def _secret_tree(root, *, git):
    import subprocess

    def run_git(*args):
        subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)

    root.mkdir()
    (root / 'train.py').write_text("token = tokens[0]\nprint('train')\n")
    (root / 'NOTES.md').write_text('The access token is refreshed hourly; each token costs money.\n')
    if git:
        run_git('init', '-q')
        run_git('config', 'user.email', 't@e.com')
        run_git('config', 'user.name', 't')
        run_git('add', '-A')
        run_git('commit', '-qm', 'init')
        # Untracked and NOT ignored: exactly what went up on prod.
        (root / '.env').write_text('PROBE_TOKEN=' + CAPTURE_SECRETS[0] + '\n')
        (root / 'scratch.py').write_text(''.join(f'K{i} = "{s}"\n' for i, s in enumerate(CAPTURE_SECRETS)))
        return {'.env', 'scratch.py'}
    (root / 'config.yaml').write_text(''.join(f'key{i}: {s}\n' for i, s in enumerate(CAPTURE_SECRETS)))
    return {'config.yaml'}


@pytest.mark.parametrize('git', [True, False], ids=['git', 'no-git'])
@pytest.mark.parametrize('storage', ['artifacts', 'archive'])
def test_code_capture_never_sends_credential_bytes(client, app, tmp_path, monkeypatch, git, storage):
    from probe.sdk import run as run_mod
    from tests.conftest import open_run

    monkeypatch.setenv(run_mod.CODE_STORAGE_ENV, storage)
    root = tmp_path / 'tree'
    secret_files = _secret_tree(root, git=git)
    run = open_run(client, experiment='e', name='r')

    import warnings

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        snap = run.snapshot(cwd=str(root), include_env=False, include_gpu=False)

    leaked = sorted({s for body in _wire_bytes(app) for s in CAPTURE_SECRETS if s.encode() in body})
    assert leaked == [], f'{len(leaked)} credential(s) crossed the wire'
    stored = _stored_files(app, run.id)
    assert set(stored) == {'train.py', 'NOTES.md'}, 'clean files are captured, keyed ones are not'
    for name, data in stored.items():
        assert data == (root / name).read_bytes(), 'captured bytes are exact: never redacted'
    assert snap['code_bytes']['pending_upload'] == 0

    meta = next(a['meta'] for a in app.artifacts[run.id] if a.get('kind') == 'code_snapshot')
    skipped = {s['path']: s['reason'] for s in meta['skipped']}
    assert {p for p, r in skipped.items() if r == 'secret'} == secret_files
    # One warning names the content-detected files, and never a value.
    content_hits = secret_files - {'.env'}
    message = ' '.join(str(w.message) for w in caught if issubclass(w.category, UserWarning))
    assert 'credential' in message
    assert all(name in message for name in content_hits)
    assert not any(secret in message for secret in CAPTURE_SECRETS)


def test_code_capture_of_a_clean_tree_does_not_warn(client, app, tmp_path):
    import warnings

    from tests.conftest import open_run

    root = tmp_path / 'tree'
    root.mkdir()
    (root / 'train.py').write_text("token = tokens[0]\nprint('train')\n")
    run = open_run(client, experiment='e', name='r')
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        snap = run.snapshot(cwd=str(root), include_env=False, include_gpu=False)
    assert snap['code_bytes']['pending_upload'] == 0


# --- the scrub cache (plan (k), shared with 1.3) ----------------------------------


def _scrub_corpus() -> list[str]:
    """Every string constant in the suites that exercise the scrubber, plus every
    line of the scanner and scrubber sources (dense with credential-shaped
    examples, key names and near-misses)."""
    import ast
    import pathlib

    import probe.sdk.redaction as red_mod
    import probe.tap_core.secrets as sec_mod

    here = pathlib.Path(__file__).parent
    found: set[str] = set()
    for name in ("test_sdk_secret_boundaries.py", "test_outbox_redaction.py", "test_artifact_secret_boundary.py"):
        tree = ast.parse((here / name).read_text())
        found.update(n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str))
    for module in (red_mod, sec_mod):
        found.update(pathlib.Path(module.__file__).read_text().splitlines())
    found.update({VENDOR, SYNTHETIC, 'password=' + SYNTHETIC, 'token', 'eos_token', 'hub_token', 'apiKey'})
    return sorted(s for s in found if len(s) <= redaction.SCRUB_CACHE_MAX_CHARS)


def test_cached_scrubs_equal_uncached_on_the_corpus():
    corpus = _scrub_corpus()
    assert len(corpus) > 1000
    assert redaction.enable_scrub_cache()
    redaction.clear_caches()
    for text in corpus:
        expected = redaction._scrub_string(text)
        assert redaction.scrub_string(text) == expected  # the miss
        assert redaction.scrub_string(text) == expected  # the hit
        assert redaction.is_sensitive_key(text) == redaction._is_sensitive_key(text)
        assert redaction.is_sensitive_key(text) == redaction._is_sensitive_key(text)
    info = redaction._scrub_string_cached.cache_info()
    assert info.hits >= len(corpus) and info.currsize <= redaction.SCRUB_CACHE_SIZE


def test_the_scrub_cache_is_bounded_and_skips_long_strings():
    assert redaction.enable_scrub_cache()
    redaction.clear_caches()
    long = 'x' * (redaction.SCRUB_CACHE_MAX_CHARS + 1)
    redaction.scrub_string(long)
    assert redaction._scrub_string_cached.cache_info().currsize == 0
    for i in range(redaction.SCRUB_CACHE_SIZE + 50):
        redaction.scrub_string(f'/d/{i}')
    assert redaction._scrub_string_cached.cache_info().currsize == redaction.SCRUB_CACHE_SIZE


def test_a_cached_answer_is_never_a_raw_credential():
    assert redaction.enable_scrub_cache()
    redaction.clear_caches()
    for _ in range(3):
        assert VENDOR not in redaction.scrub_string('token ' + VENDOR)
        assert redaction.default_scrub({'password': SYNTHETIC}) == {'password': '<redacted>'}


# The (k) review's MED: the cache was on in ANY process that imported
# `probe.sdk.redaction` (the module name decided), the hosted MCP server and the
# API's W&B import worker included. There one cache spans every tenant: it holds
# raw strings for the process lifetime, and a hit against a miss (0.16 vs 28 us)
# says whether another tenant sent that string. It is off unless a researcher's
# run turns it on.

_HOSTED_MCP = f"""
import probe.mcp.server as server
from probe.sdk import redaction
assert redaction._CACHE_ENABLED is False, "on at import"
server.http_app()
assert redaction._CACHE_ENABLED is False, "on in the hosted app"
assert redaction.enable_scrub_cache() is False, "a run opened in the hosted process turned it on"
for _ in range(3):
    redaction.scrub_string("token {VENDOR}")
    redaction.is_sensitive_key("api_key")
assert redaction._scrub_string_cached.cache_info().currsize == 0
assert redaction._is_sensitive_key_cached.cache_info().currsize == 0
print("cache off")
"""


def test_the_hosted_mcp_server_never_caches_scrubs():
    """A fresh process, as the hosted MCP image runs: import the server, build
    its hosted app, try to turn the cache on, and scrub."""
    import subprocess
    import sys

    proc = subprocess.run([sys.executable, "-c", _HOSTED_MCP], capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0 and proc.stdout.strip() == "cache off", proc.stderr[-2000:]


def test_the_sdk_run_path_turns_the_scrub_cache_on(client, monkeypatch):
    """Negative control for the test above: in a researcher's process,
    `Client.run` (and `probe.init`) turn the cache on and repeats are lookups."""
    from tests.conftest import open_run

    monkeypatch.setattr(redaction, "_CACHE_ENABLED", False)
    monkeypatch.setattr(redaction, "_CACHE_FORBIDDEN", False)
    assert redaction.scrub_string("/data/x.bin") and redaction._scrub_string_cached.cache_info().currsize == 0
    open_run(client, experiment="exp-scrub-cache")
    assert redaction._CACHE_ENABLED is True
    redaction.clear_caches()
    for _ in range(3):
        redaction.scrub_string("/data/x.bin")
    assert redaction._scrub_string_cached.cache_info().hits == 2


def test_a_forbidden_scrub_cache_stays_off_through_a_run(client, monkeypatch):
    from tests.conftest import open_run

    monkeypatch.setattr(redaction, "_CACHE_FORBIDDEN", False)
    redaction.forbid_scrub_cache()
    open_run(client, experiment="exp-scrub-cache-forbidden")
    assert redaction._CACHE_ENABLED is False
