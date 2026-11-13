"""Which arm requests Core answers itself and which it forwards to a standalone service."""
import json

from flask import Flask

from hugpy_core.web import arm_proxy


def test_an_embedded_arm_is_not_proxied_even_for_a_route_it_lacks(tmp_path, monkeypatch):
    (tmp_path / 'video.json').write_text(json.dumps({
        'arm': 'video', 'upstream': 'http://127.0.0.1:9', 'categories': ['video', 'oracle'], 'ui': '/video/'}))
    monkeypatch.setenv('HUGPY_ARMS_DIR', str(tmp_path))
    core = Flask(__name__)

    def below(environ, start_response):
        start_response('404 NOT FOUND', [('Content-Type', 'application/json')])
        return [b'{"error": "no such route"}']

    def status(app, path):
        seen = []
        b''.join(app({'PATH_INFO': path, 'REQUEST_METHOD': 'GET', 'QUERY_STRING': '', 'wsgi.url_scheme': 'http',
                      'SERVER_NAME': 'core', 'SERVER_PORT': '7020'}, lambda line, headers: seen.append(line)))
        return int(seen[0].split()[0])

    assert status(arm_proxy.wrap(below, core, embedded_arms={'video'}), '/api/oracle/does-not-exist') == 404
    # the same descriptor with the arm NOT in this process: Core forwards, and says so when nothing answers
    assert status(arm_proxy.wrap(below, core), '/api/oracle/does-not-exist') == 502
