"""One way to ask a wrapper anything: its own API, at its saved address with its key, or over its link.

Every part of Core that needs something of a wrapper (the collector's reads, a call, a transfer) asks here, so a
wrapper that connects out is asked exactly like one Core reaches directly.
"""
from ..imports import (
    ASK_TIMEOUT_S,
    http_json,
    json,
)
from . import link


class Unanswered(RuntimeError):
    """A wrapper did not give the answer that was asked of it: it said no, or said something else."""


def ask(wrapper: dict, path: str, body=None, *, method: str = None, timeout: float = ASK_TIMEOUT_S, headers: dict = None) -> tuple:
    """One JSON exchange with a wrapper -> (status, document); the document is None when the answer was not
    JSON. ``wrapper`` is a saved connection (wrappers/registry.py). OSError when nothing answers at its address;
    LookupError or TimeoutError when its link is down or silent. ``headers`` go with a request to a wrapper Core
    reaches directly; a link carries a request's path and body only."""
    if not path.startswith('/') or path.startswith('//'):
        raise ValueError('a wrapper is asked a path of its own API')
    if not wrapper['link']:
        return http_json(wrapper['url'].rstrip('/') + path, body, method=method, bearer=wrapper['key'] or None,
                         timeout=timeout, headers=headers)
    status, _ctype, raw = link.exchange(wrapper['name'], method or ('GET' if body is None else 'POST'), path,
                                        'application/json', b'' if body is None else json.dumps(body).encode(), timeout)
    try:
        return status, json.loads(raw)
    except ValueError:
        return status, None


def read(wrapper: dict, path: str, timeout: float = ASK_TIMEOUT_S, accept=(200,)) -> dict:
    """The JSON object a wrapper answers a read with. Unanswered when it answers anything else."""
    status, document = ask(wrapper, path, timeout=timeout)
    if status not in accept or not isinstance(document, dict):
        said = document.get('error') if isinstance(document, dict) else None
        raise Unanswered(f"{wrapper['name']} answered {path.split('?')[0]} with HTTP {status}" + (f': {said}' if said else ''))
    return document
