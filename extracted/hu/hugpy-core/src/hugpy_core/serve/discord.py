"""Connect the Core console to an installed Discord arm."""

from ..imports import http_json, urlencode
from .arm_schema import installed_arms


def upstream():
    arm = installed_arms().get('discord')
    return arm['upstream'].rstrip('/') if arm and 'discord' in arm['categories'] else None


def discord_status(door, args, query):
    address = upstream()
    if not address:
        return 200, dict(state='unconfigured')
    try:
        status, response = http_json(address + '/api/discord/bindings', timeout=2)
    except OSError:
        return 200, dict(state='unavailable')
    ready = status == 200 and isinstance(response, dict) and isinstance(response.get('bindings'), list)
    return 200, dict(state='ready' if ready else 'unavailable')


def discord_api(path):
    def forward(door, args, query):
        address = upstream()
        if not address:
            return 503, dict(error='The Discord bridge is not installed on this host')
        item_id = args.get('item_id')
        if item_id is not None and (not item_id.isascii() or not item_id.replace('-', '').isalnum()):
            return 404, dict(error='Invalid Discord record ID')
        url = address + '/api/discord/' + path.format(**args)
        if query:
            url += '?' + urlencode(query)
        body = door.read_json() if door.command == 'POST' else None
        try:
            status, response = http_json(url, body, method=door.command, timeout=10)
        except OSError:
            return 503, dict(error='The Discord bridge is unavailable')
        return status, response if response is not None else dict(error='Invalid reply from the Discord bridge')

    return forward
