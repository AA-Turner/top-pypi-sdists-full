"""
PlaywrightDriverWrapperDirect - Selenium-like interface for Playwright in Direct Flow (Behave).
This wrapper is used by Behave + Playwright (Direct Flow) where we don't have
PlaywrightFramework.instances to store state. Instead, capabilities are stored
directly in the wrapper.
The session_id is captured from the CDP connection's bsParams dispatch.
"""
import json
import logging
import threading
logger = logging.getLogger(__name__)
class PlaywrightDriverWrapperDirect:
    """
    Wrapper providing Selenium WebDriver-like interface for Playwright in Direct Flow.
    Used by Behave hooks to access session_id and capabilities for O11y and A11y.
    """
    _session_ids = {}
    _session_ids_lock = threading.Lock()
    def __init__(self, browser, page, capabilities, config=None):
        self._browser = browser
        self._page = page
        self._capabilities = capabilities or {}
        self._config = config or {}
        self._thread_id = threading.get_ident()
        self._cbt_info_sent = False
        self._setup_session_id_capture()
        logger.debug(f"PlaywrightDriverWrapperDirect created: thread={self._thread_id}")
    @classmethod
    def setup_dispatch_capture(cls):
        """
        Patch Connection.dispatch to capture session_id from bsParams.
        MUST be called BEFORE BrowserType.connect() so that the bsParams
        message dispatched during the connection handshake is captured.
        """
        try:
            from playwright._impl._connection import Connection
            if not hasattr(Connection, '_bstack_dispatch_patched'):
                original_dispatch = Connection.dispatch
                def patched_dispatch(conn_self, msg):
                    try:
                        if isinstance(msg, dict):
                            bs_params = msg.get('params', {}).get('bsParams', {})
                            if bs_params:
                                session_id = bs_params.get('sessionId')
                                if session_id:
                                    thread_id = threading.get_ident()
                                    with cls._session_ids_lock:
                                        cls._session_ids[thread_id] = session_id
                                    logger.debug(f"Captured session_id from dispatch: {session_id}")
                                    cls._send_cbt_info_on_session()
                            error = msg.get('error')
                            if msg.get('id') and error and isinstance(error, dict) and 'error' not in error:
                                logger.debug("BrowserStack error response: {}".format(str(error)[:500]))
                                error_normalized = dict(error)
                                if 'name' not in error_normalized:
                                    error_normalized['name'] = 'Error'
                                if 'message' not in error_normalized:
                                    error_normalized['message'] = str(error)
                                msg = dict(msg)
                                msg['error'] = {'error': error_normalized}
                    except Exception as e:
                        logger.debug(f"Error in dispatch interception: {e}")
                    return original_dispatch(conn_self, msg)
                Connection.dispatch = patched_dispatch
                Connection._bstack_dispatch_patched = True
                logger.debug("Patched Connection.dispatch for session_id capture")
        except Exception as e:
            logger.debug(f"Could not setup dispatch capture: {e}")
    @classmethod
    def _send_cbt_info_on_session(cls):
        """Send CBT info when session_id becomes available."""
        try:
            wrapper = getattr(threading.current_thread(), 'bstackSessionDriver', None)
            if wrapper and isinstance(wrapper, cls) and not wrapper._cbt_info_sent:
                wrapper._cbt_info_sent = True
                from bstack_utils.testhub_handler import TestHubHandler
                TestHubHandler.send_cbt_info(wrapper)
                logger.debug(f"CBT info sent with session_id: {wrapper.session_id}")
        except Exception as e:
            logger.debug(f"Failed to send CBT info on session: {e}")
    def _setup_session_id_capture(self):
        """Ensure dispatch capture is set up (delegates to class method)."""
        self.setup_dispatch_capture()
    @property
    def _active_page(self):
        """Get the active page from the browser, with lazy lookup from contexts."""
        if self._page is not None and hasattr(self._page, 'evaluate'):
            return self._page
        try:
            if self._browser and self._browser.contexts:
                for ctx in self._browser.contexts:
                    if ctx.pages:
                        self._page = ctx.pages[-1]
                        return self._page
        except Exception as exc:
            logger.debug("Failed to resolve active page from browser contexts: %s", exc)
        return None
    @property
    def session_id(self):
        with PlaywrightDriverWrapperDirect._session_ids_lock:
            return PlaywrightDriverWrapperDirect._session_ids.get(self._thread_id)
    @property
    def capabilities(self):
        return self._normalize_capabilities(self._capabilities)
    def _normalize_capabilities(self, caps):
        if not caps:
            return {}
        return {
            "browserName": caps.get("browser", caps.get("browserName")),
            "browserVersion": caps.get("browser_version", caps.get("browserVersion")),
            "platformName": caps.get("os", caps.get("platformName")),
            "platformVersion": caps.get("os_version", caps.get("platformVersion")),
            "bstack:options": caps.get("bstack:options", {}),
            "_original": caps
        }
    @property
    def current_url(self):
        """Get current page URL."""
        try:
            page = self._active_page
            if page:
                return page.url
        except Exception as e:
            logger.debug(f"Could not get current URL: {e}")
        return ""
    def execute_script(self, script, *args):
        """Execute JavaScript synchronously (Selenium-compatible interface).
        Browser is kept alive via deferred close — no REST API fallback needed."""
        page = self._active_page
        if not page:
            logger.debug("Cannot execute script: no page available")
            return None
        try:
            if "browserstack_executor" in script:
                return page.evaluate("_ => {}", script)
            if args:
                return page.evaluate(script, *args)
            return page.evaluate(script)
        except Exception as e:
            logger.debug(f"Script execution failed: {e}")
            raise
    def execute_async_script(self, script, *args):
        """Execute JavaScript asynchronously (Selenium-compatible interface)."""
        page = self._active_page
        if not page:
            logger.debug("Cannot execute async script: no page available")
            return None
        try:
            script_template = """(function (...bstackSdkArgs) {{
                return new Promise((resolve, reject) => {{
                    bstackSdkArgs.push(resolve);
                    {fn_body}
                }});
            }})({arg_json})"""
            modified_script = script.replace("arguments", "bstackSdkArgs")
            arg_json = json.dumps(args[0] if args else {})
            final_script = script_template.format(
                fn_body=modified_script,
                arg_json=arg_json
            )
            return page.evaluate(final_script)
        except Exception as e:
            logger.debug(f"Async script execution failed: {e}")
            raise
    def is_connected(self):
        """Check if browser is still connected."""
        try:
            return self._browser and self._browser.is_connected()
        except Exception:
            return False
    def update_page(self, page):
        """Update the page reference."""
        if page is not None and hasattr(page, 'evaluate'):
            self._page = page
            logger.debug("Updated page reference for wrapper")
    def quit(self):
        """Close the browser (Selenium-compatible interface for behave hooks)."""
        try:
            if self._browser:
                try:
                    self._browser.close(_bstack_sdk_close=True)
                except TypeError:
                    self._browser.close()
        except Exception as e:
            logger.debug(f"Error closing browser: {e}")
        finally:
            with PlaywrightDriverWrapperDirect._session_ids_lock:
                PlaywrightDriverWrapperDirect._session_ids.pop(self._thread_id, None)
    def __repr__(self):
        return f"PlaywrightDriverWrapperDirect(session_id={self.session_id}, connected={self.is_connected()})"
    def __getattr__(self, name):
        """Proxy attribute access to underlying browser."""
        if hasattr(self._browser, name):
            return getattr(self._browser, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
