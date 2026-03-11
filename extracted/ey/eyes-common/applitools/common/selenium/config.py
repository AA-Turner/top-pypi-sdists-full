from __future__ import absolute_import, division, print_function

from copy import deepcopy
from typing import TYPE_CHECKING, List, Optional, Text, Tuple, Union, overload

import attr

from ..config import Configuration as ConfigurationBase
from ..layout_breakpoints_options import LayoutBreakpointsOptions
from ..ultrafastgrid import (
    AndroidDeviceInfo,
    AndroidDeviceTarget,
    AndroidMultiDeviceTarget,
    ChromeEmulationInfo,
    DesktopBrowserInfo,
    DeviceTarget,
    IosDeviceInfo,
    IosDeviceTarget,
    IosMultiDeviceTarget,
    IRenderBrowserInfo,
    ScreenOrientation,
    VisualGridOption,
)
from ..utils import argument_guard
from ..validators import is_list_or_tuple
from .misc import BrowserType, MobileOptions, StitchMode

if TYPE_CHECKING:
    from ..cut import CutProvider
    from ..ultrafastgrid import DeviceName

__all__ = ("Configuration",)


@attr.s
class Configuration(ConfigurationBase):
    force_full_page_screenshot = attr.ib(default=None)  # type: bool
    wait_before_screenshots = attr.ib(
        default=None,
    )  # type: Optional[int]  # ms
    stitch_mode = attr.ib(default=None)  # type: Optional[StitchMode]
    hide_scrollbars = attr.ib(default=None)  # type: bool
    hide_caret = attr.ib(default=None)  # type: Optional[bool]
    # Indicates that a mobile simulator is being used
    is_simulator = attr.ib(default=None)  # type: Optional[bool]

    # Rendering Configuration
    browsers_info = attr.ib(init=False, factory=list)  # type: List[IRenderBrowserInfo]
    visual_grid_options = attr.ib(
        default=None
    )  # type: Optional[Tuple[VisualGridOption]]
    disable_browser_fetching = attr.ib(default=None)  # type: Optional[bool]
    enable_cross_origin_rendering = attr.ib(default=None)  # type: Optional[bool]
    dont_use_cookies = attr.ib(default=None)  # type: Optional[bool]
    dont_close_batches = attr.ib(default=None)  # type: Optional[bool]
    layout_breakpoints = attr.ib(
        default=None
    )  # type: Union[bool, List[int], LayoutBreakpointsOptions, None]
    scale_ratio = attr.ib(default=None)  # type: Optional[float]
    cut_provider = attr.ib(default=None)  # type: Optional[CutProvider]
    rotation = attr.ib(default=None)  # type: Optional[int]
    mobile_options = attr.ib(default=None)  # type: Optional[MobileOptions]

    def set_force_full_page_screenshot(self, force_full_page_screenshot):
        # type: (bool) -> Configuration
        self.force_full_page_screenshot = force_full_page_screenshot
        return self

    def set_wait_before_screenshots(self, wait_before_screenshots):
        # type: (int) -> Configuration
        self.wait_before_screenshots = wait_before_screenshots
        return self

    def set_stitch_mode(self, stitch_mode):
        # type: (StitchMode) -> Configuration
        self.stitch_mode = stitch_mode
        return self

    def set_hide_scrollbars(self, hide_scrollbars):
        # type: (bool) -> Configuration
        self.hide_scrollbars = hide_scrollbars
        return self

    def set_hide_caret(self, hide_caret):
        # type: (bool) -> Configuration
        self.hide_caret = hide_caret
        return self

    def set_visual_grid_options(self, *options):
        # type: (*VisualGridOption) -> Configuration
        if options == (None,):
            self.visual_grid_options = None
        else:
            argument_guard.are_(options, VisualGridOption)
            self.visual_grid_options = options
        return self

    def set_disable_browser_fetching(self, disable_browser_fetching):
        # type: (bool) -> Configuration
        self.disable_browser_fetching = disable_browser_fetching
        return self

    def set_enable_cross_origin_rendering(self, enable_cross_origin_rendering):
        # type: (bool) -> Configuration
        self.enable_cross_origin_rendering = enable_cross_origin_rendering
        return self

    def set_dont_use_cookies(self, dont_use_cookies):
        # type: (bool) -> Configuration
        self.dont_use_cookies = dont_use_cookies
        return self

    @overload
    def set_layout_breakpoints(
        self,
        enabled: bool,
        *,
        reload: Optional[bool] = None,
        height_breakpoints: Optional[bool] = None
    ) -> "Configuration":
        pass

    @overload
    def set_layout_breakpoints(self, *breakpoints, **kwargs):
        # type: (*int, Optional[bool]) -> Configuration
        pass

    def set_layout_breakpoints(self, enabled_or_first, *rest, **kwargs):
        reload = kwargs.pop("reload", None)
        height_breakpoints = kwargs.pop("height_breakpoints", None)
        assert not kwargs, "Unexpected keyword arguments {}".format(kwargs)
        if isinstance(enabled_or_first, bool):
            assert (
                not rest
            ), "`reload` and `height_breakpoints` are keyword-only arguments"
            self.layout_breakpoints = LayoutBreakpointsOptions(
                enabled_or_first, reload, height_breakpoints
            )
        elif isinstance(enabled_or_first, int):
            self.layout_breakpoints = LayoutBreakpointsOptions(
                [enabled_or_first] + list(rest), reload, height_breakpoints
            )
        else:
            raise TypeError(
                "{} is not an instance of bool or int".format(enabled_or_first)
            )
        return self

    @overload  # noqa
    def add_browser(self, desktop_browser_info):
        # type: (DesktopBrowserInfo) -> Configuration
        pass

    @overload  # noqa
    def add_browser(self, ios_device_info):
        # type: (IosDeviceInfo) -> Configuration
        pass

    @overload  # noqa
    def add_browser(self, android_device_info):
        # type: (AndroidDeviceInfo) -> Configuration
        pass

    @overload  # noqa
    def add_browser(self, chrome_emulation_info):
        # type: (ChromeEmulationInfo) -> Configuration
        pass

    @overload  # noqa
    def add_browser(self, width, height, browser_type):
        # type: (int, int, BrowserType) -> Configuration
        pass

    @overload  # noqa
    def add_browser(self, width, height, browser_type, baseline_env_name):
        # type: (int, int, BrowserType, Text) -> Configuration
        pass

    def add_browser(self, *args):  # noqa
        if isinstance(args[0], IRenderBrowserInfo):
            self.browsers_info.append(args[0])
        elif (
            isinstance(args[0], int)
            and isinstance(args[1], int)
            and isinstance(args[2], BrowserType)
        ):
            if len(args) == 4:
                baseline_env_name = args[3]
            else:
                baseline_env_name = self.baseline_env_name
            self.browsers_info.append(
                DesktopBrowserInfo(args[0], args[1], args[2], baseline_env_name)
            )
        else:
            raise TypeError(
                "Unsupported parameter: \n\ttype: {} \n\tvalue: {}".format(
                    type(args), args
                )
            )
        return self

    @overload
    def add_browsers(self, renders_info):
        # type:(List[Union[DesktopBrowserInfo,IosDeviceInfo,AndroidDeviceInfo,ChromeEmulationInfo]])->Configuration  # noqa
        pass

    @overload
    def add_browsers(self, renders_info):
        # type:(*Union[DesktopBrowserInfo,IosDeviceInfo,AndroidDeviceInfo,ChromeEmulationInfo])->Configuration
        pass

    def add_browsers(self, *renders_info):
        if len(renders_info) == 1 and is_list_or_tuple(renders_info[0]):
            renders_info = renders_info[0]

        for render_info in renders_info:
            try:
                self.add_browser(render_info)
            except TypeError as e:
                raise TypeError("Wrong argument in .add_browsers()") from e
        return self

    def add_device_emulation(self, device_name, orientation=ScreenOrientation.PORTRAIT):
        # type: (DeviceName, ScreenOrientation) -> Configuration
        argument_guard.not_none(device_name)
        self.add_browser(ChromeEmulationInfo(device_name, orientation))
        return self

    def add_mobile_device(self, mobile_device_info):
        # type: (Union[IosDeviceInfo, AndroidDeviceInfo]) -> Configuration
        return self.add_mobile_devices(mobile_device_info)

    def add_mobile_devices(self, *mobile_device_infos):
        # type: (Union[IosDeviceInfo, AndroidDeviceInfo]) -> Configuration
        return self.add_browsers(*mobile_device_infos)

    def clone(self):
        # type: () -> Configuration
        # TODO: Remove this huck when get rid of Python2
        conf = super(Configuration, self).clone()
        conf.browsers_info = deepcopy(self.browsers_info)
        conf.visual_grid_options = deepcopy(self.visual_grid_options)
        return conf

    def add_multi_device_target(self, *device_targets):
        # type: (*Union[IosMultiDeviceTarget, AndroidMultiDeviceTarget]) -> Configuration
        for device_target in device_targets:
            if isinstance(
                device_target, (IosMultiDeviceTarget, AndroidMultiDeviceTarget)
            ):
                device_target = device_target()

            if isinstance(device_target, IosDeviceTarget):
                ios_device_info = IosDeviceInfo(
                    device_name=device_target.device_name,
                    screen_orientation=device_target.screen_orientation,
                    ios_version=device_target.version,
                )
                self.add_browser(ios_device_info)
            elif isinstance(device_target, AndroidDeviceTarget):
                android_device_info = AndroidDeviceInfo(
                    device_name=device_target.device_name,
                    screen_orientation=device_target.screen_orientation,
                    android_version=device_target.version,
                )
                self.add_browser(android_device_info)
            else:
                raise TypeError(
                    "All arguments must be instances of IosMultiDeviceTarget or AndroidMultiDeviceTarget"
                )
        return self

    def set_mobile_options(self, mobile_options):
        # type: (MobileOptions) -> Configuration
        self.mobile_options = mobile_options
        return self
