"""The platform-keyed operation-adapter seam.

Every platform-specific operation resolves through a registry row, and activating
a platform is filling its row — never editing a call site.

The ios rows are now filled for every domain except `picker`, whose modes are
genuinely different machinery. Three individual operations stay absent BY DESIGN
rather than unfinished, and each is asserted below: there is no iOS paste key, no
notification shade, and no system back key.
"""
import pytest
from appium.options.android import UiAutomator2Options

from testmu_appium import _config, _vars
from testmu_appium._action_select import _Target
from testmu_appium._errors import PickerModeNotSupported, UnsupportedOnPlatform
from testmu_appium._helpers import _adapters, _keys, gesture, picker
from testmu_appium._helpers.clipboard import set_clipboard
from testmu_appium._helpers.device_control import device_control
from testmu_appium._helpers.navigate import navigate
from testmu_appium._session import build_options


class _Focus:
    def __init__(self, sink):
        self._sink = sink

    def send_keys(self, text):
        self._sink.append(str(text))


class _SwitchTo:
    def __init__(self, sink):
        self.active_element = _Focus(sink)


class _FakeDriver:
    def __init__(self):
        self.scripts = []
        self.pressed = []
        self.clipboard_writes = []
        self.hid_keyboard_calls = 0
        self.opened_notifications = 0
        self.actions = []
        self.typed = []
        self.switch_to = _SwitchTo(self.typed)

    def execute(self, command, params=None):
        """The W3C actions channel — where ActionBuilder.perform() lands."""
        self.actions.append((command, params))
        return {"value": None}

    def execute_script(self, script, payload):
        self.scripts.append((script, payload))

    def press_keycode(self, code):
        self.pressed.append(code)

    def set_clipboard_text(self, text):
        self.clipboard_writes.append(text)

    def hide_keyboard(self):
        self.hid_keyboard_calls += 1

    def open_notifications(self):
        self.opened_notifications += 1


@pytest.fixture(autouse=True)
def _clear_vars():
    yield
    _vars.clear_state()


