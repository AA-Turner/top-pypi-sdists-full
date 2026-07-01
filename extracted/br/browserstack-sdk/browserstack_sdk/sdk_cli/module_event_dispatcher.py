from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.automation_framework import AutomationFrameworkBrowser, AutomationFrameworkState, HookState
from browserstack_sdk.sdk_cli.module_base import BaseModule
from browserstack_sdk.sdk_cli.module_webdriver_test import WebDriverTestModule
from browserstack_sdk.sdk_cli.selenium_framework import SeleniumFramework
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestFrameworkTest, TestHookState, LogEntry
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import is_bstack_automation, get_writable_dir, cached_robot_pw_binary_flow
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
PY_TEST_ITEM_BASE = ["name", "parent", "config", "session", "path"]
BROWSERSTACK_ROOT_DIR = get_writable_dir()
UPLOADED_ATTACHMENTS_PREFIX = "UploadedAttachments-"
PYTEST_PROPERTIES = {
    "pytest.python.Item": PY_TEST_ITEM_BASE,
    "pytest.python.Package": PY_TEST_ITEM_BASE,
    "pytest.python.Module": PY_TEST_ITEM_BASE,
    "pytest.python.Class": PY_TEST_ITEM_BASE,
    "pytest.python.Function": PY_TEST_ITEM_BASE
    + [
        "originalname",
        "keywords",
        "fixtureinfo",
        "keywords",
        "callspec",
        "callobj",
        "start",
        "stop",
        "duration",
        "when",
    ],
    "pytest.main.Session": ["startpath", "testsfailed", "testscollected", "items"],
    "pytest.config.Config": ["invocation_params", "args"],
    "pytest.fixtures.FixtureDef": ["scope", "argname", "func", "params", "unittest", "ids"],
    "pytest.fixtures.SubRequest": ["fixturename", "param", "param_index"],
    "pytest.runner.CallInfo": ["when", "result"],
    "pytest.mark.structures.NodeKeywords": ["node", "parent"],
    "pytest.mark.structures.Mark": ["name", "args", "kwargs"],
}
_processed_attachments = set()
class EventDispatcherModule(BaseModule):
    KEY_TEST_DEFERRED = "test_deferred"
    STDOUT_LOG_LEVEL = "INFO"
    STDERR_LOG_LEVEL = "ERROR"
    stdout_write: Callable
    stderr_write: Callable
    def __init__(self, module_automation_framework, module_automation_framework_test):
        super().__init__()
        self.automation_framework_test = module_automation_framework_test
        if os.getenv("SDK_CLI_FLAG_O11Y", "1") != "1" or not self.is_enabled():
            return
        TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.PRE), self.on_before_test)
        TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.POST), self.on_after_test)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.set_hook_callback((event, state), self.on_all_test_events)
        module_automation_framework.set_hook_callback((AutomationFrameworkState.EXECUTE, HookState.POST), self.on_after_execute)
        if module_automation_framework is SeleniumFramework:
            module_automation_framework.set_hook_callback((AutomationFrameworkState.CREATE, HookState.POST), self.on_after_create)
        self.stdout_write = sys.stdout.write
        sys.stdout.write = self.new_log_capture(EventDispatcherModule.STDOUT_LOG_LEVEL, self.stdout_write)
        self.stderr_write = sys.stderr.write
        sys.stderr.write = self.new_log_capture(EventDispatcherModule.STDERR_LOG_LEVEL, self.stderr_write)
        self.orig_print = builtins.print
        builtins.print = self.new_print_capture()
        self._patch_playwright_screenshot()
    def _patch_playwright_screenshot(self):
        """Patch playwright.sync_api.Page.screenshot to forward screenshots to O11y
        via gRPC LogCreatedEvent (kind=TEST_SCREENSHOT) for Binary Flow.
        Required here (not just in playwright.py:patch_playwright) because pytest+PW
        Binary Flow does not call patch_playwright (see pytest_browserstackplugin/
        plugin.py:1516 — commented out). EventDispatcherModule is the only patch
        site for pytest+PW Binary Flow, so this method must install for screenshots
        to reach O11y in that flow. Behave+PW Binary Flow also routes through here
        (EventDispatcher loads first, sets the shared sentinel, then playwright.py's
        Direct-Flow patch becomes a no-op).
        """
        try:
            from playwright.sync_api import Page as PlaywrightPage
        except ImportError:
            return  # playwright not installed
        if getattr(PlaywrightPage, '_bstack_screenshot_patched', False):
            return
        if getattr(PlaywrightPage.screenshot, '_bstack_patched', False):
            return  # re-entry guard for worker fork/reimport
        orig_screenshot = PlaywrightPage.screenshot
        dispatcher = self  # capture for closure
        def bstack_page_screenshot(page_self, **kwargs):
            result_bytes = orig_screenshot(page_self, **kwargs)
            try:
                import base64
                screenshot_b64 = base64.b64encode(result_bytes).decode('utf-8')
                test_instances = TestFramework.get_current_instances()
                if test_instances:
                    test_instance = next(
                        (t for t in test_instances if TestFramework.has_state(t, TestFramework.KEY_TEST_UUID)),
                        None,
                    )
                    if test_instance:
                        entry = LogEntry(TestFramework.KIND_SCREENSHOT, screenshot_b64)
                        dispatcher.send_log_created_event(test_instance, [entry])
            except Exception:
                pass  # graceful degradation — never break user tests
            return result_bytes
        bstack_page_screenshot._bstack_patched = True
        PlaywrightPage.screenshot = bstack_page_screenshot
        PlaywrightPage._bstack_screenshot_patched = True  # shared sentinel
    def is_enabled(self) -> bool:
        return True
    def _is_vanilla_python_framework(self, f: TestFramework) -> bool:
        """Check if the framework is VanillaPythonFramework (python-generic)."""
        return (hasattr(f, 'FRAMEWORK_NAME') and f.FRAMEWORK_NAME == 'python-generic') or \
               (hasattr(f, 'test_frameworks') and 'python-generic' in f.test_frameworks)
    def on_all_test_events(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        is_supported = f.is_pytest_framework() or f.is_robot_framework() or f.is_behave_framework() or self._is_vanilla_python_framework(f)
        if is_supported and instance:
            o11y_time_start = datetime.now()
            test_framework_state, test_hook_state = hook_info
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return  # do not send this event over gRPC
            elif test_framework_state == TestFrameworkState.LOG:
                time_start = datetime.now()
                entries = f.get_log_entries(instance, hook_info)
                if entries:
                    self.send_log_created_event(instance, entries)
                    instance.add_benchmark("grpc:send_log_created_event", datetime.now() - time_start)
                    f.clear_logs(instance, hook_info)
                instance.add_benchmark("o11y:on_all_test_events", datetime.now() - o11y_time_start)
                return # do not send this event with the generic send_test_framework_event
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.has_state(instance, TestFramework.KEY_TEST_RESULT_AT)
            ):
                f.set_state(instance, EventDispatcherModule.KEY_TEST_DEFERRED, True)
                return # do not send this event over gRPC
            elif (
                f.get_state(instance, EventDispatcherModule.KEY_TEST_DEFERRED, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.has_state(instance, TestFramework.KEY_TEST_RESULT_AT)
            ):
                self.on_all_test_events(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            time_start = datetime.now()
            data = instance.data.copy()
            if f.is_pytest_framework():
                test_fixtures = sorted(
                    filter(lambda x: x.get("event_started_at", None), data.pop("test_fixtures", {}).values()),
                    key=lambda x: x["event_started_at"],
                )
                data.update({"test_fixtures": test_fixtures})
            elif f.is_robot_framework():
                test_keywords = sorted(
                    filter(lambda x: x.get("event_started_at", None), data.pop("test_keywords", {}).values()),
                    key=lambda x: x["event_started_at"],
                )
                data.update({"test_keywords": test_keywords})
            elif f.is_behave_framework():
                raw_steps = data.pop("test_steps", [])
                if isinstance(raw_steps, dict):
                    raw_steps = raw_steps.values()
                test_steps = sorted(
                    filter(lambda x: isinstance(x, dict) and x.get("event_started_at", None), raw_steps),
                    key=lambda x: x["event_started_at"],
                )
                data.update({"test_steps": test_steps})
            if WebDriverTestModule.KEY_AUTOMATION_SESSIONS in data:
                data.pop(WebDriverTestModule.KEY_AUTOMATION_SESSIONS)
            instance.add_benchmark("json:test_fixtures", datetime.now() - time_start)
            time_start = datetime.now()
            event_json = dumps(data, cls=PytestJSONEncoder)
            instance.add_benchmark("json:on_all_test_events", datetime.now() - time_start)
            if TestFramework.KEY_TEST_UUID in data:
                self.send_test_framework_event(instance, hook_info, event_json=event_json)
            instance.add_benchmark("o11y:on_all_test_events", datetime.now() - o11y_time_start)
    def on_before_test(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.performance_tester import PerformanceTester
        random_label = PerformanceTester.mark_start(EVENTS.SDK_AUTOMATE_SESSION_ANNOTATION.value)
        self.automation_framework_test.mark_o11y_sync(instance, f, hook_info, *args, **kwargs)
        try:
            req = self.automation_framework_test.get_cbt_event(instance, f, hook_info, *args, **kwargs)
        except Exception as e:
            self.logger.error("on_before_test get_cbt_event failed: [{}] {}\n{}".format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not cached_robot_pw_binary_flow() and not f.is_behave_framework(): # CBT data not ready for robot-playwright and behave-playwright at the time of on_before_test, so we will send CBT event in on_after_test for both
            self.send_test_session_event(f, instance, req)
        else:
            pass  # CBT data not ready for robot-playwright and behave-playwright; deferred to on_after_test
        PerformanceTester.end(EVENTS.SDK_AUTOMATE_SESSION_ANNOTATION.value, random_label + ":start", random_label + ":end", status=True, failure=None, test_name=None)
    def on_after_test(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.get_state(instance, self.automation_framework_test.KEY_CBT_SESSION_CREATED, False):
            try:
                req = self.automation_framework_test.get_cbt_event(instance, f, hook_info, *args, **kwargs)
            except Exception as e:
                self.logger.error("on_after_test get_cbt_event failed: [{}] {}\n{}".format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.send_test_session_event(f, instance, req)
    @measure(event_name=EVENTS.SDK_TEST_SESSION_EVENT, stage=STAGE.SINGLE)
    def send_test_session_event(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug("Skipping TestSessionEvent gRPC call: No valid request data")
            return
        time_start = datetime.now()
        try:
            r = self.cli_service.TestSessionEvent(req)
            instance.add_benchmark("grpc:send_test_session_event", datetime.now() - time_start)
            f.set_state(
                instance,
                self.automation_framework_test.KEY_CBT_SESSION_CREATED,
                r.success and len(req.automation_sessions) > 0,
            )
            if not r.success:
                self.logger.info("received from server: {}".format(r))
        except grpc.RpcError as e:
            self.logger.error("rpc-error: " + str(e) + "")
            traceback.print_exc()
            raise e
    def on_after_execute(
        self,
        f: SeleniumFramework,
        _driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        _hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not SeleniumFramework.is_execute_request(method_name):
            return
        if f.parse_command_name(*args) == SeleniumFramework.COMMAND_SCREENSHOT:
            o11y_time_start = datetime.now()
            screenshot = result.get("value", None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning("invalid screenshot image base64 str")
                return
            test_instance = self.resolve_test_instance(instance)
            if test_instance:
                entry = LogEntry(TestFramework.KIND_SCREENSHOT, screenshot)
                self.send_log_created_event(test_instance, [entry])
                instance.add_benchmark("o11y:on_after_execute", datetime.now() - o11y_time_start)
            else:
                self.logger.warning("unable to determine test for which this screenshot was taken by driver= {}".format(instance.ref()))
        event = {}
        test_instance = self.resolve_test_instance(instance)
        if test_instance:
            self.process_test_level_and_build_level_attachment(event, test_instance)
            if event.get("logs"):
                self.send_log_created_event(test_instance, event["logs"])
            else:
                self.logger.debug("Unable to determine logs for attachment event")
    def on_after_create(
        self,
        f: SeleniumFramework,
        _driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        _hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        """SDK-6165: emit the CBT session-link at driver-create (CREATE, POST), idempotent via KEY_CBT_SESSION_CREATED."""
        instance = exec[0]
        try:
            if not is_bstack_automation():
                return
            test_instances = TestFramework.get_context_instances(instance.context)
            test_instance = next(
                (
                    t
                    for t in test_instances
                    if TestFramework.has_state(t, TestFramework.KEY_TEST_UUID)
                ),
                None,
            )
            if not test_instance:
                self.logger.debug(
                    "on_after_create: no running test to link Automate session to"
                )
                return
            if TestFramework.get_state(
                test_instance, self.automation_framework_test.KEY_CBT_SESSION_CREATED, False
            ):
                return
            hook_info = (TestFrameworkState.TEST, TestHookState.PRE)
            req = self.automation_framework_test.get_cbt_event(
                test_instance, TestFramework, hook_info
            )
            self.send_test_session_event(TestFramework, test_instance, req)
        except Exception as e:
            self.logger.error(
                "on_after_create CBT emission failed: [{}] {}\n{}".format(
                    type(e).__name__, e, traceback.format_exc()
                )
            )
    @measure(event_name=EVENTS.SDK_CLI_LOG_CREATED_EVENT, stage=STAGE.SINGLE)
    def send_log_created_event(
        self,
        test_instance: TestFrameworkTest,
        entries: List[LogEntry],
    ):
        self.ensure_bin_session()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.get_state(test_instance, TestFramework.KEY_PLATFORM_INDEX)
        req.client_worker_id = "{}-{}".format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(test_instance.context.hash)
        req.execution_context.thread_id = str(test_instance.context.thread_id)
        req.execution_context.process_id = str(test_instance.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_FRAMEWORK_NAME)
            log_entry.test_framework_version = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_FRAMEWORK_VERSION)
            log_entry.uuid = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_UUID)
            log_entry.test_framework_state = test_instance.state.name
            log_entry.message = entry.message.encode("utf-8")
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == "TEST_ATTACHMENT":
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.fileSize
                log_entry.file_path = entry.filePath
        def make_grpc_request():
            time_start = datetime.now()
            try:
                self.cli_service.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    test_instance.add_benchmark("grpc:send_log_created_event_screenshot", datetime.now() - time_start)
                elif entry.kind == TestFramework.KIND_ATTACHMENT:
                    test_instance.add_benchmark("grpc:send_log_created_event_attachment", datetime.now() - time_start)
                else:
                    test_instance.add_benchmark("grpc:send_log_created_event_log", datetime.now() - time_start)
            except grpc.RpcError as e:
                self.log_error("rpc-error: " + str(e))
                traceback.print_exc()
                raise e
        self.async_dispatcher.enqueue(make_grpc_request)
    @measure(event_name=EVENTS.SDK_TEST_FRAMEWORK_EVENT, stage=STAGE.SINGLE)
    def send_test_framework_event(
        self,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.ensure_bin_session()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.get_state(instance, TestFramework.KEY_PLATFORM_INDEX)
        req.client_worker_id = "{}-{}".format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_NAME)
        req.test_framework_version = TestFramework.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_VERSION)
        req.test_framework_state = hook_info[0].name
        req.test_hook_state = hook_info[1].name
        started_at = TestFramework.get_state(instance, TestFramework.KEY_TEST_STARTED_AT, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.get_state(instance, TestFramework.KEY_TEST_ENDED_AT, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=PytestJSONEncoder)).encode("utf-8")
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def make_grpc_request():
            time_start = datetime.now()
            try:
                self.cli_service.TestFrameworkEvent(req)
                elapsed = datetime.now() - time_start
                instance.add_benchmark("grpc:send_test_framework_event", elapsed)
            except grpc.RpcError as e:
                self.log_error("rpc-error: " + str(e))
                traceback.print_exc()
                raise e
        self.async_dispatcher.enqueue(make_grpc_request)
    def resolve_test_instance(self, instance: AutomationFrameworkBrowser):
        test_instances = TestFramework.get_context_instances(instance.context)
        for t in test_instances:
            driver_instances = TestFramework.get_state(t, WebDriverTestModule.KEY_AUTOMATION_SESSIONS, [])
            if not is_bstack_automation() and len(driver_instances) == 0:
                driver_instances = TestFramework.get_state(t, WebDriverTestModule.KEY_NON_BROWSERSTACK_AUTOMATION_SESSIONS, [])
            if any(instance is d[1] for d in driver_instances):
                return t
    def log_info(self, message):
        self.stdout_write(message + "\n")
    def log_error(self, message):
        self.stderr_write(message + "\n")
    def new_log_capture(self, level, original_func):
        def on_log_message(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if "EventDispatcherModule" in message or "[SDKCLI]" in message or "[WebDriverModule]" in message:
                        return return_value
                    test_instances = TestFramework.get_current_instances()
                    if not test_instances:
                        return return_value
                    test_instance = next(
                        (
                            instance
                            for instance in test_instances
                            if TestFramework.has_state(instance, TestFramework.KEY_TEST_UUID)
                        ),
                        None,
                    )
                    if not test_instance:
                        return return_value
                    entry = LogEntry(TestFramework.KIND_LOG, message, level)
                    self.send_log_created_event(test_instance, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return on_log_message
    def new_print_capture(self):
        def on_print(*args, **kwargs):
            try:
                self.orig_print(*args, **kwargs)
                if not args:
                    return
                message = ' '.join(str(arg) for arg in args)
                if not message.strip():
                    return
                if "EventDispatcherModule" in message:
                    return
                test_instances = TestFramework.get_current_instances()
                if not test_instances:
                    return
                test_instance = next(
                    (
                        instance
                        for instance in test_instances
                        if TestFramework.has_state(instance, TestFramework.KEY_TEST_UUID)
                    ),
                    None,
                )
                if not test_instance:
                    return
                entry = LogEntry(TestFramework.KIND_LOG, message, EventDispatcherModule.STDOUT_LOG_LEVEL)
                self.send_log_created_event(test_instance, [entry])
            except Exception as e:
                try:
                    self.orig_print(f"[EventDispatcherModule] Log capture error: {e}")
                except:
                    pass  # If even this fails, just continue silently
        return on_print
    def process_test_level_and_build_level_attachment(self, event: dict, instance=None) -> None:
        global _processed_attachments
        levels = ["TestLevel", "BuildLevel"]
        uuid_str = ""
        if instance is not None:
            try:
                uuid_str = TestFramework.get_state(instance, TestFramework.KEY_TEST_UUID)
            except Exception as e:
                self.logger.warning("Error getting uuid from instance".format(e))
        log_entries = []
        try:
            for level in levels:
                platform_index = os.environ['BROWSERSTACK_PLATFORM_INDEX']
                attachment_dir = os.path.join(BROWSERSTACK_ROOT_DIR, (UPLOADED_ATTACHMENTS_PREFIX + str(platform_index)), level)
                if not os.path.isdir(attachment_dir):
                    self.logger.debug("Directory not present for processing Test and Build level attachments {}".format(attachment_dir))
                    continue
                file_names = os.listdir(attachment_dir)
                for file_name in file_names:
                    file_path = os.path.join(attachment_dir, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _processed_attachments:
                        self.logger.info("Path already processed {}".format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            mod_time = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(mod_time, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == "TestLevel":
                                entry = LogEntry(
                                    kind="TEST_ATTACHMENT",
                                    message="",
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    fileSize=file_size,
                                    attachmentType="MANUAL_UPLOAD",
                                    filePath=os.path.abspath(file_path),
                                    test_run_uuid=uuid_str
                                )
                            elif level == "BuildLevel":
                                entry = LogEntry(
                                    kind="TEST_ATTACHMENT",
                                    message="",
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    fileSize=file_size,
                                    attachmentType="MANUAL_UPLOAD",
                                    filePath=os.path.abspath(file_path),
                                    build_run_uuid=uuid_str
                                )
                            log_entries.append(entry)
                            _processed_attachments.add(abs_path)
                        except Exception as file_err:
                            self.logger.error("Exception raised when processing attachments {}".format(file_err))
        except Exception as e:
            self.logger.error("Exception raised when processing attachments {}".format(e))
        event["logs"] = log_entries
class PytestJSONEncoder(JSONEncoder):
    def __init__(self, **kwargs):
        self.seen_ids = set()
        kwargs["skipkeys"] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return extract_to_dict(obj, self.seen_ids)
def is_primitive(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def extract_to_dict(obj, seen_ids=None, max_depth=3):
    if seen_ids is None:
        seen_ids = set()
    if id(obj) in seen_ids or max_depth <= 0:
        return None
    max_depth -= 1
    seen_ids.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    fqcn = TestFramework.object_fqcn(obj)
    pytest_prop = next((k.lower() in fqcn.lower() for k in PYTEST_PROPERTIES.keys()), None)
    if pytest_prop:
        obj = TestFramework.extract_keys(obj, PYTEST_PROPERTIES[pytest_prop])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, "__slots__"):
            keys = getattr(obj, "__slots__", [])
        elif hasattr(obj, "__dict__"):
            keys = getattr(obj, "__dict__", {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith("_")}
        if not obj and fqcn == "pathlib.PosixPath":
            obj = {"path": str(obj)}
    result = {}
    for key, value in obj.items():
        if not is_primitive(key) or str(key).startswith("_"):
            continue
        if value is not None and is_primitive(value):
            result[key] = value
        elif isinstance(value, dict):
            r = extract_to_dict(value, seen_ids, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [extract_to_dict(o, seen_ids, max_depth) for o in value]))
    return result or None
