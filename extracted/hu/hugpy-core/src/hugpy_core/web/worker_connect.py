"""Connect installed Wrappers from the existing operator console."""
import json
import urllib.error
import urllib.parse
import urllib.request

from flask import jsonify, request

from hugpy_core.registry import registrations


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # A worker key belongs only to the supplied endpoint.


def connect_wrapper():
    # This follows the console's access policy, like its box/settings controls.
    # Machine registration at POST /fleet/workers keeps its separate key gate.
    origin = request.headers.get('Origin')
    if origin and origin.rstrip('/') != request.host_url.rstrip('/'):
        return jsonify(error='Connect a worker from this Core console.'), 403
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify(error='Expected a JSON object.'), 400
    url, key = body.get('url'), body.get('key', '')
    if not isinstance(url, str) or not isinstance(key, str):
        return jsonify(error='Wrapper endpoint and API key must be text.'), 400
    url, key = url.strip().rstrip('/'), key.strip()
    try:
        parsed = urllib.parse.urlsplit(url)
        parsed.port
        if (parsed.scheme not in ('http', 'https') or not parsed.hostname
                or parsed.username is not None or parsed.password is not None
                or parsed.query or parsed.fragment or parsed.path
                or any(c.isspace() for c in url) or '\\' in url):
            raise ValueError
        if '\r' in key or '\n' in key:
            raise ValueError
    except ValueError:
        return jsonify(error='Enter the Wrapper origin, e.g. http://192.168.1.50:52017, with no path or credentials.'), 400
    headers = {'Accept': 'application/json'}
    if key:
        headers['Authorization'] = 'Bearer ' + key
    opener = urllib.request.build_opener(NoRedirect)
    def read(path):
        req = urllib.request.Request(url + path, headers=headers)
        with opener.open(req, timeout=10) as response:
            return json.load(response)
    try:
        health = read('/health')
        if (not isinstance(health, dict) or health.get('service') not in ('hugpy-wrapper', 'hugpy-wrapper-sql')
                or health.get('status') != 'ok' or not isinstance(health.get('worker'), str)
                or not health['worker'].strip()):
            return jsonify(error='This endpoint is not a healthy Hugpy Wrapper.'), 400
        # /health is public. Verify the credentials used by intake before saving.
        state = read('/v1/telemetry/state?wait=0')
        if not isinstance(state, dict) or not state.get('store_id'):
            return jsonify(error='The Wrapper did not provide its telemetry store identity.'), 400
    except urllib.error.HTTPError as exc:
        message = ('Wrapper API key is missing or was refused.' if exc.code in (401, 403)
                   else 'Wrapper returned HTTP ' + str(exc.code) + '. Check the endpoint.')
        return jsonify(error=message), 400
    except (OSError, ValueError):
        return jsonify(error='Core could not read Wrapper telemetry. Check the address, port and network access.'), 400
    name = health['worker'].strip()
    existing = registrations.get(name)
    if existing and existing['url'].rstrip('/') != url:
        return jsonify(error='A different endpoint is already registered as ' + name + '. Remove that worker before replacing it.'), 409
    registrations.upsert({'name': name, 'url': url, 'key': key})
    return jsonify(name=name, url=url, state='registered',
                   message='Connected. Its model inventory and telemetry will appear as intake refreshes.'), 200


def saved_connections():
    """GET /fleet/workers/saved: every saved Wrapper connection (never its key),
    with whether it is connected — the console's Reconnect list."""
    from hugpy_core.registry.registrations import is_connected
    rows = [{"name": c.get("name"), "url": c.get("url"), "connected": is_connected(c),
             "connected_changed_at": c.get("connected_changed_at")}
            for c in registrations.all()]
    return jsonify(connections=rows), 200