class TestSeam:
    def test_an_undeclared_platform_raises_with_feature_and_platform(self, monkeypatch):
        monkeypatch.setattr(_adapters, "_REGISTRIES", {})
        _adapters.register("domain", {"android": {"op": lambda: None}})
        with pytest.raises(UnsupportedOnPlatform) as exc:
            _adapters.adapter("domain", "op", "the feature", platform="tizen")
        assert "the feature" in str(exc.value)
        assert "tizen" in str(exc.value)

    def test_a_declared_empty_row_raises_on_every_operation(self, monkeypatch):
        monkeypatch.setattr(_adapters, "_REGISTRIES", {})
        _adapters.register("domain", {"android": {"op": lambda: None}, "ios": {}})
        with pytest.raises(UnsupportedOnPlatform) as exc:
            _adapters.adapter("domain", "op", "the feature", platform="ios")
        assert "the feature" in str(exc.value)
        assert "ios" in str(exc.value)

    def test_register_merges_rows_per_platform(self, monkeypatch):
        monkeypatch.setattr(_adapters, "_REGISTRIES", {})
        first, second = object(), object()
        _adapters.register("domain", {"android": {"a": first}, "ios": {}})
        _adapters.register("domain", {"android": {"b": second}})
        assert _adapters.adapter("domain", "a", "f", platform="android") is first
        assert _adapters.adapter("domain", "b", "f", platform="android") is second
        with pytest.raises(UnsupportedOnPlatform):
            _adapters.adapter("domain", "a", "f", platform="ios")

    def test_the_default_platform_is_the_configured_one(self, monkeypatch):
        monkeypatch.setattr(_adapters, "_REGISTRIES", {})
        monkeypatch.setitem(_config._config, "platform", "android")
        sentinel = object()
        _adapters.register("domain", {"android": {"op": sentinel}})
        assert _adapters.adapter("domain", "op", "f") is sentinel

    #: registry → the operations each platform row ships. An operation present on
    #: android and absent on ios is a capability iOS does not have, never a gap.
    OWNED = {
        "gesture": ({"tap", "type_text", "long_press", "scroll_area",
                     "scroll_element", "scroll_travel", "scrollable_containers",
                     "drag", "click_target"},
                    {"tap", "type_text", "long_press", "scroll_area",
                     "scroll_element", "scroll_travel", "drag", "click_target"}),
        "key_dispatch": ({"press"}, {"press"}),
        "deeplink": ({"open"}, {"open"}),
        "geolocation": ({"set"}, set()),
        # device_control is deliberately absent: its platform seam moved into
        # the KINDS registry (device_control.py), whose own tests pin the
        # per-platform rows and the declared iOS gaps.
        # No iOS paste: no paste key exists, and cmd+V needs a hardware keyboard.
        "clipboard": ({"set_text", "paste", "clear"}, {"set_text", "clear"}),
        "session_options": ({"derive", "blank"}, {"derive", "blank"}),
        "picker": ({"modes", "list_id", "mode_classes", "default_mode",
                    "value_attributes", "class_attributes"},
                   {"modes", "list_id", "mode_classes", "default_mode",
                    "value_attributes", "class_attributes"}),
    }

    def test_the_shipped_registries_declare_both_platform_rows(self):
        for registry, (android, ios) in self.OWNED.items():
            assert set(_adapters._REGISTRIES[registry]["android"]) == android
            assert set(_adapters._REGISTRIES[registry]["ios"]) == ios

    #: Operations android serves and iOS does not, each because the platform has
    #: no counterpart. Every entry is a decision with a test of its own below.
    BY_DESIGN_ABSENT = {
        ("clipboard", "paste"),          # no paste key; cmd+V needs a keyboard
    }

    #: Operations not yet ported, as opposed to deliberately absent ones. The
    #: scroll path treats a missing container lookup as "no containers on
    #: screen", so iOS degrades to swiping the window area rather than failing.
    UNPORTED = {
        ("gesture", "scrollable_containers"),
        # XCUITest's location route not written yet; Android ships first.
        ("geolocation", "set"),
    }

    def test_no_registry_quietly_loses_ios(self):
        """The coverage guard, and the reason it exists.

        Three iOS rows were found empty by running this comparison by hand rather
        than by any test — foreground_app, and both screenshot_scaling entries.
        Each was a registry added after the iOS work began, so nothing pointed at
        it. A new registry now fails here until its ios row is filled or its
        absence is declared above.
        """
        gaps = set()
        for registry, row in _adapters._REGISTRIES.items():
            android = set(row.get("android", {}))
            ios = set(row.get("ios", {}))
            gaps |= {(registry, op) for op in android - ios}
        gaps -= self.UNPORTED
        assert gaps == self.BY_DESIGN_ABSENT, (
            f"undeclared iOS gaps: {sorted(gaps - self.BY_DESIGN_ABSENT)}")


class TestAndroidRowsDispatch:
    """One representative operation per domain, pinned against the driver call."""

    @pytest.fixture(autouse=True)
    def _android(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "android")

    def test_gesture_tap_runs_the_click_gesture_script(self):
        driver = _FakeDriver()
        gesture.tap(driver, 10.9, 20.2)
        assert driver.scripts == [("mobile: clickGesture", {"x": 10, "y": 20})]

    def test_key_dispatch_presses_the_resolved_keycode(self):
        driver = _FakeDriver()
        assert _keys.dispatch(driver, "ENTER", "android") == 66
        assert driver.pressed == [66]

    def test_deeplink_runs_the_deep_link_script_with_the_package(self, monkeypatch):
        monkeypatch.setitem(_config._config, "app_id", "com.example.app")
        driver = _FakeDriver()
        navigate(driver, "myapp://checkout/1")
        assert driver.scripts == [
            ("mobile: deepLink", {"url": "myapp://checkout/1", "package": "com.example.app"})
        ]

    def test_device_control_hide_keyboard_calls_the_driver(self):
        driver = _FakeDriver()
        device_control(driver, "hide_keyboard")
        assert driver.hid_keyboard_calls == 1

    def test_clipboard_set_text_writes_the_resolved_value(self):
        driver = _FakeDriver()
        set_clipboard(driver, "copied text")
        assert driver.clipboard_writes == ["copied text"]

    def test_session_blank_options_row_is_the_android_options_class(self):
        blank = _adapters.adapter(
            "session_options", "blank", "session options", platform="android"
        )
        assert blank is UiAutomator2Options


