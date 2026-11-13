"""Connecting a Wrapper: Core reads the worker itself, saves the connection and switches it on."""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from flask import Flask

from hugpy_core.web import worker_connect


def test_a_reachable_wrapper_is_saved_and_switched_on(monkeypatch):
    health = {'service': 'hugpy-wrapper', 'status': 'ok', 'worker': 'box7'}

    class Wrapper(BaseHTTPRequestHandler):
        def do_GET(self):
            raw = json.dumps(health if self.path == '/health' else {'store_id': 's1'}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def log_message(self, *args):
            pass

    server = HTTPServer(('127.0.0.1', 0), Wrapper)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_port}'

    saved = {}

    class Registrations:
        get = staticmethod(saved.get)
        is_connected = staticmethod(lambda config: bool(config) and config.get('connected', True) is not False)

        @staticmethod
        def upsert(config):
            saved[config['name']] = {**saved.get(config['name'], {}), **config}
            return saved[config['name']]

        @staticmethod
        def set_connected(name, connected):
            saved[name]['connected'] = connected

    monkeypatch.setattr(worker_connect, 'registrations', Registrations)
    app = Flask(__name__)
    app.add_url_rule('/connect', view_func=worker_connect.connect_wrapper, methods=['POST'])
    client = app.test_client()
    try:
        reply = client.post('/connect', json={'url': url + '/', 'key': ''})
        assert reply.status_code == 200 and reply.get_json()['name'] == 'box7'
        assert saved['box7']['url'] == url

        saved['box7']['connected'] = False                       # the operator disconnected it; it is connected again
        assert client.post('/connect', json={'url': url}).status_code == 200
        assert saved['box7']['connected'] is True

        assert client.post('/connect', json={'url': 'http://127.0.0.1:1'}).status_code == 400      # nothing there

        saved['box7']['url'] = 'http://127.0.0.1:1'              # the worker's address changed: the old one is silent
        moved = client.post('/connect', json={'url': url})
        assert moved.status_code == 200 and moved.get_json()['moved_from'] == 'http://127.0.0.1:1'
        assert saved['box7']['url'] == url
        twin = url.replace('127.0.0.1', 'localhost')             # a second machine under a name that still answers
        refused = client.post('/connect', json={'url': twin})
        assert refused.status_code == 409 and saved['box7']['url'] == url

        health['service'] = 'something-else'
        saved.clear()
        assert client.post('/connect', json={'url': url}).status_code == 400 and not saved
        assert client.post('/connect', json={'url': url}, headers={'Origin': 'https://evil.example'}).status_code == 403
    finally:
        server.shutdown()
