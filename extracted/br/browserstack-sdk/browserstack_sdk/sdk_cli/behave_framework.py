import os
import threading
import traceback
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.tracked_instance import TrackedInstance
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    TestFrameworkTest,
    TestHookState,
    TestFrameworkContext,
    LogEntry,
)
from browserstack_sdk.sdk_cli.async_dispatcher import AsyncDispatcher
from browserstack_sdk.sdk_cli.utils.custom_tag_manager import CustomTagManager
class BehaveFramework(TestFramework):
    """
    Behave-specific TestFramework implementation for Observability (O11y) tracking.
    Lifecycle mapping (mirrors robot_listener_playwright.py pattern):
        start_test  -> INIT_TEST.PRE (register) + TEST.PRE (fire TestRunStarted)
        end_test    -> TEST.POST (fire TestRunFinished) + LOG_REPORT.POST (load result)
        start_step  -> STEP.PRE
        end_step    -> STEP.POST
        start_hook  -> BEFORE_EACH.PRE / BEFORE_ALL.PRE
        end_hook    -> AFTER_EACH.POST / AFTER_ALL.POST
    Instance resolution:
        - INIT_TEST: derive target from behave context (context.scenario + feature)
        - TEST/LOG: same derivation from context object
        - STEP: target passed via kwargs['scenario_target'] (stored on thread by listener)
        - Hooks: same derivation from context object, or kwargs['scenario_target']
    Tracking key format: "{feature.filename}::{scenario.name}::{scenario.line}"
        This is unique across: multiple features, scenario outlines, retries, parallel shards.
    """
    KEY_STEPS = "test_steps"
    KEY_HOOKS_STARTED = "test_hooks_started"
    KEY_HOOKS_FINISHED = "test_hooks_finished"
    KEY_HOOK_LAST_STARTED = "test_hook_last_started"
    KEY_HOOK_LAST_FINISHED = "test_hook_last_finished"
    hook_events = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        test_framework_versions: Dict[str, str],
        test_frameworks: List[str] = ["behave"],
        async_dispatcher: AsyncDispatcher = None,
        cli_service=None,
    ):
        super().__init__(test_frameworks, test_framework_versions, async_dispatcher)
        self.is_behave = any("behave" in item.lower() for item in test_frameworks)
        self.cli_service = cli_service
        self.logger.info("BehaveFramework initialized (frameworks={})".format(test_frameworks))
    def track_event(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(
                "ignored callback state={} hook={}".format(test_framework_state, test_hook_state)
            )
            return
        if not self.is_behave:
            self.logger.warning(
                "track_event: unsupported framework={}".format(self.test_frameworks)
            )
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(
                "track_event: unexpected args={} kwargs={}".format(args, kwargs)
            )
            return
        instance = self.__resolve_instance(
            context, test_framework_state, test_hook_state, *args, **kwargs
        )
        if not instance:
            self.logger.debug(
                "track_event: unhandled event={}.{} args={}".format(
                    test_framework_state, test_hook_state, args
                )
            )
            return
        try:
            if not TestFramework.has_state(instance, TestFramework.KEY_TEST_ID) and test_hook_state == TestHookState.PRE:
                test_data = BehaveFramework.__parse_behave_test(args[0])
                if test_data:
                    instance.data.update(test_data)
                    if context.platform_index >= 0:
                        id_suffix = "::[platform_{}]".format(context.platform_index)
                        for key in [TestFramework.KEY_TEST_ID, TestFramework.KEY_TEST_RERUN_NAME]:
                            val = instance.data.get(key, '')
                            if val and '::[platform_' not in val:
                                instance.data[key] = val + id_suffix
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE:
                    if not TestFramework.has_state(instance, TestFramework.KEY_TEST_STARTED_AT):
                        TestFramework.set_state(
                            instance,
                            TestFramework.KEY_TEST_STARTED_AT,
                            datetime.now(tz=timezone.utc),
                        )
                elif test_hook_state == TestHookState.POST:
                    if not TestFramework.has_state(instance, TestFramework.KEY_TEST_ENDED_AT):
                        TestFramework.set_state(
                            instance,
                            TestFramework.KEY_TEST_ENDED_AT,
                            datetime.now(tz=timezone.utc),
                        )
            elif (
                test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
            ):
                self.__load_test_result(instance, *args)
                self.__load_custom_tags(instance)
            elif test_framework_state == TestFrameworkState.STEP:
                self.__track_step_event(instance, test_hook_state, *args, **kwargs)
            elif test_framework_state in BehaveFramework.hook_events:
                self.__track_hook_event(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(
                "track_event: handled event={}.{} instance={}".format(
                    test_framework_state, test_hook_state, instance.ref()
                )
            )
        except Exception as e:
            self.logger.error("track_event error: {}".format(e))
            traceback.print_exc()
        self.run_hooks(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        return instance
    def __resolve_instance(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        """
        Resolve or create the TrackedInstance for the current scenario.
        Tracking key: "{feature.filename}::{scenario.name}::{scenario.line}::{platform_index}"
        Multi-platform safety: Include platform_index (if >= 0) to ensure each platform 
        gets a unique test instance. This prevents O11y deduplication when running the same 
        scenario across multiple platforms (Chrome, Edge, Firefox, etc.).
        Resolution order:
          1. kwargs['scenario_target'] - explicit target from step events
          2. args[0] is a string - direct target (rarely used)
          3. args[0] is behave context (has .scenario attribute)
          4. args[0] is behave scenario object directly (has .filename + .feature)
        """
        target = None
        if "scenario_target" in kwargs:
            target = kwargs["scenario_target"]
        elif args:
            arg0 = args[0]
            if isinstance(arg0, str):
                target = arg0
            elif hasattr(arg0, "scenario") and hasattr(arg0.scenario, "name"):
                sc = arg0.scenario
                try:
                    target = "{}::{}::{}".format(
                        sc.feature.filename if hasattr(sc, "feature") and sc.feature else "",
                        sc.name,
                        str(sc.line),
                    )
                except Exception:
                    target = "::{}".format(sc.name)
            elif hasattr(arg0, "filename") and hasattr(arg0, "feature"):
                sc = arg0
                try:
                    target = "{}::{}::{}".format(
                        sc.feature.filename if sc.feature else "",
                        sc.name,
                        str(sc.line),
                    )
                except Exception:
                    target = "::{}".format(sc.name)
        if not target:
            self.logger.debug(
                "resolve_instance: no target for {}.{}".format(
                    test_framework_state, test_hook_state
                )
            )
            return None
        if context.platform_index >= 0:
            target = "{}::[platform_{}]".format(target, context.platform_index)
        if test_framework_state == TestFrameworkState.INIT_TEST:
            if not TestFramework.get_tracked_instance(target, strict=False):
                self.__track_behave_test(context, test_framework_state, target, *args)
        instance = TestFramework.get_tracked_instance(target, strict=False)
        if not instance:
            self.logger.debug(
                "resolve_instance: no instance found for target={} state={}.{}".format(
                    target, test_framework_state, test_hook_state
                )
            )
        return instance
    def __track_behave_test(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        target: str,
        *args,
    ):
        """Create and register a new TrackedInstance for a Behave scenario."""
        ctx = TrackedInstance.create_context(target)
        ob = TestFrameworkTest(
            ctx,
            self.test_frameworks,
            self.test_framework_versions,
            test_framework_state,
        )
        TestFramework.set_state_entries(ob, {
            TestFramework.KEY_TEST_FRAMEWORK_NAME: context.test_framework_name,
            TestFramework.KEY_TEST_FRAMEWORK_VERSION: context.test_framework_version,
            TestFramework.KEY_TEST_LOGS: [],
            BehaveFramework.KEY_STEPS: [],
            BehaveFramework.KEY_HOOKS_STARTED: {},
            BehaveFramework.KEY_HOOKS_FINISHED: {},
        })
        if context.platform_index >= 0:
            TestFramework.set_state(ob, TestFramework.KEY_PLATFORM_INDEX, context.platform_index)
        TestFramework.instances[ctx.id] = ob
        self.logger.debug(
            "track_behave_test: saved instance ctx.id={} target={}".format(ctx.id, target)
        )
        return ob
    @staticmethod
    def __parse_behave_test(arg0) -> Dict:
        """
        Extract test metadata from a Behave context or scenario object.
        KEY_TEST_UUID: uuid4() - unique per execution (required for retry/outline safety)
        KEY_TEST_ID:   file::name::line - stable scenario identifier
        KEY_TEST_NAME: scenario.name - display name
        """
        try:
            if hasattr(arg0, "scenario") and hasattr(arg0.scenario, "name"):
                scenario = arg0.scenario
                feature = getattr(arg0, "feature", None) or getattr(scenario, "feature", None)
            elif hasattr(arg0, "filename") and hasattr(arg0, "feature"):
                scenario = arg0
                feature = arg0.feature
            else:
                return {}
            feature_name = feature.name if feature else "Unknown"
            feature_filename = ""
            if feature:
                feature_filename = getattr(feature, "filename", "") or ""
            tags = list(scenario.tags) if hasattr(scenario, "tags") else []
            test_id = "{}::{}::{}".format(feature_filename, scenario.name, str(scenario.line))
            return {
                TestFramework.KEY_TEST_UUID:             str(uuid4()),       # unique per execution
                TestFramework.KEY_TEST_ID:               test_id,            # stable identifier
                TestFramework.KEY_TEST_NAME:             scenario.name,      # display name
                TestFramework.KEY_TEST_RERUN_NAME:       test_id,
                TestFramework.KEY_TEST_FILE_PATH:        feature_filename,
                TestFramework.KEY_TEST_LOCATION:         feature_filename,   # REQUIRED BY BINARY
                TestFramework.KEY_TEST_TAGS:             tags,
                TestFramework.KEY_TEST_RESULT:           TestFramework.DEFAULT_TEST_RESULT,
                TestFramework.KEY_AUTOMATE_SESSION_NAME: scenario.name,
                TestFramework.KEY_TEST_SCOPES:           [feature_name],
                TestFramework.KEY_TEST_META: {                               # REQUIRED BY BINARY
                    "feature": {
                        "name": feature_name,
                        "description": getattr(feature, "description", []) if feature else [],
                    },
                    "scenario": {
                        "name": scenario.name,
                    },
                    "steps": []
                },
            }
        except Exception as e:
            return {}
    def __load_test_result(self, instance: TestFrameworkTest, *args):
        """Load Behave scenario result into TestFrameworkTest instance."""
        arg0 = args[0] if args else None
        if not arg0:
            return
        if hasattr(arg0, "scenario"):
            scenario = arg0.scenario
        elif hasattr(arg0, "status"):
            scenario = arg0
        else:
            return
        failure = None
        failure_type = None
        try:
            raw_status = scenario.status.name.lower() if (
                hasattr(scenario, "status") and scenario.status
            ) else "unknown"
        except Exception:
            raw_status = "unknown"
        if raw_status == "error":
            raw_status = "failed"
        test_result = {
            "passed": "passed",
            "failed": "failed",
            "skipped": "skipped",
        }.get(raw_status, TestFramework.DEFAULT_TEST_RESULT)
        if test_result == "failed":
            exception = getattr(scenario, "exception", None)
            exc_traceback = getattr(scenario, "exc_traceback", None)
            if exception:
                try:
                    tb_lines = traceback.format_exception(
                        type(exception), exception, exc_traceback
                    )
                    failure = [{"backtrace": tb_lines}]
                    failure_type = type(exception).__name__
                except Exception:
                    failure = [{"backtrace": [str(exception)]}]
                    failure_type = "Exception"
        if test_result != TestFramework.DEFAULT_TEST_RESULT:
            TestFramework.set_state(
                instance, TestFramework.KEY_TEST_RESULT_AT, datetime.now(tz=timezone.utc)
            )
        TestFramework.set_state_entries(instance, {
            TestFramework.KEY_TEST_FAILURE:      failure,
            TestFramework.KEY_TEST_FAILURE_TYPE: failure_type,
            TestFramework.KEY_TEST_RESULT:       test_result,
        })
        self.logger.debug(
            "load_test_result: result={} instance={}".format(test_result, instance.ref())
        )
    def __load_custom_tags(self, instance: TestFrameworkTest):
        """Snapshot custom metadata onto the scenario, then reset CustomTagManager
        so tags do not leak into the next behave scenario. Matches the
        snapshot-then-reset discipline of pytest/robot/pytest-bdd; the reset MUST
        run after every scenario (not only when tags were set) since
        CustomTagManager holds process-global state."""
        try:
            custom_tags = CustomTagManager.get_test_level_custom_metadata()
            TestFramework.set_state(instance, TestFramework.KEY_CUSTOM_TAGS, custom_tags)
            CustomTagManager.reset_test_level_custom_metadata()
        except Exception as e:
            self.logger.debug("load_custom_tags failed: {}".format(e))
    def __track_step_event(
        self,
        instance: TestFrameworkTest,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        """Track Behave BDD step (Given / When / Then) lifecycle."""
        try:
            steps = TestFramework.get_state(instance, BehaveFramework.KEY_STEPS, [])
            step = args[0] if args else None
            if not step:
                return
            step_keyword = getattr(step, "keyword", "Step")
            step_name = getattr(step, "name", "")
            if test_hook_state == TestHookState.PRE:
                steps.append({
                    "keyword": step_keyword,
                    "name": step_name,
                    TestFramework.KEY_EVENT_STARTED_AT: datetime.now(tz=timezone.utc),
                    "status": "pending",
                })
            elif test_hook_state == TestHookState.POST and steps:
                last_step = steps[-1]
                if last_step.get("name") == step_name:
                    raw_status = getattr(
                        getattr(step, "status", None), "name", "unknown"
                    ).lower()
                    if raw_status == "error":
                        raw_status = "failed"
                    last_step["status"] = {
                        "passed": "passed", "failed": "failed", "skipped": "skipped"
                    }.get(raw_status, "pending")
                    if TestFramework.KEY_EVENT_STARTED_AT in last_step:
                        start_time = last_step[TestFramework.KEY_EVENT_STARTED_AT]
                        duration_ms = int((datetime.now(tz=timezone.utc) - start_time).total_seconds() * 1000)
                        last_step["duration_in_ms"] = duration_ms
                    last_step[TestFramework.KEY_EVENT_ENDED_AT] = datetime.now(tz=timezone.utc)
            TestFramework.set_state(instance, BehaveFramework.KEY_STEPS, steps)
            test_meta = TestFramework.get_state(instance, TestFramework.KEY_TEST_META, {})
            if isinstance(test_meta, dict):
                test_meta["steps"] = steps
                TestFramework.set_state(instance, TestFramework.KEY_TEST_META, test_meta)
        except Exception as e:
            self.logger.debug("track_step_event error: {}".format(e))
    def __track_hook_event(
        self,
        instance: TestFrameworkTest,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        """
        Track Behave hook lifecycle (before_scenario, after_scenario, etc.).
        Stores hooks in test_hooks_started / test_hooks_finished using the same
        structure as robot_framework.py so the binary translator can read them.
        Key is TestFrameworkState.name (e.g. 'BEFORE_EACH').
        """
        key = test_framework_state.name
        hooks_started = TestFramework.get_state(
            instance, BehaveFramework.KEY_HOOKS_STARTED, {}
        )
        if key not in hooks_started:
            hooks_started[key] = []
        hooks_finished = TestFramework.get_state(
            instance, BehaveFramework.KEY_HOOKS_FINISHED, {}
        )
        if key not in hooks_finished:
            hooks_finished[key] = []
        updates = {
            BehaveFramework.KEY_HOOKS_STARTED:  hooks_started,
            BehaveFramework.KEY_HOOKS_FINISHED: hooks_finished,
        }
        arg0 = args[0] if args else None
        hook_name = getattr(arg0, "name", "") if arg0 else ""
        if test_hook_state == TestHookState.PRE:
            hook = {
                "key":                          key,
                TestFramework.KEY_HOOK_ID:      str(uuid4()),
                TestFramework.KEY_HOOK_RESULT:  TestFramework.DEFAULT_HOOK_RESULT,
                TestFramework.KEY_EVENT_STARTED_AT: datetime.now(tz=timezone.utc),
                TestFramework.KEY_HOOK_LOGS:    [],
                TestFramework.KEY_HOOK_NAME:    hook_name,
                TestFramework.KEY_CUSTOM_TAGS:  CustomTagManager.get_test_level_custom_metadata(),
            }
            hooks_started[key].append(hook)
            updates[BehaveFramework.KEY_HOOK_LAST_STARTED] = key
        elif test_hook_state == TestHookState.POST:
            hooks_list = hooks_started.get(key, [])
            hook = hooks_list.pop() if hooks_list else None
            if hook:
                hook_result = "passed"
                if arg0 and getattr(arg0, "error_message", None):
                    hook_result = "failed"
                elif arg0 and getattr(arg0, "exc_traceback", None):
                    hook_result = "failed"
                hook[TestFramework.KEY_HOOK_RESULT]     = hook_result
                hook[TestFramework.KEY_EVENT_ENDED_AT]  = datetime.now(tz=timezone.utc)
                hook[TestFramework.KEY_CUSTOM_TAGS]     = CustomTagManager.get_test_level_custom_metadata()
                hooks_finished[key].append(hook)
                updates[BehaveFramework.KEY_HOOK_LAST_FINISHED] = key
        TestFramework.set_state_entries(instance, updates)
        self.logger.debug(
            "track_hook_event: {}.{} hooks_started={} hooks_finished={}".format(
                key, test_hook_state, hooks_started, hooks_finished
            )
        )
    def get_log_entries(
        self, instance: TestFrameworkTest, hook_info: Tuple[TestFrameworkState, TestHookState]
    ):
        """Return accumulated log entries for this test instance."""
        entries = []
        entries.extend(TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, []))
        return entries
    def clear_logs(
        self, instance: TestFrameworkTest, hook_info: Tuple[TestFrameworkState, TestHookState]
    ):
        """Clear accumulated log entries."""
        TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, []).clear()
    def is_behave_framework(self) -> bool:
        return True
    def is_pytest_framework(self) -> bool:
        return False
    def is_robot_framework(self) -> bool:
        return False
