"""Connect a wrapper: Core is given its address (and its API key, when Core is not on its host).

Core looks before it saves. The address must be a wrapper that says who it is (its /health: the service, a
status, its name), and its telemetry must open with the key given, because that is what the collector will read.
The connection is saved under the name the wrapper gives itself. A name already saved at another address is
taken over only when that address no longer answers as that name (a host that moved); two hosts cannot share one.

This is what the wrapper's own installer asks for (`hugpy-wrapper system register --core URL`, POST
/api/fleet/workers/connect) and what `hugpy-core connect URL` does.
"""
from ..imports import (
    STATE_PATH,
    WRAPPER_ENDPOINT_FILE,
    WRAPPER_SERVICE,
    WRAPPER_STATUSES,
    http_json,
    read_endpoint,
    urlsplit,
)
from . import registry


class Refused(Exception):
    """A connection Core did not save, and why (``status`` is what its door answers with)."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


def local_wrapper() -> str:
    """The address of this host's own wrapper, from the record its install wrote."""
    url = read_endpoint(WRAPPER_ENDPOINT_FILE).get('url')
    if not url:
        raise Refused(404, f'this host has no wrapper service ({WRAPPER_ENDPOINT_FILE} is not there): give the address of one')
    return url


def origin(url) -> str:
    """``url`` as a wrapper's origin (scheme, host, port), or Refused."""
    if not isinstance(url, str):
        raise Refused(400, 'the wrapper address must be text')
    url = url.strip().rstrip('/')
    try:
        parts = urlsplit(url)
        parts.port
        if (parts.scheme not in ('http', 'https') or not parts.hostname or parts.username is not None
                or parts.password is not None or parts.query or parts.fragment or parts.path
                or any(c.isspace() for c in url) or '\\' in url):
            raise ValueError
    except ValueError:
        raise Refused(400, 'give the wrapper origin, e.g. http://192.168.1.50:15102, with no path or credentials') from None
    return url


def answers_as(url: str, key: str, name: str) -> bool:
    """Whether a wrapper at ``url`` still answers under ``name``."""
    try:
        _, health = http_json(url.rstrip('/') + '/health', bearer=key or None, timeout=5)
    except (OSError, ValueError):
        return False
    return isinstance(health, dict) and str(health.get('worker') or '').strip() == name


def connect(url, key: str = '', by: str = None) -> dict:
    """Look at the wrapper at ``url`` and save its connection. Returns {name, url, state, message[, moved_from]};
    Refused says why not."""
    url = origin(url)
    if not isinstance(key or '', str) or '\r' in (key or '') or '\n' in (key or ''):
        raise Refused(400, 'the wrapper API key must be one line of text')
    key = (key or '').strip()
    try:
        status, health = http_json(url + '/health', bearer=key or None, timeout=10)
        if (not isinstance(health, dict) or health.get('service') != WRAPPER_SERVICE
                or health.get('status') not in WRAPPER_STATUSES or not str(health.get('worker') or '').strip()):
            raise Refused(400, f'{url} is not a hugpy wrapper (its /health does not say so)')
        # /health is open: the key is proved on the read the collector will make
        status, state = http_json(url + STATE_PATH + '?wait=0', bearer=key or None, timeout=10)
    except OSError as exc:
        raise Refused(400, f'Core could not reach {url}: {exc}. Check the address, the port and the network '
                           f'between them; a wrapper Core cannot reach connects out instead '
                           f'(sudo hugpy-wrapper system register --core CORE --link)') from None
    if status in (401, 403):
        raise Refused(400, 'the wrapper API key is missing or was refused (on its host: sudo hugpy-wrapper system key)')
    if status != 200 or not isinstance(state, dict) or not state.get('store_id'):
        raise Refused(400, f'{url} did not give its telemetry (HTTP {status}): is it a hugpy-wrapper 0.2 or later?')
    name = health['worker'].strip()
    existing = registry.get(name)
    moved_from = None
    if existing and not existing['link'] and existing['url'].rstrip('/') != url:
        if answers_as(existing['url'], existing['key'], name):
            raise Refused(409, f"another host answers as {name} at {existing['url']}: two wrappers cannot share a "
                               f"name. Give this one its own (sudo hugpy-wrapper system set worker NAME)")
        moved_from = existing['url']          # the saved address no longer is this wrapper: it moved
    registry.save(name, url, key, link=False, by=by)
    return dict(name=name, url=url, state='registered', **({'moved_from': moved_from} if moved_from else {}),
                message=(f'Connected at its new address (was {moved_from}). ' if moved_from else 'Connected. ')
                        + 'What it publishes appears as the collector reads it.')
