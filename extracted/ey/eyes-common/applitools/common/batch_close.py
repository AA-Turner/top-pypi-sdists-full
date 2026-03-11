from __future__ import absolute_import, division, print_function

from typing import List, Optional, Text, Union

import attr

from . import ProxySettings
from .command_executor import CommandExecutor
from .runner import EyesRunner
from .utils import argument_guard
from .utils.general_utils import get_env_with_prefix


@attr.s
class _EnabledBatchClose(object):
    _ids = attr.ib()  # type: List[Text]
    server_url = attr.ib()  # type: Text
    api_key = attr.ib()  # type: Text
    proxy = attr.ib(default=None)  # type: Optional[ProxySettings]
    batch_id = attr.ib(default=None)  # type: Text

    def set_url(self, url):
        # type: (Text) -> _EnabledBatchClose
        self.server_url = url
        return self

    def set_api_key(self, api_key):
        # type: (Text) -> _EnabledBatchClose
        self.api_key = api_key
        return self

    def set_proxy(self, proxy):
        # type: (ProxySettings) -> _EnabledBatchClose
        argument_guard.is_a(proxy, ProxySettings)
        self.proxy = proxy
        return self

    def close(self):
        cmd = CommandExecutor.get_instance(EyesRunner.Protocol)
        cmd.core_close_batch(self)


@attr.s
class BatchClose(object):
    api_key = attr.ib(
        factory=lambda: get_env_with_prefix("APPLITOOLS_API_KEY", None)
    )  # type: Optional[Text]
    server_url = attr.ib(default=None)  # type: Optional[Text]
    proxy = attr.ib(default=None)  # type: Optional[ProxySettings]

    def set_url(self, url):
        # type: (Text) -> BatchClose
        self.server_url = url
        return self

    def set_api_key(self, api_key):
        # type: (Text) -> BatchClose
        self.api_key = api_key
        return self

    def set_proxy(self, proxy):
        # type: (ProxySettings) -> BatchClose
        argument_guard.is_a(proxy, ProxySettings)
        self.proxy = proxy
        return self

    def set_batch_ids(self, *ids):
        # type: (Union[Text, List[Text]]) -> _EnabledBatchClose
        if isinstance(ids[0], list):
            ids = ids[0]
        return _EnabledBatchClose(ids, self.server_url, self.api_key, self.proxy)
