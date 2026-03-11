from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING, List, Optional, Text, TypeVar, overload

import attr

from .._dynamic_regions import DynamicSettings, DynamicTextTypeOrPattern
from ..accessibility import AccessibilityRegionType
from ..geometry import AccessibilityRegion, DynamicRegion, Rectangle, Region
from ..match import FloatingBounds, MatchLevel
from ..utils import argument_guard
from .region import (
    AccessibilityRegionByRectangle,
    DynamicRegionByRectangle,
    FloatingRegionByRectangle,
    GetAccessibilityRegion,
    GetDynamicRegion,
    GetFloatingRegion,
    GetRegion,
    RegionByRectangle,
)

if TYPE_CHECKING:
    from ..utils.custom_types import CodedRegionPadding, Union

__all__ = ("CheckSettings", "CheckSettingsValues")


@attr.s
class CheckSettingsValues(object):
    """
    Access to values stored in :py:class:`CheckSettings`
    """

    target_region = attr.ib(init=False, default=None)  # type: Optional[Region]
    timeout = attr.ib(init=False, default=None)  # type: Optional[int]  # milliseconds

    ignore_caret = attr.ib(init=False, default=None)  # type: Optional[bool]
    stitch_content = attr.ib(init=False, default=None)  # type: Optional[bool]
    match_level = attr.ib(init=False, default=None)  # type: Optional[MatchLevel]
    name = attr.ib(init=False, default=None)  # type: Optional[Text]

    send_dom = attr.ib(init=False, default=None)  # type: Optional[bool]
    use_dom = attr.ib(init=False, default=None)  # type: Optional[bool]
    enable_patterns = attr.ib(init=False, default=None)  # type: Optional[bool]
    ignore_displacements = attr.ib(init=False, default=None)  # type: Optional[bool]

    ignore_regions = attr.ib(init=False, factory=list)  # type: List[GetRegion]
    layout_regions = attr.ib(init=False, factory=list)  # type: List[GetRegion]
    strict_regions = attr.ib(init=False, factory=list)  # type: List[GetRegion]
    content_regions = attr.ib(init=False, factory=list)  # type: List[GetRegion]
    floating_regions = attr.ib(
        init=False, factory=list
    )  # type: List[GetFloatingRegion]
    accessibility_regions = attr.ib(
        init=False, factory=list
    )  # type: List[GetAccessibilityRegion]
    dynamic_regions = attr.ib(init=False, factory=list)  # type: List[GetDynamicRegion]
    variation_group_id = attr.ib(init=False, default=None)  # type: Optional[Text]
    wait_before_capture = attr.ib(default=None)  # type: Optional[int]
    page_id = attr.ib(default=None)  # type: Optional[Text]


Self = TypeVar("Self", bound="CheckSettings")


