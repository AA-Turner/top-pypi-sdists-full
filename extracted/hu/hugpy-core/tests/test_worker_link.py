"""A worker Core cannot reach: its Wrapper holds a link open and Core's own calls to it travel over that link
(operator 2026-11-14: "core is supposed to suggest", "the wrapper can recieve a core delegation")."""
import base64
import json
import threading
import urllib.error
import urllib.request

import pytest
from werkzeug.serving import make_server

from hugpy_core.registry import registrations, transport
from hugpy_core.web import api_access, worker_link


def _http(url, body=None, auth=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Content-Type': 'application/json', **({'Authorization': auth} if auth else {})},
                                 method='POST' if body is not None else 'GET')
    try:
        with urllib.request.urlopen(req, timeout=30) as reply:
            return reply.status, json.load(reply)
    except urllib.error.HTTPError as exc:
        return exc.code, json.load(exc)


def test_core_calls_a_linked_worker_over_the_link_it_holds_open(monkeypatch):
    saved = {}

    def upsert(config):
        saved.setdefault(config['name'], {}).update(config)
        return saved[config['name']]
    monkeypatch.setattr(registrations, 'get', saved.get)
    monkeypatch.setattr(registrations, 'upsert', upsert)
    monkeypatch.setattr(registrations, 'is_connected', lambda config: True)
    monkeypatch.setattr(api_access, 'valid_use_authorization', lambda auth: auth == 'Bearer use-key')
    monkeypatch.setattr(worker_link, '_LINKS', {})
    door = worker_link.wrap(lambda environ, start: (start('404 Not Found', []), [b''])[1])
    server = make_server('127.0.0.1', 0, door, threaded=True)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.port}'
    monkeypatch.setenv('HUGPY_CORE_LINK_BASE', base)
    monkeypatch.setenv('HUGPY_SELF_BASE', 'https://core.example')
    try:
        # the installer is open (a new box has no console login) and names this Core's public address
        with urllib.request.urlopen(base + '/fleet-link/install.sh', timeout=10) as reply:
            script = reply.read().decode()
        assert "CENTRAL=https://core.example\n" in script and '--link' in script
        assert _http(base + '/fleet-link/register', {'name': 'a-brain'}, 'Bearer nope')[0] == 401
        status, doc = _http(base + '/fleet-link/register', {'name': 'a-brain'}, 'Bearer use-key')
        assert status == 200
        secret, worker = doc['secret'], saved['a-brain']
        assert worker['url'] == base + '/_link/a-brain' and worker['key'] == secret and worker['link']

        # nobody holds the link: Core's call fails at once, it does not wait for an answer that cannot come
        with pytest.raises(RuntimeError, match='502'):
            transport.request(worker, '/v1/telemetry/state')

        def wrapper_side():
            while True:
                _, got = _http(base + '/fleet-link/a-brain/poll?wait=5', auth='Bearer ' + secret)
                for job in got['jobs']:
                    echo = {'echo': job['method'] + ' ' + job['path'],
                            'body': base64.b64decode(job['body_b64']).decode()}
                    _http(base + '/fleet-link/a-brain/answer', {
                        'id': job['id'], 'status': 200, 'content_type': 'application/json',
                        'body_b64': base64.b64encode(json.dumps(echo).encode()).decode()}, 'Bearer ' + secret)
                if got['jobs']:
                    return
        _http(base + '/fleet-link/a-brain/poll?wait=0', auth='Bearer ' + secret)      # the Wrapper is there
        threading.Thread(target=wrapper_side, daemon=True).start()
        assert transport.request(worker, '/v1/chat/completions?x=1', {'model': 'm'}) == {
            'echo': 'POST /v1/chat/completions?x=1', 'body': '{"model": "m"}'}

        # a streamed answer (raw bytes, X-Hugpy-Status) is piped to the waiting request as it comes
        blob = bytes(range(256)) * 5000

        def streaming_side():
            while True:
                _, got = _http(base + '/fleet-link/a-brain/poll?wait=5', auth='Bearer ' + secret)
                for job in got['jobs']:
                    req = urllib.request.Request(base + f"/fleet-link/a-brain/answer/{job['id']}", data=blob, method='POST',
                                                 headers={'Authorization': 'Bearer ' + secret, 'X-Hugpy-Status': '200',
                                                          'X-Hugpy-Content-Type': 'application/octet-stream',
                                                          'Content-Type': 'application/octet-stream'})
                    urllib.request.urlopen(req, timeout=30).read()
                if got['jobs']:
                    return
        threading.Thread(target=streaming_side, daemon=True).start()
        req = urllib.request.Request(worker['url'] + '/v1/central/file?offer=o&rel=m&offset=0&length=9',
                                     headers={'Authorization': 'Bearer ' + secret})
        with urllib.request.urlopen(req, timeout=30) as reply:
            assert reply.read() == blob and reply.headers['Content-Type'] == 'application/octet-stream'

        # the secret is the link's only credential, on both sides of it
        assert _http(base + '/fleet-link/a-brain/poll?wait=0', auth='Bearer wrong')[0] == 401
        with pytest.raises(RuntimeError, match='401'):
            transport.request({**worker, 'key': 'wrong'}, '/v1/telemetry/state')
    finally:
        server.shutdown()
