from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING

from .. import common
from . import (
    DeviceName,
    MatchLevel,
    ScreenOrientation,
    SessionType,
    StitchMode,
    extract_text,
)
from .accessibility import (
    AccessibilityGuidelinesVersion,
    AccessibilityLevel,
    AccessibilityRegionType,
    AccessibilityStatus,
)
from .mmallow import (
    EXCLUDE,
    BaseSchema,
    Boolean,
    DateTime,
    Dict,
    Float,
    Function,
    Integer,
    List,
    Nested,
    Raw,
    Schema,
    SchemaMeta,
    String,
    post_dump,
    post_load,
    pre_load,
)
from .schema_fields import (
    BrowserInfo,
    DebugScreenshots,
    ElementReference,
    Enum,
    EnvironmentRaw,
    Error,
    FrameReference,
    LayoutBreakpoints,
    MobileOptions,
    NormalizationRaw,
    RegionReference,
    StitchOverlap,
    TargetReference,
    VisualGridOptions,
    demarshal_error,
)
from .selenium.misc import BrowserType
from .test_results import TestResultsStatus

if TYPE_CHECKING:
    import typing as t

    from . import config


# Default marshmallow.Schema has no option to skip attributes with None value
# or empty lists / dicts. Because it uses metaclass, it should be re-defined
# instead of simple subclassing
class USDKSchema(BaseSchema, metaclass=SchemaMeta):
    # Mimic marshmallow 2 behaviour
    class Meta:
        unknown = EXCLUDE

    __doc__ = BaseSchema.__doc__
    _always_skip_values = (None, [])
    _keep_empty_objects = ("lazyLoad",)  # fields that are allowed to have {} value

    @classmethod
    def should_keep(cls, key, value):
        # type: (t.Text, t.Any) -> bool
        if value in cls._always_skip_values:
            return False
        if value == {} and key not in cls._keep_empty_objects:
            return False
        return True

    @pre_load
    def _handle_aliases(self, data, **kwargs):
        """
        For each field that uses a data_key (alias), if the alias key is missing in the input
        but the original field name is present, copy the value over. This way the schema
        accepts both the alias key and the field name on load.
        """
        for field_name, field in self.fields.items():
            alias = field.data_key
            if alias and alias not in data and field_name in data:
                data[alias] = data[field_name]
        return data

    @post_dump
    def remove_none_values_empty_lists(self, data, **_):
        # type: (dict, **t.Any) -> dict
        return {k: v for k, v in data.items() if self.should_keep(k, v)}


class Size(USDKSchema):
    width = Integer()
    height = Integer()


class DebugScreenshotHandler(USDKSchema):
    debug_screenshots_path = String(data_key="path")
    debug_screenshots_prefix = String(data_key="prefix")


class Environment(USDKSchema):
    host_os = String(data_key="os")
    host_app = String(data_key="hostingApp")
    viewport_size = Nested(Size, data_key="viewportSize")


class EnvironmentRenderer(USDKSchema):
    render_environment_id = String(data_key="renderEnvironmentId")
    ec_session_id = String(data_key="ecSessionId")
    os = String()
    os_info = String(data_key="osInfo")
    hosting_app = String(data_key="hostingApp")
    hosting_app_info = String(data_key="hostingAppInfo")
    device_name = String(data_key="deviceName")
    viewport_size = Nested(Size, data_key="viewportSize")
    user_agent = String(data_key="userAgent")
    renderer = Dict()
    raw_environment = Dict(data_key="rawEnvironment")
    properties = List(Dict())

    @post_load
    def to_python(self, data, **_):
        return common.EnvironmentInfo(**data)


class DesktopBrowserRenderer(USDKSchema):
    width = Float()
    height = Float()
    browser_type = Enum(BrowserType, data_key="name")

    @post_load
    def to_python(self, data, **_):
        return common.DesktopBrowserInfo(**data)


