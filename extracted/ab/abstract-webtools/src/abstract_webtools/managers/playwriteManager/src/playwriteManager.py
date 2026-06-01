from .imports import *

class playwriteManager(metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'initialized'):
            self.initialize(*args, **kwargs)

    def initialize(self,
                   url=None,
                   soup_mgr=None,
                   req_mgr=None,
                   url_mgr=None,
                   ua_mgr=None,
                   headless=True,
                   user_agent=None,
                   source_code=None,
                   context=None,
                   viewport=None,
                   *args, **kwargs):
        print('initializing')
        self.initialized = True
        self.headless = if_none_default(headless, True)
        user_agent = if_none_default(user_agent, DEFAULT_USER_AGENT)

        self.ua_mgr = get_ua_mgr(ua_mgr=ua_mgr, user_agent=user_agent)
        self.user_agent = self.ua_mgr.user_agent
        print(f"user_agent={self.user_agent}")
        self.soup_mgr, self.req_mgr, self.url_mgr = make_mgr_updates(
            url=url,
            source_code=source_code,
            soup_mgr=soup_mgr,
            req_mgr=req_mgr,
            url_mgr=url_mgr,
            **kwargs
        )
        print(f"url_mgr={self.url_mgr}")
        print(f"req_mgr={self.req_mgr}")
        print(f"soup_mgr={self.soup_mgr}")
        self.url = self.url_mgr.url or url
        self.viewport = viewport or {"width": 1400, "height": 900}

        # CRITICAL FIX: Start Playwright ONCE and keep it alive
        self.p_sync = sync_playwright().start()  # ← This lives forever
        self.browser = None
        self.context = None
        self.page = None

        self.launch_browser(headless=self.headless)
        self.new_page()
        if self.url:
            self.goto_url(self.url)

    def launch_browser(self, headless=None):
        headless = if_none_default(headless, self.headless)
        self.browser = self.p_sync.chromium.launch(headless=headless)
        return self.browser

    def new_context(self, user_agent=None, viewport=None):
        user_agent = user_agent or self.user_agent
        viewport = viewport or self.viewport
        self.context = self.browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
            java_script_enabled=True,
            bypass_csp=True
        )
        return self.context

    def new_page(self):
        if not self.context:
            self.new_context()
        self.page = self.context.new_page()
        return self.page

    def goto_url(self, url=None, wait_until="networkidle"):
        url = url or self.url
        if not url or not self.page:
            return False
        self.page.goto(url, wait_until=wait_until)
        self.page.wait_for_load_state("networkidle")
        time.sleep(2)  # Let React/Angular/whatever settle
        self.url = self.page.url  # Update in case of redirect
        return True

    def close(self):
        """Gracefully close everything"""
        try:
            if hasattr(self, 'context') and self.context:
                self.context.close()
            if hasattr(self, 'browser') and self.browser:
                self.browser.close()
            if hasattr(self, 'p_sync') and self.p_sync:
                self.p_sync.stop()
        except:
            pass

    def __del__(self):
        self.close()
