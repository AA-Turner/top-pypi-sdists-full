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

import aws_cdk.aws_autoscaling as _aws_cdk_aws_autoscaling_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_eks as _aws_cdk_aws_eks_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8
from ..authentication import (
    IAwsManagedMicrosoftAdParameters as _IAwsManagedMicrosoftAdParameters_42a8ccd6
)
from ..storage import IFSxWindowsParameters as _IFSxWindowsParameters_64d66ceb


class DomainWindowsNode(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skylight.compute.DomainWindowsNode",
):
    '''A Domain Windows Node represents one Windows EC2 instance configured with Active Directory.

    The DomainWindowsNode can be customized to different instance sizes and additional permissions set just like any other EC2 Instance.
    You can use this construct to run elevated domain tasks with domain permissions or run your application in a single instance setup.

    The machine will be joined to the provided Active Directory domain using a custom CloudFormation bootstrap that will wait until the required reboot to join the domain. Then it will register the machine in SSM and pull tasks from the SSM State manager.

    You can send tasks to that machine using the provided methods: runPsCommands() and runPSwithDomainAdmin()
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: "IDomainWindowsNodeProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0723826ec226714efad07703584860acdcc8ae6be920ce9c2986ff220667933c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="openRDP")
    def open_rdp(self, ipaddress: builtins.str) -> None:
        '''Open the security group of the Node Node to specific IP address on port 3389 i.e: openRDP("1.1.1.1/32").

        :param ipaddress: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0f7861658fc9f85fcd45edd5607316a5f2d10d5006e84bdd58205ea52d49556)
            check_type(argname="argument ipaddress", value=ipaddress, expected_type=type_hints["ipaddress"])
        return typing.cast(None, jsii.invoke(self, "openRDP", [ipaddress]))

    @jsii.member(jsii_name="runPsCommands")
    def run_ps_commands(
        self,
        ps_commands: typing.Sequence[builtins.str],
        id: builtins.str,
    ) -> None:
        '''Running PowerShell scripts on the Node with SSM Document.

        i.e: runPsCommands(["Write-host 'Hello world'", "Write-host 'Second command'"], "myScript")

        :param ps_commands: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b193f6e30b006bb543a5067d91641d3715cb780203489578a7aee6bd2ccac2c1)
            check_type(argname="argument ps_commands", value=ps_commands, expected_type=type_hints["ps_commands"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(None, jsii.invoke(self, "runPsCommands", [ps_commands, id]))

    @jsii.member(jsii_name="runPSwithDomainAdmin")
    def run_p_swith_domain_admin(
        self,
        ps_commands: typing.Sequence[builtins.str],
        id: builtins.str,
    ) -> None:
        '''Running PowerShell scripts on the Node with SSM Document with Domain Admin (Using the Secret used to join the machine to the domain) i.e: runPsCommands(["Write-host 'Hello world'", "Write-host 'Second command'"], "myScript") The provided psCommands will be stored in C:\\Scripts and will be run with scheduled task with Domain Admin rights.

        :param ps_commands: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913d08e9e1a9726b5638c93b41af02b4e40f2f18f0484b43b0eecbdb24e8338d)
            check_type(argname="argument ps_commands", value=ps_commands, expected_type=type_hints["ps_commands"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(None, jsii.invoke(self, "runPSwithDomainAdmin", [ps_commands, id]))

    @jsii.member(jsii_name="runShellCommands")
    def run_shell_commands(
        self,
        shell_commands: typing.Sequence[builtins.str],
        id: builtins.str,
    ) -> None:
        '''Running bash scripts on the Node with SSM Document.

        i.e: runPsCommands(["echo 'hello world'", "echo 'Second command'"], "myScript")

        :param shell_commands: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd981a6b6955258987a85d238e2828b669b29f50850e5c695d59437e9e2fec5)
            check_type(argname="argument shell_commands", value=shell_commands, expected_type=type_hints["shell_commands"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(None, jsii.invoke(self, "runShellCommands", [shell_commands, id]))

    @jsii.member(jsii_name="startInstance")
    def start_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "startInstance", []))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> _aws_cdk_aws_ec2_ceddda9d.Instance:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Instance, jsii.get(self, "instance"))

    @builtins.property
    @jsii.member(jsii_name="nodeRole")
    def node_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "nodeRole"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="passwordObject")
    def password_object(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], jsii.get(self, "passwordObject"))


@jsii.interface(jsii_type="cdk-skylight.compute.IDomainWindowsNodeProps")
class IDomainWindowsNodeProps(typing_extensions.Protocol):
    '''The properties of an DomainWindowsNodeProps, requires Active Directory parameter to read the Secret to join the domain Default setting: Domain joined, m5.2xlarge, latest windows, Managed by SSM.'''

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC to use.'''
        ...

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="amiName")
    def ami_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AMI to search in SSM (ec2.LookupNodeImage) supports Regex.

        :default: - 'Windows_Server-2022-English-Full'
        '''
        ...

    @ami_name.setter
    def ami_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        ...

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="iamManagedPoliciesList")
    def iam_managed_policies_list(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]]:
        '''IAM Instance role permissions.

        :default: - 'AmazonSSMManagedInstanceCore, AmazonSSMDirectoryServiceAccess'.
        '''
        ...

    @iam_managed_policies_list.setter
    def iam_managed_policies_list(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The EC2 Instance type to use.

        :default: - 'm5.2xlarge'.
        '''
        ...

    @instance_type.setter
    def instance_type(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="passwordObject")
    def password_object(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        ...

    @password_object.setter
    def password_object(
        self,
        value: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="usePrivateSubnet")
    def use_private_subnet(self) -> typing.Optional[builtins.bool]:
        '''Choose if to launch the instance in Private or in Public subnet Private = Subnet that routes to the internet, but not vice versa.

        Public = Subnet that routes to the internet and vice versa.

        :default: - Private.
        '''
        ...

    @use_private_subnet.setter
    def use_private_subnet(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Specific UserData to use.

        The UserData may still be mutated after creation.

        :default: - 'undefined'
        '''
        ...

    @user_data.setter
    def user_data(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="windowsMachine")
    def windows_machine(self) -> typing.Optional[builtins.bool]:
        '''
        :default: - 'true'
        '''
        ...

    @windows_machine.setter
    def windows_machine(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IDomainWindowsNodePropsProxy:
    '''The properties of an DomainWindowsNodeProps, requires Active Directory parameter to read the Secret to join the domain Default setting: Domain joined, m5.2xlarge, latest windows, Managed by SSM.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-skylight.compute.IDomainWindowsNodeProps"

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC to use.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c22d39c7cd55077d174fd589cca49e2b82d0b70798af295b911e77bf1085c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="amiName")
    def ami_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AMI to search in SSM (ec2.LookupNodeImage) supports Regex.

        :default: - 'Windows_Server-2022-English-Full'
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amiName"))

    @ami_name.setter
    def ami_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344c705449f965ea62ed119d39e62397abf8646f3dd25731c577756c567f683f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amiName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a6aaacc17fd1c844481a123fdbe51ef7ab9a9d19217159c9677f45091bb680a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamManagedPoliciesList")
    def iam_managed_policies_list(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]]:
        '''IAM Instance role permissions.

        :default: - 'AmazonSSMManagedInstanceCore, AmazonSSMDirectoryServiceAccess'.
        '''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]], jsii.get(self, "iamManagedPoliciesList"))

    @iam_managed_policies_list.setter
    def iam_managed_policies_list(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132d53d035da5e464c604bc56ff62b28983ca26aec122a2efdd769263176b7e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamManagedPoliciesList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The EC2 Instance type to use.

        :default: - 'm5.2xlarge'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf82f28c86ccb1c793a3704c00f967c596a04495a55d624fd0cd2dd04da5db4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordObject")
    def password_object(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], jsii.get(self, "passwordObject"))

    @password_object.setter
    def password_object(
        self,
        value: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47e0fc9300c397f8e30bf2ec20bce4a813e7b7dee0394eb3fc3a6e461a498dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordObject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usePrivateSubnet")
    def use_private_subnet(self) -> typing.Optional[builtins.bool]:
        '''Choose if to launch the instance in Private or in Public subnet Private = Subnet that routes to the internet, but not vice versa.

        Public = Subnet that routes to the internet and vice versa.

        :default: - Private.
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "usePrivateSubnet"))

    @use_private_subnet.setter
    def use_private_subnet(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f00a82264f4db368a86f8f03c4d6f7053df4d39e1ed6d3ad9da5599669a2ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usePrivateSubnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Specific UserData to use.

        The UserData may still be mutated after creation.

        :default: - 'undefined'
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userData"))

    @user_data.setter
    def user_data(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f9c40149129ad594e375343a82eedd2bb5326bd212e49082515ab4a32d7a1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowsMachine")
    def windows_machine(self) -> typing.Optional[builtins.bool]:
        '''
        :default: - 'true'
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "windowsMachine"))

    @windows_machine.setter
    def windows_machine(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ad4a3446e9569cbc72fec98131aabca5cfd328e7d58d4e76f0e80e73ba2925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowsMachine", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDomainWindowsNodeProps).__jsii_proxy_class__ = lambda : _IDomainWindowsNodePropsProxy


@jsii.interface(jsii_type="cdk-skylight.compute.IRuntimeNodes")
class IRuntimeNodes(typing_extensions.Protocol):
    @jsii.member(jsii_name="addAdDependency")
    def add_ad_dependency(
        self,
        ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
    ) -> None:
        '''Method to configure the Nodes to part of AD Domain Secret: The secrets manager secret to use must be in format: '{Domain: <domain.name>, UserID: 'Admin', Password: ''}' (From cdk-skylight.AwsManagedMicrosoftAdR53 Object).

        :param ad_parameters_store: -
        '''
        ...

    @jsii.member(jsii_name="addEKSDependency")
    def add_eks_dependency(
        self,
        eks_cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    ) -> None:
        '''Method to add the nodes to specific Cluster.

        :param eks_cluster: -
        '''
        ...

    @jsii.member(jsii_name="addLocalCredFile")
    def add_local_cred_file(
        self,
        ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
        ad_group_name: builtins.str,
        account_name: builtins.str,
    ) -> None:
        '''Method to add support for LocalCredFile .

        :param ad_parameters_store: -
        :param ad_group_name: -
        :param account_name: -
        '''
        ...

    @jsii.member(jsii_name="addStorageDependency")
    def add_storage_dependency(
        self,
        ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
        fsx_parameters_store: _IFSxWindowsParameters_64d66ceb,
        folder_name: builtins.str,
    ) -> None:
        '''Method to configure persistent storage dependency to the hosts by using Global Mapping.

        :param ad_parameters_store: -
        :param fsx_parameters_store: -
        :param folder_name: -
        '''
        ...

    @jsii.member(jsii_name="addUserData")
    def add_user_data(self, *commands: builtins.str) -> None:
        '''Method to add userData to the nodes.

        :param commands: -
        '''
        ...


class _IRuntimeNodesProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-skylight.compute.IRuntimeNodes"

    @jsii.member(jsii_name="addAdDependency")
    def add_ad_dependency(
        self,
        ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
    ) -> None:
        '''Method to configure the Nodes to part of AD Domain Secret: The secrets manager secret to use must be in format: '{Domain: <domain.name>, UserID: 'Admin', Password: ''}' (From cdk-skylight.AwsManagedMicrosoftAdR53 Object).

        :param ad_parameters_store: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a834eaf06878a4f5e6a9a1914830a72e5ef9d290e6775013db0cea8cde22ce1a)
            check_type(argname="argument ad_parameters_store", value=ad_parameters_store, expected_type=type_hints["ad_parameters_store"])
        return typing.cast(None, jsii.invoke(self, "addAdDependency", [ad_parameters_store]))

    @jsii.member(jsii_name="addEKSDependency")
    def add_eks_dependency(
        self,
        eks_cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    ) -> None:
        '''Method to add the nodes to specific Cluster.

        :param eks_cluster: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1fbfc6e4de58691982271e1c325c55050db3e7d14d9131b1ee28125c98bd42)
            check_type(argname="argument eks_cluster", value=eks_cluster, expected_type=type_hints["eks_cluster"])
        return typing.cast(None, jsii.invoke(self, "addEKSDependency", [eks_cluster]))

    @jsii.member(jsii_name="addLocalCredFile")
    def add_local_cred_file(
        self,
        ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
        ad_group_name: builtins.str,
        account_name: builtins.str,
    ) -> None:
        '''Method to add support for LocalCredFile .

        :param ad_parameters_store: -
        :param ad_group_name: -
        :param account_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078388c1df4c9faa0aacbe00c850eeb23953ed1be4b303f29b8ccaaac702e271)
            check_type(argname="argument ad_parameters_store", value=ad_parameters_store, expected_type=type_hints["ad_parameters_store"])
            check_type(argname="argument ad_group_name", value=ad_group_name, expected_type=type_hints["ad_group_name"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
        return typing.cast(None, jsii.invoke(self, "addLocalCredFile", [ad_parameters_store, ad_group_name, account_name]))

    @jsii.member(jsii_name="addStorageDependency")
    def add_storage_dependency(
        self,
        ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
        fsx_parameters_store: _IFSxWindowsParameters_64d66ceb,
        folder_name: builtins.str,
    ) -> None:
        '''Method to configure persistent storage dependency to the hosts by using Global Mapping.

        :param ad_parameters_store: -
        :param fsx_parameters_store: -
        :param folder_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1b076ea89348e9cb2d6c8354f86f66c4836dd6a1f39dc75b0982a9933c2c8d)
            check_type(argname="argument ad_parameters_store", value=ad_parameters_store, expected_type=type_hints["ad_parameters_store"])
            check_type(argname="argument fsx_parameters_store", value=fsx_parameters_store, expected_type=type_hints["fsx_parameters_store"])
            check_type(argname="argument folder_name", value=folder_name, expected_type=type_hints["folder_name"])
        return typing.cast(None, jsii.invoke(self, "addStorageDependency", [ad_parameters_store, fsx_parameters_store, folder_name]))

    @jsii.member(jsii_name="addUserData")
    def add_user_data(self, *commands: builtins.str) -> None:
        '''Method to add userData to the nodes.

        :param commands: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893e9079b29a73bbc4263064393fcbe2aed69c9dd2632e4dec870caf0607d166)
            check_type(argname="argument commands", value=commands, expected_type=typing.Tuple[type_hints["commands"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addUserData", [*commands]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuntimeNodes).__jsii_proxy_class__ = lambda : _IRuntimeNodesProxy


@jsii.interface(jsii_type="cdk-skylight.compute.IWindowsEKSClusterParameters")
class IWindowsEKSClusterParameters(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="clusterNamePointer")
    def cluster_name_pointer(self) -> typing.Optional[builtins.str]:
        '''The name of the SSM Object that contains the EKS Cluster name.

        :default: - 'windows-eks-cluster-name'.
        '''
        ...

    @cluster_name_pointer.setter
    def cluster_name_pointer(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The SSM namespace to read/write parameters to.

        :default: - 'cdk-skylight/compute/eks'.
        '''
        ...

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IWindowsEKSClusterParametersProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-skylight.compute.IWindowsEKSClusterParameters"

    @builtins.property
    @jsii.member(jsii_name="clusterNamePointer")
    def cluster_name_pointer(self) -> typing.Optional[builtins.str]:
        '''The name of the SSM Object that contains the EKS Cluster name.

        :default: - 'windows-eks-cluster-name'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNamePointer"))

    @cluster_name_pointer.setter
    def cluster_name_pointer(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5054eaa425fd92627bd91151ef07393466c3dbe9238dd69e28e3926f5f2fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterNamePointer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The SSM namespace to read/write parameters to.

        :default: - 'cdk-skylight/compute/eks'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58bb5f886468c46ef9c1582d735c94bc9b2fa23897cf05c415b589267f34895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWindowsEKSClusterParameters).__jsii_proxy_class__ = lambda : _IWindowsEKSClusterParametersProxy


@jsii.interface(jsii_type="cdk-skylight.compute.IWindowsEKSClusterProps")
class IWindowsEKSClusterProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        ...

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="eksSsmParameters")
    def eks_ssm_parameters(self) -> typing.Optional[IWindowsEKSClusterParameters]:
        '''The Windows EKS Cluster parameters.

        :default: - 'No default'.
        '''
        ...

    @eks_ssm_parameters.setter
    def eks_ssm_parameters(
        self,
        value: typing.Optional[IWindowsEKSClusterParameters],
    ) -> None:
        ...


class _IWindowsEKSClusterPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-skylight.compute.IWindowsEKSClusterProps"

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f211b4c19712bdb4a6d7a29019fa09950835b89f01126704df57ce36713553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eksSsmParameters")
    def eks_ssm_parameters(self) -> typing.Optional[IWindowsEKSClusterParameters]:
        '''The Windows EKS Cluster parameters.

        :default: - 'No default'.
        '''
        return typing.cast(typing.Optional[IWindowsEKSClusterParameters], jsii.get(self, "eksSsmParameters"))

    @eks_ssm_parameters.setter
    def eks_ssm_parameters(
        self,
        value: typing.Optional[IWindowsEKSClusterParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00d439014c6c371ad776c09d0fdced85e609903fd39e83911431f4e72ecc6d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eksSsmParameters", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWindowsEKSClusterProps).__jsii_proxy_class__ = lambda : _IWindowsEKSClusterPropsProxy


@jsii.interface(jsii_type="cdk-skylight.compute.IWindowsEKSNodesProps")
class IWindowsEKSNodesProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        ...

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''The instance to use.

        :default: - 'm5.large'.
        '''
        ...

    @instance_type.setter
    def instance_type(
        self,
        value: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The SSM namespace to save parameters to.

        :default: - 'cdk-skylight'.
        '''
        ...

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IWindowsEKSNodesPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-skylight.compute.IWindowsEKSNodesProps"

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56dbb99d18698dfa226d8b35d99868e185d6a52825458a74098bf15353fa00b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''The instance to use.

        :default: - 'm5.large'.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(
        self,
        value: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8210a441ad51091dce1431dca60814f7976b032d800dd7a653d59f94382ad4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The SSM namespace to save parameters to.

        :default: - 'cdk-skylight'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8ef7b2140a2294aac3ad6da3edf17d25e72e124a4f650a6c2a7a40ff09fb9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWindowsEKSNodesProps).__jsii_proxy_class__ = lambda : _IWindowsEKSNodesPropsProxy


class WindowsEKSCluster(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skylight.compute.WindowsEKSCluster",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: IWindowsEKSClusterProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74797b142db6c4aad1f5438b187ffbe74c839389841972bdf9748e4a2a19e3da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="eksCluster")
    def eks_cluster(self) -> _aws_cdk_aws_eks_ceddda9d.Cluster:
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.Cluster, jsii.get(self, "eksCluster"))


@jsii.implements(IRuntimeNodes)
class WindowsEKSNodes(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skylight.compute.WindowsEKSNodes",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: IWindowsEKSNodesProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82615b17568ec9419efc68aa47f192454e4b747f7de0ab9534673d0ca116d72)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addAdDependency")
    def add_ad_dependency(
        self,
        ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
    ) -> None:
        '''Method to configure the Nodes to part of AD Domain Secret: The secrets manager secret to use must be in format: '{Domain: <domain.name>, UserID: 'Admin', Password: ''}' (From cdk-skylight.AwsManagedMicrosoftAdR53 Object).

        :param ad_parameters_store: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b0b4f069bc74a43f7cae5c33744b97e99afa754bc2d0f7a8fc67b55b3b56676)
            check_type(argname="argument ad_parameters_store", value=ad_parameters_store, expected_type=type_hints["ad_parameters_store"])
        return typing.cast(None, jsii.invoke(self, "addAdDependency", [ad_parameters_store]))

    @jsii.member(jsii_name="addEKSDependency")
    def add_eks_dependency(
        self,
        eks_cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    ) -> None:
        '''Method to add the nodes to specific Cluster.

        :param eks_cluster: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3f6b5ddf693001f8b6fbe1c2461fee357fddb7f97914f9128477241fc54e73)
            check_type(argname="argument eks_cluster", value=eks_cluster, expected_type=type_hints["eks_cluster"])
        return typing.cast(None, jsii.invoke(self, "addEKSDependency", [eks_cluster]))

    @jsii.member(jsii_name="addLocalCredFile")
    def add_local_cred_file(
        self,
        ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
        ad_group_name: builtins.str,
        account_name: builtins.str,
    ) -> None:
        '''Method to add support for LocalCredFile .

        :param ad_parameters_store: -
        :param ad_group_name: -
        :param account_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea2bda9b7a63bfe136c7c165d8377ea97eaa0c45e2dc3fdd872541422cd95cd)
            check_type(argname="argument ad_parameters_store", value=ad_parameters_store, expected_type=type_hints["ad_parameters_store"])
            check_type(argname="argument ad_group_name", value=ad_group_name, expected_type=type_hints["ad_group_name"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
        return typing.cast(None, jsii.invoke(self, "addLocalCredFile", [ad_parameters_store, ad_group_name, account_name]))

    @jsii.member(jsii_name="addStorageDependency")
    def add_storage_dependency(
        self,
        ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
        fsx_parameters_store: _IFSxWindowsParameters_64d66ceb,
        folder_name: builtins.str,
    ) -> None:
        '''Method to configure persistent storage dependency to the hosts by using Global Mapping.

        :param ad_parameters_store: -
        :param fsx_parameters_store: -
        :param folder_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3ba3aea0907d62a26144160d9ea986681a7e609c79d967500beb72cc4475d2)
            check_type(argname="argument ad_parameters_store", value=ad_parameters_store, expected_type=type_hints["ad_parameters_store"])
            check_type(argname="argument fsx_parameters_store", value=fsx_parameters_store, expected_type=type_hints["fsx_parameters_store"])
            check_type(argname="argument folder_name", value=folder_name, expected_type=type_hints["folder_name"])
        return typing.cast(None, jsii.invoke(self, "addStorageDependency", [ad_parameters_store, fsx_parameters_store, folder_name]))

    @jsii.member(jsii_name="addUserData")
    def add_user_data(self, *commands: builtins.str) -> None:
        '''Method to add userData to the nodes.

        :param commands: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809795bad937116f874523db90a7cb85fbd14a8d35d279a54052d4d07c4626b1)
            check_type(argname="argument commands", value=commands, expected_type=typing.Tuple[type_hints["commands"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addUserData", [*commands]))

    @jsii.member(jsii_name="gMSAWebHookAutoInstall")
    def g_msa_web_hook_auto_install(
        self,
        eks_cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
        private_signer_name: builtins.str,
        awsaccountid: builtins.str,
        awsregion: builtins.str,
    ) -> None:
        '''
        :param eks_cluster: -
        :param private_signer_name: -
        :param awsaccountid: -
        :param awsregion: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e5928e5437b29fb6c9708891ece6b3ab102d81e268baf9f2cfbc30c3b57bb9)
            check_type(argname="argument eks_cluster", value=eks_cluster, expected_type=type_hints["eks_cluster"])
            check_type(argname="argument private_signer_name", value=private_signer_name, expected_type=type_hints["private_signer_name"])
            check_type(argname="argument awsaccountid", value=awsaccountid, expected_type=type_hints["awsaccountid"])
            check_type(argname="argument awsregion", value=awsregion, expected_type=type_hints["awsregion"])
        return typing.cast(None, jsii.invoke(self, "gMSAWebHookAutoInstall", [eks_cluster, private_signer_name, awsaccountid, awsregion]))

    @jsii.member(jsii_name="runPowerShellSSMDocument")
    def run_power_shell_ssm_document(
        self,
        name: builtins.str,
        commands: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: -
        :param commands: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c2314c8fe204c6e04eb4c6925420499bdbf026813ac55761939df87809029e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
        return typing.cast(None, jsii.invoke(self, "runPowerShellSSMDocument", [name, commands]))

    @builtins.property
    @jsii.member(jsii_name="asg")
    def asg(self) -> _aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup:
        return typing.cast(_aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup, jsii.get(self, "asg"))

    @builtins.property
    @jsii.member(jsii_name="asgResource")
    def asg_resource(self) -> _aws_cdk_aws_autoscaling_ceddda9d.CfnAutoScalingGroup:
        return typing.cast(_aws_cdk_aws_autoscaling_ceddda9d.CfnAutoScalingGroup, jsii.get(self, "asgResource"))

    @builtins.property
    @jsii.member(jsii_name="nodesSg")
    def nodes_sg(self) -> _aws_cdk_aws_ec2_ceddda9d.SecurityGroup:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SecurityGroup, jsii.get(self, "nodesSg"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="windowsWorkersRole")
    def windows_workers_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "windowsWorkersRole"))


__all__ = [
    "DomainWindowsNode",
    "IDomainWindowsNodeProps",
    "IRuntimeNodes",
    "IWindowsEKSClusterParameters",
    "IWindowsEKSClusterProps",
    "IWindowsEKSNodesProps",
    "WindowsEKSCluster",
    "WindowsEKSNodes",
]

publication.publish()

def _typecheckingstub__0723826ec226714efad07703584860acdcc8ae6be920ce9c2986ff220667933c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IDomainWindowsNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f7861658fc9f85fcd45edd5607316a5f2d10d5006e84bdd58205ea52d49556(
    ipaddress: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b193f6e30b006bb543a5067d91641d3715cb780203489578a7aee6bd2ccac2c1(
    ps_commands: typing.Sequence[builtins.str],
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913d08e9e1a9726b5638c93b41af02b4e40f2f18f0484b43b0eecbdb24e8338d(
    ps_commands: typing.Sequence[builtins.str],
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd981a6b6955258987a85d238e2828b669b29f50850e5c695d59437e9e2fec5(
    shell_commands: typing.Sequence[builtins.str],
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c22d39c7cd55077d174fd589cca49e2b82d0b70798af295b911e77bf1085c06(
    value: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344c705449f965ea62ed119d39e62397abf8646f3dd25731c577756c567f683f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6aaacc17fd1c844481a123fdbe51ef7ab9a9d19217159c9677f45091bb680a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132d53d035da5e464c604bc56ff62b28983ca26aec122a2efdd769263176b7e6(
    value: typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf82f28c86ccb1c793a3704c00f967c596a04495a55d624fd0cd2dd04da5db4f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47e0fc9300c397f8e30bf2ec20bce4a813e7b7dee0394eb3fc3a6e461a498dd(
    value: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f00a82264f4db368a86f8f03c4d6f7053df4d39e1ed6d3ad9da5599669a2ec3(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9c40149129ad594e375343a82eedd2bb5326bd212e49082515ab4a32d7a1c3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ad4a3446e9569cbc72fec98131aabca5cfd328e7d58d4e76f0e80e73ba2925(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a834eaf06878a4f5e6a9a1914830a72e5ef9d290e6775013db0cea8cde22ce1a(
    ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1fbfc6e4de58691982271e1c325c55050db3e7d14d9131b1ee28125c98bd42(
    eks_cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078388c1df4c9faa0aacbe00c850eeb23953ed1be4b303f29b8ccaaac702e271(
    ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
    ad_group_name: builtins.str,
    account_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1b076ea89348e9cb2d6c8354f86f66c4836dd6a1f39dc75b0982a9933c2c8d(
    ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
    fsx_parameters_store: _IFSxWindowsParameters_64d66ceb,
    folder_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893e9079b29a73bbc4263064393fcbe2aed69c9dd2632e4dec870caf0607d166(
    *commands: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5054eaa425fd92627bd91151ef07393466c3dbe9238dd69e28e3926f5f2fe3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58bb5f886468c46ef9c1582d735c94bc9b2fa23897cf05c415b589267f34895(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f211b4c19712bdb4a6d7a29019fa09950835b89f01126704df57ce36713553(
    value: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00d439014c6c371ad776c09d0fdced85e609903fd39e83911431f4e72ecc6d3(
    value: typing.Optional[IWindowsEKSClusterParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56dbb99d18698dfa226d8b35d99868e185d6a52825458a74098bf15353fa00b0(
    value: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8210a441ad51091dce1431dca60814f7976b032d800dd7a653d59f94382ad4a(
    value: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8ef7b2140a2294aac3ad6da3edf17d25e72e124a4f650a6c2a7a40ff09fb9f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74797b142db6c4aad1f5438b187ffbe74c839389841972bdf9748e4a2a19e3da(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IWindowsEKSClusterProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82615b17568ec9419efc68aa47f192454e4b747f7de0ab9534673d0ca116d72(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IWindowsEKSNodesProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0b4f069bc74a43f7cae5c33744b97e99afa754bc2d0f7a8fc67b55b3b56676(
    ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3f6b5ddf693001f8b6fbe1c2461fee357fddb7f97914f9128477241fc54e73(
    eks_cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea2bda9b7a63bfe136c7c165d8377ea97eaa0c45e2dc3fdd872541422cd95cd(
    ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
    ad_group_name: builtins.str,
    account_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3ba3aea0907d62a26144160d9ea986681a7e609c79d967500beb72cc4475d2(
    ad_parameters_store: _IAwsManagedMicrosoftAdParameters_42a8ccd6,
    fsx_parameters_store: _IFSxWindowsParameters_64d66ceb,
    folder_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809795bad937116f874523db90a7cb85fbd14a8d35d279a54052d4d07c4626b1(
    *commands: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e5928e5437b29fb6c9708891ece6b3ab102d81e268baf9f2cfbc30c3b57bb9(
    eks_cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    private_signer_name: builtins.str,
    awsaccountid: builtins.str,
    awsregion: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c2314c8fe204c6e04eb4c6925420499bdbf026813ac55761939df87809029e(
    name: builtins.str,
    commands: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
