from ..imports import *
from .functions import *
from .functions import _free_port,_make_chrome_options,_looks_like_html,_requests_fallback,_wait_until_ready,_make_profile_dir
class seleneumManager(metaclass=SingletonMeta):
    def __init__(self, url):
        if getattr(self, "initialized", False):
            return
        self.initialized = True

        p = urlparse(url)
        self.domain = p.netloc
        self.scheme = p.scheme or "https"
        self.base_url = f"{self.scheme}://{self.domain}"

        self.site_dir = os.path.join("/var/tmp", "cw-sites", self.domain)
        os.makedirs(self.site_dir, exist_ok=True)

        self._sessions: dict[str, dict] = {}  # key -> {"driver": ..., "profile": ...}
        atexit.register(lambda sm=self: sm.close_all())

    def get_url_to_path(self, url):
        url = eatAll(str(url), ['',' ','\n','\t','\\','/'])
        p = urlparse(url)
        if p.netloc == self.domain:
            parts = [x for x in p.path.split('/') if x]
            d = self.site_dir
            for seg in parts[:-1]:
                d = os.path.join(d, seg)
                os.makedirs(d, exist_ok=True)
            last = parts[-1] if parts else "index.html"
            ext = os.path.splitext(last)[-1] or ".html"
            if not hasattr(self, "page_type"):
                self.page_type = []
            self.page_type.append(ext if not self.page_type else self.page_type[-1])
            return os.path.join(d, last)

    def get_with_netloc(self, url):
        p = urlparse(url)
        if p.netloc == '':
            url = f"{self.scheme}://{self.domain}/{url.strip().lstrip('/')}"
        return url

    def get_driver(self, url) -> tuple[str, webdriver.Chrome]:
        bin_path = get_env_value('CHROME_BINARY')
        opts, prof = _make_chrome_options(binary_path=bin_path, user_data_dir=None)
        driver = webdriver.Chrome(options=opts)
        key = f"{url}#{time.time()}"
        self._sessions[key] = {"driver": driver, "profile": prof}
        return key, driver

    def close_driver(self, key: str):
        sess = self._sessions.pop(key, None)
        if not sess: return
        try:
            try: sess["driver"].quit()
            except Exception: pass
        finally:
            shutil.rmtree(sess.get("profile") or "", ignore_errors=True)

    def close_all(self):
        for key in list(self._sessions.keys()):
            self.close_driver(key)
seleniumManager = seleneumManager
