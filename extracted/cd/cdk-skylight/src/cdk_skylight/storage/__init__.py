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

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_fsx as _aws_cdk_aws_fsx_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8
from ..compute import DomainWindowsNode as _DomainWindowsNode_bbfd2a18


class FSxWindows(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skylight.storage.FSxWindows",
):
    '''A FSxWindows represents an integration pattern of Amazon FSx and Managed AD in a specific VPC.

    The Construct creates Amazon FSx for Windows
    The construct also creates (optionally) t3.nano machine that is part of the domain that can be used to run admin-tasks (such as createFolder)

    The createFolder() method creates an SMB Folder in the FSx filesystem, using the domain admin user.
    Please note: When calling createFolder() API, a Lambda will be created to start the worker machine (Using AWS-SDK),
    then each command will be scheduled with State Manager, and the instance will be shut down after complete .
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: "IFSxWindowsProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a6983f430694b923385a7ac20bef104b1971c1ba526e73de0f6b0c24251953)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createFolder")
    def create_folder(
        self,
        worker: _DomainWindowsNode_bbfd2a18,
        folder_name: builtins.str,
        secret_name: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param worker: -
        :param folder_name: -
        :param secret_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__929ad6c7747c6dd5cec009f7e9905258671b50c46b067ef7e72e9a6e0d1c1f24)
            check_type(argname="argument worker", value=worker, expected_type=type_hints["worker"])
            check_type(argname="argument folder_name", value=folder_name, expected_type=type_hints["folder_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        return typing.cast(None, jsii.invoke(self, "createFolder", [worker, folder_name, secret_name]))

    @jsii.member(jsii_name="createWorker")
    def create_worker(
        self,
        domain_name: builtins.str,
        domain_password: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> _DomainWindowsNode_bbfd2a18:
        '''
        :param domain_name: -
        :param domain_password: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f84fe7deadf0a16c7232870b2af72719c91be65973444cd8390678db0a7a4e5)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_password", value=domain_password, expected_type=type_hints["domain_password"])
        return typing.cast(_DomainWindowsNode_bbfd2a18, jsii.invoke(self, "createWorker", [domain_name, domain_password]))

    @builtins.property
    @jsii.member(jsii_name="fsxObject")
    def fsx_object(self) -> _aws_cdk_aws_fsx_ceddda9d.CfnFileSystem:
        return typing.cast(_aws_cdk_aws_fsx_ceddda9d.CfnFileSystem, jsii.get(self, "fsxObject"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "IFSxWindowsProps":
        return typing.cast("IFSxWindowsProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="ssmParameters")
    def ssm_parameters(self) -> "IFSxWindowsParameters":
        return typing.cast("IFSxWindowsParameters", jsii.get(self, "ssmParameters"))


@jsii.interface(jsii_type="cdk-skylight.storage.IFSxWindowsParameters")
class IFSxWindowsParameters(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="dnsEndpoint")
    def dns_endpoint(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter to save the FSxEndpoint DNS Endpoint.

        :default: - 'FSxEndpoint-DNS'.
        '''
        ...

    @dns_endpoint.setter
    def dns_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The SSM namespace to read/write parameters to.

        :default: - 'cdk-skylight'.
        '''
        ...

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IFSxWindowsParametersProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-skylight.storage.IFSxWindowsParameters"

    @builtins.property
    @jsii.member(jsii_name="dnsEndpoint")
    def dns_endpoint(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter to save the FSxEndpoint DNS Endpoint.

        :default: - 'FSxEndpoint-DNS'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsEndpoint"))

    @dns_endpoint.setter
    def dns_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7763067499b687db65210f99a88deea09bee48c75204da316be5c83ea3191a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The SSM namespace to read/write parameters to.

        :default: - 'cdk-skylight'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c456ef529597ab426e4f643be78ca1b514b11c72d7a43b3a11c1180277a029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFSxWindowsParameters).__jsii_proxy_class__ = lambda : _IFSxWindowsParametersProxy


@jsii.interface(jsii_type="cdk-skylight.storage.IFSxWindowsProps")
class IFSxWindowsProps(typing_extensions.Protocol):
    '''The properties for the PersistentStorage class.'''

    @builtins.property
    @jsii.member(jsii_name="directoryId")
    def directory_id(self) -> builtins.str:
        ...

    @directory_id.setter
    def directory_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC to use, must have private subnets.'''
        ...

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fileSystemInPrivateSubnet")
    def file_system_in_private_subnet(self) -> typing.Optional[builtins.bool]:
        '''Deploy the Amazon FSx file system in private subnet or public subnet See: https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html.

        :default: - true.
        '''
        ...

    @file_system_in_private_subnet.setter
    def file_system_in_private_subnet(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fileSystemSize")
    def file_system_size(self) -> typing.Optional[jsii.Number]:
        '''The Filesystem size in GB.

        :default:

        -
        200.
        '''
        ...

    @file_system_size.setter
    def file_system_size(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="multiAZ")
    def multi_az(self) -> typing.Optional[builtins.bool]:
        '''Choosing Single-AZ or Multi-AZ file system deployment See: https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html.

        :default: - true.
        '''
        ...

    @multi_az.setter
    def multi_az(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ssmParameters")
    def ssm_parameters(self) -> typing.Optional[IFSxWindowsParameters]:
        ...

    @ssm_parameters.setter
    def ssm_parameters(self, value: typing.Optional[IFSxWindowsParameters]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="throughputMbps")
    def throughput_mbps(self) -> typing.Optional[jsii.Number]:
        '''The Filesystem throughput in MBps.

        :default:

        -
        128.
        '''
        ...

    @throughput_mbps.setter
    def throughput_mbps(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _IFSxWindowsPropsProxy:
    '''The properties for the PersistentStorage class.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-skylight.storage.IFSxWindowsProps"

    @builtins.property
    @jsii.member(jsii_name="directoryId")
    def directory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryId"))

    @directory_id.setter
    def directory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce275a5cda6a731401e3855f3909b75c111d7e318b718353ba1fde1238f3e3fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC to use, must have private subnets.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8038074ec2c8ca27895e3a52988ec90f92c563254c93d29725c65ffbeb56924b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileSystemInPrivateSubnet")
    def file_system_in_private_subnet(self) -> typing.Optional[builtins.bool]:
        '''Deploy the Amazon FSx file system in private subnet or public subnet See: https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html.

        :default: - true.
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "fileSystemInPrivateSubnet"))

    @file_system_in_private_subnet.setter
    def file_system_in_private_subnet(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39542dbd26c248c094ebce179e4a4234b8e02c1e1e8cfadcae24e375e87c181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemInPrivateSubnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileSystemSize")
    def file_system_size(self) -> typing.Optional[jsii.Number]:
        '''The Filesystem size in GB.

        :default:

        -
        200.
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fileSystemSize"))

    @file_system_size.setter
    def file_system_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78c4a57121f56b75824a2c916a282a24ffe140eaa79e6b209619847707c3e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiAZ")
    def multi_az(self) -> typing.Optional[builtins.bool]:
        '''Choosing Single-AZ or Multi-AZ file system deployment See: https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html.

        :default: - true.
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "multiAZ"))

    @multi_az.setter
    def multi_az(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b72af8d89fd8bf0fdc09d66e0e1c5a54f838522817dc27c1161284d76390e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiAZ", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssmParameters")
    def ssm_parameters(self) -> typing.Optional[IFSxWindowsParameters]:
        return typing.cast(typing.Optional[IFSxWindowsParameters], jsii.get(self, "ssmParameters"))

    @ssm_parameters.setter
    def ssm_parameters(self, value: typing.Optional[IFSxWindowsParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e94fd29ab646e1baeae6502dbcce7fecf73bd80789ab76eb7679541ac4f6f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssmParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughputMbps")
    def throughput_mbps(self) -> typing.Optional[jsii.Number]:
        '''The Filesystem throughput in MBps.

        :default:

        -
        128.
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throughputMbps"))

    @throughput_mbps.setter
    def throughput_mbps(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec23e03f5f54f0330e7bc5da6577e64192a5540fcff9711b0a606572e2a9a76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputMbps", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFSxWindowsProps).__jsii_proxy_class__ = lambda : _IFSxWindowsPropsProxy


__all__ = [
    "FSxWindows",
    "IFSxWindowsParameters",
    "IFSxWindowsProps",
]

publication.publish()

def _typecheckingstub__94a6983f430694b923385a7ac20bef104b1971c1ba526e73de0f6b0c24251953(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IFSxWindowsProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929ad6c7747c6dd5cec009f7e9905258671b50c46b067ef7e72e9a6e0d1c1f24(
    worker: _DomainWindowsNode_bbfd2a18,
    folder_name: builtins.str,
    secret_name: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f84fe7deadf0a16c7232870b2af72719c91be65973444cd8390678db0a7a4e5(
    domain_name: builtins.str,
    domain_password: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7763067499b687db65210f99a88deea09bee48c75204da316be5c83ea3191a92(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c456ef529597ab426e4f643be78ca1b514b11c72d7a43b3a11c1180277a029(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce275a5cda6a731401e3855f3909b75c111d7e318b718353ba1fde1238f3e3fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8038074ec2c8ca27895e3a52988ec90f92c563254c93d29725c65ffbeb56924b(
    value: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39542dbd26c248c094ebce179e4a4234b8e02c1e1e8cfadcae24e375e87c181(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78c4a57121f56b75824a2c916a282a24ffe140eaa79e6b209619847707c3e02(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b72af8d89fd8bf0fdc09d66e0e1c5a54f838522817dc27c1161284d76390e03(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e94fd29ab646e1baeae6502dbcce7fecf73bd80789ab76eb7679541ac4f6f4b(
    value: typing.Optional[IFSxWindowsParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec23e03f5f54f0330e7bc5da6577e64192a5540fcff9711b0a606572e2a9a76(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass
