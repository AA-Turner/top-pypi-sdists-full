from __future__ import absolute_import, division, print_function

from base64 import b64encode
from io import BytesIO
from typing import TYPE_CHECKING

import attr

from ..optional_deps import Image, PathLike, fspath
from .web_check_settings import WebCheckSettings, WebCheckSettingsValues

if TYPE_CHECKING:
    from typing import ByteString, Optional, Text, Union


@attr.s
class ImagesCheckSettingsValues(WebCheckSettingsValues):
    image = attr.ib(default=None)  # type: Optional[Text]
    dom = attr.ib(default=None)  # type: Optional[Text]


@attr.s
class ImagesCheckSettings(WebCheckSettings):
    Values = ImagesCheckSettingsValues

    def with_dom(self, dom):
        # type: (Text) -> ImagesCheckSettings
        """
        Attach given DOM source text to the image.
        Needed by the Root Cause Analysis tool
        """
        self.values.dom = dom
        return self


def image_path_or_bytes(image_or_path):
    # type: (Union[ByteString, Image, Text, PathLike]) -> Text
    if isinstance(image_or_path, bytes):
        image_bytes = b64encode(image_or_path)
        return image_bytes.decode("utf-8")
    elif isinstance(image_or_path, PathLike):
        return fspath(image_or_path)
    elif isinstance(image_or_path, Image):
        image_bytes = BytesIO()
        image_or_path.save(image_bytes, format="PNG")
        image_bytes = b64encode(image_bytes.getvalue())
        return image_bytes.decode("utf-8")
    elif isinstance(image_or_path, str):
        return image_or_path
    else:
        raise ValueError("Invalid image type", type(image_or_path))
