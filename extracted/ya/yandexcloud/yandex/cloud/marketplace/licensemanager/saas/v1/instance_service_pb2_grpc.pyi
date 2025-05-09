"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.marketplace.licensemanager.saas.v1.instance_service_pb2
import yandex.cloud.marketplace.licensemanager.v1.instance_pb2
import yandex.cloud.marketplace.licensemanager.v1.user_info_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class InstanceServiceStub:
    """A set of methods for managing subscription instances."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.marketplace.licensemanager.saas.v1.instance_service_pb2.GetInstanceRequest,
        yandex.cloud.marketplace.licensemanager.v1.instance_pb2.Instance,
    ]
    """Returns the specified subscription instance."""

    GetUserInfo: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.marketplace.licensemanager.saas.v1.instance_service_pb2.GetUserInfoRequest,
        yandex.cloud.marketplace.licensemanager.v1.user_info_pb2.UserInfo,
    ]
    """Returns information about legal person (Russia only) who owns this subscription instance."""

class InstanceServiceAsyncStub:
    """A set of methods for managing subscription instances."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.marketplace.licensemanager.saas.v1.instance_service_pb2.GetInstanceRequest,
        yandex.cloud.marketplace.licensemanager.v1.instance_pb2.Instance,
    ]
    """Returns the specified subscription instance."""

    GetUserInfo: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.marketplace.licensemanager.saas.v1.instance_service_pb2.GetUserInfoRequest,
        yandex.cloud.marketplace.licensemanager.v1.user_info_pb2.UserInfo,
    ]
    """Returns information about legal person (Russia only) who owns this subscription instance."""

class InstanceServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing subscription instances."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.marketplace.licensemanager.saas.v1.instance_service_pb2.GetInstanceRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.marketplace.licensemanager.v1.instance_pb2.Instance, collections.abc.Awaitable[yandex.cloud.marketplace.licensemanager.v1.instance_pb2.Instance]]:
        """Returns the specified subscription instance."""

    @abc.abstractmethod
    def GetUserInfo(
        self,
        request: yandex.cloud.marketplace.licensemanager.saas.v1.instance_service_pb2.GetUserInfoRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.marketplace.licensemanager.v1.user_info_pb2.UserInfo, collections.abc.Awaitable[yandex.cloud.marketplace.licensemanager.v1.user_info_pb2.UserInfo]]:
        """Returns information about legal person (Russia only) who owns this subscription instance."""

def add_InstanceServiceServicer_to_server(servicer: InstanceServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