class ChromeEmulationRenderer(USDKSchema):
    device_name = Enum(DeviceName, data_key="deviceName")
    screen_orientation = Enum(ScreenOrientation, data_key="screenOrientation")

    @post_load
    def to_python(self, data, **_):
        return common.ChromeEmulationInfo(**data)


class IosDeviceRenderer(USDKSchema):
    device_name = Function(
        data_key="deviceName",
        serialize=lambda obj, *args, **kwargs: getattr(
            obj.device_name, "value", obj.device_name
        ),
        deserialize=lambda value, *args, **kwargs: value,
    )
    screen_orientation = Enum(ScreenOrientation, data_key="screenOrientation")
    ios_version = Function(
        data_key="version",
        serialize=lambda obj, *args, **kwargs: obj.ios_version.value
        if obj.ios_version
        else None,
        deserialize=lambda value, *args, **kwargs: value,
    )

    @post_load
    def to_python(self, data, **_):
        return common.IosDeviceInfo(**data)


class AndroidDeviceRenderer(USDKSchema):
    device_name = Function(
        data_key="deviceName",
        serialize=lambda obj, *args, **kwargs: getattr(
            obj.device_name, "value", obj.device_name
        ),
        deserialize=lambda value, *args, **kwargs: value,
    )
    screen_orientation = Enum(ScreenOrientation, data_key="screenOrientation")
    android_version = Function(
        data_key="version",
        serialize=lambda obj, *args, **kwargs: obj.android_version.value
        if obj.android_version
        else None,
        deserialize=lambda value, *args, **kwargs: value,
    )

    @post_load
    def to_python(self, data, **_):
        return common.AndroidDeviceInfo(**data)


class Region(USDKSchema):
    left = Float(data_key="x")
    top = Float(data_key="y")
    width = Float()
    height = Float()

    @post_load
    def to_python(self, data, **_):
        return common.geometry.Region.from_(data)


class Offset(USDKSchema):
    max_left_offset = Float(data_key="left")
    max_up_offset = Float(data_key="top")
    max_right_offset = Float(data_key="right")
    max_down_offset = Float(data_key="bottom")


class ContextReference(USDKSchema):
    frame = FrameReference()
    scroll_root_locator = ElementReference(data_key="scrollRootElement")


class ImageCropRect(USDKSchema):
    header = Float(data_key="top")
    right = Float()
    footer = Float(data_key="bottom")
    left = Float()


class Normalization(USDKSchema):
    cut_provider = Nested(ImageCropRect, data_key="cut")
    rotation = Integer()
    scale_ratio = Float(data_key="scaleRatio")


class Batch(USDKSchema):
    id = String()
    name = String()
    sequence_name = String(data_key="sequenceName")
    started_at = DateTime("%Y-%m-%dT%H:%M:%SZ", data_key="startedAt")
    notify_on_completion = Boolean(data_key="notifyOnCompletion")
    properties = List(Dict())


class LayoutBreakpointsOptions(USDKSchema):
    breakpoints = Raw()
    reload = Boolean()
    height_breakpoints = Boolean(data_key="heightBreakpoints")


class Proxy(USDKSchema):
    url = String(required=True)
    username = String()
    password = String()


class ImageTarget(USDKSchema):
    image = String()
    dom = String()


class AccessibilitySettings(USDKSchema):
    level = Enum(AccessibilityLevel)
    guidelines_version = Enum(AccessibilityGuidelinesVersion, data_key="version")


class CodedRegionReference(USDKSchema):
    region = RegionReference()
    padding = Raw()
    region_id = String(data_key="regionId")


class FloatingRegionReference(USDKSchema):
    _target_path = RegionReference(data_key="region")
    _bounds = Nested(Offset(), data_key="offset")


class AccessibilityRegionReference(USDKSchema):
    _target_path = RegionReference(data_key="region")
    _type = Enum(AccessibilityRegionType, data_key="type")


class DynamicSettingsReference(Dict):
    ignore_patterns = List(String(), data_key="ignorePatterns")

    def _serialize(self, obj, *args, **kwargs):
        return None if obj is None else obj.to_dict()["ignore_patterns"]


