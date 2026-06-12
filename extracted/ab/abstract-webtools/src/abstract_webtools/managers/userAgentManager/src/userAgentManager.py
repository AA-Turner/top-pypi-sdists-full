from .imports import *
from .functions import *
from urllib.parse import urlparse, urljoin
class UserAgentManager:
    def __init__(self,
                 operating_system=None,
                 browser=None,
                 version=None,
                 user_agent=None,
                 randomAll=False,
                 randomOperatingSystem=False,
                 randomBrowser=False):
        self.randomAll = randomAll
        self.randomOperatingSystem = randomOperatingSystem
        self.randomBrowser = randomBrowser
        self.operating_system = pickUserAgentVars(
            operating_system,
            OPERATING_SYSTEMS
            )
        self.browser = pickUserAgentVars(
            browser,
            BROWSERS
            )
        self.version = version or '42.0'
        self.user_agent = user_agent or self.get_user_agent()
        self.header = {"user-agent": self.user_agent}
    # --- small helpers -------------------------------------------------
    def _rand_locale(self):
        # common Accept-Language candidates; expand as you wish
        langs = [
            "en-US,en;q=0.9",
            "en-GB,en;q=0.9",
            "en-US,en;q=0.8,es;q=0.6",
            "en-US,en;q=0.9,fr;q=0.7",
            "de-DE,de;q=0.9,en;q=0.8"
        ]
        return random.choice(langs)

    def _rand_encoding(self):
        # Accept-Encoding header usually
        return "gzip, deflate, br"

    def _rand_connection(self):
        return random.choice(["keep-alive", "close"])

    def _rand_accept(self):
        # typical general Accept header
        return "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"

    def _sec_fetch_map(self, resource_hint="document"):
        # resource_hint: 'document', 'image', 'empty' etc
        return {
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate" if resource_hint == "document" else "no-cors",
            "Sec-Fetch-User": "?1" if resource_hint == "document" else "?0",
            "Sec-Fetch-Dest": resource_hint
        }

    def _make_sec_ch_ua(self):
        # Minimal structured Sec-CH-UA; caller may choose to include more precise entries
        # Format: '"Chromium";v="113", "Google Chrome";v="113", "Not A(Brand)";v="24"'
        # We keep it simple and swap a few brands randomly
        brands = [
            ('"Chromium";v="118"', '"Google Chrome";v="118"', '"Not A;Brand";v="99"'),
            ('"Chromium";v="120"', '"Microsoft Edge";v="120"', '"Not A;Brand";v="99"'),
            ('"Chromium";v="116"', '"Brave";v="116"', '"Not A;Brand";v="99"'),
        ]
        return ', '.join(random.choice(brands))

    def _make_sec_ch_ua_platform(self):
        plat_map = {
            "Windows": "Windows",
            "Mac": "macOS",
            "Linux": "Linux",
            "Android": "Android",
            "iOS": "iOS"
        }
        # try to infer from self.operating_system if available
        os_name = str(self.operating_system or "").lower()
        if "win" in os_name:
            return "Windows"
        if "mac" in os_name or "darwin" in os_name:
            return "macOS"
        if "android" in os_name:
            return "Android"
        if "ios" in os_name:
            return "iOS"
        return random.choice(list(plat_map.values()))

    # --- public API ---------------------------------------------------
    def generate_headers(self,
                         accept: str | None = None,
                         accept_language: str | None = None,
                         accept_encoding: str | None = None,
                         connection: str | None = None,
                         referer: str | None = None,
                         origin: str | None = None,
                         include_sec_fetch: bool = True,
                         include_ch_ua: bool = True,
                         resource_hint: str = "document",
                         extra: dict | None = None,
                         **kwargs) -> dict:
        """
        Return a fully-populated headers dict appropriate for browser-like requests.
        - resource_hint controls Sec-Fetch-Dest (document / image / empty / audio)
        - referer/origin are used as-is if provided; referer will be normalized if a URL is passed.
        - extra: dict of header->value to merge at the end (overrides defaults).
        """
        # Ensure UA exists
        ua = self.user_agent or self.get_user_agent()

        headers = {
            "User-Agent": ua,
            "Accept": accept or self._rand_accept(),
            "Accept-Language": accept_language or self._rand_locale(),
            "Accept-Encoding": accept_encoding or self._rand_encoding(),
            "Connection": connection or self._rand_connection(),
            # Optional standard hint many browsers send
            "Upgrade-Insecure-Requests": "1",
        }

        # Add Sec-Fetch* group if desired
        if include_sec_fetch:
            headers.update(self._sec_fetch_map(resource_hint=resource_hint))

        # Add Client Hints (Sec-CH-UA, Sec-CH-UA-Platform) if desired
        if include_ch_ua:
            headers["Sec-CH-UA"] = self._make_sec_ch_ua()
            headers["Sec-CH-UA-Platform"] = self._make_sec_ch_ua_platform()
            # Optional: platform version hints; keep minimal
            headers["Sec-CH-UA-Mobile"] = "?0"

        # Referer / Origin normalization
        if referer:
            headers["Referer"] = referer
        elif origin and urlparse(origin).scheme:
            headers["Referer"] = origin

        if origin:
            headers["Origin"] = origin

        # merge extra headers (explicit overrides)
        if extra and isinstance(extra, dict):
            headers.update(extra)

        # lowercase or canonicalize headers based on your preference:
        # requests library is case-insensitive so either is fine.
        self.header = headers  # store last generated header set
        return headers

    # convenience: generate a set for fetches to a given URL (sets Referer automatically)
    def generate_for_url(self, url: str, **kwargs):
        parsed = urlparse(url)
        origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else None
        kwargs.setdefault("referer", origin)
        kwargs.setdefault("origin", origin)
        return self.generate_headers(**kwargs)
    @staticmethod
    def user_agent_db():
        return BIG_USER_AGENT_DICT
    def get_random_choice(self,operating_system=False,browser=False):
        if self.randomAll or self.randomOperatingSystem or (isinstance(operating_system,bool) and operating_system == True):
            self.operating_system = randomChoice(OPERATING_SYSTEMS)
        if self.randomAll or self.randomBrowser or (isinstance(browser,bool) and browser == True):
            self.browser = randomChoice(BROWSERS)
        return self.operating_system,self.browser
    def get_user_agent(self):
        ua_db = self.user_agent_db()
        self.get_random_choice()
        os_db = getRandomValues(ua_db,self.operating_system)
        br_db = getRandomValues(os_db,self.browser)
        if self.version in br_db:
            return br_db[self.version]
        return randomChoice(br_db)


