import json
import threading
import time
import traceback
import requests
from urllib.parse import urlparse

from adam.log import Log
from adam.sso.idp import Idp
from adam.sso.idp_login import IdpLogin
from adam.config import Config
from adam.utils import json_to_csv, lines_to_tabular, log, log2
from adam.apps import Apps

class AppLogin:
    def __init__(self, session: requests.Session, app_access_token: str, idp_uri: str, idp_login: IdpLogin = None):
        self.session = session
        self.app_access_token = app_access_token
        self.idp_uri = idp_uri
        self.idp_login = idp_login

class NoAppIngressException(Exception):
    pass

class AppSession:
    sessions_by_host = {}

    def __init__(self, host: str = None, env: str = None):
        self.host = host
        self.env = env
        self.app_login: AppLogin = None

    def create(env: str, app: str, namespace: str = None) -> 'AppSession':
        if not(host := Apps.app_host(env, app, namespace)):
            raise NoAppIngressException('Cannot locate ingress for app.')

        key = f'{host}/{env}'
        if key in AppSession.sessions_by_host:
            return AppSession.sessions_by_host[key]

        session = AppSession(host, env)

        AppSession.sessions_by_host[key] = session

        return session

    def run(env: str, app: str, namespace: str, type: str, action: str, payload: any = None, forced = False):
        app_session: AppSession = AppSession.create(env, app, namespace)

        def run0(app_login: AppLogin, retried: bool):
            if app_login:
                with app_login.session as session:
                    uri = f'https://{app_session.host}/{env}/{app}/api/8/{type}/{action}'
                    r = session.post(uri, json=payload, headers={
                        'X-Request-Envelope': 'true'
                    })

                    if Config().is_debug():
                        log2(f'{r.status_code} {uri}')
                        log2(payload)

                    if r.status_code >= 200 and r.status_code < 300 or r.status_code == 400:
                        try:
                            js = r.json()
                            try:
                                header, lines = json_to_csv(js, delimiter='\t')
                                log(lines_to_tabular(lines, header=header, separator='\t'))
                            except:
                                log(js)
                        except:
                            if urlparse(r.url).hostname != urlparse(uri).hostname and not retried:
                                app_login = app_session.login(idp_uri=app_login.idp_uri, forced=forced, use_token_from_env=False, use_cached_creds=False)
                                retried = True

                                return run0(app_login, True)

                            if r.text:
                                log2(f'{r.status_code} {r.url} Failed parsing the results.')
                                Config().debug(r.text)
                    else:
                        log2(r.status_code)
                        log2(r.text)

        app_login = app_session.login(forced=forced)
        run0(app_login, False)

    def login(self, idp_uri: str = None, forced = False, use_token_from_env=True, use_cached_creds=True) -> AppLogin:
        if not forced and self.app_login:
            return self.app_login

        idp_login: IdpLogin = Idp.login(self.host, idp_uri=idp_uri, forced=forced, use_token_from_env=use_token_from_env, use_cached_creds=use_cached_creds)
        if not idp_login:
            log2(f"Invalid username/password.")

            return None

        if idp_login.state == 'EMPTY':
            idp_login.state = IdpLogin.create_from_idp_uri(self.idp_redirect_url()).state

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        form_data = {
            'state': idp_login.state,
            'id_token': idp_login.id_token
        }

        stop_event = threading.Event()

        session = idp_login.session
        if not session:
            session = requests.Session()

        def login0():
            try:
                # oidc/login may hang
                timeout = Config().get('app.login.timeout', 5)
                Config().debug(f'-> {idp_login.app_login_url}')
                session.post(idp_login.app_login_url, headers=headers, data=form_data, timeout=timeout)
            except Exception:
                pass
            finally:
                stop_event.set()

        my_thread = threading.Thread(target=login0, daemon=True)
        my_thread.start()

        app_access_token = None
        while not app_access_token and not stop_event.is_set():
            time.sleep(1)

            try:
                check_uri = Config().get('app.login.session-check-url', 'https://{host}/{env}/{app}/api/8/C3/userSessionToken')
                check_uri = check_uri.replace('{host}', self.host).replace('{env}', self.env).replace('{app}', 'c3')
                r = session.get(check_uri)
                Config().debug(f'{r.status_code} {check_uri}')

                res_text = r.text
                js = json.loads(res_text)
                if 'signedToken' not in js:
                    log2('Cannot get c3 access token, pleae re-login.')
                    break

                app_access_token = js['signedToken']
                Config().debug(f'{r.text}')

                self.app_login = AppLogin(session, app_access_token, idp_uri)
            except Exception:
                try:
                    need = urlparse(r.url).hostname
                    if idp_login.idp_uri:
                        idp_uri = r.url
                        has = urlparse(idp_login.idp_uri).hostname
                        msg = Config().get('app.login.another', "You're logged in to {has}. However, for this app, you need to log in to {need}.")
                        msg = msg.replace('{has}', has).replace('{need}', need)
                        log2(msg)
                    else:
                        log2(f"Invalid username/password.")
                    break
                finally:
                    Config().debug(traceback.format_exc())

                    if 'res_text' in locals():
                        Log.log_to_file(res_text)

        return AppLogin(session, app_access_token, idp_uri, idp_login=idp_login)

    def idp_redirect_url(self, show_endpoints = True) -> str:
        # stgawsscpsr-c3-c3
        uri = Config().get('app.login.url', 'https://{host}/{env}/{app}')
        uri = uri.replace('{host}', self.host).replace('{env}', self.env).replace('{app}', 'c3')
        r = requests.get(uri)

        parsed_url = urlparse(r.url)
        if show_endpoints:
            log2(f'{r.status_code} {uri} <-> {parsed_url.hostname}...')
        if r.status_code < 200 or r.status_code > 299:
            return None

        return r.url