class DynamicRegionReference(USDKSchema):
    _target_path = RegionReference(data_key="region")
    _dynamic_settings = DynamicSettingsReference(data_key="type")
    padding = Raw()


class LazyLoadOptions(USDKSchema):
    scroll_length = Integer(data_key="scrollLength")
    waiting_time = Integer(data_key="waitingTime")
    max_amount_to_scroll = Integer(data_key="maxAmountToScroll")


class EyesConfig(USDKSchema):
    # region
    # frames
    force_full_page_screenshot = Boolean(data_key="fully")
    # scrollRootElement
    stitch_mode = Enum(StitchMode, data_key="stitchMode")
    hide_scrollbars = Boolean(data_key="hideScrollbars")
    hide_caret = Boolean(data_key="hideCaret")
    stitch_overlap = StitchOverlap(data_key="overlap")
    wait_before_capture = Integer(data_key="waitBeforeCapture")
    # lazyLoad
    ignore_displacements = Boolean(
        attribute="default_match_settings.ignore_displacements",
        data_key="ignoreDisplacements",
    )
    # name
    # pageId
    ignore_regions = List(
        Nested(CodedRegionReference),
        attribute="default_match_settings.ignore_regions",
        data_key="ignoreRegions",
    )
    layout_regions = List(
        Nested(CodedRegionReference),
        attribute="default_match_settings.layout_regions",
        data_key="layoutRegions",
    )

    strict_regions = List(
        Nested(CodedRegionReference),
        attribute="default_match_settings.strict_regions",
        data_key="strictRegions",
    )
    content_regions = List(
        Nested(CodedRegionReference),
        attribute="default_match_settings.content_regions",
        data_key="contentRegions",
    )
    floating_match_settings = List(
        Nested(FloatingRegionReference),
        attribute="default_match_settings.floating_match_settings",
        data_key="floatingRegions",
    )
    accessibility = List(
        Nested(AccessibilityRegionReference),
        attribute="default_match_settings.accessibility",
        data_key="accessibilityRegions",
    )
    accessibility_settings = Nested(
        AccessibilitySettings,
        attribute="default_match_settings.accessibility_settings",
        data_key="accessibilitySettings",
    )
    dynamic_regions = List(
        Nested(DynamicRegionReference),
        attribute="default_match_settings.dynamic_regions",
        data_key="dynamicRegions",
    )

    match_level = Enum(
        MatchLevel,
        attribute="default_match_settings.match_level",
        data_key="matchLevel",
    )
    send_dom = Boolean(data_key="sendDom")
    use_dom = Boolean(attribute="default_match_settings.use_dom", data_key="useDom")
    enable_patterns = Boolean(
        attribute="default_match_settings.enable_patterns", data_key="enablePatterns"
    )
    ignore_caret = Boolean(
        attribute="default_match_settings.ignore_caret", data_key="ignoreCaret"
    )
    # enablePatterns
    # ignoreCaret
    visual_grid_options = VisualGridOptions(data_key="ufgOptions")
    layout_breakpoints = LayoutBreakpoints(data_key="layoutBreakpoints")
    disable_browser_fetching = Boolean(data_key="disableBrowserFetching")
    match_timeout = Float(data_key="matchTimeout")
    browsers_info = List(BrowserInfo(), data_key="environments")
    # autProxy
    normalization = NormalizationRaw()
    debug_images = DebugScreenshots(data_key="debugImages")
    mobile_options = MobileOptions(data_key="mobileOptions")
    # wait_before_screenshots = Float(data_key="waitBeforeScreenshots")


class EyesServerSettings(USDKSchema):
    server_url = String(data_key="eyesServerUrl")
    api_key = String(data_key="apiKey")
    agent_id = String(data_key="agentId")
    proxy = Nested(Proxy)
    # useDnsCache


