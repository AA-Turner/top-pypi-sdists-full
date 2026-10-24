# Browser sign-in for spy.login() called with only a URL, used by coding agents and other applications running on the
# user's own computer. SPy uses Seeq's pre-registered public OAuth client for local applications ("local-client"):
#
# 1. Open the browser at Seeq's /oauth/authorize with a PKCE challenge and a temporary
#    http://127.0.0.1:<port>/callback. The user signs in to Seeq as usual and allows access, and Seeq redirects a
#    one-time code to that callback.
# 2. Trade the code and the PKCE verifier at /oauth/token for an ordinary Seeq session token.
# 3. Save the token (in the OS keychain, or a file only the user can read) so later logins reuse it while Seeq still
#    accepts it. A lock file makes several processes starting at once share a single browser prompt.
#
# Without a local browser (SSH, containers, an agent's hidden shell) Seeq shows the code on the page instead, and a
# second spy.login(auth_code=...) call finishes the sign-in.
#
# All requests go through SPy's own SDK client, so they use the same TLS and proxy settings as the rest of SPy.
from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import time
import webbrowser
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, Iterator, Optional
from urllib.parse import parse_qs, urlencode, urlparse

from seeq.base import util
from seeq.base.seeq_names import SeeqNames
from seeq.sdk import ApiClient
from seeq.sdk.rest import ApiException
from seeq.spy._errors import SPyDependencyNotFound, SPyRuntimeError
from seeq.spy._status import Status

CLIENT_ID = 'local-client'
OUT_OF_BAND_REDIRECT = 'urn:ietf:wg:oauth:2.0:oob'
_KEYRING_SERVICE = 'seeq-spy-oauth'
_WINDOWS = os.name == 'nt'
_NO_WINDOWS_KEYCHAIN = ('Seeq browser sign-in keeps its session in the Windows Credential Manager, which needs the '
                        '"keyring" package. Install it (pip install seeq-spy[keychain]) and try again, or log in '
                        'with an access key.')


def sign_in(client: ApiClient, seeq_url: str, status: Status, code: Optional[str] = None) -> str:
    # Returns a Seeq session token: the saved one while Seeq still accepts it, otherwise a new one from the browser.
    seeq_url = seeq_url.rstrip('/')
    store = _Store(seeq_url)

    # One process at a time: others started alongside wait here, then reuse the session it saved, so several agent
    # processes starting together share a single browser prompt.
    with store.locked():
        saved = store.load()

        # Second call of a headless sign-in: finish it with the code Seeq showed the user.
        if code:
            if 'pending_verifier' not in saved:
                raise SPyRuntimeError('No Seeq browser sign-in is waiting for a code. '
                                      'Call spy.login() without a code to start one.')
            return _exchange(client, store, seeq_url, code.strip(), OUT_OF_BAND_REDIRECT, saved['pending_verifier'])

        # A saved session can end at any time (expiry, logout elsewhere, an administrator), so ask Seeq before
        # reusing it. Seeq's API only accepts its own media type.
        if 'access_token' in saved:
            media_type = 'application/vnd.seeq.v1+json'
            headers = {'Accept': media_type, 'Content-Type': media_type,
                       SeeqNames.API.Headers.auth: saved['access_token']}
            try:
                client.request('GET', f'{seeq_url}/api/users/me', headers=headers)
                return saved['access_token']
            except ApiException:
                pass

        return _authorize(client, store, seeq_url, status, saved.get('pending_verifier'))


def forget(seeq_url: str, token: Optional[str]) -> None:
    # Used by spy.logout(): remove the saved session if it is the one being logged out. Browser sign-in always creates
    # the folder, so without it there is nothing to remove, and other logouts leave the disk and keychain alone.
    store = _Store(seeq_url.rstrip('/'))
    if not token or not store.file.parent.exists():
        return
    with store.locked():
        if store.load().get('access_token') == token:
            store.delete()


def _authorize(client: ApiClient, store: _Store, seeq_url: str, status: Status, pending_verifier: Optional[str]) -> str:
    # Seeq answers 404 here when it does not support browser sign-in (older versions, or no SSO directory).
    try:
        client.request('GET', f'{seeq_url}/.well-known/oauth-authorization-server')
    except ApiException as e:
        raise SPyRuntimeError(f'{seeq_url} does not support browser sign-in ({e.status}). '
                              'Log in with an access key instead.')

    # Windows has no file only the user can read, so there the keychain is required: stop before the browser opens
    # rather than obtain a session SPy cannot protect.
    if _WINDOWS and not store.keychain_works():
        raise SPyDependencyNotFound(_NO_WINDOWS_KEYCHAIN)

    # PKCE: the code Seeq hands out is useless without this verifier, which never leaves this machine. A headless
    # sign-in that is still waiting keeps its verifier, so an agent retrying spy.login() does not invalidate the URL
    # the user already has.
    verifier = pending_verifier or secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    state = secrets.token_urlsafe(32)

    def authorize_url(redirect_uri: str) -> str:
        return f'{seeq_url}/oauth/authorize?' + urlencode({
            'response_type': 'code', 'client_id': CLIENT_ID, 'redirect_uri': redirect_uri, 'scope': 'seeq.access',
            'state': state, 'code_challenge': challenge, 'code_challenge_method': 'S256'})

    # The temporary loopback callback for the browser's redirect (port 0 lets the OS pick a free port).
    with _CallbackServer(('127.0.0.1', 0), _CallbackHandler) as server:
        server.state = state
        redirect_uri = f'http://127.0.0.1:{server.server_port}/callback'
        browser_url = authorize_url(redirect_uri)

        # No local browser (webbrowser.open returns False): ask Seeq to show the code on the page instead, remember
        # the verifier, and let a second spy.login(auth_code=...) call finish.
        if not webbrowser.open(browser_url):
            store.save({'pending_verifier': verifier})
            raise SPyRuntimeError(
                'Seeq sign-in needs approval in a browser.\n'
                'Ask the user to open this URL, allow access, and report back the code Seeq shows:\n'
                f'{authorize_url(OUT_OF_BAND_REDIRECT)}\n'
                f"Then run: spy.login(url='{seeq_url}', auth_code='<that code>')")

        # Wait up to five minutes for the browser to come back with the code (or with an error on Cancel).
        status.update(f'Opening Seeq sign-in in your browser. If it does not open, visit: {browser_url}',
                      Status.RUNNING)
        deadline = time.monotonic() + 300
        while server.result is None:
            server.timeout = deadline - time.monotonic()
            if server.timeout <= 0:
                raise SPyRuntimeError('Timed out waiting for Seeq sign-in to be approved in the browser.')
            server.handle_request()

    if 'code' not in server.result:
        raise SPyRuntimeError(f"Seeq sign-in was not approved: {server.result.get('error', 'no code returned')}")
    return _exchange(client, store, seeq_url, server.result['code'], redirect_uri, verifier)


