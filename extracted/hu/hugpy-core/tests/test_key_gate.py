"""Who needs an API key: the console's switch, and the key holder's door onto control routes."""
import json

import pytest

from hugpy_core.lifted.key_auth import KeyAuth
from hugpy_core.web import api_access, ui


class Settings:
    """The two statements the gate uses on Core's settings table."""

    def __init__(self, **rows):
        self.rows = dict(rows)

    def read(self, sql, params=()):
        return [{'value': self.rows[params[0]]}] if params and params[0] in self.rows else []

    def write(self, sql, params=()):
        if params:
            self.rows[params[0]] = params[1]


@pytest.fixture
def gate(monkeypatch):
    for name in ('T_KEY', 'T_REQUIRE', 'T_NETS', 'T_PROXIES'):
        monkeypatch.delenv(name, raising=False)

    def install(**saved):
        store = Settings(**saved)
        monkeypatch.setattr(api_access.routing, 'STORE', store)
        monkeypatch.setattr(api_access.routing, 'KEYS', KeyAuth(store, 'T_KEY', 'T_REQUIRE', 'T_NETS', 'T_PROXIES'))
        return store
    return install


def test_the_switch_means_everybody_and_a_named_mode_survives_a_restart(gate, monkeypatch):
    gate()
    assert api_access.keys_require_set(require=True) == {'require_key': True, 'mode': 'always'}
    assert api_access.keys_require_set(require=False) == {'require_key': False, 'mode': 'never'}
    assert api_access.keys_require_set(mode='sometimes')[1] == 400
    assert api_access.keys_require_set(mode='outside')['mode'] == 'outside'     # only when asked for by name

    monkeypatch.delenv('T_REQUIRE')                 # a restart: only what was saved remains
    api_access.initialize_api_access()
    assert api_access.keys_require_get()['mode'] == 'outside'

    # an install whose switch is on stays on for everybody across an upgrade
    gate(require_key_mode='always')
    monkeypatch.delenv('T_REQUIRE', raising=False)
    api_access.initialize_api_access()
    assert api_access.keys_require_get() == {'require_key': True, 'mode': 'always'}


def test_live_api_is_the_keyed_door_onto_named_control_sections(gate, monkeypatch, tmp_path):
    gate()
    monkeypatch.setenv('T_REQUIRE', 'outside')
    monkeypatch.setenv('T_KEY', 'hpk_box_secret')
    reached = []

    def below(environ, start_response):         # everything under the door: aliases, guest gate, arms, console
        reached.append(environ['PATH_INFO'])
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [b'{}']

    app = ui.LiveApi(below)

    def call(path, peer, **headers):
        environ = {'PATH_INFO': path, 'REQUEST_METHOD': 'GET', 'REMOTE_ADDR': peer, 'SCRIPT_NAME': '',
                   **{'HTTP_' + name.upper(): value for name, value in headers.items()}}
        status = []
        body = b''.join(app(environ, lambda line, _headers: status.append(int(line.split()[0]))))
        return status[0], json.loads(body or b'{}')

    assert call('/live-api/llm/workers', '127.0.0.1')[0] == 200        # this box needs no key
    assert reached[-1] == '/api/llm/workers'                           # and goes on as the /api request
    assert call('/live-api/llm/workers', '203.0.113.9')[0] == 401      # the internet does
    assert call('/live-api/llm/workers', '203.0.113.9', authorization='Bearer hpk_box_secret')[0] == 200
    assert call('/live-api/keys', '127.0.0.1')[0] == 404               # not a key holder's section, for anyone

    # fleet and agent are a use key's only in part; the rest of each is the operator's
    monkeypatch.setattr(api_access.routing.KEYS, 'scope_of',
                        lambda key: {'hpk_box_secret': 'admin', 'hpk_use': 'use'}.get(key))
    use, admin = {'authorization': 'Bearer hpk_use'}, {'authorization': 'Bearer hpk_box_secret'}
    for path in ('/live-api/fleet/workers', '/live-api/fleet/workers/w1/health', '/live-api/fleet/models/m',
                 '/live-api/agent/register'):
        assert call(path, '203.0.113.9', **use)[0] == 200, path
    for path in ('/live-api/fleet/hub/token', '/live-api/fleet/central/drives', '/live-api/agent/nodes'):
        assert call(path, '203.0.113.9', **use)[0] == 403, path
        assert call(path, '203.0.113.9', **admin)[0] == 200, path
    assert reached[-1] == '/api/agent/nodes'

    # behind a front: a forwarded caller is unknown until Core is told the front is its proxy
    assert call('/live-api/llm/workers', '127.0.0.1', x_forwarded_for='192.168.1.50')[0] == 401
    monkeypatch.setenv('T_PROXIES', '127.0.0.1')
    assert call('/live-api/llm/workers', '127.0.0.1', x_forwarded_for='192.168.1.50')[0] == 200
    assert call('/live-api/llm/workers', '127.0.0.1', x_forwarded_for='192.168.1.50, 198.51.100.7')[0] == 401
    # a front location that names no caller (no X-Forwarded-For hop of its own) leaves it unknown
    assert call('/live-api/llm/workers', '127.0.0.1', x_real_ip='192.168.1.50')[0] == 401
    assert call('/live-api/llm/workers', '127.0.0.1', x_forwarded_for='127.0.0.1')[0] == 401

    monkeypatch.setenv('T_REQUIRE', 'always')                          # strict: local callers too
    assert call('/live-api/llm/workers', '127.0.0.1')[0] == 401


def test_principal_names_the_caller_the_gate_would_admit(gate, monkeypatch):
    from flask import Flask
    gate()
    monkeypatch.setenv('T_REQUIRE', 'outside')
    monkeypatch.setenv('T_KEY', 'hpk_box_secret')
    app = Flask(__name__)

    def who(peer, **headers):
        with app.test_request_context('/api/oracle/grants', environ_base={'REMOTE_ADDR': peer}, headers=headers):
            return api_access.principal()

    direct = {'console': False, 'role': None}
    assert who('127.0.0.1') == {'scope': 'admin', 'inside': True, **direct}       # this box manages itself
    assert who('192.168.1.50') == {'scope': 'use', 'inside': True, **direct}      # the LAN may use, not manage
    assert who('203.0.113.9') == {'scope': None, 'inside': False, **direct}
    assert who('203.0.113.9', Authorization='Bearer hpk_box_secret')['scope'] == 'admin'
    # through a front's session gate the caller is the front; what it says of the session rides along
    session = who('127.0.0.1', **{'X-Hugpy-Console-Authenticated': '1', 'X-Hugpy-Role': 'member'})
    assert (session['console'], session['role']) == (True, 'member')
    assert who('203.0.113.9', **{'X-Hugpy-Console-Authenticated': '1', 'X-Hugpy-Role': 'admin'})['console'] is False