class OpenSettings(EyesServerSettings, USDKSchema):
    app_name = String(data_key="appName")
    test_name = String(data_key="testName")
    # displayName
    user_test_id = String(data_key="userTestId")
    session_type = Enum(SessionType, data_key="sessionType")
    properties = List(Dict())
    batch = Nested(Batch)
    dont_close_batches = Boolean(data_key="keepBatchOpen")
    environment = EnvironmentRaw()
    environment_name = String(data_key="environmentName")
    baseline_env_name = String(data_key="baselineEnvName")
    branch_name = String(data_key="branchName")
    parent_branch_name = String(data_key="parentBranchName")
    baseline_branch_name = String(data_key="baselineBranchName")
    is_disabled = Boolean(data_key="isDisabled")
    # compareWithParentBranch
    # gitBranchingTimestamp
    # ignoreGitBranching
    # ignoreBaseline
    save_diffs = Boolean(data_key="saveDiffs")
    # abortIdleTestTimeout
    _timeout = Integer(data_key="connectionTimeout")
    # removeSession
    # isFunctionalTest
    # isComponentTest
    # ufgServerUrl
    # fallbackBaselineId
    # latestCommitInfo
    # processId
    # removeDuplicateTests

    # UFG related
    disable_nml_url_cache = Boolean(data_key="disableBrokerUrlCache")


class CheckSettings(USDKSchema):
    name = String()
    disable_browser_fetching = Boolean(data_key="disableBrowserFetching")
    layout_breakpoints = Nested(LayoutBreakpointsOptions, data_key="layoutBreakpoints")
    visual_grid_options = VisualGridOptions(data_key="ufgOptions")
    script_hooks = Dict(data_key="hooks")
    page_id = String(data_key="pageId")
    variation_group_id = String(data_key="userCommandId")
    timeout = Integer(data_key="matchTimeout")
    wait_before_capture = Integer(data_key="waitBeforeCapture")
    lazy_load = Nested(LazyLoadOptions, data_key="lazyLoad")
    # ScreenshotSettings
    region = TargetReference()
    frame_chain = List(Nested(ContextReference), data_key="frames")
    scroll_root_locator = ElementReference(data_key="scrollRootElement")
    stitch_content = Boolean(data_key="fully")
    # MatchSettings
    match_level = Enum(MatchLevel, data_key="matchLevel")
    send_dom = Boolean(data_key="sendDom")
    use_dom = Boolean(data_key="useDom")
    enable_patterns = Boolean(data_key="enablePatterns")
    ignore_caret = Boolean(data_key="ignoreCaret")
    ignore_displacements = Boolean(data_key="ignoreDisplacements")
    ignore_regions = List(Nested(CodedRegionReference), data_key="ignoreRegions")
    layout_regions = List(Nested(CodedRegionReference), data_key="layoutRegions")
    strict_regions = List(Nested(CodedRegionReference), data_key="strictRegions")
    content_regions = List(Nested(CodedRegionReference), data_key="contentRegions")
    floating_regions = List(Nested(FloatingRegionReference), data_key="floatingRegions")
    accessibility_regions = List(
        Nested(AccessibilityRegionReference), data_key="accessibilityRegions"
    )
    dynamic_regions = List(Nested(DynamicRegionReference), data_key="dynamicRegions")
    webview = Raw()
    screenshot_mode = String(data_key="screenshotMode")


class LocateSettings(USDKSchema):
    names = List(String(), data_key="locatorNames")
    first_only = Boolean(data_key="firstOnly")


class OCRSearchSettings(USDKSchema):
    _patterns = List(String(), data_key="patterns")
    _ignore_case = Boolean(data_key="ignoreCase")
    _first_only = Boolean(data_key="firstOnly")
    _language = String(data_key="language")


class ExtractTextSettings(USDKSchema):
    target = RegionReference(data_key="region")
    _hint = String(data_key="hint")
    _min_match = Float(data_key="minMatch")
    _language = String(data_key="language")