class _ScrollTarget:
    """An element both platform rows can act on.

    Android names it by id and iOS swipes over the box it occupies, so a bare
    object() only survived while iOS refused before reaching the element.
    """

    id = "elem-1"
    rect = {"x": 0, "y": 100, "width": 400, "height": 400}


#: Every gesture verb, with the feature name its raise carries.
GESTURE_CALLS = [
    ("tap", "coordinate tap", lambda d: gesture.tap(d, 1, 2)),
    ("type_text", "coordinate text entry", lambda d: gesture.type_text(d, "hi")),
    ("long_press", "coordinate long press", lambda d: gesture.long_press(d, 1, 2)),
    ("scroll_area", "scroll gesture",
     lambda d: gesture.scroll_area(d, 0, 0, 10, 10, "down", 0.5)),
    ("scroll_element", "scroll gesture",
     lambda d: gesture.scroll_element(d, _ScrollTarget(), "down", 0.5)),
    ("drag_gesture", "drag gesture", lambda d: gesture.drag_gesture(d, (1, 2), (3, 4))),
]


class TestIosRowsDispatch:
    """The iOS rows reach a real driver call rather than a refusal."""

    @pytest.fixture(autouse=True)
    def _ios(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "ios")

    @pytest.mark.parametrize("name,feature,call", GESTURE_CALLS,
                             ids=[name for name, _, _ in GESTURE_CALLS])
    def test_every_gesture_reaches_the_device(self, name, feature, call):
        """Reached the device by SOME channel — a `mobile:` script, a W3C pointer
        batch, or the focused element. Which one is the verb's business; that it
        did something is this test's."""
        driver = _FakeDriver()
        call(driver)
        assert driver.scripts or driver.actions or driver.typed, (
            f"{name} dispatched nothing")
        # None of them falls back to an Android keycode.
        assert driver.pressed == []

    def test_key_dispatch_presses_a_button_without_a_keycode(self):
        driver = _FakeDriver()
        _keys.dispatch(driver, "HOME", "ios")
        assert driver.scripts == [("mobile: pressButton", {"name": "home"})]
        assert driver.pressed == []

    def test_the_derived_session_options_are_the_ios_ones(self):
        caps = build_options("ios").to_capabilities()
        assert caps["platformName"].lower() == "ios"
        assert caps["appium:automationName"].lower() == "xcuitest"

    def test_an_explicit_capability_dict_lands_on_the_ios_options_class(self, monkeypatch):
        monkeypatch.setitem(_config._config, "capability", {"platformName": "iOS"})
        assert build_options("ios").to_capabilities()["platformName"] == "iOS"


class TestIosAbsencesAreDesign:
    """Three operations iOS genuinely lacks, refused rather than approximated.

    Each raise is the point: it sends the caller to the path that does work —
    an ordinary element the agent can already see — instead of no-op'ing.
    """

    @pytest.fixture(autouse=True)
    def _ios(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "ios")

    def test_there_is_no_paste_key(self):
        with pytest.raises(UnsupportedOnPlatform) as exc:
            _adapters.adapter("clipboard", "paste", "paste_clipboard", platform="ios")
        assert "paste_clipboard" in str(exc.value)

    def test_there_is_no_notification_shade(self):
        driver = _FakeDriver()
        with pytest.raises(UnsupportedOnPlatform):
            device_control(driver, "notification", value="show")
        assert driver.opened_notifications == 0

    def test_there_is_no_system_back_key(self):
        """UnknownKeyEvent, not UnsupportedOnPlatform: iOS key events ARE shipped,
        and the message lists what the platform does have."""
        from testmu_appium._errors import UnknownKeyEvent
        with pytest.raises(UnknownKeyEvent) as exc:
            _keys.keycode("BACK", "ios")
        assert "HOME" in str(exc.value)


