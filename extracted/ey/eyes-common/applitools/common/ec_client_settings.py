from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING

import attr

if TYPE_CHECKING:
    from typing import Optional, Text

    from .config import ProxySettings


@attr.s
class ECClientCapabilitiesOptions(object):
    api_key = attr.ib(default=None)  # type: Optional[Text]
    server_url = attr.ib(default=None)  # type: Optional[Text]


@attr.s
class ECClientSettings(object):
    options = attr.ib(
        type=ECClientCapabilitiesOptions
    )  # type: ECClientCapabilitiesOptions
    proxy = attr.ib(default=None)  # type: Optional[ProxySettings]
