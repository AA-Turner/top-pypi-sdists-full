"""Addresses that carry an id in the path reach the handler that takes it as an argument."""
from hugpy_core.web.worker_aliases import WorkerAliases


def test_published_lease_and_cancel_addresses_reach_their_handlers():
    seen = []

    def below(environ, start_response):
        seen.append((environ['PATH_INFO'], environ.get('QUERY_STRING', '')))
        start_response('200 OK', [])
        return [b'']

    app = WorkerAliases(below)

    def call(path, query=''):
        b''.join(app({'PATH_INFO': path, 'QUERY_STRING': query, 'REQUEST_METHOD': 'POST'}, lambda *args: None))
        return seen[-1]

    assert call('/api/llm/sessions/ha-12/lease') == ('/api/llm/sessions/lease', 'session_id=ha-12')
    assert call('/api/llm/sessions/ha-12/lease', 'state=active') == ('/api/llm/sessions/lease',
                                                                     'state=active&session_id=ha-12')
    assert call('/api/llm/chat/cancel/v1-abc') == ('/api/llm/chat/cancel', 'request_id=v1-abc')
    assert call('/api/llm/jobs/v1-abc/cancel') == ('/api/llm/chat/cancel', 'request_id=v1-abc')
    # the forms the handlers serve directly are left alone
    assert call('/api/llm/sessions/lease') == ('/api/llm/sessions/lease', '')
    assert call('/api/llm/queue') == ('/api/llm/queue', '')
