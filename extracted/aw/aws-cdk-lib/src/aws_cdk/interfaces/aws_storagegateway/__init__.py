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


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.INFSFileShareRef")
class INFSFileShareRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a NFSFileShare.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="nfsFileShareRef")
    def nfs_file_share_ref(self) -> "NFSFileShareReference":
        '''(experimental) A reference to a NFSFileShare resource.

        :stability: experimental
        '''
        ...


class _INFSFileShareRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a NFSFileShare.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_storagegateway.INFSFileShareRef"

    @builtins.property
    @jsii.member(jsii_name="nfsFileShareRef")
    def nfs_file_share_ref(self) -> "NFSFileShareReference":
        '''(experimental) A reference to a NFSFileShare resource.

        :stability: experimental
        '''
        return typing.cast("NFSFileShareReference", jsii.get(self, "nfsFileShareRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INFSFileShareRef).__jsii_proxy_class__ = lambda : _INFSFileShareRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.ISMBFileShareRef")
class ISMBFileShareRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a SMBFileShare.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="smbFileShareRef")
    def smb_file_share_ref(self) -> "SMBFileShareReference":
        '''(experimental) A reference to a SMBFileShare resource.

        :stability: experimental
        '''
        ...


class _ISMBFileShareRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a SMBFileShare.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_storagegateway.ISMBFileShareRef"

    @builtins.property
    @jsii.member(jsii_name="smbFileShareRef")
    def smb_file_share_ref(self) -> "SMBFileShareReference":
        '''(experimental) A reference to a SMBFileShare resource.

        :stability: experimental
        '''
        return typing.cast("SMBFileShareReference", jsii.get(self, "smbFileShareRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISMBFileShareRef).__jsii_proxy_class__ = lambda : _ISMBFileShareRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.ITapePoolRef")
class ITapePoolRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a TapePool.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="tapePoolRef")
    def tape_pool_ref(self) -> "TapePoolReference":
        '''(experimental) A reference to a TapePool resource.

        :stability: experimental
        '''
        ...


class _ITapePoolRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a TapePool.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_storagegateway.ITapePoolRef"

    @builtins.property
    @jsii.member(jsii_name="tapePoolRef")
    def tape_pool_ref(self) -> "TapePoolReference":
        '''(experimental) A reference to a TapePool resource.

        :stability: experimental
        '''
        return typing.cast("TapePoolReference", jsii.get(self, "tapePoolRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITapePoolRef).__jsii_proxy_class__ = lambda : _ITapePoolRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.ITapeRef")
class ITapeRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Tape.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="tapeRef")
    def tape_ref(self) -> "TapeReference":
        '''(experimental) A reference to a Tape resource.

        :stability: experimental
        '''
        ...


class _ITapeRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Tape.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_storagegateway.ITapeRef"

    @builtins.property
    @jsii.member(jsii_name="tapeRef")
    def tape_ref(self) -> "TapeReference":
        '''(experimental) A reference to a Tape resource.

        :stability: experimental
        '''
        return typing.cast("TapeReference", jsii.get(self, "tapeRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITapeRef).__jsii_proxy_class__ = lambda : _ITapeRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.IVolumeRef")
class IVolumeRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Volume.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="volumeRef")
    def volume_ref(self) -> "VolumeReference":
        '''(experimental) A reference to a Volume resource.

        :stability: experimental
        '''
        ...


