"""Session bootstrap: options factory, local/cloud targets, verdict, teardown."""
import pytest

from testmu_appium import _config, _session
from testmu_appium._errors import TestmuConfigError, UnsupportedOnPlatform
from testmu_appium._helpers.driver import get_driver
from testmu_appium._session import build_options, run
from testmu_appium._step import step
from testmu_appium._test_state import reset_test_state


class _FakeDriver:
    def __init__(self):
        self.scripts = []
        self.quit_called = False
        self.capabilities = {"platformName": "Android", "platformVersion": "14"}

    def execute_script(self, script, *args):
        self.scripts.append(script)

    def update_settings(self, settings):
        self.settings = settings

    def quit(self):
        self.quit_called = True


@pytest.fixture
def created(monkeypatch):
    """Capture the Remote() call the session makes instead of starting a real one."""
    calls = {}
    driver = _FakeDriver()

    def _remote(command_executor=None, options=None, **kw):
        calls["url"] = command_executor
        calls["options"] = options
        return driver

    monkeypatch.setattr(_session.webdriver, "Remote", _remote)
    monkeypatch.setattr(_session.time, "sleep", lambda s: None)
    calls["driver"] = driver
    return calls


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    monkeypatch.delenv("NETWORK_PROFILE", raising=False)
    monkeypatch.delenv("DOWNLOAD_SPEED", raising=False)
    monkeypatch.delenv("UPLOAD_SPEED", raising=False)
    monkeypatch.delenv("LATENCY", raising=False)
    monkeypatch.setattr(_config, "run_target", "local")
    monkeypatch.setattr(_config, "lt_auth", False)
    monkeypatch.setattr(_config, "smart", False)
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setitem(_config._config, "app_id", "com.example.app")
    reset_test_state()
    yield
    reset_test_state()


class TestOptionsFactory:
    def test_android_options_carry_the_configured_identity(self, monkeypatch):
        monkeypatch.setitem(_config._config, "udid", "emulator-5554")
        monkeypatch.setitem(_config._config, "no_reset", True)
        options = build_options("android")
        caps = options.to_capabilities()
        assert caps["platformName"].lower() == "android"
        assert caps["appium:automationName"].lower() == "uiautomator2"
        assert caps["appium:appPackage"] == "com.example.app"
        assert caps["appium:udid"] == "emulator-5554"
        assert caps["appium:noReset"] is True

    def test_app_id_is_neutral_and_optional(self, monkeypatch):
        monkeypatch.setitem(_config._config, "app_id", "")
        caps = build_options("android").to_capabilities()
        assert "appium:appPackage" not in caps

    def test_custom_capabilities_are_merged(self, monkeypatch):
        monkeypatch.setitem(_config._config, "custom_capabilities",
                            {"appium:autoGrantPermissions": True})
        caps = build_options("android").to_capabilities()
        assert caps["appium:autoGrantPermissions"] is True

    def test_cloud_options_carry_lt_options(self, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setitem(_config._config, "build", "b1")
        monkeypatch.setitem(_config._config, "name", "n1")
        monkeypatch.setitem(_config._config, "device_name", "Pixel 8")
        monkeypatch.setitem(_config._config, "platform_version", "14")
        caps = build_options("android").to_capabilities()
        assert caps["LT:Options"]["build"] == "b1"
        assert caps["LT:Options"]["name"] == "n1"
        assert caps["LT:Options"]["deviceName"] == "Pixel 8"
        assert caps["LT:Options"]["platformVersion"] == "14"
        assert caps["LT:Options"]["isRealMobile"] is True

    @pytest.mark.parametrize(("platform", "option"), [
        ("android", "autoGrantPermissions"),
        ("ios", "autoAcceptAlerts"),
    ])
    def test_authored_fixed_options_override_swappable_test_config(
            self, monkeypatch, platform, option):
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setitem(_config._config, "platform", platform)
        monkeypatch.setitem(_config._config, "lt_options", {option: False})
        monkeypatch.setitem(_config._config, "lt_options_fixed", {option: True})

        lt_options = build_options(platform).to_capabilities()["LT:Options"]

        assert lt_options[option] is True

    def test_cloud_device_targeting_stays_out_of_the_appium_namespace(self, monkeypatch):
        """The LT allocator matches LT:Options.deviceName as a regex but an
        appium:deviceName literally — the V2 device-class regex there allocates
        nothing and the session dies on QUEUE_TIMEOUT_DEVICE_UNAVAILABLE."""
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setitem(_config._config, "device_name", "^(?!.*(Tab|Fold)).*")
        monkeypatch.setitem(_config._config, "platform_version", "16")
        monkeypatch.setitem(_config._config, "app", "lt://APP123")
        monkeypatch.setitem(_config._config, "udid", "RUNPICKED")
        monkeypatch.setitem(_config._config, "appium_version", "2.11.4-kane-ai")
        caps = build_options("android").to_capabilities()
        for cap in ("appium:deviceName", "appium:platformVersion", "appium:app", "appium:udid"):
            assert cap not in caps
        lt = caps["LT:Options"]
        assert lt["deviceName"] == "^(?!.*(Tab|Fold)).*"
        assert lt["platformVersion"] == "16"
        assert lt["app"] == "lt://APP123"
        assert lt["udid"] == "RUNPICKED"
        assert lt["appiumVersion"] == "2.11.4-kane-ai"

    def test_local_device_targeting_keeps_the_appium_namespace(self, monkeypatch):
        monkeypatch.setitem(_config._config, "device_name", "Pixel 8")
        monkeypatch.setitem(_config._config, "app", "/tmp/app.apk")
        caps = build_options("android").to_capabilities()
        assert caps["appium:deviceName"] == "Pixel 8"
        assert caps["appium:app"] == "/tmp/app.apk"

    def test_explicit_capability_dict_wins_outright(self, monkeypatch):
        monkeypatch.setitem(_config._config, "capability",
                            {"platformName": "Android", "appium:automationName": "UiAutomator2",
                             "appium:appPackage": "com.other"})
        caps = build_options("android").to_capabilities()
        assert caps["appium:appPackage"] == "com.other"

    def test_mjpeg_forward_is_requested_for_a_local_run(self, monkeypatch):
        """Appium creates the forward perception reads frames off."""
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_AUTO)
        caps = build_options("android").to_capabilities()
        assert caps["appium:mjpegServerPort"] == _config._DEFAULT_MJPEG_PORT

    def test_the_forwarded_mjpeg_port_is_configurable(self, monkeypatch):
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_AUTO)
        monkeypatch.setitem(_config._config, "mjpeg_port", 7999)
        assert build_options("android").to_capabilities()["appium:mjpegServerPort"] == 7999

    def test_a_cloud_session_asks_for_no_mjpeg_forward(self, monkeypatch):
        """The forward would land on LT's device host, where 127.0.0.1 does not reach
        it, so the cloud capability set is the one it was without this path."""
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_AUTO)
        assert "appium:mjpegServerPort" not in build_options("android").to_capabilities()

    def test_forcing_the_appium_screenshot_asks_for_no_forward(self, monkeypatch):
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_APPIUM)
        assert "appium:mjpegServerPort" not in build_options("android").to_capabilities()

    def test_forcing_mjpeg_asks_for_the_forward_on_any_target(self, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_MJPEG)
        assert "appium:mjpegServerPort" in build_options("android").to_capabilities()

    def test_an_explicit_capability_dict_gains_no_mjpeg_port(self, monkeypatch):
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_AUTO)
        monkeypatch.setitem(_config._config, "capability", {"platformName": "Android"})
        assert "appium:mjpegServerPort" not in build_options("android").to_capabilities()

    def test_ios_options_carry_the_configured_identity(self, monkeypatch):
        monkeypatch.setitem(_config._config, "udid", "00008030-000A49E40C08802E")
        monkeypatch.setitem(_config._config, "no_reset", True)
        options = build_options("ios")
        caps = options.to_capabilities()
        assert caps["platformName"].lower() == "ios"
        assert caps["appium:automationName"].lower() == "xcuitest"
        assert caps["appium:udid"] == "00008030-000A49E40C08802E"
        assert caps["appium:noReset"] is True

    def test_ios_options_do_not_wait_for_quiescence(self):
        """Two waits XCUITest inserts that an agent pays on EVERY step and
        needs on none — and that the driver-settings waitForIdleTimeout does
        NOT cover, being per-step where these are session-level."""
        caps = build_options("ios").to_capabilities()
        assert caps["appium:waitForQuiescence"] is False
        assert caps["appium:animationCoolOffTimeout"] == 0

    def test_app_id_lands_on_bundle_id_for_ios(self):
        """The SAME neutral `app_id` the Android row puts on appPackage.

        This is what keeps a recorded artifact platform-portable: one identity
        field, resolved to whichever capability the platform names it with.
        """
        caps = build_options("ios").to_capabilities()
        assert caps["appium:bundleId"] == "com.example.app"
        assert "appium:appPackage" not in caps

    def test_explicit_capability_dict_wins_outright_on_ios_too(self, monkeypatch):
        """The bare-options table has to cover every platform the factory table does.

        A platform present in one and missing from the other would derive fields
        over a host runtime's already-resolved capability dict.
        """
        monkeypatch.setitem(_config._config, "capability",
                            {"platformName": "iOS", "appium:automationName": "XCUITest",
                             "appium:bundleId": "com.other"})
        caps = build_options("ios").to_capabilities()
        assert caps["appium:bundleId"] == "com.other"
        assert "appium:noReset" not in caps

    def test_unknown_platform_raises(self):
        with pytest.raises(UnsupportedOnPlatform):
            build_options("tizen")