class _PickerEl:
    def __init__(self, attributes=None, texts=None):
        self.attributes = attributes or {}
        self.rect = {"x": 100, "y": 200, "width": 200, "height": 100}
        self.calls = []
        self._texts = list(texts) if texts else None

    def click(self):
        self.calls.append("click")

    def get_attribute(self, name):
        if name == "text" and self._texts is not None:
            return self._texts.pop(0) if len(self._texts) > 1 else self._texts[0]
        return self.attributes.get(name)


class _PickerDriver(_FakeDriver):
    def __init__(self, queue=None):
        super().__init__()
        self.queue = list(queue) if queue is not None else []
        self.find_calls = []

    def find_elements(self, by, value):
        self.find_calls.append((by, value))
        return self.queue.pop(0) if self.queue else []


class TestPickerAndroidRow:
    """Detection, displayed-value reads and mode dispatch resolve from the row's data."""

    @pytest.fixture(autouse=True)
    def _android(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "android")

    @pytest.mark.parametrize("widget_class,mode", [
        ("android.widget.NumberPicker", "number_picker"),
        ("android.widget.SeekBar", "slider"),
        ("com.google.android.material.slider.Slider", "slider"),
        ("android.widget.Spinner", "spinner"),
    ], ids=["number_picker", "seekbar", "material_slider", "default_spinner"])
    def test_auto_detection_maps_the_widget_class_through_the_row_table(
        self, widget_class, mode
    ):
        assert picker._detect_mode(_PickerEl(attributes={"class": widget_class})) == mode

    def test_the_spinner_index_lookup_is_scoped_to_the_row_list_id(self):
        spinner = _PickerEl(attributes={"class": "android.widget.Spinner"})
        option = _PickerEl()
        driver = _PickerDriver(queue=[[option]])
        assert picker.select_picker(driver, spinner, _Target(index=0), "auto") is True
        assert "android:id/select_dialog_listview" in driver.find_calls[0][1]
        assert option.calls == ["click"]

    def test_the_spinner_lookup_follows_a_changed_row_list_id(self, monkeypatch):
        row = dict(_adapters._REGISTRIES["picker"]["android"])
        row["list_id"] = lambda: "test:id/other_list"
        monkeypatch.setitem(_adapters._REGISTRIES["picker"], "android", row)
        spinner = _PickerEl(attributes={"class": "android.widget.Spinner"})
        driver = _PickerDriver(queue=[[_PickerEl()]])
        picker.select_picker(driver, spinner, _Target(index=0), "auto")
        assert "test:id/other_list" in driver.find_calls[0][1]

    def test_the_displayed_value_prefers_text_over_content_desc(self):
        wheel = _PickerEl(attributes={"content-desc": "9"}, texts=["3"])
        assert picker._displayed_value(wheel) == "3"

    def test_the_displayed_value_falls_back_to_the_row_content_desc_attribute(self):
        wheel = _PickerEl(
            attributes={"class": "android.widget.NumberPicker", "content-desc": "7"}
        )
        driver = _PickerDriver()
        assert picker.select_picker(driver, wheel, _Target(value="7"), "auto") is True
        assert driver.scripts == []

    def test_an_explicit_mode_dispatches_the_row_runner(self):
        slider = _PickerEl(attributes={"class": "android.widget.Spinner"})
        driver = _PickerDriver()
        assert picker.select_picker(driver, slider, _Target(value="50"), "slider") is True
        assert driver.scripts[0][0] == "mobile: dragGesture"


