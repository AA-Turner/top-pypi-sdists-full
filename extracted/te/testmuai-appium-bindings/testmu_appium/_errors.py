"""Public exception classes for testmu_appium.

Grouped by who raises them:
- configure()/run() validation → TestmuConfigError
- the strategy compiler / keycode tables → UnknownStrategy, UnknownKeyEvent
- platform tables that are declared but not shipped → UnsupportedOnPlatform
- the element verb engine → ElementNotFound, ElementBlocked, CoordinateFallbackUnavailable
- deferred surfaces → SmartUINotAvailable, PickerModeNotSupported, NetworkQueryUnavailable
- the network mock verb → NetworkMockUnavailable
- mobile-web driver verbs → WebSurfaceUnavailable
- the vision verb's own precondition → ScreenshotUnavailable
"""


class TestmuConfigError(Exception):
    """Raised when configure(**kwargs) receives invalid, unknown or conflicting config."""

    # The name matches pytest's class-collection pattern; this keeps it out of
    # collection wherever a test module imports it.
    __test__ = False


class UnsupportedOnPlatform(Exception):
    """Raised when a verb, key name or data table has no entry for the live platform.

    Loud by design: a mobile verb that is second-class on a platform fails with the
    platform named rather than silently degrading.
    """

    def __init__(self, feature: str, platform: str = ""):
        self.feature = feature
        self.platform = platform
        suffix = f" (platform={platform!r})" if platform else ""
        super().__init__(f"{feature} is not supported{suffix}")


class UnknownStrategy(Exception):
    """Raised when a recorded selector carries a strategy the compiler has no row for.

    Strategies are open semantic strings; an unknown one is producer/binding version
    skew, never something to guess at.
    """

    def __init__(self, strategy: str, platform: str, known):
        self.strategy = strategy
        self.platform = platform
        super().__init__(
            f"unknown selector strategy {strategy!r} for platform {platform!r}; "
            f"known: {sorted(known)}"
        )


class UnknownKeyEvent(Exception):
    """Raised when a semantic key name has no keycode row for the live platform."""

    def __init__(self, key: str, platform: str, known):
        self.key = key
        self.platform = platform
        super().__init__(
            f"unknown key event {key!r} for platform {platform!r}; known: {sorted(known)}"
        )


class ElementNotFound(Exception):
    """Raised when every recorded strategy missed and heal produced no live element.

    Carries the strategies that were tried so the failure names what was searched.
    """

    def __init__(self, description: str, tried, reason: str = ""):
        self.description = description
        self.tried = list(tried)
        self.reason = reason
        super().__init__(
            f"element not found for {description!r}; tried strategies {self.tried}"
            + (f"; {reason}" if reason else "")
        )


class ElementBlocked(Exception):
    """Raised when the element resolves but stays non-interactable after bounded retry.

    Never routed to heal: the element exists, so a fresh locator cannot help, and a
    coordinate tap would punch through whatever overlay is covering it.
    """

    def __init__(self, description: str, original: Exception):
        self.description = description
        self.original = original
        super().__init__(f"element for {description!r} is present but blocked: {original}")


class CoordinateFallbackUnavailable(Exception):
    """Raised when heal is authoritatively out of options and coordinates cannot be used.

    Either no basis was recorded, or the live orientation differs from the recorded
    basis orientation — replaying a portrait ratio on a landscape screen taps the
    wrong place, so the binding refuses loudly instead.
    """


class SmartUINotAvailable(Exception):
    """Raised by smartui_screenshot outside a cloud session.

    SmartUI capture is a LambdaTest cloud service; there is no local equivalent to
    degrade to.
    """


class PickerModeNotSupported(Exception):
    """Raised for picker widget modes deferred out of the v1 select() surface.

    Deferred contract: SeekBar wheel-column walk (AM/PM, month and other cyclic
    column pickers) and the clock-face dial picker port behavior-for-behavior from
    the legacy runtime's SeekBar modes. Shipping now: native spinner/dropdown
    selection, NumberPicker scroll-to-value, and plain slider drag-to-percent.
    """

    def __init__(self, mode: str, widget_class: str):
        self.mode = mode
        self.widget_class = widget_class
        super().__init__(
            f"picker mode {mode!r} on widget {widget_class!r} is not supported yet; "
            f"supported modes: spinner/dropdown select, NumberPicker scroll-to-value, "
            f"slider drag-to-percent"
        )


class NetworkQueryUnavailable(Exception):
    """Raised when network_query runs without a cloud device-host side channel.

    Deferred contract: on a LambdaTest mobile session the device host publishes
    PROXY_API_PORT/HOST_IP through rd-details.env; network_query polls the
    network-log endpoint on that host. There is no local Appium equivalent — a
    local Appium session has no proxy recording traffic — so the local path raises
    rather than returning an empty result that would read as "no matching request".
    """


class NetworkMockUnavailable(RuntimeError):
    """Raised when the mock-set API is unreachable.

    PROXY_API_PORT/HOST_IP missing from rd-details.env / env. The device
    session must be started with mitmProxy enabled (networkCapture /
    MITM_PROXY).
    """


class WebSurfaceUnavailable(Exception):
    """Raised when a mobile-web driver verb cannot reach the visible page.

    Cookie, localStorage, refresh, and browser-history operations deliberately
    stay in ``NATIVE_APP`` and use the existing local CDP side channel. Falling
    back to a native driver operation would act on a different surface (and,
    for BACK, may leave the app), so an absent visible channel is a hard, named
    precondition failure.
    """

    def __init__(self, feature: str, package: str = ""):
        self.feature = feature
        self.package = package
        suffix = f" (package={package!r})" if package else ""
        super().__init__(
            f"{feature} requires a visible debuggable mobile web surface{suffix}"
        )


class ScreenshotUnavailable(Exception):
    """Raised when a verb whose premise IS the screenshot cannot capture one.

    `vision_query` reads a value off the pixels. Answering it from the flat entry
    list alone is not a degraded visual query — it is a different question, answered
    against no pixels, returned to the caller as though it were the one they asked.
    Heal's perception is deliberately NOT gated this way: heal is a recovery path
    that is allowed to run degraded rather than not at all.
    """


class ViewportCaptureError(Exception):
    """Raised when a fresh viewport tree cannot be captured and parsed."""


class DegenerateViewportCaptureError(ViewportCaptureError):
    """Raised when a fresh tree has collapsed relative to its recorded baseline."""


class UnsupportedTreeContract(Exception):
    """Raised when a viewport extraction names an unknown row contract."""

    def __init__(self, contract: str):
        self.contract = contract
        super().__init__(f"unsupported viewport tree contract {contract!r}")


class ViewportSelectionDriftError(Exception):
    """Raised when a recorded non-empty selection no longer matches fresh rows."""


class ViewportResultMissError(Exception):
    """Raised when a viewport extraction returns no value."""


class ViewportScriptCompileError(Exception):
    """Raised when a viewport extraction cannot be compiled."""


class ViewportScriptPolicyError(Exception):
    """Raised when a viewport extraction exceeds the restricted script contract."""


class ViewportScriptTimeoutError(Exception):
    """Raised when a viewport extraction exceeds its execution deadline."""


class ViewportScriptRuntimeError(Exception):
    """Raised when a viewport extraction raises while running in its worker."""


class ViewportResultTypeError(Exception):
    """Raised when a viewport extraction does not return its declared scalar type."""
