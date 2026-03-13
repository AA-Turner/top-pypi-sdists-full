import json
import logging
import threading
from bstack_utils import logger_utils
logger = logging.getLogger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
class PlaywrightDriverWrapperDirect:
    _session_ids = {}
    _session_ids_lock = threading.Lock()
    _A11Y_SCAN_EXCLUDE = {'evaluate', 'evaluate_handle', 'close'}
    _LOCATOR_CREATING_METHODS = {
        'locator', 'frameLocator',  # Core locator methods
        'get_by_role', 'get_by_text', 'get_by_label',  # Query methods
        'get_by_placeholder', 'get_by_alt_text', 'get_by_title', 'get_by_test_id',
        'filter', 'first', 'last', 'nth',  # Filtering methods
    }
    def __init__(self, browser, page, capabilities, config=None):
        self._browser = browser
        self._page = page
        self._capabilities = capabilities or {}
        self._config = config or {}
        self._thread_id = threading.get_ident()
        self._cbt_info_sent = False
        self._setup_session_id_capture()
        if page is not None:
            self._wrap_page_for_a11y(page, self)
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
                            if not bs_params:
                                bs_params = msg.get('bStackParams', {})
                                if bs_params:
                                    msg = dict(msg)
                                    msg.pop('bStackParams', None)
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
                                if 'stack' not in error_normalized:
                                    error_normalized['stack'] = ''
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
    def _perform_scan_with_fallback(cls, wrapper, cmd_name):
        """Trigger an A11y scan for a single Playwright command.
        Bypasses perform_scan's is_enabled_platform guard (which requires CONFIG
        and PLATFORM_INDEX to be correctly set) by checking bstackA11yShouldScan
        directly — the same flag that playwright.py sets when a11y_enabled is True
        for this specific session/platform.
        """
        try:
            if not getattr(wrapper, 'bstackA11yShouldScan', False):
                return
            from bstack_utils.accessibility_scripts import accessibility_scripts
            scan_script = accessibility_scripts.perform_scan
            if not scan_script:
                return
            result = wrapper.execute_async_script(scan_script, {'method': cmd_name})
            try:
                log_data = {
                    "request": {
                        "command": "A11Y_SCAN",
                        "parameters": [
                            {"method": cmd_name}
                        ]
                    },
                    "response": {
                        "body": {
                            "msg": result.get("msg", "") if isinstance(result, dict) else "",
                            "success": result.get("success", True) if isinstance(result, dict) else True
                        }
                    }
                }
                automation_logger.info(json.dumps(log_data, separators=(",", ":")))
            except Exception:
                pass
        except Exception as e:
            logger.debug(f"Per-command A11y scan failed ({cmd_name}): {e}")
    @classmethod
    def _wrap_locator_for_a11y(cls, locator, wrapper):
        """Wrap a Playwright Locator's action methods to trigger A11y scans.
        Also wraps locator-returning methods (locator.locator, .filter, .nth, etc.)
        so that chained locators are covered automatically.
        """
        if locator is None:
            return
        if getattr(locator, '_bstack_a11y_loc_wrapped', False):
            return
        try:
            locator._bstack_a11y_loc_wrapped = True
        except Exception:
            pass
        try:
            from bstack_utils.accessibility_scripts import accessibility_scripts
            commands = accessibility_scripts.commands_to_wrap or []
            cmd_names = set()
            for cmd in commands:
                name = cmd.get('name') if isinstance(cmd, dict) else cmd
                if name and name not in cls._A11Y_SCAN_EXCLUDE:
                    cmd_names.add(name)
            for method_name in cmd_names:
                original = getattr(locator, method_name, None)
                if original is None or not callable(original):
                    continue
                if getattr(original, '_bstack_a11y_wrapped', False):
                    continue
                def make_action_wrapper(orig, cmd_name):
                    def wrapped(*args, **kwargs):
                        result = orig(*args, **kwargs)
                        cls._perform_scan_with_fallback(wrapper, cmd_name)
                        return result
                    wrapped._bstack_a11y_wrapped = True
                    return wrapped
                setattr(locator, method_name, make_action_wrapper(original, method_name))
            for method_name in cls._LOCATOR_CREATING_METHODS:
                original = getattr(locator, method_name, None)
                if original is None or not callable(original):
                    continue
                if getattr(original, '_bstack_a11y_loc_creator_wrapped', False):
                    continue
                def make_locator_creator_wrapper(orig):
                    def wrapped(*args, **kwargs):
                        sub_locator = orig(*args, **kwargs)
                        cls._wrap_locator_for_a11y(sub_locator, wrapper)
                        return sub_locator
                    wrapped._bstack_a11y_loc_creator_wrapped = True
                    return wrapped
                setattr(locator, method_name, make_locator_creator_wrapper(original))
            logger.debug("Wrapped Locator for A11y scanning")
        except Exception as e:
            logger.debug(f"Failed to wrap Locator for A11y: {e}")
    @classmethod
    def _wrap_page_for_a11y(cls, page, wrapper):
        """Wrap Page action methods and locator-returning methods for A11y scanning.
        Action methods (goto, click, fill, …) fire a scan AFTER each call.
        Locator-returning methods (locator, get_by_role, …) wrap the returned
        Locator so that ``page.locator('btn').click()`` also fires a scan.
        """
        try:
            from bstack_utils.accessibility_scripts import accessibility_scripts
            commands = accessibility_scripts.commands_to_wrap or []
            wrapped_count = 0
            for cmd in commands:
                method_name = cmd.get('name') if isinstance(cmd, dict) else cmd
                if not method_name or method_name in cls._A11Y_SCAN_EXCLUDE:
                    continue
                original = getattr(page, method_name, None)
                if original is None or not callable(original):
                    continue
                if getattr(original, '_bstack_a11y_wrapped', False):
                    continue
                def make_wrapper(orig, cmd_name):
                    def wrapped(*args, **kwargs):
                        result = orig(*args, **kwargs)
                        cls._perform_scan_with_fallback(wrapper, cmd_name)
                        return result
                    wrapped._bstack_a11y_wrapped = True
                    return wrapped
                setattr(page, method_name, make_wrapper(original, method_name))
                wrapped_count += 1
            locator_wrapped_count = 0
            for method_name in cls._LOCATOR_CREATING_METHODS:
                original = getattr(page, method_name, None)
                if original is None or not callable(original):
                    continue
                if getattr(original, '_bstack_a11y_loc_creator_wrapped', False):
                    continue
                def make_locator_creator(orig):
                    def wrapped(*args, **kwargs):
                        locator = orig(*args, **kwargs)
                        cls._wrap_locator_for_a11y(locator, wrapper)
                        return locator
                    wrapped._bstack_a11y_loc_creator_wrapped = True
                    return wrapped
                setattr(page, method_name, make_locator_creator(original))
                locator_wrapped_count += 1
            logger.debug(
                f"Wrapped {wrapped_count} Page action methods and "
                f"{locator_wrapped_count} locator-creating methods for A11y scanning"
            )
            if not getattr(page, '_bstack_a11y_assertion_methods_injected', False):
                def _make_get_results_fn(wrapper_ref, script_attr, log_label):
                    def _fn():
                        try:
                            if not getattr(wrapper_ref, 'bstackA11yShouldScan', False):
                                logger.debug(
                                    "Not an Accessibility Automation session, "
                                    "cannot retrieve Accessibility " + log_label + "."
                                )
                                return {}
                            script_code = getattr(accessibility_scripts, script_attr, None)
                            if not script_code:
                                logger.warning(
                                    "Cannot retrieve Accessibility " + log_label +
                                    " — script not available yet."
                                )
                                return {}
                            logger.debug('Performing scan before getting ' + log_label)
                            scan_script = accessibility_scripts.perform_scan
                            if scan_script:
                                try:
                                    wrapper_ref.execute_async_script(scan_script)
                                except Exception:
                                    pass
                            return wrapper_ref.execute_async_script(script_code)
                        except Exception as e:
                            logger.error("Accessibility " + log_label + " could not be retrieved: " + str(e))
                            return {}
                    return _fn
                get_results_fn = _make_get_results_fn(wrapper, 'get_results', 'results')
                get_summary_fn = _make_get_results_fn(wrapper, 'get_results_summary', 'results summary')
                setattr(page, 'getAccessibilityResults', get_results_fn)
                setattr(page, 'get_accessibility_results', get_results_fn)
                setattr(page, 'getAccessibilityResultsSummary', get_summary_fn)
                setattr(page, 'get_accessibility_results_summary', get_summary_fn)
                page._bstack_a11y_assertion_methods_injected = True
                logger.debug("Injected A11y assertion methods onto page object")
        except Exception as e:
            logger.debug(f"Failed to wrap Page for A11y: {e}")
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
            if not args:
                return page.evaluate(script)
            if len(args) == 1:
                return page.evaluate(script, args[0])
            return page.evaluate(script, list(args))
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
                    const _bstackTimeout = setTimeout(() => resolve(null), 30000);
                    bstackSdkArgs.push(function(result) {{
                        clearTimeout(_bstackTimeout);
                        resolve(result);
                    }});
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
        if page is not None and hasattr(page, 'evaluate'):
            self._page = page
            self._wrap_page_for_a11y(page, self)
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