def _exchange(client: ApiClient, store: _Store, seeq_url: str, code: str, redirect_uri: str, verifier: str) -> str:
    # Trade the one-time code (plus the verifier that proves we asked for it) for a Seeq session, and save it.
    try:
        response = client.request('POST', f'{seeq_url}/oauth/token',
                                  headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                  post_params={'grant_type': 'authorization_code', 'client_id': CLIENT_ID,
                                               'code': code, 'redirect_uri': redirect_uri, 'code_verifier': verifier})
    except ApiException as e:
        raise SPyRuntimeError(f'Seeq sign-in failed ({e.status}): {e.body}. Call spy.login() again to start over.')
    token = json.loads(response.data)['access_token']
    store.save({'access_token': token})
    return token


class _CallbackServer(HTTPServer):
    # The loopback listener: `state` names the sign-in it waits for, `result` holds the redirect's query values.
    state: str
    result: Optional[Dict[str, str]] = None


class _CallbackHandler(BaseHTTPRequestHandler):
    # Answers the browser's redirect to the loopback callback, and hands its query values to the waiting sign-in.

    # Browsers open idle pre-connect sockets; don't let one of them block the wait for long.
    timeout = 10
    server: _CallbackServer

    def do_GET(self) -> None:
        url = urlparse(self.path)
        values = {key: items[0] for key, items in parse_qs(url.query).items()}
        # Only this sign-in's own redirect (bound by state) may end the wait.
        if url.path != '/callback' or values.get('state') != self.server.state:
            self.send_error(404)
            return
        self.server.result = values
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        if 'code' in values:
            title, message = 'Seeq sign-in complete', 'You are signed in. Return to your application to continue.'
        else:
            title, message = 'Seeq sign-in canceled', 'No access was granted. You can return to your application.'
        page = (Path(__file__).parent / '_oauth_callback.html').read_text(encoding='utf-8')
        self.wfile.write(page.replace('{{TITLE}}', title).replace('{{MESSAGE}}', message).encode())

    def log_message(self, format: str, *args: Any) -> None:
        pass  # keep request logging out of the user's output


class _Store:
    # The saved sign-in for one Seeq URL: in the OS keychain when there is one, otherwise (Unix only) in a file only the
    # user can read (keychains are often unavailable over SSH and in containers).

    def __init__(self, seeq_url: str) -> None:
        self.key = seeq_url.lower()
        file_name = f'oauth-{hashlib.sha256(self.key.encode()).hexdigest()[:16]}.json'
        self.file = Path(util.get_home_dir(), '.seeq', 'spy', file_name)

    @contextmanager
    def locked(self) -> Iterator[None]:
        # An exclusive lock on a file beside the saved sign-in, held while the body runs.
        self.file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with util.safe_open(str(self.file.with_suffix('.lock')), 'a', encoding='utf-8') as lock:
            if _WINDOWS:
                import msvcrt
                while True:
                    try:
                        msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
                        break
                    except OSError:
                        pass  # LK_LOCK gives up after about ten seconds; keep waiting for the process signing in
                try:
                    yield
                finally:
                    msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX)  # released when the file closes
                yield

    def keychain_works(self) -> bool:
        try:
            import keyring
            keyring.get_password(_KEYRING_SERVICE, self.key)
            return True
        except Exception:
            return False

    def load(self) -> Dict[str, str]:
        # The file only exists when the keychain failed at the last save, so it is the newer copy if both exist.
        try:
            if self.file.exists():
                return json.loads(self.file.read_text(encoding='utf-8'))
            import keyring
            return json.loads(keyring.get_password(_KEYRING_SERVICE, self.key) or '{}')
        except Exception:
            return {}

    def save(self, credential: Dict[str, str]) -> None:
        value = json.dumps(credential)
        try:
            import keyring
            keyring.set_password(_KEYRING_SERVICE, self.key, value)
            self.file.unlink(missing_ok=True)
        except Exception:
            if _WINDOWS:
                raise SPyDependencyNotFound(_NO_WINDOWS_KEYCHAIN)
            self.file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            self.file.touch(mode=0o600)
            os.chmod(self.file, 0o600)  # also tightens a file that already existed
            self.file.write_text(value, encoding='utf-8')

    def delete(self) -> None:
        try:
            import keyring
            keyring.delete_password(_KEYRING_SERVICE, self.key)
        except Exception:
            pass
        self.file.unlink(missing_ok=True)
