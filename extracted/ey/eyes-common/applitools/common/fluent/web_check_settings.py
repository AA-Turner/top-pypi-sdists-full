from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, List, Optional, Text, Tuple, TypeVar, Union, overload

import attr

from ..accessibility import AccessibilityRegionType
from ..geometry import AccessibilityRegion, Region
from ..layout_breakpoints_options import LayoutBreakpointsOptions
from ..ultrafastgrid import VisualGridOption
from ..utils import argument_guard
from ..validators import is_list_or_tuple, is_webelement
from .check_settings import CheckSettings, CheckSettingsValues
from .region import (
    AccessibilityRegionBySelector,
    DynamicRegionBySelector,
    FloatingRegionBySelector,
    RegionBySelector,
)
from .target_path import RegionLocator, TargetPath

if TYPE_CHECKING:
    from ..extract_text import OCRRegion
    from ..utils.custom_types import (
        FLOATING_VALUES,
        AnyWebElement,
        BySelector,
        CodedRegionPadding,
        CssSelector,
        FrameIndex,
        FrameNameOrId,
    )

BEFORE_CAPTURE_SCREENSHOT = "beforeCaptureScreenshot"


@attr.s
class FrameLocator(object):
    frame_locator = attr.ib(default=None)  # type: RegionLocator
    frame_name_or_id = attr.ib(default=None)  # type: FrameNameOrId
    frame_index = attr.ib(default=None)  # type: FrameIndex
    scroll_root_locator = attr.ib(default=None)  # type: RegionLocator


@attr.s
class LazyLoadOptions(object):
    scroll_length = attr.ib(default=None)  # type: Optional[int]
    waiting_time = attr.ib(default=None)  # type: Optional[int]
    max_amount_to_scroll = attr.ib(default=None)  # type: Optional[int]


@attr.s
class WebCheckSettingsValues(CheckSettingsValues):
    # hide_caret = attr.ib(init=False, default=None)
    scroll_root_locator = attr.ib(init=False, default=None)  # type: RegionLocator
    target_locator = attr.ib(init=False, default=None)  # type: RegionLocator
    frame_chain = attr.ib(init=False, factory=list)  # type: List[FrameLocator]

    script_hooks = attr.ib(factory=dict)  # type: dict
    visual_grid_options = attr.ib(default=())  # type: Tuple[VisualGridOption]
    disable_browser_fetching = attr.ib(default=None)  # type: Optional[bool]
    ocr_region = attr.ib(init=False, default=None)  # type: Optional[OCRRegion]
    layout_breakpoints = attr.ib(
        default=None
    )  # type: Union[bool, List[int], LayoutBreakpointsOptions, None]
    lazy_load = attr.ib(default=None)  # type: Optional[LazyLoadOptions]
    webview = attr.ib(default=None)  # type: Union[None, bool, Text]
    screenshot_mode = attr.ib(default=None)  # type: Optional[Text]

    @property
    def size_mode(self):
        if self.is_target_empty:
            if self.stitch_content:
                return "full-page"
            return "viewport"
        elif self.target_region:
            return "region"
        elif self.stitch_content:
            return "full-selector"
        return "selector"

    @property
    def is_target_empty(self):
        # type: () -> bool
        return self.target_region is None and self.target_locator is None


Self = TypeVar("Self", bound="WebCheckSettings")


