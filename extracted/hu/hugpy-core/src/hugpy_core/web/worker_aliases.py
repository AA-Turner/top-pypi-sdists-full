"""Compatibility for old worker clients; Fleet owns the only registered routes.

An internal rewrite preserves methods, bodies and response contracts for old
clients, including POST requests that must not be redirected by the browser.
"""
from __future__ import annotations
import re
from urllib.parse import quote

# Addresses that carried an id in the path until their handlers took it as a keyword argument.
# Published clients (hugpy-agent's session signals and fleet TUI, hugpy-terminal's gateway) still
# call these forms; each is answered by the handler it always meant.
PATH_IDS = (
    (re.compile(r"/api/llm/sessions/(?P<id>[^/]+)/lease/?"), "/api/llm/sessions/lease", "session_id"),
    (re.compile(r"/api/llm/chat/cancel/(?P<id>[^/]+)/?"), "/api/llm/chat/cancel", "request_id"),
    (re.compile(r"/api/llm/jobs/(?P<id>[^/]+)/cancel/?"), "/api/llm/chat/cancel", "request_id"),
)


class WorkerAliases:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        for pattern, target, name in PATH_IDS:
            found = pattern.fullmatch(path)
            if found:
                query = environ.get('QUERY_STRING', '')
                environ = dict(environ, PATH_INFO=target,
                               QUERY_STRING=(query + '&' if query else '') + name + '=' + quote(found['id'], safe=''))
                return self.app(environ, start_response)
        for old, new in (('/api/llm/workers', '/api/fleet/workers'),):
            if path == old or path.startswith(old + '/'):
                environ = dict(environ)
                environ['PATH_INFO'] = new + path[len(old):]
                environ['hugpy.legacy_worker_path'] = path
                def deprecated(status, headers, exc_info=None):
                    return start_response(status, headers + [('Deprecation', 'true'),
                        ('Link', '</api/fleet/workers>; rel="successor-version"')], exc_info)
                return self.app(environ, deprecated)
        return self.app(environ, start_response)