@attr.s
class CheckSettings(object):
    """
    The Match settings object to use in the various Eyes.Check methods.
    """

    Values = CheckSettingsValues  # value storage class overridable by child classes
    values = attr.ib(init=False)  # type: Self.Values

    def __attrs_post_init__(self):
        self.values = self.Values()

    def variation_group_id(self, variation_group_id):
        # type: (Text) -> Self
        self.values.variation_group_id = variation_group_id
        return self

    def layout(self, *regions, **kwargs):
        # type: (Self, *Region, **Optional[CodedRegionPadding])  -> Self
        """Shortcut to set the match level to :py:attr:`MatchLevel.LAYOUT`."""
        if not regions:
            self.values.match_level = MatchLevel.LAYOUT
            return self
        try:
            self.values.layout_regions = self.__regions(
                regions,
                method_name="layout_regions",
                padding=kwargs.get("padding"),
                region_id=kwargs.get("region_id"),
            )
        except TypeError as e:
            raise TypeError("Wrong argument in .layout()") from e
        return self

    def exact(self):
        """Shortcut to set the match level to :py:attr:`MatchLevel.EXACT` if no args"""
        self.values.match_level = MatchLevel.EXACT
        return self

    def strict(self, *regions, **kwargs):
        # type: (Self, *Region, **Optional[CodedRegionPadding])  -> Self
        """Shortcut to set the match level to :py:attr:`MatchLevel.STRICT` if no args"""
        if not regions:
            self.values.match_level = MatchLevel.STRICT
            return self
        try:
            self.values.strict_regions = self.__regions(
                regions,
                method_name="strict_regions",
                padding=kwargs.get("padding"),
                region_id=kwargs.get("region_id"),
            )
        except TypeError as e:
            raise TypeError("Wrong argument in .strict()") from e
        return self

    def content(self, *regions, **kwargs):
        # type: (Self, *Region, **Optional[CodedRegionPadding])  -> Self
        """
        Set match level to :py:attr:`MatchLevel.IGNORE_COLORS` if no args provided
        or add one or more ignore colors regions with optional padding.

        This method is kept for backward compatibility.
        """
        return self.ignore_colors(*regions, **kwargs)

    def ignore_colors(self, *regions, **kwargs):
        # type: (Self, *Region, **Optional[CodedRegionPadding])  -> Self
        """
        Set match level to :py:attr:`MatchLevel.IGNORE_COLORS` if no args provided
        or add one or more ignore colors regions with optional padding.
        """
        if not regions:
            self.values.match_level = MatchLevel.IGNORE_COLORS
            return self
        try:
            self.values.content_regions = self.__regions(
                regions,
                method_name="content_regions",
                padding=kwargs.get("padding"),
                region_id=kwargs.get("region_id"),
            )
        except TypeError as e:
            raise TypeError("Wrong argument in .content()") from e
        return self

    def ignore(self, *regions, **kwargs):
        # type: (Self, *Region, **Union[CodedRegionPadding, Text])  -> Self
        """Adds one or more ignore regions."""
        try:
            self.values.ignore_regions = self.__regions(
                regions,
                method_name="ignore_regions",
                padding=kwargs.get("padding"),
                region_id=kwargs.get("region_id"),
            )
        except TypeError as e:
            raise TypeError("Wrong argument in .ignore()") from e
        return self

    @overload  # noqa
    def accessibility(self, region):
        # type:(Self, AccessibilityRegion) -> Self
        pass

    @overload  # noqa
    def accessibility(self, region, type):
        # type:(Self, Region, AccessibilityRegionType) -> Self
        pass

    def accessibility(self, region, type=None):  # noqa
        """Adds one accessibility region."""
        if type:
            argument_guard.is_a(type, AccessibilityRegionType)
        try:
            self.values.accessibility_regions.append(
                self._accessibility_provider_from(region, type)
            )
        except TypeError as e:
            raise TypeError("Wrong argument in .accessibility()") from e
        return self

    @overload  # noqa
    def dynamic(self):
        # type:(Self) -> Self
        pass

    @overload  # noqa
    def dynamic(self, region):
        # type:(Self, DynamicRegion) -> Self
        pass

    @overload  # noqa
    def dynamic(self, region, *text_types):
        # type:(Self, Region, *DynamicTextTypeOrPattern) -> Self
        pass

    def dynamic(self, *args, **kwargs):
        """Adds one dynamic region."""
        if len(args) == 0:
            self.values.match_level = MatchLevel.DYNAMIC
            return self

        region = args[0]
        text_types = args[1:]

        dynamic_settings = None
        if text_types:
            dynamic_settings = DynamicSettings.from_(text_types)
        try:
            self.values.dynamic_regions.append(
                self._dynamic_provider_from(
                    region, dynamic_settings, padding=kwargs.get("padding")
                )
            )
        except TypeError as e:
            raise TypeError("Wrong argument in .dynamic()") from e
        return self

    @overload  # noqa
    def floating(self, max_offset, region):
        # type: (Self, int, Region) -> Self
        pass

    @overload  # noqa
    def floating(
        self, region, max_up_offset, max_down_offset, max_left_offset, max_right_offset
    ):
        # type: (Self, Region, int, int, int, int) -> Self
        pass

    def floating(self, *args):  # noqa
        """
        Adds a floating region. Region and max_offset or [max_up_offset, max_down_offset, "
                "max_left_offset, max_right_offset] are required parameters.

        :param arg1: max_offset | Region
        :param arg2: Region     | max_up_offset
        :param arg3: None       | max_down_offset
        :param arg4: None       | max_left_offset
        :param arg5: None       | max_right_offset
        """
        if len(args) < 2:
            raise TypeError("Not enough arguments")
        if isinstance(args[0], int) and not isinstance(args[1], int):
            max_offset = args[0]  # type: int
            region = args[1]  # type: ignore
            bounds = FloatingBounds(
                max_up_offset=max_offset,
                max_down_offset=max_offset,
                max_left_offset=max_offset,
                max_right_offset=max_offset,
            )
        elif (
            isinstance(args[1], int)
            and isinstance(args[2], int)
            and isinstance(args[3], int)
            and isinstance(args[4], int)
        ):
            region = args[0]  # type: ignore
            bounds = FloatingBounds(
                max_up_offset=args[1],
                max_down_offset=args[2],
                max_left_offset=args[3],
                max_right_offset=args[4],
            )
        else:
            raise TypeError("No type match")
        try:
            region_or_container = self._floating_provider_from(region, bounds)
        except TypeError as e:
            raise TypeError("Wrong arguments in .floating()") from e
        self.values.floating_regions.append(region_or_container)
        return self

    def send_dom(self, senddom=True):
        # type: (bool) -> Self
        """
        Defines whether to send the document DOM or not.
        """
        self.values.send_dom = senddom
        return self

    def use_dom(self, use=True):
        # type: (bool) -> Self
        """
        Defines useDom for enabling the match algorithm to use dom.
        """
        self.values.use_dom = use
        return self

    def enable_patterns(self, enable=True):
        # type: (bool) -> Self
        self.values.enable_patterns = enable
        return self

    def ignore_displacements(self, should_ignore=True):
        # type: (bool) -> Self
        self.values.ignore_displacements = should_ignore
        return self

    def match_level(self, match_level):
        # type: (MatchLevel)  -> Self
        self.values.match_level = match_level
        return self

    def ignore_caret(self, ignore=True):
        # type: (bool)  -> Self
        self.values.ignore_caret = ignore
        return self

    def fully(self, fully=True):
        # type: (bool)  -> Self
        self.values.stitch_content = fully
        return self

    def with_name(self, name):
        # type: (Text)  -> Self
        self.values.name = name
        return self

    def page_id(self, page_id):
        # type: (Text) -> Self
        self.values.page_id = page_id
        return self

    def stitch_content(self, stitch_content=True):
        # type: (bool)  -> Self
        self.values.stitch_content = stitch_content
        return self

    def timeout(self, timeout):
        # type: (int)  -> Self
        self.values.timeout = timeout
        return self

    def wait_before_capture(self, milliseconds):
        # type: (int) -> Self
        self.values.wait_before_capture = milliseconds
        return self

    def __regions(self, regions, method_name, padding, region_id):
        if not regions:
            raise TypeError(
                "{name} method called without arguments!".format(name=method_name)
            )

        regions_list = getattr(self.values, method_name)
        for region in regions:
            regions_list.append(
                self._region_provider_from(region, method_name, padding, region_id)
            )
        return regions_list

    def _region_provider_from(self, region, method_name, padding, region_id):
        if isinstance(region, Region):
            return RegionByRectangle(region)
        raise TypeError(
            "Unsupported region: \n\ttype: {} \n\tvalue: {}".format(
                type(region), region
            )
        )

    def _floating_provider_from(self, region, bounds):
        if isinstance(region, Region):
            return FloatingRegionByRectangle(Region.from_(region), bounds)
        raise TypeError(
            "Unsupported floating region: \n\ttype: {} \n\tvalue: {}".format(
                type(region), region
            )
        )

    def _accessibility_provider_from(self, region, accessibility_region_type):
        if isinstance(region, (Region, Rectangle)) and accessibility_region_type:
            return AccessibilityRegionByRectangle(region, accessibility_region_type)
        elif isinstance(region, AccessibilityRegion):
            return AccessibilityRegionByRectangle(region)
        raise TypeError(
            "Unsupported accessibility region: \n\ttype: {} \n\tvalue: {}".format(
                type(region), region
            )
        )

    def _dynamic_provider_from(self, region, dynamic_settings, padding=None):
        if isinstance(region, (Region, Rectangle)):
            return DynamicRegionByRectangle(region, dynamic_settings, padding)
        raise TypeError(
            "Unsupported dynamic region: \n\ttype: {} \n\tvalue: {}".format(
                type(region), region
            )
        )
