from __future__ import annotations

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from jsii._type_checking import cached_type_hints, check_type


from ..._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk.interfaces as _interfaces_8ca7e747
    import constructs as _constructs_77d1e7e8
else:

    _constructs_77d1e7e8 = _LazyImport("constructs")
    _interfaces_8ca7e747 = _LazyImport("aws_cdk.interfaces")


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_appfabric.AppAuthorizationReference",
    jsii_struct_bases=[],
    name_mapping={"app_authorization_arn": "appAuthorizationArn"},
)
class AppAuthorizationReference:
    def __init__(self, *, app_authorization_arn: builtins.str) -> None:
        '''A reference to a AppAuthorization resource.

        :param app_authorization_arn: The AppAuthorizationArn of the AppAuthorization resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_appfabric as interfaces_appfabric
            
            app_authorization_reference = interfaces_appfabric.AppAuthorizationReference(
                app_authorization_arn="appAuthorizationArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ba17382f5bcb502afdfb286355ee6c9d9098453583eb50af8d155391428934ec)
            check_type(argname="argument app_authorization_arn", value=app_authorization_arn, expected_type=type_hints["app_authorization_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_authorization_arn": app_authorization_arn,
        }

    @builtins.property
    def app_authorization_arn(self) -> builtins.str:
        '''The AppAuthorizationArn of the AppAuthorization resource.'''
        result = self._values.get("app_authorization_arn")
        assert result is not None, "Required property 'app_authorization_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppAuthorizationReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_appfabric.IAppAuthorizationRef")
class IAppAuthorizationRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a AppAuthorization.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="appAuthorizationRef")
    def app_authorization_ref(self) -> "AppAuthorizationReference":
        '''(experimental) A reference to a AppAuthorization resource.

        :stability: experimental
        '''
        ...


class _IAppAuthorizationRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a AppAuthorization.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_appfabric.IAppAuthorizationRef"

    @builtins.property
    @jsii.member(jsii_name="appAuthorizationRef")
    def app_authorization_ref(self) -> "AppAuthorizationReference":
        '''(experimental) A reference to a AppAuthorization resource.

        :stability: experimental
        '''
        return typing.cast("AppAuthorizationReference", jsii.get(self, "appAuthorizationRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAppAuthorizationRef).__jsii_proxy_class__ = lambda : _IAppAuthorizationRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_appfabric.IIngestionDestinationRef"
)
class IIngestionDestinationRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a IngestionDestination.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ingestionDestinationRef")
    def ingestion_destination_ref(self) -> "IngestionDestinationReference":
        '''(experimental) A reference to a IngestionDestination resource.

        :stability: experimental
        '''
        ...


class _IIngestionDestinationRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a IngestionDestination.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_appfabric.IIngestionDestinationRef"

    @builtins.property
    @jsii.member(jsii_name="ingestionDestinationRef")
    def ingestion_destination_ref(self) -> "IngestionDestinationReference":
        '''(experimental) A reference to a IngestionDestination resource.

        :stability: experimental
        '''
        return typing.cast("IngestionDestinationReference", jsii.get(self, "ingestionDestinationRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIngestionDestinationRef).__jsii_proxy_class__ = lambda : _IIngestionDestinationRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_appfabric.IngestionDestinationReference",
    jsii_struct_bases=[],
    name_mapping={"ingestion_destination_arn": "ingestionDestinationArn"},
)
class IngestionDestinationReference:
    def __init__(self, *, ingestion_destination_arn: builtins.str) -> None:
        '''A reference to a IngestionDestination resource.

        :param ingestion_destination_arn: The Arn of the IngestionDestination resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_appfabric as interfaces_appfabric
            
            ingestion_destination_reference = interfaces_appfabric.IngestionDestinationReference(
                ingestion_destination_arn="ingestionDestinationArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3699f08bc317604ae8d61df4e0f96f9dbcfe8a56a69f59e29c14a01747d69864)
            check_type(argname="argument ingestion_destination_arn", value=ingestion_destination_arn, expected_type=type_hints["ingestion_destination_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ingestion_destination_arn": ingestion_destination_arn,
        }

    @builtins.property
    def ingestion_destination_arn(self) -> builtins.str:
        '''The Arn of the IngestionDestination resource.'''
        result = self._values.get("ingestion_destination_arn")
        assert result is not None, "Required property 'ingestion_destination_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IngestionDestinationReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AppAuthorizationReference",
    "IAppAuthorizationRef",
    "IIngestionDestinationRef",
    "IngestionDestinationReference",
]

publication.publish()

def _typecheckingstub__ba17382f5bcb502afdfb286355ee6c9d9098453583eb50af8d155391428934ec(
    *,
    app_authorization_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3699f08bc317604ae8d61df4e0f96f9dbcfe8a56a69f59e29c14a01747d69864(
    *,
    ingestion_destination_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IAppAuthorizationRef, IIngestionDestinationRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
