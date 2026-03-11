from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING, overload

from .images_check_settings import ImagesCheckSettings, image_path_or_bytes

if TYPE_CHECKING:
    from typing import ByteString, Text, Union

    from ..geometry import Region
    from ..optional_deps import Image, PathLike


class Target(object):
    """
    Fluent interface factory class for image targets
    """

    @staticmethod  # noqa
    @overload
    def image(image):
        # type: (Image) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    @overload
    def image(image):
        # type: (ByteString) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    @overload
    def image(path):
        # type: (Union[Text, PathLike]) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    def image(image_or_path):
        check_settings = ImagesCheckSettings()
        check_settings.values.image = image_path_or_bytes(image_or_path)
        return check_settings

    @staticmethod  # noqa
    @overload
    def region(image, rect):
        # type: (Image, Region) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    @overload
    def region(image, rect):
        # type: (ByteString, Region) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    @overload
    def region(path, rect):
        # type: (Union[Text, PathLike], Region) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    def region(image_or_path, rect):
        check_settings = Target.image(image_or_path)
        check_settings.values.target_region = rect
        return check_settings
