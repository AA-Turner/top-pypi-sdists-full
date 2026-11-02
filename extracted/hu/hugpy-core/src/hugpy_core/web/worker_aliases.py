"""Compatibility for old worker clients; Fleet owns the only registered routes.

An internal rewrite preserves methods, bodies and response contracts for old
clients, including POST requests that must not be redirected by the browser.
"""
from __future__ import annotations


class WorkerAliases:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        for old, new in (('/api/llm/workers', '/api/fleet/workers'),
                         ('/llm/workers', '/fleet/workers')):
            if path == old or path.startswith(old + '/'):
                environ = dict(environ)
                environ['PATH_INFO'] = new + path[len(old):]
                environ['hugpy.legacy_worker_path'] = path
                def deprecated(status, headers, exc_info=None):
                    return start_response(status, headers + [('Deprecation', 'true'),
                        ('Link', '</api/fleet/workers>; rel="successor-version"')], exc_info)
                return self.app(environ, deprecated)
        return self.app(environ, start_response)
