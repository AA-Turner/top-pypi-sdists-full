"""Approved package updates use the registered wrapper API and its own key."""
import json
import urllib.request
from . import registrations


def request(name,body=None,update_id=None):
    worker=registrations.get(name)
    if not worker:raise ValueError('No wrapper registration for '+name)
    route='/v1/updates'
    if update_id:
        import re
        if not re.fullmatch('[a-f0-9]{32}',update_id):raise ValueError('Invalid update id')
        route+='/'+update_id
    headers={}
    if worker.get('key'):headers['Authorization']='Bearer '+worker['key']
    data=None
    if body is not None:
        if body.get('approved') is not True:raise ValueError('Explicit operator approval is required')
        data=json.dumps(body).encode();headers['Content-Type']='application/json'
    req=urllib.request.Request(worker['url'].rstrip('/')+route,data=data,headers=headers)
    with urllib.request.urlopen(req,timeout=20) as response:return json.load(response)


def submit(name, *, version=None, requested_by='Core console'):
    """Deliver only the exact release selected by an explicit operator action."""
    from .releases import fleet_versions, release
    version = version or fleet_versions().get('hugpy-wrapper')
    if not version:
        raise ValueError('No central Wrapper release is available')
    selected = release(version=version)
    body = {'approved': True, 'version': version, 'requested_by': requested_by}
    if selected and selected.get('artifact'):
        from .transport import target, request as wrapper_request
        from .releases import _ver_key
        health = wrapper_request(target(name), '/health', timeout=5)
        # The vault's first published staged-update build is 0.1.165; local
        # Debian builds previously used a separate 0.1.168+ version sequence.
        if _ver_key(health.get('source_version') or health.get('version')) < _ver_key('0.1.165'):
            raise ValueError('Install the current Wrapper package when idle to enable staged updates')
        body['artifact'] = selected['artifact']
    return request(name, body)