class TestRun:
    def test_initial_network_profile_is_applied_before_the_test_body(
            self, created, monkeypatch):
        from testmu_appium._helpers import network_throttle as throttle_module

        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setattr(_config, "lt_auth", True)
        monkeypatch.setenv("NETWORK_PROFILE", "4G-Advanced")
        monkeypatch.setattr(throttle_module.time, "sleep", lambda _: None)
        observed = {}

        def body(driver):
            observed["scripts"] = list(driver.scripts)

        run(body)

        assert "updateNetworkProfile=4G-Advanced" in observed["scripts"]

    def test_a_session_start_reprobes_the_mjpeg_stream(self, created, monkeypatch):
        """The stream's reachability belongs to the session about to start, not to the
        one that just ended."""
        from testmu_appium._helpers import _mjpeg

        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_AUTO)
        _mjpeg.mark_unreachable(RuntimeError("a previous session had no stream"))
        run(lambda driver: None)
        assert _mjpeg.usable()

    def test_local_target_connects_to_the_appium_server(self, created, monkeypatch):
        monkeypatch.setitem(_config._config, "appium_url", "http://127.0.0.1:4723")
        run(lambda driver: None)
        assert created["url"] == "http://127.0.0.1:4723"

    def test_cloud_target_connects_to_the_mobile_hub(self, created, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setattr(_config, "lt_auth", True)
        monkeypatch.setitem(_config._config, "lt_hub_url",
                            "https://mobile-hub.lambdatest.com/wd/hub")
        run(lambda driver: None)
        assert created["url"] == "https://mobile-hub.lambdatest.com/wd/hub"

    def test_the_driver_is_registered_for_the_test_body(self, created):
        seen = {}
        run(lambda driver: seen.update(registered=get_driver(), passed=driver))
        assert seen["registered"] is created["driver"]
        assert seen["passed"] is created["driver"]

    def test_the_registry_is_cleared_after_teardown(self, created):
        run(lambda driver: None)
        assert get_driver() is None

    def test_driver_is_always_quit(self, created):
        with pytest.raises(RuntimeError):
            run(lambda driver: (_ for _ in ()).throw(RuntimeError("body failed")))
        assert created["driver"].quit_called

    def test_passing_run_reports_the_passed_verdict(self, created, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setattr(_config, "lt_auth", True)
        run(lambda driver: None)
        assert "lambda-status=passed" in created["driver"].scripts

    def test_failing_run_reports_the_failed_verdict(self, created, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setattr(_config, "lt_auth", True)
        with pytest.raises(RuntimeError):
            run(lambda driver: (_ for _ in ()).throw(RuntimeError("boom")))
        assert "lambda-status=failed" in created["driver"].scripts

    def test_pending_fail_continue_failures_raise_at_session_end(self, created):
        def body(driver):
            with step("Tap Go", on_failure="fail-continue"):
                raise RuntimeError("swallowed")

        with pytest.raises(RuntimeError) as exc:
            run(body)
        assert "Tap Go" in str(exc.value)

    def test_pending_failures_report_the_failed_verdict(self, created, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setattr(_config, "lt_auth", True)

        def body(driver):
            with step("Tap Go", on_failure="fail-continue"):
                raise RuntimeError("swallowed")

        with pytest.raises(RuntimeError):
            run(body)
        assert "lambda-status=failed" in created["driver"].scripts

    def test_warn_continue_does_not_fail_the_session(self, created):
        def body(driver):
            with step("Tap Go", on_failure="warn-continue"):
                raise RuntimeError("warned")

        run(body)

    def test_step_counter_restarts_each_session(self, created):
        from testmu_appium._step import get_step_count

        def body(driver):
            with step("a"):
                pass

        run(body)
        run(body)
        assert get_step_count() == 1

    def test_prior_pending_failures_do_not_contaminate_a_new_session(self, created):
        def failing(driver):
            with step("Tap Go", on_failure="fail-continue"):
                raise RuntimeError("swallowed")

        with pytest.raises(RuntimeError):
            run(failing)
        run(lambda driver: None)


class TestSingleVerdictOwner:
    """run() emits exactly one pass_test/fail_test on every path.

    Counts, not membership: on the pending-failure path the RuntimeError raised right
    after fail_test must not be re-caught by the body's own except and reported again.
    """

    class _SpyReporter:
        def __init__(self):
            self.events = []

        def set_driver(self, driver): pass
        def begin_test(self, name): self.events.append("begin_test")
        def pass_test(self): self.events.append("pass_test")
        def fail_test(self, error): self.events.append("fail_test")
        def begin_step(self, description, instruction_id=None): pass

        def end_step(self, description, ok, error=None, instruction_id=None,
                     is_autohealed=False, autoheal_source="", interacted_element=None):
            pass

        def warn_step(self, description, error): pass
        def attach_screenshot(self, data): pass

        def verdicts(self):
            return [e for e in self.events if e in ("pass_test", "fail_test")]

    @pytest.fixture
    def spy(self, monkeypatch):
        reporter = self._SpyReporter()
        monkeypatch.setattr(_session, "reporter", lambda: reporter)
        import testmu_appium._step as step_mod
        monkeypatch.setattr(step_mod, "reporter", lambda: reporter)
        return reporter

    def test_a_passing_run_emits_one_pass(self, created, spy):
        run(lambda driver: None)
        assert spy.verdicts() == ["pass_test"]

    def test_a_raising_body_emits_one_fail(self, created, spy):
        with pytest.raises(RuntimeError):
            run(lambda driver: (_ for _ in ()).throw(RuntimeError("boom")))
        assert spy.verdicts() == ["fail_test"]

    def test_pending_failures_emit_one_fail_not_two(self, created, spy):
        def body(driver):
            with step("Tap Go", on_failure="fail-continue"):
                raise RuntimeError("swallowed")

        with pytest.raises(RuntimeError):
            run(body)
        assert spy.verdicts() == ["fail_test"]

    def test_several_pending_failures_still_emit_one_fail(self, created, spy):
        def body(driver):
            for label in ("Tap Go", "Tap Next", "Tap Done"):
                with step(label, on_failure="fail-continue"):
                    raise RuntimeError("swallowed")

        with pytest.raises(RuntimeError):
            run(body)
        assert spy.verdicts() == ["fail_test"]

    def test_a_warn_continue_run_emits_one_pass(self, created, spy):
        def body(driver):
            with step("Tap Go", on_failure="warn-continue"):
                raise RuntimeError("warned")

        run(body)
        assert spy.verdicts() == ["pass_test"]

    def test_a_decorated_body_does_not_add_a_second_verdict(self, created, spy):
        """The shape codegen emits: @test on the body, invoked through run()."""
        from testmu_appium._decorator import test as testmu_test

        @testmu_test
        def body(driver):
            pass

        run(body)
        assert spy.verdicts() == ["pass_test"]

    def test_a_decorated_failing_body_emits_one_fail(self, created, spy):
        from testmu_appium._decorator import test as testmu_test

        @testmu_test
        def body(driver):
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError):
            run(body)
        assert spy.verdicts() == ["fail_test"]

    def test_a_teardown_failure_does_not_add_a_verdict(self, created, spy, monkeypatch):
        def _boom():
            raise RuntimeError("quit failed")

        monkeypatch.setattr(created["driver"], "quit", _boom)
        run(lambda driver: None)
        assert spy.verdicts() == ["pass_test"]

    def test_the_body_exception_wins_over_the_pending_summary(self, created, spy):
        """A body that both records a fail-continue AND raises reports the raise: its
        class and message are more specific than the aggregate."""

        def body(driver):
            with step("Tap Go", on_failure="fail-continue"):
                raise RuntimeError("swallowed")
            raise ValueError("the real failure")

        with pytest.raises(ValueError):
            run(body)
        assert spy.verdicts() == ["fail_test"]


class TestSmartGate:
    """Smart without LT auth is fatal on cloud, degraded locally."""

    @pytest.fixture(autouse=True)
    def _undegrade(self):
        _config._set_smart_degraded(False)
        yield
        _config._set_smart_degraded(False)

    def test_cloud_without_auth_fails_fast(self, created, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.setattr(_config, "smart", True)
        with pytest.raises(TestmuConfigError):
            run(lambda driver: None)
        assert "url" not in created, "the session must not start"

    def test_local_without_auth_warns_and_degrades(self, created, monkeypatch, caplog):
        import logging

        caplog.set_level(logging.WARNING, logger="testmu_appium")
        monkeypatch.setattr(_config, "run_target", "local")
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.setattr(_config, "smart", True)
        run(lambda driver: None)
        assert _config.smart_enabled() is False
        assert "smart" in caplog.text.lower()

    def test_the_degrade_does_not_survive_into_the_next_run(self, created, monkeypatch):
        """The degrade is scoped to one session, so a later run in the same process
        that does have credentials still gets smart features."""
        monkeypatch.setattr(_config, "run_target", "local")
        monkeypatch.setattr(_config, "smart", True)

        monkeypatch.setattr(_config, "lt_auth", False)
        run(lambda driver: None)
        assert _config.smart_enabled() is False

        monkeypatch.setattr(_config, "lt_auth", True)
        run(lambda driver: None)
        assert _config.smart_enabled() is True

    def test_the_configured_flag_is_never_mutated_by_the_gate(self, created, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "local")
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.setattr(_config, "smart", True)
        run(lambda driver: None)
        assert _config.smart is True, "the gate degrades the session, not the config"

    def test_cloud_with_auth_is_fine(self, created, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "cloud")
        monkeypatch.setattr(_config, "lt_auth", True)
        monkeypatch.setattr(_config, "smart", True)
        run(lambda driver: None)
        assert created["url"]

    def test_a_degrade_left_over_from_a_prior_run_is_cleared_at_session_start(
        self, created, monkeypatch
    ):
        _config._set_smart_degraded(True)
        monkeypatch.setattr(_config, "run_target", "local")
        monkeypatch.setattr(_config, "lt_auth", True)
        monkeypatch.setattr(_config, "smart", True)
        run(lambda driver: None)
        assert _config.smart_enabled() is True


class TestSmartVariableSeeding:
    """`{{smart.device_os}}` and its siblings are session facts. A standalone
    test has no runtime to hand them over, so the session itself records them
    — and it has to happen before the body runs, not after."""

    def test_run_seeds_the_device_names_before_the_body(self, created, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "ios")
        monkeypatch.setitem(_config._config, "app_id", "com.example.app")
        created["driver"].capabilities = {"platformVersion": "18.2"}
        seen = {}

        def _body(driver):
            from testmu_appium._vars import var
            seen["device_os"] = var("{{smart.device_os}}")
            seen["app_package_name"] = var("{{smart.app_package_name}}")
            seen["device_os_version"] = var("{{smart.device_os_version}}")

        run(_body)
        assert seen == {"device_os": "ios",
                        "app_package_name": "com.example.app",
                        "device_os_version": "18.2"}
