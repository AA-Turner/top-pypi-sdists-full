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


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_ram.IPermissionAssociationRef")
class IPermissionAssociationRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a PermissionAssociation.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="permissionAssociationRef")
    def permission_association_ref(self) -> "PermissionAssociationReference":
        '''(experimental) A reference to a PermissionAssociation resource.

        :stability: experimental
        '''
        ...


class _IPermissionAssociationRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a PermissionAssociation.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_ram.IPermissionAssociationRef"

    @builtins.property
    @jsii.member(jsii_name="permissionAssociationRef")
    def permission_association_ref(self) -> "PermissionAssociationReference":
        '''(experimental) A reference to a PermissionAssociation resource.

        :stability: experimental
        '''
        return typing.cast("PermissionAssociationReference", jsii.get(self, "permissionAssociationRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPermissionAssociationRef).__jsii_proxy_class__ = lambda : _IPermissionAssociationRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_ram.IPermissionRef")
class IPermissionRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Permission.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="permissionRef")
    def permission_ref(self) -> "PermissionReference":
        '''(experimental) A reference to a Permission resource.

        :stability: experimental
        '''
        ...


class _IPermissionRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Permission.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_ram.IPermissionRef"

    @builtins.property
    @jsii.member(jsii_name="permissionRef")
    def permission_ref(self) -> "PermissionReference":
        '''(experimental) A reference to a Permission resource.

        :stability: experimental
        '''
        return typing.cast("PermissionReference", jsii.get(self, "permissionRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPermissionRef).__jsii_proxy_class__ = lambda : _IPermissionRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_ram.IPrincipalAssociationRef")
class IPrincipalAssociationRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a PrincipalAssociation.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="principalAssociationRef")
    def principal_association_ref(self) -> "PrincipalAssociationReference":
        '''(experimental) A reference to a PrincipalAssociation resource.

        :stability: experimental
        '''
        ...


class _IPrincipalAssociationRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a PrincipalAssociation.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_ram.IPrincipalAssociationRef"

    @builtins.property
    @jsii.member(jsii_name="principalAssociationRef")
    def principal_association_ref(self) -> "PrincipalAssociationReference":
        '''(experimental) A reference to a PrincipalAssociation resource.

        :stability: experimental
        '''
        return typing.cast("PrincipalAssociationReference", jsii.get(self, "principalAssociationRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPrincipalAssociationRef).__jsii_proxy_class__ = lambda : _IPrincipalAssociationRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_ram.IResourceAssociationRef")
class IResourceAssociationRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a ResourceAssociation.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="resourceAssociationRef")
    def resource_association_ref(self) -> "ResourceAssociationReference":
        '''(experimental) A reference to a ResourceAssociation resource.

        :stability: experimental
        '''
        ...


class _IResourceAssociationRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a ResourceAssociation.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_ram.IResourceAssociationRef"

    @builtins.property
    @jsii.member(jsii_name="resourceAssociationRef")
    def resource_association_ref(self) -> "ResourceAssociationReference":
        '''(experimental) A reference to a ResourceAssociation resource.

        :stability: experimental
        '''
        return typing.cast("ResourceAssociationReference", jsii.get(self, "resourceAssociationRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResourceAssociationRef).__jsii_proxy_class__ = lambda : _IResourceAssociationRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_ram.IResourceShareRef")
class IResourceShareRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a ResourceShare.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="resourceShareRef")
    def resource_share_ref(self) -> "ResourceShareReference":
        '''(experimental) A reference to a ResourceShare resource.

        :stability: experimental
        '''
        ...


class _IResourceShareRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a ResourceShare.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_ram.IResourceShareRef"

    @builtins.property
    @jsii.member(jsii_name="resourceShareRef")
    def resource_share_ref(self) -> "ResourceShareReference":
        '''(experimental) A reference to a ResourceShare resource.

        :stability: experimental
        '''
        return typing.cast("ResourceShareReference", jsii.get(self, "resourceShareRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResourceShareRef).__jsii_proxy_class__ = lambda : _IResourceShareRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_ram.ISourceAssociationRef")
class ISourceAssociationRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a SourceAssociation.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="sourceAssociationRef")
    def source_association_ref(self) -> "SourceAssociationReference":
        '''(experimental) A reference to a SourceAssociation resource.

        :stability: experimental
        '''
        ...