class CloseSettings(USDKSchema):
    # raise_ex = Boolean(data_key="throwErr")  # not present in config
    save_new_tests = Boolean(data_key="updateBaselineIfNew")
    save_failed_tests = Boolean(data_key="updateBaselineIfDifferent")


class CloseBatchSettings(USDKSchema):
    batch_id = String(data_key="batchId")
    server_url = String(data_key="eyesServerUrl")
    api_key = String(data_key="apiKey")
    proxy = Nested(Proxy)


class DeleteTestSettings(USDKSchema):
    id = String(data_key="testId")
    batch_id = String(data_key="batchId")
    secret_token = String(data_key="secretToken")
    server_url = String(
        attribute="_connection_config.server_url", data_key="eyesServerUrl"
    )
    api_key = String(attribute="_connection_config.api_key", data_key="apiKey")
    proxy = Nested(Proxy, attribute="_connection_config.proxy")


class ECClientCapabilitiesOptions(USDKSchema):
    server_url = String(data_key="ecServerUrl")
    api_key = String(data_key="apiKey")


class ECClientSettings(USDKSchema):
    options = Nested(ECClientCapabilitiesOptions)
    proxy = Nested(Proxy)


# De-marshaling schema
# Mimic marshmallow 2 behaviour
class DeMarshalingSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    @pre_load
    def _handle_aliases(self, data, **kwargs):
        """
        For each field that uses a data_key (alias), if the alias key is missing in the input
        but the original field name is present, copy the value over. This way the schema
        accepts both the alias key and the field name on load.
        """
        for field_name, field in self.fields.items():
            alias = field.data_key
            if alias and alias not in data and field_name in data:
                data[alias] = data[field_name]
        return data


class RectangleSize(DeMarshalingSchema):
    width = Integer()
    height = Integer()

    @post_load
    def to_python(self, data, **_):
        return common.RectangleSize(**data)


class ServerInfo(DeMarshalingSchema):
    logs_dir = String(data_key="logsDir")

    @post_load
    def to_python(self, data, **_):
        return common.ServerInfo(**data)


class SessionUrls(DeMarshalingSchema):
    batch = String()
    session = String()

    @post_load
    def to_python(self, data, **_):
        return common.test_results.SessionUrls(**data)


class ApiUrls(DeMarshalingSchema):
    baseline_image = String(data_key="baselineImage")
    current_image = String(data_key="currentImage")
    diff_image = String(data_key="diffImage")
    checkpoint_image = String(data_key="checkpointImage")
    checkpoint_image_thumbnail = String(data_key="checkpointImageThumbnail")
    side_by_side_image = String(data_key="sideBySideImage")

    @post_load
    def to_python(self, data, **_):
        return common.test_results.StepInfo.ApiUrls(**data)


class AppUrls(DeMarshalingSchema):
    step = String(data_key="step")
    step_editor = String(data_key="stepEditor")

    @post_load
    def to_python(self, data, **_):
        return common.test_results.StepInfo.AppUrls(**data)


class SessionAccessibilityStatus(DeMarshalingSchema):
    level = Enum(AccessibilityLevel)
    version = Enum(AccessibilityGuidelinesVersion)
    status = Enum(AccessibilityStatus)

    @post_load
    def to_python(self, data, **_):
        return common.accessibility.SessionAccessibilityStatus(**data)


class StepInfo(DeMarshalingSchema):
    name = String()
    is_different = Boolean(data_key="isDifferent")
    has_baseline_image = Boolean(data_key="hasBaselineImage")
    has_current_image = Boolean(data_key="hasCurrentImage")
    has_checkpoint_image = Boolean(data_key="hasCheckpointImage")
    api_urls = Nested(ApiUrls, data_key="apiUrls")
    app_urls = Nested(AppUrls, data_key="appUrls")

    @post_load
    def to_python(self, data, **_):
        return common.test_results.StepInfo(**data)


