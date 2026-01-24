# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast_vendor.webob.headers import ResponseHeaders
from contrast.agent.middlewares.response_wrappers.base_response_wrapper import (
    BaseResponseWrapper,
)


class AioHttpResponseWrapper(BaseResponseWrapper):
    def __init__(self, response):
        self._response = response
        self._streaming_cache = None

    @property
    def body(self):
        return self._response.body

    @property
    def headers(self):
        return ResponseHeaders(self._response.headers)

    @property
    def status_code(self):
        return self._response.status