class _ISourceAssociationRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a SourceAssociation.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_ram.ISourceAssociationRef"

    @builtins.property
    @jsii.member(jsii_name="sourceAssociationRef")
    def source_association_ref(self) -> "SourceAssociationReference":
        '''(experimental) A reference to a SourceAssociation resource.

        :stability: experimental
        '''
        return typing.cast("SourceAssociationReference", jsii.get(self, "sourceAssociationRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISourceAssociationRef).__jsii_proxy_class__ = lambda : _ISourceAssociationRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_ram.PermissionAssociationReference",
    jsii_struct_bases=[],
    name_mapping={
        "permission_arn": "permissionArn",
        "resource_share_arn": "resourceShareArn",
    },
)
class PermissionAssociationReference:
    def __init__(
        self,
        *,
        permission_arn: builtins.str,
        resource_share_arn: builtins.str,
    ) -> None:
        '''A reference to a PermissionAssociation resource.

        :param permission_arn: The PermissionArn of the PermissionAssociation resource.
        :param resource_share_arn: The ResourceShareArn of the PermissionAssociation resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_ram as interfaces_ram
            
            permission_association_reference = interfaces_ram.PermissionAssociationReference(
                permission_arn="permissionArn",
                resource_share_arn="resourceShareArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__32334b9de58383c74e829f0d0039b1bc2f6f6c1eddedaa8b4b69893b40bf9667)
            check_type(argname="argument permission_arn", value=permission_arn, expected_type=type_hints["permission_arn"])
            check_type(argname="argument resource_share_arn", value=resource_share_arn, expected_type=type_hints["resource_share_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permission_arn": permission_arn,
            "resource_share_arn": resource_share_arn,
        }

    @builtins.property
    def permission_arn(self) -> builtins.str:
        '''The PermissionArn of the PermissionAssociation resource.'''
        result = self._values.get("permission_arn")
        assert result is not None, "Required property 'permission_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_share_arn(self) -> builtins.str:
        '''The ResourceShareArn of the PermissionAssociation resource.'''
        result = self._values.get("resource_share_arn")
        assert result is not None, "Required property 'resource_share_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PermissionAssociationReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_ram.PermissionReference",
    jsii_struct_bases=[],
    name_mapping={"permission_arn": "permissionArn"},
)
class PermissionReference:
    def __init__(self, *, permission_arn: builtins.str) -> None:
        '''A reference to a Permission resource.

        :param permission_arn: The Arn of the Permission resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_ram as interfaces_ram
            
            permission_reference = interfaces_ram.PermissionReference(
                permission_arn="permissionArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cfa3f97bc406de95182cb7061f24b81a30b9ef1f6b5ab54e34b402acd5885658)
            check_type(argname="argument permission_arn", value=permission_arn, expected_type=type_hints["permission_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permission_arn": permission_arn,
        }

    @builtins.property
    def permission_arn(self) -> builtins.str:
        '''The Arn of the Permission resource.'''
        result = self._values.get("permission_arn")
        assert result is not None, "Required property 'permission_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PermissionReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_ram.PrincipalAssociationReference",
    jsii_struct_bases=[],
    name_mapping={"principal": "principal", "resource_share_arn": "resourceShareArn"},
)
class PrincipalAssociationReference:
    def __init__(
        self,
        *,
        principal: builtins.str,
        resource_share_arn: builtins.str,
    ) -> None:
        '''A reference to a PrincipalAssociation resource.

        :param principal: The Principal of the PrincipalAssociation resource.
        :param resource_share_arn: The ResourceShareArn of the PrincipalAssociation resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_ram as interfaces_ram
            
            principal_association_reference = interfaces_ram.PrincipalAssociationReference(
                principal="principal",
                resource_share_arn="resourceShareArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__28746105a6a98aea5587a61cbc807532928ce5eb65db13234f194ae16b3c0a2a)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument resource_share_arn", value=resource_share_arn, expected_type=type_hints["resource_share_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principal": principal,
            "resource_share_arn": resource_share_arn,
        }

    @builtins.property
    def principal(self) -> builtins.str:
        '''The Principal of the PrincipalAssociation resource.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_share_arn(self) -> builtins.str:
        '''The ResourceShareArn of the PrincipalAssociation resource.'''
        result = self._values.get("resource_share_arn")
        assert result is not None, "Required property 'resource_share_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrincipalAssociationReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_ram.ResourceAssociationReference",
    jsii_struct_bases=[],
    name_mapping={
        "resource_arn": "resourceArn",
        "resource_share_arn": "resourceShareArn",
    },
)
class ResourceAssociationReference:
    def __init__(
        self,
        *,
        resource_arn: builtins.str,
        resource_share_arn: builtins.str,
    ) -> None:
        '''A reference to a ResourceAssociation resource.

        :param resource_arn: The ResourceArn of the ResourceAssociation resource.
        :param resource_share_arn: The ResourceShareArn of the ResourceAssociation resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_ram as interfaces_ram
            
            resource_association_reference = interfaces_ram.ResourceAssociationReference(
                resource_arn="resourceArn",
                resource_share_arn="resourceShareArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c73739cfbafc24c53d59d698c7f2332e01f6e9098e2ae36f8833711e40c2dd81)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument resource_share_arn", value=resource_share_arn, expected_type=type_hints["resource_share_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "resource_share_arn": resource_share_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''The ResourceArn of the ResourceAssociation resource.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_share_arn(self) -> builtins.str:
        '''The ResourceShareArn of the ResourceAssociation resource.'''
        result = self._values.get("resource_share_arn")
        assert result is not None, "Required property 'resource_share_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceAssociationReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_ram.ResourceShareReference",
    jsii_struct_bases=[],
    name_mapping={"resource_share_arn": "resourceShareArn"},
)
class ResourceShareReference:
    def __init__(self, *, resource_share_arn: builtins.str) -> None:
        '''A reference to a ResourceShare resource.

        :param resource_share_arn: The Arn of the ResourceShare resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_ram as interfaces_ram
            
            resource_share_reference = interfaces_ram.ResourceShareReference(
                resource_share_arn="resourceShareArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d05e6d9a057d581bc15e590623c6799f543dd64365bd5d095ac352a0fd449d36)
            check_type(argname="argument resource_share_arn", value=resource_share_arn, expected_type=type_hints["resource_share_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_share_arn": resource_share_arn,
        }

    @builtins.property
    def resource_share_arn(self) -> builtins.str:
        '''The Arn of the ResourceShare resource.'''
        result = self._values.get("resource_share_arn")
        assert result is not None, "Required property 'resource_share_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceShareReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_ram.SourceAssociationReference",
    jsii_struct_bases=[],
    name_mapping={"resource_share_arn": "resourceShareArn", "source_id": "sourceId"},
)
class SourceAssociationReference:
    def __init__(
        self,
        *,
        resource_share_arn: builtins.str,
        source_id: builtins.str,
    ) -> None:
        '''A reference to a SourceAssociation resource.

        :param resource_share_arn: The ResourceShareArn of the SourceAssociation resource.
        :param source_id: The SourceId of the SourceAssociation resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_ram as interfaces_ram
            
            source_association_reference = interfaces_ram.SourceAssociationReference(
                resource_share_arn="resourceShareArn",
                source_id="sourceId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e6b1e7971b3c2359d7073adbee5575fa3d2052e0708697b4927104b5981870a3)
            check_type(argname="argument resource_share_arn", value=resource_share_arn, expected_type=type_hints["resource_share_arn"])
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_share_arn": resource_share_arn,
            "source_id": source_id,
        }

    @builtins.property
    def resource_share_arn(self) -> builtins.str:
        '''The ResourceShareArn of the SourceAssociation resource.'''
        result = self._values.get("resource_share_arn")
        assert result is not None, "Required property 'resource_share_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_id(self) -> builtins.str:
        '''The SourceId of the SourceAssociation resource.'''
        result = self._values.get("source_id")
        assert result is not None, "Required property 'source_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceAssociationReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IPermissionAssociationRef",
    "IPermissionRef",
    "IPrincipalAssociationRef",
    "IResourceAssociationRef",
    "IResourceShareRef",
    "ISourceAssociationRef",
    "PermissionAssociationReference",
    "PermissionReference",
    "PrincipalAssociationReference",
    "ResourceAssociationReference",
    "ResourceShareReference",
    "SourceAssociationReference",
]

publication.publish()

def _typecheckingstub__32334b9de58383c74e829f0d0039b1bc2f6f6c1eddedaa8b4b69893b40bf9667(
    *,
    permission_arn: builtins.str,
    resource_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa3f97bc406de95182cb7061f24b81a30b9ef1f6b5ab54e34b402acd5885658(
    *,
    permission_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28746105a6a98aea5587a61cbc807532928ce5eb65db13234f194ae16b3c0a2a(
    *,
    principal: builtins.str,
    resource_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73739cfbafc24c53d59d698c7f2332e01f6e9098e2ae36f8833711e40c2dd81(
    *,
    resource_arn: builtins.str,
    resource_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05e6d9a057d581bc15e590623c6799f543dd64365bd5d095ac352a0fd449d36(
    *,
    resource_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b1e7971b3c2359d7073adbee5575fa3d2052e0708697b4927104b5981870a3(
    *,
    resource_share_arn: builtins.str,
    source_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IPermissionAssociationRef, IPermissionRef, IPrincipalAssociationRef, IResourceAssociationRef, IResourceShareRef, ISourceAssociationRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