class _IosPickerEl(_PickerEl):
    """An iOS control. Its value is SET rather than dragged to.

    Faithful to WDA on the one attribute that burned us: the widget class is
    served as `type`, and asking for `class` RAISES — a fake that politely
    answered the Android word hid that every iOS auto-detection fell through
    to the default on a real device."""

    def __init__(self, attributes=None):
        attributes = dict(attributes or {})
        if "class" in attributes and "type" not in attributes:
            attributes["type"] = attributes.pop("class")
        super().__init__(attributes=attributes)
        self.typed = []

    def get_attribute(self, name):
        if name in ("class", "className"):
            raise RuntimeError(
                "FBUnknownAttributeException: the attribute 'class' is unknown")
        return super().get_attribute(name)

    def send_keys(self, value):
        self.typed.append(value)


class TestPickerIosRow:
    @pytest.fixture(autouse=True)
    def _ios(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "ios")

    @pytest.mark.parametrize("cls,mode", [
        # The first two pin marker ORDER as much as mapping: matching is
        # substring and "Picker" sits inside both of these type names, so the
        # container marker must never see them first.
        ("XCUIElementTypePickerWheel", "wheel_column"),
        ("XCUIElementTypeDatePicker", "date_wheels"),
        ("XCUIElementTypePicker", "picker_wheels"),
        ("XCUIElementTypeSlider", "slider"),
        ("XCUIElementTypeStepper", "stepper"),
        ("XCUIElementTypeButton", "spinner"),
    ], ids=["wheel", "date", "picker_container", "slider", "stepper",
            "default_spinner"])
    def test_auto_detection_maps_the_element_type_through_the_row(self, cls, mode):
        assert picker._detect_mode(_IosPickerEl(attributes={"class": cls})) == mode

    class _StepperButton:
        def __init__(self, stepper, name, delta, x):
            self._stepper = stepper
            self._name = name
            self._delta = delta
            self.rect = {"x": x, "y": 0, "width": 40, "height": 40}
            self.clicks = 0

        def get_attribute(self, key):
            return self._name if key == "name" else None

        def click(self):
            self.clicks += 1
            floor, ceiling = self._stepper.limits
            self._stepper.value = min(
                ceiling, max(floor, self._stepper.value + self._delta))

    class _Stepper:
        """A UIStepper: a value, a step size, limits, and two child buttons."""

        def __init__(self, value=0.0, step=1.0, limits=(0.0, 100.0)):
            self.value = value
            self.limits = limits
            self.decrement = TestPickerIosRow._StepperButton(
                self, "Decrement", -step, x=0)
            self.increment = TestPickerIosRow._StepperButton(
                self, "Increment", +step, x=60)

        def get_attribute(self, key):
            if key in ("class", "className"):
                raise RuntimeError("FBUnknownAttributeException")
            if key == "type":
                return "XCUIElementTypeStepper"
            if key == "value":
                return str(self.value)
            return None

        def find_elements(self, by, value):
            assert value == "XCUIElementTypeButton"
            return [self.decrement, self.increment]

    def test_a_stepper_walks_to_its_target_by_its_own_buttons(self):
        stepper = self._Stepper(value=2.0)
        assert picker.select_picker(
            _PickerDriver(), stepper, _Target(value="5"), "auto") is True
        assert stepper.value == 5.0
        assert stepper.increment.clicks == 3
        assert stepper.decrement.clicks == 0

    def test_a_stepper_walks_down_too(self):
        stepper = self._Stepper(value=4.0)
        picker.select_picker(_PickerDriver(), stepper, _Target(value="1"), "auto")
        assert stepper.value == 1.0

    def test_a_fractional_step_size_needs_no_configuration(self):
        """The step size is the control's secret: tap, re-read, repeat."""
        stepper = self._Stepper(value=1.0, step=0.5)
        picker.select_picker(_PickerDriver(), stepper, _Target(value="2.5"), "auto")
        assert stepper.value == 2.5

    def test_a_stepper_names_its_own_limit_instead_of_spinning(self):
        """A tap that changes nothing is the control's min or max saying no."""
        stepper = self._Stepper(value=98.0, limits=(0.0, 99.0))
        with pytest.raises(RuntimeError) as exc:
            picker.select_picker(
                _PickerDriver(), stepper, _Target(value="150"), "auto")
        assert "limit" in str(exc.value)
        assert stepper.value == 99.0

    def test_localized_buttons_resolve_by_geometry(self):
        """A German build labels them Erhöhen/Verringern; left is still
        decrement in LTR."""
        stepper = self._Stepper(value=1.0)
        stepper.decrement._name = "Verringern"
        stepper.increment._name = "Erhöhen"
        picker.select_picker(_PickerDriver(), stepper, _Target(value="3"), "auto")
        assert stepper.value == 3.0

    class _DateWheel(_IosPickerEl):
        def __init__(self, value=""):
            super().__init__(attributes={"class": "XCUIElementTypePickerWheel",
                                         "value": value})

    class _DatePicker:
        def __init__(self, wheels):
            self.wheels = wheels

        def get_attribute(self, key):
            if key in ("class", "className"):
                raise RuntimeError("FBUnknownAttributeException")
            return "XCUIElementTypeDatePicker" if key == "type" else None

        def find_elements(self, by, value):
            assert value == "XCUIElementTypePickerWheel"
            return self.wheels

    def test_a_wheels_date_picker_sets_one_part_per_wheel_in_order(self):
        month, day, year = (self._DateWheel() for _ in range(3))
        element = self._DatePicker([month, day, year])
        assert picker.select_picker(
            _PickerDriver(), element,
            _Target(value="March|15|2025"), "auto") is True
        assert month.typed == ["March"]
        assert day.typed == ["15"]
        assert year.typed == ["2025"]

    def test_a_part_count_that_does_not_match_the_wheels_is_refused(self):
        element = self._DatePicker([self._DateWheel(), self._DateWheel()])
        with pytest.raises(ValueError) as exc:
            picker.select_picker(
                _PickerDriver(), element, _Target(value="March|15|2025"), "auto")
        assert "2 wheel(s)" in str(exc.value)
        assert "3 part(s)" in str(exc.value)

    class _PickerContainer:
        """A Picker: the NAMED shell whose value lives on wheel children."""

        def __init__(self, wheels):
            self.wheels = wheels
            self.calls = []

        def click(self):
            self.calls.append("click")

        def get_attribute(self, key):
            if key in ("class", "className"):
                raise RuntimeError("FBUnknownAttributeException")
            return "XCUIElementTypePicker" if key == "type" else None

        def find_elements(self, by, value):
            assert value == "XCUIElementTypePickerWheel"
            return self.wheels

    def test_a_picker_container_sets_the_wheel_inside_it(self):
        """The model records the container — its identifier names the control,
        while the wheel child is named by whatever row is selected. Detected as
        spinner, this raised 'matched 0 entries': wheel rows are not elements."""
        wheel = self._DateWheel()
        element = self._PickerContainer([wheel])
        assert picker.select_picker(
            _PickerDriver(), element, _Target(value="Wheel row 7"), "auto") is True
        assert wheel.typed == ["Wheel row 7"]
        assert element.calls == []

    def test_a_multi_wheel_picker_takes_one_part_per_wheel(self):
        left, right = self._DateWheel(), self._DateWheel()
        element = self._PickerContainer([left, right])
        assert picker.select_picker(
            _PickerDriver(), element, _Target(value="March|2025"), "auto") is True
        assert left.typed == ["March"]
        assert right.typed == ["2025"]

    def test_a_picker_showing_no_wheels_still_runs_the_tap_then_choose_flow(self):
        """A menu-styled Picker renders options as tappable rows — exactly what
        the spinner flow serves, so falling through IS the old behavior."""
        element = self._PickerContainer([])
        with pytest.raises(ValueError, match="spinner option"):
            picker.select_picker(
                _PickerDriver(), element, _Target(value="Wheel row 7"), "auto")
        assert element.calls == ["click"]

    def test_a_mode_served_only_by_the_other_platform_refuses_by_name(self):
        """`number_picker` is Android machinery; asking iOS for it used to
        explode with a bare KeyError instead of a named refusal."""
        from testmu_appium._errors import PickerModeNotSupported

        with pytest.raises(PickerModeNotSupported) as exc:
            picker.select_picker(
                _PickerDriver(), _IosPickerEl(), _Target(value="5"),
                "number_picker")
        assert "number_picker" in str(exc.value)

    def test_a_compact_date_picker_refuses_by_name(self):
        """iOS 14's default style renders a calendar, not wheels — its date
        cells are ordinary elements, not a wheel assignment to half-imitate."""
        from testmu_appium._errors import PickerModeNotSupported

        element = self._DatePicker([])
        with pytest.raises(PickerModeNotSupported) as exc:
            picker.select_picker(
                _PickerDriver(), element, _Target(value="March|15|2025"), "auto")
        assert "compact" in str(exc.value)

    def test_a_wheel_is_set_to_its_value_not_tapped(self):
        """A wheel's options are a spun value, not a list of rows — XCUITest
        assigns to the element rather than finding one."""
        wheel = _IosPickerEl(attributes={"class": "XCUIElementTypePickerWheel"})
        driver = _PickerDriver()
        assert picker.select_picker(driver, wheel, _Target(value="March"), "auto") is True
        assert wheel.typed == ["March"]
        assert wheel.calls == []
        assert driver.find_calls == []

    def test_an_index_is_refused_for_a_wheel_in_those_words(self):
        """select(index=...) has no meaning for a value range, and saying so beats
        silently selecting whatever sits at that offset."""
        wheel = _IosPickerEl(attributes={"class": "XCUIElementTypePickerWheel"})
        with pytest.raises(ValueError, match="value range"):
            picker.select_picker(_PickerDriver(), wheel, _Target(index=2), "auto")

    def test_a_slider_takes_the_normalized_position_directly(self):
        """No drag across the track, so unlike Android's row it cannot miss it."""
        slider = _IosPickerEl(attributes={"class": "XCUIElementTypeSlider"})
        driver = _PickerDriver()
        assert picker.select_picker(driver, slider, _Target(value="50"), "auto") is True
        assert slider.typed == ["0.5"]
        assert driver.scripts == []

    def test_the_spinner_option_lookup_is_a_class_chain_over_the_sheet(self):
        """iOS has no resource ids, so the row names the container by TYPE."""
        sheet = _IosPickerEl(attributes={"class": "XCUIElementTypeButton"})
        option = _IosPickerEl()
        driver = _PickerDriver(queue=[[option]])
        assert picker.select_picker(driver, sheet, _Target(index=0), "auto") is True
        assert "XCUIElementTypeSheet" in driver.find_calls[0][1]
        assert option.calls == ["click"]

    def test_wheel_column_is_deferred_by_platform_not_globally(self):
        """Android still has no runner for it and says so; iOS ships it. The mode
        list is shared, so the ROW has to decide."""
        with pytest.raises(PickerModeNotSupported):
            picker.select_picker(
                _PickerDriver(), _PickerEl(), _Target(value="x"), "dial")


class TestAndroidPickerModeRefusal:
    """The mirror of the iOS case: `date_wheels` is iOS machinery, and asking
    Android for it used to explode with a bare KeyError."""

    def test_an_ios_only_mode_refuses_by_name_on_android(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "android")
        with pytest.raises(PickerModeNotSupported) as exc:
            picker.select_picker(
                _PickerDriver(), _PickerEl(), _Target(value="March|15|2025"),
                "date_wheels")
        assert "date_wheels" in str(exc.value)