class LocateTextResponse(DeMarshalingSchema):
    left = Integer(data_key="x")
    top = Integer(data_key="y")
    width = Integer()
    height = Integer()
    text = String()

    @post_load
    def to_python(self, data, **_):
        return extract_text.TextRegion(**data)


class TestResults(DeMarshalingSchema):
    steps = Integer()
    matches = Integer()
    mismatches = Integer()
    missing = Integer()
    exact_matches = Integer(data_key="exactMatches")
    strict_matches = Integer(data_key="strictMatches")
    content_matches = Integer(data_key="contentMatches")
    layout_matches = Integer(data_key="layoutMatches")
    none_matches = Integer(data_key="noneMatches")
    is_new = Boolean(data_key="isNew")
    url = String()
    status = Enum(TestResultsStatus)
    name = String()
    secret_token = String(data_key="secretToken")
    id = String()
    app_name = String(data_key="appName")
    batch_name = String(data_key="batchName")
    batch_id = String(data_key="batchId")
    branch_name = String(data_key="branchName")
    host_os = String(data_key="hostOS")
    host_app = String(data_key="hostApp")
    host_display_size = Nested(RectangleSize, data_key="hostDisplaySize")
    started_at = String(data_key="startedAt")
    duration = Integer()
    is_different = Boolean(data_key="isDifferent")
    is_aborted = Boolean(data_key="isAborted")
    is_empty = Boolean(data_key="isEmpty")
    app_urls = Nested(SessionUrls, data_key="appUrls")
    api_urls = Nested(SessionUrls, data_key="apiUrls")
    steps_info = List(Nested(StepInfo), data_key="stepsInfo")
    baseline_id = String(data_key="baselineId")
    accessibility_status = Nested(
        SessionAccessibilityStatus, data_key="accessibilityStatus"
    )
    user_test_id = String(data_key="userTestId")

    @post_load
    def to_python(self, data, **_):
        return common.TestResults(**data)


class TestResultContainer(DeMarshalingSchema):
    test_results = Nested(TestResults, data_key="result")
    browser_info = BrowserInfo(data_key="environment")
    exception = Error(allow_none=True, data_key="error")
    user_test_id = String(data_key="userTestId")

    @post_load
    def to_python(self, data, **_):
        return common.TestResultContainer(**data)


class TestResultsSummary(DeMarshalingSchema):
    results = List(Nested(TestResultContainer))
    exceptions = Integer()
    passed = Integer()
    unresolved = Integer()
    failed = Integer()
    # these attributes get None value when Eyes.locate call fails
    mismatches = Integer(allow_none=True)
    missing = Integer(allow_none=True)
    matches = Integer(allow_none=True)

    @post_load
    def to_python(self, data, **_):
        return common.TestResultsSummary(**data)


def demarshal_locate_result(results):
    # type: (dict) -> t.Dict[t.Text, t.List[common.Region]]
    return {
        locator_id: [Region().load(r) for r in regions] if regions else []
        for locator_id, regions in results.items()
    }


def demarshal_locate_text_result(results):
    # type: (dict) -> t.Dict[t.Text, t.List[extract_text.TextRegion]]
    return {
        locator_id: ([LocateTextResponse().load(r) for r in regions] if regions else [])
        for locator_id, regions in results.items()
    }


def demarshal_test_results(results_list, conf):
    # type: (t.List[dict], config.Configuration) -> t.List[common.TestResults]
    # When locating visual locators, result might be None
    results = [TestResults().load(r) for r in results_list if r]
    for result in results:
        result.set_connection_config(conf.server_url, conf.api_key, conf.proxy)
    return results


def demarshal_close_manager_results(close_manager_result_dict, conf):
    # type: (dict, config.Configuration) -> common.TestResultsSummary
    results = TestResultsSummary().load(close_manager_result_dict)
    for container in results:
        if container.test_results:
            container.test_results.set_connection_config(
                conf.server_url, conf.api_key, conf.proxy
            )
    return results


def demarshal_server_info(info_dict):
    # type: (dict) -> common.ServerInfo
    return ServerInfo().load(info_dict)