@attr.s
class WebCheckSettings(CheckSettings):
    Values = WebCheckSettingsValues

    @overload  # noqa
    def layout(
        self,
        *by,  # type: BySelector
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def layout(
        self,
        *element,  # type: AnyWebElement
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def layout(
        self,
        *css_selector,  # type: CssSelector
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def layout(
        self,
        *target_path,  # type: RegionLocator
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def layout(
        self,
        *region,  # type: Region
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    def layout(self, *region, **kwargs):  # noqa
        """
        Adds one or more layout regions. And allow to set up paddings for them.

        :param kwargs: accepts `padding` parameter where there region paddings
         could be specified.
         Example of definition: `padding=dict(top=10, left=10, right=11, bottom=12)`
          where each keys are optional
        """
        return super(WebCheckSettings, self).layout(*region, **kwargs)

    @overload  # noqa
    def strict(
        self,
        *by,  # type: BySelector
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def strict(
        self,
        *element,  # type: AnyWebElement
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def strict(
        self,
        *css_selector,  # type: CssSelector
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def strict(
        self,
        *target_path,  # type: RegionLocator
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def strict(
        self,
        *region,  # type: Region
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    def strict(self, *region, **kwargs):  # noqa
        """
        Adds one or more strict regions. And allow to set up paddings for them.

        :param kwargs: accepts `padding` parameter where there region paddings
         could be specified.
         Example of definition: `padding=dict(top=10, left=10, right=11, bottom=12)`
          where each keys are optional
        """
        return super(WebCheckSettings, self).strict(*region, **kwargs)

    @overload  # noqa
    def content(
        self,
        *by,  # type: BySelector
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def content(
        self,
        *element,  # type: AnyWebElement
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def content(
        self,
        *css_selector,  # type: CssSelector
        **kwargs  # type: Union[CodedRegionPadding,Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def content(
        self,
        *target_path,  # type: RegionLocator
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def content(
        self,
        *region,  # type: Region
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    def content(self, *region, **kwargs):  # noqa
        """
        Adds one or more ignore colors regions. Optionally set up paddings for them.

        :param kwargs: accepts `padding` parameter that specifies padding for regions.
         Example of definition: `padding=dict(top=10, left=10, right=11, bottom=12)`
          where all keys are optional.

        This method is kept for backward compatibility.
        """
        return super(WebCheckSettings, self).ignore_colors(*region, **kwargs)

    @overload  # noqa
    def ignore_colors(
        self,
        *by,  # type: BySelector
        **kwargs  # type: Union[Text, CodedRegionPadding]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def ignore_colors(
        self,
        *element,  # type: AnyWebElement
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def ignore_colors(
        self,
        *css_selector,  # type: CssSelector
        **kwargs  # type: Union[CodedRegionPadding,Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def ignore_colors(
        self,
        *target_path,  # type: RegionLocator
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def ignore_colors(
        self,
        *region,  # type: Region
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    def ignore_colors(self, *region, **kwargs):  # noqa
        """
        Adds one or more ignore colors regions. Optionally set up paddings for them.

        :param kwargs: accepts `padding` parameter that specifies padding for regions.
         Example of definition: `padding=dict(top=10, left=10, right=11, bottom=12)`
          where all keys are optional
        """
        return super(WebCheckSettings, self).ignore_colors(*region, **kwargs)

    @overload  # noqa
    def ignore(
        self,
        *by,  # type: BySelector
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def ignore(
        self,
        *element,  # type: AnyWebElement
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def ignore(
        self,
        *css_selector,  # type: CssSelector
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def ignore(
        self,
        *target_path,  # type: RegionLocator
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    @overload  # noqa
    def ignore(
        self,
        *region,  # type: Region
        **kwargs  # type: Union[CodedRegionPadding, Text]
    ):
        # type: (...) -> Self
        pass

    def ignore(self, *region, **kwargs):  # noqa
        """
        Adds one or more ignore regions. And allow to set up paddings for them.

        :param kwargs: accepts `padding` parameter where there region paddings
         could be specified.
         Example of definition: `padding=dict(top=10, left=10, right=11, bottom=12)`
          where each keys are optional
        """
        return super(WebCheckSettings, self).ignore(*region, **kwargs)

    @overload  # noqa
    def floating(self, max_offset, region):
        # type: (int, FLOATING_VALUES) -> Self
        pass

    @overload  # noqa
    def floating(
        self, region, max_up_offset, max_down_offset, max_left_offset, max_right_offset
    ):
        # type: (FLOATING_VALUES, int, int, int, int) -> Self
        pass

    def floating(self, *args):  # noqa
        return super(WebCheckSettings, self).floating(*args)

    @overload  # noqa
    def accessibility(self, region):  # noqa
        # type:(AccessibilityRegion) -> Self
        pass

    @overload  # noqa
    def accessibility(self, css_selector, type):  # noqa
        # type:(CssSelector, AccessibilityRegionType) -> Self
        pass

    @overload  # noqa
    def accessibility(self, target_path, type):  # noqa
        # type:(RegionLocator, AccessibilityRegionType) -> Self
        pass

    @overload  # noqa
    def accessibility(self, by, type):  # noqa
        # type:(BySelector, AccessibilityRegionType) -> Self
        pass

    @overload  # noqa
    def accessibility(self, element, type):  # noqa
        # type:(AnyWebElement, AccessibilityRegionType) -> Self
        pass

    @overload  # noqa
    def accessibility(self, region, type):  # noqa
        # type:(Region, AccessibilityRegionType) -> Self
        pass

    def accessibility(self, region, type=None):  # noqa
        # type:(...) -> Self
        return super(WebCheckSettings, self).accessibility(region, type)

    @overload  # noqa
    def region(self, region):  # noqa
        # type: (Region) -> Self
        pass

    @overload  # noqa
    def region(self, css_selector):  # noqa
        # type: (CssSelector) -> Self
        pass

    @overload  # noqa
    def region(self, target_path):  # noqa
        # type: (RegionLocator) -> Self
        pass

    @overload  # noqa
    def region(self, element):  # noqa
        # type: (AnyWebElement) -> Self
        pass

    @overload  # noqa
    def region(self, by):  # noqa
        # type: (BySelector) -> Self
        pass

    def region(self, region):  # noqa
        # type:(...) -> Self
        if isinstance(region, Region):
            self.values.target_region = region
        elif is_list_or_tuple(region):
            path = self.values.target_locator or TargetPath
            self.values.target_locator = path.region(*region)
        elif isinstance(region, str) or is_webelement(region):
            path = self.values.target_locator or TargetPath
            self.values.target_locator = path.region(region)
        elif isinstance(region, RegionLocator):
            self.values.target_locator = region
        else:
            raise TypeError("region method called with argument of unknown type!")
        return self

    @overload  # noqa
    def frame(self, frame_name_or_id):
        # type: (FrameNameOrId) -> Self
        pass

    @overload  # noqa
    def frame(self, element):
        # type: (AnyWebElement) -> Self
        pass

    @overload  # noqa
    def frame(self, index):
        # type: (FrameIndex) -> Self
        pass

    @overload  # noqa
    def frame(self, by):
        # type: (BySelector) -> Self
        pass

    @overload  # noqa
    def frame(self, target_path):
        # type: (RegionLocator) -> Self
        pass

    def frame(self, frame):  # noqa
        # type:(...) -> Self
        fl = FrameLocator()
        if isinstance(frame, int):
            fl.frame_index = frame
        elif isinstance(frame, str):
            fl.frame_name_or_id = frame
        elif is_webelement(frame):
            fl.frame_locator = TargetPath.frame(frame)
        elif is_list_or_tuple(frame):
            fl.frame_locator = TargetPath.frame(*frame)
        elif isinstance(frame, RegionLocator):
            fl.frame_locator = frame
        else:
            raise TypeError("frame method called with argument of unknown type!")
        self.values.frame_chain.append(fl)
        return self

    def before_render_screenshot_hook(self, hook):
        # type: (Text) -> Self
        self.values.script_hooks[BEFORE_CAPTURE_SCREENSHOT] = hook
        return self

    def _region_provider_from(self, region, method_name, padding, region_id):
        if isinstance(region, str) or is_webelement(region):
            return RegionBySelector(TargetPath.region(region), padding, region_id)
        elif is_list_or_tuple(region):
            return RegionBySelector(TargetPath.region(*region), padding, region_id)
        elif isinstance(region, RegionLocator):
            return RegionBySelector(region, padding, region_id)
        return super(WebCheckSettings, self)._region_provider_from(
            region, method_name, padding, region_id
        )

    def _set_scroll_root_locator(self, target_path):
        if len(self.values.frame_chain) == 0:
            self.values.scroll_root_locator = target_path
        else:
            self.values.frame_chain[-1].scroll_root_locator = target_path

    @overload  # noqa
    def scroll_root_element(self, element):
        # type: (AnyWebElement) -> Self
        pass

    @overload  # noqa
    def scroll_root_element(self, selector):
        # type: (CssSelector) -> Self
        pass

    @overload  # noqa
    def scroll_root_element(self, target_path):
        # type: (RegionLocator) -> Self
        pass

    @overload  # noqa
    def scroll_root_element(self, by):
        # type: (BySelector) -> Self
        pass

    def scroll_root_element(self, element_or_selector):  # noqa
        if isinstance(element_or_selector, str) or is_webelement(element_or_selector):
            self._set_scroll_root_locator(TargetPath.region(element_or_selector))
        elif is_list_or_tuple(element_or_selector):
            self._set_scroll_root_locator(TargetPath.region(*element_or_selector))
        elif isinstance(element_or_selector, RegionLocator):
            self._set_scroll_root_locator(element_or_selector)
        else:
            raise TypeError("Unsupported type of scroll root element")
        return self

    def _floating_provider_from(self, region, bounds):
        if isinstance(region, str) or is_webelement(region):
            return FloatingRegionBySelector(TargetPath.region(region), bounds)
        elif is_list_or_tuple(region):
            return FloatingRegionBySelector(TargetPath.region(*region), bounds)
        elif isinstance(region, RegionLocator):
            return FloatingRegionBySelector(region, bounds)
        return super(WebCheckSettings, self)._floating_provider_from(region, bounds)

    def _accessibility_provider_from(self, region, accessibility_region_type):
        if isinstance(region, str) or is_webelement(region):
            return AccessibilityRegionBySelector(
                TargetPath.region(region), accessibility_region_type
            )
        elif is_list_or_tuple(region):
            return AccessibilityRegionBySelector(
                TargetPath.region(*region), accessibility_region_type
            )
        elif isinstance(region, RegionLocator):
            return AccessibilityRegionBySelector(region, accessibility_region_type)
        return super(WebCheckSettings, self)._accessibility_provider_from(
            region, accessibility_region_type
        )

    def _dynamic_provider_from(self, region, dynamic_settings, padding=None):
        if isinstance(region, str) or is_webelement(region):
            return DynamicRegionBySelector(
                TargetPath.region(region), dynamic_settings, padding
            )
        elif is_list_or_tuple(region):
            return DynamicRegionBySelector(
                TargetPath.region(*region), dynamic_settings, padding
            )
        elif isinstance(region, RegionLocator):
            return DynamicRegionBySelector(region, dynamic_settings, padding)
        return super(WebCheckSettings, self)._dynamic_provider_from(
            region, dynamic_settings, padding
        )

    def visual_grid_options(self, *options):
        # type: (*VisualGridOption) -> Self
        argument_guard.are_(options, VisualGridOption)
        self.values.visual_grid_options = options
        return self

    def disable_browser_fetching(self, disable=True):
        # type: (bool) -> Self
        self.values.disable_browser_fetching = disable
        return self

    @overload
    def layout_breakpoints(
        self,
        enabled: bool,
        *,
        reload: Optional[bool] = None,
        height_breakpoints: Optional[bool] = None
    ) -> Self:
        pass

    @overload
    def layout_breakpoints(self, *breakpoints, **kwargs):
        # type: (*int, Optional[bool]) -> Self
        pass

    def layout_breakpoints(self, enabled_or_first, *rest, **kwargs):
        reload = kwargs.pop("reload", None)
        height_breakpoints = kwargs.pop("height_breakpoints", None)
        assert not kwargs, "Unexpected keyword arguments {}".format(kwargs)
        if isinstance(enabled_or_first, bool):
            assert (
                not rest
            ), "`reload` and `height_breakpoints` are keyword-only arguments"
            self.values.layout_breakpoints = LayoutBreakpointsOptions(
                enabled_or_first, reload, height_breakpoints
            )
        elif isinstance(enabled_or_first, int):
            self.values.layout_breakpoints = LayoutBreakpointsOptions(
                [enabled_or_first] + list(rest), reload, height_breakpoints
            )
        else:
            raise TypeError(
                "{} is not an instance of bool or int".format(enabled_or_first)
            )
        return self

    def lazy_load(
        self, scroll_length=None, waiting_time=None, max_amount_to_scroll=None
    ):
        # type: (Optional[int], Optional[int], Optional[int]) -> Self
        value = LazyLoadOptions(scroll_length, waiting_time, max_amount_to_scroll)
        self.values.lazy_load = value
        return self

    @overload
    def webview(self):
        # type: () -> Self
        pass

    @overload
    def webview(self, use_default):
        # type: (bool) -> Self
        pass

    @overload
    def webview(self, webview_id):
        # type: (Text) -> Self
        pass

    def webview(self, webview=True):
        self.values.webview = webview
        return self

    def use_system_screenshot(self, should_use=True):
        self.values.screenshot_mode = "default" if should_use else "applitools-lib"
        return self

    @property
    def is_check_window(self):
        # type: () -> bool
        return self.values.is_target_empty