class _IVolumeRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Volume.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_storagegateway.IVolumeRef"

    @builtins.property
    @jsii.member(jsii_name="volumeRef")
    def volume_ref(self) -> "VolumeReference":
        '''(experimental) A reference to a Volume resource.

        :stability: experimental
        '''
        return typing.cast("VolumeReference", jsii.get(self, "volumeRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVolumeRef).__jsii_proxy_class__ = lambda : _IVolumeRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.NFSFileShareReference",
    jsii_struct_bases=[],
    name_mapping={"file_share_arn": "fileShareArn"},
)
class NFSFileShareReference:
    def __init__(self, *, file_share_arn: builtins.str) -> None:
        '''A reference to a NFSFileShare resource.

        :param file_share_arn: The FileShareARN of the NFSFileShare resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_storagegateway as interfaces_storagegateway
            
            n_fs_file_share_reference = interfaces_storagegateway.NFSFileShareReference(
                file_share_arn="fileShareArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a9fdf3e97ceda0f80f4a80a4404d1cf3950112c471d37bd7f9fa4e896e458cfc)
            check_type(argname="argument file_share_arn", value=file_share_arn, expected_type=type_hints["file_share_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_share_arn": file_share_arn,
        }

    @builtins.property
    def file_share_arn(self) -> builtins.str:
        '''The FileShareARN of the NFSFileShare resource.'''
        result = self._values.get("file_share_arn")
        assert result is not None, "Required property 'file_share_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NFSFileShareReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.SMBFileShareReference",
    jsii_struct_bases=[],
    name_mapping={"file_share_arn": "fileShareArn"},
)
class SMBFileShareReference:
    def __init__(self, *, file_share_arn: builtins.str) -> None:
        '''A reference to a SMBFileShare resource.

        :param file_share_arn: The FileShareARN of the SMBFileShare resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_storagegateway as interfaces_storagegateway
            
            s_mb_file_share_reference = interfaces_storagegateway.SMBFileShareReference(
                file_share_arn="fileShareArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3b751ab17ed1eedd1bbad6367298ff48b93b36a2c1244811851a0f55e6cd5335)
            check_type(argname="argument file_share_arn", value=file_share_arn, expected_type=type_hints["file_share_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_share_arn": file_share_arn,
        }

    @builtins.property
    def file_share_arn(self) -> builtins.str:
        '''The FileShareARN of the SMBFileShare resource.'''
        result = self._values.get("file_share_arn")
        assert result is not None, "Required property 'file_share_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SMBFileShareReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.TapePoolReference",
    jsii_struct_bases=[],
    name_mapping={"pool_arn": "poolArn", "pool_id": "poolId"},
)
class TapePoolReference:
    def __init__(self, *, pool_arn: builtins.str, pool_id: builtins.str) -> None:
        '''A reference to a TapePool resource.

        :param pool_arn: The PoolARN of the TapePool resource.
        :param pool_id: The PoolId of the TapePool resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_storagegateway as interfaces_storagegateway
            
            tape_pool_reference = interfaces_storagegateway.TapePoolReference(
                pool_arn="poolArn",
                pool_id="poolId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__931a079c099cafcf7c3658f645d8e30f357c406d91c831ab4fc86f2ae8c9fdce)
            check_type(argname="argument pool_arn", value=pool_arn, expected_type=type_hints["pool_arn"])
            check_type(argname="argument pool_id", value=pool_id, expected_type=type_hints["pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pool_arn": pool_arn,
            "pool_id": pool_id,
        }

    @builtins.property
    def pool_arn(self) -> builtins.str:
        '''The PoolARN of the TapePool resource.'''
        result = self._values.get("pool_arn")
        assert result is not None, "Required property 'pool_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool_id(self) -> builtins.str:
        '''The PoolId of the TapePool resource.'''
        result = self._values.get("pool_id")
        assert result is not None, "Required property 'pool_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TapePoolReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.TapeReference",
    jsii_struct_bases=[],
    name_mapping={"tape_arn": "tapeArn"},
)
class TapeReference:
    def __init__(self, *, tape_arn: builtins.str) -> None:
        '''A reference to a Tape resource.

        :param tape_arn: The TapeARN of the Tape resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_storagegateway as interfaces_storagegateway
            
            tape_reference = interfaces_storagegateway.TapeReference(
                tape_arn="tapeArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c9f0711496041eef9374207d243de9b8c5298ca999dd19031e3b54759c5c4306)
            check_type(argname="argument tape_arn", value=tape_arn, expected_type=type_hints["tape_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tape_arn": tape_arn,
        }

    @builtins.property
    def tape_arn(self) -> builtins.str:
        '''The TapeARN of the Tape resource.'''
        result = self._values.get("tape_arn")
        assert result is not None, "Required property 'tape_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TapeReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_storagegateway.VolumeReference",
    jsii_struct_bases=[],
    name_mapping={"volume_arn": "volumeArn"},
)
class VolumeReference:
    def __init__(self, *, volume_arn: builtins.str) -> None:
        '''A reference to a Volume resource.

        :param volume_arn: The VolumeARN of the Volume resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_storagegateway as interfaces_storagegateway
            
            volume_reference = interfaces_storagegateway.VolumeReference(
                volume_arn="volumeArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fa56affb5b28498dfa94bfc6e9e66be39cd6b3647aaa44b547b63aa80f8b6918)
            check_type(argname="argument volume_arn", value=volume_arn, expected_type=type_hints["volume_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "volume_arn": volume_arn,
        }

    @builtins.property
    def volume_arn(self) -> builtins.str:
        '''The VolumeARN of the Volume resource.'''
        result = self._values.get("volume_arn")
        assert result is not None, "Required property 'volume_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VolumeReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "INFSFileShareRef",
    "ISMBFileShareRef",
    "ITapePoolRef",
    "ITapeRef",
    "IVolumeRef",
    "NFSFileShareReference",
    "SMBFileShareReference",
    "TapePoolReference",
    "TapeReference",
    "VolumeReference",
]

publication.publish()

def _typecheckingstub__a9fdf3e97ceda0f80f4a80a4404d1cf3950112c471d37bd7f9fa4e896e458cfc(
    *,
    file_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b751ab17ed1eedd1bbad6367298ff48b93b36a2c1244811851a0f55e6cd5335(
    *,
    file_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931a079c099cafcf7c3658f645d8e30f357c406d91c831ab4fc86f2ae8c9fdce(
    *,
    pool_arn: builtins.str,
    pool_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f0711496041eef9374207d243de9b8c5298ca999dd19031e3b54759c5c4306(
    *,
    tape_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa56affb5b28498dfa94bfc6e9e66be39cd6b3647aaa44b547b63aa80f8b6918(
    *,
    volume_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [INFSFileShareRef, ISMBFileShareRef, ITapePoolRef, ITapeRef, IVolumeRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
