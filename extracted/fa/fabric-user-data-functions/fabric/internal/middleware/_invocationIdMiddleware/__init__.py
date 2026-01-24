# flake8: noqa: I005
from logging import Logger
import typing

from azure.functions import AppExtensionBase, Context, HttpResponse

INVOCATION_ID_HEADER = 'x-ms-invocation-id'
INVOCATION_ID_PARAMETER = 'reqInvocationId'

class InvocationIdMiddleware(AppExtensionBase):
    """A Python worker extension to add the invocation id to the response headers.
    """

    @classmethod
    def init(cls):
        pass

    @classmethod
    def configure(cls, *args, append_to_http_response:bool=False, **kwargs):
        pass

    @classmethod
    def pre_invocation_app_level(
        cls, logger: Logger, context: Context,
        func_args: typing.Dict[str, object],
        *args, **kwargs
    ) -> None:
        func_args.update({INVOCATION_ID_PARAMETER : context.invocation_id})

    @classmethod
    def post_invocation_app_level(
        cls, logger: Logger, context: Context,
        func_args: typing.Dict[str, object],
        func_ret: typing.Optional[object],
        *args, **kwargs
    ) -> None:
        if func_ret.headers is not None:
            func_ret.headers.add(INVOCATION_ID_HEADER, context.invocation_id)