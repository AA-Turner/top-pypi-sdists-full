# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import abc

from contrast_vendor.webob.multidict import MultiDict


class BaseResponseWrapper(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def body(self) -> bytes:
        """
        Response body as bytes
        """

    @property
    @abc.abstractmethod
    def headers(self) -> MultiDict:
        """
        Response headers as a dictionary-like object.

        This object **MUST** support normalized case-insensitive lookup.
        For example, the following should all return the same value:

        my_response_wrapper.headers['content-length']
        my_response_wrapper.headers['Content-Length']
        my_response_wrapper.headers['CONTENT-LENGTH']
        ... any other case variation

        In order to properly extract response headers for analysis, we currently expect
        this field to be a multidict that implements a method called `dict_of_lists()`.
        """

    @property
    @abc.abstractmethod
    def status_code(self) -> int:
        """
        Status code as an integer
        """
