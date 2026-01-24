from .imports import *
from .functions import *
from urllib3.util.retry import Retry               # <-- correct place
import logging
class NetworkManager:
    def __init__(self, user_agent_manager=None, user_agent=None, tls_adapter=None, ssl_manager=None,
                 proxies=None, cookies=None, ciphers=None, certification: Optional[str]=None,
                 ssl_options: Optional[List[str]]=None):
        self.ua_mgr = user_agent_manager or UserAgentManager()
        self.ciphers = ciphers or CipherManager().ciphers_string
        self.ssl_mgr = ssl_manager or SSLManager(
            ciphers=self.ciphers or CipherManager().ciphers_string,
            ssl_options=ssl_options,
            certification=certification
        )

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent or self.ua_mgr.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        })

        self.tls_adapter = tls_adapter or TLSAdapter(self.ssl_mgr)
        self.session.mount("https://", self.tls_adapter)
        self.session.mount("http://", HTTPAdapter())

        if proxies:
            self.session.proxies = proxies
        self.proxies = self.session.proxies

        # normalize cookies then load into jar
        norm = self._normalize_cookies(cookies)
        if norm:
            jar = requests.cookies.RequestsCookieJar()
            for k, v in norm.items():
                jar.set(k, v)
            self.session.cookies = jar
        self.cookies = norm

        # robust retries
        retry = Retry(total=5, backoff_factor=0.5, status_forcelist=[429,500,502,503,504])
        self.session.get_adapter("https://").max_retries = retry
        self.session.get_adapter("http://").max_retries = retry

    def _normalize_cookies(self, cookies):
        """Ensure cookies are always a dict of str->str"""
        if not cookies:
            return {}
        if isinstance(cookies, dict):
            return {str(k): str(v) for k, v in cookies.items()}
        if isinstance(cookies, requests.cookies.RequestsCookieJar):
            return {c.name: str(c.value) for c in cookies}
        logging.warning("Dropping invalid cookies object: %r", cookies)
        return {}
